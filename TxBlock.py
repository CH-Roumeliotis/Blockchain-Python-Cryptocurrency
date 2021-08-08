from BlockChain import RBlock
from Signatures import generate_keys, sign, verify
from Transaction import Tx
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
import pickle

class TxBlock(RBlock):
    def __init__(self, previous):
        pass
    def addTx(self, Tx_in):
        pass
    def isValid(self):
        return False
if __name__ == "__main__":
    pr1, pu1 = generate_keys()
    pr2, pu2 = generate_keys()
    pr3, pu3 = generate_keys()

    Tx1 = Tx()
    Tx1.add_input(pu1, 1)
    Tx1.add_output(pu2, 1)
    Tx1.signature(pr1)

    print(Tx1.is_Valid())

    message = b"Some text"
    signature = sign(message, pr1)
    print(verify(message, signature, pu1))

    saveFile = open("save.dat", "wb")
#    pu_ser = pu1.public_bytes(
#        encoding=serialization.Encoding.PEM,
#        format=serialization.PublicFormat.SubjectPublicKeyInfo
#    )
    pickle.dump(pu1, saveFile)
    saveFile.close()

    loadFile = open("save.dat", "rb")
    new_pu = pickle.load(loadFile)
    loaded_pu = serialization.load_pem_public_key(
        new_pu,
        backend = default_backend()
    )
    print(verify(message, signature, loaded_pu))
    #newTx = pickle.load(loadFile)

    print(newTx.is_Valid())
