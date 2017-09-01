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


filename1 = "/home/mrsolt/hps/Layer0Studies/Nominal/ap/L1L1/acceptance_"+str(mass)+".root"
filename2 = "/home/mrsolt/hps/Layer0Studies/Nominal/ap/L1L2/acceptance_"+str(mass)+".root"
filename3 = "/home/mrsolt/hps/Layer0Studies/Nominal/ap/L2L2/acceptance_"+str(mass)+".root"
outname = "nominal_eff"
histoTitle = "eff_all"

exppol4=TF1("exppol4","exp(pol4(0))",-5,100)

if (int(mass) > 59 and int(mass < 71)):
    filename2_nom = "/home/mrsolt/hps/Layer0Studies/Nominal/ap/100mm/L1L2/acceptance_"+str(mass)+".root"

plotTitle = str(mass) + " MeV Nominal Efficiency"

inFile1 = TFile(filename1)
inFile2 = TFile(filename2)
inFile3 = TFile(filename3)

zFile1 = TFile("/home/mrsolt/hps/Vertexing/nominal/1pt05/ap/upperlimit/golden_massbin.root")
zFile2 = TFile("/home/mrsolt/hps/Vertexing/nominal/1pt05/ap/L1L2/golden.root")
zFile3 = TFile("/home/mrsolt/hps/Vertexing/nominal/1pt05/ap/L2L2/golden.root")

c = TCanvas("c","c",800,600);

XaxisTitle = inFile1.Get(histoTitle).GetXaxis().GetTitle();
YaxisTitle = inFile1.Get(histoTitle).GetYaxis().GetTitle();

Histo1 = inFile1.Get(histoTitle)
Histo2 = inFile2.Get(histoTitle)
Histo3 = inFile3.Get(histoTitle)

func1 = inFile1.Get(histoTitle).GetFunction("exppol4")
func2 = inFile2.Get(histoTitle).GetFunction("exppol4")
func3 = inFile3.Get(histoTitle).GetFunction("gaus")


legend = TLegend(.68,.66,.92,.87)
legend.SetBorderSize(0)
legend.SetFillColor(0)
legend.SetFillStyle(0)
legend.SetTextFont(42)
legend.SetTextSize(0.035)
legend.AddEntry(Histo1,"L1L1","LP")
legend.AddEntry(Histo2,"L1L2","LP")
legend.AddEntry(Histo3,"L2L2","LP")

xArr1 = array.array('d')
yArr1 = array.array('d')
yArr2 = array.array('d')
yArr3 = array.array('d')

xArrdum = ROOT.Double(0)
yArrdum = ROOT.Double(0)

n_bins = zFile1.Get("zcut").GetN()

for i in range (0,n_bins):
    xArr1.append(0.)
    yArr1.append(0.)
    yArr2.append(0.)
    yArr3.append(0.)

for i in range(0,n_bins):
    zFile1.Get("zcut").GetPoint(i,xArrdum,yArrdum)
    xArr1[i] = xArrdum
    yArr1[i] = yArrdum
    zFile2.Get("zcut").GetPoint(i,xArrdum,yArrdum)
    yArr2[i] = yArrdum
    zFile3.Get("zcut").GetPoint(i,xArrdum,yArrdum)
    yArr3[i] = yArrdum

mass_index = 0

for i in range(0,n_bins):
    if(xArr1[i] < float(mass)/1000.): continue
    else:
        mass_index = i
        break

zcut1 = yArr1[mass_index]
zcut2 = yArr2[mass_index]
zcut3 = yArr3[mass_index]

print mass_index
print zcut1
print zcut2
print zcut3

line1 = TLine(zcut1,0,zcut1,0.15)
line2 = TLine(zcut2,0,zcut2,0.15)
line3 = TLine(zcut3,0,zcut3,0.15)

histodumb = TH1F("histodumb","",100,-5,150)
histodumb.Fill(149,0.0001)

gStyle.SetOptStat(0)
histodumb.Draw("")
histodumb.GetXaxis().SetRangeUser(-5,150)
histodumb.GetYaxis().SetRangeUser(0,1.1)
histodumb.SetTitle(plotTitle)
histodumb.GetXaxis().SetTitle(XaxisTitle)
histodumb.GetYaxis().SetTitle("efficiency")
histodumb.SetStats(0)


Histo1.Draw("*same")
Histo1.SetStats(0)
func1.Draw("same")
func1.SetLineColor(1)
#line1.Draw("same")
#line1.SetLineColor(1)
Histo2.Draw("*same")
Histo2.SetLineColor(4)
Histo2.SetStats(0)
#line2.Draw("same")
#line2.SetLineColor(4)
func2.Draw("same")
func2.SetLineColor(4)
Histo3.Draw("*same")
Histo3.SetLineColor(2)
Histo3.SetStats(0)
func3.Draw("same")
func3.SetLineColor(2)
#line3.Draw("same")
#line3.SetLineColor(2)
gStyle.SetOptStat(0)

c.Update()

legend.Draw()
c.Print(outname+"_"+str(mass)+"_scaled.pdf","Title:histoTitle")
