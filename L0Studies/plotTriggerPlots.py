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

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'h')

# Parse the command line arguments
for opt, arg in options:
        if opt=='-h':
            print_usage()
            sys.exit(0)


filename1 = "/home/mrsolt/hps/L0Studies/nominal/1pt05/wab-beam-tri-5mrad/wab-beam-tri-TriggerPlots.root"
filename2 = "/home/mrsolt/hps/L0Studies/L0/1pt05/wab-beam-tri-5mrad/wab-beam-tri-TriggerPlots.root"
outname = "nominal_eff"
histoTitle = "Cluster Position All Particles"

plotTitle = "Cluster Rates"

inFile1 = TFile(filename1)
inFile2 = TFile(filename2)

c = TCanvas("c","c",800,600);


Histo1 = inFile1.Get(histoTitle)
Histo2 = inFile2.Get(histoTitle)

Histo3=inFile2.Get("Energy")
Histo4=inFile1.Get("Energy")
Histo5=inFile2.Get("Energy Fiducial")
Histo6=inFile1.Get("Energy Fiducial")

legend = TLegend(.68,.66,.92,.87)
legend.SetBorderSize(0)
legend.SetFillColor(0)
legend.SetFillStyle(0)
legend.SetTextFont(42)
legend.SetTextSize(0.035)
legend.AddEntry(Histo3,"L0","LP")
legend.AddEntry(Histo4,"Nominal","LP")

Histo1.Scale(0.1)
Histo2.Scale(0.1)

c.Print("TriggerPlots.pdf[","Title:histoTitle")

Histo1.Draw("COLZ")
Histo1.SetTitle(plotTitle + " Nominal")
Histo1.GetXaxis().SetTitle("x [mm]")
Histo1.GetYaxis().SetTitle("y [mm]")
Histo1.SetMaximum(3500)
gStyle.SetOptStat(0)

c.Print("TriggerPlots.pdf","Title:histoTitle")

Histo2.Draw("COLZ")
Histo2.SetTitle(plotTitle + " L0")
Histo2.GetXaxis().SetTitle("x [mm]")
Histo2.GetYaxis().SetTitle("y [mm]")
Histo2.SetMaximum(3500)
gStyle.SetOptStat(0)

c.Print("TriggerPlots.pdf","Title:histoTitle")

Histo3.Draw("")
Histo3.SetTitle("Cluster Energy All")
Histo3.GetXaxis().SetTitle("Energy [GeV]")
Histo3.SetLineColor(2)
Histo4.Draw("same")

legend.Draw()
gStyle.SetOptStat(1)

c.Print("TriggerPlots.pdf","Title:histoTitle")

Histo5.Draw("")
Histo5.SetTitle("Cluster Energy Edge")
Histo5.GetXaxis().SetTitle("Energy [GeV]")
Histo5.SetLineColor(2)
Histo6.Draw("same")

legend.Draw()
gStyle.SetOptStat(1)

c.Print("TriggerPlots.pdf","Title:histoTitle")

c.Print("TriggerPlots.pdf]","Title:histoTitle")
