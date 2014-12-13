import os, sys, inspect, struct
from btchip.btchip import *
from btchip.btchipUtils import *
from btchip.bitcoinTransaction import *
from btchip.bitcoinVarint import *
import simplejson as json
import settings, pprint, getpass, binascii, hashlib, sys, re
from ckapi import CKRequestor
import click
import textwrap
from signTxCoinkiteJSON import signCoinkiteJSON

pp = pprint.PrettyPrinter(indent=2)
apiBase = "https://api.coinkite.com"

@click.command()
@click.option('--coinkite-ref', '-c', type=str, prompt=True, help="Coinkite Reference ID of the tx you want to sign.")
@click.option('--user-refnum', '-u', type=str, help="Your user's refnum for signing.", default=settings.COINKITE_USER_REF)
@click.option('--api-key', default=settings.COINKITE_API_KEY )
@click.option('--api-secret', default=settings.COINKITE_API_SECRET )
def main(coinkite_ref, user_refnum, api_key, api_secret):
  """Co-sign transactions using the Coinkite API.

  It lists pending transactions, prompts for an ID to sign, displays the tx details
  and signs. It requires an API key with the 'co-sign' permission.
  """
  if not len(api_key) or not len(api_secret):
    print "ERROR: Specify a COINKITE_API_KEY and COINKITE_API_SECRET in settings.py or via flags."
    exit(1)

  print "This script will sign a multisig transaction using the Coinkite API."
  print "NOTE: This is a work in progress and may be buggy."

  # Get Dongle
  dongle = getDongle(False) # Bool is debug mode
  app = btchip(dongle)

  # Authenticate with dongle
  pin = getpass.getpass("PIN: ")
  app.verifyPin(pin)

  # Create a requestor object
  r = CKRequestor(str(api_key), str(api_secret))

  # Get the ref we're signing
  print "Getting transaction details..."
  tx = r.get('/v1/detail/' + coinkite_ref)
  co = r.get('/v1/co-sign/' + coinkite_ref)
  # print r.get('/v1/list/need_sigs')

  print txDetails(tx, co, printUserRefs=(not user_refnum))
  # FIXME talk to Coinkite, this is sometimes true when it shouldn't be
  # assertCondition(not tx.detail.is_completed, "This transaction is already complete!")

  if not user_refnum:
    user_refnum = raw_input("Your user ref (put this in settings.COINKITE_USER_REF in the future): ")
  assertCondition(not co.has_signed_already[user_refnum], "This transaction has already been signed by this user!")
  
  # signing time
  signTX = r.get('/v1/co-sign/' + coinkite_ref + '/' + user_refnum)
  result = signCoinkiteJSON(app, dongle, signTX.signing_info)
  putResult = r.put('/v1/co-sign/' + coinkite_ref + '/' + user_refnum + '/sign', \
    _data={'signatures': result['signatures']})

  print "Result: %s" % (putResult.message)


def txDetails(tx, co, printUserRefs=False):
  """Print pretty transaction details."""
  # Print out user refs if the user hasn't provided one, would indicate they don't know their ref
  signed = ""
  for signer in co.cosigners:
    label = signer.user_label if not printUserRefs else "%s (ref: %s)" % (signer.user_label, signer.CK_refnum)
    signed += "\n%s: %s" % (label, co.has_signed_already[signer.CK_refnum])

  d = tx.detail
  return textwrap.dedent("""
  ==--==--==--==--==--==--==--==--==--==--==--==--==

  Transaction
  ===========

  Created: %s
  Is completed? %s

  TX URL: %s
  Co-sign URL: %s

  Signed By: %s

  Memo: %s
  Coin Type: %s

  ==--==--==--==--==--==--==--==--==--==--==--==--==
  """) % (d.created_at, d.is_completed, d.detail_page, d.cosign.cosign_url, signed, d.memo, d.coin_type)

def assertCondition(condition, message):
  """Assert a condition is true. If it isn't, print message and exit."""
  if not condition:
    print message
    print "Exiting..."
    exit(1)

if __name__ == "__main__":
  main()
