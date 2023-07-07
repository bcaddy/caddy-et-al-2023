#!/usr/bin/env python3
"""
================================================================================
 Written by Robert Caddy.

 Generates the MHD blast wave plots
================================================================================
"""

from timeit import default_timer

import collections
import functools

import matplotlib
import matplotlib.animation as animation
import matplotlib.pyplot as plt

import numpy as np
import h5py

import argparse
import pathlib

import shared_tools

plt.close('all')

# ==============================================================================
def main():
    # Check for CLI arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--in_path', help='The path to the directory that the source files are located in. Defaults to "~/Code/cholla/bin"')
    parser.add_argument('-o', '--out_path', help='The path of the directory to write the plots out to. Defaults to writing in the same directory as the input files')
    parser.add_argument('-r', '--run_cholla', action="store_true", help='Runs cholla to generate all the data')
    parser.add_argument('-f', '--figure', action="store_true", help='Generate the plots')

    args = parser.parse_args()

    if args.in_path:
        rootPath = pathlib.Path(str(args.in_path))
    else:
        rootPath = pathlib.Path(__file__).resolve().parent.parent

    if args.out_path:
        OutPath = pathlib.Path(str(args.out_path))
    else:
        OutPath = pathlib.Path(__file__).resolve().parent.parent / 'assets' / '3-mhd-tests'

    if args.run_cholla:
        shared_tools.cholla_runner(param_file_name=f'mhd_blast.txt',
                                   move_final=True,
                                   final_filename=f'mhd-blast')

    if args.figure:
        plotBlastWave(rootPath, OutPath)
        shared_tools.update_plot_entry("mhd-blast", 'python/blast-wave.py')

# ==============================================================================

# ==============================================================================
def plotBlastWave(rootPath, outPath):
    # Plotting info
    line_width         = 00.1
    suptitle_font_size = 15
    subtitle_font_size = 10
    num_contours       = 30

    # Field info
    fields = ['density', 'magnetic_energy']
    field_indices = {'density':0, 'magnetic_energy':1}

    # Setup figure
    figSizeScale = 2.                 # Scaling factor for the figure size
    figHeight    = 4.8 * figSizeScale # height of the plot in inches, default is 4.8
    figWidth     = 7.0 * figSizeScale # width of the plot in inches, default is 6.4
    fig, subPlot = plt.subplots(1, 2)#figsize = (figWidth, figHeight))

    # Whole plot settings
    # fig.suptitle(f'', fontsize=suptitle_font_size)
    fig.tight_layout()

    # Load data
    data = shared_tools.load_conserved_data('mhd-blast')
    data = shared_tools.center_magnetic_fields(data)
    data = shared_tools.slice_data(data, z_slice_loc=data['resolution'][2]//2)
    data = shared_tools.compute_velocities(data)
    data = shared_tools.compute_derived_quantities(data, data['gamma'])

    for field in fields:
        # Get info for this field
        subplot_idx = field_indices[field]
        field_data  = np.fliplr(np.rot90(data[field]))

        # Compute where the contours are
        contours = np.linspace(np.min(field_data), np.max(field_data), num_contours)

        # Plot the data
        subPlot[subplot_idx].contour(field_data, levels=num_contours, colors='black', linewidths=line_width)

        # Set ticks and grid
        subPlot[subplot_idx].tick_params(labelleft=False, labelbottom=False,
                                         bottom=False, left=False)

        # Ensure equal axis
        subPlot[subplot_idx].set_aspect('equal')

        # Set titles
        subPlot[subplot_idx].set_title(f'{shared_tools.pretty_names[field]}')

    # Save the figure and close it
    plt.savefig(outPath / f'mhd-blast.pdf', transparent = True)
    plt.close()
# ==============================================================================

if __name__ == '__main__':
    start = default_timer()
    main()
    print(f'Time to execute: {round(default_timer()-start,2)} seconds')