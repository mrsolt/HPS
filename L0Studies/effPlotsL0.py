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


#filename1 = "/home/mrsolt/hps/Layer0Studies/Layer0/ap/L0L0/acceptance_" + str(mass) + ".root"
#filename2 = "/home/mrsolt/hps/Layer0Studies/Layer0/ap/L0L1/acceptance_" + str(mass) + ".root"
#filename3 = "/home/mrsolt/hps/Layer0Studies/Layer0/ap/L1L1/acceptance_" + str(mass) + ".root"
#filename4 = "/home/mrsolt/hps/Layer0Studies/Layer0/ap/L1L2/acceptance_" + str(mass) + ".root"
#filename5 = "/home/mrsolt/hps/Layer0Studies/Layer0/ap/L2L2/acceptance_" + str(mass) + ".root"
#filename6 = "/home/mrsolt/hps/Layer0Studies/Layer0/ap/L0L2/acceptance_" + str(mass) + ".root"

filename1 = "/home/mrsolt/hps/L0Studies/L0/1pt05/ap/L0L0/acceptance_" + str(mass) + ".root"
filename2 = "/home/mrsolt/hps/L0Studies/L0/1pt05/ap/L0L1/acceptance_" + str(mass) + ".root"
filename3 = "/home/mrsolt/hps/L0Studies/L0/1pt05/ap/L1L1/acceptance_" + str(mass) + ".root"
filename4 = "/home/mrsolt/hps/L0Studies/L0/1pt05/ap/L1L2/acceptance_" + str(mass) + ".root"
filename5 = "/home/mrsolt/hps/L0Studies/L0/1pt05/ap/L2L2/acceptance_" + str(mass) + ".root"
filename6 = "/home/mrsolt/hps/L0Studies/L0/1pt05/ap/L0L2/acceptance_" + str(mass) + ".root"

outname = "L0_eff"
histoTitle = "eff_all"

exppol4=TF1("exppol4","exp(pol4(0))",-5,100)

plotTitle = str(mass) + " MeV L0 Efficiency"

inFile1 = TFile(filename1)
inFile2 = TFile(filename2)
inFile3 = TFile(filename3)
inFile4 = TFile(filename4)
inFile5 = TFile(filename5)
inFile6 = TFile(filename6)

zFile1 = TFile("/home/mrsolt/hps/Vertexing/L0/1pt05/ap/upperlimit/golden_massbin.root")
zFile2 = TFile("/home/mrsolt/hps/Vertexing/L0/1pt05/ap/L1L2/golden.root")
zFile3 = TFile("/home/mrsolt/hps/Vertexing/L0/1pt05/ap/L2L2/golden.root")
zFile4 = TFile("/home/mrsolt/hps/Vertexing/L0/1pt05/ap/L2L3/golden.root")
zFile5 = TFile("/home/mrsolt/hps/Vertexing/L0/1pt05/ap/L3L3/golden.root")
zFile6 = ""

c = TCanvas("c","c",800,600);

XaxisTitle = inFile1.Get(histoTitle).GetXaxis().GetTitle();
YaxisTitle = inFile1.Get(histoTitle).GetYaxis().GetTitle();

Histo1 = inFile1.Get(histoTitle)
Histo2 = inFile2.Get("eff_all_unscaled")
Histo3 = inFile3.Get(histoTitle)
Histo4 = inFile4.Get(histoTitle)
Histo5 = inFile5.Get(histoTitle)
Histo6 = inFile6.Get("eff_all_unscaled")

normHisto = inFile1.Get("eff_all_unscaled").GetFunction("exppol4").Eval(-5)
print normHisto
Histo2.Scale(1./normHisto)
Histo6.Scale(1./normHisto)

func1 = inFile1.Get(histoTitle).GetFunction("exppol4")
func2 = Histo2.GetFunction("exppol4")
func3 = inFile3.Get(histoTitle).GetFunction("gaus")
func4 = inFile4.Get(histoTitle).GetFunction("gaus")
func5 = inFile5.Get(histoTitle).GetFunction("gaus")
func6 = Histo6.GetFunction("exppol4")

func2.SetParameter(0,func2.GetParameter(0)+math.log(1./normHisto))
func6.SetParameter(0,func6.GetParameter(0)+math.log(1./normHisto))

legend = TLegend(.68,.66,.92,.87)
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

xArr1 = array.array('d')
yArr1 = array.array('d')
yArr2 = array.array('d')
yArr3 = array.array('d')
yArr4 = array.array('d')
yArr5 = array.array('d')
yArr6 = array.array('d')

xArrdum = ROOT.Double(0)
yArrdum = ROOT.Double(0)

n_bins = zFile1.Get("zcut").GetN()

for i in range (0,n_bins):
    xArr1.append(0.)
    yArr1.append(0.)
    yArr2.append(0.)
    yArr3.append(0.)
    yArr4.append(0.)
    yArr5.append(0.)
    yArr6.append(0.)


for i in range(0,n_bins):
    zFile1.Get("zcut").GetPoint(i,xArrdum,yArrdum)
    xArr1[i] = xArrdum
    yArr1[i] = yArrdum
    zFile2.Get("zcut").GetPoint(i,xArrdum,yArrdum)
    yArr2[i] = yArrdum
    zFile3.Get("zcut").GetPoint(i,xArrdum,yArrdum)
    yArr3[i] = yArrdum
    zFile4.Get("zcut").GetPoint(i,xArrdum,yArrdum)
    yArr4[i] = yArrdum
    zFile5.Get("zcut").GetPoint(i,xArrdum,yArrdum)
    yArr5[i] = yArrdum
    #zFile6.Get("zcut").GetPoint(i,xArrdum,yArrdum)
    #yArr6[i] = yArrdum

mass_index = 0

for i in range(0,n_bins):
    if(xArr1[i] < float(mass)/1000.): continue
    else:
        mass_index = i
        break

zcut1 = yArr1[mass_index]
zcut2 = yArr2[mass_index]
zcut3 = yArr3[mass_index]
zcut4 = yArr4[mass_index]
zcut5 = yArr5[mass_index]
#zcut6 = yArr6[mass_index]

print mass_index
print zcut1
print zcut2
print zcut3
print zcut4
print zcut5
#print zcut6

line1 = TLine(zcut1,0,zcut1,0.15)
line2 = TLine(zcut2,0,zcut2,0.15)
line3 = TLine(zcut3,0,zcut3,0.15)
line4 = TLine(zcut4,0,zcut4,0.15)
line5 = TLine(zcut5,0,zcut5,0.15)
#line6 = TLine(zcut5,0,zcut6,0.15)

histodumb = TH1F("histodumb","",100,-5,150)
histodumb.Fill(149,0.0001)

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
Histo4.Draw("*same")
Histo4.SetLineColor(3)
Histo4.SetStats(0)
func4.Draw("same")
func4.SetLineColor(3)
#line4.Draw("same")
#line4.SetLineColor(3)
Histo5.Draw("*same")
Histo5.SetLineColor(6)
Histo5.SetStats(0)
func5.Draw("same")
func5.SetLineColor(6)
#line5.Draw("same")
#line5.SetLineColor(6)
Histo6.Draw("*same")
Histo6.SetLineColor(7)
Histo6.SetStats(0)
func6.Draw("same")
func6.SetLineColor(7)
#line6.Draw("same")
#line6.SetLineColor(7)
gStyle.SetOptStat(0)
gROOT.ForceStyle()

legend.Draw()
c.Print(outname+"_"+str(mass)+"_scaled_loose.pdf","Title:histoTitle")
