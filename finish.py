#!/usr/bin/env python3

import argparse

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
    parser.add_argument('-t', '--test', type=str, default="foo")
    args = parser.parse_args()

    print(args.test)

if __name__ == '__main__':
    finish()
