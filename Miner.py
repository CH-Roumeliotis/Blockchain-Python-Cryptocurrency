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
    try:
        tx_list = loadTxList("Txs.dat")
        if verbose: print("Loaded tx_list has " + str(len(tx_list)) + " transactions.")
    except:
        print("No previous transactions. Starting fresh")
        tx_list = []
    head_blocks=[None]
    my_ip, my_port = my_addr
    server = SocketUtils.newServerConnection(my_ip,my_port)
    # Get Transactions from wallets
    while not break_now:
        newTx = SocketUtils.recvObj(server)
        if isinstance(newTx,Transaction.Tx):
            tx_list.append(newTx)
            if verbose: print ("Received transaction")
    if verbose: print ("Saving " + str(len(tx_list)) + " transactions to Txs.dat")
    saveTxList(tx_list,"Txs.dat")
    return False

def nonceFinder(wallet_list, miner_public):
    global break_now
    # add Transactions to new block
    while not break_now:
        newBlock = TxBlock.TxBlock(TxBlock.findLongestBlockchain(head_blocks))
        for tx in tx_list:
            newBlock.addTx(tx)
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
            head_blocks.remove(newBlock.previous)
            head_blocks.append(newBlock)
            # Send new block
            savePrev = newBlock.previous
            newBlock.previous = None
            for ip_addr,port in wallet_list:
                if verbose: print ("Sending to " + ip_addr + ":" + str(port))
                SocketUtils.sendBlock(ip_addr,newBlock,5006)
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
    
    my_pr, my_pu = Signatures.generate_keys()
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
