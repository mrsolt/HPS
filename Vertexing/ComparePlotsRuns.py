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
    print '\t-d: make 2D plots'
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

def saveFitPlot(histo,outfile,canvas,XaxisTitle="",YaxisTitle="",plotTitle="",stats=1,logY=0):
	histo.SetTitle(plotTitle)
	histo.GetXaxis().SetTitle(XaxisTitle)
	histo.GetYaxis().SetTitle(YaxisTitle)
	histo.SetStats(stats)
	histo.Fit("gaus")
	fit = histo.GetFunction("gaus")
	histo.Draw()
	canvas.SetLogy(logY)
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

def savehisto(histo,outfile,canvas,XaxisTitle="",YaxisTitle="",plotTitle="",stats=0,logY=0):
	histo.SetTitle(plotTitle)
	histo.GetXaxis().SetTitle(XaxisTitle)
	histo.GetYaxis().SetTitle(YaxisTitle)
	histo.SetTitle(plotTitle)
	histo.SetStats(stats)
	histo.Draw("")
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

infiles[0].cd()
histos = []
for h in infiles[0].GetListOfKeys():
	h = h.ReadObj()
	if(h.ClassName() != "TH1F" and h.ClassName() != "TH1D"): continue
	histos.append(h)

for i in range(len(histos)):
	pdfFileName = outfile+"_"+histos[i].GetTitle()
	openPDF(pdfFileName,c)
	for j in range(len(infiles)):
		histo = infiles[j].Get(histos[i].GetTitle())
		savehisto(histo,pdfFileName,c,histos[i].GetTitle(),"",filenames[j],1)

	closePDF(pdfFileName,c)

fitGaus = []
fitGaus.append("uncVZ")
fitGaus.append("uncVY")
fitGaus.append("uncVX")

gStyle.SetOptFit()

for i in range(len(fitGaus)):
	pdfFileName = outfile+"_"+histos[i].GetTitle()+"_fit"
	plot = getPlot(fitGaus[i])
	openPDF(pdfFileName,c)
	mean = []
	sigma = []
	meanErr = []
	sigmaErr = []
	for j in range(len(infiles)):
		histo = infiles[j].Get(plot)
		params = saveFitPlot(histo,pdfFileName,c,plot,"",filenames[j])
		mean.append(params[0])
		meanErr.append(params[1])
		sigma.append(params[2])
		sigmaErr.append(params[3])
		del params
	saveFitParams(mean,meanErr,pdfFileName,c,"File Number","Fitted Mean [mm]",plot)
	saveFitParams(sigma,sigmaErr,pdfFileName,c,"File Number","Fitted Sigma [mm]",plot)
	del mean
	del sigma
	del meanErr
	del sigmaErr

	closePDF(pdfFileName,c)