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
    print '\t-h: this help message'
    print

zTarg = 0.5
minVZ = -20
maxVZ = 80
massBin = 0.002
nZ = 20
zBin = 5
saveFits = False

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'z:b:c:d:sm:n:h')

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
		if opt=='-h':
			print_usage()
			sys.exit(0)

gStyle.SetOptStat(0)
c = TCanvas("c","c",800,600)

def drawHisto(histo,XaxisTitle="",YaxisTitle="",plotTitle="",stats=0):
	histo.Draw("")
	#histo.GetXaxis().SetRangeUser(-5,150)
	histo.GetYaxis().SetRangeUser(-2,2)
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

applots2D = []
applots2D.append("(uncVZ-triEndZ)/sqrt(uncCovZZ) triEndZ -5 5 {0} {1}".format(minVZ,maxVZ))
applots2D.append("(uncVX-triEndX)/sqrt(uncCovXX) triEndZ -5 5 {0} {1}".format(minVZ,maxVZ))
applots2D.append("(uncVY-triEndY)/sqrt(uncCovYY) triEndZ -5 5 {0} {1}".format(minVZ,maxVZ))
applots2D.append("(uncM-triM)/uncMErr triEndZ -5 5 {0} {1}".format(minVZ,maxVZ))
applots2D.append("(uncP-triP)/uncMomErr triEndZ -5 5 {0} {1}".format(minVZ,maxVZ))
applots2D.append("(uncPX-triPX)/uncMomXErr triEndZ -5 5 {0} {1}".format(minVZ,maxVZ))
applots2D.append("(uncPY-triPY)/uncMomYErr triEndZ -5 5 {0} {1}".format(minVZ,maxVZ))
applots2D.append("(uncPZ-triPZ)/uncMomZErr triEndZ -5 5 {0} {1}".format(minVZ,maxVZ))
applots2D.append("(uncTargProjX-triStartX)/uncTargProjXErr triEndZ -5 5 {0} {1}".format(minVZ,maxVZ))
applots2D.append("(uncTargProjY-triStartY)/uncTargProjYErr triEndZ -5 5 {0} {1}".format(minVZ,maxVZ))

fitplots = []
fitplots.append("(uncVZ-triEndZ)/sqrt(uncCovZZ) triEndZ -5 5 {0} {1}".format(minVZ,maxVZ))
fitplots.append("(uncVX-triEndX)/sqrt(uncCovXX) triEndZ -5 5 {0} {1}".format(minVZ,maxVZ))
fitplots.append("(uncVY-triEndY)/sqrt(uncCovYY) triEndZ -5 5 {0} {1}".format(minVZ,maxVZ))
fitplots.append("(uncM-triM)/uncMErr triEndZ -5 5 {0} {1}".format(minVZ,maxVZ))
fitplots.append("(uncP-triP)/uncMomErr triEndZ -5 5 {0} {1}".format(minVZ,maxVZ))
fitplots.append("(uncPX-triPX)/uncMomXErr triEndZ -5 5 {0} {1}".format(minVZ,maxVZ))
fitplots.append("(uncPY-triPY)/uncMomYErr triEndZ -5 5 {0} {1}".format(minVZ,maxVZ))
fitplots.append("(uncPZ-triPZ)/uncMomZErr triEndZ -5 5 {0} {1}".format(minVZ,maxVZ))
fitplots.append("(uncTargProjX-triStartX)/uncTargProjXErr triEndZ -5 5 {0} {1}".format(minVZ,maxVZ))
fitplots.append("(uncTargProjY-triStartY)/uncTargProjYErr triEndZ -5 5 {0} {1}".format(minVZ,maxVZ))
openPDF(outfile,c)

for i in range(len(applots2D)):
	plot1 = getPlot(applots2D[i])
	plot2 = getPlot2D(applots2D[i])
	minX = getMinX2D(applots2D[i])
	maxX = getMaxX2D(applots2D[i])
	minY = getMinY(applots2D[i])
	maxY = getMaxY(applots2D[i])
	for j in range(len(masses)):
		mass = masses[j]
		saveTuplePlot2D(apevents[j],plot1,plot2,nBins,minX,maxX,nBins,minY,maxY,outfile,c,plot1,plot2,plot2+" vs {0} A' mass = {1:.2f} GeV".format(plot1,mass))

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
		saveHisto(histoMean,outfile,c,"z [mm]","Fitted Mean","Fitted Means {0} A' mass {1:.2f} GeV".format(plot1,mass))
		saveHisto(histoSigma,outfile,c,"z [mm]","Fitted Sigma","Fitted Sigmas {0} A' mass {1:.2f} GeV".format(plot1,mass))
		del histoMean
		del histoSigma

closePDF(outfile,c)