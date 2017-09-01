#!/usr/bin/env python
import sys
import array, math
import ROOT
from ROOT import gROOT, gStyle, TFile, TTree, TChain, TMVA, TCut, TCanvas, gDirectory, TH1, TH1F, TGraph, gPad, TF1, TGraphErrors, TLegend, TGaxis, TLine
import getopt


def print_usage():
    print "\nUsage:"
    print "Arguments: "
    print '\t-h: this help message'
    print "\n"

mass = 40

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'hm:')

# Parse the command line arguments
for opt, arg in options:
        if opt=='-m':
            mass = arg
        if opt=='-h':
            print_usage()
            sys.exit(0)


filename1 = "/home/mrsolt/hps/Layer0Studies/Res/tails_nominal.root"
filename2 = "/home/mrsolt/hps/Layer0Studies/Res/tails_L0.root"
filename3 = "/home/mrsolt/hps/L0Studies/nominal/2pt3/tails/Vres.root"
filename4 = "/home/mrsolt/hps/L0Studies/L0/2pt3/tails/Vres.root"
filename5 = "/home/mrsolt/hps/L0Studies/nominal/4pt4/tails/Vres.root"
filename6 = "/home/mrsolt/hps/L0Studies/L0/4pt4/tails/Vres.root"
filename7 = "/home/mrsolt/hps/L0Studies/nominal/6pt6/tails/Vres.root"
filename8 = "/home/mrsolt/hps/L0Studies/L0/6pt6/tails/Vres.root"

histoTitle = "res"

plotTitle = "Vertex Resolution Ratio Nominal/L0"

inFile1 = TFile(filename1)
inFile2 = TFile(filename2)
inFile3 = TFile(filename3)
inFile4 = TFile(filename4)
inFile5 = TFile(filename5)
inFile6 = TFile(filename6)
inFile7 = TFile(filename7)
inFile8 = TFile(filename8)

c = TCanvas("c","c",800,600);

XaxisTitle = inFile1.Get(histoTitle).GetXaxis().GetTitle();
YaxisTitle = inFile1.Get(histoTitle).GetYaxis().GetTitle();

Histo1 = inFile1.Get(histoTitle)
Histo2 = inFile2.Get(histoTitle)
Histo3 = inFile3.Get(histoTitle)
Histo4 = inFile4.Get(histoTitle)
Histo5 = inFile5.Get(histoTitle)
Histo6 = inFile6.Get(histoTitle)
Histo7 = inFile7.Get(histoTitle)
Histo8 = inFile8.Get(histoTitle)

#func1 = inFile1.Get(histoTitle).GetFunction("pol3")
#func2 = inFile2.Get(histoTitle).GetFunction("pol3")
#func3 = inFile3.Get(histoTitle).GetFunction("pol3")
#func4 = inFile4.Get(histoTitle).GetFunction("pol3")
#func5 = inFile5.Get(histoTitle).GetFunction("pol3")
#func6 = inFile6.Get(histoTitle).GetFunction("pol3")
#func7 = inFile7.Get(histoTitle).GetFunction("pol3")
#func8 = inFile8.Get(histoTitle).GetFunction("pol3")

def ratio(graph1,graph2,minmass,maxmass):
    xArr1=array.array('d')
    xArr2=array.array('d')
    yArr1=array.array('d')
    yArr2=array.array('d')
    ratio=array.array('d')

    xArr1 = graph1.GetX()
    xArr2 = graph2.GetX()
    yArr1 = graph1.GetY()
    yArr2 = graph2.GetY()

    if(len(xArr1) != len(xArr2)):
	print "Graphs are not the same length"
	return 0
    for i in range(len(xArr1)):
        if(xArr1[i] != xArr2[i]):
	    print "X arrays are NOT the same"
	    return 0
        if(yArr2[i] != 0):
	    ratio.append(yArr1[i]/float(yArr2[i]))
        else: 
	    ratio.append(0)
    ratio_graph = TGraph(len(xArr1),xArr1,ratio)
    return ratio_graph

def histo(graph):
    xArr1=array.array('d')
    yArr1=array.array('d')
    xArr1=graph.GetX()
    yArr1=graph.GetY()

    Histo = TH1F("h","h",len(xArr1),min(xArr1),max(xArr1))

    for i in range(len(xArr1)):
	Histo.SetBinContent(i+1,yArr1[i])
    
    return Histo

GraphRatio1 = ratio(Histo1,Histo2,0.021,0.06)
GraphRatio2 = ratio(Histo3,Histo4,0.041,0.120)
GraphRatio3 = ratio(Histo5,Histo6,0.081,0.240)
GraphRatio4 = ratio(Histo7,Histo8,0.121,0.320)

funcRatio1 = GraphRatio1.GetFunction("pol3")
funcRatio2 = GraphRatio2.GetFunction("pol3")
funcRatio3 = GraphRatio3.GetFunction("pol3")
funcRatio4 = GraphRatio4.GetFunction("pol3")

Graph1 = histo(Histo1)
Graph2 = histo(Histo2)
Graph3 = histo(Histo3)
Graph4 = histo(Histo4)
Graph5 = histo(Histo5)
Graph6 = histo(Histo6)
Graph7 = histo(Histo7)
Graph8 = histo(Histo8)

legend2 = TLegend(.65,.60,.89,.87)
legend2.SetBorderSize(0)
legend2.SetFillColor(0)
legend2.SetFillStyle(0)
legend2.SetTextFont(42)
legend2.SetTextSize(0.035)
legend2.AddEntry(Graph1,"1.05 GeV nominal","LP")
legend2.AddEntry(Graph3,"2.3 GeV nominal","LP")
legend2.AddEntry(Graph5,"4.4 GeV nominal","LP")
legend2.AddEntry(Graph7,"6.6 GeV nominal","LP")
legend2.AddEntry(Graph2,"1.05 GeV L0","LP")
legend2.AddEntry(Graph4,"2.3 GeV L0","LP")
legend2.AddEntry(Graph6,"4.4 GeV L0","LP")
legend2.AddEntry(Graph8,"6.6 GeV L0","LP")

histodumb = TH1F("histodumb","histodumb",2,0.015,0.340)
histodumb.Draw("")
histodumb.GetXaxis().SetRangeUser(0.015,0.340)
histodumb.GetYaxis().SetRangeUser(0,6.5)
histodumb.SetTitle("VZ Resolution")
histodumb.GetXaxis().SetTitle(XaxisTitle)
histodumb.GetYaxis().SetTitle("Vz Resolution")
histodumb.SetStats(0)


Graph1.Draw("samePC")
Graph1.SetMarkerColor(1)
Graph1.SetLineColor(1)
#Graph1.SetLineStyle(3)
Graph1.SetMarkerStyle(3)
Graph2.Draw("samePC")
Graph2.SetMarkerColor(2)
Graph2.SetLineColor(2)
Graph2.SetMarkerStyle(3)

Graph3.Draw("samePC")
Graph3.SetMarkerColor(1)
Graph3.SetLineColor(1)
Graph3.SetMarkerStyle(8)
Graph4.Draw("samePC")
Graph4.SetMarkerColor(2)
Graph4.SetLineColor(2)
Graph4.SetMarkerStyle(8)

Graph5.Draw("samePC")
Graph5.SetMarkerColor(1)
Graph5.SetLineColor(1)
Graph5.SetMarkerStyle(21)
Graph6.Draw("samePC")
Graph6.SetMarkerColor(2)
Graph6.SetLineColor(2)
Graph6.SetMarkerStyle(21)

Graph7.Draw("samePC")
Graph7.SetMarkerColor(1)
Graph7.SetLineColor(1)
Graph7.SetMarkerStyle(22)
Graph8.Draw("samePC")
Graph8.SetMarkerColor(2)
Graph8.SetLineColor(2)
Graph8.SetMarkerStyle(22)

c.SetLogx(1)
c.Update()

legend2.Draw()
c.Print("VZ_Resolution_total.pdf","Title:histoTitle")


c.Clear()

legend = TLegend(.65,.66,.89,.87)
legend.SetBorderSize(0)
legend.SetFillColor(0)
legend.SetFillStyle(0)
legend.SetTextFont(42)
legend.SetTextSize(0.035)
legend.AddEntry(GraphRatio1,"1.05 GeV","LP")
legend.AddEntry(GraphRatio2,"2.3 GeV","LP")
legend.AddEntry(GraphRatio3,"4.4 GeV","LP")
legend.AddEntry(GraphRatio4,"6.6 GeV","LP")

xdumb=array.array('d')
ydumb=array.array('d')

xdumb.append(0)
xdumb.append(0.330)
ydumb.append(0)
ydumb.append(0)

graphdumb = TGraph(2,xdumb,ydumb)
graphdumb.Draw("")
graphdumb.GetXaxis().SetRangeUser(0.015,0.340)
graphdumb.GetYaxis().SetRangeUser(0,4)
graphdumb.SetTitle(plotTitle)
graphdumb.GetXaxis().SetTitle(XaxisTitle)
graphdumb.GetYaxis().SetTitle("Vz Resolution Ratio")
#graphdumb.SetStats(0)

GraphRatio1.Draw("*sameL")
GraphRatio1.SetTitle(plotTitle)
#GraphRatio1.GetXaxis().SetRangeUser(0,0.14)
#GraphRatio1.GetYaxis().SetRangeUser(0,5)
#GraphRatio1.SetRangeX(0,0.14)
#GraphRatio1.SetRangeY(0,5)
#GraphRatio1.GetXaxis().SetTitle(XaxisTitle)
#GraphRatio1.GetYaxis().SetTitle("Vz Resolution Ratio")
#funcRatio1.Draw("same")
#funcRatio1.SetLineColor(1)
GraphRatio2.Draw("*sameL")
GraphRatio2.SetMarkerColor(2)
#funcRatio2.Draw("same")
#funcRatio2.SetLineColor(2)
GraphRatio3.Draw("*sameL")
GraphRatio3.SetMarkerColor(4)
GraphRatio4.Draw("*sameL")
GraphRatio4.SetMarkerColor(3)
#funcRatio3.Draw("same")
#funcRatio3.SetLineColor(4)

c.SetLogx(1)
c.Update()

legend.Draw()
c.Print("VZ_Resolution_ratio.pdf","Title:histoTitle")
