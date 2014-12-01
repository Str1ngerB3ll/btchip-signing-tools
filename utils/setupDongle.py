from btchip.btchip import *
from btchip.btchipUtils import *
import getpass

print "This script is for setting up a new BTChip."

SEED = bytearray(raw_input("Paste your seed: ").decode('hex'))
PIN = getpass.getpass("New PIN: ")
# SEED = bytearray("1762F9A3007DBC825D0DD9958B04880284C88A10C57CF569BB3DADF7B1027F2D".decode('hex'))

# Optional setup
dongle = getDongle(False)
app = btchip(dongle)
try:
  # Testnet
  app.setup(btchip.OPERATION_MODE_RELAXED_WALLET, btchip.FEATURE_RFC6979|btchip.FEATURE_NO_2FA_P2SH, 111, 196, PIN, None, btchip.QWERTY_KEYMAP, SEED)
  # Mainnet
  # app.setup(btchip.OPERATION_MODE_RELAXED_WALLET, btchip.FEATURE_RFC6979|btchip.FEATURE_NO_2FA_P2SH, 0, 5, PIN, None, btchip.QWERTY_KEYMAP, SEED)
except BTChipException as e:
  if e.sw == 0x6985:
    print "ERROR: Chip is already set up. If you want to set it up with a new seed, run resetChip.py first."
  exit(1)
  
# Authenticate
app.verifyPin(PIN)
