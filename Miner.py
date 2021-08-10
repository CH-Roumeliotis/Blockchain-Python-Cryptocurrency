#Miner
import SocketUtils
import Transaction
import TxBlock
import Signatures

wallets = ['localhost']
tx_list = []
    
def minerServer(my_ip, wallet_list, my_public):
    server = SocketUtils.newServerConnection(my_ip)
    # Get 2 Txs from wallets
    for i in range(10):
        newTx = SocketUtils.recvObj(server)
        if isinstance(newTx,Transaction.Tx):
            tx_list.append(newTx)
            print ("Received tx")
        if len(tx_list) >= 2:
            break
    # add Txs to new block
    newBlock = TxBlock.TxBlock(None)
    newBlock.addTx(tx_list[0])
    newBlock.addTx(tx_list[1])
    # Compute and add mining reward
    total_in,total_out = newBlock.count_totals()
    mine_reward = Transaction.Tx()
    mine_reward.add_output(my_public, 25.0 + total_in - total_out)
    newBlock.addTx(mine_reward)
    # Find nonce
    for i in range(10):
        print ("Finding Nonce...")
        newBlock.find_nonce()
        if newBlock.good_nonce():
            print ("Good nonce found")
            break
    if not newBlock.good_nonce():
        print ("ERROR. Couldn't find nonce")
        return False
    # Send new block
    for ip_addr in wallet_list:
        print ("Sending to " + ip_addr)
        SocketUtils.sendBlock(ip_addr, newBlock, 5006)
    head_blocks.remove(newBlock.previousBlock)
    head_blocks.append(newBlock)
    return False

my_pr, my_pu = Signatures.generate_keys()
minerServer('localhost', wallets, my_pu)
