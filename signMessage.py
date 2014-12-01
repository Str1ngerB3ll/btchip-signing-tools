import os, sys, inspect, base64
# Add ./btchip-python to path so it works as if we were importing it from the inside.
cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"btchip-python")))
if cmd_subfolder not in sys.path:
    sys.path.insert(0, cmd_subfolder)

from btchip.btchip import *
from btchip.btchipUtils import *
from getKey import parsePath
import getpass, hashlib
from base64 import b64encode

def main():
  if len(sys.argv) < 2:
    print "Usage: python signMessage.py <path>"
    exit(1)

  path = parsePath(sys.argv[1])

  dongle = getDongle(True)
  app = btchip(dongle)

  # Authenticate
  pin = getpass.getpass("PIN: ")
  app.verifyPin(pin)

  print "Signed message: " + signMessage(app, dongle, path, raw_input("Message: "))

def signMessage(app, dongle, path, data):
  app.signMessagePrepare(path, data)

  print "Signing message with key at path " + path

  dongle.close()
  # Wait for the second factor confirmation
  # Done on the same application for test purposes, this is typically done in another window
  # or another computer for bigger transactions
  response = prompt2FA()

  return _sign(path, response)

def prompt2FA():
  response = raw_input("Powercycle the dongle to get the second factor and powercycle again. " + \
    "If it doesn't match what you expect, press <ctrl-c>. \n")
  while not len(response):
    print "Warning: Chip not powercycled, please powercycle the chip."
    response = prompt2FA()
  return response

def _sign(path, response):
  # Get a reference to the dongle again, as it was disconnected
  try:
    dongle = getDongle(False)
  except BTChipException as e:
    raw_input("Powercycle the chip first, then press <enter>.")
    return _sign(path, response)

  app = btchip(dongle)
  # Compute the signature
  signature = app.signMessageSign(response[len(response) - 4:])
  
  # Parse the ASN.1 signature

  rLength = signature[3]
  r = signature[4 : 4 + rLength]
  sLength = signature[4 + rLength + 1]
  s = signature[4 + rLength + 2:]
  if rLength == 33:
      r = r[1:]
  if sLength == 33:
      s = s[1:]
  r = str(r)
  s = str(s)

  # And convert it

  return b64encode(chr(27 + 4 + (signature[0] & 0x01)) + r + s)

if __name__ == "__main__":
  main()
