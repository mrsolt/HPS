#!/usr/local/bin/python2.7

# 
# bsub_readout.py
#
#	author: Matt Solt
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
    parser.add_argument("-Y", "--Year",   help="Beam energy of run (2015 for 1.05 GeV, 2016 for 2.3 GeV, or 2018 for 4.4 GeV).")
    parser.add_argument("-W", "--time",   help="Amount of time for each batch job.")
    parser.add_argument("-N", "--NLayers",   help="Number of Layers (6 or 7).")

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

    if ((args.Year != "2015") and (args.Year != "2016") and (args.Year != "2018")):
        print "Put a valid entry for the beam energy. -E <2015 for 1.05, 2016 for 2.3, or 2018 for 4.4>"
        print args.Year
        sys.exit(2)

    if ((args.NLayers != "6") and (args.NLayers != "7")):
        print "Put a valid entry for the number of SVT layers. -E <6 or 7>"
        sys.exit(2)

    if (args.NLayers == "6"):
        Run = "5772"
        if (args.Year == "2015"):
            Detector = "HPS-EngRun2015-Nominal-v5-0-fieldmap"
            SteeringFile = "EngineeringRun2015TrigPairs1_Pass2.lcsim" 

        if (args.Year == "2016"):
            Detector = "HPS-PhysicsRun2016-Nominal-v5-0-fieldmap"
            SteeringFile = "PhysicsRun2016TrigPairs1.lcsim"

        if (args.Year == "2018"):
            Detector = "HPS-PhysicsRun2016-Nominal-v5-0-4pt4-fieldmap"
            SteeringFile = "LooseCuts4pt4GeVTrigPairs1.lcsim"

    if (args.NLayers == "7"):
        Run = "1000000"
        if (args.Year == "2015"):
            Detector = "HPS-Proposal2017-Nominal-v2-1pt05-fieldmap"
            SteeringFile = "EngineeringRun2015TrigPairs1_Pass2.lcsim"

        if (args.Year == "2016"):
            Detector = "HPS-Proposal2017-Nominal-v2-2pt3-fieldmap"
            SteeringFile = "PhysicsRun2016TrigPairs1.lcsim"

        if (args.Year == "2018"):
            Detector = "HPS-Proposal2017-Nominal-v2-4pt4-fieldmap"
            SteeringFile = "LooseCuts4pt4GeVTrigPairs1.lcsim"
        
    # Command that will be used to set up the environment
    command = ['bash', '-c', 'source /u/br/omoreno/ldmx/prod/slic_single_particles/init_ilcsoft_rel.sh && env']
    proc = subprocess.Popen(command, stdout=subprocess.PIPE)

    for line in proc.stdout : 
        (key, _, value) = line.partition("=")
        os.environ[key] = value.strip()

    proc.communicate() 
    pprint.pprint(dict(os.environ))

    for line in file_list : 
        
        print "Processing file: " + str(line.strip())

        # Output file name
        output_path = line.strip().replace('.slcio', '_readout')
        output_path = output_path[output_path.rfind("/")+1:]
        print "Writing readout file: " + output_path

        # Name and path of log file
        log_path = output_path.replace('_readout', '.log')
        print "Writing log to: " + log_path

        # Command that will be submitted to the batch system
        command = "java -jar " + args.JarFile + " -i " + line.strip() + " -Ddetector=" + Detector + " -Drun=" + Run + " -DoutputFile=" + output_path + " -r /org/hps/steering/readout/" + SteeringFile
        #batch_command = command
        batch_command = "bsub -W " + args.time + " -o " + log_path + " " + command
        subprocess.Popen(batch_command, shell=True).wait() 

if __name__ == "__main__" : 
    main()
