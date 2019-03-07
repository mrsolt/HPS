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
minVZ = zTarg
maxVZ = 120
beamX = 0.0
beamY = 0.0

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'z:x:y:m:n:h')

# Parse the command line argumentz
for opt, arg in options:
		if opt=='-z':
			zTarg = float(arg)
		if opt=='-x':
			beamX = float(arg)
		if opt=='-y':
			beamY = float(arg)
		if opt=='-m':
			minVZ = float(arg)
		if opt=='-n':
			maxVZ = float(arg)
		if opt=='-h':
			print_usage()
			sys.exit(0)

gStyle.SetOptStat(0)
c = TCanvas("c","c",800,600)

def saveTuplePlot(events,inHisto,nBins,minX,maxX,outfile,canvas,XaxisTitle="",YaxisTitle="",plotTitle="",stats=0,logY=0):
	events.Draw("{0}>>histo({1},{2},{3})".format(inHisto,nBins,minX,maxX))
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

def saveTuplePlot2D(events,inHisto1,inHisto2,nBinsX,minX,maxX,nBinsY,minY,maxY,outfile,canvas,XaxisTitle="",YaxisTitle="",plotTitle="",stats=0,logY=0):
	events.Draw("{0}:{1}>>histo({2},{3},{4},{5},{6},{7})".format(inHisto1,inHisto2,nBinsX,minX,maxX,nBinsY,minY,maxY))
	histo = ROOT.gROOT.FindObject("histo")
	histo.SetTitle(plotTitle)
	histo.GetXaxis().SetTitle(XaxisTitle)
	histo.GetYaxis().SetTitle(YaxisTitle)
	histo.SetStats(stats)
	histo.Draw("COLZ")
	canvas.SetLogy(logY)
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
plots.append("uncChisq 0 10")
plots.append("uncChisqProb 0 1")
plots.append("bscChisq 0 20")
plots.append("bscChisqProb 0 1")
plots.append("tarChisq 0 30")
plots.append("tarChisqProb 0 1")

openPDF(outfile,c)

for i in range(len(plots)):
	plot = getPlot(plots[i])
	minX = getMinX(plots[i])
	maxX = getMaxX(plots[i])
	saveTuplePlot(events,plot,nBins,minX,maxX,outfile,c,plot,"",plot)
	saveTuplePlot2D(events,plot,"triEndZ",nBins,minX,maxX,nBins,minVZ,maxVZ,outfile,c,plot,"triEndZ",plot+" vs Truth Z")

closePDF(outfile,c)

rootfile.Close()