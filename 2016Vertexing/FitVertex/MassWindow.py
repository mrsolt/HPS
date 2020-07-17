#!/usr/bin/env python
import sys, array,math
import getopt
import EffFuncs
from EffFuncs import Interpolate, getMassArray, getZArray, getEfficiency
import ROOT
from ROOT import gROOT, TCanvas, TF1, TFile, gStyle, TFormula, TGraph, TGraphErrors, TLegend, TH1D, TCutG, TH2D, gDirectory, RooDataSet, RooRealVar, RooArgSet, RooFormulaVar, RooWorkspace, RooAbsData, RooGlobalFunc, RooFit, RooAbsReal, RooArgList, gPad, TLatex, TH1F

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

gamma = 0.965
zcut_val = 0.5

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

def getZCut(fitfunc,zcut_val=0.5,scale=1.0,zBin=0.01,minZ=-60,maxZ=60):
    iMax = int((maxZ-minZ)/zBin)
    for i in range(iMax):
        z = maxZ - zBin*i
        integral = fitfunc.Integral(z,maxZ)
        if(integral > zcut_val/scale):
            return z
    print("ZCut not found!")
    return -9999.


gROOT.SetBatch(True)
gStyle.SetOptFit(1)
gStyle.SetOptStat(0)
c = TCanvas("c","c",800,600);

inFile = TFile(remainder[1])
effFileL1L1 = remainder[2]
events = inFile.Get("ntuple")

gStyle.SetOptStat(1111)

fzL1L1 = TF1("fzL1L1","{0}+{1}*x+{2}*x^2+{3}*x^3+{4}*x^4+{5}*x^5".format(-2.308,1227,-29030,285300,-1296000,2229000),0.05,0.175) #L1L1 10%
radfracf = TF1("radfracf","{0}+{1}*x+{2}*x^2+{3}*x^3+{4}*x^4+{5}*x^5".format(0.1926,-2.142,11.7,26,95,-385.9,823.2),0.04,0.2)
num_pairsf = TF1("num_pairsf","exp({0}+{1}*x+{2}*x^2+{3}*x^3+{4}*x^4+{5}*x^5)".format(4.903,208.3,-1880,-1868,68700,-198000),0.04,0.2)
mresL1L1f = TF1("mresL1L1f","{0}+{1}*x+{2}*x^2+{3}*x^3+{4}*x^4+{5}*x^5".format(0.01095/1000.,0.04305,0,0,0,0),0.04,0.2)

zArrL1L1 = getZArray(effFileL1L1)
mArrL1L1 = getMassArray(effFileL1L1)
effMatL1L1 = getEfficiency(effFileL1L1)

fitfunc = TF1("fitfunc","[0]*exp( (((x-[1])/[2])<[3])*(-0.5*(x-[1])^2/[2]^2) + (((x-[1])/[2])>=[3])*(0.5*[3]^2-[3]*(x-[1])/[2]))",-50,50)
fitfunc.SetParName(0,"Amplitude")
fitfunc.SetParName(1,"Mean")
fitfunc.SetParName(2,"Sigma")
fitfunc.SetParName(3,"Tail Z")

exppol1=TF1("exppol1","exp(pol1(0))",-5,100)

mass = 0.10
eps = []
eps.append(math.log10(1e-9))
eps.append(math.log10(2e-9))
eps.append(math.log10(3e-9))
#eps1 = -8
#eps2 = -9
#eps3 = -10

#Mass Resolution Parameters
masscut_nsigma = array.array('d')
masscut_nsigma.append(3.00)
masscut_nsigma.append(2.90)
masscut_nsigma.append(2.80)
masscut_nsigma.append(2.70)
masscut_nsigma.append(2.60)
masscut_nsigma.append(2.50)
masscut_nsigma.append(2.40)
masscut_nsigma.append(2.30)
masscut_nsigma.append(2.20)
masscut_nsigma.append(2.10)
masscut_nsigma.append(2.00)
masscut_nsigma.append(1.90)
masscut_nsigma.append(1.80)
masscut_nsigma.append(1.70)
masscut_nsigma.append(1.60)
masscut_nsigma.append(1.50)
masscut_nsigma.append(1.40)
masscut_nsigma.append(1.30)
masscut_nsigma.append(1.20)
masscut_nsigma.append(1.10)
masscut_nsigma.append(1.00)

masscut_eff2 = array.array('d')
masscut_eff2.append(0.00135)
masscut_eff2.append(0.00187)
masscut_eff2.append(0.00256)
masscut_eff2.append(0.00347)
masscut_eff2.append(0.00466)
masscut_eff2.append(0.00621)
masscut_eff2.append(0.00820)
masscut_eff2.append(0.01072)
masscut_eff2.append(0.01390)
masscut_eff2.append(0.01786)
masscut_eff2.append(0.02275)
masscut_eff2.append(0.02872)
masscut_eff2.append(0.03593)
masscut_eff2.append(0.04457)
masscut_eff2.append(0.05480)
masscut_eff2.append(0.06681)
masscut_eff2.append(0.08076)
masscut_eff2.append(0.09680)
masscut_eff2.append(0.11507)
masscut_eff2.append(0.13567)
masscut_eff2.append(0.15866)

masscut_eff = array.array('d')
for i in range(len(masscut_eff2)):
    masscut_eff.append((0.5-masscut_eff2[i])/0.5)

mres = mresL1L1f.Eval(mass)
radfrac = radfracf.Eval(mass)
    
deltaM = 0.001
num_pairs = num_pairsf.Eval(mass)*scale_factor
num_rad = radfrac*num_pairs
ap_yield= 3*math.pi/(2*(1/137.0))*num_rad*(mass/deltaM)
print "{0} pairs, {1} radfrac, {2} rad, {3} A'".format(num_pairs,radfrac,num_rad,ap_yield)

nzbin = 50
nBins = 1000

sigyield1 = array.array('d')
sigyield2 = array.array('d')
sigyield3 = array.array('d')

zcutArr = array.array('d')

hbar_c = 1.973e-13
for k in range(len(eps)):
    ct = hbar_c*3.0/(mass*(1/137.036)*10**eps[k])
    gammact = hbar_c*3.0*2.3*gamma/(mass*mass*(1/137.036)*10**eps[k])
    exppol1.SetParameters(targetz/gammact-math.log(gammact),-1.0/gammact)

    for i in range(len(masscut_nsigma)): 
        events.Draw("uncVZ>>hnew1d(200,-50,50)","abs({0}-{1})<{2}/2*{3}".format(massVar,mass,masscut_nsigma[i],mres),"")      
        h1d = gDirectory.Get("hnew1d")
        fit=h1d.Fit("gaus","QS")
        peak=fit.Get().Parameter(0)
        mean=fit.Get().Parameter(1)
        sigma=fit.Get().Parameter(2)
        fit=h1d.Fit("gaus","QS","",mean-3*sigma,mean+3*sigma)
        mean=fit.Get().Parameter(1)
        sigma=fit.Get().Parameter(2)
        fitfunc.SetParameters(peak,mean,sigma,3)
        fit=h1d.Fit(fitfunc,"LSQIM","",mean-2*sigma,mean+10*sigma)
        zcut = getZCut(fitfunc,zcut_val=zcut_val)

        effHistoL1L1_1 = TH1F("effHistoL1L1_1","effHistoL1L1_1",nBins,targetz,maxz)
        for j in range(nBins):
            vz = (maxz-targetz)/nBins * j + targetz
            effHistoL1L1_1.SetBinContent(j+1,Interpolate(mass,vz,mArrL1L1,zArrL1L1,effMatL1L1)*exppol1.Eval(vz))

        sig_integralL1L1 = effHistoL1L1_1.Integral(effHistoL1L1_1.GetXaxis().FindBin(zcut),effHistoL1L1_1.GetXaxis().FindBin(maxz),"width")
        print("{0}  zcut:{1}  signal:{2}  mass eff:{3}".format(masscut_nsigma[i],zcut,sig_integralL1L1,masscut_eff[i]))
        if(i == 0):
            sigyield_3 = sig_integralL1L1*masscut_eff[i]
        if(k == 0):
            sigyield1.append(sig_integralL1L1*masscut_eff[i]/sigyield_3)
            zcutArr.append(zcut)
        if(k == 1):
            sigyield2.append(sig_integralL1L1*masscut_eff[i]/sigyield_3)
        if(k == 2):
            sigyield3.append(sig_integralL1L1*masscut_eff[i]/sigyield_3)

graph1=TGraph(len(masscut_nsigma),masscut_nsigma,sigyield1)
graph2=TGraph(len(masscut_nsigma),masscut_nsigma,sigyield2)
graph3=TGraph(len(masscut_nsigma),masscut_nsigma,sigyield3)
graph1.SetTitle("Signal Yield Relative to 3#sigma Window {0} MeV A' {1}".format(mass*1000,label))
graph1.GetXaxis().SetTitle("Mass Window N#sigma")
graph1.GetYaxis().SetTitle("relative signal yield")
maximum = max(sigyield1)
if(max(sigyield2) > maximum):
    maximum = max(sigyield2)
if(max(sigyield3) > maximum):
    maximum = max(sigyield3)
graph1.GetYaxis().SetRangeUser(0.5,1.1*maximum)
graph1.Draw("AL*")
graph2.SetLineColor(2)
graph2.SetMarkerColor(2)
graph2.Draw("L* same")
graph3.SetLineColor(4)
graph3.SetMarkerColor(4)
graph3.Draw("L* same")

legend = TLegend(.68,.16,.92,.37)
legend.SetBorderSize(0)
legend.SetFillColor(0)
legend.SetFillStyle(0)
legend.SetTextFont(42)
legend.SetTextSize(0.035)
legend.AddEntry(graph1,"#epsilon^{2} = "+"{0:0.02e}".format(10**eps[0]),"LP")
legend.AddEntry(graph2,"#epsilon^{2} = "+"{0:0.02e}".format(10**eps[1]),"LP")
legend.AddEntry(graph3,"#epsilon^{2} = "+"{0:0.02e}".format(10**eps[2]),"LP")
legend.Draw("same")

c.Print(remainder[0]+".pdf[")

c.Print(remainder[0]+".pdf")

c.Print(remainder[0]+".pdf]")

c.Print(remainder[0]+"_zcut.pdf[")

graph=TGraph(len(masscut_nsigma),masscut_nsigma,zcutArr)
graph.SetTitle("Zcut for Varying Mass Windows {0} MeV Window {1}".format(mass*1000,label))
graph.GetXaxis().SetTitle("Mass Window N#sigma")
graph.GetYaxis().SetTitle("zcut (mm)")
#graph.GetYaxis().SetRangeUser(0.5,1.1*maximum)
graph.Draw("AL*")

c.Print(remainder[0]+"_zcut.pdf")

c.Print(remainder[0]+"_zcut.pdf]")