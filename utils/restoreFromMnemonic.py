import mnemonic, binascii, getpass, sys, click
from setupDongle import setup

@click.command()
@click.option('--testnet', default=False, is_flag=True, help="If set, will set up the dongle in testnet mode." )
def main(testnet):
  print "This script is for restoring a new BTChip from a mnemonic seed."

  M = mnemonic.Mnemonic("english")
  wordlist = raw_input("Backup Mnemonic: ")
  passphrase = getpass.getpass("Backup Passphrase (Press enter if blank):")
  seed = binascii.hexlify(M.to_seed(wordlist, passphrase))
  print 'mnemonic : %s (%d words)' % (wordlist, len(wordlist.split(' ')))
  print 'seed     : %s (%d bits)\n' % (seed, len(seed) * 4)

  setup(bytearray(seed.decode('hex')), testnet)

if __name__ == "__main__":
  main()
