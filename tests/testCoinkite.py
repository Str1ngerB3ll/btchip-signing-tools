from btchip.btchip import *
from btchip.btchipUtils import *
from signTxCoinkite import signCoinkiteJSON, createReturnJSON
from os.path import dirname, join
import json, binascii

# Optional setup
EXPECTED = "3044022030258b927bea37ad6f54e671fea34eac16effb0be8488dabf9a80070a52a1ef2022031137cca05628eecf93331c0855fec97f76d39b87c1ae52d37f0bebe6a58aa3d01"
SEED = bytearray("1762F9A3007DBC825D0DD9958B04880284C88A10C57CF569BB3DADF7B1027F2D".decode('hex'))
dongle = getDongle(True)
app = btchip(dongle)
try:
  app.setup(btchip.OPERATION_MODE_WALLET, btchip.FEATURE_RFC6979 | btchip.FEATURE_NO_2FA_P2SH, 111, 196, "1234", None, btchip.QWERTY_KEYMAP, SEED)
except:
  pass

app.verifyPin("1234")

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
result = signCoinkiteJSON(app, dongle, requestData, promptTx=False)

#verify
print json.dumps(result)
signature = result['signatures'][0][0]
if EXPECTED <> signature:
  print "Got:      " + signature
  print "Expected: " + EXPECTED
  raise Exception("Generated signature doesn't match!")

outData = createReturnJSON(app, dongle, result)

if outData <> refData:
  print "Got:      " + json.dumps(outData)
  print "Expected: " + json.dumps(refData)
  raise Exception("Generated JSON doesn't match reference!")
