#!/usr/bin/env python
import sys
import array, math
import ROOT
from ROOT import gROOT, gStyle, TFile, TTree, TChain, TMVA, TCut, TCanvas, gDirectory, TH1, TH1F, TGraph, gPad, TF1, TGraphErrors, TLegend, TGaxis, TLine, TMath
import getopt


def print_usage():
    print "\nUsage:"
    print "Arguments: "
    print '\t-h: this help message'
    print "\n"

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'h')

# Parse the command line arguments
for opt, arg in options:
        if opt=='-h':
            print_usage()
            sys.exit(0)

filename1 = "/home/mrsolt/hps/Layer6/eng2015rawplotsslot.root"
filename2 = "/home/mrsolt/hps/Layer6/phys2016rawplotsslot.root"

chanMin = 301
chanMax = 330
nSamples = 6
L1Sensor = "module_L1t_halfmodule_axial_sensor0"
L6Sensor = "module_L6t_halfmodule_stereo_slot_sensor0"

inFile1 = TFile(filename1)
inFile2 = TFile(filename2)

histo1 = inFile1.Get(L6Sensor + " Channel " + str(chanMin) + " - Amplitude")
histo2 = inFile2.Get(L6Sensor + " Channel " + str(chanMin) + " - Amplitude")

c = TCanvas("c","c",800,600)

legend = TLegend(.65,.66,.89,.87)
legend.SetBorderSize(0)
legend.SetFillColor(0)
legend.SetFillStyle(0)
legend.SetTextFont(42)
legend.SetTextSize(0.035)
legend.AddEntry(histo1,"Eng 2015","LP")
legend.AddEntry(histo2,"Phys 2016","LP")

def plot(inFile1,inFile2,sensor,chanMin,chanMax,histo,legend,outName):
    c.Print(outName + ".pdf[")
    for chan in range(chanMin,chanMax):
        histo1 = inFile1.Get(sensor + " Channel " + str(chan) + " - " + histo)
        histo2 = inFile2.Get(sensor + " Channel " + str(chan) + " - " + histo)
        histo1.Scale(1./histo1.Integral())
        histo2.Scale(1./histo2.Integral())
        max1 = histo1.GetMaximum()
	max2 = histo2.GetMaximum()
	maxHisto = 1.0
	if max1 > max2: maxHisto = 1.2*max1
	else: maxHisto = 1.2*max2
        histo1.Draw("")
        histo1.SetTitle(histo1.GetTitle())
	histo1.GetYaxis().SetRangeUser(0,maxHisto)
        histo2.Draw("same")
        histo2.SetLineColor(2)
        legend.Draw("")
        c.Print(outName + ".pdf")
	gStyle.SetOptStat(0)
    c.Print(outName + ".pdf]")

def plot2D(inFile,sensor,chanMin,chanMax,histo,outName):
    c.Print(outName + ".pdf[")
    for chan in range(chanMin,chanMax):
        histo1 = inFile.Get(sensor + " Channel " + str(chan) + " - " + histo)
        histo1.Draw("COLZ")
        histo1.SetTitle(histo1.GetTitle())
        c.Print(outName + ".pdf")
    c.Print(outName + ".pdf]")

def plot2DNeighbor(inFile,sensor,chanMin,chanMax,histo,outName):
    c.Print(outName + ".pdf[")
    for chan in range(chanMin,chanMax):
        histo1 = inFile.Get(sensor + " Channel " + str(chan) + " - " + histo)
        histo1.Draw("COLZ")
        histo1.SetTitle(histo1.GetTitle())
        c.Print(outName + ".pdf")
    c.Print(outName + ".pdf]")

def plotSample(inFile1,inFile2,sensor,chanMin,chanMax,histo,legend,outName):
    c.Print(outName + ".pdf[")
    for chan in range(chanMin,chanMax):
        histo2D1 = inFile1.Get(sensor + " Channel " + str(chan) + " - " + histo)
        histo2D2 = inFile2.Get(sensor + " Channel " + str(chan) + " - " + histo)
	histo1 = histo2D1.ProjectionY("histo1",4,4)
	histo2 = histo2D2.ProjectionY("histo2",4,4)
        histo1.Scale(1./histo1.Integral())
        histo2.Scale(1./histo2.Integral())
        max1 = histo1.GetMaximum()
	max2 = histo2.GetMaximum()
	maxHisto = 1.0
	if max1 > max2: maxHisto = 1.2*max1
	else: maxHisto = 1.2*max2
        histo1.Draw("")
        histo1.SetTitle(histo2D1.GetTitle())
	histo1.GetYaxis().SetRangeUser(0,maxHisto)
        histo2.Draw("same")
        histo2.SetLineColor(2)
        legend.Draw("")
        c.Print(outName + ".pdf")
	gStyle.SetOptStat(0)
    c.Print(outName + ".pdf]")

def plotAllSamples(inFile1,inFile2,sensor,chanMin,chanMax,histo,legend,outName):
    c.Print(outName + ".pdf[")
    for chan in range(chanMin,chanMax):
        histo2D1 = inFile1.Get(sensor + " Channel " + str(chan) + " - " + histo)
        histo2D2 = inFile2.Get(sensor + " Channel " + str(chan) + " - " + histo)
	for i in range(nSamples):
	    histo1 = histo2D1.ProjectionY("histo1_"+str(i),i+1,i+1)
	    histo2 = histo2D2.ProjectionY("histo2_"+str(i),i+1,i+1)
            histo1.Scale(1./histo1.Integral())
            histo2.Scale(1./histo2.Integral())
            max1 = histo1.GetMaximum()
	    max2 = histo2.GetMaximum()
	    maxHisto = 1.0
	    if max1 > max2: maxHisto = 1.2*max1
	    else: maxHisto = 1.2*max2
            histo1.Draw("")
            histo1.SetTitle(histo2D1.GetTitle()+" Sample "+ str(i))
	    histo1.GetYaxis().SetRangeUser(0,maxHisto)
            histo2.Draw("same")
            histo2.SetLineColor(2)
            legend.Draw("")
            c.Print(outName + ".pdf")
	    gStyle.SetOptStat(0)
    c.Print(outName + ".pdf]")


def plotAllSamplesMean(inFile1,inFile2,sensor,chanMin,chanMax,histo,legend,outName):
    c.Print(outName + "_mean.pdf[")
    for chan in range(chanMin,chanMax):
        histo2D1 = inFile1.Get(sensor + " Channel " + str(chan) + " - " + histo)
        histo2D2 = inFile2.Get(sensor + " Channel " + str(chan) + " - " + histo)
	mean1 = TH1F("","",nSamples,0,nSamples)
        mean2 = TH1F("","",nSamples,0,nSamples)
	shift1 = 0
	shift2 = 0
	for i in range(nSamples):
	    histo1 = histo2D1.ProjectionY("histo1_"+str(i),i+1,i+1)
	    histo2 = histo2D2.ProjectionY("histo2_"+str(i),i+1,i+1)
            histo1.Scale(1./histo1.Integral())
            histo2.Scale(1./histo2.Integral())
	    if i == 0:
		shift1 = histo1.GetMean()
		shift2 = histo2.GetMean()
	    error1 = histo1.GetRMS()/TMath.Sqrt(histo1.GetEntries())
            error2 = histo1.GetRMS()/TMath.Sqrt(histo2.GetEntries())
	    mean1.Fill(i,histo1.GetMean() - shift1)
	    mean2.Fill(i,histo2.GetMean() - shift2)
	    mean1.SetBinError(i+1,error1)
	    mean2.SetBinError(i+1,error2)	
        mean1.Draw("")
        mean1.SetTitle(histo2D1.GetTitle()+" Mean Sample")
	mean1.GetYaxis().SetRangeUser(0,1000)
        mean2.Draw("same")
        mean2.SetLineColor(2)
        legend.Draw("")
        c.Print(outName + "_mean.pdf")
	gStyle.SetOptStat(0)	
    c.Print(outName + "_mean.pdf]")

plot(inFile1,inFile2,L6Sensor,chanMin,chanMax,"Amplitude",legend,"L6Amplitude")
c.Clear()
plot(inFile1,inFile2,L6Sensor,chanMin,chanMax,"Neighbor Amplitude",legend,"L6NeighborAmplitude")
c.Clear()
plot(inFile1,inFile2,L6Sensor,chanMin,chanMax,"Chi2 Probability",legend,"L6Chi2Probability")
c.Clear()
plot(inFile1,inFile2,L6Sensor,chanMin,chanMax,"Neighbor Chi2 Probability",legend,"L6NeighborChi2Probability")
c.Clear()
plot(inFile1,inFile2,L6Sensor,chanMin,chanMax,"First Pedestal ADC Counts",legend,"L6FirstPedestalADCCounts")
c.Clear()
plot(inFile1,inFile2,L6Sensor,chanMin,chanMax,"Neighbor First Pedestal ADC Counts",legend,"L6NeighborFirstPedestalADCCounts")
c.Clear()
plot(inFile1,inFile2,L6Sensor,chanMin,chanMax,"T0",legend,"L6T0")
c.Clear()
plot(inFile1,inFile2,L6Sensor,chanMin,chanMax,"Neighbor T0",legend,"L6NeighborT0")
c.Clear()

plot2D(inFile1,L6Sensor,chanMin,chanMax,"ADC Counts","Eng2015L6ADCCounts")
c.Clear()
plot2D(inFile2,L6Sensor,chanMin,chanMax,"ADC Counts","Phy2016L6ADCCounts")
c.Clear()
plot2DNeighbor(inFile1,L6Sensor,chanMin,chanMax,"Neighbor ADC Counts","Eng2015L6NeighborADCCounts")
c.Clear()
plot2DNeighbor(inFile2,L6Sensor,chanMin,chanMax,"Neighbor ADC Counts","Phy2016L6NeighborADCCounts")
c.Clear()
plot2D(inFile1,L6Sensor,chanMin,chanMax,"Chi2 vs Amplitude","Eng2015L6Chi2Amp")
c.Clear()
plot2D(inFile2,L6Sensor,chanMin,chanMax,"Chi2 vs Amplitude","phys2016L6Chi2Amp")
c.Clear()
plot2D(inFile1,L6Sensor,chanMin,chanMax,"Neighbor Chi2 vs Amplitude","Eng2015L6NeighborChi2Amp")
c.Clear()
plot2D(inFile2,L6Sensor,chanMin,chanMax,"Neighbor Chi2 vs Amplitude","phys2016L6NeighborChi2Amp")
c.Clear()
plot2D(inFile1,L6Sensor,chanMin,chanMax,"Sample 1 vs Sample 4","Eng2015L6Samp1Samp4")
c.Clear()
plot2D(inFile2,L6Sensor,chanMin,chanMax,"Sample 1 vs Sample 4","phys2016L6Samp1Samp4")
c.Clear()
plot2D(inFile1,L6Sensor,chanMin,chanMax,"Neighbor Sample 1 vs Sample 4","Eng2015L6NeighborSamp1Samp4")
c.Clear()
plot2D(inFile2,L6Sensor,chanMin,chanMax,"Neighbor Sample 1 vs Sample 4","phys2016L6NeighborSamp1Samp4")
c.Clear()

plotSample(inFile1,inFile2,L6Sensor,chanMin,chanMax,"ADC Counts",legend,"L6Sample4")
c.Clear()

plotAllSamples(inFile1,inFile2,L6Sensor,chanMin,chanMax,"ADC Counts",legend,"L6AllSamples")
c.Clear()
plotAllSamplesMean(inFile1,inFile2,L6Sensor,chanMin,chanMax,"ADC Counts",legend,"L6AllSamples")
c.Clear()

c.Update()
