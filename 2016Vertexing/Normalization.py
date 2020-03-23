import sys, array
tmpargv = sys.argv
sys.argv = []
import getopt
import ROOT
from ROOT import gROOT, TCanvas, TF1, TFile, gStyle, TFormula, TGraph, TGraphErrors, TH1D, TCutG, TH2D, gDirectory, TLegend
sys.argv = tmpargv

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'hw:r:t:d:', ['help',])

for opt, arg in options:
    if opt in ('-h', '--help'):
        print "\nUsage: "+sys.argv[0]+" <output basename>"
        print "Arguments: "
        print '\t-w: wab file path'
        print '\t-r: rad file path'
        print '\t-t: tritrig file path'
        print '\t-d: data file path'
        print "\n"
        sys.exit(0)

# Parse the command line arguments
for opt, arg in options:
		if opt=='-w':
			wabFilePath = arg
		if opt=='-r':
			radFilePath = arg
		if opt=='-t':
			triFilePath = arg
		if opt=='-d':
			dataFilePath = arg
		if opt=='-h':
			print_usage()
			sys.exit(0)

def tupleToMassHisto(events,histo,nBins,minX,maxX):
	events.Draw("{0}>>{1}({2},{3},{4})".format("uncM",histo,nBins,minX,maxX))
	histo = ROOT.gROOT.FindObject(histo)
	return histo

def tupleToPHisto(events,histo,nBins,minX,maxX):
	events.Draw("{0}>>{1}({2},{3},{4})".format("uncP",histo,nBins,minX,maxX))
	histo = ROOT.gROOT.FindObject(histo)
	return histo

def saveRadFracHisto(radMassHisto, triMassHisto, wabMassHisto, canvas):
	totalHisto = triMassHisto.Clone("total")
	totalHisto.Add(wabMassHisto)
	radfracHisto = radMassHisto.Clone("radfrac")
	radfracHisto.Divide(totalHisto)
	radfracHisto.GetXaxis().SetTitle("Invariant Mass [MeV]")
	radfracHisto.SetTitle("Radiative Fraction")
	radfracHisto.Draw()
	canvas.Print(outfile+".pdf")

def addTriWabHisto(triHisto, wabHisto):
	totalHisto = triHisto.Clone("total")
	totalHisto.Add(wabHisto)
	return totalHisto

def saveNHisto(radHisto, triHisto, wabHisto, dataHisto, sumHisto, canvas, XaxisTitle="", YaxisTitle="", PlotTitle=""):
	radHisto.SetLineColor(1)
	radHisto.GetXaxis().SetTitle(XaxisTitle)
	radHisto.GetYaxis().SetTitle(YaxisTitle)
	radHisto.SetTitle(PlotTitle)
	triHisto.SetLineColor(2)
	wabHisto.SetLineColor(3)
	dataHisto.SetLineColor(4)
	sumHisto.SetLineColor(7)
	radHisto.Draw()
	triHisto.Draw("same")
	wabHisto.Draw("same")
	dataHisto.Draw("same")
	sumHisto.Draw("same")
	legend = TLegend(.68,.66,.92,.87)
	legend.SetBorderSize(0)
	legend.SetFillColor(0)
	legend.SetFillStyle(0)
	legend.SetTextFont(42)
	legend.SetTextSize(0.035)
	legend.AddEntry(radHisto,"Rad","LP")
	legend.AddEntry(triHisto,"Trident","LP")
	legend.AddEntry(wabHisto,"Wab","LP")
	legend.AddEntry(dataHisto,"Data","LP")
	legend.AddEntry(sumHisto,"Trident + Wab","LP")
	legend.Draw()
	canvas.Print(outfile+".pdf")

def truthMatch(events,cut):
	cutevents = events.CopyTree(cut)
	return cutevents

def openPDF(outfile,canvas):
	c.Print(outfile+".pdf[")

def closePDF(outfile,canvas):
	c.Print(outfile+".pdf]")

gStyle.SetOptStat(0)
c = TCanvas("c","c",800,600)

parentID = 622
truthcut = "elepdgid==11&&pospdgid==-11&&eleparentID=={0}&&posparentID=={0}".format(parentID)

outfile = remainder[0]

radFile = TFile(radFilePath)
triFile = TFile(triFilePath)
wabFile = TFile(wabFilePath)
dataFile = TFile(dataFilePath)
radEvents = radFile.Get("ntuple")
triEvents = triFile.Get("ntuple")
wabEvents = wabFile.Get("ntuple")
dataEvents = dataFile.Get("ntuple")

nBins = 50
minMass = 0.0
maxMass = 0.2
minP = 0.0
maxP = 2.7
#width = 0.1
#scaling = nbins/width#500
radXS = 81.61 #microbarn
triXS = 1.416 #millibarn
wabXS = 0.1985 #barn
radNGen = 10000*10000
triNGen = 50000*2000
wabNGen = 100000*1000

dataLum = 1101 #nb^-1

radLum = radNGen / radXS
triLum = triNGen / triXS
wabLum = wabNGen / wabXS

weight = 1.

radEventsTruth = truthMatch(radEvents,truthcut)

radEventsTruth.SetWeight(weight/radLum)
triEvents.SetWeight(weight/triLum)
wabEvents.SetWeight(weight/wabLum)
dataEvents.SetWeight(weight/dataLum)

radMassHisto = tupleToMassHisto(radEventsTruth,"radMassHisto",nBins,minMass,maxMass)
triMassHisto = tupleToMassHisto(triEvents,"triMassHisto",nBins,minMass,maxMass)
wabMassHisto = tupleToMassHisto(wabEvents,"wabMassHisto",nBins,minMass,maxMass)
dataMassHisto = tupleToMassHisto(dataEvents,"dataMassHisto",nBins,minMass,maxMass)

radPHisto = tupleToPHisto(radEventsTruth,"radPHisto",nBins,minP,maxP)
triPHisto = tupleToPHisto(triEvents,"triPHisto",nBins,minP,maxP)
wabPHisto = tupleToPHisto(wabEvents,"wabPHisto",nBins,minP,maxP)
dataPHisto = tupleToPHisto(dataEvents,"dataPHisto",nBins,minP,maxP)

openPDF(outfile,c)

saveRadFracHisto(radMassHisto, triMassHisto, wabMassHisto, c)
massSumHisto = addTriWabHisto(triMassHisto, wabMassHisto)
pSumHisto = addTriWabHisto(triPHisto, wabPHisto)

saveNHisto(radMassHisto, triMassHisto, wabMassHisto, dataMassHisto, massSumHisto, c, "Invariant Mass [MeV]", "Cross Section [ub]", "")
saveNHisto(radPHisto, triPHisto, wabPHisto, dataPHisto, pSumHisto, c, "V0 Momentum [MeV]", "Cross Section [ub]", "")

closePDF(outfile,c)
