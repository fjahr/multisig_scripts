#!/usr/bin/env python3

import argparse

# 1/ Generate a new receive address:
#   ./bitcoin-cli [-testnet|-mainnet] -datadir=[DATADIR] -rpcwallet=[WALLET] getnewaddress "test_addr" bech32
#
# 2/ Create funded PSBT:
#   ./bitcoin-cli [-testnet|-mainnet] -datadir=[DATADIR] -rpcwallet=[WALLET] walletcreatefundedpsbt [] "{\"[SEND_TO_ADDR]\": [AMOUNT]}" 0 "{\"subtractFeeFromOutputs\":[0], \"includeWatching\":true}" true
# *Note: last 'true' param means include BIP32 derivation paths in the PSBT
#
# 3/ Decode PSBT:
#   ./bitcoin-cli [-testnet|-mainnet] -datadir=[DATADIR] decodepsbt [PSBT]
#
# 4/ Show receive and change address to the user

def init():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--test', type=str, default="foo")
    args = parser.parse_args()

    print(args.test)

if __name__ == '__main__':
    init()
