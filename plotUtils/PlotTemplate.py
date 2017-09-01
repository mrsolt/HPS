import sys
tmpargv = sys.argv
sys.argv = []
import getopt
import ROOT
from ROOT import gROOT, TFile, TTree, TChain, gDirectory, TLine, gStyle, TCanvas, TLegend
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

gStyle.SetOptStat(0)
c = TCanvas("c","c",800,600)

outfile = remainder[0]
infile = TFile(remainder[1])

filename = "<file>"
events = infile.Get("ntuple")

xArr = array.array('d')

def getFunction(histo,funcName):
	func = histo.GetFunction("{0}".format(funcName))
	return func

def tupleToHisto(events,inHisto,histo,nBins,minX,maxX):
	{0}.format(events).Draw("{0}>>{1}({2},{3},{4})".format(inHisto,histo,nBIns,minX,maxX))
	histo = ROOT.gROOT.FindObject(histo)
	return histo

def saveTuplePlot(inHisto,nBins,minX,maxX,outfile,canvas):
	events.Draw("{0}>>({1},{2},{3})".format(inHisto,nBins,minX,maxX))
	canvas.Print(outfile+".pdf")

def openPDF(outfile,canvas):
	c.Print(outfile+".pdf[")

def closePDF(outfile,canvas):
	c.Print(outfile+".pdf]")

def getHisto(histoTitle,infile):
	histo = infile.Get(histoTitle)
	return histo

def buildLegend(entries,options):
	legend = TLegend()
	legend = TLegend(.68,.66,.92,.87)
	legend.SetBorderSize(0)
	legend.SetFillColor(0)
	legend.SetFillStyle(0)
	legend.SetTextFont(42)
	legend.SetTextSize(0.035)
	legend.AddEntry(Histo1,"L0L0","LP")
	return legend

def drawHisto(histo,XaxisTitle="",YaxisTitle="",plotTitle="",stats=0):
	histo.Draw("")
	#histo.GetXaxis().SetRangeUser(-5,150)
	#histo.GetYaxis().SetRangeUser(0,1.1)
	histo.SetTitle(plotTitle)
	histo.GetXaxis().SetTitle(XaxisTitle)
	histo.GetYaxis().SetTitle(YaxisTitle)
	histo.SetStats(stats)

def saveHisto(histo,XaxisTitle="",YaxisTitle="",plotTitle="",stats=0,outfile,canvas):
	drawHisto(histo,XaxisTitle,YaxisTitle,plotTitle,stats)
	canvas.Print(outfile+".pdf")
