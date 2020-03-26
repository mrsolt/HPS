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
        time.sleep(0.1)

    outdir = '/nfs/slac/g/hps2/mrsolt/hps/Data2016/analysisnoteplots/'
    outdirSelection = '{0}/selection/'.format(outdir)
    outdirResults = '{0}/results/'.format(outdir)
    outdirMassRes = '{0}/MassRes/'.format(outdir)

    tightL1L1dir = '/nfs/slac/g/hps2/mrsolt/hps/Data2016/DataMCCompare/Tight/L1L1/cutflow_L1L1'
    singleL1L1dir = '/nfs/slac/g/hps2/mrsolt/hps/Data2016/DataMCCompare/Tight/L1L1/singleV0_L1L1_compare'
    tailfitsL1L1dir = '/nfs/slac/g/hps2/mrsolt/hps/Data2016/DataMCCompare/TailFits/L1L1/compare_tailfits_L1L1'
    isoplotsL1L1dir = '/nfs/slac/g/hps2/mrsolt/hps/Data2016/DataMCCompare/IsoPlots/L1L1/isoplots_L1L1'
    applotsL1L1dir = '/nfs/slac/g/hps2/mrsolt/hps/Data2016/MC/ap-beam/Tight/L1L1/ap-beam_'
    massResL1L1dir = '/nfs/slac/g/hps2/mrsolt/hps/Data2016/MC/ap-beam/Tight/MassRes/L1L1/massRes_L1L1'
    tightL1L2dir = '/nfs/slac/g/hps2/mrsolt/hps/Data2016/DataMCCompare/Tight/L1L2/cutflow_L1L2'
    singleL1L2dir = '/nfs/slac/g/hps2/mrsolt/hps/Data2016/DataMCCompare/Tight/L1L2/singleV0_L1L2_compare'
    tailfitsL1L2dir = '/nfs/slac/g/hps2/mrsolt/hps/Data2016/DataMCCompare/TailFits/L1L2/compare_tailfits_L1L2'
    isoplotsL1L2dir = '/nfs/slac/g/hps2/mrsolt/hps/Data2016/DataMCCompare/IsoPlots/L1L2/isoplots_L1L2'
    applotsL1L2dir = '/nfs/slac/g/hps2/mrsolt/hps/Data2016/MC/ap-beam/Tight/L1L2/ap-beam_'
    massResL1L2dir = '/nfs/slac/g/hps2/mrsolt/hps/Data2016/MC/ap-beam/Tight/MassRes/L1L2/massRes_L1L2'

    copyfile('{0}_compare1.pdf'.format(tightL1L1dir),'{0}{1}.pdf'.format(outdirSelection,'tightcutflowL1L1')) #Tight Cutflow L1L1
    copyfile('{0}_compare2.pdf'.format(tightL1L1dir),'{0}{1}.pdf'.format(outdirSelection,'z0pos_excl')) #Positron IP Exclusion
    copyfile('{0}_compare3.pdf'.format(tightL1L1dir),'{0}{1}.pdf'.format(outdirSelection,'z0ele_excl')) #Electron IP Exclusion
    copyfile('{0}_compare4.pdf'.format(tightL1L1dir),'{0}{1}.pdf'.format(outdirSelection,'isocutpos_excl')) #Positron Isocut Exclusion
    copyfile('{0}_compare5.pdf'.format(tightL1L1dir),'{0}{1}.pdf'.format(outdirSelection,'isocutele_excl')) #Electron Isocut Exclusion
    copyfile('{0}_compare6.pdf'.format(tightL1L1dir),'{0}{1}.pdf'.format(outdirSelection,'v0p_excl')) #V0 Momentum Exclusion
    copyfile('{0}_compare7.pdf'.format(tightL1L1dir),'{0}{1}.pdf'.format(outdirSelection,'uncChisq_excl')) #UncChisq Exclusion
    copyfile('{0}_compare8.pdf'.format(tightL1L1dir),'{0}{1}.pdf'.format(outdirSelection,'v0proj_excl')) #V0 Projection Exclusion
    copyfile('{0}_compare9.pdf'.format(tightL1L1dir),'{0}{1}.pdf'.format(outdirSelection,'L1L1_excl')) #L1L1 Exclusion
    copyfile('{0}_compare50.pdf'.format(tightL1L1dir),'{0}{1}.pdf'.format(outdirSelection,'preselection_compare')) #Preselection Compare
    copyfile('{0}_compare48.pdf'.format(tightL1L1dir),'{0}{1}.pdf'.format(outdirSelection,'L1L1_excl_z')) #L1L1 Exclusion Vz
    copyfile('{0}_compare46.pdf'.format(tightL1L1dir),'{0}{1}.pdf'.format(outdirSelection,'v0proj_excl_z')) #V0 Projection Exclusion Vz
    copyfile('{0}_compare44.pdf'.format(tightL1L1dir),'{0}{1}.pdf'.format(outdirSelection,'uncChisq_excl_z')) #UncChisq Exclusion Vz
    copyfile('{0}_compare42.pdf'.format(tightL1L1dir),'{0}{1}.pdf'.format(outdirSelection,'v0p_excl_z')) #V0 Momentum Exclusion Vz
    copyfile('{0}_compare40.pdf'.format(tightL1L1dir),'{0}{1}.pdf'.format(outdirSelection,'isocut_excl_z')) #Isocut Exclusion Vz
    copyfile('{0}_compare38.pdf'.format(tightL1L1dir),'{0}{1}.pdf'.format(outdirSelection,'ip_excl_z')) #IP Exclusion Vz

    copyfile('{0}68.pdf'.format(tightL1L1dir),'{0}{1}.pdf'.format(outdirSelection,'L1L1_excl_zm')) #L1L1 Exclusion Vz vs Mass
    copyfile('{0}67.pdf'.format(tightL1L1dir),'{0}{1}.pdf'.format(outdirSelection,'voproj_excl_zm')) #V0 Projection Exclusion Vz vs Mass
    copyfile('{0}66.pdf'.format(tightL1L1dir),'{0}{1}.pdf'.format(outdirSelection,'uncChisq_excl_zm')) #UncChisq Exclusion Vz vs Mass
    copyfile('{0}65.pdf'.format(tightL1L1dir),'{0}{1}.pdf'.format(outdirSelection,'v0p_excl_zm')) #V0 Momentum Exclusion Vz vs Mass
    copyfile('{0}64.pdf'.format(tightL1L1dir),'{0}{1}.pdf'.format(outdirSelection,'isocut_excl_zm')) #Isocut Exclusion Vz vs Mass
    copyfile('{0}63.pdf'.format(tightL1L1dir),'{0}{1}.pdf'.format(outdirSelection,'ip_excl_zm')) #IP Exclusion Vz vs Mass
    copyfile('{0}62.pdf'.format(tightL1L1dir),'{0}{1}.pdf'.format(outdirSelection,'tightcutflowL1L1_full')) #Tight Cutflow L1L1 Full

    copyfile('{0}58.pdf'.format(tightL1L1dir),'{0}{1}.pdf'.format(outdirSelection,'L1L1_n_1_z')) #L1L1 n-1 Vz
    copyfile('{0}56.pdf'.format(tightL1L1dir),'{0}{1}.pdf'.format(outdirSelection,'voproj_n_1_z')) #V0 Projection n-1 Vz
    copyfile('{0}54.pdf'.format(tightL1L1dir),'{0}{1}.pdf'.format(outdirSelection,'uncChisq_n_1_z')) #UncChisq n-1 Vz
    copyfile('{0}52.pdf'.format(tightL1L1dir),'{0}{1}.pdf'.format(outdirSelection,'v0p_n_1_z')) #V0 Momentum n-1 Vz
    copyfile('{0}50.pdf'.format(tightL1L1dir),'{0}{1}.pdf'.format(outdirSelection,'isocut_n_1_z')) #Isocut n-1 Vz
    copyfile('{0}48.pdf'.format(tightL1L1dir),'{0}{1}.pdf'.format(outdirSelection,'ip_n_1_z')) #IP n-1 Vz

    copyfile('{0}4.pdf'.format(singleL1L1dir),'{0}{1}.pdf'.format(outdirSelection,'tightcuts_compare')) #Data/MC Compare Tight Cuts
    copyfile('{0}5.pdf'.format(singleL1L1dir),'{0}{1}.pdf'.format(outdirSelection,'final_compare')) #Data/MC Compare Final Selection
    copyfile('{0}6.pdf'.format(singleL1L1dir),'{0}{1}.pdf'.format(outdirSelection,'final_selection_cutflow')) #Compare Tight to Final Selection

    copyfile('{0}5.pdf'.format(tailfitsL1L1dir),'{0}{1}.pdf'.format(outdirResults,'mean_slice')) #Compare Vertex Mean
    copyfile('{0}4.pdf'.format(tailfitsL1L1dir),'{0}{1}.pdf'.format(outdirResults,'sigma_slice')) #Compare Vertex Resolution
    copyfile('{0}74.pdf'.format(tailfitsL1L1dir),'{0}{1}.pdf'.format(outdirResults,'mass_slice')) #Mass Slice Compare

    copyfile('{0}3.pdf'.format(isoplotsL1L1dir),'{0}{1}.pdf'.format(outdirSelection,'isocut_ap100MeV_z')) #100 MeV A' Isocut Vz
    copyfile('{0}4.pdf'.format(isoplotsL1L1dir),'{0}{1}.pdf'.format(outdirSelection,'isocut_ap100MeV_isocut_z')) #100 MeV A' Isocut vs Vz
    copyfile('{0}5.pdf'.format(isoplotsL1L1dir),'{0}{1}.pdf'.format(outdirSelection,'isocut_ap80MeV_z')) #80 MeV A' Isocut Vz
    copyfile('{0}6.pdf'.format(isoplotsL1L1dir),'{0}{1}.pdf'.format(outdirSelection,'isocut_ap80MeV_isocut_z')) #80 MeV A' Isocut vs Vz
    copyfile('{0}7.pdf'.format(isoplotsL1L1dir),'{0}{1}.pdf'.format(outdirSelection,'isocut_goodbad_z')) #Good Bad Tracks Comparison
    copyfile('{0}1.pdf'.format(isoplotsL1L1dir),'{0}{1}.pdf'.format(outdirSelection,'isocut_iso')) #Isolation Value
    copyfile('{0}2.pdf'.format(isoplotsL1L1dir),'{0}{1}.pdf'.format(outdirSelection,'isocut_isocut')) #Isocut Value
    copyfile('{0}8.pdf'.format(isoplotsL1L1dir),'{0}{1}.pdf'.format(outdirSelection,'isocut_mc_puretracks_z')) #MC Vz vs Isocut for Pure Tracks
    copyfile('{0}9.pdf'.format(isoplotsL1L1dir),'{0}{1}.pdf'.format(outdirSelection,'isocut_mc_badtracks_z')) #MC Vz vs Isocut for Bad Tracks
    copyfile('{0}12.pdf'.format(isoplotsL1L1dir),'{0}{1}.pdf'.format(outdirSelection,'isocut_data_z')) #data Vz vs Isocut

    copyfile('{0}{1}MeV_{2}62.pdf'.format(applotsL1L1dir,'80','L1L1'),'{0}{1}.pdf'.format(outdirSelection,'ap_80MeV_tightcutflowL1L1')) #80 MeV A' Tight Cutflow L1L1
    copyfile('{0}{1}MeV_{2}58.pdf'.format(applotsL1L1dir,'80','L1L1'),'{0}{1}.pdf'.format(outdirSelection,'ap_80MeV_L1L1_n_1_z')) #80 MeV A' L1L1 n-1 Vz
    copyfile('{0}{1}MeV_{2}56.pdf'.format(applotsL1L1dir,'80','L1L1'),'{0}{1}.pdf'.format(outdirSelection,'ap_80MeV_v0proj_n_1_z')) #80 MeV A' V0 Projection n-1 Vz
    copyfile('{0}{1}MeV_{2}54.pdf'.format(applotsL1L1dir,'80','L1L1'),'{0}{1}.pdf'.format(outdirSelection,'ap_80MeV_uncChisq_n_1_z')) #80 MeV A' UncChisq n-1 Vz
    copyfile('{0}{1}MeV_{2}52.pdf'.format(applotsL1L1dir,'80','L1L1'),'{0}{1}.pdf'.format(outdirSelection,'ap_80MeV_vop_n_1_z')) #80 MeV A' V0 Momentum n-1 Vz
    copyfile('{0}{1}MeV_{2}50.pdf'.format(applotsL1L1dir,'80','L1L1'),'{0}{1}.pdf'.format(outdirSelection,'ap_80MeV_isocut_n_1_z')) #80 MeV A' Isocut n-1 Vz
    copyfile('{0}{1}MeV_{2}48.pdf'.format(applotsL1L1dir,'80','L1L1'),'{0}{1}.pdf'.format(outdirSelection,'ap_80MeV_ip_n_1_z')) #80 MeV A' IP n-1 Vz
    copyfile('{0}{1}MeV_{2}_singleV02.pdf'.format(applotsL1L1dir,'80','L1L1'),'{0}{1}.pdf'.format(outdirSelection,'ap_80MeV_singleV0')) #80 MeV A' Single V0 Vz
    copyfile('{0}{1}MeV_{2}62.pdf'.format(applotsL1L1dir,'100','L1L1'),'{0}{1}.pdf'.format(outdirSelection,'ap_100MeV_tightcutflowL1L1')) #100 MeV A' Tight Cutflow L1L1
    copyfile('{0}{1}MeV_{2}58.pdf'.format(applotsL1L1dir,'100','L1L1'),'{0}{1}.pdf'.format(outdirSelection,'ap_100MeV_L1L1_n_1_z')) #100 MeV A' L1L1 n-1 Vz
    copyfile('{0}{1}MeV_{2}56.pdf'.format(applotsL1L1dir,'100','L1L1'),'{0}{1}.pdf'.format(outdirSelection,'ap_100MeV_v0proj_n_1_z')) #100 MeV A' V0 Projection n-1 Vz
    copyfile('{0}{1}MeV_{2}54.pdf'.format(applotsL1L1dir,'100','L1L1'),'{0}{1}.pdf'.format(outdirSelection,'ap_100MeV_uncChisq_n_1_z')) #100 MeV A' UncChisq n-1 Vz
    copyfile('{0}{1}MeV_{2}52.pdf'.format(applotsL1L1dir,'100','L1L1'),'{0}{1}.pdf'.format(outdirSelection,'ap_100MeV_vop_n_1_z')) #100 MeV A' V0 Momentum n-1 Vz
    copyfile('{0}{1}MeV_{2}50.pdf'.format(applotsL1L1dir,'100','L1L1'),'{0}{1}.pdf'.format(outdirSelection,'ap_100MeV_isocut_n_1_z')) #100 MeV A' Isocut n-1 Vz
    copyfile('{0}{1}MeV_{2}48.pdf'.format(applotsL1L1dir,'100','L1L1'),'{0}{1}.pdf'.format(outdirSelection,'ap_100MeV_ip_n_1_z')) #100 MeV A' IP n-1 Vz
    copyfile('{0}{1}MeV_{2}_singleV02.pdf'.format(applotsL1L1dir,'100','L1L1'),'{0}{1}.pdf'.format(outdirSelection,'ap_100MeV_singleV0')) #100 MeV A' Single V0 Vz

    copyfile('{0}1.pdf'.format(massResL1L1dir),'{0}{1}.pdf'.format(outdirMassRes,'massResL1L1')) #Mass Resolution L1L1
    copyfile('{0}60.pdf'.format(massResL1L1dir),'{0}{1}.pdf'.format(outdirMassRes,'massResL1L1_ap100MeV_m_z')) #100 MeV A' Mass vs Z L1L1
    copyfile('{0}61.pdf'.format(massResL1L1dir),'{0}{1}.pdf'.format(outdirMassRes,'massResL1L1_ap100MeV_smeared')) #100 MeV Mass Resolution L1L1
    copyfile('{0}62.pdf'.format(massResL1L1dir),'{0}{1}.pdf'.format(outdirMassRes,'massResL1L1_ap100MeV')) #100 MeV Mass Resolution L1L1
    copyfile('{0}58.pdf'.format(massResL1L1dir),'{0}{1}.pdf'.format(outdirMassRes,'massResL1L1_ap100MeV_z')) #100 MeV z L1L1

    copyfile('{0}_compare1.pdf'.format(tightL1L2dir),'{0}{1}.pdf'.format(outdirSelection,'tightcutflowL1L2')) #Tight Cutflow L1L2
    copyfile('{0}_compare2.pdf'.format(tightL1L2dir),'{0}{1}.pdf'.format(outdirSelection,'z0pos_excl_L1L2')) #Positron IP Exclusion L1L2
    copyfile('{0}_compare3.pdf'.format(tightL1L2dir),'{0}{1}.pdf'.format(outdirSelection,'z0ele_excl_L1L2')) #Electron IP Exclusion L1L2
    copyfile('{0}_compare4.pdf'.format(tightL1L2dir),'{0}{1}.pdf'.format(outdirSelection,'isocutpos_excl_L1L2')) #Positron Isocut Exclusion L1L2
    copyfile('{0}_compare5.pdf'.format(tightL1L2dir),'{0}{1}.pdf'.format(outdirSelection,'isocutele_excl_L1L2')) #Electron Isocut Exclusion L1L2
    copyfile('{0}_compare6.pdf'.format(tightL1L2dir),'{0}{1}.pdf'.format(outdirSelection,'v0p_excl_L1L2')) #V0 Momentum Exclusion L1L2
    copyfile('{0}_compare7.pdf'.format(tightL1L2dir),'{0}{1}.pdf'.format(outdirSelection,'uncChisq_excl_L1L2')) #UncChisq Exclusion L1L2
    copyfile('{0}_compare8.pdf'.format(tightL1L2dir),'{0}{1}.pdf'.format(outdirSelection,'v0proj_excl_L1L2')) #V0 Projection Exclusion L1L2
    copyfile('{0}_compare9.pdf'.format(tightL1L2dir),'{0}{1}.pdf'.format(outdirSelection,'L1L1_excl_L1L2')) #L1L1 Exclusion L1L2
    copyfile('{0}_compare50.pdf'.format(tightL1L2dir),'{0}{1}.pdf'.format(outdirSelection,'preselection_compare_L1L2')) #Preselection Compare L1L2
    copyfile('{0}_compare48.pdf'.format(tightL1L2dir),'{0}{1}.pdf'.format(outdirSelection,'L1L1_excl_z_L1L2')) #L1L2 Exclusion Vz
    copyfile('{0}_compare46.pdf'.format(tightL1L2dir),'{0}{1}.pdf'.format(outdirSelection,'v0proj_excl_z_L1L2')) #V0 Projection Exclusion Vz L1L2
    copyfile('{0}_compare44.pdf'.format(tightL1L2dir),'{0}{1}.pdf'.format(outdirSelection,'uncChisq_excl_z_L1L2')) #UncChisq Exclusion Vz L1L2
    copyfile('{0}_compare42.pdf'.format(tightL1L2dir),'{0}{1}.pdf'.format(outdirSelection,'v0p_excl_z_L1L2')) #V0 Momentum Exclusion Vz L1L2
    copyfile('{0}_compare40.pdf'.format(tightL1L2dir),'{0}{1}.pdf'.format(outdirSelection,'isocut_excl_z_L1L2')) #Isocut Exclusion Vz L1L2
    copyfile('{0}_compare38.pdf'.format(tightL1L2dir),'{0}{1}.pdf'.format(outdirSelection,'ip_excl_z_L1L2')) #IP Exclusion Vz L1L2

    copyfile('{0}68.pdf'.format(tightL1L2dir),'{0}{1}.pdf'.format(outdirSelection,'L1L1_excl_zm_L1L2')) #L1L2 Exclusion Vz vs Mass
    copyfile('{0}67.pdf'.format(tightL1L2dir),'{0}{1}.pdf'.format(outdirSelection,'voproj_excl_zm_L1L2')) #V0 Projection Exclusion Vz vs Mass L1L2
    copyfile('{0}66.pdf'.format(tightL1L2dir),'{0}{1}.pdf'.format(outdirSelection,'uncChisq_excl_zm_L1L2')) #UncChisq Exclusion Vz vs Mass L1L2
    copyfile('{0}65.pdf'.format(tightL1L2dir),'{0}{1}.pdf'.format(outdirSelection,'v0p_excl_zm_L1L2')) #V0 Momentum Exclusion Vz vs Mass L1L2
    copyfile('{0}64.pdf'.format(tightL1L2dir),'{0}{1}.pdf'.format(outdirSelection,'isocut_excl_zm_L1L2')) #Isocut Exclusion Vz vs Mass L1L2
    copyfile('{0}63.pdf'.format(tightL1L2dir),'{0}{1}.pdf'.format(outdirSelection,'ip_excl_zm_L1L2')) #IP Exclusion Vz vs Mass L1L2
    copyfile('{0}62.pdf'.format(tightL1L2dir),'{0}{1}.pdf'.format(outdirSelection,'tightcutflowL1L2_full')) #Tight Cutflow L1L1 Full L1L2

    copyfile('{0}58.pdf'.format(tightL1L2dir),'{0}{1}.pdf'.format(outdirSelection,'L1L2_n_1_z')) #L1L2 n-1 Vz
    copyfile('{0}56.pdf'.format(tightL1L2dir),'{0}{1}.pdf'.format(outdirSelection,'voproj_n_1_z_L1L2')) #V0 Projection n-1 Vz L1L2
    copyfile('{0}54.pdf'.format(tightL1L2dir),'{0}{1}.pdf'.format(outdirSelection,'uncChisq_n_1_z_L1L2')) #UncChisq n-1 Vz L1L2
    copyfile('{0}52.pdf'.format(tightL1L2dir),'{0}{1}.pdf'.format(outdirSelection,'v0p_n_1_z_L1L2')) #V0 Momentum n-1 Vz L1L2
    copyfile('{0}50.pdf'.format(tightL1L2dir),'{0}{1}.pdf'.format(outdirSelection,'isocut_n_1_z_L1L2')) #Isocut n-1 Vz L1L2
    copyfile('{0}48.pdf'.format(tightL1L2dir),'{0}{1}.pdf'.format(outdirSelection,'ip_n_1_z_L1L2')) #IP n-1 Vz L1L2

    copyfile('{0}4.pdf'.format(singleL1L2dir),'{0}{1}.pdf'.format(outdirSelection,'tightcuts_compare_L1L2')) #Data/MC Compare Tight Cuts L1L2
    copyfile('{0}5.pdf'.format(singleL1L2dir),'{0}{1}.pdf'.format(outdirSelection,'final_compare_L1L2')) #Data/MC Compare Final Selection L1L2
    copyfile('{0}6.pdf'.format(singleL1L2dir),'{0}{1}.pdf'.format(outdirSelection,'final_selection_cutflow_L1L2')) #Compare Tight to Final Selection L1L2

    copyfile('{0}5.pdf'.format(tailfitsL1L2dir),'{0}{1}.pdf'.format(outdirResults,'mean_slice_L1L2')) #Compare Vertex Mean L1L2
    copyfile('{0}4.pdf'.format(tailfitsL1L2dir),'{0}{1}.pdf'.format(outdirResults,'sigma_slice_L1L2')) #Compare Vertex Resolution L1L2
    copyfile('{0}74.pdf'.format(tailfitsL1L2dir),'{0}{1}.pdf'.format(outdirResults,'mass_slice_L1L2')) #Mass Slice Compare L1L2

    copyfile('{0}3.pdf'.format(isoplotsL1L2dir),'{0}{1}.pdf'.format(outdirSelection,'isocut_ap100MeV_z_L1L2')) #100 MeV A' Isocut Vz L1L2
    copyfile('{0}4.pdf'.format(isoplotsL1L2dir),'{0}{1}.pdf'.format(outdirSelection,'isocut_ap100MeV_isocut_z_L1L2')) #100 MeV A' Isocut vs Vz L1L2
    copyfile('{0}5.pdf'.format(isoplotsL1L2dir),'{0}{1}.pdf'.format(outdirSelection,'isocut_ap80MeV_z_L1L2')) #80 MeV A' Isocut Vz L1L2
    copyfile('{0}6.pdf'.format(isoplotsL1L2dir),'{0}{1}.pdf'.format(outdirSelection,'isocut_ap80MeV_isocut_z_L1L2')) #80 MeV A' Isocut vs Vz L1L2
    copyfile('{0}7.pdf'.format(isoplotsL1L2dir),'{0}{1}.pdf'.format(outdirSelection,'isocut_goodbad_z_L1L2')) #Good Bad Tracks Comparison L1L2
    copyfile('{0}1.pdf'.format(isoplotsL1L2dir),'{0}{1}.pdf'.format(outdirSelection,'isocut_iso_L1L2')) #Isolation Value L1L2
    copyfile('{0}2.pdf'.format(isoplotsL1L2dir),'{0}{1}.pdf'.format(outdirSelection,'isocut_isocut_L1L2')) #Isocut Value L1L2
    copyfile('{0}8.pdf'.format(isoplotsL1L2dir),'{0}{1}.pdf'.format(outdirSelection,'isocut_mc_puretracks_z_L1L2')) #MC Vz vs Isocut for Pure Tracks L1L2
    copyfile('{0}9.pdf'.format(isoplotsL1L2dir),'{0}{1}.pdf'.format(outdirSelection,'isocut_mc_badtracks_z_L1L2')) #MC Vz vs Isocut for Bad Tracks L1L2
    copyfile('{0}12.pdf'.format(isoplotsL1L2dir),'{0}{1}.pdf'.format(outdirSelection,'isocut_data_z_L1L2')) #data Vz vs Isocut L1L2

    copyfile('{0}{1}MeV_{2}62.pdf'.format(applotsL1L2dir,'80','L1L2'),'{0}{1}.pdf'.format(outdirSelection,'ap_80MeV_tightcutflowL1L2')) #80 MeV A' Tight Cutflow L1L2
    copyfile('{0}{1}MeV_{2}58.pdf'.format(applotsL1L2dir,'80','L1L2'),'{0}{1}.pdf'.format(outdirSelection,'ap_80MeV_L1L2_n_1_z')) #80 MeV A' L1L2 n-1 Vz
    copyfile('{0}{1}MeV_{2}56.pdf'.format(applotsL1L2dir,'80','L1L2'),'{0}{1}.pdf'.format(outdirSelection,'ap_80MeV_v0proj_n_1_z_L1L2')) #80 MeV A' V0 Projection n-1 Vz L1L2
    copyfile('{0}{1}MeV_{2}54.pdf'.format(applotsL1L2dir,'80','L1L2'),'{0}{1}.pdf'.format(outdirSelection,'ap_80MeV_uncChisq_n_1_z_L1L2')) #80 MeV A' UncChisq n-1 Vz L1L2
    copyfile('{0}{1}MeV_{2}52.pdf'.format(applotsL1L2dir,'80','L1L2'),'{0}{1}.pdf'.format(outdirSelection,'ap_80MeV_vop_n_1_z_L1L2')) #80 MeV A' V0 Momentum n-1 Vz L1L2
    copyfile('{0}{1}MeV_{2}50.pdf'.format(applotsL1L2dir,'80','L1L2'),'{0}{1}.pdf'.format(outdirSelection,'ap_80MeV_isocut_n_1_z_L1L2')) #80 MeV A' Isocut n-1 Vz L1L2
    copyfile('{0}{1}MeV_{2}48.pdf'.format(applotsL1L2dir,'80','L1L2'),'{0}{1}.pdf'.format(outdirSelection,'ap_80MeV_ip_n_1_z_L1L2')) #80 MeV A' IP n-1 Vz L1L2
    copyfile('{0}{1}MeV_{2}_singleV02.pdf'.format(applotsL1L2dir,'80','L1L2'),'{0}{1}.pdf'.format(outdirSelection,'ap_80MeV_singleV0_L1L2')) #80 MeV A' Single V0 Vz L1L2
    copyfile('{0}{1}MeV_{2}62.pdf'.format(applotsL1L2dir,'100','L1L2'),'{0}{1}.pdf'.format(outdirSelection,'ap_100MeV_tightcutflowL1L2')) #100 MeV A' Tight Cutflow L1L2
    copyfile('{0}{1}MeV_{2}58.pdf'.format(applotsL1L2dir,'100','L1L2'),'{0}{1}.pdf'.format(outdirSelection,'ap_100MeV_L1L2_n_1_z_L1L2')) #100 MeV A' L1L2 n-1 Vz
    copyfile('{0}{1}MeV_{2}56.pdf'.format(applotsL1L2dir,'100','L1L2'),'{0}{1}.pdf'.format(outdirSelection,'ap_100MeV_v0proj_n_1_z_L1L2')) #100 MeV A' V0 Projection n-1 Vz L1L2
    copyfile('{0}{1}MeV_{2}54.pdf'.format(applotsL1L2dir,'100','L1L2'),'{0}{1}.pdf'.format(outdirSelection,'ap_100MeV_uncChisq_n_1_z_L1L2')) #100 MeV A' UncChisq n-1 Vz L1L2
    copyfile('{0}{1}MeV_{2}52.pdf'.format(applotsL1L2dir,'100','L1L2'),'{0}{1}.pdf'.format(outdirSelection,'ap_100MeV_vop_n_1_z_L1L2')) #100 MeV A' V0 Momentum n-1 Vz L1L2
    copyfile('{0}{1}MeV_{2}50.pdf'.format(applotsL1L2dir,'100','L1L2'),'{0}{1}.pdf'.format(outdirSelection,'ap_100MeV_isocut_n_1_z_L1L2')) #100 MeV A' Isocut n-1 Vz L1L2
    copyfile('{0}{1}MeV_{2}48.pdf'.format(applotsL1L2dir,'100','L1L2'),'{0}{1}.pdf'.format(outdirSelection,'ap_100MeV_ip_n_1_z_L1L2')) #100 MeV A' IP n-1 Vz L1L2
    copyfile('{0}{1}MeV_{2}_singleV02.pdf'.format(applotsL1L2dir,'100','L1L2'),'{0}{1}.pdf'.format(outdirSelection,'ap_100MeV_singleV0_L1L2')) #100 MeV A' Single V0 Vz L1L2

    copyfile('{0}1.pdf'.format(massResL1L2dir),'{0}{1}.pdf'.format(outdirMassRes,'massResL1L2')) #Mass Resolution L1L2
    copyfile('{0}60.pdf'.format(massResL1L2dir),'{0}{1}.pdf'.format(outdirMassRes,'massResL1L2_ap100MeV_m_z')) #100 MeV A' Mass vs Z L1L2
    copyfile('{0}61.pdf'.format(massResL1L2dir),'{0}{1}.pdf'.format(outdirMassRes,'massResL1L2_ap100MeV_smeared')) #100 MeV Mass Resolution L1L2
    copyfile('{0}62.pdf'.format(massResL1L2dir),'{0}{1}.pdf'.format(outdirMassRes,'massResL1L2_ap100MeV')) #100 MeV Mass Resolution L1L2
    copyfile('{0}58.pdf'.format(massResL1L2dir),'{0}{1}.pdf'.format(outdirMassRes,'massResL1L2_ap100MeV_z')) #100 MeV z L1L2


if __name__ == "__main__" : 
    main() 

