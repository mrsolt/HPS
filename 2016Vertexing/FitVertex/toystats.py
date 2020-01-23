#!/usr/bin/env python
import sys, array,math
import getopt
import ROOT
from ROOT import gROOT, TCanvas, TF1, TFile, gStyle, TFormula, TGraph, TGraphErrors, TH1D, TCutG, TH2D, RooDataSet, TFeldmanCousins, TLegend
from ROOT.RooStats import ModelConfig, ProfileLikelihoodCalculator, LikelihoodIntervalPlot, FrequentistCalculator, FeldmanCousins, AsymptoticCalculator
import upperlimit
import numpy

def print_usage():
    print "\nUsage: {0} <output basename>".format(sys.argv[0])
    print "Arguments: "
    print "\n"

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'n:s:j:h')

cutfile=""

n = 10000
bkg_lambda = 2
junk_lambda = 5
sig_lambda = 20
signal_strength = 0.001
junk_strength = 0.01
CL = 0.9

for opt, arg in options:
    if opt=='-n':
        n = int(arg)
    elif opt=='-s':
        signal_strength = float(arg)
    elif opt=='-j':
        junk_strength = float(arg)
    elif opt=='-h':
        print_usage()
        sys.exit(0)


if (len(remainder)!=1):
        print_usage()
        sys.exit()

print "{0} events, signal fraction {1}, junk fraction {2}".format(n,signal_strength,junk_strength)

c = TCanvas("c","c",800,600);
c.Print(remainder[0]+".pdf[")
w = ROOT.RooWorkspace("w")

w.factory("Exponential::bkg(x[0,100],{0})".format(-1.0/bkg_lambda))
#w.factory("Gaussian::bkg(x[-50,50],0,3)")
w.factory("Exponential::junk(x,{0})".format(-1.0/junk_lambda))

w.factory("Exponential::signal(x,{0})".format(-1.0/sig_lambda))
#w.factory("EXPR::signal_step('x>0?1:0',x)")
#w.factory("Gaussian::signal_res(x,0,3)")
#w.factory("PROD::signal(signal_decay,signal_step)")
#w.factory("FCONV::signal(x,signal_truth,signal_res)")
w.factory("SUM::source(strength[{0},0,0.005]*signal,{1}*junk,bkg)".format(signal_strength,junk_strength))
w.factory("SUM::model(strength*signal,bkg)")
w.defineSet("obs","x")
w.defineSet("poi","strength")

modelConfig = ModelConfig("test")
modelConfig.SetWorkspace(w)
modelConfig.SetPdf("model")
modelConfig.SetParametersOfInterest("strength")
modelConfig.SetObservables("x")

pdf = w.pdf("model")

#data= pdf.generate(w.set("obs"),n)
data= w.pdf("source").generate(w.set("obs"),n)

plc = ProfileLikelihoodCalculator(data,modelConfig)

nullParams = w.set("poi").snapshot()
nullParams.setRealValue("strength",0)
plc.SetNullParameters(nullParams)

hypo = plc.GetHypoTest()
#hypo.SetPValueIsRightTail(True)
print "PLR p-value {0}, significance {1}".format(hypo.NullPValue(),hypo.Significance())


plc.SetConfidenceLevel(CL)
interval = plc.GetInterval()
interval.Print()
print "likelihood interval: [{0}, {1}]".format(n*interval.LowerLimit(w.var("strength")), n*interval.UpperLimit(w.var("strength")))
#likelihoodPlot = LikelihoodIntervalPlot(interval)
#likelihoodPlot.SetNPoints(100)
#likelihoodPlot.SetRange(0,0.005)
#likelihoodPlot.Draw()
#c.Print(remainder[0]+".pdf","Title:test")

zcutArr=array.array('d')
limitArr=array.array('d')
limitBkgArr=array.array('d')
fractionArr=array.array('d')
countArr=array.array('d')
expectArr=array.array('d')
fcLowerArr=array.array('d')
fcUpperArr=array.array('d')
fcUpperNobkgArr=array.array('d')

fc = TFeldmanCousins()
fc.SetCL(CL)
fc.SetMuMax(100)
signalCdf = w.pdf("signal").createCdf(w.set("obs"))
bkgCdf = w.pdf("bkg").createCdf(w.set("obs"))

print "zcut for 0.5 events = {0}".format(bkg_lambda*math.log(n/0.5))

zcut_count = 10
zcut = bkg_lambda*math.log(n/zcut_count)
print zcut
sigCdfHist = TH1D("sigCdfHist","sigCdfHist",100,0,1.0)
w.var("x").setVal(zcut)
cdfAtZcut = signalCdf.getVal()
bkgCdfAtZcut = bkgCdf.getVal()
dataPastCut = data.reduce(w.set("obs"),"x>{0}".format(zcut))
for i in xrange(0,dataPastCut.numEntries()):
    thisX = dataPastCut.get(i).getRealValue("x")
    w.var("x").setVal(thisX)
    sigCdfHist.Fill((signalCdf.getVal()-cdfAtZcut)/(1.0-cdfAtZcut))
sigCdfHist.Draw()
sigCdfHist.SetTitle("Points for optimum interval test")
sigCdfHist.GetXaxis().SetTitle("x/mu")
c.Print(remainder[0]+".pdf","Title:test")



for i in xrange(0,100):
    #zcut_count = 0.1+0.1*i
    #zcut = bkg_lambda*math.log(n/zcut_count)

    zcut = 11+0.5*i
    zcut_count = n/math.exp(zcut/bkg_lambda)
    eventsPastZcut = data.sumEntries("x>{0}".format(zcut))
    fcLower = fc.CalculateLowerLimit(eventsPastZcut,zcut_count)
    fcUpper = fc.CalculateUpperLimit(eventsPastZcut,zcut_count)

    fcUpper_nobkg = fc.CalculateUpperLimit(eventsPastZcut,0.0)

    #print "zcut {0} for {1} past zcut, got {2} past zcut, FC limits [{3} {4}]".format(zcut,zcut_count,eventsPastZcut,fcLower,fcUpper)

    #w.factory("n[0,100]")
    #w.defineSet("n","n")

    #w.factory("b[{0}]".format(zcut_count))
    #w.factory("prod::yield(strength,{0})".format(n*math.exp(-zcut/sig_lambda)))
    #w.factory("sum::mean(b,yield)")
    #w.factory("Poisson::pois(n,mean)")
    #w.var("n").setVal(eventsPastZcut)
    #countData = RooDataSet("countData","countData",w.set("n"))
    #countData.add(w.set("n"))

    #countData.Print("v")

    #fcModel = ModelConfig("fcProblem",w)
    #fcModel.SetPdf(w.pdf("pois"))
    #fcModel.SetParametersOfInterest("strength")
    #fcModel.SetObservables(w.set("n"))
    #fc = FeldmanCousins(countData,fcModel)
    #fc.SetTestSize(0.05)
    #fc.UseAdaptiveSampling(True)
    #fc.FluctuateNumDataEntries(False)
    #fc.SetNBins(100)
    #fcInterval = fc.GetInterval()
    #print "F-C interval: [{0},{1}]".format(fcInterval.LowerLimit(w.var("strength")),fcInterval.UpperLimit(w.var("strength")))

    w.var("x").setVal(zcut)
    cdfAtZcut = signalCdf.getVal()
    bkgCdfAtZcut = bkgCdf.getVal()
    dataPastCut = data.reduce(w.set("obs"),"x>{0}".format(zcut))
    dataArray=numpy.zeros(dataPastCut.numEntries()+2)
    bkgArray=numpy.zeros(dataPastCut.numEntries()+2)
    dataArray[0] = 0.0
    bkgArray[0] = 0.0
    for i in xrange(0,dataPastCut.numEntries()):
        thisX = dataPastCut.get(i).getRealValue("x")
        w.var("x").setVal(thisX)
        dataArray[i+1]=(signalCdf.getVal()-cdfAtZcut)
        bkgArray[i+1]=(bkgCdf.getVal()-bkgCdfAtZcut)
    dataArray[dataPastCut.numEntries()+1] = 1.0-cdfAtZcut
    bkgArray[dataPastCut.numEntries()+1] = 1.0-bkgCdfAtZcut
    dataArray/= (1.0-cdfAtZcut)
    bkgArray/= (1.0-bkgCdfAtZcut)
    dataArray.sort()
    bkgArray.sort()
    #print "zcut {0} data {1}".format(zcut,dataArray)
    output = upperlimit.upperlim(CL, 1, dataArray, 0., dataArray)
    rawlimit = output[0]
    if output[1]==256:
	    rawlimit = upperlimit.upperlimcom.exclude_low[0]
    limit = rawlimit/(1.0-cdfAtZcut)
    limitArr.append(limit)

    outputBkg = upperlimit.upperlim(CL, 1, dataArray, zcut_count, bkgArray)
    #print outputBkg
    rawlimitBkg = outputBkg[0]
    if outputBkg[1]==256:
	    rawlimitBkg = upperlimit.upperlimcom.exclude_low[0]
    if outputBkg[1]!=0:
        print outputBkg
    bkglimit = rawlimitBkg/(1.0-cdfAtZcut)
    limitBkgArr.append(bkglimit)


    zcutArr.append(zcut)
    countArr.append(eventsPastZcut)
    expectArr.append(zcut_count)
    fractionArr.append(1.0-cdfAtZcut)
    fcLowerArr.append(fcLower/(1.0-cdfAtZcut))
    fcUpperArr.append(fcUpper/(1.0-cdfAtZcut))
    fcUpperNobkgArr.append(fcUpper_nobkg/(1.0-cdfAtZcut))
    #print output
    #print "zcut = {0}, expect {1} past zcut, got {2} past zcut, signal fraction past zcut = {3}, limit = {4}".format(zcut,zcut_count,eventsPastZcut,1.0-cdfAtZcut,limit)

graph=TGraph(len(zcutArr),zcutArr,fcUpperArr)
graph.GetXaxis().SetTitle("zcut")
graph.GetYaxis().SetRangeUser(0,100)
graph.SetTitle("Feldman-Cousins upper limit")
graph.Draw("AL*")
c.Print(remainder[0]+".pdf","Title:test")

graph=TGraph(len(zcutArr),zcutArr,fcLowerArr)
graph.GetXaxis().SetTitle("zcut")
graph.GetYaxis().SetRangeUser(0,100)
graph.SetTitle("Feldman-Cousins lower limit")
graph.Draw("AL*")
c.Print(remainder[0]+".pdf","Title:test")

graph=TGraph(len(zcutArr),zcutArr,limitArr)
graph.GetXaxis().SetTitle("zcut")
graph.GetYaxis().SetRangeUser(0,100)
graph.SetTitle("Optimum interval limit")
graph.Draw("AL*")
c.Print(remainder[0]+".pdf","Title:test")

leg = TLegend(0.1,0.75,0.5,0.9)
graph=TGraph(len(zcutArr),zcutArr,fcUpperArr)
graph.GetXaxis().SetTitle("zcut")
graph.GetYaxis().SetTitle("limit [events]")
graph.GetYaxis().SetRangeUser(0,50)
graph.SetTitle("Upper limits")
leg.AddEntry(graph,"Feldman-Cousins upper limit, background subtracted")
graph.Draw("AL*")
fcngraph=TGraph(len(zcutArr),zcutArr,fcUpperNobkgArr)
fcngraph.SetLineColor(3)
fcngraph.SetMarkerColor(3)
leg.AddEntry(fcngraph,"Feldman-Cousins upper limit, no background subtraction")
fcngraph.Draw("L*")
oigraph=TGraph(len(zcutArr),zcutArr,limitArr)
oigraph.SetLineColor(2)
oigraph.SetMarkerColor(2)
leg.AddEntry(oigraph,"Optimum interval upper limit, no background subtraction")
oigraph.Draw("L*")
oibgraph=TGraph(len(zcutArr),zcutArr,limitBkgArr)
oibgraph.SetLineColor(4)
oibgraph.SetMarkerColor(4)
leg.AddEntry(oibgraph,"Optimum interval upper limit, background subtracted")
oibgraph.Draw("L*")
leg.Draw()
c.Print(remainder[0]+".pdf","Title:test")

leg = TLegend(0.1,0.75,0.5,0.9)
fcngraph=TGraph(len(zcutArr),zcutArr,fcUpperNobkgArr)
fcngraph.SetLineColor(3)
fcngraph.SetMarkerColor(3)
fcngraph.GetXaxis().SetTitle("zcut")
fcngraph.GetYaxis().SetTitle("limit [events]")
fcngraph.GetYaxis().SetRangeUser(0,50)
fcngraph.SetTitle("Upper limits")
leg.AddEntry(fcngraph,"Feldman-Cousins upper limit")
fcngraph.Draw("AL*")
oigraph=TGraph(len(zcutArr),zcutArr,limitArr)
oigraph.SetLineColor(2)
oigraph.SetMarkerColor(2)
leg.AddEntry(oigraph,"Optimum interval upper limit")
oigraph.Draw("L*")
leg.Draw()
c.Print(remainder[0]+".pdf","Title:test")


graph=TGraph(len(zcutArr),zcutArr,countArr)
graph.SetTitle("Events past zcut")
graph.GetXaxis().SetTitle("zcut")
graph.GetYaxis().SetRangeUser(0,20)
graph.Draw("AL*")
c.Print(remainder[0]+".pdf","Title:test")

graph=TGraph(len(zcutArr),zcutArr,fractionArr)
graph.SetTitle("Signal efficiency")
graph.GetXaxis().SetTitle("zcut")
graph.GetYaxis().SetRangeUser(0,1)
graph.Draw("AL*")
c.Print(remainder[0]+".pdf","Title:test")

c.SetLogy(1)
graph=TGraph(len(zcutArr),zcutArr,expectArr)
graph.SetTitle("Expected events past zcut")
graph.GetXaxis().SetTitle("zcut")
#graph.GetYaxis().SetRangeUser(0,0.01)
graph.Draw("AL*")
c.Print(remainder[0]+".pdf","Title:test")
c.SetLogy(0)


w.var("strength").setVal(signal_strength)
frame=w.var("x").frame()
c.SetLogy()
data.plotOn(frame)
#fitresult = pdf.fitTo(data)
w.pdf("source").plotOn(frame)
frame.SetMinimum(0.1)
frame.Draw()
c.Print(remainder[0]+".pdf","Title:test2")
#data = w.pdf("g").generate(w.set("

#fcalc = FrequentistCalculator(data,"signal","bkg")
c.Print(remainder[0]+".pdf]")
