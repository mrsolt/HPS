import sys
tmpargv = sys.argv
sys.argv = []
import getopt
import numpy as np
import array
import ROOT
import random
from ROOT import gROOT, TFile, TTree, TChain, gDirectory, TLine, gStyle, TCanvas, TLegend, TH1F, TF1, TGraphErrors, TMultiGraph, TPad
sys.argv = tmpargv

#List arguments
def print_usage():
    print "\nUsage: {0} <output file base name> <input root file>".format(sys.argv[0])
    print "Arguments: "
    print '\t-y: plot label'
    print '\t-h: this help message'
    print

zTarg = -4.3
label = ""

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'y:h')

# Parse the command line arguments
for opt, arg in options:
		if opt=='-y':
			label = str(arg)
		if opt=='-h':
			print_usage()
			sys.exit(0)

gStyle.SetOptStat(0)
gStyle.SetOptFit(1011)
c = TCanvas("c","c",800,600)

def SmearHisto(events,nBins,minX,maxX):
	smear_Top5hits = 0.0589307 
	smear_Top6hits = 0.0433669 
	smear_Bot5hits = 0.0551252 
	smear_Bot6hits = 0.045657 
	histoP = TH1F("histoP","histoP",nBins,minX,maxX)
	histoPsmear = TH1F("histoPsmear","histoPsmear",nBins,minX,maxX)
	histoPsmearcut = TH1F("histoPsmearcut","histoPsmearcut",nBins,minX,maxX)
	eleP = array.array('d',[0])
	posP = array.array('d',[0])
	uncM = array.array('d',[0])
	eleNTrackHits = array.array('d',[0])
	posNTrackHits = array.array('d',[0])
	eleTrkLambda = array.array('d',[0])

	events.Branch("eleP",eleP,"eleP/D")
	events.Branch("posP",posP,"posP/D")
	events.Branch("uncM",uncM,"uncM/D")
	events.Branch("eleNTrackHits",eleNTrackHits,"eleNTrackHits/I")
	events.Branch("posNTrackHits",posNTrackHits,"posNTrackHits/I")
	events.Branch("eleTrkLambda",eleTrkLambda,"eleTrkLambda/D")

	nevents = events.GetEntries()

	for entry in xrange(nevents):
		events.GetEntry(entry)
		histoP.Fill(events.eleP+events.posP)
		if(events.eleTrkLambda > 0):
			if(events.eleNTrackHits == 5):
				ele_smear = smear_Top5hits
			else:
				ele_smear = smear_Top6hits
			if(events.posNTrackHits == 5):
				pos_smear = smear_Bot5hits
			else:
				pos_smear = smear_Bot6hits
		else:
			if(events.eleNTrackHits == 5):
				ele_smear = smear_Bot5hits
			else:
				ele_smear = smear_Bot6hits
			if(events.posNTrackHits == 5):
				pos_smear = smear_Top5hits
			else:
				pos_smear = smear_Top6hits

		P_positron_Smear = random.gauss(events.posP, events.posP*pos_smear)
		P_electron_Smear = random.gauss(events.eleP, events.eleP*ele_smear)

		histoPsmear.Fill(P_electron_Smear+P_positron_Smear)
		if(P_electron_Smear > 0.4 and P_positron_Smear > 0.4):
			histoPsmearcut.Fill(P_electron_Smear+P_positron_Smear)

	return histoP, histoPsmear, histoPsmearcut

def openPDF(outfile,canvas):
	c.Print(outfile+".pdf[")

def closePDF(outfile,canvas):
	c.Print(outfile+".pdf]")


nBins = 100
maxX = 2.6
minX = 0.8

outfile = remainder[0]+"_smear"
outfile2 = remainder[0]+"_cuts"
#outfileroot = TFile(remainder[0]+".root","RECREATE")

events = TChain("ntuple")
for i in range(1,len(remainder)):
    events.Add(remainder[i])

histo0, histo1, histo2 = SmearHisto(events,nBins,minX,maxX)

RatioMin = 0.2
RatioMax = 2.2

openPDF(outfile,c)

histo0.SetStats(0)
histo1.SetStats(0)
histo2.SetStats(0)

histo0.Sumw2()
histo1.Sumw2()
histo2.Sumw2()

top = TPad("top","top",0,0.42,1,1)
bot = TPad("bot","bot",0,0,1,0.38)
    
top.Draw()
top.SetBottomMargin(0)
#top.SetTopMargin(gStyle.GetPadTopMargin()*topScale)
bot.Draw()
bot.SetTopMargin(0)
bot.SetBottomMargin(0.4)
top.cd()

histo1.SetLineColor(2)
histo0.GetXaxis().SetTitle("Momentum Sum (GeV)")
histo0.GetYaxis().SetTitle("")
histo0.SetTitle("Comparing P Sum with Momentum Smearing {0}".format(label))

histo2.GetXaxis().SetTitle("Momentum Sum (GeV)")
histo2.GetYaxis().SetTitle("")
histo2.SetTitle("Comparing P Sum with Momentum Cuts {0}".format(label))

legend = TLegend(.15,.66,.42,.87)
legend.SetBorderSize(0)
legend.SetFillColor(0)
legend.SetFillStyle(0)
legend.SetTextFont(42)
legend.SetTextSize(0.035)
legend.AddEntry(histo0,"No Smearing","LP")
legend.AddEntry(histo1,"With Smearing","LP")

legend2 = TLegend(.15,.66,.42,.87)
legend2.SetBorderSize(0)
legend2.SetFillColor(0)
legend2.SetFillStyle(0)
legend2.SetTextFont(42)
legend2.SetTextSize(0.035)
legend2.AddEntry(histo2,"With Momentum Cuts","LP")
legend2.AddEntry(histo1,"No Momentum Cuts","LP")

histo0.Draw()
histo1.Draw("same")
legend.Draw("same")

bot.cd()
reference = histo0.Clone("reference")
reference.GetYaxis().SetTitle("Ratio")
reference.GetYaxis().SetTitleSize(0.06)
reference.GetYaxis().SetLabelSize(0.1)
reference.GetXaxis().SetTitleSize(0.1)
reference.GetXaxis().SetLabelSize(0.1)
reference.GetXaxis().SetTitle("Momentum Sum (GeV)")
reference.GetYaxis().SetRangeUser(RatioMin,RatioMax)
reference.GetYaxis().SetNdivisions(508)
reference.GetYaxis().SetDecimals(True)
reference.Draw("axis")
ratio = histo1.Clone("Ratio"+histo1.GetName())
ratio.Divide(reference)
ratio.DrawCopy("pe same")

c.Print(outfile+".pdf")
c.Clear()
closePDF(outfile,c)

openPDF(outfile2,c)

top = TPad("top","top",0,0.42,1,1)
bot = TPad("bot","bot",0,0,1,0.38)
    
top.Draw()
top.SetBottomMargin(0)
#top.SetTopMargin(gStyle.GetPadTopMargin()*topScale)
bot.Draw()
bot.SetTopMargin(0)
bot.SetBottomMargin(0.4)
top.cd()

histo2.Draw()
histo1.Draw("same")
legend2.Draw("same")

bot.cd()
reference = histo1.Clone("reference")
reference.GetYaxis().SetTitle("Ratio")
reference.GetYaxis().SetTitleSize(0.06)
reference.GetYaxis().SetLabelSize(0.1)
reference.GetXaxis().SetTitleSize(0.1)
reference.GetXaxis().SetLabelSize(0.1)
reference.GetXaxis().SetTitle("Momentum Sum (GeV)")
reference.GetYaxis().SetRangeUser(RatioMin,RatioMax)
reference.GetYaxis().SetNdivisions(508)
reference.GetYaxis().SetDecimals(True)
reference.Draw("axis")
ratio = histo2.Clone("Ratio"+histo2.GetName())
ratio.Divide(reference)
ratio.DrawCopy("pe same")

c.Print(outfile2+".pdf")

closePDF(outfile2,c)
#outfileroot.Close()