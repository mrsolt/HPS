#!/usr/local/bin/python2.7

# 
# Copy local files to analysis note directory
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

    outdir = '/home/mrsolt/hps/Data2016/analysis_note_plots/final/results/'
    finaldir = '/home/mrsolt/HPS/2016Vertexing/FitVertex/plots/final'

    copyfile('{0}1.pdf'.format(finaldir),'{0}{1}.pdf'.format(outdir,'ap_produced')) #A's produced
    copyfile('{0}6.pdf'.format(finaldir),'{0}{1}.pdf'.format(outdir,'ap_rate_L1L1_L1L2')) #A' rate L1L1 + L1L2
    copyfile('{0}8.pdf'.format(finaldir),'{0}{1}.pdf'.format(outdir,'ap_rate_L1L2')) #A' rate L1L2
    copyfile('{0}9.pdf'.format(finaldir),'{0}{1}.pdf'.format(outdir,'ap_rate_L1L1')) #A' rate L1L1
    copyfile('{0}10.pdf'.format(finaldir),'{0}{1}.pdf'.format(outdir,'oim_L1L1_L1L2')) #OIM L1L1 + L1L2
    copyfile('{0}13.pdf'.format(finaldir),'{0}{1}.pdf'.format(outdir,'oim_L1L2')) #OIM L1L2
    copyfile('{0}15.pdf'.format(finaldir),'{0}{1}.pdf'.format(outdir,'oim_L1L1')) #OIM L1L1
    copyfile('{0}23.pdf'.format(finaldir),'{0}{1}.pdf'.format(outdir,'pval_L1L1_L1L2')) #P Value L1L1 + L1L2
    copyfile('{0}24.pdf'.format(finaldir),'{0}{1}.pdf'.format(outdir,'signif_L1L1_L1L2')) #Signficance L1L1 + L1L2 
    copyfile('{0}28.pdf'.format(finaldir),'{0}{1}.pdf'.format(outdir,'pval_L1L2')) #P Value L1L2
    copyfile('{0}29.pdf'.format(finaldir),'{0}{1}.pdf'.format(outdir,'back_L1L2')) #Estimated Background L1L2	
    copyfile('{0}30.pdf'.format(finaldir),'{0}{1}.pdf'.format(outdir,'signif_L1L2')) #Signficance L1L2 
    copyfile('{0}31.pdf'.format(finaldir),'{0}{1}.pdf'.format(outdir,'pval_L1L1')) #P Value L1L1 
    copyfile('{0}32.pdf'.format(finaldir),'{0}{1}.pdf'.format(outdir,'back_L1L1')) #Estimated Background L1L1	
    copyfile('{0}33.pdf'.format(finaldir),'{0}{1}.pdf'.format(outdir,'signif_L1L1')) #Signficance L1L1 
    copyfile('{0}35.pdf'.format(finaldir),'{0}{1}.pdf'.format(outdir,'cand_L1L2')) #Candidate Events L1L2 
    copyfile('{0}36.pdf'.format(finaldir),'{0}{1}.pdf'.format(outdir,'cand_L1L1')) #Candidate Events L1L1 
    copyfile('{0}42.pdf'.format(finaldir),'{0}{1}.pdf'.format(outdir,'zcut_unbiased_L1L2')) #Zcut Unbiased L1L2 
    copyfile('{0}43.pdf'.format(finaldir),'{0}{1}.pdf'.format(outdir,'zcut_unbiased_L1L1')) #Zcut Unbiased L1L1 


if __name__ == "__main__" : 
    main() 