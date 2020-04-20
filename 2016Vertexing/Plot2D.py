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
    print '\t-z: plot zcut (default false)'
    print '\t-r: is L1L2 (default false)'
    print '\t-h: this help message'
    print

plotZcut = False
isL1L2 = False

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'zrh')

# Parse the command line arguments
for opt, arg in options:
		if opt=='-z':
			plotZcut = True
		if opt=='-r':
			isL1L2 = True
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

file = TFile(remainder[1])
events = file.Get("ntuple")

label = ""
label = str(remainder[2])

events.Draw("uncVZ:uncM>>histo(100,0,0.2,100,-30,30)")
histo = gDirectory.FindObject("histo")

histo.GetXaxis().SetTitle("Reconstructed e+e- Mass (GeV)")
histo.GetYaxis().SetTitle("Reconstructed z (mm)")
histo.SetTitle("Final Selection {0}".format(label))
histo.Draw("COLZ")
c.SetLogz(1)

openPDF(outfile,c)

outfileroot.cd()

c.Print(outfile+".pdf")
c.Write()
histo.Write("histo")

closePDF(outfile,c)

if(plotZcut):
	outfilezcut = outfile + "_zcut"
	openPDF(outfilezcut,c)

	if(not isL1L2):
		fz_10per = TF1("fz_10per","{0}+{1}*x+{2}*x^2+{3}*x^3+{4}*x^4+{5}*x^5".format(-2.308,1227,-29030,285300,-1296000,2229000),0.05,0.175) #L1L1 10%
		fz_scaled = TF1("fz_scaled","{0}+{1}*x+{2}*x^2+{3}*x^3+{4}*x^4+{5}*x^5".format(1.628,1301,-31950,318900,-1456000,2497000),0.05,0.175) #L1L1 scaled 100%
		fz_mc = TF1("fz_mc","{0}+{1}*x+{2}*x^2+{3}*x^3+{4}*x^4+{5}*x^5".format(3.628,1301,-31950,318900,-1456000,2497000),0.05,0.175) #L1L1 MC
	else:
		fz_10per = TF1("fz_10per","{0}+{1}*x+{2}*x^2+{3}*x^3+{4}*x^4+{5}*x^5".format(-133,8211,-162000,1480000,-6406000,10560000),0.05,0.175) #L1L2 10%
		fz_scaled = TF1("fz_scaled","{0}+{1}*x+{2}*x^2+{3}*x^3+{4}*x^4+{5}*x^5".format(-156.8,9720,-191100,1736000,-7433000,12040000),0.05,0.175) #L1L2 scaled 100%
		fz_mc = TF1("fz_mc","{0}+{1}*x+{2}*x^2+{3}*x^3+{4}*x^4+{5}*x^5".format(-154.8,9720,-191100,1736000,-7433000,12040000),0.05,0.175) #L1L2 MC

	histo.SetStats(0)
	histo.Draw("COLZ")

	fz_10per.SetLineColor(1)
	fz_scaled.SetLineColor(2)
	fz_mc.SetLineColor(4)

	fz_10per.Draw("same")
	fz_scaled.Draw("same")
	fz_mc.Draw("same")

	legend = TLegend(.68,.66,.92,.87)
	legend.SetBorderSize(0)
	legend.SetFillColor(0)
	legend.SetFillStyle(0)
	legend.SetTextFont(42)
	legend.SetTextSize(0.035)
	legend.AddEntry(fz_10per,"10% Data","LP")
	legend.AddEntry(fz_scaled,"Scaled Data","LP")
	legend.AddEntry(fz_mc,"MC","LP")
	legend.Draw("same")

	c.Print(outfilezcut+".pdf")
	c.Write()

	closePDF(outfilezcut,c)

outfileroot.Close()