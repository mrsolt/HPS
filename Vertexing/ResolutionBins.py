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

def getMinX(string):
	arr = string.split(" ")
	if(len(arr) < 2): return -9999
	else: return float(arr[1])

def getMaxX(string):
	arr = string.split(" ")
	if(len(arr) < 3): return -9999
	else: return float(arr[2])

def getCut(string):
	arr = string.split(" ")
	if(len(arr) < 4): return ""
	else: return arr[3]

def getPlotX(string):
	arr = string.split(" ")
	return arr[0]

def getPlotY(string):
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

def getCut2D(string):
	arr = string.split(" ")
	if(len(arr) < 7): return ""
	else: return arr[6]

def openPDF(outfile,canvas):
	c.Print(outfile+".pdf[")

def closePDF(outfile,canvas):
	c.Print(outfile+".pdf]")

def saveTuplePlot(events,inHisto,nBinsX,minX,maxX,outfile,canvas,XaxisTitle="",plotTitle="",cut="",stats=0,logY=0):
	events.Draw("{0}>>histo({1},{2},{3})".format(inHisto,nBinsX,minX,maxX),cut)
	histo = ROOT.gROOT.FindObject("histo")
	histo.SetTitle(plotTitle)
	histo.GetXaxis().SetTitle(XaxisTitle)
	histo.SetStats(stats)
	histo.Draw()
	canvas.SetLogy(logY)
	canvas.Print(outfile+".pdf")
	del histo

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

minVZ = -20
maxVZ = 70
maxZerr = 15
res1 = 3
res2 = 6

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'm:n:z:r:s:h')

# Parse the command line arguments
for opt, arg in options:
		if opt=='-m':
			minVZ = float(arg)
		if opt=='-n':
			maxVZ = float(arg)
		if opt=='-z':
			maxZerr = float(arg)
		if opt=='-r':
			res1 = float(arg)
		if opt=='-s':
			res2 = float(arg)
		if opt=='-h':
			print_usage()
			sys.exit(0)

gStyle.SetOptStat(110011)
c = TCanvas("c","c",800,600)

outfile = remainder[0]
events = TChain("ntuple")
for i in range(1,len(remainder)):
    events.Add(remainder[i])

nBins = 100
minX = ""
maxX = ""
minY = ""
maxY = ""

highres = "sqrt(uncCovZZ)<{0}".format(res1)
medres = "sqrt(uncCovZZ)>{0}&&sqrt(uncCovZZ)<{1}".format(res1,res2)
lowres = "sqrt(uncCovZZ)>{0}".format(res2)

plots = []

plots.append("sqrt(uncCovZZ) 0 {0}".format(maxZerr))
plots.append("sqrt(uncCovZZ) 0 {0} {1}".format(maxZerr,highres))
plots.append("sqrt(uncCovZZ) 0 {0} {1}".format(maxZerr,medres))
plots.append("sqrt(uncCovZZ) 0 {0} {1}".format(maxZerr,lowres))

plots2D = []

plots2D.append("uncM uncVZ 0 0.1 {0} {1}".format(minVZ,maxVZ))
plots2D.append("uncM uncVZ 0 0.1 {0} {1} {2}".format(minVZ,maxVZ,highres))
plots2D.append("uncM uncVZ 0 0.1 {0} {1} {2}".format(minVZ,maxVZ,medres))
plots2D.append("uncM uncVZ 0 0.1 {0} {1} {2}".format(minVZ,maxVZ,lowres))

openPDF(outfile,c)

for j in range(0,len(plots)):
	x = getPlotX(plots[j])
	minX = getMinX(plots[j])
	maxX = getMaxX(plots[j])
	cut = getCut(plots[j])
	saveTuplePlot(events,x,nBins,minX,maxX,outfile,c,x,x+" "+cut,cut)

for j in range(0,len(plots2D)):
	x = getPlotX(plots2D[j])
	y = getPlotY(plots2D[j])
	minX = getMinX2D(plots2D[j])
	maxX = getMaxX2D(plots2D[j])
	minY = getMinY(plots2D[j])
	maxY = getMaxY(plots2D[j])
	cut = getCut2D(plots2D[j])
	saveTuplePlot2D(events,x,y,nBins,minX,maxX,nBins,minY,maxY,outfile,c,x,y,y+" vs "+x+" "+cut,cut,1)

closePDF(outfile,c)