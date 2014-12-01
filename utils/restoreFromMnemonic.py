import mnemonic, binascii, getpass
from btchip.btchip import *
from btchip.btchipUtils import *

isTestnet = len(sys.argv) > 2 and sys.argv[2] == '--testnet'

M = mnemonic.Mnemonic("english")

print "This script is for restoring a new BTChip from a mnemonic seed."

wordlist = raw_input("Backup Mnemonic: ")
passphrase = getpass.getpass("Backup Passphrase (Press enter if blank):")
seed = binascii.hexlify(M.to_seed(wordlist, passphrase))
print 'mnemonic : %s (%d words)' % (wordlist, len(wordlist.split(' ')))
print 'seed     : %s (%d bits)\n' % (seed, len(seed) * 4)
SEED = bytearray(seed.decode('hex'))

# Setup
PIN = getpass.getpass("New PIN: ")
dongle = getDongle(False)
app = btchip(dongle)
try:
  if isTestnet:
    app.setup(btchip.OPERATION_MODE_RELAXED_WALLET, btchip.FEATURE_RFC6979|btchip.FEATURE_NO_2FA_P2SH, 111, 196, PIN, None, btchip.QWERTY_KEYMAP, SEED)
  else:
    app.setup(btchip.OPERATION_MODE_RELAXED_WALLET, btchip.FEATURE_RFC6979|btchip.FEATURE_NO_2FA_P2SH, 0, 5, PIN, None, btchip.QWERTY_KEYMAP, SEED)
except:
  pass
  
# Authenticate to stop key from emitting the seed anymore
app.verifyPin(PIN)
