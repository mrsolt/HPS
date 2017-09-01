#!/usr/bin/env python
import sys
import array, math
import ROOT
from ROOT import gROOT, gStyle, TFile, TTree, TChain, TMVA, TCut, TCanvas, gDirectory, TH1, TGraph, gPad, TF1, TGraphErrors, TLegend, TGaxis, TLine
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


filename1_nom = "/home/mrsolt/hps/Layer0Studies/Nominal/ap/L1L1/acceptance_"+str(mass)+".root"
filename2_nom = "/home/mrsolt/hps/Layer0Studies/Nominal/ap/L1L2/acceptance_"+str(mass)+".root"
filename3_nom = "/home/mrsolt/hps/Layer0Studies/Nominal/ap/L2L2/acceptance_"+str(mass)+".root"
filename1_L0 = "/home/mrsolt/hps/Layer0Studies/Layer0/ap/L0L0/acceptance_" + str(mass) + ".root"
filename2_L0 = "/home/mrsolt/hps/Layer0Studies/Layer0/ap/L0L1/acceptance_" + str(mass) + ".root"
filename3_L0 = "/home/mrsolt/hps/Layer0Studies/Layer0/ap/L1L1/acceptance_" + str(mass) + ".root"
filename4_L0 = "/home/mrsolt/hps/Layer0Studies/Layer0/ap/L1L2/acceptance_" + str(mass) + ".root"
filename5_L0 = "/home/mrsolt/hps/Layer0Studies/Layer0/ap/L2L2/acceptance_" + str(mass) + ".root"
filename6_L0 = "/home/mrsolt/hps/Layer0Studies/Layer0/ap/L0L2/acceptance_" + str(mass) + ".root"
outname = "combined_eff"
histoTitle = "eff_all_unscaled"

#if (int(mass) > 59 and int(mass < 71)):
#    filename2_nom = "/home/mrsolt/hps/Layer0Studies/Nominal/ap/100mm/L1L2/acceptance_"+str(mass)+".root"

exppol3=TF1("exppol3","exp(pol3(0))",-5,100)
exppol4=TF1("exppol4","exp(pol4(0))",-5,100)
exppol5=TF1("exppol5","exp(pol5(0))",-5,100)

plotTitle = str(mass) + " MeV Total Efficiency"

inFile1_nom = TFile(filename1_nom)
inFile2_nom = TFile(filename2_nom)
inFile3_nom = TFile(filename3_nom)
inFile1_L0 = TFile(filename1_L0)
inFile2_L0 = TFile(filename2_L0)
inFile3_L0 = TFile(filename3_L0)
inFile4_L0 = TFile(filename4_L0)
inFile5_L0 = TFile(filename5_L0)
inFile6_L0 = TFile(filename6_L0)

c = TCanvas("c","c",800,600);

XaxisTitle = inFile1_nom.Get(histoTitle).GetXaxis().GetTitle();
YaxisTitle = inFile1_nom.Get(histoTitle).GetYaxis().GetTitle();

Histo1_nom = inFile1_nom.Get(histoTitle)
Histo2_nom = inFile2_nom.Get(histoTitle)
Histo3_nom = inFile3_nom.Get(histoTitle)

Histo1_L0 = inFile1_L0.Get(histoTitle)
Histo2_L0 = inFile2_L0.Get(histoTitle)
Histo3_L0 = inFile3_L0.Get(histoTitle)
Histo4_L0 = inFile4_L0.Get(histoTitle)
Histo5_L0 = inFile5_L0.Get(histoTitle)

#func1_nom = inFile1_nom.Get(histoTitle).GetFunction("exppol4")
#func2_nom = inFile2_nom.Get(histoTitle).GetFunction("exppol3")
#func3_nom = inFile3_nom.Get(histoTitle).GetFunction("exppol5")

#func1_L0 = inFile1_L0.Get(histoTitle).GetFunction("exppol3")
#func2_L0 = inFile2_L0.Get(histoTitle).GetFunction("exppol4")
#func3_L0 = inFile3_L0.Get(histoTitle).GetFunction("exppol5")
#func4_L0 = inFile4_L0.Get(histoTitle).GetFunction("exppol4")
#func5_L0 = inFile5_L0.Get(histoTitle).GetFunction("exppol5")

func1_nom = inFile1_nom.Get(histoTitle).GetFunction("exppol4")
func2_nom = inFile2_nom.Get(histoTitle).GetFunction("exppol4")
func3_nom = inFile3_nom.Get(histoTitle).GetFunction("gaus")

func1_L0 = inFile1_L0.Get(histoTitle).GetFunction("exppol4")
func2_L0 = inFile2_L0.Get(histoTitle).GetFunction("exppol4")
func3_L0 = inFile3_L0.Get(histoTitle).GetFunction("gaus")
func4_L0 = inFile4_L0.Get(histoTitle).GetFunction("gaus")
func5_L0 = inFile5_L0.Get(histoTitle).GetFunction("gaus")
func6_L0 = inFile6_L0.Get(histoTitle).GetFunction("exppol4")

zmin = -4.9
zmax = 150
nbins = 500

L1L1_nom_min = [-5,-5,-5,-5,-5,-5,-5,-5]
L1L1_nom_max = [100,100,100,100,100,100,100,100]
L1L2_nom_min = [-5,-5,-5,-5,20,30,0,0]
L1L2_nom_max = [60,80,90,100,100,100,0,0]
#L2L2_nom_min = [-5,15,30,30,50,0,0,0]
#L2L2_nom_max = [60,100,120,120,120,0,0,0]
L2L2_nom_min = [-5,-5,-5,-5,-5,0,0,0]
L2L2_nom_max = [150,150,150,150,150,0,0,0]

L0L0_L0_min = [-5,-5,-5,-5,-5,-5,-5,-5]
L0L0_L0_max = [50,50,50,50,50,50,50,50]
L0L1_L0_min = [-5,-5,-5,-5,-5,-5,0,0]
L0L1_L0_max = [50,50,50,50,50,50,0,0]
#L1L1_L0_min = [0,5,5,5,10,10,0,0]
#L1L1_L0_max = [35,70,70,70,80,80,0,0]
L1L1_L0_min = [-5,-5,-5,-5,-5,-5,0,0]
L1L1_L0_max = [150,150,150,150,150,150,0,0]
#L1L2_L0_min = [-5,10,10,10,10,20,0,0]
#L1L2_L0_max = [70,80,100,100,100,110,0,0]
L1L2_L0_min = [-5,-5,-5,-5,-5,-5,0,0]
L1L2_L0_max = [150,150,150,150,150,150,0,0]
#L2L2_L0_min = [5,10,20,20,20,0,0,0]
#L2L2_L0_max = [100,130,140,140,140,0,0,0]
L2L2_L0_min = [-5,-5,-5,-5,-5,0,0,0]
L2L2_L0_max = [150,150,150,150,150,0,0,0]
L0L2_L0_min = [-5,-5,-5,-5,-5,-5,0,0]
L0L2_L0_max = [45,60,60,60,60,60,0,0]

z_arr = array.array('d')
eff_L1L1_nom = array.array('d')
eff_L1L2_nom = array.array('d')
eff_L2L2_nom = array.array('d')
eff_L0L0_L0 = array.array('d')
eff_L0L1_L0 = array.array('d')
eff_L1L1_L0 = array.array('d')
eff_L1L2_L0 = array.array('d')
eff_L2L2_L0 = array.array('d')
eff_L0L2_L0 = array.array('d')
eff_arr_nom = array.array('d')
eff_arr_L0 = array.array('d')

m = 0
mass = int(mass)
if(mass > 19 and mass < 21): m = 0
if(mass > 29 and mass < 31): m = 1
if(mass > 39 and mass < 41): m = 2
if(mass > 49 and mass < 51): m = 3
if(mass > 59 and mass < 61): m = 4
if(mass > 69 and mass < 71): m = 5
if(mass > 79 and mass < 81): m = 6
if(mass > 89 and mass < 91): m = 7

for i in range (0,nbins):
    z = zmin + i * (zmax - zmin) / float(nbins)
    z_arr.append(z)
    if(z > L1L1_nom_min[m] and z < L1L1_nom_max[m]): eff_L1L1_nom.append(func1_nom.Eval(z))
    else: eff_L1L1_nom.append(0.0)
    if(z > L1L2_nom_min[m] and z < L1L2_nom_max[m]): eff_L1L2_nom.append(func2_nom.Eval(z))
    else: eff_L1L2_nom.append(0.0)
    if(z > L2L2_nom_min[m] and z < L2L2_nom_max[m]): eff_L2L2_nom.append(func3_nom.Eval(z))
    else: eff_L2L2_nom.append(0.0)
    if(z > L0L0_L0_min[m] and z < L0L0_L0_max[m]): eff_L0L0_L0.append(func1_L0.Eval(z))
    else: eff_L0L0_L0.append(0.0)
    if(z > L0L1_L0_min[m] and z < L0L1_L0_max[m]): eff_L0L1_L0.append(func2_L0.Eval(z))
    else: eff_L0L1_L0.append(0.0)
    if(z > L1L1_L0_min[m] and z < L1L1_L0_max[m]): eff_L1L1_L0.append(func3_L0.Eval(z))
    else: eff_L1L1_L0.append(0.0)
    if(z > L1L2_L0_min[m] and z < L1L2_L0_max[m]): eff_L1L2_L0.append(func4_L0.Eval(z))
    else: eff_L1L2_L0.append(0.0)
    if(z > L2L2_L0_min[m] and z < L2L2_L0_max[m]): eff_L2L2_L0.append(func5_L0.Eval(z))
    else: eff_L2L2_L0.append(0.0)
    if(z > L0L2_L0_min[m] and z < L0L2_L0_max[m]): eff_L0L2_L0.append(func6_L0.Eval(z))
    else: eff_L0L2_L0.append(0.0)
    eff_arr_nom.append(eff_L1L1_nom[i] + eff_L1L2_nom[i] + eff_L2L2_nom[i])
    eff_arr_L0.append(eff_L0L0_L0[i] + eff_L0L1_L0[i] + eff_L1L1_L0[i] + eff_L1L2_L0[i] + eff_L2L2_L0[i] + eff_L0L2_L0[i])

graph1 = TGraph(nbins,z_arr,eff_arr_L0)
graph2 = TGraph(nbins,z_arr,eff_arr_nom)

legend = TLegend(.68,.66,.92,.87)
legend.SetBorderSize(0)
legend.SetFillColor(0)
legend.SetFillStyle(0)
legend.SetTextFont(42)
legend.SetTextSize(0.035)
legend.AddEntry(graph1,"L0","LP")
legend.AddEntry(graph2,"Nominal","LP")

graph1.Draw("")
graph1.SetTitle(plotTitle)
graph1.GetXaxis().SetTitle(XaxisTitle);
graph1.GetYaxis().SetTitle("efficiency");
graph1.SetLineColor(1)
graph1.GetXaxis().SetRangeUser(-5,150)
graph1.GetYaxis().SetRangeUser(0,0.15)
graph2.Draw("same")
graph2.SetLineColor(2)
gStyle.SetOptStat(0)


legend.Draw()
c.Print(outname+"_"+str(mass)+".pdf","Title:histoTitle")
