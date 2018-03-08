#!/usr/bin/env python2.7
"""Command-line drive script for hera_cal.delay_filter"""
from hera_cal.delay_filter import Delay_Filter, delay_filter_argparser
import sys

parser = delay_filter_argparser()
a = parser.parse_args()

# Run Delay Filter
df = Delay_Filter()
df.load_data(a.infile, filetype = a.filetype)
df.run_filter(standoff = a.standoff, horizon = a.horizon, tol = a.tol, window = a.window, 
              skip_wgt = a.skip_wgt, maxiter = a.maxiter)
df.write_filtered_data(a.outfile, filetype_out=a.filetype, add_to_history = ' '.join(sys.argv), 
                       clobber = a.clobber, write_CLEAN_models = a.write_model)