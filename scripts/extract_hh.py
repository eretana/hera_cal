#! /usr/bin/env python
import os
import argparse
import pyuvdata
from hera_cal.version import version_info
import pyuvdata.utils as uvutils
import numpy as np

parser = argparse.ArgumentParser(description='Extract HERA hex antennas from data '
                                 'file, and save with new extension.')
parser.add_argument('--extension', type=str, help='Extension to be appended to '
                    'filename for output. Default="HH".', default='HH')
parser.add_argument('--filetype', type=str, help='Input and output file type. '
                    'Allowed values are "miriad" (default), and "uvfits".',
                    default='miriad')
parser.add_argument('--fixuvws', action='store_true', help='Optional flag to '
                    'use antenna positions to replace uvws.')
parser.add_argument('files', metavar='files', type=str, nargs='+',
                    help='Files to be processed.')
args = parser.parse_args()

uv = pyuvdata.UVData()
for filename in args.files:
    if args.filetype is 'miriad':
        uv.read_miriad(filename)
    elif args.filetype is 'uvfits':
        uv.read_uvfits(filename)
    else:
        raise ValueError('Unrecognized file type ' + str(args.filetype))
    st_type_str = uv.extra_keywords.pop('st_type').replace('\x00', '')
    st_type_list = st_type_str[1:-1].split(', ')
    ind = [i for i, x in enumerate(st_type_list) if x == 'herahex']
    uv.select(antenna_nums=uv.antenna_numbers[ind])
    uv.history += ' Hera Hex antennas selected with hera_cal/scripts/extract_hh.py' \
                  ', hera_cal version: ' + str(version_info) + '.'
    if args.fixuvws:
        antpos = uv.antenna_positions + uv.telescope_location
        antpos = uvutils.ENU_from_ECEF(antpos.T, *uv.telescope_location_lat_lon_alt).T
        antmap = -np.ones(np.max(uv.antenna_numbers) + 1, dtype=int)
        for i, ant in enumerate(uv.antenna_numbers):
            antmap[ant] = i
        uv.uvw_array = antpos[antmap[uv.ant_2_array], :] - antpos[antmap[uv.ant_1_array], :]
    if args.filetype is 'miriad':
        base, ext = os.path.splitext(filename)
        uv.write_miriad(base + '.' + args.extension + ext)
    else:
        base, ext = os.path.splitext(filename)
        uv.write_uvfits(base + args.extension + ext)
