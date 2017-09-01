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
detector = 0

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'hm:d:')

# Parse the command line arguments
for opt, arg in options:
        if opt=='-m':
            mass = arg
        if opt=='-d':
            detector = int(arg)
        if opt=='-h':
            print_usage()
            sys.exit(0)

if (detector == 0): detectorName = "nominal"
if (detector == 1): detectorName = "L0"

filename1 = "/home/mrsolt/hps/L0Studies/" + detectorName + "/1pt05/tails/upperlimit/120_nb_loose.root"
filename2 = "/home/mrsolt/hps/L0Studies/" + detectorName + "/1pt05/tails/upperlimit/4_weeks_loose.root"
filename3 = "/home/mrsolt/hps/L0Studies/" + detectorName + "/1pt05/tails/upperlimit/10_weeks_loose.root"
filename4 = "/home/mrsolt/hps/L0Studies/" + detectorName + "/1pt05/tails/upperlimit/180_days_loose.root"

outname = "zcut_" + detectorName
histoTitle = "zcut"

plotTitle = "Z Cut " + detectorName

inFile1 = TFile(filename1)
inFile2 = TFile(filename2)
inFile3 = TFile(filename3)
inFile4 = TFile(filename4)

c = TCanvas("c","c",800,600);

XaxisTitle = inFile1.Get(histoTitle).GetXaxis().GetTitle();
YaxisTitle = inFile1.Get(histoTitle).GetYaxis().GetTitle();

Histo1 = inFile1.Get(histoTitle)
Histo2 = inFile2.Get(histoTitle)
Histo3 = inFile3.Get(histoTitle)
Histo4 = inFile4.Get(histoTitle)

func1 = inFile1.Get(histoTitle).GetFunction("pol4")
func2 = inFile2.Get(histoTitle).GetFunction("pol4")
func3 = inFile3.Get(histoTitle).GetFunction("pol4")
func4 = inFile4.Get(histoTitle).GetFunction("pol4")


legend = TLegend(.65,.66,.89,.87)
legend.SetBorderSize(0)
legend.SetFillColor(0)
legend.SetFillStyle(0)
legend.SetTextFont(42)
legend.SetTextSize(0.035)
legend.AddEntry(Histo1,"1.7 Days","LP")
legend.AddEntry(Histo2,"4 Weeks","LP")
legend.AddEntry(Histo3,"10 Weeks","LP")
legend.AddEntry(Histo4,"180 Days","LP")


Histo1.Draw("")
Histo1.SetTitle(plotTitle)
#Histo1.GetXaxis().SetRangeUser(-5,150)
Histo1.GetYaxis().SetRangeUser(0,50)
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
Histo4.SetMarkerColor(8)
Histo4.SetLineColor(8)
func4.Draw("same")
func4.SetLineColor(8)

c.Update()
legend.Draw()
c.Print(outname + "_loose.pdf","Title:histoTitle")
