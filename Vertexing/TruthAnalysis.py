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
	del histo

def savehisto2D(histo,outfile,canvas,XaxisTitle="",YaxisTitle="",plotTitle="",stats=0,logY=0):
	histo.SetTitle(plotTitle)
	histo.GetXaxis().SetTitle(XaxisTitle)
	histo.GetYaxis().SetTitle(YaxisTitle)
	histo.SetStats(stats)
	histo.Draw("COLZ")
	canvas.SetLogy(logY)
	canvas.Print(outfile+".pdf")
	del histo

L1L2 = False

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'hl')

# Parse the command line arguments
for opt, arg in options:
		if opt=='-l':
			L1L2 = True
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
minTheta = -0.05
maxTheta = 0.05
minVZ = -50
maxVZ = 130

plots = []
plots.append("uncM uncVZ 0 0.1 {0} {1}".format(minVZ,maxVZ))
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

plots.append("uncVZ -eleL1tInthetaY {0} {1} {2} {3}".format(minVZ,maxVZ,minTheta,maxTheta))
plots.append("uncVZ -eleL2tInthetaY {0} {1} {2} {3}".format(minVZ,maxVZ,minTheta,maxTheta))
plots.append("uncVZ -eleL3tInthetaY {0} {1} {2} {3}".format(minVZ,maxVZ,minTheta,maxTheta))
plots.append("uncVZ -eleL4tInthetaY {0} {1} {2} {3}".format(minVZ,maxVZ,minTheta,maxTheta))
plots.append("uncVZ eleL1bInthetaY {0} {1} {2} {3}".format(minVZ,maxVZ,minTheta,maxTheta))
plots.append("uncVZ eleL2bInthetaY {0} {1} {2} {3}".format(minVZ,maxVZ,minTheta,maxTheta))
plots.append("uncVZ eleL3bInthetaY {0} {1} {2} {3}".format(minVZ,maxVZ,minTheta,maxTheta))
plots.append("uncVZ eleL4bInthetaY {0} {1} {2} {3}".format(minVZ,maxVZ,minTheta,maxTheta))
plots.append("uncVZ -posL1tInthetaY {0} {1} {2} {3}".format(minVZ,maxVZ,minTheta,maxTheta))
plots.append("uncVZ -posL2tInthetaY {0} {1} {2} {3}".format(minVZ,maxVZ,minTheta,maxTheta))
plots.append("uncVZ -posL3tInthetaY {0} {1} {2} {3}".format(minVZ,maxVZ,minTheta,maxTheta))
plots.append("uncVZ -posL4tInthetaY {0} {1} {2} {3}".format(minVZ,maxVZ,minTheta,maxTheta))
plots.append("uncVZ posL1bInthetaY {0} {1} {2} {3}".format(minVZ,maxVZ,minTheta,maxTheta))
plots.append("uncVZ posL2bInthetaY {0} {1} {2} {3}".format(minVZ,maxVZ,minTheta,maxTheta))
plots.append("uncVZ posL3bInthetaY {0} {1} {2} {3}".format(minVZ,maxVZ,minTheta,maxTheta))
plots.append("uncVZ posL4bInthetaY {0} {1} {2} {3}".format(minVZ,maxVZ,minTheta,maxTheta))

plots.append("uncVZ -(eleL1tthetaY+eleL2tthetaY) {0} {1} {2} {3}".format(minVZ,maxVZ,minTheta,maxTheta))
plots.append("uncVZ (eleL1bthetaY+eleL2bthetaY) {0} {1} {2} {3}".format(minVZ,maxVZ,minTheta,maxTheta))
plots.append("uncVZ -(eleL1tInthetaY+eleL2tthetaY) {0} {1} {2} {3}".format(minVZ,maxVZ,minTheta,maxTheta))
plots.append("uncVZ (eleL1bInthetaY+eleL2bthetaY) {0} {1} {2} {3}".format(minVZ,maxVZ,minTheta,maxTheta))
plots.append("uncVZ -(eleL1tInthetaY+eleL2tInthetaY) {0} {1} {2} {3}".format(minVZ,maxVZ,minTheta,maxTheta))
plots.append("uncVZ (eleL1bInthetaY+eleL2bInthetaY) {0} {1} {2} {3}".format(minVZ,maxVZ,minTheta,maxTheta))
plots.append("uncVZ -(posL1tthetaY+posL2tthetaY) {0} {1} {2} {3}".format(minVZ,maxVZ,minTheta,maxTheta))
plots.append("uncVZ (posL1bthetaY+posL2bthetaY) {0} {1} {2} {3}".format(minVZ,maxVZ,minTheta,maxTheta))
plots.append("uncVZ -(posL1tInthetaY+posL2tthetaY) {0} {1} {2} {3}".format(minVZ,maxVZ,minTheta,maxTheta))
plots.append("uncVZ (posL1bInthetaY+posL2bthetaY) {0} {1} {2} {3}".format(minVZ,maxVZ,minTheta,maxTheta))
plots.append("uncVZ -(posL1tInthetaY+posL2tInthetaY) {0} {1} {2} {3}".format(minVZ,maxVZ,minTheta,maxTheta))
plots.append("uncVZ (posL1bInthetaY+posL2bInthetaY) {0} {1} {2} {3}".format(minVZ,maxVZ,minTheta,maxTheta))

plots.append("uncVZ -(eleL1tthetaY+eleL2tthetaY)+(posL1bthetaY+posL2bthetaY) {0} {1} {2} {3} eleL1tthetaY>-9998&&eleL2tthetaY>-9998&&posL1bthetaY>-9998&&posL2bthetaY>-9998".format(minVZ,maxVZ,minTheta,maxTheta))
plots.append("uncVZ (eleL1bthetaY+eleL2bthetaY)-(posL1tthetaY+posL2tthetaY) {0} {1} {2} {3} eleL1bthetaY>-9998&&eleL2bthetaY>-9998&&posL1tthetaY>-9998&&posL2tthetaY>-9998".format(minVZ,maxVZ,minTheta,maxTheta))

plots.append("uncVZ -(eleL1tInthetaY+eleL2tthetaY)+(posL1bthetaY+posL2bthetaY) {0} {1} {2} {3} eleL1tInthetaY>-9998&&eleL2tthetaY>-9998&&posL1bthetaY>-9998&&posL2bthetaY>-9998".format(minVZ,maxVZ,minTheta,maxTheta))
plots.append("uncVZ (eleL1bInthetaY+eleL2bthetaY)-(posL1tthetaY+posL2tthetaY) {0} {1} {2} {3} eleL1bInthetaY>-9998&&eleL2bthetaY>-9998&&posL1tthetaY>-9998&&posL2tthetaY>-9998".format(minVZ,maxVZ,minTheta,maxTheta))

plots.append("uncVZ -(eleL1tthetaY+eleL2tthetaY)+(posL1bInthetaY+posL2bthetaY) {0} {1} {2} {3} eleL1tthetaY>-9998&&eleL2tthetaY>-9998&&posL1bInthetaY>-9998&&posL2bthetaY>-9998".format(minVZ,maxVZ,minTheta,maxTheta))
plots.append("uncVZ (eleL1bthetaY+eleL2bthetaY)-(posL1tInthetaY+posL2tthetaY) {0} {1} {2} {3} eleL1bthetaY>-9998&&eleL2bthetaY>-9998&&posL1tInthetaY>-9998&&posL2tthetaY>-9998".format(minVZ,maxVZ,minTheta,maxTheta))

plots.append("uncVZ -(eleL1tthetaY+eleL2tInthetaY)+(posL1bthetaY+posL2bthetaY) {0} {1} {2} {3} eleL1tthetaY>-9998&&eleL2tInthetaY>-9998&&posL1bthetaY>-9998&&posL2bthetaY>-9998".format(minVZ,maxVZ,minTheta,maxTheta))
plots.append("uncVZ (eleL1bthetaY+eleL2bInthetaY)-(posL1tthetaY+posL2tthetaY) {0} {1} {2} {3} eleL1bthetaY>-9998&&eleL2bInthetaY>-9998&&posL1tthetaY>-9998&&posL2tthetaY>-9998".format(minVZ,maxVZ,minTheta,maxTheta))

plots.append("uncVZ -(eleL1tthetaY+eleL2tthetaY)+(posL1bthetaY+posL2bInthetaY) {0} {1} {2} {3} eleL1tthetaY>-9998&&eleL2tthetaY>-9998&&posL1bthetaY>-9998&&posL2bInthetaY>-9998".format(minVZ,maxVZ,minTheta,maxTheta))
plots.append("uncVZ (eleL1bthetaY+eleL2bthetaY)-(posL1tthetaY+posL2tInthetaY) {0} {1} {2} {3} eleL1bthetaY>-9998&&eleL2bthetaY>-9998&&posL1tthetaY>-9998&&posL2tInthetaY>-9998".format(minVZ,maxVZ,minTheta,maxTheta))

plots.append("uncVZ -(eleL1tInthetaY+eleL2tInthetaY)+(posL1bthetaY+posL2bthetaY) {0} {1} {2} {3} eleL1tInthetaY>-9998&&eleL2tInthetaY>-9998&&posL1bthetaY>-9998&&posL2bthetaY>-9998".format(minVZ,maxVZ,minTheta,maxTheta))
plots.append("uncVZ (eleL1bInthetaY+eleL2bInthetaY)-(posL1tthetaY+posL2tthetaY) {0} {1} {2} {3} eleL1bInthetaY>-9998&&eleL2bInthetaY>-9998&&posL1tthetaY>-9998&&posL2tthetaY>-9998".format(minVZ,maxVZ,minTheta,maxTheta))

plots.append("uncVZ -(eleL1tthetaY+eleL2tthetaY)+(posL1bInthetaY+posL2bInthetaY) {0} {1} {2} {3} eleL1tthetaY>-9998&&eleL2tthetaY>-9998&&posL1bInthetaY>-9998&&posL2bInthetaY>-9998".format(minVZ,maxVZ,minTheta,maxTheta))
plots.append("uncVZ (eleL1bthetaY+eleL2bthetaY)-(posL1tInthetaY+posL2tInthetaY) {0} {1} {2} {3} eleL1bthetaY>-9998&&eleL2bthetaY>-9998&&posL1tInthetaY>-9998&&posL2tInthetaY>-9998".format(minVZ,maxVZ,minTheta,maxTheta))

plots.append("uncVZ -(eleL1tInthetaY+eleL2tInthetaY)+(posL1bInthetaY+posL2bthetaY) {0} {1} {2} {3} eleL1tInthetaY>-9998&&eleL2tInthetaY>-9998&&posL1bInthetaY>-9998&&posL2bthetaY>-9998".format(minVZ,maxVZ,minTheta,maxTheta))
plots.append("uncVZ (eleL1bInthetaY+eleL2bInthetaY)-(posL1tInthetaY+posL2tthetaY) {0} {1} {2} {3} eleL1bInthetaY>-9998&&eleL2bInthetaY>-9998&&posL1tInthetaY>-9998&&posL2tthetaY>-9998".format(minVZ,maxVZ,minTheta,maxTheta))

plots.append("uncVZ -(eleL1tInthetaY+eleL2tInthetaY)+(posL1bthetaY+posL2bInthetaY) {0} {1} {2} {3} eleL1tInthetaY>-9998&&eleL2tInthetaY>-9998&&posL1bthetaY>-9998&&posL2bInthetaY>-9998".format(minVZ,maxVZ,minTheta,maxTheta))
plots.append("uncVZ (eleL1bInthetaY+eleL2bInthetaY)-(posL1tthetaY+posL2tInthetaY) {0} {1} {2} {3} eleL1bInthetaY>-9998&&eleL2bInthetaY>-9998&&posL1tthetaY>-9998&&posL2tInthetaY>-9998".format(minVZ,maxVZ,minTheta,maxTheta))

plots.append("uncVZ -(eleL1tInthetaY+eleL2tthetaY)+(posL1bInthetaY+posL2bInthetaY) {0} {1} {2} {3} eleL1tInthetaY>-9998&&eleL2tthetaY>-9998&&posL1bInthetaY>-9998&&posL2bInthetaY>-9998".format(minVZ,maxVZ,minTheta,maxTheta))
plots.append("uncVZ (eleL1bInthetaY+eleL2bthetaY)-(posL1tInthetaY+posL2tInthetaY) {0} {1} {2} {3} eleL1bInthetaY>-9998&&eleL2bthetaY>-9998&&posL1tInthetaY>-9998&&posL2tInthetaY>-9998".format(minVZ,maxVZ,minTheta,maxTheta))

plots.append("uncVZ -(eleL1tthetaY+eleL2tInthetaY)+(posL1bInthetaY+posL2bInthetaY) {0} {1} {2} {3} eleL1tthetaY>-9998&&eleL2tInthetaY>-9998&&posL1bInthetaY>-9998&&posL2bInthetaY>-9998".format(minVZ,maxVZ,minTheta,maxTheta))
plots.append("uncVZ (eleL1bthetaY+eleL2bInthetaY)-(posL1tInthetaY+posL2tInthetaY) {0} {1} {2} {3} eleL1bthetaY>-9998&&eleL2bInthetaY>-9998&&posL1tInthetaY>-9998&&posL2tInthetaY>-9998".format(minVZ,maxVZ,minTheta,maxTheta))

plots.append("uncVZ -(eleL1tInthetaY+eleL2tInthetaY)+(posL1bInthetaY+posL2bInthetaY) {0} {1} {2} {3} eleL1tInthetaY>-9998&&eleL2tInthetaY>-9998&&posL1bInthetaY>-9998&&posL2bInthetaY>-9998".format(minVZ,maxVZ,minTheta,maxTheta))
plots.append("uncVZ (eleL1bInthetaY+eleL2bInthetaY)-(posL1tInthetaY+posL2tInthetaY) {0} {1} {2} {3} eleL1bInthetaY>-9998&&eleL2bInthetaY>-9998&&posL1tInthetaY>-9998&&posL2tInthetaY>-9998".format(minVZ,maxVZ,minTheta,maxTheta))


plots.append("uncVZ -(eleL1tthetaY+eleL2tthetaY+eleL3tthetaY+eleL4tthetaY)+(posL1bthetaY+posL2bthetaY+posL3bthetaY+posL4bthetaY) {0} {1} {2} {3} eleL1tthetaY>-9998&&eleL2tthetaY>-9998&&eleL3tthetaY>-9998&&eleL4tthetaY>-9998&&posL1bthetaY>-9998&&posL2bthetaY>-9998&&posL3bthetaY>-9998&&posL4bthetaY>-9998".format(minVZ,maxVZ,minTheta,maxTheta))
plots.append("uncVZ -(eleL1bthetaY+eleL2bthetaY+eleL3bthetaY+eleL4bthetaY)+(posL1tthetaY+posL2tthetaY+posL3tthetaY+posL4tthetaY) {0} {1} {2} {3} eleL1bthetaY>-9998&&eleL2bthetaY>-9998&&eleL3bthetaY>-9998&&eleL4bthetaY>-9998&&posL1tthetaY>-9998&&posL2tthetaY>-9998&&posL3tthetaY>-9998&&posL4tthetaY>-9998".format(minVZ,maxVZ,minTheta,maxTheta))

plots.append("uncVZ -(eleL1tInthetaY+eleL2tthetaY+eleL3tthetaY+eleL4tthetaY)+(posL1bthetaY+posL2bthetaY+posL3bthetaY+posL4bthetaY) {0} {1} {2} {3} eleL1tInthetaY>-9998&&eleL2tthetaY>-9998&&eleL3tthetaY>-9998&&eleL4tthetaY>-9998&&posL1bthetaY>-9998&&posL2bthetaY>-9998&&posL3bthetaY>-9998&&posL4bthetaY>-9998".format(minVZ,maxVZ,minTheta,maxTheta))
plots.append("uncVZ -(eleL1bInthetaY+eleL2bthetaY+eleL3bthetaY+eleL4bthetaY)+(posL1tthetaY+posL2tthetaY+posL3tthetaY+posL4tthetaY) {0} {1} {2} {3} eleL1bInthetaY>-9998&&eleL2bthetaY>-9998&&eleL3bthetaY>-9998&&eleL4bthetaY>-9998&&posL1tthetaY>-9998&&posL2tthetaY>-9998&&posL3tthetaY>-9998&&posL4tthetaY>-9998".format(minVZ,maxVZ,minTheta,maxTheta))

plots.append("uncVZ -(eleL1tthetaY+eleL2tInthetaY+eleL3tthetaY+eleL4tthetaY)+(posL1bthetaY+posL2bthetaY+posL3bthetaY+posL4bthetaY) {0} {1} {2} {3} eleL1tthetaY>-9998&&eleL2tInthetaY>-9998&&eleL3tthetaY>-9998&&eleL4tthetaY>-9998&&posL1bthetaY>-9998&&posL2bthetaY>-9998&&posL3bthetaY>-9998&&posL4bthetaY>-9998".format(minVZ,maxVZ,minTheta,maxTheta))
plots.append("uncVZ -(eleL1bthetaY+eleL2bInthetaY+eleL3bthetaY+eleL4bthetaY)+(posL1tthetaY+posL2tthetaY+posL3tthetaY+posL4tthetaY) {0} {1} {2} {3} eleL1bthetaY>-9998&&eleL2bInthetaY>-9998&&eleL3bthetaY>-9998&&eleL4bthetaY>-9998&&posL1tthetaY>-9998&&posL2tthetaY>-9998&&posL3tthetaY>-9998&&posL4tthetaY>-9998".format(minVZ,maxVZ,minTheta,maxTheta))

plots.append("uncVZ -(eleL1tthetaY+eleL2tthetaY+eleL3tthetaY+eleL4tthetaY)+(posL1bInthetaY+posL2bthetaY+posL3bthetaY+posL4bthetaY) {0} {1} {2} {3} eleL1tthetaY>-9998&&eleL2tthetaY>-9998&&eleL3tthetaY>-9998&&eleL4tthetaY>-9998&&posL1bInthetaY>-9998&&posL2bthetaY>-9998&&posL3bthetaY>-9998&&posL4bthetaY>-9998".format(minVZ,maxVZ,minTheta,maxTheta))
plots.append("uncVZ -(eleL1bthetaY+eleL2bthetaY+eleL3bthetaY+eleL4bthetaY)+(posL1tInthetaY+posL2tthetaY+posL3tthetaY+posL4tthetaY) {0} {1} {2} {3} eleL1bthetaY>-9998&&eleL2bthetaY>-9998&&eleL3bthetaY>-9998&&eleL4bthetaY>-9998&&posL1tInthetaY>-9998&&posL2tthetaY>-9998&&posL3tthetaY>-9998&&posL4tthetaY>-9998".format(minVZ,maxVZ,minTheta,maxTheta))

plots.append("uncVZ -(eleL1tthetaY+eleL2tthetaY+eleL3tthetaY+eleL4tthetaY)+(posL1bthetaY+posL2bInthetaY+posL3bthetaY+posL4bthetaY) {0} {1} {2} {3} eleL1tthetaY>-9998&&eleL2tthetaY>-9998&&eleL3tthetaY>-9998&&eleL4tthetaY>-9998&&posL1bthetaY>-9998&&posL2bInthetaY>-9998&&posL3bthetaY>-9998&&posL4bthetaY>-9998".format(minVZ,maxVZ,minTheta,maxTheta))
plots.append("uncVZ -(eleL1bthetaY+eleL2bthetaY+eleL3bthetaY+eleL4bthetaY)+(posL1tthetaY+posL2tInthetaY+posL3tthetaY+posL4tthetaY) {0} {1} {2} {3} eleL1bthetaY>-9998&&eleL2bthetaY>-9998&&eleL3bthetaY>-9998&&eleL4bthetaY>-9998&&posL1tthetaY>-9998&&posL2tInthetaY>-9998&&posL3tthetaY>-9998&&posL4tthetaY>-9998".format(minVZ,maxVZ,minTheta,maxTheta))

plots.append("uncVZ -(eleL1tInthetaY+eleL2tInthetaY+eleL3tthetaY+eleL4tthetaY)+(posL1bthetaY+posL2bthetaY+posL3bthetaY+posL4bthetaY) {0} {1} {2} {3} eleL1tInthetaY>-9998&&eleL2tInthetaY>-9998&&eleL3tthetaY>-9998&&eleL4tthetaY>-9998&&posL1bthetaY>-9998&&posL2bthetaY>-9998&&posL3bthetaY>-9998&&posL4bthetaY>-9998".format(minVZ,maxVZ,minTheta,maxTheta))
plots.append("uncVZ -(eleL1bInthetaY+eleL2bInthetaY+eleL3bthetaY+eleL4bthetaY)+(posL1tthetaY+posL2tthetaY+posL3tthetaY+posL4tthetaY) {0} {1} {2} {3} eleL1bInthetaY>-9998&&eleL2bInthetaY>-9998&&eleL3bthetaY>-9998&&eleL4bthetaY>-9998&&posL1tthetaY>-9998&&posL2tthetaY>-9998&&posL3tthetaY>-9998&&posL4tthetaY>-9998".format(minVZ,maxVZ,minTheta,maxTheta))

plots.append("uncVZ -(eleL1tthetaY+eleL2tthetaY+eleL3tthetaY+eleL4tthetaY)+(posL1bInthetaY+posL2bInthetaY+posL3bthetaY+posL4bthetaY) {0} {1} {2} {3} eleL1tthetaY>-9998&&eleL2tthetaY>-9998&&eleL3tthetaY>-9998&&eleL4tthetaY>-9998&&posL1bInthetaY>-9998&&posL2bInthetaY>-9998&&posL3bthetaY>-9998&&posL4bthetaY>-9998".format(minVZ,maxVZ,minTheta,maxTheta))
plots.append("uncVZ -(eleL1bthetaY+eleL2bthetaY+eleL3bthetaY+eleL4bthetaY)+(posL1tInthetaY+posL2tInthetaY+posL3tthetaY+posL4tthetaY) {0} {1} {2} {3} eleL1bthetaY>-9998&&eleL2bthetaY>-9998&&eleL3bthetaY>-9998&&eleL4bthetaY>-9998&&posL1tInthetaY>-9998&&posL2tInthetaY>-9998&&posL3tthetaY>-9998&&posL4tthetaY>-9998".format(minVZ,maxVZ,minTheta,maxTheta))

cuts = []
cuts.append("")

if(L1L2):
	cuts.append("eleHasTruthMatch&&eleHasL1&&posHasTruthMatch&&!posHasL1")
	cuts.append("eleHasTruthMatch&&eleHasL1&&!posHasTruthMatch&&!posHasL1")
	cuts.append("!eleHasTruthMatch&&eleHasL1&&!posHasTruthMatch&&!posHasL1")
	cuts.append("!eleHasTruthMatch&&eleHasL1&&posHasTruthMatch&&!posHasL1")

	cuts.append("eleHasTruthMatch&&!eleHasL1&&posHasTruthMatch&&posHasL1")
	cuts.append("eleHasTruthMatch&&!eleHasL1&&!posHasTruthMatch&&posHasL1")
	cuts.append("!eleHasTruthMatch&&!eleHasL1&&!posHasTruthMatch&&posHasL1")
	cuts.append("!eleHasTruthMatch&&!eleHasL1&&posHasTruthMatch&&posHasL1")

else:
	cuts.append("eleHasTruthMatch&&posHasTruthMatch")
	cuts.append("!eleHasTruthMatch&&posHasTruthMatch")
	cuts.append("!eleHasTruthMatch&&!posHasTruthMatch")

nevents = events.GetEntries()
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

events.Branch("uncVZ",uncVZ,"uncVZ")

events.Branch("eleL1tthetaY",eleL1tthetaY,"eleL1tthetaY/D")
events.Branch("eleL2tthetaY",eleL2tthetaY,"eleL2tthetaY/D")
events.Branch("eleL3tthetaY",eleL3tthetaY,"eleL3tthetaY/D")
events.Branch("eleL4tthetaY",eleL4tthetaY,"eleL4tthetaY/D")
events.Branch("eleL1bthetaY",eleL1bthetaY,"eleL1bthetaY/D")
events.Branch("eleL2bthetaY",eleL2bthetaY,"eleL2bthetaY/D")
events.Branch("eleL3bthetaY",eleL3bthetaY,"eleL3bthetaY/D")
events.Branch("eleL4bthetaY",eleL4bthetaY,"eleL4bthetaY/D")

events.Branch("eleL1tInthetaY",eleL1tInthetaY,"eleL1tInthetaY/D")
events.Branch("eleL2tInthetaY",eleL2tInthetaY,"eleL2tInthetaY/D")
events.Branch("eleL3tInthetaY",eleL3tInthetaY,"eleL3tInthetaY/D")
events.Branch("eleL4tInthetaY",eleL4tInthetaY,"eleL4tInthetaY/D")
events.Branch("eleL1bInthetaY",eleL1bInthetaY,"eleL1bInthetaY/D")
events.Branch("eleL2bInthetaY",eleL2bInthetaY,"eleL2bInthetaY/D")
events.Branch("eleL3bInthetaY",eleL3bInthetaY,"eleL3bInthetaY/D")
events.Branch("eleL4bInthetaY",eleL4bInthetaY,"eleL4bInthetaY/D")

events.Branch("posL1tthetaY",posL1tthetaY,"posL1tthetaY/D")
events.Branch("posL2tthetaY",posL2tthetaY,"posL2tthetaY/D")
events.Branch("posL3tthetaY",posL3tthetaY,"posL3tthetaY/D")
events.Branch("posL4tthetaY",posL4tthetaY,"posL4tthetaY/D")
events.Branch("posL1bthetaY",posL1bthetaY,"posL1bthetaY/D")
events.Branch("posL2bthetaY",posL2bthetaY,"posL2bthetaY/D")
events.Branch("posL3bthetaY",posL3bthetaY,"posL3bthetaY/D")
events.Branch("posL4bthetaY",posL4bthetaY,"posL4bthetaY/D")

events.Branch("posL1tInthetaY",posL1tInthetaY,"posL1tInthetaY/D")
events.Branch("posL2tInthetaY",posL2tInthetaY,"posL2tInthetaY/D")
events.Branch("posL3tInthetaY",posL3tInthetaY,"posL3tInthetaY/D")
events.Branch("posL4tInthetaY",posL4tInthetaY,"posL4tInthetaY/D")
events.Branch("posL1bInthetaY",posL1bInthetaY,"posL1bInthetaY/D")
events.Branch("posL2bInthetaY",posL2bInthetaY,"posL2bInthetaY/D")
events.Branch("posL3bInthetaY",posL3bInthetaY,"posL3bInthetaY/D")
events.Branch("posL4bInthetaY",posL4bInthetaY,"posL4bInthetaY/D")

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

	for entry in xrange(nevents):
		events.GetEntry(entry)
		eleL1t = getScatter(events.eleL1tthetaY,events.eleL1tInthetaY)
		eleL2t = getScatter(events.eleL2tthetaY,events.eleL2tInthetaY)
		eleL3t = getScatter(events.eleL3tthetaY,events.eleL3tInthetaY)
		eleL4t = getScatter(events.eleL4tthetaY,events.eleL4tInthetaY)
		posL1t = getScatter(events.posL1tthetaY,events.posL1tInthetaY)
		posL2t = getScatter(events.posL2tthetaY,events.posL2tInthetaY)
		posL3t = getScatter(events.posL3tthetaY,events.posL3tInthetaY)
		posL4t = getScatter(events.posL4tthetaY,events.posL4tInthetaY)
		eleL1b = getScatter(events.eleL1bthetaY,events.eleL1bInthetaY)
		eleL2b = getScatter(events.eleL2bthetaY,events.eleL2bInthetaY)
		eleL3b = getScatter(events.eleL3bthetaY,events.eleL3bInthetaY)
		eleL4b = getScatter(events.eleL4bthetaY,events.eleL4bInthetaY)
		posL1b = getScatter(events.posL1bthetaY,events.posL1bInthetaY)
		posL2b = getScatter(events.posL2bthetaY,events.posL2bInthetaY)
		posL3b = getScatter(events.posL3bthetaY,events.posL3bInthetaY)
		posL4b = getScatter(events.posL4bthetaY,events.posL4bInthetaY)

		eleL1tscatter.Fill(events.uncVZ,-(eleL1t+eleL2t))
		eleL1bscatter.Fill(events.uncVZ,(eleL1b+eleL2b))
		eleL12tscatter.Fill(events.uncVZ,-(eleL1t+eleL2t+eleL3t+eleL4t))
		eleL12bscatter.Fill(events.uncVZ,(eleL1b+eleL2b+eleL3b+eleL4b))

		posL1tscatter.Fill(events.uncVZ,-(posL1t+posL2t))
		posL1bscatter.Fill(events.uncVZ,(posL1b+posL2b))
		posL12tscatter.Fill(events.uncVZ,-(posL1t+posL2t+posL3t+posL4t))
		posL12bscatter.Fill(events.uncVZ,(posL1b+posL2b+posL3b+posL4b))

		if(eleL1t>-9998 and eleL2t>-9998 and posL1b>-9998 and posL2b>-9998):
			eleposL1tscatter.Fill(events.uncVZ,-(eleL1t+eleL2t)+(posL1b+posL2b))
		if(eleL1b>-9998 and eleL2b>-9998 and posL1t>-9998 and posL2t>-9998):
			eleposL1bscatter.Fill(events.uncVZ,-(posL1t+posL2t)+(eleL1b+eleL2b))
		if(eleL1t>-9998 and eleL2t>-9998 and eleL3t>-9998 and eleL4t>-9998 and posL1b>-9998 and posL2b>-9998 and posL3b>-9998 and posL4b>-9998):
			eleposL12tscatter.Fill(events.uncVZ,-(eleL1t+eleL2t+eleL3t+eleL4t)+(posL1b+posL2b+posL3b+posL4b))
		if(eleL1b>-9998 and eleL2b>-9998 and eleL3b>-9998 and eleL4b>-9998 and posL1t>-9998 and posL2t>-9998 and posL3t>-9998 and posL4t>-9998):
			eleposL12bscatter.Fill(events.uncVZ,(eleL1b+eleL2b+eleL3b+eleL4b)-(posL1t+posL2t+posL3t+posL4t))

	savehisto2D(eleL1tscatter,outfile,c,"uncVZ","theta","L1t Electron Scatter")
	savehisto2D(eleL1bscatter,outfile,c,"uncVZ","theta","L1b Electron Scatter")
	savehisto2D(eleL12tscatter,outfile,c,"uncVZ","theta","L1t + L2t Electron Scatter")
	savehisto2D(eleL12bscatter,outfile,c,"uncVZ","theta","L1b + L2t Electron Scatter")

	savehisto2D(posL1tscatter,outfile,c,"uncVZ","theta","L1t Positron Scatter")
	savehisto2D(posL1bscatter,outfile,c,"uncVZ","theta","L1b Positron Scatter")
	savehisto2D(posL12tscatter,outfile,c,"uncVZ","theta","L1t + L2t Positron Scatter")
	savehisto2D(posL12bscatter,outfile,c,"uncVZ","theta","L1b + L2t Positron Scatter")

	savehisto2D(eleposL1tscatter,outfile,c,"uncVZ","theta","L1t Electron - Positron Scatter")
	savehisto2D(eleposL1bscatter,outfile,c,"uncVZ","theta","L1b Electron - Positron Scatter")
	savehisto2D(eleposL12tscatter,outfile,c,"uncVZ","theta","L1t + L2t Electron - Positron Scatter")
	savehisto2D(eleposL12bscatter,outfile,c,"uncVZ","theta","L1b + L2t Electron - Positron Scatter")

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