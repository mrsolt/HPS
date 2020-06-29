import sys
tmpargv = sys.argv
sys.argv = []
import getopt
import ROOT
from ROOT import gROOT, TFile, TTree, TChain, gDirectory, TLine, gStyle, TCanvas, TLegend, TH1F
sys.argv = tmpargv

#List arguments
def print_usage():
    print "\nUsage: {0} <output file base name> <input text Data file> <input text MC file> <input text A' files>".format(sys.argv[0])
    print "Arguments: "
    print '\t-z: target position (default -4.3 mm)'
    print '\t-m: minimum uncVZ (default -30 mm)'
    print '\t-n: maximum uncVZ (default 60 mm)'
    print '\t-e: beam energy (default 2.3 GeV)'
    print '\t-b: number of bins (default 100)'
    print '\t-h: this help message'
    print

zTarg = -4.3
ebeam = 2.3
minVZ = -40
maxVZ = 40
nBins = 100


options, remainder = getopt.gnu_getopt(sys.argv[1:], 'hz:m:n:e:b:')

# Parse the command line arguments
for opt, arg in options:
		if opt=='-z':
			zTarg = float(arg)
		if opt=='-m':
			minVZ = float(arg)
		if opt=='-n':
			maxVZ = float(arg)
		if opt=='-e':
			ebeam = float(arg)
		if opt=='-b':
			nBins = float(arg)
		if opt=='-h':
			print_usage()
			sys.exit(0)

gStyle.SetOptStat(0)
c = TCanvas("c","c",800,600)

def saveTuplePlot(events,inHisto,nBins,minX,maxX,minVZ,maxVZ,outfile,canvas,cut=""):
	events.Draw("uncVZ:{0}>>histo({1},{2},{3},{1},{4},{5})".format(inHisto,nBins,minX,maxX,minVZ,maxVZ),cut)
	histo = ROOT.gROOT.FindObject("histo")
	histo.SetTitle("Reconstruced z vs {0}".format(inHisto))
	histo.GetYaxis().SetTitle("Reconstructed Z (mm)")
	histo.GetXaxis().SetTitle("{0} (mm)".format(inHisto))
	canvas.SetLogz(1)
	histo.Draw("COLZ")
	canvas.Print(outfile+".pdf")

def openPDF(outfile,canvas):
	c.Print(outfile+".pdf[")

def closePDF(outfile,canvas):
	c.Print(outfile+".pdf]")

def getPlot(string):
	arr = string.split(" ")
	return arr[0]

def getMin(string):
	arr = string.split(" ")
	if(len(arr) < 2): return ""
	else: return float(arr[1])

def getMax(string):
	arr = string.split(" ")
	if(len(arr) < 3): return ""
	else: return float(arr[2])

outfile = remainder[0]

file = TFile(remainder[1])
events = file.Get("ntuple")

fileap = TFile(remainder[2])
eventsap = fileap.Get("ntuple")

minVZap = 0
maxVZap = 80
minExtrpAxial = -25
maxExtrpAxial = -10
minExtrpStereo = 10
maxExtrpStereo = 25
plots = []
plots.append("eleTrkExtrpYSensorAxialTopL1 {0} {1}".format(minExtrpAxial,maxExtrpAxial))
plots.append("posTrkExtrpYSensorAxialTopL1 {0} {1}".format(minExtrpAxial,maxExtrpAxial))
plots.append("eleTrkExtrpYSensorStereoTopL1 {0} {1}".format(minExtrpStereo,maxExtrpStereo))
plots.append("posTrkExtrpYSensorStereoTopL1 {0} {1}".format(minExtrpStereo,maxExtrpStereo))
plots.append("eleTrkExtrpYSensorAxialBotL1 {0} {1}".format(minExtrpAxial,maxExtrpAxial))
plots.append("posTrkExtrpYSensorAxialBotL1 {0} {1}".format(minExtrpAxial,maxExtrpAxial))
plots.append("eleTrkExtrpYSensorStereoBotL1 {0} {1}".format(minExtrpStereo,maxExtrpStereo))
plots.append("posTrkExtrpYSensorStereoBotL1 {0} {1}".format(minExtrpStereo,maxExtrpStereo))

edge = 19.2
res = 0.080

cuts = []
cuts.append("uncP<9999")
cuts.append("(eleTrkExtrpYSensorAxialTopL1>-{0}&&eleTrkExtrpYSensorStereoTopL1>{0}&&posTrkExtrpYSensorAxialBotL1>-{0}&&posTrkExtrpYSensorStereoBotL1>{0})||(posTrkExtrpYSensorAxialTopL1>-{0}&&posTrkExtrpYSensorStereoTopL1>{0}&&eleTrkExtrpYSensorAxialBotL1>-{0}&&eleTrkExtrpYSensorStereoBotL1>{0})".format(edge-3.0*res))
cuts.append("(eleTrkExtrpYSensorAxialTopL1>-{0}&&eleTrkExtrpYSensorStereoTopL1>{0}&&posTrkExtrpYSensorAxialBotL1>-{0}&&posTrkExtrpYSensorStereoBotL1>{0})||(posTrkExtrpYSensorAxialTopL1>-{0}&&posTrkExtrpYSensorStereoTopL1>{0}&&eleTrkExtrpYSensorAxialBotL1>-{0}&&eleTrkExtrpYSensorStereoBotL1>{0})".format(edge-2.0*res))
cuts.append("(eleTrkExtrpYSensorAxialTopL1>-{0}&&eleTrkExtrpYSensorStereoTopL1>{0}&&posTrkExtrpYSensorAxialBotL1>-{0}&&posTrkExtrpYSensorStereoBotL1>{0})||(posTrkExtrpYSensorAxialTopL1>-{0}&&posTrkExtrpYSensorStereoTopL1>{0}&&eleTrkExtrpYSensorAxialBotL1>-{0}&&eleTrkExtrpYSensorStereoBotL1>{0})".format(edge-1.0*res))
cuts.append("(eleTrkExtrpYSensorAxialTopL1>-{0}&&eleTrkExtrpYSensorStereoTopL1>{0}&&posTrkExtrpYSensorAxialBotL1>-{0}&&posTrkExtrpYSensorStereoBotL1>{0})||(posTrkExtrpYSensorAxialTopL1>-{0}&&posTrkExtrpYSensorStereoTopL1>{0}&&eleTrkExtrpYSensorAxialBotL1>-{0}&&eleTrkExtrpYSensorStereoBotL1>{0})".format(edge-0.0*res))

openPDF(outfile,c)

for i in range(len(plots)):
	plot = getPlot(plots[i])
	minimum = getMin(plots[i])
	maximum = getMax(plots[i])
	saveTuplePlot(events,plot,nBins,minimum,maximum,minVZ,maxVZ,outfile,c)
	saveTuplePlot(eventsap,plot,nBins,minimum,maximum,minVZap,maxVZap,outfile,c)

histos = []
for i in range(len(cuts)):
	saveTuplePlot(events,"uncM",nBins,0.0,0.2,minVZ,maxVZ,outfile,c,cuts[i])
	eventsap.Draw("uncVZ>>histo{3}({0},{1},{2})".format(nBins,minVZap,maxVZap,i),cuts[i])
	histos.append(ROOT.gROOT.FindObject("histo{0}".format(0)))

color = 1
c.SetLogy(0)
for i in range(len(histos)):
	histos[i].SetLineColor(color)
	histos[i].SetStats(0)
	histos[i].Sumw2()
	if(i == 0):
		histos[i].Draw()
		histos[i].SetTitle("Reconstructed Ap")
		histos[i].GetXaxis().SetTitle("Reconstructed z [mm]")
	else:
		histos[i].Draw("same")
c.Print(outfile+".pdf")

closePDF(outfile,c)