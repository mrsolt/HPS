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

file = open(remainder[1],"r")
files = []

for line in (raw.strip().split() for raw in file):
	files.append(line[0])
events = TChain("ntuple")
for i in range(len(files)):
    events.Add(files[i])

label = str(remainder[2])

events.Draw("elePurity>>elepurity(100,0,1.1)")
events.Draw("posPurity>>pospurity(100,0,1.1)")

events.Draw("elePurity>>elenomatch(2,-10000,1.1)","elePurity<-1")
events.Draw("posPurity>>posnomatch(2,-10000,1.1)","posPurity<-1")

elepurity = gDirectory.FindObject("elepurity")
pospurity = gDirectory.FindObject("pospurity")

elenomatch = gDirectory.FindObject("elenomatch")
posnomatch = gDirectory.FindObject("posnomatch")

n_ele = elenomatch.Integral()
n_pos = posnomatch.Integral()

print ("Number of V0s:{0}".format(elepurity.Integral()))
print ("Number electrons without match:{0}  Number of positrons without a match: {1}".format(n_ele,n_pos))

eleBad = TH1F("eleBad","eleBad",12,0,12)
posBad = TH1F("posBad","posBad",12,0,12)

for i in range(1,12):
	events.Draw("uncVZ>>eleHisto(1,0,1)".format(i),"(eleL{0}tIsGoodTruthHit<0.5&&eleL{0}tIsGoodTruthHit>-0.5)||(eleL{0}bIsGoodTruthHit<0.5&&eleL{0}bIsGoodTruthHit>-0.5)".format(i))
	events.Draw("uncVZ>>posHisto(1,0,1)".format(i),"(posL{0}tIsGoodTruthHit<0.5&&posL{0}tIsGoodTruthHit>-0.5)||(posL{0}bIsGoodTruthHit<0.5&&posL{0}bIsGoodTruthHit>-0.5)".format(i))
	eleHisto = gDirectory.FindObject("eleHisto")
	posHisto = gDirectory.FindObject("posHisto")
	eleBad.SetBinContent(i,eleHisto.Integral())
	posBad.SetBinContent(i,posHisto.Integral())
	del eleHisto
	del posHisto

openPDF(outfile,c)

elepurity.Sumw2()
pospurity.Sumw2()
pospurity.SetLineColor(2)
elepurity.Draw()
elepurity.GetXaxis().SetTitle("Purity")
elepurity.SetTitle("Track-Truth Match Purity {0}".format(label))
pospurity.Draw("same")
legend = TLegend(.10,.66,.42,.87)
legend.SetBorderSize(0)
legend.SetFillColor(0)
legend.SetFillStyle(0)
legend.SetTextFont(42)
legend.SetTextSize(0.035)
legend.AddEntry(elepurity,"electrons","LP")
legend.AddEntry(pospurity,"positrons","LP")
legend.Draw("same")
c.SetLogy(1)
outfileroot.cd()
c.Print(outfile+".pdf")
c.Write()

eleBad.Sumw2()
posBad.Sumw2()
posBad.SetLineColor(2)
eleBad.Draw()
eleBad.GetXaxis().SetTitle("Tracker Layer")
eleBad.SetTitle("Bad Hit Layers {0}".format(label))
posBad.Draw("same")
legend.Draw("same")
outfileroot.cd()
c.Print(outfile+".pdf")
c.Write()

closePDF(outfile,c)
outfileroot.Close()