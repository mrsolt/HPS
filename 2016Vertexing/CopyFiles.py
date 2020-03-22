#!/usr/local/bin/python2.7

# 
# Copy files to analysis note directory
#
#       author: Matt Solt
#

import argparse
import math
import os
import operator
import pprint
import shutil
import sys
import subprocess
import time

def main() :

    def copyfile(file1,file2):
        command = 'cp {0} {1}'.format(file1,file2)
        subprocess.Popen(command, shell=True).wait() 
        time.sleep(1)

    outdir = '/nfs/slac/g/hps2/mrsolt/hps/Data2016/analysisnoteplots/'
    tightL1L1dir = '/nfs/slac/g/hps2/mrsolt/hps/Data2016/DataMCCompare/Tight/L1L1/cutflow_L1L1'
    singleL1L1dir = '/nfs/slac/g/hps2/mrsolt/hps/Data2016/DataMCCompare/Tight/L1L1/cutflow_L1L1compare'
    tailfitsL1L1dir = '/nfs/slac/g/hps2/mrsolt/hps/Data2016/DataMCCompare/TailFits/L1L1/compare_tailfits_L1L1'
    isoplotsL1L1dir = '/nfs/slac/g/hps2/mrsolt/hps/Data2016/DataMCCompare/IsoPlots/L1L1/'
    tightL1L2dir = '/nfs/slac/g/hps2/mrsolt/hps/Data2016/DataMCCompare/Tight/L1L2/cutflow_L1L2'
    singleL1L2dir = '/nfs/slac/g/hps2/mrsolt/hps/Data2016/DataMCCompare/Tight/L1L2/cutflow_L1L2compare'
    tailfitsL1L2dir = '/nfs/slac/g/hps2/mrsolt/hps/Data2016/DataMCCompare/TailFits/L1L2/compare_tailfits_L1L2'
    isoplotsL1L2dir = '/nfs/slac/g/hps2/mrsolt/hps/Data2016/DataMCCompare/IsoPlots/L1L2/'


    copyfile('{0}compare1.pdf'.format(tightL1L1dir),'{0}{1}.pdf'.format(outdir,'tightcutflowL1L1')) #Tight Cutflow L1L1
    copyfile('{0}compare2.pdf'.format(tightL1L1dir),'{0}{1}.pdf'.format(outdir,'z0pos_excl')) #Positron IP Exclusion
    copyfile('{0}compare3.pdf'.format(tightL1L1dir),'{0}{1}.pdf'.format(outdir,'z0ele_excl')) #Electron IP Exclusion
    copyfile('{0}compare4.pdf'.format(tightL1L1dir),'{0}{1}.pdf'.format(outdir,'isocutpos_excl')) #Positron Isocut Exclusion
    copyfile('{0}compare5.pdf'.format(tightL1L1dir),'{0}{1}.pdf'.format(outdir,'isocutele_excl')) #Electron Isocut Exclusion
    copyfile('{0}compare6.pdf'.format(tightL1L1dir),'{0}{1}.pdf'.format(outdir,'v0p_excl')) #V0 Momentum Exclusion
    copyfile('{0}compare7.pdf'.format(tightL1L1dir),'{0}{1}.pdf'.format(outdir,'uncChisq_excl')) #UncChisq Exclusion
    copyfile('{0}compare8.pdf'.format(tightL1L1dir),'{0}{1}.pdf'.format(outdir,'v0proj_excl')) #V0 Projection Exclusion
    copyfile('{0}compare9.pdf'.format(tightL1L1dir),'{0}{1}.pdf'.format(outdir,'L1L1_excl')) #L1L1 Exclusion
    copyfile('{0}compare50.pdf'.format(tightL1L1dir),'{0}{1}.pdf'.format(outdir,'preselection_compare')) #Preselection Compare
    copyfile('{0}compare48.pdf'.format(tightL1L1dir),'{0}{1}.pdf'.format(outdir,'L1L1_excl_z')) #L1L1 Exclusion Vz
    copyfile('{0}compare46.pdf'.format(tightL1L1dir),'{0}{1}.pdf'.format(outdir,'v0proj_excl_z')) #V0 Projection Exclusion Vz
    copyfile('{0}compare44.pdf'.format(tightL1L1dir),'{0}{1}.pdf'.format(outdir,'uncChisq_excl_z')) #UncChisq Exclusion Vz
    copyfile('{0}compare42.pdf'.format(tightL1L1dir),'{0}{1}.pdf'.format(outdir,'v0p_excl_z')) #V0 Momentum Exclusion Vz
    copyfile('{0}compare40.pdf'.format(tightL1L1dir),'{0}{1}.pdf'.format(outdir,'isocut_excl_z')) #Isocut Exclusion Vz
    copyfile('{0}compare38.pdf'.format(tightL1L1dir),'{0}{1}.pdf'.format(outdir,'ip_excl_z')) #IP Exclusion Vz

    copyfile('{0}68.pdf'.format(tightL1L1dir),'{0}{1}.pdf'.format(outdir,'L1L1_excl_zm')) #L1L1 Exclusion Vz vs Mass
    copyfile('{0}67.pdf'.format(tightL1L1dir),'{0}{1}.pdf'.format(outdir,'voproj_excl_zm')) #V0 Projection Exclusion Vz vs Mass
    copyfile('{0}66.pdf'.format(tightL1L1dir),'{0}{1}.pdf'.format(outdir,'uncChisq_excl_zm')) #UncChisq Exclusion Vz vs Mass
    copyfile('{0}65.pdf'.format(tightL1L1dir),'{0}{1}.pdf'.format(outdir,'v0p_excl_zm')) #V0 Momentum Exclusion Vz vs Mass
    copyfile('{0}64.pdf'.format(tightL1L1dir),'{0}{1}.pdf'.format(outdir,'isocut_excl_zm')) #Isocut Exclusion Vz vs Mass
    copyfile('{0}63.pdf'.format(tightL1L1dir),'{0}{1}.pdf'.format(outdir,'ip_excl_zm')) #IP Exclusion Vz vs Mass
    copyfile('{0}62.pdf'.format(tightL1L1dir),'{0}{1}.pdf'.format(outdir,'tightcutflowL1L1_full')) #Tight Cutflow L1L1 Full

    copyfile('{0}58.pdf'.format(tightL1L1dir),'{0}{1}.pdf'.format(outdir,'L1L1_n_1_z')) #L1L1 n-1 Vz
    copyfile('{0}56.pdf'.format(tightL1L1dir),'{0}{1}.pdf'.format(outdir,'voproj_n_1_z')) #V0 Projection n-1 Vz
    copyfile('{0}54.pdf'.format(tightL1L1dir),'{0}{1}.pdf'.format(outdir,'uncChisq_n_1_z')) #UncChisq n-1 Vz
    copyfile('{0}52.pdf'.format(tightL1L1dir),'{0}{1}.pdf'.format(outdir,'v0p_n_1_z')) #V0 Momentum n-1 Vz
    copyfile('{0}50.pdf'.format(tightL1L1dir),'{0}{1}.pdf'.format(outdir,'isocut_n_1_z')) #Isocut n-1 Vz
    copyfile('{0}48.pdf'.format(tightL1L1dir),'{0}{1}.pdf'.format(outdir,'ip_n_1_z')) #IP n-1 Vz

    copyfile('{0}4.pdf'.format(singleL1L1dir),'{0}{1}.pdf'.format(outdir,'tightcuts_compare')) #Data/MC Compare Tight Cuts
    copyfile('{0}5.pdf'.format(singleL1L1dir),'{0}{1}.pdf'.format(outdir,'final_compare')) #Data/MC Compare Final Selection
    copyfile('{0}6.pdf'.format(singleL1L1dir),'{0}{1}.pdf'.format(outdir,'final_selection_cutflow')) #Compare Tight to Final Selection

    copyfile('{0}5.pdf'.format(tailfitsL1L1dir),'{0}{1}.pdf'.format(outdir,'mean_slice')) #Compare Vertex Mean
    copyfile('{0}4.pdf'.format(tailfitsL1L1dir),'{0}{1}.pdf'.format(outdir,'sigma_slice')) #Compare Vertex Resolution
    copyfile('{0}74.pdf'.format(tailfitsL1L1dir),'{0}{1}.pdf'.format(outdir,'mass_slice')) #Mass Slice Compare

    copyfile('{0}1.pdf'.format(isoplotsL1L1dir),'{0}{1}.pdf'.format(outdir,'isocut_ap100MeV_z')) #100 MeV A' Isocut Vz
    copyfile('{0}2.pdf'.format(isoplotsL1L1dir),'{0}{1}.pdf'.format(outdir,'isocut_ap80MeV_z')) #80 MeV A' Isocut Vz
    copyfile('{0}3.pdf'.format(isoplotsL1L1dir),'{0}{1}.pdf'.format(outdir,'isocut_goodbad_z')) #Good Bad Tracks Comparison
    copyfile('{0}4.pdf'.format(isoplotsL1L1dir),'{0}{1}.pdf'.format(outdir,'isocut_iso')) #Isolation Value
    copyfile('{0}5.pdf'.format(isoplotsL1L1dir),'{0}{1}.pdf'.format(outdir,'isocut_isocut))' #Isocut Value


    copyfile('{0}compare1.pdf'.format(tightL1L2dir),'{0}{1}.pdf'.format(outdir,'tightcutflowL1L2')) #Tight Cutflow L1L2
    copyfile('{0}compare2.pdf'.format(tightL1L2dir),'{0}{1}.pdf'.format(outdir,'z0pos_excl_L1L2')) #Positron IP Exclusion L1L2
    copyfile('{0}compare3.pdf'.format(tightL1L2dir),'{0}{1}.pdf'.format(outdir,'z0ele_excl_L1L2')) #Electron IP Exclusion L1L2
    copyfile('{0}compare4.pdf'.format(tightL1L2dir),'{0}{1}.pdf'.format(outdir,'isocutpos_excl_L1L2')) #Positron Isocut Exclusion L1L2
    copyfile('{0}compare5.pdf'.format(tightL1L2dir),'{0}{1}.pdf'.format(outdir,'isocutele_excl_L1L2')) #Electron Isocut Exclusion L1L2
    copyfile('{0}compare6.pdf'.format(tightL1L2dir),'{0}{1}.pdf'.format(outdir,'v0p_excl_L1L2')) #V0 Momentum Exclusion L1L2
    copyfile('{0}compare7.pdf'.format(tightL1L2dir),'{0}{1}.pdf'.format(outdir,'uncChisq_excl_L1L2')) #UncChisq Exclusion L1L2
    copyfile('{0}compare8.pdf'.format(tightL1L2dir),'{0}{1}.pdf'.format(outdir,'v0proj_excl_L1L2')) #V0 Projection Exclusion L1L2
    copyfile('{0}compare9.pdf'.format(tightL1L2dir),'{0}{1}.pdf'.format(outdir,'L1L1_excl_L1L2')) #L1L1 Exclusion L1L2
    copyfile('{0}compare50.pdf'.format(tightL1L2dir),'{0}{1}.pdf'.format(outdir,'preselection_compare_L1L2')) #Preselection Compare L1L2
    copyfile('{0}compare48.pdf'.format(tightL1L2dir),'{0}{1}.pdf'.format(outdir,'L1L1_excl_z_L1L2')) #L1L2 Exclusion Vz
    copyfile('{0}compare46.pdf'.format(tightL1L2dir),'{0}{1}.pdf'.format(outdir,'v0proj_excl_z_L1L2')) #V0 Projection Exclusion Vz L1L2
    copyfile('{0}compare44.pdf'.format(tightL1L2dir),'{0}{1}.pdf'.format(outdir,'uncChisq_excl_z_L1L2')) #UncChisq Exclusion Vz L1L2
    copyfile('{0}compare42.pdf'.format(tightL1L2dir),'{0}{1}.pdf'.format(outdir,'v0p_excl_z_L1L2')) #V0 Momentum Exclusion Vz L1L2
    copyfile('{0}compare40.pdf'.format(tightL1L2dir),'{0}{1}.pdf'.format(outdir,'isocut_excl_z_L1L2')) #Isocut Exclusion Vz L1L2
    copyfile('{0}compare38.pdf'.format(tightL1L2dir),'{0}{1}.pdf'.format(outdir,'ip_excl_z_L1L2')) #IP Exclusion Vz L1L2

    copyfile('{0}68.pdf'.format(tightL1L2dir),'{0}{1}.pdf'.format(outdir,'L1L1_excl_zm_L1L2')) #L1L2 Exclusion Vz vs Mass
    copyfile('{0}67.pdf'.format(tightL1L2dir),'{0}{1}.pdf'.format(outdir,'voproj_excl_zm_L1L2')) #V0 Projection Exclusion Vz vs Mass L1L2
    copyfile('{0}66.pdf'.format(tightL1L2dir),'{0}{1}.pdf'.format(outdir,'uncChisq_excl_zm_L1L2')) #UncChisq Exclusion Vz vs Mass L1L2
    copyfile('{0}65.pdf'.format(tightL1L2dir),'{0}{1}.pdf'.format(outdir,'v0p_excl_zm_L1L2')) #V0 Momentum Exclusion Vz vs Mass L1L2
    copyfile('{0}64.pdf'.format(tightL1L2dir),'{0}{1}.pdf'.format(outdir,'isocut_excl_zm_L1L2')) #Isocut Exclusion Vz vs Mass L1L2
    copyfile('{0}63.pdf'.format(tightL1L2dir),'{0}{1}.pdf'.format(outdir,'ip_excl_zm_L1L2')) #IP Exclusion Vz vs Mass L1L2
    copyfile('{0}62.pdf'.format(tightL1L2dir),'{0}{1}.pdf'.format(outdir,'tightcutflowL1L2_full')) #Tight Cutflow L1L1 Full L1L2

    copyfile('{0}58.pdf'.format(tightL1L2dir),'{0}{1}.pdf'.format(outdir,'L1L2_n_1_z')) #L1L2 n-1 Vz
    copyfile('{0}56.pdf'.format(tightL1L2dir),'{0}{1}.pdf'.format(outdir,'voproj_n_1_z_L1L2')) #V0 Projection n-1 Vz L1L2
    copyfile('{0}54.pdf'.format(tightL1L2dir),'{0}{1}.pdf'.format(outdir,'uncChisq_n_1_z_L1L2')) #UncChisq n-1 Vz L1L2
    copyfile('{0}52.pdf'.format(tightL1L2dir),'{0}{1}.pdf'.format(outdir,'v0p_n_1_z_L1L2')) #V0 Momentum n-1 Vz L1L2
    copyfile('{0}50.pdf'.format(tightL1L2dir),'{0}{1}.pdf'.format(outdir,'isocut_n_1_z_L1L2')) #Isocut n-1 Vz L1L2
    copyfile('{0}48.pdf'.format(tightL1L2dir),'{0}{1}.pdf'.format(outdir,'ip_n_1_z_L1L2')) #IP n-1 Vz L1L2

    copyfile('{0}4.pdf'.format(singleL1L2dir),'{0}{1}.pdf'.format(outdir,'tightcuts_compare_L1L2')) #Data/MC Compare Tight Cuts L1L2
    copyfile('{0}5.pdf'.format(singleL1L2dir),'{0}{1}.pdf'.format(outdir,'final_compare_L1L2')) #Data/MC Compare Final Selection L1L2
    copyfile('{0}6.pdf'.format(singleL1L2dir),'{0}{1}.pdf'.format(outdir,'final_selection_cutflow_L1L2')) #Compare Tight to Final Selection L1L2

    copyfile('{0}5.pdf'.format(tailfitsL1L2dir),'{0}{1}.pdf'.format(outdir,'mean_slice_L1L2')) #Compare Vertex Mean L1L2
    copyfile('{0}4.pdf'.format(tailfitsL1L2dir),'{0}{1}.pdf'.format(outdir,'sigma_slice_L1L2')) #Compare Vertex Resolution L1L2
    copyfile('{0}74.pdf'.format(tailfitsL1L2dir),'{0}{1}.pdf'.format(outdir,'mass_slice_L1L2')) #Mass Slice Compare L1L2

    copyfile('{0}1.pdf'.format(isoplotsL1L2dir),'{0}{1}.pdf'.format(outdir,'isocut_ap100MeV_z_L1L2')) #100 MeV A' Isocut Vz L1L2
    copyfile('{0}2.pdf'.format(isoplotsL1L2dir),'{0}{1}.pdf'.format(outdir,'isocut_ap80MeV_z_L1L2')) #80 MeV A' Isocut Vz L1L2
    copyfile('{0}3.pdf'.format(isoplotsL1L2dir),'{0}{1}.pdf'.format(outdir,'isocut_goodbad_z_L1L2')) #Good Bad Tracks Comparison L1L2
    copyfile('{0}4.pdf'.format(isoplotsL1L2dir),'{0}{1}.pdf'.format(outdir,'isocut_iso_L1L2')) #Isolation Value L1L2
    copyfile('{0}5.pdf'.format(isoplotsL1L2dir),'{0}{1}.pdf'.format(outdir,'isocut_isocut_L1L2))' #Isocut Value L1L2


if __name__ == "__main__" : 
    main() 

