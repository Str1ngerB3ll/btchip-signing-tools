import os, sys, inspect
# Add ./btchip-python to path so it works as if we were importing it from the inside.
cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"btchip-python")))
if cmd_subfolder not in sys.path:
    sys.path.insert(0, cmd_subfolder)

from btchip.btchip import *
from btchip.btchipUtils import *
from getKey import parsePath
import getpass, binascii

if len(sys.argv) < 2:
  print "Usage: python signMessage.py <path>"
  exit(1)

path = parsePath(sys.argv[1])

dongle = getDongle(True)
app = btchip(dongle)

# Authenticate
pin = getpass.getpass("PIN: ")
app.verifyPin(pin)

# Start signing
app.signMessagePrepare(path, raw_input("Message: "))

print "Signing message with key at path " + path

dongle.close()
# Wait for the second factor confirmation
# Done on the same application for test purposes, this is typically done in another window
# or another computer for bigger transactions
response = raw_input("Powercycle the dongle to get the second factor and powercycle again. " + \
  "If it doesn't match what you expect, press <ctrl-c>. \n")

# Get a reference to the dongle again, as it was disconnected
dongle = getDongle(True)
app = btchip(dongle)
# Compute the signature
signature = app.signMessageSign(response[len(response) - 4:])
print "Signature: " + binascii.hexlify(signature)
