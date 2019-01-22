#!/usr/local/bin/python2.7

# 
# Run script over a list of runs
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
    parser.add_argument("-r", "--run_list", help="List runs to process.")
    parser.add_argument("-i", "--input_file", help="Input file basename.")
    parser.add_argument("-c", "--com", help="Script and command.")
    parser.add_argument("-o", "--outputFile",   help="Output File.")
    parser.add_argument("-W", "--time",   help="Time of job for batch.")

    args = parser.parse_args()

    # If a list of runs has not been specified, warn the user and 
    # exit the application.
    if args.run_list is None : 
        print "A list of runs needs to be specified." 
        sys.exit(2)

    #Time of each batch job. Default is no batch job submitted
    bsub = ""
    if(args.time is not None):
        bsub = "bsub -W " + args.time + ' -R "rhel60" '

    # Open the file containing the list of stdhep files to process
    try : 
        file_list = open(args.run_list, 'r')
    except IOError : 
        print "Unable to open file " + str(args.run_list)
        sys.exit(2)

    for line in file_list : 
        run = line.strip()
        file = input_file + str(run) + "*"
        print "Processing run: " + str(run)
        # Command that will be submitted to the batch system
        output = args.outputFile + "_" + str(run)
        command = bsub + " " + com + " " + output + " " + file
        subprocess.Popen(command, shell=True).wait() 
        print "Writing output file: " + output
        time.sleep(1)

if __name__ == "__main__" : 
    main() 

