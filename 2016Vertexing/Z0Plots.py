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
    print '\t-a: do not use Ap file (default use)'
    print '\t-h: this help message'
    print

zTarg = -4.3
ebeam = 2.3
minVZ = -20
maxVZ = 60
nBins = 100
useAp = True


options, remainder = getopt.gnu_getopt(sys.argv[1:], 'hz:m:n:e:b:a')

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
		if opt=='-a':
			useAp = False
		if opt=='-h':
			print_usage()
			sys.exit(0)

gStyle.SetOptStat(0)
c = TCanvas("c","c",800,600)

def saveTupleFitPlot(events,inHisto,nBins,mass,minX,maxX,minVZ,maxVZ,cut,outfile,canvas):
	events.Draw("{0}:uncVZ>>histo({1},{4},{5},{1},{2},{3})".format(inHisto,nBins,minX,maxX,minVZ,maxVZ),cut)
	histo = ROOT.gROOT.FindObject("histo")
	histo.SetTitle("{0} vs uncVZ {1:.0f} MeV Mass Bin".format(inHisto,mass*1000))
	histo.GetXaxis().SetTitle("uncVZ (mm)")
	histo.GetYaxis().SetTitle("{0} (mm)".format(inHisto))
	histo.Draw("COLZ")
	canvas.Print(outfile+".pdf")

def openPDF(outfile,canvas):
	c.Print(outfile+".pdf[")

def closePDF(outfile,canvas):
	c.Print(outfile+".pdf]")

def getPlot(string):
	arr = string.split(" ")
	return arr[0]

def getMin(string):
	arr = string.split(" ")
	if(len(arr) < 2): return ""
	else: return float(arr[1])

def getMax(string):
	arr = string.split(" ")
	if(len(arr) < 3): return ""
	else: return float(arr[2])

outfile = remainder[0]

if(not useAp):
	#inFile = TFile(remainder[1])
	#events = inFile.Get("ntuple")
	file = open(remainder[1],"r")
	files = []
	for line in (raw.strip().split() for raw in file):
		files.append(line[0])
	events = TChain("ntuple")
	for i in range(len(files)):
		events.Add(files[i])
	mass = []
	nMass = 20
	minMass = 0.050
	massBin = 0.005
	for i in range(nMass):
		m = minMass + i * massBin
		mass.append(m)

if(useAp):
	apfile = open(remainder[1],"r")
	apfiles = []
	events = []
	mass = []

	for line in (raw.strip().split() for raw in apfile):
		apfiles.append(TFile(line[0]))

	for i in range(len(apfiles)):
		events.append(apfiles[i].Get("ntuple"))
		events[i].Draw("triM>>dummy({0},{1},{2})".format(1000,0,1))
		dummy = ROOT.gROOT.FindObject("dummy")
		mass.append(dummy.GetMean())
		del dummy

minZ0 = -4.0
maxZ0 = -minZ0
plots = []
#plots.append("eleTrkZ0 {0} {1}".format(minZ0,maxZ0))
#plots.append("posTrkZ0 {0} {1}".format(minZ0,maxZ0))
plots.append("eleTrkD0 {0} {1}".format(minZ0,maxZ0))
plots.append("posTrkD0 {0} {1}".format(minZ0,maxZ0))
#plots.append("sqrt(uncCovZZ) {0} {1}".format(0,5))

openPDF(outfile,c)

if(useAp):
	for i in range(len(plots)):
		plot = getPlot(plots[i])
		minimum = getMin(plots[i])
		maximum = getMax(plots[i])
		mass_range = 0.005
		for j in range(len(mass)):
			masscut = "uncM>{0}&&uncM<{1}".format(mass[j]-mass_range,mass[j]+mass_range)
			saveTupleFitPlot(events[j],plot,nBins,mass[j],minimum,maximum,minVZ,maxVZ,masscut,outfile,c)

if(not useAp):
	for i in range(len(plots)):
		plot = getPlot(plots[i])
		minimum = getMin(plots[i])
		maximum = getMax(plots[i])
		mass_range = 0.005
		for j in range(len(mass)):
			masscut = "uncM>{0}&&uncM<{1}".format(mass[j]-mass_range,mass[j]+mass_range)
			saveTupleFitPlot(events,plot,nBins,mass[j],minimum,maximum,minVZ,maxVZ,masscut,outfile,c)

closePDF(outfile,c)