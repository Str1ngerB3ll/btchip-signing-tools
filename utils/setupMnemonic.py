import mnemonic, binascii, getpass
from btchip.btchip import *
from btchip.btchipUtils import *

M = mnemonic.Mnemonic("english")

print "This script is for setting up a new BTChip with a random mnemonic seed."

passphrase = getpass.getpass("Backup Passphrase (optional, increases backup security): ")
wordlist = M.generate(strength=256)
seed = binascii.hexlify(M.to_seed(wordlist, passphrase))
print 'mnemonic : %s (%d words)' % (wordlist, len(wordlist.split(' ')))
print 'seed     : %s (%d bits)\n' % (seed, len(seed) * 4)
SEED = bytearray(seed.decode('hex'))

# Setup
PIN = getpass.getpass("New PIN: ")
dongle = getDongle(True)
app = btchip(dongle)
try:
  # Testnet
  app.setup(btchip.OPERATION_MODE_RELAXED_WALLET, btchip.FEATURE_RFC6979|btchip.FEATURE_NO_2FA_P2SH, 111, 196, PIN, None, btchip.QWERTY_KEYMAP, None)
  # Mainnet
  # app.setup(btchip.OPERATION_MODE_RELAXED_WALLET, btchip.FEATURE_RFC6979|btchip.FEATURE_NO_2FA_P2SH, 0, 5, PIN, None, btchip.QWERTY_KEYMAP, SEED)
except:
  pass
  
# Authenticate to stop key from emitting the seed anymore
app.verifyPin(PIN)