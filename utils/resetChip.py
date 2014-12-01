from btchip.btchip import *
from btchip.btchipUtils import *
import re

print "This script will WIPE a chip. Press ctrl-c now if you do not wish to do this."
raw_input("To continue, press <enter>.")

needsResetting = True
while needsResetting:
  try:
    dongle = getDongle(True)
    app = btchip(dongle)
    app.verifyPin("fioejwaofjawpoejvxvzxv") # man that would be awkward if this were your pin
  except BTChipException as e:
    raw_input("Please re-insert your chip and press <enter>.")
    if e.sw == 0x63c0:
      print "Reset complete."
      exit(0)
