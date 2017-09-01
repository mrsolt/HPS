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

#filename1 = "/home/mrsolt/hps/Layer0Studies/Res/tails_nominal.root"
#filename2 = "/home/mrsolt/hps/Layer0Studies/Res/tails_L0.root"

#filename1 = "/home/mrsolt/hps/L0Studies/nominal/4pt4/tails/Vres.root"
#filename2 = "/home/mrsolt/hps/L0Studies/L0/4pt4/tails/Vres.root"

filename1 = "/home/mrsolt/hps/L0Studies/nominal/6pt6/tails/Vres.root"
filename2 = "/home/mrsolt/hps/L0Studies/L0/6pt6/tails/Vres.root"
outname = "nominal_eff"
histoTitle = "res"

exppol4=TF1("exppol4","exp(pol4(0))",-5,100)

plotTitle = "Vertex Resolution"

inFile1 = TFile(filename1)
inFile2 = TFile(filename2)

c = TCanvas("c","c",800,600);

XaxisTitle = inFile1.Get(histoTitle).GetXaxis().GetTitle();
YaxisTitle = inFile1.Get(histoTitle).GetYaxis().GetTitle();

Histo1 = inFile1.Get(histoTitle)
Histo2 = inFile2.Get(histoTitle)

func1 = inFile1.Get(histoTitle).GetFunction("pol3")
func2 = inFile2.Get(histoTitle).GetFunction("pol3")


legend = TLegend(.65,.66,.89,.87)
legend.SetBorderSize(0)
legend.SetFillColor(0)
legend.SetFillStyle(0)
legend.SetTextFont(42)
legend.SetTextSize(0.035)
legend.AddEntry(Histo1,"Nominal Detector","LP")
legend.AddEntry(Histo2,"L0 Detector","LP")


Histo1.Draw("")
Histo1.SetTitle(plotTitle)
#Histo1.GetXaxis().SetRangeUser(-5,150)
Histo1.GetYaxis().SetRangeUser(0,2)
Histo1.GetXaxis().SetTitle(XaxisTitle)
Histo1.GetYaxis().SetTitle(YaxisTitle)
func1.Draw("same")
func1.SetLineColor(1)
Histo2.Draw("*same")
Histo2.SetLineColor(2)
func2.Draw("same")
func2.SetLineColor(2)


c.Update()

legend.Draw()
c.Print("VZ_Resolution.pdf","Title:histoTitle")
