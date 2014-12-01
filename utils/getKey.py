import os, sys, inspect
# Add ./btchip-python to path so it works as if we were importing it from the inside.
cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"btchip-python")))
if cmd_subfolder not in sys.path:
    sys.path.insert(0, cmd_subfolder)

from btchip.btchip import *
from btchip.btchipUtils import *
from struct import pack,unpack
import getpass, sys, re, hashlib


def main():

  if len(sys.argv) < 2:
    print "Usage: python getKey.py <path>"
    exit(1)

  # Get path from cli
  inputPath = sys.argv[1]
  parsedPath = parsePath(inputPath)

  # Optional setup
  dongle = getDongle(True)
  app = btchip(dongle)

  # Authenticate
  pin = getpass.getpass("PIN: ")
  app.verifyPin(pin)

  printPath(app, parsedPath)

def parsePath(bip32Path):
  bip32Path = re.sub(r'^m/', '', bip32Path)
  bip32Path = re.sub(r'(\d+)h', "\g<1>'", bip32Path)
  return bip32Path

def printPath(app, path):
  publicKey = app.getWalletPublicKey(path)
  print "Path: " + path
  print "Full Public Key: " + str(publicKey['publicKey']).encode('hex')
  print "Public Key: " + str(compress_public_key(publicKey['publicKey'])).encode('hex')
  print "Address: " + str(publicKey['address'])
  xpub, tpub = getXPUB(app, path, publicKey)
  print "XPUB: " + xpub
  print "TPUB: " + tpub

def getXPUB(app, bip32_path, pubKey):
  splitPath = bip32_path.split('/')
  fingerprint = 0    

  # Grab previous node first if it exists
  if len(splitPath) > 1:
    prevPath = "/".join(splitPath[0:len(splitPath) - 1])
    nodeData = app.getWalletPublicKey(prevPath)
    publicKey = compress_public_key(nodeData['publicKey'])
    h = hashlib.new('ripemd160')
    h.update(hashlib.sha256(publicKey).digest())
    fingerprint = unpack(">I", h.digest()[0:4])[0]      

  nodeData = pubKey
  publicKey = compress_public_key(nodeData['publicKey'])
  depth = len(splitPath)
  lastChild = splitPath[len(splitPath) - 1].split('\'')
  if len(lastChild) == 1:
    childnum = int(lastChild[0])
  else:
    childnum = 0x80000000 | int(lastChild[0])    

  xpub = createXPUB(depth, fingerprint, childnum, nodeData['chainCode'], publicKey)
  tpub = createXPUB(depth, fingerprint, childnum, nodeData['chainCode'], publicKey, testnet=True)

  return EncodeBase58Check(xpub), EncodeBase58Check(tpub)

def createXPUB(depth, fingerprint, childnum, chainCode, publicKey, testnet=False):
  magic = "043587CF" if testnet else "0488B21E"
  return magic.decode('hex') + chr(depth) + i4b(fingerprint) + i4b(childnum) + \
      str(chainCode) + str(publicKey)

# From Electrum

__b58chars = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
__b58base = len(__b58chars)

def b58encode(v):
  """ encode v, which is a string of bytes, to base58."""
  long_value = 0L
  for (i, c) in enumerate(v[::-1]):
    long_value += (256**i) * ord(c)

  result = ''
  while long_value >= __b58base:
    div, mod = divmod(long_value, __b58base)
    result = __b58chars[mod] + result
    long_value = div
  result = __b58chars[long_value] + result

  # Bitcoin does a little leading-zero-compression:
  # leading 0-bytes in the input become leading-1s
  nPad = 0
  for c in v:
    if c == '\0': nPad += 1
    else: break

  return (__b58chars[0]*nPad) + result

def EncodeBase58Check(vchIn):
  hash = Hash(vchIn)
  return b58encode(vchIn + hash[0:4])

def Hash(x):
  if type(x) is unicode: x=x.encode('utf-8')
  return sha256(sha256(x))

def sha256(x):
  return hashlib.sha256(x).digest()

def i4b(x):
  return pack('>I', x)

if __name__ == "__main__":
  main()
