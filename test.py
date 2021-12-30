from Crypto.PublicKey import RSA
from Crypto import Random
import base64
from Crypto.Hash import SHA256
from Crypto.Signature import pkcs1_15
import json
from Crypto.PublicKey import RSA
from Crypto.Util import asn1
from base64 import b64decode

"""mykey = "-----BEGIN PUBLIC KEY-----\\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA35jGy0zDBv8qDDA0aCUS\\n/pIWbHKGl/V837yxbVAKYQewE9AHE3CcW/mbe0ok8+3YUowUI2dXN5WQCt0wl8wl\\n1Tpn5eGpzCmJ0cAkSrdXb6YLXMOV3XzJlcx/j3mwkG6mk+RIHmcbH4T8j20+ceJI\\nAcwEPvKYJmXy0+NYurFwX9VbexFxmjwtrSE/5dhb7b50qxSkng/SZfhC/WZqoEX8\\na7LvT5MvhM5PkPYjOFs/OCVQeXBxrpZzp9CH0ZeNwl/dlv5ocQSZjO4prUzssZ9H\\neQ+XiaUnYNV9BgCOAM/4Tk0cNLBBAsh4UD5/sxZvSiPwBuD+NR9/+CdTielG2Thf\\nCQIDAQAB\\n-----END PUBLIC KEY-----"
key64 = (
    mykey.replace("\\n", "")
    .replace("-----BEGIN PUBLIC KEY-----", "")
    .replace("-----END PUBLIC KEY-----", "")
    .strip()
)
keyDER = b64decode(key64)
publickey = RSA.importKey(keyDER)


signature = 'b"\xb6\x90\x12\x92\x918\xb8\xdd#\xde\x84aX\xcf]\xed\xbb/\xaf\xd6M\x12\xc5\x17\xcfR+\xe5\xab\x8d\ra\xf5\x12(\x8c_\xd3!\xc7\xbdm\xbe\x96\xa8\xa5\xc6\xf4u\x05x]\x89\xb2\x80\xb9\x15\xf0\xddT\x9aSt3\xf0\x98\xd1\x97\x9a\xe2\xe8\xf0\xdag\x12\xec\xe9R\xd8\x98\xacl\xc4WS,@\x92\x013\x9d\x99\x07\xae:\x84\xf4t\x1cL\xe43\xbfu\xc2\\\xf7=\xb9\xd1+\xc1qLL\xa9\xf7\x9a\x18 \xcd\\\xd3n^\xb3\xb6\x99\xb5C\xc2\x01\x12\xbb(\xef-\xd1\xfd/\x1e\x88\xdd\x04\x9a.@\xe3RL1\xdbL\xa7\xf1r\xff\t\xf6`\xf5MGO\x12T\xce\xfd)\xee\x8f.~L\x00h/\x04g\x8b\xae\xcc\xe1k\x95\xf2\xb8R\x07\xd5\xf9\xef\x18\x8a6\xfdW\xc12\x95?\xfdsF;\xb8o\x041\x07\xcb>\xfa\xfd\x8efp\x1c|<\xa5\xcd\xed\xe1\x17!\x9c>\x8c|\xec\xbc5$\xe6\xcf\x0f\xb6A(\x98\x96\x92\x98\x1e\x84I\xc8\x8b\x87\xb6m,5\xcf\x82"'
signature = signature[2:-1]
signature = bytes(signature, encoding="utf8")
print(signature)
print(type(signature))
message = json.dumps(
    {"sender": "Default", "receiver": "D", "amount": 30}, indent=2
).encode("utf-8")
h = SHA256.new(message)
try:
    pkcs1_15.new(publickey).verify(h, signature)
    print(True)
except (ValueError, TypeError):
    print(False)"""

from base64 import b64decode

signature = b"\xb6\x90\x12\x92\x918\xb8\xdd#\xde\x84aX\xcf]\xed\xbb/\xaf\xd6M\x12\xc5\x17\xcfR+\xe5\xab\x8d\ra\xf5\x12(\x8c_\xd3!\xc7\xbdm\xbe\x96\xa8\xa5\xc6\xf4u\x05x]\x89\xb2\x80\xb9\x15\xf0\xddT\x9aSt3\xf0\x98\xd1\x97\x9a\xe2\xe8\xf0\xdag\x12\xec\xe9R\xd8\x98\xacl\xc4WS,@\x92\x013\x9d\x99\x07\xae:\x84\xf4t\x1cL\xe43\xbfu\xc2\\\xf7=\xb9\xd1+\xc1qLL\xa9\xf7\x9a\x18 \xcd\\\xd3n^\xb3\xb6\x99\xb5C\xc2\x01\x12\xbb(\xef-\xd1\xfd/\x1e\x88\xdd\x04\x9a.@\xe3RL1\xdbL\xa7\xf1r\xff\t\xf6`\xf5MGO\x12T\xce\xfd)\xee\x8f.~L\x00h/\x04g\x8b\xae\xcc\xe1k\x95\xf2\xb8R\x07\xd5\xf9\xef\x18\x8a6\xfdW\xc12\x95?\xfdsF;\xb8o\x041\x07\xcb>\xfa\xfd\x8efp\x1c|<\xa5\xcd\xed\xe1\x17!\x9c>\x8c|\xec\xbc5$\xe6\xcf\x0f\xb6A(\x98\x96\x92\x98\x1e\x84I\xc8\x8b\x87\xb6m,5\xcf\x82"
signature = str(signature)
signature = signature.encode("utf-8")
message = json.dumps(
    {"sender": "Default", "receiver": "D", "amount": 30}, indent=2
).encode("utf-8")
h = SHA256.new(message)
key = "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA35jGy0zDBv8qDDA0aCUS/pIWbHKGl/V837yxbVAKYQewE9AHE3CcW/mbe0ok8+3YUowUI2dXN5WQCt0wl8wl1Tpn5eGpzCmJ0cAkSrdXb6YLXMOV3XzJlcx/j3mwkG6mk+RIHmcbH4T8j20+ceJIAcwEPvKYJmXy0+NYurFwX9VbexFxmjwtrSE/5dhb7b50qxSkng/SZfhC/WZqoEX8a7LvT5MvhM5PkPYjOFs/OCVQeXBxrpZzp9CH0ZeNwl/dlv5ocQSZjO4prUzssZ9HeQ+XiaUnYNV9BgCOAM/4Tk0cNLBBAsh4UD5/sxZvSiPwBuD+NR9/+CdTielG2ThfCQIDAQAB"
keyDER = b64decode(key)
publickey = RSA.importKey(keyDER)
pkcs1_15.new(publickey).verify(h, signature)
