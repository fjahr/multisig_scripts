#!/usr/bin/env python3

import argparse
import json
import shlex
import subprocess
import sys

# ./sign.py [-t DEVICE_TYPE] [--testnet] "PSBT"

def run_hwi(args):
    cli_args = []
    for arg in args:
        cli_args.append(shlex.quote(arg))
    proc = subprocess.Popen(['hwi ' + ' '.join(cli_args)], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, shell=True)
    result = proc.communicate()
    return json.loads(result[0].decode())

def sign():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--type', type=str, default="")
    parser.add_argument("--testnet", default=False, action="store_true" , help="sign for testnet")
    parser.add_argument('psbt', type=str, default="")

    args = parser.parse_args()

    if not args.psbt:
        print("ERROR: Empty PSBT");
        sys.exit()

    # 1/ Get HWI path for device
    #   hwi enumerate
    #
    # 2/ Sign PSBT with hardware wallet
    #   hwi -t trezor [--testnet] -d [DEVICE_PATH] signtx [PSBT]
    result = run_hwi(['enumerate'])

    device_type = ''
    if not result:
        print("ERROR: No device detected, please check your connection");
        sys.exit()
    elif (len(result) > 1) and (not args.type):
        print("ERROR: More than one device detected, please specify device type [-t trezor|coldcard]")
        sys.exit()
    else:
        device_type = result[0]['type']
    
    device_path = ''
    for dev in result:
        if dev['type'] == device_type:
            device_path = dev['path']

    hwi_params = ['-t', device_type, '-d', device_path, 'signtx', args.psbt]
    if args.testnet:
        hwi_params.insert(0, '--testnet')
    sign_result = run_hwi(hwi_params)
    print(sign_result)

if __name__ == '__main__':
    sign()
