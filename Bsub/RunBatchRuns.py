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
    parser.add_argument("-i", "--input_list", help="List of runs to process.")
    parser.add_argument("-l", "--outputFile",   help="Output Logs.")
    parser.add_argument("-c", "--com",   help="Input command.")
    parser.add_argument("-W", "--time",   help="Time of job for batch.")

    args = parser.parse_args()

    # If a list of input files has not been specified, warn the user and 
    # exit the application.
    if args.input_list is None : 
        print "A list of lcio files needs to be specified." 
        sys.exit(2)

    if args.com is None : 
        print "A command needs to be specified." 
        sys.exit(2)

    #Time of each batch job. Default is no batch job submitted
    bsub = ""
    if(args.time is not None):
        bsub = "bsub -W " + args.time + ' -R "rhel60" '

    # Open the file containing the list of stdhep files to process
    try : 
        run_list = open(args.input_list, 'r')
    except IOError : 
        print "Unable to open file " + str(args.input_list)
        sys.exit(2)

    for line in run_list : 
        run = line.strip()
        print "Processing run: " + str(line.strip())
        # Command that will be submitted to the batch system
        output = args.outputFile + "_{0}.log".format(run)
        command = bsub + " " + args.com.format(run) + " -o " + output
        subprocess.Popen(command, shell=True).wait() 
        print args.com.format(run)
        files = ""
        time.sleep(1)

if __name__ == "__main__" : 
    main() 

