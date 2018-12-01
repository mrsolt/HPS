import sys
tmpargv = sys.argv
sys.argv = []
import getopt
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
	canvas.SetLogy(logY)
	canvas.Print(outfile+".pdf")
	#histo.Write(plotTitle)

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
for h in infile1.GetListOfKeys():
	h = h.ReadObj()
	if(h.ClassName() != "TH1F" and h.ClassName() != "TH1D"): continue
	histos1.append(h)

infile2.cd()
histos2 = []
for h in infile2.GetListOfKeys():
	h = h.ReadObj()
	if(h.ClassName() != "TH1F" and h.ClassName() != "TH1D"): continue
	histos2.append(h)

openPDF(outfile,c)
for i in range(len(histos1)):
	savehisto(histos1[i],histos2[i],label1,label2,outfile,c,"","",histos1[i].GetTitle())

closePDF(outfile,c)