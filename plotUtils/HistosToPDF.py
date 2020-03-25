import sys
tmpargv = sys.argv
sys.argv = []
import getopt
import ROOT
from ROOT import gROOT, gSystem, TFile, gDirectory, gStyle, TCanvas, TH1
sys.argv = tmpargv

#List arguments
def print_usage():
    print "\nUsage: {0} <output file base name> <input file name>".format(sys.argv[0])
    print "Arguments: "
    print '\t-h: this help message'
    print

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'h')

# Parse the command line arguments
for opt, arg in options:
		if opt=='-h':
			print_usage()
			sys.exit(0)

def openPDF(outfile,canvas):
	c.Print(outfile+".pdf[")

def closePDF(outfile,canvas):
	c.Print(outfile+".pdf]")

def savehisto(histo,outfile,canvas,XaxisTitle="",YaxisTitle="",plotTitle="",stats=0,logY=0,logZ=1):
	histo.SetTitle(plotTitle)
	histo.GetXaxis().SetTitle(XaxisTitle)
	histo.GetYaxis().SetTitle(YaxisTitle)
	#histo.SetStats(stats)
	histo.Draw("COLZ")
	canvas.SetLogy(logY)
	canvas.SetLogz(logZ)
	canvas.Print(outfile+".pdf")
	histo.Write(plotTitle)

#gStyle.SetOptStat(0)
gStyle.SetOptStat(110011)
c = TCanvas("c","c",800,600)

outfile = remainder[0]
infiles = []
for i in range(len(remainder)-1):
	infiles.append(TFile(remainder[i+1]))

infile = infiles[0]
histos = []
infile.cd()
for h in infile.GetListOfKeys():
	h = h.ReadObj()
	if(h.ClassName() != "TH1F" and h.ClassName() != "TH1D" and h.ClassName() != "TH2F" and h.ClassName() != "TH2D"): continue
	histos.append(h)

for i in range(len(infiles)-1):
	file = infiles[i+1]
	file.cd()
	j = 0
	for h in file.GetListOfKeys():
		h = h.ReadObj()
		if(h.ClassName() != "TH1F" and h.ClassName() != "TH1D" and h.ClassName() != "TH2F" and h.ClassName() != "TH2D"): continue
		histos[j].Add(h)
		j = j + 1

gSystem.cd(".")
rootfile = TFile(outfile+".root","recreate")

openPDF(outfile,c)
for i in range(len(histos)):
	savehisto(histos[i],outfile,c,histos[i].GetXaxis().GetTitle(),histos[i].GetYaxis().GetTitle(),histos[i].GetTitle())

closePDF(outfile,c)

rootfile.Close()