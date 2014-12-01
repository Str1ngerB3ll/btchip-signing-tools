#!/bin/bash

# For getting a new server up and running
# Must be run with sudo
if [ "$(id -u)" != "0" ]; then
  echo "This script must be run as root (sudo bash setup.sh)" 1>&2
  exit 1
fi

echo "This script gets you set up with bitmex-btchip-signer."

pip install cython

# Install hidapi
git clone https://github.com/trezor/cython-hidapi.git
cd cython-hidapi
git submodule init
git submodule update
python setup.py build
python setup.py install

# Setup this module
cd ..
python setup.py develop
