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

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'h')

# Parse the command line arguments
for opt, arg in options:
		if opt=='-h':
			print_usage()
			sys.exit(0)

gStyle.SetOptStat(0)
c = TCanvas("c","c",800,600)

f1 = TF1("double_gaus", "gaus(0) + gaus(3)");
f1.SetParNames("Constant 1", "Mean 1", "Sigma 1",
               "Constant 2", "Mean 2", "Sigma 2");

def saveFitPlot(events,plot,outfile,canvas,nBins,minX,maxX,XaxisTitle="",YaxisTitle="",plotTitle="",stats=1,logY=0):
	events.Draw("{0}>>histo({1},{2},{3})".format(plot,nBins,minX,maxX))
	histo = ROOT.gROOT.FindObject("histo")
	histo.SetTitle(plotTitle)
	histo.GetXaxis().SetTitle(XaxisTitle)
	histo.GetYaxis().SetTitle(YaxisTitle)
	histo.SetStats(stats)
	histo.Fit("gaus")
	fit_gaus = histo.GetFunction("gaus")
	f1.SetParameters(fit_gaus.GetParameter(0),fit_gaus.GetParameter(1),fit_gaus.GetParameter(2),fit_gaus.GetParameter(0)/10.,fit_gaus.GetParameter(1),fit_gaus.GetParameter(2)*10)
	f1.SetParLimits(3,0,fit_gaus.GetParameter(0)/4.)
	f1.SetParLimits(4,-fit_gaus.GetParameter(1)-2*fit_gaus.GetParameter(2),fit_gaus.GetParameter(1)+2*fit_gaus.GetParameter(2))
	f1.SetParLimits(5,fit_gaus.GetParameter(2)/4.,9999)
	histo.Fit("double_gaus")
	fit = histo.GetFunction("double_gaus")
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
	fit_gaus1 = TF1("gaus","gaus",-100,100)
	fit_gaus2 = TF1("gaus","gaus",-100,100)
	fit_gaus1.SetParameters(fit.GetParameter(0),fit.GetParameter(1),fit.GetParameter(2))
	fit_gaus2.SetParameters(fit.GetParameter(3),fit.GetParameter(4),fit.GetParameter(5))
	fit.SetLineColor(1)
	histo.Draw()
	fit_gaus1.SetLineColor(2)
	fit_gaus1.SetLineColor(4)
	fit_gaus1.Draw("same")
	fit_gaus2.Draw("same")
	canvas.SetLogy(logY)
	canvas.Print(outfile+".pdf")
	fitpar = []
	fitpar.append(mean)
	fitpar.append(meanErr)
	fitpar.append(sigma)
	fitpar.append(sigmaErr)
	del histo
	del fit
	del fit_gaus
	del fit_gaus1
	del fit_gaus2
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

#infiles[0].cd()

fitGaus = []
fitGaus.append("uncVX -2 2")
fitGaus.append("uncVY -1 1")
fitGaus.append("uncVZ -35 25")

nBins = 100
beamX = []
beamY = []
Run = []

gStyle.SetOptFit()

for i in range(len(fitGaus)):
	plot = getPlot(fitGaus[i])
	minX = getMinX(fitGaus[i])
	maxX = getMaxX(fitGaus[i])
	pdfFileName = outfile+"_"+plot+"_fit"
	#textFileName = outfile+"_"+plot+"_params.txt"
	openPDF(pdfFileName,c)
	#textFile = open(textFileName,"w")
	mean = []
	sigma = []
	meanErr = []
	sigmaErr = []
	for j in range(len(infiles)):
		event = infiles[j].Get("ntuple")
		run = array('d',[0])
		event.Branch("run",run,"run")
		event.GetEntry(0)
		params = saveFitPlot(event,plot,pdfFileName,c,nBins,minX,maxX,plot,"","Run " + str(event.run))
		mean.append(params[0])
		meanErr.append(params[1])
		sigma.append(params[2])
		sigmaErr.append(params[3])
		#textFile.write(str(event.run) + " " + str(params[0]) + "\n")
		if(i == 0):
			Run.append(str(event.run))
		del params
	saveFitParams(mean,meanErr,pdfFileName,c,"Run Number","Fitted Mean [mm]",plot)
	saveFitParams(sigma,sigmaErr,pdfFileName,c,"Run Number","Fitted Sigma [mm]",plot)
	if(plot == "uncVX"): 
		beamX = mean
	if(plot == "uncVY"):
		beamY = mean
	del mean
	del sigma
	del meanErr
	del sigmaErr

	closePDF(pdfFileName,c)
	#textFile.close()

textFileName = outfile+"_params.txt"
textFile = open(textFileName,"w")
for i in range(len(infiles)):
	textFile.write(Run[i] + " " + str(beamX[0]) + " " + str(beamY[0]) + "\n")

textFile.close()