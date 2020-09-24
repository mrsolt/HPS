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
		print ("\nUsage: "+sys.argv[0]+" <output basename>")
		print ("Arguments: ")
		print ('\t-w: wab file path')
		print ('\t-t: tritrig file path')
		print ('\t-d: data file path')
		print ('\t-p: radiative cut (default 0.0)')
		print ('\t-y: plot label (default "")')
		print ("\n")
		sys.exit(0)

pcut = 0.0
label = ""

# Parse the command line arguments
for opt, arg in options:
		if opt=='-w':
			wabFilePath = arg
		if opt=='-t':
			triFilePath = arg
		if opt=='-d':
			dataFilePath = arg
		if opt=='-p':
			pcut = float(arg)
		if opt=='-y':
			label = str(arg)
		if opt=='-h':
			print_usage()
			sys.exit(0)

def getEffTH1(hfile, hname):
	print ('Getting Efficiency Graph...converting to TH1')
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


def tupleToPHisto(events,histo,nBins,minX,maxX,factor,cuts=""):
	events.Draw("{0}>>{1}({2},{3},{4})".format("uncP",histo,nBins,minX,maxX),cuts)
	histo = ROOT.gROOT.FindObject(histo)
	histo.Sumw2()
	histo.Scale(factor)
	return histo

def addTriWabHisto(triHisto, wabHisto):
	totalHisto = triHisto.Clone("total")
	totalHisto.Add(wabHisto)
	return totalHisto

def saveNHisto(triHisto, wabHisto, dataHisto, sumHisto, canvas, XaxisTitle="", YaxisTitle="", PlotTitle=""):
	outfileroot.cd()
	triHisto.SetLineColor(1)
	triHisto.GetXaxis().SetTitle(XaxisTitle)
	triHisto.GetYaxis().SetTitle(YaxisTitle)
	triHisto.GetXaxis().SetLabelSize(0.05)
	triHisto.GetYaxis().SetLabelSize(0.05)
	triHisto.GetXaxis().SetTitleOffset(0.8)
	triHisto.GetXaxis().SetTitleSize(0.06)
	triHisto.GetYaxis().SetTitleOffset(0.8)
	triHisto.GetYaxis().SetTitleSize(0.06)
	triHisto.SetTitle(PlotTitle)
	maximum = triHisto.GetMaximum()
	if(wabHisto.GetMaximum() > maximum):
		maximum = wabHisto.GetMaximum()
	if(dataHisto.GetMaximum() > maximum):
		maximum = dataHisto.GetMaximum()
	if(sumHisto.GetMaximum() > maximum):
		maximum = sumHisto.GetMaximum()
	triHisto.GetYaxis().SetRangeUser(0,1.3*maximum)
	wabHisto.SetLineColor(3)
	dataHisto.SetLineColor(4)
	sumHisto.SetLineColor(2)
	triHisto.Draw()
	wabHisto.Draw("same")
	dataHisto.Draw("same")
	sumHisto.Draw("same")
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
	legend.AddEntry(triHisto,"Trident","LP")
	legend.AddEntry(wabHisto,"Wab","LP")
	legend.AddEntry(dataHisto,"Data","LP")
	legend.AddEntry(sumHisto,"Trident + Wab","LP")
	legend.Draw()
	canvas.Print(outfile+".pdf")
	canvas.Write()

def openPDF(outfile,canvas):
	c.Print(outfile+".pdf[")

def closePDF(outfile,canvas):
	c.Print(outfile+".pdf]")

gStyle.SetOptFit(1)
gStyle.SetOptStat(0)
c = TCanvas("c","c",800,600)

cuts = ""
L1L1cut = "eleHasL1&&posHasL1&&eleHasL2&&posHasL2"
L1L2cut = "((!eleHasL1&&posHasL1)||(eleHasL1&&!posHasL1))&&eleHasL2&&posHasL2"
L2L2cut = "!eleHasL1&&!posHasL1&&eleHasL2&&posHasL2"

outfile = remainder[0]
outfileroot = TFile(remainder[0]+".root","RECREATE")

triFile = TFile(triFilePath)
wabFile = TFile(wabFilePath)
dataFile = TFile(dataFilePath)
triEvents = triFile.Get("ntuple")
wabEvents = wabFile.Get("ntuple")
dataEvents = dataFile.Get("ntuple")

def NewEventsL1L1(events,type,outfile):
	eleNTrackHits = array.array('d',[0])
	posNTrackHits = array.array('d',[0])
	eleTrkLambda = array.array('d',[0])
	posTrkLambda = array.array('d',[0])

	file = TFile("dumL1L1_{0:}_{1}.root".format(type,outfile),"recreate")
	events1 = events.CloneTree(0)
	events2 = events.CloneTree(0)
	events3 = events.CloneTree(0)

	events1.SetName("ntuple_L1L1")
	events2.SetName("ntuple_L1L2")
	events3.SetName("ntuple_L2L2")

	events.Branch("eleNTrackHits",eleNTrackHits,"eleNTrackHits/I")
	events.Branch("posNTrackHits",posNTrackHits,"posNTrackHits/I")
	events.Branch("eleTrkLambda",eleTrkLambda,"eleTrkLambda/D")
	events.Branch("posTrkLambda",posTrkLambda,"posTrkLambda/D")

	nevents = events.GetEntries()

	for entry in xrange(nevents):
		events.GetEntry(entry)
		removehitEle = RemoveHit(events.eleTrkLambda)
		removehitPos = RemoveHit(events.posTrkLambda)
		if((removehitEle and events.eleNTrackHits == 5) or (removehitPos and events.posNTrackHits == 5)):
			continue
		elif((removehitEle and events.eleNTrackHits == 6) and (removehitPos and events.posNTrackHits == 6)):
			events3.Fill()
		elif((removehitEle and events.eleNTrackHits == 6) or (removehitPos and events.posNTrackHits == 6)):
			events2.Fill()
		elif(not removehitEle and not removehitPos):
			events1.Fill()
		else:
			print("You missed a category for L1L1")
	events1.AutoSave()
	events2.AutoSave()
	events3.AutoSave()
	del file
	return events1, events2, events3

def NewEventsL1L2(events,type,outfile):
	eleNTrackHits = array.array('d',[0])
	posNTrackHits = array.array('d',[0])
	eleTrkLambda = array.array('d',[0])
	posTrkLambda = array.array('d',[0])
	eleHasL1 = array.array('d',[0])
	posHasL1 = array.array('d',[0])

	file = TFile("dumL1L2_{0}_{1}.root".format(type,outfile),"recreate")
	events1 = events.CloneTree(0)
	events2 = events.CloneTree(0)
	events3 = events.CloneTree(0)

	events1.SetName("ntuple_L1L1")
	events2.SetName("ntuple_L1L2")
	events3.SetName("ntuple_L2L2")

	events.Branch("eleNTrackHits",eleNTrackHits,"eleNTrackHits/I")
	events.Branch("posNTrackHits",posNTrackHits,"posNTrackHits/I")
	events.Branch("eleTrkLambda",eleTrkLambda,"eleTrkLambda/D")
	events.Branch("posTrkLambda",posTrkLambda,"posTrkLambda/D")
	events.Branch("eleHasL1",eleHasL1,"eleHasL1/I")
	events.Branch("posHasL1",posHasL1,"posHasL1/I")

	nevents = events.GetEntries()

	for entry in xrange(nevents):
		events.GetEntry(entry)
		removehitEle = False
		removehitPos = False
		if(events.eleHasL1):
			removehitEle = RemoveHit(events.eleTrkLambda)
		if(events.posHasL1):
			removehitPos = RemoveHit(events.posTrkLambda)
		if((removehitEle and events.eleNTrackHits == 5) or (removehitPos and events.posNTrackHits == 5)):
			continue
		elif(not removehitEle and not removehitPos):
			events2.Fill()
		elif((removehitEle and events.eleNTrackHits == 6) or (removehitPos and events.posNTrackHits == 6)):
			events3.Fill()
		else:
			print("You missed a category for L1L1")
	events1.AutoSave()
	events2.AutoSave()
	events3.AutoSave()
	del file
	return events2, events3

def GetCategories(events,type,outfile):

	L1L1cut = "eleHasL1&&posHasL1"
	L1L2cut = "((!eleHasL1&&posHasL1)||(eleHasL1&&!posHasL1))"
	L2L2cut = "!eleHasL1&&!posHasL1"
	file = TFile("dum_laycut_{0}_{1}.root".format(type,outfile),"recreate")
	eventsL1L1 = events.CopyTree(L1L1cut)
	eventsL1L2 = events.CopyTree(L1L2cut)
	eventsL2L2 = events.CopyTree(L2L2cut)
	eventsL1L1.SetName("ntuple_L1L1")
	eventsL1L2.SetName("ntuple_L1L2")
	eventsL2L2.SetName("ntuple_L2L2")
	eventsL1L1.Write()
	eventsL1L2.Write()
	eventsL2L2.Write()

	newevents1, newevents2_L1L1, newevents3_L1L1 = NewEventsL1L1(eventsL1L1,type,outfile)
	newevents2_L1L2, newevents3_L1L2 = NewEventsL1L2(eventsL1L2, type,outfile)

	newevents1 = TChain("ntuple_L1L1")
	newevents1.Add("dumL1L1_{0}_{1}.root".format(type,outfile))
	newevents1.Add("dumL1L2_{0}_{1}.root".format(type,outfile))

	newevents2 = TChain("ntuple_L1L2")
	newevents2.Add("dumL1L1_{0}_{1}.root".format(type,outfile))
	newevents2.Add("dumL1L2_{0}_{1}.root".format(type,outfile))

	newevents3 = TChain("ntuple_L2L2")
	newevents3.Add("dumL1L1_{0}_{1}.root".format(type,outfile))
	newevents3.Add("dumL1L2_{0}_{1}.root".format(type,outfile))
	newevents3.Add("dum_laycut_{0}_{1}.root".format(type,outfile))

	return newevents0, newevents1, newevents2, newevents3

triEventsHitKillL1L1, triEventsHitKillL1L2, triEventsHitKillL2L2 = GetCategories(triEvents,"trident",outfile)
wabEventsHitKillL1L1, wabEventsHitKillL1L2, wabEventsHitKillL2L2 = GetCategories(wabEvents,"wab",outfile)

massBin = 0.001
minMass = 0.0
maxMass = 0.2
nBins = int(maxMass/massBin)
minP = 0.0
maxP = 2.5

triXS = 1.416*1000. #millibarn*1000
wabXS = 0.1985*1e6 #barn*1e6
triNGen = 50000*10000
wabNGen = 100000*10000

dataLum = 1101*1000 #nb^-1/1000

triLum = triNGen / triXS
wabLum = wabNGen / wabXS

weight = 1.

triPHisto = tupleToPHisto(triEvents,"triPHisto",nBins/2,minP,maxP,weight/triLum,cuts)
wabPHisto = tupleToPHisto(wabEvents,"wabPHisto",nBins/2,minP,maxP,weight/wabLum,cuts)
dataPHisto = tupleToPHisto(dataEvents,"dataPHisto",nBins/2,minP,maxP,weight/dataLum,cuts)
pSumHisto = addTriWabHisto(triPHisto, wabPHisto)

triPHistoL1L1 = tupleToPHisto(triEvents,"triPHistoL1L1",nBins/2,minP,maxP,weight/triLum,L1L1cut)
wabPHistoL1L1 = tupleToPHisto(wabEvents,"wabPHistoL1L1",nBins/2,minP,maxP,weight/wabLum,L1L1cut)
dataPHistoL1L1 = tupleToPHisto(dataEvents,"dataPHistoL1L1",nBins/2,minP,maxP,weight/dataLum,L1L1cut)
pSumHistoL1L1 = addTriWabHisto(triPHistoL1L1, wabPHistoL1L1)

triPHistoL1L2 = tupleToPHisto(triEvents,"triPHistoL1L2",nBins/2,minP,maxP,weight/triLum,L1L2cut)
wabPHistoL1L2 = tupleToPHisto(wabEvents,"wabPHistoL1L2",nBins/2,minP,maxP,weight/wabLum,L1L2cut)
dataPHistoL1L2 = tupleToPHisto(dataEvents,"dataPHistL1L2",nBins/2,minP,maxP,weight/dataLum,L1L2cut)
pSumHistoL1L2 = addTriWabHisto(triPHistoL1L2, wabPHistoL1L2)

triPHistoL2L2 = tupleToPHisto(triEvents,"triPHistoL2L2",nBins/2,minP,maxP,weight/triLum,L2L2cut)
wabPHistoL2L2 = tupleToPHisto(wabEvents,"wabPHistoL2L2",nBins/2,minP,maxP,weight/wabLum,L2L2cut)
dataPHistoL2L2 = tupleToPHisto(dataEvents,"dataPHistoL2L2",nBins/2,minP,maxP,weight/dataLum,L2L2cut)
pSumHistoL2L2 = addTriWabHisto(triPHistoL2L2, wabPHistoL2L2)

triPHistoL1L1HitKill = tupleToPHisto(triEventsHitKillL1L1,"triPHistoL1L1HitKill",nBins/2,minP,maxP,weight/triLum,L1L1cut)
wabPHistoL1L1HitKill = tupleToPHisto(wabEventsHitKillL1L1,"wabPHistoL1L1HitKill",nBins/2,minP,maxP,weight/wabLum,L1L1cut)
pSumHistoL1L1HitKill = addTriWabHisto(triPHistoL1L1HitKill, wabPHistoL1L1HitKill)

triPHistoL1L2HitKill = tupleToPHisto(triEventsHitKillL1L2,"triPHistoL1L2HitKill",nBins/2,minP,maxP,weight/triLum,L1L2cut)
wabPHistoL1L2HitKill = tupleToPHisto(wabEventsHitKillL1L2,"wabPHistoL1L2HitKill",nBins/2,minP,maxP,weight/wabLum,L1L2cut)
pSumHistoL1L2HitKill = addTriWabHisto(triPHistoL1L2HitKill, wabPHistoL1L2HitKill)

triPHistoL2L2HitKill = tupleToPHisto(triEventsHitKillL2L2,"triPHistoL2L2HitKill",nBins/2,minP,maxP,weight/triLum,L2L2cut)
wabPHistoL2L2HitKill = tupleToPHisto(wabEventsHitKillL2L2,"wabPHistoL2L2HitKill",nBins/2,minP,maxP,weight/wabLum,L2L2cut)
pSumHistoL2L2HitKill = addTriWabHisto(triPHistoL2L2HitKill, wabPHistoL2L2HitKill)

triPHistoHitKill = triPHistoL1L1HitKill.Clone()
triPHistoHitKill.Add(triPHistoL1L2HitKill)
triPHistoHitKill.Add(triPHistoL2L2HitKill)
wabPHistoHitKill = wabPHistoL1L1HitKill.Clone()
wabPHistoHitKill.Add(wabPHistoL1L2HitKill)
wabPHistoHitKill.Add(wabPHistoL2L2HitKill)
pSumHistoHitKill = addTriWabHisto(triPHistoHitKill, wabPHistoHitKill)

openPDF(outfile,c)

gStyle.SetOptFit(0)
saveNHisto(triPHisto, wabPHisto, dataPHisto, pSumHisto, c, "V0 Momentum [GeV]", "d#sigma/dP [#mub/12.5 MeV]", "{0}".format(label))
saveNHisto(triPHistoL1L1, wabPHistoL1L1, dataPHistoL1L1, pSumHistoL1L1, c, "V0 Momentum [GeV]", "d#sigma/dP [#mub/12.5 MeV]", "{0} L1L1".format(label))
saveNHisto(triPHistoL1L2, wabPHistoL1L2, dataPHistoL1L2, pSumHistoL1L2, c, "V0 Momentum [GeV]", "d#sigma/dP [#mub/12.5 MeV]", "{0} L1L2".format(label))
saveNHisto(triPHistoL2L2, wabPHistoL2L2, dataPHistoL2L2, pSumHistoL2L2, c, "V0 Momentum [GeV]", "d#sigma/dP [#mub/12.5 MeV]", "{0} L2L2".format(label))

saveNHisto(triPHistoHitKill, wabPHistoHitKill, dataPHisto, pSumHistoHitKill, c, "V0 Momentum [GeV]", "d#sigma/dP [#mub/12.5 MeV]", "{0} with Hit Killing".format(label))
saveNHisto(triPHistoL1L1HitKill, wabPHistoL1L1HitKill, dataPHistoL1L1, pSumHistoL1L1HitKill, c, "V0 Momentum [GeV]", "d#sigma/dP [#mub/12.5 MeV]", "{0} L1L1 with Hit Killing".format(label))
saveNHisto(triPHistoL1L2HitKill, wabPHistoL1L2HitKill, dataPHistoL1L2, pSumHistoL1L2HitKill, c, "V0 Momentum [GeV]", "d#sigma/dP [#mub/12.5 MeV]", "{0} L1L2 with Hit Killing".format(label))
saveNHisto(triPHistoL2L2HitKill, wabPHistoL2L2HitKill, dataPHistoL2L2, pSumHistoL2L2HitKill, c, "V0 Momentum [GeV]", "d#sigma/dP [#mub/12.5 MeV]", "{0} L2L2 with Hit Killing".format(label))

closePDF(outfile,c)
outfileroot.Close()
file.Close()
