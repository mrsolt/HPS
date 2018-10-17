import sys
tmpargv = sys.argv
sys.argv = []
import getopt
import ROOT
from ROOT import gROOT, TFile, TTree, TChain, gDirectory, TLine, gStyle, TCanvas, TLegend, TH1F, TF1
sys.argv = tmpargv

#List arguments
def print_usage():
    print "\nUsage: {0} <output file base name> <input A' text file> <input text file name>".format(sys.argv[0])
    print "Arguments: "
    print '\t-z: target z position'
    print '\t-b: mass bin size'
    print '\t-c: z bin size'
    print '\t-d: number of fitted z bins'
    print '\t-s: save fitted histograms'
    print '\t-m: minimum uncVZ'
    print '\t-n: maximum uncVZ'
    print '\t-a: no MC Files'
    print '\t-h: this help message'
    print

zTarg = 0.5
minVZ = -20
maxVZ = 120
massBin = 0.002
nZ = 20
zBin = 5
saveFits = False
doMC = True

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'z:b:c:d:sm:n:ah')

# Parse the command line argumentz
for opt, arg in options:
		if opt=='-z':
			zTarg = float(arg)
		if opt=='-b':
			massBin = float(arg)
		if opt=='-c':
			zBin = float(arg)
		if opt=='-d':
			nZ = float(arg)
		if opt=='-s':
			saveFits = True
		if opt=='-m':
			minVZ = float(arg)
		if opt=='-n':
			maxVZ = float(arg)
		if opt=='-a':
			doMC = False
		if opt=='-h':
			print_usage()
			sys.exit(0)

gStyle.SetOptStat(0)
c = TCanvas("c","c",800,600)

def drawHisto(histo,XaxisTitle="",YaxisTitle="",plotTitle="",stats=0):
	histo.Draw("")
	#histo.GetXaxis().SetRangeUser(-5,150)
	histo.GetYaxis().SetRangeUser(-5,5)
	histo.SetTitle(plotTitle)
	histo.GetXaxis().SetTitle(XaxisTitle)
	histo.GetYaxis().SetTitle(YaxisTitle)
	histo.SetStats(stats)

def saveHisto(histo,outfile,canvas,XaxisTitle="",YaxisTitle="",plotTitle="",stats=0):
	drawHisto(histo,XaxisTitle,YaxisTitle,plotTitle,stats)
	canvas.Print(outfile+".pdf")

def saveTuplePlot(events,inHisto,nBins,minX,maxX,outfile,canvas,XaxisTitle="",YaxisTitle="",plotTitle="",m=0,mRange=9999,stats=0,logY=0):
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


def saveTuplePlot2D(events,inHisto1,inHisto2,nBinsX,minX,maxX,nBinsY,minY,maxY,outfile,canvas,XaxisTitle="",YaxisTitle="",plotTitle="",m=0,mRange=9999,stats=0,logY=0):
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

def fitSlice(events,inHisto1,inHisto2,nBinsX,minX,maxX,nBinsY,minY,maxY,outfile,canvas,z=0,zRange=9999,saveFits=False):
	ex = "Null Fit"
	events.Draw("{0}:{1}>>histo({2},{3},{4},{5},{6},{7})".format(inHisto2,inHisto1,nBinsX,minX,maxX,nBinsY,minY,maxY),"triEndZ>{0}-{1}&&triEndZ<{0}+{1}".format(z,zRange))
	histo = ROOT.gROOT.FindObject("histo")
	histo1D = histo.ProjectionX()
	histo1D.Fit("gaus")
	fit = histo1D.GetFunction("gaus")
	if saveFits:
		canvas.Print(outfile+".pdf")
	fitpar = []
	mean = 0
	meanErr = 0
	sigma = 0
	sigmaErr = 0
	try:
		mean = fit.GetParameter(1)
		meanErr = fit.GetParError(1)
		sigma = fit.GetParameter(2)
		sigmaErr = fit.GetParError(2)
	except Exception as ex:
		print(ex)
	fitpar.append(mean)
	fitpar.append(meanErr)
	fitpar.append(sigma)
	fitpar.append(sigmaErr)
	del histo
	del histo1D
	del fit
	return fitpar

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

apfile = open(remainder[1],"r")
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

events = TChain("ntuple")
if (doMC):
	mcfile = open(remainder[2],"r")
	mcFiles = []

	for line in (raw.strip().split() for raw in mcfile):
		mcFiles.append(line[0])
	for i in range(len(mcFiles)):
		events.Add(mcFiles[i])

plots = []
plots.append("uncVZ {0} {1}".format(minVZ,maxVZ))
plots.append("sqrt(uncCovZZ) 0 10")
plots.append("uncVX {0} {1} -1 1")
plots.append("sqrt(uncCovXX) 0 1")
plots.append("uncVY {0} {1} -1 1")
plots.append("sqrt(uncCovYY) 0 1")
plots.append("uncM 0 0.1")
plots.append("uncMErr 0 0.02")
plots.append("(uncVZ-{0})/sqrt(uncCovZZ) -5 5".format(zTarg))
plots.append("(uncVX)/sqrt(uncCovXX) -5 5")
plots.append("(uncVY)/sqrt(uncCovYY) -5 5")
plots.append("uncP 0 1.5")
plots.append("uncMomErr 0 0.3")
plots.append("uncPX -0.2 0.2")
plots.append("uncMomXErr 0 0.03")
plots.append("uncPY -0.2 0.2")
plots.append("uncMomYErr 0 0.03")
plots.append("uncPZ 0 1.5")
plots.append("uncMomZErr 0 0.3")
plots.append("uncTargProjXErr 0 1")
plots.append("uncTargProjYErr 0 1")
plots.append("uncTargProjX/uncTargProjXErr -5 5")
plots.append("uncTargProjY/uncTargProjYErr -5 5")
plots.append("eleTrkZ0Err 0 1")
plots.append("posTrkZ0Err 0 1")
plots.append("eleTrkD0Err 0 1")
plots.append("posTrkD0Err 0 1")
plots.append("eleTrkZ0/eleTrkZ0Err -5 5")
plots.append("posTrkZ0/posTrkZ0Err -5 5")
plots.append("eleTrkD0/eleTrkD0Err -5 5")
plots.append("posTrkD0/posTrkD0Err -5 5")
plots.append("(-triEle1PY/triEle1PZ*triEndZ-eleTrkZ0)/eleTrkZ0Err -5 5")
plots.append("(-triPosPY/triPosPZ*triEndZ-posTrkZ0)/posTrkZ0Err -5 5")
plots.append("(-triEle1PX/triEle1PZ*triEndZ-eleTrkD0)/eleTrkD0Err -5 5")
plots.append("(-triPosPX/triPosPZ*triEndZ-posTrkD0)/posTrkD0Err -5 5")
plots.append("(triEle1PY/triEle1PZ-eleTrkLambda)/eleTrkLambdaErr -5 5")
plots.append("(triPosPY/triPosPZ-posTrkLambda)/posTrkLambdaErr -5 5")
plots.append("((triEle1PX-0.000075*triEndZ)/triEle1PZ+0.0305-eleTrkPhi)/eleTrkPhiErr -5 5")
plots.append("((triPosPX-0.000075*triEndZ)/triPosPZ+0.0305-posTrkPhi)/posTrkPhiErr -5 5")
plots.append("(0.000075/sqrt(triEle1PX**2+triEle1PZ**2)-eleTrkOmega)/eleTrkOmegaErr -5 5")
plots.append("(0.000075/sqrt(triPosPX**2+triPosPZ**2)+posTrkOmega)/posTrkOmegaErr -5 5")

plots2D = []
plots2D.append("uncM uncVZ 0 0.1 {0} {1}".format(minVZ,maxVZ))
plots2D.append("sqrt(uncCovZZ) uncVZ 0 10 {0} {1}".format(minVZ,maxVZ))
plots2D.append("(uncVZ-{0})/sqrt(uncCovZZ) uncVZ -5 5 {1} {2}".format(zTarg,minVZ,maxVZ))
plots2D.append("uncTargProjXErr uncVZ 0 1 {0} {1}".format(minVZ,maxVZ))
plots2D.append("uncTargProjYErr uncVZ 0 1 {0} {1}".format(minVZ,maxVZ))
plots2D.append("uncTargProjX/uncTargProjXErr uncVZ -5 5 {0} {1}".format(minVZ,maxVZ))
plots2D.append("uncTargProjY/uncTargProjYErr uncVZ -5 5 {0} {1}".format(minVZ,maxVZ))
plots2D.append("eleTrkZ0Err uncVZ 0 1 {0} {1}".format(minVZ,maxVZ))
plots2D.append("posTrkZ0Err uncVZ 0 1 {0} {1}".format(minVZ,maxVZ))
plots2D.append("eleTrkD0Err uncVZ 0 1 {0} {1}".format(minVZ,maxVZ))
plots2D.append("posTrkD0Err uncVZ 0 1 {0} {1}".format(minVZ,maxVZ))
plots2D.append("eleTrkZ0/eleTrkZ0Err uncVZ -5 5 {0} {1}".format(minVZ,maxVZ))
plots2D.append("posTrkZ0/posTrkZ0Err uncVZ -5 5 {0} {1}".format(minVZ,maxVZ))
plots2D.append("eleTrkD0/eleTrkD0Err uncVZ -5 5 {0} {1}".format(minVZ,maxVZ))
plots2D.append("posTrkD0/posTrkD0Err uncVZ -5 5 {0} {1}".format(minVZ,maxVZ))
plots2D.append("(-triEle1PY/triEle1PZ*triEndZ+triEndY-eleTrkZ0)/eleTrkZ0Err uncVZ -5 5 {0} {1}".format(minVZ,maxVZ))
plots2D.append("(-triPosPY/triPosPZ*triEndZ+triEndY-posTrkZ0)/posTrkZ0Err uncVZ -5 5 {0} {1}".format(minVZ,maxVZ))
plots2D.append("(-triEle1PX/triEle1PZ*triEndZ+triEndX-0.000075*triEndZ**2-eleTrkD0)/eleTrkD0Err uncVZ -5 5 {0} {1}".format(minVZ,maxVZ))
plots2D.append("(-triPosPX/triPosPZ*triEndZ+triEndX+0.000075*triEndZ**2-posTrkD0)/posTrkD0Err uncVZ -5 5 {0} {1}".format(minVZ,maxVZ))
plots2D.append("(triEle1PY/triEle1PZ-eleTrkLambda)/eleTrkLambdaErr uncVZ -5 5 {0} {1}".format(minVZ,maxVZ))
plots2D.append("(triPosPY/triPosPZ-posTrkLambda)/posTrkLambdaErr uncVZ -5 5 {0} {1}".format(minVZ,maxVZ))
plots2D.append("((triEle1PX+0.000075*triEndZ)/triEle1PZ+0.0305-eleTrkPhi)/eleTrkPhiErr uncVZ -5 5 {0} {1}".format(minVZ,maxVZ))
plots2D.append("((triPosPX-0.000075*triEndZ)/triPosPZ+0.0305-posTrkPhi)/posTrkPhiErr uncVZ -5 5 {0} {1}".format(minVZ,maxVZ))
plots2D.append("(0.000075/sqrt(triEle1PX**2+triEle1PZ**2)-eleTrkOmega)/eleTrkOmegaErr uncVZ -5 5 {0} {1}".format(minVZ,maxVZ))
plots2D.append("(0.000075/sqrt(triPosPX**2+triPosPZ**2)+posTrkOmega)/posTrkOmegaErr uncVZ -5 5 {0} {1}".format(minVZ,maxVZ))


applots = []
applots.append("(uncVZ-{0})/sqrt(uncCovZZ) -5 50".format(zTarg))
applots.append("(uncVZ-triEndZ)/sqrt(uncCovZZ) -5 5")
applots.append("(uncVX-triEndX)/sqrt(uncCovXX) -5 5")
applots.append("(uncVY-triEndY)/sqrt(uncCovYY) -5 5")
applots.append("(uncM-triM)/uncMErr -5 5")
applots.append("(uncP-triP)/uncMomErr -5 5")
applots.append("(uncPX-triPX)/uncMomXErr -5 5")
applots.append("(uncPY-triPY)/uncMomYErr -5 5")
applots.append("(uncPZ-triPZ)/uncMomZErr -5 5")
applots.append("(uncPZ-triPZ)/(0.000075*(eleTrkOmegaErr/eleTrkOmega^2+posTrkOmegaErr/posTrkOmega^2)) -5 5")
applots.append("(uncPZ-triPZ)/(0.000075*sqrt(((eleTrkOmegaErr/eleTrkOmega^2)^2+(posTrkOmegaErr/posTrkOmega^2)^2)) -5 5")
applots.append("(-triEle1PY/triEle1PZ*triEndZ+triEndY-eleTrkZ0)/eleTrkZ0Err -5 5")
applots.append("(-triPosPY/triPosPZ*triEndZ+triEndY-posTrkZ0)/posTrkZ0Err -5 5")
applots.append("(-triEle1PX/triEle1PZ*triEndZ+triEndX-0.000075*triEndZ**2-eleTrkD0)/eleTrkD0Err -5 5")
applots.append("(-triPosPX/triPosPZ*triEndZ+triEndX+0.000075*triEndZ**2-posTrkD0)/posTrkD0Err -5 5")
applots.append("(triEle1PY/triEle1PZ-eleTrkLambda)/eleTrkLambdaErr -5 5")
applots.append("(triPosPY/triPosPZ-posTrkLambda)/posTrkLambdaErr -5 5")
applots.append("((triEle1PX+0.000075*triEndZ)/triEle1PZ+0.0305-eleTrkPhi)/eleTrkPhiErr -5 5")
applots.append("((triPosPX-0.000075*triEndZ)/triPosPZ+0.0305-posTrkPhi)/posTrkPhiErr -5 5")
applots.append("(0.000075/sqrt(triEle1PX**2+triEle1PZ**2)-eleTrkOmega)/eleTrkOmegaErr -5 5")
applots.append("(0.000075/sqrt(triPosPX**2+triPosPZ**2)+posTrkOmega)/posTrkOmegaErr -5 5")

applots2D = []
applots2D.append("(uncVZ-{0})/sqrt(uncCovZZ) triEndZ -5 50 {1} {2}".format(zTarg,minVZ,maxVZ))
applots2D.append("(uncVZ-triEndZ)/sqrt(uncCovZZ) triEndZ -5 5 {0} {1}".format(minVZ,maxVZ))
applots2D.append("(uncVX-triEndX)/sqrt(uncCovXX) triEndZ -5 5 {0} {1}".format(minVZ,maxVZ))
applots2D.append("(uncVY-triEndY)/sqrt(uncCovYY) triEndZ -5 5 {0} {1}".format(minVZ,maxVZ))
applots2D.append("(uncM-triM)/uncMErr triEndZ -5 5 {0} {1}".format(minVZ,maxVZ))
applots2D.append("(uncP-triP)/uncMomErr triEndZ -5 5 {0} {1}".format(minVZ,maxVZ))
applots2D.append("(uncPX-triPX)/uncMomXErr triEndZ -5 5 {0} {1}".format(minVZ,maxVZ))
applots2D.append("(uncPY-triPY)/uncMomYErr triEndZ -5 5 {0} {1}".format(minVZ,maxVZ))
applots2D.append("(uncPZ-triPZ)/uncMomZErr triEndZ -5 5 {0} {1}".format(minVZ,maxVZ))
applots2D.append("(uncPZ-triPZ)/(0.000075*(eleTrkOmegaErr/eleTrkOmega^2+posTrkOmegaErr/posTrkOmega^2)) -5 5 {0} {1}".format(minVZ,maxVZ))
applots2D.append("(uncPZ-triPZ)/(0.000075*sqrt(((eleTrkOmegaErr/eleTrkOmega^2)^2+(posTrkOmegaErr/posTrkOmega^2)^2)) -5 5 {0} {1}".format(minVZ,maxVZ))
applots2D.append("uncTargProjX/uncTargProjXErr triEndZ -5 5 {0} {1}".format(minVZ,maxVZ))
applots2D.append("uncTargProjY/uncTargProjYErr triEndZ -5 5 {0} {1}".format(minVZ,maxVZ))
applots2D.append("uncTargProjX/((sqrt(uncCovXX)+(sqrt(uncCovZZ)*uncPX/uncPZ)+(uncVZ-0.5)*(uncMomXErr/uncPZ+uncPX*(0.000075*(eleTrkOmegaErr/eleTrkOmega^2+posTrkOmegaErr/posTrkOmega^2))/uncPZ^2))) triEndZ -5 5 {0} {1}".format(minVZ,maxVZ))
applots2D.append("uncTargProjY/((sqrt(uncCovYY)+(sqrt(uncCovZZ)*uncPY/uncPZ)+(uncVZ-0.5)*(uncMomYErr/uncPZ+uncPY*(0.000075*(eleTrkOmegaErr/eleTrkOmega^2+posTrkOmegaErr/posTrkOmega^2))/uncPZ^2))) triEndZ -5 5 {0} {1}".format(minVZ,maxVZ))
applots2D.append("uncTargProjX/((sqrt(uncCovXX)+(sqrt(uncCovZZ)*uncPX/uncPZ)+(uncVZ-0.5)*(uncMomXErr/uncPZ+uncPX*(0.000075*sqrt(((eleTrkOmegaErr/eleTrkOmega^2)^2+(posTrkOmegaErr/posTrkOmega^2)^2))/uncPZ^2))) triEndZ -5 5 {0} {1}".format(minVZ,maxVZ))
applots2D.append("uncTargProjY/((sqrt(uncCovYY)+(sqrt(uncCovZZ)*uncPY/uncPZ)+(uncVZ-0.5)*(uncMomYErr/uncPZ+uncPY*(0.000075*sqrt(((eleTrkOmegaErr/eleTrkOmega^2)^2+(posTrkOmegaErr/posTrkOmega^2)^2))/uncPZ^2))) triEndZ -5 5 {0} {1}".format(minVZ,maxVZ))
applots2D.append("(-triEle1PY/triEle1PZ*triEndZ+triEndY-eleTrkZ0)/eleTrkZ0Err triEndZ -5 5 {0} {1}".format(minVZ,maxVZ))
applots2D.append("(-triPosPY/triPosPZ*triEndZ+triEndY-posTrkZ0)/posTrkZ0Err triEndZ -5 5 {0} {1}".format(minVZ,maxVZ))
applots2D.append("(-triEle1PX/triEle1PZ*triEndZ+triEndX-0.000075*triEndZ**2-eleTrkD0)/eleTrkD0Err triEndZ -5 5 {0} {1}".format(minVZ,maxVZ))
applots2D.append("(-triPosPX/triPosPZ*triEndZ+triEndX+0.000075*triEndZ**2-posTrkD0)/posTrkD0Err triEndZ -5 5 {0} {1}".format(minVZ,maxVZ))
applots2D.append("(triEle1PY/triEle1PZ-eleTrkLambda)/eleTrkLambdaErr triEndZ -5 5 {0} {1}".format(minVZ,maxVZ))
applots2D.append("(triPosPY/triPosPZ-posTrkLambda)/posTrkLambdaErr triEndZ -5 5 {0} {1}".format(minVZ,maxVZ))
applots2D.append("((triEle1PX+0.000075*triEndZ)/triEle1PZ+0.0305-eleTrkPhi)/eleTrkPhiErr triEndZ -5 5 {0} {1}".format(minVZ,maxVZ))
applots2D.append("((triPosPX-0.000075*triEndZ)/triPosPZ+0.0305-posTrkPhi)/posTrkPhiErr triEndZ -5 5 {0} {1}".format(minVZ,maxVZ))
applots2D.append("(0.000075/sqrt(triEle1PX**2+triEle1PZ**2)-eleTrkOmega)/eleTrkOmegaErr triEndZ -5 5 {0} {1}".format(minVZ,maxVZ))
applots2D.append("(0.000075/sqrt(triPosPX**2+triPosPZ**2)+posTrkOmega)/posTrkOmegaErr triEndZ -5 5 {0} {1}".format(minVZ,maxVZ))


fitplots = []
fitplots.append("(uncVZ-triEndZ)/sqrt(uncCovZZ) triEndZ -5 5 {0} {1}".format(minVZ,maxVZ))
fitplots.append("(uncVX-triEndX)/sqrt(uncCovXX) triEndZ -5 5 {0} {1}".format(minVZ,maxVZ))
fitplots.append("(uncVY-triEndY)/sqrt(uncCovYY) triEndZ -5 5 {0} {1}".format(minVZ,maxVZ))
fitplots.append("(uncM-triM)/uncMErr triEndZ -5 5 {0} {1}".format(minVZ,maxVZ))
fitplots.append("(uncP-triP)/uncMomErr triEndZ -5 5 {0} {1}".format(minVZ,maxVZ))
fitplots.append("(uncPX-triPX)/uncMomXErr triEndZ -5 5 {0} {1}".format(minVZ,maxVZ))
fitplots.append("(uncPY-triPY)/uncMomYErr triEndZ -5 5 {0} {1}".format(minVZ,maxVZ))
fitplots.append("(uncPZ-triPZ)/uncMomZErr triEndZ -5 5 {0} {1}".format(minVZ,maxVZ))
fitplots.append("(uncPZ-triPZ)/(0.000075*(eleTrkOmegaErr/eleTrkOmega^2+posTrkOmegaErr/posTrkOmega^2)) -5 5 {0} {1}".format(minVZ,maxVZ))
fitplots.append("(uncPZ-triPZ)/(0.000075*sqrt(((eleTrkOmegaErr/eleTrkOmega^2)^2+(posTrkOmegaErr/posTrkOmega^2)^2)) -5 5 {0} {1}".format(minVZ,maxVZ))
fitplots.append("uncTargProjX/uncTargProjXErr triEndZ -5 5 {0} {1}".format(minVZ,maxVZ))
fitplots.append("uncTargProjY/uncTargProjYErr triEndZ -5 5 {0} {1}".format(minVZ,maxVZ))
fitplots.append("uncTargProjX/((sqrt(uncCovXX)+(sqrt(uncCovZZ)*uncPX/uncPZ)+(uncVZ-0.5)*(uncMomXErr/uncPZ+uncPX*(0.000075*(eleTrkOmegaErr/eleTrkOmega^2+posTrkOmegaErr/posTrkOmega^2)/uncPZ^2))) triEndZ -5 5 {0} {1}".format(minVZ,maxVZ))
fitplots.append("uncTargProjY/((sqrt(uncCovYY)+(sqrt(uncCovZZ)*uncPY/uncPZ)+(uncVZ-0.5)*(uncMomYErr/uncPZ+uncPY*(0.000075*(eleTrkOmegaErr/eleTrkOmega^2+posTrkOmegaErr/posTrkOmega^2)/uncPZ^2))) triEndZ -5 5 {0} {1}".format(minVZ,maxVZ))
fitplots.append("uncTargProjX/((sqrt(uncCovXX)+(sqrt(uncCovZZ)*uncPX/uncPZ)+(uncVZ-0.5)*(uncMomXErr/uncPZ+uncPX*(0.000075*sqrt(((eleTrkOmegaErr/eleTrkOmega^2)^2+(posTrkOmegaErr/posTrkOmega^2)^2)/uncPZ^2)))) triEndZ -5 5 {0} {1}".format(minVZ,maxVZ))
fitplots.append("uncTargProjY/((sqrt(uncCovYY)+(sqrt(uncCovZZ)*uncPY/uncPZ)+(uncVZ-0.5)*(uncMomYErr/uncPZ+uncPY*(0.000075*sqrt(((eleTrkOmegaErr/eleTrkOmega^2)^2+(posTrkOmegaErr/posTrkOmega^2)^2)/uncPZ^2)))) triEndZ -5 5 {0} {1}".format(minVZ,maxVZ))
fitplots.append("(-triEle1PY/triEle1PZ*triEndZ+triEndY-eleTrkZ0)/eleTrkZ0Err triEndZ -5 5 {0} {1}".format(minVZ,maxVZ))
fitplots.append("(-triPosPY/triPosPZ*triEndZ+triEndY-posTrkZ0)/posTrkZ0Err triEndZ -5 5 {0} {1}".format(minVZ,maxVZ))
fitplots.append("(-triEle1PX/triEle1PZ*triEndZ+triEndX-0.000075*triEndZ**2-eleTrkD0)/eleTrkD0Err triEndZ -5 5 {0} {1}".format(minVZ,maxVZ))
fitplots.append("(-triPosPX/triPosPZ*triEndZ+triEndX+0.000075*triEndZ**2-posTrkD0)/posTrkD0Err triEndZ -5 5 {0} {1}".format(minVZ,maxVZ))
fitplots.append("(triEle1PY/triEle1PZ-eleTrkLambda)/eleTrkLambdaErr triEndZ -5 5 {0} {1}".format(minVZ,maxVZ))
fitplots.append("(triPosPY/triPosPZ-posTrkLambda)/posTrkLambdaErr triEndZ -5 5 {0} {1}".format(minVZ,maxVZ))
fitplots.append("((triEle1PX+0.000075*triEndZ)/triEle1PZ+0.0305-eleTrkPhi)/eleTrkPhiErr triEndZ -5 5 {0} {1}".format(minVZ,maxVZ))
fitplots.append("((triPosPX-0.000075*triEndZ)/triPosPZ+0.0305-posTrkPhi)/posTrkPhiErr triEndZ -5 5 {0} {1}".format(minVZ,maxVZ))
fitplots.append("(0.000075/sqrt(triEle1PX**2+triEle1PZ**2)-eleTrkOmega)/eleTrkOmegaErr triEndZ -5 5 {0} {1}".format(minVZ,maxVZ))
fitplots.append("(0.000075/sqrt(triPosPX**2+triPosPZ**2)+posTrkOmega)/posTrkOmegaErr triEndZ -5 5 {0} {1}".format(minVZ,maxVZ))

openPDF(outfile,c)

if(doMC):
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

for i in range(len(applots)):
	plot = getPlot(applots[i])
	minX = getMinX(applots[i])
	maxX = getMaxX(applots[i])
	for j in range(len(masses)):
		mass = masses[j]
		saveTuplePlot(apevents[j],plot,nBins,minX,maxX,outfile,c,plot,"",plot+" A' mass = "+str(mass)+" GeV")

for i in range(len(applots2D)):
	plot1 = getPlot(applots2D[i])
	plot2 = getPlot2D(applots2D[i])
	minX = getMinX2D(applots2D[i])
	maxX = getMaxX2D(applots2D[i])
	minY = getMinY(applots2D[i])
	maxY = getMaxY(applots2D[i])
	for j in range(len(masses)):
		mass = masses[j]
		saveTuplePlot2D(apevents[j],plot1,plot2,nBins,minX,maxX,nBins,minY,maxY,outfile,c,plot1,plot2,plot2+" vs "+plot1+" A' mass = "+str(mass)+" GeV")

for i in range(len(fitplots)):
	plot1 = getPlot(fitplots[i])
	plot2 = getPlot2D(fitplots[i])
	minX = getMinX2D(fitplots[i])
	maxX = getMaxX2D(fitplots[i])
	minY = getMinY(fitplots[i])
	maxY = getMaxY(fitplots[i])
	for j in range(len(masses)):
		mass = masses[j]
		histoMean = TH1F("histoMean","histoMean",nZ,zTarg,maxVZ)
		histoSigma = TH1F("histoSigma","histoSigma",nZ,zTarg,maxVZ)
		for k in range(nZ):
			z = zTarg + (k+0.5) * (maxVZ - zTarg)/float(nZ)
			params = fitSlice(apevents[j],plot1,plot2,nBins,minX,maxX,nBins,minY,maxY,outfile,c,z,zBin,saveFits)
			histoMean.SetBinContent(k+1,params[0])
			histoMean.SetBinError(k+1,params[1])
			histoSigma.SetBinContent(k+1,params[2])
			histoSigma.SetBinError(k+1,params[3])
		saveHisto(histoMean,outfile,c,"z [mm]","Fitted Mean","Fitted Means {0} A' mass {1} GeV".format(plot1,mass))
		saveHisto(histoSigma,outfile,c,"z [mm]","Fitted Sigma","Fitted Sigmas {0} A' mass {1} GeV".format(plot1,mass))
		del histoMean
		del histoSigma

closePDF(outfile,c)