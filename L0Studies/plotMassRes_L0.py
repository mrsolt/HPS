#!/usr/bin/env python
import sys
import array, math
import ROOT
from ROOT import gROOT, gStyle, TFile, TTree, TChain, TMVA, TCut, TCanvas, gDirectory, TH1, TH1F, TGraph, gPad, TF1, TGraphErrors, TLegend, TGaxis, TLine
import getopt


def print_usage():
    print "\nUsage:"
    print "Arguments: "
    print '\t-h: this help message'
    print "\n"

mass = 40

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'hm:')

# Parse the command line arguments
for opt, arg in options:
        if opt=='-m':
            mass = arg
        if opt=='-h':
            print_usage()
            sys.exit(0)


filename1 = "/home/mrsolt/hps/L0Studies/L0/1pt05/ap/L0L0/acceptance_data.root"
filename2 = "/home/mrsolt/hps/L0Studies/L0/1pt05/ap/L0L1/acceptance_data.root"
filename3 = "/home/mrsolt/hps/L0Studies/L0/1pt05/ap/L1L1/acceptance_data.root"
filename4 = "/home/mrsolt/hps/L0Studies/L0/1pt05/ap/L1L2/acceptance_data.root"
filename5 = "/home/mrsolt/hps/L0Studies/L0/1pt05/ap/L2L2/acceptance_data.root"
filename6 = "/home/mrsolt/hps/L0Studies/L0/1pt05/ap/L0L2/acceptance_data.root"
outname = "mass_res_L0"
histoTitle = "mres_l1_p0"

plotTitle = "Invariant Mass Resolution"

inFile1 = TFile(filename1)
inFile2 = TFile(filename2)
inFile3 = TFile(filename3)
inFile4 = TFile(filename4)
inFile5 = TFile(filename5)
inFile6 = TFile(filename6)

c = TCanvas("c","c",800,600);

XaxisTitle = inFile1.Get(histoTitle).GetXaxis().GetTitle();
YaxisTitle = inFile1.Get(histoTitle).GetYaxis().GetTitle();

Histo1 = inFile1.Get(histoTitle)
Histo2 = inFile2.Get(histoTitle)
Histo3 = inFile3.Get(histoTitle)
Histo4 = inFile4.Get(histoTitle)
Histo5 = inFile5.Get(histoTitle)
Histo6 = inFile6.Get(histoTitle)

func1 = inFile1.Get(histoTitle).GetFunction("pol1")
func2 = inFile2.Get(histoTitle).GetFunction("pol1")
func3 = inFile3.Get(histoTitle).GetFunction("pol1")
func4 = inFile4.Get(histoTitle).GetFunction("pol1")
func5 = inFile5.Get(histoTitle).GetFunction("pol1")
func6 = inFile6.Get(histoTitle).GetFunction("pol1")


legend = TLegend(.65,.66,.89,.87)
legend.SetBorderSize(0)
legend.SetFillColor(0)
legend.SetFillStyle(0)
legend.SetTextFont(42)
legend.SetTextSize(0.035)
legend.AddEntry(Histo1,"L0L0","LP")
legend.AddEntry(Histo2,"L0L1","LP")
legend.AddEntry(Histo3,"L1L1","LP")
legend.AddEntry(Histo4,"L1L2","LP")
legend.AddEntry(Histo5,"L2L2","LP")
legend.AddEntry(Histo6,"L0L2","LP")


Histo1.Draw("")
Histo1.SetTitle(plotTitle)
#Histo1.GetXaxis().SetRangeUser(-5,150)
Histo1.GetYaxis().SetRangeUser(0,0.008)
Histo1.GetXaxis().SetTitle(XaxisTitle)
Histo1.GetYaxis().SetTitle(YaxisTitle)
func1.Draw("same")
func1.SetLineColor(1)
Histo2.Draw("*same")
Histo2.SetMarkerColor(2)
Histo2.SetLineColor(2)
func2.Draw("same")
func2.SetLineColor(2)
Histo3.Draw("*same")
Histo3.SetMarkerColor(4)
Histo3.SetLineColor(4)
func3.Draw("same")
func3.SetLineColor(4)

Histo4.Draw("*same")
Histo4.SetMarkerColor(3)
Histo4.SetLineColor(3)
func4.Draw("same")
func4.SetLineColor(3)

Histo5.Draw("*same")
Histo5.SetMarkerColor(5)
Histo5.SetLineColor(5)
func5.Draw("same")
func5.SetLineColor(5)

Histo6.Draw("*same")
Histo6.SetMarkerColor(6)
Histo6.SetLineColor(6)
func6.Draw("same")
func6.SetLineColor(6)

c.Update()
legend.Draw()
c.Print(outname + ".pdf","Title:histoTitle")
