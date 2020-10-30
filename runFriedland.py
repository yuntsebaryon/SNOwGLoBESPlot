#!/usr/bin/env python

import os
import glob
import argparse
import numpy as np
import matplotlib.pyplot as plt

def makePlot( flux, arrivedFile, detectedFile, oDir ):
    arrived = np.genfromtxt( arrivedFile )
    detected = np.genfromtxt( detectedFile, skip_footer=2 )
    plt.rc( 'xtick', labelsize = 20 )
    plt.rc( 'ytick', labelsize = 20 )
    plt.ylim( 0, 450 )
    plt.plot( arrived[:,0], arrived[:,1]/1.e7, linewidth = 2, label = r'Arrived/$10^7$' )
    plt.plot( detected[:,0], detected[:,1], linewidth = 2, label = 'Detected' )
    plt.xlabel( 'Energy [GeV]', fontsize = 20 )
    plt.ylabel( 'Event Rate', fontsize = 20 )
    plt.legend()
    plt.tight_layout()
    outfile = oDir + '/' + flux + '.pdf'
    plt.savefig( outfile )
    plt.close()

# def makePlot()

if __name__ == "__main__":

    parser = argparse.ArgumentParser( description = 'Run SNOwGLoBES on Alex Friedland supernova neutrino fluxes and plot them' )
    parser.add_argument( '-s', dest = 'sDir', type = str, help = 'the location of SNOwGLoBES' )
    parser.add_argument( '-o', dest = 'oDir', type = str, help = 'the directory of the output plots' )
    parser.add_argument( '-c', dest = 'dConfig', type = str, help = 'the detector resolution/smearing, default = ar40kt_DCR_THR35QENonRefl2PE', default = 'ar40kt_DCR_THR35QENonRefl2PE' )

    args = parser.parse_args()

    files = glob.glob( args.sDir + '/fluxes/rf*' )

    fluxes = []

    for file in files:
        file = os.path.split(file)[-1]
        if file.endswith( '.dat' ): file = file[:-len('.dat')]
        fluxes.append( file )

    # Run SNOwGLoBES
    for flux in fluxes:
        cmd = './supernova.pl ' + flux + ' argon_marley1_ar ' + args.dConfig
        # os.system( cmd )

    if not os.path.exists( args.oDir ):
        os.mkdir( args.oDir )

    # Make flux plots
    for flux in fluxes:
        infile = args.sDir + '/fluxes/' + flux + '.dat'
        outfile = args.sDir + '/out/' + flux + '_nue_Ar40_marley1_' + args.dConfig + '_events_smeared.dat'
        makePlot( flux, infile, outfile, args.oDir )
