#!/usr/bin/env python
import sys, array, math
import getopt
import upperlimit
import numpy
import EffFuncs
from EffFuncs import Interpolate, getMassArray, getZArray, getEfficiency
import ROOT
from ROOT import gROOT, TTree, TCanvas, TF1, TFile, gStyle, TFormula, TGraph, TGraphErrors, TH1D, TH1F, TCutG, TH2D, gDirectory, RooDataSet, RooRealVar, RooArgSet, RooFormulaVar, RooWorkspace, RooAbsData, RooFit, RooAbsReal, RooArgList, gPad, RooDataHist, RooHistPdf, TMath, TLatex, TPaveText, TLegend
from ROOT.RooStats import ModelConfig, ProfileLikelihoodCalculator, LikelihoodIntervalPlot

def print_usage():
    print "\nUsage: {0} <output basename> <input ROOT 2D histo file> <efficiency text file>".format(sys.argv[0])
    print "Arguments: "
    print '\t-z: target z (default -4.3 mm)'
    print '\t-s: scale factor (default 1)'
    print '\t-b: number of mass and epsilon bins (default 50)'
    print '\t-y: add title to plots'
    print '\t-h: this help message'
    print "\n"


scale_factor = 1
massVar = "uncM"
label = ""

#Model and Fit Ranges
targetz = -4.3
maxz = 90 #max Z out to where we have acceptance

#Mass Resolution Parameters
masscut_nsigma = 2.80
masscut_eff = 0.93

CL = 0.90
gamma = 0.965


options, remainder = getopt.gnu_getopt(sys.argv[1:], 'tuz:s:y:b:h')
for opt, arg in options:
    if opt=='-z':
        targetz = float(arg)
    if opt=='-s':
        scale_factor = float(arg)
    if opt=='-y':
        label = str(arg)
    if opt=='-b':
        n_massbins = int(arg)
        n_epsbins = int(arg)
    elif opt=='-h':
        print_usage()
        sys.exit(0)


gROOT.SetBatch(True)
gStyle.SetOptFit(1)
gStyle.SetOptStat(0)
c = TCanvas("c","c",800,600);

inFileL1L1 = TFile(remainder[1])
effFileL1L1 = remainder[2]
eventsL1L1 = inFileL1L1.Get("ntuple")

gStyle.SetOptStat(1111)

fzL1L1 = TF1("fzL1L1","{0}+{1}*x+{2}*x^2+{3}*x^3+{4}*x^4+{5}*x^5".format(-2.308,1227,-29030,285300,-1296000,2229000),0.05,0.175) #L1L1 10%
radfracf = TF1("radfracf","{0}+{1}*x+{2}*x^2+{3}*x^3+{4}*x^4+{5}*x^5".format(0.1926,-2.142,11.7,26,95,-385.9,823.2),0.04,0.2)
num_pairsf = TF1("num_pairsf","exp({0}+{1}*x+{2}*x^2+{3}*x^3+{4}*x^4+{5}*x^5)".format(4.903,208.3,-1880,-1868,68700,-198000),0.04,0.2)
mresL1L1f = TF1("mresL1L1f","{0}+{1}*x+{2}*x^2+{3}*x^3+{4}*x^4+{5}*x^5".format(0.01095/1000.,0.04305,0,0,0,0),0.04,0.2)

zArrL1L1 = getZArray(effFileL1L1)
mArrL1L1 = getMassArray(effFileL1L1)
effMatL1L1 = getEfficiency(effFileL1L1)

zArr = array.array('d')
outputArr1 = array.array('d')
outputArr2 = array.array('d')
outputArr3 = array.array('d')

wL1L1 = RooWorkspace("wL1L1")
wL1L1.factory("{0}[0,0.2]".format(massVar))
wL1L1.factory("uncVZ[-100,100]")
wL1L1.factory("uncP[0,10]")
wL1L1.factory("cut[0,1]")
wL1L1.defineSet("myVars","{0},uncVZ".format(massVar))

datasetL1L1 = RooDataSet("dataL1L1","dataL1L1",eventsL1L1,wL1L1.set("myVars"),"")

wL1L1.defineSet("obs_1dL1L1","uncVZ")
obsL1L1 = wL1L1.set("obs_1dL1L1")
uncVZL1L1 = wL1L1.var("uncVZ")
uncVZL1L1.setBins(200)

exppol1=TF1("exppol1","exp(pol1(0))",-5,100)

mass = 0.08
eps1 = -8
eps2 = -9
eps3 = -10

mresL1L1 = mresL1L1f.Eval(mass)

radfrac = radfracf.Eval(mass)
    
deltaM = 0.001
num_pairs = num_pairsf.Eval(mass)*scale_factor
num_rad = radfrac*num_pairs
ap_yield= 3*math.pi/(2*(1/137.0))*num_rad*(mass/deltaM)
print "{0} pairs, {1} radfrac, {2} rad, {3} A'".format(num_pairs,radfrac,num_rad,ap_yield)

dataInRangeL1L1 = datasetL1L1.reduce(obsL1L1,"abs({0}-{1})<{2}/2*{3}".format(massVar,mass,masscut_nsigma,mresL1L1))
    
zcutL1L1 = fzL1L1.Eval(mass)

nzbin = 50

hbar_c = 1.973e-13
ct = hbar_c*3.0/(mass*(1/137.036)*10**eps1)
gammact = hbar_c*3.0*2.3*gamma/(mass*mass*(1/137.036)*10**eps1)
       
nBins = 1000
effHistoL1L1_1 = TH1F("effHistoL1L1_1","effHistoL1L1_1",nBins,targetz,maxz)
exppol1.SetParameters(targetz/gammact-math.log(gammact),-1.0/gammact)
for i in range(nBins):
    vz = (maxz-targetz)/nBins * i + targetz
    effHistoL1L1_1.SetBinContent(i+1,Interpolate(mass,vz,mArrL1L1,zArrL1L1,effMatL1L1)*exppol1.Eval(vz))

sig_integralL1L1 = effHistoL1L1_1.Integral(effHistoL1L1_1.GetXaxis().FindBin(targetz),effHistoL1L1_1.GetXaxis().FindBin(maxz),"width")
cdfAtZcutL1L1 = effHistoL1L1_1.Integral(effHistoL1L1_1.GetXaxis().FindBin(zcutL1L1),effHistoL1L1_1.GetXaxis().FindBin(maxz),"width")

if (cdfAtZcutL1L1 == 0):
    cdfAtZcutL1L1 = 10**-20

for i in range(nzbin):
    z = zcutL1L1 + (maxz-zcutL1L1)/(nzbin) *i
    zArr.append(z)

    #dataPastCutL1L1 = dataInRangeL1L1.reduce(wL1L1.set("obs_1dL1L1"),"uncVZ>{0}".format(zcutL1L1))

    n_candidatesL1L1 = 1

    #dataArrayL1L1=numpy.zeros(dataPastCutL1L1.numEntries()+2)
    dataArrayL1L1_1=numpy.zeros(n_candidatesL1L1+2)
    dataArrayL1L1_1[0] = 0.0
    #for k in xrange(0,dataPastCutL1L1.numEntries()):
    for k in xrange(0,n_candidatesL1L1):
        #thisX = dataPastCutL1L1.get(k).getRealValue("uncVZ")
        thisX = z
        wL1L1.var("uncVZ").setVal(thisX)
        dataArrayL1L1_1[k+1]=(cdfAtZcutL1L1-effHistoL1L1_1.Integral(effHistoL1L1_1.GetXaxis().FindBin(thisX),effHistoL1L1_1.GetXaxis().FindBin(maxz),"width"))
    #dataArrayL1L1[dataPastCutL1L1.numEntries()+1] = cdfAtZcutL1L1
    dataArrayL1L1_1[n_candidatesL1L1+1] = cdfAtZcutL1L1

    dataArrayL1L1_1/= (cdfAtZcutL1L1)
    dataArrayL1L1_1.sort()
    outputL1L1 = upperlimit.upperlim(CL, 1, dataArrayL1L1_1, 0., dataArrayL1L1_1)
    if(i == 0):
        ouptutL1L1_0 = outputL1L1[0]
    outputArr1.append(outputL1L1[0]/ouptutL1L1_0)



ct = hbar_c*3.0/(mass*(1/137.036)*10**eps2)
gammact = hbar_c*3.0*2.3*gamma/(mass*mass*(1/137.036)*10**eps2)
       
nBins = 1000
effHistoL1L1_2 = TH1F("effHistoL1L1_2","effHistoL1L1_2",nBins,targetz,maxz)
exppol1.SetParameters(targetz/gammact-math.log(gammact),-1.0/gammact)
for i in range(nBins):
    vz = (maxz-targetz)/nBins * i + targetz
    effHistoL1L1_2.SetBinContent(i+1,Interpolate(mass,vz,mArrL1L1,zArrL1L1,effMatL1L1)*exppol1.Eval(vz))

sig_integralL1L1 = effHistoL1L1_2.Integral(effHistoL1L1_2.GetXaxis().FindBin(targetz),effHistoL1L1_2.GetXaxis().FindBin(maxz),"width")
cdfAtZcutL1L1 = effHistoL1L1_2.Integral(effHistoL1L1_2.GetXaxis().FindBin(zcutL1L1),effHistoL1L1_2.GetXaxis().FindBin(maxz),"width")

if (cdfAtZcutL1L1 == 0):
    cdfAtZcutL1L1 = 10**-20

for i in range(nzbin):
    z = zcutL1L1 + (maxz-zcutL1L1)/(nzbin) *i

    #dataPastCutL1L1 = dataInRangeL1L1.reduce(wL1L1.set("obs_1dL1L1"),"uncVZ>{0}".format(zcutL1L1))

    n_candidatesL1L1 = 1

    #dataArrayL1L1=numpy.zeros(dataPastCutL1L1.numEntries()+2)
    dataArrayL1L1_2=numpy.zeros(n_candidatesL1L1+2)
    dataArrayL1L1_2[0] = 0.0
    #for k in xrange(0,dataPastCutL1L1.numEntries()):
    for k in xrange(0,n_candidatesL1L1):
        #thisX = dataPastCutL1L1.get(k).getRealValue("uncVZ")
        thisX = z
        wL1L1.var("uncVZ").setVal(thisX)
        dataArrayL1L1_2[k+1]=(cdfAtZcutL1L1-effHistoL1L1_2.Integral(effHistoL1L1_2.GetXaxis().FindBin(thisX),effHistoL1L1_2.GetXaxis().FindBin(maxz),"width"))
    #dataArrayL1L1[dataPastCutL1L1.numEntries()+1] = cdfAtZcutL1L1
    dataArrayL1L1_2[n_candidatesL1L1+1] = cdfAtZcutL1L1

    dataArrayL1L1_2/= (cdfAtZcutL1L1)
    dataArrayL1L1_2.sort()
    outputL1L1 = upperlimit.upperlim(CL, 1, dataArrayL1L1_2, 0., dataArrayL1L1_2)
    if(i == 0):
        ouptutL1L1_0 = outputL1L1[0]
    outputArr2.append(outputL1L1[0]/ouptutL1L1_0)




ct = hbar_c*3.0/(mass*(1/137.036)*10**eps3)
gammact = hbar_c*3.0*2.3*gamma/(mass*mass*(1/137.036)*10**eps3)
       
nBins = 1000
effHistoL1L1_3 = TH1F("effHistoL1L1_3","effHistoL1L1_3",nBins,targetz,maxz)
exppol1.SetParameters(targetz/gammact-math.log(gammact),-1.0/gammact)
for i in range(nBins):
    vz = (maxz-targetz)/nBins * i + targetz
    effHistoL1L1_3.SetBinContent(i+1,Interpolate(mass,vz,mArrL1L1,zArrL1L1,effMatL1L1)*exppol1.Eval(vz))

sig_integralL1L1 = effHistoL1L1_3.Integral(effHistoL1L1_3.GetXaxis().FindBin(targetz),effHistoL1L1_3.GetXaxis().FindBin(maxz),"width")
cdfAtZcutL1L1 = effHistoL1L1_3.Integral(effHistoL1L1_3.GetXaxis().FindBin(zcutL1L1),effHistoL1L1_3.GetXaxis().FindBin(maxz),"width")

if (cdfAtZcutL1L1 == 0):
    cdfAtZcutL1L1 = 10**-20

for i in range(nzbin):
    z = zcutL1L1 + (maxz-zcutL1L1)/(nzbin) *i

    #dataPastCutL1L1 = dataInRangeL1L1.reduce(wL1L1.set("obs_1dL1L1"),"uncVZ>{0}".format(zcutL1L1))

    n_candidatesL1L1 = 1

    #dataArrayL1L1=numpy.zeros(dataPastCutL1L1.numEntries()+2)
    dataArrayL1L1_3=numpy.zeros(n_candidatesL1L1+2)
    dataArrayL1L1_3[0] = 0.0
    #for k in xrange(0,dataPastCutL1L1.numEntries()):
    for k in xrange(0,n_candidatesL1L1):
        #thisX = dataPastCutL1L1.get(k).getRealValue("uncVZ")
        thisX = z
        wL1L1.var("uncVZ").setVal(thisX)
        dataArrayL1L1_3[k+1]=(cdfAtZcutL1L1-effHistoL1L1_3.Integral(effHistoL1L1_3.GetXaxis().FindBin(thisX),effHistoL1L1_3.GetXaxis().FindBin(maxz),"width"))
    #dataArrayL1L1[dataPastCutL1L1.numEntries()+1] = cdfAtZcutL1L1
    dataArrayL1L1_3[n_candidatesL1L1+1] = cdfAtZcutL1L1

    dataArrayL1L1_3/= (cdfAtZcutL1L1)
    dataArrayL1L1_3.sort()
    outputL1L1 = upperlimit.upperlim(CL, 1, dataArrayL1L1_3, 0., dataArrayL1L1_3)
    if(i == 0):
        ouptutL1L1_0 = outputL1L1[0]
    outputArr3.append(outputL1L1[0]/ouptutL1L1_0)

graph1=TGraph(len(zArr),zArr,outputArr1)
graph2=TGraph(len(zArr),zArr,outputArr2)
graph3=TGraph(len(zArr),zArr,outputArr3)
graph1.SetTitle("OIM Relative Limit {0} MeV A' {1}".format(mass*1000,label))
graph1.GetXaxis().SetTitle("z [mm]")
graph1.GetYaxis().SetTitle("OIM relative limit")
maximum = max(outputArr1)
if(max(outputArr2) > maximum):
    maximum = max(outputArr2)
if(max(outputArr3) > maximum):
    maximum = max(outputArr3)
graph1.GetYaxis().SetRangeUser(0.9,1.1*maximum)
graph1.Draw("AL*")
graph2.SetLineColor(2)
graph2.SetMarkerColor(2)
graph2.Draw("L* same")
graph3.SetLineColor(4)
graph3.SetMarkerColor(4)
graph3.Draw("L* same")

legend = TLegend(.68,.66,.92,.87)
legend.SetBorderSize(0)
legend.SetFillColor(0)
legend.SetFillStyle(0)
legend.SetTextFont(42)
legend.SetTextSize(0.035)
legend.AddEntry(graph1,"#epsilon^{2} = 10^"+"{0:0.02f}".format(eps1),"LP")
legend.AddEntry(graph2,"#epsilon^{2} = 10^"+"{0:0.02f}".format(eps2),"LP")
legend.AddEntry(graph3,"#epsilon^{2} = 10^"+"{0:0.02f}".format(eps3),"LP")
legend.Draw("same")

c.Print(remainder[0]+".pdf[")

c.Print(remainder[0]+".pdf")

c.Print(remainder[0]+".pdf]")