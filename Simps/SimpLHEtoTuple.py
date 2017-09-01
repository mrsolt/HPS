#!/usr/bin/env python
import sys
import getopt
from ROOT import gROOT, TFile, TTree, TNtuple

def print_usage():
    print "\nUsage: {0} <output file basename> <input LHE file>".format(sys.argv[0])
    print "Arguments: "
    print '\t-h: this help message'
    print

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'h')

# Parse the command line arguments
for opt, arg in options:
        if opt=='-h':
            print_usage()
            sys.exit(0)

if len(remainder)!=2:
    print_usage()
    sys.exit(0)

outfile = remainder[0]
inputfile = remainder[1]

gROOT.Reset()

rootfile = TFile(outfile + ".root","RECREATE")

eleBeamNtuple = TNtuple("eleBeamNtuple","data from lhefile file","PID:Px:Py:Pz:E:m")
ApNtuple = TNtuple("ApNtuple","data from lhefile file","PID:Px:Py:Pz:E:m")
RhoNtuple = TNtuple("RhoNtuple","data from lhefile file","PID:Px:Py:Pz:E:m")
eleRecoilNtuple = TNtuple("eleRecoilNtuple","data from lhefile file","PID:Px:Py:Pz:E:m")
WRecoilNtuple = TNtuple("WRecoilNtuple","data from lhefile file","PID:Px:Py:Pz:E:m")
posDecayNtuple = TNtuple("posDecayNtuple","data from lhefile file","PID:Px:Py:Pz:E:m")
eleDecayNtuple = TNtuple("eleDecayNtuple","data from lhefile file","PID:Px:Py:Pz:E:m")
PionNtuple = TNtuple("PionNtuple","data from lhefile file","PID:Px:Py:Pz:E:m")

LHEfile = open(inputfile,"r")
lines = LHEfile.readlines()
readEvent = False
nPart = 0
nEvents = 0
for line in lines:
    if(line == "<mgrwt>\n"): readEvent = False
    if(readEvent):
	nPart += 1
	if(nPart == 1): continue
	varList = line.split()
	PID = int(varList[0])
	Px = float(varList[6])
	Py = float(varList[7])
	Pz = float(varList[8])
	E = float(varList[9])
	m = float(varList[10])
    if(nPart == 2): eleBeamNtuple.Fill(PID,Px,Py,Pz,E,m)
	if(nPart == 4): ApNtuple.Fill(PID,Px,Py,Pz,E,m)
	if(nPart == 5): RhoNtuple.Fill(PID,Px,Py,Pz,E,m)
	if(nPart == 6): eleRecoilNtuple.Fill(PID,Px,Py,Pz,E,m)
	if(nPart == 7): WRecoilNtuple.Fill(PID,Px,Py,Pz,E,m)
	if(nPart == 8): posDecayNtuple.Fill(PID,Px,Py,Pz,E,m)
	if(nPart == 9): eleDecayNtuple.Fill(PID,Px,Py,Pz,E,m)
	if(nPart == 10): PionNtuple.Fill(PID,Px,Py,Pz,E,m)
	nEvents += 1
	if(nEvents%10000 == 0): print "Adding event number " + str(nEvents)
    if(line == "<event>\n"): 
	readEvent = True
	nPart = 0
LHEfile.close()
rootfile.Write()

print outfile + ".root created with " + str(nEvents) + " events"
