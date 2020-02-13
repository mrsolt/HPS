import sys
tmpargv = sys.argv
sys.argv = []
import getopt
import ROOT
from ROOT import gROOT, TFile, TTree, TChain, gDirectory, TLine, gStyle, TCanvas, TLegend, TH1F
sys.argv = tmpargv

#List arguments
def print_usage():
    print "\nUsage: {0} <output file base name> <input Data file> <input MC text file> <input 80 MeV A' file> <input 100 MeV A' file>".format(sys.argv[0])
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

datafile = TFile(remainder[1])
dataevents = datafile.Get("ntuple")

mcfile = open(remainder[2],"r")
mcFiles = []

for line in (raw.strip().split() for raw in mcfile):
	mcFiles.append(line[0])
mcevents = TChain("ntuple")
for i in range(len(mcFiles)):
    mcevents.Add(mcFiles[i])

ap1file = TFile(remainder[3])
ap1events = ap1file.Get("ntuple")

ap2file = TFile(remainder[4])
ap2events = ap2file.Get("ntuple")

x0_cut1_pos_x0 = -0.3392
x1_cut1_pos_x0 = -0.03407

x0_cut1_pos_x1 = 0.01971
x1_cut1_pos_x1 = 0.1114

x0_cut1_pos = "({0}+{1}*uncM)".format(x0_cut1_pos_x0,x1_cut1_pos_x0)
x1_cut1_pos = "({0}+{1}*uncM)".format(x0_cut1_pos_x1,x1_cut1_pos_x1)
cut1_pos = "({0}+{1}*uncVZ)".format(x0_cut1_pos,x1_cut1_pos)


x0_cut2_pos_x0 = -0.4990
x1_cut2_pos_x0 = 1.618

x0_cut2_pos_x1 = 0.06256
x1_cut2_pos_x1 = 0.08516

x0_cut2_pos = "({0}+{1}*uncM)".format(x0_cut2_pos_x0,x1_cut2_pos_x0)
x1_cut2_pos = "({0}+{1}*uncM)".format(x0_cut2_pos_x1,x1_cut2_pos_x1)
cut2_pos = "({0}+{1}*uncVZ)".format(x0_cut2_pos,x1_cut2_pos)


x0_cut1_neg_x0 = -0.04928
x1_cut1_neg_x0 = -0.9747

x0_cut1_neg_x1 = 0.01264
x1_cut1_neg_x1 = 0.1757

x0_cut1_neg = "({0}+{1}*uncM)".format(x0_cut1_neg_x0,x1_cut1_neg_x0)
x1_cut1_neg = "({0}+{1}*uncM)".format(x0_cut1_neg_x1,x1_cut1_neg_x1)
cut1_neg = "({0}+{1}*uncVZ)".format(x0_cut1_neg,x1_cut1_neg)


x0_cut2_neg_x0 = -0.09531
x1_cut2_neg_x0 = -0.6908

x0_cut2_neg_x1 = 0.05686
x1_cut2_neg_x1 = 0.1009

x0_cut2_neg = "({0}+{1}*uncM)".format(x0_cut2_neg_x0,x1_cut2_neg_x0)
x1_cut2_neg = "({0}+{1}*uncM)".format(x0_cut2_neg_x1,x1_cut2_neg_x1)
cut2_neg = "({0}+{1}*uncVZ)".format(x0_cut2_neg,x1_cut2_neg)

#cut = "(eleTrkZ0>{0}&&eleTrkZ0<{1}&&-posTrkZ0>{2}&&-posTrkZ0<{3})||(posTrkZ0>{0}&&posTrkZ0<{1}&&-eleTrkZ0>{2}&&-eleTrkZ0<{3})".format(cut1_pos,cut2_pos,cut1_neg,cut2_neg)
cut = "(eleTrkZ0>{0}&&-posTrkZ0>{1})||(posTrkZ0>{0}&&-eleTrkZ0>{1})".format(cut1_pos,cut1_neg)

dataevents.Draw("uncVZ>>vz_data(100,-40,40)")
dataevents.Draw("uncVZ:uncM>>vz_m_data(100,0,0.2,100,-40,40)")

dataevents.Draw("uncVZ>>vz_data_cut(100,-40,40)",cut)
dataevents.Draw("uncVZ:uncM>>vz_m_data_cut(100,0,0.2,100,-40,40)",cut)

dataevents.Draw("uncVZ:eleTrkZ0>>elez0_data(100,-4,4,100,-40,40)")
dataevents.Draw("uncVZ:posTrkZ0>>posz0_data(100,-4,4,100,-40,40)")

dataevents.Draw("uncVZ:eleTrkZ0>>elez0_data_cut(100,-4,4,100,-40,40)",cut)
dataevents.Draw("uncVZ:posTrkZ0>>posz0_data_cut(100,-4,4,100,-40,40)",cut)

mcevents.Draw("uncVZ>>vz_mc(100,-40,40)")
mcevents.Draw("uncVZ:uncM>>vz_m_mc(100,0,0.2,100,-40,40)")

mcevents.Draw("uncVZ>>vz_mc_cut(100,-40,40)",cut)
mcevents.Draw("uncVZ:uncM>>vz_m_mc_cut(100,0,0.2,100,-40,40)",cut)

mcevents.Draw("uncVZ:eleTrkZ0>>elez0_mc(100,-4,4,100,-40,40)")
mcevents.Draw("uncVZ:posTrkZ0>>posz0_mc(100,-4,4,100,-40,40)")

mcevents.Draw("uncVZ:eleTrkZ0>>elez0_mc_cut(100,-4,4,100,-40,40)",cut)
mcevents.Draw("uncVZ:posTrkZ0>>posz0_mc_cut(100,-4,4,100,-40,40)",cut)

ap1events.Draw("uncVZ>>vz_ap1(100,-40,60)")
ap1events.Draw("uncVZ:uncM>>vz_m_ap1(100,0,0.2,100,-40,60)")

ap1events.Draw("uncVZ>>vz_ap1_cut(100,-40,60)",cut)
ap1events.Draw("uncVZ:uncM>>vz_m_ap1_cut(100,0,0.2,100,-40,60)",cut)

ap1events.Draw("uncVZ:eleTrkZ0>>elez0_ap1(100,-4,4,100,-40,40)")
ap1events.Draw("uncVZ:posTrkZ0>>posz0_ap1(100,-4,4,100,-40,40)")

ap1events.Draw("uncVZ:eleTrkZ0>>elez0_ap1_cut(100,-4,4,100,-40,40)",cut)
ap1events.Draw("uncVZ:posTrkZ0>>posz0_ap1_cut(100,-4,4,100,-40,40)",cut)

ap2events.Draw("uncVZ>>vz_ap2(100,-40,60)")
ap2events.Draw("uncVZ:uncM>>vz_m_ap2(100,0,0.2,100,-40,60)")

ap2events.Draw("uncVZ>>vz_ap2_cut(,100,-40,60)",cut)
ap2events.Draw("uncVZ:uncM>>vz_m_ap2_cut(100,0,0.2,100,-40,60)",cut)

ap2events.Draw("uncVZ:eleTrkZ0>>elez0_ap2(100,-4,4,100,-40,40)")
ap2events.Draw("uncVZ:posTrkZ0>>posz0_ap2(100,-4,4,100,-40,40)")

ap2events.Draw("uncVZ:eleTrkZ0>>elez0_ap2_cut(100,-4,4,100,-40,40)",cut)
ap2events.Draw("uncVZ:posTrkZ0>>posz0_ap2_cut(100,-4,4,100,-40,40)",cut)

openPDF(outfile,c)

c.SetLogz(1)

vz_data = gDirectory.FindObject("vz_data")
vz_m_data = gDirectory.FindObject("vz_m_data")
vz_data_cut = gDirectory.FindObject("vz_data_cut")
vz_m_data_cut = gDirectory.FindObject("vz_m_data_cut")
elez0_data = gDirectory.FindObject("elez0_data")
posz0_data = gDirectory.FindObject("posz0_data")
elez0_data_cut = gDirectory.FindObject("elez0_data_cut")
posz0_data_cut = gDirectory.FindObject("posz0_data_cut")
elez0_data.Add(posz0_data)
elez0_data_cut.Add(posz0_data_cut)

vz_mc = gDirectory.FindObject("vz_mc")
vz_m_mc = gDirectory.FindObject("vz_m_mc")
vz_mc_cut = gDirectory.FindObject("vz_mc_cut")
vz_m_mc_cut = gDirectory.FindObject("vz_m_mc_cut")
elez0_mc = gDirectory.FindObject("elez0_mc")
posz0_mc = gDirectory.FindObject("posz0_mc")
elez0_mc_cut = gDirectory.FindObject("elez0_mc_cut")
posz0_mc_cut = gDirectory.FindObject("posz0_mc_cut")
elez0_mc.Add(posz0_mc)
elez0_mc_cut.Add(posz0_mc_cut)

vz_ap1 = gDirectory.FindObject("vz_ap1")
vz_m_ap1 = gDirectory.FindObject("vz_m_ap1")
vz_ap1_cut = gDirectory.FindObject("vz_ap1_cut")
vz_m_ap1_cut = gDirectory.FindObject("vz_m_ap1_cut")
elez0_ap1 = gDirectory.FindObject("elez0_ap1")
posz0_ap1 = gDirectory.FindObject("posz0_ap1")
elez0_ap1_cut = gDirectory.FindObject("elez0_ap1_cut")
posz0_ap1_cut = gDirectory.FindObject("posz0_ap1_cut")
elez0_ap1.Add(posz0_ap1)
elez0_ap1_cut.Add(posz0_ap1_cut)

vz_ap2 = gDirectory.FindObject("vz_ap2")
vz_m_ap2 = gDirectory.FindObject("vz_m_ap2")
vz_ap2_cut = gDirectory.FindObject("vz_ap2_cut")
vz_m_ap2_cut = gDirectory.FindObject("vz_m_ap2_cut")
elez0_ap2 = gDirectory.FindObject("elez0_ap2")
posz0_ap2 = gDirectory.FindObject("posz0_ap2")
elez0_ap2_cut = gDirectory.FindObject("elez0_ap2_cut")
posz0_ap2_cut = gDirectory.FindObject("posz0_ap2_cut")
elez0_ap2.Add(posz0_ap2)
elez0_ap2_cut.Add(posz0_ap2_cut)

outfileroot.cd()

c.SetLogy(1)

vz_data.Sumw2()
vz_data_cut.Sumw2()
vz_data_cut.SetLineColor(2)
vz_data.SetTitle("Data")
vz_data.GetXaxis().SetTitle("Reconstructed z [mm]")
vz_data.Draw()
vz_data_cut.Draw("same")
legend = TLegend(.10,.76,.42,.97)
legend.SetBorderSize(0)
legend.SetFillColor(0)
legend.SetFillStyle(0)
legend.SetTextFont(42)
legend.SetTextSize(0.035)
legend.AddEntry(vz_data,"No IP Cut","LP")
legend.AddEntry(vz_data_cut,"IP Cut","LP")
legend.Draw("same")
c.Print(outfile+".pdf")
c.Write()

vz_mc.Sumw2()
vz_mc_cut.Sumw2()
vz_mc_cut.SetLineColor(2)
vz_mc.SetTitle("MC")
vz_mc.GetXaxis().SetTitle("Reconstructed z [mm]")
vz_mc.Draw()
vz_mc_cut.Draw("same")
legend.Draw("same")
c.Print(outfile+".pdf")
c.Write()

c.SetLogy(0)
vz_ap1.Sumw2()
vz_ap1_cut.Sumw2()
vz_ap1_cut.SetLineColor(2)
vz_ap1.SetTitle("80 MeV A'")
vz_ap1.GetXaxis().SetTitle("Reconstructed z [mm]")
vz_ap1.Draw()
vz_ap1_cut.Draw("same")
legend.Draw("same")
c.Print(outfile+".pdf")
c.Write()

vz_ap2.Sumw2()
vz_ap2_cut.Sumw2()
vz_ap2_cut.SetLineColor(2)
vz_ap2.SetTitle("100 MeV A'")
vz_ap2.GetXaxis().SetTitle("Reconstructed z [mm]")
vz_ap2.Draw()
vz_ap2_cut.Draw("same")
legend.Draw("same")
c.Print(outfile+".pdf")
c.Write()

c.SetLogy(0)
vz_m_data.Draw("COLZ")
vz_m_data.SetTitle("Data No Impact Parameter Cut")
vz_m_data.GetXaxis().SetTitle("Mass [GeV]")
vz_m_data.GetYaxis().SetTitle("Reconstructed z [mm]")
c.Print(outfile+".pdf")
c.Write()

vz_m_data_cut.Draw("COLZ")
vz_m_data_cut.SetTitle("Data With Impact Parameter Cut")
vz_m_data_cut.GetXaxis().SetTitle("Mass [GeV]")
vz_m_data_cut.GetYaxis().SetTitle("Reconstructed z [mm]")
c.Print(outfile+".pdf")
c.Write()

vz_m_mc.Draw("COLZ")
vz_m_mc.SetTitle("MC No Impact Parameter Cut")
vz_m_mc.GetXaxis().SetTitle("Mass [GeV]")
vz_m_mc.GetYaxis().SetTitle("Reconstructed z [mm]")
c.Print(outfile+".pdf")
c.Write()

vz_m_mc_cut.Draw("COLZ")
vz_m_mc_cut.SetTitle("MC With Impact Parameter Cut")
vz_m_mc_cut.GetXaxis().SetTitle("Mass [GeV]")
vz_m_mc_cut.GetYaxis().SetTitle("Reconstructed z [mm]")
c.Print(outfile+".pdf")
c.Write()

vz_m_ap1.Draw("COLZ")
vz_m_ap1.SetTitle("80 MeV A' No Impact Parameter Cut")
vz_m_ap1.GetXaxis().SetTitle("Mass [GeV]")
vz_m_ap1.GetYaxis().SetTitle("Reconstructed z [mm]")
c.Print(outfile+".pdf")
c.Write()

vz_m_ap1_cut.Draw("COLZ")
vz_m_ap1_cut.SetTitle("80 MeV A' With Impact Parameter Cut")
vz_m_ap1_cut.GetXaxis().SetTitle("Mass [GeV]")
vz_m_ap1_cut.GetYaxis().SetTitle("Reconstructed z [mm]")
c.Print(outfile+".pdf")
c.Write()

vz_m_ap2.Draw("COLZ")
vz_m_ap2.SetTitle("100 MeV A' No Impact Parameter Cut")
vz_m_ap2.GetXaxis().SetTitle("Mass [GeV]")
vz_m_ap2.GetYaxis().SetTitle("Reconstructed z [mm]")
c.Print(outfile+".pdf")
c.Write()

vz_m_ap2_cut.Draw("COLZ")
vz_m_ap2_cut.SetTitle("100 MeV A' With Impact Parameter Cut")
vz_m_ap2_cut.GetXaxis().SetTitle("Mass [GeV]")
vz_m_ap2_cut.GetYaxis().SetTitle("Reconstructed z [mm]")
c.Print(outfile+".pdf")
c.Write()

elez0_data.Draw("COLZ")
elez0_data.SetTitle("Data No Impact Parameter Cut")
elez0_data.GetXaxis().SetTitle("Ele/Pos Z0 [mm]")
elez0_data.GetYaxis().SetTitle("Reconstructed z [mm]")
c.Print(outfile+".pdf")
c.Write()

elez0_data_cut.Draw("COLZ")
elez0_data_cut.SetTitle("Data With Impact Parameter Cut")
elez0_data_cut.GetXaxis().SetTitle("Ele/Pos Z0 [mm]")
elez0_data_cut.GetYaxis().SetTitle("Reconstructed z [mm]")
c.Print(outfile+".pdf")
c.Write()

elez0_mc.Draw("COLZ")
elez0_mc.SetTitle("MC No Impact Parameter Cut")
elez0_mc.GetXaxis().SetTitle("Ele/Pos Z0 [mm]")
elez0_mc.GetYaxis().SetTitle("Reconstructed z [mm]")
c.Print(outfile+".pdf")
c.Write()

elez0_mc_cut.Draw("COLZ")
elez0_mc_cut.SetTitle("MC With Impact Parameter Cut")
elez0_mc_cut.GetXaxis().SetTitle("Ele/Pos Z0 [mm]")
elez0_mc_cut.GetYaxis().SetTitle("Reconstructed z [mm]")
c.Print(outfile+".pdf")
c.Write()

elez0_ap1.Draw("COLZ")
elez0_ap1.SetTitle("80 MeV A' No Impact Parameter Cut")
elez0_ap1.GetXaxis().SetTitle("Ele/Pos Z0 [mm]")
elez0_ap1.GetYaxis().SetTitle("Reconstructed z [mm]")
c.Print(outfile+".pdf")
c.Write()

elez0_ap1_cut.Draw("COLZ")
elez0_ap1_cut.SetTitle("80 MeV A' With Impact Parameter Cut")
elez0_ap1_cut.GetXaxis().SetTitle("Ele/Pos Z0 [mm]")
elez0_ap1_cut.GetYaxis().SetTitle("Reconstructed z [mm]")
c.Print(outfile+".pdf")
c.Write()

elez0_ap2.Draw("COLZ")
elez0_ap2.SetTitle("100 MeV A' No Impact Parameter Cut")
elez0_ap2.GetXaxis().SetTitle("Ele/Pos Z0 [mm]")
elez0_ap2.GetYaxis().SetTitle("Reconstructed z [mm]")
c.Print(outfile+".pdf")
c.Write()

elez0_ap2_cut.Draw("COLZ")
elez0_ap2_cut.SetTitle("100 MeV A' With Impact Parameter Cut")
elez0_ap2_cut.GetXaxis().SetTitle("Ele/Pos Z0 [mm]")
elez0_ap2_cut.GetYaxis().SetTitle("Reconstructed z [mm]")
c.Print(outfile+".pdf")
c.Write()


closePDF(outfile,c)
outfileroot.Close()