from btchip.btchip import *
from btchip.btchipUtils import *
from signTxCoinkite import signCoinkiteJSON
from os.path import dirname, join
import json

# Optional setup
SEED = bytearray("1762F9A3007DBC825D0DD9958B04880284C88A10C57CF569BB3DADF7B1027F2D".decode('hex'))
dongle = getDongle(True)
app = btchip(dongle)
# try:
  # app.setup(btchip.OPERATION_MODE_RELAXED_WALLET, btchip.FEATURE_RFC6979, 111, 196, "1234", None, btchip.QWERTY_KEYMAP, SEED)
# except:
  # pass

# Open fixtures
here = dirname(__file__)
inPath = here + "/fixtures/sign.json"
refPath = here + "/fixtures/output.json" # output.json came from coinkite's internal page
f = open(inPath, 'r')
signData = json.load(f)
requestData = json.loads(signData['contents'])
f = open(refPath, 'r')
refData = json.load(f)

# Sign data and compare to reference
outData = signCoinkiteJSON(app, dongle, requestData)
assert outData == refData
