#!/usr/bin/env python
import sys, array,math
import getopt
import ROOT
from ROOT import gROOT, TCanvas, TF1, TFile, gStyle, TFormula, TGraph, TGraphErrors, TLegend, TH1D, TCutG, TH2D, gDirectory, RooDataSet, RooRealVar, RooArgSet, RooFormulaVar, RooWorkspace, RooAbsData, RooGlobalFunc, RooFit, RooAbsReal, RooArgList, gPad, TLatex, TH1F

def print_usage():
    print "\nUsage: {0} <output basename> <input ROOT file>".format(sys.argv[0])
    print "Arguments: "
    print '\t-n: width of mass bins in nsigma (default is 2.80)'
    print '\t-m: shift mean (default false)'
    print '\t-r: is L1L2 (default false)'
    print '\t-t: is L2L2 (default false)'
    print '\t-s: scale factor (default is 1)'
    print '\t-z: expected number of events at zcut (default is 0.5)'
    print '\t-g: number of sigma to plot fit error (default is 1)'
    print '\t-y: add label to plots'
    print '\t-p: plot max z (default true)'
    print '\t-h: this help message'
    print "\n"

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'nmrtz:s:y:g:ph')

massVar = "uncM"
#masscut_nsigma = 2.80
masscut_nsigma = 1.90
scale = 1.
zcut_val = 0.5
shift_mean = False
nsig = 1.
label = ""
isL1L2 = False
isL2L2 = False
plotmaxZ = True

for opt, arg in options:
    if opt=='-n':
        n = float(arg)
    if opt=='-m':
        shift_mean = True
    if opt=='-r':
        isL1L2 = True
    if opt=='-t':
        isL2L2 = True
    if opt=='-z':
        zcut_val = float(arg)
    if opt=='-s':
        scale = float(arg)
    if opt=='-y':
        label = str(arg)
    if opt=='-g':
        nsig = float(arg)
    if opt=='-p':
        plotmaxZ = False
    if opt=='-h':
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
gStyle.SetOptStat(1111)
c = TCanvas("c","c",800,600);
c.Print(remainder[0]+".pdf[")
outfile = TFile(remainder[0]+".root","RECREATE")

inFile = TFile(remainder[1])
events = inFile.Get("ntuple")

events.Draw("uncVZ:{0}>>hnew(100,0,0.2,100,-50,50)".format(massVar),"","colz")
c.Print(remainder[0]+".pdf")

fitfunc = TF1("fitfunc","[0]*exp( (((x-[1])/[2])<[3])*(-0.5*(x-[1])^2/[2]^2) + (((x-[1])/[2])>=[3])*(0.5*[3]^2-[3]*(x-[1])/[2]))",-50,50)
fitfunc.SetParName(0,"Amplitude")
fitfunc.SetParName(1,"Mean")
fitfunc.SetParName(2,"Sigma")
fitfunc.SetParName(3,"Tail Z")

fitfunc2 = TF1("fitfunc2","[0]*exp( (((x-[1])/[2])<[3])*(-0.5*(x-[1])^2/[2]^2) + (((x-[1])/[2])>=[3])*(0.5*[3]^2-[3]*(x-[1])/[2]))",-50,50)
fitfunc2.SetParName(0,"Amplitude")
fitfunc2.SetParName(1,"Mean")
fitfunc2.SetParName(2,"Sigma")
fitfunc2.SetParName(3,"Tail Z")

fitfunc3 = TF1("fitfunc3","[0]*exp( (((x-[1])/[2])<[3])*(-0.5*(x-[1])^2/[2]^2) + (((x-[1])/[2])>=[3])*(0.5*[3]^2-[3]*(x-[1])/[2]))",-50,50)
fitfunc3.SetParName(0,"Amplitude")
fitfunc3.SetParName(1,"Mean")
fitfunc3.SetParName(2,"Sigma")
fitfunc3.SetParName(3,"Tail Z")

if(isL1L2):
    mresf = TF1("mresf","{0}+{1}*x+{2}*x^2+{3}*x^3+{4}*x^4".format(0.8427/1000,0.04709,-0.2067,2.087,-5.584),0.04,0.2)
    label = label + " L1L2"
elif(isL2L2):
    mresf = TF1("mresf","{0}+{1}*x+{2}*x^2+{3}*x^3+{4}*x^4".format(1.005/1000,0.04436,-0.1,1.117,-2.893),0.04,0.2)
    label = label + " L2L2"
else:
    #mresf = TF1("mresf","{0}+{1}*x+{2}*x^2+{3}*x^3+{4}*x^4+{5}*x^5".format(0.01095/1000.,0.04305,0,0,0,0),0.04,0.2)
    #mresf = TF1("mresf","{0}+{1}*x+{2}*x^2+{3}*x^3+{4}*x^4".format(-0.6066/1000,0.1123,-1.452,11.55,-30.76),0.04,0.2)
    #mresf = TF1("mresf","{0}+{1}*x+{2}*x^2+{3}*x^3+{4}*x^4".format(0.386/1000,0.06735,-0.7197,6.417,-17.63),0.04,0.2)
    mresf = TF1("mresf","{0}+{1}*x+{2}*x^2+{3}*x^3+{4}*x^4".format(0.9348/1000,0.05442,-0.5784,5.852,-17.24),0.04,0.2)
    label = label + " L1L1"

massarray=array.array('d')
zeroArr=array.array('d')
meanarray=array.array('d')
sigmaarray=array.array('d')
breakzarray=array.array('d')
zcutarray=array.array('d')
zcutscaledarray=array.array('d')
zcutarray2=array.array('d')
zcutscaledarray2=array.array('d')
zcutarray3=array.array('d')
zcutscaledarray3=array.array('d')
meanErr=array.array('d')
sigmaErr=array.array('d')
breakzErr=array.array('d')
maxZarr=array.array('d')
#zcutErr=array.array('d')
#zcutscaledErr=array.array('d')

n_massbins=50
minmass=0.04
maxmass=0.175

massWidth = (maxmass-minmass)/((n_massbins-1)*2)
histozcut = TH1F("histozcut","histozcut",n_massbins,minmass-massWidth,maxmass+massWidth)
histozcutscaled = TH1F("histozcutscaled","histozcutscaled",n_massbins,minmass,maxmass)

#mres_p0 = 1.364/1000.
#mres_p1 = 0.02608

for i in range(0,n_massbins):
    mass = minmass+i*(maxmass-minmass)/(n_massbins-1)
    massarray.append(mass)
    zeroArr.append(0)

    #mres = mres_p0 + mres_p1*mass
    mres = mresf.Eval(mass)

    if(mass > 9999):
        meanarray.append(meanarray[i-1])
        sigmaarray.append(sigmaarray[i-1])
        breakzarray.append(breakzarray[i-1])
        meanErr.append(meanErr[i-1])
        sigmaErr.append(sigmaErr[i-1])
        breakzErr.append(breakzErr[i-1])
        zcutarray.append(zcutarray[i-1])
        zcutscaledarray.append(zcutscaledarray[i-1])
        zcutarray2.append(zcutarray2[i-1])
        zcutscaledarray2.append(zcutscaledarray2[i-1])
        zcutarray3.append(zcutarray3[i-1])
        zcutscaledarray3.append(zcutscaledarray3[i-1])
        histozcut.SetBinContent(i+1,zcutarray[i])
        histozcut.SetBinError(i+1,zcutarray2[i]-zcutarray[i])
        histozcutscaled.SetBinContent(i+1,zcutscaledarray[i])
        histozcutscaled.SetBinError(i+1,zcutarray2[i]-zcutarray[i])
        if(plotmaxZ):
            cutevents = events.CopyTree("abs({0}-{1})<{2}/2*{3}".format(massVar,mass,masscut_nsigma,mres))
            maxZarr.append(cutevents.GetMaximum("uncVZ"))
        else:
            maxZarr.append(0)
        continue


    c.Clear()
    c.Divide(1,2)
    c.cd(1)
    events.Draw("uncVZ:{0}>>hnew2d(100,0,0.2,100,-50,50)".format(massVar),"abs({0}-{1})<{2}/2*{3}".format(massVar,mass,masscut_nsigma,mres),"colz")
    hnew2d = gDirectory.Get("hnew2d")
    hnew2d.SetTitle("{0:0.1f} MeV < Mass < {1:0.1f} MeV".format((mass-masscut_nsigma/2*mres)*1000,(mass+masscut_nsigma/2*mres)*1000))
    hnew2d.GetXaxis().SetTitle("Mass (GeV)")
    hnew2d.GetYaxis().SetTitle("Reconstructed z (mm)")
    c.cd(2)
    gPad.SetLogy(1)
    events.Draw("uncVZ>>hnew1d(200,-50,50)","abs({0}-{1})<{2}/2*{3}".format(massVar,mass,masscut_nsigma,mres),"")

    h1d = gDirectory.Get("hnew1d")
    fit=h1d.Fit("gaus","QS")
    peak=fit.Get().Parameter(0)
    mean=fit.Get().Parameter(1)
    sigma=fit.Get().Parameter(2)
    fit=h1d.Fit("gaus","QS","",mean-3*sigma,mean+3*sigma)
    mean=fit.Get().Parameter(1)
    sigma=fit.Get().Parameter(2)
    print("mean {0}  sigma {1}".format(mean,sigma))
    fitfunc.SetParameters(peak,mean,sigma,3)
    fit=h1d.Fit(fitfunc,"LSQIM","",mean-2*sigma,mean+10*sigma)
    outfile.cd()
    h1d.GetXaxis().SetTitle("Reconstructed z (mm)")
    h1d.GetYaxis().SetTitle("dN/dz (0.5 mm)^{-1}")
    h1d.GetXaxis().SetLabelSize(0.05)
    h1d.GetYaxis().SetLabelSize(0.05)
    h1d.GetZaxis().SetLabelSize(0.05)
    h1d.GetXaxis().SetTitleOffset(0.8)
    h1d.GetXaxis().SetTitleSize(0.06)
    h1d.GetYaxis().SetTitleOffset(0.8)
    h1d.GetYaxis().SetTitleSize(0.06)
    h1d.SetTitle("{0:0.1f} MeV < Mass < {1:0.1f} MeV {2}".format((mass-masscut_nsigma/2*mres)*1000,(mass+masscut_nsigma/2*mres)*1000,label))
    h1d.Write("{0} < uncM < {1}".format(mass-masscut_nsigma/2*mres,mass+masscut_nsigma/2*mres))
    meanarray.append(fit.Get().Parameter(1))
    sigmaarray.append(fit.Get().Parameter(2))
    breakzarray.append(fit.Get().Parameter(3))
    meanErr.append(fit.Get().ParError(1))
    sigmaErr.append(fit.Get().ParError(2))
    breakzErr.append(fit.Get().ParError(3))
    zcut = getZCut(fitfunc,zcut_val=zcut_val)
    zcut_scaled = getZCut(fitfunc,zcut_val=zcut_val,scale=scale)
    zcutarray.append(zcut)
    #zcutErr.append(0)
    zcutscaledarray.append(zcut_scaled)
    #zcutscaledErr.append(0)
    c.Print(remainder[0]+".pdf","Title:mass_{0}".format(mass))

    if(plotmaxZ):
        cutevents = events.CopyTree("abs({0}-{1})<{2}/2*{3}".format(massVar,mass,masscut_nsigma,mres))
        maxZarr.append(cutevents.GetMaximum("uncVZ"))
    else:
        maxZarr.append(0)
    c.Clear()
    c.SetLogy(1)
    fitfunc2.SetParameters(fit.Get().Parameter(0),fit.Get().Parameter(1),fit.Get().Parameter(2),fit.Get().Parameter(3)+nsig*fit.Get().ParError(3))
    zcut2 = getZCut(fitfunc2,zcut_val=zcut_val)
    zcut2_scaled = getZCut(fitfunc2,zcut_val=zcut_val,scale=scale)
    zcutarray2.append(zcut2)
    zcutscaledarray2.append(zcut2_scaled)
    fitfunc3.SetParameters(fit.Get().Parameter(0),fit.Get().Parameter(1),fit.Get().Parameter(2),fit.Get().Parameter(3)-nsig*fit.Get().ParError(3))
    zcut3 = getZCut(fitfunc3,zcut_val=zcut_val)
    zcut3_scaled = getZCut(fitfunc3,zcut_val=zcut_val,scale=scale)
    zcutarray3.append(zcut3)
    zcutscaledarray3.append(zcut3_scaled)

    h1d.Sumw2()
    h1d.Draw()
    fitfunc.SetLineColor(1)
    fitfunc2.SetLineColor(2)
    fitfunc3.SetLineColor(4)
    fitfunc.Draw("same")
    fitfunc2.Draw("same")
    fitfunc3.Draw("same")
    legend = TLegend(.10,.66,.34,.87)
    legend.SetBorderSize(0)
    legend.SetFillColor(0)
    legend.SetFillStyle(0)
    legend.SetTextFont(42)
    legend.SetTextSize(0.05)
    legend.AddEntry(fitfunc,"Nominal Fit","LP")
    legend.AddEntry(fitfunc2,"Fit +{0}#sigma".format(nsig),"LP")
    legend.AddEntry(fitfunc3,"Fit -{0}#sigma".format(nsig),"LP")
    legend.Draw()
    c.Write()
    c.Print(remainder[0]+".pdf","Title:mass_{0}".format(mass))

    histozcut.SetBinContent(i+1,zcut)
    histozcut.SetBinError(i+1,zcut2-zcut)
    histozcutscaled.SetBinContent(i+1,zcut_scaled)
    histozcutscaled.SetBinError(i+1,zcut2-zcut)

    if(shift_mean):
        c.Clear()
        events.Draw("uncVZ-{0}>>hnew1d_shift(200,-50,50)".format(fit.Get().Parameter(1)),"abs({0}-{1})<{2}/2*{3}".format(massVar,mass,masscut_nsigma,mres),"")
        h1d_shift = gDirectory.Get("hnew1d_shift")
        h1d_shift.GetXaxis().SetTitle("Reconstructed z (mm)")
        h1d_shift.GetYaxis().SetTitle("dN/dz (0.5 mm)^{-1}")
        h1d_shift.GetXaxis().SetLabelSize(0.05)
        h1d_shift.GetYaxis().SetLabelSize(0.05)
        h1d_shift.GetZaxis().SetLabelSize(0.05)
        h1d_shift.GetXaxis().SetTitleOffset(0.8)
        h1d_shift.GetXaxis().SetTitleSize(0.06)
        h1d_shift.GetYaxis().SetTitleOffset(0.8)
        h1d_shift.GetYaxis().SetTitleSize(0.06)
        h1d_shift.SetTitle("{0:0.1f} MeV < Mass < {1:0.1f} MeV: Mean Shifted {2}".format((mass-masscut_nsigma/2*mres)*1000,(mass+masscut_nsigma/2*mres)*1000,label))
        h1d_shift.Write("{0} < uncM < {1} Mean Shifted".format(mass-masscut_nsigma/2*mres,mass+masscut_nsigma/2*mres))

c.Clear()
outfile.cd()

c.SetLogy(0)
graph=TGraph(len(massarray),massarray,meanarray)
graph=TGraphErrors(len(massarray),massarray,meanarray,zeroArr,meanErr)
graph.Draw("A*")
graph.SetTitle("Fitted Mean {0}".format(label))
graph.GetXaxis().SetTitle("mass [GeV]")
graph.GetYaxis().SetTitle("mean [mm]")
graph.Fit("pol5")
graph.Write("mean")
c.Print(remainder[0]+".pdf","Title:mean")

graph=TGraph(len(massarray),massarray,sigmaarray)
graph=TGraphErrors(len(massarray),massarray,sigmaarray,zeroArr,sigmaErr)
graph.Draw("A*")
graph.SetTitle("Fitted Sigma {0}".format(label))
graph.GetXaxis().SetTitle("mass [GeV]")
graph.GetYaxis().SetTitle("sigma [mm]")
graph.Fit("pol5")
graph.Write("sigma")
c.Print(remainder[0]+".pdf","Title:sigma")

graph=TGraph(len(massarray),massarray,breakzarray)
graph=TGraphErrors(len(massarray),massarray,breakzarray,zeroArr,breakzErr)
graph.Draw("A*")
graph.SetTitle("Tail Z {0}".format(label))
graph.GetXaxis().SetTitle("mass [GeV]")
graph.GetYaxis().SetTitle("tail Z [mm]")
graph.Fit("pol5")
graph.Write("breakz")
c.Print(remainder[0]+".pdf","Title:tailz")

graph=TGraph(len(massarray),massarray,zcutarray)
#graph=TGraphErrors(len(massarray),massarray,zcutarray,zeroArr,zcutErr)
graph.Draw("A*")
graph.SetTitle("Zcut at {0:.1f} Background {1}".format(zcut_val,label))
graph.GetXaxis().SetTitle("mass [GeV]")
graph.GetYaxis().SetTitle("zcut [mm]")
graph.Fit("pol5","","",0.05,0.15)
graph.Write("zcut")
c.Print(remainder[0]+".pdf","Title:zcut")

graph=TGraph(len(massarray),massarray,zcutscaledarray)
#graph=TGraphErrors(len(massarray),massarray,zcutscaledarray,zeroArr,zcutscaledErr)
graph.Draw("A*")
graph.SetTitle("Zcut Scaled x{0:.2f} at {1:.1f} Background {2}".format(scale,zcut_val,label))
graph.GetXaxis().SetTitle("mass [GeV]")
graph.GetYaxis().SetTitle("zcut [mm]")
graph.Fit("pol5","","",0.05,0.15)
graph.Write("zcutscaled")
c.Print(remainder[0]+".pdf","Title:zcutscaled")

graph=TGraph(len(massarray),massarray,zcutarray2)
#graph=TGraphErrors(len(massarray),massarray,zcutarray,zeroArr,zcutErr)
graph.Draw("A*")
graph.SetTitle("Zcut at {0:.1f} Background +{1}#sigma {2}".format(zcut_val,nsig,label))
graph.GetXaxis().SetTitle("mass [GeV]")
graph.GetYaxis().SetTitle("zcut [mm]")
graph.Fit("pol5","","",0.05,0.15)
graph.Write("zcut2")
c.Print(remainder[0]+".pdf","Title:zcut")

graph=TGraph(len(massarray),massarray,zcutscaledarray2)
#graph=TGraphErrors(len(massarray),massarray,zcutscaledarray,zeroArr,zcutscaledErr)
graph.Draw("A*")
graph.SetTitle("Zcut Scaled x{0:.2f} at {1:.1f} Background +{2}#sigma {3}".format(scale,zcut_val,nsig,label))
graph.GetXaxis().SetTitle("mass [GeV]")
graph.GetYaxis().SetTitle("zcut [mm]")
graph.Fit("pol5","","",0.05,0.15)
graph.Write("zcutscaled2")
c.Print(remainder[0]+".pdf","Title:zcutscaled")

graph=TGraph(len(massarray),massarray,zcutarray3)
#graph=TGraphErrors(len(massarray),massarray,zcutarray,zeroArr,zcutErr)
graph.Draw("A*")
graph.SetTitle("Zcut at {0:.1f} Background -{1}#sigma {2}".format(zcut_val,nsig,label))
graph.GetXaxis().SetTitle("mass [GeV]")
graph.GetYaxis().SetTitle("zcut [mm]")
graph.Fit("pol5","","",0.05,0.15)
graph.Write("zcut3")
c.Print(remainder[0]+".pdf","Title:zcut")

graph=TGraph(len(massarray),massarray,zcutscaledarray3)
#graph=TGraphErrors(len(massarray),massarray,zcutscaledarray,zeroArr,zcutscaledErr)
graph.Draw("A*")
graph.SetTitle("Zcut Scaled x{0:.2f} at {1:.1f} Background -{2}#sigma {3}".format(scale,zcut_val,nsig,label))
graph.GetXaxis().SetTitle("mass [GeV]")
graph.GetYaxis().SetTitle("zcut [mm]")
graph.Fit("pol5","","",0.05,0.15)
graph.Write("zcutscaled3")
c.Print(remainder[0]+".pdf","Title:zcutscaled")

graph=TGraph(len(massarray),massarray,maxZarr)
graph.Draw("A*")
graph.SetTitle("Maximum Z in Mass Bin {0}".format(label))
graph.GetXaxis().SetTitle("mass [GeV]")
graph.GetYaxis().SetTitle("max Z [mm]")
graph.Write("maxZ")
c.Print(remainder[0]+".pdf","Title:maxZ")

c.Print(remainder[0]+".pdf]")
outfile.Write()
outfile.Close()

outfile2 = TFile(remainder[0]+"_zcut.root","RECREATE")

outfile2.cd()
histozcut.Write("zcut")
histozcutscaled.Write("zcutscaled")

outfile2.Close()
sys.exit(0)
