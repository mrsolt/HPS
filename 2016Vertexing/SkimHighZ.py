import sys
tmpargv = sys.argv
sys.argv = []
import getopt
from array import array
import ROOT
from ROOT import gROOT, TFile, TTree, TChain, gDirectory, TLine, gStyle, TCanvas, TLegend, TH2F
sys.argv = tmpargv

#List arguments
def print_usage():
    print "\nUsage: {0} <output file base name> <input file name>".format(sys.argv[0])
    print "Arguments: "
    print '\t-z: high Z skim value (default false)'
    print '\t-h: this help message'
    print

maxVZ = 10

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'z:h')

# Parse the command line arguments
for opt, arg in options:
		if opt=='-z':
			maxVZ = float(arg)
		if opt=='-h':
			print_usage()
			sys.exit(0)


outfile = open(remainder[0]+".txt","w")
events = TChain("ntuple")
for i in range(1,len(remainder)):
    events.Add(remainder[i])


run = array('d',[0])
event = array('d',[0])
uncVZ = array('d',[0])

events.Branch("run",run,"run/I")
events.Branch("event",event,"event/I")
events.Branch("uncVZ",uncVZ,"uncVZ/D")

nevents = events.GetEntries()

for entry in xrange(nevents):
	events.GetEntry(entry)
	if(events.uncVZ < maxVZ): continue
	outfile.write("{0} {1}\n".format(events.run,events.event))

outfile.close()