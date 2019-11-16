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
    print '\t-m: minimum uncVZ'
    print '\t-n: maximum uncVZ'
    print '\t-b: number of bins'
    print '\t-e: beam energy'
    print '\t-t: track time diff offset'
    print '\t-x: beam x position'
    print '\t-y: beam y position'
    print '\t-z: target z position'
    print '\t-p: plot 2D plots'
    print '\t-h: this help message'
    print

#Default Values
minVZ = -30
maxVZ = 30
nBins = 100
energy = 2.3
trackTDiff = 43 #only for MC, should be ~55 for data
beamX = -0.224
beamY = -0.080
targZ = -4.3
plot2D = False
nentries = 99999999999999

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'm:n:b:e:t:x:y:z:s:ph')

# Parse the command line arguments
for opt, arg in options:
		if opt=='-m':
			minVZ = float(arg)
		if opt=='-n':
			maxVZ = float(arg)
		if opt=='-b':
			nBins = float(arg)
		if opt=='-e':
			energy = float(arg)
		if opt=='-t':
			trackTDiff = float(arg)
		if opt=='-x':
			beamX = float(arg)
		if opt=='-y':
			beamY = float(arg)
		if opt=='-z':
			targZ = float(arg)
		if opt=='-s':
			nentries = int(arg)
		if opt=='-p':
			plot2D = True
		if opt=='-h':
			print_usage()
			sys.exit(0)

gStyle.SetOptStat(0)
c = TCanvas("c","c",800,600)

#Save plot to pdf and root file
def saveTuplePlot(events,inHisto,nBins,minX,maxX,outfile,canvas,XaxisTitle="",YaxisTitle="",plotTitle="",nentries=0,stats=0,logY=0,cuts=""):
	events.Draw("{0}>>histo({1},{2},{3})".format(inHisto,nBins,minX,maxX),cuts,"",nentries)
	histo = ROOT.gROOT.FindObject("histo")
	histo.SetTitle(plotTitle)
	histo.GetXaxis().SetTitle(XaxisTitle)
	histo.GetYaxis().SetTitle(YaxisTitle)
	histo.SetStats(stats)
	histo.Draw("E")
	canvas.SetLogy(logY)
	canvas.Print(outfile+".pdf")
	histo.Write(plotTitle)
	del histo


#Save 2D plot to pdf and root file
def saveTuplePlot2D(events,inHisto1,inHisto2,nBinsX,minX,maxX,nBinsY,minY,maxY,outfile,canvas,XaxisTitle="",YaxisTitle="",plotTitle="",nentries=0,stats=0,logY=0,cuts=""):
	events.Draw("{0}:{1}>>histo({2},{3},{4},{5},{6},{7})".format(inHisto2,inHisto1,nBinsX,minX,maxX,nBinsY,minY,maxY),cuts,"",nentries)
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

#Grab name of plot
def getPlot(string):
	arr = string.split(" ")
	return arr[0]

#Grab name of 2D plot
def getPlot2D(string):
	arr = string.split(" ")
	if(len(arr) < 2): return ""
	else: return arr[1]

#Get minimum x value
def getMinX(string):
	arr = string.split(" ")
	if(len(arr) < 2): return -9999
	else: return float(arr[1])

#Get maximum x value
def getMaxX(string):
	arr = string.split(" ")
	if(len(arr) < 3): return -9999
	else: return float(arr[2])

#Get minimum x value for 2D plot
def getMinX2D(string):
	arr = string.split(" ")
	if(len(arr) < 3): return -9999
	else: return float(arr[2])

#Get maximum x value for 2D plot
def getMaxX2D(string):
	arr = string.split(" ")
	if(len(arr) < 4): return -9999
	else: return float(arr[3])

#Get minimum y value for 2D plot
def getMinY(string):
	arr = string.split(" ")
	if(len(arr) < 5): return -9999
	else: return float(arr[4])

#Get maximum y value for 2D plot
def getMaxY(string):
	arr = string.split(" ")
	if(len(arr) < 6): return -9999
	else: return float(arr[5])

#Base name of outfile
outfile = remainder[0]

#Create a TChain
#Loop over all files
events = TChain("ntuple")
for i in range(1,len(remainder)):
    events.Add(remainder[i])

#List of cuts
#cuts = "uncVZ<5.7"
cuts = "uncVZ<0.7"
#Example list of cuts
rootfile = TFile(outfile+".root","recreate")

#List of plots
plots = []
plots.append("uncVZ {0} {1}".format(minVZ,maxVZ))
plots.append("uncVY -1 1")
plots.append("uncVX -3 3")
plots.append("uncM 0 {0}".format(0.1*energy))
plots.append("uncPX -0.1 0.1")
plots.append("uncPY -0.1 0.1")
plots.append("uncPZ 0 {0}".format(1.6*energy))
plots.append("uncP 0 {0}".format(1.6*energy))
plots.append("uncChisq 0 20")
plots.append("bscChisq 0 20")
plots.append("eleP 0 {0}".format(1.6*energy))
plots.append("posP 0 {0}".format(1.6*energy))
plots.append("eleTrkChisq/(2*eleTrkHits-5) 0 7")
plots.append("posTrkChisq/(2*posTrkHits-5) 0 7")
plots.append("eleTrkHits 0 10")
plots.append("posTrkHits 0 10")
plots.append("eleClT-eleTrkT-{0} -10 10".format(trackTDiff))
plots.append("posClT-posTrkT-{0} -10 10".format(trackTDiff))
plots.append("eleTrkZ0 -3 3")
plots.append("posTrkZ0 -3 3")
plots.append("eleTrkD0 -3 3")
plots.append("posTrkD0 -3 3")
plots.append("eleTrkLambda -0.1 0.1")
plots.append("posTrkLambda -0.1 0.1")
plots.append("eleTrkPhi -0.1 0.1")
plots.append("posTrkPhi -0.1 0.1")
plots.append("eleMatchChisq 0 15")
plots.append("posMatchChisq 0 15")
plots.append("bscChisq-uncChisq 0 15")
plots.append("nSVTHits 0 1000")
plots.append("nSVTHitsL1 0 400")
plots.append("nSVTHitsL1b 0 400")
plots.append("uncTargProjX-{0} -4 4".format(beamX))
plots.append("uncTargProjY-{0} -2 2".format(beamY))
plots.append("(uncTargProjX-{0})/uncTargProjXErr -10 10".format(beamX))
plots.append("(uncTargProjY-{0})/uncTargProjYErr -10 10".format(beamY))
plots.append("(uncVX-{0})/sqrt(uncCovXX) -10 10".format(beamX))
plots.append("(uncVY-{0})/sqrt(uncCovYY) -10 10".format(beamY))
plots.append("(uncVZ-{0})/sqrt(uncCovZZ) -10 10".format(targZ))

openPDF(outfile,c)

#Loop over list of plots
saveTuplePlot2D(events,"uncM","uncVZ",nBins,0.0,0.1*energy,nBins,minVZ,maxVZ,outfile,c,"uncM","uncVZ","uncVZ vs. uncM",nentries,cuts=cuts)
for i in range(len(plots)):
	plot = getPlot(plots[i]) #variable to be plotted
	minX = getMinX(plots[i])
	maxX = getMaxX(plots[i])
	saveTuplePlot(events,plot,nBins,minX,maxX,outfile,c,plot,"",plot,nentries,cuts=cuts)
	if(plot2D): saveTuplePlot2D(events,"uncVZ",plot,nBins,minVZ,maxVZ,nBins,minX,maxX,outfile,c,"uncVZ",plot,plot+" vs uncVZ",nentries,cuts=cuts)

closePDF(outfile,c)

rootfile.Close()