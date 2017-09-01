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
energy = "1pt05"

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'hm:e:')

# Parse the command line arguments
for opt, arg in options:
        if opt=='-m':
            mass = arg
	if opt=='-e':
            energy = str(arg)
        if opt=='-h':
            print_usage()
            sys.exit(0)


#filename1 = "/home/mrsolt/hps/Layer0Studies/Layer0/ap/L0L0/ap_" + str(mass) + "MeV_displaced_L0L0_vertcuts.root"
#filename2 = "/home/mrsolt/hps/Layer0Studies/Layer0/ap/L0L1/ap_" + str(mass) + "_displaced_L0L1_vertcuts.root"
#filename3 = "/home/mrsolt/hps/Layer0Studies/Layer0/ap/L1L1/ap_" + str(mass) + "_displaced_L1L1_vertcuts.root"
#filename4 = "/home/mrsolt/hps/Layer0Studies/Layer0/ap/L1L2/ap_" + str(mass) + "_displaced_L1L2_vertcuts.root"
#filename5 = "/home/mrsolt/hps/Layer0Studies/Layer0/ap/L2L2/ap_" + str(mass) + "MeV_displaced_L2L2_vertcuts.root"
#filename6 = "/home/mrsolt/hps/Layer0Studies/Layer0/ap/L0L2/ap_" + str(mass) + "_displaced_L0L2_vertcuts.root"

filename1 = "/home/mrsolt/hps/L0Studies/L0/1pt05/ap/L0L0/ap_" + str(mass) + "MeV_loose_vertcuts.root"
filename2 = "/home/mrsolt/hps/L0Studies/L0/1pt05/ap/L0L1/ap_" + str(mass) + "MeV_loose_vertcuts.root"
filename3 = "/home/mrsolt/hps/L0Studies/L0/1pt05/ap/L1L1/ap_" + str(mass) + "MeV_loose_vertcuts.root"
filename4 = "/home/mrsolt/hps/L0Studies/L0/1pt05/ap/L1L2/ap_" + str(mass) + "MeV_loose_vertcuts.root"
filename5 = "/home/mrsolt/hps/L0Studies/L0/1pt05/ap/L2L2/ap_" + str(mass) + "MeV_loose_vertcuts.root"
filename6 = "/home/mrsolt/hps/L0Studies/L0/1pt05/ap/L0L2/ap_" + str(mass) + "MeV_loose_vertcuts.root"

filename7 = "/home/mrsolt/hps/Layer0Studies/Nominal/ap/L1L1/ap_" + str(mass) + "MeV_displaced_vertcuts.root"
filename8 = "/home/mrsolt/hps/Layer0Studies/Nominal/ap/L1L2/ap_" + str(mass) + "MeV_displaced_vertcuts.root"
filename9 = "/home/mrsolt/hps/Layer0Studies/Nominal/ap/L2L2/ap_" + str(mass) + "MeV_displaced_vertcuts.root"

filename10 = "/home/mrsolt/hps/Layer0Studies/Layer0/ap/truth/ap_1pt05_" + str(mass) + "MeV_truth.root"
filename11 = "/home/mrsolt/hps/Layer0Studies/Nominal/ap/truth/apsignal_slic_displaced_" + str(mass) + "_dq_truth.root"

outname = "stat_eff"
histoTitle = "uncVZ"
histoTitleTruth = "triEndZ"

plotTitle = str(mass) + " MeV Total Efficiency"

file_L0L0_L0 = TFile(filename1)
file_L0L1_L0 = TFile(filename2)
file_L1L1_L0 = TFile(filename3)
file_L1L2_L0 = TFile(filename4)
file_L2L2_L0 = TFile(filename5)
file_L0L2_L0 = TFile(filename6)

file_L1L1_nom = TFile(filename7)
file_L1L2_nom = TFile(filename8)
file_L2L2_nom = TFile(filename9)

file_truth_L0 = TFile(filename10)
file_truth_nom = TFile(filename11)


c = TCanvas("c","c",800,600);

zmin = -4.9
zmax = 150
nBins = 50

file_truth_L0.Get("ntuple").Draw(histoTitleTruth + ">>L0_truth_h({0},{1},{2})".format(nBins,zmin,zmax))
L0_truth_h = ROOT.gROOT.FindObject("L0_truth_h")
file_truth_nom.Get("ntuple").Draw(histoTitleTruth + ">>nom_truth_h({0},{1},{2})".format(nBins,zmin,zmax))
nom_truth_h = ROOT.gROOT.FindObject("nom_truth_h")

file_L0L0_L0.Get("cut").Draw(histoTitle + ">>L0_L0L0_h({0},{1},{2})".format(nBins,zmin,zmax))
L0_L0L0_h = ROOT.gROOT.FindObject("L0_L0L0_h")
file_L0L1_L0.Get("cut").Draw(histoTitle + ">>L0_L0L1_h({0},{1},{2})".format(nBins,zmin,zmax))
L0_L0L1_h = ROOT.gROOT.FindObject("L0_L0L1_h")
file_L1L1_L0.Get("cut").Draw(histoTitle + ">>L0_L1L1_h({0},{1},{2})".format(nBins,zmin,zmax))
L0_L1L1_h = ROOT.gROOT.FindObject("L0_L1L1_h")
file_L1L2_L0.Get("cut").Draw(histoTitle + ">>L0_L1L2_h({0},{1},{2})".format(nBins,zmin,zmax))
L0_L1L2_h = ROOT.gROOT.FindObject("L0_L1L2_h")
file_L2L2_L0.Get("cut").Draw(histoTitle + ">>L0_L2L2_h({0},{1},{2})".format(nBins,zmin,zmax))
L0_L2L2_h = ROOT.gROOT.FindObject("L0_L2L2_h")
file_L0L2_L0.Get("cut").Draw(histoTitle + ">>L0_L0L2_h({0},{1},{2})".format(nBins,zmin,zmax))
L0_L0L2_h = ROOT.gROOT.FindObject("L0_L0L2_h")

file_L1L1_nom.Get("cut").Draw(histoTitle + ">>nom_L1L1_h({0},{1},{2})".format(nBins,zmin,zmax))
nom_L1L1_h = ROOT.gROOT.FindObject("nom_L1L1_h")
file_L1L2_nom.Get("cut").Draw(histoTitle + ">>nom_L1L2_h({0},{1},{2})".format(nBins,zmin,zmax))
nom_L1L2_h = ROOT.gROOT.FindObject("nom_L1L2_h")
file_L2L2_nom.Get("cut").Draw(histoTitle + ">>nom_L2L2_h({0},{1},{2})".format(nBins,zmin,zmax))
nom_L2L2_h = ROOT.gROOT.FindObject("nom_L2L2_h")

zArr = array.array('d')
L0Arr = array.array('d')
nomArr = array.array('d')

HistoNom = TH1F("HistoNom","HistoNom",nBins,zmin,zmax)
HistoL0 = TH1F("HistoL0","HistoL0",nBins,zmin,zmax)

for i in range(0,nBins):
    z = zmin + (zmax-zmin)/float(nBins) * i

    L0L0_L0 = L0_L0L0_h.GetBinContent(i+1)
    L0L1_L0 = L0_L0L1_h.GetBinContent(i+1)
    L1L1_L0 = L0_L1L1_h.GetBinContent(i+1)
    L1L2_L0 = L0_L1L2_h.GetBinContent(i+1)
    L2L2_L0 = L0_L2L2_h.GetBinContent(i+1)
    L0L2_L0 = L0_L0L2_h.GetBinContent(i+1)

    L1L1_nom = nom_L1L1_h.GetBinContent(i+1)
    L1L2_nom = nom_L1L2_h.GetBinContent(i+1)
    L2L2_nom = nom_L2L2_h.GetBinContent(i+1)

    L0_truth = L0_truth_h.GetBinContent(i+1)
    nom_truth = nom_truth_h.GetBinContent(i+1)

    zArr.append(z)
    L0Arr.append((L0L0_L0 + L0L1_L0 + L1L1_L0 + L1L2_L0 + L2L2_L0 + L0L2_L0)/float(L0_truth))
    nomArr.append((L1L1_nom + L1L2_nom + L2L2_nom)/float(nom_truth))
    
    HistoL0.SetBinContent(i+1,(L0L0_L0 + L0L1_L0 + L1L1_L0 + L1L2_L0 + L2L2_L0 + L0L2_L0)/float(L0_truth))
    HistoNom.SetBinContent(i+1,(L1L1_nom + L1L2_nom + L2L2_nom)/float(nom_truth))

GraphL0 = TGraph(nBins,zArr,L0Arr)
GraphNom = TGraph(nBins,zArr,nomArr)

c.Clear()

legend = TLegend(.68,.66,.92,.87)
legend.SetBorderSize(0)
legend.SetFillColor(0)
legend.SetFillStyle(0)
legend.SetTextFont(42)
legend.SetTextSize(0.035)
legend.AddEntry(GraphL0,"L0","P")
legend.AddEntry(GraphNom,"nominal","P")

#histodumb = TH1F("histodumb","",nBins,zmin,zmax)
#histodumb.Fill(zmax-1,0.0001)

#histodumb.Draw("")
#histodumb.GetXaxis().SetRangeUser(-5,150)
#histodumb.GetYaxis().SetRangeUser(0,1.1)
#histodumb.SetTitle(plotTitle)
#histodumb.GetXaxis().SetTitle(XaxisTitle)
#histodumb.GetYaxis().SetTitle("efficiency")
#histodumb.SetStats(0)

GraphNom.Draw("")
#GraphNom.SetStats(0)
GraphNom.GetXaxis().SetRangeUser(zmin,zmax)
GraphNom.GetYaxis().SetRangeUser(0,0.15)
GraphNom.SetTitle(plotTitle)
GraphNom.GetXaxis().SetTitle("z [mm]")
GraphNom.GetYaxis().SetTitle("efficiency")
GraphL0.Draw("same")
GraphL0.SetLineColor(2)

gStyle.SetOptStat(0)


legend.Draw()
c.Print("/home/mrsolt/hps/L0Studies/figs/1pt05/eff/"+outname+"_"+str(mass)+"loose.pdf","Title:histoTitle")

legend2 = TLegend(.68,.66,.92,.87)
legend2.SetBorderSize(0)
legend2.SetFillColor(0)
legend2.SetFillStyle(0)
legend2.SetTextFont(42)
legend2.SetTextSize(0.035)
legend2.AddEntry(HistoL0,"L0","LP")
legend2.AddEntry(HistoNom,"nominal","LP")

c.Clear()

HistoNom.Draw("")
#GraphNom.SetStats(0)
HistoNom.GetXaxis().SetRangeUser(zmin,zmax)
HistoNom.GetYaxis().SetRangeUser(0,0.15)
HistoNom.SetTitle(plotTitle)
HistoNom.SetTitleSize(0.8)
HistoNom.GetXaxis().SetTitle("z [mm]")
HistoNom.GetXaxis().SetTitleSize(0.05)
HistoNom.GetYaxis().SetTitle("efficiency")
HistoNom.GetYaxis().SetTitleSize(0.05)
HistoL0.Draw("same")
HistoL0.SetLineColor(2)

gStyle.SetOptStat(0)
c.Update()


legend2.Draw()
c.Print("/home/mrsolt/hps/L0Studies/figs/1pt05/eff/"+outname+"_"+str(mass)+"loose_histo.pdf","Title:histoTitle")
