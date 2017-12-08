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

    args = parser.parse_args()

    # If a list of input files has not been specified, warn the user and 
    # exit the application.
    if args.input_list is None : 
        print "A list of lcio files needs to be specified." 
        sys.exit(2)

    # Open the file containing the list of stdhep files to process
    try : 
        file_list = open(args.input_list, 'r')
    except IOError : 
        print "Unable to open file " + str(args.input_list)
        sys.exit(2)

    files = ""

    for line in file_list : 
	    files = files + " -i " + line.strip()
        
    print "Processing file: " + str(line.strip())

    # Output file name
    print "Writing lcio and root file: " + args.outputFile

    # Command that will be submitted to the batch system
    command = "java -jar " + args.JarFile + " " + args.steeringFile  + " " + files + " -DoutputFile=" + args.outputFile
    subprocess.Popen(command, shell=True).wait() 

if __name__ == "__main__" : 
    main() 

