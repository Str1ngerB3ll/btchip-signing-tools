import os, sys, inspect
# Add ./BitcoinArmory to path so it works as if we were importing it from the inside.
cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"BitcoinArmory")))
if cmd_subfolder not in sys.path:
    sys.path.insert(0, cmd_subfolder)

from btchip.btchip import *
from btchip.btchipUtils import *
from armoryengine.Transaction import *
from armoryengine.ArmoryUtils import binary_to_hex, hex_to_binary
import json
import settings
import pprint
pp = pprint.PrettyPrinter(indent=2)
import binascii

# Run on non configured dongle or dongle configured with test seed below
SEED = bytearray(settings.SEED.decode('hex'))

if not hasattr(settings, "KEYPATH"):
  KEYPATH = raw_input("Enter keypath: (e.g. 0'/0/0)")
else:
  KEYPATH = settings.KEYPATH

if not hasattr(settings, "SIGCOLLECT"):
  SIGCOLLECT = raw_input("Enter SIGCOLLECT: ")
else:
  SIGCOLLECT = settings.SIGCOLLECT


a = UnsignedTransaction()
tx = a.unserializeAscii(SIGCOLLECT)

txJSON = tx.toJSONMap();

print "JSON:\n"
pp.pprint(txJSON)

print "\nTransaction summary:\n"
tx.pprint()
tx.evaluateSigningStatus().pprint()

# Get input tx
UTX = bytearray(txJSON['inputs'][0]['supporttx'].decode('hex'))

# Create outputs from armory script
outputs = []
for output in txJSON['outputs']:
  outputs.append([str(output['txoutvalue'] / 10e7), bytearray(output['txoutscript'].decode('hex'))])
print outputs
OUTPUT = get_output_script(outputs)
# print binascii.hexlify(OUTPUT)

REDEEMSCRIPT = txJSON['inputs'][0]['p2shscript']
print REDEEMSCRIPT

# Get Input index (IMPORTANT! We have to sign the correct output of the prev. tx)
UTXO_INDEX = txJSON['inputs'][0]['supporttxoutindex']

# Get Dongle
dongle = getDongle(True)
app = btchip(dongle)

try:
  # 111 is testnet bitcoin key version
  # 196 is p2sh testnet type
  app.setup(btchip.OPERATION_MODE_RELAXED_WALLET, btchip.FEATURE_RFC6979|btchip.FEATURE_NO_2FA_P2SH, 111, 196, "1234", None, btchip.QWERTY_KEYMAP, SEED)
except:
  pass

# Authenticate
pin = raw_input("PIN: ")
app.verifyPin(pin)

pubKeyRaw = app.getWalletPublicKey(KEYPATH)
pubKey = str(compress_public_key(pubKeyRaw['publicKey'])).encode('hex')
print "Your pubkey: " + pubKey

# Get the input
print "Getting input from transaction..."
transaction = bitcoinTransaction(UTX)
print str(transaction)
trustedInput = app.getTrustedInput(transaction, UTXO_INDEX)

# Start composing transaction
print "Creating transaction on BTChip..."
app.startUntrustedTransaction(True, 0, [trustedInput], bytearray(REDEEMSCRIPT.decode('hex')))
app.finalizeInputFull(OUTPUT)

print "Signing..."
signature = app.untrustedHashSign(KEYPATH, "")
sigStr = hex_to_binary(binascii.hexlify(signature))

# Put signature back into armory transaction
tx.insertSignature(sigStr, hex_to_binary(pubKey))

print "\n\nSignature summary and signing status:\n\n"

tx.pprint()
tx.evaluateSigningStatus().pprint()

print "\n\nRaw transaction:\n\n"

# doVerifySigs = tx.evaluateSigningStatus().canBroadcast
# print binary_to_hex(tx.getSignedPyTx(doVerifySigs=doVerifySigs).serialize())

# Unfortunately Armory doesn't appear to be able to verify these, so you're best off broadcasting the raw
# tx via the bitcoind CLI.
print binary_to_hex(tx.getSignedPyTx(doVerifySigs=False).serialize())

print "\n\nSigcollect below:\n\n"
print tx.serializeAscii()

exit(0)
