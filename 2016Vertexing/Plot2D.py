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
		#fz_10per = TF1("fz_10per","{0}+{1}*x+{2}*x^2+{3}*x^3+{4}*x^4+{5}*x^5".format(-2.308,1227,-29030,285300,-1296000,2229000),0.05,0.150) #L1L1 10%
		#fz_scaled = TF1("fz_scaled","{0}+{1}*x+{2}*x^2+{3}*x^3+{4}*x^4+{5}*x^5".format(1.628,1301,-31950,318900,-1456000,2497000),0.05,0.150) #L1L1 scaled 100%
		#fz_mc = TF1("fz_mc","{0}+{1}*x+{2}*x^2+{3}*x^3+{4}*x^4+{5}*x^5".format(22.23,48.63,-5150,49760,-169900,141700),0.05,0.150) #L1L1 MC
		#fz_10per = TF1("fz_10per","{0}+{1}*x+{2}*x^2+{3}*x^3+{4}*x^4+{5}*x^5".format(-3.413,1360,-3.276e4,3.292e5,-1.535e6,2.733e6),0.05,0.150) #L1L1 10%
		#fz_scaled = TF1("fz_scaled","{0}+{1}*x+{2}*x^2+{3}*x^3+{4}*x^4+{5}*x^5".format(1.809,1373,-3.444e4,3.503e5,-1.633e6,2.886e6),0.05,0.150) #L1L1 scaled 100%
		#fz_mc = TF1("fz_mc","{0}+{1}*x+{2}*x^2+{3}*x^3+{4}*x^4+{5}*x^5".format(19.42,245.1,-9846,1.011e5,-4.354e5,6.71e5),0.05,0.150) #L1L1 MC
		fz_10per = TF1("fz_10per","{0}+{1}*x+{2}*x^2+{3}*x^3+{4}*x^4+{5}*x^5".format(19,53.04,-2566,-4258,2.345e5,-8.994e5),0.05,0.150) #L1L1 10%
		fz_scaled = TF1("fz_scaled","{0}+{1}*x+{2}*x^2+{3}*x^3+{4}*x^4+{5}*x^5".format(26.85,-124.3,593.6,-3.954e4,4.451e5,-1.393e6),0.05,0.150) #L1L1 scaled 100%
		fz_mc = TF1("fz_mc","{0}+{1}*x+{2}*x^2+{3}*x^3+{4}*x^4+{5}*x^5".format(23.55,152.9,-9489,1.091e5,-5.19e5,9.013e5),0.05,0.150) #L1L1 MC
	else:
		#fz_10per = TF1("fz_10per","{0}+{1}*x+{2}*x^2+{3}*x^3+{4}*x^4+{5}*x^5".format(-133,8211,-162000,1480000,-6406000,10560000),0.05,0.150) #L1L2 10%
		#fz_scaled = TF1("fz_scaled","{0}+{1}*x+{2}*x^2+{3}*x^3+{4}*x^4+{5}*x^5".format(-156.8,9720,-191100,1736000,-7433000,12040000),0.05,0.150) #L1L2 scaled 100%
		#fz_mc = TF1("fz_mc","{0}+{1}*x+{2}*x^2+{3}*x^3+{4}*x^4+{5}*x^5".format(25.23,47.14,-2987,12370,0,0),0.05,0.150) #L1L2 MC
		#fz_10per = TF1("fz_10per","{0}+{1}*x+{2}*x^2+{3}*x^3+{4}*x^4+{5}*x^5".format(-162,9927,-2.028e5,1.952e6,-9.05e6,1.627e7),0.05,0.150) #L1L2 10%
		#fz_scaled = TF1("fz_scaled","{0}+{1}*x+{2}*x^2+{3}*x^3+{4}*x^4+{5}*x^5".format(-199.6,1.224e4,-2.501e5,2.411e6,-1.117e7,2.001e7),0.05,0.150) #L1L2 scaled 100%
		#fz_mc = TF1("fz_mc","{0}+{1}*x+{2}*x^2+{3}*x^3+{4}*x^4+{5}*x^5".format(15.5,146.2,5740,-1.857e5,1.49e6,-3.796e6),0.05,0.150) #L1L2 MC
		fz_10per = TF1("fz_10per","{0}+{1}*x+{2}*x^2+{3}*x^3+{4}*x^4+{5}*x^5".format(-164.9,1.012e4,-2.087e5,2.039e6,-9.614e6,1.761e7),0.05,0.150) #L1L2 10%
		fz_scaled = TF1("fz_scaled","{0}+{1}*x+{2}*x^2+{3}*x^3+{4}*x^4+{5}*x^5".format(-205.6,1.258e4,-2.595e5,2.538e6,-1.197e7,2.19e7),0.05,0.150) #L1L2 scaled 100%
		fz_mc = TF1("fz_mc","{0}+{1}*x+{2}*x^2+{3}*x^3+{4}*x^4+{5}*x^5".format(74.12,-2922,7.02e4,-8.567e5,4.936e6,-1.075e7),0.05,0.150) #L1L2 MC

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