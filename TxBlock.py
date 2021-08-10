from BlockChain import RBlock
from Signatures import generate_keys, sign, verify
from Transaction import Tx
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
import pickle
import time

reward = 25.0 #25.0 is our block reward

class TxBlock(RBlock):
    nonce = "AAAAAAA"
    def __init__(self, previous):
        super(TxBlock, self).__init__([], previous)
    def addTx(self, Tx_in):
        self.data.append(Tx_in)
    def __count_totals(self):
        total_in = 0
        total_out = 0
        for tx in self.data:
            for addr,amt in tx.inputs:
                total_in = total_in + amt
            for addr,amt in tx.outputs:
                total_out = total_out + amt
        return total_in, total_out
    def is_Valid(self):
        if not super(TxBlock, self).is_Valid():
            return False
        for tx in self.data:
            if not tx.is_Valid():
                return False
        total_in, total_out = self.__count_totals()
        if total_out - total_in - reward > 0.00000000001:
            return False
        return True
    def good_nonce(self):
        return False
    def find_nonce(self):
        return self.nonce
if __name__ == "__main__":
    pr1, pu1 = generate_keys()
    pr2, pu2 = generate_keys()
    pr3, pu3 = generate_keys()

    Tx1 = Tx()
    Tx1.add_input(pu1, 1)
    Tx1.add_output(pu2, 1)
    Tx1.signature(pr1)

    if Tx1.is_Valid():
        print("Success, Tx is valid")

    message = b"Some text"
    signature = sign(message, pr1)
    print(verify(message, signature, pu1))

    addrFile = open("public.dat", "wb")
#    pu_ser = pu1.public_bytes(
#        encoding=serialization.Encoding.PEM,
#        format=serialization.PublicFormat.SubjectPublicKeyInfo
#    )
    pickle.dump(pu1, addrFile)
    addrFile.close()
    saveFile = open("tx.dat", "wb")
    pickle.dump(Tx1, saveFile)
    saveFile.close()

    loadFile = open("public.dat", "rb")
    new_pu = pickle.load(loadFile)
#    loaded_pu = serialization.load_pem_public_key(
#        new_pu,
#        backend = default_backend()
#    )
    print(verify(message, signature, new_pu))
    loadFile.close()

    loadFile = open("tx.dat", "rb")
    newTx = pickle.load(loadFile)

    if newTx.is_Valid():
        print("Success Loaded tx is valid")
    loadFile.close()

    root = TxBlock(None)
    root.addTx(Tx1)

    Tx2 = Tx()
    Tx2.add_input(pu2, 1.1)
    Tx2.add_output(pu3, 1)
    Tx2.signature(pr2)
    root.addTx(Tx2)

    B1 = TxBlock(root)
    
    Tx3 = Tx()
    Tx3.add_input(pu3, 1.1)
    Tx3.add_output(pu1, 1)
    Tx3.signature(pr3)
    B1.addTx(Tx3)

    Tx4 = Tx()
    Tx4.add_input(pu1, 1)
    Tx4.add_output(pu2, 1)
    Tx4.add_Req_Signatures(pu3)
    Tx4.signature(pr1)
    Tx4.signature(pr3)
    B1.addTx(Tx4)
    start = time.time()
    print(B1.find_nonce())
    elapsed = time.time() - start
    print("Elapsed time:" + str(elapsed) + "s.")
    
    if elapsed < 60:
        print("ERROR, Mining is too fast")
    if B1.good_nonce():
        print("Success, nonce is good")
    else:
        print("ERROR, wrong nonce")

#    B1.is_Valid()
#    root.is_Valid()

    saveFile = open("block.dat", "wb")
    pickle.dump(B1, saveFile)
    saveFile.close()

    loadFile = open("block.dat", "rb")
    load_B1 = pickle.load(loadFile)

    #load_B1.is_Valid

#    print(bytes(str(load_B1.data), 'utf8'))

    for b in [root, B1, load_B1, load_B1.previous]:
        if b.is_Valid():
            print("Success, Valid Block")
        else:
            print("ERROR Block")

    if B1.good_nonce():
        print("Success, nonce is good after save & load")
    else:
        print("ERROR, wrong nonce after save & load")

    B2 = TxBlock(B1)
    Tx5 = Tx()
    Tx5.add_input(pu3, 1)
    Tx5.add_output(pu1, 100)
    Tx5.signature(pr3)
    B2.addTx(Tx5)
#    print(B2.data)
#    print(Tx5.is_Valid())
    load_B1.previous.addTx(Tx4)
    
    for b in [B2, load_B1]:
        if b.is_Valid():
            print("ERROR, block is not verified")
        else:
            print("Succeed, unverified blocks detected")

#Test mining reward
    pr4, pu4 = generate_keys()
    B3 = TxBlock(B2)
    B3.addTx(Tx2)
    B3.addTx(Tx3)
    B3.addTx(Tx4)
    Tx6 = Tx()
    Tx6.add_output(pu4, 25) #miner' s public key
    B3.addTx(Tx6)
    
    if B3.is_Valid():
        print("Success! Wrong Blocks detected")
    else:
        print("ERROR! Block reward fail")

    B4 = TxBlock(B3)
    B4.addTx(Tx2)
    B4.addTx(Tx3)
    B4.addTx(Tx4)
    Tx7 = Tx()
    Tx7.add_output(pu4, 25.2)
    B4.addTx(Tx7)
    
    if B4.is_Valid():
        print("Success! Tx fees succeeds")
    else:
        print("ERROR! Tx fees fail")
        
#Greedy miner
    B5 = TxBlock(B4)
    B5.addTx(Tx2)
    B5.addTx(Tx3)
    B5.addTx(Tx4)
    Tx8 = Tx()
    Tx8.add_output(pu4, 26.2)
    B5.addTx(Tx8)
    
    if not B5.is_Valid():
        print("Success! Greedy miner detected")
    else:
        print("ERROR! Greedy miner not detected")      
