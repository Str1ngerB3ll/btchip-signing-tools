import os, sys, inspect

cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"BitcoinArmory")))
if cmd_subfolder not in sys.path:
    sys.path.insert(0, cmd_subfolder)

from btchip.btchip import *
from btchip.btchipUtils import *
from armoryengine.Transaction import *
import json
import settings


# Run on non configured dongle or dongle configured with test seed below

SEED = bytearray(settings.SEED.decode('hex'))

if not hasattr(settings, "KEYPATH"):
  KEYPATH = raw_input("Enter keypath: (e.g. 0'/0/0)")
else:
  KEYPATH = settings.KEYPATH

if not hasattr(settings, "SIGCOLLECT"):
  SIGCOLLECT = raw_input("Enter SIGCOLLECT: ")
else:
  SIGCOLLECT = settings.SIGCOLLECT


# Note this is a testnet sigcollect, so it will fail the magic check
# if you don't specify `--testnet` when invoking this script.
sigcollect = """=====TXSIGCOLLECT-8jkccikU======================================
AQAAAAsRCQcAAAAAAf3yAQEAAAALEQkHAIM4E374BgH68oOqiWv9gOu4QuKQEiJT
ytoa/Lh2FgwAAAAA4AEAAAABPp/hKRfYVKDgk7mC6qRpkCieImLy25/BvT8TcY88
gG4BAAAAa0gwRQIhAK9mjkguPtNj9Rs23autfN8g0XcQTJK4Z2pbFPURBxeWAiBs
Ts1nVEx0xmicpFPiFX0MC4pGCNhZVkKdJhUnWlHGbwEhA3TbNZoARiba8vzxC4YB
9fOUOISKZzPHaOiM4K05iued/////wKA570CAAAAABepFOKiJ+tA386QLywdgN2v
p5ixbSLDh2yPyEYAAAAAGXapFK9Y8Jz2WyE7ub0YGpThM7StTWsniKwAAAAAaVIh
AmlpSDARTksfbvVlzk77kzaBAy0wMzyA33E99rYKTGKDIQL0O5BenjXM0idX+u35
7OtlLcm6GYo5BNQ/Qpje8CE+tSEDe541eN07VVnWE7wmQZMebOfVWp0IGwc0eIjX
0XorkQJTrghKTEJlcmNaawD/////AyECaWlIMBFOSx9u9WXOTvuTNoEDLTAzPIDf
cT32tgpMYoMAACEC9DuQXp41zNInV/rt+ezrZS3JuhmKOQTUP0KY3vAhPrUAACED
e541eN07VVnWE7wmQZMebOfVWp0IGwc0eIjX0XorkQIAAAIyAQAAAAsRCQcXqRTA
w7atpzLHl4gdAN5sNQ7sluPSIoeAlpgAAAAAAAAABE5PTkUAAAAyAQAAAAsRCQcX
qRTioifrQN/OkC8sHYDdr6eYsW0iw4fwKSUCAAAAAAAABE5PTkUAAAA=
================================================================"""

a = UnsignedTransaction()
tx = a.unserializeAscii(sigcollect)
print tx.toJSONMap()
print tx.pprint()

exit(0)


UTX = bytearray("01000000013e9fe12917d854a0e093b982eaa46990289e2262f2db9fc1bd3f13718f3c806e010000006b483045022100af668e482e3ed363f51b36ddabad7cdf20d177104c92b8676a5b14f51107179602206c4ecd67544c74c6689ca453e2157d0c0b8a4608d85956429d2615275a51c66f01210374db359a004626daf2fcf10b8601f5f39438848a6733c768e88ce0ad398ae79dffffffff0280e7bd020000000017a914e2a227eb40dfce902f2c1d80ddafa798b16d22c3876c8fc846000000001976a914af58f09cf65b213bb9bd181a94e133b4ad4d6b2788ac00000000".decode('hex'))
UTXO_INDEX = 0
OUTPUT = bytearray("02809698000000000017a914c0c3b6ada732c797881d00de6c350eec96e3d22287f02925020000000017a914e2a227eb40dfce902f2c1d80ddafa798b16d22c387".decode('hex'))
REDEEMSCRIPT = bytearray("52210269694830114e4b1f6ef565ce4efb933681032d30333c80df713df6b60a4c62832102f43b905e9e35ccd22757faedf9eceb652dc9ba198a3904d43f4298def0213eb521037b9e3578dd3b5559d613bc2641931e6ce7d55a9d081b07347888d7d17a2b910253ae".decode('hex'))

SIGNATURE_0 = bytearray("3044022056cb1b781fd04cfe6c04756ad56d02e5512f3fe7f411bc22d1594da5c815a393022074ad7f4d47af7c3f8a7ddf0ba2903f986a88649b0018ce1538c379b304a6a23801".decode('hex'))
SIGNATURE_1 = bytearray("304402205545419c4aded39c7f194b3f8c828f90e8d9352c756f7c131ed50e189c02f29a02201b160503d7310df49055b04a327e185fc22dfe68f433594ed7ce526d99a5026001".decode('hex'))
SIGNATURE_2 = bytearray("30440220634fbbfaaea74d42280a8c9e56c97418af04539f93458e85285d15462aec7712022041ba27a5644642a2f5b3c02610235ec2c6115bf4137bb51181cbc0a3a54dc0db01".decode('hex'))
TRANSACTION = bytearray("0100000001008338137ef80601faf283aa896bfd80ebb842e290122253cada1afcb876160c00000000fc004730440220634fbbfaaea74d42280a8c9e56c97418af04539f93458e85285d15462aec7712022041ba27a5644642a2f5b3c02610235ec2c6115bf4137bb51181cbc0a3a54dc0db0147304402205545419c4aded39c7f194b3f8c828f90e8d9352c756f7c131ed50e189c02f29a02201b160503d7310df49055b04a327e185fc22dfe68f433594ed7ce526d99a50260014c6952210269694830114e4b1f6ef565ce4efb933681032d30333c80df713df6b60a4c62832102f43b905e9e35ccd22757faedf9eceb652dc9ba198a3904d43f4298def0213eb521037b9e3578dd3b5559d613bc2641931e6ce7d55a9d081b07347888d7d17a2b910253aeffffffff02809698000000000017a914c0c3b6ada732c797881d00de6c350eec96e3d22287f02925020000000017a914e2a227eb40dfce902f2c1d80ddafa798b16d22c38700000000".decode('hex'))

output = get_output_script([["0.1", bytearray("a914c0c3b6ada732c797881d00de6c350eec96e3d22287".decode('hex'))], ["0.3599", bytearray("a914e2a227eb40dfce902f2c1d80ddafa798b16d22c387".decode('hex'))]]);
if output<>OUTPUT:
  raise BTChipException("Invalid output script encoding");  

# Optional setup
dongle = getDongle(True)
app = btchip(dongle)
try:
  app.setup(btchip.OPERATION_MODE_RELAXED_WALLET, btchip.FEATURE_RFC6979|btchip.FEATURE_NO_2FA_P2SH, 111, 196, "1234", None, btchip.QWERTY_KEYMAP, SEED)
except:
  pass
# Authenticate
app.verifyPin("1234")
# Get the trusted input associated to the UTXO
transaction = bitcoinTransaction(UTX)
print transaction
trustedInput = app.getTrustedInput(transaction, UTXO_INDEX)
# Start composing the transaction
app.startUntrustedTransaction(True, 0, [trustedInput], REDEEMSCRIPT)
app.finalizeInputFull(OUTPUT)
signature1 = app.untrustedHashSign("0'/0/1", "")
if signature1 <> SIGNATURE_1:
  raise BTChipException("Invalid signature1")

# Same thing for the second signature

app.startUntrustedTransaction(True, 0, [trustedInput], REDEEMSCRIPT)
app.finalizeInputFull(OUTPUT)
signature2 = app.untrustedHashSign("0'/0/2", "")
if signature2 <> SIGNATURE_2:
  raise BTChipException("Invalid signature2")

# Finalize the transaction - build the redeem script and put everything together
inputScript = get_p2sh_input_script(REDEEMSCRIPT, [signature2, signature1])
transaction = format_transaction(OUTPUT, [ [ trustedInput['value'], inputScript] ])
print "Generated transaction : " + str(transaction).encode('hex')
if transaction <> TRANSACTION:
  raise BTChipException("Invalid transaction")
# The transaction is ready to be broadcast, enjoy

