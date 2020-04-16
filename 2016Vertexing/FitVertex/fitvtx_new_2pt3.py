#!/usr/bin/env python
import sys, array, math
import getopt
import upperlimit
import numpy
import EffFuncs
from EffFuncs import Interpolate, getMassArray, getZArray, getEfficiency
import ROOT
from ROOT import gROOT, TTree, TCanvas, TF1, TFile, gStyle, TFormula, TGraph, TGraphErrors, TH1D, TH1F, TCutG, TH2D, gDirectory, RooDataSet, RooRealVar, RooArgSet, RooFormulaVar, RooWorkspace, RooAbsData, RooFit, RooAbsReal, RooArgList, gPad, TFeldmanCousins, RooDataHist, RooHistPdf, TMath, TLatex, TPaveText, TLegend
from ROOT.RooStats import ModelConfig, ProfileLikelihoodCalculator, LikelihoodIntervalPlot

def print_usage():
    print "\nUsage: {0} <output basename> <input ROOT 2D histo file> <efficiency text file>".format(sys.argv[0])
    print "Arguments: "
    print '\t-n: ignore candidates past zcut (default false)'
    print '\t-t: do not use target position as function of mass (default true)'
    print '\t-u: use unbiased zcut (default false)'
    print '\t-z: target z (default -4.3 mm)'
    print '\t-s: scale factor (default 1)'
    print '\t-b: number of mass and epsilon bins (default 50)'
    print '\t-y: add title to plots'
    print '\t-h: this help message'
    print "\n"


no_candidates = False
scale_factor = 1
massVar = "uncM"
label = ""

#Model and Fit Ranges
n_massbins=50
minmass=0.051
maxmass=0.150
n_epsbins=50
mineps=-10.0
maxeps=-7.5
useVarTarget = True
useUnbiasedZcut = False
targetz = -4.3
maxz = 90 #max Z out to where we have acceptance
maxzL2L2 = 140 #max Z out to where we have acceptance for L2L2
zcut_count = 0.5

#Mass Resolution Parameters
masscut_nsigma = 2.80
masscut_eff = 0.93
#mres_p0_L1L1 = 1.364/1000.
#mres_p1_L1L1 = 0.02608

#mres_p0_L1L2 = 1.364/1000.
#mres_p1_L1L2 = 0.02608

#mres_p0_L2L2 = 1.364/1000.
#mres_p1_L2L2 = 0.02608

CL = 0.90
gamma = 0.95


options, remainder = getopt.gnu_getopt(sys.argv[1:], 'ntuz:s:y:b:h')
for opt, arg in options:
    if opt=='-n':
        no_candidates = True
    if opt=='-t':
        useVarTarget = False
    if opt=='-u':
        useUnbiasedZcut = True
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

def getUnbiasedZcut(mass,masswindow,zcuthisto,n_massbins,minmass,maxmass,outfile,canvas,plotlabel=""):
    histo = zcuthisto.Clone()
    for i in range(histo.GetNbinsX()):
        nbin = i + 1
        m = zcuthisto.GetBinCenter(nbin) 
        if(abs(mass - m) < masswindow):
            histo.SetBinError(nbin,0)
    fit = TF1("fit","pol5")
    histo.Fit('fit')
    zcutnew = fit.Eval(mass)
    histo.GetXaxis().SetTitle("mass (GeV)")
    histo.GetYaxis().SetTitle("zcut (mm)")
    histo.SetTitle("Unbiased Zcut = {0:0.1f} mm for Mass = {1:0.3f} GeV {2}".format(zcutnew,mass,plotlabel))
    histo.Draw()
    canvas.Print(outfile)
    del histo
    del fit
    return zcutnew

gROOT.SetBatch(True)
gStyle.SetOptFit(1)
gStyle.SetOptStat(0)
c = TCanvas("c","c",800,600);
c.Print(remainder[0]+".pdf[")
outfile = TFile(remainder[0]+".root","RECREATE")

inFileL1L1 = TFile(remainder[1])
inFileL1L2 = TFile(remainder[2])
inFileL2L2 = TFile(remainder[3])
effFileL1L1 = remainder[4]
effFileL1L2 = remainder[5]
effFileL2L2 = remainder[6]
eventsL1L1 = inFileL1L1.Get("ntuple")
eventsL1L2 = inFileL1L2.Get("ntuple")
eventsL2L2 = inFileL2L2.Get("ntuple")

if(useUnbiasedZcut):
    zcutfileL1L1 = TFile(remainder[7])
    histozcutL1L1 = zcutfileL1L1.Get("zcut")
    histozcutscaledL1L1 = zcutfileL1L1.Get("zcutscaled")

    zcutfileL1L2 = TFile(remainder[8])
    histozcutL1L2 = zcutfileL1L2.Get("zcut")
    histozcutscaledL1L2 = zcutfileL1L2.Get("zcutscaled")

    zcutfileL2L2 = TFile(remainder[9])
    histozcutL2L2 = zcutfileL2L2.Get("zcut")
    histozcutscaledL2L2 = zcutfileL2L2.Get("zcutscaled")

gStyle.SetOptStat(1111)

fzL1L1 = TF1("fzL1L1","{0}+{1}*x+{2}*x^2+{3}*x^3+{4}*x^4+{5}*x^5".format(21.61,-339.8,6319,-84860,556600,-1362000),0.05,0.175) #L1L1
#fzL1L1 = TF1("fz1","{0}+{1}*x+{2}*x^2+{3}*x^3".format(41.65,-466,2238,-3757),0.05,0.15) #L1L1
fzL1L2 = TF1("fzL1L2","{0}+{1}*x+{2}*x^2+{3}*x^3+{4}*x^4+{5}*x^5".format(-32.95,2706,-49020,366700,-1079000,592400),0.05,0.175) #L1L2
fzL2L2 = TF1("fzL1L2","{0}+{1}*x+{2}*x^2+{3}*x^3+{4}*x^4+{5}*x^5".format(-32.95,2706,-49020,366700,-1079000,592400),0.05,0.175) #L1L2 but L2L2 for now

#fz1 = TF1("fz1","41.65-466*x+2238*x^2-3757*x^3",0.05,0.15) #L1L1
#fz1 = TF1("fz1","33.8-361*x+1509*x^2-2041*x^3",0.05,0.15) #L1L1 10%
#fz1 = TF1("fz1","15.59-117.9*x-171.6*x^2+1887*x^3",0.05,0.15) #L1L1 10% with zcut = 100
#fz1 = TF1("fz1","17.94-148.8*x-39.36*x^2+1400*x^3",0.05,0.15) #L1L1 10% with zcut = 50
#fz1 = TF1("fz1","71.8-1130*x+9023*x^2-26830*x^3",0.05,0.15) #L1L2
#fz1 = TF1("fz1","58.33-876.9*x+6591*x^2-19110*x^3",0.05,0.15) #L1L2 10%
#fz1 = TF1("fz1","93.51-1447*x+10630*x^2-31440*x^3",0.05,0.15) #L2L2
#fz1 = TF1("fz1","70.76-945.6*x+5337*x^2-12440*x^3",0.05,0.15) #L2L2 10%

radfracf = TF1("radfracf","{0}+{1}*x+{2}*x^2+{3}*x^3+{4}*x^4+{5}*x^5".format(0.2018,-2.342,12.86,25.88,-405.8,898.6),0.04,0.2)
num_pairsf = TF1("num_pairsf","exp({0}+{1}*x+{2}*x^2+{3}*x^3+{4}*x^4+{5}*x^5)".format(4.903,208.3,-1880,-1868,68700,-198000),0.04,0.2)
#mresL1L1f = TF1("mresL1L1f","{0}+{1}*x+{2}*x^2+{3}*x^3+{4}*x^4+{5}*x^5".format(1.364/1000.,0.02608,0,0,0,0),0.04,0.2)
#mresL1L2f = TF1("mresL1L2f","{0}+{1}*x+{2}*x^2+{3}*x^3+{4}*x^4+{5}*x^5".format(1.364/1000.,0.02608,0,0,0,0),0.04,0.2)
#mresL2L2f = TF1("mresL2L2f","{0}+{1}*x+{2}*x^2+{3}*x^3+{4}*x^4+{5}*x^5".format(1.364/1000.,0.02608,0,0,0,0),0.04,0.2)
mresL1L1f = TF1("mresL1L1f","{0}+{1}*x+{2}*x^2+{3}*x^3+{4}*x^4+{5}*x^5".format(0.01095/1000.,0.04305,0,0,0,0),0.04,0.2)
mresL1L2f = TF1("mresL1L2f","{0}+{1}*x+{2}*x^2+{3}*x^3+{4}*x^4+{5}*x^5".format(0.04906/1000.,0.04606,0,0,0,0),0.04,0.2)
mresL2L2f = TF1("mresL2L2f","{0}+{1}*x+{2}*x^2+{3}*x^3+{4}*x^4+{5}*x^5".format(0.04906/1000.,0.04606,0,0,0,0),0.04,0.2)

targetzf = TF1("targetzf","{0}+{1}*x+{2}*x^2+{3}*x^3+{4}*x^4+{5}*x^5".format(-8.073,216.1,-4372,39880,-172500,288700),0.05,0.175)

zArrL1L1 = getZArray(effFileL1L1)
mArrL1L1 = getMassArray(effFileL1L1)
effMatL1L1 = getEfficiency(effFileL1L1)

zArrL1L2 = getZArray(effFileL1L2)
mArrL1L2 = getMassArray(effFileL1L2)
effMatL1L2 = getEfficiency(effFileL1L2)

zArrL2L2 = getZArray(effFileL2L2)
mArrL2L2 = getMassArray(effFileL2L2)
effMatL2L2 = getEfficiency(effFileL2L2)

xedges = array.array('d')
yedges = array.array('d')
for i in range(0,n_massbins+1):
    xedges.append((minmass+(i-0.5)*(maxmass-minmass)/(n_massbins-1))*1000)
for j in range(0,n_epsbins+1):
    yedges.append(10**(mineps+(j-0.5)*(maxeps-mineps)/(n_epsbins-1)))

outfile.cd()
massArr = array.array('d')
massArrMeV = array.array('d')
minMassArrL1L1 = array.array('d')
massWindowArrL1L1 = array.array('d')
minMassArrL1L2 = array.array('d')
massWindowArrL1L2 = array.array('d')
minMassArrL2L2 = array.array('d')
massWindowArrL2L2 = array.array('d')
zcutArrL1L1 = array.array('d')
zcutArrL1L2 = array.array('d')
zcutArrL2L2 = array.array('d')
zcutunbiasedArrL1L1 = array.array('d')
zcutunbiasedArrL1L2 = array.array('d')
zcutunbiasedArrL2L2 = array.array('d')
num_pairsArr = array.array('d')
targetzArr = array.array('d')
mResArrL1L1 = array.array('d')
mResArrL1L2 = array.array('d')
mResArrL2L2 = array.array('d')
radfracArr = array.array('d')
candArrL1L1 = array.array('d')
candArrL1L2 = array.array('d')
candArrL2L2 = array.array('d')
limitHistL1L1=TH2D("OIM Scaled Limit L1L1 {0}".format(label),"OIM Scaled Limit L1L1 {0}".format(label),n_massbins,xedges,n_epsbins,yedges)
limitHistL1L2=TH2D("OIM Scaled Limit L1L2 {0}".format(label),"OIM Scaled limit L1L2 {0}".format(label),n_massbins,xedges,n_epsbins,yedges)
limitHistL2L2=TH2D("OIM Scaled Limit L2L2 {0}".format(label),"OIM Scaled Limit L2L2 {0}".format(label),n_massbins,xedges,n_epsbins,yedges)
limitHistcombined=TH2D("OIM Scaled Limit L1L1 L1L2 Combined {0}".format(label),"OIM Scaled Limit L1L1 L1L2 Combined {0}".format(label),n_massbins,xedges,n_epsbins,yedges)
detectableHistL1L1=TH2D("Expected A' Rate L1L1 {0}".format(label),"Expected A' Rate L1L1 {0}".format(label),n_massbins,xedges,n_epsbins,yedges)
detectableHistL1L2=TH2D("Expected A' Rate L1L2 {0}".format(label),"Expected A' Rate L1L2 {0}".format(label),n_massbins,xedges,n_epsbins,yedges)
detectableHistL2L2=TH2D("Expected A' Rate L2L2 {0}".format(label),"Expected A' Rate L2L2 {0}".format(label),n_massbins,xedges,n_epsbins,yedges)
detectableHistcombined=TH2D("Expected A' Rate L1L1 + L1L2 {0}".format(label),"Expected A' Rate L1L1 + L1L2 {0}".format(label),n_massbins,xedges,n_epsbins,yedges)
gammactHist=TH2D("gammact {0}".format(label),"gammact {0}".format(label),n_massbins,xedges,n_epsbins,yedges)
allzHistL1L1=TH2D("detectable_allzL1L1 {0}".format(label),"detectable_allzL1L1 {0}".format(label),n_massbins,xedges,n_epsbins,yedges)
allzHistL1L2=TH2D("detectable_allzL1L2 {0}".format(label),"detectable_allzL1L2 {0}".format(label),n_massbins,xedges,n_epsbins,yedges)
allzHistL2L2=TH2D("detectable_allzL2L2 {0}".format(label),"detectable_allzL2L2 {0}".format(label),n_massbins,xedges,n_epsbins,yedges)
prodHist=TH2D("A's Produced within Prompt Acceptance {0}".format(label),"A's Produced within Prompt Acceptance {0}".format(label),n_massbins,xedges,n_epsbins,yedges)
candHistL1L1=TH1D("candidatesL1L1 {0}".format(label),"candidatesL1L1 {0}".format(label),n_massbins,xedges)
candHistL1L2=TH1D("candidatesL1L2 {0}".format(label),"candidatesL1L2 {0}".format(label),n_massbins,xedges)
candHistL2L2=TH1D("candidatesL2L2 {0}".format(label),"candidatesL2L2 {0}".format(label),n_massbins,xedges)
fcLowerHistL1L1=TH2D("fcLowerLimitL1L1 {0}".format(label),"fcLowerLimitL1L1 {0}".format(label),n_massbins,xedges,n_epsbins,yedges)
fcLowerHistL1L2=TH2D("fcLowerLimitL1L2 {0}".format(label),"fcLowerLimitL1L2 {0}".format(label),n_massbins,xedges,n_epsbins,yedges)
fcLowerHistL2L2=TH2D("fcLowerLimitL2L2 {0}".format(label),"fcLowerLimitL2L2 {0}".format(label),n_massbins,xedges,n_epsbins,yedges)
fcUpperHistL1L1=TH2D("fcUpperLimitL1L1 {0}".format(label),"fcUpperLimitL1L1 {0}".format(label),n_massbins,xedges,n_epsbins,yedges)
fcUpperHistL1L2=TH2D("fcUpperLimitL1L2 {0}".format(label),"fcUpperLimitL1L2 {0}".format(label),n_massbins,xedges,n_epsbins,yedges)
fcUpperHistL2L2=TH2D("fcUpperLimitL2L2 {0}".format(label),"fcUpperLimitL2L2 {0}".format(label),n_massbins,xedges,n_epsbins,yedges)

wL1L1 = RooWorkspace("wL1L1")
wL1L1.factory("{0}[0,0.2]".format(massVar))
wL1L1.factory("uncVZ[-100,100]")
wL1L1.factory("uncP[0,10]")
wL1L1.factory("cut[0,1]")
wL1L1.defineSet("myVars","{0},uncVZ".format(massVar))

wL1L2 = RooWorkspace("wL1L2")
wL1L2.factory("{0}[0,0.2]".format(massVar))
wL1L2.factory("uncVZ[-100,100]")
wL1L2.factory("uncP[0,10]")
wL1L2.factory("cut[0,1]")
wL1L2.defineSet("myVars","{0},uncVZ".format(massVar))

wL2L2 = RooWorkspace("wL2L2")
wL2L2.factory("{0}[0,0.2]".format(massVar))
wL2L2.factory("uncVZ[-100,100]")
wL2L2.factory("uncP[0,10]")
wL2L2.factory("cut[0,1]")
wL2L2.defineSet("myVars","{0},uncVZ".format(massVar))

datasetL1L1 = RooDataSet("dataL1L1","dataL1L1",eventsL1L1,wL1L1.set("myVars"),"")
datasetL1L2 = RooDataSet("dataL1L2","dataL1L2",eventsL1L2,wL1L2.set("myVars"),"")
datasetL2L2 = RooDataSet("dataL2L2","dataL2L2",eventsL2L2,wL2L2.set("myVars"),"")

wL1L1.defineSet("obs_1dL1L1","uncVZ")
obsL1L1 = wL1L1.set("obs_1dL1L1")
uncVZL1L1 = wL1L1.var("uncVZ")
uncVZL1L1.setBins(200)

wL1L2.defineSet("obs_1dL1L2","uncVZ")
obsL1L2 = wL1L2.set("obs_1dL1L2")
uncVZL1L2 = wL1L2.var("uncVZ")
uncVZL1L2.setBins(200)

wL2L2.defineSet("obs_1dL2L2","uncVZ")
obsL2L2 = wL2L2.set("obs_1dL2L2")
uncVZL2L2 = wL2L2.var("uncVZ")
uncVZL2L2.setBins(200)

exppol1=TF1("exppol1","exp(pol1(0))",-5,100)

fc = TFeldmanCousins()
fc.SetCL(CL)

if(useUnbiasedZcut):
    c.Print(remainder[0]+"_zcuttest.pdf[")

for i in range(0,n_massbins):
    mass = minmass+i*(maxmass-minmass)/(n_massbins-1)
    massArr.append(mass)
    massArrMeV.append(mass*1000)

    #mresL1L1 = mres_p0_L1L1 + mres_p1_L1L1*mass
    #mresL1L2 = mres_p0_L1L2 + mres_p1_L1L2*mass
    #mresL2L2 = mres_p0_L2L2 + mres_p1_L2L2*mass

    mresL1L1 = mresL1L1f.Eval(mass)
    mresL1L2 = mresL1L2f.Eval(mass)
    mresL2L2 = mresL2L2f.Eval(mass)

    radfrac = radfracf.Eval(mass)

    if(useVarTarget):
        targetz_truth = targetzf.Eval(mass)
    else:
        targetz_truth = targetz
    targetzArr.append(targetz_truth)

    massWindowArrL1L1.append(0.5*masscut_nsigma*mresL1L1)
    minMassArrL1L1.append(mass - 0.5*masscut_nsigma*mresL1L1)
    massWindowArrL1L2.append(0.5*masscut_nsigma*mresL1L2)
    minMassArrL1L2.append(mass - 0.5*masscut_nsigma*mresL1L2)
    massWindowArrL2L2.append(0.5*masscut_nsigma*mresL2L2)
    minMassArrL2L2.append(mass - 0.5*masscut_nsigma*mresL2L2)
    c.Clear()
    
    #deltaM = 0.001
    #eventsL1L1.Draw("{0}>>mass(100,{1}-{2},{1}+{2})".format(massVar,mass,0.5*deltaM),"abs({0}-{1})<{2}".format(massVar,mass,0.5*deltaM),"")
    #num_pairs = gDirectory.Get("mass").GetEntries()*scale_factor
    num_pairs = num_pairsf.Eval(mass)*scale_factor
    num_pairsArr.append(num_pairs)
    num_rad = radfrac*num_pairs
    ap_yield= 3*math.pi/(2*(1/137.0))*num_rad*(mass/deltaM)
    print "{0} pairs, {1} radfrac, {2} rad, {3} A'".format(num_pairs,radfrac,num_rad,ap_yield)

    dataInRangeL1L1 = datasetL1L1.reduce(obsL1L1,"abs({0}-{1})<{2}/2*{3}".format(massVar,mass,masscut_nsigma,mresL1L1))
    dataInRangeL1L2 = datasetL1L2.reduce(obsL1L2,"abs({0}-{1})<{2}/2*{3}".format(massVar,mass,masscut_nsigma,mresL1L2))
    dataInRangeL2L2 = datasetL2L2.reduce(obsL2L2,"abs({0}-{1})<{2}/2*{3}".format(massVar,mass,masscut_nsigma,mresL2L2))
    
    zcutL1L1 = fzL1L1.Eval(mass)
    zcutL1L2 = fzL1L2.Eval(mass)
    zcutL2L2 = fzL2L2.Eval(mass)
    zcutArrL1L1.append(zcutL1L1)
    zcutArrL1L2.append(zcutL1L2)
    zcutArrL2L2.append(zcutL2L2)
    if(useUnbiasedZcut):
        if(scale_factor == 1):
            zcutL1L1 = getUnbiasedZcut(mass,mresL1L1/2*masscut_nsigma,histozcutL1L1,n_massbins,minmass,maxmass,remainder[0]+"_zcuttest.pdf[",c,label)
            zcutL1L2 = getUnbiasedZcut(mass,mresL1L2/2*masscut_nsigma,histozcutL1L2,n_massbins,minmass,maxmass,remainder[0]+"_zcuttest.pdf[",c,label)
            zcutL2L2 = getUnbiasedZcut(mass,mresL2L2/2*masscut_nsigma,histozcutL2L2,n_massbins,minmass,maxmass,remainder[0]+"_zcuttest.pdf[",c,label)
        else:
            zcutL1L1 = getUnbiasedZcut(mass,mresL1L1/2*masscut_nsigma,histozcutscaledL1L1,n_massbins,minmass,maxmass,remainder[0]+"_zcuttest.pdf[",c,label)
            zcutL1L2 = getUnbiasedZcut(mass,mresL1L2/2*masscut_nsigma,histozcutscaledL1L2,n_massbins,minmass,maxmass,remainder[0]+"_zcuttest.pdf[",c,label)
            zcutL2L2 = getUnbiasedZcut(mass,mresL2L2/2*masscut_nsigma,histozcutscaledL2L2,n_massbins,minmass,maxmass,remainder[0]+"_zcuttest.pdf[",c,label)
    zcutunbiasedArrL1L1.append(zcutL1L1)
    zcutunbiasedArrL1L2.append(zcutL1L2)
    zcutunbiasedArrL2L2.append(zcutL2L2)
    print "L1L1: zcut {0}  L1L2: zcut {1}  L2L2: zcut {2}".format(zcutL1L1,zcutL1L2,zcutL2L2)
    dataPastCutL1L1 = dataInRangeL1L1.reduce(wL1L1.set("obs_1dL1L1"),"uncVZ>{0}".format(zcutL1L1))
    dataPastCutL1L2 = dataInRangeL1L2.reduce(wL1L2.set("obs_1dL1L2"),"uncVZ>{0}".format(zcutL1L2))
    dataPastCutL2L2 = dataInRangeL2L2.reduce(wL2L2.set("obs_1dL2L2"),"uncVZ>{0}".format(zcutL2L2))
    
    mResArrL1L1.append(mresL1L1)
    mResArrL1L2.append(mresL1L2)
    mResArrL2L2.append(mresL2L2)
    radfracArr.append(radfrac)

    n_candidatesL1L1 = dataPastCutL1L1.numEntries()
    n_candidatesL1L2 = dataPastCutL1L2.numEntries()
    n_candidatesL2L2 = dataPastCutL2L2.numEntries()
    if (no_candidates):
        n_candidatesL1L1 = 0
        n_candidatesL1L2 = 0
        n_candidatesL2L2 = 0
    print ("Number of Candidates L1L1: {0}  L1L2: {1}  L2L2: {2}".format(n_candidatesL1L1,n_candidatesL1L2,n_candidatesL2L2))
    for k in range(0,n_candidatesL1L1):
        candHistL1L1.Fill(mass)
    for k in range(0,n_candidatesL1L2):
        candHistL1L2.Fill(mass)
    for k in range(0,n_candidatesL2L2):
        candHistL2L2.Fill(mass)
    candArrL1L1.append(n_candidatesL1L1)
    candArrL1L2.append(n_candidatesL1L2)
    candArrL2L2.append(n_candidatesL2L2)
    fcLowerL1L1 = fc.CalculateLowerLimit(n_candidatesL1L1,zcut_count)
    fcUpperL1L1 = fc.CalculateUpperLimit(n_candidatesL1L1,zcut_count)
    fcLowerL1L2 = fc.CalculateLowerLimit(n_candidatesL1L2,zcut_count)
    fcUpperL1L2 = fc.CalculateUpperLimit(n_candidatesL1L2,zcut_count)
    fcLowerL2L2 = fc.CalculateLowerLimit(n_candidatesL2L2,zcut_count)
    fcUpperL2L2 = fc.CalculateUpperLimit(n_candidatesL2L2,zcut_count)

    for j in range(0,n_epsbins):
        c.Clear()
        eps = mineps+j*(maxeps-mineps)/(n_epsbins-1)
        hbar_c = 1.973e-13
        ct = hbar_c*3.0/(mass*(1/137.036)*10**eps)
        gammact = hbar_c*3.0*2.3*gamma/(mass*mass*(1/137.036)*10**eps)
       
        nBins = 1000
        effHistoL1L1 = TH1F("effHistoL1L1","effHistoL1L1",nBins,targetz,maxz)
        effHistoL1L2 = TH1F("effHistoL1L2","effHistoL1L2",nBins,targetz,maxz)
        effHistoL2L2 = TH1F("effHistoL2L2","effHistoL2L2",nBins,targetz,maxzL2L2)
        exppol1.SetParameters(targetz_truth/gammact-math.log(gammact),-1.0/gammact)
        for i in range(nBins):
            vz = (maxz-targetz)/nBins * i + targetz
            effHistoL1L1.SetBinContent(i+1,Interpolate(mass,vz,mArrL1L1,zArrL1L1,effMatL1L1)*exppol1.Eval(vz))
            effHistoL1L2.SetBinContent(i+1,Interpolate(mass,vz,mArrL1L2,zArrL1L2,effMatL1L2)*exppol1.Eval(vz))

        for i in range(nBins):
            vz = (maxzL2L2-targetz)/nBins * i + targetz
            effHistoL2L2.SetBinContent(i+1,Interpolate(mass,vz,mArrL2L2,zArrL2L2,effMatL2L2)*exppol1.Eval(vz))

        sig_integralL1L1 = effHistoL1L1.Integral(effHistoL1L1.GetXaxis().FindBin(targetz),effHistoL1L1.GetXaxis().FindBin(maxz),"width")
        sig_integralL1L2 = effHistoL1L2.Integral(effHistoL1L2.GetXaxis().FindBin(targetz),effHistoL1L2.GetXaxis().FindBin(maxz),"width")
        sig_integralL2L2 = effHistoL2L2.Integral(effHistoL2L2.GetXaxis().FindBin(targetz),effHistoL2L2.GetXaxis().FindBin(maxzL2L2),"width")

        cdfAtZcutL1L1 = effHistoL1L1.Integral(effHistoL1L1.GetXaxis().FindBin(zcutL1L1),effHistoL1L1.GetXaxis().FindBin(maxz),"width")
        cdfAtZcutL1L2 = effHistoL1L2.Integral(effHistoL1L2.GetXaxis().FindBin(zcutL1L2),effHistoL1L2.GetXaxis().FindBin(maxz),"width")
        cdfAtZcutL2L2 = effHistoL2L2.Integral(effHistoL2L2.GetXaxis().FindBin(zcutL2L2),effHistoL2L2.GetXaxis().FindBin(maxzL2L2),"width")

        if (cdfAtZcutL1L1 == 0):
            cdfAtZcutL1L1 = 10**-20
        if (cdfAtZcutL1L2 == 0):
            cdfAtZcutL1L2 = 10**-20
        if (cdfAtZcutL2L2 == 0):
            cdfAtZcutL2L2 = 10**-20

        if (no_candidates):
            dataArrayL1L1=numpy.zeros(2)
            dataArrayL1L1[1] = cdfAtZcutL1L1
            dataArrayL1L2=numpy.zeros(2)
            dataArrayL1L2[1] = cdfAtZcutL1L2
            dataArrayL2L2=numpy.zeros(2)
            dataArrayL2L2[1] = cdfAtZcutL2L2
        else:
            dataArrayL1L1=numpy.zeros(dataPastCutL1L1.numEntries()+2)
            dataArrayL1L1[0] = 0.0
            dataArrayL1L2=numpy.zeros(dataPastCutL1L2.numEntries()+2)
            dataArrayL1L2[0] = 0.0
            dataArrayL2L2=numpy.zeros(dataPastCutL2L2.numEntries()+2)
            dataArrayL2L2[0] = 0.0
            for k in xrange(0,dataPastCutL1L1.numEntries()):
                thisX = dataPastCutL1L1.get(k).getRealValue("uncVZ")
                wL1L1.var("uncVZ").setVal(thisX)
                dataArrayL1L1[k+1]=(cdfAtZcutL1L1-effHistoL1L1.Integral(effHistoL1L1.GetXaxis().FindBin(thisX),effHistoL1L1.GetXaxis().FindBin(maxz),"width"))
            dataArrayL1L1[dataPastCutL1L1.numEntries()+1] = cdfAtZcutL1L1
            for k in xrange(0,dataPastCutL1L2.numEntries()):
                thisX = dataPastCutL1L2.get(k).getRealValue("uncVZ")
                wL1L2.var("uncVZ").setVal(thisX)
                dataArrayL1L2[k+1]=(cdfAtZcutL1L2-effHistoL1L2.Integral(effHistoL1L2.GetXaxis().FindBin(thisX),effHistoL1L2.GetXaxis().FindBin(maxz),"width"))
            dataArrayL1L2[dataPastCutL1L2.numEntries()+1] = cdfAtZcutL1L2
            for k in xrange(0,dataPastCutL2L2.numEntries()):
                thisX = dataPastCutL2L2.get(k).getRealValue("uncVZ")
                wL2L2.var("uncVZ").setVal(thisX)
                dataArrayL2L2[k+1]=(cdfAtZcutL2L2-effHistoL2L2.Integral(effHistoL2L2.GetXaxis().FindBin(thisX),effHistoL2L2.GetXaxis().FindBin(maxzL2L2),"width"))
            dataArrayL2L2[dataPastCutL2L2.numEntries()+1] = cdfAtZcutL2L2

        dataArrayL1L1/= (cdfAtZcutL1L1)
        dataArrayL1L1.sort()
        dataArrayL1L2/= (cdfAtZcutL1L2)
        dataArrayL1L2.sort()
        dataArrayL2L2/= (cdfAtZcutL2L2)
        dataArrayL2L2.sort()
        outputL1L1 = upperlimit.upperlim(CL, 1, dataArrayL1L1, 0., dataArrayL1L1)
        outputL1L2 = upperlimit.upperlim(CL, 1, dataArrayL1L2, 0., dataArrayL1L2)
        outputL2L2 = upperlimit.upperlim(CL, 1, dataArrayL2L2, 0., dataArrayL2L2)
        for i in range(len(outputL1L1)):
            print("Output L1L1 {0}: {1}".format(i,outputL1L1[i]))
        for i in range(len(outputL1L2)):
            print("Output L1L2 {0}: {1}".format(i,outputL1L2[i]))
        for i in range(len(outputL2L2)):
            print("Output L2L2 {0}: {1}".format(i,outputL2L2[i]))

        prodHist.Fill(mass*1000,10**eps,ap_yield*10**eps)
        allzHistL1L1.Fill(mass*1000,10**eps,ap_yield*10**eps*sig_integralL1L1)
        detectableHistL1L1.Fill(mass*1000,10**eps,ap_yield*10**eps*cdfAtZcutL1L1)
        gammactHist.Fill(mass*1000,10**eps,gammact)
        limit_detectableL1L1 = outputL1L1[0] # this is a limit on number of detectable A' (past zcut, within mass cut)
        limit_allzL1L1 = limit_detectableL1L1/((cdfAtZcutL1L1/sig_integralL1L1)*masscut_eff) # this is a limit on number of detectable A' if we didn't have zcut or mass cut
        limit_productionL1L1 = limit_allzL1L1/sig_integralL1L1 # limit on number of produced A'
        limit_epsL1L1 = limit_productionL1L1/ap_yield
        limit_scaledL1L1 = limit_epsL1L1/10**eps
        print "{0} {1} {2} {3} {4}".format(limit_detectableL1L1,limit_allzL1L1,limit_productionL1L1,limit_epsL1L1,limit_scaledL1L1)
        limitHistL1L1.Fill(mass*1000,10**eps,limit_scaledL1L1)
        fcLowerHistL1L1.Fill(mass*1000,10**eps,fcLowerL1L1/cdfAtZcutL1L1/masscut_eff/ap_yield/10**eps)
        fcUpperHistL1L1.Fill(mass*1000,10**eps,fcUpperL1L1/cdfAtZcutL1L1/masscut_eff/ap_yield/10**eps)
        del effHistoL1L1

        allzHistL1L2.Fill(mass*1000,10**eps,ap_yield*10**eps*sig_integralL1L2)
        detectableHistL1L2.Fill(mass*1000,10**eps,ap_yield*10**eps*cdfAtZcutL1L2)
        limit_detectableL1L2 = outputL1L2[0] # this is a limit on number of detectable A' (past zcut, within mass cut)
        limit_allzL1L2 = limit_detectableL1L2/((cdfAtZcutL1L2/sig_integralL1L2)*masscut_eff) # this is a limit on number of detectable A' if we didn't have zcut or mass cut
        limit_productionL1L2 = limit_allzL1L2/sig_integralL1L2 # limit on number of produced A'
        limit_epsL1L2 = limit_productionL1L2/ap_yield
        limit_scaledL1L2 = limit_epsL1L2/10**eps
        print "{0} {1} {2} {3} {4}".format(limit_detectableL1L2,limit_allzL1L2,limit_productionL1L2,limit_epsL1L2,limit_scaledL1L2)
        limitHistL1L2.Fill(mass*1000,10**eps,limit_scaledL1L2)
        fcLowerHistL1L2.Fill(mass*1000,10**eps,fcLowerL1L2/cdfAtZcutL1L2/masscut_eff/ap_yield/10**eps)
        fcUpperHistL1L2.Fill(mass*1000,10**eps,fcUpperL1L2/cdfAtZcutL1L2/masscut_eff/ap_yield/10**eps)
        del effHistoL1L2

        allzHistL2L2.Fill(mass*1000,10**eps,ap_yield*10**eps*sig_integralL2L2)
        detectableHistL2L2.Fill(mass*1000,10**eps,ap_yield*10**eps*cdfAtZcutL2L2)
        limit_detectableL2L2 = outputL2L2[0] # this is a limit on number of detectable A' (past zcut, within mass cut)
        limit_allzL2L2 = limit_detectableL2L2/((cdfAtZcutL2L2/sig_integralL2L2)*masscut_eff) # this is a limit on number of detectable A' if we didn't have zcut or mass cut
        limit_productionL2L2 = limit_allzL2L2/sig_integralL2L2 # limit on number of produced A'
        limit_epsL2L2 = limit_productionL2L2/ap_yield
        limit_scaledL2L2 = limit_epsL2L2/10**eps
        print "{0} {1} {2} {3} {4}".format(limit_detectableL2L2,limit_allzL2L2,limit_productionL2L2,limit_epsL2L2,limit_scaledL2L2)
        limitHistL2L2.Fill(mass*1000,10**eps,limit_scaledL2L2)
        fcLowerHistL2L2.Fill(mass*1000,10**eps,fcLowerL2L2/cdfAtZcutL2L2/masscut_eff/ap_yield/10**eps)
        fcUpperHistL2L2.Fill(mass*1000,10**eps,fcUpperL2L2/cdfAtZcutL2L2/masscut_eff/ap_yield/10**eps)
        del effHistoL2L2

if(useUnbiasedZcut):
    c.Print(remainder[0]+"_zcuttest.pdf]")
poiMassArrL1L1 = array.array('d')
poiPvalArrL1L1 = array.array('d')
poiSigArrL1L1 = array.array('d')
poiBkgArrL1L1 = array.array('d')

c.SetLogy(0)
for i in xrange(0,len(massArr)):
    mass = massArr[i]
    sigMassArr = array.array('d')
    sigCandArr = array.array('d')
    hasLowSide = False
    hasHighSide = False
    for j in xrange(0,len(massArr)):
        if abs(mass-massArr[j])>massWindowArrL1L1[i]+massWindowArrL1L1[j]:
            if j<i:
                hasLowSide = True
            if i<j:
                hasHighSide = True
            sigMassArr.append(massArrMeV[j])
            sigCandArr.append(candArrL1L1[j])
    if (hasLowSide and hasHighSide):

        graph=TGraph(len(sigMassArr),sigMassArr,sigCandArr)
        graph.SetTitle("background L1L1")
        graph.Draw("A*")
        graph.Fit("pol2")
        graph.GetXaxis().SetMoreLogLabels()
        c.Print(remainder[0]+".pdf","Title:test")
        nbkg = graph.GetFunction("pol2").Eval(mass)
        if nbkg<0.5:
            nbkg = 0.5
        poiBkgArrL1L1.append(nbkg)
        pval = 1.0-TMath.Prob(2*nbkg,2*int(candArrL1L1[i]))
        zscore = TMath.NormQuantile(1.0-pval)
        poiMassArrL1L1.append(mass*1000)
        poiPvalArrL1L1.append(pval)
        poiSigArrL1L1.append(zscore)

poiMassArrL1L2 = array.array('d')
poiPvalArrL1L2 = array.array('d')
poiSigArrL1L2 = array.array('d')
poiBkgArrL1L2 = array.array('d')

c.Clear()

c.SetLogy(0)
for i in xrange(0,len(massArr)):
    mass = massArr[i]
    sigMassArr = array.array('d')
    sigCandArr = array.array('d')
    hasLowSide = False
    hasHighSide = False
    for j in xrange(0,len(massArr)):
        if abs(mass-massArr[j])>massWindowArrL1L2[i]+massWindowArrL1L2[j]:
            if j<i:
                hasLowSide = True
            if i<j:
                hasHighSide = True
            sigMassArr.append(massArrMeV[j])
            sigCandArr.append(candArrL1L2[j])
    if (hasLowSide and hasHighSide):

        graph=TGraph(len(sigMassArr),sigMassArr,sigCandArr)
        graph.SetTitle("background L1L2")
        graph.Draw("A*")
        graph.Fit("pol2")
        graph.GetXaxis().SetMoreLogLabels()
        c.Print(remainder[0]+".pdf","Title:test")
        nbkg = graph.GetFunction("pol2").Eval(mass)
        if nbkg<0.5:
            nbkg = 0.5
        poiBkgArrL1L2.append(nbkg)
        pval = 1.0-TMath.Prob(2*nbkg,2*int(candArrL1L2[i]))
        zscore = TMath.NormQuantile(1.0-pval)
        poiMassArrL1L2.append(mass*1000)
        poiPvalArrL1L2.append(pval)
        poiSigArrL1L2.append(zscore)

poiMassArrL2L2 = array.array('d')
poiPvalArrL2L2 = array.array('d')
poiSigArrL2L2 = array.array('d')
poiBkgArrL2L2 = array.array('d')

c.Clear()

c.SetLogy(0)
for i in xrange(0,len(massArr)):
    mass = massArr[i]
    sigMassArr = array.array('d')
    sigCandArr = array.array('d')
    hasLowSide = False
    hasHighSide = False
    for j in xrange(0,len(massArr)):
        if abs(mass-massArr[j])>massWindowArrL2L2[i]+massWindowArrL2L2[j]:
            if j<i:
                hasLowSide = True
            if i<j:
                hasHighSide = True
            sigMassArr.append(massArrMeV[j])
            sigCandArr.append(candArrL2L2[j])
    if (hasLowSide and hasHighSide):

        graph=TGraph(len(sigMassArr),sigMassArr,sigCandArr)
        graph.SetTitle("background L2L2")
        graph.Draw("A*")
        graph.Fit("pol2")
        graph.GetXaxis().SetMoreLogLabels()
        c.Print(remainder[0]+".pdf","Title:test")
        nbkg = graph.GetFunction("pol2").Eval(mass)
        if nbkg<0.5:
            nbkg = 0.5
        poiBkgArrL2L2.append(nbkg)
        pval = 1.0-TMath.Prob(2*nbkg,2*int(candArrL2L2[i]))
        zscore = TMath.NormQuantile(1.0-pval)
        poiMassArrL2L2.append(mass*1000)
        poiPvalArrL2L2.append(pval)
        poiSigArrL2L2.append(zscore)

c.Clear()

c.Print(remainder[0]+".pdf]")

c.Print(remainder[0]+"_output.pdf[")
gStyle.SetOptStat(0)
c.SetLogy(0)

def drawGraph(xdata,ydata,title,drawopt):
    graph=TGraph(len(xdata),xdata,ydata)
    graph.SetTitle(title)
    graph.Draw(drawopt)
    graph.GetXaxis().SetMoreLogLabels()
    graph.GetXaxis().SetTitle("mass [MeV]")
    return graph

def drawGraph2(xdata,ydata,ydata2,title,c):
    graph=TGraph(len(xdata),xdata,ydata)
    graph2=TGraph(len(xdata),xdata,ydata2)
    graph.SetTitle(title)
    graph.GetXaxis().SetMoreLogLabels()
    graph.GetXaxis().SetTitle("mass [MeV]")
    graph.GetYaxis().SetTitle("zcut [mm]")
    graph.GetYaxis().SetRangeUser(-4.3,50)
    graph.Draw("AL*")
    graph2.SetLineColor(2)
    graph2.SetMarkerColor(2)
    graph2.Draw("L* same")
    legend = TLegend(.68,.66,.92,.87)
    legend.SetBorderSize(0)
    legend.SetFillColor(0)
    legend.SetFillStyle(0)
    legend.SetTextFont(42)
    legend.SetTextSize(0.035)
    legend.AddEntry(graph,"Biased","LP")
    legend.AddEntry(graph2,"Unbiased","LP")
    legend.Draw("same")
    c.Print(remainder[0]+"_output.pdf","Title:test")
    c.Write()

c.SetLogx(1)
graph = drawGraph(massArrMeV,targetzArr,"target","AL*")
graph.GetXaxis().SetTitle("mass [MeV]")
graph.GetYaxis().SetTitle("Target Z [mm]")

c.Print(remainder[0]+"_output.pdf","Title:test")
c.Write()

drawGraph2(massArrMeV,zcutArrL1L1,zcutunbiasedArrL1L1,"zcut L1L1 {0}".format(label),c)

drawGraph2(massArrMeV,zcutArrL1L2,zcutunbiasedArrL1L2,"zcut L1L2 {0}".format(label),c)

drawGraph2(massArrMeV,zcutArrL2L2,zcutunbiasedArrL2L2,"zcut L2L2 {0}".format(label),c)

graph = drawGraph(massArrMeV,mResArrL1L1,"mres L1L1","AL*")
graph.GetXaxis().SetTitle("mass [MeV]")
graph.GetYaxis().SetTitle("Mass Resolution [GeV]")
c.Print(remainder[0]+"_output.pdf","Title:test")
c.Write()

graph = drawGraph(massArrMeV,mResArrL1L2,"mresL1L2","AL*")
graph.GetXaxis().SetTitle("mass [MeV]")
graph.GetYaxis().SetTitle("Mass Resolution [GeV]")
c.Print(remainder[0]+"_output.pdf","Title:test")
c.Write()

graph = drawGraph(massArrMeV,mResArrL2L2,"mresL2L2","AL*")
graph.GetXaxis().SetTitle("mass [MeV]")
graph.GetYaxis().SetTitle("Mass Resolution [GeV]")
c.Print(remainder[0]+"_output.pdf","Title:test")
c.Write()

graph = drawGraph(massArrMeV,radfracArr,"radfrac","AL*")
graph.GetXaxis().SetTitle("mass [MeV]")
graph.GetYaxis().SetTitle("Radiative Fraction")
c.Print(remainder[0]+"_output.pdf","Title:test")
c.Write()

graph = drawGraph(massArrMeV,num_pairsArr,"numPairs","AL*")
graph.GetXaxis().SetTitle("mass [MeV]")
graph.GetYaxis().SetTitle("Number of e+e- Pairs")
c.Print(remainder[0]+"_output.pdf","Title:test")
c.Write()


zcutMassArrL1L1 = minMassArrL1L1[:]
zcutZcutArrL1L1 = zcutArrL1L1[:]
zcutMassArrL1L1.append(0.2)
zcutZcutArrL1L1.append(zcutArrL1L1[-1])
zcutMassArrL1L1.append(0.2)
zcutZcutArrL1L1.append(100)
zcutMassArrL1L1.append(0)
zcutZcutArrL1L1.append(100)
zcutMassArrL1L1.append(0)
zcutZcutArrL1L1.append(zcutArrL1L1[0])
zcutMassArrL1L1.append(minMassArrL1L1[0])
zcutZcutArrL1L1.append(zcutArrL1L1[0])
zcutTcutL1L1=TCutG("highzcut",len(zcutMassArrL1L1),zcutMassArrL1L1,zcutZcutArrL1L1)
zcutTcutL1L1.SetVarX(massVar)
zcutTcutL1L1.SetVarY("uncVZ")

c.SetLogx(0)
eventsL1L1.Draw("uncVZ:{0}>>hnew(100,0,0.2,100,-60,60)".format(massVar),"highzcut","colz")
gDirectory.Get("hnew").SetTitle("")
zcutTcutL1L1.Draw("L")
c.Print(remainder[0]+"_output.pdf","Title:test")
eventsL1L1.Draw("{0}>>hnew(100,0,0.2)".format(massVar),"highzcut","colz")
c.Print(remainder[0]+"_output.pdf","Title:test")
c.SetLogx(1)

zcutZcutunbiasedArrL1L1 = zcutunbiasedArrL1L1[:]
zcutZcutunbiasedArrL1L1.append(zcutunbiasedArrL1L1[-1])
zcutZcutunbiasedArrL1L1.append(100)
zcutZcutunbiasedArrL1L1.append(100)
zcutZcutunbiasedArrL1L1.append(zcutunbiasedArrL1L1[0])
zcutZcutunbiasedArrL1L1.append(zcutunbiasedArrL1L1[0])
zcutunbiasedTcutL1L1=TCutG("highzcutunbiased",len(zcutMassArrL1L1),zcutMassArrL1L1,zcutZcutunbiasedArrL1L1)
zcutunbiasedTcutL1L1.SetVarX(massVar)
zcutunbiasedTcutL1L1.SetVarY("uncVZ")

c.SetLogx(0)
eventsL1L1.Draw("uncVZ:{0}>>hnew(100,0,0.2,100,-60,60)".format(massVar),"highzcutunbiased","colz")
gDirectory.Get("hnew").SetTitle("")
zcutunbiasedTcutL1L1.Draw("L")
c.Print(remainder[0]+"_output.pdf","Title:test")
eventsL1L1.Draw("{0}>>hnew(100,0,0.2)".format(massVar),"highzcutunbiased","colz")
c.Print(remainder[0]+"_output.pdf","Title:test")
c.SetLogx(1)

zcutMassArrL1L2 = minMassArrL1L2[:]
zcutZcutArrL1L2 = zcutArrL1L2[:]
zcutMassArrL1L2.append(0.2)
zcutZcutArrL1L2.append(zcutArrL1L2[-1])
zcutMassArrL1L2.append(0.2)
zcutZcutArrL1L2.append(100)
zcutMassArrL1L2.append(0)
zcutZcutArrL1L2.append(100)
zcutMassArrL1L2.append(0)
zcutZcutArrL1L2.append(zcutArrL1L2[0])
zcutMassArrL1L2.append(minMassArrL1L2[0])
zcutZcutArrL1L2.append(zcutArrL1L2[0])
zcutTcutL1L2=TCutG("highzcut",len(zcutMassArrL1L2),zcutMassArrL1L2,zcutZcutArrL1L2)
zcutTcutL1L2.SetVarX(massVar)
zcutTcutL1L2.SetVarY("uncVZ")

c.SetLogx(0)
eventsL1L2.Draw("uncVZ:{0}>>hnew(100,0,0.2,100,-60,60)".format(massVar),"highzcut","colz")
gDirectory.Get("hnew").SetTitle("")
zcutTcutL1L2.Draw("L")
c.Print(remainder[0]+"_output.pdf","Title:test")
eventsL1L2.Draw("{0}>>hnew(100,0,0.2)".format(massVar),"highzcut","colz")
c.Print(remainder[0]+"_output.pdf","Title:test")
c.SetLogx(1)

zcutZcutunbiasedArrL1L2 = zcutunbiasedArrL1L2[:]
zcutZcutunbiasedArrL1L2.append(zcutunbiasedArrL1L2[-1])
zcutZcutunbiasedArrL1L2.append(100)
zcutZcutunbiasedArrL1L2.append(100)
zcutZcutunbiasedArrL1L2.append(zcutunbiasedArrL1L2[0])
zcutZcutunbiasedArrL1L2.append(zcutunbiasedArrL1L2[0])
zcutunbiasedTcutL1L2=TCutG("highzcutunbiased",len(zcutMassArrL1L2),zcutMassArrL1L2,zcutZcutunbiasedArrL1L2)
zcutunbiasedTcutL1L2.SetVarX(massVar)
zcutunbiasedTcutL1L2.SetVarY("uncVZ")

c.SetLogx(0)
eventsL1L2.Draw("uncVZ:{0}>>hnew(100,0,0.2,100,-60,60)".format(massVar),"highzcutunbiased","colz")
gDirectory.Get("hnew").SetTitle("")
zcutunbiasedTcutL1L2.Draw("L")
c.Print(remainder[0]+"_output.pdf","Title:test")
eventsL1L2.Draw("{0}>>hnew(100,0,0.2)".format(massVar),"highzcutunbiased","colz")
c.Print(remainder[0]+"_output.pdf","Title:test")
c.SetLogx(1)

zcutMassArrL2L2 = minMassArrL2L2[:]
zcutZcutArrL2L2 = zcutArrL2L2[:]
zcutMassArrL2L2.append(0.2)
zcutZcutArrL2L2.append(zcutArrL2L2[-1])
zcutMassArrL2L2.append(0.2)
zcutZcutArrL2L2.append(100)
zcutMassArrL2L2.append(0)
zcutZcutArrL2L2.append(100)
zcutMassArrL2L2.append(0)
zcutZcutArrL2L2.append(zcutArrL2L2[0])
zcutMassArrL2L2.append(minMassArrL2L2[0])
zcutZcutArrL2L2.append(zcutArrL2L2[0])
zcutTcutL2L2=TCutG("highzcut",len(zcutMassArrL2L2),zcutMassArrL2L2,zcutZcutArrL2L2)
zcutTcutL2L2.SetVarX(massVar)
zcutTcutL2L2.SetVarY("uncVZ")

c.SetLogx(0)
eventsL2L2.Draw("uncVZ:{0}>>hnew(100,0,0.2,100,-60,60)".format(massVar),"highzcut","colz")
gDirectory.Get("hnew").SetTitle("")
zcutTcutL2L2.Draw("L")
c.Print(remainder[0]+"_output.pdf","Title:test")
eventsL2L2.Draw("{0}>>hnew(100,0,0.2)".format(massVar),"highzcut","colz")
c.Print(remainder[0]+"_output.pdf","Title:test")
c.SetLogx(1)

zcutZcutunbiasedArrL2L2 = zcutunbiasedArrL2L2[:]
zcutZcutunbiasedArrL2L2.append(zcutunbiasedArrL2L2[-1])
zcutZcutunbiasedArrL2L2.append(100)
zcutZcutunbiasedArrL2L2.append(100)
zcutZcutunbiasedArrL2L2.append(zcutunbiasedArrL2L2[0])
zcutZcutunbiasedArrL2L2.append(zcutunbiasedArrL2L2[0])
zcutunbiasedTcutL2L2=TCutG("highzcutunbiased",len(zcutMassArrL2L2),zcutMassArrL2L2,zcutZcutunbiasedArrL2L2)
zcutunbiasedTcutL2L2.SetVarX(massVar)
zcutunbiasedTcutL2L2.SetVarY("uncVZ")

c.SetLogx(0)
eventsL2L2.Draw("uncVZ:{0}>>hnew(100,0,0.2,100,-60,60)".format(massVar),"highzcutunbiased","colz")
gDirectory.Get("hnew").SetTitle("")
zcutunbiasedTcutL2L2.Draw("L")
c.Print(remainder[0]+"_output.pdf","Title:test")
eventsL2L2.Draw("{0}>>hnew(100,0,0.2)".format(massVar),"highzcutunbiased","colz")
c.Print(remainder[0]+"_output.pdf","Title:test")
c.SetLogx(1)

graph = drawGraph(massArrMeV,candArrL1L1,"Candidate Events L1L1","A*")
graph.GetYaxis().SetTitle("counts")
c.Print(remainder[0]+"_output.pdf","Title:test")
c.Write()

graph = drawGraph(massArrMeV,candArrL1L2,"Candidate Events L1L2","A*")
graph.GetYaxis().SetTitle("counts")
c.Print(remainder[0]+"_output.pdf","Title:test")
c.Write()

graph = drawGraph(massArrMeV,candArrL2L2,"Candidate Events L2L2","A*")
graph.GetYaxis().SetTitle("counts")
c.Print(remainder[0]+"_output.pdf","Title:test")
c.Write()

graph = drawGraph(poiMassArrL1L1,poiSigArrL1L1,"cut-and-count significance L1L1","A*")
graph.GetYaxis().SetTitle("N#sigma")
graph.Write("poiSigL1L1")
c.Print(remainder[0]+"_output.pdf","Title:test")
c.Write()

graph = drawGraph(poiMassArrL1L1,poiBkgArrL1L1,"cut-and-count estimated background L1L1","A*")
graph.GetYaxis().SetTitle("counts")
graph.Write("poiSigL1L1")
c.Print(remainder[0]+"_output.pdf","Title:test")
c.Write()

c.SetLogy(1)
graph = drawGraph(poiMassArrL1L1,poiPvalArrL1L1,"cut-and-count p-value L1L1","A*")
graph.GetYaxis().SetMoreLogLabels()
graph.Write("poiPvalL1L1")
c.Print(remainder[0]+"_output.pdf","Title:test")
c.Write()

#c.SetLogy(0)
#graph = drawGraph(poiMassArrL1L2,poiSigArrL1L2,"cut-and-count significance L1L2","A*")
#graph.GetYaxis().SetTitle("N#sigma")
#graph.Write("poiSigL1L2")
#c.Print(remainder[0]+"_output.pdf","Title:test")
#c.Write()

#graph = drawGraph(poiMassArrL1L2,poiBkgArrL1L2,"cut-and-count estimated background L1L2","A*")
#graph.GetYaxis().SetTitle("counts")
#graph.Write("poiSigL1L2")
#c.Print(remainder[0]+"_output.pdf","Title:test")
#c.Write()

#c.SetLogy(1)
#graph = drawGraph(poiMassArrL1L2,poiPvalArrL1L2,"cut-and-count p-value L1L2","A*")
#graph.GetYaxis().SetMoreLogLabels()
#graph.Write("poiPvalL1L2")
#c.Print(remainder[0]+"_output.pdf","Title:test")
#c.Write()

#c.SetLogy(0)
#graph = drawGraph(poiMassArrL2L2,poiSigArrL2L2,"cut-and-count significance L2L2","A*")
#graph.GetYaxis().SetTitle("N#sigma")
#graph.Write("poiSigL2L2")
#c.Print(remainder[0]+"_output.pdf","Title:test")
#c.Write()

#graph = drawGraph(poiMassArrL2L2,poiBkgArrL2L2,"cut-and-count estimated background L2L2","A*")
#graph.GetYaxis().SetTitle("counts")
#graph.Write("poiSigL2L2")
#c.Print(remainder[0]+"_output.pdf","Title:test")
#c.Write()

#c.SetLogy(1)
#graph = drawGraph(poiMassArrL2L2,poiPvalArrL2L2,"cut-and-count p-value L2L2","A*")
#graph.GetYaxis().SetMoreLogLabels()
#graph.Write("poiPvalL2L2")
#c.Print(remainder[0]+"_output.pdf","Title:test")
#c.Write()

#c.SetLogy(0)
#graph = drawGraph(poiMassArrL1L1,poiSigArrL1L1,"Combined cut-and-count significance L1L1 + L1L2","A*")
#graph.GetYaxis().SetTitle("N#sigma")
#graph.Write("poiSigL1L1")
#c.Print(remainder[0]+"_output.pdf","Title:test")
#c.Write()

#c.SetLogy(1)
#graph = drawGraph(poiMassArrL1L1,poiPvalArrL1L1,"Combined cut-and-count p-value L1L1 + L1L2","A*")
#graph.GetYaxis().SetMoreLogLabels()
#graph.Write("poiPvalL1L1")
#c.Print(remainder[0]+"_output.pdf","Title:test")
#c.Write()

def GetMaximum(hist):
    maxbin = hist.GetMaximumBin()
    maxx,maxy,maxz = ROOT.Long(0), ROOT.Long(0), ROOT.Long(0)
    hist.GetBinXYZ(maxbin,maxx,maxy,maxz)
    print("{0} {1} {2} {3}".format(maxbin,maxx,maxy,maxz))
    mass = hist.GetXaxis().GetBinCenter(maxx)
    eps = hist.GetYaxis().GetBinCenter(maxy)
    maximum = hist.GetBinContent(maxbin)
    print("{0} {1} {2}".format(mass,eps,maximum))
    return maximum, mass, eps

def GetMinimum(hist):
    minbin = hist.GetMinimumBin()
    minx,miny,minz = ROOT.Long(0), ROOT.Long(0), ROOT.Long(0)
    hist.GetBinXYZ(minbin,minx,miny,minz)
    print("{0} {1} {2} {3}".format(minbin,minx,miny,minz))
    mass = hist.GetXaxis().GetBinCenter(minx)
    eps = hist.GetYaxis().GetBinCenter(miny)
    minimum = hist.GetBinContent(minbin)
    print("{0} {1} {2}".format(mass,eps,minimum))
    return minimum, mass, eps

def drawContour(hist,nlevels):
    minValue = hist.GetMinimum(0)
    bottom = int(math.floor(math.log10(minValue)))
    limitLevels = array.array('d')
    for i in range(bottom,bottom+nlevels):
        for j in range(1,10):
            limitLevels.append((10**i)*j)
    hist.SetContour(len(limitLevels),limitLevels)
    hist.GetXaxis().SetMoreLogLabels()
    hist.GetXaxis().SetTitle("mass [MeV]")
    hist.GetYaxis().SetTitle("#epsilon^{2}")
    hist.SetStats(0)
    hist.Draw("cont1z")
    hist.GetZaxis().SetRangeUser(10**bottom,10**(bottom+nlevels))

def drawMaxContour(hist,nlevels):
    maxValue = hist.GetBinContent(hist.GetMaximumBin())
    bottom = int(math.floor(math.log10(maxValue)))-nlevels+1
    limitLevels = array.array('d')
    for i in range(bottom,bottom+nlevels):
        for j in range(1,10):
            limitLevels.append((10**i)*j)
    hist.SetContour(len(limitLevels),limitLevels)
    hist.GetXaxis().SetMoreLogLabels()
    hist.GetXaxis().SetTitle("mass [MeV]")
    hist.GetYaxis().SetTitle("#epsilon^{2}")
    hist.Draw("cont1z")
    hist.GetZaxis().SetRangeUser(10**bottom,10**(bottom+nlevels))

def drawHist(hist,nlevels,minz,maxz):
    hist.SetContour(nlevels)
    hist.SetStats(0)
    minimum, mass, eps = GetMinimum(hist)
    pt = TPaveText(.05,.1,.95,.8,"NDC")
    pt.AddText("Minimum Limit is {0:0.2f} #times A' Cross Section".format(minimum))
    pt.AddText("at Mass {0:0.1f} MeV and ".format(mass)+"#epsilon^{2} = "+"{0}".format(eps))
    pt.Draw()
    hist.Draw("cont4z")
    hist.GetXaxis().SetMoreLogLabels()
    hist.GetXaxis().SetTitle("mass [MeV]")
    hist.GetYaxis().SetTitle("#epsilon^{2}")
    hist.GetZaxis().SetRangeUser(minz,maxz)

def drawHistDetectable(hist,nlevels,minz,maxz):
    hist.SetContour(nlevels)
    hist.SetStats(0)
    maximum, mass, eps = GetMaximum(hist)
    pt = TPaveText(0.8,0.8,1,1,"brNDC")
    pt.AddText("Maximum Detectable is {0:0.2f} events".format(maximum))
    pt.AddText("at Mass {0:0.1f} MeV and ".format(mass)+"#epsilon^{2} = "+"{0}".format(eps))
    hist.Draw("cont0z")
    pt.Draw()
    hist.GetXaxis().SetMoreLogLabels()
    hist.GetXaxis().SetTitle("mass [MeV]")
    hist.GetYaxis().SetTitle("#epsilon^{2}")
    hist.GetZaxis().SetRangeUser(minz,maxz)


c.SetLogy(1)
c.SetLogz(1)

drawContour(fcLowerHistL1L1,3)
c.Print(remainder[0]+"_output.pdf","Title:tada")
c.Write()
drawContour(fcUpperHistL1L1,3)
c.Print(remainder[0]+"_output.pdf","Title:tada")
c.Write()
drawContour(fcLowerHistL1L2,3)
c.Print(remainder[0]+"_output.pdf","Title:tada")
c.Write()
drawContour(fcUpperHistL1L2,3)
c.Print(remainder[0]+"_output.pdf","Title:tada")
c.Write()
drawContour(fcLowerHistL2L2,3)
c.Print(remainder[0]+"_output.pdf","Title:tada")
c.Write()
drawContour(fcUpperHistL2L2,3)
c.Print(remainder[0]+"_output.pdf","Title:tada")
c.Write()

drawContour(limitHistL1L1,3)
c.Print(remainder[0]+"_output.pdf","Title:tada")
c.Write()
drawHist(limitHistL1L1,20,1,1e4)
c.Print(remainder[0]+"_output.pdf","Title:tada")
c.Write()
drawContour(limitHistL1L2,3)
c.Print(remainder[0]+"_output.pdf","Title:tada")
c.Write()
drawHist(limitHistL1L2,20,1,1e4)
c.Print(remainder[0]+"_output.pdf","Title:tada")
c.Write()
drawContour(limitHistL2L2,3)
c.Print(remainder[0]+"_output.pdf","Title:tada")
c.Write()
drawHist(limitHistL2L2,20,1,1e4)
c.Print(remainder[0]+"_output.pdf","Title:tada")
c.Write()
limitHistcombined = limitHistL1L1.Clone()
limitHistcombined.Multiply(limitHistL1L2)
limitHistcombined.SetTitle("OIM Scaled Limit L1L1 L1L2 Combined")
drawHist(limitHistcombined,20,1,1e4)
c.Print(remainder[0]+"_output.pdf","Title:tada")
c.Write()

c.SetLogz(0)
drawHistDetectable(detectableHistL1L1,20,0,0.5*scale_factor/9.77)
c.Print(remainder[0]+"_output.pdf","Title:tada")
c.Write()
#drawContour(detectableHistL1L1,20)
#c.Print(remainder[0]+"_output.pdf","Title:tada")
drawHistDetectable(detectableHistL1L2,20,0,0.5*scale_factor/9.77)
c.Print(remainder[0]+"_output.pdf","Title:tada")
c.Write()
#drawContour(detectableHistL1L2,20)
#c.Print(remainder[0]+"_output.pdf","Title:tada")
drawHistDetectable(detectableHistL2L2,20,0,0.5*scale_factor/9.77)
c.Print(remainder[0]+"_output.pdf","Title:tada")
c.Write()
#drawContour(detectableHistL2L2,20)
#c.Print(remainder[0]+"_output.pdf","Title:tada")
detectableHistcombined = detectableHistL1L1.Clone()
detectableHistcombined.Add(detectableHistL1L2)
detectableHistcombined.SetTitle("Expected A' Rate L1L1 + L1L2")
drawHistDetectable(detectableHistcombined,20,0,1.*scale_factor/9.77)
c.Print(remainder[0]+"_output.pdf","Title:tada")
c.Write()

c.SetLogz(1)
drawHist(allzHistL1L1,20,1e-2,1e2)
c.Print(remainder[0]+"_output.pdf","Title:tada")
c.Write()
drawHist(allzHistL1L2,20,1e-2,1e2)
c.Print(remainder[0]+"_output.pdf","Title:tada")
c.Write()
drawHist(allzHistL2L2,20,1e-2,1e2)
c.Print(remainder[0]+"_output.pdf","Title:tada")
c.Write()

drawContour(gammactHist,4)
c.Print(remainder[0]+"_output.pdf","Title:tada")
c.Write()

drawHist(prodHist,20,1e-2,1e2)
c.Print(remainder[0]+"_output.pdf","Title:tada")
c.Write()

c.Print(remainder[0]+"_output.pdf]")
outfile.Write()
outfile.Close()
sys.exit(0)

