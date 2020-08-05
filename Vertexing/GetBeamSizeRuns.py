import sys
tmpargv = sys.argv
sys.argv = []
import getopt
from array import array
import ROOT
from ROOT import gROOT, TFile, TTree, TChain, gDirectory, TLine, gStyle, TCanvas, TLegend, TH1F, TF1
sys.argv = tmpargv

#List arguments
def print_usage():
    print "\nUsage: {0} <output file base name> <input text file name>".format(sys.argv[0])
    print "Arguments: "
    print '\t-h: this help message'
    print

useSingleGaus = True

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'h')

# Parse the command line arguments
for opt, arg in options:
		if opt=='-h':
			print_usage()
			sys.exit(0)

gStyle.SetOptStat(0)
c = TCanvas("c","c",800,600)

def saveFitPlot(events,plot,outfile,canvas,nBins,minX,maxX,XaxisTitle="",YaxisTitle="",plotTitle="",useSingleGaus=True,stats=1,logY=0):
	events.Draw("{0}>>histo({1},{2},{3})".format(plot,nBins,minX,maxX))
	histo = ROOT.gROOT.FindObject("histo")
	histo.SetTitle(plotTitle)
	histo.GetXaxis().SetTitle(XaxisTitle)
	histo.GetYaxis().SetTitle(YaxisTitle)
	histo.SetStats(stats)
	mean1 = histo.GetMean()
	sigma1 = histo.GetRMS()
	histo.Fit("gaus","","",mean1 - 1.5*sigma1,mean1+1.5*sigma1)
	fit = histo.GetFunction("gaus")
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

	histo.Draw()
	canvas.SetLogy(logY)
	canvas.Print(outfile+".pdf")
	fitpar = []
	fitpar.append(mean)
	fitpar.append(meanErr)
	fitpar.append(sigma)
	fitpar.append(sigmaErr)
	del histo
	del fit
	return fitpar

def saveFitParams(array,arrayErr,outfile,canvas,XaxisTitle="",YaxisTitle="",plotTitle=""):
	histo = TH1F("histo","histo",len(array),0,len(array)+1)
	for i in range(len(array)):
		histo.Fill(i+1,array[i])
		histo.SetBinError(i+1,arrayErr[i])
	histo.SetTitle(plotTitle)
	histo.GetXaxis().SetTitle(XaxisTitle)
	histo.GetYaxis().SetTitle(YaxisTitle)
	histo.Draw()
	canvas.Print(outfile+".pdf")
	del histo

def openPDF(outfile,canvas):
	c.Print(outfile+".pdf[")

def closePDF(outfile,canvas):
	c.Print(outfile+".pdf]")

def getPlot(string):
	arr = string.split(" ")
	return arr[0]

def getMinX(string):
	arr = string.split(" ")
	if(len(arr) < 2): return -9999
	else: return float(arr[1])

def getMaxX(string):
	arr = string.split(" ")
	if(len(arr) < 3): return -9999
	else: return float(arr[2])

outfile = remainder[0]

events = TChain("ntuple")
for i in range(1,len(remainder)):
    events.Add(remainder[i])

outfile = remainder[0]
infile = open(remainder[1],"r")
infiles = []
filenames = []

for line in (raw.strip().split() for raw in infile):
	filenames.append(line[0])
	infiles.append(TFile(line[0]))

fitGaus = []
fitGaus.append("uncVX -2 2")
fitGaus.append("uncVY -1 1")
fitGaus.append("uncVZ -35 25")
fitGaus.append("bscVX -2 2")
fitGaus.append("bscVY -1 1")
fitGaus.append("bscVZ -35 25")

nBins = 100
beamX = []
beamY = []
beamZ = []
Run = []

gStyle.SetOptFit()

for i in range(len(fitGaus)):
	plot = getPlot(fitGaus[i])
	minX = getMinX(fitGaus[i])
	maxX = getMaxX(fitGaus[i])
	pdfFileName = outfile+"_"+plot+"_fit"
	openPDF(pdfFileName,c)
	mean = []
	sigma = []
	meanErr = []
	sigmaErr = []
	for j in range(len(infiles)):
		event = infiles[j].Get("ntuple")
		run = array('d',[0])
		event.Branch("run",run,"run")
		event.GetEntry(0)
		params = saveFitPlot(event,plot,pdfFileName,c,nBins,minX,maxX,plot,"","Run " + str(event.run),useSingleGaus)
		mean.append(params[0])
		meanErr.append(params[1])
		sigma.append(params[2])
		sigmaErr.append(params[3])
		if(i == 0):
			Run.append(str(event.run))
		del params
	saveFitParams(mean,meanErr,pdfFileName,c,"Run Number","Fitted Mean [mm]",plot)
	saveFitParams(sigma,sigmaErr,pdfFileName,c,"Run Number","Fitted Sigma [mm]",plot)
	if(plot == "uncVX"): 
		beamX = mean
	if(plot == "uncVY"):
		beamY = mean
	if(plot == "uncVZ"):
		beamZ = mean
	del mean
	del sigma
	del meanErr
	del sigmaErr
	closePDF(pdfFileName,c)

textFileName = outfile+"_params.txt"
textFile = open(textFileName,"w")
for i in range(len(infiles)):
	textFile.write(Run[i] + " " + str(beamX[i]) + " " + str(beamY[i]) + " " + str(beamZ[i]) + "\n")
	if(Run[i] == "7782"):
		textFile.write("7783 " + str(beamX[i]) + " " + str(beamY[i]) + " " + str(beamZ[i]) + "\n")

textFile.close()