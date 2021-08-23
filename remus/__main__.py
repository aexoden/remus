#!/usr/bin/env python3

import argparse
import os
import sys

from remus import datfile


#-------------------------------------------------------------------------------
# Functions
#-------------------------------------------------------------------------------

def command_import(args: argparse.Namespace):
    dat_file = datfile.DatFile(args.dat_filename)

    for root, _, files in os.walk(args.directory):
        for filename in files:
            print(dat_file.match(os.path.join(root, filename)))


#-------------------------------------------------------------------------------
# Main Execution
#-------------------------------------------------------------------------------

parser = argparse.ArgumentParser(prog='python -m remus', description='A tool for managing emulation-related data files')
subparsers = parser.add_subparsers()

parser_scan = subparsers.add_parser('import', help='Import matching files from a given directory')
parser_scan.add_argument('directory', metavar='DIRECTORY', help='Directory to import from')
parser_scan.add_argument('dat_filename', metavar='DATFILENAME', help='The filename of the DAT file')
parser_scan.set_defaults(func=command_import)

args = parser.parse_args(sys.argv[1:])
args.func(args)
