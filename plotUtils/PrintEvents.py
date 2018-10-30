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
    print '\t-h: this help message'
    print


options, remainder = getopt.gnu_getopt(sys.argv[1:], 'h')

# Parse the command line arguments
for opt, arg in options:
		if opt=='-h':
			print_usage()
			sys.exit(0)

outfile = remainder[0]
events = TChain("ntuple")
for i in range(1,len(remainder)):
    events.Add(remainder[i])


run = array('d',[0])
event = array('d',[0])

events.Branch("run",run,"run")
events.Branch("event",event,"event")

txtfile = open(outfile+".txt","w")

for entry in xrange(events.GetEntries()):
	events.GetEntry(entry)
	txtfile.write(str(events.run) + " " + str(events.event) + "\n")

txtfile.close()