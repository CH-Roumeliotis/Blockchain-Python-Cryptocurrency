#Signatures RSA
#First, you have to install 'cryptography'

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.exceptions import InvalidSignature

def generate_keys():
    private = rsa.generate_private_key(
        public_exponent = 65537,
        key_size = 2048,
        backend = default_backend())
    public = private.public_key()
    return private, public

def sign(message, private):
    message = bytes(message, 'utf-8')
    signature = private.sign(
        message,
        padding.PSS(
            mgf = padding.MGF1(hashes.SHA256()),
            salt_length = padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    return signature

def verify(message, signature, public):
    message = bytes(str(message), 'utf-8')
    try:
        public.verify(
            signature,
            message,
            padding.PSS(
                mgf = padding.MGF1(hashes.SHA256()),
                salt_length = padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return True
    except InvalidSignature:
        return False
    except:
        print("Error Executing public key verify")
        return False

if __name__ == '__main__':
    pr, pu = generate_keys()
    print(pr)
    print(pu)
    message = "This is a secret message" #Removed the 'b' for bytes, we added the message = bytes(message, 'utf-8')
    signature = sign(message, pr)
    print(signature)
    correct = verify(message, signature, pu)

    if correct:
        print("Success")
    else:
        print("Error...Signature is wrong")

    #So lets be an attacker and generate a wrong private key...
    pr2, pu2 = generate_keys()
    signature2 = sign(message, pr2)
    correct = verify(message, signature2, pu)

    if correct:
        print("ERROR, Wrong signature")
    else:
        print("Success, Wrong Signature detected")

    badmess = message + "Q"
    correct = verify(badmess, signature, pu)
    if correct:
        print("ERROR...Tampered message")
    else:
        print("Success, Tampering detected")
