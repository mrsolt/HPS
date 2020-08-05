import sys
tmpargv = sys.argv
sys.argv = []
import getopt
import utilities as utils
import ROOT
from ROOT import gROOT, TFile, gDirectory, gStyle, TCanvas, TH1, TLegend
sys.argv = tmpargv

#List arguments
def print_usage():
    print "\nUsage: {0} <output file base name> <input file name>".format(sys.argv[0])
    print "Arguments: "
    print '\t-h: this help message'
    print

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'h')

# Parse the command line arguments
for opt, arg in options:
		if opt=='-h':
			print_usage()
			sys.exit(0)

def openPDF(outfile,canvas):
	c.Print(outfile+".pdf[")

def closePDF(outfile,canvas):
	c.Print(outfile+".pdf]")

def savehisto(histo1,histo2,label1,label2,outfile,canvas,XaxisTitle="",YaxisTitle="",plotTitle="",stats=0,logY=0):
	histo1.SetTitle(plotTitle)
	histo1.GetXaxis().SetTitle(XaxisTitle)
	histo1.GetYaxis().SetTitle(YaxisTitle)
	#histo.SetStats(stats)
	histo1.Scale(1/histo1.GetEntries())
	histo2.Scale(1/histo2.GetEntries())
	maximum = histo1.GetMaximum()
	if(histo2.GetMaximum() > maximum):
		maximum = histo2.GetMaximum()
	histo1.GetYaxis().SetRangeUser(0,1.2*maximum)
	histo1.Draw("")
	histo2.SetLineColor(2)
	histo2.Draw("same")
	legend = TLegend(.68,.66,.92,.87)
	legend.SetBorderSize(0)
	legend.SetFillColor(0)
	legend.SetFillStyle(0)
	legend.SetTextFont(42)
	legend.SetTextSize(0.035)
	legend.AddEntry(histo1,label1,"LP")
	legend.AddEntry(histo2,label2,"LP")
	legend.Draw("")
	histos = []
	histos.append(histo1)
	histos.append(histo2)
	legends = []
	legends.append(label1)
	legends.append(label2)
	utils.MakePlot(histo1.GetName(),outfile,histos,legends,".png",LogY=True,RatioType="Sequential")
	canvas.SetLogy(logY)
	canvas.Print(outfile+".pdf")

def savehisto2D(histo1,histo2,label1,label2,outfile,canvas,XaxisTitle="",YaxisTitle="",plotTitle="",stats=1,logY=0):
	histo1.SetTitle(plotTitle+" "+label1)
	histo1.GetXaxis().SetTitle(XaxisTitle)
	histo1.GetYaxis().SetTitle(YaxisTitle)
	histo1.SetStats(stats)
	histo1.Draw("COLZ")
	canvas.SetLogy(logY)
	canvas.Print(outfile+".pdf")
	histo2.SetTitle(plotTitle+" "+label2)
	histo2.GetXaxis().SetTitle(XaxisTitle)
	histo2.GetYaxis().SetTitle(YaxisTitle)
	histo2.SetStats(stats)
	histo2.Draw("COLZ")
	canvas.SetLogy(logY)
	canvas.Print(outfile+".pdf")

#gStyle.SetOptStat(0)
gStyle.SetOptStat(110011)
c = TCanvas("c","c",800,600)

outfile = remainder[0]
infile1 = TFile(remainder[1])
infile2 = TFile(remainder[2])
label1 = remainder[3]
label2 = remainder[4]

infile1.cd()
histos1 = []
histos1_2D = []
for h in infile1.GetListOfKeys():
	h = h.ReadObj()
	plotHisto = True
	for i in range(len(histos1)):
		if(histos1[i].GetTitle() == h.GetTitle()): 
			plotHisto = False
			continue
	for i in range(len(histos1_2D)):
		if(histos1_2D[i].GetTitle() == h.GetTitle()):
			plotHisto = False
			continue
	if(not plotHisto): continue
	h.GetListOfFunctions().Remove(h.GetFunction("gaus"))
	if(h.ClassName() == "TH1F" or h.ClassName() == "TH1D"):
		histos1.append(h)
	if(h.ClassName() == "TH2F" or h.ClassName() == "TH2D"):
		histos1_2D.append(h)

infile2.cd()
histos2 = []
histos2_2D = []
for h in infile2.GetListOfKeys():
	h = h.ReadObj()
	plotHisto = True
	for i in range(len(histos2)):
		if(histos2[i].GetTitle() == h.GetTitle()):
			plotHisto = False
			continue
	for i in range(len(histos2_2D)):
		if(histos2_2D[i].GetTitle() == h.GetTitle()):
			plotHisto = False
			continue
	if(not plotHisto): continue
	h.GetListOfFunctions().Remove(h.GetFunction("gaus"))
	if(h.ClassName() == "TH1F" or h.ClassName() == "TH1D"):
		histos2.append(h)
	if(h.ClassName() == "TH2F" or h.ClassName() == "TH2D"):
		histos2_2D.append(h)

openPDF(outfile,c)
for i in range(len(histos1)):
	savehisto(histos1[i],histos2[i],label1,label2,outfile,c,histos1[i].GetXaxis().GetTitle(),"",histos1[i].GetTitle())

for i in range(len(histos1_2D)):
	savehisto2D(histos1_2D[i],histos2_2D[i],label1,label2,outfile,c,histos1_2D[i].GetXaxis().GetTitle(),histos1_2D[i].GetYaxis().GetTitle(),histos1_2D[i].GetTitle())

closePDF(outfile,c)