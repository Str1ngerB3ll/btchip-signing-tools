from btchip.btchip import *
from btchip.btchipUtils import *

print "This script is for setting up a new BTChip."

SEED = raw_input("Paste your seed: ")

# Optional setup
dongle = getDongle(True)
app = btchip(dongle)
try:
  app.setup(btchip.OPERATION_MODE_RELAXED_WALLET, btchip.FEATURE_RFC6979|btchip.FEATURE_NO_2FA_P2SH, 111, 196, "1234", None, btchip.QWERTY_KEYMAP, SEED)
except:
  pass
# Authenticate
app.verifyPin("1234")
