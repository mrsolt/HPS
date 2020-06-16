import sys
tmpargv = sys.argv
sys.argv = []
import getopt
import ROOT
from ROOT import gROOT, TFile, TTree, TChain, gDirectory, TLine, gStyle, TCanvas, TLegend, TH1F, TF1
sys.argv = tmpargv

#List arguments
def print_usage():
    print "\nUsage: {0} <output file base name> <input Data file>".format(sys.argv[0])
    print "Arguments: "
    print '\t-z: target position (default -4.3 mm)'
    print '\t-b: number of bins (default 100)'
    print '\t-h: this help message'
    print

zTarg = -4.3
nBins = 100


options, remainder = getopt.gnu_getopt(sys.argv[1:], 'hz:b:')

# Parse the command line arguments
for opt, arg in options:
		if opt=='-z':
			zTarg = float(arg)
		if opt=='-b':
			nBins = float(arg)
		if opt=='-h':
			print_usage()
			sys.exit(0)

gStyle.SetOptStat(0)
c = TCanvas("c","c",800,600)

def saveTuplePlot(events,inHisto,nBins,minx,maxx,mass,massRes,masscut_nsigma,massCut,zcut,outfile,canvas):
	cut = "{0}&&uncVZ>{1}".format(massCut,zcut)
	events.Draw("{0}>>histo({1},{2},{3})".format(inHisto,nBins,minx,maxx),cut)
	histo = ROOT.gROOT.FindObject("histo")
	minMass = mass-massRes*masscut_nsigma/2
	maxMass = mass+massRes*masscut_nsigma/2
	histo.SetTitle("Mass = {0:.3f} #pm {1:.4f} MeV Zcut = {2:0.2f} mm".format(mass,massRes*masscut_nsigma/2,zcut))
	histo.GetXaxis().SetTitle(inHisto)
	histo.Draw("")
	canvas.SetLogy(0)
	canvas.Print(outfile+".pdf")

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

def openPDF(outfile,canvas):
	c.Print(outfile+".pdf[")

def closePDF(outfile,canvas):
	c.Print(outfile+".pdf]")

masscut_nsigma = 1.90
zcut = TF1("zcut","{0}+{1}*x+{2}*x^2+{3}*x^3+{4}*x^4+{5}*x^5".format(-0.4738,1551,-3.835e4,3.930e5,-1.865e6,3.373e6),0.05,0.175)
mres = TF1("mres","{0}+{1}*x+{2}*x^2+{3}*x^3+{4}*x^4".format(0.9348/1000,0.05442,-0.5784,5.852,-17.24),0.04,0.2)

outfile = remainder[0]

events = TChain("ntuple")
for i in range(1,len(remainder)):
    events.Add(remainder[i])

massArr = []
massArr.append(0.057)
massArr.append(0.060)
massArr.append(0.062)
massArr.append(0.065)
massArr.append(0.070)

plots = []
plots.append("uncVZ 10 30")
plots.append("uncVY -0.5 0.5")
plots.append("uncVX -1 1")
plots.append("uncM 0.055 0.075")
plots.append("uncChisq 0 10")
plots.append("uncP 1.85 2.4")

openPDF(outfile,c)

for i in range(len(massArr)):
	mass = massArr[i]
	massRes = mres.Eval(mass)
	massCut = "uncM>{0}&&uncM<{1}".format(mass-massRes*masscut_nsigma/2,mass+massRes*masscut_nsigma/2)
	Zcut = zcut.Eval(mass)
	for j in range(len(plots)):
		plot = getPlot(plots[j])
		minx = getMin(plots[j])
		maxx = getMax(plots[j])
		saveTuplePlot(events,plot,nBins,minx,maxx,mass,massRes,masscut_nsigma,massCut,Zcut,outfile,c)

closePDF(outfile,c)