#!/usr/bin/env python3

import argparse
import json
import os
import sys

from remus import datfile


#-------------------------------------------------------------------------------
# Functions
#-------------------------------------------------------------------------------

def command_import(dat_files: dict[str, list[datfile.DatFile]], args: argparse.Namespace):
    for root, _, files in os.walk(args.directory):
        for filename in files:
            for _, system_dat_files in dat_files.items():
                for dat_file in system_dat_files:
                    result = dat_file.match(os.path.join(root, filename))

                    if result:
                        print(result)


def load_config():
    if not os.path.exists('remus.json'):
        print('Configuration file remus.json does not exist', file=sys.stderr)
        sys.exit(1)

    with open('remus.json') as f:
        return json.load(f)


#-------------------------------------------------------------------------------
# Main Execution
#-------------------------------------------------------------------------------

config = load_config()

dat_path = os.path.abspath(config['paths']['dats'])
dat_files: dict[str, list[datfile.DatFile]] = {}

for system, data in config['systems'].items():
    dat_files[system] = [datfile.DatFile(os.path.join(dat_path, filename)) for filename in data['dats']]

parser = argparse.ArgumentParser(prog='python -m remus', description='A tool for managing emulation-related data files')
subparsers = parser.add_subparsers()

parser_import = subparsers.add_parser('import', help='Import matching files from a given directory')
parser_import.add_argument('directory', metavar='DIRECTORY', help='Directory to import from')
parser_import.set_defaults(func=command_import)

args = parser.parse_args(sys.argv[1:])
args.func(dat_files, args)
