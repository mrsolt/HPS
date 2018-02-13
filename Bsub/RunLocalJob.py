#!/usr/local/bin/python2.7

# 
# bsub_MakeTupleMC.py
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
    parser.add_argument("-j", "--JarFile",   help="Jar file for jobs.")
    parser.add_argument("-o", "--outputFile",   help="Output File.")
    parser.add_argument("-s", "--steeringFile",   help="Steering File.")
    parser.add_argument("-n", "--nFiles",   help="Number of Files per command.")
    parser.add_argument("-t", "--opt",   help="List of options.")
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
        bsub = "bsub -W " + args.time

    #Number of Files per batch job. Default is 1
    n = 1
    if(args.nFiles is not None):
        n = int(args.nFiles)

    # Open the file containing the list of stdhep files to process
    try : 
        file_list = open(args.input_list, 'r')
    except IOError : 
        print "Unable to open file " + str(args.input_list)
        sys.exit(2)

    files = ""

    file_max = 0
    m = 0
    for line in file_list : 
	    files = files + " -i " + line.strip()
        file_max = file_max + 1
        print "Processing file: " + str(line.strip())
        if(n == file_max):
            m = m + 1
            # Command that will be submitted to the batch system
            output = args.outputFile + str(m)
            command = bsub + " java -jar " + args.JarFile + " " + args.steeringFile  + " " + files + " -DoutputFile=" + output + " " + opt
            subprocess.Popen(command, shell=True).wait() 
            file_max = 0
            print "Writing output file: " + output

if __name__ == "__main__" : 
    main() 

