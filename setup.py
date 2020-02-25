#!/usr/bin/env python3

import argparse
import sys
import json
import subprocess
import shlex

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
#   ./bitcoin-cli [-testnet|-mainnet] -datadir=[DATADIR] createwallet [WALLET_NAME] true true "" true true
#   (Create a wallet that a/ has private keys disabled b/ is blank c/ has no passphrase d/ disallow coin reuse e/ is a descriptor wallet)

# 7/ Import the descriptors into the new wallet
#   ./bitcoin-cli [-testnet|-mainnet] -datadir=[DATADIR] -rpcwallet=[WALLET_NAME] importdescriptors [DESC]

def run_hwi(args):
    cli_args = []
    for arg in args:
        cli_args.append(shlex.quote(arg))
    proc = subprocess.Popen(['hwi ' + ' '.join(cli_args)], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, shell=True)
    result = proc.communicate()
    return json.loads(result[0].decode())

def run_bitcoincli(args):
    cli_args = []
    for arg in args:
        cli_args.append(shlex.quote(arg))
    
    proc = subprocess.Popen(['./bitcoin-cli ' + ' '.join(cli_args)], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, shell=True)
    result = proc.communicate()
    return json.loads(result[0].decode())

def get_descriptors(xpubs, origins):
    return ''

def create_wallet_with_descriptors(wallet_name, descriptors):
    create_args = [
        'createwallet',
        '"{}"'.format(wallet_name),
        'true',
        'true',
        '""',
        'true',
        'true'
    ]

    run_bitcoincli(create_args)

    descriptor_string = '[{{\"desc\": \"{}\", \"timestamp\": \"now\", \"internal\": false, \"label\": \"multisig_addresses\"}}]'.format(descriptors)

    import_args = [
        '-rpcwallet=' + wallet_name,
        'importdescriptors',
        descriptor_string
    ]

    run_bitcoincli(import_args)

    return True

def get_xpubs_and_origins(num_xpubs, testnet):
    xpubs = []
    key_origins = []
    bip_32_derive_path = 'm/48h/1h/0h/2h'
    origin_derive_path = 'm/48h'

    for _ in range(num_xpubs):
        result = run_hwi(['enumerate'])

        device_type = ''
        if not result:
            print("ERROR: No device detected, please check your connection");
            sys.exit()
        elif (len(result) > 1):
            print("ERROR: More than one device detected, please specify device type [-t trezor|coldcard]")
            sys.exit()
        else:
            device_type = result[0]['type']

        device_path = ''
        for dev in result:
            if dev['type'] == device_type:
                device_path = dev['path']

        getxpub_params = ['-t', device_type, '-d', device_path, 'getxpub', bip_32_derive_path]
        if testnet:
            getxpub_params.insert(0, '--testnet')
        xpub_result = run_hwi(getxpub_params)

        print(xpub_result['xpub'])
        xpubs.append(xpub_result['xpub'])

        #   hwi -t trezor --testnet -d [DEVICE_PATH] getxpub m/48h
        #   bx base58-decode “[XPUB @ m/48h]” | cut -c 11-18
        #   printf "[XPUB @ m/48h]" | base58 -dc | xxd -p -c 2048 | cut -c 11-18

        getorigin_params = ['-t', device_type, '-d', device_path, 'getxpub', origin_derive_path]
        if testnet:
            getorigin_params.insert(0, '--testnet')
        origin_result = run_hwi(getorigin_params)

        proc = subprocess.Popen(['printf {} | base58 -dc | xxd -p -c 2048 | cut -c 11-18'.format(origin_result['xpub'])], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, shell=True)
        fingerprint_result = proc.communicate()
        print(fingerprint_result[0].decode().rstrip())
        key_origins.append(fingerprint_result[0].decode().rstrip())

        print("{} XPUBs extracted, please unplug and connect the next device, press Enter to continue\n".format(len(xpubs)))
        input().lower()
    
    if len(xpubs) != len(set(xpubs)):
        print("Duplicate XPUBs detected, please try again")
        sys.exit()

    return [xpubs, key_origins]


def init():
    parser = argparse.ArgumentParser()
    parser.add_argument("--testnet", default=False, action="store_true" , help="sign for testnet")
    parser.add_argument('-wallet', type=str, default="multisig_bech32", help="name of multisig wallet")
    parser.add_argument('-m', type=int, default=2)
    parser.add_argument('-n', type=int, default=3)
    args = parser.parse_args()

    # xpubs, key_origins = get_xpubs_and_origins(args.n, args.testnet)
    xpubs = ['tpubDEi3gpBhtY2GaMUSsfukbGDQaMGGv3qiBqQ7hCkLo4uVzX2sWen9ZmG8m2f44bHpFnbe7JjVzpa2stFk5zHz355aymwrisejApq8koKnZPm', 'tpubDF2rnouQaaYrXF4noGTv6rQYmx87cQ4GrUdhpvXkhtChwQPbdGTi8GA88NUaSrwZBwNsTkC9bFkkC8vDyGBVVAQTZ2AS6gs68RQXtXcCvkP', 'tpubDF5KqurbAdsSH8S9LFGvJhv4XEZsRqWCgkXCCBYSnrNjEHxDXgzFqcKR1Q1EtFcrEqJBeTvKG2RsKhgmwCKAkHRybDve37xgWmGjzS4vgFs']
    key_origins = ['84ef4b40', '0f056943', '8375b5d4']

    print(xpubs)
    print(key_origins)

    descriptors = get_descriptors(xpubs, key_origins)
    if create_wallet_with_descriptors(args.wallet, descriptors):
        print("Successfully created a {}-of-{}, watch-only wallet: '{}'".format(args.m, args.n, args.wallet))
    else:
        print("Could not create wallet")

if __name__ == '__main__':
    init()
