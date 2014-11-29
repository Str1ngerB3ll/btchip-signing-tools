from btchip.btchip import *
from btchip.btchipUtils import *

# Optional setup
dongle = getDongle(True)
app = btchip(dongle)

# Authenticate
app.verifyPin(raw_input("PIN: "))
# Get the public key and compress it
for i in range(0,3):
  publicKey = app.getWalletPublicKey("0'/0/" + str(i))
  print str(publicKey['publicKey']).encode('hex')
  print "Public Key " + str(i + 1) + ": " + str(compress_public_key(publicKey['publicKey'])).encode('hex')
  print "Address " + str(i + 1) + ": " + str(publicKey['address'])
