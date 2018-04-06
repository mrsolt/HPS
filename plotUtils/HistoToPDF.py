import sys
tmpargv = sys.argv
sys.argv = []
import getopt
import ROOT
from ROOT import gROOT, TFile, gDirectory, gStyle, TCanvas, TH1
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

def savehisto2D(histo,outfile,canvas,XaxisTitle="",YaxisTitle="",plotTitle="",stats=0,logY=0):
	histo.SetTitle(plotTitle)
	histo.GetXaxis().SetTitle(XaxisTitle)
	histo.GetYaxis().SetTitle(YaxisTitle)
	histo.SetStats(stats)
	histo.Draw("COLZ")
	canvas.SetLogy(logY)
	canvas.Print(outfile+".pdf")
	histo.Write(plotTitle)

#gStyle.SetOptStat(0)
gStyle.SetOptStat(110011)
c = TCanvas("c","c",800,600)

outfile = remainder[0]
infile = TFile(remainder[1])

openPDF(outfile,c)
infile.cd()
for h in infile.GetListOfKeys():
	h = h.ReadObj()
	if(h.ClassName() != "TH1F" or h.ClassName() != "TH1D"): continue
	savehisto2D(h,outfile,c,"","",h.GetName())

closePDF(outfile,c)