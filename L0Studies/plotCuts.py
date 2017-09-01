#!/usr/bin/env python
import sys
tmpargv = sys.argv
sys.argv = []
import getopt
import ROOT
from ROOT import gROOT, TFile, TTree, TChain, gDirectory, TLine, gStyle, TCanvas, TLegend, TH1F
sys.argv = tmpargv

def print_usage():
    print "\nUsage: {0} <output pdf file base name> <input L0 ROOT file name> <input nominal ROOT file name>".format(sys.argv[0])
    print "Arguments: "
    print '\t-h: this help message'
    print

ebeam=1.056
clusterT = 43.0
targetZ = -5.0
energy = "1pt05"
mass = "40"

gStyle.SetOptStat(0)
c = TCanvas("c","c",800,600);

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'hm:e:')

# Parse the command line arguments
for opt, arg in options:
	if opt=='-m':
	    mass=str(arg)
	if opt=='-e':
	    energy=str(arg)
        if opt=='-h':
            print_usage()
            sys.exit(0)

outfile = "/home/mrsolt/hps/L0Studies/figs/" + energy + "/cuts/cuts_" + mass + "_MeV"

L0_truth_file = TFile("/home/mrsolt/hps/L0Studies/L0/" + energy + "/ap/truth/ap_1pt05_" + mass + "MeV_truth.root")
nominal_truth_file = TFile("/home/mrsolt/hps/L0Studies/nominal/" + energy + "/ap/truth/apsignal_slic_displaced_" + mass + "_dq_truth.root")

L0_tri_file = TFile("/home/mrsolt/hps/L0Studies/L0/" + energy + "/ap/ap_" + mass + "MeV.root")
nominal_tri_file = TFile("/home/mrsolt/hps/L0Studies/nominal/" + energy + "/ap/ap_" + mass + "MeV.root")

MatchChi2_cut = "max(eleMatchChisq,posMatchChisq)<10"
Tdiff_cut = "max(abs(eleClT-eleTrkT-{0}),abs(posClT-posTrkT-{0}))<4".format(clusterT)
ClT_cut = "abs(eleClT-posClT)<2"
Oppo_cut = "eleClY*posClY<0"
BscChi2_cut = "bscChisq<10"
Chi2Diff_cut = "bscChisq-uncChisq<5"
TrkChi2_cut = "max(eleTrkChisq,posTrkChisq)<30"
Iso_cut = "min(eleMinPositiveIso+0.5*(eleTrkZ0+{0}*elePY/eleP)*sign(elePY),posMinPositiveIso+0.5*(posTrkZ0+{0}*posPY/posP)*sign(posPY))>0".format(targetZ)
Passym_cut = "abs(eleP-posP)/(eleP+posP)<0.4"
PosD0_cut = "posTrkD0+{0}*posPX/posP<1.5".format(targetZ)
eleP_cut = "eleP<{0}*0.75".format(ebeam)
uncP_cut = "uncP<{0}*1.15".format(ebeam)
L1L1_L0_cut = "(eleHasL1&&posHasL1)||(eleHasL1&&!posHasL1&&posHasL2)||(!eleHasL1&&eleHasL2&&posHasL1)"
L1L1_nominal_cut = "eleHasL1&&posHasL1"
L1L2_L0_cut = "(!eleHasL1&&!posHasL1&&eleHasL2&&!posHasL2)||(!eleHasL1&&!posHasL1&&!eleHasL2&&posHasL2)||(eleHasL1&&!posHasL1&!posHasL2)||(!eleHasL1&&!eleHasL2&posHasL1)"
L1L2_nominal_cut = "(eleHasL1&&!posHasL1)||(!eleHasL1&&posHasL1)"
L2L2_L0_cut = "!eleHasL1&&!posHasL1&&!eleHasL2&&!posHasL2"
L2L2_nominal_cut = "!eleHasL1&&!posHasL1"

L0_truth_file.Get("ntuple").Draw("triEndZ>>L0_truth_h(170.,-20.,150.)")
L0_truth_h = ROOT.gROOT.FindObject("L0_truth_h")
nominal_truth_file.Get("ntuple").Draw("triEndZ>>nominal_truth_h(170.,-20.,150.)")
nominal_truth_h = ROOT.gROOT.FindObject("nominal_truth_h")

L0_tri_file.Get("ntuple").Draw("triEndZ>>L0_MatchChi2(170.,-20.,150.)",MatchChi2_cut)
L0_MatchChi2 = ROOT.gROOT.FindObject("L0_MatchChi2")
nominal_tri_file.Get("ntuple").Draw("triEndZ>>nominal_MatchChi2(170.,-20.,150.)",MatchChi2_cut)
nominal_MatchChi2 = ROOT.gROOT.FindObject("nominal_MatchChi2")

L0_tri_file.Get("ntuple").Draw("triEndZ>>L0_Tdiff(170.,-20.,150.)",Tdiff_cut)
L0_Tdiff = ROOT.gROOT.FindObject("L0_Tdiff")
nominal_tri_file.Get("ntuple").Draw("triEndZ>>nominal_Tdiff(170.,-20.,150.)",Tdiff_cut)
nominal_Tdiff = ROOT.gROOT.FindObject("nominal_Tdiff")

L0_tri_file.Get("ntuple").Draw("triEndZ>>L0_ClT(170.,-20.,150.)",ClT_cut)
L0_ClT = ROOT.gROOT.FindObject("L0_ClT")
nominal_tri_file.Get("ntuple").Draw("triEndZ>>nominal_ClT(170.,-20.,150.)",ClT_cut)
nominal_ClT = ROOT.gROOT.FindObject("nominal_ClT")

L0_tri_file.Get("ntuple").Draw("triEndZ>>L0_Oppo(170.,-20.,150.)",Oppo_cut)
L0_Oppo = ROOT.gROOT.FindObject("L0_Oppo")
nominal_tri_file.Get("ntuple").Draw("triEndZ>>nominal_Oppo(170.,-20.,150.)",Oppo_cut)
nominal_Oppo = ROOT.gROOT.FindObject("nominal_Oppo")

L0_tri_file.Get("ntuple").Draw("triEndZ>>L0_BscChi2(170.,-20.,150.)",BscChi2_cut)
L0_BscChi2 = ROOT.gROOT.FindObject("L0_BscChi2")
nominal_tri_file.Get("ntuple").Draw("triEndZ>>nominal_BscChi2(170.,-20.,150.)",BscChi2_cut)
nominal_BscChi2 = ROOT.gROOT.FindObject("nominal_BscChi2")

L0_tri_file.Get("ntuple").Draw("triEndZ>>L0_Chi2Diff(170.,-20.,150.)",Chi2Diff_cut)
L0_Chi2Diff = ROOT.gROOT.FindObject("L0_Chi2Diff")
nominal_tri_file.Get("ntuple").Draw("triEndZ>>nominal_Chi2Diff(170.,-20.,150.)",Chi2Diff_cut)
nominal_Chi2Diff = ROOT.gROOT.FindObject("nominal_Chi2Diff")

L0_tri_file.Get("ntuple").Draw("triEndZ>>L0_TrkChi2(170.,-20.,150.)",TrkChi2_cut)
L0_TrkChi2 = ROOT.gROOT.FindObject("L0_TrkChi2")
nominal_tri_file.Get("ntuple").Draw("triEndZ>>nominal_TrkChi2(170.,-20.,150.)",TrkChi2_cut)
nominal_TrkChi2 = ROOT.gROOT.FindObject("nominal_TrkChi2")

L0_tri_file.Get("ntuple").Draw("triEndZ>>L0_Iso(170.,-20.,150.)",Iso_cut)
L0_Iso = ROOT.gROOT.FindObject("L0_Iso")
nominal_tri_file.Get("ntuple").Draw("triEndZ>>nominal_Iso(170.,-20.,150.)",Iso_cut)
nominal_Iso = ROOT.gROOT.FindObject("nominal_Iso")

L0_tri_file.Get("ntuple").Draw("triEndZ>>L0_Passym(170.,-20.,150.)",Passym_cut)
L0_Passym = ROOT.gROOT.FindObject("L0_Passym")
nominal_tri_file.Get("ntuple").Draw("triEndZ>>nominal_Passym(170.,-20.,150.)",Passym_cut)
nominal_Passym = ROOT.gROOT.FindObject("nominal_Passym")

L0_tri_file.Get("ntuple").Draw("triEndZ>>L0_PosD0(170.,-20.,150.)",PosD0_cut)
L0_PosD0 = ROOT.gROOT.FindObject("L0_PosD0")
nominal_tri_file.Get("ntuple").Draw("triEndZ>>nominal_PosD0(170.,-20.,150.)",PosD0_cut)
nominal_PosD0 = ROOT.gROOT.FindObject("nominal_PosD0")

L0_tri_file.Get("ntuple").Draw("triEndZ>>L0_eleP(170.,-20.,150.)",eleP_cut)
L0_eleP = ROOT.gROOT.FindObject("L0_eleP")
nominal_tri_file.Get("ntuple").Draw("triEndZ>>nominal_eleP(170.,-20.,150.)",eleP_cut)
nominal_eleP = ROOT.gROOT.FindObject("nominal_eleP")

L0_tri_file.Get("ntuple").Draw("triEndZ>>L0_uncP(170.,-20.,150.)",uncP_cut)
L0_uncP = ROOT.gROOT.FindObject("L0_uncP")
nominal_tri_file.Get("ntuple").Draw("triEndZ>>nominal_uncP(170.,-20.,150.)",uncP_cut)
nominal_uncP = ROOT.gROOT.FindObject("nominal_uncP")

L0_tri_file.Get("ntuple").Draw("triEndZ>>L0_L1L1(170.,-20.,150.)",L1L1_L0_cut)
L0_L1L1 = ROOT.gROOT.FindObject("L0_L1L1")
nominal_tri_file.Get("ntuple").Draw("triEndZ>>nominal_L1L1(170.,-20.,150.)",L1L1_nominal_cut)
nominal_L1L1 = ROOT.gROOT.FindObject("nominal_L1L1")

L0_tri_file.Get("ntuple").Draw("triEndZ>>L0_L1L2(170.,-20.,150.)",L1L2_L0_cut)
L0_L1L2 = ROOT.gROOT.FindObject("L0_L1L2")
nominal_tri_file.Get("ntuple").Draw("triEndZ>>nominal_L1L2(170.,-20.,150.)",L1L2_nominal_cut)
nominal_L1L2 = ROOT.gROOT.FindObject("nominal_L1L2")

L0_tri_file.Get("ntuple").Draw("triEndZ>>L0_L2L2(170.,-20.,150.)",L2L2_L0_cut)
L0_L2L2 = ROOT.gROOT.FindObject("L0_L2L2")
nominal_tri_file.Get("ntuple").Draw("triEndZ>>nominal_L2L2(170.,-20.,150.)",L2L2_nominal_cut)
nominal_L2L2 = ROOT.gROOT.FindObject("nominal_L2L2")




def ratio(tri,histo):
    ratio_h = TH1F("ratio_h",str(histo),170,-20,150)
    for i in range(tri.GetNbinsX()):
        if(tri.GetBinContent(i+1) != 0):
	    ratio_h.SetBinContent(i+1,(histo.GetBinContent(i+1))/float(tri.GetBinContent(i+1)))
        else: ratio_h.SetBinContent(i+1,0)
    return ratio_h

ratio_L0_assym = ratio(L0_truth_h,L0_Passym)
ratio_L0_bscChi2 = ratio(L0_truth_h,L0_BscChi2)
ratio_L0_Chi2diff = ratio(L0_truth_h,L0_Chi2Diff)
ratio_L0_ClTdiff = ratio(L0_truth_h,L0_Tdiff)
ratio_L0_ClT = ratio(L0_truth_h,L0_Tdiff)
ratio_L0_eleP = ratio(L0_truth_h,L0_eleP)
ratio_L0_iso = ratio(L0_truth_h,L0_Iso)
ratio_L0_matchChi2 = ratio(L0_truth_h,L0_MatchChi2)
ratio_L0_oppo = ratio(L0_truth_h,L0_Oppo)
ratio_L0_posD0 = ratio(L0_truth_h,L0_PosD0)
ratio_L0_trkChi2 = ratio(L0_truth_h,L0_TrkChi2)
ratio_L0_uncP = ratio(L0_truth_h,L0_uncP)
ratio_L0_L1L1 = ratio(L0_truth_h,L0_L1L1)
ratio_L0_L1L2 = ratio(L0_truth_h,L0_L1L2)
ratio_L0_L2L2 = ratio(L0_truth_h,L0_L2L2)

ratio_nominal_assym = ratio(nominal_truth_h,nominal_Passym)
ratio_nominal_bscChi2 = ratio(nominal_truth_h,nominal_BscChi2)
ratio_nominal_Chi2diff = ratio(nominal_truth_h,nominal_Chi2Diff)
ratio_nominal_ClTdiff = ratio(nominal_truth_h,nominal_Tdiff)
ratio_nominal_ClT = ratio(nominal_truth_h,nominal_Tdiff)
ratio_nominal_eleP = ratio(nominal_truth_h,nominal_eleP)
ratio_nominal_iso = ratio(nominal_truth_h,nominal_Iso)
ratio_nominal_matchChi2 = ratio(nominal_truth_h,nominal_MatchChi2)
ratio_nominal_oppo = ratio(nominal_truth_h,nominal_Oppo)
ratio_nominal_posD0 = ratio(nominal_truth_h,nominal_PosD0)
ratio_nominal_trkChi2 = ratio(nominal_truth_h,nominal_TrkChi2)
ratio_nominal_uncP = ratio(nominal_truth_h,nominal_uncP)
ratio_nominal_L1L1 = ratio(nominal_truth_h,nominal_L1L1)
ratio_nominal_L1L2 = ratio(nominal_truth_h,nominal_L1L2)
ratio_nominal_L2L2 = ratio(nominal_truth_h,nominal_L2L2)

legend = TLegend(.68,.66,.92,.87)
legend.SetBorderSize(0)
legend.SetFillColor(0)
legend.SetFillStyle(0)
legend.SetTextFont(42)
legend.SetTextSize(0.035)
legend.AddEntry(ratio_L0_assym,"L0","LP")
legend.AddEntry(ratio_nominal_assym,"nominal","LP")

c.Print(outfile+".pdf[")

def plot(histo1,histo2,outfile,legend):
    histo1.Draw("")
    histo1.SetTitle(str(histo1))
    histo2.Draw("same")
    histo2.SetLineColor(1)
    legend.Draw("same")
    c.Print(outfile+".pdf","Title:plot")

plot(ratio_L0_assym,ratio_nominal_assym,outfile,legend)
plot(ratio_L0_bscChi2,ratio_nominal_bscChi2,outfile,legend)
plot(ratio_L0_Chi2diff,ratio_nominal_Chi2diff,outfile,legend)
plot(ratio_L0_ClTdiff,ratio_nominal_ClTdiff,outfile,legend)
plot(ratio_L0_ClT,ratio_nominal_ClT,outfile,legend)
plot(ratio_L0_eleP,ratio_nominal_eleP,outfile,legend)
plot(ratio_L0_iso,ratio_nominal_iso,outfile,legend)
plot(ratio_L0_matchChi2,ratio_nominal_matchChi2,outfile,legend)
plot(ratio_L0_oppo,ratio_nominal_oppo,outfile,legend)
plot(ratio_L0_posD0,ratio_nominal_posD0,outfile,legend)
plot(ratio_L0_trkChi2,ratio_nominal_trkChi2,outfile,legend)
plot(ratio_L0_uncP,ratio_nominal_uncP,outfile,legend)
plot(ratio_L0_L1L1,ratio_nominal_L1L1,outfile,legend)
plot(ratio_L0_L1L2,ratio_nominal_L1L2,outfile,legend)
plot(ratio_L0_L2L2,ratio_nominal_L2L2,outfile,legend)


c.Print(outfile+".pdf]")
