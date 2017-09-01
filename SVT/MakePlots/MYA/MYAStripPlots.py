#!/usr/local/bin/python2.7

# 
# This script dumps MYA values of a specfic 
# SVT DAQ variable for all Febs/hybrids in
# a text file
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
import numpy as np

def main() : 

# Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-b", "--StartTime", help="Start Time")
    parser.add_argument("-s", "--StepTime",   help="Step size")
    parser.add_argument("-n", "--NSteps",   help="Number of steps")
    parser.add_argument("-o", "--Output",   help="Output Directory")

    args = parser.parse_args()
    #Output variables of interest
    plotVar = []
    plotVar.append("avdd:i_rd")
    plotVar.append("avdd:stat")
    plotVar.append("avdd:vf")
    plotVar.append("avdd:vn")
    plotVar.append("avdd:v_set_rd")
    plotVar.append("dpm:dpm_rd")
    plotVar.append("dvdd:i_rd")
    plotVar.append("dvdd:stat")
    plotVar.append("dvdd:vf")
    plotVar.append("dvdd:vn")
    plotVar.append("dvdd:v_set_rd")
    plotVar.append("stat")
    plotVar.append("sync:sync_rd")
    plotVar.append("v125:i_rd")
    plotVar.append("v125:stat")
    plotVar.append("v125:vf")
    plotVar.append("v125:vn")
    plotVar.append("v125:v_set_rd")

    nFEBs = 10
    nHYBs = 4

    #Loop over all the variables
    for k in range (len(plotVar)):
        #Make a directory for each variable
        mkDir = "mkdir " + args.Output + plotVar[k]
        print "Making Directory " + mkDir
        subprocess.Popen(mkDir, shell=True).wait()
        #Loop over all Febs
        for i in range (nFEBs):
            #Loop over all hybrids
	    for j in range (nHYBs):
	        feb = i
	        hybrid = j
                param = "SVT:lv:" + str(feb) + ":" + str(hybrid) + ":" + plotVar[k] #Epics variable
    	        command = "mySampler -b " + args.StartTime + " -s " + args.StepTime + " -n " + args.NSteps + " " + param #Shell command
                text_file_name = "feb_" + str(feb) + "_hyb_" + str(hybrid) + ".txt" #Text file output
    	        output_command = command + " > " + args.Output + plotVar[k] + "/" + text_file_name
                print output_command
    	        subprocess.Popen(output_command, shell=True).wait()	    

if __name__ == "__main__" : 
    main() 
