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
	histo.Draw()
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
cuts = ""
#Example list of cuts
#cuts="isPair1&&max(eleMatchChisq,posMatchChisq)<10&&max(abs(eleClT-eleTrkT-{1}),abs(posClT-posTrkT-{1}))<4&&abs(eleClT-posClT)<2&&
    #bscChisq<10&&bscChisq-uncChisq<5&&eleP<{0}*0.75&&uncP<{0}*1.15&&uncP>{0}*0.8&&eleHasL2&&posHasL2".format(energy,trackTDiff)
rootfile = TFile(outfile+".root","recreate")

#List of plots
plots = []
plots.append("uncVZ {0} {1}".format(minVZ,maxVZ))
plots.append("uncVY -1 1")
plots.append("uncVX -3 3")
plots.append("uncM 0 {0}".format(0.1*energy))
plots.append("uncP 0 {0}".format(1.6*energy))
plots.append("uncChisq 0 20")
plots.append("bscChisq 0 20")
plots.append("eleP 0 {0}".format(1.6*energy))
plots.append("posP 0 {0}".format(1.6*energy))
plots.append("eleTrkChisq/(2*eleTrkHits-5) 0 10")
plots.append("posTrkChisq/(2*posTrkHits-5) 0 10")
plots.append("eleClT-eleTrkT-{0} -10 10".format(trackTDiff))
plots.append("posClT-posTrkT-{0} -10 10".format(trackTDiff))
plots.append("eleTrkZ0 -3 3")
plots.append("posTrkZ0 -3 3")
plots.append("eleMatchChisq 0 15")
plots.append("posMatchChisq 0 15")
plots.append("bscChisq-uncChisq 0 15")
plots.append("elePhiKink1 -0.005 0.005")
plots.append("posPhiKink1 -0.005 0.005")
plots.append("elePhiKink2 -0.005 0.005")
plots.append("posPhiKink2 -0.005 0.005")
plots.append("elePhiKink3 -0.005 0.005")
plots.append("posPhiKink3 -0.005 0.005")
plots.append("eleLambdaKink1 -0.01 0.01")
plots.append("posLambdaKink1 -0.01 0.01")
plots.append("eleLambdaKink2 -0.01 0.01")
plots.append("posLambdaKink2 -0.01 0.01")
plots.append("eleLambdaKink3 -0.01 0.01")
plots.append("posLambdaKink3 -0.01 0.01")
plots.append("eleIsoStereo -5 10")
plots.append("posIsoStereo -5 10")
plots.append("eleIsoAxial -5 10")
plots.append("posIsoAxial -5 10")
plots.append("nSVTHits 0 1000")
plots.append("nSVTHitsL1 0 400")
plots.append("nSVTHitsL1b 0 400")
plots.append("nPos 0 10")
plots.append("(eleP-posP)/uncP -1 1")
plots.append("uncTargProjX-{0} -4 4".format(beamX))
plots.append("uncTargProjY-{0} -2 2".format(beamY))
plots.append("(uncTargProjX-{0})/uncTargProjXErr -10 10".format(beamX))
plots.append("(uncTargProjY-{0})/uncTargProjYErr -10 10".format(beamY))
plots.append("(uncVX-{0})/sqrt(uncCovXX) -10 10".format(beamX))
plots.append("(uncVY-{0})/sqrt(uncCovYY) -10 10".format(beamY))
plots.append("(uncVZ-{0})/sqrt(uncCovZZ) -10 10".format(targZ))

#List of 2D plots
plots2D = []
plots2D.append("uncM uncVZ 0 {2} {0} {1}".format(minVZ,maxVZ,0.1*energy))

openPDF(outfile,c)

#Loop over list of plots
for i in range(len(plots)):
	plot = getPlot(plots[i]) #variable to be plotted
	minX = getMinX(plots[i])
	maxX = getMaxX(plots[i])
	saveTuplePlot(events,plot,nBins,minX,maxX,outfile,c,plot,"",plot,nentries,cuts=cuts)
	if(plot2D): saveTuplePlot2D(events,"uncVZ",plot,nBins,minVZ,maxVZ,nBins,minX,maxX,outfile,c,"uncVZ",plot,plot+" vs uncVZ",nentries,cuts=cuts)

#Loop over list of 2D plots
for i in range(len(plots2D)):
	plot1 = getPlot(plots2D[i]) #x axis variable
	plot2 = getPlot2D(plots2D[i]) #y axis variable
	minX = getMinX2D(plots2D[i])
	maxX = getMaxX2D(plots2D[i])
	minY = getMinY(plots2D[i])
	maxY = getMaxY(plots2D[i])
	saveTuplePlot2D(events,plot1,plot2,nBins,minX,maxX,nBins,minY,maxY,outfile,c,plot1,plot2,plot2+" vs "+plot1,nentries,cuts=cuts)

closePDF(outfile,c)

rootfile.Close()