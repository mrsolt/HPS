import sys
tmpargv = sys.argv
sys.argv = []
import getopt
import ROOT
from ROOT import gROOT, TFile, TTree, TChain, gDirectory, TLine, gStyle, TCanvas, TLegend, TH1F
sys.argv = tmpargv

#List arguments
def print_usage():
    print "\nUsage: {0} <output file base name>".format(sys.argv[0])
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

def saveTuplePlot2D(events,inHisto1,inHisto2,nBinsX,minX,maxX,nBinsY,minY,maxY,outfile,canvas,XaxisTitle="",YaxisTitle="",plotTitle="",cut="",stats=0,logY=0):
	events.Draw("{0}:{1}>>histo({2},{3},{4},{5},{6},{7})".format(inHisto2,inHisto1,nBinsX,minX,maxX,nBinsY,minY,maxY),cut)
	histo = ROOT.gROOT.FindObject("histo")
	histo.SetTitle(plotTitle)
	histo.GetXaxis().SetTitle(XaxisTitle)
	histo.GetYaxis().SetTitle(YaxisTitle)
	histo.SetStats(stats)
	histo.Draw("COLZ")
	canvas.SetLogy(logY)
	canvas.Print(outfile+".pdf")
	del histo

def openPDF(outfile,canvas):
	c.Print(outfile+".pdf[")

def closePDF(outfile,canvas):
	c.Print(outfile+".pdf]")

def getPlot(string):
	arr = string.split(" ")
	return arr[0]

def getPlot2D(string):
	arr = string.split(" ")
	if(len(arr) < 2): return ""
	else: return arr[1]

def getMinX(string):
	arr = string.split(" ")
	if(len(arr) < 2): return -9999
	else: return float(arr[1])

def getMaxX(string):
	arr = string.split(" ")
	if(len(arr) < 3): return -9999
	else: return float(arr[2])

def getMinX2D(string):
	arr = string.split(" ")
	if(len(arr) < 3): return -9999
	else: return float(arr[2])

def getMaxX2D(string):
	arr = string.split(" ")
	if(len(arr) < 4): return -9999
	else: return float(arr[3])

def getMinY(string):
	arr = string.split(" ")
	if(len(arr) < 5): return -9999
	else: return float(arr[4])

def getMaxY(string):
	arr = string.split(" ")
	if(len(arr) < 6): return -9999
	else: return float(arr[5])

nBins = 100

outfile_simp = remainder[0] + "_simp"
outfile_ap = remainder[0] + "_ap"

simp_files = []
simp_files.append("/nfs/slac/g/hps3/data/TriggerStudies2019/simps/tuple/125_75_10_truth.root")
simp_files.append("/nfs/slac/g/hps3/data/TriggerStudies2019/simps/tuple/125_75_42_truth.root")
simp_files.append("/nfs/slac/g/hps3/data/TriggerStudies2019/simps/tuple/200_75_42_truth.root")
simp_files.append("/nfs/slac/g/hps3/data/TriggerStudies2019/simps/tuple/250_225_10_truth.root")
simp_files.append("/nfs/slac/g/hps3/data/TriggerStudies2019/simps/tuple/375_225_10_truth.root")
simp_files.append("/nfs/slac/g/hps3/data/TriggerStudies2019/simps/tuple/375_225_125_truth.root")

simp_mass = []
simp_mass.append("125 75 10")
simp_mass.append("125 75 42")
simp_mass.append("200 75 42")
simp_mass.append("250 225 10")
simp_mass.append("375 225 10")
simp_mass.append("375 225 125")

ap_files = []
ap_files.append("/nfs/slac/g/hps3/data/TriggerStudies2019/ap/slic_tuple/225/ap_225_MeV_slic.root")
ap_files.append("/nfs/slac/g/hps3/data/TriggerStudies2019/ap/slic_tuple/75/ap_75_MeV_slic.root")

ap_mass = []
ap_mass.append("75")
ap_mass.append("225")

simp_events = []
for i in range(len(simp_files)):
    simp_events.append(simp_files[i].Get("ntuple"))

ap_events = []
for i in range(len(ap_files)):
    ap_events.append(ap_files[i].Get("ntuple"))


plots2D = []
plots2D.append("triPosEndZ triPosE 0 30 0 1.5")

cut = "triPosEndZ>1400&&triPosEndZ<1600"

openPDF(outfile_simp,c)

for j in range(len(simp_events)):
    for i in range(len(plots2D)):
	    plot1 = getPlot(plots2D[i])
	    plot2 = getPlot2D(plots2D[i])
	    minX = getMinX2D(plots2D[i])
	    maxX = getMaxX2D(plots2D[i])
	    minY = getMinY(plots2D[i])
	    maxY = getMaxY(plots2D[i])
	    mass = GetMass1(simp_mass[i])
	    Vmass = GetMass2(simp_mass[i])
	    Pimass = GetMass3(simp_mass[i])
	    saveTuplePlot2D(simp_events[j],plot1,plot2,nBins,minX,maxX,maxY,minY,maxY,outfile,c,plot1,plot2,"A' " + str(mass) + " MeV;  V " + str(Vmass) + " MeV;  Pion " + str(Pimass) + " MeV",cut)

closePDF(outfile_simp,c)

openPDF(outfile_ap,c)

for j in range(len(ap_events)):
    for i in range(len(plots2D)):
	    plot1 = getPlot(plots2D[i])
	    plot2 = getPlot2D(plots2D[i])
	    minX = getMinX2D(plots2D[i])
	    maxX = getMaxX2D(plots2D[i])
	    minY = getMinY(plots2D[i])
	    maxY = getMaxY(plots2D[i])
	    mass = GetMass1(ap_mass[i])
	    saveTuplePlot2D(ap_events[j],plot1,plot2,nBins,minX,maxX,maxY,minY,maxY,outfile,c,plot1,plot2,"A' " + str(mass) + " MeV",cut)

closePDF(outfile_ap,c)