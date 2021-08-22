#!/usr/bin/env python3

import sys

from remus import datfile

dat_file = datfile.DatFile(sys.argv[1])
print(dat_file.match(sys.argv[2]))
