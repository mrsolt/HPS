import sys, array
tmpargv = sys.argv
sys.argv = []
import random
import numpy as np
import getopt
import ROOT
from ROOT import gROOT, TCanvas, TF1, TFile, gStyle, TFormula, TGraph, TGraphErrors, TH1D, TH1F, TCutG, TH2D, gDirectory, TLegend, TPad, TLatex
sys.argv = tmpargv

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'hw:r:t:d:p:', ['help',])

for opt, arg in options:
	if opt in ('-h', '--help'):
		print "\nUsage: "+sys.argv[0]+" <output basename>"
		print "Arguments: "
		print '\t-w: wab file path'
		print '\t-r: rad file path'
		print '\t-t: tritrig file path'
		print '\t-d: data file path'
		print '\t-p: radiative cut (default 0.0)'
		print "\n"
		sys.exit(0)

pcut = 0.0

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
		if opt=='-p':
			pcut = float(arg)
		if opt=='-h':
			print_usage()
			sys.exit(0)

def getEffTH1(hfile, hname):
	print 'Getting Efficiency Graph...converting to TH1'
	effGraph=hfile.Get(hname)
	effGraph.Print("v")
	xmin=effGraph.GetXaxis().GetXmin()
	xmax=effGraph.GetXaxis().GetXmax()
	xsize=effGraph.GetErrorXhigh(0)*2
	nbins=effGraph.GetN()
	nbinsHist=(int)((xmax-xmin)/xsize)
	x=ROOT.Double(0.0)
	y=ROOT.Double(0.0)
	effHist=ROOT.TH1D(effGraph.GetName(),effGraph.GetTitle(),nbinsHist,xmin,xmax)
	for i in range(0,nbins) :
		effGraph.GetPoint(i,x,y)
		histBin=effHist.FindBin(x)
		#print str(x)+' ' +str(y) + ' '+str(i)+ '  '+str(histBin)
		effHist.SetBinContent(histBin,y)
	return effHist

effSlopeFileName = 'EmGamma-L1HitEfficiencyResults-2016.root'
effRatioName = 'p2slopehps_007963.1GamEm_L1HitInefficiency'
effSlopeFile = ROOT.TFile(effSlopeFileName)
effSlopeData = getEffTH1(effSlopeFile,effRatioName)
effSlopeData.Print("v")

def RemoveHit(slp):
	rndm = random.random()
	ibin = effSlopeData.FindBin(slp)
	eff = 1 - effSlopeData.GetBinContent(ibin) #the slope "efficiency" is actually an inefficiency
	if rndm > eff:
		return True
	else:
		return False

def SmearHisto(events,nBins,minX,maxX):
	smear_Top5hits = 0.0589307
	smear_Top6hits = 0.0433669
	smear_Bot5hits = 0.0551252
	smear_Bot6hits = 0.045657
	histoMass = TH1F("histoMass","histoMass",nBins,minX,maxX)
	eleP = array.array('d',[0])
	posP = array.array('d',[0])
	uncM = array.array('d',[0])
	eleNTrackHits = array.array('d',[0])
	posNTrackHits = array.array('d',[0])
	eleTrkLambda = array.array('d',[0])
	posTrkLambda = array.array('d',[0])
	eleHasL1 = array.array('d',[0])
	posHasL1 = array.array('d',[0])

	events.Branch("eleP",eleP,"eleP/D")
	events.Branch("posP",posP,"posP/D")
	events.Branch("uncM",uncM,"uncM/D")
	events.Branch("eleNTrackHits",eleNTrackHits,"eleNTrackHits/I")
	events.Branch("posNTrackHits",posNTrackHits,"posNTrackHits/I")
	events.Branch("eleTrkLambda",eleTrkLambda,"eleTrkLambda/D")
	events.Branch("posTrkLambda",posTrkLambda,"posTrkLambda/D")
	events.Branch("eleHasL1",eleHasL1,"eleHasL1/I")
	events.Branch("posHasL1",posHasL1,"posHasL1/I")

	nevents = events.GetEntries()

	for entry in xrange(nevents):
		events.GetEntry(entry)
		killevent = False
		if(events.eleHasL1 and events.eleNTrackHits == 5):
			killevent = RemoveHit(events.eleTrkLambda)
		if(events.posHasL1 and events.posNTrackHits == 5):
			killevent = RemoveHit(events.posTrkLambda)
		if(killevent):
			continue
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

		MSmear = np.sqrt((P_positron_Smear/events.posP)*(P_electron_Smear/events.eleP))*events.uncM
		histoMass.Fill(MSmear)
		#histoMass.Fill(events.uncM)

	return histoMass

def tupleToMassHisto(events,histoname,nBins,minX,maxX,factor,cuts=""):
	#events.Draw("{0}>>{1}({2},{3},{4})".format("uncM",histo,nBins,minX,maxX),cuts)
	#histo = ROOT.gROOT.FindObject(histo)
	histo = SmearHisto(events,nBins,minX,maxX)
	histo.SetName(histoname)
	histo.Sumw2()
	histo.Scale(factor)
	return histo

def tupleToMassHistoData(events,histoname,nBins,minX,maxX,factor,cuts=""):
	events.Draw("{0}>>{1}({2},{3},{4})".format("uncM",histoname,nBins,minX,maxX),cuts)
	histo = ROOT.gROOT.FindObject(histoname)
	histo.Sumw2()
	histo.Scale(factor)
	return histo

def tupleToTruthMassHisto(events,histoname,nBins,minX,maxX,factor,output,cuts=""):
	eleP = array.array('d',[0])
	posP = array.array('d',[0])
	uncM = array.array('d',[0])
	eleNTrackHits = array.array('d',[0])
	posNTrackHits = array.array('d',[0])
	eleTrkLambda = array.array('d',[0])
	posTrkLambda = array.array('d',[0])
	eleHasL1 = array.array('d',[0])
	posHasL1 = array.array('d',[0])

	killevents = events.CloneTree(0)

	events.Branch("eleNTrackHits",eleNTrackHits,"eleNTrackHits/I")
	events.Branch("posNTrackHits",posNTrackHits,"posNTrackHits/I")
	events.Branch("eleTrkLambda",eleTrkLambda,"eleTrkLambda/D")
	events.Branch("posTrkLambda",posTrkLambda,"posTrkLambda/D")
	events.Branch("eleHasL1",eleHasL1,"eleHasL1/I")
	events.Branch("posHasL1",posHasL1,"posHasL1/I")

	nevents = events.GetEntries()
	for entry in xrange(nevents):
		events.GetEntry(entry)
		killevent = False
		if(events.eleHasL1 and events.eleNTrackHits == 5):
			killevent = RemoveHit(events.eleTrkLambda)
		if(events.posHasL1 and events.posNTrackHits == 5):
			killevent = RemoveHit(events.posTrkLambda)
		if(killevent):
			continue
		killevents.Fill()

	eleMass = 0.00051099895
	#truthMass = "sqrt(eleP^2+posP^2+2*{0}^2+2*sqrt((eleP^2+{0}^2)*(posP^2+{0}^2))-((elePX+posPX)^2+(elePY+posPY)^2+(elePZ+posPZ)^2))".format(eleMass)
	e1 = "sqrt({0}^2+{1}^2+{2}^2+{3}^2)".format('eleStartPX','eleStartPY','eleStartPZ',eleMass)
	e2 = "sqrt({0}^2+{1}^2+{2}^2+{3}^2)".format('posStartPX','posStartPY','posStartPZ',eleMass)
	esum = "({0}+{1})".format(e1,e2)
	psum = "sqrt(({0}+{1})^2+({2}+{3})^2+({4}+{5})^2)".format('eleStartPX','posStartPX','eleStartPY','posStartPY','eleStartPZ','posStartPZ')
	truthMass = "sqrt({0}^2-{1}^2)".format(esum,psum)
	killevents.Draw("{0}>>{1}({2},{3},{4})".format(truthMass,histoname,nBins,minX,maxX),cuts)
	histoRad = ROOT.gROOT.FindObject(histoname)
	histoRad.Sumw2()
	histoRad.Scale(factor)
	return histoRad

def tupleToPHisto(events,histo,nBins,minX,maxX,factor,cuts=""):
	events.Draw("{0}>>{1}({2},{3},{4})".format("uncM",histo,nBins,minX,maxX),cuts)
	histo = ROOT.gROOT.FindObject(histo)
	histo.Sumw2()
	histo.Scale(factor)
	return histo

def saveRadFracHisto(radMassHisto, triMassHisto, wabMassHisto, canvas):
	outfileroot.cd()
	totalHisto = triMassHisto.Clone("total")
	totalHisto.Add(wabMassHisto)
	radfracHisto = radMassHisto.Clone("radfrac")
	radfracHisto.Divide(totalHisto)
	radfracHisto.GetXaxis().SetTitle("Invariant Mass [MeV]")
	radfracHisto.SetTitle("Radiative Fraction")
	radfracHisto.GetYaxis().SetRangeUser(0,0.2)
	radfracHisto.GetXaxis().SetLabelSize(0.05)
	radfracHisto.GetYaxis().SetLabelSize(0.05)
	radfracHisto.GetXaxis().SetTitleOffset(0.8)
	radfracHisto.GetXaxis().SetTitleSize(0.06)
	radfracHisto.GetYaxis().SetTitleOffset(0.8)
	radfracHisto.GetYaxis().SetTitleSize(0.06)
	radfracHisto.Fit("pol5","pol5","",0.04,0.2)
	radfracHisto.SetStats(1)
	radfracHisto.Draw()
	outfileroot.cd()
	radfracHisto.Write("Radiative Fraction")
	canvas.Print(outfile+".pdf")
	canvas.Write()

def saveDataMassHisto(events,nBins,canvas):
	outfileroot.cd()
	massBin = 0.001
	maxMass = 0.2
	massbins = maxMass/massBin
	events.Draw("{0}>>{1}({2},{3},{4})".format("uncM","histo",massbins,0,maxMass))
	histo = ROOT.gROOT.FindObject("histo")
	histo.GetXaxis().SetTitle("Invariant Mass [MeV]")
	histo.GetYaxis().SetTitle("dN/dm [1/MeV]")
	histo.GetXaxis().SetLabelSize(0.05)
	histo.GetYaxis().SetLabelSize(0.05)
	histo.GetXaxis().SetTitleOffset(0.8)
	histo.GetXaxis().SetTitleSize(0.06)
	histo.GetYaxis().SetTitleOffset(0.8)
	histo.GetYaxis().SetTitleSize(0.06)
	histo.SetTitle("Radiative Selection Invariant Mass Distribution")
	histo.GetXaxis().SetRangeUser(0,0.2)
	histo.Sumw2()
	exppol5=TF1("exppol5","exp(pol5(0))",0.05,0.15)
	histo.Fit("exppol5","QR")
	histo.SetStats(1)
	histo.Draw()
	histo.Write("Data Mass")
	canvas.Print(outfile+".pdf")
	canvas.Write()

def addTriWabHisto(triHisto, wabHisto):
	totalHisto = triHisto.Clone("total")
	totalHisto.Add(wabHisto)
	return totalHisto

def saveNHisto(radHisto, triHisto, wabHisto, dataHisto, sumHisto, canvas, XaxisTitle="", YaxisTitle="", PlotTitle=""):
	outfileroot.cd()
	radHisto.SetLineColor(1)
	radHisto.GetXaxis().SetTitle(XaxisTitle)
	radHisto.GetYaxis().SetTitle(YaxisTitle)
	radHisto.GetXaxis().SetLabelSize(0.05)
	radHisto.GetYaxis().SetLabelSize(0.05)
	radHisto.GetXaxis().SetTitleOffset(0.8)
	radHisto.GetXaxis().SetTitleSize(0.06)
	radHisto.GetYaxis().SetTitleOffset(0.8)
	radHisto.GetYaxis().SetTitleSize(0.06)
	radHisto.SetTitle(PlotTitle)
	maximum = radHisto.GetMaximum()
	if(triHisto.GetMaximum() > maximum):
		maximum = triHisto.GetMaximum()
	if(wabHisto.GetMaximum() > maximum):
		maximum = wabHisto.GetMaximum()
	if(dataHisto.GetMaximum() > maximum):
		maximum = dataHisto.GetMaximum()
	if(sumHisto.GetMaximum() > maximum):
		maximum = sumHisto.GetMaximum()
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
	top.SetLogy(0)

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
	radHisto.GetXaxis().SetLabelSize(0.05)
	radHisto.GetYaxis().SetLabelSize(0.05)
	radHisto.GetXaxis().SetTitleOffset(0.8)
	radHisto.GetXaxis().SetTitleSize(0.06)
	radHisto.GetYaxis().SetTitleOffset(0.8)
	radHisto.GetYaxis().SetTitleSize(0.06)
	radHisto.SetTitle("Differential Cross Section")
	radHisto.SetStats(0)
	maximum = radHisto.GetMaximum()
	if(triHisto.GetMaximum() > maximum):
		maximum = triHisto.GetMaximum()
	if(wabHisto.GetMaximum() > maximum):
		maximum = wabHisto.GetMaximum()
	if(dataHisto.GetMaximum() > maximum):
		maximum = dataHisto.GetMaximum()
	if(sumHisto.GetMaximum() > maximum):
		maximum = sumHisto.GetMaximum()
	#radHisto.GetYaxis().SetRangeUser(maximum/1e7,1.3*maximum)
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
	reference.SetTitle("Radiative Fraction")
	#reference.GetYaxis().SetTitleSize(0.06)
	reference.GetYaxis().SetLabelSize(0.1)
	#reference.GetXaxis().SetTitleSize(0.1)
	reference.GetXaxis().SetLabelSize(0.1)

	reference.GetXaxis().SetTitleOffset(0.8)
	reference.GetXaxis().SetTitleSize(0.12)
	reference.GetYaxis().SetTitleOffset(0.4)
	reference.GetYaxis().SetTitleSize(0.1)

	reference.GetXaxis().SetTitle(XaxisTitle)
	reference.GetYaxis().SetRangeUser(RatioMin,RatioMax)
	reference.GetYaxis().SetNdivisions(508)
	reference.GetYaxis().SetDecimals(True)
	reference.Draw("axis")
	ratio = radHisto.Clone("Ratio"+radHisto.GetName())
	ratio.Divide(reference)
	ratio.SetLineColor(1)
	ratio.Fit("pol5","pol5","",0.04,0.2)
	ratio.GetXaxis().SetRangeUser(0,0.2)
	ratio.GetYaxis().SetRangeUser(0,0.2)
	ratio.GetYaxis().SetTitle("Radiative Fraction")
	ratio.SetTitle("Radiative Fraction")
	ratio.SetStats(0)
	ratio.DrawCopy("pe same")
	canvas.Print(outfile+".pdf")
	canvas.Write()

def openPDF(outfile,canvas):
	c.Print(outfile+".pdf[")

def closePDF(outfile,canvas):
	c.Print(outfile+".pdf]")

gStyle.SetOptFit(1)
gStyle.SetOptStat(0)
c = TCanvas("c","c",800,600)

parentID = 622
truthcut = "elepdgid==11&&pospdgid==-11&&eleparentID=={0}&&posparentID=={0}".format(parentID)
cuts = "eleHasL2&&posHasL2&&uncP>{0}".format(pcut)
#truthcut = ""

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

massBin = 0.001
minMass = 0.0
maxMass = 0.2
nBins = int(maxMass/massBin)
minP = 0.0
maxP = 2.5
#width = 0.1
#scaling = nbins/width#500
#radXS = 81.61 #microbarn
radXS = 66.36 #microbarn
triXS = 1.416*1000. #millibarn*1000
wabXS = 0.1985*1e6 #barn*1e6
radNGen = 10000*10000
triNGen = 50000*10000
wabNGen = 100000*10000

dataLum = 1101*1000 #nb^-1/1000

radLum = radNGen / radXS
triLum = triNGen / triXS
wabLum = wabNGen / wabXS

weight = 1.

file = TFile("rad_cut_{0}.root".format(outfile),"recreate")
radEventsTruth = radEvents.CopyTree(truthcut)
radEventsTruth.Write()

#radEventsTruth.SetWeight(weight/radLum)
#triEvents.SetWeight(weight/triLum)
#wabEvents.SetWeight(weight/wabLum)
#dataEvents.SetWeight(weight/dataLum)

radMassHisto = tupleToTruthMassHisto(radEventsTruth,"radMassHisto",nBins,minMass,maxMass,weight/radLum,outfile,cuts)
triMassHisto = tupleToMassHisto(triEvents,"triMassHisto",nBins,minMass,maxMass,weight/triLum,cuts)
wabMassHisto = tupleToMassHisto(wabEvents,"wabMassHisto",nBins,minMass,maxMass,weight/wabLum,cuts)
dataMassHisto = tupleToMassHistoData(dataEvents,"dataMassHisto",nBins,minMass,maxMass,weight/dataLum,cuts)

radPHisto = tupleToPHisto(radEventsTruth,"radPHisto",nBins/2,minP,maxP,weight/radLum,cuts)
triPHisto = tupleToPHisto(triEvents,"triPHisto",nBins/2,minP,maxP,weight/triLum,cuts)
wabPHisto = tupleToPHisto(wabEvents,"wabPHisto",nBins/2,minP,maxP,weight/wabLum,cuts)
dataPHisto = tupleToPHisto(dataEvents,"dataPHisto",nBins/2,minP,maxP,weight/dataLum,cuts)

openPDF(outfile,c)

saveDataMassHisto(dataEvents,nBins,c)
saveRadFracHisto(radMassHisto, triMassHisto, wabMassHisto, c)
massSumHisto = addTriWabHisto(triMassHisto, wabMassHisto)
pSumHisto = addTriWabHisto(triPHisto, wabPHisto)

gStyle.SetOptFit(0)
saveNHisto(radMassHisto, triMassHisto, wabMassHisto, dataMassHisto, massSumHisto, c, "Invariant Mass [MeV]", "d#sigma/dm [#mub/MeV]", "")
saveNHisto(radPHisto, triPHisto, wabPHisto, dataPHisto, pSumHisto, c, "V0 Momentum [GeV]", "d#sigma/dP [#mub/12.5 MeV]", "")
saveNHistoRatio(radMassHisto, triMassHisto, wabMassHisto, dataMassHisto, massSumHisto, c, "Invariant Mass [MeV]", "d#sigma/dm [#mub/MeV]", "Radiative Fraction")
saveNHistoRatio(radPHisto, triPHisto, wabPHisto, dataPHisto, pSumHisto, c, "V0 Momentum [GeV]", "d#sigma/dP [#mub/12.5 MeV]", "")

closePDF(outfile,c)
outfileroot.Close()
file.Close()
