from btchip.btchip import *
from btchip.btchipUtils import *
import getpass, click

@click.command()
@click.option('--testnet', default=False, is_flag=True, help="If set, will set up the dongle in testnet mode." )
def main(testnet):
  print "This script is for setting up a new BTChip."

  seed = bytearray(raw_input("Paste your seed: ").decode('hex'))
  # This is the test seed
  # seed = bytearray("1762F9A3007DBC825D0DD9958B04880284C88A10C57CF569BB3DADF7B1027F2D".decode('hex'))

  setup(seed, testnet)

# Exported
def setup(seed, testnet=False):
  network = "Testnet" if testnet else "Mainnet"
  print "Chip will be used on network: " + network

  pin = getpass.getpass("New PIN: ")

  dongle = getDongle(False)
  app = btchip(dongle)
  try:
    if testnet:
      app.setup(btchip.OPERATION_MODE_RELAXED_WALLET, btchip.FEATURE_RFC6979|btchip.FEATURE_NO_2FA_P2SH, 111, 196, pin, None, btchip.QWERTY_KEYMAP, seed)
    else:
      app.setup(btchip.OPERATION_MODE_RELAXED_WALLET, btchip.FEATURE_RFC6979|btchip.FEATURE_NO_2FA_P2SH, 0, 5, pin, None, btchip.QWERTY_KEYMAP, seed)
  except BTChipException as e:
    if e.sw == 0x6985:
      print "ERROR: Chip is already set up. If you want to set it up with a new seed, run resetChip.py first."
    exit(1)
    
  # Authenticate to stop key from emitting the seed anymore
  app.verifyPin(pin)

if __name__ == "__main__":
  main()
