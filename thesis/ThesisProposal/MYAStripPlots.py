#!/usr/local/bin/python2.7

# 
# bsub_slic.py
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
import matplotlib.pyplot as plt
import numpy as np

def main() : 

# Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-b", "--StartTime", help="Start Time")
    parser.add_argument("-s", "--StepTime",   help="Step size")
    parser.add_argument("-n", "--NSteps",   help="Number of steps")
    parser.add_argument("-p", "--Signal",   help="Input Parameter")
    parser.add_argument("-o", "--Output",   help="Output Directory")

    args = parser.parse_args()

    # If all options have not been specified, warn the user and exit
    if len(args) != 5: 
        print "You need exactly 5 arguments. Please see help." 
        sys.exit(2)
    nFEBs = 10
    nHYBs = 4
    output = args.Output+"_"+args.Signal
    c.Print(output+".pdf[")
    for i in range nFEBs:
	for j in range nHYBs:
	    feb = i
	    hybrid = j
            param = "SVT:lv:" + feb + ":" + hybrid + ":" + args.Signal
    	    command = "mySampler -b " + args.StartTime + " -s " + args.StepTime + " -n " + args.NSteps + " " + param
            text_file_name = args.Signal + ".txt"
    	    output_command = "less " + command + " | tee " + text_file_name
            shellOutput = subprocess.check_output(['ls', '-l'])
	    plot(shellOutput,param,args.NSteps,output)
    	    subprocess.Popen(output_command, shell=True).wait()	    
    c.Print(output+".pdf]")


def plot(shellOutput,param,nSteps,output):
    time = shellOutput(x)
    var = shellOutput(y)
    plt.plot(time, var)
    plt.xlabel('time')
    plt.ylabel(param)
    plt.title(param)
    plt.savefig(output+".png")
     


if __name__ == "__main__" : 
    main() 
