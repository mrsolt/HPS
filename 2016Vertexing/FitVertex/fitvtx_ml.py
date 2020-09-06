#!/usr/bin/env python
import sys, array, math
import getopt
import upperlimit
import numpy
import csv
import ctypes
import EffFuncs
from EffFuncs import Interpolate, getMassArray, getZArray, getEfficiency
import ROOT
from ROOT import gROOT, TTree, TCanvas, TF1, TFile, gStyle, TFormula, TGraph, TGraphErrors, TH1D, TH1F, TCutG, TH2D, gDirectory, RooDataSet, RooRealVar, RooArgSet, RooFormulaVar, RooWorkspace, RooAbsData, RooFit, RooAbsReal, RooArgList, gPad, TFeldmanCousins, RooDataHist, RooHistPdf, TMath, TLatex, TPaveText, TLegend, TLine, TNtuple
from ROOT.RooStats import ModelConfig, ProfileLikelihoodCalculator, LikelihoodIntervalPlot

def print_usage():
    print ("\nUsage: {0} <output basename> <input ROOT 2D histo file> <efficiency text file>".format(sys.argv[0]))
    print ("Arguments: ")
    print ('\t-n: ignore candidates past zcut (default false)')
    print ('\t-t: do not use target position as function of mass (default true)')
    print ('\t-z: target z (default -4.3 mm)')
    print ('\t-s: scale factor (default 1)')
    print ('\t-b: number of mass and epsilon bins (default 50)')
    print ('\t-y: add title to plots')
    print ('\t-h: this help message')
    print ("\n")


no_candidates = False
scale_factor = 1
massVar = "uncM"
label = ""

#Model and Fit Ranges
n_epsbins=50
mineps=-10.0
maxeps=-7.5
useVarTarget = True
targetz = -4.3
maxz = 90 #max Z out to where we have acceptance
masscut_eff = 0.94256

CL = 0.90
gamma = 0.965

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'ntz:s:y:b:h')
for opt, arg in options:
    if opt=='-n':
        no_candidates = True
    if opt=='-t':
        useVarTarget = False
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

def Interpolate1D(Z,z,eff):
    iZ = 0
    #Grab the index of z
    for i in range(nBins):
        if(Z < z[i]):
            iZ = i
            break
    #Check to make sure z is not out of range
    if(iZ == 0):
        print ("Z is behind target!")
        return
    iZ1 = iZ - 1
    iZ2 = iZ
    Q1 = eff[0][iZ1]
    Q2 = eff[0][iZ2]
    #Interpolate value
    interpolate = Q1 * (1-(Z-z[iZ1])/(z[iZ2]-z[iZ1])) + Q2 * (Z-z[iZ1])/(z[iZ2]-z[iZ1])
    return interpolate

gROOT.SetBatch(True)
gStyle.SetOptFit(1)
gStyle.SetOptStat(0)
c = TCanvas("c","c",800,600);
outfile = TFile(remainder[0]+".root","RECREATE")
infile = remainder[1]

massArr = array.array('d')
massArr.append(0.060)
massArr.append(0.065)
massArr.append(0.070)
massArr.append(0.075)
massArr.append(0.080)
massArr.append(0.085)
massArr.append(0.090)
massArr.append(0.095)
massArr.append(0.100)
massArr.append(0.105)
massArr.append(0.110)
massArr.append(0.115)
massArr.append(0.120)
massArr.append(0.125)
massArr.append(0.130)
massArr.append(0.135)
massArr.append(0.140)
massArr.append(0.145)
massArr.append(0.150)
n_massbins = len(massArr)

norm = array.array('d')
#norm.append(0.052)
#norm.append(0.125)
#norm.append(0.180)

#norm.append(0.000586898922519)
#norm.append(0.00209222449564)

norm.append(0.00568946879541)
norm.append(0.0113485706131)
norm.append(0.0218580007351)
norm.append(0.0353520284282)
norm.append(0.0545814179681)
norm.append(0.0861279384064)
norm.append(0.119332871896)
norm.append(0.126487661538)
norm.append(0.0890930544387)
norm.append(0.0811392272122)
norm.append(0.071955355928)
norm.append(0.0706879058697)
norm.append(0.0707820119056)
norm.append(0.0581198889013)
norm.append(0.0580413228671)
norm.append(0.0524424474695)
norm.append(0.0435950552988)
norm.append(0.0409331507515)
norm.append(0.0328941133779)

nbins = 50
minVZ = targetz
maxVZ = minVZ + 100
z = array.array('d')

#Build array of z values
for i in range(nbins):
    z.append(targetz+i*(maxVZ-targetz)/float(nbins))

gStyle.SetOptStat(1111)

radfracf = TF1("radfracf","{0}+{1}*x+{2}*x^2+{3}*x^3+{4}*x^4+{5}*x^5".format(0.1168,-1.375,10.19,9.422,-367.5,1023),0.04,0.2)
#num_pairsf = TF1("num_pairsf","exp({0}+{1}*x+{2}*x^2+{3}*x^3+{4}*x^4+{5}*x^5)".format(6.565,178,-1644,-1745,58930,-164800),0.04,0.2) #10%
num_pairsf = TF1("num_pairsf","exp({0}+{1}*x+{2}*x^2+{3}*x^3+{4}*x^4+{5}*x^5)".format(6.309,328.4,-5099,3.675e4,-1.492e5,2.724e5),0.04,0.2) #100%
targetzf = TF1("targetzf","{0}+{1}*x+{2}*x^2+{3}*x^3+{4}*x^4+{5}*x^5".format(-7.591,198,-4126,38540,-170500,291600),0.05,0.175)

xedges = array.array('d')
yedges = array.array('d')
for i in range(len(massArr)):
    xedges.append(massArr[i]*1000-2.5)
xedges.append(massArr[len(massArr)-1]*1000+2.5)
for j in range(0,n_epsbins+1):
    yedges.append(10**(mineps+(j-0.5)*(maxeps-mineps)/(n_epsbins-1)))

outfile.cd()
massArrMeV = array.array('d')
num_pairsArr = array.array('d')
targetzArr = array.array('d')
radfracArr = array.array('d')
candArrL1L1 = array.array('d')
candArrL1L1RF = array.array('d')
limitHistL1L1=TH2D("Limit Random Forest {0}".format(label),"Limit Random Forest {0}".format(label),n_massbins,xedges,n_epsbins,yedges)
detectableHistL1L1=TH2D("Expected A' Rate Random Forest {0}".format(label),"Expected A' Rate Random Forest {0}".format(label),n_massbins,xedges,n_epsbins,yedges)
limitHistL1L1RF=TH2D("OIM Limit L1L1 RF {0}".format(label),"OIM Limit L1L1 RF {0}".format(label),n_massbins,xedges,n_epsbins,yedges)
detectableHistL1L1RF=TH2D("Expected A' Rate L1L1 RF {0}".format(label),"Expected A' Rate L1L1 RF {0}".format(label),n_massbins,xedges,n_epsbins,yedges)
gammactHist=TH2D("gammact {0}".format(label),"gammact {0}".format(label),n_massbins,xedges,n_epsbins,yedges)
prodHist=TH2D("A's Produced within Prompt Acceptance {0}".format(label),"A's Produced within Prompt Acceptance {0}".format(label),n_massbins,xedges,n_epsbins,yedges)

exppol1=TF1("exppol1","exp(pol1(0))",-5,100)

histo = []
histotruth = []
c.Print(remainder[0]+"_output.pdf[")
for i in range(len(massArr)):
    mass = massArr[i]

    wL1L1 = RooWorkspace("wL1L1")
    wL1L1.factory("uncVZ[-100,100]")
    wL1L1.factory("clf[-1,1]")
    wL1L1.defineSet("myVars","uncVZ,clf")

    truthfile = TFile('/Users/matthewsolt/Documents/hps/Data2016/MachineLearning/files/tuple/ap_{0:0.0f}MeV_truth.root'.format(mass*1000))
    eventstruth = truthfile.Get("ntuple")

    eventstruth.Draw("triEndZ>>histotruth({0},{1},{2})".format(nbins,minVZ,maxVZ))
    histotruth.append(gDirectory.FindObject("histotruth"))
    histo.append(TH1F("histo","histo",nbins,minVZ,maxVZ))
    with open("/Users/matthewsolt/Documents/hps/Data2016/MachineLearning/CsvFinal/{0}_{1:0.0f}MeV_sig.csv".format(infile,mass*1000), mode='r') as output_file:
        file_reader = csv.reader(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        count = 0
        for j in file_reader:
            count = count + 1
            if(count == 1): continue
            histo[i].Fill(float(j[0]))

    textfile = open("/Users/matthewsolt/Documents/hps/Data2016/MachineLearning/Eff/{0}_{1:0.0f}MeV.eff".format(infile,mass*1000),"w")
    textfile.write(str(mass) + " ")
    textfile.write("\n")
    for j in range(len(z)):
        textfile.write(str(z[j]) + " ")
    textfile.write("\n")

    histo[i].Divide(histotruth[i])
    histo[i].Draw()
    c.Print(remainder[0]+"_output.pdf")
    histo[i].Scale(1/norm[i])
    for j in range(histo[i].GetNbinsX()):
        textfile.write(str(histo[i].GetBinContent(j+1)) + " ")

    textfile.close()

    effFileL1L1 = "/Users/matthewsolt/Documents/hps/Data2016/MachineLearning/Eff/{0}_{1:0.0f}MeV.eff".format(infile,mass*1000)
    zArrL1L1 = getZArray(effFileL1L1)
    effMatL1L1 = getEfficiency(effFileL1L1)

    file = TFile("/Users/matthewsolt/Documents/hps/Data2016/MachineLearning/OutputRoot/{0}_{1:0.0f}MeV.root".format(infile,mass*1000),"RECREATE")

    file.cd()
    events = TNtuple("ntuple","ntuple","uncVZ:clf")
    with open("/Users/matthewsolt/Documents/hps/Data2016/MachineLearning/CsvFinal/{0}_{1:0.0f}MeV_data.csv".format(infile,mass*1000), mode='r') as output_file:
        file_reader2 = csv.reader(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        count = 0
        for j in file_reader2:
            count = count + 1
            if(count == 1): continue
            events.Fill(float(j[0]),float(j[1]))

    datasetL1L1 = RooDataSet("datasetL1L1","datasetL1L1",events,wL1L1.set("myVars"),"")
    datasetL1L1RF = RooDataSet("datasetL1L1RF","datasetL1L1RF",events,wL1L1.set("myVars"),"")

    wL1L1.defineSet("obs_1dL1L1","uncVZ")
    obsL1L1 = wL1L1.set("obs_1dL1L1")
    uncVZL1L1 = wL1L1.var("uncVZ")
    uncVZL1L1.setBins(200)

    dataInRangeL1L1 = datasetL1L1.reduce(obsL1L1,"uncVZ>-9999")
    dataPastCutL1L1 = dataInRangeL1L1.reduce(wL1L1.set("obs_1dL1L1"),"uncVZ>-9999")

    dataInRangeL1L1RF = datasetL1L1RF.reduce(obsL1L1,"uncVZ>-9999")
    dataPastCutL1L1RF = dataInRangeL1L1RF.reduce(wL1L1.set("obs_1dL1L1"),"uncVZ>-9999")

    massArrMeV.append(mass*1000)
    radfrac = radfracf.Eval(mass)
    radfracArr.append(radfrac)

    if(useVarTarget):
        targetz_truth = targetzf.Eval(mass)
    else:
        targetz_truth = targetz
    targetzArr.append(targetz_truth)

    deltaM = 0.001
    num_pairs = num_pairsf.Eval(mass)*scale_factor
    num_pairsArr.append(num_pairs)
    num_rad = radfrac*num_pairs
    ap_yield= 3*math.pi/(2*(1/137.0))*num_rad*(mass/deltaM)
    print ("{0} pairs, {1} radfrac, {2} rad, {3} A'".format(num_pairs,radfrac,num_rad,ap_yield))

    n_candidatesL1L1 = dataPastCutL1L1.numEntries()
    n_candidatesL1L1RF = dataPastCutL1L1RF.numEntries()
    if (no_candidates):
        n_candidatesL1L1 = 0
        n_candidatesL1L1RF = 0
    print ("Number of Candidates L1L1: {0} {1}".format(n_candidatesL1L1,n_candidatesL1L1RF))
    candArrL1L1.append(n_candidatesL1L1)
    candArrL1L1RF.append(n_candidatesL1L1RF)
    for j in range(0,n_epsbins):
        c.Clear()
        eps = mineps+j*(maxeps-mineps)/(n_epsbins-1)
        hbar_c = 1.973e-13
        ct = hbar_c*3.0/(mass*(1/137.036)*10**eps)
        gammact = hbar_c*3.0*2.3*gamma/(mass*mass*(1/137.036)*10**eps)

        nBins = 1000
        effHistoL1L1 = TH1F("effHistoL1L1","effHistoL1L1",nBins,targetz,maxz)
        effHistoL1L1RF = TH1F("effHistoL1L1RF","effHistoL1L1RF",nBins,0.9,1.0)
        exppol1.SetParameters(targetz_truth/gammact-math.log(gammact),-1.0/gammact)
        for k in range(nBins):
            vz = (maxz-targetz)/nBins * k + targetz
            effHistoL1L1.SetBinContent(k+1,Interpolate1D(vz,zArrL1L1,effMatL1L1)*exppol1.Eval(vz))
            effHistoL1L1RF.SetBinContent(k+1,Interpolate1D(vz,zArrL1L1,effMatL1L1)*exppol1.Eval(vz))


        sig_integralL1L1 = effHistoL1L1.Integral(effHistoL1L1.GetXaxis().FindBin(targetz),effHistoL1L1.GetXaxis().FindBin(maxz),"width")
        cdfAtZcutL1L1 = effHistoL1L1.Integral(effHistoL1L1.GetXaxis().FindBin(targetz),effHistoL1L1.GetXaxis().FindBin(maxz),"width")

        sig_integralL1L1RF = effHistoL1L1RF.Integral(effHistoL1L1RF.GetXaxis().FindBin(0.9),effHistoL1L1RF.GetXaxis().FindBin(1.0),"width")
        cdfAtZcutL1L1RF = effHistoL1L1RF.Integral(effHistoL1L1RF.GetXaxis().FindBin(0.9),effHistoL1L1RF.GetXaxis().FindBin(1.0),"width")

        if (cdfAtZcutL1L1 == 0):
            cdfAtZcutL1L1 = 10**-20
        if (cdfAtZcutL1L1RF == 0):
            cdfAtZcutL1L1RF = 10**-20

        if (no_candidates):
            dataArrayL1L1=numpy.zeros(2)
            dataArrayL1L1[1] = cdfAtZcutL1L1
            dataArrayL1L1RF=numpy.zeros(2)
            dataArrayL1L1RF[1] = cdfAtZcutL1L1RF
        else:
            dataArrayL1L1=numpy.zeros(dataPastCutL1L1.numEntries()+2)
            dataArrayL1L1[0] = 0.0
            for k in range(0,dataPastCutL1L1.numEntries()):
                thisX = dataPastCutL1L1.get(k).getRealValue("uncVZ")
                wL1L1.var("uncVZ").setVal(thisX)
                dataArrayL1L1[k+1]=(cdfAtZcutL1L1-effHistoL1L1.Integral(effHistoL1L1.GetXaxis().FindBin(thisX),effHistoL1L1.GetXaxis().FindBin(maxz),"width"))
            dataArrayL1L1[dataPastCutL1L1.numEntries()+1] = cdfAtZcutL1L1

            dataArrayL1L1RF=numpy.zeros(dataPastCutL1L1RF.numEntries()+2)
            dataArrayL1L1RF[0] = 0.0
            for k in range(0,dataPastCutL1L1RF.numEntries()):
                thisX = dataPastCutL1L1RF.get(k).getRealValue("clf")
                wL1L1.var("clf").setVal(thisX)
                dataArrayL1L1RF[k+1]=(cdfAtZcutL1L1RF-effHistoL1L1RF.Integral(effHistoL1L1RF.GetXaxis().FindBin(thisX),effHistoL1L1RF.GetXaxis().FindBin(1.0),"width"))
            dataArrayL1L1RF[dataPastCutL1L1RF.numEntries()+1] = cdfAtZcutL1L1RF

        dataArrayL1L1/= (cdfAtZcutL1L1)
        dataArrayL1L1.sort()

        dataArrayL1L1RF/= (cdfAtZcutL1L1RF)
        dataArrayL1L1RF.sort()

        outputL1L1 = upperlimit.upperlim(CL, 1, dataArrayL1L1, 0., dataArrayL1L1)
        outputL1L1RF = upperlimit.upperlim(CL, 1, dataArrayL1L1RF, 0., dataArrayL1L1RF)

        for i in range(len(outputL1L1)):
            print("Output L1L1 {0}: {1}".format(i,outputL1L1[i]))
        for i in range(len(outputL1L1RF)):
            print("Output L1L1 RF {0}: {1}".format(i,outputL1L1RF[i]))
        prodHist.Fill(mass*1000,10**eps,ap_yield*10**eps)
        detectableHistL1L1.Fill(mass*1000,10**eps,ap_yield*10**eps*cdfAtZcutL1L1)
        detectableHistL1L1RF.Fill(mass*1000,10**eps,ap_yield*10**eps*cdfAtZcutL1L1RF)
        gammactHist.Fill(mass*1000,10**eps,gammact)
        limit_detectableL1L1 = outputL1L1[0] # this is a limit on number of detectable A' (past zcut, within mass cut)
        limit_allzL1L1 = limit_detectableL1L1/((cdfAtZcutL1L1/sig_integralL1L1)*masscut_eff) # this is a limit on number of detectable A' if we didn't have zcut or mass cut
        limit_productionL1L1 = limit_allzL1L1/sig_integralL1L1 # limit on number of produced A'
        limit_epsL1L1 = limit_productionL1L1/ap_yield
        limit_scaledL1L1 = limit_epsL1L1/10**eps
        print ("{0} {1} {2} {3} {4}".format(limit_detectableL1L1,limit_allzL1L1,limit_productionL1L1,limit_epsL1L1,limit_scaledL1L1))
        limitHistL1L1.Fill(mass*1000,10**eps,limit_scaledL1L1)
        limit_detectableL1L1RF = outputL1L1RF[0] # this is a limit on number of detectable A' (past zcut, within mass cut)
        limit_allzL1L1RF = limit_detectableL1L1RF/((cdfAtZcutL1L1RF/sig_integralL1L1RF)*masscut_eff) # this is a limit on number of detectable A' if we didn't have zcut or mass cut
        limit_productionL1L1RF = limit_allzL1L1RF/sig_integralL1L1RF # limit on number of produced A'
        limit_epsL1L1RF = limit_productionL1L1RF/ap_yield
        limit_scaledL1L1RF = limit_epsL1L1RF/10**eps
        print ("RF: {0} {1} {2} {3} {4}".format(limit_detectableL1L1RF,limit_allzL1L1RF,limit_productionL1L1RF,limit_epsL1L1RF,limit_scaledL1L1RF))
        limitHistL1L1RF.Fill(mass*1000,10**eps,limit_scaledL1L1RF)
        del effHistoL1L1
        del effHistoL1L1RF
    del file
    del events
    del wL1L1
    del datasetL1L1
    del eventstruth
    del textfile

outfile.cd()
#c.Print(remainder[0]+"_output.pdf[")
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

graphCand = drawGraph(massArrMeV,candArrL1L1,"Candidate Events L1L1","A*")
graphCand.GetYaxis().SetTitle("counts")
c.Print(remainder[0]+"_output.pdf","Title:test")
c.Write()

graphCand = drawGraph(massArrMeV,candArrL1L1RF,"Candidate Events L1L1 RF","A*")
graphCand.GetYaxis().SetTitle("counts")
c.Print(remainder[0]+"_output.pdf","Title:test")
c.Write()


def GetMaximum(hist):
    maxbin = hist.GetMaximumBin()
    #maxx,maxy,maxz = ROOT.Long(0), ROOT.Long(0), ROOT.Long(0)
    maxx,maxy,maxz = ctypes.c_int(), ctypes.c_int(), ctypes.c_int()
    hist.GetBinXYZ(maxbin,maxx,maxy,maxz)
    print("{0} {1} {2} {3}".format(maxbin,maxx,maxy,maxz))
    mass = hist.GetXaxis().GetBinCenter(maxx.value)
    eps = hist.GetYaxis().GetBinCenter(maxy.value)
    maximum = hist.GetBinContent(maxbin)
    print("{0} {1} {2}".format(mass,eps,maximum))
    return maximum, mass, eps

def GetMinimum(hist):
    minbin = hist.GetMinimumBin()
    #minx,miny,minz = ROOT.Long(0), ROOT.Long(0), ROOT.Long(0)
    minx,miny,minz = ctypes.c_int(), ctypes.c_int(), ctypes.c_int()
    hist.GetBinXYZ(minbin,minx,miny,minz)
    print("{0} {1} {2} {3}".format(minbin,minx,miny,minz))
    mass = hist.GetXaxis().GetBinCenter(minx.value)
    eps = hist.GetYaxis().GetBinCenter(miny.value)
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

def drawHist(hist,nlevels,minz,maxz):
    hist.SetContour(nlevels)
    hist.SetStats(0)
    hist.Draw("cont4z")
    hist.GetXaxis().SetMoreLogLabels()
    hist.GetXaxis().SetTitle("mass [MeV]")
    hist.GetYaxis().SetTitle("#epsilon^{2}")
    hist.GetZaxis().SetRangeUser(minz,maxz)

c.SetLogx(0)
c.SetLogy(1)
c.SetLogz(1)

limitHistL1L1.SetContour(20)
limitHistL1L1.SetStats(0)
minimum, mass, eps = GetMinimum(limitHistL1L1)
pt = TPaveText(0.55,0.8,0.9,0.9,"NDC")
pt.AddText("Minimum Limit is {0:0.2f} #times A' Cross Section".format(minimum))
pt.AddText("at Mass {0:0.1f} MeV and ".format(mass)+"#epsilon^{2} = "+"{0:0.2e}".format(eps))
limitLevel = array.array('d')
limitLevel.append(10)
limitHistL1L1.Draw("cont4z")
pt.Draw()
limitHistL1L1.GetXaxis().SetMoreLogLabels()
limitHistL1L1.GetXaxis().SetTitle("mass [MeV]")
limitHistL1L1.GetYaxis().SetTitle("#epsilon^{2}")
limitHistL1L1.GetXaxis().SetLabelSize(0.05)
limitHistL1L1.GetYaxis().SetLabelSize(0.05)
limitHistL1L1.GetXaxis().SetTitleOffset(0.8)
limitHistL1L1.GetXaxis().SetTitleSize(0.06)
limitHistL1L1.GetYaxis().SetTitleOffset(0.8)
limitHistL1L1.GetYaxis().SetTitleSize(0.06)
limitHistL1L1.GetZaxis().SetRangeUser(1,1e4)
limitHistL1L1.GetZaxis().SetRangeUser(1,1e4)
c.Print(remainder[0]+"_output.pdf","Title:tada")
c.Write()

c.Clear()
c.SetLogz(0)
detectableHistL1L1.SetContour(20)
detectableHistL1L1.SetStats(0)
maximum, mass, eps = GetMaximum(detectableHistL1L1)
pt4 = TPaveText(0.55,0.8,0.9,0.9,"NDC")
pt4.SetTextSize(0.03)
pt4.AddText("Maximum Detectable is {0:0.2f} events".format(maximum))
pt4.AddText("at Mass {0:0.1f} MeV and ".format(mass)+"#epsilon^{2} = "+"{0:0.2e}".format(eps))
detectableHistL1L1.Draw("cont4z")
pt4.Draw("")
detectableHistL1L1.GetXaxis().SetTitle("mass [MeV]")
detectableHistL1L1.GetYaxis().SetTitle("#epsilon^{2}")
detectableHistL1L1.GetXaxis().SetLabelSize(0.05)
detectableHistL1L1.GetYaxis().SetLabelSize(0.05)
detectableHistL1L1.GetXaxis().SetTitleOffset(0.8)
detectableHistL1L1.GetXaxis().SetTitleSize(0.06)
detectableHistL1L1.GetYaxis().SetTitleOffset(0.8)
detectableHistL1L1.GetYaxis().SetTitleSize(0.06)
detectableHistL1L1.GetZaxis().SetRangeUser(0,1.0*scale_factor)
c.Print(remainder[0]+"_output.pdf","Title:tada")
c.Write()



limitHistL1L1RF.SetContour(20)
limitHistL1L1RF.SetStats(0)
minimum, mass, eps = GetMinimum(limitHistL1L1RF)
pt2 = TPaveText(0.55,0.8,0.9,0.9,"NDC")
pt2.AddText("Minimum Limit is {0:0.2f} #times A' Cross Section".format(minimum))
pt2.AddText("at Mass {0:0.1f} MeV and ".format(mass)+"#epsilon^{2} = "+"{0:0.2e}".format(eps))
limitLevel = array.array('d')
limitLevel.append(10)
limitHistL1L1RF.Draw("cont4z")
pt2.Draw()
limitHistL1L1RF.GetXaxis().SetMoreLogLabels()
limitHistL1L1RF.GetXaxis().SetTitle("mass [MeV]")
limitHistL1L1RF.GetYaxis().SetTitle("#epsilon^{2}")
limitHistL1L1RF.GetZaxis().SetRangeUser(1,1e4)
c.Print(remainder[0]+"_output.pdf","Title:tada")
c.Write()

c.Clear()
c.SetLogz(0)
detectableHistL1L1RF.SetContour(20)
detectableHistL1L1RF.SetStats(0)
maximum, mass, eps = GetMaximum(detectableHistL1L1RF)
pt3 = TPaveText(0.55,0.8,0.9,0.9,"NDC")
pt3.SetTextSize(0.03)
pt3.AddText("Maximum Detectable is {0:0.2f} events".format(maximum))
pt3.AddText("at Mass {0:0.1f} MeV and ".format(mass)+"#epsilon^{2} = "+"{0:0.2e}".format(eps))
detectableHistL1L1RF.Draw("cont4z")
pt3.Draw("")
detectableHistL1L1RF.GetXaxis().SetTitle("mass [MeV]")
detectableHistL1L1RF.GetYaxis().SetTitle("#epsilon^{2}")
detectableHistL1L1RF.GetZaxis().SetRangeUser(0,0.1*scale_factor)
c.Print(remainder[0]+"_output.pdf","Title:tada")
c.Write()



c.SetLogz(1)

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
