#This file will be our blockchain

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes

class someClass:
    string = None
    num = 528677
    def __init__(self, mystr):
        self.string = mystr
    def __repr__(self):
        return self.string + "^^^" + str(self.num)

class RBlock:
    data = None
    previousHash = None
    previous = None
    def __init__(self, data, previous):
        self.data = data
        self.previous = previous
        if previous != None:
            self.previousHash = previous.computeHash()
    def computeHash(self):
        digest = hashes.Hash(hashes.SHA256(), backend = default_backend())
        digest.update(bytes(str(self.data), 'utf8'))
        digest.update(bytes(str(self.previousHash), 'utf8'))
        return digest.finalize()
    def is_Valid(self):
        if self.previous == None:
            return True
        return self.previous.computeHash() == self.previousHash

#Blockchain unit tests
if __name__ == '__main__':
    root = RBlock('I am Rrr', None)
    B1 = RBlock(b'Rrrrr', root)
    B2 = RBlock('Chris R', root)
    B3 = RBlock(12354, B1)
    B4 = RBlock(someClass('Hey man'), B3)
    B5 = RBlock("Top block", B4)

    for b in [B1, B2, B3, B4, B5]:
        if B1.previous.computeHash() == B1.previousHash:
            print("Succeed")
        else:
            print("ERROR")

    B3.data = 12345
    print(B4.previous.data)
    if B4.previous.computeHash() == B4.previousHash:
        print("ERROR")
    else:
        print("Success, tampering detected")

    print(B4.data)
    B4.data.num = 454348
    print(B4.data)
    if B5.previous.computeHash() == B5.previousHash:
        print("ERROR")
    else:
        print("Success, tampering detected")
