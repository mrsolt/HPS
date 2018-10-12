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
	del histo

minVZ = -20
maxVZ = 70

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

nBins = 100
minX = ""
maxX = ""
minY = ""
maxY = ""

isoEle = "eleMinPositiveIso+0.5*(eleTrkZ0+0.5*elePY/eleP)*sign(elePY)"
isoPos = "posMinPositiveIso+0.5*(posTrkZ0+0.5*posPY/posP)*sign(posPY)"

minx = -30
maxx = -minx
miny = -10
maxy = -miny

plots = []

plots.append("uncM uncVZ 0 0.1 {0} {1}".format(minVZ,maxVZ))
plots.append("uncM uncVZ 0 0.1 {0} {1} elePurity<0.99||posPurity<0.99".format(minVZ,maxVZ))
plots.append("uncM uncVZ 0 0.1 {0} {1} (elePurity<0.99||posPurity<0.99)&&(min({2},{3})>0)".format(minVZ,maxVZ,isoEle,isoPos))

plots.append("uncM uncVZ 0 0.1 {0} {1} eleL1tIsGoodTruthHit>-9998&&eleL1tIsGoodTruthHit<1".format(minVZ,maxVZ))
plots.append("eleL1tsvthitX eleL1tsvthitY {0} {1} {2} {3} eleL1tIsGoodTruthHit>-9998&&eleL1tIsGoodTruthHit<1".format(minx,maxx,miny,maxy))
plots.append("eleL1tInsvthitX eleL1tInsvthitY {0} {1} {2} {3} eleL1tIsGoodTruthHit>-9998&&eleL1tIsGoodTruthHit<1".format(minx,maxx,miny,maxy))
plots.append("{2} uncVZ -5 20 {0} {1} eleL1tIsGoodTruthHit>-9998&&eleL1tIsGoodTruthHit<1".format(minVZ,maxVZ,isoEle))
plots.append("uncM uncVZ 0 0.1 {0} {1} eleL1tIsGoodTruthHit>-9998&&eleL1tIsGoodTruthHit<1&&{2}>0".format(minVZ,maxVZ,isoEle))
plots.append("eleL1tsvthitX eleL1tsvthitY {0} {1} {2} {3} eleL1tIsGoodTruthHit>-9998&&eleL1tIsGoodTruthHit<1&&{4}>0".format(minx,maxx,miny,maxy,isoEle))
plots.append("eleL1tInsvthitX eleL1tInsvthitY {0} {1} {2} {3} eleL1tIsGoodTruthHit>-9998&&eleL1tIsGoodTruthHit<1&&{4}>0".format(minx,maxx,miny,maxy,isoEle))

plots.append("uncM uncVZ 0 0.1 {0} {1} eleL2tIsGoodTruthHit>-9998&&eleL2tIsGoodTruthHit<1".format(minVZ,maxVZ))
plots.append("eleL2tsvthitX eleL2tsvthitY {0} {1} {2} {3} eleL2tIsGoodTruthHit>-9998&&eleL2tIsGoodTruthHit<1".format(minx,maxx,miny,maxy))
plots.append("eleL2tInsvthitX eleL2tInsvthitY {0} {1} {2} {3} eleL2tIsGoodTruthHit>-9998&&eleL2tIsGoodTruthHit<1".format(minx,maxx,miny,maxy))
plots.append("{2} uncVZ -5 20 {0} {1} eleL2tIsGoodTruthHit>-9998&&eleL2tIsGoodTruthHit<1".format(minVZ,maxVZ,isoEle))
plots.append("uncM uncVZ 0 0.1 {0} {1} eleL2tIsGoodTruthHit>-9998&&eleL2tIsGoodTruthHit<1&&{2}>0".format(minVZ,maxVZ,isoEle))
plots.append("eleL2tsvthitX eleL2tsvthitY {0} {1} {2} {3} eleL2tIsGoodTruthHit>-9998&&eleL2tIsGoodTruthHit<1&&{4}>0".format(minx,maxx,miny,maxy,isoEle))
plots.append("eleL2tInsvthitX eleL2tInsvthitY {0} {1} {2} {3} eleL2tIsGoodTruthHit>-9998&&eleL2tIsGoodTruthHit<1&&{4}>0".format(minx,maxx,miny,maxy,isoEle))

plots.append("uncM uncVZ 0 0.1 {0} {1} eleL1bIsGoodTruthHit>-9998&&eleL1bIsGoodTruthHit<1".format(minVZ,maxVZ))
plots.append("eleL1bsvthitX eleL1bsvthitY {0} {1} {2} {3} eleL1bIsGoodTruthHit>-9998&&eleL1bIsGoodTruthHit<1".format(minx,maxx,miny,maxy))
plots.append("eleL1bInsvthitX eleL1bInsvthitY {0} {1} {2} {3} eleL1bIsGoodTruthHit>-9998&&eleL1bIsGoodTruthHit<1".format(minx,maxx,miny,maxy))
plots.append("{2} uncVZ -5 20 {0} {1} eleL1bIsGoodTruthHit>-9998&&eleL1bIsGoodTruthHit<1".format(minVZ,maxVZ,isoEle))
plots.append("uncM uncVZ 0 0.1 {0} {1} eleL1bIsGoodTruthHit>-9998&&eleL1bIsGoodTruthHit<1&&{2}>0".format(minVZ,maxVZ,isoEle))
plots.append("eleL1bsvthitX eleL1bsvthitY {0} {1} {2} {3} eleL1bIsGoodTruthHit>-9998&&eleL1bIsGoodTruthHit<1&&{4}>0".format(minx,maxx,miny,maxy,isoEle))
plots.append("eleL1bInsvthitX eleL1bInsvthitY {0} {1} {2} {3} eleL1bIsGoodTruthHit>-9998&&eleL1bIsGoodTruthHit<1&&{4}>0".format(minx,maxx,miny,maxy,isoEle))

plots.append("uncM uncVZ 0 0.1 {0} {1} eleL2bIsGoodTruthHit>-9998&&eleL2bIsGoodTruthHit<1".format(minVZ,maxVZ))
plots.append("eleL2bsvthitX eleL2bsvthitY {0} {1} {2} {3} eleL2bIsGoodTruthHit>-9998&&eleL2bIsGoodTruthHit<1".format(minx,maxx,miny,maxy))
plots.append("eleL2bInsvthitX eleL2bInsvthitY {0} {1} {2} {3} eleL2bIsGoodTruthHit>-9998&&eleL2bIsGoodTruthHit<1".format(minx,maxx,miny,maxy))
plots.append("{2} uncVZ -5 20 {0} {1} eleL2bIsGoodTruthHit>-9998&&eleL2bIsGoodTruthHit<1".format(minVZ,maxVZ,isoEle))
plots.append("uncM uncVZ 0 0.1 {0} {1} eleL2bIsGoodTruthHit>-9998&&eleL2bIsGoodTruthHit<1&&{2}>0".format(minVZ,maxVZ,isoEle))
plots.append("eleL2bsvthitX eleL2bsvthitY {0} {1} {2} {3} eleL2bIsGoodTruthHit>-9998&&eleL2bIsGoodTruthHit<1&&{4}>0".format(minx,maxx,miny,maxy,isoEle))
plots.append("eleL2bInsvthitX eleL2bInsvthitY {0} {1} {2} {3} eleL2bIsGoodTruthHit>-9998&&eleL2bIsGoodTruthHit<1&&{4}>0".format(minx,maxx,miny,maxy,isoEle))


plots.append("uncM uncVZ 0 0.1 {0} {1} posL1tIsGoodTruthHit>-9998&&posL1tIsGoodTruthHit<1".format(minVZ,maxVZ))
plots.append("posL1tsvthitX posL1tsvthitY {0} {1} {2} {3} posL1tIsGoodTruthHit>-9998&&posL1tIsGoodTruthHit<1".format(minx,maxx,miny,maxy))
plots.append("posL1tInsvthitX posL1tInsvthitY {0} {1} {2} {3} posL1tIsGoodTruthHit>-9998&&posL1tIsGoodTruthHit<1".format(minx,maxx,miny,maxy))
plots.append("{2} uncVZ -5 20 {0} {1} posL1tIsGoodTruthHit>-9998&&posL1tIsGoodTruthHit<1".format(minVZ,maxVZ,isoPos))
plots.append("uncM uncVZ 0 0.1 {0} {1} posL1tIsGoodTruthHit>-9998&&posL1tIsGoodTruthHit<1&&{2}>0".format(minVZ,maxVZ,isoPos))
plots.append("posL1tsvthitX posL1tsvthitY {0} {1} {2} {3} posL1tIsGoodTruthHit>-9998&&posL1tIsGoodTruthHit<1&&{4}>0".format(minx,maxx,miny,maxy,isoPos))
plots.append("posL1tInsvthitX posL1tInsvthitY {0} {1} {2} {3} posL1tIsGoodTruthHit>-9998&&posL1tIsGoodTruthHit<1&&{4}>0".format(minx,maxx,miny,maxy,isoPos))

plots.append("uncM uncVZ 0 0.1 {0} {1} posL2tIsGoodTruthHit>-9998&&posL2tIsGoodTruthHit<1".format(minVZ,maxVZ))
plots.append("posL2tsvthitX posL2tsvthitY {0} {1} {2} {3} posL2tIsGoodTruthHit>-9998&&posL2tIsGoodTruthHit<1".format(minx,maxx,miny,maxy))
plots.append("posL2tInsvthitX posL2tInsvthitY {0} {1} {2} {3} posL2tIsGoodTruthHit>-9998&&posL2tIsGoodTruthHit<1".format(minx,maxx,miny,maxy))
plots.append("{2} uncVZ -5 20 {0} {1} posL2tIsGoodTruthHit>-9998&&posL2tIsGoodTruthHit<1".format(minVZ,maxVZ,isoPos))
plots.append("uncM uncVZ 0 0.1 {0} {1} posL2tIsGoodTruthHit>-9998&&posL2tIsGoodTruthHit<1&&{2}>0".format(minVZ,maxVZ,isoPos))
plots.append("posL2tsvthitX posL2tsvthitY {0} {1} {2} {3} posL2tIsGoodTruthHit>-9998&&posL2tIsGoodTruthHit<1&&{4}>0".format(minx,maxx,miny,maxy,isoPos))
plots.append("posL2tInsvthitX posL2tInsvthitY {0} {1} {2} {3} posL2tIsGoodTruthHit>-9998&&posL2tIsGoodTruthHit<1&&{4}>0".format(minx,maxx,miny,maxy,isoPos))

plots.append("uncM uncVZ 0 0.1 {0} {1} posL1bIsGoodTruthHit>-9998&&posL1bIsGoodTruthHit<1".format(minVZ,maxVZ))
plots.append("posL1bsvthitX posL1bsvthitY {0} {1} {2} {3} posL1bIsGoodTruthHit>-9998&&posL1bIsGoodTruthHit<1".format(minx,maxx,miny,maxy))
plots.append("posL1bInsvthitX posL1bInsvthitY {0} {1} {2} {3} posL1bIsGoodTruthHit>-9998&&posL1bIsGoodTruthHit<1".format(minx,maxx,miny,maxy))
plots.append("{2} uncVZ -5 20 {0} {1} posL1bIsGoodTruthHit>-9998&&posL1bIsGoodTruthHit<1".format(minVZ,maxVZ,isoPos))
plots.append("uncM uncVZ 0 0.1 {0} {1} posL1bIsGoodTruthHit>-9998&&posL1bIsGoodTruthHit<1&&{2}>0".format(minVZ,maxVZ,isoPos))
plots.append("posL1bsvthitX posL1bsvthitY {0} {1} {2} {3} posL1bIsGoodTruthHit>-9998&&posL1bIsGoodTruthHit<1&&{4}>0".format(minx,maxx,miny,maxy,isoPos))
plots.append("posL1bInsvthitX posL1bInsvthitY {0} {1} {2} {3} posL1bIsGoodTruthHit>-9998&&posL1bIsGoodTruthHit<1&&{4}>0".format(minx,maxx,miny,maxy,isoPos))

plots.append("uncM uncVZ 0 0.1 {0} {1} posL2bIsGoodTruthHit>-9998&&posL2bIsGoodTruthHit<1".format(minVZ,maxVZ))
plots.append("posL2bsvthitX posL2bsvthitY {0} {1} {2} {3} posL2bIsGoodTruthHit>-9998&&posL2bIsGoodTruthHit<1".format(minx,maxx,miny,maxy))
plots.append("posL2bInsvthitX posL2bInsvthitY {0} {1} {2} {3} posL2bIsGoodTruthHit>-9998&&posL2bIsGoodTruthHit<1".format(minx,maxx,miny,maxy))
plots.append("{2} uncVZ -5 20 {0} {1} posL2bIsGoodTruthHit>-9998&&posL2bIsGoodTruthHit<1".format(minVZ,maxVZ,isoPos))
plots.append("uncM uncVZ 0 0.1 {0} {1} posL2bIsGoodTruthHit>-9998&&posL2bIsGoodTruthHit<1&&{2}>0".format(minVZ,maxVZ,isoPos))
plots.append("posL2bsvthitX posL2bsvthitY {0} {1} {2} {3} posL2bIsGoodTruthHit>-9998&&posL2bIsGoodTruthHit<1&&{4}>0".format(minx,maxx,miny,maxy,isoPos))
plots.append("posL2bInsvthitX posL2bInsvthitY {0} {1} {2} {3} posL2bIsGoodTruthHit>-9998&&posL2bIsGoodTruthHit<1&&{4}>0".format(minx,maxx,miny,maxy,isoPos))

#rootfile = TFile(outfile+".root","recreate")

openPDF(outfile,c)

for j in range(0,len(plots)):
	x = getPlotX(plots[j])
	y = getPlotY(plots[j])
	minX = getMinX(plots[j])
	maxX = getMaxX(plots[j])
	minY = getMinY(plots[j])
	maxY = getMaxY(plots[j])
	cut = getCut(plots[j])
	saveTuplePlot2D(events,x,y,nBins,minX,maxX,nBins,minY,maxY,outfile,c,x,y,y+" vs "+x+" "+cut,cut,1)

closePDF(outfile,c)
#rootfile.Close()