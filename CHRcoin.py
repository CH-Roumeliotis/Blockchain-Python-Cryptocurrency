import time
import Wallet
import Miner
import threading
import Signatures

wallets=[]
miners=[]
my_ip = 'localhost'
wallets.append((my_ip,5006))
miners.append((my_ip,5005))

tMS = None
tNF = None
tWS = None

def startMiner():
    global tMS,tNF
    try:
        my_pu = Signatures.loadPublic("public.key")
    except:
        print("No public.key Need to generate?")
        pass #TODO
    tMS = threading.Thread(target=Miner.minerServer, args=((my_ip, 5005),))
    tNF = threading.Thread(target=Miner.nonceFinder, args=(wallets, my_pu))
    tMS.start()
    tNF.start()
    return True

def startWallet():
    global tWS
    Wallet.my_private, Wallet.my_public = Signatures.loadKeys("private.key","public.key")
    
    tWS = threading.Thread(target=Wallet.walletServer, args=((my_ip,5006),))
    tWS.start()
    return True

def stopMiner():
    global tMS, tNF
    Miner.StopAll()
    if tMS: tMS.join()
    if tNF: tNF.join()
    tMS = None
    tNF = None
    return True

def stopWallet():
    global tWS
    Wallet.StopAll()
    if tWS: tWS.join()
    tWS = None
    return True

def getBalance(pu_key):
    if not tWS:
        print("Start the server by calling startWallet before checking balances")
        return 0.0
    return Wallet.getBalance(pu_key)

def sendCoins(pu_recv, amt, tx_fee):
    Wallet.sendCoins(Wallet.my_public, amt+tx_fee, Wallet.my_private, pu_recv,
                     amt, miners)
    return True

def makeNewKeys():
    return None, None






if __name__ == "__main__":
    startMiner()
    startWallet()
    other_public = b'-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAuNWjb731EO93Dw5z6Yo8\nSdTyGhwflZiKe5trf+KPSdySIu6Yqtwta87sIXgYkJSBzO58kWWg/9poS1jtEWc4\nGXKTwk3p1he7X3QQBUDMMM1W5K6WUr2luUXxZwJr44y3NtZjs43diCNjWGMI2a4N\n4DmNjQ8kzA8kau1XHWfbtv9unBzlOknZkhixZKZo+/c4j0SxQtbmiplLYOH8b7jg\nam2EiPgk73FW27TCW7qc9DBORqoIUtGKaGDC6Rmw6Xj0S1Qbstg000XJxz2VD/pz\nezKlbTCy+TeQjU60VqxgMm9G1ZeKC9ohUJjnY1B8MxUGHxBRgpGuwb+3W0wtokpw\niwIDAQAB\n-----END PUBLIC KEY-----\n'
    
    time.sleep(2)
    print(getBalance(Wallet.my_public))
    sendCoins( other_public, 1.0, 0.1 )
    time.sleep(20)
    print(getBalance(other_public))
    print(getBalance(Wallet.my_public))

    time.sleep(1)
    stopWallet()
    stopMiner()
