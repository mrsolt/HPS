#!/usr/bin/env python
import sys, array,math
import getopt
import ROOT
from ROOT import gROOT, TCanvas, TF1, TFile, gStyle, TFormula, TGraph, TGraphErrors, TLegend, TH1D, TCutG, TH2D, gDirectory, RooDataSet, RooRealVar, RooArgSet, RooFormulaVar, RooWorkspace, RooAbsData, RooGlobalFunc, RooFit, RooAbsReal, RooArgList, gPad, TLatex, TH1F, TLine, TGaxis

def print_usage():
    print "\nUsage: {0} <output basename> <input ROOT file>".format(sys.argv[0])
    print "Arguments: "
    print '\t-n: width of mass bins in nsigma (default is 2.80)'
    print '\t-m: shift mean (default false)'
    print '\t-r: is L1L2 (default false)'
    print '\t-s: scale factor (default is 1)'
    print '\t-z: expected number of events at zcut (default is 0.5)'
    print '\t-g: number of sigma to plot fit error (default is 1)'
    print '\t-y: add label to plots'
    print '\t-h: this help message'
    print "\n"

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'nmrz:s:y:g:h')

massVar = "uncM"
#masscut_nsigma = 2.80
masscut_nsigma = 1.90
scale = 1.
zcut_val = 0.5
shift_mean = False
nsig = 1.
label = ""
isL1L2 = False

for opt, arg in options:
    if opt=='-n':
        n = float(arg)
    if opt=='-m':
        shift_mean = True
    if opt=='-r':
        isL1L2 = True
    if opt=='-z':
        zcut_val = float(arg)
    if opt=='-s':
        scale = float(arg)
    if opt=='-y':
        label = str(arg)
    if opt=='-g':
        nsig = float(arg)
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
#gStyle.SetOptFit(0)
#gStyle.SetOptStat(0)
gStyle.SetOptFit(1)
gStyle.SetOptStat(1111)
c = TCanvas("c","c",800,600);
c.Print(remainder[0]+".pdf[")
outfile = TFile(remainder[0]+".root","RECREATE")

inFile = TFile(remainder[1])
events = inFile.Get("ntuple")

inFile2 = TFile(remainder[2])
apevents = inFile2.Get("ntuple")

fitfunc = TF1("fitfunc","[0]*exp( (((x-[1])/[2])<[3])*(-0.5*(x-[1])^2/[2]^2) + (((x-[1])/[2])>=[3])*(0.5*[3]^2-[3]*(x-[1])/[2]))",-50,50)
fitfunc.SetParName(0,"Amplitude")
fitfunc.SetParName(1,"Mean")
fitfunc.SetParName(2,"Sigma")
fitfunc.SetParName(3,"Tail Z")

mresf = TF1("mresf","{0}+{1}*x+{2}*x^2+{3}*x^3+{4}*x^4".format(0.9348/1000,0.05442,-0.5784,5.852,-17.24),0.04,0.2)
apevents.Draw("triM>>histoMass({0},{1},{2})".format(1000,0,1))
histoMass = ROOT.gROOT.FindObject("histoMass")
mass = histoMass.GetMean()
#mass = 0.100
mres = mresf.Eval(mass)

events.Draw("uncVZ>>Data(100,-30,70)","abs({0}-{1})<{2}/2*{3}".format(massVar,mass,masscut_nsigma,mres),"")
h1d = gDirectory.Get("Data")
h1d.Sumw2()
h1d.GetXaxis().SetTitle("Reconstructed z (mm)")
h1d.GetYaxis().SetTitle("dN/dz [1/mm]")
h1d.SetTitle("Reconstructed Z for {0:0.0f} MeV #pm {1:0.1f} MeV Mass Slice {2}".format(mass*1000,(masscut_nsigma/2*mres)*1000,label))
fit=h1d.Fit("gaus","QS")
peak=fit.Get().Parameter(0)
mean=fit.Get().Parameter(1)
sigma=fit.Get().Parameter(2)
fit=h1d.Fit("gaus","QS","",mean-3*sigma,mean+3*sigma)
mean=fit.Get().Parameter(1)
sigma=fit.Get().Parameter(2)
print("mean {0}  sigma {1}".format(mean,sigma))

fitfunc3 = TF1("fitfunc2","gaus",-30,70)
fitfunc3.SetParameters(fit.Get().Parameter(0),mean,sigma)

fitfunc.SetParameters(peak,mean,sigma,3)
fit2 = h1d.Fit(fitfunc,"LSQIM","",mean-2*sigma,mean+10*sigma)
fitfunc2 = TF1("fitfunc2","[0]*exp( (((x-[1])/[2])<[3])*(-0.5*(x-[1])^2/[2]^2) + (((x-[1])/[2])>=[3])*(0.5*[3]^2-[3]*(x-[1])/[2]))",fit2.Get().Parameter(3),70)
fitfunc2.SetParName(0,"Amplitude")
fitfunc2.SetParName(1,"Mean")
fitfunc2.SetParName(2,"Sigma")
fitfunc2.SetParName(3,"Tail Z")
fitfunc2.SetParameters(fit2.Get().Parameter(0),fit2.Get().Parameter(1),fit2.Get().Parameter(2),fit2.Get().Parameter(3))
zcut = getZCut(fitfunc,zcut_val=zcut_val)

c.Clear()
c.SetLogy()

linemax = 10e2
line = TLine(zcut,0,zcut,linemax)
line.SetLineColor(1)
line.SetLineWidth(3)

nBins = 100
nBin1 = int(nBins/(70--30) * (zcut - -30))
apevents.Draw("uncVZ>>hnewap({1},-30,{0})".format(zcut,nBin1),"abs({0}-{1})<{2}/2*{3}".format(massVar,mass,masscut_nsigma,mres),"")
hnewap = gDirectory.Get("hnewap")
apevents.Draw("uncVZ>>hnewap2({1},{0},70)".format(zcut,nBins-nBin1),"abs({0}-{1})<{2}/2*{3}".format(massVar,mass,masscut_nsigma,mres),"")
hnewap2 = gDirectory.Get("hnewap2")
scale = hnewap.GetMaximum() #hnewap.GetBinContent(hnewap.GetXaxis().FindBin(-4.3))
hnewap.Sumw2()
hnewap2.Sumw2()
h1d.SetLineColor(1)
h1d.SetMarkerStyle(2)
h1d.SetMarkerColor(1)
h1d.GetYaxis().SetRangeUser(10e-2,10e5)
hnewap.SetLineColor(4)
hnewap.SetMarkerStyle(2)
hnewap.SetMarkerColor(4)
#hnewap.Scale(signal/hnewap2.Integral(hnewap.GetXaxis().FindBin(zcut),hnewap.GetXaxis().FindBin(70)))
#hnewap.Scale(signal/hnewap2.Integral())
hnewap2.SetLineColor(4)
hnewap2.SetMarkerStyle(2)
hnewap2.SetMarkerColor(4)
hnewap2.SetFillColor(5)
hnewap2.SetFillStyle(3001)
#hnewap2.Scale(signal/hnewap2.Integral())
fitfunc3.SetLineColor(1)
fitfunc3.SetLineStyle(7)
fitfunc2.SetLineColor(2)
fitfunc3.SetMarkerColor(1)
fitfunc2.SetMarkerColor(2)
h1d.Draw()
fitfunc3.Draw("same")
fitfunc2.Draw("same")
line.Draw("same")
hnewap.Draw("same")
hnewap2.Draw("hist e same")
legend = TLegend(.58,.32,.82,.53)
legend.SetBorderSize(0)
legend.SetFillColor(0)
legend.SetFillStyle(0)
legend.SetTextFont(42)
legend.SetTextSize(0.035)
legend.AddEntry(h1d,"Data","LP")
legend.AddEntry(hnewap,"{0:0.0f} MeV A'".format(mass*1000),"LP")
legend.AddEntry(fitfunc3,"Gaussian Core Fit","L")
legend.AddEntry(fitfunc2,"Exponential Tail Fit","L")
legend.AddEntry(line,"z_{cut} @ 1/2 Background","L")
legend.Draw("same")

hnewap.Scale(1/scale)
hnewap2.Scale(1/scale)
print hnewap.GetMaximum()
rightmax = 5.0#*hnewap.GetMaximum()
scale2 = 10#rightmax #gPad.GetUymax()/rightmax
hnewap.Scale(scale2)
hnewap2.Scale(scale2)
hnewap.Draw("same")

#axis = TGaxis(gPad.GetUxmax(),gPad.GetUymin(),gPad.GetUxmax(), gPad.GetUymax(),0,rightmax,510,"+L")
axis = TGaxis(70,gPad.GetUymin(),70, 50,10e-3,rightmax,510,"+LG")
#axis.SetLogy(1)
axis.SetLabelColor(4)
axis.SetLineColor(4)
axis.SetTextColor(4)
axis.SetTitle("Relative Efficiency")
axis.Draw()

c.SetLogy(1)

c.Print(remainder[0]+".pdf")

c.Print(remainder[0]+".pdf]")

outfile.cd()

sys.exit(0)