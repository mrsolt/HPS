#!/usr/bin/env python
import sys
import array, math
import ROOT
from ROOT import gROOT, gStyle, TFile, TTree, TChain, TMVA, TCut, TCanvas, gDirectory, TH1, TGraph, gPad, TF1, TGraphErrors, TLegend, TGaxis, gROOT, TList, TObjArray
import getopt


def print_usage():
    print "\nUsage: {0} <output file basename> <ROOT file> <plot Title>".format(sys.argv[0])
    print "Arguments: "
    print '\t-h: this help message'
    print "Arguments: "
    print '\t-r: plot the ratio'
    print '\t-t: give the graph a new title'
    print "\n"

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'ht:')

# Parse the command line arguments
for opt, arg in options:
	if opt=='-t':
	    useTitle = True
	    plotTitle = str(arg)
        if opt=='-h':
            print_usage()
            sys.exit(0)

if (len(remainder)!=3):
        print_usage()
        sys.exit()

filename = remainder[1]
outname = remainder[0]
plotTitle = remainder[2]
histoTitle = "detectable"

inFile = TFile(filename)

if (inFile.Get(histoTitle) == None):
        print "One of the files does not have a histogram of that name!"
        print_usage()
        sys.exit()


c = TCanvas("c","c",800,600);
c.SetLogx()
c.SetLogy()
c.Update()

XaxisTitle = inFile.Get(histoTitle).GetXaxis().GetTitle();
YaxisTitle = inFile.Get(histoTitle).GetYaxis().GetTitle();

Histo = inFile.Get(histoTitle)

#legend = TLegend(.18,.66,.42,.87)
#legend.SetBorderSize(0)
#legend.SetFillColor(0)
#legend.SetFillStyle(0)
#legend.SetTextFont(42)
#legend.SetTextSize(0.035)
#legend.AddEntry(HistoL0,"L0","LP")
#legend.AddEntry(Histonominal,"Nominal","LP")

palette = array.array('i')
palette.append(1)
palette.append(2)
gStyle.SetPalette(2,palette)

#limitLevelsnominal = array.array('d')
#limitLevelsnominal.append(1.0)
limitLevels = array.array('d')
limitLevels.append(2.3)
#Histonominal.SetContour(1,limitLevelsnominal)
#Histonominal.GetXaxis().SetMoreLogLabels()
#Histonominal.SetTitle("Projected Reach 180 Days L0")
#Histonominal.GetXaxis().SetTitle(XaxisTitle);
#Histonominal.GetYaxis().SetTitle(YaxisTitle);
#Histonominal.GetXaxis().SetRangeUser(0.02,0.08)
#gStyle.SetPalette(55)
#Histonominal.Draw("cont1")

Histo.SetContour(1,limitLevels)
Histo.SetTitle(plotTitle)
Histo.Draw("cont2")
gStyle.SetOptStat(0)

#Histonominal.Draw("CONTLIST")
#contours = TObjArray(gROOT.GetListOfSpecials().FindObject("contours"))
#list = TList(contours.At(1))
#gr1 = list.First()
#gr1.Draw("ACP")

#legend.Draw()
c.Print(outname+".pdf","Title:histoTitle")
