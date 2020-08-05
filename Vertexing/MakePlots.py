import sys
tmpargv = sys.argv
sys.argv = []
import getopt
import ROOT
from ROOT import gROOT, TFile, TTree, TChain, gDirectory, TLine, gStyle, TCanvas, TLegend, TH1F
sys.argv = tmpargv

#List arguments
def print_usage():
    print "\nUsage: {0} <output file base name> <input Data file> <input MC file> <input A' files>".format(sys.argv[0])
    print "Arguments: "
    print '\t-a: include Ap files'
    print '\t-m: include MC files'
    print '\t-d: include data files'
    print '\t-z: target position (default 0.5 mm)'
    print '\t-h: this help message'
    print

zTarg = 0.5
ebeam = 1.05
ap = False
mc = False
data = False

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'hz:e:amd')

# Parse the command line arguments
for opt, arg in options:
		if opt=='-z':
			zTarg = float(arg)
		if opt=='-e':
			ebeam = float(arg)
		if opt=='-a':
			ap = True
		if opt=='-m':
			mc = True
		if opt=='-d':
			data = True
		if opt=='-h':
			print_usage()
			sys.exit(0)

gStyle.SetOptStat(0)
c = TCanvas("c","c",800,600)

def tupleToHisto(events,inHisto,histo,nBins,minX,maxX):
	events.Draw("{0}>>{1}({2},{3},{4})".format(inHisto,histo,nBins,minX,maxX))
	histo = ROOT.gROOT.FindObject(histo)
	return histo

def saveTuplePlot(events,inHisto,nBins,minX,maxX,outfile,canvas,XaxisTitle="",YaxisTitle="",plotTitle="",stats=0):
	events.Draw("{0}>>histo({1},{2},{3})".format(inHisto,nBins,minX,maxX))
	histo = ROOT.gROOT.FindObject("histo")
	histo.SetTitle(plotTitle)
	histo.GetXaxis().SetTitle(XaxisTitle)
	histo.GetYaxis().SetTitle(YaxisTitle)
	histo.SetStats(stats)
	canvas.Print(outfile+".pdf")

def saveTuplePlot2D(events,inHisto1,inHisto2,nBinsX,minX,maxX,nBinsY,minY,maxY,outfile,canvas,XaxisTitle="",YaxisTitle="",plotTitle="",cut="",stats=0,logY=0):
	events.Draw("{0}:{1}>>histo({2},{3},{4},{5},{6},{7})".format(inHisto2,inHisto1,nBinsX,minX,maxX,nBinsY,minY,maxY),cut)
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

def getHisto(histoTitle,infile):
	histo = infile.Get(histoTitle)
	return histo

def drawHisto(histo,XaxisTitle="",YaxisTitle="",plotTitle="",stats=0):
	histo.Draw("")
	#histo.GetXaxis().SetRangeUser(-5,150)
	#histo.GetYaxis().SetRangeUser(0,1.1)
	histo.SetTitle(plotTitle)
	histo.GetXaxis().SetTitle(XaxisTitle)
	histo.GetYaxis().SetTitle(YaxisTitle)
	histo.SetStats(stats)

def saveHisto(histo,outfile,canvas,XaxisTitle="",YaxisTitle="",plotTitle="",stats=0):
	drawHisto(histo,XaxisTitle,YaxisTitle,plotTitle,stats)
	canvas.Print(outfile+".pdf")

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

nBins = 100
minVZ = -60
maxVZ = 60
maxX = 3
minX = -maxX
maxY = 3
minY = -maxY


outfile = remainder[0]

datafile = open(remainder[1],"r")
dataFiles = []

for line in (raw.strip().split() for raw in datafile):
	dataFiles.append(line[0])
dataevents = TChain("ntuple")
for i in range(len(dataFiles)):
    dataevents.Add(dataFiles[i])

mcfile = open(remainder[2],"r")
mcFiles = []

for line in (raw.strip().split() for raw in mcfile):
	mcFiles.append(line[0])
mcevents = TChain("ntuple")
for i in range(len(mcFiles)):
    mcevents.Add(mcFiles[i])

apfile = open(remainder[3],"r")
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

plots = []
plots.append("uncTargProjX/uncTargProjXErr -8 8")
plots.append("uncTargProjY/uncTargProjYErr -8 8")
plots.append("eleTrkZ0/eleTrkZ0Err -8 8")
plots.append("posTrkZ0/posTrkZ0Err -8 8")
plots.append("eleTrkD0/eleTrkD0Err -8 8")
plots.append("posTrkD0/posTrkD0Err -8 8")
plots.append("posTrkD0/posTrkD0Err -8 8")

openPDF(outfile,c)

for i in range(len(plots)):
	plot = getPlot(plots[i])
	minimum = getMin(plots[i])
	maximum = getMax(plots[i])
	if(data):
		saveTuplePlot(dataevents,plot,nBins,minimum,maximum,outfile,c,plot,""," Data " + plot)
		saveTuplePlot2D(dataevents,"uncVZ",plot,nBins,minVZ,maxVZ,nBins,minimum,maximum,outfile,c,"uncVZ",plot," Data " + plot)
	if(mc):
		saveTuplePlot(mcevents,plot,nBins,minimum,maximum,outfile,c,plot,""," MC " + plot)
		saveTuplePlot2D(mcevents,"uncVZ",plot,nBins,minVZ,maxVZ,nBins,minimum,maximum,outfile,c,"uncVZ",plot," MC " + plot)
	if(ap):
		for j in range(len(events)):
			saveTuplePlot(events[j],plot,nBins,minimum,maximum,outfile,c,plot,"",str(mass[j]) + " GeV A' " + plot)
			saveTuplePlot2D(events[j],"uncVZ",plot,nBins,minVZ,maxVZ,nBins,minimum,maximum,outfile,c,"uncVZ",plot,str(mass[j]) + " GeV A' " + plot)

closePDF(outfile,c)