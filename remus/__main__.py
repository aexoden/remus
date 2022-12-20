#!/usr/bin/env python3

import argparse
import json
import os
import shutil
import sys

from remus import datfile


#-------------------------------------------------------------------------------
# Functions
#-------------------------------------------------------------------------------

def command_import(library_path: str, dat_files: dict[str, list[datfile.DatFile]], args: argparse.Namespace):
    import_count = 0

    for root, _, files in os.walk(args.directory):
        for filename in sorted(files):
            for system, system_dat_files in dat_files.items():
                for dat_file in system_dat_files:
                    source_filename = os.path.join(root, filename)
                    result = dat_file.match(source_filename)

                    if result:
                        target_filename = os.path.join(library_path, system, result.region, result.name)

                        if os.path.exists(target_filename):
                            print(f'{target_filename} already exists... skipping!')
                        else:
                            os.makedirs(os.path.dirname(target_filename), exist_ok=True)
                            shutil.move(source_filename, target_filename)
                            print(f'{source_filename} -> {target_filename}')
                            import_count += 1

    print(f'Imported {import_count} files')


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

library_path = os.path.abspath(config['paths']['library'])

if not os.path.exists(library_path):
    print(f'Library path {library_path} does not exist', file=sys.stderr)
    sys.exit(2)

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
args.func(library_path, dat_files, args)
