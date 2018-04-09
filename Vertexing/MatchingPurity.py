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
    print '\t-m: minimum uncVZ'
    print '\t-n: maximum uncVZ'
    print '\t-h: this help message'
    print

def getPlotX(string):
	arr = string.split(" ")
	return arr[0]

def getPlotY(string):
	arr = string.split(" ")
	if(len(arr) < 2): return ""
	else: return arr[1]

def getMinX(string):
	arr = string.split(" ")
	if(len(arr) < 3): return -9999
	else: return float(arr[2])

def getMaxX(string):
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

def getCut(string):
	arr = string.split(" ")
	if(len(arr) < 7): return ""
	else: return arr[6]

def getScatter(actsensor,inactsensor):
	scatter = actsensor
	if(scatter < -9998):
		scatter = inactsensor
	return scatter

def openPDF(outfile,canvas):
	c.Print(outfile+".pdf[")

def closePDF(outfile,canvas):
	c.Print(outfile+".pdf]")

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
	histo.Write(plotTitle)
	del histo

def savehisto2D(histo,outfile,canvas,XaxisTitle="",YaxisTitle="",plotTitle="",stats=0,logY=0):
	histo.SetTitle(plotTitle)
	histo.GetXaxis().SetTitle(XaxisTitle)
	histo.GetYaxis().SetTitle(YaxisTitle)
	histo.SetStats(stats)
	histo.Draw("COLZ")
	canvas.SetLogy(logY)
	canvas.Print(outfile+".pdf")
	histo.Write(plotTitle)
	del histo

minVZ = -20
maxVZ = 120

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'm:n:h')

# Parse the command line arguments
for opt, arg in options:
		if opt=='-m':
			minVZ = float(arg)
		if opt=='-n':
			maxVZ = float(arg)
		if opt=='-h':
			print_usage()
			sys.exit(0)

gStyle.SetOptStat(110011)
c = TCanvas("c","c",800,600)

outfile = remainder[0]
events = TChain("ntuple")
for i in range(1,len(remainder)):
    events.Add(remainder[i])

nBins = 50
minX = ""
maxX = ""
minY = ""
maxY = ""

plots = []
plots.append("uncM uncVZ 0 0.1 {0} {1}".format(minVZ,maxVZ))
plots.append("elePurity uncVZ 0 1.1 {0} {1}".format(minVZ,maxVZ))
plots.append("posPurity uncVZ 0 1.1 {0} {1}".format(minVZ,maxVZ))
plots.append("elePurity eleTrkChisq 0 1.1 0 30")
plots.append("posPurity posTrkChisq 0 1.1 0 30")
plots.append("eleTrkChisq uncVZ 0 5 {0} {1}".format(minVZ,maxVZ))
plots.append("posTrkChisq uncVZ 0 5 {0} {1}".format(minVZ,maxVZ))
plots.append("elePurity eleTrkD0 0 1.1 -10 10")
plots.append("posPurity posTrkD0 0 1.1 -10 10")
plots.append("eleTrkD0 uncVZ -10 10 {0} {1}".format(minVZ,maxVZ))
plots.append("posTrkD0 uncVZ -10 10 {0} {1}".format(minVZ,maxVZ))
plots.append("elePurity eleTrkZ0 0 1.1 -10 10")
plots.append("posPurity posTrkZ0 0 1.1 -10 10")
plots.append("eleTrkZ0 uncVZ -10 10 {0} {1}".format(minVZ,maxVZ))
plots.append("posTrkZ0 uncVZ -10 10 {0} {1}".format(minVZ,maxVZ))
plots.append("elePurity bscChisq 0 1.1 0 10")
plots.append("posPurity bscChisq 0 1.1 0 10")
plots.append("bscChisq uncVZ 0 10 {0} {1}".format(minVZ,maxVZ))
plots.append("elePurity eleP 0 1.1 0 1.5")
plots.append("posPurity posP 0 1.1 0 1.5")
plots.append("eleP uncVZ 0 1.5 {0} {1}".format(minVZ,maxVZ))
plots.append("posP uncVZ 0 1.5 {0} {1}".format(minVZ,maxVZ))

cuts = []
cuts.append("max(eleTrkChisq,posTrkChisq)<5")

cuts.append("max(eleTrkChisq,posTrkChisq)<5&&elePurity>0.99&&posPurity>0.99")
cuts.append("max(eleTrkChisq,posTrkChisq)<5&&elePurity<0.99&&posPurity>0.99")
cuts.append("max(eleTrkChisq,posTrkChisq)<5&&elePurity>0.99&&posPurity<0.99")
cuts.append("max(eleTrkChisq,posTrkChisq)<5&&elePurity<0.99&&posPurity<0.99")

rootfile = TFile(outfile+".root","recreate")

openPDF(outfile,c)

for i in range(0,len(cuts)):
	cut = cuts[i]
	for j in range(0,len(plots)):
		x = getPlotX(plots[j])
		y = getPlotY(plots[j])
		minX = getMinX(plots[j])
		maxX = getMaxX(plots[j])
		minY = getMinY(plots[j])
		maxY = getMaxY(plots[j])
		finalcut = cut + "&&" + getCut(plots[j])
		if getCut(plots[j]) == "":
			finalcut = cut
		if cut == "":
			finalcut = getCut(plots[j])
		saveTuplePlot2D(events,x,y,nBins,minX,maxX,nBins,minY,maxY,outfile,c,x,y,y+" vs "+x+" "+cut,finalcut,1)

closePDF(outfile,c)
rootfile.Close()