#!/usr/bin/env python
import sys, array,math
import getopt
import upperlimit
import numpy
import ROOT
from ROOT import gROOT, TCanvas, TF1, TFile, gStyle, TFormula, TGraph, TGraphErrors, TH1D, TCutG, TH2D, gDirectory, RooDataSet, RooRealVar, RooArgSet, RooFormulaVar, RooWorkspace, RooAbsData, RooFit, RooAbsReal, RooArgList, gPad, TFeldmanCousins, RooDataHist, RooHistPdf, TMath
from ROOT.RooStats import ModelConfig, ProfileLikelihoodCalculator, LikelihoodIntervalPlot

def frange(x, y, jump):
	while x < y:
		yield x
		x += jump

def print_usage():
    print "\nUsage: {0} <output basename> <input ROOT file> <acceptance ROOT file> <tails ROOT file> <radfrac ROOT file>".format(sys.argv[0])
    print "./fitvtx.py stuff ../golden_vertcuts.root ../acceptance/acceptance_data.root ../tails.root ../frac.root -u"
    print "Arguments: "
    print '\t-h: this help message'
    print "\n"


cutfile=""
uniform_efficiency = False
no_candidates = False
scale_factor = 1.0
correct_mres = False
massVar = "uncM"

n_massbins=50
minmass=0.02
maxmass=0.06
n_epsbins=50
mineps=-10.0
maxeps=-7.5

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'unmcs:b:h')
for opt, arg in options:
    if opt=='-u':
        uniform_efficiency = True
    if opt=='-n':
        no_candidates = True
    if opt=='-m':
        correct_mres= True
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


if (len(remainder)!=5):
        print_usage()
        sys.exit()

#CL = 0.97725 #2-sigma
CL = 0.90

gROOT.SetBatch(True)
gStyle.SetOptFit(1)
gStyle.SetOptStat(0)
c = TCanvas("c","c",800,600);
c.Print(remainder[0]+".pdf[")
outfile = TFile(remainder[0]+".root","RECREATE")

inFile = TFile(remainder[1])
events = inFile.Get("cut")
#events.Print()
events.Draw("uncVZ:{0}>>hnew(100,0,0.1,100,-50,50)".format(massVar),"","colz")
gDirectory.Get("hnew").SetTitle("vertexing data")
gDirectory.Get("hnew").GetXaxis().SetTitle("mass [GeV]")
gDirectory.Get("hnew").GetYaxis().SetTitle("vertex z [mm]")
c.Print(remainder[0]+".pdf")
gStyle.SetOptStat(1111)

acceptanceFile = TFile(remainder[2])
tailsFile = TFile(remainder[3])
radfracFile = TFile(remainder[4])

fitfunc = TF1("fitfunc","[0]*exp( ((x-[1])<[3])*(-0.5*(x-[1])^2/[2]^2) + ((x-[1])>=[3])*(-0.5*[3]^2/[2]^2-(x-[1]-[3])/[4]))",-50,50)
fitfunc.SetParName(0,"Amplitude")
fitfunc.SetParName(1,"Mean")
fitfunc.SetParName(2,"Sigma")
fitfunc.SetParName(3,"Tail Z")
fitfunc.SetParName(4,"Tail length")


targetz = -5.0
maxz = 100 #max Z out to where we have acceptance (fitted acceptance curve may blow up past this)
zcut_count = 0.5

masscut_nsigma = 2.80
masscut_eff = 0.838

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
candHist=TH1D("candidates","candidates",n_massbins,xedges)
fcLowerHist=TH2D("fcLowerLimit","fcLowerLimit",n_massbins,xedges,n_epsbins,yedges)
fcUpperHist=TH2D("fcUpperLimit","fcUpperLimit",n_massbins,xedges,n_epsbins,yedges)
plrPvalHist=TH2D("plrPval","plrPval",n_massbins,xedges,n_epsbins,yedges)
plrSigHist=TH2D("plrSig","plrSig",n_massbins,xedges,n_epsbins,yedges)
logplrHist=TH2D("logplr","logplr",n_massbins,xedges,n_epsbins,yedges)
candRescaledHist=TH1D("candidates_rescaled","candidates_rescaled",100,0,1.0)
candRescaled2DHist=TH2D("candidates_rescaled_2d","candidates_rescaled_2d",n_massbins,xedges,100,0,1.0)

w = RooWorkspace("w")
w.factory("{0}[0,0.1]".format(massVar))
w.factory("uncVZ[-100,100]")
w.factory("uncP[0,10]")
w.factory("cut[0,1]")

w.defineSet("myVars","{0},uncVZ".format(massVar))

dataset = RooDataSet("data","data",events,w.set("myVars"),"")

w.factory("Gaussian::vtx_model(uncVZ,mean[-50,50],sigma[0,50])")
gauss_pdf = w.pdf("vtx_model")
w.factory("EXPR::gaussExp('exp( ((@0-@1)<@3)*(-0.5*(@0-@1)^2/@2^2) + ((@0-@1)>=@3)*(-0.5*@3^2/@2^2-(@0-@1-@3)/@4))',uncVZ,gauss_mean[-5,-20,20],gauss_sigma[5,1,50],exp_breakpoint[10,0,50],exp_length[3,0.5,20])")
gaussexp_pdf = w.pdf("gaussExp")
w.defineSet("obs_1d","uncVZ")
obs=w.set("obs_1d")
uncVZ = w.var("uncVZ")
uncVZ.setBins(200)
gauss_params = gauss_pdf.getParameters(obs)
gaussexp_params = gaussexp_pdf.getParameters(obs)

exppol4=TF1("exppol4","exp(pol4(0))",-5,100)
w.factory("EXPR::signal('(@0>{0})*exp(@1 + @2*@0 + @3*@0^2 + @4*@0^3 + @5*@0^4)',uncVZ,eff_p0[-1,1],eff_p1[-1,1],eff_p2[-1,1],eff_p3[-1,1],eff_p4[-1,1])".format(targetz))
w.factory("SUM::model(strength[0,1]*signal,gaussExp)")

w.defineSet("poi","strength")
w.factory("nbkg[0,1e6]")
nbins_histpdf = 200
bkgHist = TH1D("bkgHist","bkgHist",nbins_histpdf,-100,100)
sigHist = TH1D("sigHist","sigHist",nbins_histpdf,-100,100)

pdf = w.pdf("model")

fc = TFeldmanCousins()
fc.SetCL(CL)

for i in range(0,n_massbins):
    mass = minmass+i*(maxmass-minmass)/(n_massbins-1)
    massArr.append(mass)
    mres_p0 = acceptanceFile.Get("mres_l1_p0").GetFunction("pol1").Eval(mass)
    mres_p1 = acceptanceFile.Get("mres_l1_p1").GetFunction("pol1").Eval(mass)
    if correct_mres:
        mres_p1 = 0
    massWindowArr.append(0.5*masscut_nsigma*mres_p0)
    minMassArr.append(mass - 0.5*masscut_nsigma*mres_p0)
    c.Clear()
    c.Divide(1,2)
    c.cd(1)
    #events.Draw("uncVZ:uncM>>hnew2d(100,0,0.1,100,-50,50)","abs(uncM-{0})<{1}/2*({2}+{3}*uncVZ)".format(mass,masscut_nsigma,mres_p0,mres_p1),"colz")
    #gPad.SetLogy(1)
    
    deltaM = 0.001
    events.Draw("{0}>>mass(100,{1}-{2},{1}+{2})".format(massVar,mass,0.5*deltaM),"abs({0}-{1})<{2}".format(massVar,mass,0.5*deltaM),"")
    #c.Print(remainder[0]+".pdf","Title:mass_{0}".format(mass))

    num_pairs = gDirectory.Get("mass").GetEntries()*scale_factor
    radfrac = radfracFile.Get("radfrac").GetFunction("pol3").Eval(mass)
    num_rad = radfrac*num_pairs
    ap_yield= 3*math.pi/(2*(1/137.0))*num_rad*(mass/deltaM)
    print "{0} pairs, {1} radfrac, {2} rad, {3} A'".format(num_pairs,radfrac,num_rad,ap_yield)


    breakz = tailsFile.Get("breakz").GetFunction("pol3").Eval(mass)
    length = tailsFile.Get("length").GetFunction("pol3").Eval(mass)

    c.cd(2)
    gPad.SetLogy()
    frame=uncVZ.frame()
    dataInRange = dataset.reduce(obs,"abs({0}-{1})<{2}/2*({3}+{4}*uncVZ)".format(massVar,mass,masscut_nsigma,mres_p0,mres_p1))
    binnedData = dataInRange.binnedClone()
    binnedData.plotOn(frame)
    mean = binnedData.mean(uncVZ)
    sigma = binnedData.sigma(uncVZ)
    uncVZ.setRange("fitRange",mean-2*sigma,mean+2*sigma)
    gauss_params.setRealValue("mean",mean)
    gauss_params.setRealValue("sigma",sigma)
    gauss_pdf.fitTo(binnedData,RooFit.Range("fitRange"),RooFit.PrintLevel(-1))
    mean= gauss_params.getRealValue("mean")
    sigma= gauss_params.getRealValue("sigma")
    gaussexp_params.setRealValue("gauss_mean",mean)
    gaussexp_params.setRealValue("gauss_sigma",sigma)
    gaussexp_params.setRealValue("exp_breakpoint",breakz)
    gaussexp_params.setRealValue("exp_length",length)
    w.var("gauss_mean").setConstant(True)
    w.var("gauss_sigma").setConstant(True)
    w.var("exp_breakpoint").setConstant(True)
    w.var("exp_length").setConstant(True)
    func = gaussexp_pdf.createCdf(obs).asTF(RooArgList(obs),RooArgList(gaussexp_params))
    zcut_frac = zcut_count/(dataInRange.sumEntries()*scale_factor)
    zcut = func.GetX(1-zcut_frac,0,50)
    print "zcut {}".format(zcut)
    dataPastCut = dataInRange.reduce(w.set("obs_1d"),"uncVZ>{0}".format(zcut))
    zresArr.append(sigma)
    zcutArr.append(zcut)

    gaussexp_pdf.plotOn(frame)
    #gaussexp_pdf.paramOn(frame)
    frame.SetAxisRange(-50,50)
    frame.SetMinimum(0.5)
    name="vertex Z, mass {0} +/- {1} GeV, zcut {2} mm".format(mass,0.5*masscut_nsigma*mres_p0,zcut)
    frame.SetTitle(name)
    frame.GetXaxis().SetTitle("Vertex Z [mm]")
    frame.Draw()
    c.Print(remainder[0]+".pdf","Title:mass {0} zcut {1}".format(mass,zcut))
#
    #c.cd(2)
    c.Clear()
    gPad.SetLogy(0)
    candRescaledHist.Reset()
    for k in xrange(0,dataPastCut.numEntries()):
        thisX = dataPastCut.get(k).getRealValue("uncVZ")
        #print math.exp((zcut-thisX)/length)
        candRescaledHist.Fill((1-math.exp((zcut-thisX)/length)))
        candRescaled2DHist.Fill(mass,(1-math.exp((zcut-thisX)/length)))
    candRescaledHist.GetXaxis().SetTitle("background cdf")
    candRescaledHist.SetTitle("mass {0}".format(mass))
    candRescaledHist.Draw()
    c.Print(remainder[0]+".pdf","Title:mass {0} zcut {1}".format(mass,zcut))


    #zcut2_frac = 20.0/(dataInRange.sumEntries()/scale_factor)
    #zcut2 = func.GetX(1-zcut2_frac,0,50)
    tailcut = targetz-2.0*sigma
    print "tailcut "+str(tailcut)
    dataPastCut2 = dataInRange.reduce(w.set("obs_1d"),"uncVZ>{0}".format(tailcut)).binnedClone()

    n_candidates = dataPastCut.numEntries()
    if (no_candidates):
        n_candidates = 0
    print n_candidates
    for k in range(0,n_candidates):
        candHist.Fill(mass)
    candArr.append(n_candidates)
    #candHist.Fill(mass,n_candidates)
    fcLower = fc.CalculateLowerLimit(n_candidates,zcut_count)
    fcUpper = fc.CalculateUpperLimit(n_candidates,zcut_count)


    gamma = acceptanceFile.Get("gamma").GetFunction("pol0").Eval(mass)
    eff_p0= acceptanceFile.Get("l1_p0").GetFunction("pol1").Eval(mass)
    eff_p1= acceptanceFile.Get("l1_p1").GetFunction("pol1").Eval(mass)
    eff_p2= acceptanceFile.Get("l1_p2").GetFunction("pol3").Eval(mass)
    eff_p3= acceptanceFile.Get("l1_p3").GetFunction("pol3").Eval(mass)
    #eff_p4= acceptanceFile.Get("l1_p4").GetFunction("pol4").Eval(mass)
    eff_p4= 0
    exppol4.SetParameters(eff_p0,eff_p1,eff_p2,eff_p3,eff_p4)
    exppol4.Draw()
    exppol4.GetYaxis().SetRangeUser(0,2)

    fitfunc.SetParameters(1.0,mean,sigma,breakz,length)
    bkgHist.Reset()
    for binnum in xrange(1,nbins_histpdf+1):
        bkgHist.SetBinContent(binnum,fitfunc.Eval(bkgHist.GetXaxis().GetBinCenter(binnum)))
#    bkgHist.Draw()
    bkgDataHist = RooDataHist("bkgDataHist_{0}".format(i),"bkgDataHist_{0}".format(i),RooArgList(w.set("obs_1d")),bkgHist)
    bkgPdf = RooHistPdf("bkgPdf_{0}".format(i),"bkgPdf_{0}".format(i),w.set("obs_1d"),bkgDataHist)
    getattr(w,'import')(bkgPdf,RooFit.Silence())

    #w.factory("Exponential::bkg_{0}(uncVZ,{0})".format(i,-1.0/length))
    #w.factory("EXPR::gaussExp_{0}('exp( ((@0-{1})<{3})*(-0.5*(@0-{1})^2/{2}^2) + ((@0-{1})>={3})*(-0.5*{3}^2/{2}^2-(@0-{1}-{3})/{4}))',uncVZ)".format(i,mean,sigma,breakz,length))

    c.Clear()
    c.SetLogy()
    uncVZ.setRange("fitRange",tailcut,50)
    frame=uncVZ.frame()
    frame.SetAxisRange(tailcut,50)
    frame.SetTitle(name)
    frame.GetXaxis().SetTitle("Vertex Z [mm]")
    dataPastCut2.plotOn(frame)
    thispdf = w.pdf("bkgPdf_{0}".format(i))
    fitresult = thispdf.fitTo(dataPastCut2,RooFit.Range("fitRange"),RooFit.PrintLevel(-1),RooFit.Save())
    bkgNLL = fitresult.minNll()
    thispdf.plotOn(frame,RooFit.Range("fitRange"),RooFit.NormRange("fitRange"))
    #thispdf.paramOn(frame)
    frame.SetMinimum(0.1)
    frame.Draw()
    c.Print(remainder[0]+".pdf","Title:test2")

    for j in range(0,n_epsbins):
        c.Clear()
        eps = mineps+j*(maxeps-mineps)/(n_epsbins-1)
        #ct = 80e-3*1e-8/(10**eps)*(0.1/mass)
        #gammact = 8*(1.05/10)*1e-8/(10**eps)*(0.1/mass)**2
        hbar_c = 1.973e-13
        ct = hbar_c*3.0/(mass*(1/137.036)*10**eps)
        gammact = hbar_c*3.0*1.056*gamma/(mass*mass*(1/137.036)*10**eps)
        #print "epsq {0} ct {1} gammact {2}".format(eps,ct,gammact)
        #if (gammact<1):
        #    continue

        #exppol4.SetParameters(targetz/gammact-math.log(gammact),-1.0/gammact,0,0,0)
        #exppol4.Draw()
        #c.Print(remainder[0]+".pdf","Title:mass_{0}_eps_{1}".format(mass,eps))
        blahh = 0
        #print "decay integral {0}".format(exppol4.IntegralOneDim(targetz,100,1e-12,1e-12,ROOT.Double(blahh)))
        
        exppol4.SetParameters(eff_p0+targetz/gammact-math.log(gammact),eff_p1-1.0/gammact,eff_p2,eff_p3,eff_p4)
        if (uniform_efficiency):
            exppol4.SetParameters(targetz/gammact-math.log(gammact),-1.0/gammact,0,0,0)
        #c.SetLogy(0)
        #exppol4.Draw()
        #c.Print(remainder[0]+".pdf","Title:mass_{0}_eps{1}".format(mass,eps))
        sig_integral = exppol4.IntegralOneDim(targetz,maxz,1e-12,1e-12,ROOT.Double(blahh))
        #print "signal integral {0}".format(sig_integral) #this is production-weighted efficiency

        sigHist.Reset()
        for binnum in xrange(1,nbins_histpdf+1):
            #print exppol4.Eval(sigHist.GetXaxis().GetBinCenter(binnum))
            if sigHist.GetXaxis().GetBinCenter(binnum)>=targetz:
                sigHist.SetBinContent(binnum,exppol4.Eval(sigHist.GetXaxis().GetBinCenter(binnum)))
        #sigHist.Draw()
        sigDataHist = RooDataHist("sigDataHist_{0}_{1}".format(i,j),"sigDataHist_{0}_{1}".format(i,j),RooArgList(w.set("obs_1d")),sigHist)
        sigPdf = RooHistPdf("sigPdf_{0}_{1}".format(i,j),"sigPdf_{0}_{1}".format(i,j),w.set("obs_1d"),sigDataHist)
        getattr(w,'import')(sigPdf,RooFit.Silence())
        #w.Print()

        #w.factory("EXPR::signal_{0}_{1}('(@0>{2})*exp({3} + {4}*@0 + {5}*@0^2 + {6}*@0^3 + {7}*@0^4)',uncVZ)".format(i,j,targetz,eff_p0+targetz/gammact-math.log(gammact),eff_p1-1.0/gammact,eff_p2,eff_p3,eff_p4))

        #w.var("eff_p0").setVal(eff_p0+targetz/gammact-math.log(gammact))
        #w.var("eff_p1").setVal(eff_p1-1.0/gammact)
        #w.var("eff_p2").setVal(eff_p2)
        #w.var("eff_p3").setVal(eff_p3)
        #w.var("eff_p4").setVal(eff_p4)
        #w.var("eff_p0").setConstant(True)
        #w.var("eff_p1").setConstant(True)
        #w.var("eff_p2").setConstant(True)
        #w.var("eff_p3").setConstant(True)
        #w.var("eff_p4").setConstant(True)
        c.SetLogy()

        #w.factory("SUM::model_{0}_{1}(strength*sigPdf_{0}_{1},bkgPdf_{0})".format(i,j))
        #w.factory("SUM::null_{0}_{1}(nbkg*bkgPdf_{0})".format(i,j))
        w.factory("SUM::model_{0}_{1}(strength*sigPdf_{0}_{1},bkgPdf_{0})".format(i,j))
        #w.factory("SUM::null_{0}(nbkg*bkg_{0})".format(i))
        w.var("strength").setVal(0.0001)
        #w.var("nbkg").setVal(0.5*dataInRange.sumEntries())

        #modelConfig = ModelConfig("test")
        #modelConfig.SetWorkspace(w)
        #modelConfig.SetPdf("model_{0}_{1}".format(i,j))
        #modelConfig.SetParametersOfInterest("strength")
        #modelConfig.SetObservables("uncVZ")

        #plc = ProfileLikelihoodCalculator(dataPastCut2,modelConfig)
        #plc = ProfileLikelihoodCalculator(binnedData,modelConfig)

        #nullParams = w.set("poi").snapshot()
        #nullParams.setRealValue("strength",0)
        #plc.SetNullParameters(nullParams)

        #hypo = plc.GetHypoTest()
        #print "PLR p-value {0}, significance {1}".format(hypo.NullPValue(),hypo.Significance())
        #plrPvalHist.Fill(mass,10**eps,hypo.NullPValue())
        #plrSigHist.Fill(mass,10**eps,hypo.NullPValue())
        #hypo.SetPValueIsRightTail(True)

        #if gammact>length:
        uncVZ.setRange("fitRange",tailcut,50)
        #uncVZ.setRange(tailcut,50)
        #frame=uncVZ.frame()
        #frame.SetTitle(name)
        #dataPastCut2.plotOn(frame)
        thispdf = w.pdf("model_{0}_{1}".format(i,j))
        fitresult = thispdf.fitTo(dataPastCut2,RooFit.Range("fitRange"),RooFit.PrintLevel(-1),RooFit.Save())
        sigNLL = fitresult.minNll()
        #thispdf.plotOn(frame,RooFit.Range("fitRange"),RooFit.NormRange("fitRange"))
        #thispdf.paramOn(frame)
        #frame.SetMinimum(0.1)
        #frame.Draw()
        #c.Print(remainder[0]+".pdf","Title:test2")
        print "bkg-only NLL {0}, sig+bkg NLL {1}".format(bkgNLL,sigNLL)
        logplrHist.Fill(mass,10**eps,bkgNLL-sigNLL)




        #signalCdf = w.pdf("signal").createCdf(w.set("obs_1d"))
        #w.var("uncVZ").setVal(zcut)
        #cdfAtZcut = signalCdf.getVal()
        cdfAtZcut = exppol4.IntegralOneDim(zcut,maxz,1e-12,1e-12,ROOT.Double(blahh))
        if (no_candidates):
            dataArray=numpy.zeros(2)
            dataArray[1] = cdfAtZcut
        else:
            dataArray=numpy.zeros(dataPastCut.numEntries()+2)
            dataArray[0] = 0.0
            for k in xrange(0,dataPastCut.numEntries()):
                thisX = dataPastCut.get(k).getRealValue("uncVZ")
                w.var("uncVZ").setVal(thisX)
                #dataArray[i+1]=(signalCdf.getVal()-cdfAtZcut)
                dataArray[k+1]=(cdfAtZcut-exppol4.IntegralOneDim(thisX,maxz,1e-12,1e-12,ROOT.Double(blahh)))
                #print "thisX={0}, cdf={1}".format(thisX,dataArray[i+1])
            dataArray[dataPastCut.numEntries()+1] = cdfAtZcut
        dataArray/= (cdfAtZcut)
        dataArray.sort()
        #print dataArray
        output = upperlimit.upperlim(CL, 1, dataArray, 0., dataArray)

        prodHist.Fill(mass,10**eps,ap_yield*10**eps)
        allzHist.Fill(mass,10**eps,ap_yield*10**eps*sig_integral)
        detectableHist.Fill(mass,10**eps,ap_yield*10**eps*sig_integral*cdfAtZcut)
        gammactHist.Fill(mass,10**eps,gammact)
        limit_detectable = output[0] # this is a limit on number of detectable A' (past zcut, within mass cut)
        limit_allz = limit_detectable/(cdfAtZcut*masscut_eff) # this is a limit on number of detectable A' if we didn't have zcut or mass cut
        limit_production = limit_allz/sig_integral # limit on number of produced A'
        limit_eps = limit_production/ap_yield
        limit_scaled = limit_eps/10**eps
        print "{0} {1} {2} {3} {4}".format(limit_detectable,limit_allz,limit_production,limit_eps,limit_scaled)
        limitHist.Fill(mass,10**eps,limit_scaled)
        fcLowerHist.Fill(mass,10**eps,fcLower/cdfAtZcut/masscut_eff/sig_integral/ap_yield/10**eps)
        fcUpperHist.Fill(mass,10**eps,fcUpper/cdfAtZcut/masscut_eff/sig_integral/ap_yield/10**eps)

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
            #print "{0} {1} {2} {3}".format(mass,massArr[j],massWindowArr[i],massWindowArr[j])
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
        #graph.Write("zcut")
        c.Print(remainder[0]+".pdf","Title:test")
        nbkg = graph.GetFunction("pol2").Eval(mass)
        if nbkg<0.5:
            nbkg = 0.5
        poiBkgArr.append(nbkg)
        pval = 1.0-TMath.Prob(2*nbkg,2*int(candArr[i]))
        #if pval>0.5:
        #    pval = 0.5
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
graph.Fit("pol4")
graph.Write("zcut")
c.Print(remainder[0]+"_output.pdf","Title:test")

graph = drawGraph(massArr,zresArr,"zres","AL*")
graph.GetXaxis().SetTitle("mass [GeV]")
graph.GetYaxis().SetTitle("sigma_z [mm]")
graph.Write("zres")
c.Print(remainder[0]+"_output.pdf","Title:test")


zcutMassArr = minMassArr[:]
zcutZcutArr = zcutArr[:]
zcutMassArr.append(0.1)
zcutZcutArr.append(zcutArr[-1])
zcutMassArr.append(0.1)
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
events.Draw("uncVZ:{0}>>hnew(100,0,0.1,100,-50,50)".format(massVar),"highzcut","colz")
gDirectory.Get("hnew").SetTitle("")
zcutTcut.Draw("L")
c.Print(remainder[0]+"_output.pdf","Title:test")
events.Draw("{0}>>hnew(100,0,0.1)".format(massVar),"highzcut","colz")
c.Print(remainder[0]+"_output.pdf","Title:test")
gDirectory.Get("hnew").Fit("pol2","L")
c.Print(remainder[0]+"_output.pdf","Title:test")
c.SetLogx(1)

candRescaled2DHist.Draw("colz")
candRescaled2DHist.SetTitle("Candidate events")
candRescaled2DHist.GetXaxis().SetMoreLogLabels()
candRescaled2DHist.GetXaxis().SetTitle("mass [GeV]")
candRescaled2DHist.GetYaxis().SetTitle("background cdf")
c.Print(remainder[0]+"_output.pdf","Title:test")

graph = drawGraph(massArr,candArr,"candidate events","A*")
graph.GetYaxis().SetTitle("counts")
c.Print(remainder[0]+"_output.pdf","Title:test")
graph.Fit("pol2")
graph.Write("n_candidates")
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
drawHist(fcLowerHist,20,1,1e3)
c.Print(remainder[0]+"_output.pdf","Title:tada")
drawContour(fcUpperHist,3)
c.Print(remainder[0]+"_output.pdf","Title:tada")
drawContour(limitHist,3)
c.Print(remainder[0]+"_output.pdf","Title:tada")
drawMaxContour(detectableHist,3)
c.Print(remainder[0]+"_output.pdf","Title:tada")

drawHist(detectableHist,20,1e-2,2.4)
c.Print(remainder[0]+"_output.pdf","Title:tada")

drawHist(allzHist,20,1e-2,1e2)
c.Print(remainder[0]+"_output.pdf","Title:tada")

drawContour(gammactHist,4)
c.Print(remainder[0]+"_output.pdf","Title:tada")

drawHist(prodHist,20,1e-2,1e2)
c.Print(remainder[0]+"_output.pdf","Title:tada")

drawContour(plrPvalHist,3)
c.Print(remainder[0]+"_output.pdf","Title:tada")

drawHist(plrSigHist,20,1e-2,1e2)
c.Print(remainder[0]+"_output.pdf","Title:tada")

#c.SetLogz(0)
drawHist(logplrHist,20,1e-2,1e2)
c.Print(remainder[0]+"_output.pdf","Title:tada")

#c.SetLogy(0)
#candHist.Draw()
#c.Print(remainder[0]+"_output.pdf","Title:tada")
#outfile.cd()


c.Print(remainder[0]+"_output.pdf]")
outfile.Write()
outfile.Close()
sys.exit(0)

