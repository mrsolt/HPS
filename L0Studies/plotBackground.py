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
#normL0 = 30.
normL0 = 10.
normnom = 10.

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

outfile = "/home/mrsolt/hps/L0Studies/figs/" + energy + "/background/wabbeamtri-5mrad/"

L0_file = TFile("/home/mrsolt/hps/L0Studies/L0/" + energy + "/wab-beam-tri-5mrad/wab-beam-tri-5mrad.root")
nominal_file = TFile("/home/mrsolt/hps/L0Studies/nominal/" + energy + "/wab-beam-tri-5mrad/wab-beam-tri-5mrad.root")

#cut_nom = "bscChisq<10&&min(eleMinPositiveIso+0.5*(eleTrkZ0+{0}*elePY/eleP)*sign(elePY),posMinPositiveIso+0.5*(posTrkZ0+{0}*posPY/posP)*sign(posPY))>0&&eleClY*posClY<0".format(targetZ)
#cut_L0 = "bscChisq<10&&min(eleMinPositiveIso+0.5*(eleTrkZ0+{0}*elePY/eleP)*sign(elePY),posMinPositiveIso+0.5*(posTrkZ0+{0}*posPY/posP)*sign(posPY))>0&&eleClY*posClY<0".format(targetZ)
cut_nom = "bscChisq<10&&min(eleMinPositiveIso+0.5*(eleTrkZ0+{0}*elePY/eleP)*sign(elePY),posMinPositiveIso+0.5*(posTrkZ0+{0}*posPY/posP)*sign(posPY))>0".format(targetZ)
cut_L0 = "bscChisq<10&&min(eleMinPositiveIso+0.5*(eleTrkZ0+{0}*elePY/eleP)*sign(elePY),posMinPositiveIso+0.5*(posTrkZ0+{0}*posPY/posP)*sign(posPY))>0".format(targetZ)

vertCut = "isPair1&&eleHasL1&&posHasL1&&max(eleMatchChisq,posMatchChisq)<10&&max(abs(eleClT-eleTrkT-{1}),abs(posClT-posTrkT-{1}))<4&&abs(eleClT-posClT)<2&&eleClY*posClY<0&&bscChisq<10&&bscChisq-uncChisq<5&&max(eleTrkChisq,posTrkChisq)<30&&min(eleMinPositiveIso+0.5*(eleTrkZ0+{2}*elePY/eleP)*sign(elePY),posMinPositiveIso+0.5*(posTrkZ0+{2}*posPY/posP)*sign(posPY))>0&&abs(eleP-posP)/(eleP+posP)<0.4&&posTrkD0+{2}*posPX/posP<1.5&&eleP<{0}*0.75&&uncP<{0}*1.15".format(ebeam,clusterT,targetZ)

#cut_L0 = vertCut
#cut_nom = vertCut

L0_file.Get("ntuple").Draw("uncVZ>>L0_uncVZ(100,-20,150)",cut_L0)
L0_uncVZ = ROOT.gROOT.FindObject("L0_uncVZ")
L0_file.Get("ntuple").Draw("eleClE+posClE>>L0_ESum(100,0,{0})".format(ebeam*1.3),cut_L0)
L0_ESum = ROOT.gROOT.FindObject("L0_ESum")
L0_file.Get("ntuple").Draw("posTrkLambda>>L0_posLambda(100,-0.1,0.1)",cut_L0)
L0_posLambda = ROOT.gROOT.FindObject("L0_posLambda")
L0_file.Get("ntuple").Draw("eleTrkLambda>>L0_eleLambda(100,-0.1,0.1)",cut_L0)
L0_eleLambda = ROOT.gROOT.FindObject("L0_eleLambda")

nominal_file.Get("ntuple").Draw("uncVZ>>nom_uncVZ(100,-20,150)",cut_nom)
nom_uncVZ = ROOT.gROOT.FindObject("nom_uncVZ")
nominal_file.Get("ntuple").Draw("eleClE+posClE>>nom_ESum(100,0,{0})".format(ebeam*1.3),cut_nom)
nom_ESum = ROOT.gROOT.FindObject("nom_ESum")
nominal_file.Get("ntuple").Draw("posTrkLambda>>nom_posLambda(100,-0.1,0.1)",cut_nom)
nom_posLambda = ROOT.gROOT.FindObject("nom_posLambda")
nominal_file.Get("ntuple").Draw("eleTrkLambda>>nom_eleLambda(100,-0.1,0.1)",cut_nom)
nom_eleLambda = ROOT.gROOT.FindObject("nom_eleLambda")

L0_uncVZ.Scale(1./normL0)
L0_ESum.Scale(1./normL0)
L0_posLambda.Scale(1./normL0)
L0_eleLambda.Scale(1./normL0)

nom_uncVZ.Scale(1./normnom)
nom_ESum.Scale(1./normnom)
nom_posLambda.Scale(1./normnom)
nom_eleLambda.Scale(1./normnom)

legend = TLegend(.68,.66,.92,.87)
legend.SetBorderSize(0)
legend.SetFillColor(0)
legend.SetFillStyle(0)
legend.SetTextFont(42)
legend.SetTextSize(0.035)
legend.AddEntry(L0_uncVZ,"L0","LP")
legend.AddEntry(nom_uncVZ,"nominal","LP")

c.Print(outfile+".pdf[")

def plot(histo1,histo2,outfile,legend):
    histo1.Draw("")
    histo1.SetTitle(str(histo1))
    histo2.Draw("same")
    histo2.SetLineColor(2)
    legend.Draw("same")
    c.Print(outfile+".pdf","Title:plot")

plot(L0_uncVZ,nom_uncVZ,outfile,legend)
c.SetLogy(1)
plot(L0_uncVZ,nom_uncVZ,outfile,legend)
c.SetLogy(0)
plot(L0_ESum,nom_ESum,outfile,legend)
plot(L0_posLambda,nom_posLambda,outfile,legend)
plot(L0_eleLambda,nom_eleLambda,outfile,legend)

c.Print(outfile+".pdf]")

c.Clear()

L0_uncVZ.Draw("")
L0_uncVZ.SetTitle("Vertex Z Vertexing Cuts")
L0_uncVZ.GetXaxis().SetTitle("z [mm]")
nom_uncVZ.Draw("same")
nom_uncVZ.SetLineColor(2)
legend.Draw("same")
c.SetLogy(1)
c.Print("log_uncVZ_vertcuts.pdf","Title:plot")

c.Clear()
c.SetLogy(0)

L0_ESum.Draw("")
L0_ESum.SetTitle("Energy Sum Minimal Cuts")
L0_ESum.GetXaxis().SetTitle("E Sum [GeV]")
#L0_ESum.GetYaxis().SetRangeUser(0,35)
nom_ESum.Draw("same")
nom_ESum.SetLineColor(2)
legend.Draw("same")
c.Print("Esum.pdf","Title:plot")

L0_eleLambda.Draw("")
L0_eleLambda.SetTitle("Electron TanLambda Minimal Cuts")
L0_eleLambda.GetXaxis().SetTitle("E Sum [GeV]")
nom_eleLambda.Draw("same")
nom_eleLambda.SetLineColor(2)
legend.Draw("same")
c.Print("eleLambda.pdf","Title:plot")
