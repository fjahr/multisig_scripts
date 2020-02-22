#!/usr/bin/env python3

import argparse

def finish():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--test', type=str, default="foo")
    args = parser.parse_args()

    print(args.test)

if __name__ == '__main__':
    finish()
