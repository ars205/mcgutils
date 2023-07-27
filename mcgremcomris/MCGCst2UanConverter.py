'''
name: MCGCst2UanConverter.py
type: script
import: from MCGCst2UanConverter import MCGCst2UanConverter (or MCGConvert_multiple_files)
version: 1.0
author: Artan Salihu, Le Hao
contact: artan.salihu@tuwien.ac.at
date: 2023-07-27
website: https://www.artansalihu.com, https://mcg-deep-wrt.netlify.app/deep-wrt/utilities/
license: MIT
dependencies: numpy
description: This script converts the output of CST pattern into a UAN pattern file useful for Remcom WIS Antenna Design.
'''

import numpy as np

def MCGCst2UanConverter(filename, output_filename):
    '''
    This function converts the output of CST pattern into a UAN pattern file useful for Remcom WIS Antenna Design.
    The input file must be a text file with the following format:
    theta phi gain_theta phase_theta gain_phi phase_phi gain_total phase_total (all in degrees) and the first two lines must be skipped.
    The output file is a UAN file with the following format:
    begin_<parameters>
    format free
    phi_min 0.0000000
    phi_max 360.0000
    phi_inc 1.000000
    theta_min 0.0000000
    theta_max 180.0000
    theta_inc 1.000000
    complex
    mag_phase
    pattern field
    magnitude linear
    maximum_gain 0.0000000
    direction degrees
    end_<parameters>
    theta phi gain_theta gain_phi phase_theta phase_phi (all in degrees) and the first two lines must be skipped.

    Arguments:
    filename -- name of the input file
    output_filename -- name of the output file

    Returns:
    None
    '''
    # Read data from text file
    data = np.loadtxt(filename, skiprows=2)

    # Extract columns
    theta = data[:, 0]
    phi = data[:, 1]
    gain_theta = data[:, 3]
    gain_phi = data[:, 5]
    phase_theta = data[:, 4]
    phase_phi = data[:, 6]

    # Open output file
    with open(output_filename, 'w') as fid:
        # Write header
        fid.write('begin_<parameters>\n')
        fid.write('format free\n')
        fid.write('phi_min 0.0000000\n')
        fid.write('phi_max 360.0000\n')
        fid.write('phi_inc 1.000000\n')
        fid.write('theta_min 0.0000000\n')
        fid.write('theta_max 180.0000\n')
        fid.write('theta_inc 1.000000\n')
        fid.write('complex\n')
        fid.write('mag_phase\n')
        fid.write('pattern field\n')
        fid.write('magnitude linear\n')
        fid.write('maximum_gain 0.0000000\n')
        fid.write('direction degrees\n')
        fid.write('end_<parameters>\n')

        # Write body
        for i in range(data.shape[0]):
            fid.write('{:.6f} {:.6f} {:.6e} {:.6e} {:.6f} {:.6f}\n'.format(
                theta[i], phi[i], gain_theta[i], gain_phi[i], phase_theta[i], phase_phi[i]))

# If multiple files are needed to be converted, use
def MCGConvert_multiple_files(input_files, output_files):
    '''
    This method converts multiple files at once.
    Arguments:
    input_files -- list of input files to be converted
    output_files -- list of converted files

    Returns:
    None
    '''
    for input_file, output_file in zip(input_files, output_files):
        MCGCst2UanConverter(input_file, output_file)

# Example of usage (for multiple files)
if __name__ == '__main__':
    input_files = ['farfield (f=26) [Zmax(1)]_32.txt', 'farfield (f=26) [Zmax(17)]_32.txt']
    output_files = ['RIS_LE_Rx_Pattern_1.uan', 'RIS_LE_Tx_Pattern_1.uan']
    MCGConvert_multiple_files(input_files, output_files)