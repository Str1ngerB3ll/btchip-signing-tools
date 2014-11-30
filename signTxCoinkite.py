import os, sys, inspect
# Add ./btchip-python to path so it works as if we were importing it from the inside.
cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"btchip-python")))
if cmd_subfolder not in sys.path:
    sys.path.insert(0, cmd_subfolder)

from btchip.btchip import *
from btchip.btchipUtils import *
import json, settings, pprint, getpass, binascii,hashlib
from signMessage import signMessage
from pycoin.tx.Tx import Tx
pp = pprint.PrettyPrinter(indent=2)

def main():

  if len(sys.argv) < 2:
    print "Usage: python signTxCoinkite.py <JSON path>"
    exit(1)

  # Get path from cli
  inputPath = sys.argv[1]

  f = open(sys.argv[1], 'r')
  signData = json.load(f)
  requestData = json.loads(signData['contents'])

  body = signCoinkiteJSON(requestData)

  fName = 'output-' + requestData['request'] + '.json'
  fOut = open(fName, 'w')
  fOut.write(json.dumps(body))
  fOut.close()

  print "Output written to " + fName

  print json.dumps(body)

def signCoinkiteJSON(requestData):
  # Get Dongle
  dongle = getDongle(True)
  app = btchip(dongle)

  # Authenticate with dongle
  pin = getpass.getpass("PIN: ")
  app.verifyPin(pin)

  pp.pprint(requestData)

  # Keys: 
  # inputs: array of '1', input hash
  # proposal_title
  # raw_unsigned_txn (jackpot)
  # redeem_scripts: '1': {addr: addr, redeem: redeemScript}
  # req_keys: {1: [address, pubkey, pubkey]} (can generate redeemscript from this)
  # request (id)
  # super_tech_html - key path is inside here, regex for <td><code>m/1</code></td>

  result = {}
  result['cosigner'] = requestData['cosigner']
  result['request'] = requestData['request']
  result['signatures'] = []

  # Get input tx
  UTX = bytearray(requestData['raw_unsigned_txn'].decode('hex'))
  txObj = Tx.tx_from_hex(requestData['raw_unsigned_txn'])

  # Create outputs from tx
  outputs = []
  for output in txObj.txs_out:
    outputs.append([str(output.coin_value), bytearray(output.script)])
  OUTPUT = get_output_script(outputs)

  wallets = {}

  # Sign each input
  for i, signInput in enumerate(requestData['inputs']):
    # Get the input
    print "Getting input from transaction..."
    transaction = bitcoinTransaction(UTX)
    print str(transaction)
    UTXO_INDEX = requestData['input_info'][i]['out_num']
    trustedInput = app.getTrustedInput(transaction, UTXO_INDEX)

    # Start composing transaction
    print "Creating transaction on BTChip..."
    redeemScript = requestData['redeem_scripts'][signInput[0]]['redeem']
    app.startUntrustedTransaction(True, 0, [trustedInput], bytearray(redeemScript.decode('hex')))
    app.finalizeInputFull(OUTPUT)

    # Get pub key for each input
    for path, keyHash in requestData['req_keys'].iteritems():
      print "Signing..."
      keyPath = settings.KEYPATH_BASE + "/" + path
      pubKeyRaw = app.getWalletPublicKey(keyPath)
      wallets[path] = str(compress_public_key(pubKeyRaw['publicKey'])).encode('hex')
      print "Your pubkey for %s: %s" % (keyPath, wallets[path])
      assert pubKeyRaw['address'] == keyHash[0]
      signature = app.untrustedHashSign(keyPath, "")
      result['signatures'].append([binascii.hexlify(signature), signInput[1].encode('hex'), signInput[0]])


  body = {}
  body['_humans'] = "Upload this set of signatures to Coinkite."
  body['content'] = json.dumps(result)

  rootKey = app.getWalletPublicKey(settings.KEYPATH_BASE)
  messageHash = Hash(body['content'])
  print "hash: " + messageHash.encode('hex')
  body['signature'] = signMessage(app, dongle, settings.KEYPATH_BASE, messageHash.encode('hex'))
  body['signed_by'] = rootKey['address'] # Bug, should use network

  return body

def sha256(x):
  return hashlib.sha256(x).digest()

def Hash(x):
  if type(x) is unicode: x=x.encode('utf-8')
  return sha256(sha256(x))

if __name__ == "__main__":
  main()
