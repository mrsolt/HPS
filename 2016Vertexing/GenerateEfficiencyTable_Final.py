#!/usr/bin/env python
#Author Matt Solt mrsolt@slac.stanford.edu
import sys
import array, math
import numpy as np
import random
import root_numpy, numpy
import ROOT
from ROOT import gROOT, gStyle, TFile, TTree, TChain, TMVA, TCut, TCanvas, gDirectory, TH1, TGraph, gPad, TF1, TH1F, TLegend, TLatex, TGraphErrors
import getopt

def print_usage():
	print "\nUsage: {0} <output file basename> <input recon files list> <input recon truth tuple files list>".format(sys.argv[0])
	print "Arguments: "
	print '\t-e: use this beam energy <default 2.3 GeV>'
	print '\t-t: use this target position <default -4.3 mm>'
	print '\t-n: number of bins in histograms <default 50>'
	print '\t-z: total range in z covered <default 100 mm>'
	print '\t-T: plot Test plots'
	print '\t-s: tuple name <default is "ntuple">'
	print '\t-c: cut tracks with shared hits <default is false>'
	print '\t-u: use zcut <default is false>'
	print '\t-v: use unblinded data <default is true>'
	print '\t-S: shift in L1L2 zcut 10% <default is 0.0>'
	print '\t-h: this help message'
	print

#Default Values
eBeam = 2.3
makeTestPlots = False
killInTrackSlope = True
targZ = -4.3
nBins = 50
zRange = 100
removeSharedHits = False
zcut = False
unblind = True
tupleName = "ntuple"
zshift = 0.0

#Function to plot efficiency tests of known masses
def plotTest(iMass,inputFile,output,targZ,maxZ,canvas):
	inputfile = open(inputFile,"r")
	mass = []
	z = []
	result = []
	eff = []
	#Readlines from input file
	lines = inputfile.readlines()
	for x in lines:
		result.append(x.split())
	inputfile.close()
	nMass = len(result[0])
	nBins = len(result[1])
	#Grab Array of Masses
	for i in range(nMass):
		mass.append(float(result[0][i]))
	#Grab Array of z's
	for i in range(nBins):
		z.append(float(result[1][i]))
	#Convert the strings from input file into floats
	for i in range(nMass):
		dummy = []
		for j in range(nBins):
			dummy.append(float(result[i+2][j]))
		eff.append(dummy)
		del dummy
	#define histograms
	histo1 = TH1F("histo1","histo1",nBins-1,targZ,maxZ) #test histogram
	histo2 = TH1F("histo2","histo2",nBins,targZ,maxZ) #known histogram
	#Use the mass greater than and less than the mass of interest
	iMass1 = iMass - 1
	iMass2 = iMass + 1
	for i in range(nBins-1):
		iZ1 = i
		iZ2 = i + 1
		Q11 = eff[iMass1][iZ1]
		Q12 = eff[iMass2][iZ1]
		Q21 = eff[iMass1][iZ2]
		Q22 = eff[iMass2][iZ2]
		#Interpolate value
		interpolate = Bilinear(z[i],mass[iMass],z[iZ1],z[iZ2],mass[iMass1],mass[iMass2],Q11,Q12,Q21,Q22)
		histo1.SetBinContent(i+1,interpolate)
	for i in range(nBins):
		histo2.SetBinContent(i+1,eff[iMass][i])
	#Draw Histograms
	legend = TLegend(.68,.66,.92,.87)
	legend.SetBorderSize(0)
	legend.SetFillColor(0)
	legend.SetFillStyle(0)
	legend.SetTextFont(42)
	legend.SetTextSize(0.035)
	legend.AddEntry(histo1,"Interpolation","LP")
	legend.AddEntry(histo2,"MC","LP")
	maximum = histo1.GetMaximum()
	if(histo2.GetMaximum() > maximum): maximum = histo2.GetMaximum()
	histo1.Draw("")
	histo1.GetXaxis().SetTitle("z [mm]")
	histo1.SetTitle("A' Efficiency {0:0.3f} GeV".format(mass[iMass]))
	histo1.GetYaxis().SetRangeUser(0,maximum*1.2)
	histo2.Draw("same")
	histo2.SetLineColor(2)
	legend.Draw("")
	gStyle.SetOptStat(0)
	canvas.Print(output+".pdf")

#Function to plot efficiency tests of known masses
def Interpolate(Mass,Z,mass,z,eff):
	iMass = 0
	iZ = 0
	#Grab the index of mass and z
	for i in range(nMass):
		if(Mass < mass[i]):
			iMass = i
			break
	for i in range(nBins):
		if(Z < z[i]):
			iZ = i
			break
	#Check to make sure mass and z are not out of range
	if(iMass == 0):
		print "Mass is out of range!"
		return
	if(iZ == 0):
		print "Z is behind target!"
		return
	iMass1 = iMass - 1
	iMass2 = iMass
	iZ1 = iZ - 1
	iZ2 = iZ
	Q11 = eff[iMass1][iZ1]
	Q12 = eff[iMass2][iZ1]
	Q21 = eff[iMass1][iZ2]
	Q22 = eff[iMass2][iZ2]
	#Interpolate value
	interpolate = Bilinear(Z,Mass,z[iZ1],z[iZ2],mass[iMass1],mass[iMass2],Q11,Q12,Q21,Q22)
	return interpolate

#Function to plot efficiency tests of known masses directly from file
def InterpolateFromFile(Mass,Z,inputFile):
	mass = getMassArray(inputFile)
	z = getZArray(inputFile)
	eff = getEfficiency(inputFile)
	interpolate = Interpolate(Mass,Z,mass,z,eff)
	return interpolate

def getMassArray(inputFile):
	inputfile = open(inputFile,"r")
	mass = []
	result = []
	#Readlines from input file
	lines = inputfile.readlines()
	for x in lines:
		result.append(x.split())
	inputfile.close()
	nMass = len(result[0])
	#Grab Array of Masses
	for i in range(nMass):
		mass.append(float(result[0][i]))
	return mass

def getZArray(inputFile):
	inputfile = open(inputFile,"r")
	z = []
	result = []
	#Readlines from input file
	lines = inputfile.readlines()
	for x in lines:
		result.append(x.split())
	inputfile.close()
	nBins = len(result[1])
	#Grab Array of z's
	for i in range(nBins):
		z.append(float(result[1][i]))
	return z

def getEfficiency(inputFile):
	inputfile = open(inputFile,"r")
	result = []
	eff = []
	#Readlines from input file
	lines = inputfile.readlines()
	for x in lines:
		result.append(x.split())
	inputfile.close()
	nMass = len(result[0])
	nBins = len(result[1])
	#Convert the strings from input file into floats
	for i in range(nMass):
		dummy = []
		for j in range(nBins):
				dummy.append(float(result[i+2][j]))
		eff.append(dummy)
		del dummy
	return eff

#Function for Bilinear interpolation
def Bilinear(x,y,x1,x2,y1,y2,Q11,Q12,Q21,Q22):
	denom = (x2-x1)*(y2-y1)
	t1 = (x2-x)*(y2-y)/denom*Q11
	t2 = (x-x1)*(y2-y)/denom*Q21
	t3 = (x2-x)*(y-y1)/denom*Q12
	t4 = (x-x1)*(y-y1)/denom*Q22
	return t1+t2+t3+t4

def plotEff(histos,histosTruth,normArr,output,outPDF,outfileroot,canvas,mass,useNorm,title=""):
	outfileroot.cd()
	canvas.Clear()
	legend = TLegend(.68,.50,.92,.97)
	legend.SetBorderSize(0)
	legend.SetFillColor(0)
	legend.SetFillStyle(0)
	legend.SetTextFont(42)
	legend.SetTextSize(0.035)
	maximum = 0
	histos_copy = []
	for i in range(len(mass)):
		histos_copy.append(histos[i].Clone())

	for i in range(len(mass)):
		histos_copy[i].SetLineColor(i+1)
		histos_copy[i].Divide(histosTruth[i])
		if(useNorm):
			histos_copy[i].Scale(1/normArr[i])
		if(histos[i].GetMaximum() > maximum):
			maximum = histos_copy[i].GetMaximum()
		legend.AddEntry(histos_copy[i],str("%.3g" % (mass[i] * 1000))+" MeV","LP")
		if(i == 0):
			histos_copy[i].Draw()
			histos_copy[i].SetStats(0)
			histos_copy[i].GetXaxis().SetTitle("z [mm]")
			histos_copy[i].GetYaxis().SetTitle("efficiency")
			histos_copy[i].SetTitle("A' Acceptance * Efficiency {0}".format(title))
		else:
			histos_copy[i].Draw("same")
	histos_copy[0].GetYaxis().SetRangeUser(0,1.3*maximum)
	legend.Draw()
	canvas.Print(output+".png")
	canvas.Print(outPDF+".pdf")
	canvas.Write()
	del histos_copy

def plotAll(histosL1L1,histosL1L2,histosL2L2,histosTruth,normArr,output,outPDF,outfileroot,canvas,mass,title=""):
	outfileroot.cd()
	maximum = 0
	histos_copy_L1L1 = []
	histos_copy_L1L2 = []
	histos_copy_L2L2 = []
	for i in range(len(mass)):
		histos_copy_L1L1.append(histosL1L1[i].Clone())
		histos_copy_L1L2.append(histosL1L2[i].Clone())
		histos_copy_L2L2.append(histosL2L2[i].Clone())

	for i in range(len(mass)):
		canvas.Clear()
		histos_copy_L1L1[i].SetLineColor(1)
		histos_copy_L1L2[i].SetLineColor(2)
		histos_copy_L2L2[i].SetLineColor(4)
		histos_copy_L1L1[i].Divide(histosTruth[i])
		histos_copy_L1L2[i].Divide(histosTruth[i])
		histos_copy_L2L2[i].Divide(histosTruth[i])
		sumhisto = histos_copy_L1L1[i].Clone()
		sumhisto.Add(histos_copy_L1L2[i])
		sumhisto.Add(histos_copy_L2L2[i])
		sumhisto.SetLineColor(28)
		maximum = sumhisto.GetMaximum()
		legend = TLegend(.68,.70,.92,.90)
		legend.SetBorderSize(0)
		legend.SetFillColor(0)
		legend.SetFillStyle(0)
		legend.SetTextFont(42)
		legend.SetTextSize(0.05)
		legend.AddEntry(histos_copy_L1L1[i],"L1L1","LP")
		legend.AddEntry(histos_copy_L1L2[i],"L1L2","LP")
		legend.AddEntry(histos_copy_L2L2[i],"L2L2","LP")
		legend.AddEntry(sumhisto,"Sum","LP")
		histos_copy_L1L1[i].Draw()
		histos_copy_L1L1[i].SetStats(0)
		histos_copy_L1L1[i].GetXaxis().SetTitle("z [mm]")
		histos_copy_L1L1[i].GetYaxis().SetTitle("efficiency")
		histos_copy_L1L1[i].GetXaxis().SetLabelSize(0.05)
		histos_copy_L1L1[i].GetYaxis().SetLabelSize(0.05)
		histos_copy_L1L1[i].GetZaxis().SetLabelSize(0.05)
		histos_copy_L1L1[i].GetXaxis().SetTitleOffset(0.8)
		histos_copy_L1L1[i].GetXaxis().SetTitleSize(0.06)
		histos_copy_L1L1[i].GetYaxis().SetTitleOffset(0.8)
		histos_copy_L1L1[i].GetYaxis().SetTitleSize(0.06)
		histos_copy_L1L1[i].SetTitle("A' Acceptance * Efficiency {0:0.0f} MeV A' {1}".format(mass[i]*1000,title))
		histos_copy_L1L1[i].GetYaxis().SetRangeUser(0,1.3*maximum)
		histos_copy_L1L2[i].Draw("same")
		histos_copy_L2L2[i].Draw("same")
		sumhisto.Draw("same")
		legend.Draw()
		canvas.Print(output+".png")
		canvas.Print(outPDF+".pdf")
		canvas.Write()

		canvas.Clear()
		histos_copy_L1L1[i].Scale(1/normArr[i])
		histos_copy_L1L2[i].Scale(1/normArr[i])
		histos_copy_L2L2[i].Scale(1/normArr[i])
		sumhistonorm = histos_copy_L1L1[i].Clone()
		sumhistonorm.Add(histos_copy_L1L2[i])
		sumhistonorm.Add(histos_copy_L2L2[i])
		sumhistonorm.SetLineColor(28)
		maximum = sumhistonorm.GetMaximum()
		histos_copy_L1L1[i].Draw()
		histos_copy_L1L1[i].SetStats(0)
		histos_copy_L1L1[i].GetXaxis().SetTitle("Truth z [mm]")
		histos_copy_L1L1[i].GetYaxis().SetTitle("efficiency")
		histos_copy_L1L1[i].SetTitle("Normalized A' Acceptance * Efficiency {0:0.0f} MeV A' {1}".format(mass[i]*1000,title))
		histos_copy_L1L1[i].GetYaxis().SetRangeUser(0,1.3*maximum)
		histos_copy_L1L2[i].Draw("same")
		histos_copy_L2L2[i].Draw("same")
		sumhistonorm.Draw("same")
		legend.Draw()
		canvas.Print(output+".png")
		canvas.Print(outPDF+".pdf")
		canvas.Write()
		del sumhisto
		del sumhistonorm
		del legend
	del histos_copy_L1L1
	del histos_copy_L1L2
	del histos_copy_L2L2

def plotFit(histoL1L1,histoL1L2,histoL2L2,histoTruth,normArr,outPDF,outfileroot,canvas,mass,targZ,title=""):
	outfileroot.cd()
	maximum = 0
	histo_copy_L1L1 = histoL1L1.Clone()
	histo_copy_L1L2 = histoL1L2.Clone()
	histo_copy_L2L2 = histoL2L2.Clone()

	canvas.Clear()
	histo_copy_L1L1.SetLineColor(1)
	histo_copy_L1L2.SetLineColor(2)
	histo_copy_L2L2.SetLineColor(4)
	histo_copy_L1L1.Divide(histoTruth)
	histo_copy_L1L2.Divide(histoTruth)
	histo_copy_L2L2.Divide(histoTruth)
	sumhisto = histo_copy_L1L1.Clone()
	sumhisto.Add(histo_copy_L1L2)
	sumhisto.Add(histo_copy_L2L2)
	sumhisto.SetLineColor(28)
	#fit = sumhisto.Fit("exppol4","QR")
	fit = sumhisto.Fit(exppol4,"LSQIM")
	maximum = sumhisto.GetMaximum()
	legend = TLegend(.68,.70,.92,.90)
	legend.SetBorderSize(0)
	legend.SetFillColor(0)
	legend.SetFillStyle(0)
	legend.SetTextFont(42)
	legend.SetTextSize(0.05)
	legend.AddEntry(histo_copy_L1L1,"L1L1","LP")
	legend.AddEntry(histo_copy_L1L2,"L1L2","LP")
	legend.AddEntry(histo_copy_L2L2,"L2L2","LP")
	legend.AddEntry(sumhisto,"Sum","LP")
	histo_copy_L1L1.SetStats(0)
	histo_copy_L1L1.Draw()
	histo_copy_L1L1.GetXaxis().SetTitle("Truth z [mm]")
	histo_copy_L1L1.GetYaxis().SetTitle("efficiency")
	histo_copy_L1L1.GetXaxis().SetLabelSize(0.05)
	histo_copy_L1L1.GetYaxis().SetLabelSize(0.05)
	histo_copy_L1L1.GetZaxis().SetLabelSize(0.05)
	histo_copy_L1L1.GetXaxis().SetTitleOffset(0.8)
	histo_copy_L1L1.GetXaxis().SetTitleSize(0.06)
	histo_copy_L1L1.GetYaxis().SetTitleOffset(0.8)
	histo_copy_L1L1.GetYaxis().SetTitleSize(0.06)
	histo_copy_L1L1.SetTitle("A' Acceptance * Efficiency {0:0.0f} MeV A' {1}".format(mass*1000,title))
	histo_copy_L1L1.GetYaxis().SetRangeUser(0,1.3*maximum)
	histo_copy_L1L2.Draw("same")
	histo_copy_L2L2.Draw("same")
	sumhisto.Draw("same")
	legend.Draw()
	canvas.Print(outPDF+".pdf")
	canvas.Write()

	print("{0}  {1}".format(fit.Get().Parameter(0), fit.Get().ParError(0)))
	print("{0}  {1}".format(fit.Get().Parameter(1), fit.Get().ParError(1)))
	print("{0}  {1}".format(fit.Get().Parameter(2), fit.Get().ParError(2)))
	print("{0}  {1}".format(fit.Get().Parameter(3), fit.Get().ParError(3)))
	print("{0}  {1}".format(fit.Get().Parameter(4), fit.Get().ParError(4)))

	norm = exppol4.Eval(targZ)
	norm_min = []

	exppol4_m.SetParameters(fit.Get().Parameter(0)-fit.Get().ParError(0),fit.Get().Parameter(1),fit.Get().Parameter(2),
		fit.Get().Parameter(3),fit.Get().Parameter(4))
	norm_min.append(exppol4_m.Eval(targZ))
	exppol4_m.SetParameters(fit.Get().Parameter(0),fit.Get().Parameter(1)-fit.Get().ParError(1),fit.Get().Parameter(2),
		fit.Get().Parameter(3),fit.Get().Parameter(4))
	norm_min.append(exppol4_m.Eval(targZ))
	exppol4_m.SetParameters(fit.Get().Parameter(0),fit.Get().Parameter(1),fit.Get().Parameter(2)-fit.Get().ParError(2),
		fit.Get().Parameter(3),fit.Get().Parameter(4))
	norm_min.append(exppol4_m.Eval(targZ))
	exppol4_m.SetParameters(fit.Get().Parameter(0),fit.Get().Parameter(1),fit.Get().Parameter(2),
		fit.Get().Parameter(3)-fit.Get().ParError(3),fit.Get().Parameter(4))
	norm_min.append(exppol4_m.Eval(targZ))
	exppol4_m.SetParameters(fit.Get().Parameter(0),fit.Get().Parameter(1),fit.Get().Parameter(2),
		fit.Get().Parameter(3),fit.Get().Parameter(4)-fit.Get().ParError(4))
	norm_min.append(exppol4_m.Eval(targZ))

	error_min = 0
	for i in range(len(norm_min)):
		error = (norm - norm_min[i])/norm
		print("{0}  {1}".format(i,error))
		error_min = math.sqrt(error_min*error_min + error * error)
	norm_sig = error_min * norm

	norm_plus = []

	exppol4_p.SetParameters(fit.Get().Parameter(0)+fit.Get().ParError(0),fit.Get().Parameter(1),fit.Get().Parameter(2),
		fit.Get().Parameter(3),fit.Get().Parameter(4))
	norm_plus.append(exppol4_p.Eval(targZ))
	exppol4_p.SetParameters(fit.Get().Parameter(0),fit.Get().Parameter(1)+fit.Get().ParError(1),fit.Get().Parameter(2),
		fit.Get().Parameter(3),fit.Get().Parameter(4))
	norm_plus.append(exppol4_p.Eval(targZ))
	exppol4_p.SetParameters(fit.Get().Parameter(0),fit.Get().Parameter(1),fit.Get().Parameter(2)+fit.Get().ParError(2),
		fit.Get().Parameter(3),fit.Get().Parameter(4))
	norm_plus.append(exppol4_p.Eval(targZ))
	exppol4_p.SetParameters(fit.Get().Parameter(0),fit.Get().Parameter(1),fit.Get().Parameter(2),
		fit.Get().Parameter(3)+fit.Get().ParError(3),fit.Get().Parameter(4))
	norm_plus.append(exppol4_p.Eval(targZ))
	exppol4_p.SetParameters(fit.Get().Parameter(0),fit.Get().Parameter(1),fit.Get().Parameter(2),
		fit.Get().Parameter(3),fit.Get().Parameter(4)+fit.Get().ParError(4))
	norm_plus.append(exppol4_p.Eval(targZ))

	error_plus = 0
	for i in range(len(norm_plus)):
		error = (norm - norm_plus[i])/norm
		print("{0}  {1}".format(i,error))
		error_plus = math.sqrt(error_plus*error_plus + error * error)
	norm_psig = error_plus * norm

	#exppol4_m.SetParameters(fit.Get().Parameter(0)-fit.Get().ParError(0),fit.Get().Parameter(1)-fit.Get().ParError(1),fit.Get().Parameter(2)-fit.Get().ParError(2),
	#    fit.Get().Parameter(3)-fit.Get().ParError(3),fit.Get().Parameter(4)-fit.Get().ParError(4))
	#norm_sig = exppol4_m.Eval(targZ)
	#exppol4_p.SetParameters(fit.Get().Parameter(0)+fit.Get().ParError(0),fit.Get().Parameter(1)+fit.Get().ParError(1),fit.Get().Parameter(2)+fit.Get().ParError(2),
	#    fit.Get().Parameter(3)+fit.Get().ParError(3),fit.Get().Parameter(4)+fit.Get().ParError(4))
	#norm_psig = exppol4_p.Eval(targZ)

	del sumhisto
	del legend
	del histo_copy_L1L1
	del histo_copy_L1L2
	del histo_copy_L2L2
	del norm_min
	del norm_plus
	return norm, norm_sig, norm_psig

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

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'e:t:n:z:Tcuvs:S:h')

# Parse the command line arguments
for opt, arg in options:
	if opt=='-e':
		eBeam=float(arg)
	if opt=='-t':
		targZ=float(arg)
	if opt=='-n':
		nBins=int(arg)
	if opt=='-z':
		zRange=float(arg)
	if opt=='-T':
		makeTestPlots = True
	if opt=='-c':
		removeSharedHits = True
	if opt=='-u':
		zcut = True
	if opt=='-v':
		unblind = False
	if opt=='-s':
		tupleName = str(arg)
	if opt=='-S':
		zshift = float(arg)
	if opt=='-h':
		print_usage()
		sys.exit(0)

if len(remainder)!=3:
	print_usage()
	sys.exit(0)

if killInTrackSlope:
	#effSlopeFileName = '/home/mrsolt/hps/test/EmGamma-L1HitEfficiencyResults-2016.root'
	effSlopeFileName = 'EmGamma-L1HitEfficiencyResults-2016.root'
	effRatioName = 'p2slopehps_007963.1GamEm_L1HitInefficiency'
	effSlopeFile = ROOT.TFile(effSlopeFileName)
	effSlopeData = getEffTH1(effSlopeFile,effRatioName)
	effSlopeData.Print("v")

total = TH1F("total","total",nBins,-0.08,0.08)
passed = TH1F("passed","passed",nBins,-0.08,0.08)

def RemoveHit(slp):
	rndm = random.random()
	ibin = effSlopeData.FindBin(slp)
	eff = 1 - effSlopeData.GetBinContent(ibin) #the slope "efficiency" is actually an inefficiency
	total.Fill(slp)
	if rndm > eff:
	#if rndm > 0.8:
		return True
	else:
		passed.Fill(slp)
		return False

def NewEventsL1L1(events,mass,outfile):
	eleNTrackHits = array.array('d',[0])
	posNTrackHits = array.array('d',[0])
	eleTrkLambda = array.array('d',[0])
	posTrkLambda = array.array('d',[0])

	file = TFile("dumL1L1_{0:0.0f}_{1}.root".format(mass*1000,outfile),"recreate")
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

def NewEventsL1L2(events,mass,outfile):
	eleNTrackHits = array.array('d',[0])
	posNTrackHits = array.array('d',[0])
	eleTrkLambda = array.array('d',[0])
	posTrkLambda = array.array('d',[0])
	eleHasL1 = array.array('d',[0])
	posHasL1 = array.array('d',[0])

	file = TFile("dumL1L2_{0:0.0f}_{1}.root".format(mass*1000,outfile),"recreate")
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

def GetCategories(events,mass,outfile):

	L1L1cut = "eleHasL1&&posHasL1"
	L1L2cut = "((!eleHasL1&&posHasL1)||(eleHasL1&&!posHasL1))"
	L2L2cut = "!eleHasL1&&!posHasL1"
	file = TFile("dum_laycut_{0:0.0f}_{1}.root".format(mass*1000,outfile),"recreate")
	eventsL1L1 = events.CopyTree(L1L1cut)
	eventsL1L2 = events.CopyTree(L1L2cut)
	eventsL2L2 = events.CopyTree(L2L2cut)
	eventsL1L1.SetName("ntuple_L1L1")
	eventsL1L2.SetName("ntuple_L1L2")
	eventsL2L2.SetName("ntuple_L2L2")
	eventsL1L1.Write()
	eventsL1L2.Write()
	eventsL2L2.Write()

	newevents1, newevents2_L1L1, newevents3_L1L1 = NewEventsL1L1(eventsL1L1,mass,outfile)
	newevents2_L1L2, newevents3_L1L2 = NewEventsL1L2(eventsL1L2, mass,outfile)

	newevents1 = TChain("ntuple_L1L1")
	newevents1.Add("dumL1L1_{0:0.0f}_{1}.root".format(mass*1000,outfile))
	newevents1.Add("dumL1L2_{0:0.0f}_{1}.root".format(mass*1000,outfile))

	newevents2 = TChain("ntuple_L1L2")
	newevents2.Add("dumL1L1_{0:0.0f}_{1}.root".format(mass*1000,outfile))
	newevents2.Add("dumL1L2_{0:0.0f}_{1}.root".format(mass*1000,outfile))

	newevents3 = TChain("ntuple_L2L2")
	newevents3.Add("dumL1L1_{0:0.0f}_{1}.root".format(mass*1000,outfile))
	newevents3.Add("dumL1L2_{0:0.0f}_{1}.root".format(mass*1000,outfile))
	newevents3.Add("dum_laycut_{0:0.0f}_{1}.root".format(mass*1000,outfile))

	return newevents1, newevents2, newevents3

def SelectSingleV0s(filename,tuplename,mass):

	branchlist=["event","run","triEndZ","triStartP","uncVZ","bscChisq","uncM","uncP","eleTrkZ0","posTrkZ0","eleP","posP","elePY","posPY","uncVX","uncVY","uncPX","uncPY","uncPZ","eleMinPositiveIso","posMinPositiveIso","eleMinPositiveIsoL2","posMinPositiveIsoL2","eleTrkLambda","posTrkLambda","eleTrkOmega","posTrkOmega","eleTrkZ0Err","posTrkZ0Err","eleTrkLambdaErr","posTrkLambdaErr","eleTrkOmegaErr","posTrkOmegaErr","eleNHitsShared","posNHitsShared","eleHasL1","posHasL1"]
	events_SingleV0 = root_numpy.root2array(filename,branches=branchlist,treename=tuplename)
	n = events_SingleV0.size

	names = ["event","run","triEndZ","triStartP","uncVZ","bscChisq","uncM","uncP","eleTrkZ0","posTrkZ0","eleP","posP","elePY","posPY","uncVX","uncVY","uncPX","uncPY","uncPZ","eleMinPositiveIso","posMinPositiveIso","eleMinPositiveIsoL2","posMinPositiveIsoL2","eleTrkLambda","posTrkLambda","eleTrkOmega","posTrkOmega","eleTrkZ0Err","posTrkZ0Err","eleTrkLambdaErr","posTrkLambdaErr","eleTrkOmegaErr","posTrkOmegaErr","eleNHitsShared","posNHitsShared","eleHasL1","posHasL1"]
	cut = events_SingleV0["uncP"]>0.0
	stuff = [[events_SingleV0[i],(i,events_SingleV0.dtype[i])] for i in names]
	stuff.append([cut,("cut",numpy.int8)])
	stuff.append([numpy.zeros(n),("nPass",numpy.int8)])
	stuff.append([numpy.zeros(n),("rank",numpy.int8)])

	dataarray = [i[0] for i in stuff]
	typearray = [i[1] for i in stuff]
	output = numpy.core.records.fromarrays(dataarray,dtype=typearray)
	currentevent = -99999
	candidates = []

	duplicates = 0
	for i in xrange(0,n):
		if events_SingleV0[i]["event"]!=currentevent:
			candidates.sort(key=lambda x:events_SingleV0[x]["bscChisq"],reverse=False)
			rank=1
			for j in candidates:
				output[j]["nPass"]=len(candidates)
				output[j]["rank"]=rank
				rank+=1
				if(rank>2):
					duplicates = duplicates + 1
			del candidates[:]
			currentevent = events_SingleV0[i]["event"]
		if output[i]["cut"]!=0:
			candidates.append(i)

	output = output[output["nPass"]==1]

	print("Number of events with a duplicate V0 = {0}".format(duplicates))
	print("Total Number of V0s = {0}".format(n))
	print("Total Number of V0s Remaining = {0}".format(output.size))
	root_numpy.array2root(output,"dum_singleV0_{0}_{1:0.0f}.root".format(tuplename,mass*1000),mode="recreate",treename=tuplename)
	filefinal = TFile("dum_singleV0_{0}_{1:0.0f}.root".format(tuplename,mass*1000))

	#del events_SingleV0
	del stuff
	del dataarray
	del typearray
	del output

	return filefinal

def openPDF(outfile,canvas):
	canvas.Print(outfile+".pdf[")

def closePDF(outfile,canvas):
	canvas.Print(outfile+".pdf]")

gROOT.SetBatch(True)
c = TCanvas("c","c",1200,900)
maxZ = targZ + zRange #Define Maximum Z

#Set outfile and grab infile
outfile = remainder[0]
outfileroot = TFile(remainder[0]+"_all.root","RECREATE")
infile = open(remainder[1],"r")
truthfile = open(remainder[2],"r")
infiles = []
truthFiles = []

histosgamma = []

#Read files from L1L1 input text file
for line in (raw.strip().split() for raw in infile):
			infiles.append(line[0])

#Read files from input text truth file
for line in (raw.strip().split() for raw in truthfile):
			truthFiles.append(line[0])

if (len(truthFiles) != len(infiles)):
	print "The number of recon files and truth files do not match!"
	print_usage()
	sys.exit(0)

mass = array.array('d')
z = array.array('d')
nMass = len(truthFiles)

#Grab values of mass from the truth in the tuple files
for i in range(nMass):
	inputTruthFile = TFile(str(truthFiles[i]))
	inputTruthFile.Get(tupleName).Draw("triM>>histoMass({0},{1},{2})".format(1000,0,1))
	histoMass = ROOT.gROOT.FindObject("histoMass")
	mass.append(histoMass.GetMean())
	del histoMass

#Build array of z values
for i in range(nBins):
	z.append(targZ+i*(maxZ-targZ)/float(nBins))

#Function to fit for normalization
exppol4=TF1("exppol4","exp(pol4(0))",-5,100)
exppol4_m=TF1("exppol4_m","exp(pol4(0))",-5,100)
exppol4_p=TF1("exppol4_p","exp(pol4(0))",-5,100)

#uncTargProjX = -0.0917593000854
#uncTargProjXSig = 0.215671748567
#uncTargProjY = -0.0772518524373
#uncTargProjYSig = 0.0862582336468

angleMC = 0.111025680707
angleData = 0.0386557750132
angle = angleMC
xProj = "(uncVX-(uncVZ-{0})*uncPX/uncPZ)".format(targZ)
yProj = "(uncVY-(uncVZ-{0})*uncPY/uncPZ)".format(targZ)
xProj_rot = "({0}*cos({2})-{1}*sin({2}))".format(xProj,yProj,-angle)
yProj_rot = "({0}*sin({2})+{1}*cos({2}))".format(xProj,yProj,-angle)

uncTargProjX = -0.0995461972579
uncTargProjXSig = 0.217919555935
uncTargProjY = -0.0668941015569
uncTargProjYSig = 0.0831670646584
nSig = 2

eleiso = "eleMinPositiveIso+0.5*((eleTrkZ0+{0}*elePY/eleP)*sign(elePY)-3*(eleTrkZ0Err+abs({0}*eleTrkLambdaErr)+abs(2*{0}*eleTrkLambda*eleTrkOmegaErr/eleTrkOmega)))>0".format(targZ)
posiso = "posMinPositiveIso+0.5*((posTrkZ0+{0}*posPY/posP)*sign(posPY)-3*(posTrkZ0Err+abs({0}*posTrkLambdaErr)+abs(2*{0}*posTrkLambda*posTrkOmegaErr/posTrkOmega)))>0".format(targZ)

isocut = "({0}&&{1})".format(eleiso,posiso)

m0 = -0.201776054859
a0 = 0.0518988558564
a1 = -0.00230111045957
b0 = 0.0471576968062
b1 = -0.00108639651791
dz = 0.

eleZ0_up = "(eleTrkZ0>{0}+{1}*(uncVZ+{3})+{2}*1/uncM^1*(uncVZ+{3}))".format(m0,a0,a1,dz)
posZ0_up = "(posTrkZ0>{0}+{1}*(uncVZ+{3})+{2}*1/uncM^1*(uncVZ+{3}))".format(m0,a0,a1,dz)
eleZ0_down = "(-eleTrkZ0>{0}+{1}*(uncVZ+{3})+{2}*1/uncM^1*(uncVZ+{3}))".format(m0,b0,b1,dz)
posZ0_down = "(-posTrkZ0>{0}+{1}*(uncVZ+{3})+{2}*1/uncM^1*(uncVZ+{3}))".format(m0,b0,b1,dz)

#a0 = -0.177913468428
#a1 = -0.932330924205
#a2 = 0.00961915803124
#a3 = 0.228303547556
#b0 = 0.0115212779435
#b1 = -0.651929048499
#b2 = 0.0125216209858
#b3 = 0.217752673675
#dz = 0.

#eleZ0_up = "(eleTrkZ0>{0}+{1}*uncM+{2}*(uncVZ+{4})+{3}*uncM*(uncVZ+{4}))".format(a0,a1,a2,a3,dz)
#posZ0_up = "(posTrkZ0>{0}+{1}*uncM+{2}*(uncVZ+{4})+{3}*uncM*(uncVZ+{4}))".format(a0,a1,a2,a3,dz)

#eleZ0_down = "(-eleTrkZ0>{0}+{1}*uncM+{2}*(uncVZ+{4})+{3}*uncM*(uncVZ+{4}))".format(b0,b1,b2,b3,dz)
#posZ0_down = "(-posTrkZ0>{0}+{1}*uncM+{2}*(uncVZ+{4})+{3}*uncM*(uncVZ+{4}))".format(b0,b1,b2,b3,dz)

z0cut = "(({0}&&{1})||({2}&&{3}))".format(eleZ0_up,posZ0_down,posZ0_up,eleZ0_down)

cutsL1L1 = []
#cutsL1L1.append("eleHasL1&&posHasL1")
#cutsL1L1.append("sqrt((abs((uncVX-(uncVZ-{4})*uncPX/uncPZ)-{0})/(2*{1}))^2+(abs((uncVY-(uncVZ-{4})*uncPY/uncPZ)-{2})/(2*{3}))^2)<1".format(uncTargProjX,uncTargProjXSig,uncTargProjY,uncTargProjYSig,targZ))
cutsL1L1.append("sqrt((({4}-{0})/({6}*{1}))^2+(({5}-{2})/({6}*{3}))^2)<1".format(uncTargProjX,uncTargProjXSig,uncTargProjY,uncTargProjYSig,xProj_rot,yProj_rot,nSig))
cutsL1L1.append(isocut)
cutsL1L1.append(z0cut)
if(removeSharedHits):
	cutsL1L1.append("eleNHitsShared<0.5&&posNHitsShared<0.5")
if(zcut):
	if(unblind):
		#zcutL1L1 = "{0}+{1}*uncM+{2}*uncM^2+{3}*uncM^3+{4}*uncM^4+{5}*uncM^5".format(-8.555,1625,-38800,396200,-1892000,3458000) #10% Data L1L1
		#zcutL1L1 = "{0}+{1}*uncM+{2}*uncM^2+{3}*uncM^3+{4}*uncM^4+{5}*uncM^5".format(-3.413,1360,-3.276e4,3.292e5,-1.535e6,2.733e6) #10% Data L1L1
		zcutL1L1 = "{0}+{1}*uncM+{2}*uncM^2+{3}*uncM^3+{4}*uncM^4+{5}*uncM^5".format(19,53.04,-2566,-4258,2.345e5,-8.994e5) #10% Data L1L1
	else:
		#zcutL1L1 = "{0}+{1}*uncM+{2}*uncM^2+{3}*uncM^3+{4}*uncM^4+{5}*uncM^5".format(-4.912,1730,-42640,441300,-2117000,3865000) #100% scaled Data L1L1
		#zcutL1L1 = "{0}+{1}*uncM+{2}*uncM^2+{3}*uncM^3+{4}*uncM^4+{5}*uncM^5".format(1.809,1373,-3.444e4,3.503e5,-1.633e6,2.886e6) #100% scaled Data L1L1
		#zcutL1L1 = "{0}+{1}*uncM+{2}*uncM^2+{3}*uncM^3+{4}*uncM^4+{5}*uncM^5".format(26.85,-124.3,593.6,-3.954e4,4.451e5,-1.393e6) #100% scaled Data L1L1
		zcutL1L1 = "{0}+{1}*uncM+{2}*uncM^2+{3}*uncM^3+{4}*uncM^4+{5}*uncM^5".format(-0.4738,1551,-3.835e4,3.930e5,-1.865e6,3.373e6) #100% Data L1L1
	cutsL1L1.append("uncVZ>{0}".format(zcutL1L1))

cutL1L1 = cutsL1L1[0]
for i in range(1,len(cutsL1L1)):
	cutL1L1 = cutL1L1 + "&&" + cutsL1L1[i]

eleisoL1 = "eleMinPositiveIso+0.5*((eleTrkZ0+{0}*elePY/eleP)*sign(elePY)-3*(eleTrkZ0Err+abs({0}*eleTrkLambdaErr)+abs(2*{0}*eleTrkLambda*eleTrkOmegaErr/eleTrkOmega)))>0".format(targZ)
posisoL1 = "posMinPositiveIso+0.5*((posTrkZ0+{0}*posPY/posP)*sign(posPY)-3*(posTrkZ0Err+abs({0}*posTrkLambdaErr)+abs(2*{0}*posTrkLambda*posTrkOmegaErr/posTrkOmega)))>0".format(targZ)

eleisoL2 = "eleMinPositiveIsoL2+1/3.*((eleTrkZ0+{0}*elePY/eleP)*sign(elePY)-3*(eleTrkZ0Err+abs({0}*eleTrkLambdaErr)+abs(2*{0}*eleTrkLambda*eleTrkOmegaErr/eleTrkOmega)))>0".format(targZ)
posisoL2 = "posMinPositiveIsoL2+1/3.*((posTrkZ0+{0}*posPY/posP)*sign(posPY)-3*(posTrkZ0Err+abs({0}*posTrkLambdaErr)+abs(2*{0}*posTrkLambda*posTrkOmegaErr/posTrkOmega)))>0".format(targZ)

eleiso_L1L2 = "((eleHasL1&&{0})||(!eleHasL1&&{1}))".format(eleisoL1,eleisoL2)
posiso_L1L2 = "((posHasL1&&{0})||(!posHasL1&&{1}))".format(posisoL1,posisoL2)

isocut_L1L2 = "({0}&&{1})".format(eleiso_L1L2,posiso_L1L2)

uncTargProjXSigL1L2 = 1.25 * uncTargProjXSig
uncTargProjYSigL1L2 = 1.5 * uncTargProjYSig

m0 = -0.167438502208
a0 = 0.016762652862
a1 = 0.00033162637213
b0 = 0.0207347770085
b1 = 0.000331699098944

eleZ0_up_L1L2 = "(eleTrkZ0>{0}+{1}*(uncVZ+{3})+{2}*1/uncM^1*(uncVZ+{3}))".format(m0,a0,a1,dz)
posZ0_up_L1L2 = "(posTrkZ0>{0}+{1}*(uncVZ+{3})+{2}*1/uncM^1*(uncVZ+{3}))".format(m0,a0,a1,dz)
eleZ0_down_L1L2 = "(-eleTrkZ0>{0}+{1}*(uncVZ+{3})+{2}*1/uncM^1*(uncVZ+{3}))".format(m0,b0,b1,dz)
posZ0_down_L1L2 = "(-posTrkZ0>{0}+{1}*(uncVZ+{3})+{2}*1/uncM^1*(uncVZ+{3}))".format(m0,b0,b1,dz)

#a0 = -0.204298550172
#a1 = -0.819203072994
#a2 = 0.0215541584276
#a3 = 0.0769066743212
#b0 = -0.0131964462788
#b1 = -0.356152922206
#b2 = 0.0199952852357
#b3 = 0.0682704240163

#eleZ0_up_L1L2 = "(eleTrkZ0>{0}+{1}*uncM+{2}*(uncVZ+{4})+{3}*uncM*(uncVZ+{4}))".format(a0,a1,a2,a3,dz)
#posZ0_up_L1L2 = "(posTrkZ0>{0}+{1}*uncM+{2}*(uncVZ+{4})+{3}*uncM*(uncVZ+{4}))".format(a0,a1,a2,a3,dz)

#eleZ0_down_L1L2 = "(-eleTrkZ0>{0}+{1}*uncM+{2}*(uncVZ+{4})+{3}*uncM*(uncVZ+{4}))".format(b0,b1,b2,b3,dz)
#posZ0_down_L1L2 = "(-posTrkZ0>{0}+{1}*uncM+{2}*(uncVZ+{4})+{3}*uncM*(uncVZ+{4}))".format(b0,b1,b2,b3,dz)

z0cut_L1L2 = "(({0}&&{1})||({2}&&{3}))".format(eleZ0_up_L1L2,posZ0_down_L1L2,posZ0_up_L1L2,eleZ0_down_L1L2)

cutsL1L2 = []
#cutsL1L2.append("((!eleHasL1&&posHasL1)||(eleHasL1&&!posHasL1))")
#cutsL1L2.append("sqrt((abs((uncVX-(uncVZ-{4})*uncPX/uncPZ)-{0})/(2*{1}))^2+(abs((uncVY-(uncVZ-{4})*uncPY/uncPZ)-{2})/(2*{3}))^2)<1".format(uncTargProjX,uncTargProjXSigL1L2,uncTargProjY,uncTargProjYSigL1L2,targZ))
cutsL1L2.append("sqrt((({4}-{0})/({6}*{1}))^2+(({5}-{2})/({6}*{3}))^2)<1".format(uncTargProjX,uncTargProjXSig,uncTargProjY,uncTargProjYSig,xProj_rot,yProj_rot,nSig))
cutsL1L2.append(isocut_L1L2)
cutsL1L2.append(z0cut_L1L2)
if(removeSharedHits):
	cutsL1L2.append("eleNHitsShared<0.5&&posNHitsShared<0.5")
if(zcut):
	if(unblind):
		#zcutL1L2 = "{0}+{1}*uncM+{2}*uncM^2+{3}*uncM^3+{4}*uncM^4+{5}*uncM^5".format(-133,8211,-162000,1480000,-6406000,10560000) #10% Data L1L2
		#zcutL1L2 = "{0}+{1}*uncM+{2}*uncM^2+{3}*uncM^3+{4}*uncM^4+{5}*uncM^5".format(-162,9927,-2.028e5,1.952e6,-9.05e6,1.627e7) #10% Data L1L2
		zcutL1L2 = "{0}+{1}*uncM+{2}*uncM^2+{3}*uncM^3+{4}*uncM^4+{5}*uncM^5".format(-164.9+zshift,1.012e4,-2.087e5,2.039e6,-9.614e6,1.761e7) #10% Data L1L2
	else:
		#zcutL1L2 = "{0}+{1}*uncM+{2}*uncM^2+{3}*uncM^3+{4}*uncM^4+{5}*uncM^5".format(-170.1,10510,-209100,1934000,-8502000,14280000) #100% scaled Data L1L2
		#zcutL1L2 = "{0}+{1}*uncM+{2}*uncM^2+{3}*uncM^3+{4}*uncM^4+{5}*uncM^5".format(-199.6,1.224e4,-2.501e5,2.411e6,-1.117e7,2.001e7) #100% scaled Data L1L2
		zcutL1L2 = "{0}+{1}*uncM+{2}*uncM^2+{3}*uncM^3+{4}*uncM^4+{5}*uncM^5".format(-205.8,1.259e4,-2.597e5,2.541e6,-1.198e7,2.192e7) #100% scaled Data L1L2
	cutsL1L2.append("uncVZ>{0}".format(zcutL1L2))

cutL1L2 = cutsL1L2[0]
for i in range(1,len(cutsL1L2)):
	cutL1L2 = cutL1L2 + "&&" + cutsL1L2[i]

cutsL2L2 = []
#cutsL2L2.append("(!eleHasL1&&!posHasL1)")
#cutsL2L2.append("sqrt((abs((uncVX-(uncVZ-{4})*uncPX/uncPZ)-{0})/(2*{1}))^2+(abs((uncVY-(uncVZ-{4})*uncPY/uncPZ)-{2})/(2*{3}))^2)<1".format(uncTargProjX,uncTargProjXSigL1L2,uncTargProjY,uncTargProjYSigL1L2,targZ))
cutsL2L2.append("sqrt((({4}-{0})/({6}*{1}))^2+(({5}-{2})/({6}*{3}))^2)<1".format(uncTargProjX,uncTargProjXSig,uncTargProjY,uncTargProjYSig,xProj_rot,yProj_rot,nSig))
cutsL2L2.append("({0}&&{1})".format(eleisoL2,posisoL2))
cutsL2L2.append(z0cut_L1L2)
if(removeSharedHits):
	cutsL2L2.append("eleNHitsShared<0.5&&posNHitsShared<0.5")
if(zcut):
	if(unblind):
		zcutL2L2 = "{0}+{1}*uncM+{2}*uncM^2+{3}*uncM^3+{4}*uncM^4+{5}*uncM^5".format(-168.1,1.14e4,-2.278e5,2.051e6,-8.728e6,1.438e7) #10% Data L2L2
	else:
		zcutL2L2 = "{0}+{1}*uncM+{2}*uncM^2+{3}*uncM^3+{4}*uncM^4+{5}*uncM^5".format(-238.7,1.572e4,-3.165e5,2.912e6,-1.28e7,2.198e7) #10% Data L2L2 Scaled
	cutsL2L2.append("uncVZ>{0}".format(zcutL2L2))

cutL2L2 = cutsL2L2[0]
for i in range(1,len(cutsL2L2)):
	cutL2L2 = cutL2L2 + "&&" + cutsL2L2[i]

#Create text files to write to
textfileL1L1 = open(outfile + "_L1L1.eff","w")
textfileL1L1Norm = open(outfile + "_L1L1_norm.eff","w")

textfileL1L2 = open(outfile + "_L1L2.eff","w")
textfileL1L2Norm = open(outfile + "_L1L2_norm.eff","w")

textfileL2L2 = open(outfile + "_L2L2.eff","w")
textfileL2L2Norm = open(outfile + "_L2L2_norm.eff","w")

textfilenorm = open(outfile + ".norm","w")
#Write values of mass in the first row
for i in range(nMass):
	textfileL1L1.write(str(mass[i]) + " ")
	textfileL1L1Norm.write(str(mass[i]) + " ")
	textfileL1L2.write(str(mass[i]) + " ")
	textfileL1L2Norm.write(str(mass[i]) + " ")
	textfileL2L2.write(str(mass[i]) + " ")
	textfileL2L2Norm.write(str(mass[i]) + " ")
textfileL1L1.write("\n")
textfileL1L1Norm.write("\n")
textfileL1L2.write("\n")
textfileL1L2Norm.write("\n")
textfileL2L2.write("\n")
textfileL2L2Norm.write("\n")

#Write values of z in the 2nd row
for i in range(nBins):
	textfileL1L1.write(str(z[i]) + " ")
	textfileL1L1Norm.write(str(z[i]) + " ")
	textfileL1L2.write(str(z[i]) + " ")
	textfileL1L2Norm.write(str(z[i]) + " ")
	textfileL2L2.write(str(z[i]) + " ")
	textfileL2L2Norm.write(str(z[i]) + " ")
textfileL1L1.write("\n")
textfileL1L1Norm.write("\n")
textfileL1L2.write("\n")
textfileL1L2Norm.write("\n")
textfileL2L2.write("\n")
textfileL2L2Norm.write("\n")

histosL1L1 = []
histosL1L2 = []
histosL2L2 = []
histosTruth = []
histoscutL1L1 = []
histoscutL1L2 = []
histoscutL2L2 = []
normArr = array.array('d')
normArr_n = array.array('d')
normArr_p = array.array('d')

gammamean = array.array('d')
gammameanerror = array.array('d')
zeros = array.array('d')

openPDF(outfile+"_fitplots",c)
#Loop over all values of mass
for i in range(nMass):
	inputReconFile = TFile(str(infiles[i]))
	L1L1events, L1L2events, L2L2events = GetCategories(inputReconFile.Get(tupleName),mass[i],outfile)
	eventstruth = inputTruthFile.Get(tupleName)

	print("Mass {0:0.0f}".format(mass[i]*1000))
	L1L1events.Draw("triEndZ>>histoReconL1L1_{3:0.0f}({0},{1},{2})".format(nBins,targZ,maxZ,mass[i]*1000))
	histosL1L1.append(ROOT.gROOT.FindObject("histoReconL1L1_{0:0.0f}".format(mass[i]*1000)))
	L1L2events.Draw("triEndZ>>histoReconL1L2_{3:0.0f}({0},{1},{2})".format(nBins,targZ,maxZ,mass[i]*1000))
	histosL1L2.append(ROOT.gROOT.FindObject("histoReconL1L2_{0:0.0f}".format(mass[i]*1000)))
	L2L2events.Draw("triEndZ>>histoReconL2L2_{3:0.0f}({0},{1},{2})".format(nBins,targZ,maxZ,mass[i]*1000))
	histosL2L2.append(ROOT.gROOT.FindObject("histoReconL2L2_{0:0.0f}".format(mass[i]*1000)))
	#eventstruth.Draw("triEndZ>>histoTruth_{3:0.0f}({0},{1},{2})".format(nBins,targZ,maxZ,mass[i]*1000),"triStartP>0.8*{0}".format(eBeam))
	eventstruth.Draw("triEndZ>>histoTruth_{3:0.0f}({0},{1},{2})".format(nBins,targZ,maxZ,mass[i]*1000))
	histosTruth.append(ROOT.gROOT.FindObject("histoTruth_{0:0.0f}".format(mass[i]*1000)))

	file1 = TFile("dum_laycut_L1L1_{0:0.0f}_{1}.root".format(mass[i]*1000,outfile),"recreate")
	eventsL1L1_singleV0 = L1L1events.CopyTree(cutL1L1)
	eventsL1L1_singleV0.SetName("ntuple_L1L1")
	eventsL1L1_singleV0.Write()
	fileL1L1 = SelectSingleV0s("dum_laycut_L1L1_{0:0.0f}_{1}.root".format(mass[i]*1000,outfile),"ntuple_L1L1",mass[i])
	L1L1events_singleV0 = fileL1L1.Get("ntuple_L1L1")

	file2 = TFile("dum_laycut_L1L2_{0:0.0f}_{1}.root".format(mass[i]*1000,outfile),"recreate")
	eventsL1L2_singleV0 = L1L2events.CopyTree(cutL1L2)
	eventsL1L2_singleV0.SetName("ntuple_L1L2")
	eventsL1L2_singleV0.Write()
	fileL1L2 = SelectSingleV0s("dum_laycut_L1L2_{0:0.0f}_{1}.root".format(mass[i]*1000,outfile),"ntuple_L1L2",mass[i])
	L1L2events_singleV0 = fileL1L2.Get("ntuple_L1L2")

	file3 = TFile("dum_laycut_L2L2_{0:0.0f}_{1}.root".format(mass[i]*1000,outfile),"recreate")
	eventsL2L2_singleV0 = L2L2events.CopyTree(cutL2L2)
	eventsL2L2_singleV0.SetName("ntuple_L2L2")
	eventsL2L2_singleV0.Write()
	fileL2L2 = SelectSingleV0s("dum_laycut_L2L2_{0:0.0f}_{1}.root".format(mass[i]*1000,outfile),"ntuple_L2L2",mass[i])
	L2L2events_singleV0 = fileL2L2.Get("ntuple_L2L2")

	outfileroot.cd()

	L1L1events_singleV0.Draw("triEndZ>>histoReconL1L1_cut_{3:0.0f}({0},{1},{2})".format(nBins,targZ,maxZ,mass[i]*1000))
	histoscutL1L1.append(ROOT.gROOT.FindObject("histoReconL1L1_cut_{0:0.0f}".format(mass[i]*1000)))
	L1L2events_singleV0.Draw("triEndZ>>histoReconL1L2_cut_{3:0.0f}({0},{1},{2})".format(nBins,targZ,maxZ,mass[i]*1000))
	histoscutL1L2.append(ROOT.gROOT.FindObject("histoReconL1L2_cut_{0:0.0f}".format(mass[i]*1000)))
	L2L2events_singleV0.Draw("triEndZ>>histoReconL2L2_cut_{3:0.0f}({0},{1},{2})".format(nBins,targZ,maxZ,mass[i]*1000))
	histoscutL2L2.append(ROOT.gROOT.FindObject("histoReconL2L2_cut_{0:0.0f}".format(mass[i]*1000)))

	histosL1L1[i].Sumw2()
	histosL1L2[i].Sumw2()
	histosL2L2[i].Sumw2()
	histoscutL1L1[i].Sumw2()
	histoscutL1L2[i].Sumw2()
	histoscutL2L2[i].Sumw2()
	histosTruth[i].Sumw2()
	outfileroot.cd()
	histosL1L1[i].Write("L1L1 {0:0.0f} MeV".format(mass[i]*1000))
	histosL1L2[i].Write("L1L2 {0:0.0f} MeV".format(mass[i]*1000))
	histosL2L2[i].Write("L2L2 {0:0.0f} MeV".format(mass[i]*1000))
	histoscutL1L1[i].Write("L1L1 Cut {0:0.0f} MeV".format(mass[i]*1000))
	histoscutL1L2[i].Write("L1L2 Cut {0:0.0f} MeV".format(mass[i]*1000))
	histoscutL2L2[i].Write("L2L2 Cut {0:0.0f} MeV".format(mass[i]*1000))
	histosTruth[i].Write("Truth {0:0.0f} MeV".format(mass[i]*1000))

	#Find the normalization based on a certain number of bins
	norm, norm_sig, norm_psig = plotFit(histosL1L1[i],histosL1L2[i],histosL2L2[i],histosTruth[i],normArr,outfile+"_fitplots",outfileroot,c,mass[i],targZ,title="")
	print norm
	textfilenorm.write("norm.append({0})".format(norm))
	normArr.append(norm)
	normArr_n.append(norm_sig)
	normArr_p.append(norm_psig)
	#Write the efficiency for a given mass (row) as function of z
	for j in range(nBins):
		if (histosTruth[i].GetBinContent(j+1) == 0):
			textfileL1L1.write("0.0 ")
			textfileL1L1Norm.write("0.0 ")
			textfileL1L2.write("0.0 ")
			textfileL1L2Norm.write("0.0 ")
			textfileL2L2.write("0.0 ")
			textfileL2L2Norm.write("0.0 ")
		else:
			textfileL1L1.write(str(histoscutL1L1[i].GetBinContent(j+1)/histosTruth[i].GetBinContent(j+1)) + " ")
			textfileL1L2.write(str(histoscutL1L2[i].GetBinContent(j+1)/histosTruth[i].GetBinContent(j+1)) + " ")
			textfileL2L2.write(str(histoscutL2L2[i].GetBinContent(j+1)/histosTruth[i].GetBinContent(j+1)) + " ")
			if(norm != 0):
				textfileL1L1Norm.write(str(histoscutL1L1[i].GetBinContent(j+1)/(histosTruth[i].GetBinContent(j+1)*norm)) + " ")
				textfileL1L2Norm.write(str(histoscutL1L2[i].GetBinContent(j+1)/(histosTruth[i].GetBinContent(j+1)*norm)) + " ")
				textfileL2L2Norm.write(str(histoscutL2L2[i].GetBinContent(j+1)/(histosTruth[i].GetBinContent(j+1)*norm)) + " ")
			else:
				textfileL1L1Norm.write("0.0 ")
				textfileL1L2Norm.write("0.0 ")
				textfileL2L2Norm.write("0.0 ")
	textfileL1L1.write("\n")
	textfileL1L1Norm.write("\n")
	textfileL1L2.write("\n")
	textfileL1L2Norm.write("\n")
	textfileL2L2.write("\n")
	textfileL2L2Norm.write("\n")
	textfilenorm.write("\n")
	L1L1events_singleV0.Draw("triStartP/({4})>>gammahisto_{3:0.0f}({0},{1},{2})".format(nBins,0.8,1.,mass[i]*1000,eBeam))
	histosgamma.append(ROOT.gROOT.FindObject("gammahisto_{0:0.0f}".format(mass[i]*1000)))
	gammamean.append(histosgamma[i].GetMean())
	print(histosgamma[i].GetMean())
	gammameanerror.append(histosgamma[i].GetMeanError())
	zeros.append(0.)

textfileL1L1.close()
textfileL1L1Norm.close()
textfileL1L2.close()
textfileL1L2Norm.close()
textfileL2L2.close()
textfileL2L2Norm.close()
textfilenorm.close()

closePDF(outfile+"_fitplots",c)

#Make test plots if desired
if(makeTestPlots):
	#Make Absolute Efficiency Plots
	c1 = TCanvas("c1","c1",1200,900)
	c1.Print(outfile+"_L1L1.pdf[")

	for i in range(1,nMass-1):
		plotTest(i,outfile+"_L1L1.eff",outfile+"_L1L1",targZ,maxZ,c1)

	c1.Print(outfile+"_L1L1.pdf]")

	del c1

	#Make Normalized Efficiency Plots
	c2 = TCanvas("c2","c2",1200,900)
	c2.Print(outfile+"_L1L1_norm.pdf[")

	for i in range(1,nMass-1):
		plotTest(i,outfile+"_L1L1_norm.eff",outfile+"_L1L1_norm",targZ,maxZ,c2)

	c2.Print(outfile+"_L1L1_norm.pdf]")

	del c2

	#Make Absolute Efficiency Plots
	c3 = TCanvas("c3","c3",1200,900)
	c3.Print(outfile+"_L1L2.pdf[")

	for i in range(1,nMass-1):
		plotTest(i,outfile+"_L1L2.eff",outfile+"_L1L2",targZ,maxZ,c3)

	c3.Print(outfile+"_L1L2.pdf]")

	del c3

	#Make Normalized Efficiency Plots
	c4 = TCanvas("c4","c4",1200,900)
	c4.Print(outfile+"_L1L2_norm.pdf[")

	for i in range(1,nMass-1):
		plotTest(i,outfile+"_L1L2_norm.eff",outfile+"_L1L2_norm",targZ,maxZ,c4)

	c4.Print(outfile+"_L1L2_norm.pdf]")

	del c4

	#Make Absolute Efficiency Plots
	c5 = TCanvas("c5","c5",1200,900)
	c5.Print(outfile+"_L2L2.pdf[")

	for i in range(1,nMass-1):
		plotTest(i,outfile+"_L2L2.eff",outfile+"_L2L2",targZ,maxZ,c5)

	c5.Print(outfile+"_L2L2.pdf]")

	del c5

	#Make Normalized Efficiency Plots
	c6 = TCanvas("c6","c6",1200,900)
	c6.Print(outfile+"_L2L2_norm.pdf[")

	for i in range(1,nMass-1):
		plotTest(i,outfile+"_L2L2_norm.eff",outfile+"_L2L2_norm",targZ,maxZ,c6)

	c6.Print(outfile+"_L2L2_norm.pdf]")

	del c6

c7 = TCanvas("c7","c7",1200,900)

c7.Print(outfile+"_plots.pdf[")

plotEff(histoscutL1L1,histosTruth,normArr,outfile+"_L1L1",outfile+"_plots",outfileroot,c7,mass,False,title="L1L1")
plotEff(histoscutL1L1,histosTruth,normArr,outfile+"_L1L1_norm",outfile+"_plots",outfileroot,c7,mass,True,title="L1L1 Normalized")
plotEff(histoscutL1L2,histosTruth,normArr,outfile+"_L1L2",outfile+"_plots",outfileroot,c7,mass,False,title="L1L2")
plotEff(histoscutL1L2,histosTruth,normArr,outfile+"_L1L2_norm",outfile+"_plots",outfileroot,c7,mass,True,title="L2L2 Normalized")
plotEff(histoscutL2L2,histosTruth,normArr,outfile+"_L2L2",outfile+"_plots",outfileroot,c7,mass,False,title="L2L2")
plotEff(histoscutL2L2,histosTruth,normArr,outfile+"_L2L2_norm",outfile+"_plots",outfileroot,c7,mass,True,title="L2L2 Normalized")

plotAll(histoscutL1L1,histoscutL1L2,histoscutL2L2,histosTruth,normArr,outfile+"_all",outfile+"_plots",outfileroot,c7,mass)

passed.Sumw2()
total.Sumw2()
passed.Divide(total)
passed.SetTitle("L1 Hit Efficiency")
passed.GetXaxis().SetTitle("Track Slope")
passed.GetYaxis().SetTitle("Efficiency")
passed.SetStats(0)
passed.Draw()
c7.Print(outfile+"_plots.pdf")
passed.Write("Efficiency")

graph = TGraphErrors(len(mass),mass,gammamean,zeros,gammameanerror)
graph.SetTitle("A' Truth Energy / E_{beam}")
graph.GetXaxis().SetTitle("Truth Mass (GeV)")
graph.GetYaxis().SetTitle("Fraction of E_{beam}")
graph.GetXaxis().SetRangeUser(0,.2)
graph.GetYaxis().SetRangeUser(0.9,1.0)
graph.Draw("AP")
c7.Print(outfile+"_plots.pdf")
graph.Write("Gamma")

def MakeGammaHistos(histo,mass,canvas,output):
	histo.SetTitle("{0:0.0f}".format(mass) + " MeV A' Truth Energy / E_{beam}")
	histo.GetXaxis().SetTitle("Truth Energy /E_{beam}")
	histo.GetYaxis().SetTitle("")
	histo.Sumw2()
	histo.SetStats(0)
	histo.Draw()
	canvas.Print(output+".pdf")
	histo.Write("{0} MeV A' Energy".format(mass))

for i in range(len(mass)):
	MakeGammaHistos(histosgamma[i],mass[i]*1000,c7,outfile+"_plots")

graph = TGraph(len(mass),mass,normArr)
graph.SetTitle("Prompt A' Acceptance * Efficiency")
graph.GetXaxis().SetTitle("Truth Mass (GeV)")
graph.GetYaxis().SetTitle("Efficiency")
graph.GetXaxis().SetRangeUser(0,.4)
graph.GetYaxis().SetRangeUser(0,0.2)
graph.SetLineColor(1)
graph.SetMarkerColor(1)
graph.Draw("AP*")
c7.Print(outfile+"_plots.pdf")
graph.Write("Prompt Acceptance")

graph_m = TGraph(len(mass),mass,normArr_n)
graph_p = TGraph(len(mass),mass,normArr_p)

graph.SetTitle("Normalization Factor Systematic")
graph.GetYaxis().SetTitle("Norm Factor")
graph.SetLineColor(1)
graph.SetMarkerColor(1)
graph_m.SetLineColor(2)
graph_m.SetMarkerColor(2)
graph_p.SetLineColor(4)
graph_p.SetMarkerColor(4)

graph.Draw("AP*")
graph_m.Draw("P*same")
graph_p.Draw("P*same")

legend = TLegend(.68,.66,.92,.87)
legend.SetBorderSize(0)
legend.SetFillColor(0)
legend.SetFillStyle(0)
legend.SetTextFont(42)
legend.SetTextSize(0.035)
legend.AddEntry(graph,"Nominal","LP")
legend.AddEntry(graph_m,"-1#sigma","LP")
legend.AddEntry(graph_p,"+1#sigma","LP")
legend.Draw()

c7.Print(outfile+"_plots.pdf")
graph.Write("Prompt Acceptance Systematic")

c7.Print(outfile+"_plots.pdf]")
outfileroot.Close()
