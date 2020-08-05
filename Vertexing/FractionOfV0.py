import sys
tmpargv = sys.argv
sys.argv = []
import getopt
import ROOT
from ROOT import gROOT, TFile, TTree, TChain, gDirectory, TLine, gStyle, TCanvas, TLegend
sys.argv = tmpargv

#List arguments
def print_usage():
    print "\nUsage: {0} <input file name>".format(sys.argv[0])
    print "Arguments: "
    print '\t-n: Number of total events'
    print '\t-h: this help message'
    print

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'hn:')
nevents = 0
# Parse the command line arguments
for opt, arg in options:
        if opt=='-n':
            nevents=int(arg)
        if opt=='-h':
            print_usage()
            sys.exit(0)

if(nevents == 0):
    print "You must set the total number of triggered events!"
    sys.exit(0)

infile = TFile(remainder[0])

events = infile.Get("ntuple")

def tupleToHisto(events,inHisto,histo,nBins,minX,maxX):
	events.Draw("{0}>>{1}({2},{3},{4})".format(inHisto,histo,nBins,minX,maxX))
	histo = ROOT.gROOT.FindObject(histo)
	return histo

def GetMax(events,inHisto,histo,nBins,minX,maxX):
    events.Draw("{0}>>{1}({2},{3},{4})".format(inHisto,histo,nBins,minX,maxX))
    histo = ROOT.gROOT.FindObject(histo)
    return histo


eventNum = tupleToHisto(events,"tupleevent","eventNum",nevents,0,nevents)

event_with_V0 = 0
event_wo_V0 = 0

for i in range (0,nevents):
    content = eventNum.GetBinContent(i+1)
    if (content == 0): event_wo_V0 = event_wo_V0 +1
    else: event_with_V0 = event_with_V0 +1

print "Total number of events is " + str(nevents)
print "Total number of V0 particles is " + str(events.GetEntries())
print "The number of events with V0 particles is " + str(event_with_V0)
print "The number of events withOUT V0 particles is " + str(event_wo_V0)
print "The fraction of events with a V0 partcle in it " + str(event_with_V0/nevents)