import sys
tmpargv = sys.argv
sys.argv = []
import getopt
import ROOT
from ROOT import gROOT, TFile, TTree, TChain, gDirectory, TLine, gStyle, TCanvas, TLegend, TH1F, TF1
sys.argv = tmpargv

#List arguments
def print_usage():
    print "\nUsage: {0} <output file base name> <input A' text file> <input text file name>".format(sys.argv[0])
    print "Arguments: "
    print '\t-z: target z position'
    print '\t-b: mass bin size'
    print '\t-c: z bin size'
    print '\t-d: number of fitted z bins'
    print '\t-s: save fitted histograms'
    print '\t-m: minimum uncVZ'
    print '\t-n: maximum uncVZ'
    print '\t-a: no MC Files'
    print '\t-h: this help message'
    print

minVZ = -20
maxVZ = 70

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'm:n:h')

# Parse the command line argumentz
for opt, arg in options:
		if opt=='-m':
			minVZ = float(arg)
		if opt=='-n':
			maxVZ = float(arg)
		if opt=='-h':
			print_usage()
			sys.exit(0)

gStyle.SetOptStat(0)
c = TCanvas("c","c",800,600)

def saveTuplePlot2D(events,inHisto1,inHisto2,nBinsX,minX,maxX,nBinsY,minY,maxY,outfile,canvas,XaxisTitle="",YaxisTitle="",plotTitle="",stats=0,logY=0):
	events.Draw("{0}:{1}>>histo({2},{3},{4},{5},{6},{7})".format(inHisto2,inHisto1,nBinsX,minX,maxX,nBinsY,minY,maxY))
	histo = ROOT.gROOT.FindObject("histo")
	histo.SetTitle(plotTitle)
	histo.GetXaxis().SetTitle(XaxisTitle)
	histo.GetYaxis().SetTitle(YaxisTitle)
	histo.SetStats(stats)
	histo.Draw("COLZ")
	canvas.SetLogy(logY)
	canvas.Print(outfile+".pdf")
	del histo

def openPDF(outfile,canvas):
	c.Print(outfile+".pdf[")

def closePDF(outfile,canvas):
	c.Print(outfile+".pdf]")

def getPlot(string):
	arr = string.split(" ")
	return arr[0]

def getPlot2D(string):
	arr = string.split(" ")
	if(len(arr) < 2): return ""
	else: return arr[1]

def getMinX2D(string):
	arr = string.split(" ")
	if(len(arr) < 3): return -9999
	else: return float(arr[2])

def getMaxX2D(string):
	arr = string.split(" ")
	if(len(arr) < 4): return -9999
	else: return float(arr[3])

def getMinY(string):
	arr = string.split(" ")
	if(len(arr) < 5): return -9999
	else: return float(arr[4])

def getMaxY(string):
	arr = string.split(" ")
	if(len(arr) < 6): return -9999
	else: return float(arr[5])

nBins = 50

outfile = remainder[0]

apfile = TFile(remainder[1])
mcfile = TFile(remainder[2])

apevents = apfile.Get("ntuple")
mcevents = mcfile.Get("ntuple")

plots = []
plots.append("uncVZ uncVX {0} {1} -3 3".format(minVZ,maxVZ))
plots.append("uncVZ uncVY {0} {1} -3 3".format(minVZ,maxVZ))
plots.append("uncVZ uncVZ {0} {1} {0} {1}".format(minVZ,maxVZ))
plots.append("uncVZ bscChisq {0} {1} 0 10".format(minVZ,maxVZ))
plots.append("uncVZ bscChisq-uncChisq {0} {1} 0 5".format(minVZ,maxVZ))
plots.append("uncVZ sqrt(uncCovZZ) {0} {1} 0 15".format(minVZ,maxVZ))
plots.append("uncVZ eleTrkZ0 {0} {1} -10 10".format(minVZ,maxVZ))
plots.append("uncVZ posTrkZ0 {0} {1} -10 10".format(minVZ,maxVZ))
plots.append("uncVZ eleTrkD0 {0} {1} -10 10".format(minVZ,maxVZ))
plots.append("uncVZ posTrkD0 {0} {1} -10 10".format(minVZ,maxVZ))
plots.append("uncVZ uncVX-(uncVZ)*uncPX/uncPZ {0} {1} -2 2".format(minVZ,maxVZ))
plots.append("uncVZ uncVY-(uncVZ)*uncPY/uncPZ {0} {1} -2 2".format(minVZ,maxVZ))
plots.append("uncVZ (eleTrkChisq/(2.0*eleNTrackHits-5.0)+posTrkChisq/(2.0*posNTrackHits-5.0)) {0} {1} 0 6".format(minVZ,maxVZ))

openPDF(outfile,c)

for i in range(len(plots)):
	plot1 = getPlot(plots[i])
	plot2 = getPlot2D(plots[i])
	minX = getMinX2D(plots[i])
	maxX = getMaxX2D(plots[i])
	minY = getMinY(plots[i])
	maxY = getMaxY(plots[i])
	saveTuplePlot2D(apevents,plot1,plot2,nBins,minX,maxX,nBins,minY,maxY,outfile,c,plot1,plot2,"Ap " + plot2 + " vs. " + plot1)
	saveTuplePlot2D(mcevents,plot1,plot2,nBins,minX,maxX,nBins,minY,maxY,outfile,c,plot1,plot2,"MC " + plot2 + " vs. " + plot1)


closePDF(outfile,c)