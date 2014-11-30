from btchip.btchip import *
from btchip.btchipUtils import *
import getpass, sys, re

if len(sys.argv) < 2:
  print "Usage: python getKey.py <path>"
  exit(1)

def main():
  # Get path from cli
  inputPath = sys.argv[1]
  parsedPath = parsePath(inputPath)

  # Optional setup
  dongle = getDongle(True)
  app = btchip(dongle)

  # Authenticate
  pin = getpass.getpass("PIN: ")
  app.verifyPin(pin)

  printPath(parsedPath)

def parsePath(bip32Path):
  bip32Path = re.sub(r'^m/', '', bip32Path)
  bip32Path = re.sub(r'(\d+)h', "\g<1>'", bip32Path)
  return bip32Path

def printPath(path):
  publicKey = app.getWalletPublicKey(path)
  print "Path: " + path
  print "Full Public Key: " + str(publicKey['publicKey']).encode('hex')
  print "Public Key: " + str(compress_public_key(publicKey['publicKey'])).encode('hex')
  print "Address: " + str(publicKey['address'])

if __name__ == "__main__":
  main()
