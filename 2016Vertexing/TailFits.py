#!/usr/bin/env python
import sys, array,math
import getopt
import ROOT
from ROOT import gROOT, TCanvas, TF1, TFile, gStyle, TFormula, TGraph, TGraphErrors, TH1D, TCutG, TH2D, gDirectory, RooDataSet, RooRealVar, RooArgSet, RooFormulaVar, RooWorkspace, RooAbsData, RooGlobalFunc, RooFit, RooAbsReal, RooArgList, gPad

def print_usage():
    print "\nUsage: {0} <output basename> <input ROOT file>".format(sys.argv[0])
    print "Arguments: "
    print '\t-n: width of mass bins in nsigma (default is 2.80)'
    print '\t-a: scale factor (default is 1)'
    print '\t-z: expected number of events at zcut (default is 0.5)'
    print '\t-h: this help message'
    print "\n"

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'n:z:s:h')

massVar = "uncM"
masscut_nsigma = 2.80
scale = 1.
zcut_val = 0.5

for opt, arg in options:
    if opt=='-n':
        n = float(arg)
    if opt=='-z':
        zcut_val = float(arg)
    if opt=='-s':
        scale = float(arg)
    if opt=='-h':
        print_usage()
        sys.exit(0)


def getZCut(zcut_val=0.5,scale=1.0,zBin=0.01,minZ=-60,maxZ=60):
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


#fitfunc = TF1("fitfunc","exp(((x-[0])>=[2])*(pow([2]/2.0,2.0)-[2]*(x-[0])/[1]))",-60,60)
#fitfunc = TF1("fitfunc","[0]*exp( (((x-[1])/[2])<[3])*(-0.5*(x-[1])^2/[2]^2) + (((x-[1])/[2])>=[3])*(-0.5*[3]^2-[3]*(x-[1])/[2]))",-50,50)
#fitfunc = TF1("fitfunc","[0]*exp(((x-[1])>=[3])*(pow([3]/2.0,2.0)-[3]*(x-[1])/[2]))",-50,50)
#fitfunc.SetParName(0,"Amplitude")
#fitfunc.SetParName(1,"Mean")
#fitfunc.SetParName(2,"Sigma")
#fitfunc.SetParName(3,"Tail Z")

fitfunc = TF1("fitfunc","[0]*exp( ((x-[1])<[3])*(-0.5*(x-[1])^2/[2]^2) + ((x-[1])>=[3])*(-0.5*[3]^2/[2]^2-(x-[1]-[3])/[4]))",-50,50)
fitfunc.SetParName(0,"Amplitude")
fitfunc.SetParName(1,"Mean")
fitfunc.SetParName(2,"Sigma")
fitfunc.SetParName(3,"Tail Z")
fitfunc.SetParName(4,"Tail length")

massarray=array.array('d')
zeroArr=array.array('d')
meanarray=array.array('d')
sigmaarray=array.array('d')
breakzarray=array.array('d')
#lengtharray=array.array('d')
zcutarray=array.array('d')
zcutscaledarray=array.array('d')
meanErr=array.array('d')
sigmaErr=array.array('d')
breakzErr=array.array('d')
#lengthErr=array.array('d')
#zcutErr=array.array('d')
#zcutscaledErr=array.array('d')

n_massbins=50
minmass=0.04
maxmass=0.12

mres_p0 = 0.001853
mres_p1 = 0.03541

for i in range(0,n_massbins):
    mass = minmass+i*(maxmass-minmass)/(n_massbins-1)
    massarray.append(mass)
    zeroArr.append(0)

    mres = mres_p0 + mres_p1*mass

    c.Clear()
    c.Divide(1,2)
    c.cd(1)
    events.Draw("uncVZ:{0}>>hnew2d(100,0,0.2,100,-50,50)".format(massVar),"abs({0}-{1})<{2}/2*{3}".format(massVar,mass,masscut_nsigma,mres),"colz")
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
    fitfunc.SetParameters(peak,mean,sigma,3*sigma);
    fit=h1d.Fit(fitfunc,"LSQIM","",mean-2*sigma,mean+10*sigma)
    meanarray.append(fit.Get().Parameter(1))
    sigmaarray.append(fit.Get().Parameter(2))
    breakzarray.append(fit.Get().Parameter(3))
    #lengtharray.append(fit.Get().Parameter(4))
    meanErr.append(fit.Get().ParError(1))
    sigmaErr.append(fit.Get().ParError(2))
    breakzErr.append(fit.Get().ParError(3))
    #lengthErr.append(fit.Get().ParError(4))
    zcut = getZCut(zcut_val=zcut_val)
    zcut_scaled = getZCut(zcut_val=zcut_val,scale=scale)
    zcutarray.append(zcut)
    #zcutErr.append(0)
    zcutscaledarray.append(zcut_scaled)
    #zcutscaledErr.append(0)

    c.Print(remainder[0]+".pdf","Title:mass_{0}".format(mass))

c.Clear()
outfile.cd()

graph=TGraph(len(massarray),massarray,meanarray)
graph=TGraphErrors(len(massarray),massarray,meanarray,zeroArr,meanErr)
graph.Draw("A*")
graph.SetTitle("Fitted Mean")
graph.GetXaxis().SetTitle("mass [GeV]")
graph.GetYaxis().SetTitle("mean [mm]")
graph.Fit("pol3")
graph.Write("mean")
c.Print(remainder[0]+".pdf","Title:mean")

graph=TGraph(len(massarray),massarray,sigmaarray)
graph=TGraphErrors(len(massarray),massarray,sigmaarray,zeroArr,sigmaErr)
graph.Draw("A*")
graph.SetTitle("Fitted Sigma")
graph.GetXaxis().SetTitle("mass [GeV]")
graph.GetYaxis().SetTitle("sigma [mm]")
graph.Fit("pol3")
graph.Write("sigma")
c.Print(remainder[0]+".pdf","Title:sigma")

graph=TGraph(len(massarray),massarray,breakzarray)
graph=TGraphErrors(len(massarray),massarray,breakzarray,zeroArr,breakzErr)
graph.Draw("A*")
graph.SetTitle("Tail Z")
graph.GetXaxis().SetTitle("mass [GeV]")
graph.GetYaxis().SetTitle("tail Z [mm]")
graph.Fit("pol3")
graph.Write("breakz")
c.Print(remainder[0]+".pdf","Title:tailz")

#graph=TGraphErrors(len(massarray),massarray,lengtharray,zeroArr,lengthErr)
#graph.Draw("A*")
#graph.SetTitle("Tail length")
#graph.GetXaxis().SetTitle("mass [GeV]")
#graph.GetYaxis().SetTitle("tail length [mm]")
#graph.Fit("pol3")
#graph.Write("length")
#c.Print(remainder[0]+".pdf","Title:length")

graph=TGraph(len(massarray),massarray,zcutarray)
#graph=TGraphErrors(len(massarray),massarray,zcutarray,zeroArr,zcutErr)
graph.Draw("A*")
graph.SetTitle("Zcut at {0:.1f} Background".format(zcut_val))
graph.GetXaxis().SetTitle("mass [GeV]")
graph.GetYaxis().SetTitle("zcut [mm]")
graph.Fit("pol3")
graph.Write("zcut")
c.Print(remainder[0]+".pdf","Title:zcut")

graph=TGraph(len(massarray),massarray,zcutscaledarray)
#graph=TGraphErrors(len(massarray),massarray,zcutscaledarray,zeroArr,zcutscaledErr)
graph.Draw("A*")
graph.SetTitle("Zcut Scaled x{0:.2f} at {1:.1f} Background".format(scale,zcut_val))
graph.GetXaxis().SetTitle("mass [GeV]")
graph.GetYaxis().SetTitle("zcut [mm]")
graph.Fit("pol3")
graph.Write("zcutscaled")
c.Print(remainder[0]+".pdf","Title:zcutscaled")

c.Print(remainder[0]+".pdf]")
outfile.Write()
outfile.Close()
sys.exit(0)