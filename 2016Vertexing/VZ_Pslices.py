import sys
tmpargv = sys.argv
sys.argv = []
import getopt
import ROOT
from ROOT import gROOT, TFile, TTree, TChain, gDirectory, TLine, gStyle, TCanvas, TLegend, TH1F
sys.argv = tmpargv

#List arguments
def print_usage():
    print "\nUsage: {0} <output file base name> <input text Data file> <input text MC file> <input text A' files>".format(sys.argv[0])
    print "Arguments: "
    print '\t-z: target position (default -4.3 mm)'
    print '\t-m: minimum uncVZ (default -30 mm)'
    print '\t-n: maximum uncVZ (default 60 mm)'
    print '\t-e: beam energy (default 2.3 GeV)'
    print '\t-b: number of bins (default 100)'
    print '\t-h: this help message'
    print

zTarg = -4.3
ebeam = 2.3
minVZ = -50
maxVZ = 50
nBins = 100


options, remainder = getopt.gnu_getopt(sys.argv[1:], 'hz:m:n:e:b:')

# Parse the command line arguments
for opt, arg in options:
		if opt=='-z':
			zTarg = float(arg)
		if opt=='-m':
			minVZ = float(arg)
		if opt=='-n':
			maxVZ = float(arg)
		if opt=='-e':
			ebeam = float(arg)
		if opt=='-b':
			nBins = float(arg)
		if opt=='-h':
			print_usage()
			sys.exit(0)

gStyle.SetOptStat(0)
c = TCanvas("c","c",800,600)

def saveTuplePlot(events,inHisto,nBins,minVZ,maxVZ,minP,maxP,cut,outfile,canvas):
	events.Draw("{0}>>histo({1},{2},{3})".format(inHisto,nBins,minVZ,maxVZ),cut)
	histo = ROOT.gROOT.FindObject("histo")
	histo.SetTitle("{0} P Bin {1:.3f} < uncP < {2:.3f}".format(inHisto,minP,maxP))
	histo.GetXaxis().SetTitle("uncVZ (mm)")
	histo.Draw("COLZ")
	canvas.SetLogy(1)
	canvas.Print(outfile+".pdf")

def openPDF(outfile,canvas):
	c.Print(outfile+".pdf[")

def closePDF(outfile,canvas):
	c.Print(outfile+".pdf]")


outfile = remainder[0]

file = open(remainder[1],"r")
Files = []

for line in (raw.strip().split() for raw in file):
	Files.append(line[0])
events = TChain("ntuple")
for i in range(len(Files)):
	events.Add(Files[i])

cuts = []
cuts.append("")
cuts.append("eleP>0.4**posP>0.4")
cuts.append("eleP>0.5**posP>0.5")
cuts.append("eleP>0.6**posP>0.6")
pmin = 0.5
pmax = 2.5
nPBins = 10
p_range = 0.1

openPDF(outfile,c)

for i in range(len(cuts)):
	events.Draw("{0}:uncVZ>>histo({1},{4},{5},{1},{2},{3})".format("uncP",nBins,0.,3.,minVZ,maxVZ),cuts[i])
	histo = ROOT.gROOT.FindObject("histo")
	histo.SetTitle("uncP vs uncVZ for {0}".format(cuts[i]))
	histo.GetXaxis().SetTitle("uncVZ (mm)")
	histo.GetYaxis().SetTitle("uncP (GeV)")
	histo.Draw("COLZ")
	c.SetLogy(0)
	c.Print(outfile+".pdf")
	del histo
	for j in range(nPBins):
		p = pmin + (pmax-pmin)/float(nPBins) * j
		pcut = "uncP>{0}&&uncP<{1}".format(p-p_range,p+p_range)
		if(i == 0):
			cut = pcut
		else:
			cut = pcut + "&&" + cuts[i]
		saveTuplePlot(events,"uncVZ",nBins,minVZ,maxVZ,p-p_range,p+p_range,cut,outfile,c)

closePDF(outfile,c)