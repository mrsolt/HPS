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
    print '\t-l: is L1L2 (default false)'
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

L1L2 = False
minVZ = -20
maxVZ = 120

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'm:n:hl')

# Parse the command line arguments
for opt, arg in options:
		if opt=='-l':
			L1L2 = True
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
maxTheta = 0.05
minTheta = -maxTheta

plots = []
plots.append("uncM uncVZ 0 0.1 {0} {1}".format(minVZ,maxVZ))
plots.append("eleMinPositiveIsoL2 uncVZ 0 10 {0} {1}".format(minVZ,maxVZ))
plots.append("posMinPositiveIsoL2 uncVZ 0 10 {0} {1}".format(minVZ,maxVZ))
plots.append("uncVZ -eleL1tthetaY {0} {1} {2} {3}".format(minVZ,maxVZ,minTheta,maxTheta))
plots.append("uncVZ -eleL2tthetaY {0} {1} {2} {3}".format(minVZ,maxVZ,minTheta,maxTheta))
plots.append("uncVZ -eleL3tthetaY {0} {1} {2} {3}".format(minVZ,maxVZ,minTheta,maxTheta))
plots.append("uncVZ -eleL4tthetaY {0} {1} {2} {3}".format(minVZ,maxVZ,minTheta,maxTheta))
plots.append("uncVZ eleL1bthetaY {0} {1} {2} {3}".format(minVZ,maxVZ,minTheta,maxTheta))
plots.append("uncVZ eleL2bthetaY {0} {1} {2} {3}".format(minVZ,maxVZ,minTheta,maxTheta))
plots.append("uncVZ eleL3bthetaY {0} {1} {2} {3}".format(minVZ,maxVZ,minTheta,maxTheta))
plots.append("uncVZ eleL4bthetaY {0} {1} {2} {3}".format(minVZ,maxVZ,minTheta,maxTheta))
plots.append("uncVZ -posL1tthetaY {0} {1} {2} {3}".format(minVZ,maxVZ,minTheta,maxTheta))
plots.append("uncVZ -posL2tthetaY {0} {1} {2} {3}".format(minVZ,maxVZ,minTheta,maxTheta))
plots.append("uncVZ -posL3tthetaY {0} {1} {2} {3}".format(minVZ,maxVZ,minTheta,maxTheta))
plots.append("uncVZ -posL4tthetaY {0} {1} {2} {3}".format(minVZ,maxVZ,minTheta,maxTheta))
plots.append("uncVZ posL1bthetaY {0} {1} {2} {3}".format(minVZ,maxVZ,minTheta,maxTheta))
plots.append("uncVZ posL2bthetaY {0} {1} {2} {3}".format(minVZ,maxVZ,minTheta,maxTheta))
plots.append("uncVZ posL3bthetaY {0} {1} {2} {3}".format(minVZ,maxVZ,minTheta,maxTheta))
plots.append("uncVZ posL4bthetaY {0} {1} {2} {3}".format(minVZ,maxVZ,minTheta,maxTheta))

#plots.append("uncVZ -eleL1tInthetaY {0} {1} {2} {3}".format(minVZ,maxVZ,minTheta,maxTheta))
#plots.append("uncVZ -eleL2tInthetaY {0} {1} {2} {3}".format(minVZ,maxVZ,minTheta,maxTheta))
#plots.append("uncVZ -eleL3tInthetaY {0} {1} {2} {3}".format(minVZ,maxVZ,minTheta,maxTheta))
#plots.append("uncVZ -eleL4tInthetaY {0} {1} {2} {3}".format(minVZ,maxVZ,minTheta,maxTheta))
#plots.append("uncVZ eleL1bInthetaY {0} {1} {2} {3}".format(minVZ,maxVZ,minTheta,maxTheta))
#plots.append("uncVZ eleL2bInthetaY {0} {1} {2} {3}".format(minVZ,maxVZ,minTheta,maxTheta))
#plots.append("uncVZ eleL3bInthetaY {0} {1} {2} {3}".format(minVZ,maxVZ,minTheta,maxTheta))
#plots.append("uncVZ eleL4bInthetaY {0} {1} {2} {3}".format(minVZ,maxVZ,minTheta,maxTheta))
#plots.append("uncVZ -posL1tInthetaY {0} {1} {2} {3}".format(minVZ,maxVZ,minTheta,maxTheta))
#plots.append("uncVZ -posL2tInthetaY {0} {1} {2} {3}".format(minVZ,maxVZ,minTheta,maxTheta))
#plots.append("uncVZ -posL3tInthetaY {0} {1} {2} {3}".format(minVZ,maxVZ,minTheta,maxTheta))
#plots.append("uncVZ -posL4tInthetaY {0} {1} {2} {3}".format(minVZ,maxVZ,minTheta,maxTheta))
#plots.append("uncVZ posL1bInthetaY {0} {1} {2} {3}".format(minVZ,maxVZ,minTheta,maxTheta))
#plots.append("uncVZ posL2bInthetaY {0} {1} {2} {3}".format(minVZ,maxVZ,minTheta,maxTheta))
#plots.append("uncVZ posL3bInthetaY {0} {1} {2} {3}".format(minVZ,maxVZ,minTheta,maxTheta))
#plots.append("uncVZ posL4bInthetaY {0} {1} {2} {3}".format(minVZ,maxVZ,minTheta,maxTheta))

#plots.append("uncVZ -(eleL1tthetaY+eleL2tthetaY) {0} {1} {2} {3}".format(minVZ,maxVZ,minTheta,maxTheta))
#plots.append("uncVZ (eleL1bthetaY+eleL2bthetaY) {0} {1} {2} {3}".format(minVZ,maxVZ,minTheta,maxTheta))
#plots.append("uncVZ -(eleL1tInthetaY+eleL2tthetaY) {0} {1} {2} {3}".format(minVZ,maxVZ,minTheta,maxTheta))
#plots.append("uncVZ (eleL1bInthetaY+eleL2bthetaY) {0} {1} {2} {3}".format(minVZ,maxVZ,minTheta,maxTheta))
#plots.append("uncVZ -(eleL1tInthetaY+eleL2tInthetaY) {0} {1} {2} {3}".format(minVZ,maxVZ,minTheta,maxTheta))
#plots.append("uncVZ (eleL1bInthetaY+eleL2bInthetaY) {0} {1} {2} {3}".format(minVZ,maxVZ,minTheta,maxTheta))
#plots.append("uncVZ -(posL1tthetaY+posL2tthetaY) {0} {1} {2} {3}".format(minVZ,maxVZ,minTheta,maxTheta))
#plots.append("uncVZ (posL1bthetaY+posL2bthetaY) {0} {1} {2} {3}".format(minVZ,maxVZ,minTheta,maxTheta))
#plots.append("uncVZ -(posL1tInthetaY+posL2tthetaY) {0} {1} {2} {3}".format(minVZ,maxVZ,minTheta,maxTheta))
#plots.append("uncVZ (posL1bInthetaY+posL2bthetaY) {0} {1} {2} {3}".format(minVZ,maxVZ,minTheta,maxTheta))
#plots.append("uncVZ -(posL1tInthetaY+posL2tInthetaY) {0} {1} {2} {3}".format(minVZ,maxVZ,minTheta,maxTheta))
#plots.append("uncVZ (posL1bInthetaY+posL2bInthetaY) {0} {1} {2} {3}".format(minVZ,maxVZ,minTheta,maxTheta))

#plots.append("uncVZ -(eleL1tthetaY+eleL2tthetaY)+(posL1bthetaY+posL2bthetaY) {0} {1} {2} {3} eleL1tthetaY>-9998&&eleL2tthetaY>-9998&&posL1bthetaY>-9998&&posL2bthetaY>-9998".format(minVZ,maxVZ,minTheta,maxTheta))
#plots.append("uncVZ (eleL1bthetaY+eleL2bthetaY)-(posL1tthetaY+posL2tthetaY) {0} {1} {2} {3} eleL1bthetaY>-9998&&eleL2bthetaY>-9998&&posL1tthetaY>-9998&&posL2tthetaY>-9998".format(minVZ,maxVZ,minTheta,maxTheta))

#plots.append("uncVZ -(eleL1tInthetaY+eleL2tthetaY)+(posL1bthetaY+posL2bthetaY) {0} {1} {2} {3} eleL1tInthetaY>-9998&&eleL2tthetaY>-9998&&posL1bthetaY>-9998&&posL2bthetaY>-9998".format(minVZ,maxVZ,minTheta,maxTheta))
#plots.append("uncVZ (eleL1bInthetaY+eleL2bthetaY)-(posL1tthetaY+posL2tthetaY) {0} {1} {2} {3} eleL1bInthetaY>-9998&&eleL2bthetaY>-9998&&posL1tthetaY>-9998&&posL2tthetaY>-9998".format(minVZ,maxVZ,minTheta,maxTheta))

#plots.append("uncVZ -(eleL1tthetaY+eleL2tthetaY)+(posL1bInthetaY+posL2bthetaY) {0} {1} {2} {3} eleL1tthetaY>-9998&&eleL2tthetaY>-9998&&posL1bInthetaY>-9998&&posL2bthetaY>-9998".format(minVZ,maxVZ,minTheta,maxTheta))
#plots.append("uncVZ (eleL1bthetaY+eleL2bthetaY)-(posL1tInthetaY+posL2tthetaY) {0} {1} {2} {3} eleL1bthetaY>-9998&&eleL2bthetaY>-9998&&posL1tInthetaY>-9998&&posL2tthetaY>-9998".format(minVZ,maxVZ,minTheta,maxTheta))

#plots.append("uncVZ -(eleL1tthetaY+eleL2tInthetaY)+(posL1bthetaY+posL2bthetaY) {0} {1} {2} {3} eleL1tthetaY>-9998&&eleL2tInthetaY>-9998&&posL1bthetaY>-9998&&posL2bthetaY>-9998".format(minVZ,maxVZ,minTheta,maxTheta))
#plots.append("uncVZ (eleL1bthetaY+eleL2bInthetaY)-(posL1tthetaY+posL2tthetaY) {0} {1} {2} {3} eleL1bthetaY>-9998&&eleL2bInthetaY>-9998&&posL1tthetaY>-9998&&posL2tthetaY>-9998".format(minVZ,maxVZ,minTheta,maxTheta))

#plots.append("uncVZ -(eleL1tthetaY+eleL2tthetaY)+(posL1bthetaY+posL2bInthetaY) {0} {1} {2} {3} eleL1tthetaY>-9998&&eleL2tthetaY>-9998&&posL1bthetaY>-9998&&posL2bInthetaY>-9998".format(minVZ,maxVZ,minTheta,maxTheta))
#plots.append("uncVZ (eleL1bthetaY+eleL2bthetaY)-(posL1tthetaY+posL2tInthetaY) {0} {1} {2} {3} eleL1bthetaY>-9998&&eleL2bthetaY>-9998&&posL1tthetaY>-9998&&posL2tInthetaY>-9998".format(minVZ,maxVZ,minTheta,maxTheta))

#plots.append("uncVZ -(eleL1tInthetaY+eleL2tInthetaY)+(posL1bthetaY+posL2bthetaY) {0} {1} {2} {3} eleL1tInthetaY>-9998&&eleL2tInthetaY>-9998&&posL1bthetaY>-9998&&posL2bthetaY>-9998".format(minVZ,maxVZ,minTheta,maxTheta))
#plots.append("uncVZ (eleL1bInthetaY+eleL2bInthetaY)-(posL1tthetaY+posL2tthetaY) {0} {1} {2} {3} eleL1bInthetaY>-9998&&eleL2bInthetaY>-9998&&posL1tthetaY>-9998&&posL2tthetaY>-9998".format(minVZ,maxVZ,minTheta,maxTheta))

#plots.append("uncVZ -(eleL1tthetaY+eleL2tthetaY)+(posL1bInthetaY+posL2bInthetaY) {0} {1} {2} {3} eleL1tthetaY>-9998&&eleL2tthetaY>-9998&&posL1bInthetaY>-9998&&posL2bInthetaY>-9998".format(minVZ,maxVZ,minTheta,maxTheta))
#plots.append("uncVZ (eleL1bthetaY+eleL2bthetaY)-(posL1tInthetaY+posL2tInthetaY) {0} {1} {2} {3} eleL1bthetaY>-9998&&eleL2bthetaY>-9998&&posL1tInthetaY>-9998&&posL2tInthetaY>-9998".format(minVZ,maxVZ,minTheta,maxTheta))

#plots.append("uncVZ -(eleL1tInthetaY+eleL2tInthetaY)+(posL1bInthetaY+posL2bthetaY) {0} {1} {2} {3} eleL1tInthetaY>-9998&&eleL2tInthetaY>-9998&&posL1bInthetaY>-9998&&posL2bthetaY>-9998".format(minVZ,maxVZ,minTheta,maxTheta))
#plots.append("uncVZ (eleL1bInthetaY+eleL2bInthetaY)-(posL1tInthetaY+posL2tthetaY) {0} {1} {2} {3} eleL1bInthetaY>-9998&&eleL2bInthetaY>-9998&&posL1tInthetaY>-9998&&posL2tthetaY>-9998".format(minVZ,maxVZ,minTheta,maxTheta))

#plots.append("uncVZ -(eleL1tInthetaY+eleL2tInthetaY)+(posL1bthetaY+posL2bInthetaY) {0} {1} {2} {3} eleL1tInthetaY>-9998&&eleL2tInthetaY>-9998&&posL1bthetaY>-9998&&posL2bInthetaY>-9998".format(minVZ,maxVZ,minTheta,maxTheta))
#plots.append("uncVZ (eleL1bInthetaY+eleL2bInthetaY)-(posL1tthetaY+posL2tInthetaY) {0} {1} {2} {3} eleL1bInthetaY>-9998&&eleL2bInthetaY>-9998&&posL1tthetaY>-9998&&posL2tInthetaY>-9998".format(minVZ,maxVZ,minTheta,maxTheta))

#plots.append("uncVZ -(eleL1tInthetaY+eleL2tthetaY)+(posL1bInthetaY+posL2bInthetaY) {0} {1} {2} {3} eleL1tInthetaY>-9998&&eleL2tthetaY>-9998&&posL1bInthetaY>-9998&&posL2bInthetaY>-9998".format(minVZ,maxVZ,minTheta,maxTheta))
#plots.append("uncVZ (eleL1bInthetaY+eleL2bthetaY)-(posL1tInthetaY+posL2tInthetaY) {0} {1} {2} {3} eleL1bInthetaY>-9998&&eleL2bthetaY>-9998&&posL1tInthetaY>-9998&&posL2tInthetaY>-9998".format(minVZ,maxVZ,minTheta,maxTheta))

#plots.append("uncVZ -(eleL1tthetaY+eleL2tInthetaY)+(posL1bInthetaY+posL2bInthetaY) {0} {1} {2} {3} eleL1tthetaY>-9998&&eleL2tInthetaY>-9998&&posL1bInthetaY>-9998&&posL2bInthetaY>-9998".format(minVZ,maxVZ,minTheta,maxTheta))
#plots.append("uncVZ (eleL1bthetaY+eleL2bInthetaY)-(posL1tInthetaY+posL2tInthetaY) {0} {1} {2} {3} eleL1bthetaY>-9998&&eleL2bInthetaY>-9998&&posL1tInthetaY>-9998&&posL2tInthetaY>-9998".format(minVZ,maxVZ,minTheta,maxTheta))

#plots.append("uncVZ -(eleL1tInthetaY+eleL2tInthetaY)+(posL1bInthetaY+posL2bInthetaY) {0} {1} {2} {3} eleL1tInthetaY>-9998&&eleL2tInthetaY>-9998&&posL1bInthetaY>-9998&&posL2bInthetaY>-9998".format(minVZ,maxVZ,minTheta,maxTheta))
#plots.append("uncVZ (eleL1bInthetaY+eleL2bInthetaY)-(posL1tInthetaY+posL2tInthetaY) {0} {1} {2} {3} eleL1bInthetaY>-9998&&eleL2bInthetaY>-9998&&posL1tInthetaY>-9998&&posL2tInthetaY>-9998".format(minVZ,maxVZ,minTheta,maxTheta))


#plots.append("uncVZ -(eleL1tthetaY+eleL2tthetaY+eleL3tthetaY+eleL4tthetaY)+(posL1bthetaY+posL2bthetaY+posL3bthetaY+posL4bthetaY) {0} {1} {2} {3} eleL1tthetaY>-9998&&eleL2tthetaY>-9998&&eleL3tthetaY>-9998&&eleL4tthetaY>-9998&&posL1bthetaY>-9998&&posL2bthetaY>-9998&&posL3bthetaY>-9998&&posL4bthetaY>-9998".format(minVZ,maxVZ,minTheta,maxTheta))
#plots.append("uncVZ -(eleL1bthetaY+eleL2bthetaY+eleL3bthetaY+eleL4bthetaY)+(posL1tthetaY+posL2tthetaY+posL3tthetaY+posL4tthetaY) {0} {1} {2} {3} eleL1bthetaY>-9998&&eleL2bthetaY>-9998&&eleL3bthetaY>-9998&&eleL4bthetaY>-9998&&posL1tthetaY>-9998&&posL2tthetaY>-9998&&posL3tthetaY>-9998&&posL4tthetaY>-9998".format(minVZ,maxVZ,minTheta,maxTheta))

#plots.append("uncVZ -(eleL1tInthetaY+eleL2tthetaY+eleL3tthetaY+eleL4tthetaY)+(posL1bthetaY+posL2bthetaY+posL3bthetaY+posL4bthetaY) {0} {1} {2} {3} eleL1tInthetaY>-9998&&eleL2tthetaY>-9998&&eleL3tthetaY>-9998&&eleL4tthetaY>-9998&&posL1bthetaY>-9998&&posL2bthetaY>-9998&&posL3bthetaY>-9998&&posL4bthetaY>-9998".format(minVZ,maxVZ,minTheta,maxTheta))
#plots.append("uncVZ -(eleL1bInthetaY+eleL2bthetaY+eleL3bthetaY+eleL4bthetaY)+(posL1tthetaY+posL2tthetaY+posL3tthetaY+posL4tthetaY) {0} {1} {2} {3} eleL1bInthetaY>-9998&&eleL2bthetaY>-9998&&eleL3bthetaY>-9998&&eleL4bthetaY>-9998&&posL1tthetaY>-9998&&posL2tthetaY>-9998&&posL3tthetaY>-9998&&posL4tthetaY>-9998".format(minVZ,maxVZ,minTheta,maxTheta))

#plots.append("uncVZ -(eleL1tthetaY+eleL2tInthetaY+eleL3tthetaY+eleL4tthetaY)+(posL1bthetaY+posL2bthetaY+posL3bthetaY+posL4bthetaY) {0} {1} {2} {3} eleL1tthetaY>-9998&&eleL2tInthetaY>-9998&&eleL3tthetaY>-9998&&eleL4tthetaY>-9998&&posL1bthetaY>-9998&&posL2bthetaY>-9998&&posL3bthetaY>-9998&&posL4bthetaY>-9998".format(minVZ,maxVZ,minTheta,maxTheta))
#plots.append("uncVZ -(eleL1bthetaY+eleL2bInthetaY+eleL3bthetaY+eleL4bthetaY)+(posL1tthetaY+posL2tthetaY+posL3tthetaY+posL4tthetaY) {0} {1} {2} {3} eleL1bthetaY>-9998&&eleL2bInthetaY>-9998&&eleL3bthetaY>-9998&&eleL4bthetaY>-9998&&posL1tthetaY>-9998&&posL2tthetaY>-9998&&posL3tthetaY>-9998&&posL4tthetaY>-9998".format(minVZ,maxVZ,minTheta,maxTheta))

#plots.append("uncVZ -(eleL1tthetaY+eleL2tthetaY+eleL3tthetaY+eleL4tthetaY)+(posL1bInthetaY+posL2bthetaY+posL3bthetaY+posL4bthetaY) {0} {1} {2} {3} eleL1tthetaY>-9998&&eleL2tthetaY>-9998&&eleL3tthetaY>-9998&&eleL4tthetaY>-9998&&posL1bInthetaY>-9998&&posL2bthetaY>-9998&&posL3bthetaY>-9998&&posL4bthetaY>-9998".format(minVZ,maxVZ,minTheta,maxTheta))
#plots.append("uncVZ -(eleL1bthetaY+eleL2bthetaY+eleL3bthetaY+eleL4bthetaY)+(posL1tInthetaY+posL2tthetaY+posL3tthetaY+posL4tthetaY) {0} {1} {2} {3} eleL1bthetaY>-9998&&eleL2bthetaY>-9998&&eleL3bthetaY>-9998&&eleL4bthetaY>-9998&&posL1tInthetaY>-9998&&posL2tthetaY>-9998&&posL3tthetaY>-9998&&posL4tthetaY>-9998".format(minVZ,maxVZ,minTheta,maxTheta))

#plots.append("uncVZ -(eleL1tthetaY+eleL2tthetaY+eleL3tthetaY+eleL4tthetaY)+(posL1bthetaY+posL2bInthetaY+posL3bthetaY+posL4bthetaY) {0} {1} {2} {3} eleL1tthetaY>-9998&&eleL2tthetaY>-9998&&eleL3tthetaY>-9998&&eleL4tthetaY>-9998&&posL1bthetaY>-9998&&posL2bInthetaY>-9998&&posL3bthetaY>-9998&&posL4bthetaY>-9998".format(minVZ,maxVZ,minTheta,maxTheta))
#plots.append("uncVZ -(eleL1bthetaY+eleL2bthetaY+eleL3bthetaY+eleL4bthetaY)+(posL1tthetaY+posL2tInthetaY+posL3tthetaY+posL4tthetaY) {0} {1} {2} {3} eleL1bthetaY>-9998&&eleL2bthetaY>-9998&&eleL3bthetaY>-9998&&eleL4bthetaY>-9998&&posL1tthetaY>-9998&&posL2tInthetaY>-9998&&posL3tthetaY>-9998&&posL4tthetaY>-9998".format(minVZ,maxVZ,minTheta,maxTheta))

#plots.append("uncVZ -(eleL1tInthetaY+eleL2tInthetaY+eleL3tthetaY+eleL4tthetaY)+(posL1bthetaY+posL2bthetaY+posL3bthetaY+posL4bthetaY) {0} {1} {2} {3} eleL1tInthetaY>-9998&&eleL2tInthetaY>-9998&&eleL3tthetaY>-9998&&eleL4tthetaY>-9998&&posL1bthetaY>-9998&&posL2bthetaY>-9998&&posL3bthetaY>-9998&&posL4bthetaY>-9998".format(minVZ,maxVZ,minTheta,maxTheta))
#plots.append("uncVZ -(eleL1bInthetaY+eleL2bInthetaY+eleL3bthetaY+eleL4bthetaY)+(posL1tthetaY+posL2tthetaY+posL3tthetaY+posL4tthetaY) {0} {1} {2} {3} eleL1bInthetaY>-9998&&eleL2bInthetaY>-9998&&eleL3bthetaY>-9998&&eleL4bthetaY>-9998&&posL1tthetaY>-9998&&posL2tthetaY>-9998&&posL3tthetaY>-9998&&posL4tthetaY>-9998".format(minVZ,maxVZ,minTheta,maxTheta))

#plots.append("uncVZ -(eleL1tthetaY+eleL2tthetaY+eleL3tthetaY+eleL4tthetaY)+(posL1bInthetaY+posL2bInthetaY+posL3bthetaY+posL4bthetaY) {0} {1} {2} {3} eleL1tthetaY>-9998&&eleL2tthetaY>-9998&&eleL3tthetaY>-9998&&eleL4tthetaY>-9998&&posL1bInthetaY>-9998&&posL2bInthetaY>-9998&&posL3bthetaY>-9998&&posL4bthetaY>-9998".format(minVZ,maxVZ,minTheta,maxTheta))
#plots.append("uncVZ -(eleL1bthetaY+eleL2bthetaY+eleL3bthetaY+eleL4bthetaY)+(posL1tInthetaY+posL2tInthetaY+posL3tthetaY+posL4tthetaY) {0} {1} {2} {3} eleL1bthetaY>-9998&&eleL2bthetaY>-9998&&eleL3bthetaY>-9998&&eleL4bthetaY>-9998&&posL1tInthetaY>-9998&&posL2tInthetaY>-9998&&posL3tthetaY>-9998&&posL4tthetaY>-9998".format(minVZ,maxVZ,minTheta,maxTheta))

cuts = []
cuts.append("")
#cuts.append("max(eleTrkChisq,posTrkChisq)<5")

if(L1L2):
	cuts.append("eleHasTruthMatch&&eleHasL1&&posHasTruthMatch&&!posHasL1")
	cuts.append("eleHasTruthMatch&&eleHasL1&&!posHasTruthMatch&&!posHasL1")
	cuts.append("!eleHasTruthMatch&&eleHasL1&&!posHasTruthMatch&&!posHasL1")
	cuts.append("!eleHasTruthMatch&&eleHasL1&&posHasTruthMatch&&!posHasL1")

	cuts.append("eleHasTruthMatch&&!eleHasL1&&posHasTruthMatch&&posHasL1")
	cuts.append("eleHasTruthMatch&&!eleHasL1&&!posHasTruthMatch&&posHasL1")
	cuts.append("!eleHasTruthMatch&&!eleHasL1&&!posHasTruthMatch&&posHasL1")
	cuts.append("!eleHasTruthMatch&&!eleHasL1&&posHasTruthMatch&&posHasL1")

#else:
#	cuts.append("max(eleTrkChisq,posTrkChisq)<5&&eleHasTruthMatch&&posHasTruthMatch")
#	cuts.append("max(eleTrkChisq,posTrkChisq)<5&&!eleHasTruthMatch&&posHasTruthMatch")
#	cuts.append("max(eleTrkChisq,posTrkChisq)<5&&eleHasTruthMatch&&!posHasTruthMatch")
#	cuts.append("max(eleTrkChisq,posTrkChisq)<5&&!eleHasTruthMatch&&!posHasTruthMatch")

#cuts.append("max(eleTrkChisq,posTrkChisq)<5&&elePurity>0.99&&posPurity>0.99")
#cuts.append("max(eleTrkChisq,posTrkChisq)<5&&elePurity<0.99&&posPurity>0.99")
#cuts.append("max(eleTrkChisq,posTrkChisq)<5&&elePurity>0.99&&posPurity<0.99")
#cuts.append("max(eleTrkChisq,posTrkChisq)<5&&elePurity<0.99&&posPurity<0.99")

#cuts.append("max(eleTrkChisq,posTrkChisq)<5&&(eleL1tIsGoodTruthHit==1||eleL1bIsGoodTruthHit==1)")
#cuts.append("max(eleTrkChisq,posTrkChisq)<5&&(eleL1tIsGoodTruthHit==0||eleL1bIsGoodTruthHit==0)")
#cuts.append("max(eleTrkChisq,posTrkChisq)<5&&(posL1tIsGoodTruthHit==1||posL1bIsGoodTruthHit==1)")
#cuts.append("max(eleTrkChisq,posTrkChisq)<5&&(posL1tIsGoodTruthHit==0||posL1bIsGoodTruthHit==0)")
#cuts.append("max(eleTrkChisq,posTrkChisq)<5&&(eleL2tIsGoodTruthHit==1||eleL2bIsGoodTruthHit==1)")
#cuts.append("max(eleTrkChisq,posTrkChisq)<5&&(eleL2tIsGoodTruthHit==0||eleL2bIsGoodTruthHit==0)")
#cuts.append("max(eleTrkChisq,posTrkChisq)<5&&(posL2tIsGoodTruthHit==1||posL2bIsGoodTruthHit==1)")
#cuts.append("max(eleTrkChisq,posTrkChisq)<5&&(posL2tIsGoodTruthHit==0||posL2bIsGoodTruthHit==0)")

#cuts.append("max(eleTrkChisq,posTrkChisq)<5&&(eleL1tNTruthParticles==1||eleL1bNTruthParticles==1)")
#cuts.append("max(eleTrkChisq,posTrkChisq)<5&&(eleL1tNTruthParticles>1||eleL1bNTruthParticles>1)")
#cuts.append("max(eleTrkChisq,posTrkChisq)<5&&(posL1tNTruthParticles==1||posL1bNTruthParticles==1)")
#cuts.append("max(eleTrkChisq,posTrkChisq)<5&&(posL1tNTruthParticles>1||posL1bNTruthParticles>1)")
#cuts.append("max(eleTrkChisq,posTrkChisq)<5&&(eleL2tNTruthParticles==1||eleL2bNTruthParticles==1)")
#cuts.append("max(eleTrkChisq,posTrkChisq)<5&&(eleL2tNTruthParticles>1||eleL2bNTruthParticles>1)")
#cuts.append("max(eleTrkChisq,posTrkChisq)<5&&(posL2tNTruthParticles==1||posL2bNTruthParticles==1)")
#cuts.append("max(eleTrkChisq,posTrkChisq)<5&&(posL2tNTruthParticles>1||posL2bNTruthParticles>1)")

#cuts.append("max(eleTrkChisq,posTrkChisq)<5&&(eleL3tIsGoodTruthHit==1||eleL3bIsGoodTruthHit==1)")
#cuts.append("max(eleTrkChisq,posTrkChisq)<5&&(eleL3tIsGoodTruthHit==0||eleL3bIsGoodTruthHit==0)")
#cuts.append("max(eleTrkChisq,posTrkChisq)<5&&(posL3tIsGoodTruthHit==1||posL3bIsGoodTruthHit==1)")
#cuts.append("max(eleTrkChisq,posTrkChisq)<5&&(posL3tIsGoodTruthHit==0||posL3bIsGoodTruthHit==0)")
#cuts.append("max(eleTrkChisq,posTrkChisq)<5&&(eleL4tIsGoodTruthHit==1||eleL4bIsGoodTruthHit==1)")
#cuts.append("max(eleTrkChisq,posTrkChisq)<5&&(eleL4tIsGoodTruthHit==0||eleL4bIsGoodTruthHit==0)")
#cuts.append("max(eleTrkChisq,posTrkChisq)<5&&(posL4tIsGoodTruthHit==1||posL4bIsGoodTruthHit==1)")
#cuts.append("max(eleTrkChisq,posTrkChisq)<5&&(posL4tIsGoodTruthHit==0||posL4bIsGoodTruthHit==0)")

#cuts.append("max(eleTrkChisq,posTrkChisq)<5&&(eleL3tNTruthParticles==1||eleL3bNTruthParticles==1)")
#cuts.append("max(eleTrkChisq,posTrkChisq)<5&&(eleL3tNTruthParticles>1||eleL3bNTruthParticles>1)")
#cuts.append("max(eleTrkChisq,posTrkChisq)<5&&(posL3tNTruthParticles==1||posL3bNTruthParticles==1)")
#cuts.append("max(eleTrkChisq,posTrkChisq)<5&&(posL3tNTruthParticles>1||posL3bNTruthParticles>1)")
#cuts.append("max(eleTrkChisq,posTrkChisq)<5&&(eleL4tNTruthParticles==1||eleL4bNTruthParticles==1)")
#cuts.append("max(eleTrkChisq,posTrkChisq)<5&&(eleL4tNTruthParticles>1||eleL4bNTruthParticles>1)")
#cuts.append("max(eleTrkChisq,posTrkChisq)<5&&(posL4tNTruthParticles==1||posL4bNTruthParticles==1)")
#cuts.append("max(eleTrkChisq,posTrkChisq)<5&&(posL4tNTruthParticles>1||posL4bNTruthParticles>1)")

#cuts.append("max(eleTrkChisq,posTrkChisq)<5&&nEcalCl==2")
#cuts.append("max(eleTrkChisq,posTrkChisq)<5&&nEcalCl>2")


rootfile = TFile(outfile+".root","recreate")

openPDF(outfile,c)

for i in range(0,len(cuts)):
	cut = cuts[i]
	eleL1tscatter = TH2F("eleL1tscatter","eleL1tscatter",nBins,minVZ,maxVZ,nBins,minTheta,maxTheta)
	eleL1bscatter = TH2F("eleL1bscatter","eleL1bscatter",nBins,minVZ,maxVZ,nBins,minTheta,maxTheta)
	eleL12tscatter = TH2F("eleL12tscatter","eleL12tscatter",nBins,minVZ,maxVZ,nBins,minTheta,maxTheta)
	eleL12bscatter = TH2F("eleL12bscatter","eleL12bscatter",nBins,minVZ,maxVZ,nBins,minTheta,maxTheta)

	posL1tscatter = TH2F("posL1tscatter","posL1tscatter",nBins,minVZ,maxVZ,nBins,minTheta,maxTheta)
	posL1bscatter = TH2F("posL1bscatter","posL1bscatter",nBins,minVZ,maxVZ,nBins,minTheta,maxTheta)
	posL12tscatter = TH2F("posL12tscatter","posL12tscatter",nBins,minVZ,maxVZ,nBins,minTheta,maxTheta)
	posL12bscatter = TH2F("posL12bscatter","posL12bscatter",nBins,minVZ,maxVZ,nBins,minTheta,maxTheta)

	eleposL1tscatter = TH2F("eleposL1tscatter","eleposL1tscatter",nBins,minVZ,maxVZ,nBins,minTheta,maxTheta)
	eleposL1bscatter = TH2F("eleposL1bscatter","eleposL1bscatter",nBins,minVZ,maxVZ,nBins,minTheta,maxTheta)
	eleposL12tscatter = TH2F("eleposL12tscatter","eleposL12tscatter",nBins,minVZ,maxVZ,nBins,minTheta,maxTheta)
	eleposL12bscatter = TH2F("eleposL12bscatter","eleposL12bscatter",nBins,minVZ,maxVZ,nBins,minTheta,maxTheta)

	cutevents = events.CopyTree(cut)
	neventscut = cutevents.GetEntries()

	uncVZ = array('d',[0])

	eleL1tthetaY = array('d',[0])
	eleL2tthetaY = array('d',[0])
	eleL3tthetaY = array('d',[0])
	eleL4tthetaY = array('d',[0])
	eleL1bthetaY = array('d',[0])
	eleL2bthetaY = array('d',[0])
	eleL3bthetaY = array('d',[0])
	eleL4bthetaY = array('d',[0])

	eleL1tInthetaY = array('d',[0])
	eleL2tInthetaY = array('d',[0])
	eleL3tInthetaY = array('d',[0])
	eleL4tInthetaY = array('d',[0])
	eleL1bInthetaY = array('d',[0])
	eleL2bInthetaY = array('d',[0])
	eleL3bInthetaY = array('d',[0])
	eleL4bInthetaY = array('d',[0])

	posL1tthetaY = array('d',[0])
	posL2tthetaY = array('d',[0])
	posL3tthetaY = array('d',[0])
	posL4tthetaY = array('d',[0])
	posL1bthetaY = array('d',[0])
	posL2bthetaY = array('d',[0])
	posL3bthetaY = array('d',[0])
	posL4bthetaY = array('d',[0])

	posL1tInthetaY = array('d',[0])
	posL2tInthetaY = array('d',[0])
	posL3tInthetaY = array('d',[0])
	posL4tInthetaY = array('d',[0])
	posL1bInthetaY = array('d',[0])
	posL2bInthetaY = array('d',[0])
	posL3bInthetaY = array('d',[0])
	posL4bInthetaY = array('d',[0])

	cutevents.Branch("uncVZ",uncVZ,"uncVZ")

	cutevents.Branch("eleL1tthetaY",eleL1tthetaY,"eleL1tthetaY/D")
	cutevents.Branch("eleL2tthetaY",eleL2tthetaY,"eleL2tthetaY/D")
	cutevents.Branch("eleL3tthetaY",eleL3tthetaY,"eleL3tthetaY/D")
	cutevents.Branch("eleL4tthetaY",eleL4tthetaY,"eleL4tthetaY/D")
	cutevents.Branch("eleL1bthetaY",eleL1bthetaY,"eleL1bthetaY/D")
	cutevents.Branch("eleL2bthetaY",eleL2bthetaY,"eleL2bthetaY/D")
	cutevents.Branch("eleL3bthetaY",eleL3bthetaY,"eleL3bthetaY/D")
	cutevents.Branch("eleL4bthetaY",eleL4bthetaY,"eleL4bthetaY/D")

	cutevents.Branch("eleL1tInthetaY",eleL1tInthetaY,"eleL1tInthetaY/D")
	cutevents.Branch("eleL2tInthetaY",eleL2tInthetaY,"eleL2tInthetaY/D")
	cutevents.Branch("eleL3tInthetaY",eleL3tInthetaY,"eleL3tInthetaY/D")
	cutevents.Branch("eleL4tInthetaY",eleL4tInthetaY,"eleL4tInthetaY/D")
	cutevents.Branch("eleL1bInthetaY",eleL1bInthetaY,"eleL1bInthetaY/D")
	cutevents.Branch("eleL2bInthetaY",eleL2bInthetaY,"eleL2bInthetaY/D")
	cutevents.Branch("eleL3bInthetaY",eleL3bInthetaY,"eleL3bInthetaY/D")
	cutevents.Branch("eleL4bInthetaY",eleL4bInthetaY,"eleL4bInthetaY/D")

	cutevents.Branch("posL1tthetaY",posL1tthetaY,"posL1tthetaY/D")
	cutevents.Branch("posL2tthetaY",posL2tthetaY,"posL2tthetaY/D")
	cutevents.Branch("posL3tthetaY",posL3tthetaY,"posL3tthetaY/D")
	cutevents.Branch("posL4tthetaY",posL4tthetaY,"posL4tthetaY/D")
	cutevents.Branch("posL1bthetaY",posL1bthetaY,"posL1bthetaY/D")
	cutevents.Branch("posL2bthetaY",posL2bthetaY,"posL2bthetaY/D")
	cutevents.Branch("posL3bthetaY",posL3bthetaY,"posL3bthetaY/D")
	cutevents.Branch("posL4bthetaY",posL4bthetaY,"posL4bthetaY/D")

	cutevents.Branch("posL1tInthetaY",posL1tInthetaY,"posL1tInthetaY/D")
	cutevents.Branch("posL2tInthetaY",posL2tInthetaY,"posL2tInthetaY/D")
	cutevents.Branch("posL3tInthetaY",posL3tInthetaY,"posL3tInthetaY/D")
	cutevents.Branch("posL4tInthetaY",posL4tInthetaY,"posL4tInthetaY/D")
	cutevents.Branch("posL1bInthetaY",posL1bInthetaY,"posL1bInthetaY/D")
	cutevents.Branch("posL2bInthetaY",posL2bInthetaY,"posL2bInthetaY/D")
	cutevents.Branch("posL3bInthetaY",posL3bInthetaY,"posL3bInthetaY/D")
	cutevents.Branch("posL4bInthetaY",posL4bInthetaY,"posL4bInthetaY/D")

	for entry in xrange(neventscut):
		cutevents.GetEntry(entry)
		eleL1t = getScatter(cutevents.eleL1tthetaY,cutevents.eleL1tInthetaY)
		eleL2t = getScatter(cutevents.eleL2tthetaY,cutevents.eleL2tInthetaY)
		eleL3t = getScatter(cutevents.eleL3tthetaY,cutevents.eleL3tInthetaY)
		eleL4t = getScatter(cutevents.eleL4tthetaY,cutevents.eleL4tInthetaY)
		posL1t = getScatter(cutevents.posL1tthetaY,cutevents.posL1tInthetaY)
		posL2t = getScatter(cutevents.posL2tthetaY,cutevents.posL2tInthetaY)
		posL3t = getScatter(cutevents.posL3tthetaY,cutevents.posL3tInthetaY)
		posL4t = getScatter(cutevents.posL4tthetaY,cutevents.posL4tInthetaY)
		eleL1b = getScatter(cutevents.eleL1bthetaY,cutevents.eleL1bInthetaY)
		eleL2b = getScatter(cutevents.eleL2bthetaY,cutevents.eleL2bInthetaY)
		eleL3b = getScatter(cutevents.eleL3bthetaY,cutevents.eleL3bInthetaY)
		eleL4b = getScatter(cutevents.eleL4bthetaY,cutevents.eleL4bInthetaY)
		posL1b = getScatter(cutevents.posL1bthetaY,cutevents.posL1bInthetaY)
		posL2b = getScatter(cutevents.posL2bthetaY,cutevents.posL2bInthetaY)
		posL3b = getScatter(cutevents.posL3bthetaY,cutevents.posL3bInthetaY)
		posL4b = getScatter(cutevents.posL4bthetaY,cutevents.posL4bInthetaY)

		eleL1tscatter.Fill(cutevents.uncVZ,-(eleL1t+eleL2t))
		eleL1bscatter.Fill(cutevents.uncVZ,(eleL1b+eleL2b))
		eleL12tscatter.Fill(cutevents.uncVZ,-(eleL1t+eleL2t+eleL3t+eleL4t))
		eleL12bscatter.Fill(cutevents.uncVZ,(eleL1b+eleL2b+eleL3b+eleL4b))

		posL1tscatter.Fill(cutevents.uncVZ,-(posL1t+posL2t))
		posL1bscatter.Fill(cutevents.uncVZ,(posL1b+posL2b))
		posL12tscatter.Fill(cutevents.uncVZ,-(posL1t+posL2t+posL3t+posL4t))
		posL12bscatter.Fill(cutevents.uncVZ,(posL1b+posL2b+posL3b+posL4b))

		if(eleL1t>-9998 and eleL2t>-9998 and posL1b>-9998 and posL2b>-9998):
			eleposL1tscatter.Fill(cutevents.uncVZ,-(eleL1t+eleL2t)+(posL1b+posL2b))
		if(eleL1b>-9998 and eleL2b>-9998 and posL1t>-9998 and posL2t>-9998):
			eleposL1bscatter.Fill(cutevents.uncVZ,-(posL1t+posL2t)+(eleL1b+eleL2b))
		if(eleL1t>-9998 and eleL2t>-9998 and eleL3t>-9998 and eleL4t>-9998 and posL1b>-9998 and posL2b>-9998 and posL3b>-9998 and posL4b>-9998):
			eleposL12tscatter.Fill(cutevents.uncVZ,-(eleL1t+eleL2t+eleL3t+eleL4t)+(posL1b+posL2b+posL3b+posL4b))
		if(eleL1b>-9998 and eleL2b>-9998 and eleL3b>-9998 and eleL4b>-9998 and posL1t>-9998 and posL2t>-9998 and posL3t>-9998 and posL4t>-9998):
			eleposL12bscatter.Fill(cutevents.uncVZ,(eleL1b+eleL2b+eleL3b+eleL4b)-(posL1t+posL2t+posL3t+posL4t))

	savehisto2D(eleL1tscatter,outfile,c,"uncVZ","theta","L1t Electron Scatter " + cut,1)
	savehisto2D(eleL1bscatter,outfile,c,"uncVZ","theta","L1b Electron Scatter " + cut,1)
	savehisto2D(eleL12tscatter,outfile,c,"uncVZ","theta","L1t + L2t Electron Scatter " + cut,1)
	savehisto2D(eleL12bscatter,outfile,c,"uncVZ","theta","L1b + L2t Electron Scatter " + cut,1)

	savehisto2D(posL1tscatter,outfile,c,"uncVZ","theta","L1t Positron Scatter " + cut,1)
	savehisto2D(posL1bscatter,outfile,c,"uncVZ","theta","L1b Positron Scatter " + cut,1)
	savehisto2D(posL12tscatter,outfile,c,"uncVZ","theta","L1t + L2t Positron Scatter " + cut,1)
	savehisto2D(posL12bscatter,outfile,c,"uncVZ","theta","L1b + L2t Positron Scatter " + cut,1)

	savehisto2D(eleposL1tscatter,outfile,c,"uncVZ","theta","L1t Electron - Positron Scatter " + cut,1)
	savehisto2D(eleposL1bscatter,outfile,c,"uncVZ","theta","L1b Electron - Positron Scatter " + cut,1)
	savehisto2D(eleposL12tscatter,outfile,c,"uncVZ","theta","L1t + L2t Electron - Positron Scatter " + cut,1)
	savehisto2D(eleposL12bscatter,outfile,c,"uncVZ","theta","L1b + L2t Electron - Positron Scatter " + cut,1)

	del cutevents

	del eleL1tthetaY
	del eleL2tthetaY
	del eleL3tthetaY
	del eleL4tthetaY
	del eleL1bthetaY
	del eleL2bthetaY
	del eleL3bthetaY
	del eleL4bthetaY

	del eleL1tInthetaY
	del eleL2tInthetaY
	del eleL3tInthetaY
	del eleL4tInthetaY
	del eleL1bInthetaY
	del eleL2bInthetaY
	del eleL3bInthetaY
	del eleL4bInthetaY

	del posL1tthetaY
	del posL2tthetaY
	del posL3tthetaY
	del posL4tthetaY
	del posL1bthetaY
	del posL2bthetaY
	del posL3bthetaY
	del posL4bthetaY

	del posL1tInthetaY
	del posL2tInthetaY
	del posL3tInthetaY
	del posL4tInthetaY
	del posL1bInthetaY
	del posL2bInthetaY
	del posL3bInthetaY
	del posL4bInthetaY

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