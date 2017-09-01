#!/usr/bin/env python
import sys
import array, math
import ROOT
from ROOT import gROOT, gStyle, TFile, TTree, TChain, TMVA, TCut, TCanvas, gDirectory, TH1, TGraph, gPad, TF1, TGraphErrors, TLegend, TGaxis
import getopt


def print_usage():
    print "\nUsage: {0} <L0 ROOT file> <nominal ROOT file>".format(sys.argv[0])
    print "Arguments: "
    print '\t-h: this help message'
    print "Arguments: "
    print '\t-r: plot the ratio'
    print '\t-t: give the graph a new title'
    print "\n"

plotRatio = False
useTitle = False
options, remainder = getopt.gnu_getopt(sys.argv[1:], 'hrt:e:')

eps2 = 5*10.**-10

# Parse the command line arguments
for opt, arg in options:
        if opt=='-r':
            plotRatio = True
        if opt=='-e':
            eps2 = float(arg)
	if opt=='-t':
	    useTitle = True
	    plotTitle = str(arg)
        if opt=='-h':
            print_usage()
            sys.exit(0)

if (len(remainder)!=2):
        print_usage()
        sys.exit()

filenameL0 = remainder[0]
filenamenominal = remainder[1]

inFileL0 = TFile(filenameL0)
inFilenominal = TFile(filenamenominal)

#limitL0 = inFileL0.Get("limit")
detectableL0 = inFileL0.Get("detectable")
#limitnom = inFilenominal.Get("limit")
detectablenom = inFilenominal.Get("detectable")

n_binsL0X = detectableL0.GetNbinsX()
n_binsnominalX = detectableL0.GetNbinsX()
n_binsL0Y = detectablenom.GetNbinsY()
n_binsnominalY = detectablenom.GetNbinsY()

xArrL0 = array.array('d')
xArrnominal = array.array('d')
yArrL0 = array.array('d')
yArrnominal = array.array('d')

for i in range (0,n_binsL0X):
    xArrL0.append(0.)
    yArrL0.append(0.)

for i in range (0,n_binsnominalX):
    xArrnominal.append(0.)
    yArrnominal.append(0.)

c = TCanvas("c","c",800,600)

diffepsL0 = 100000.
epsbinL0 = 0
diffepsnom = 100000.
epsbinnom = 0

for i in range (0,n_binsL0Y):
    diff = abs(detectableL0.GetYaxis().GetBinCenter(i+1) - eps2)/eps2
    if(diffepsL0 > diff): 
        diffepsL0 = diff
        epsbinL0 = i

for i in range (0,n_binsnominalY):
    diff = abs(detectablenom.GetYaxis().GetBinCenter(i+1) - eps2)/eps2
    if(diffepsnom > diff): 
        diffepsnom = diff
        epsbinnom = i

for i in range (0,n_binsL0X):
    xArrL0[i] = detectableL0.GetXaxis().GetBinCenter(i+1)
    yArrL0[i] = detectableL0.GetBinContent(i+1,epsbinL0+1)

for i in range (0,n_binsnominalX):
    xArrnominal[i] = detectablenom.GetXaxis().GetBinCenter(i+1)
    yArrnominal[i] = detectablenom.GetBinContent(i+1,epsbinnom+1)

graphL0 = TGraph(n_binsL0X,xArrL0,yArrL0)
graphnom = TGraph(n_binsnominalX,xArrnominal,yArrnominal)

legend = TLegend(.18,.66,.42,.87)
legend.SetBorderSize(0)
legend.SetFillColor(0)
legend.SetFillStyle(0)
legend.SetTextFont(42)
legend.SetTextSize(0.035)
legend.AddEntry(graphL0,"L0","LP")
legend.AddEntry(graphnom,"Nominal","LP")

#limitL0.Draw("COLZ")
#limitL0.SetTitle("Limit L0")
#limitL0.GetXaxis().SetTitle("Mass [GeV]")
#limitL0.GetYaxis().SetTitle("Epsilon^2")
#c.SetLogx()
#c.SetLogy()
#c.SetLogz()
#gStyle.SetOptStat(0)
#c.Print("reachL0.pdf","Title:histoTitle")

#limitnom.Draw("COLZ")
#limitnom.SetTitle("Limit Nominal")
#limitnom.GetXaxis().SetTitle("Mass [GeV]")
#limitnom.GetYaxis().SetTitle("Epsilon^2")
#c.SetLogx()
#c.SetLogy()
#c.SetLogz()
#gStyle.SetOptStat(0)
#c.Print("reachnom.pdf","Title:histoTitle")

graphL0.Draw("")
graphL0.SetLineColor(2)
graphL0.SetTitle("Number A's Detectable Epsilson^2 = " + str(eps2))
graphL0.GetXaxis().SetTitle("Mass [GeV]")
graphnom.Draw("same")
graphnom.SetMarkerColor(1)
legend.Draw("same")

c.Print("detectable_" + str(eps2) + ".pdf","Title:histoTitle")
