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

# 7/ Import the descriptors into the new wallet

def run_hwi(args):
    cli_args = []
    for arg in args:
        cli_args.append(shlex.quote(arg))
    proc = subprocess.Popen(['hwi ' + ' '.join(cli_args)], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, shell=True)
    result = proc.communicate()
    return json.loads(result[0].decode())

def get_xpubs(num_xpubs, testnet):
    xpubs = []
    bip_32_derive_path = 'm/48h/1h/0h/2h'

    for _ in num_xpubs:
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
        xpub = run_hwi(getxpub_params)

        print(xpub)
        xpubs.append(xpub)

        print("%d XPUB extracted, please unplug and connect the next device, press Enter to continue\n", len(xpubs))
        input().lower()

    return xpubs


def init():
    parser = argparse.ArgumentParser()
    parser.add_argument("--testnet", default=False, action="store_true" , help="sign for testnet")
    parser.add_argument('-m', type=int, default=2)
    parser.add_argument('-n', type=int, default=3)
    args = parser.parse_args()

    xpubs = get_xpubs(args.testnet, args.n)
    print(xpubs)


if __name__ == '__main__':
    init()
