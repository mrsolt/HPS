import sys
tmpargv = sys.argv
sys.argv = []
import getopt
import ROOT
from ROOT import gROOT, TFile, TTree, TChain, gDirectory, TLine, gStyle, TCanvas, TLegend, TH1F
sys.argv = tmpargv

#List arguments
def print_usage():
    print "\nUsage: {0} <output file base name> <input file name>".format(sys.argv[0])
    print "Arguments: "
    print '\t-z: target z position'
    print '\t-b: mass bin size'
    print '\t-m: minimum uncVZ'
    print '\t-n: maximum uncVZ'
    print '\t-h: this help message'
    print

zTarg = 0.5
minVZ = -20
maxVZ = 120
massBin = 0.002

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'z:b:m:n:h')

# Parse the command line argumentz
for opt, arg in options:
		if opt=='-z':
			zTarg = float(arg)
		if opt=='-b':
			massBin = float(arg)
		if opt=='-m':
			minVZ = float(arg)
		if opt=='-n':
			maxVZ = float(arg)
		if opt=='-h':
			print_usage()
			sys.exit(0)

gStyle.SetOptStat(0)
c = TCanvas("c","c",800,600)

def saveTuplePlot(events,inHisto,nBins,minX,maxX,outfile,canvas,XaxisTitle="",YaxisTitle="",plotTitle="",m=0,mRange=0,stats=0,logY=0):
	events.Draw("{0}>>histo({1},{2},{3})".format(inHisto,nBins,minX,maxX),"uncM>{0}-{1}&&uncM<{0}+{1}".format(m,mRange))
	histo = ROOT.gROOT.FindObject("histo")
	histo.SetTitle(plotTitle)
	histo.GetXaxis().SetTitle(XaxisTitle)
	histo.GetYaxis().SetTitle(YaxisTitle)
	histo.SetStats(stats)
	histo.Draw()
	canvas.SetLogy(logY)
	canvas.Print(outfile+".pdf")
	del histo


def saveTuplePlot2D(events,inHisto1,inHisto2,nBinsX,minX,maxX,nBinsY,minY,maxY,outfile,canvas,XaxisTitle="",YaxisTitle="",plotTitle="",m=0,mRange=0,stats=0,logY=0):
	events.Draw("{0}:{1}>>histo({2},{3},{4},{5},{6},{7})".format(inHisto2,inHisto1,nBinsX,minX,maxX,nBinsY,minY,maxY),"uncM>{0}-{1}&&uncM<{0}+{1}".format(m,mRange))
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

def getMinX(string):
	arr = string.split(" ")
	if(len(arr) < 2): return -9999
	else: return float(arr[1])

def getMaxX(string):
	arr = string.split(" ")
	if(len(arr) < 3): return -9999
	else: return float(arr[2])

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

mcfile = open(remainder[1],"r")
mcFiles = []

for line in (raw.strip().split() for raw in mcfile):
	mcFiles.append(line[0])
events = TChain("ntuple")
for i in range(len(mcFiles)):
    events.Add(mcFiles[i])

apfile = open(remainder[2],"r")
apfiles = []
apevents = []
masses = []

for line in (raw.strip().split() for raw in apfile):
	apfiles.append(TFile(line[0]))

for i in range(len(apfiles)):
	apevents.append(apfiles[i].Get("ntuple"))
	apevents[i].Draw("triM>>dummy({0},{1},{2})".format(1000,0,1))
	dummy = ROOT.gROOT.FindObject("dummy")
	masses.append(dummy.GetMean())
	del dummy

plots = []
plots.append("uncVZ {0} {1}".format(minVZ,maxVZ))
plots.append("sqrt(uncCovZZ) 0 10")
plots.append("(uncVZ-{0})/sqrt(uncCovZZ) -5 5".format(zTarg))
#plots.append("(uncVZ-triEndZ)/sqrt(uncCovZZ) -5 5")
plots.append("uncTargProjXErr 0 10")
plots.append("uncTargProjYErr 0 10")
plots.append("uncTargProjX/uncTargProjXErr -5 5")
plots.append("uncTargProjY/uncTargProjYErr -5 5")
plots.append("eleTrkZ0Err 0 10")
plots.append("posTrkZ0Err 0 10")
plots.append("eleTrkD0Err 0 10")
plots.append("posTrkD0Err 0 10")
plots.append("eleTrkZ0/eleTrkZ0Err -5 5")
plots.append("posTrkZ0/posTrkZ0Err -5 5")
plots.append("eleTrkD0/eleTrkD0Err -5 5")
plots.append("posTrkD0/posTrkD0Err -5 5")

plots2D = []
plots2D.append("uncM uncVZ 0 0.1 {0} {1}".format(minVZ,maxVZ))
plots2D.append("sqrt(uncCovZZ) uncVZ 0 10 {0} {1}".format(minVZ,maxVZ))
plots2D.append("(uncVZ-{0})/sqrt(uncCovZZ) uncVZ -5 5 {1} {2}".format(zTarg,minVZ,maxVZ))
#plots2D.append("(uncVZ-triEndZ)/sqrt(uncCovZZ) uncVZ -5 5 {0} {1}".format(minVZ,maxVZ))
plots2D.append("uncTargProjXErr uncVZ 0 10 {0} {1}".format(minVZ,maxVZ))
plots2D.append("uncTargProjYErr uncVZ 0 10 {0} {1}".format(minVZ,maxVZ))
plots2D.append("uncTargProjX/uncTargProjXErr uncVZ -5 5 {0} {1}".format(minVZ,maxVZ))
plots2D.append("uncTargProjY/uncTargProjYErr uncVZ -5 5 {0} {1}".format(minVZ,maxVZ))
plots2D.append("eleTrkZ0Err uncVZ 0 10 {0} {1}".format(minVZ,maxVZ))
plots2D.append("posTrkZ0Err uncVZ 0 10 {0} {1}".format(minVZ,maxVZ))
plots2D.append("eleTrkD0Err uncVZ 0 10 {0} {1}".format(minVZ,maxVZ))
plots2D.append("posTrkD0Err uncVZ 0 10 {0} {1}".format(minVZ,maxVZ))
plots2D.append("eleTrkZ0Err/eleTrkZ0Err uncVZ -5 5 {0} {1}".format(minVZ,maxVZ))
plots2D.append("posTrkZ0Err/posTrkZ0Err uncVZ -5 5 {0} {1}".format(minVZ,maxVZ))
plots2D.append("eleTrkD0Err/eleTrkD0Err uncVZ -5 5 {0} {1}".format(minVZ,maxVZ))
plots2D.append("posTrkD0Err/posTrkD0Err uncVZ -5 5 {0} {1}".format(minVZ,maxVZ))

openPDF(outfile,c)

for i in range(len(plots)):
	plot = getPlot(plots[i])
	minX = getMinX(plots[i])
	maxX = getMaxX(plots[i])
	saveTuplePlot(events,plot,nBins,minX,maxX,outfile,c,plot,"",plot)
	for j in range(len(masses)):
		mass = masses[j]
		saveTuplePlot(events,plot,nBins,minX,maxX,outfile,c,plot,"",plot+" MC mass = "+str(mass)+" +/- "+str(massBin)+" GeV",mass,massBin)
		saveTuplePlot(apevents[j],plot,nBins,minX,maxX,outfile,c,plot,"",plot+" A' mass = "+str(mass)+" GeV")

for i in range(len(plots2D)):
	plot1 = getPlot(plots2D[i])
	plot2 = getPlot2D(plots2D[i])
	minX = getMinX2D(plots2D[i])
	maxX = getMaxX2D(plots2D[i])
	minY = getMinY(plots2D[i])
	maxY = getMaxY(plots2D[i])
	saveTuplePlot2D(events,plot1,plot2,nBins,minX,maxX,nBins,minY,maxY,outfile,c,plot1,plot2,plot2+" vs "+plot1)
	for j in range(len(masses)):
		mass = masses[j]
		saveTuplePlot2D(events,plot1,plot2,nBins,minX,maxX,nBins,minY,maxY,outfile,c,plot1,plot2,plot2+" vs "+plot1+" mass = "+str(mass)+" +/- "+str(massBin)+" GeV",mass,massBin)
		saveTuplePlot2D(apevents[j],plot1,plot2,nBins,minX,maxX,nBins,minY,maxY,outfile,c,plot1,plot2,plot2+" vs "+plot1+" A' mass = "+str(mass)+" GeV")

closePDF(outfile,c)