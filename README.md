BTChip-Signing-Tools
====================

This is a collection of scripts used for signing messages and transactions with the BTChip HW.1 and Ledger Wallets (available on https://www.ledgerwallet.com)

This is very much a work in progress, and many things will change. 

Setup
-----

Usually, you can set this module up just by executing `python setup.py develop`.

Unfortunately, on OS X, you might see issues installing cython-hidapi. (`hid.c does not exist`). If so,
run `sudo ./setup.sh`, which will install from source.

Usage
-----

See the sections below for usage. If your dongle is already set up, all you need is the xpub/tpub
to get started with Coinkite, which you can get with the `utils/getKey.py` script. See below for an example.

Once you are set up, see the "Co-Signing" section below.

Setting up a new dongle
-----------------------

Fresh out of the box, the chip just needs to be loaded with a seed. If it already has one, run 
`python utils/resetChip.py`.

```
# Add --testnet to build a testnet key. They can only operate on one network at a time.
python utils/setupMnemonic.py
```

You can back up the mnemonic however you like. If you want to restore, run `python utils/restoreFromMnemonic.py`.
The restore script also accepts the `--testnet` flag.

To generate an xpub/tpub for use with services like Coinkite:

```
# BIP32 roots are using the BIP44 standard, but they could be anything
# Mainnet
python utils/getKey.py m/44h/0h/0h
# Testnet
python utils/getKey.py m/44h/1h/0h
```

Co-signing a Coinkite request (API) 
-----------------------------------

Coinkite now allows signing via their API. It is generally faster and easier to use but takes a bit of setup.

To sign via the API, generate an API key with the `co-sign` and `read` permissions, and fill out `settings.py`
with your API key (see settings.py.example).

To sign via the API you just need the CK ref num, for example `A32A0845AD-1B6D51`:

```
# If the CK Ref Num is not provided, the script will prompt for it.
python signTxCoinkiteAPI.py -c <CK Ref Num>
```

On your first sign, you will have to enter the reference ID for your user account. You can copy/paste it from
the list of co-signers attached to the transaction. You can then paste it into your `settings.py` so you won't
get prompted again.

Co-signing a Coinkite request (JSON/Browser)
--------------------------------------------

If you don't want to fool around with API keys, simply download the signing JSON (click `advanced` on the 
co-signing page).

```
python signTxCoinkiteJSON.py <JSON Path>
```

This will generate a JSON file in this folder that you can upload back to Coinkite.

----

Notes on BIP32 paths
--------------------

There are two competing formats for BIP32 paths. These are equivalent and both are accepted as parameters:

```
m/44h/0h/0h
44'/0'/0'
```

The `h` or `'` means it's a hardened key. For more on that, see the 
[BIP32 Spec](https://github.com/bitcoin/bips/blob/master/bip-0032.mediawiki#implications).

Notes on xpub/xpriv
-------------------

You can use `getKey.py` to generate pubkeys and addresses at different depths.

For the sake of demonstration we're using the path m/44h/1h/0h, which is the bip0044 path for 
account 0 on testnet. Say, we want to get the xpub to send to an external service like coinkite.

To get the pubkey and address at this path, call `getKey.py`:

```bash
> python getKey.py m/44h/1h/0h

Path: 44'/1'/0'
Full Public Key: 04ce5709455899ac0593910721431224dfeb628c1f6f889baf1463d22289e3e111d075426080db7db46fa850b33a1b6b3e988e66d51b8899557d5d66eaaab28f62
Public Key: 02ce5709455899ac0593910721431224dfeb628c1f6f889baf1463d22289e3e111
Address: 1C1osyRQEJr6gZ6ynxp9nLLGe6DccZ8pRK
xpub: xpub6DLDS6aRe3ZwHAEwTHBXptdKGCi14kuXggBLgb3rVnSFphA2FCMFBKUpPPkYU54AphijBJ1FWjfjKj6g7YU4pR1WhvtykMQwYDs8Se2SUQ5
tpub: tpubDMr6xR7WkFfom4whA8aygMBgxiCH7d4dsRSGqg7qAtKPA6A9JKbPHvmycsU2aaXL2A6sQq4wSQhC5Par5DsSxDGv8oGcqBWtU2LykdpPtuv
```

[Bip32gen](https://github.com/jmcorgan/bip32utils) (part of bip32utils) is really useful
for doing calculations on the keys, such as generating xprv/xpub at different trees.

For testing purposes, to get xprv, given a seed:

```
echo 1762F9A3007DBC825D0DD9958B04880284C88A10C57CF569BB3DADF7B1027F2D | bip32gen -i entropy -o xpub,addr,pubkey,xprv -v -f - -F - -x -X m/44h/1h/0h -n 256
```

To get tprv from xprv (`ku` comes from [pycoin](https://github.com/richardkiss/pycoin)):

```
ku xprv9zLs2b3Xog1e4gAUMFeXTkgaiAsWfJBgKTFjtCeEwSuGwtpshf2zdXALY7bFSaNNXGJRA98Xw9gaLtBMsDpSJDLDBomheqNqKtLyPga2uMG --override-network XTN
```


