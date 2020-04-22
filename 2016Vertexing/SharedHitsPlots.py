import sys
tmpargv = sys.argv
sys.argv = []
import numpy as np
import getopt
import ROOT
from ROOT import gROOT, TFile, TTree, TChain, gDirectory, TLine, gStyle, TCanvas, TLegend, TH1F, TF1, TLatex
sys.argv = tmpargv

#List arguments
def print_usage():
    print "\nUsage: {0} <output file base name> <input file> <label>".format(sys.argv[0])
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

def openPDF(outfile,canvas):
	c.Print(outfile+".pdf[")

def closePDF(outfile,canvas):
	c.Print(outfile+".pdf]")

outfile = remainder[0]
outfileroot = TFile(remainder[0]+".root","RECREATE")

events = TChain("ntuple")
for i in range(2,len(remainder)):
    events.Add(remainder[i])

label = ""
label = str(remainder[1])

cut="eleNHitsShared>0.5||posNHitsShared>0.5"
events.Draw("uncVZ>>histo(100,-30,30)")
histo = gDirectory.FindObject("histo")
events.Draw("uncVZ>>histo2(100,-30,30)",cut)
histo2 = gDirectory.FindObject("histo2")

histo.GetXaxis().SetTitle("Reconstructed z (mm)")
histo.SetTitle("Tight Selection Comparing Tracks with Shared Hits {0}".format(label))
histo.Sumw2()
histo2.Sumw2()
histo.Draw("")
histo2.SetLineColor(2)
histo2.Draw("same")

legend = TLegend(.65,.66,.87,.87)
legend.SetBorderSize(0)
legend.SetFillColor(0)
legend.SetFillStyle(0)
legend.SetTextFont(42)
legend.SetTextSize(0.035)
legend.AddEntry(histo,"Tight Cuts","LP")
legend.AddEntry(histo2,"With Shared Hits","LP")
legend.Draw("same")
c.SetLogy(1)

openPDF(outfile,c)

outfileroot.cd()

c.Print(outfile+".pdf")
c.Write()
histo.Write("histo")

print("{0} events. {1} with shared hits. Fraction {2}".format(histo.GetEntries(),histo2.GetEntries(),histo2.GetEntries()/histo.GetEntries()))

closePDF(outfile,c)
outfileroot.Close()