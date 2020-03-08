import sys
tmpargv = sys.argv
sys.argv = []
import getopt
import ROOT
from ROOT import gROOT, TFile, TTree, TChain, gDirectory, TLine, gStyle, TCanvas, TLegend, TH1F
sys.argv = tmpargv

#List arguments
def print_usage():
    print "\nUsage: {0} <output file base name> <input Data text file> <input MC text file> <input 100 MeV A' file>".format(sys.argv[0])
    print '\t-z: target position (default -4.3 mm)'
    print '\t-h: this help message'
    print

zTarg = -4.3

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'z:h')

# Parse the command line arguments
for opt, arg in options:
		if opt=='-z':
			zTarg = float(arg)
		if opt=='-h':
			print_usage()
			sys.exit(0)

gStyle.SetOptStat(0)
c = TCanvas("c","c",800,600)

def openPDF(outfile,canvas):
	c.Print(outfile+".pdf[")

def closePDF(outfile,canvas):
	c.Print(outfile+".pdf]")

outfile = remainder[0]
outfileroot = TFile(remainder[0]+".root","RECREATE")

datafile = open(remainder[1],"r")
dataFiles = []

for line in (raw.strip().split() for raw in datafile):
	dataFiles.append(line[0])
dataevents = TChain("ntuple")
for i in range(len(dataFiles)):
    dataevents.Add(dataFiles[i])

mcfile = open(remainder[2],"r")
mcFiles = []

for line in (raw.strip().split() for raw in mcfile):
	mcFiles.append(line[0])
mcevents = TChain("ntuple")
for i in range(len(mcFiles)):
    mcevents.Add(mcFiles[i])

apfile = TFile(remainder[3])
apevents = apfile.Get("ntuple")

zcut = 5
cut = "uncVZ>{0}".format(zcut)

dataevents.Draw("uncChisq:uncVZ>>chisq_vz_data(100,-40,60,100,0,10)")
dataevents.Draw("uncChisq>>chisq_data(100,0,10)")
dataevents.Draw("uncChisq>>chisq_data_cut(100,0,10)",cut)

mcevents.Draw("uncChisq:uncVZ>>chisq_vz_mc(100,-40,60,100,0,10)")
mcevents.Draw("uncChisq>>chisq_mc(100,0,10)")
mcevents.Draw("uncChisq>>chisq_mc_cut(100,0,10)",cut)

apevents.Draw("uncChisq:uncVZ>>chisq_vz_ap(100,-40,60,100,0,10)")
apevents.Draw("uncChisq>>chisq_ap(100,0,10)")
apevents.Draw("uncChisq>>chisq_ap_cut(100,0,10)",cut)

openPDF(outfile,c)

c.SetLogz(1)

chisq_vz_data = gDirectory.FindObject("chisq_vz_data")
chisq_data = gDirectory.FindObject("chisq_data")
chisq_data_cut = gDirectory.FindObject("chisq_data_cut")

chisq_vz_mc = gDirectory.FindObject("chisq_vz_mc")
chisq_mc = gDirectory.FindObject("chisq_mc")
chisq_mc_cut = gDirectory.FindObject("chisq_mc_cut")

chisq_vz_ap = gDirectory.FindObject("chisq_vz_ap")
chisq_ap = gDirectory.FindObject("chisq_ap")
chisq_ap_cut = gDirectory.FindObject("chisq_ap_cut")

outfileroot.cd()

c.SetLogy(1)

chisq_data.Sumw2()
chisq_data_cut.Sumw2()
chisq_mc.Sumw2()
chisq_mc_cut.Sumw2()
chisq_ap.Sumw2()
chisq_ap_cut.Sumw2()

chisq_data.Scale(1./chisq_data.Integral())
chisq_data_cut.Scale(1./chisq_data_cut.Integral())
chisq_mc.Scale(1./chisq_mc.Integral())
chisq_mc_cut.Scale(1./chisq_mc_cut.Integral())
chisq_ap.Scale(1./chisq_ap.Integral())
chisq_ap_cut.Scale(1./chisq_ap_cut.Integral())

chisq_mc.SetLineColor(2)
chisq_mc_cut.SetLineColor(2)
chisq_ap.SetLineColor(1)
chisq_ap_cut.SetLineColor(1)

chisq_data.SetTitle("")
chisq_data.GetXaxis().SetTitle("Unconstrained Chisq")
chisq_data.GetYaxis().SetRangeUser(0.00001,chisq_ap.GetMaximum()*1.2)
chisq_data.Draw()
chisq_mc.Draw("same")
chisq_ap.Draw("same")
legend = TLegend(.60,.66,.92,.87)
legend.SetBorderSize(0)
legend.SetFillColor(0)
legend.SetFillStyle(0)
legend.SetTextFont(42)
legend.SetTextSize(0.035)
legend.AddEntry(chisq_data,"Data","LP")
legend.AddEntry(chisq_mc,"MC","LP")
legend.AddEntry(chisq_ap,"100 MeV A'","LP")
legend.Draw("same")
c.Print(outfile+".pdf")
c.Write()

chisq_data_cut.SetTitle("Z > 5 mm")
chisq_data_cut.GetXaxis().SetTitle("Unconstrained Chisq")
chisq_data_cut.GetYaxis().SetRangeUser(0.00001,chisq_ap_cut.GetMaximum()*1.2)
chisq_data_cut.Draw()
chisq_mc_cut.Draw("same")
chisq_ap_cut.Draw("same")
legend.Draw("same")
c.Print(outfile+".pdf")
c.Write()

c.SetLogy(0)

chisq_data.SetTitle("")
chisq_data.GetXaxis().SetTitle("Unconstrained Chisq")
chisq_data.GetYaxis().SetRangeUser(0,chisq_ap.GetMaximum()*1.2)
chisq_data.Draw()
chisq_mc.Draw("same")
chisq_ap.Draw("same")
legend.Draw("same")
c.Print(outfile+".pdf")
c.Write()

chisq_data_cut.SetTitle("Z > 5 mm")
chisq_data_cut.GetXaxis().SetTitle("Unconstrained Chisq")
chisq_data_cut.GetYaxis().SetRangeUser(0,chisq_ap_cut.GetMaximum()*1.2)
chisq_data_cut.Draw()
chisq_mc_cut.Draw("same")
chisq_ap_cut.Draw("same")
legend.Draw("same")
c.Print(outfile+".pdf")
c.Write()

chisq_vz_data.Draw("COLZ")
chisq_vz_data.SetTitle("Data L1L1 Preselection")
chisq_vz_data.GetYaxis().SetTitle("Unconstrained Chisq")
chisq_vz_data.GetXaxis().SetTitle("Reconstructed z [mm]")
c.Print(outfile+".pdf")
c.Write()

chisq_vz_mc.Draw("COLZ")
chisq_vz_mc.SetTitle("MC L1L1 Preselection")
chisq_vz_mc.GetYaxis().SetTitle("Unconstrained Chisq")
chisq_vz_mc.GetXaxis().SetTitle("Reconstructed z [mm]")
c.Print(outfile+".pdf")
c.Write()

chisq_vz_ap.Draw("COLZ")
chisq_vz_ap.SetTitle("A' 100 MeV L1L1 Preselection")
chisq_vz_ap.GetYaxis().SetTitle("Unconstrained Chisq")
chisq_vz_ap.GetXaxis().SetTitle("Reconstructed z [mm]")
c.Print(outfile+".pdf")
c.Write()

closePDF(outfile,c)
outfileroot.Close()