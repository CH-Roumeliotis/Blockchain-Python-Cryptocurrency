from BlockChain import RBlock
from Signatures import generate_keys, sign, verify
from Transaction import Tx
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
import pickle
import random
import time

reward = 25.0 #25.0 is our block reward
leading_zeros = 2
next_char_limit = 100

class TxBlock(RBlock):
    nonce = "AAAAAAA"

    def __init__(self, previous):
        super(TxBlock, self).__init__([], previous)

    def addTx(self, Tx_in):
        self.data.append(Tx_in)

    def removeTx(self, Tx_in):
        if Tx_in in self.data:
            self.data.remove(Tx_in)
            return True
        return False

    def count_totals(self):
        total_in = 0
        total_out = 0
        for tx in self.data:
            for addr,amt in tx.inputs:
                total_in = total_in + amt
            for addr,amt in tx.outputs:
                total_out = total_out + amt
        return total_in, total_out

    def check_size(self):
        savePrev = self.previous
        self.previous = None
        this_size = len(pickle.dumps(self))
        self.previous = savePrev
        if this_size > 10000:
            return False
        return True

    def is_Valid(self):
        if not super(TxBlock, self).is_Valid():
            return False
        for tx in self.data:
            if not tx.is_Valid():
                return False
        total_in, total_out = self.count_totals()
        if total_out - total_in - reward > 0.00000000001:
            return False
        if not self.check_size():
            return False
        return True

    def good_nonce(self):
        digest = hashes.Hash(hashes.SHA256(), backend = default_backend())
        digest.update(bytes(str(self.data), 'utf8'))
        digest.update(bytes(str(self.previousHash), 'utf8'))
        digest.update(bytes(str(self.nonce), 'utf8'))
        this_hash =  digest.finalize()

        if this_hash[:leading_zeros] != bytes(''.join([ '\x4f' for i in range(leading_zeros)]),'utf8'):
            return False
        return int(this_hash[leading_zeros]) < next_char_limit

    def find_nonce(self,n_tries=1000000):
        for i in range(n_tries):
            self.nonce = ''.join([chr(random.randint(0,255)) for i in range(10*leading_zeros)])
            if self.good_nonce():
                return self.nonce
        return None
    
def findLongestBlockchain(head_blocks):
    longest = -1
    long_head = None
    for b in head_blocks:
        current = b
        this_len = 0
        while current != None:
            this_len = this_len + 1
            current = current.previous
        if this_len > longest:
            long_head = b
            longest = this_len
    return long_head
    
def saveBlocks(block_list, filename):
    fp = open(filename, "wb")
    pickle.dump(block_list, fp)
    fp.close()
    return True

def loadBlocks(filename):
    fin = open(filename, "rb")
    ret = pickle.load(fin)
    fin.close()
    return ret

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

#    message = b"Some text"
#    signature = sign(message, pr1)
#    print(verify(message, signature, pu1))

#    addrFile = open("public.dat", "wb")
#    pu_ser = pu1.public_bytes(
#        encoding=serialization.Encoding.PEM,
#        format=serialization.PublicFormat.SubjectPublicKeyInfo
#    )
#    pickle.dump(pu1, addrFile)
#    addrFile.close()
    saveFile = open("tx.dat", "wb")
    pickle.dump(Tx1, saveFile)
    saveFile.close()

#    loadFile = open("public.dat", "rb")
#    new_pu = pickle.load(loadFile)
#    loaded_pu = serialization.load_pem_public_key(
#        new_pu,
#        backend = default_backend()
#    )
#    print(verify(message, signature, new_pu))
#    loadFile.close()

    loadFile = open("tx.dat", "rb")
    newTx = pickle.load(loadFile)

    if newTx.is_Valid():
        print("Success Loaded tx is valid")
    loadFile.close()

    root = TxBlock(None)
    mine1 = Tx()
    mine1.add_output(pu1,8.0)
    mine1.add_output(pu2,8.0)
    mine1.add_output(pu3,8.0)
    
    root.addTx(Tx1)
    root.addTx(mine1)

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

    B6 = TxBlock(B4)
    this_pu = pu4
    this_pr = pr4
    for i in range(30):
        newTx = Tx()
        new_pr, new_pu = generate_keys()
        newTx.add_input(this_pu,0.3)
        newTx.add_output(new_pu,0.3)
        newTx.signature(this_pr)
        B6.addTx(newTx)
        this_pu, this_pr = new_pu, new_pr
        savePrev = B6.previous
        B6.previous = None
        this_size = len(pickle.dumps(B6))
        B6.previous = savePrev              
        if B6.is_Valid() and this_size > 10000:
            print ("ERROR! Big blocks are valid: size = ", str(this_size))
        elif (not B6.is_Valid ) and this_size <= 10000:
            print ("ERROR! Small blocks are invalid: size = ", str(this_size))
        else:
            print ("Success! Block passed.")

    overspend = Tx()
    overspend.add_input(pu1,45.0)
    overspend.add_output(pu2,44.5)
    overspend.signature(pr1)
    B7 = TxBlock(B4)
    B7.addTx(overspend)
    if B7.is_Valid():
        print("ERROR! Overspend not detected")
    else:
        print("Success! Overspend detected")

    overspend1 = Tx()
    overspend1.add_input(pu1,5.0)
    overspend1.add_output(pu2,4.5)
    overspend1.signature(pr1)
    overspend2 = Tx()
    overspend2.add_input(pu1,15.0)
    overspend2.add_output(pu3,14.5)
    overspend2.signature(pr1)
    overspend3 = Tx()
    overspend3.add_input(pu1,5.0)
    overspend3.add_output(pu4,4.5)
    overspend3.signature(pr1)
    overspend4 = Tx()
    overspend4.add_input(pu1,8.0)
    overspend4.add_output(pu2,4.5)
    overspend4.signature(pr1)
    B8 = TxBlock(B4)
    B8.addTx(overspend1)
    B8.addTx(overspend2)
    B8.addTx(overspend3)
    B8.addTx(overspend4)
    if B8.is_Valid():
        print("ERROR! Overspend not detected")
    else:
        print("Success! Overspend detected")
