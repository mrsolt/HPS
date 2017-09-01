#!/usr/bin/env python
import sys
import array, math
import ROOT
from ROOT import gROOT, gStyle, TFile, TTree, TChain, TMVA, TCut, TCanvas, gDirectory, TH1, TH1F, TGraph, gPad, TF1, TGraphErrors, TLegend, TGaxis, TLine, TFitResult
import getopt


def print_usage():
    print "\nUsage:"
    print "Arguments: "
    print '\t-h: this help message'
    print "\n"

energy = "1pt05"

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'he:')

# Parse the command line arguments
for opt, arg in options:
	if opt=='-e':
            energy = str(arg)
        if opt=='-h':
            print_usage()
            sys.exit(0)

nMass = 8

L0_15_file = TFile("/home/mrsolt/hps/L0Studies/L0/" + energy + "/ap/prompt/ap_15MeV_prompt_bump.root")
L0_20_file = TFile("/home/mrsolt/hps/L0Studies/L0/" + energy + "/ap/prompt/ap_20MeV_prompt_bump.root")
L0_30_file = TFile("/home/mrsolt/hps/L0Studies/L0/" + energy + "/ap/prompt/ap_30MeV_prompt_bump.root")
L0_40_file = TFile("/home/mrsolt/hps/L0Studies/L0/" + energy + "/ap/prompt/ap_40MeV_prompt_bump.root")
L0_50_file = TFile("/home/mrsolt/hps/L0Studies/L0/" + energy + "/ap/prompt/ap_50MeV_prompt_bump.root")
L0_60_file = TFile("/home/mrsolt/hps/L0Studies/L0/" + energy + "/ap/prompt/ap_60MeV_prompt_bump.root")
L0_70_file = TFile("/home/mrsolt/hps/L0Studies/L0/" + energy + "/ap/prompt/ap_70MeV_prompt_bump.root")
L0_80_file = TFile("/home/mrsolt/hps/L0Studies/L0/" + energy + "/ap/prompt/ap_80MeV_prompt_bump.root")
L0_90_file = TFile("/home/mrsolt/hps/L0Studies/L0/" + energy + "/ap/prompt/ap_90MeV_prompt_bump.root")

nom_15_file = TFile("/home/mrsolt/hps/L0Studies/nominal/" + energy + "/ap/prompt/ap_15MeV_prompt_bump.root")
nom_20_file = TFile("/home/mrsolt/hps/L0Studies/nominal/" + energy + "/ap/prompt/ap_20MeV_prompt_bump.root")
nom_30_file = TFile("/home/mrsolt/hps/L0Studies/nominal/" + energy + "/ap/prompt/ap_30MeV_prompt_bump.root")
nom_40_file = TFile("/home/mrsolt/hps/L0Studies/nominal/" + energy + "/ap/prompt/ap_40MeV_prompt_bump.root")
nom_50_file = TFile("/home/mrsolt/hps/L0Studies/nominal/" + energy + "/ap/prompt/ap_50MeV_prompt_bump.root")
nom_60_file = TFile("/home/mrsolt/hps/L0Studies/nominal/" + energy + "/ap/prompt/ap_60MeV_prompt_bump.root")
nom_70_file = TFile("/home/mrsolt/hps/L0Studies/nominal/" + energy + "/ap/prompt/ap_70MeV_prompt_bump.root")
nom_80_file = TFile("/home/mrsolt/hps/L0Studies/nominal/" + energy + "/ap/prompt/ap_80MeV_prompt_bump.root")
nom_90_file = TFile("/home/mrsolt/hps/L0Studies/nominal/" + energy + "/ap/prompt/ap_90MeV_prompt_bump.root")

histoTitleUnc = "uncM"
histoTitleTarg = "tarM"

plotTitle =  "Invariant Mass"

c = TCanvas("c","c",800,600);

minMass = 0
maxMass = 0.12
nBins = 180

L0_15_file.Get("ntuple").Draw(histoTitleUnc + ">>L0_15_Unc_h({0},{1},{2})".format(nBins,minMass,maxMass))
L0_15_Unc_h = ROOT.gROOT.FindObject("L0_15_Unc_h")
L0_20_file.Get("ntuple").Draw(histoTitleUnc + ">>L0_20_Unc_h({0},{1},{2})".format(nBins,minMass,maxMass))
L0_20_Unc_h = ROOT.gROOT.FindObject("L0_20_Unc_h")
L0_30_file.Get("ntuple").Draw(histoTitleUnc + ">>L0_30_Unc_h({0},{1},{2})".format(nBins,minMass,maxMass))
L0_30_Unc_h = ROOT.gROOT.FindObject("L0_30_Unc_h")
L0_40_file.Get("ntuple").Draw(histoTitleUnc + ">>L0_40_Unc_h({0},{1},{2})".format(nBins,minMass,maxMass))
L0_40_Unc_h = ROOT.gROOT.FindObject("L0_40_Unc_h")
L0_50_file.Get("ntuple").Draw(histoTitleUnc + ">>L0_50_Unc_h({0},{1},{2})".format(nBins,minMass,maxMass))
L0_50_Unc_h = ROOT.gROOT.FindObject("L0_50_Unc_h")
L0_60_file.Get("ntuple").Draw(histoTitleUnc + ">>L0_60_Unc_h({0},{1},{2})".format(nBins,minMass,maxMass))
L0_60_Unc_h = ROOT.gROOT.FindObject("L0_60_Unc_h")
L0_70_file.Get("ntuple").Draw(histoTitleUnc + ">>L0_70_Unc_h({0},{1},{2})".format(nBins,minMass,maxMass))
L0_70_Unc_h = ROOT.gROOT.FindObject("L0_70_Unc_h")
L0_80_file.Get("ntuple").Draw(histoTitleUnc + ">>L0_80_Unc_h({0},{1},{2})".format(nBins,minMass,maxMass))
L0_80_Unc_h = ROOT.gROOT.FindObject("L0_80_Unc_h")
L0_90_file.Get("ntuple").Draw(histoTitleUnc + ">>L0_90_Unc_h({0},{1},{2})".format(nBins,minMass,maxMass))
L0_90_Unc_h = ROOT.gROOT.FindObject("L0_90_Unc_h")

nom_15_file.Get("ntuple").Draw(histoTitleUnc + ">>nom_15_Unc_h({0},{1},{2})".format(nBins,minMass,maxMass))
nom_15_Unc_h = ROOT.gROOT.FindObject("nom_15_Unc_h")
nom_20_file.Get("ntuple").Draw(histoTitleUnc + ">>nom_20_Unc_h({0},{1},{2})".format(nBins,minMass,maxMass))
nom_20_Unc_h = ROOT.gROOT.FindObject("nom_20_Unc_h")
nom_30_file.Get("ntuple").Draw(histoTitleUnc + ">>nom_30_Unc_h({0},{1},{2})".format(nBins,minMass,maxMass))
nom_30_Unc_h = ROOT.gROOT.FindObject("nom_30_Unc_h")
nom_40_file.Get("ntuple").Draw(histoTitleUnc + ">>nom_40_Unc_h({0},{1},{2})".format(nBins,minMass,maxMass))
nom_40_Unc_h = ROOT.gROOT.FindObject("nom_40_Unc_h")
nom_50_file.Get("ntuple").Draw(histoTitleUnc + ">>nom_50_Unc_h({0},{1},{2})".format(nBins,minMass,maxMass))
nom_50_Unc_h = ROOT.gROOT.FindObject("nom_50_Unc_h")
nom_60_file.Get("ntuple").Draw(histoTitleUnc + ">>nom_60_Unc_h({0},{1},{2})".format(nBins,minMass,maxMass))
nom_60_Unc_h = ROOT.gROOT.FindObject("nom_60_Unc_h")
nom_70_file.Get("ntuple").Draw(histoTitleUnc + ">>nom_70_Unc_h({0},{1},{2})".format(nBins,minMass,maxMass))
nom_70_Unc_h = ROOT.gROOT.FindObject("nom_70_Unc_h")
nom_80_file.Get("ntuple").Draw(histoTitleUnc + ">>nom_80_Unc_h({0},{1},{2})".format(nBins,minMass,maxMass))
nom_80_Unc_h = ROOT.gROOT.FindObject("nom_80_Unc_h")
nom_90_file.Get("ntuple").Draw(histoTitleUnc + ">>nom_90_Unc_h({0},{1},{2})".format(nBins,minMass,maxMass))
nom_90_Unc_h = ROOT.gROOT.FindObject("nom_90_Unc_h")


L0_15_file.Get("ntuple").Draw(histoTitleTarg + ">>L0_15_Targ_h({0},{1},{2})".format(nBins,minMass,maxMass))
L0_15_Targ_h = ROOT.gROOT.FindObject("L0_15_Targ_h")
L0_20_file.Get("ntuple").Draw(histoTitleTarg + ">>L0_20_Targ_h({0},{1},{2})".format(nBins,minMass,maxMass))
L0_20_Targ_h = ROOT.gROOT.FindObject("L0_20_Targ_h")
L0_30_file.Get("ntuple").Draw(histoTitleTarg + ">>L0_30_Targ_h({0},{1},{2})".format(nBins,minMass,maxMass))
L0_30_Targ_h = ROOT.gROOT.FindObject("L0_30_Targ_h")
L0_40_file.Get("ntuple").Draw(histoTitleTarg + ">>L0_40_Targ_h({0},{1},{2})".format(nBins,minMass,maxMass))
L0_40_Targ_h = ROOT.gROOT.FindObject("L0_40_Targ_h")
L0_50_file.Get("ntuple").Draw(histoTitleTarg + ">>L0_50_Targ_h({0},{1},{2})".format(nBins,minMass,maxMass))
L0_50_Targ_h = ROOT.gROOT.FindObject("L0_50_Targ_h")
L0_60_file.Get("ntuple").Draw(histoTitleTarg + ">>L0_60_Targ_h({0},{1},{2})".format(nBins,minMass,maxMass))
L0_60_Targ_h = ROOT.gROOT.FindObject("L0_60_Targ_h")
L0_70_file.Get("ntuple").Draw(histoTitleTarg + ">>L0_70_Targ_h({0},{1},{2})".format(nBins,minMass,maxMass))
L0_70_Targ_h = ROOT.gROOT.FindObject("L0_70_Targ_h")
L0_80_file.Get("ntuple").Draw(histoTitleTarg + ">>L0_80_Targ_h({0},{1},{2})".format(nBins,minMass,maxMass))
L0_80_Targ_h = ROOT.gROOT.FindObject("L0_80_Targ_h")
L0_90_file.Get("ntuple").Draw(histoTitleTarg + ">>L0_90_Targ_h({0},{1},{2})".format(nBins,minMass,maxMass))
L0_90_Targ_h = ROOT.gROOT.FindObject("L0_90_Targ_h")

nom_15_file.Get("ntuple").Draw(histoTitleTarg + ">>nom_15_Targ_h({0},{1},{2})".format(nBins,minMass,maxMass))
nom_15_Targ_h = ROOT.gROOT.FindObject("nom_15_Targ_h")
nom_20_file.Get("ntuple").Draw(histoTitleTarg + ">>nom_20_Targ_h({0},{1},{2})".format(nBins,minMass,maxMass))
nom_20_Targ_h = ROOT.gROOT.FindObject("nom_20_Targ_h")
nom_30_file.Get("ntuple").Draw(histoTitleTarg + ">>nom_30_Targ_h({0},{1},{2})".format(nBins,minMass,maxMass))
nom_30_Targ_h = ROOT.gROOT.FindObject("nom_30_Targ_h")
nom_40_file.Get("ntuple").Draw(histoTitleTarg + ">>nom_40_Targ_h({0},{1},{2})".format(nBins,minMass,maxMass))
nom_40_Targ_h = ROOT.gROOT.FindObject("nom_40_Targ_h")
nom_50_file.Get("ntuple").Draw(histoTitleTarg + ">>nom_50_Targ_h({0},{1},{2})".format(nBins,minMass,maxMass))
nom_50_Targ_h = ROOT.gROOT.FindObject("nom_50_Targ_h")
nom_60_file.Get("ntuple").Draw(histoTitleTarg + ">>nom_60_Targ_h({0},{1},{2})".format(nBins,minMass,maxMass))
nom_60_Targ_h = ROOT.gROOT.FindObject("nom_60_Targ_h")
nom_70_file.Get("ntuple").Draw(histoTitleTarg + ">>nom_70_Targ_h({0},{1},{2})".format(nBins,minMass,maxMass))
nom_70_Targ_h = ROOT.gROOT.FindObject("nom_70_Targ_h")
nom_80_file.Get("ntuple").Draw(histoTitleTarg + ">>nom_80_Targ_h({0},{1},{2})".format(nBins,minMass,maxMass))
nom_80_Targ_h = ROOT.gROOT.FindObject("nom_80_Targ_h")
nom_90_file.Get("ntuple").Draw(histoTitleTarg + ">>nom_90_Targ_h({0},{1},{2})".format(nBins,minMass,maxMass))
nom_90_Targ_h = ROOT.gROOT.FindObject("nom_90_Targ_h")


massArr = array.array('d')
massArrErr = array.array('d')
L0UncArr = array.array('d')
nomUncArr = array.array('d')
L0TargArr = array.array('d')
nomTargArr = array.array('d')
L0UncArrErr = array.array('d')
nomUncArrErr = array.array('d')
L0TargArrErr = array.array('d')
nomTargArrErr = array.array('d')

#massArr.append(0.015)
massArr.append(0.020)
massArr.append(0.030)
massArr.append(0.040)
massArr.append(0.050)
massArr.append(0.060)
massArr.append(0.070)
massArr.append(0.080)
massArr.append(0.090)

for i in range(0,nMass):
    massArrErr.append(0)

c.Print("uncL0Fits.pdf[","Title:histoTitle")
L0_20_Unc_h.Fit("gaus","gaus","",0.01,0.025)
L0UncArr.append(L0_20_Unc_h.Fit("gaus","gaus","",0.01,0.025).Parameter(2))
L0UncArrErr.append(L0_20_Unc_h.Fit("gaus","gaus","",0.01,0.03).Get().ParError(2))
c.Print("uncL0Fits.pdf","Title:histoTitle")

L0_30_Unc_h.Fit("gaus","gaus","",0.02,0.035)
L0UncArr.append(L0_30_Unc_h.Fit("gaus","gaus","",0.02,0.035).Parameter(2))
L0UncArrErr.append(L0_30_Unc_h.Fit("gaus","gaus","",0.02,0.035).Get().ParError(2))
c.Print("uncL0Fits.pdf","Title:histoTitle")

L0_40_Unc_h.Fit("gaus","gaus","",0.03,0.05)
L0UncArr.append(L0_40_Unc_h.Fit("gaus","gaus","",0.03,0.05).Parameter(2))
L0UncArrErr.append(L0_40_Unc_h.Fit("gaus","gaus","",0.03,0.05).Get().ParError(2))
c.Print("uncL0Fits.pdf","Title:histoTitle")

L0_50_Unc_h.Fit("gaus","gaus","",0.04,0.06)
L0UncArr.append(L0_50_Unc_h.Fit("gaus","gaus","",0.04,0.06).Parameter(2))
L0UncArrErr.append(L0_50_Unc_h.Fit("gaus","gaus","",0.04,0.06).Get().ParError(2))
c.Print("uncL0Fits.pdf","Title:histoTitle")

L0_60_Unc_h.Fit("gaus","gaus","",0.05,0.07)
L0UncArr.append(L0_60_Unc_h.Fit("gaus","gaus","",0.05,0.07).Parameter(2))
L0UncArrErr.append(L0_60_Unc_h.Fit("gaus","gaus","",0.05,0.07).Get().ParError(2))
c.Print("uncL0Fits.pdf","Title:histoTitle")

L0_70_Unc_h.Fit("gaus","gaus","",0.06,0.08)
L0UncArr.append(L0_70_Unc_h.Fit("gaus","gaus","",0.06,0.08).Parameter(2))
L0UncArrErr.append(L0_70_Unc_h.Fit("gaus","gaus","",0.06,0.08).Get().ParError(2))
c.Print("uncL0Fits.pdf","Title:histoTitle")

L0_80_Unc_h.Fit("gaus","gaus","",0.07,0.09)
L0UncArr.append(L0_80_Unc_h.Fit("gaus","gaus","",0.07,0.09).Parameter(2))
L0UncArrErr.append(L0_80_Unc_h.Fit("gaus","gaus","",0.07,0.09).Get().ParError(2))
c.Print("uncL0Fits.pdf","Title:histoTitle")

L0_90_Unc_h.Fit("gaus","gaus","",0.08,0.105)
L0UncArr.append(L0_90_Unc_h.Fit("gaus","gaus","",0.08,0.105).Parameter(2))
L0UncArrErr.append(L0_90_Unc_h.Fit("gaus","gaus","",0.08,0.105).Get().ParError(2))
c.Print("uncL0Fits.pdf","Title:histoTitle")

c.Print("uncL0Fits.pdf]","Title:histoTitle")

c.Print("uncnomFits.pdf[","Title:histoTitle")
nom_20_Unc_h.Fit("gaus","gaus","",0.01,0.025)
nomUncArr.append(nom_20_Unc_h.Fit("gaus","gaus","",0.01,0.025).Parameter(2))
nomUncArrErr.append(nom_20_Unc_h.Fit("gaus","gaus","",0.01,0.025).Get().ParError(2))
c.Print("uncnomFits.pdf","Title:histoTitle")

nom_30_Unc_h.Fit("gaus","gaus","",0.02,0.035)
nomUncArr.append(nom_30_Unc_h.Fit("gaus","gaus","",0.02,0.035).Parameter(2))
nomUncArrErr.append(nom_30_Unc_h.Fit("gaus","gaus","",0.02,0.035).Get().ParError(2))
c.Print("uncnomFits.pdf","Title:histoTitle")

nom_40_Unc_h.Fit("gaus","gaus","",0.03,0.05)
nomUncArr.append(nom_40_Unc_h.Fit("gaus","gaus","",0.03,0.05).Parameter(2))
nomUncArrErr.append(nom_40_Unc_h.Fit("gaus","gaus","",0.03,0.05).Get().ParError(2))
c.Print("uncnomFits.pdf","Title:histoTitle")

nom_50_Unc_h.Fit("gaus","gaus","",0.04,0.06)
nomUncArr.append(nom_50_Unc_h.Fit("gaus","gaus","",0.04,0.06).Parameter(2))
nomUncArrErr.append(nom_50_Unc_h.Fit("gaus","gaus","",0.04,0.06).Get().ParError(2))
c.Print("uncnomFits.pdf","Title:histoTitle")

nom_60_Unc_h.Fit("gaus","gaus","",0.05,0.07)
nomUncArr.append(nom_60_Unc_h.Fit("gaus","gaus","",0.05,0.07).Parameter(2))
nomUncArrErr.append(nom_60_Unc_h.Fit("gaus","gaus","",0.05,0.07).Get().ParError(2))
c.Print("uncnomFits.pdf","Title:histoTitle")

nom_70_Unc_h.Fit("gaus","gaus","",0.06,0.08)
nomUncArr.append(nom_70_Unc_h.Fit("gaus","gaus","",0.06,0.08).Parameter(2))
nomUncArrErr.append(nom_70_Unc_h.Fit("gaus","gaus","",0.06,0.08).Get().ParError(2))
c.Print("uncnomFits.pdf","Title:histoTitle")

nom_80_Unc_h.Fit("gaus","gaus","",0.07,0.09)
nomUncArr.append(nom_80_Unc_h.Fit("gaus","gaus","",0.07,0.09).Parameter(2))
nomUncArrErr.append(nom_80_Unc_h.Fit("gaus","gaus","",0.07,0.09).Get().ParError(2))
c.Print("uncnomFits.pdf","Title:histoTitle")

nom_90_Unc_h.Fit("gaus","gaus","",0.08,0.105)
nomUncArr.append(nom_90_Unc_h.Fit("gaus","gaus","",0.08,0.105).Parameter(2))
nomUncArrErr.append(nom_90_Unc_h.Fit("gaus","gaus","",0.08,0.105).Get().ParError(2))
c.Print("uncnomFits.pdf","Title:histoTitle")

c.Print("uncnomFits.pdf]","Title:histoTitle")



c.Print("TargL0Fits.pdf[","Title:histoTitle")
L0_20_Targ_h.Fit("gaus","gaus","",0.015,0.022)
L0TargArr.append(L0_20_Targ_h.Fit("gaus","gaus","",0.01,0.03).Parameter(2))
L0TargArrErr.append(L0_20_Targ_h.Fit("gaus","gaus","",0.01,0.03).Get().ParError(2))
c.Print("TargL0Fits.pdf","Title:histoTitle")

L0_30_Targ_h.Fit("gaus","gaus","",0.02,0.04)
L0TargArr.append(L0_30_Targ_h.Fit("gaus","gaus","",0.02,0.04).Parameter(2))
L0TargArrErr.append(L0_30_Targ_h.Fit("gaus","gaus","",0.02,0.04).Get().ParError(2))
c.Print("TargL0Fits.pdf","Title:histoTitle")

L0_40_Targ_h.Fit("gaus","gaus","",0.03,0.05)
L0TargArr.append(L0_40_Targ_h.Fit("gaus","gaus","",0.03,0.05).Parameter(2))
L0TargArrErr.append(L0_40_Targ_h.Fit("gaus","gaus","",0.03,0.05).Get().ParError(2))
c.Print("TargL0Fits.pdf","Title:histoTitle")

L0_50_Targ_h.Fit("gaus","gaus","",0.04,0.06)
L0TargArr.append(L0_50_Targ_h.Fit("gaus","gaus","",0.04,0.06).Parameter(2))
L0TargArrErr.append(L0_50_Targ_h.Fit("gaus","gaus","",0.04,0.06).Get().ParError(2))
c.Print("TargL0Fits.pdf","Title:histoTitle")

L0_60_Targ_h.Fit("gaus","gaus","",0.05,0.07)
L0TargArr.append(L0_60_Targ_h.Fit("gaus","gaus","",0.05,0.07).Parameter(2))
L0TargArrErr.append(L0_60_Targ_h.Fit("gaus","gaus","",0.05,0.07).Get().ParError(2))
c.Print("TargL0Fits.pdf","Title:histoTitle")

L0_70_Targ_h.Fit("gaus","gaus","",0.06,0.08)
L0TargArr.append(L0_70_Targ_h.Fit("gaus","gaus","",0.06,0.08).Parameter(2))
L0TargArrErr.append(L0_70_Targ_h.Fit("gaus","gaus","",0.06,0.08).Get().ParError(2))
c.Print("TargL0Fits.pdf","Title:histoTitle")

L0_80_Targ_h.Fit("gaus","gaus","",0.07,0.09)
L0TargArr.append(L0_80_Targ_h.Fit("gaus","gaus","",0.07,0.09).Parameter(2))
L0TargArrErr.append(L0_80_Targ_h.Fit("gaus","gaus","",0.07,0.09).Get().ParError(2))
c.Print("TargL0Fits.pdf","Title:histoTitle")

L0_90_Targ_h.Fit("gaus","gaus","",0.08,0.10)
L0TargArr.append(L0_90_Targ_h.Fit("gaus","gaus","",0.08,0.10).Parameter(2))
L0TargArrErr.append(L0_90_Targ_h.Fit("gaus","gaus","",0.08,0.10).Get().ParError(2))
c.Print("TargL0Fits.pdf","Title:histoTitle")

c.Print("TargL0Fits.pdf]","Title:histoTitle")

c.Print("TargnomFits.pdf[","Title:histoTitle")
nom_20_Targ_h.Fit("gaus","gaus","",0.015,0.022)
nomTargArr.append(nom_20_Targ_h.Fit("gaus","gaus","",0.01,0.03).Parameter(2))
nomTargArrErr.append(nom_20_Targ_h.Fit("gaus","gaus","",0.01,0.03).Get().ParError(2))
c.Print("TargnomFits.pdf","Title:histoTitle")

nom_30_Targ_h.Fit("gaus","gaus","",0.02,0.04)
nomTargArr.append(nom_30_Targ_h.Fit("gaus","gaus","",0.02,0.04).Parameter(2))
nomTargArrErr.append(nom_30_Targ_h.Fit("gaus","gaus","",0.02,0.04).Get().ParError(2))
c.Print("TargnomFits.pdf","Title:histoTitle")

nom_40_Targ_h.Fit("gaus","gaus","",0.03,0.05)
nomTargArr.append(nom_40_Targ_h.Fit("gaus","gaus","",0.03,0.05).Parameter(2))
nomTargArrErr.append(nom_40_Targ_h.Fit("gaus","gaus","",0.03,0.05).Get().ParError(2))
c.Print("TargnomFits.pdf","Title:histoTitle")

nom_50_Targ_h.Fit("gaus","gaus","",0.04,0.06)
nomTargArr.append(nom_50_Targ_h.Fit("gaus","gaus","",0.04,0.06).Parameter(2))
nomTargArrErr.append(nom_50_Targ_h.Fit("gaus","gaus","",0.04,0.06).Get().ParError(2))
c.Print("TargnomFits.pdf","Title:histoTitle")

nom_60_Targ_h.Fit("gaus","gaus","",0.05,0.07)
nomTargArr.append(nom_60_Targ_h.Fit("gaus","gaus","",0.05,0.07).Parameter(2))
nomTargArrErr.append(nom_60_Targ_h.Fit("gaus","gaus","",0.05,0.07).Get().ParError(2))
c.Print("TargnomFits.pdf","Title:histoTitle")

nom_70_Targ_h.Fit("gaus","gaus","",0.06,0.08)
nomTargArr.append(nom_70_Targ_h.Fit("gaus","gaus","",0.06,0.08).Parameter(2))
nomTargArrErr.append(nom_70_Targ_h.Fit("gaus","gaus","",0.06,0.08).Get().ParError(2))
c.Print("TargnomFits.pdf","Title:histoTitle")

nom_80_Targ_h.Fit("gaus","gaus","",0.07,0.09)
nomTargArr.append(nom_80_Targ_h.Fit("gaus","gaus","",0.07,0.09).Parameter(2))
nomTargArrErr.append(nom_80_Targ_h.Fit("gaus","gaus","",0.07,0.09).Get().ParError(2))
c.Print("TargnomFits.pdf","Title:histoTitle")

nom_90_Targ_h.Fit("gaus","gaus","",0.08,0.10)
nomTargArr.append(nom_90_Targ_h.Fit("gaus","gaus","",0.08,0.10).Parameter(2))
nomTargArrErr.append(nom_90_Targ_h.Fit("gaus","gaus","",0.08,0.10).Get().ParError(2))
c.Print("TargnomFits.pdf","Title:histoTitle")

c.Print("TargnomFits.pdf]","Title:histoTitle")


GraphL0Unc = TGraphErrors(nMass,massArr,L0UncArr,massArrErr,L0UncArrErr)
GraphNomUnc = TGraphErrors(nMass,massArr,nomUncArr,massArrErr,nomUncArrErr)
GraphL0Targ = TGraphErrors(nMass,massArr,L0TargArr,massArrErr,L0TargArrErr)
GraphNomTarg = TGraphErrors(nMass,massArr,nomTargArr,massArrErr,nomTargArrErr)

c.Clear()

legend = TLegend(.18,.66,.42,.87)
legend.SetBorderSize(0)
legend.SetFillColor(0)
legend.SetFillStyle(0)
legend.SetTextFont(42)
legend.SetTextSize(0.035)
legend.AddEntry(GraphL0Unc,"L0","LP")
legend.AddEntry(GraphNomUnc,"nominal","LP")

GraphNomUnc.Draw("")
GraphNomUnc.GetXaxis().SetRangeUser(minMass,maxMass)
GraphNomUnc.GetYaxis().SetRangeUser(0,0.005)
GraphNomUnc.SetTitle("Unconstrained Invariant Mass Resolution Prompt A's")
GraphNomUnc.GetXaxis().SetTitle("mass [GeV]")
GraphNomUnc.GetYaxis().SetTitle("mass resolution [GeV]")
GraphL0Unc.Draw("same")
GraphL0Unc.SetLineColor(2)

gStyle.SetOptStat(0)

legend.Draw()
c.Print("uncInvMass.pdf","Title:histoTitle")

c.Clear()

GraphNomTarg.Draw("")
GraphNomTarg.GetXaxis().SetRangeUser(minMass,maxMass)
GraphNomTarg.GetYaxis().SetRangeUser(0,0.005)
GraphNomTarg.SetTitle("Target Constrained Invariant Mass Resolution Prompt A's")
GraphNomTarg.GetXaxis().SetTitle("mass [GeV]")
GraphNomTarg.GetYaxis().SetTitle("mass resolution [GeV]")
GraphL0Targ.Draw("same")
GraphL0Targ.SetLineColor(2)

gStyle.SetOptStat(0)

legend.Draw()
c.Print("targInvMass.pdf","Title:histoTitle")
