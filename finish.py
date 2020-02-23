#!/usr/bin/env python3

import argparse
import json
import subprocess
import sys

# 1/ Combine PSBTs:
#   ./bitcoin-cli [-testnet|-mainnet] -datadir=[DATADIR] -rpcwallet=[WALLET] combinepsbt [PSBT1, PSBT2]

# 2/ Finalize PSBT:
#   ./bitcoin-cli [-testnet|-mainnet] -datadir=[DATADIR] -rpcwallet=[WALLET] finalizepsbt [PSBT]

# 3/ Decode raw transaction, show addresses and amounts one more time
#   ./bitcoin-cli [-testnet|-mainnet] -datadir=[DATADIR] -rpcwallet=[WALLET] decoderawtransaction [RAW_TX]

# 4/ Send raw transaction
#   ./bitcoin-cli [-testnet|-mainnet] -datadir=[DATADIR] -rpcwallet=[WALLET] sendrawtransaction [RAW_TX]

def finish():
    parser = argparse.ArgumentParser()
    parser.add_argument('-datadir', type=str, default="/Users/hugohn/Projects/multisig_wallet1")
    parser.add_argument('-p1', '--psbt1', type=str)
    parser.add_argument('-p2', '--psbt2', type=str)
    args = parser.parse_args()

    combine_args = [
        'combinepsbt',
        '\'["{}", "{}"]\''.format(args.psbt1, args.psbt2)
    ]
    if args.datadir:
        combine_args.insert(0, '-datadir=' + args.datadir)

    combined = subprocess.Popen(['./bitcoin-cli ' + ' '.join(combine_args)], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, shell=True)
    combined_result = combined.communicate()[0].decode().rstrip()

    finalize_args = [
        'finalizepsbt'
        ' "{}"'.format(combined_result)
    ]
    if args.datadir:
        finalize_args.insert(0, '-datadir=' + args.datadir)
    finalized = subprocess.Popen(['./bitcoin-cli ' + ' '.join(finalize_args)], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, shell=True)

    result = finalized.communicate()
    raw_tx = json.loads(result[0].decode())['hex']

    decode_args = [
        'decoderawtransaction',
        raw_tx
    ]
    if args.datadir:
        decode_args.insert(0, '-datadir=' + args.datadir)

    decoded = subprocess.Popen(['./bitcoin-cli ' + ' '.join(decode_args)], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, shell=True)

    result = decoded.communicate()
    parsed_decoded = json.loads(result[0].decode())

    print(parsed_decoded)

    sys.stdout.write("Send this transaction? [y/n]")
    choice = input().lower()

    if choice == 'y':
        send_args = [
            'sendrawtransaction',
            raw_tx
        ]
        if args.datadir:
            send_args.insert(0, '-datadir=' + args.datadir)
        send = subprocess.Popen(['./bitcoin-cli ' + ' '.join(send_args)], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, shell=True)
        result = send.communicate()
        print("sent!")
    else:
        print("not sent!")

if __name__ == '__main__':
    finish()
