#!/usr/local/bin/python2.7

# 
# Submit Batch Job general script
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

    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--inputDir",   help="Input directory name.")
    parser.add_argument("-l", "--logFile",   help="Output Logs.")
    parser.add_argument("-o", "--outputFiles",   help="Output files.")
    parser.add_argument("-f", "--inputFiles",   help="Input files.")
    parser.add_argument("-c", "--clT",   help="cluster time shift.")
    parser.add_argument("-t", "--scriptcut",   help="cut from script.")
    parser.add_argument("-W", "--time",   help="Time of job for batch.")

    args = parser.parse_args()

    # If a list of input files has not been specified, warn the user and 
    # exit the application.
    if args.inputFiles is None : 
        print "A list of lcio files needs to be specified." 
        sys.exit(2)

    #Time of each batch job. Default is no batch job submitted
    bsub = ""
    if(args.time is not None):
        bsub = "bsub -W " + args.time + ' -R "rhel60" '

    # Open the file containing the list of stdhep files to process
    try : 
        run_list = open(args.inputFiles, 'r')
    except IOError : 
        print "Unable to open file " + str(args.inputFiles)
        sys.exit(2)

    cutcommand = " python /nfs/slac/g/hps2/mrsolt/hps/HPS-CODE/ANALYSIS/vertexing/vertexCuts2016.py -c {0} -j {1} -k {2} -m {3} -n {4} -o {5} -p {6} -a {7} -b {8} -{9} "
    for line in run_list : 
        #run = line.strip()
        linesplit = line.split()
        run = linesplit[0]
        uncVX = linesplit[1]
        uncVXSig = linesplit[2]
        uncVY = linesplit[3]
        uncVYSig = linesplit[4]
        uncTargProjX = linesplit[7]
        uncTargProjXSig = linesplit[8]
        uncTargProjY = linesplit[9]
        uncTargProjYSig = linesplit[10]
        print "Processing run: " + str(line.strip())
        # Command that will be submitted to the batch system
        log = args.logFile + "_{0}.log".format(run)
        outFile = args.outputFiles + "_{0}.root".format(run)
        cut = cutcommand.format(args.clT,uncVX,uncVXSig,uncVY,uncVYSig,uncTargProjX,uncTargProjXSig,uncTargProjY,uncTargProjYSig,args.scriptcut)
        command = bsub + " -o " + log + cut + outFile + " " + args.inputDir.format(run)
        subprocess.Popen(command, shell=True).wait() 
        print command
        files = ""
        time.sleep(1)

if __name__ == "__main__" : 
    main() 

