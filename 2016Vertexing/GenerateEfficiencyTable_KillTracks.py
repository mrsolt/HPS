#!/usr/bin/env python
#Author Matt Solt mrsolt@slac.stanford.edu
import sys
import array, math
import numpy as np
import random
import ROOT
from ROOT import gROOT, gStyle, TFile, TTree, TChain, TMVA, TCut, TCanvas, gDirectory, TH1, TGraph, gPad, TF1, TH1F, TLegend, TLatex, TGraphErrors
import getopt

def print_usage():
    print "\nUsage: {0} <output file basename> <L1L1 input files list> <L1L2 input files list> <L2L2 input files list> <input recon truth tuple files list>".format(sys.argv[0])
    print "Arguments: "
    print '\t-e: use this beam energy <default 2.3 GeV>'
    print '\t-t: use this target position <default -4.3 mm>'
    print '\t-n: number of bins in histograms <default 50>'
    print '\t-z: total range in z covered <default 100 mm>'
    print '\t-T: plot Test plots'
    print '\t-N: number of bins from target to normalize to <default is 4>'
    print '\t-s: tuple name <default is "ntuple">'
    print '\t-h: this help message'
    print

#Default Values
eBeam = 2.3
makeTestPlots = False
killInTrackSlope = True
targZ = -4.3
nBins = 50
zRange = 100
nNorm = 4
tupleName = "ntuple"
fittype = 5

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

def plotEff(inputFile,output,nBins,targZ,maxZ,canvas):
    inputfile = open(inputFile,"r")
    mass = getMassArray(inputFile)
    z = getZArray(inputFile)
    eff = getEfficiency(inputFile)
    histos = []
    for i in range(len(mass)):
        histos.append(TH1F("histo{0}".format(mass[i]),"histo{0}".format(mass[i]),nBins,targZ,maxZ))
    legend = TLegend(.68,.50,.92,.97)
    legend.SetBorderSize(0)
    legend.SetFillColor(0)
    legend.SetFillStyle(0)
    legend.SetTextFont(42)
    legend.SetTextSize(0.035)
    maximum = 0
    for i in range(len(mass)):
        for j in range(len(z)):
            histos[i].SetBinContent(j+1,eff[i][j])
            if(eff[i][0] > maximum):
                maximum = eff[i][0]
        #legend.AddEntry(histos[i],str().format('{0:.3f}',mass[i]*1000)+" MeV","LP")
        legend.AddEntry(histos[i],str("%.3g" % (mass[i] * 1000))+" MeV","LP")
        if(i == 0):
            histos[i].Draw()
            histos[i].SetStats(0)
            histos[i].GetXaxis().SetTitle("z [mm]")
            histos[i].GetYaxis().SetTitle("efficiency")
            histos[i].SetTitle("A' Acceptance * Efficiency")
        else:
            histos[i].Draw("same")
        histos[i].SetLineColor(i+1)
    histos[0].GetYaxis().SetRangeUser(0,0.13)
    legend.Draw()
    canvas.Print(output+".png")

def plotEff2(histos,histosTruth,normArr,output,outPDF,outfileroot,canvas,mass,useNorm,title=""):
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
        #histos[i].Sumw2()
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
        legend.SetTextSize(0.035)
        legend.AddEntry(histos_copy_L1L1[i],"L1L1","LP")
        legend.AddEntry(histos_copy_L1L2[i],"L1L2","LP")
        legend.AddEntry(histos_copy_L2L2[i],"L2L2","LP")
        legend.AddEntry(sumhisto,"Sum","LP")
        histos_copy_L1L1[i].Draw()
        histos_copy_L1L1[i].SetStats(0)
        histos_copy_L1L1[i].GetXaxis().SetTitle("z [mm]")
        histos_copy_L1L1[i].GetYaxis().SetTitle("efficiency")
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
    sumhisto.Fit("exppol4","QR")
    maximum = sumhisto.GetMaximum()
    legend = TLegend(.68,.70,.92,.90)
    legend.SetBorderSize(0)
    legend.SetFillColor(0)
    legend.SetFillStyle(0)
    legend.SetTextFont(42)
    legend.SetTextSize(0.035)
    legend.AddEntry(histo_copy_L1L1,"L1L1","LP")
    legend.AddEntry(histo_copy_L1L2,"L1L2","LP")
    legend.AddEntry(histo_copy_L2L2,"L2L2","LP")
    legend.AddEntry(sumhisto,"Sum","LP")
    histo_copy_L1L1.SetStats(0)
    histo_copy_L1L1.Draw()
    histo_copy_L1L1.GetXaxis().SetTitle("z [mm]")
    histo_copy_L1L1.GetYaxis().SetTitle("efficiency")
    histo_copy_L1L1.SetTitle("A' Acceptance * Efficiency {0:0.0f} MeV A' {1}".format(mass*1000,title))
    histo_copy_L1L1.GetYaxis().SetRangeUser(0,1.3*maximum)
    histo_copy_L1L2.Draw("same")
    histo_copy_L2L2.Draw("same")
    sumhisto.Draw("same")
    legend.Draw()
    canvas.Print(outPDF+".pdf")
    canvas.Write()

    del sumhisto
    del legend
    del histo_copy_L1L1
    del histo_copy_L1L2
    del histo_copy_L2L2
    return exppol4.Eval(targZ)

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

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'e:t:n:z:TN:s:f:h')

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
    if opt=='-N':
        nNorm = int(arg)
    if opt=='-s':
        tupleName = str(arg)
    if opt=='-f':
        fittype = int(arg)
    if opt=='-h':
        print_usage()
        sys.exit(0)

if len(remainder)!=5:
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


def KillHits(events1, events2, events3, mass, inputL2L2ReconFile,outfile):
    newevents1, newevents2_L1L1, newevents3_L1L1 = NewEventsL1L1(events1,mass,outfile)
    newevents2_L1L2, newevents3_L1L2 = NewEventsL1L2(events2, mass,outfile)

    newevents1 = TChain("ntuple_L1L1")
    newevents1.Add("dumL1L1_{0:0.0f}_{1}.root".format(mass*1000,outfile))
    newevents1.Add("dumL1L2_{0:0.0f}_{1}.root".format(mass*1000,outfile))

    newevents2 = TChain("ntuple_L1L2")
    newevents2.Add("dumL1L1_{0:0.0f}_{1}.root".format(mass*1000,outfile))
    newevents2.Add("dumL1L2_{0:0.0f}_{1}.root".format(mass*1000,outfile))

    file = TFile("dumL2L2_{0:0.0f}_{1}.root".format(mass*1000,outfile),"recreate")
    eventsL2L2 = events3.CloneTree(0)
    eventsL2L2.SetName("ntuple_L2L2")
    nevents = events3.GetEntries()

    for entry in xrange(nevents):
        events3.GetEntry(entry)
        eventsL2L2.Fill()
    eventsL2L2.AutoSave()

    newevents3 = TChain("ntuple_L2L2")
    newevents3.Add("dumL1L1_{0:0.0f}_{1}.root".format(mass*1000,outfile))
    newevents3.Add("dumL1L2_{0:0.0f}_{1}.root".format(mass*1000,outfile))
    newevents3.Add("dumL2L2_{0:0.0f}_{1}.root".format(mass*1000,outfile))

    del file

    return newevents1, newevents2, newevents3

def openPDF(outfile,canvas):
    canvas.Print(outfile+".pdf[")

def closePDF(outfile,canvas):
    canvas.Print(outfile+".pdf]")

def CompareHisto(events1,events2,truthevents,nBins,targZ,maxZ,outfileroot,canvas,outfile,mass,title=""):
    outfileroot.cd()
    canvas.Clear()
    events1.Draw("triEndZ>>histo1({0},{1},{2})".format(nBins,targZ,maxZ))
    histo1 = ROOT.gROOT.FindObject("histo1")
    events2.Draw("triEndZ>>histo2({0},{1},{2})".format(nBins,targZ,maxZ))
    histo2 = ROOT.gROOT.FindObject("histo2")
    truthevents.Draw("triEndZ>>truthhisto({0},{1},{2})".format(nBins,targZ,maxZ))
    truthhisto = ROOT.gROOT.FindObject("truthhisto")

    histo1.Sumw2()
    histo2.Sumw2()
    truthhisto.Sumw2()

    histo1.Divide(truthhisto)
    histo2.Divide(truthhisto)

    histo1.Draw()
    histo1.SetStats(0)
    histo1.SetTitle("Compare Hit Killing {0:0.0f} MeV A' for {1}".format(mass*1000,title))
    histo1.GetXaxis().SetTitle("Truth z (mm)")
    histo1.GetYaxis().SetTitle("efficiency")
    histo2.SetLineColor(2)
    histo2.Draw("same")

    legend = TLegend(.58,.66,.92,.87)
    legend.SetBorderSize(0)
    legend.SetFillColor(0)
    legend.SetFillStyle(0)
    legend.SetTextFont(42)
    legend.SetTextSize(0.035)
    legend.AddEntry(histo1,"No L1 Hit Killing","LP")
    legend.AddEntry(histo2,"With L1 Hit Killing","LP")
    legend.Draw("same")

    canvas.Print(outfile+".pdf")
    canvas.Write()

def CompareKill(L1L1events,L1L1killevents,L1L2events,L1L2killevents,L2L2events,L2L2killevents,truthevents,nBins,targZ,outfileroot,canvas,outfile,mass):
    output = outfile+"_comparekill"
    CompareHisto(L1L1events,L1L1killevents,truthevents,nBins,targZ,80,outfileroot,canvas,output,mass,"L1L1")
    CompareHisto(L1L2events,L1L2killevents,truthevents,nBins,targZ,90,outfileroot,canvas,output,mass,"L1L2")
    CompareHisto(L2L2events,L2L2killevents,truthevents,nBins,targZ,160,outfileroot,canvas,output,mass,"L2L2")



#removedL1Hit={}   #dictionary...for c++/java you can use a map or something...
#for fsp in <fspInV0> : 
#    if isMC and trackKiller and killInTrackSlope :
#        track=fsp.getTracks()[0]
#        nHits=len(track.getSvtHits())
#        slp=track.getTanLambda()
#        rndm=random.random()           
#        ibin=effSlopeData.FindBin(slp)
#        eff=1-effSlopeData.GetBinContent(ibin) #the slope "efficiency" is actually an inefficiency                       
#        if rndm>eff:
#            if nHits==5:
#                print(str(fsp)+'::  Removing this particle due to L1 inefficiency')
#                nKilled+=1
#                continue
#            else :                           
#                print(str(fsp)+'::  Removing this particle L1 hit due to inefficiency')
#                removedL1Hit[fsp]=True
#        else:
#            print(str(fsp)+'::  Leaving this particle alone')
#            removedL1Hit[fsp]=False  

gROOT.SetBatch(True)
c = TCanvas("c","c",1200,900)
maxZ = targZ + zRange #Define Maximum Z

#Set outfile and grab infile
outfile = remainder[0]
outfileroot = TFile(remainder[0]+"_all.root","RECREATE")
L1L1file = open(remainder[1],"r")
L1L2file = open(remainder[2],"r")
L2L2file = open(remainder[3],"r")
truthfile = open(remainder[4],"r")

L1L1Files = []
L1L2Files = []
L2L2Files = []
truthFiles = []

histosgamma = []

#Read files from L1L1 input text file
for line in (raw.strip().split() for raw in L1L1file):
            L1L1Files.append(line[0])

#Read files from L1L2 input text file
for line in (raw.strip().split() for raw in L1L2file):
            L1L2Files.append(line[0])

#Read files from L1L1 input text file
for line in (raw.strip().split() for raw in L2L2file):
            L2L2Files.append(line[0])

#Read files from input text truth file
for line in (raw.strip().split() for raw in truthfile):
            truthFiles.append(line[0])

if (len(truthFiles) != len(L1L1Files) or len(truthFiles) != len(L1L2Files) or len(truthFiles) != len(L2L2Files)):
    print "The number of L1L1 files, input files, or truth files do not match!"
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
if(fittype == 0):
    exppol4=TF1("exppol4","exp(pol2(0))",-5,50)
elif(fittype == 1):
    exppol4=TF1("exppol4","exp(pol2(0))",-5,100)
elif(fittype == 2):
    exppol4=TF1("exppol4","exp(pol3(0))",-5,50)
elif(fittype == 3):
    exppol4=TF1("exppol4","exp(pol3(0))",-5,100)
elif(fittype == 4):
    exppol4=TF1("exppol4","exp(pol4(0))",-5,50)
elif(fittype == 5):
    exppol4=TF1("exppol4","exp(pol4(0))",-5,100)
elif(fittype == 6):
    exppol4=TF1("exppol4","pol3",-5,50)
elif(fittype == 7):
    exppol4=TF1("exppol4","pol3",-5,100)
elif(fittype == 8):
    exppol4=TF1("exppol4","pol4",-5,50)
elif(fittype == 9):
    exppol4=TF1("exppol4","pol4",-5,100)
elif(fittype == 10):
    exppol4=TF1("exppol4","pol5",-5,50)
elif(fittype == 11):
    exppol4=TF1("exppol4","pol5",-5,100)
elif(fittype == 12):
    exppol4=TF1("exppol4","pol6",-5,50)
else:
    exppol4=TF1("exppol4","pol6",-5,100)

#Create text files to write to
textfileL1L1 = open(outfile + "_L1L1.eff","w")
textfileL1L1Norm = open(outfile + "_L1L1_norm.eff","w")
textfileL1L1Killed = open(outfile + "_L1L1_kill.eff","w")
textfileL1L1KilledNorm = open(outfile + "_L1L1_kill_norm.eff","w")

textfileL1L2 = open(outfile + "_L1L2.eff","w")
textfileL1L2Norm = open(outfile + "_L1L2_norm.eff","w")
textfileL1L2Killed = open(outfile + "_L1L2_kill.eff","w")
textfileL1L2KilledNorm = open(outfile + "_L1L2_kill_norm.eff","w")

textfileL2L2 = open(outfile + "_L2L2.eff","w")
textfileL2L2Norm = open(outfile + "_L2L2_norm.eff","w")
textfileL2L2Killed = open(outfile + "_L2L2_kill.eff","w")
textfileL2L2KilledNorm = open(outfile + "_L2L2_kill_norm.eff","w")

#Write values of mass in the first row
for i in range(nMass):
    textfileL1L1.write(str(mass[i]) + " ")
    textfileL1L1Norm.write(str(mass[i]) + " ")
    textfileL1L1Killed.write(str(mass[i]) + " ")
    textfileL1L1KilledNorm.write(str(mass[i]) + " ")
    textfileL1L2.write(str(mass[i]) + " ")
    textfileL1L2Norm.write(str(mass[i]) + " ")
    textfileL1L2Killed.write(str(mass[i]) + " ")
    textfileL1L2KilledNorm.write(str(mass[i]) + " ")
    textfileL2L2.write(str(mass[i]) + " ")
    textfileL2L2Norm.write(str(mass[i]) + " ")
    textfileL2L2Killed.write(str(mass[i]) + " ")
    textfileL2L2KilledNorm.write(str(mass[i]) + " ")
textfileL1L1.write("\n")
textfileL1L1Norm.write("\n")
textfileL1L1Killed.write("\n")
textfileL1L1KilledNorm.write("\n")
textfileL1L2.write("\n")
textfileL1L2Norm.write("\n")
textfileL1L2Killed.write("\n")
textfileL1L2KilledNorm.write("\n")
textfileL2L2.write("\n")
textfileL2L2Norm.write("\n")
textfileL2L2Killed.write("\n")
textfileL2L2KilledNorm.write("\n")

#Write values of z in the 2nd row
for i in range(nBins):
    textfileL1L1.write(str(z[i]) + " ") 
    textfileL1L1Norm.write(str(z[i]) + " ") 
    textfileL1L1Killed.write(str(z[i]) + " ") 
    textfileL1L1KilledNorm.write(str(z[i]) + " ")  
    textfileL1L2.write(str(z[i]) + " ") 
    textfileL1L2Norm.write(str(z[i]) + " ") 
    textfileL1L2Killed.write(str(z[i]) + " ") 
    textfileL1L2KilledNorm.write(str(z[i]) + " ")  
    textfileL2L2.write(str(z[i]) + " ") 
    textfileL2L2Norm.write(str(z[i]) + " ") 
    textfileL2L2Killed.write(str(z[i]) + " ") 
    textfileL2L2KilledNorm.write(str(z[i]) + " ")  
textfileL1L1.write("\n")
textfileL1L1Norm.write("\n")
textfileL1L1Killed.write("\n")
textfileL1L1KilledNorm.write("\n")
textfileL1L2.write("\n")
textfileL1L2Norm.write("\n")
textfileL1L2Killed.write("\n")
textfileL1L2KilledNorm.write("\n")
textfileL2L2.write("\n")
textfileL2L2Norm.write("\n")
textfileL2L2Killed.write("\n")
textfileL2L2KilledNorm.write("\n")

L1L1events = []
L1L1killevents = []
L1L2events = []
L1L2killevents = []
L2L2events = []
L2L2killevents = []
eventstruth = []

histosL1L1 = []
histosL1L2 = []
histosL2L2 = []
histosTruth = []
normArr = array.array('d')

histosL1L1kill = []
histosL1L2kill = []
histosL2L2kill = []
normkillArr = array.array('d')
gammamean = array.array('d')
gammameanerror = array.array('d')
zeros = array.array('d')

openPDF(outfile+"_comparekill",c)
openPDF(outfile+"_fitplots",c)
#Loop over all values of mass
for i in range(nMass):
    inputL1L1ReconFile = TFile(str(L1L1Files[i])) #L1L1 tuple files after cuts
    inputL1L2ReconFile = TFile(str(L1L2Files[i])) #L1L2 tuple files after cuts
    inputL2L2ReconFile = TFile(str(L2L2Files[i])) #L2L2 tuple files after cuts
    inputTruthFile = TFile(str(truthFiles[i])) #truth files
    #L1L1events.append(inputL1L1ReconFile.Get(tupleName))
    #L1L2events.append(inputL1L2ReconFile.Get(tupleName))
    #L2L2events.append(inputL2L2ReconFile.Get(tupleName))
    L1L1events = inputL1L1ReconFile.Get(tupleName)
    L1L2events = inputL1L2ReconFile.Get(tupleName)
    L2L2events = inputL2L2ReconFile.Get(tupleName)
    L1L1killevents, L1L2killevents, L2L2killevents = KillHits(inputL1L1ReconFile.Get(tupleName),inputL1L2ReconFile.Get(tupleName),inputL2L2ReconFile.Get(tupleName),mass[i],L2L2Files[i],outfile)
    #L1L1killevents.append(eventsL1L1)
    #L1L2killevents.append(eventsL1L2)
    #L2L2killevents.append(eventsL2L2)
    #L1L1killevents.append(L1L1events[i])
    #L1L2killevents.append(L1L2events[i])
    #L2L2killevents.append(L2L2events[i])
    #L1L1killevents = eventsL1L1
    #L1L2killevents = eventsL1L2
    #L2L2killevents = eventsL2L2
    #L1L1killevents = L1L1events
    #L1L2killevents = L1L2events
    #L2L2killevents = L2L2events
    #eventstruth.append(inputTruthFile.Get(tupleName))
    eventstruth = inputTruthFile.Get(tupleName)
    CompareKill(L1L1events,L1L1killevents,L1L2events,L1L2killevents,L2L2events,L2L2killevents,eventstruth,nBins,targZ,outfileroot,c,outfile,mass[i])
#closePDF(outfile+"_comparekill",c)
    #del eventsL1L1
    #del eventsL1L2
    #del eventsL2L2

#histosL1L1 = []
#histosL1L2 = []
#histosL2L2 = []
#histosTruth = []
#normArr = []

#for i in range(nMass):
    print("Mass {0:0.0f}".format(mass[i]*1000))
    L1L1events.Draw("triEndZ>>histoReconL1L1_{3:0.0f}({0},{1},{2})".format(nBins,targZ,maxZ,mass[i]*1000))
    #histoReconL1L1 = ROOT.gROOT.FindObject("histoReconL1L1_{0:0.0f}".format(mass[i]*1000))
    histosL1L1.append(ROOT.gROOT.FindObject("histoReconL1L1_{0:0.0f}".format(mass[i]*1000)))
    L1L2events.Draw("triEndZ>>histoReconL1L2_{3:0.0f}({0},{1},{2})".format(nBins,targZ,maxZ,mass[i]*1000))
    #histoReconL1L2 = ROOT.gROOT.FindObject("histoReconL1L2_{0:0.0f}".format(mass[i]*1000))
    histosL1L2.append(ROOT.gROOT.FindObject("histoReconL1L2_{0:0.0f}".format(mass[i]*1000)))
    L2L2events.Draw("triEndZ>>histoReconL2L2_{3:0.0f}({0},{1},{2})".format(nBins,targZ,maxZ,mass[i]*1000))
    #histoReconL2L2 = ROOT.gROOT.FindObject("histoReconL2L2_{0:0.0f}".format(mass[i]*1000))
    histosL2L2.append(ROOT.gROOT.FindObject("histoReconL2L2_{0:0.0f}".format(mass[i]*1000)))
    eventstruth.Draw("triEndZ>>histoTruth_{3:0.0f}({0},{1},{2})".format(nBins,targZ,maxZ,mass[i]*1000),"triStartP>0.8*{0}".format(eBeam))
    #histoTruth = ROOT.gROOT.FindObject("histoTruth".format(mass[i]*1000))
    histosTruth.append(ROOT.gROOT.FindObject("histoTruth_{0:0.0f}".format(mass[i]*1000)))
    #histoReconL1L1.Sumw2()
    #histoReconL1L2.Sumw2()
    #histoReconL2L2.Sumw2()
    #histoTruth.Sumw2()
    histosL1L1[i].Sumw2()
    histosL1L2[i].Sumw2()
    histosL2L2[i].Sumw2()
    histosTruth[i].Sumw2()
    outfileroot.cd()
    histosL1L1[i].Write("L1L1 {0:0.0f} MeV".format(mass[i]*1000))
    histosL1L2[i].Write("L1L2 {0:0.0f} MeV".format(mass[i]*1000))
    histosL2L2[i].Write("L2L2 {0:0.0f} MeV".format(mass[i]*1000))
    histosTruth[i].Write("Truth {0:0.0f} MeV".format(mass[i]*1000))

    #Find the normalization based on a certain number of bins
    norm = plotFit(histosL1L1[i],histosL1L2[i],histosL2L2[i],histosTruth[i],normArr,outfile+"_fitplots",outfileroot,c,mass[i],targZ,title="Without Hit Killing")
    #norm = 0.0
    #for j in range(nNorm):
        #if (histoTruth.GetBinContent(j+1) != 0): 
        #    norm += histoReconL1L1.GetBinContent(j+1)/histoTruth.GetBinContent(j+1)
    #    if (histosTruth[i].GetBinContent(j+1) != 0): 
    #        norm += histosL1L1[i].GetBinContent(j+1)/histosTruth[i].GetBinContent(j+1)
    #    else: 
    #        norm = 0.0
    #        break
    #norm = norm/nNorm
    print norm
    normArr.append(norm)
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
            #textfileL1L1.write(str(histoReconL1L1.GetBinContent(j+1)/histoTruth.GetBinContent(j+1)) + " ")
            #textfileL1L2.write(str(histoReconL1L2.GetBinContent(j+1)/histoTruth.GetBinContent(j+1)) + " ")
            #textfileL2L2.write(str(histoReconL2L2.GetBinContent(j+1)/histoTruth.GetBinContent(j+1)) + " ")
            textfileL1L1.write(str(histosL1L1[i].GetBinContent(j+1)/histosTruth[i].GetBinContent(j+1)) + " ")
            textfileL1L2.write(str(histosL1L2[i].GetBinContent(j+1)/histosTruth[i].GetBinContent(j+1)) + " ")
            textfileL2L2.write(str(histosL2L2[i].GetBinContent(j+1)/histosTruth[i].GetBinContent(j+1)) + " ")
            if(norm != 0):
                #textfileL1L1Norm.write(str(histoReconL1L1.GetBinContent(j+1)/(histoTruth.GetBinContent(j+1)*norm)) + " ")
                #textfileL1L2Norm.write(str(histoReconL1L2.GetBinContent(j+1)/(histoTruth.GetBinContent(j+1)*norm)) + " ")
                #textfileL2L2Norm.write(str(histoReconL2L2.GetBinContent(j+1)/(histoTruth.GetBinContent(j+1)*norm)) + " ")
                textfileL1L1Norm.write(str(histosL1L1[i].GetBinContent(j+1)/(histosTruth[i].GetBinContent(j+1)*norm)) + " ")
                textfileL1L2Norm.write(str(histosL1L2[i].GetBinContent(j+1)/(histosTruth[i].GetBinContent(j+1)*norm)) + " ")
                textfileL2L2Norm.write(str(histosL2L2[i].GetBinContent(j+1)/(histosTruth[i].GetBinContent(j+1)*norm)) + " ")
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
    L1L1events.Draw("triStartP/({4})>>gammahisto_{3:0.0f}({0},{1},{2})".format(nBins,0.8,1.,mass[i]*1000,eBeam))
    histosgamma.append(ROOT.gROOT.FindObject("gammahisto_{0:0.0f}".format(mass[i]*1000)))
    gammamean.append(histosgamma[i].GetMean())
    print(histosgamma[i].GetMean())
    gammameanerror.append(histosgamma[i].GetMeanError())
    zeros.append(0.)

#textfileL1L1.close()
#textfileL1L1Norm.close()
#textfileL1L2.close()
#textfileL1L2Norm.close()
#textfileL2L2.close()
#textfileL2L2Norm.close()

#histosL1L1kill = []
#histosL1L2kill = []
#histosL2L2kill = []
#normkillArr = []

#for i in range(nMass):
    L1L1killevents.Draw("triEndZ>>histoReconL1L1_kill_{3:0.0f}({0},{1},{2})".format(nBins,targZ,maxZ,mass[i]*1000))
    #histoReconL1L1 = ROOT.gROOT.FindObject("histoReconL1L1")
    histosL1L1kill.append(ROOT.gROOT.FindObject("histoReconL1L1_kill_{0:0.0f}".format(mass[i]*1000)))
    L1L2killevents.Draw("triEndZ>>histoReconL1L2_kill_{3:0.0f}({0},{1},{2})".format(nBins,targZ,maxZ,mass[i]*1000))
    #histoReconL1L2 = ROOT.gROOT.FindObject("histoReconL1L2")
    histosL1L2kill.append(ROOT.gROOT.FindObject("histoReconL1L2_kill_{0:0.0f}".format(mass[i]*1000)))
    L2L2killevents.Draw("triEndZ>>histoReconL2L2_kill_{3:0.0f}({0},{1},{2})".format(nBins,targZ,maxZ,mass[i]*1000))
    #histoReconL2L2 = ROOT.gROOT.FindObject("histoReconL2L2")
    histosL2L2kill.append(ROOT.gROOT.FindObject("histoReconL2L2_kill_{0:0.0f}".format(mass[i]*1000)))
    #eventstruth[i].Draw("triEndZ>>histoTruth({0},{1},{2})".format(nBins,targZ,maxZ),"triStartP>0.8*{0}".format(eBeam))
    #histoTruth = ROOT.gROOT.FindObject("histoTruth")
    #histoReconL1L1.Sumw2()
    #histoReconL1L2.Sumw2()
    #histoReconL2L2.Sumw2()
    #histoTruth.Sumw2()
    histosL1L1kill[i].Sumw2()
    histosL1L2kill[i].Sumw2()
    histosL2L2kill[i].Sumw2()
    outfileroot.cd()
    histosL1L1kill[i].Write("L1L1 {0:0.0f} MeV Hit Killed".format(mass[i]*1000))
    histosL1L2kill[i].Write("L1L2 {0:0.0f} MeV Hit Killed".format(mass[i]*1000))
    histosL2L2kill[i].Write("L2L2 {0:0.0f} MeV Hit Killed".format(mass[i]*1000))
    #Find the normalization based on a certain number of bins
    normKill = plotFit(histosL1L1kill[i],histosL1L2kill[i],histosL2L2kill[i],histosTruth[i],normArr,outfile+"_fitplots",outfileroot,c,mass[i],targZ,title="With Hit Killing")
    #norm = 0.0
    #for j in range(nNorm):
        #if (histoTruth.GetBinContent(j+1) != 0): 
        #    norm += histoReconL1L1.GetBinContent(j+1)/histoTruth.GetBinContent(j+1)
    #    if (histosTruth[i].GetBinContent(j+1) != 0): 
    #        norm += (histosL1L1kill[i].GetBinContent(j+1)+histosL1L2kill[i].GetBinContent(j+1)+histosL2L2kill[i].GetBinContent(j+1))/histosTruth[i].GetBinContent(j+1)
    #    else: 
    #        norm = 0.0
    #        break
    #norm = norm/nNorm
    print normKill
    normkillArr.append(normKill)
    #Write the efficiency for a given mass (row) as function of z
    for j in range(nBins):
        if (histosTruth[i].GetBinContent(j+1) == 0):
            textfileL1L1Killed.write("0.0 ")
            textfileL1L1KilledNorm.write("0.0 ")
            textfileL1L2Killed.write("0.0 ")
            textfileL1L2KilledNorm.write("0.0 ")
            textfileL2L2Killed.write("0.0 ")
            textfileL2L2KilledNorm.write("0.0 ")
        else:
            #textfileL1L1Killed.write(str(histoReconL1L1.GetBinContent(j+1)/histoTruth.GetBinContent(j+1)) + " ")
            #textfileL1L2Killed.write(str(histoReconL1L2.GetBinContent(j+1)/histoTruth.GetBinContent(j+1)) + " ")
            #textfileL2L2Killed.write(str(histoReconL2L2.GetBinContent(j+1)/histoTruth.GetBinContent(j+1)) + " ")
            textfileL1L1Killed.write(str(histosL1L1kill[i].GetBinContent(j+1)/histosTruth[i].GetBinContent(j+1)) + " ")
            textfileL1L2Killed.write(str(histosL1L2kill[i].GetBinContent(j+1)/histosTruth[i].GetBinContent(j+1)) + " ")
            textfileL2L2Killed.write(str(histosL2L2kill[i].GetBinContent(j+1)/histosTruth[i].GetBinContent(j+1)) + " ")
            if(norm != 0):
                #textfileL1L1KilledNorm.write(str(histoReconL1L1.GetBinContent(j+1)/(histoTruth.GetBinContent(j+1)*norm)) + " ")
                #textfileL1L2KilledNorm.write(str(histoReconL1L2.GetBinContent(j+1)/(histoTruth.GetBinContent(j+1)*norm)) + " ")
                #textfileL2L2KilledNorm.write(str(histoReconL2L2.GetBinContent(j+1)/(histoTruth.GetBinContent(j+1)*norm)) + " ")
                textfileL1L1KilledNorm.write(str(histosL1L1kill[i].GetBinContent(j+1)/(histosTruth[i].GetBinContent(j+1)*norm)) + " ")
                textfileL1L2KilledNorm.write(str(histosL1L2kill[i].GetBinContent(j+1)/(histosTruth[i].GetBinContent(j+1)*norm)) + " ")
                textfileL2L2KilledNorm.write(str(histosL2L2kill[i].GetBinContent(j+1)/(histosTruth[i].GetBinContent(j+1)*norm)) + " ")
            else:
                textfileL1L1KilledNorm.write("0.0 ")
                textfileL1L2KilledNorm.write("0.0 ")
                textfileL2L2KilledNorm.write("0.0 ")
    textfileL1L1Killed.write("\n")
    textfileL1L1KilledNorm.write("\n")
    textfileL1L2Killed.write("\n")
    textfileL1L2KilledNorm.write("\n")
    textfileL2L2Killed.write("\n")
    textfileL2L2KilledNorm.write("\n")
    del L1L1events
    del L1L2events
    del L2L2events
    del L1L1killevents
    del L1L2killevents
    del L2L2killevents
    del eventstruth
    del inputL1L1ReconFile
    del inputL1L2ReconFile
    del inputL2L2ReconFile
    del inputTruthFile

textfileL1L1.close()
textfileL1L1Norm.close()
textfileL1L2.close()
textfileL1L2Norm.close()
textfileL2L2.close()
textfileL2L2Norm.close()

textfileL1L1Killed.close()
textfileL1L1KilledNorm.close()
textfileL1L2Killed.close()
textfileL1L2KilledNorm.close()
textfileL2L2Killed.close()
textfileL2L2KilledNorm.close()

closePDF(outfile+"_comparekill",c)
closePDF(outfile+"_fitplots",c)

#Make test plots if desired
if(makeTestPlots):
    #Make Absolute Efficiency Plots
    c1 = TCanvas("c","c",1200,900)
    c1.Print(outfile+"_L1L1.pdf[")   

    for i in range(1,nMass-1):
        plotTest(i,outfile+"_L1L1.eff",outfile,targZ,maxZ,c1)

    c1.Print(outfile+"_L1L1.pdf]")

    del c1
    
    #Make Normalized Efficiency Plots
    c2 = TCanvas("c","c",1200,900)
    c2.Print(outfile+"_L1L1_norm.pdf[")

    for i in range(1,nMass-1):
        plotTest(i,outfile+"_L1L1_norm.eff",outfileNorm,targZ,maxZ,c2)

    c2.Print(outfile+"_L1L1_norm.pdf]")

    del c2

    #Make Absolute Efficiency Plots
    c3 = TCanvas("c","c",1200,900)
    c3.Print(outfile+"_L1L1_kill.pdf[")   

    for i in range(1,nMass-1):
        plotTest(i,outfile+"_L1L1_kill.eff",outfile,targZ,maxZ,c3)

    c3.Print(outfile+"_L1L1_kill.pdf]")

    del c3
    
    #Make Normalized Efficiency Plots
    c4 = TCanvas("c","c",1200,900)
    c4.Print(outfile+"_L1L1_kill_norm.pdf[")

    for i in range(1,nMass-1):
        plotTest(i,outfile+"_L1L1_kill_norm.eff",outfileNorm,targZ,maxZ,c4)

    c4.Print(outfile+"_L1L1_kill_norm.pdf]")

    del c4


        #Make Absolute Efficiency Plots
    c5 = TCanvas("c","c",1200,900)
    c5.Print(outfile+"_L1L2.pdf[")   

    for i in range(1,nMass-1):
        plotTest(i,outfile+"_L1L2.eff",outfile,targZ,maxZ,c5)

    c5.Print(outfile+"_L1L2.pdf]")

    del c5
    
    #Make Normalized Efficiency Plots
    c6 = TCanvas("c","c",1200,900)
    c6.Print(outfile+"_L1L2_norm.pdf[")

    for i in range(1,nMass-1):
        plotTest(i,outfile+"_L1L2_norm.eff",outfileNorm,targZ,maxZ,c6)

    c6.Print(outfile+"_L1L2_norm.pdf]")

    del c6

    #Make Absolute Efficiency Plots
    c7 = TCanvas("c","c",1200,900)
    c7.Print(outfile+"_L1L2_kill.pdf[")   

    for i in range(1,nMass-1):
        plotTest(i,outfile+"_L1L2_kill.eff",outfile,targZ,maxZ,c7)

    c7.Print(outfile+"_L1L2_kill.pdf]")

    del c7
    
    #Make Normalized Efficiency Plots
    c8 = TCanvas("c","c",1200,900)
    c8.Print(outfile+"_L1L2_kill_norm.pdf[")

    for i in range(1,nMass-1):
        plotTest(i,outfile+"_L1L2_kill_norm.eff",outfileNorm,targZ,maxZ,c8)

    c8.Print(outfile+"_L1L2_kill_norm.pdf]")

    del c8


        #Make Absolute Efficiency Plots
    c9 = TCanvas("c","c",1200,900)
    c9.Print(outfile+"_L2L2.pdf[")   

    for i in range(1,nMass-1):
        plotTest(i,outfile+"_L2L2.eff",outfile,targZ,maxZ,c9)

    c9.Print(outfile+"_L2L2.pdf]")

    del c9
    
    #Make Normalized Efficiency Plots
    c10 = TCanvas("c","c",1200,900)
    c10.Print(outfile+"_L2L2_norm.pdf[")

    for i in range(1,nMass-1):
        plotTest(i,outfile+"_L2L2_norm.eff",outfileNorm,targZ,maxZ,c10)

    c10.Print(outfile+"_L2L2_norm.pdf]")

    del c10

    #Make Absolute Efficiency Plots
    c11 = TCanvas("c","c",1200,900)
    c11.Print(outfile+"_L2L2_kill.pdf[")   

    for i in range(1,nMass-1):
        plotTest(i,outfile+"_L2L2_kill.eff",outfile,targZ,maxZ,c11)

    c11.Print(outfile+"_L2L2_kill.pdf]")

    del c11
    
    #Make Normalized Efficiency Plots
    c12 = TCanvas("c","c",1200,900)
    c12.Print(outfile+"_L2L2_kill_norm.pdf[")

    for i in range(1,nMass-1):
        plotTest(i,outfile+"_L2L2_kill_norm.eff",outfileNorm,targZ,maxZ,c12)

    c12.Print(outfile+"_L2L2_kill_norm.pdf]")

    del c12

c13 = TCanvas("c","c",1200,900)
#plotEff(outfile+"_L1L1.eff",outfile+"_L1L1",nBins,targZ,maxZ,c13)
#plotEff(outfile+"_L1L1_norm.eff",outfile+"_L1L1_norm",nBins,targZ,maxZ,c13)
#plotEff(outfile+"_L1L1_kill.eff",outfile+"_L1L1_kill",nBins,targZ,maxZ,c13)
#plotEff(outfile+"_L1L1_kill_norm.eff",outfile+"_L1L1_kill_norm",nBins,targZ,maxZ,c13)
#plotEff(outfile+"_L1L2.eff",outfile+"_L1L2",nBins,targZ,maxZ,c13)
#plotEff(outfile+"_L1L2_norm.eff",outfile+"_L1L2_norm",nBins,targZ,maxZ,c13)
#plotEff(outfile+"_L1L2_kill.eff",outfile+"_L1L2_kill",nBins,targZ,maxZ,c13)
#plotEff(outfile+"_L1L2_kill_norm.eff",outfile+"_L1L2_kill_norm",nBins,targZ,maxZ,c13)
#plotEff(outfile+"_L2L2.eff",outfile+"_L2L2",nBins,targZ,maxZ,c13)
#plotEff(outfile+"_L2L2_norm.eff",outfile+"_L2L2_norm",nBins,targZ,maxZ,c13)
#plotEff(outfile+"_L2L2_kill.eff",outfile+"_L2L2_kill",nBins,targZ,maxZ,c13)
#plotEff(outfile+"_L2L2_kill_norm.eff",outfile+"_L2L2_kill_norm",nBins,targZ,maxZ,c13)

c13.Print(outfile+"_plots.pdf[") 

plotEff2(histosL1L1,histosTruth,normArr,outfile+"_L1L1",outfile+"_plots",outfileroot,c13,mass,False,title="L1L1")
plotEff2(histosL1L1,histosTruth,normArr,outfile+"_L1L1_norm",outfile+"_plots",outfileroot,c13,mass,True,title="L1L1 Normalized")
plotEff2(histosL1L1kill,histosTruth,normkillArr,outfile+"_L1L1_kill",outfile+"_plots",outfileroot,c13,mass,False,title="L1L1 Hit Killed")
plotEff2(histosL1L1kill,histosTruth,normkillArr,outfile+"_L1L1_kill_norm",outfile+"_plots",outfileroot,c13,mass,True,title="L1L1 Normalized Hit Killed")
plotEff2(histosL1L2,histosTruth,normArr,outfile+"_L1L2",outfile+"_plots",outfileroot,c13,mass,False,title="L1L2")
plotEff2(histosL1L2,histosTruth,normArr,outfile+"_L1L2_norm",outfile+"_plots",outfileroot,c13,mass,True,title="L2L2 Normalized")
plotEff2(histosL1L2kill,histosTruth,normkillArr,outfile+"_L1L2_kill",outfile+"_plots",outfileroot,c13,mass,False,title="L1L2 Hit Killed")
plotEff2(histosL1L2kill,histosTruth,normkillArr,outfile+"_L1L2_kill_norm",outfile+"_plots",outfileroot,c13,mass,True,title="L1L2 Normalized Hit Killed")
plotEff2(histosL2L2,histosTruth,normArr,outfile+"_L2L2",outfile+"_plots",outfileroot,c13,mass,False,title="L2L2")
plotEff2(histosL2L2,histosTruth,normArr,outfile+"_L2L2_norm",outfile+"_plots",outfileroot,c13,mass,True,title="L2L2 Normalized")
plotEff2(histosL2L2kill,histosTruth,normkillArr,outfile+"_L2L2_kill",outfile+"_plots",outfileroot,c13,mass,False,title="L2L2 Hit Killed")
plotEff2(histosL2L2kill,histosTruth,normkillArr,outfile+"_L2L2_kill_norm",outfile+"_plots",outfileroot,c13,mass,True,title="L2L2 Normalized Hit Killed")

plotAll(histosL1L1,histosL1L2,histosL2L2,histosTruth,normArr,outfile+"_all",outfile+"_plots",outfileroot,c13,mass)
plotAll(histosL1L1kill,histosL1L2kill,histosL2L2kill,histosTruth,normkillArr,outfile+"_kill_all",outfile+"_plots",outfileroot,c13,mass,title="With Hit Killing")

passed.Sumw2()
total.Sumw2()
passed.Divide(total)
passed.SetTitle("L1 Hit Efficiency")
passed.GetXaxis().SetTitle("Track Slope")
passed.GetYaxis().SetTitle("Efficiency")
passed.SetStats(0)
passed.Draw()
c13.Print(outfile+"_plots.pdf") 
passed.Write("Efficiency")

graph = TGraphErrors(len(mass),mass,gammamean,zeros,gammameanerror)
graph.SetTitle("A' Truth Energy / E_{beam}")
graph.GetXaxis().SetTitle("Truth Mass (GeV)")
graph.GetYaxis().SetTitle("Fraction of E_{beam}")
graph.GetXaxis().SetRangeUser(0,.2)
graph.GetYaxis().SetRangeUser(0.9,1.0)
graph.Draw("AP")
c13.Print(outfile+"_plots.pdf") 
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
    MakeGammaHistos(histosgamma[i],mass[i]*1000,c13,outfile+"_plots")

graph = TGraph(len(mass),mass,normArr)
graph2 = TGraph(len(mass),mass,normkillArr)
graph.SetTitle("Prompt A' Acceptance * Efficiency")
graph.GetXaxis().SetTitle("Truth Mass (GeV)")
graph.GetYaxis().SetTitle("Efficiency")
graph.GetXaxis().SetRangeUser(0,.2)
graph.GetYaxis().SetRangeUser(0,0.4)
graph.SetLineColor(1)
graph.SetMarkerColor(1)
graph2.SetLineColor(2)
graph2.SetMarkerColor(2)
graph.Draw("AP*")
graph2.Draw("P* same")
legend = TLegend(.58,.66,.92,.87)
legend.SetBorderSize(0)
legend.SetFillColor(0)
legend.SetFillStyle(0)
legend.SetTextFont(42)
legend.SetTextSize(0.035)
legend.AddEntry(graph,"No L1 Hit Killing","LP")
legend.AddEntry(graph2,"With L1 Hit Killing","LP")
legend.Draw("same")
c13.Print(outfile+"_plots.pdf") 
graph.Write("Prompt Acceptance")
graph2.Write("Prompt Acceptance With Hit Killing")


c13.Print(outfile+"_plots.pdf]") 
outfileroot.Close()