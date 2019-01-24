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
    print '\t-m: minimum uncVZ'
    print '\t-n: maximum uncVZ'
    print '\t-h: this help message'
    print

zTarg = -4
minVZ = -35
maxVZ = 25

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'z:m:n:h')

# Parse the command line argumentz
for opt, arg in options:
		if opt=='-z':
			zTarg = float(arg)
		if opt=='-m':
			minVZ = float(arg)
		if opt=='-n':
			maxVZ = float(arg)
		if opt=='-h':
			print_usage()
			sys.exit(0)

gStyle.SetOptStat(0)
c = TCanvas("c","c",800,600)

def saveTuplePlot(events,inHisto,nBins,minX,maxX,outfile,canvas,XaxisTitle="",YaxisTitle="",plotTitle="",m=0,mRange=9999,stats=0,logY=0):
	events.Draw("{0}>>histo({1},{2},{3})".format(inHisto,nBins,minX,maxX),"uncM>{0}-{1}&&uncM<{0}+{1}".format(m,mRange))
	histo = ROOT.gROOT.FindObject("histo")
	histo.SetTitle(plotTitle)
	histo.GetXaxis().SetTitle(XaxisTitle)
	histo.GetYaxis().SetTitle(YaxisTitle)
	histo.SetStats(stats)
	histo.Draw()
	canvas.SetLogy(logY)
	canvas.Print(outfile+".pdf")
	histo.Write(plotTitle)
	del histo

def fitPlot(events,inHisto,nBinsX,minX,maxX,outfile,canvas,XaxisTitle="",YaxisTitle="",plotTitle="",stats=1):
	events.Draw("{0}>>histo({1},{2},{3})".format(inHisto,nBinsX,minX,maxX))
	histo = ROOT.gROOT.FindObject("histo")
	histo.SetTitle(plotTitle)
	histo.GetXaxis().SetTitle(XaxisTitle)
	histo.GetYaxis().SetTitle(YaxisTitle)
	histo.SetStats(stats)
	histo.Fit("gaus")
	histo.Draw()
	canvas.Print(outfile+".pdf")
	histo.Write(plotTitle)
	del histo

def openPDF(outfile,canvas):
	c.Print(outfile+".pdf[")

def closePDF(outfile,canvas):
	c.Print(outfile+".pdf]")

def getPlot(string):
	arr = string.split(" ")
	return arr[0]

def getMinX(string):
	arr = string.split(" ")
	if(len(arr) < 2): return -9999
	else: return float(arr[1])

def getMaxX(string):
	arr = string.split(" ")
	if(len(arr) < 3): return -9999
	else: return float(arr[2])

nBins = 50

outfile = remainder[0]

events = TChain("ntuple")

events = TChain("ntuple")
for i in range(1,len(remainder)):
    events.Add(remainder[i])

rootfile = TFile(outfile+".root","recreate")

plots = []
plots.append("uncVZ {0} {1}".format(minVZ,maxVZ))
plots.append("sqrt(uncCovZZ) 0 10")
plots.append("uncVX -1 1")
plots.append("sqrt(uncCovXX) 0 0.5")
plots.append("uncVY -1 1")
plots.append("sqrt(uncCovYY) 0 0.25")
plots.append("bscVZ {0} {1}".format(minVZ,maxVZ))
plots.append("sqrt(bscCovZZ) 0 10")
plots.append("bscVX -1 1")
plots.append("sqrt(bscCovXX) 0 0.25")
plots.append("bscVY -1 1")
plots.append("sqrt(bscCovYY) 0 0.25")
plots.append("bscChisq 0 10")
plots.append("uncChisq 0 10")
plots.append("uncM 0 0.2")
plots.append("uncMErr 0 0.01")
plots.append("bscM 0 0.2")
plots.append("bscMErr 0 0.01")
plots.append("uncP 0 3")
plots.append("uncMomErr 0 0.15")
plots.append("uncPX -0.2 0.2")
plots.append("uncMomXErr 0 0.01")
plots.append("uncPY -0.2 0.2")
plots.append("uncMomYErr 0 0.005")
plots.append("uncPZ 0 3")
plots.append("uncMomZErr 0 0.15")
plots.append("uncTargProjXErr 0 0.5")
plots.append("uncTargProjYErr 0 0.5")
plots.append("eleTrkZ0Err 0 0.5")
plots.append("posTrkZ0Err 0 0.5")
plots.append("eleTrkD0Err 0 1")
plots.append("posTrkD0Err 0 1")

fitplots = []
fitplots.append("(uncVZ-{0})/sqrt(uncCovZZ) -5 5".format(zTarg))
fitplots.append("(uncVX)/sqrt(uncCovXX) -5 5")
fitplots.append("(uncVY)/sqrt(uncCovYY) -5 5")
fitplots.append("(bscVZ-{0})/sqrt(bscCovZZ) -5 5".format(zTarg))
fitplots.append("(bscVX)/sqrt(bscCovXX) -5 5")
fitplots.append("(bscVY)/sqrt(bscCovYY) -5 5")
fitplots.append("uncTargProjX/uncTargProjXErr -5 5")
fitplots.append("uncTargProjY/uncTargProjYErr -5 5")
fitplots.append("eleTrkZ0/eleTrkZ0Err -5 5")
fitplots.append("posTrkZ0/posTrkZ0Err -5 5")
fitplots.append("eleTrkD0/eleTrkD0Err -5 5")
fitplots.append("posTrkD0/posTrkD0Err -5 5")

openPDF(outfile,c)

gStyle.SetOptFit()
for i in range(len(fitplots)):
	plot = getPlot(fitplots[i])
	minX = getMinX(fitplots[i])
	maxX = getMaxX(fitplots[i])
	fitPlot(events,plot,nBins,minX,maxX,outfile,c,plot,"",plot)

for i in range(len(plots)):
	plot = getPlot(plots[i])
	minX = getMinX(plots[i])
	maxX = getMaxX(plots[i])
	saveTuplePlot(events,plot,nBins,minX,maxX,outfile,c,plot,"",plot)

closePDF(outfile,c)

rootfile.Close()