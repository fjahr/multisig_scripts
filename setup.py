#!/usr/bin/env python3

import argparse

# 1/ Set up the hardware, then get their Xpubs at BIP48 derivation path:
#   hwi enumerate
#   hwi -t coldcard --testnet -d [DEVICE_PATH] getxpub m/48h/1h/0h/2h
#   hwi -t trezor --testnet -d [DEVICE_PATH] getxpub m/48h/1h/0h/2h

# 2/ Get key origin:
#   hwi -t trezor --testnet -d [DEVICE_PATH] getxpub m/48h
#   bx base58-decode “[XPUB @ m/48h]” | cut -c 11-18

# 3/ Construct the descriptor strings using above key origin + XPUBs
#
# 4/ Add checksums to the descriptors
#
# 5/ Add other metadata to the descriptors (active, range, timestamp, internal, watchonly)

# 6/ Create a new wallet

# 7/ Import the descriptors into the new wallet

def init():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--test', type=str, default="foo")
    args = parser.parse_args()

    print(args.test)

if __name__ == '__main__':
    init()
