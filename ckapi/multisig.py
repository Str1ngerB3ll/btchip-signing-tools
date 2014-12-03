#
# Transaction Co-Signing for Coinkite API
#
# Full docs at: https://docs.coinkite.com/
# 
# Copyright (C) 2014 Coinkite Inc. (https://coinkite.com) ... See LICENSE.md
#

def cosign_spend_request(xprvkey_or_wallet, req_keys, inputs, xpub_check):
    '''
        Sign the inputs of a transaction, given the sighashs and subkey paths for each input

    Args:
        xprvkey_or_wallet = 111-char base58 encoded serialization of BIP32 wallet
                            or pycoin.key.BIP32Node object (w/ private key)

        req_keys = dictionary: key is subpath ('a/b/c', but only 'a' for now as a string)
                    value is tuple: (address, public pair) ... optional checking data

        inputs = list of by transaction input: (subpath, sighash_all value)

    Returns:
        list of 3-tuples: (der-encoded signature, sighash, subpath)

    '''

    # We need just these features from pycoin <https://github.com/richardkiss/pycoin>
    from pycoin import ecdsa
    from pycoin.key.BIP32Node import BIP32Node
    from pycoin.tx.script import der
    
    # We need a BIP32 "wallet" for the root of all keys.
    if isinstance(xprvkey_or_wallet, basestring):
        wallet = BIP32Node.from_wallet_key(xprvkey_or_wallet.strip())
    else:
        wallet = xprvkey_or_wallet

    # Verify we are looking at the right extended private key
    check = wallet.hwif(as_private = False)[-len(xpub_check):]
    if check != xpub_check:
        raise ValueError("This private key isn't the right one for xpub...%s" % xpub_check)

    # Make the right subkey for each inputs
    wallets = {}
    for sp, (addr_check, ppair) in req_keys.items():
        w = wallet.subkey_for_path(sp)
        assert w.bitcoin_address() == addr_check
        assert w.public_pair() == tuple(ppair)
        wallets[sp] = w

    # Generate a signature for each input required
    sigs = []
    SIGHASH_ALL = 1
    order = ecdsa.generator_secp256k1.order()
    for sp, sighash in inputs:
        sighash_int = int(sighash, 16)
        r,s = ecdsa.sign(ecdsa.generator_secp256k1, wallets[sp].secret_exponent(), sighash_int)
        if s + s > order:
            s = order - s
        sig = der.sigencode_der(r, s) + chr(SIGHASH_ALL)
        sigs.append((sig.encode('hex'), sighash, sp))

    return sigs

