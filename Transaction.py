#Escrow Transactions

import Signatures

class Tx:
    inputs = None
    outputs = None
    signatures = None
    requiresSigns = None
    def __init__(self):
        self.inputs = []
        self.outputs = []
        self.signatures = []
        self.requiresSigns = []
    def add_input(self,_from, amount):
        self.inputs.append((_from, amount))#it's just tuple type 
    def add_output(self, _to, amount):
        self.outputs.append((_to, amount))
    def add_Req_Signatures(self, addr):
        self.requiresSigns.append(addr)
    def signature(self, private):
        message = self.__gather() #member function of the transaction class (in python this means private member function)
        newsig = Signatures.sign(message, private)
        self.signatures.append(newsig)
    def is_Valid(self):
        total_in = 0
        total_out = 0
        message = self.__gather()
        
        for addr,amount in self.inputs:
            found = False
            for s in self.signatures:
                if Signatures.verify(message, s, addr):
                    found = True
            if not found:
                return False
            if amount<0:
                return False
            total_in = total_in + amount
            
        for addr in self.requiresSigns:
            found = False
            for s in self.signatures:
                if Signatures.verify(message, s, addr):
                    found = True
            if not found:
                return False
        for addr,amount in self.outputs:
            if amount<0:
                return False
            total_out = total_out + amount

        #if total_out > total_in:
            #return False
        
        return True
    def __gather(self):
        data = []
        data.append(self.inputs)
        data.append(self.outputs)
        data.append(self.requiresSigns)
        return data
    def __repr__(self):
        reprstr = "INPUTS:\n"
        for addr,amt in self.inputs:
            reprstr = reprstr + str(amt) + " from " + str(addr) + "\n"
        reprstr = reprstr + "OUTPUT:\n"
        for addr,amt in self.outputs:
            reprstr = reprstr + str(amt) + " to " + str(addr) + "\n"
        reprstr = reprstr + "REGUIRE-SIGNATURES:\n"
        for r in self.requiresSigns:
            reprstr = reprstr + str(r) + "\n"
        reprstr = reprstr + "SIGNATURES:\n"
        for s in self.signatures:
            reprstr = reprstr + str(s) + "\n"
        reprstr = reprstr + "END\n"
        return reprstr
            

#some tests
if __name__ == "__main__":
    pr1, pu1 = Signatures.generate_keys()
    pr2, pu2 = Signatures.generate_keys()
    pr3, pu3 = Signatures.generate_keys()
    pr4, pu4 = Signatures.generate_keys()

    Tx1 = Tx()
    Tx1.add_input(pu1, 1)
    Tx1.add_output(pu2, 1)
    Tx1.signature(pr1)
    
    if Tx1.is_Valid():
        print("Succeed")
    else:
        print("Transaction is invalid")

    Tx2 = Tx()
    Tx2.add_input(pu1, 2)
    Tx2.add_output(pu2, 1)
    Tx2.add_output(pu3, 1)
    Tx2.signature(pr1)

    #Escrow Tx
    Tx3 = Tx()
    Tx3.add_input(pu3, 1.2)
    Tx3.add_output(pu1, 1.1)
    Tx3.add_Req_Signatures(pu4)
    Tx3.signature(pr3)
    Tx3.signature(pr4)
    
    for t in [Tx1, Tx2, Tx3]:
        if t.is_Valid():
            print("Succeed")
        else:
            print("ERROR")

    #Wrong signatures
    Tx4 = Tx()
    Tx4.add_input(pu1, 1)
    Tx4.add_output(pu2, 1)
    Tx4.signature(pr2)

    #Escrow
    Tx5 = Tx()
    Tx5.add_input(pu3, 1.2)
    Tx5.add_output(pu1, 1.1)
    Tx5.add_Req_Signatures(pu4)
    Tx5.signature(pr3)
    
    #Modified Tx
    Tx6 = Tx()
    Tx6.add_input(pu1, 1)
    Tx6.add_output(pu2, 1)
    Tx6.signature(pr1)
    Tx6.outputs[0]=(pu3, 1)
    
    for t in [Tx4, Tx5, Tx6]:
        if t.is_Valid():
            print("ERROR, Tx is valid")
        else:
            print("Succeed, invalid Tx")
