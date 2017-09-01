#!/usr/bin/env python
import sys
tmpargv = sys.argv
sys.argv = []
import getopt
import ROOT
from ROOT import gROOT, TFile, TTree, TChain, gDirectory, TLine, gStyle, TCanvas, TLegend, TH1F
sys.argv = tmpargv

def print_usage():
    print "\nUsage: {0} <output pdf file base name> <input wab-beam-tri> <input tritrig-wab-beam file name> <input tritrig file> <input wab file> <norm wab-beam-tri> <norm tritrig-beam-tri> <norm tritrig> <norm wab>".format(sys.argv[0])
    print "Arguments: "
    print '\t-h: this help message'
    print

ebeam=1.056
clusterT = 43.0
targetZ = -5.0
energy = "1pt05"
mass = "40"

gStyle.SetOptStat(0)
c = TCanvas("c","c",800,600);

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'hm:e:')

# Parse the command line arguments
for opt, arg in options:
	if opt=='-m':
	    mass=str(arg)
	if opt=='-e':
	    energy=str(arg)
        if opt=='-h':
            print_usage()
            sys.exit(0)

outfile = str(remainder[0])

wabbeamtri_file = TFile(remainder[1])
tritrigwabbeam_file = TFile(remainder[2])
tritrig_file = TFile(remainder[3])
wab_file = TFile(remainder[4])

wabbeamtri_norm = float(remainder[5])
tritrigwabbeam_norm = float(remainder[6])
tritrig_norm = float(remainder[7])
wab_norm = float(remainder[8])

radcut="uncP>0.8*1.05"
#radcut=""

wabbeamtri_file.Get("ntuple").Draw("eleP+posP>>psum_wabbeamtri(50,0,1.5)",radcut)
psum_wabbeamtri = ROOT.gROOT.FindObject("psum_wabbeamtri")
tritrigwabbeam_file.Get("ntuple").Draw("eleP+posP>>psum_tritrigwabbeam(50,0,1.5)",radcut)
psum_tritrigwabbeam = ROOT.gROOT.FindObject("psum_tritrigwabbeam")
tritrig_file.Get("ntuple").Draw("eleP+posP>>psum_tritrig(50,0,1.5)",radcut)
psum_tritrig = ROOT.gROOT.FindObject("psum_tritrig")
wab_file.Get("ntuple").Draw("eleP+posP>>psum_wab(50,0,1.5)",radcut)
psum_wab = ROOT.gROOT.FindObject("psum_wab")

psum_wabbeamtri.Scale(1/wabbeamtri_norm)
psum_tritrigwabbeam.Scale(1/tritrigwabbeam_norm)
psum_tritrig.Scale(1/tritrig_norm)
psum_wab.Scale(1/wab_norm)

psum_tritrig_wab = TH1F("psum_tritrig_wab","psum_tritrig_wab",50,0,1.5)
for i in range (0,psum_wab.GetNbinsX()):
    psum_tritrig_wab.SetBinContent(i+1,psum_tritrig.GetBinContent(i+1)+psum_wab.GetBinContent(i+1))

legend = TLegend(.18,.66,.42,.87)
legend.SetBorderSize(0)
legend.SetFillColor(0)
legend.SetFillStyle(0)
legend.SetTextFont(42)
legend.SetTextSize(0.035)
legend.AddEntry(psum_wabbeamtri,"wab-beam-tri","LP")
legend.AddEntry(psum_tritrigwabbeam,"tritrig-wab-beam","LP")
legend.AddEntry(psum_tritrig,"tritrig","LP")
legend.AddEntry(psum_wab,"wab","LP")
legend.AddEntry(psum_tritrig_wab,"tritrig + wab","LP")

psum_wabbeamtri.Draw("")
psum_wabbeamtri.SetTitle("P Sum Nominal")
psum_wabbeamtri.GetYaxis().SetRangeUser(0,5000)
psum_tritrigwabbeam.Draw("same")
psum_tritrigwabbeam.SetLineColor(2)
psum_tritrig.Draw("same")
psum_tritrig.SetLineColor(3)
psum_wab.Draw("same")
psum_wab.SetLineColor(4)
psum_tritrig_wab.Draw("same")
psum_tritrig_wab.SetLineColor(6)

legend.Draw("same")
c.Print(outfile+".pdf","Title:plot")


