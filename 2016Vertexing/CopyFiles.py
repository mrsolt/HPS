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
    outdirSystematics = '{0}/Systematics/'.format(outdir)

    preselectiondir = '/nfs/slac/g/hps2/mrsolt/hps/Data2016/pass4c/Preselection/plots/preselection'
    tightL1L1dir = '/nfs/slac/g/hps2/mrsolt/hps/Data2016/DataMCCompare/Tight/L1L1/cutflow_L1L1'
    singleL1L1dir = '/nfs/slac/g/hps2/mrsolt/hps/Data2016/DataMCCompare/Tight/L1L1/singleV0_L1L1_compare'
    tailfitsL1L1dir = '/nfs/slac/g/hps2/mrsolt/hps/Data2016/DataMCCompare/TailFits/L1L1/compare_tailfits_L1L1'
    isoplotsL1L1dir = '/nfs/slac/g/hps2/mrsolt/hps/Data2016/DataMCCompare/IsoPlots/L1L1/isoplots_L1L1'
    applotsL1L1dir = '/nfs/slac/g/hps2/mrsolt/hps/Data2016/MC/ap-beam/Tight/L1L1/ap-beam_'
    massResL1L1dir = '/nfs/slac/g/hps2/mrsolt/hps/Data2016/MC/ap-beam/Tight/MassRes/L1L1/massRes_L1L1'
    datatightL1L1dir = '/nfs/slac/g/hps2/mrsolt/hps/Data2016/pass4c/Tight/L1L1/L1L1_floatcut'
    mctightL1L1dir = '/nfs/slac/g/hps2/mrsolt/hps/Data2016/MC/tritrig-wab-beam/Tight/L1L1/L1L1_floatcut_tritrig-wab-beam'
    aptightL1L1dir = '/nfs/slac/g/hps2/mrsolt/hps/Data2016/MC/ap-beam/Tight/L1L1/ap-beam_'
    tightL1L2dir = '/nfs/slac/g/hps2/mrsolt/hps/Data2016/DataMCCompare/Tight/L1L2/cutflow_L1L2'
    singleL1L2dir = '/nfs/slac/g/hps2/mrsolt/hps/Data2016/DataMCCompare/Tight/L1L2/singleV0_L1L2_compare'
    tailfitsL1L2dir = '/nfs/slac/g/hps2/mrsolt/hps/Data2016/DataMCCompare/TailFits/L1L2/compare_tailfits_L1L2'
    isoplotsL1L2dir = '/nfs/slac/g/hps2/mrsolt/hps/Data2016/DataMCCompare/IsoPlots/L1L2/isoplots_L1L2'
    applotsL1L2dir = '/nfs/slac/g/hps2/mrsolt/hps/Data2016/MC/ap-beam/Tight/L1L2/ap-beam_'
    massResL1L2dir = '/nfs/slac/g/hps2/mrsolt/hps/Data2016/MC/ap-beam/Tight/MassRes/L1L2/massRes_L1L2'
    datatightL1L2dir = '/nfs/slac/g/hps2/mrsolt/hps/Data2016/pass4c/Tight/L1L2/L1L2_floatcut'
    mctightL1L2dir = '/nfs/slac/g/hps2/mrsolt/hps/Data2016/MC/tritrig-wab-beam/Tight/L1L2/L1L2_floatcut_tritrig-wab-beam'
    aptightL1L2dir = '/nfs/slac/g/hps2/mrsolt/hps/Data2016/MC/ap-beam/Tight/L1L2/ap-beam_'

    copyfile('{0}28.pdf'.format(preselectiondir),'{0}{1}.pdf'.format(outdirSelection,'pre_cutflow_data')) #Preselection Cutflow Data
    copyfile('{0}26.pdf'.format(preselectiondir),'{0}{1}.pdf'.format(outdirSelection,'pre_cutflow_mc')) #Preselection Cutflow MC
    copyfile('{0}24.pdf'.format(preselectiondir),'{0}{1}.pdf'.format(outdirSelection,'pre_cutflow_ap80')) #Preselection Cutflow A' 80 MeV
    copyfile('{0}22.pdf'.format(preselectiondir),'{0}{1}.pdf'.format(outdirSelection,'pre_cutflow_ap100')) #Preselection Cutflow A' 100 MeV
    copyfile('{0}21.pdf'.format(preselectiondir),'{0}{1}.pdf'.format(outdirSelection,'pre_cutflow_uncM_data')) #Preselection Cutflow Data Mass
    copyfile('{0}20.pdf'.format(preselectiondir),'{0}{1}.pdf'.format(outdirSelection,'pre_cutflow_uncM_mc')) #Preselection Cutflow MC Mass
    copyfile('{0}19.pdf'.format(preselectiondir),'{0}{1}.pdf'.format(outdirSelection,'pre_cutflow_uncM_ap80')) #Preselection Cutflow A' 80 MeV Mass
    copyfile('{0}18.pdf'.format(preselectiondir),'{0}{1}.pdf'.format(outdirSelection,'pre_cutflow_uncM_ap100')) #Preselection Cutflow A' 100 MeV Mass
    copyfile('{0}17.pdf'.format(preselectiondir),'{0}{1}.pdf'.format(outdirSelection,'pre_cutflow_uncP_data')) #Preselection Cutflow Data Momentum
    copyfile('{0}16.pdf'.format(preselectiondir),'{0}{1}.pdf'.format(outdirSelection,'pre_cutflow_uncP_mc')) #Preselection Cutflow MC Momentum
    copyfile('{0}15.pdf'.format(preselectiondir),'{0}{1}.pdf'.format(outdirSelection,'pre_cutflow_uncP_ap80')) #Preselection Cutflow A' 80 MeV Momentum
    copyfile('{0}14.pdf'.format(preselectiondir),'{0}{1}.pdf'.format(outdirSelection,'pre_cutflow_uncP_ap100')) #Preselection Cutflow A' 100 MeV Momentum
    copyfile('{0}12.pdf'.format(preselectiondir),'{0}{1}.pdf'.format(outdirSelection,'pre_eleMatchChisq')) #Preselection Electron Match Chisq
    copyfile('{0}11.pdf'.format(preselectiondir),'{0}{1}.pdf'.format(outdirSelection,'pre_posMatchChisq')) #Preselection Positron Match Chisq
    copyfile('{0}10.pdf'.format(preselectiondir),'{0}{1}.pdf'.format(outdirSelection,'pre_clT')) #Preselection Cluster Time Diff
    copyfile('{0}9.pdf'.format(preselectiondir),'{0}{1}.pdf'.format(outdirSelection,'pre_eleTrkT')) #Preselection Electron Track Cluster Time Diff
    copyfile('{0}8.pdf'.format(preselectiondir),'{0}{1}.pdf'.format(outdirSelection,'pre_posTrkT')) #Preselection Positron Track Cluster Time Diff
    copyfile('{0}7.pdf'.format(preselectiondir),'{0}{1}.pdf'.format(outdirSelection,'pre_eleP')) #Preselection Electron Momentum
    copyfile('{0}6.pdf'.format(preselectiondir),'{0}{1}.pdf'.format(outdirSelection,'pre_eleTrkChisq')) #Preselection Electron Track Chisq
    copyfile('{0}5.pdf'.format(preselectiondir),'{0}{1}.pdf'.format(outdirSelection,'pre_posTrkChisq')) #Preselection Positron Track Chisq
    copyfile('{0}4.pdf'.format(preselectiondir),'{0}{1}.pdf'.format(outdirSelection,'pre_uncChisq')) #Preselection Unconstrained Chisq
    copyfile('{0}3.pdf'.format(preselectiondir),'{0}{1}.pdf'.format(outdirSelection,'pre_posP')) #Preselection Positron Momentum
    copyfile('{0}2.pdf'.format(preselectiondir),'{0}{1}.pdf'.format(outdirSelection,'pre_uncP')) #Preselection V0 Momentum
    copyfile('{0}1.pdf'.format(preselectiondir),'{0}{1}.pdf'.format(outdirSelection,'pre_cutflow')) #Preselection Cutflow

    copyfile('{0}52.pdf'.format('/nfs/slac/g/hps2/mrsolt/hps/Data2016/MC/ap-beam/Tight/acceptance/final/plots/acceptance'),'{0}{1}.pdf'.format(outdir+'aprime/','ap_80MeV_eff_norm')) #80 MeV A' Efficiency Normalized
    copyfile('{0}44.pdf'.format('/nfs/slac/g/hps2/mrsolt/hps/Data2016/MC/ap-beam/Tight/acceptance/final/plots/acceptance'),'{0}{1}.pdf'.format(outdir+'aprime/','ap_100MeV_eff_norm')) #100 MeV A' Efficiency Normalized
    copyfile('{0}52.pdf'.format('/nfs/slac/g/hps2/mrsolt/hps/Data2016/MC/ap-beam/Tight/acceptance/zcut/plots/acceptance_zcut'),'{0}{1}.pdf'.format(outdir+'aprime/','ap_80MeV_eff_norm_zcut')) #80 MeV A' Efficiency Normalized Zcut
    copyfile('{0}44.pdf'.format('/nfs/slac/g/hps2/mrsolt/hps/Data2016/MC/ap-beam/Tight/acceptance/zcut/plots/acceptance_zcut'),'{0}{1}.pdf'.format(outdir+'aprime/','ap_100MeV_eff_norm_zcut')) #100 MeV A' Efficiency Normalized Zcut
    copyfile('{0}16.pdf'.format('/nfs/slac/g/hps2/mrsolt/hps/Data2016/MC/ap-beam/Tight/acceptance/zcut/plots/acceptance_zcut'),'{0}{1}.pdf'.format(outdir+'aprime/','ap_80MeV_eff_fit')) #80 MeV A' Efficiency Fitfunc
    copyfile('{0}12.pdf'.format('/nfs/slac/g/hps2/mrsolt/hps/Data2016/MC/ap-beam/Tight/acceptance/zcut/plots/acceptance_zcut'),'{0}{1}.pdf'.format(outdir+'aprime/','ap_100MeV_eff_fit')) #100 MeV A' Efficiency Fitfunc

    copyfile('{0}70.pdf'.format('/nfs/slac/g/hps2/mrsolt/hps/Data2016/pass4c/Tight/L1L1/L1L1_cutflow'),'{0}{1}.pdf'.format(outdirSelection,'data_L1L1_tight_vz_mass')) #Data Tight L1L1 Vz vs Mass
    copyfile('{0}62.pdf'.format('/nfs/slac/g/hps2/mrsolt/hps/Data2016/pass4c/Tight/L1L1/L1L1_cutflow'),'{0}{1}.pdf'.format(outdirSelection,'datatightcutflowL1L1_vz')) #Data Tight Cutflow L1L1 Vz
    copyfile('{0}44.pdf'.format('/nfs/slac/g/hps2/mrsolt/hps/Data2016/pass4c/Tight/L1L1/L1L1_cutflow'),'{0}{1}.pdf'.format(outdirSelection,'datatightcutflowL1L1_mass')) #Data Tight Cutflow L1L1 Mass
    copyfile('{0}26.pdf'.format('/nfs/slac/g/hps2/mrsolt/hps/Data2016/pass4c/Tight/L1L1/L1L1_cutflow'),'{0}{1}.pdf'.format(outdirSelection,'datatightcutflowL1L1_p')) #Data Tight Cutflow L1L1 P
    copyfile('{0}62.pdf'.format('/nfs/slac/g/hps2/mrsolt/hps/Data2016/MC/tritrig-wab-beam/Tight/L1L1/L1L1_cutflow_tritrig-wab-beam'),'{0}{1}.pdf'.format(outdirSelection,'mctightcutflowL1L1_vz')) #MC Tight Cutflow L1L1 Vz
    copyfile('{0}44.pdf'.format('/nfs/slac/g/hps2/mrsolt/hps/Data2016/MC/tritrig-wab-beam/Tight/L1L1/L1L1_cutflow_tritrig-wab-beam'),'{0}{1}.pdf'.format(outdirSelection,'mctightcutflowL1L1_mass')) #MC Tight Cutflow L1L1 Mass
    copyfile('{0}26.pdf'.format('/nfs/slac/g/hps2/mrsolt/hps/Data2016/MC/tritrig-wab-beam/Tight/L1L1/L1L1_cutflow_tritrig-wab-beam'),'{0}{1}.pdf'.format(outdirSelection,'mctightcutflowL1L1_p')) #MC Tight Cutflow L1L1 P

    copyfile('{0}.pdf'.format('/nfs/slac/g/hps2/mrsolt/hps/Data2016/pass4c/Tight/10per_L1L1_final'),'{0}{1}.pdf'.format(outdirSelection,'data_L1L1_final_vz_mass')) #Data Final L1L1 Vz vs Mass
    copyfile('{0}.pdf'.format('/nfs/slac/g/hps2/mrsolt/hps/Data2016/pass4c/Tight/10per_L1L1_final_zcut'),'{0}{1}.pdf'.format(outdirSelection,'data_L1L1_final_vz_mass_zcut')) #Data Final L1L1 Vz vs Mass Zcut
    copyfile('{0}.pdf'.format('/nfs/slac/g/hps2/mrsolt/hps/Data2016/MC/tritrig-wab-beam/Tight/tritrig-wab-beam_L1L1_final'),'{0}{1}.pdf'.format(outdirSelection,'mc_L1L1_final_vz_mass')) #Mass Final L1L1 Vz vs Mass
    copyfile('{0}.pdf'.format('/nfs/slac/g/hps2/mrsolt/hps/Data2016/MC/tritrig-wab-beam/Tight/tritrig-wab-beam_L1L1_final_zcut'),'{0}{1}.pdf'.format(outdirSelection,'mc_L1L1_final_vz_mass_zcut')) #Mass Final L1L1 Vz vs Mass Zcut

    copyfile('{0}.pdf'.format('/nfs/slac/g/hps2/mrsolt/hps/Data2016/pass4c/Tight/10per_L1L1_sharedhits'),'{0}{1}.pdf'.format(outdirSelection,'L1L1_sharedhits_data')) #Shared Hits L1L1 data
    copyfile('{0}.pdf'.format('/nfs/slac/g/hps2/mrsolt/hps/Data2016/MC/tritrig-wab-beam/Tight/tritrig-wab-beam_L1L1_sharedhits'),'{0}{1}.pdf'.format(outdirSelection,'L1L1_sharedhits_mc')) #Shared Hits L1L1 MC

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

    copyfile('{0}10.pdf'.format(tailfitsL1L1dir),'{0}{1}.pdf'.format(outdirResults,'mean_slice')) #Compare Vertex Mean
    copyfile('{0}9.pdf'.format(tailfitsL1L1dir),'{0}{1}.pdf'.format(outdirResults,'sigma_slice')) #Compare Vertex Resolution
    copyfile('{0}79.pdf'.format(tailfitsL1L1dir),'{0}{1}.pdf'.format(outdirResults,'mass_slice')) #Mass Slice Compare
    copyfile('{0}4.pdf'.format(tailfitsL1L1dir),'{0}{1}.pdf'.format(outdirResults,'zcut')) #Zcut L1L1
    copyfile('{0}8.pdf'.format(tailfitsL1L1dir),'{0}{1}.pdf'.format(outdirResults,'tailz')) #TailZ L1L1

    copyfile('{0}3.pdf'.format(tailfitsL1L1dir),'{0}{1}.pdf'.format(outdirSystematics,'data_zcut_1sig')) #Data 1 sigma Zcut L1L1
    copyfile('{0}2.pdf'.format(tailfitsL1L1dir),'{0}{1}.pdf'.format(outdirSystematics,'mc_zcut_1sig')) #MC 1 sigma Zcut L1L1
    copyfile('{0}_5sig3.pdf'.format(tailfitsL1L1dir),'{0}{1}.pdf'.format(outdirSystematics,'data_zcut_5sig')) #Data 5 sigma Zcut L1L1
    copyfile('{0}_5sig2.pdf'.format(tailfitsL1L1dir),'{0}{1}.pdf'.format(outdirSystematics,'mc_zcut_5sig')) #MC 5 sigma Zcut L1L1
    copyfile('{0}35.pdf'.format('/nfs/slac/g/hps2/mrsolt/hps/Data2016/pass4c/Tight/Tailfits/plots/10per_L1L1_tailfits'),'{0}{1}.pdf'.format(outdirSystematics,'data_fitslice_1sig')) #Data 1 sigma Fit Slice L1L1
    copyfile('{0}35.pdf'.format('/nfs/slac/g/hps2/mrsolt/hps/Data2016/pass4c/Tight/Tailfits/plots/10per_L1L1_tailfits_5sig'),'{0}{1}.pdf'.format(outdirSystematics,'data_fitslice_5sig')) #Data 5 sigma Fit Slice L1L1
    copyfile('{0}35.pdf'.format('/nfs/slac/g/hps2/mrsolt/hps/Data2016/MC/tritrig-wab-beam/Tight/TailFits/plots/tritrig-wab-beam_L1L1_tailfits'),'{0}{1}.pdf'.format(outdirSystematics,'mc_fitslice_1sig')) #MC 1 sigma Fit Slice L1L1
    copyfile('{0}35.pdf'.format('/nfs/slac/g/hps2/mrsolt/hps/Data2016/MC/tritrig-wab-beam/Tight/TailFits/plots/tritrig-wab-beam_L1L1_tailfits_5sig'),'{0}{1}.pdf'.format(outdirSystematics,'mc_fitslice_5sig')) #MC 5 sigma Fit Slice L1L1

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

    copyfile('{0}1.pdf'.format('/nfs/slac/g/hps2/mrsolt/hps/Data2016/MC/ap-beam/Tight/MassRes/Prompt/L1L1/massRes_L1L1'),'{0}{1}.pdf'.format(outdirMassRes,'massResL1L1')) #Mass Resolution L1L1
    copyfile('{0}60.pdf'.format(massResL1L1dir),'{0}{1}.pdf'.format(outdirMassRes,'massResL1L1_ap100MeV_m_z')) #100 MeV A' Mass vs Z L1L1
    copyfile('{0}61.pdf'.format(massResL1L1dir),'{0}{1}.pdf'.format(outdirMassRes,'massResL1L1_ap100MeV_smeared')) #100 MeV Mass Resolution L1L1
    copyfile('{0}62.pdf'.format(massResL1L1dir),'{0}{1}.pdf'.format(outdirMassRes,'massResL1L1_ap100MeV')) #100 MeV Mass Resolution L1L1
    copyfile('{0}58.pdf'.format(massResL1L1dir),'{0}{1}.pdf'.format(outdirMassRes,'massResL1L1_ap100MeV_z')) #100 MeV z L1L1

    copyfile('{0}5.pdf'.format(datatightL1L1dir),'{0}{1}.pdf'.format(outdirSystematics,'data_floatcut_ip')) #Data L1L1 Float Cut IP
    copyfile('{0}10.pdf'.format(datatightL1L1dir),'{0}{1}.pdf'.format(outdirSystematics,'data_floatcut_iso')) #Data L1L1 Float Cut Isocut
    copyfile('{0}15.pdf'.format(datatightL1L1dir),'{0}{1}.pdf'.format(outdirSystematics,'data_floatcut_v0p')) #Data L1L1 Float Cut V0 Momentum
    copyfile('{0}20.pdf'.format(datatightL1L1dir),'{0}{1}.pdf'.format(outdirSystematics,'data_floatcut_uncChisq')) #Data L1L1 Float Cut uncChisq
    copyfile('{0}25.pdf'.format(datatightL1L1dir),'{0}{1}.pdf'.format(outdirSystematics,'data_floatcut_v0proj')) #Data L1L1 Float Cut V0 Projection

    copyfile('{0}5.pdf'.format(mctightL1L1dir),'{0}{1}.pdf'.format(outdirSystematics,'mc_floatcut_ip')) #MC L1L1 Float Cut IP
    copyfile('{0}10.pdf'.format(mctightL1L1dir),'{0}{1}.pdf'.format(outdirSystematics,'mc_floatcut_iso')) #MC L1L1 Float Cut Isocut
    copyfile('{0}15.pdf'.format(mctightL1L1dir),'{0}{1}.pdf'.format(outdirSystematics,'mc_floatcut_v0p')) #MC L1L1 Float Cut V0 Momentum
    copyfile('{0}20.pdf'.format(mctightL1L1dir),'{0}{1}.pdf'.format(outdirSystematics,'mc_floatcut_uncChisq')) #MC L1L1 Float Cut uncChisq
    copyfile('{0}25.pdf'.format(mctightL1L1dir),'{0}{1}.pdf'.format(outdirSystematics,'mc_floatcut_v0proj')) #MC L1L1 Float Cut V0 Projection

    copyfile('{0}{1}MeV_L1L1_floatcut5.pdf'.format(aptightL1L1dir,'80'),'{0}{1}.pdf'.format(outdirSystematics,'ap80MeV_floatcut_ip')) #80 MeV A' L1L1 Float Cut IP
    copyfile('{0}{1}MeV_L1L1_floatcut10.pdf'.format(aptightL1L1dir,'80'),'{0}{1}.pdf'.format(outdirSystematics,'ap80MeV_floatcut_iso')) #80 MeV A' L1L1 Float Cut Isocut
    copyfile('{0}{1}MeV_L1L1_floatcut15.pdf'.format(aptightL1L1dir,'80'),'{0}{1}.pdf'.format(outdirSystematics,'ap80MeV_floatcut_v0p')) #80 MeV A' L1L1 Float Cut V0 Momentum
    copyfile('{0}{1}MeV_L1L1_floatcut20.pdf'.format(aptightL1L1dir,'80'),'{0}{1}.pdf'.format(outdirSystematics,'ap80MeV_floatcut_uncChisq')) #80 MeV A' L1L1 Float Cut uncChisq
    copyfile('{0}{1}MeV_L1L1_floatcut25.pdf'.format(aptightL1L1dir,'80'),'{0}{1}.pdf'.format(outdirSystematics,'ap80MeV_floatcut_v0proj')) #80 MeV A' L1L1 Float Cut V0 Projection

    copyfile('{0}{1}MeV_L1L1_floatcut5.pdf'.format(aptightL1L1dir,'100'),'{0}{1}.pdf'.format(outdirSystematics,'ap100MeV_floatcut_ip')) #100 MeV A' L1L1 Float Cut IP
    copyfile('{0}{1}MeV_L1L1_floatcut10.pdf'.format(aptightL1L1dir,'100'),'{0}{1}.pdf'.format(outdirSystematics,'ap100MeV_floatcut_iso')) #100 MeV A' L1L1 Float Cut Isocut
    copyfile('{0}{1}MeV_L1L1_floatcut15.pdf'.format(aptightL1L1dir,'100'),'{0}{1}.pdf'.format(outdirSystematics,'ap100MeV_floatcut_v0p')) #100 MeV A' L1L1 Float Cut V0 Momentum
    copyfile('{0}{1}MeV_L1L1_floatcut20.pdf'.format(aptightL1L1dir,'100'),'{0}{1}.pdf'.format(outdirSystematics,'ap100MeV_floatcut_uncChisq')) #100 MeV A' L1L1 Float Cut uncChisq
    copyfile('{0}{1}MeV_L1L1_floatcut25.pdf'.format(aptightL1L1dir,'100'),'{0}{1}.pdf'.format(outdirSystematics,'ap100MeV_floatcut_v0proj')) #100 MeV A' L1L1 Float Cut V0 Projection

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

    copyfile('{0}.pdf'.format('/nfs/slac/g/hps2/mrsolt/hps/Data2016/pass4c/Tight/10per_L1L2_final'),'{0}{1}.pdf'.format(outdirSelection,'data_L1L2_final_vz_mass')) #Data Final L1L2 Vz vs Mass
    copyfile('{0}.pdf'.format('/nfs/slac/g/hps2/mrsolt/hps/Data2016/pass4c/Tight/10per_L1L2_final_zcut'),'{0}{1}.pdf'.format(outdirSelection,'data_L1L2_final_vz_mass_zcut')) #Data Final L1L2 Vz vs Mass Zcut
    copyfile('{0}.pdf'.format('/nfs/slac/g/hps2/mrsolt/hps/Data2016/MC/tritrig-wab-beam/Tight/tritrig-wab-beam_L1L2_final'),'{0}{1}.pdf'.format(outdirSelection,'mc_L1L2_final_vz_mass')) #Mass Final L1L2 Vz vs Mass
    copyfile('{0}.pdf'.format('/nfs/slac/g/hps2/mrsolt/hps/Data2016/MC/tritrig-wab-beam/Tight/tritrig-wab-beam_L1L2_final_zcut'),'{0}{1}.pdf'.format(outdirSelection,'mc_L1L2_final_vz_mass_zcut')) #Mass Final L1L2 Vz vs Mass Zcut
    copyfile('{0}70.pdf'.format('/nfs/slac/g/hps2/mrsolt/hps/Data2016/pass4c/Tight/L1L2/L1L2_cutflow'),'{0}{1}.pdf'.format(outdirSelection,'data_L1L2_tight_vz_mass')) #Data Tight L1L2 Vz vs Mass
    copyfile('{0}62.pdf'.format('/nfs/slac/g/hps2/mrsolt/hps/Data2016/pass4c/Tight/L1L2/L1L2_cutflow'),'{0}{1}.pdf'.format(outdirSelection,'datatightcutflowL1L2_vz')) #Data Tight Cutflow L1L2 Vz
    copyfile('{0}44.pdf'.format('/nfs/slac/g/hps2/mrsolt/hps/Data2016/pass4c/Tight/L1L2/L1L2_cutflow'),'{0}{1}.pdf'.format(outdirSelection,'datatightcutflowL1L2_mass')) #Data Tight Cutflow L1L2 Mass
    copyfile('{0}26.pdf'.format('/nfs/slac/g/hps2/mrsolt/hps/Data2016/pass4c/Tight/L1L2/L1L2_cutflow'),'{0}{1}.pdf'.format(outdirSelection,'datatightcutflowL1L2_p')) #Data Tight Cutflow L1L2 P
    copyfile('{0}62.pdf'.format('/nfs/slac/g/hps2/mrsolt/hps/Data2016/MC/tritrig-wab-beam/Tight/L1L2/L1L2_cutflow_tritrig-wab-beam'),'{0}{1}.pdf'.format(outdirSelection,'mctightcutflowL1L2_vz')) #MC Tight Cutflow L1L2 Vz
    copyfile('{0}44.pdf'.format('/nfs/slac/g/hps2/mrsolt/hps/Data2016/MC/tritrig-wab-beam/Tight/L1L2/L1L2_cutflow_tritrig-wab-beam'),'{0}{1}.pdf'.format(outdirSelection,'mctightcutflowL1L2_mass')) #MC Tight Cutflow L1L2 Mass
    copyfile('{0}26.pdf'.format('/nfs/slac/g/hps2/mrsolt/hps/Data2016/MC/tritrig-wab-beam/Tight/L1L2/L1L2_cutflow_tritrig-wab-beam'),'{0}{1}.pdf'.format(outdirSelection,'mctightcutflowL1L2_p')) #MC Tight Cutflow L1L2 P

    copyfile('{0}.pdf'.format('/nfs/slac/g/hps2/mrsolt/hps/Data2016/pass4c/Tight/10per_L1L2_sharedhits'),'{0}{1}.pdf'.format(outdirSelection,'L1L2_sharedhits_data')) #Shared Hits L1L2 data
    copyfile('{0}.pdf'.format('/nfs/slac/g/hps2/mrsolt/hps/Data2016/MC/tritrig-wab-beam/Tight/tritrig-wab-beam_L1L2_sharedhits'),'{0}{1}.pdf'.format(outdirSelection,'L1L2_sharedhits_mc')) #Shared Hits L1L2 MC

    copyfile('{0}4.pdf'.format(singleL1L2dir),'{0}{1}.pdf'.format(outdirSelection,'tightcuts_compare_L1L2')) #Data/MC Compare Tight Cuts L1L2
    copyfile('{0}5.pdf'.format(singleL1L2dir),'{0}{1}.pdf'.format(outdirSelection,'final_compare_L1L2')) #Data/MC Compare Final Selection L1L2
    copyfile('{0}6.pdf'.format(singleL1L2dir),'{0}{1}.pdf'.format(outdirSelection,'final_selection_cutflow_L1L2')) #Compare Tight to Final Selection L1L2

    copyfile('{0}10.pdf'.format(tailfitsL1L2dir),'{0}{1}.pdf'.format(outdirResults,'mean_slice_L1L2')) #Compare Vertex Mean L1L2
    copyfile('{0}9.pdf'.format(tailfitsL1L2dir),'{0}{1}.pdf'.format(outdirResults,'sigma_slice_L1L2')) #Compare Vertex Resolution L1L2
    copyfile('{0}79.pdf'.format(tailfitsL1L2dir),'{0}{1}.pdf'.format(outdirResults,'mass_slice_L1L2')) #Mass Slice Compare L1L2
    copyfile('{0}4.pdf'.format(tailfitsL1L2dir),'{0}{1}.pdf'.format(outdirResults,'zcut_L1L2')) #Zcut L1L1
    copyfile('{0}8.pdf'.format(tailfitsL1L2dir),'{0}{1}.pdf'.format(outdirResults,'tailz_L1L2')) #TailZ L1L1

    copyfile('{0}3.pdf'.format(tailfitsL1L2dir),'{0}{1}.pdf'.format(outdirSystematics,'data_zcut_1sigL1L2')) #Data 1 sigma Zcut L1L2
    copyfile('{0}2.pdf'.format(tailfitsL1L2dir),'{0}{1}.pdf'.format(outdirSystematics,'mc_zcut_1sig_L1L2')) #MC 1 sigma Zcut L1L2
    copyfile('{0}_5sig3.pdf'.format(tailfitsL1L2dir),'{0}{1}.pdf'.format(outdirSystematics,'data_zcut_5sig_L1L2')) #Data 5 sigma Zcut L1L2
    copyfile('{0}_5sig2.pdf'.format(tailfitsL1L2dir),'{0}{1}.pdf'.format(outdirSystematics,'mc_zcut_5sig_L1L2')) #MC 5 sigma Zcut L1L2
    copyfile('{0}35.pdf'.format('/nfs/slac/g/hps2/mrsolt/hps/Data2016/pass4c/Tight/Tailfits/plots/10per_L1L2_tailfits'),'{0}{1}.pdf'.format(outdirSystematics,'data_fitslice_1sig_L1L2')) #Data 1 sigma Fit Slice L1L2
    copyfile('{0}35.pdf'.format('/nfs/slac/g/hps2/mrsolt/hps/Data2016/pass4c/Tight/Tailfits/plots/10per_L1L2_tailfits_5sig'),'{0}{1}.pdf'.format(outdirSystematics,'data_fitslice_5sig_L1L2')) #Data 5 sigma Fit Slice L1L2
    copyfile('{0}35.pdf'.format('/nfs/slac/g/hps2/mrsolt/hps/Data2016/MC/tritrig-wab-beam/Tight/TailFits/plots/tritrig-wab-beam_L1L2_tailfits'),'{0}{1}.pdf'.format(outdirSystematics,'mc_fitslice_1sig_L1L2')) #MC 1 sigma Fit Slice L1L2
    copyfile('{0}35.pdf'.format('/nfs/slac/g/hps2/mrsolt/hps/Data2016/MC/tritrig-wab-beam/Tight/TailFits/plots/tritrig-wab-beam_L1L2_tailfits_5sig'),'{0}{1}.pdf'.format(outdirSystematics,'mc_fitslice_5sig_L1L2')) #MC 5 sigma Fit Slice L1L2

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

    copyfile('{0}5.pdf'.format(datatightL1L2dir),'{0}{1}.pdf'.format(outdirSystematics,'data_floatcut_ip_L1L2')) #Data L1L2 Float Cut IP
    copyfile('{0}10.pdf'.format(datatightL1L2dir),'{0}{1}.pdf'.format(outdirSystematics,'data_floatcut_iso_L1L2')) #Data L1L2 Float Cut Isocut
    copyfile('{0}15.pdf'.format(datatightL1L2dir),'{0}{1}.pdf'.format(outdirSystematics,'data_floatcut_v0p_L1L2')) #Data L1L2 Float Cut V0 Momentum
    copyfile('{0}20.pdf'.format(datatightL1L2dir),'{0}{1}.pdf'.format(outdirSystematics,'data_floatcut_uncChisq_L1L2')) #Data L1L2 Float Cut uncChisq
    copyfile('{0}25.pdf'.format(datatightL1L2dir),'{0}{1}.pdf'.format(outdirSystematics,'data_floatcut_v0proj_L1L2')) #Data L1L2 Float Cut V0 Projection

    copyfile('{0}5.pdf'.format(mctightL1L2dir),'{0}{1}.pdf'.format(outdirSystematics,'mc_floatcut_ip_L1L2')) #MC L1L2 Float Cut IP
    copyfile('{0}10.pdf'.format(mctightL1L2dir),'{0}{1}.pdf'.format(outdirSystematics,'mc_floatcut_iso_L1L2')) #MC L1L2 Float Cut Isocut
    copyfile('{0}15.pdf'.format(mctightL1L2dir),'{0}{1}.pdf'.format(outdirSystematics,'mc_floatcut_v0p_L1L2')) #MC L1L2 Float Cut V0 Momentum
    copyfile('{0}20.pdf'.format(mctightL1L2dir),'{0}{1}.pdf'.format(outdirSystematics,'mc_floatcut_uncChisq_L1L2')) #MC L1L2 Float Cut uncChisq
    copyfile('{0}25.pdf'.format(mctightL1L2dir),'{0}{1}.pdf'.format(outdirSystematics,'mc_floatcut_v0proj_L1L2')) #MC L1L2 Float Cut V0 Projection

    copyfile('{0}{1}MeV_L1L2_floatcut5.pdf'.format(aptightL1L2dir,'80'),'{0}{1}.pdf'.format(outdirSystematics,'ap80MeV_floatcut_ip_L1L2')) #80 MeV A' L1L2 Float Cut IP
    copyfile('{0}{1}MeV_L1L2_floatcut10.pdf'.format(aptightL1L2dir,'80'),'{0}{1}.pdf'.format(outdirSystematics,'ap80MeV_floatcut_iso_L1L2')) #80 MeV A' L1L2 Float Cut Isocut
    copyfile('{0}{1}MeV_L1L2_floatcut15.pdf'.format(aptightL1L2dir,'80'),'{0}{1}.pdf'.format(outdirSystematics,'ap80MeV_floatcut_v0p_L1L2')) #80 MeV A' L1L2 Float Cut V0 Momentum
    copyfile('{0}{1}MeV_L1L2_floatcut20.pdf'.format(aptightL1L2dir,'80'),'{0}{1}.pdf'.format(outdirSystematics,'ap80MeV_floatcut_uncChisq_L1L2')) #80 MeV A' L1L2 Float Cut uncChisq
    copyfile('{0}{1}MeV_L1L2_floatcut25.pdf'.format(aptightL1L2dir,'80'),'{0}{1}.pdf'.format(outdirSystematics,'ap80MeV_floatcut_v0proj_L1L2')) #80 MeV A' L1L2 Float Cut V0 Projection

    copyfile('{0}{1}MeV_L1L2_floatcut5.pdf'.format(aptightL1L2dir,'100'),'{0}{1}.pdf'.format(outdirSystematics,'ap100MeV_floatcut_ip_L1L2')) #100 MeV A' L1L2 Float Cut IP
    copyfile('{0}{1}MeV_L1L2_floatcut10.pdf'.format(aptightL1L2dir,'100'),'{0}{1}.pdf'.format(outdirSystematics,'ap100MeV_floatcut_iso_L1L2')) #100 MeV A' L1L2 Float Cut Isocut
    copyfile('{0}{1}MeV_L1L2_floatcut15.pdf'.format(aptightL1L2dir,'100'),'{0}{1}.pdf'.format(outdirSystematics,'ap100MeV_floatcut_v0p_L1L2')) #100 MeV A' L1L2 Float Cut V0 Momentum
    copyfile('{0}{1}MeV_L1L2_floatcut20.pdf'.format(aptightL1L2dir,'100'),'{0}{1}.pdf'.format(outdirSystematics,'ap100MeV_floatcut_uncChisq_L1L2')) #100 MeV A' L1L2 Float Cut uncChisq
    copyfile('{0}{1}MeV_L1L2_floatcut25.pdf'.format(aptightL1L2dir,'100'),'{0}{1}.pdf'.format(outdirSystematics,'ap100MeV_floatcut_v0proj_L1L2')) #100 MeV A' L1L2 Float Cut V0 Projection

    copyfile('{0}2.pdf'.format('/nfs/slac/g/hps2/mrsolt/hps/Data2016/RadFrad/plots/radfrac'),'{0}{1}.pdf'.format(outdir+'/radfrac/','radfracall')) #Radiative Fraction Log
    copyfile('{0}5.pdf'.format('/nfs/slac/g/hps2/mrsolt/hps/Data2016/RadFrad/plots/radfrac'),'{0}{1}.pdf'.format(outdir+'/radfrac/','radfrac')) #Radiative Fraction
    copyfile('{0}6.pdf'.format('/nfs/slac/g/hps2/mrsolt/hps/Data2016/RadFrad/plots/radfrac'),'{0}{1}.pdf'.format(outdir+'/radfrac/','invmass')) #Invariant Mass with Rad Frac selections

    copyfile('{0}3.pdf'.format('/nfs/slac/g/hps2/mrsolt/hps/Data2016/MC/ap-beam/Tight/acceptance/plots/acceptance_plots'),'{0}{1}.pdf'.format(outdirResults,'accept_100MeV_HitKill_norm')) #100 MeV A' Acceptance with Hit Killing Normalized
    copyfile('{0}4.pdf'.format('/nfs/slac/g/hps2/mrsolt/hps/Data2016/MC/ap-beam/Tight/acceptance/plots/acceptance_plots'),'{0}{1}.pdf'.format(outdirResults,'accept_100MeV_HitKill')) #100 MeV A' Acceptance with Hit Killing
    copyfile('{0}5.pdf'.format('/nfs/slac/g/hps2/mrsolt/hps/Data2016/MC/ap-beam/Tight/acceptance/plots/acceptance_plots'),'{0}{1}.pdf'.format(outdirResults,'accept_80MeV_HitKill_norm')) #80 MeV A' Acceptance with Hit Killing Normalized
    copyfile('{0}6.pdf'.format('/nfs/slac/g/hps2/mrsolt/hps/Data2016/MC/ap-beam/Tight/acceptance/plots/acceptance_plots'),'{0}{1}.pdf'.format(outdirResults,'accept_80MeV_HitKill')) #80 MeV A' Acceptance with Hit Killing
    copyfile('{0}9.pdf'.format('/nfs/slac/g/hps2/mrsolt/hps/Data2016/MC/ap-beam/Tight/acceptance/plots/acceptance_plots'),'{0}{1}.pdf'.format(outdirResults,'accept_100MeV_norm')) #100 MeV A' Acceptance Normalized
    copyfile('{0}10.pdf'.format('/nfs/slac/g/hps2/mrsolt/hps/Data2016/MC/ap-beam/Tight/acceptance/plots/acceptance_plots'),'{0}{1}.pdf'.format(outdirResults,'accept_100MeV')) #100 MeV A' Acceptance 
    copyfile('{0}11.pdf'.format('/nfs/slac/g/hps2/mrsolt/hps/Data2016/MC/ap-beam/Tight/acceptance/plots/acceptance_plots'),'{0}{1}.pdf'.format(outdirResults,'accept_80MeV_norm')) #80 MeV A' Acceptance Normalized
    copyfile('{0}12.pdf'.format('/nfs/slac/g/hps2/mrsolt/hps/Data2016/MC/ap-beam/Tight/acceptance/plots/acceptance_plots'),'{0}{1}.pdf'.format(outdirResults,'accept_80MeV')) #80 MeV A' Acceptance
    copyfile('{0}17.pdf'.format('/nfs/slac/g/hps2/mrsolt/hps/Data2016/MC/ap-beam/Tight/acceptance/plots/acceptance_plots'),'{0}{1}.pdf'.format(outdirResults,'accept_L1L2_HitKill_norm')) #L1L2 Acceptance with Hit Killing Normalized
    copyfile('{0}18.pdf'.format('/nfs/slac/g/hps2/mrsolt/hps/Data2016/MC/ap-beam/Tight/acceptance/plots/acceptance_plots'),'{0}{1}.pdf'.format(outdirResults,'accept_L1L2_HitKill')) #L1L2 Acceptance with Hit Killing
    copyfile('{0}21.pdf'.format('/nfs/slac/g/hps2/mrsolt/hps/Data2016/MC/ap-beam/Tight/acceptance/plots/acceptance_plots'),'{0}{1}.pdf'.format(outdirResults,'accept_L1L1_HitKill_norm')) #L1L1 Acceptance with Hit Killing Normalized
    copyfile('{0}22.pdf'.format('/nfs/slac/g/hps2/mrsolt/hps/Data2016/MC/ap-beam/Tight/acceptance/plots/acceptance_plots'),'{0}{1}.pdf'.format(outdirResults,'accept_L1L1_HitKill')) #L1L1 Acceptance with Hit Killing
    copyfile('{0}19.pdf'.format('/nfs/slac/g/hps2/mrsolt/hps/Data2016/MC/ap-beam/Tight/acceptance/plots/acceptance_plots'),'{0}{1}.pdf'.format(outdirResults,'accept_L1L2_norm')) #L1L2 AcceptanceNormalized
    copyfile('{0}20.pdf'.format('/nfs/slac/g/hps2/mrsolt/hps/Data2016/MC/ap-beam/Tight/acceptance/plots/acceptance_plots'),'{0}{1}.pdf'.format(outdirResults,'accept_L1L2')) #L1L2 Acceptance
    copyfile('{0}23.pdf'.format('/nfs/slac/g/hps2/mrsolt/hps/Data2016/MC/ap-beam/Tight/acceptance/plots/acceptance_plots'),'{0}{1}.pdf'.format(outdirResults,'accept_L1L1_norm')) #L1L1 Acceptance Normalized
    copyfile('{0}24.pdf'.format('/nfs/slac/g/hps2/mrsolt/hps/Data2016/MC/ap-beam/Tight/acceptance/plots/acceptance_plots'),'{0}{1}.pdf'.format(outdirResults,'accept_L1L1')) #L1L1 Acceptance


if __name__ == "__main__" : 
    main() 

