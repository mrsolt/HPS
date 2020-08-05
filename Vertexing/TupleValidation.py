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
    print '\t-t: use full truth plots'
    print '\t-m: minimum uncVZ'
    print '\t-n: maximum uncVZ'
    print '\t-h: this help message'
    print

fullTruth = False
minVZ = -20
maxVZ = 120

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'tm:n:h')

# Parse the command line arguments
for opt, arg in options:
		if opt=='-t':
			fullTruth = True
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
	del histo


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

nBins = 100

outfile = remainder[0]

events = TChain("ntuple")
for i in range(1,len(remainder)):
    events.Add(remainder[i])

plots = []
plots.append("uncVZ {0} {1}".format(minVZ,maxVZ))
plots.append("uncM 0 0.2")
plots.append("uncP 0 3.2")
plots.append("uncChisq 0 20")
plots.append("bscChisq 0 20")
plots.append("sqrt(uncCovZZ) 0 30")
plots.append("eleClT 20 80")
plots.append("posClT 20 80")
plots.append("eleClE 0 3.2")
plots.append("posClE 0 3.2")
plots.append("eleP 0 3.2")
plots.append("posP 0 3.2")
plots.append("eleTrkChisq 0 50")
plots.append("posTrkChisq 0 50")
plots.append("eleTrkT -20 20")
plots.append("posTrkT -20 20")
plots.append("eleTrkZ0 -5 5")
plots.append("posTrkZ0 -5 5")
plots.append("eleTrkD0 -5 5")
plots.append("posTrkD0 -5 5")
plots.append("eleTrkLambda -0.1 0.1")
plots.append("posTrkLambda -0.1 0.1")
plots.append("eleHasL1 0 2")
plots.append("posHasL1 0 2")
plots.append("eleNTrackHits 0 7")
plots.append("posNTrackHits 0 7")
plots.append("eleMatchChisq 0 20")
plots.append("posMatchChisq 0 20")
plots.append("eleTrkExtrpYErrorSensorAxialTopL1 0 2")
plots.append("posTrkExtrpYErrorSensorAxialTopL1 0 2")
plots.append("eleTrkExtrpYErrorSensorStereoTopL1 0 2")
plots.append("posTrkExtrpYErrorSensorStereoTopL1 0 2")
plots.append("eleTrkExtrpYErrorSensorAxialBotL1 0 2")
plots.append("posTrkExtrpYErrorSensorAxialBotL1 0 2")
plots.append("eleTrkExtrpYErrorSensorStereoBotL1 0 2")
plots.append("posTrkExtrpYErrorSensorStereoBotL1 0 2")
plots.append("eleTrkExtrpYSensorAxialTopL1 -25 -10")
plots.append("posTrkExtrpYSensorAxialTopL1 -25 -10")
plots.append("eleTrkExtrpYSensorStereoTopL1 10 25")
plots.append("posTrkExtrpYSensorStereoTopL1 10 25")
plots.append("eleTrkExtrpYSensorAxialBotL1 -25 -10")
plots.append("posTrkExtrpYSensorAxialBotL1 -25 -10")
plots.append("eleTrkExtrpYSensorStereoBotL1 10 25")
plots.append("posTrkExtrpYSensorStereoBotL1 10 25")

if(fullTruth):
	plots.append("eleE 0 1.6")
	plots.append("posE 0 1.6")
	plots.append("elepdgid -25 25")
	plots.append("pospdgid -25 25")
	plots.append("eleparentID -25 650")
	plots.append("posparentID -25 650")
	plots.append("eleNTruthHits 0 13")
	plots.append("posNTruthHits 0 13")
	plots.append("elePurity 0 1.01")
	plots.append("posPurity 0 1.01")
	plots.append("eleHit0ecalhitEnergy 0 1.6")
	plots.append("eleHit0ecalhitEnergy 0 1.6")
	plots.append("eleL1tthetaX -0.01 0.01")
	plots.append("posL1tthetaX -0.01 0.01")
	plots.append("eleL1tthetaY -0.01 0.01")
	plots.append("posL1tthetaY -0.01 0.01")
	plots.append("eleL1tresidualX -0.1 0.1")
	plots.append("posL1tresidualX -0.1 0.1")
	plots.append("eleL1tresidualY -0.1 0.1")
	plots.append("posL1tresidualY -0.1 0.1")
	plots.append("eleL1bthetaX -0.01 0.01")
	plots.append("posL1bthetaX -0.01 0.01")
	plots.append("eleL1bthetaY -0.01 0.01")
	plots.append("posL1bthetaY -0.01 0.01")
	plots.append("eleL1bresidualX -0.1 0.1")
	plots.append("posL1bresidualX -0.1 0.1")
	plots.append("eleL1bresidualY -0.1 0.1")
	plots.append("posL1bresidualY -0.1 0.1")
	plots.append("eleL1tInthetaX -0.01 0.01")
	plots.append("posL1tInthetaX -0.01 0.01")
	plots.append("eleL1tInthetaY -0.01 0.01")
	plots.append("posL1tInthetaY -0.01 0.01")
	plots.append("eleL1tInresidualX -0.1 0.1")
	plots.append("posL1tInresidualX -0.1 0.1")
	plots.append("eleL1tInresidualY -0.1 0.1")
	plots.append("posL1tInresidualY -0.1 0.1")
	plots.append("eleL1bInthetaX -0.01 0.01")
	plots.append("posL1bInthetaX -0.01 0.01")
	plots.append("eleL1bInthetaY -0.01 0.01")
	plots.append("posL1bInthetaY -0.01 0.01")
	plots.append("eleL1bInresidualX -0.1 0.1")
	plots.append("posL1bInresidualX -0.1 0.1")
	plots.append("eleL1bInresidualY -0.1 0.1")
	plots.append("posL1bInresidualY -0.1 0.1")


plots2D = []
plots2D.append("uncM uncVZ 0 0.2 {0} {1}".format(minVZ,maxVZ))
plots2D.append("eleTrkExtrpXAxialTopL1 eleTrkExtrpYAxialTopL1 -40 40 -20 20")
plots2D.append("posTrkExtrpXAxialTopL1 posTrkExtrpYAxialTopL1 -40 40 -20 20")
plots2D.append("eleTrkExtrpXStereoTopL1 eleTrkExtrpYStereoTopL1 -40 40 -20 20")
plots2D.append("posTrkExtrpXStereoTopL1 posTrkExtrpYStereoTopL1 -40 40 -20 20")
plots2D.append("eleTrkExtrpXAxialBotL1 eleTrkExtrpYAxialBotL1 -40 40 -20 20")
plots2D.append("posTrkExtrpXAxialBotL1 posTrkExtrpYAxialBotL1 -40 40 -20 20")
plots2D.append("eleTrkExtrpXStereoBotL1 eleTrkExtrpYStereoBotL1 -40 40 -20 20")
plots2D.append("posTrkExtrpXStereoBotL1 posTrkExtrpYStereoBotL1 -40 40 -20 20")
plots2D.append("eleTrkExtrpXSensorAxialTopL1 eleTrkExtrpYSensorAxialTopL1 -30 30 -30 30")
plots2D.append("posTrkExtrpXSensorAxialTopL1 posTrkExtrpYSensorAxialTopL1 -30 30 -30 30")
plots2D.append("eleTrkExtrpXSensorStereoTopL1 eleTrkExtrpYSensorStereoTopL1 -30 30 -30 30")
plots2D.append("posTrkExtrpXSensorStereoTopL1 posTrkExtrpYSensorStereoTopL1 -30 30 -30 30")
plots2D.append("eleTrkExtrpXSensorAxialBotL1 eleTrkExtrpYSensorAxialBotL1 -30 30 -30 30")
plots2D.append("posTrkExtrpXSensorAxialBotL1 posTrkExtrpYSensorAxialBotL1 -30 30 -30 30")
plots2D.append("eleTrkExtrpXSensorStereoBotL1 eleTrkExtrpYSensorStereoBotL1 -30 30 -30 30")
plots2D.append("posTrkExtrpXSensorStereoBotL1 posTrkExtrpYSensorStereoBotL1 -30 30 -30 30")
plots2D.append("eleTrkEcalX eleTrkEcalY -300 300 -100 100")
plots2D.append("posTrkEcalX posTrkEcalY -300 300 -100 100")

if(fullTruth):
	plots2D.append("eleHit0ecalhitX eleHit0ecalhitY -300 300 -100 100")
	plots2D.append("posHit0ecalhitX posHit0ecalhitY -300 300 -100 100")
	plots2D.append("eleL1tsvthitX eleL1tsvthitY -30 30 -20 20")
	plots2D.append("posL1tsvthitX posL1tsvthitY -30 30 -20 20")
	plots2D.append("eleL1tthetaX eleL1tthetaY -0.01 0.01 -0.01 0.01")
	plots2D.append("posL1tthetaX posL1tthetaY -0.01 0.01 -0.01 0.01")
	plots2D.append("eleL1bsvthitX eleL1bsvthitY -30 30 -20 20")
	plots2D.append("posL1bsvthitX posL1bsvthitY -30 30 -20 20")
	plots2D.append("eleL1bthetaX eleL1bthetaY -0.01 0.01 -0.01 0.01")
	plots2D.append("posL1bthetaX posL1bthetaY -0.01 0.01 -0.01 0.01")

openPDF(outfile,c)

for i in range(len(plots)):
	plot = getPlot(plots[i])
	minX = getMinX(plots[i])
	maxX = getMaxX(plots[i])
	saveTuplePlot(events,plot,nBins,minX,maxX,outfile,c,plot,"",plot)
	saveTuplePlot2D(events,"uncVZ",plot,nBins,minVZ,maxVZ,nBins,minX,maxX,outfile,c,"uncVZ",plot,plot+" vs uncVZ")

for i in range(len(plots2D)):
	plot1 = getPlot(plots2D[i])
	plot2 = getPlot2D(plots2D[i])
	minX = getMinX2D(plots2D[i])
	maxX = getMaxX2D(plots2D[i])
	minY = getMinY(plots2D[i])
	maxY = getMaxY(plots2D[i])
	saveTuplePlot2D(events,plot1,plot2,nBins,minX,maxX,nBins,minY,maxY,outfile,c,plot1,plot2,plot2+" vs "+plot1)

closePDF(outfile,c)