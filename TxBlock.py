from BlockChain import RBlock
from Signatures import generate_keys, sign, verify
from Transaction import Tx
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
import pickle

class TxBlock(RBlock):
    def __init__(self, previous):
        super(TxBlock, self).__init__([], previous)
    def addTx(self, Tx_in):
        self.data.append(Tx_in)
    def is_Valid(self):
        if not super(TxBlock, self).is_Valid():
            return False
        return True
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

#    B1.is_Valid()
#    root.is_Valid()

    saveFile = open("block.dat", "wb")
    pickle.dump(B1, saveFile)
    saveFile.close()

    loadFile = open("block.dat", "rb")
    load_B1 = pickle.load(loadFile)

    load_B1.is_Valid

    for b in [root, B1, load_B1, load_B1.previous]:
        if b.is_Valid():
            print("Success, Valid Block")
        else:
            print("ERROR Block")

    B2 = TxBlock(B1)
    Tx5 = Tx()
    Tx5.add_input(pu3, 1)
    Tx5.add_output(pu1, 100)
    Tx5.signature(pr3)

    load_B1.previous.addTx(Tx4)
    for b in [B2, load_B1]:
        if b.is_Valid():
            print("Error, block is not verified")
        else:
            print("Succeed, block verified")
            
