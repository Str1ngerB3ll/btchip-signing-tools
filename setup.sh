#!/bin/bash

echo -e "\nBitMEX BTChip Signer setup"
echo -e "--------------------------\n"

DIR=`dirname $0`

git submodule init
git submodule update

cd $DIR/BitcoinArmory
make
cd ..

if [ ! -f ./settings.py ]; then
  cp settings.py.example settings.py
  echo "Edit settings.py before getting started."
fi
echo -e "\nSetup done.\n"
