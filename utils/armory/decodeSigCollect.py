import os, sys, inspect
# Add ../../BitcoinArmory to path so it works as if we were importing it from the inside.
cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"../../BitcoinArmory")))
if cmd_subfolder not in sys.path:
    sys.path.insert(0, cmd_subfolder)

from armoryengine.Transaction import *
from armoryengine.ArmoryUtils import binary_to_hex, hex_to_binary
import json
import settings
import pprint
pp = pprint.PrettyPrinter(indent=2)

# We've had SIGCOLLECTs fail to broadcaset from Armory. Recently we had one with multiple
# signed inputs completely fail with a `string index out of range` error in Armory.
#
# This tool takes in a SIGCOLLECT block and prints transaction details and a raw transaction that can be
# broadcast via bitcoind or any blockchain API like blockchain.info.
#
# You need to have the BitcoinArmory repo cloned in the root directory of the signer repo.
def decodeSigCollect():
  print "Paste your TXSIGCOLLECT below and press <enter>:\n"
  stopAt = "================================================================"
  SIGCOLLECT = ""
  for line in iter(raw_input, stopAt):
    SIGCOLLECT += line + "\n"

  SIGCOLLECT += stopAt

  a = UnsignedTransaction()
  tx = a.unserializeAscii(SIGCOLLECT)

  txJSON = tx.toJSONMap();

  pp.pprint(txJSON)
  print "\n"

  print "\nTransaction summary:\n"
  tx.pprint()
  tx.evaluateSigningStatus().pprint()

  print "\nRaw Transaction:\n"
  print binary_to_hex(tx.getSignedPyTx(doVerifySigs=False).serialize())


if __name__ == "__main__":
  decodeSigCollect()
