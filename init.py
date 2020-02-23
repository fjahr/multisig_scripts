#!/usr/bin/env python3

import argparse
import json
import shlex
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

def run_command(args):
    cli_args = []
    for arg in args:
        cli_args.append(arg)
    #     cli_args.append(shlex.quote(arg))
    proc = subprocess.Popen(['./bitcoin-cli ' + ' '.join(cli_args)], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, shell=True)
    result = proc.communicate()
    return json.loads(result[0].decode())

def init():
    parser = argparse.ArgumentParser()
    parser.add_argument("--testnet", default=False, action="store_true" , help="create PSBT for testnet")
    parser.add_argument('-datadir', type=str, default="/Users/hugohn/Projects/multisig_wallet1")
    parser.add_argument('-wallet', type=str, default="multisig_bech32")
    parser.add_argument('-a', '--amount', type=float)
    parser.add_argument('-t', '--to', type=str)
    args = parser.parse_args()

    fund_args = ['-datadir=' + args.datadir,
                 '-rpcwallet=' + args.wallet,
                 'walletcreatefundedpsbt',
                '[]',
                '"{{\\\"{}\\\": {}}}"'.format(args.to, args.amount),
                '0',
                '"{\\\"subtractFeeFromOutputs\\\":[0], \\\"includeWatching\\\":true}"',
                'true']
    if args.datadir:
        fund_args.insert(0, '-datadir=' + args.datadir)
    if args.testnet:
        fund_args.insert(0, '-testnet')
    parsed_create = run_command(fund_args)

    decode_args = ['-datadir=' + args.datadir,
                   '-rpcwallet=' + args.wallet,
                   'decodepsbt',
                   parsed_create['psbt']]
    if args.datadir:
        fund_args.insert(0, '-datadir=' + args.datadir)
    if args.testnet:
        decode_args.insert(0, '-testnet')
    parsed_decode = run_command(decode_args)

    for out in parsed_decode['tx']['vout']:
        print('{}: {}\n'.format(out['scriptPubKey']['addresses'][0], out['value']))

if __name__ == '__main__':
    init()
