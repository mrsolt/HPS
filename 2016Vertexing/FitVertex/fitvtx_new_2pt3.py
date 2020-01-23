#!/usr/bin/env python
import sys, array, math
import getopt
import upperlimit
import numpy
import EffFuncs
from EffFuncs import Interpolate, getMassArray, getZArray, getEfficiency
import ROOT
from ROOT import gROOT, TTree, TCanvas, TF1, TFile, gStyle, TFormula, TGraph, TGraphErrors, TH1D, TH1F, TCutG, TH2D, gDirectory, RooDataSet, RooRealVar, RooArgSet, RooFormulaVar, RooWorkspace, RooAbsData, RooFit, RooAbsReal, RooArgList, gPad, TFeldmanCousins, RooDataHist, RooHistPdf, TMath
from ROOT.RooStats import ModelConfig, ProfileLikelihoodCalculator, LikelihoodIntervalPlot

def print_usage():
    print "\nUsage: {0} <output basename> <input ROOT 2D histo file> <efficiency text file>".format(sys.argv[0])
    print "Arguments: "
    print '\t-n: ignore candidates past zcut (default false)'
    print '\t-r: use radiative fraction as function of mass (default false)'
    print '\t-z: target z (default -4.3 mm)'
    print '\t-s: scale factor (default 1)'
    print '\t-b: number of mass and epsilon bins (default 50)'
    print '\t-l: is L1L1 (default true)'
    print '\t-h: this help message'
    print "\n"


no_candidates = False
scale_factor = 1.0
massVar = "uncM"

n_massbins=50
minmass=0.051
maxmass=0.150
n_epsbins=50
mineps=-10.0
maxeps=-7.5
targetz = -4.3
maxz = 90 #max Z out to where we have acceptance (fitted acceptance curve may blow up past this)
zcut_count = 0.5

masscut_nsigma = 2.80
masscut_eff = 0.93
mres_p0 = 1.364/1000.
mres_p1 = 0.02608

useVarRadFrac = False
radfrac = 0.15
L1L1 = True
CL = 0.90


options, remainder = getopt.gnu_getopt(sys.argv[1:], 'nrz:s:b:lh')
for opt, arg in options:
    if opt=='-n':
        no_candidates = True
    if opt=='-r':
        useVarRadFrac = True
    if opt=='-z':
        targetz = float(arg)
    if opt=='-s':
        scale_factor = float(arg)
    if opt=='-b':
        n_massbins = int(arg)
        n_epsbins = int(arg)
    if opt=='-l':
        L1L1 = False
    elif opt=='-h':
        print_usage()
        sys.exit(0)

gROOT.SetBatch(True)
gStyle.SetOptFit(1)
gStyle.SetOptStat(0)
c = TCanvas("c","c",800,600);
c.Print(remainder[0]+".pdf[")
outfile = TFile(remainder[0]+".root","RECREATE")

inFile = TFile(remainder[1])
effFile = remainder[2]
events = inFile.Get("ntuple")
if(not L1L1):
    inFileL1L1 = TFile(remainder[3])
    eventsL1L1 = inFileL1L1.Get("ntuple")

gStyle.SetOptStat(1111)

#fz1 = TF1("fz1","41.65-466*x+2238*x^2-3757*x^3",0.05,0.15) #L1L1
fz1 = TF1("fz1","33.8-361*x+1509*x^2-2041*x^3",0.05,0.15) #L1L1 10%
#fz1 = TF1("fz1","15.59-117.9*x-171.6*x^2+1887*x^3",0.05,0.15) #L1L1 10% with zcut = 100
#fz1 = TF1("fz1","17.94-148.8*x-39.36*x^2+1400*x^3",0.05,0.15) #L1L1 10% with zcut = 50
#fz1 = TF1("fz1","71.8-1130*x+9023*x^2-26830*x^3",0.05,0.15) #L1L2
#fz1 = TF1("fz1","58.33-876.9*x+6591*x^2-19110*x^3",0.05,0.15) #L1L2 10%
#fz1 = TF1("fz1","93.51-1447*x+10630*x^2-31440*x^3",0.05,0.15) #L2L2
#fz1 = TF1("fz1","70.76-945.6*x+5337*x^2-12440*x^3",0.05,0.15) #L2L2 10%

zArr = getZArray(effFile)
mArr = getMassArray(effFile)
effMat = getEfficiency(effFile)

xedges = array.array('d')
yedges = array.array('d')
for i in range(0,n_massbins+1):
    xedges.append(minmass+(i-0.5)*(maxmass-minmass)/(n_massbins-1))
for j in range(0,n_epsbins+1):
    yedges.append(10**(mineps+(j-0.5)*(maxeps-mineps)/(n_epsbins-1)))

outfile.cd()
massArr = array.array('d')
minMassArr = array.array('d')
massWindowArr = array.array('d')
zcutArr = array.array('d')
mResArr = array.array('d')
radfracArr = array.array('d')
candArr = array.array('d')
limitHist=TH2D("limit","limit",n_massbins,xedges,n_epsbins,yedges)
detectableHist=TH2D("detectable","detectable",n_massbins,xedges,n_epsbins,yedges)
gammactHist=TH2D("gammact","gammact",n_massbins,xedges,n_epsbins,yedges)
allzHist=TH2D("detectable_allz","detectable_allz",n_massbins,xedges,n_epsbins,yedges)
prodHist=TH2D("production","production",n_massbins,xedges,n_epsbins,yedges)
candHist=TH1D("candidates","candidates",n_massbins,xedges)
fcLowerHist=TH2D("fcLowerLimit","fcLowerLimit",n_massbins,xedges,n_epsbins,yedges)
fcUpperHist=TH2D("fcUpperLimit","fcUpperLimit",n_massbins,xedges,n_epsbins,yedges)

w = RooWorkspace("w")
w.factory("{0}[0,0.2]".format(massVar))
w.factory("uncVZ[-100,100]")
w.factory("uncP[0,10]")
w.factory("cut[0,1]")

w.defineSet("myVars","{0},uncVZ".format(massVar))

dataset = RooDataSet("data","data",events,w.set("myVars"),"")

w.defineSet("obs_1d","uncVZ")
obs = w.set("obs_1d")
uncVZ = w.var("uncVZ")
uncVZ.setBins(200)

exppol1=TF1("exppol1","exp(pol1(0))",-5,100)

fc = TFeldmanCousins()
fc.SetCL(CL)

for i in range(0,n_massbins):
    mass = minmass+i*(maxmass-minmass)/(n_massbins-1)
    massArr.append(mass)

    mres = mres_p0 + mres_p1*mass

    if(useVarRadFrac):
        radfrac = 0.0

    massWindowArr.append(0.5*masscut_nsigma*mres)
    minMassArr.append(mass - 0.5*masscut_nsigma*mres)
    c.Clear()
    
    deltaM = 0.001
    if(L1L1):
        events.Draw("{0}>>mass(100,{1}-{2},{1}+{2})".format(massVar,mass,0.5*deltaM),"abs({0}-{1})<{2}".format(massVar,mass,0.5*deltaM),"")
    else:
        eventsL1L1.Draw("{0}>>mass(100,{1}-{2},{1}+{2})".format(massVar,mass,0.5*deltaM),"abs({0}-{1})<{2}".format(massVar,mass,0.5*deltaM),"")
    num_pairs = gDirectory.Get("mass").GetEntries()*scale_factor
    num_rad = radfrac*num_pairs
    ap_yield= 3*math.pi/(2*(1/137.0))*num_rad*(mass/deltaM)
    print "{0} pairs, {1} radfrac, {2} rad, {3} A'".format(num_pairs,radfrac,num_rad,ap_yield)

    dataInRange = dataset.reduce(obs,"abs({0}-{1})<{2}/2*{3}".format(massVar,mass,masscut_nsigma,mres))
    
    zcut = fz1.Eval(mass)
    print "zcut {}".format(zcut)
    dataPastCut = dataInRange.reduce(w.set("obs_1d"),"uncVZ>{0}".format(zcut))
    zcutArr.append(zcut)
    mResArr.append(mres)
    radfracArr.append(radfrac)

    n_candidates = dataPastCut.numEntries()
    if (no_candidates):
        n_candidates = 0
    print n_candidates
    for k in range(0,n_candidates):
        candHist.Fill(mass)
    candArr.append(n_candidates)
    fcLower = fc.CalculateLowerLimit(n_candidates,zcut_count)
    fcUpper = fc.CalculateUpperLimit(n_candidates,zcut_count)

    gamma = 0.95

    for j in range(0,n_epsbins):
        c.Clear()
        eps = mineps+j*(maxeps-mineps)/(n_epsbins-1)
        hbar_c = 1.973e-13
        ct = hbar_c*3.0/(mass*(1/137.036)*10**eps)
        gammact = hbar_c*3.0*2.3*gamma/(mass*mass*(1/137.036)*10**eps)
       
        nBins = 1000
        effHisto = TH1F("effHisto","effHisto",nBins,targetz,maxz)
        exppol1.SetParameters(targetz/gammact-math.log(gammact),-1.0/gammact)
        for i in range(nBins):
            vz = (maxz-targetz)/nBins * i + targetz
            effHisto.SetBinContent(i+1,Interpolate(mass,vz,mArr,zArr,effMat)*exppol1.Eval(vz))

        sig_integral = effHisto.Integral(effHisto.GetXaxis().FindBin(targetz),effHisto.GetXaxis().FindBin(maxz),"width")
        cdfAtZcut = effHisto.Integral(effHisto.GetXaxis().FindBin(zcut),effHisto.GetXaxis().FindBin(maxz),"width")
        if (cdfAtZcut == 0):
            cdfAtZcut = 10**-20
        if (no_candidates):
            dataArray=numpy.zeros(2)
            dataArray[1] = cdfAtZcut
        else:
            dataArray=numpy.zeros(dataPastCut.numEntries()+2)
            dataArray[0] = 0.0
            for k in xrange(0,dataPastCut.numEntries()):
                thisX = dataPastCut.get(k).getRealValue("uncVZ")
                w.var("uncVZ").setVal(thisX)
                dataArray[k+1]=(cdfAtZcut-effHisto.Integral(effHisto.GetXaxis().FindBin(thisX),effHisto.GetXaxis().FindBin(maxz),"width"))
            dataArray[dataPastCut.numEntries()+1] = cdfAtZcut
        dataArray/= (cdfAtZcut)
        dataArray.sort()
        output = upperlimit.upperlim(CL, 1, dataArray, 0., dataArray)

        prodHist.Fill(mass,10**eps,ap_yield*10**eps)
        allzHist.Fill(mass,10**eps,ap_yield*10**eps*sig_integral)
        detectableHist.Fill(mass,10**eps,ap_yield*10**eps*cdfAtZcut)
        gammactHist.Fill(mass,10**eps,gammact)
        limit_detectable = output[0] # this is a limit on number of detectable A' (past zcut, within mass cut)
        limit_allz = limit_detectable/((cdfAtZcut/sig_integral)*masscut_eff) # this is a limit on number of detectable A' if we didn't have zcut or mass cut
        limit_production = limit_allz/sig_integral # limit on number of produced A'
        limit_eps = limit_production/ap_yield
        limit_scaled = limit_eps/10**eps
        print "{0} {1} {2} {3} {4}".format(limit_detectable,limit_allz,limit_production,limit_eps,limit_scaled)
        limitHist.Fill(mass,10**eps,limit_scaled)
        fcLowerHist.Fill(mass,10**eps,fcLower/cdfAtZcut/masscut_eff/ap_yield/10**eps)
        fcUpperHist.Fill(mass,10**eps,fcUpper/cdfAtZcut/masscut_eff/ap_yield/10**eps)
        del effHisto

poiMassArr = array.array('d')
poiPvalArr = array.array('d')
poiSigArr = array.array('d')
poiBkgArr = array.array('d')

c.SetLogy(0)
for i in xrange(0,len(massArr)):
    mass = massArr[i]
    sigMassArr = array.array('d')
    sigCandArr = array.array('d')
    hasLowSide = False
    hasHighSide = False
    for j in xrange(0,len(massArr)):
        if abs(mass-massArr[j])>massWindowArr[i]+massWindowArr[j]:
            if j<i:
                hasLowSide = True
            if i<j:
                hasHighSide = True
            sigMassArr.append(massArr[j])
            sigCandArr.append(candArr[j])
    if (hasLowSide and hasHighSide):

        graph=TGraph(len(sigMassArr),sigMassArr,sigCandArr)
        graph.SetTitle("background")
        graph.Draw("A*")
        graph.Fit("pol2")
        graph.GetXaxis().SetMoreLogLabels()
        c.Print(remainder[0]+".pdf","Title:test")
        nbkg = graph.GetFunction("pol2").Eval(mass)
        if nbkg<0.5:
            nbkg = 0.5
        poiBkgArr.append(nbkg)
        pval = 1.0-TMath.Prob(2*nbkg,2*int(candArr[i]))
        zscore = TMath.NormQuantile(1.0-pval)
        poiMassArr.append(mass)
        poiPvalArr.append(pval)
        poiSigArr.append(zscore)

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
    graph.GetXaxis().SetTitle("mass [GeV]")
    return graph

c.SetLogx(1)
graph = drawGraph(massArr,zcutArr,"zcut","AL*")
graph.GetXaxis().SetTitle("mass [GeV]")
graph.GetYaxis().SetTitle("zcut [mm]")
c.Print(remainder[0]+"_output.pdf","Title:test")

graph = drawGraph(massArr,mResArr,"mres","AL*")
graph.GetXaxis().SetTitle("mass [GeV]")
graph.GetYaxis().SetTitle("Mass Resolution [GeV]")
c.Print(remainder[0]+"_output.pdf","Title:test")

graph = drawGraph(massArr,radfracArr,"radfrac","AL*")
graph.GetXaxis().SetTitle("mass [GeV]")
graph.GetYaxis().SetTitle("Radiative Fraction")
c.Print(remainder[0]+"_output.pdf","Title:test")


zcutMassArr = minMassArr[:]
zcutZcutArr = zcutArr[:]
zcutMassArr.append(0.2)
zcutZcutArr.append(zcutArr[-1])
zcutMassArr.append(0.2)
zcutZcutArr.append(100)
zcutMassArr.append(0)
zcutZcutArr.append(100)
zcutMassArr.append(0)
zcutZcutArr.append(zcutArr[0])
zcutMassArr.append(minMassArr[0])
zcutZcutArr.append(zcutArr[0])
zcutTcut=TCutG("highzcut",len(zcutMassArr),zcutMassArr,zcutZcutArr)
zcutTcut.SetVarX(massVar)
zcutTcut.SetVarY("uncVZ")

c.SetLogx(0)
events.Draw("uncVZ:{0}>>hnew(100,0,0.2,100,-60,60)".format(massVar),"highzcut","colz")
gDirectory.Get("hnew").SetTitle("")
zcutTcut.Draw("L")
c.Print(remainder[0]+"_output.pdf","Title:test")
events.Draw("{0}>>hnew(100,0,0.2)".format(massVar),"highzcut","colz")
c.Print(remainder[0]+"_output.pdf","Title:test")
c.SetLogx(1)

graph = drawGraph(massArr,candArr,"candidate events","A*")
graph.GetYaxis().SetTitle("counts")
c.Print(remainder[0]+"_output.pdf","Title:test")

graph = drawGraph(poiMassArr,poiSigArr,"cut-and-count significance","A*")
graph.GetYaxis().SetTitle("Nsigma")
graph.Write("poiSig")
c.Print(remainder[0]+"_output.pdf","Title:test")

graph = drawGraph(poiMassArr,poiBkgArr,"cut-and-count estimated background","A*")
graph.GetYaxis().SetTitle("counts")
graph.Write("poiSig")
c.Print(remainder[0]+"_output.pdf","Title:test")

c.SetLogy(1)
graph = drawGraph(poiMassArr,poiPvalArr,"cut-and-count p-value","A*")
graph.GetYaxis().SetMoreLogLabels()
graph.Write("poiPval")
c.Print(remainder[0]+"_output.pdf","Title:test")

def drawContour(hist,nlevels):
    minValue = hist.GetMinimum(0)
    bottom = int(math.floor(math.log10(minValue)))
    limitLevels = array.array('d')
    for i in range(bottom,bottom+nlevels):
        for j in range(1,10):
            limitLevels.append((10**i)*j)
    hist.SetContour(len(limitLevels),limitLevels)
    hist.GetXaxis().SetMoreLogLabels()
    hist.GetXaxis().SetTitle("mass [GeV]")
    hist.GetYaxis().SetTitle("epsilon^2")
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
    hist.GetXaxis().SetTitle("mass [GeV]")
    hist.GetYaxis().SetTitle("epsilon^2")
    hist.Draw("cont1z")
    hist.GetZaxis().SetRangeUser(10**bottom,10**(bottom+nlevels))
def drawHist(hist,nlevels,minz,maxz):
    hist.SetContour(nlevels)
    hist.Draw("colz")
    hist.GetXaxis().SetMoreLogLabels()
    hist.GetXaxis().SetTitle("mass [GeV]")
    hist.GetYaxis().SetTitle("epsilon^2")
    hist.GetZaxis().SetRangeUser(minz,maxz)


c.SetLogy(1)
c.SetLogz(1)

drawContour(fcLowerHist,3)
c.Print(remainder[0]+"_output.pdf","Title:tada")
drawContour(fcUpperHist,3)
c.Print(remainder[0]+"_output.pdf","Title:tada")
drawContour(limitHist,3)
c.Print(remainder[0]+"_output.pdf","Title:tada")

drawHist(limitHist,20,1,1e4)
c.Print(remainder[0]+"_output.pdf","Title:tada")

drawHist(detectableHist,20,1e-2,2.4)
c.Print(remainder[0]+"_output.pdf","Title:tada")

drawHist(allzHist,20,1e-2,1e2)
c.Print(remainder[0]+"_output.pdf","Title:tada")

drawContour(gammactHist,4)
c.Print(remainder[0]+"_output.pdf","Title:tada")

drawHist(prodHist,20,1e-2,1e2)
c.Print(remainder[0]+"_output.pdf","Title:tada")

c.Print(remainder[0]+"_output.pdf]")
outfile.Write()
outfile.Close()
sys.exit(0)

