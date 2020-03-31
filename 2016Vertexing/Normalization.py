import sys, array
tmpargv = sys.argv
sys.argv = []
import getopt
import ROOT
from ROOT import gROOT, TCanvas, TF1, TFile, gStyle, TFormula, TGraph, TGraphErrors, TH1D, TCutG, TH2D, gDirectory, TLegend, TPad, TLatex
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

def tupleToMassHisto(events,histo,nBins,minX,maxX,factor):
	events.Draw("{0}>>{1}({2},{3},{4})".format("uncM",histo,nBins,minX,maxX))
	histo = ROOT.gROOT.FindObject(histo)
	histo.Sumw2()
	histo.Scale(factor)
	return histo

def tupleToTruthMassHisto(events,histo,nBins,minX,maxX,factor):
	eleMass = 0.00051099895
	truthMass = "sqrt(eleP^2+posP^2+2*{0}^2+2*sqrt((eleP^2+{0}^2)*(posP^2+{0}^2))-((elePX+posPX)^2+(elePY+posPY)^2+(elePZ+posPZ)^2))".format(eleMass)
	events.Draw("{0}>>{1}({2},{3},{4})".format(truthMass,histo,nBins,minX,maxX))
	histo = ROOT.gROOT.FindObject(histo)
	histo.Sumw2()
	histo.Scale(factor)
	return histo

def tupleToPHisto(events,histo,nBins,minX,maxX,factor):
	events.Draw("{0}>>{1}({2},{3},{4})".format("uncP",histo,nBins,minX,maxX))
	histo = ROOT.gROOT.FindObject(histo)
	histo.Sumw2()
	histo.Scale(factor)
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
	outfileroot.cd()
	radHisto.SetLineColor(1)
	radHisto.GetXaxis().SetTitle(XaxisTitle)
	radHisto.GetYaxis().SetTitle(YaxisTitle)
	radHisto.SetTitle(PlotTitle)
	maximum = radHisto.GetMaximum()
	if(triHisto.GetMaximum() > maximum):
		maximum = triHisto.GetMaximum()
	if(wabHisto.GetMaximum() > maximum):
		maximum = wabHisto.GetMaximum()
	if(dataHisto.GetMaximum() > maximum):
		maximum = dataHisto.GetMaximum()
	radHisto.GetYaxis().SetRangeUser(0,1.3*maximum)
	triHisto.SetLineColor(2)
	wabHisto.SetLineColor(3)
	dataHisto.SetLineColor(4)
	sumHisto.SetLineColor(7)
	radHisto.Draw()
	triHisto.Draw("same")
	wabHisto.Draw("same")
	dataHisto.Draw("same")
	sumHisto.Draw("same")
	radHisto.Write("Radiative {0}".format(XaxisTitle))
	triHisto.Write("Trident {0}".format(XaxisTitle))
	wabHisto.Write("Wab {0}".format(XaxisTitle))
	sumHisto.Write("e+e- Sum {0}".format(XaxisTitle))
	dataHisto.Write("Data {0}".format(XaxisTitle))
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
	canvas.Write()


def saveNHistoRatio(radHisto, triHisto, wabHisto, dataHisto, sumHisto, canvas, XaxisTitle="", YaxisTitle="", PlotTitle=""):	
	outfileroot.cd()
	canvas.Clear()
	RatioMin = 0.0
	RatioMax = 0.15

	top = TPad("top","top",0,0.42,1,1)
	top.SetLogy(1)
    
	bot = TPad("bot","bot",0,0,1,0.38)
    
	top.Draw()
	top.SetBottomMargin(0)
	#top.SetTopMargin(gStyle.GetPadTopMargin()*topScale)
	bot.Draw()
	bot.SetTopMargin(0)
	bot.SetBottomMargin(0.4)
	top.cd()

	radHisto.SetLineColor(1)
	radHisto.GetXaxis().SetTitle(XaxisTitle)
	radHisto.GetYaxis().SetTitle(YaxisTitle)
	radHisto.SetTitle(PlotTitle)
	maximum = radHisto.GetMaximum()
	if(triHisto.GetMaximum() > maximum):
		maximum = triHisto.GetMaximum()
	if(wabHisto.GetMaximum() > maximum):
		maximum = wabHisto.GetMaximum()
	if(dataHisto.GetMaximum() > maximum):
		maximum = dataHisto.GetMaximum()
	radHisto.GetYaxis().SetRangeUser(maximum/1e7,1.3*maximum)
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

	bot.cd()
	reference = sumHisto.Clone("reference")
	reference.GetYaxis().SetTitle("Radiative Fraction")
	reference.GetYaxis().SetTitleSize(0.06)
	reference.GetYaxis().SetLabelSize(0.1)
	reference.GetXaxis().SetTitleSize(0.1)
	reference.GetXaxis().SetLabelSize(0.1)
	reference.GetXaxis().SetTitle(XaxisTitle)
	reference.GetYaxis().SetRangeUser(RatioMin,RatioMax)
	reference.GetYaxis().SetNdivisions(508)
	reference.GetYaxis().SetDecimals(True)
	reference.Draw("axis")
	ratio = radHisto.Clone("Ratio"+radHisto.GetName())
	ratio.Divide(reference)
	ratio.SetLineColor(1)
	ratio.DrawCopy("pe same")
	canvas.Print(outfile+".pdf")
	canvas.Write()

def openPDF(outfile,canvas):
	c.Print(outfile+".pdf[")

def closePDF(outfile,canvas):
	c.Print(outfile+".pdf]")

gStyle.SetOptStat(0)
c = TCanvas("c","c",800,600)

parentID = 622
truthcut = "elepdgid==11&&pospdgid==-11&&eleparentID=={0}&&posparentID=={0}".format(parentID)

outfile = remainder[0]
outfileroot = TFile(remainder[0]+".root","RECREATE")

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
maxP = 2.5
#width = 0.1
#scaling = nbins/width#500
radXS = 81.61 #microbarn
triXS = 1.416*1000. #millibarn*1000
wabXS = 0.1985*1e6 #barn*1e6
radNGen = 10000*10000
triNGen = 50000*2000
wabNGen = 100000*1000

dataLum = 1101/1000 #nb^-1/1000

radLum = radNGen / radXS
triLum = triNGen / triXS
wabLum = wabNGen / wabXS

weight = 1.

file = TFile("rad_cut.root","recreate")
radEventsTruth = radEvents.CopyTree(truthcut)
radEventsTruth.Write()

#radEventsTruth.SetWeight(weight/radLum)
#triEvents.SetWeight(weight/triLum)
#wabEvents.SetWeight(weight/wabLum)
#dataEvents.SetWeight(weight/dataLum)

radMassHisto = tupleToTruthMassHisto(radEventsTruth,"radMassHisto",nBins,minMass,maxMass,weight/radLum)
triMassHisto = tupleToMassHisto(triEvents,"triMassHisto",nBins,minMass,maxMass,weight/triLum)
wabMassHisto = tupleToMassHisto(wabEvents,"wabMassHisto",nBins,minMass,maxMass,weight/wabLum)
dataMassHisto = tupleToMassHisto(dataEvents,"dataMassHisto",nBins,minMass,maxMass,weight/dataLum)

radPHisto = tupleToPHisto(radEventsTruth,"radPHisto",nBins/2,minP,maxP,weight/radLum)
triPHisto = tupleToPHisto(triEvents,"triPHisto",nBins/2,minP,maxP,weight/triLum)
wabPHisto = tupleToPHisto(wabEvents,"wabPHisto",nBins/2,minP,maxP,weight/wabLum)
dataPHisto = tupleToPHisto(dataEvents,"dataPHisto",nBins/2,minP,maxP,weight/dataLum)

openPDF(outfile,c)

saveRadFracHisto(radMassHisto, triMassHisto, wabMassHisto, c)
massSumHisto = addTriWabHisto(triMassHisto, wabMassHisto)
pSumHisto = addTriWabHisto(triPHisto, wabPHisto)

saveNHisto(radMassHisto, triMassHisto, wabMassHisto, dataMassHisto, massSumHisto, c, "Invariant Mass [MeV]", "d#sigma/dm [#mub/4 MeV]", "")
saveNHisto(radPHisto, triPHisto, wabPHisto, dataPHisto, pSumHisto, c, "V0 Momentum [GeV]", "d#sigma/dP [#mub/0.1 GeV]", "")
saveNHistoRatio(radMassHisto, triMassHisto, wabMassHisto, dataMassHisto, massSumHisto, c, "Invariant Mass [MeV]", "d#sigma/dm [#mub/4 MeV]", "")
saveNHistoRatio(radPHisto, triPHisto, wabPHisto, dataPHisto, pSumHisto, c, "V0 Momentum [GeV]", "d#sigma/dP [#mub/0.1 GeV]", "")

closePDF(outfile,c)
outfileroot.Close()
file.Close()