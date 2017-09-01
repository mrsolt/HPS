#!/usr/bin/env python
import sys
import array, math
import ROOT
from ROOT import gROOT, gStyle, TFile, TTree, TChain, TMVA, TCut, TCanvas, gDirectory, TH1, TGraph, gPad, TF1, TGraphErrors, TLegend, TGaxis, gROOT, TList, TObjArray
import getopt


def print_usage():
    print "\nUsage: {0} <output file basename> <L0 ROOT file> <nominal ROOT file> <Graph Name>".format(sys.argv[0])
    print "Arguments: "
    print '\t-h: this help message'
    print "Arguments: "
    print '\t-r: plot the ratio'
    print '\t-t: give the graph a new title'
    print "\n"

plotRatio = False
useTitle = False
options, remainder = getopt.gnu_getopt(sys.argv[1:], 'hrt:')

# Parse the command line arguments
for opt, arg in options:
        if opt=='-r':
            plotRatio = True
	if opt=='-t':
	    useTitle = True
	    plotTitle = str(arg)
        if opt=='-h':
            print_usage()
            sys.exit(0)

if (len(remainder)!=4):
        print_usage()
        sys.exit()

filenameL0 = remainder[1]
filenamenominal = remainder[2]
outname = remainder[0]
histoTitle = remainder[3]

if(useTitle is False): plotTitle = histoTitle

inFileL0 = TFile(filenameL0)
inFilenominal = TFile(filenamenominal)

if (inFileL0.Get(histoTitle) == None or inFilenominal.Get(histoTitle) == None):
        print "One of the files does not have a histogram of that name!"
        print_usage()
        sys.exit()


c = TCanvas("c","c",800,600);
c.SetLogx()
c.SetLogy()
c.Update()

XaxisTitle = inFileL0.Get(histoTitle).GetXaxis().GetTitle();
YaxisTitle = inFileL0.Get(histoTitle).GetYaxis().GetTitle();

HistoL0 = inFileL0.Get(histoTitle)
Histonominal = inFilenominal.Get(histoTitle)

legend = TLegend(.18,.66,.42,.87)
legend.SetBorderSize(0)
legend.SetFillColor(0)
legend.SetFillStyle(0)
legend.SetTextFont(42)
legend.SetTextSize(0.035)
legend.AddEntry(HistoL0,"L0","LP")
legend.AddEntry(Histonominal,"Nominal","LP")

palette = array.array('i')
palette.append(1)
palette.append(2)
gStyle.SetPalette(2,palette)

limitLevelsnominal = array.array('d')
limitLevelsnominal.append(1.0)
limitLevelsL0 = array.array('d')
limitLevelsL0.append(1.0)
#Histonominal.SetContour(1,limitLevelsnominal)
#Histonominal.GetXaxis().SetMoreLogLabels()
#Histonominal.SetTitle("Projected Reach 180 Days L0")
#Histonominal.GetXaxis().SetTitle(XaxisTitle);
#Histonominal.GetYaxis().SetTitle(YaxisTitle);
#Histonominal.GetXaxis().SetRangeUser(0.02,0.08)
#gStyle.SetPalette(55)
Histonominal.Draw("cont1")

HistoL0.Scale(1.0)
HistoL0.SetContour(1,limitLevelsL0)
HistoL0.SetTitle("Projected Reach 10 Weeks Nominal Data Scaled")
HistoL0.Draw("cont2")
HistoL0.Draw("cont2 same")
gStyle.SetOptStat(0)

#Histonominal.Draw("CONTLIST")
#contours = TObjArray(gROOT.GetListOfSpecials().FindObject("contours"))
#list = TList(contours.At(1))
#gr1 = list.First()
#gr1.Draw("ACP")

#legend.Draw()
c.Print(outname+"_loose.pdf","Title:histoTitle")
