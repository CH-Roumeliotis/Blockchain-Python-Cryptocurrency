#client


import TxBlock
import Transaction
import Signatures
import pickle
import socket

TCP_PORT = 5005

def sendBlock(ip_addr, block):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip_addr, TCP_PORT))
    data = pickle.dumps(block)
    s.send(data)
    s.close()
    return False

if __name__ == "__main__":
    pr1,pu1 = Signatures.generate_keys()
    pr2,pu2 = Signatures.generate_keys()
    pr3,pu3 = Signatures.generate_keys()
    Tx1 = Transaction.Tx()
    Tx1.add_input(pu1,2.3)
    Tx1.add_output(pu2,1.0)
    Tx1.add_output(pu3,1.1)
    Tx1.signature(pr1)

    Tx2 = Transaction.Tx()
    Tx2.add_input(pu3,2.3)
    Tx2.add_input(pu2,1.0)
    Tx2.add_output(pu1,3.1)
    Tx2.signature(pr2)
    Tx2.signature(pr3)

    B1 = TxBlock.TxBlock(None)
    B1.addTx(Tx1)
    B1.addTx(Tx2)

    sendBlock('localhost', B1)

    sendBlock('localhost', Tx2)
    
    
    
