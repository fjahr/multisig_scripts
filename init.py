#!/usr/bin/env python3

import argparse
import json
import subprocess

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
# 4/ Show receive address, change address and the amount sent to each address to the user

def init():
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--amount', type=float)
    args = parser.parse_args()

    receive_address = subprocess.run(['./bitcoin-cli',
                                      '-rpcwallet=multisig',
                                      'getnewaddress',
                                      '""',
                                      'bech32'], stdout=subprocess.PIPE)

    create_funded = subprocess.run(['./bitcoin-cli',
                                    '-rpcwallet=multisig',
                                    'walletcreatefundedpsbt',
                                    '[]',
                                    '"{\"{}\": {}}"'.format(receive_address, args.amount),
                                    '0',
                                    '"{\"subtractFeeFromOutputs\":[0], \"includeWatching\":true}"',
                                    'true'], stdout=subprocess.PIPE)

    parsed_create = json.loads(create_funded)

    decode = subprocess.run(['./bitcoin-cli',
                             'decodepsbt',
                             parsed_create['psbt']], stdout=subprocess.PIPE)

    parsed_decode = json.loads(decode)

    for out in parsed_decode['tx']['vout']:
        print('{}: {}\n'.format(out['scriptPubKey']['addresses'][0], out['value'])

if __name__ == '__main__':
    init()
