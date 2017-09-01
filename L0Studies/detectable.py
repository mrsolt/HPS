#!/usr/bin/env python
import sys
import array, math
import ROOT
from ROOT import gROOT, gStyle, TFile, TTree, TChain, TMVA, TCut, TCanvas, gDirectory, TH1, TGraph, gPad, TF1, TGraphErrors, TLegend, TGaxis, TLine, TH1F
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


filename20_L0 = TFile("/home/mrsolt/hps/Vertexing/L0/1pt05/ap/truth/acceptance/acceptance_20_truth.root")
filename30_L0 = TFile("/home/mrsolt/hps/Vertexing/L0/1pt05/ap/truth/acceptance/acceptance_30_truth.root")
filename40_L0 = TFile("/home/mrsolt/hps/Vertexing/L0/1pt05/ap/truth/acceptance/acceptance_40_truth.root")
filename50_L0 = TFile("/home/mrsolt/hps/Vertexing/L0/1pt05/ap/truth/acceptance/acceptance_50_truth.root")
filename60_L0 = TFile("/home/mrsolt/hps/Vertexing/L0/1pt05/ap/truth/acceptance/acceptance_60_truth.root")
filename70_L0 = TFile("/home/mrsolt/hps/Vertexing/L0/1pt05/ap/truth/acceptance/acceptance_70_truth.root")
filename80_L0 = TFile("/home/mrsolt/hps/Vertexing/L0/1pt05/ap/truth/acceptance/acceptance_80_truth.root")
filename90_L0 = TFile("/home/mrsolt/hps/Vertexing/L0/1pt05/ap/truth/acceptance/acceptance_90_truth.root")
filename20_nom = TFile("/home/mrsolt/hps/Vertexing/nominal/1pt05/ap/truth/acceptance/acceptance_20_truth.root")
filename30_nom = TFile("/home/mrsolt/hps/Vertexing/nominal/1pt05/ap/truth/acceptance/acceptance_30_truth.root")
filename40_nom = TFile("/home/mrsolt/hps/Vertexing/nominal/1pt05/ap/truth/acceptance/acceptance_40_truth.root")
filename50_nom = TFile("/home/mrsolt/hps/Vertexing/nominal/1pt05/ap/truth/acceptance/acceptance_50_truth.root")
filename60_nom = TFile("/home/mrsolt/hps/Vertexing/nominal/1pt05/ap/truth/acceptance/acceptance_60_truth.root")
filename70_nom = TFile("/home/mrsolt/hps/Vertexing/nominal/1pt05/ap/truth/acceptance/acceptance_70_truth.root")
filename80_nom = TFile("/home/mrsolt/hps/Vertexing/nominal/1pt05/ap/truth/acceptance/acceptance_80_truth.root")
filename90_nom = TFile("/home/mrsolt/hps/Vertexing/nominal/1pt05/ap/truth/acceptance/acceptance_90_truth.root")

outname = "detectable"
outname2 = outname + "_fits"
histoTitleEff = "eff"
#histoTitleProd = "prodz"

zmaxL0 = 50
zmaxnom = 100
ztarg = -5

exppol4nom = TF1("exppol4nom","exp(pol3(0))",ztarg,zmaxnom)
exppol4L0 = TF1("exppol4L0","exp(pol3(0))",ztarg,zmaxL0)
#exp = TF1("exp","expo",-5,100)
#productL0 = TF1("productL0","expo*min(exp(pol3(0)),2.)",ztarg,zmaxL0)
#product = TF1("product","expo*min(exp(pol3(0)),2.)",ztarg,zmaxnom)

zFile1 = TFile("/home/mrsolt/hps/Vertexing/L0/1pt05/ap/upperlimit/golden_massbin.root")
zFile2 = TFile("/home/mrsolt/hps/Vertexing/nominal/1pt05/ap/upperlimit/golden_massbin.root")

c = TCanvas("c","c",800,600)
#c2 = TCanvas("c2","c2",800,600);

#Histo20L0eff = filename20_L0.Get(histoTitleEff)
#Histo30L0eff = filename30_L0.Get(histoTitleEff)
#Histo40L0eff = filename40_L0.Get(histoTitleEff)
#Histo50L0eff = filename50_L0.Get(histoTitleEff)
#Histo60L0eff = filename60_L0.Get(histoTitleEff)
#Histo70L0eff = filename70_L0.Get(histoTitleEff)
#Histo80L0eff = filename80_L0.Get(histoTitleEff)
#Histo90L0eff = filename90_L0.Get(histoTitleEff)

#Histo20nomeff = filename20_nom.Get(histoTitleEff)
#Histo30nomeff = filename30_nom.Get(histoTitleEff)
#Histo40nomeff = filename40_nom.Get(histoTitleEff)
#Histo50nomeff = filename50_nom.Get(histoTitleEff)
#Histo60nomeff = filename60_nom.Get(histoTitleEff)
#Histo70nomeff = filename70_nom.Get(histoTitleEff)
#Histo80nomeff = filename80_nom.Get(histoTitleEff)
#Histo90nomeff = filename90_nom.Get(histoTitleEff)

#Histo20L0prod = filename20_L0.Get(histoTitleProd)
#Histo30L0prod = filename30_L0.Get(histoTitleProd)
#Histo40L0prod = filename40_L0.Get(histoTitleProd)
#Histo50L0prod = filename50_L0.Get(histoTitleProd)
#Histo60L0prod = filename60_L0.Get(histoTitleProd)
#Histo70L0prod = filename70_L0.Get(histoTitleProd)
#Histo80L0prod = filename80_L0.Get(histoTitleProd)
#Histo90L0prod = filename90_L0.Get(histoTitleProd)

#Histo20nomprod = filename20_nom.Get(histoTitleProd)
#Histo30nomprod = filename30_nom.Get(histoTitleProd)
#Histo40nomprod = filename40_nom.Get(histoTitleProd)
#Histo50nomprod = filename50_nom.Get(histoTitleProd)
#Histo60nomprod = filename60_nom.Get(histoTitleProd)
#Histo70nomprod = filename70_nom.Get(histoTitleProd)
#Histo80nomprod = filename80_nom.Get(histoTitleProd)
#Histo90nomprod = filename90_nom.Get(histoTitleProd)

n_massbins = 6
minmass = 0.020
maxmass = 0.070
n_epsbins = 4
mineps = 1*10**-9
maxeps = 4*10**-9
gamma = 0.95

eff_p0_L0 = array.array('d')
eff_p1_L0 = array.array('d')
eff_p2_L0 = array.array('d')
eff_p3_L0 = array.array('d')

eff_p0_nom = array.array('d')
eff_p1_nom = array.array('d')
eff_p2_nom = array.array('d')
eff_p3_nom = array.array('d')

massArr = array.array('d')

for i in range(0,n_massbins):
    massArr.append(minmass+i*(maxmass-minmass)/(n_massbins-1))
    eff_p0_L0.append(0.)
    eff_p1_L0.append(0.)
    eff_p2_L0.append(0.)
    eff_p3_L0.append(0.)
    eff_p0_nom.append(0.)
    eff_p1_nom.append(0.)
    eff_p2_nom.append(0.)
    eff_p3_nom.append(0.)

filename20_L0.Get(histoTitleEff).Fit("exppol4L0", "0")
eff_p0_L0[0] = exppol4L0.GetParameter(0)
eff_p1_L0[0] = exppol4L0.GetParameter(1)
eff_p2_L0[0] = exppol4L0.GetParameter(2)
eff_p3_L0[0] = exppol4L0.GetParameter(3)

filename30_L0.Get(histoTitleEff).Fit("exppol4L0", "0")
eff_p0_L0[1] = exppol4L0.GetParameter(0)
eff_p1_L0[1] = exppol4L0.GetParameter(1)
eff_p2_L0[1] = exppol4L0.GetParameter(2)
eff_p3_L0[1] = exppol4L0.GetParameter(3)

filename40_L0.Get(histoTitleEff).Fit("exppol4L0", "0")
eff_p0_L0[2] = exppol4L0.GetParameter(0)
eff_p1_L0[2] = exppol4L0.GetParameter(1)
eff_p2_L0[2] = exppol4L0.GetParameter(2)
eff_p3_L0[2] = exppol4L0.GetParameter(3)

filename50_L0.Get(histoTitleEff).Fit("exppol4L0", "0")
eff_p0_L0[3] = exppol4L0.GetParameter(0)
eff_p1_L0[3] = exppol4L0.GetParameter(1)
eff_p2_L0[3] = exppol4L0.GetParameter(2)
eff_p3_L0[3] = exppol4L0.GetParameter(3)

filename60_L0.Get(histoTitleEff).Fit("exppol4L0", "0")
eff_p0_L0[4] = exppol4L0.GetParameter(0)
eff_p1_L0[4] = exppol4L0.GetParameter(1)
eff_p2_L0[4] = exppol4L0.GetParameter(2)
eff_p3_L0[4] = exppol4L0.GetParameter(3)

filename70_L0.Get(histoTitleEff).Fit("exppol4L0", "0")
eff_p0_L0[5] = exppol4L0.GetParameter(0)
eff_p1_L0[5] = exppol4L0.GetParameter(1)
eff_p2_L0[5] = exppol4L0.GetParameter(2)
eff_p3_L0[5] = exppol4L0.GetParameter(3)


filename20_nom.Get(histoTitleEff).Fit("exppol4nom", "0")
eff_p0_nom[0] = exppol4nom.GetParameter(0)
eff_p1_nom[0] = exppol4nom.GetParameter(1)
eff_p2_nom[0] = exppol4nom.GetParameter(2)
eff_p3_nom[0] = exppol4nom.GetParameter(3)

filename30_nom.Get(histoTitleEff).Fit("exppol4nom", "0")
eff_p0_nom[1] = exppol4nom.GetParameter(0)
eff_p1_nom[1] = exppol4nom.GetParameter(1)
eff_p2_nom[1] = exppol4nom.GetParameter(2)
eff_p3_nom[1] = exppol4nom.GetParameter(3)

filename40_nom.Get(histoTitleEff).Fit("exppol4nom", "0")
eff_p0_nom[2] = exppol4nom.GetParameter(0)
eff_p1_nom[2] = exppol4nom.GetParameter(1)
eff_p2_nom[2] = exppol4nom.GetParameter(2)
eff_p3_nom[2] = exppol4nom.GetParameter(3)

filename50_nom.Get(histoTitleEff).Fit("exppol4nom", "0")
eff_p0_nom[3] = exppol4nom.GetParameter(0)
eff_p1_nom[3] = exppol4nom.GetParameter(1)
eff_p2_nom[3] = exppol4nom.GetParameter(2)
eff_p3_nom[3] = exppol4nom.GetParameter(3)

filename60_nom.Get(histoTitleEff).Fit("exppol4nom", "0")
eff_p0_nom[4] = exppol4nom.GetParameter(0)
eff_p1_nom[4] = exppol4nom.GetParameter(1)
eff_p2_nom[4] = exppol4nom.GetParameter(2)
eff_p3_nom[4] = exppol4nom.GetParameter(3)

filename70_nom.Get(histoTitleEff).Fit("exppol4nom", "0")
eff_p0_nom[5] = exppol4nom.GetParameter(0)
eff_p1_nom[5] = exppol4nom.GetParameter(1)
eff_p2_nom[5] = exppol4nom.GetParameter(2)
eff_p3_nom[5] = exppol4nom.GetParameter(3)

#func20nomeff = filename20_nom.Get(histoTitleEff).GetFunction("exppol4")
#func30nomeff = filename30_nom.Get(histoTitleEff).GetFunction("exppol4")
#func40nomeff = filename40_nom.Get(histoTitleEff).GetFunction("exppol4")
#func50nomeff = filename50_nom.Get(histoTitleEff).GetFunction("exppol4")
#func60nomeff = filename60_nom.Get(histoTitleEff).GetFunction("exppol4")
#func70nomeff = filename70_nom.Get(histoTitleEff).GetFunction("exppol4")
#func80nomeff = filename80_nom.Get(histoTitleEff).GetFunction("exppol4")
#func90nomeff = filename90_nom.Get(histoTitleEff).GetFunction("exppol4")

#func20L0prod = filename20_L0.Get(histoTitleProd).GetFunction("exp")
#func30L0prod = filename30_L0.Get(histoTitleProd).GetFunction("exp")
#func40L0prod = filename40_L0.Get(histoTitleProd).GetFunction("exp")
#func50L0prod = filename50_L0.Get(histoTitleProd).GetFunction("exp")
#func60L0prod = filename60_L0.Get(histoTitleProd).GetFunction("exp")
#func70L0prod = filename70_L0.Get(histoTitleProd).GetFunction("exp")
#func80L0prod = filename80_L0.Get(histoTitleProd).GetFunction("exp")
#func90L0prod = filename90_L0.Get(histoTitleProd).GetFunction("exp")

#func20nomprod = filename20_nom.Get(histoTitleProd).GetFunction("exp")
#func30nomprod = filename30_nom.Get(histoTitleProd).GetFunction("exp")
#func40nomprod = filename40_nom.Get(histoTitleProd).GetFunction("exp")
#func50nomprod = filename50_nom.Get(histoTitleProd).GetFunction("exp")
#func60nomprod = filename60_nom.Get(histoTitleProd).GetFunction("exp")
#func70nomprod = filename70_nom.Get(histoTitleProd).GetFunction("exp")
#func80nomprod = filename80_nom.Get(histoTitleProd).GetFunction("exp")
#func90nomprod = filename90_nom.Get(histoTitleProd).GetFunction("exp")


#func20L0 = ("func20L0eff*func20L0eff",ztarg,zmaxL0)
#func30L0 = ("func30L0eff*func30L0eff",ztarg,zmaxL0)
#func40L0 = ("func40L0eff*func40L0eff",ztarg,zmaxL0)
#func50L0 = ("func50L0eff*func50L0eff",ztarg,zmaxL0)
#func60L0 = ("func60L0eff*func60L0eff",ztarg,zmaxL0)
#func70L0 = ("func70L0eff*func70L0eff",ztarg,zmaxL0)
#func80L0 = ("func80L0eff*func80L0eff",ztarg,zmaxL0)
#func90L0 = ("func90L0eff*func90L0eff",ztarg,zmaxL0)

#func20nom = ("func20nomeff*func20nomeff",ztarg,zmaxnom)
#func30nom = ("func30nomeff*func30nomeff",ztarg,zmaxnom)
#func40nom = ("func40nomeff*func40nomeff",ztarg,zmaxnom)
#func50nom = ("func50nomeff*func50nomeff",ztarg,zmaxnom)
#func60nom = ("func60nomeff*func60nomeff",ztarg,zmaxnom)
#func70nom = ("func70nomeff*func70nomeff",ztarg,zmaxnom)
#func80nom = ("func80nomeff*func80nomeff",ztarg,zmaxnom)
#func90nom = ("func90nomeff*func90nomeff",ztarg,zmaxnom)

deltaM = 0.001
num_pairs = gDirectory.Get("mass").GetEntries()*scale_factor
radfrac = radfracFile.Get("radfrac").GetFunction("pol3").Eval(mass)
num_rad = radfrac*num_pairs
ap_yield= 3*math.pi/(2*(1/137.0))*num_rad*(mass/deltaM)

xArr1 = array.array('d')
yArr1 = array.array('d')
yArr2 = array.array('d')
zcutL0 = array.array('d')
zcutnom = array.array('d')
detectableL0 = array.array('d')
detectablenom = array.array('d')
ratio = array.array('d')
graphL0 = [n_massbins]
graphnom = [n_massbins]
graphratio = [n_massbins]

for i in range(0,n_massbins):
    zcutL0.append(0.)
    zcutnom.append(0.)
    detectableL0.append(0.)
    detectablenom.append(0.)
    ratio.append(0.)
    graphL0.append(0)
    graphnom.append(0)
    graphratio.append(0)

xArrdum = ROOT.Double(0)
yArrdum = ROOT.Double(0)

n_bins = zFile1.Get("zcut").GetN()

for i in range (0,n_bins):
    xArr1.append(0.)
    yArr1.append(0.)
    yArr2.append(0.)


for i in range(0,n_bins):
    zFile1.Get("zcut").GetPoint(i,xArrdum,yArrdum)
    xArr1[i] = xArrdum
    yArr1[i] = yArrdum
    zFile2.Get("zcut").GetPoint(i,xArrdum,yArrdum)
    yArr2[i] = yArrdum

for i in range(0,n_massbins):
    for j in range(0,n_bins):
        #print str(i) + "   " + str(j)
        if(xArr1[j] < float(massArr[i])): continue
        else:
            zcutL0[i] = yArr1[j]
            zcutnom[i] = yArr2[j]
            break
    print str(zcutL0[i]) + "   " + str(zcutnom[i])
legend = TLegend(.18,.66,.42,.87)
legend.SetBorderSize(0)
legend.SetFillColor(0)
legend.SetFillStyle(0)
legend.SetTextFont(42)
legend.SetTextSize(0.035)

#c2.Print(outname2+".pdf[")

for i in range(0,n_epsbins):
    eps = mineps+i*(maxeps-mineps)/(n_epsbins-1)  
    for j in range(0,n_massbins):
        mass = minmass+j*(maxmass-minmass)/(n_massbins-1) 
        hbar_c = 1.973e-13
        ct = hbar_c*3.0/(mass*(1/137.036)*eps)
        gammact = hbar_c*3.0*1.056*gamma/(mass*mass*(1/137.036)*eps)
        exppol4L0.SetParameters(eff_p0_L0[j]+ztarg/gammact-math.log(gammact),eff_p1_L0[j]-1.0/gammact,eff_p2_L0[j],eff_p3_L0[j])
        #exppol4L0.Draw("")
        #exppol4L0.SetTitle("Fit " + str(mass) + "  eps = " + str(eps))
        detectableL0[j] = float(exppol4L0.IntegralOneDim(zcutL0[j]+ztarg,zmaxL0,1e-12,1e-12,ROOT.Double(0)))
        exppol4nom.SetParameters(eff_p0_nom[j]+ztarg/gammact-math.log(gammact),eff_p1_nom[j]-1.0/gammact,eff_p2_nom[j],eff_p3_nom[j])
        #exppol4nom.Draw("same")
        #exppol4nom.SetLineColor(1)
        #c2.Print(outname2+".pdf","Title:histoTitle")
        detectablenom[j] = float(exppol4nom.IntegralOneDim(zcutnom[j]+ztarg,zmaxnom,1e-12,1e-12,ROOT.Double(0)))
        if(detectablenom[j] !=0): 
	    ratio[j] = float(detectableL0[j])/float(detectablenom[j])
        else:
            ratio[j] = 0.
        print str(massArr[j]) + "   " + str(detectableL0[j])
    graphL0[i] = TGraph(n_massbins,massArr,detectableL0)
    graphnom[i] = TGraph(n_massbins,massArr,detectablenom)
    graphratio[i] = TGraph(n_massbins,massArr,ratio)
    legend.AddEntry(graphratio[i],"eps = " + str(eps),"LP")

#c2.Print(outname2+".pdf]")


#graphL0[2].Draw("")
#c.Print(outname+".pdf","Title:histoTitle")

def plot(graphs,n,XAxisTitle,plotTitle):
    for i in range(0,n):
        graphs[i].Draw("*same")
        graphs[i].SetMarkerColor(i)
        graphs[i].SetTitle(plotTitle)
        graphs[i].GetXaxis().SetTitle("Mass [GeV]");
    legend.Draw("same")
    c.Print(outname+".pdf","Title:histoTitle")
    return

c.Print(outname+".pdf[")

#graphL0[0].Draw("")
#graphL0[0].SetTitle("L0 Detectable A's")
#graphL0[0].GetXaxis().SetTitle("Mass [GeV]")
#for i in range(1,n_epsbins):
#    graphL0[i].Draw("*same")
#    graphL0[i].SetMarkerColor(i)
#legend.Draw("same")
#c.Print(outname+".pdf","Title:histoTitle")

#graphnom[0].Draw("")
#graphnom[0].SetTitle("Nominal Detectable A's")
#graphnom[0].GetXaxis().SetTitle("Mass [GeV]")
#for i in range(1,n_epsbins):
#    graphnom[i].Draw("*same")
#    graphnom[i].SetMarkerColor(i)
#legend.Draw("same")
#c.Print(outname+".pdf","Title:histoTitle")

graphratio[0].Draw("")
graphratio[0].SetMarkerColor(1)
graphratio[0].SetTitle("Ratio L0/Nominal Detectable A's")
graphratio[0].GetXaxis().SetTitle("XaxisTitle")
graphratio[0].GetYaxis().SetRangeUser(0,30)
for i in range(1,n_epsbins):
    graphratio[i].Draw("*sameL")
    graphratio[i].SetMarkerColor(i+1)
legend.Draw("same")
c.Print(outname+".pdf","Title:histoTitle")


#plot(graphL0,n_epsbins,"Mass [GeV]", "L0 Detectable A's")
#plot(graphnom,n_epsbins,"Mass [GeV]", "Nominal Detectable A's")
#plot(graphratio,n_epsbins,"Mass [GeV]", "Ratio L0/Nominal Detectable A's")

c.Print(outname+".pdf]")
