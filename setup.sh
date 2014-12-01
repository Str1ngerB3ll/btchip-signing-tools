#!/bin/bash

echo "This script gets you set up with bitmex-btchip-signer."

pip install cython hidapi pyusb
python setup.py develop
