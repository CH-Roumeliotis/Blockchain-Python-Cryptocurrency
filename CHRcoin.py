import time
import Wallet

wallets=[]
miners=[]
my_ip = 'localhost'

def startMiner():
    #Start nonceFinder
    #Start minerServer
    #Load tx_list
    #Load head_blocks
    #Load public_key
    return True
def startWallet():
    #Start walletServer
    #Load public and private keys
    #Load head_blocsk
    return True

def stopMiner():
    #Stop nonceFinder
    #Stop minerServer
    #Save tx_list
    #Save head_blocks
    return True
def stopWallet():
    #Stop walletServer
    #Save head_blocks
    return True

def getBalance(pu_key):
    return 0.0

def sendCoins(pu_recv, amt, tx_fee):
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
    print(getBalance(other_public))
    print(getBalance(Wallet.my_public))

    time.sleep(1)
    stopWallet()
    stopMiner()
