import sys, array
tmpargv = sys.argv
sys.argv = []
import random
import numpy as np
import getopt
import ROOT
from ROOT import gROOT, TCanvas, TF1, TFile, gStyle, TFormula, TGraph, TGraphErrors, TH1D, TH1F, TCutG, TH2D, gDirectory, TLegend, TPad, TLatex, TChain
sys.argv = tmpargv

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'hp:', ['help',])

for opt, arg in options:
    if opt in ('-h', '--help'):
        print "\nUsage: "+sys.argv[0]+" <output basename>"
        print "Arguments: "
        print '\t-p: radiative cut (default 0.0)'
        print "\n"
        sys.exit(0)

pcut = 0.0

# Parse the command line arguments
for opt, arg in options:
		if opt=='-p':
			pcut = float(arg)
		if opt=='-h':
			print_usage()
			sys.exit(0)


def saveDataMassHisto(events,nBins,canvas):
	outfileroot.cd()
	massBin = 0.001
	maxMass = 0.2
	massbins = maxMass/massBin
	events.Draw("{0}>>{1}({2},{3},{4})".format("uncM","histo",massbins,0,maxMass))
	histo = ROOT.gROOT.FindObject("histo")
	histo.GetXaxis().SetTitle("Invariant Mass [MeV]")
	histo.GetYaxis().SetTitle("dN/dm [1/MeV]")
	histo.SetTitle("Radiative Selection Invariant Mass Distribution")
	histo.GetXaxis().SetRangeUser(0,0.2)
	histo.Sumw2()
	exppol5=TF1("exppol5","exp(pol5(0))",0.05,0.15)
	histo.Fit("exppol5","QR")
	histo.SetStats(1)
	histo.Draw()
	histo.Write("Data Mass")
	canvas.Print(outfile+".pdf")
	canvas.Write()

def openPDF(outfile,canvas):
	c.Print(outfile+".pdf[")

def closePDF(outfile,canvas):
	c.Print(outfile+".pdf]")

gStyle.SetOptFit(1)
gStyle.SetOptStat(0)
c = TCanvas("c","c",800,600)

cuts = "eleHasL2&&posHasL2&&uncP>{0}".format(pcut)

outfile = remainder[0]
outfileroot = TFile(remainder[0]+".root","RECREATE")

events = TChain("ntuple")
for i in range(1,len(remainder)):
    events.Add(remainder[i])

massBin = 0.001
minMass = 0.0
maxMass = 0.2
nBins = int(maxMass/massBin)

openPDF(outfile,c)

saveDataMassHisto(events,nBins,c)

closePDF(outfile,c)
outfileroot.Close()