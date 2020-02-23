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
    parser.add_argument('-p1', '--psbt1', type=str)
    parser.add_argument('-p2', '--psbt2', type=str)
    args = parser.parse_args()

    combined = subprocess.Popen(['./bitcoin-cli',
                                '-testnet',
                                '-rpcwallet=multisig',
                                'combinepsbt',
                                args.psbt1,
                                args.psbt2], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

    out, err = combined.communicate()
    parsed_combined = json.load(out)

    finalized = subprocess.Popen(['./bitcoin-cli',
                                '-testnet',
                                '-rpcwallet=multisig',
                                'decoderawtransaction',
                                parsed_combined.psbt], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

    out, err = finalized.communicate()
    parsed_finalized = json.load(out)

    decoded = subprocess.Popen(['./bitcoin-cli',
                                '-testnet',
                                '-rpcwallet=multisig',
                                'finalizepsbt',
                                parsed_finalized.hex], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

    out, err = decoded.communicate()
    parsed_decoded = json.load(out)

    print(parsed_decoded)

    sys.stdout.write("Send this transaction? [y/n]")
    choice = raw_input().lower()

    if choice == 'y':
        subprocess.Popen(['./bitcoin-cli',
                                '-testnet',
                                '-rpcwallet=multisig',
                                'sendrawtransaction',
                                parsed_finalized.hex], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        print("sent!")
    else:
        print("not sent!")

if __name__ == '__main__':
    finish()
