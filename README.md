BTChip-Armory-Signer
====================

To run the test code:

```
./setup.sh
# wait...
python sign.py --testnet
```

Setting up a new dongle
-----------------------

Fresh out of the box, the chip just needs to be loaded with a seed. If it already has one, run 
`python utils/resetChip.py`.

```
# Add --testnet to build a testnet key. They can only operate on one network at a time.
python utils/setupMnemonic.py
```

You can back up the mneomonic however you like. If you want to restore, run `python utils/restoreFromMnemnonic.py`.
The restore script also accepts the `--testnet` flag.

To generate an xpub/tpub for use with services like Coinkite:

```
# BIP32 roots are using the BIP44 standard, but they could be anything
# Mainnet
python utils/getKey.py 44h/0h/0h
# Testnet
python utils/getKey.py 44h/1h/0h
```


Notes on xpub/xpriv
-------------------

[Bip32gen](https://github.com/jmcorgan/bip32utils) (part of bip32utils) is really useful
for doing calculations on the keys, such as generating xprv/xpub at different trees.

For instance, you can use `getKey.py` to generate pubkeys and addresses at different depths.

For the sake of demonstration we're using the path m/44h/1h/0h, which is the bip0044 path for 
account 0 on testnet. Say, we want to get the xpub to send to an external service like coinkite.

To get the pubkey and address at this path, call `getKey.py`:

```bash
> python getKey.py m/44h/1h/0h

Path: 44'/1'/0'
Full Public Key: 04ce5709455899ac0593910721431224dfeb628c1f6f889baf1463d22289e3e111d075426080db7db46fa850b33a1b6b3e988e66d51b8899557d5d66eaaab28f62
Public Key: 02ce5709455899ac0593910721431224dfeb628c1f6f889baf1463d22289e3e111
Address: 1C1osyRQEJr6gZ6ynxp9nLLGe6DccZ8pRK
```

That's useful, but we don't have an xpub here and as far as I know, we can't get it from btchip utils. It's just
math though, so let's do it with bip32gen:

```
> echo 1762F9A3007DBC825D0DD9958B04880284C88A10C57CF569BB3DADF7B1027F2D | bip32gen -i entropy -o xpub,addr,pubkey -v -f - -F - -x -X m/44h/1h/0h -n 256

Creating master key and seed using 256 bits of entropy read from stdin
entropy: 1762f9a3007dbc825d0dd9958b04880284c88a10c57cf569bb3dadf7b1027f2d
Keyspec: m/44h/1h/0h
xpub:    xpub6DLDS6aRe3ZwHAEwTHBXptdKGCi14kuXggBLgb3rVnSFphA2FCMFBKUpPPkYU54AphijBJ1FWjfjKj6g7YU4pR1WhvtykMQwYDs8Se2SUQ5
addr:    1C1osyRQEJr6gZ6ynxp9nLLGe6DccZ8pRK
pubkey:  02ce5709455899ac0593910721431224dfeb628c1f6f889baf1463d22289e3e111
```


To get tprv from xprv:

```
ku xprv9zLs2b3Xog1e4gAUMFeXTkgaiAsWfJBgKTFjtCeEwSuGwtpshf2zdXALY7bFSaNNXGJRA98Xw9gaLtBMsDpSJDLDBomheqNqKtLyPga2uMG --override-network XTN
```

To get xprv:

```
echo 1762F9A3007DBC825D0DD9958B04880284C88A10C57CF569BB3DADF7B1027F2D | bip32gen -i entropy -o xpub,addr,pubkey,xprv -v -f - -F - -x -X m/44h/1h/0h -n 256
```
