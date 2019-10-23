#!/usr/local/bin/python2.7

# 
# Make Data Tuples
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
    parser.add_argument("-i", "--input_list", help="List lcio files to process.")
    parser.add_argument("-o", "--outputFile",   help="Output File Directory.")
    parser.add_argument("-W", "--time",   help="Time of job for batch.")

    args = parser.parse_args()

    # If a list of input files has not been specified, warn the user and 
    # exit the application.
    if args.input_list is None : 
        print "A list of lcio files needs to be specified." 
        sys.exit(2)

    #Time of each batch job. Default is no batch job submitted
    bsub = ""
    if(args.time is not None):
        bsub = "bsub -W " + args.time + ' -R "rhel60" '
    else:
        bsub = 'bsub -W 4:00 -R "rhel60" '

    # Open the file containing the list of stdhep files to process
    try : 
        file_list = open(args.input_list, 'r')
    except IOError : q
        print "Unable to open file " + str(args.input_list)
        sys.exit(2)

    addon = ".root"
    outputfile = "/nfs/slac/g/hps_data2/tuple/2pt3/data/"
    if(args.time is not None):
        outputfile = args.outputFile
    com = "/nfs/slac/g/hps2/mrsolt/hps/HPS-CODE/ANALYSIS/tuple/makeTree.py "
    for line in file_list : 
        file = line.strip()
        print "Processing file: " + str(file)
        # Command that will be submitted to the batch system
        output = file.replace('.txt','')
        output = output.replace('/nfs/slac/g/hps_data2/data/physrun2016/pass4v0FullPass/tuple/','')
        log = outputfile + "logs/" + output + ".log "
        output = outputfile + output + addon + " "
        command = bsub + " -o " + log + com  + output + file
        subprocess.Popen(command, shell=True).wait() 
        print "Writing output file: " + output
        time.sleep(0.1)

if __name__ == "__main__" : 
    main() 