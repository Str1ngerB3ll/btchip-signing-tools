#!/bin/bash

echo "BitMEX BTChip Signer setup."

git submodule init
git submodule update

cd BitcoinArmory
touch __init__.py
make

echo "Setup done."
