import os, sys, inspect, base64
from btchip.btchip import *
from btchip.btchipUtils import *
from utils.getKey import parsePath
from signMessage import signMessage
import getpass, hashlib
from base64 import b64encode
import re

def main():
  if len(sys.argv) < 2:
    print "Usage: python signBitID.py <path>"
    exit(1)

  path = parsePath(sys.argv[1])
  # magic hack to turn off 2FA
  path = re.sub(r'(\d+)(\')?$', "\g<1>" + str(0xb11e) + "\g<2>", path)

  dongle = getDongle(False)
  app = btchip(dongle)

  # Authenticate
  pin = getpass.getpass("PIN: ")
  app.verifyPin(pin)

  challenge = raw_input("Copy/Paste your challenge: ")

  publicKey = app.getWalletPublicKey(path)

  print "Address: " + str(publicKey['address'])
  print "Signed message: " + signMessage(app, dongle, path, challenge, use2FA=False)

if __name__ == "__main__":
  main()
