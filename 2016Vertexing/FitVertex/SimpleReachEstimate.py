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

def frange(x, y, jump):
	while x < y:
		yield x
		x += jump

def print_usage():
    print "\nUsage: {0} <output basename> <input ROOT 2D histo file> <efficiency text file>".format(sys.argv[0])
    print "Arguments: "
    print '\t-h: this help message'
    print "\n"


cutfile=""
no_candidates = False
scale_factor = 1.0
massVar = "uncM"

n_massbins=50
minmass=0.051
maxmass=0.150
n_epsbins=50
mineps=-10.0
maxeps=-7.5

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'ncs:b:h')
for opt, arg in options:
    if opt=='-n':
        no_candidates = True
    if opt=='-c':
        massVar= "corrM"
    if opt=='-s':
        scale_factor = float(arg)
    if opt=='-b':
        n_massbins = int(arg)
        n_epsbins = int(arg)
    elif opt=='-h':
        print_usage()
        sys.exit(0)


#if (len(remainder)!=5):
#        print_usage()
#        sys.exit()

#CL = 0.97725 #2-sigma
CL = 0.90

gROOT.SetBatch(True)
gStyle.SetOptFit(1)
gStyle.SetOptStat(0)
c = TCanvas("c","c",800,600);
c.Print(remainder[0]+".pdf[")
outfile = TFile(remainder[0]+".root","RECREATE")

inFile = TFile(remainder[1])
outrootfile = TFile(remainder[0]+"_new.root","RECREATE")
events = TTree("events","events")
h_zvm = inFile.Get("h_zvm")
uncM = array.array("f",[0])
uncVZ = array.array("f",[0])
events.Branch("uncM",uncM,"uncM/F")
events.Branch("uncVZ",uncVZ,"uncVZ/F")


for i in range(h_zvm.GetNbinsX()):
    uncM[0] = h_zvm.GetXaxis().GetBinCenter(i+1)
    for j in range(h_zvm.GetNbinsY()):
        uncVZ[0] = h_zvm.GetYaxis().GetBinCenter(j+1)
        for k in range(int(h_zvm.GetBinContent(i+1,j+1))):
            events.Fill()

events.Print()
outrootfile.Write()

events.Draw("uncVZ:{0}>>hnew(100,0,0.2,100,-60,60)".format(massVar),"","colz")
gDirectory.Get("hnew").SetTitle("vertexing data")
gDirectory.Get("hnew").GetXaxis().SetTitle("mass [GeV]")
gDirectory.Get("hnew").GetYaxis().SetTitle("vertex z [mm]")
c.Print(remainder[0]+".pdf")
gStyle.SetOptStat(1111)

effFile = remainder[2]

#fitfunc = TF1("fitfunc","exp(((x-[0])>=[2])*(pow([2]/2.0,2.0)-[2]*(x-[0])/[1]))",-60,60)
fitfunc = TF1("fitfunc","[0]*exp( ((x-[1])<[3])*(-0.5*(x-[1])^2/[2]^2) + ((x-[1])>=[3])*(-0.5*[3]^2/[2]^2-(x-[1]-[3])/[4]))",-50,50)

targetz = -4.3
maxz = 90 #max Z out to where we have acceptance (fitted acceptance curve may blow up past this)
zcut_count = 0.5

masscut_nsigma = 3.80
masscut_eff = 0.93

radfrac = 0.10

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
zresArr = array.array('d')
zcutArr = array.array('d')
candArr = array.array('d')
limitHist=TH2D("limit","limit",n_massbins,xedges,n_epsbins,yedges)
detectableHist=TH2D("detectable","detectable",n_massbins,xedges,n_epsbins,yedges)
gammactHist=TH2D("gammact","gammact",n_massbins,xedges,n_epsbins,yedges)
allzHist=TH2D("detectable_allz","detectable_allz",n_massbins,xedges,n_epsbins,yedges)
prodHist=TH2D("production","production",n_massbins,xedges,n_epsbins,yedges)

w = RooWorkspace("w")
w.factory("{0}[0,0.2]".format(massVar))
w.factory("uncVZ[-100,100]")
w.factory("uncP[0,10]")
w.factory("cut[0,1]")

w.defineSet("myVars","{0},uncVZ".format(massVar))

dataset = RooDataSet("data","data",events,w.set("myVars"),"")

w.factory("Gaussian::vtx_model(uncVZ,mean[-50,50],sigma[0,50])")
gauss_pdf = w.pdf("vtx_model")
w.factory("EXPR::gaussExp('exp( ((@0-@1)<@3)*(-0.5*(@0-@1)^2/@2^2) + ((@0-@1)>=@3)*(-0.5*@3^2/@2^2-(@0-@1-@3)/@4))',uncVZ,gauss_mean[-5,-20,20],gauss_sigma[5,1,50],exp_breakpoint[10,0,50],exp_length[3,0.5,20])")
#w.factory("EXPR::gaussExp('exp( ((@0-@1)>=@3)*((0.5*@3)^2-@3*(@0-@1)/@2))',uncVZ,gauss_mean[-5,-20,20],gauss_sigma[5,1,50],exp_breakpoint[10,0,50])")
gaussexp_pdf = w.pdf("gaussExp")
w.defineSet("obs_1d","uncVZ")
obs=w.set("obs_1d")
uncVZ = w.var("uncVZ")
uncVZ.setBins(200)
gauss_params = gauss_pdf.getParameters(obs)
gaussexp_params = gaussexp_pdf.getParameters(obs)

exppol4=TF1("exppol4","exp(pol4(0))",-5,100)

nbins_histpdf = 200

for i in range(0,n_massbins):
    mass = minmass+i*(maxmass-minmass)/(n_massbins-1)
    massArr.append(mass)
    mres_p0 = 0.0007 + 0.02436*mass
    massWindowArr.append(0.5*masscut_nsigma*mres_p0)
    minMassArr.append(mass - 0.5*masscut_nsigma*mres_p0)
    c.Clear()
    c.Divide(1,2)
    c.cd(1)
    
    deltaM = 0.001
    events.Draw("{0}>>mass(100,{1}-{2},{1}+{2})".format(massVar,mass,0.5*deltaM),"abs({0}-{1})<{2}".format(massVar,mass,0.5*deltaM),"")
    events.Draw("uncVZ>>h1d(100,-50,50)","abs({0}-{1})<{2}/2*{3}".format(massVar,mass,masscut_nsigma,mres_p0),"")

    num_pairs = gDirectory.Get("mass").GetEntries()*scale_factor
    num_rad = radfrac*num_pairs
    ap_yield= 3*math.pi/(2*(1/137.0))*num_rad*(mass/deltaM)
    print "{0} pairs, {1} radfrac, {2} rad, {3} A'".format(num_pairs,radfrac,num_rad,ap_yield)

    c.cd(2)
    gPad.SetLogy()
    frame=uncVZ.frame()
    dataInRange = dataset.reduce(obs,"abs({0}-{1})<{2}/2*({3})".format(massVar,mass,masscut_nsigma,mres_p0))
    binnedData = dataInRange.binnedClone()
    binnedData.plotOn(frame)


    h1d = gDirectory.Get("h1d")
    fit=h1d.Fit("gaus","QS")
    peak=fit.Get().Parameter(0)
    mean=fit.Get().Parameter(1)
    sigma=fit.Get().Parameter(2)
    fit=h1d.Fit("gaus","QS","",mean-3*sigma,mean+3*sigma)
    mean=fit.Get().Parameter(1)
    sigma=fit.Get().Parameter(2)
    fitfunc.SetParameters(peak,mean,sigma,3*sigma,5);
    fit=h1d.Fit(fitfunc,"LSQIM","",mean-2*sigma,mean+10*sigma)
    #fit.Draw()
    #c.Print(remainder[0]+".pdf")
    #breakzarray.append(fit.Get().Parameter(3))
    #lengtharray.append(fit.Get().Parameter(4))
    #breakzErr.append(fit.Get().ParError(3))
    #lengthErr.append(fit.Get().ParError(4))

    #mean = binnedData.mean(uncVZ)
    #sigma = binnedData.sigma(uncVZ)

    uncVZ.setRange("fitRange",mean-2*sigma,mean+2*sigma)
    gauss_params.setRealValue("mean",mean)
    gauss_params.setRealValue("sigma",sigma)
    gauss_pdf.fitTo(binnedData,RooFit.Range("fitRange"),RooFit.PrintLevel(-1))
    mean= gauss_params.getRealValue("mean")
    sigma= gauss_params.getRealValue("sigma")
    gaussexp_params.setRealValue("gauss_mean",mean)
    gaussexp_params.setRealValue("gauss_sigma",sigma)
    gaussexp_params.setRealValue("exp_breakpoint",fit.Get().Parameter(3))
    gaussexp_params.setRealValue("exp_length",fit.Get().Parameter(4))
    w.var("gauss_mean").setConstant(True)
    w.var("gauss_sigma").setConstant(True)
    w.var("exp_breakpoint").setConstant(True)

    w.var("exp_length").setConstant(True)
    func = gaussexp_pdf.createCdf(obs).asTF(RooArgList(obs),RooArgList(gaussexp_params))
    print "mass " + str(mass) + "  Data in Range " + str(dataInRange.sumEntries()) + "  Get Entries " + str(h1d.GetEntries())
    #zcut_frac = zcut_count/(dataInRange.sumEntries()*scale_factor)
    #zcut = func.GetX(1-zcut_frac,0,50)
    #h1d.Draw()
    #c.Print(remainder[0]+".pdf")
    zcut = func.GetX(1-zcut_count/(h1d.GetEntries()*scale_factor),0,50)
    zcut = 0.
    print "zcut {}".format(zcut)
    dataPastCut = dataInRange.reduce(w.set("obs_1d"),"uncVZ>{0}".format(zcut))
    zresArr.append(sigma)
    zcutArr.append(zcut)

    c.Clear()
    gPad.SetLogy(0)


    tailcut = targetz-2.0*sigma
    gamma = 0.95
    c.Clear()
    c.SetLogy()

    for j in range(0,n_epsbins):
        c.Clear()
        eps = mineps+j*(maxeps-mineps)/(n_epsbins-1)
        hbar_c = 1.973e-13
        ct = hbar_c*3.0/(mass*(1/137.036)*10**eps)
        gammact = hbar_c*3.0*2.3*gamma/(mass*mass*(1/137.036)*10**eps)
        blahh = 0
        
        nBins = 1000
        effHisto = TH1F("effHisto","effHisto",nBins,targetz,maxz)
        exppol4.SetParameters(targetz/gammact-math.log(gammact),-1.0/gammact,0,0,0)
        for i in range(nBins):
            vz = (maxz-targetz)/nBins * i + targetz
            effHisto.SetBinContent(i+1,Interpolate(mass,vz,mArr,zArr,effMat)*exppol4.Eval(vz))

        sig_integral = effHisto.Integral(effHisto.GetXaxis().FindBin(targetz),effHisto.GetXaxis().FindBin(maxz),"width")
        #effHisto.Draw()
        #c.Print(remainder[0]+".pdf")
        c.SetLogy()

        cdfAtZcut = effHisto.Integral(effHisto.GetXaxis().FindBin(zcut),effHisto.GetXaxis().FindBin(maxz),"width")
        if (cdfAtZcut == 0):
            cdfAtZcut = 10**-20

        prodHist.Fill(mass,10**eps,ap_yield*10**eps)
        allzHist.Fill(mass,10**eps,ap_yield*10**eps*sig_integral)
        detectableHist.Fill(mass,10**eps,ap_yield*10**eps*cdfAtZcut)
        gammactHist.Fill(mass,10**eps,gammact)

c.SetLogy(0)

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

h_zvm.Draw("COLZ")
c.Print(remainder[0]+"_output.pdf","Title:test")
graph = drawGraph(massArr,zcutArr,"zcut","AL*")
graph.GetXaxis().SetTitle("mass [GeV]")
graph.GetYaxis().SetTitle("zcut [mm]")
c.Print(remainder[0]+"_output.pdf","Title:test")

graph = drawGraph(massArr,zresArr,"zres","AL*")
graph.GetXaxis().SetTitle("mass [GeV]")
graph.GetYaxis().SetTitle("sigma_z [mm]")
graph.Write("zres")
c.Print(remainder[0]+"_output.pdf","Title:test")

c.SetLogx(1)

def drawContour(hist,nlevels):
    #minValue = hist.GetBinContent(hist.GetMinimumBin())
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
drawMaxContour(detectableHist,3)
c.Print(remainder[0]+"_output.pdf","Title:tada")

drawHist(detectableHist,20,1e-2,1)
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