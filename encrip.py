from Crypto.Cipher import *
import hashlib
password = "mypassword".encode()
key  = hashlib.sha256(password).digest()
mode  = AES.MODE_CBC
    #print (key)
    IV  = 'THIS IS AN iv456'

    def p.message(message)
    wile len(message)% 16! =0 :
        message = message + ""
    return message

  
cipher = AES.new(key, mod, IV)
message= "entrada mensaje"
padded_message = pad_message(message)
encrypted_message  = cipher.encrypt(padded_message)