#Miner
import SocketUtils
import Transaction
import TxBlock
import pickle

wallets = [('localhost',5006)]
tx_list = []
head_blocks=[None]
break_now = False
verbose = True

def StopAll():
    global break_now
    break_now = True

def minerServer(my_addr):
    global tx_list
    global break_now
    global head_blocks
    try:
        tx_list = loadTxList("Txs.dat")
        if verbose: print ("Loaded tx_list has " +str(len(tx_list))+" Txs.")
    except:
        print("No previous tx_list found. Starting new")
        tx_list = []         
    my_ip, my_port = my_addr
    server = SocketUtils.newServerConnection(my_ip,my_port)
    # Get Transactions from wallets
    while not break_now:
        newObj = SocketUtils.recvObj(server)
        if isinstance(newObj,Transaction.Tx):
            duplicate = False
            for addr,amt,inx in newObj.inputs:
                for tx in tx_list:
                    for addr2,amt2,inx2 in tx.inputs:
                        if addr2 == addr and inx2 == inx:
                            duplicate = True
            if duplicate: break
            tx_list.append(newObj)
            if verbose:
                print ("Received tx")
            if verbose:
                print ("tx_list contains " + str(len(tx_list)) + " transactions.")
        elif isinstance(newObj,TxBlock.TxBlock):
            print("Received new block")
            TxBlock.processNewBlock(newObj,head_blocks,True)
            for tx in newObj.data:
                if tx in tx_list:
                    tx_list.remove(tx)
        else:
            print ("Received " + str(type(newObj)))
    if verbose: print("Saving " + str(len(tx_list)) + " transactions to Txs.dat")
    saveTxList(tx_list, "Txs.dat")
    return False

def nonceFinder(wallet_list, miner_public):
    global break_now
    global head_blocks
    # add Transactions to new block
    try:
        head_blocks = TxBlock.loadBlocks("AllBlocks.dat")
    except:
        head_blocks = TxBlock.loadBlocks("GenesisBlock.dat")
    while not break_now:
        newBlock = TxBlock.TxBlock(TxBlock.findLongestBlockchain(head_blocks))
        tmp = Transaction.Tx()
        tmp.add_output(miner_public,25.0)
        newBlock.addTx(tmp)
        for tx in tx_list:
            newBlock.addTx(tx)
            if not newBlock.check_size():
                newBlock.removeTx(tx)
                break
            
        newBlock.removeTx(tmp)
        # Compute and add mining reward
        total_in,total_out = newBlock.count_totals()
        mine_reward = Transaction.Tx()
        mine_reward.add_output(miner_public,25.0+total_in-total_out)
        newBlock.addTx(mine_reward)
        # Find nonce
        if verbose: print ("Finding Nonce...")
        newBlock.find_nonce(10000)
        if newBlock.good_nonce():
            if verbose: print ("Good nonce found")
            if not newBlock.previous in head_blocks:
                break
            head_blocks.remove(newBlock.previous)
            head_blocks.append(newBlock)
            # Send new block
            # Send new block
            savePrev = newBlock.previous
            newBlock.previous = None
            for ip_addr,port in wallet_list:
                if verbose: print ("Sending to " + ip_addr + ":" + str(port))
                SocketUtils.sendBlock(ip_addr,newBlock,port)
            newBlock.previous = savePrev
            # Remove used txs from tx_list
            for tx in newBlock.data:
                if tx != mine_reward:
                    tx_list.remove(tx)
    TxBlock.saveBlocks(head_blocks,"AllBlocks.dat")
    return True

def loadTxList(filename):
    fin = open(filename, "rb")
    ret = pickle.load(fin)
    fin.close()
    return ret

def saveTxList(the_list, filename):
    fp = open(filename, "wb")
    pickle.dump(the_list, fp)
    fp.close()
    return True

if __name__ == "__main__":

    import Signatures
    import threading
    import time
    
    my_pr, my_pu = Signatures.loadKeys("private.key","public.key")
    t1 = threading.Thread(target=minerServer, args=(('localhost',5005),))
    t2 = threading.Thread(target=nonceFinder, args=(wallets, my_pu))
    server = SocketUtils.newServerConnection('localhost',5006)
    t1.start()
    t2.start()
    pr1,pu1 = Signatures.generate_keys()
    pr2,pu2 = Signatures.generate_keys()
    pr3,pu3 = Signatures.generate_keys()

    Tx1 = Transaction.Tx()
    Tx2 = Transaction.Tx()

    Tx1.add_input(pu1, 4.0)
    Tx1.add_input(pu2, 1.0)
    Tx1.add_output(pu3, 4.8)
    Tx2.add_input(pu3, 4.0)
    Tx2.add_output(pu2, 4.0)
    Tx2.add_Req_Signatures(pu1)

    Tx1.signature(pr1)
    Tx1.signature(pr2)
    Tx2.signature(pr3)
    Tx2.signature(pr1)

    new_tx_list = [Tx1, Tx2]
    saveTxList(new_tx_list, "Txs.dat")
    new_new_tx_list = loadTxList("Txs.dat")
    

    for tx in new_new_tx_list:
        try:
            SocketUtils.sendBlock('localhost',tx)
            print ("Sent Transaction")
        except:
            print ("ERROR! Connection Fail")

    for i in range(30):
        newBlock = SocketUtils.recvObj(server)
        if newBlock:
            break

    if newBlock.is_Valid():
        print("Success, Block is valid")
    if newBlock.good_nonce():
        print("Success, Nonce is valid")
    for tx in newBlock.data:
        try:
            if tx.inputs[0][0] == pu1 and tx.inputs[0][1] == 4.0:
                print("Tx1 is present")
        except:
            pass
        try:
            if tx.inputs[0][0] == pu3 and tx.inputs[0][1] == 4.0:
                print("Tx2 is present")
        except:
            pass

    time.sleep(20)
    break_now=True
    time.sleep(2)
    server.close()

    t1.join()
    t2.join()

    print("Done!")
