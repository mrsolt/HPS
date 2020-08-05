import sys
tmpargv = sys.argv
sys.argv = []
import getopt
import ROOT
from ROOT import gROOT, TFile, TTree, TChain, gDirectory, TLine, gStyle, TCanvas, TLegend, TH2F
sys.argv = tmpargv

#List arguments
def print_usage():
    print "\nUsage: {0} <output file base name> <input file name>".format(sys.argv[0])
    print "Arguments: "
    print '\t-h: this help message'
    print

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'h')

# Parse the command line arguments
for opt, arg in options:
        if opt=='-h':
            print_usage()
            sys.exit(0)

gStyle.SetOptStat(0)
c = TCanvas("c","c",800,600)

outfile = remainder[0]
infile = TFile(remainder[1])

events = infile.Get("ntuple")

def tupleToHisto(events,inHisto,histo,nBins,minX,maxX):
	events.Draw("{0}>>{1}({2},{3},{4})".format(inHisto,histo,nBins,minX,maxX))
	histo = ROOT.gROOT.FindObject(histo)
	return histo

def saveTuplePlot(inHisto,nBins,minX,maxX,outfile,canvas,log=0):
	events.Draw("{0}>>({1},{2},{3})".format(inHisto,nBins,minX,maxX))
	canvas.SetLogy(log)
	canvas.Print(outfile+".pdf")

def tupleTo2DHistoSave(events,inHisto1,inHisto2,inHisto3,nBinsX,minX,maxX,nBinsY,minY,maxY,canvas,outfile,plotTitle="",XaxisTitle="",YaxisTitle="",cuts="",cuts2="",stats=0):
	events.Draw("{0}:{1}>>{2}({3},{4},{5},{6},{7},{8})".format(inHisto2,inHisto1,"histo",nBinsX,minX,maxX,nBinsY,minY,maxY),cuts)
	histo = ROOT.gROOT.FindObject("histo")
	events.Draw("{0}:{1}>>{2}({3},{4},{5},{6},{7},{8})".format(inHisto3,inHisto1,"histo2",nBinsX,minX,maxX,nBinsY,minY,maxY),cuts2)
	histo2 = ROOT.gROOT.FindObject("histo2")

	histoTot = TH2F("histoTot","histoTot",nBinsX,minX,maxX,nBinsY,minY,maxY)
	for i in range (0,nBinsX):
		for j in range (0,nBinsY):
			tot = histo.GetBinContent(i+1,j+1) + histo2.GetBinContent(i+1,j+1)
			histoTot.SetBinContent(i+1,j+1,tot)

	histoTot.Draw("COLZ")
	histoTot.SetTitle(plotTitle)
	histoTot.GetXaxis().SetTitle(XaxisTitle)
	histoTot.GetYaxis().SetTitle(YaxisTitle)
	histoTot.SetStats(stats)
	canvas.Print(outfile+".png")	

def tupleTo2DHistoSave2(events,inHisto1,inHisto2,inHisto3,inHisto4,inHisto5,nBinsX,minX,maxX,nBinsY,minY,maxY,canvas,outfile,plotTitle="",XaxisTitle="",YaxisTitle="",cuts="",cuts2="",cuts3="",cuts4="",stats=0):
	events.Draw("{0}:{1}>>{2}({3},{4},{5},{6},{7},{8})".format(inHisto2,inHisto1,"histo",nBinsX,minX,maxX,nBinsY,minY,maxY),cuts)
	histo = ROOT.gROOT.FindObject("histo")
	events.Draw("{0}:{1}>>{2}({3},{4},{5},{6},{7},{8})".format(inHisto3,inHisto1,"histo2",nBinsX,minX,maxX,nBinsY,minY,maxY),cuts2)
	histo2 = ROOT.gROOT.FindObject("histo2")
	events.Draw("{0}:{1}>>{2}({3},{4},{5},{6},{7},{8})".format(inHisto4,inHisto1,"histo3",nBinsX,minX,maxX,nBinsY,minY,maxY),cuts3)
	histo3 = ROOT.gROOT.FindObject("histo3")
	events.Draw("{0}:{1}>>{2}({3},{4},{5},{6},{7},{8})".format(inHisto5,inHisto1,"histo4",nBinsX,minX,maxX,nBinsY,minY,maxY),cuts4)
	histo4 = ROOT.gROOT.FindObject("histo4")

	histoTot = TH2F("histoTot","histoTot",nBinsX,minX,maxX,nBinsY,minY,maxY)
	for i in range (0,nBinsX):
		for j in range (0,nBinsY):
			tot = histo.GetBinContent(i+1,j+1) + histo2.GetBinContent(i+1,j+1) + histo3.GetBinContent(i+1,j+1) + histo4.GetBinContent(i+1,j+1)
			histoTot.SetBinContent(i+1,j+1,tot)

	histoTot.Draw("COLZ")
	histoTot.SetTitle(plotTitle)
	histoTot.GetXaxis().SetTitle(XaxisTitle)
	histoTot.GetYaxis().SetTitle(YaxisTitle)
	histoTot.SetStats(stats)
	canvas.Print(outfile+".png")

def tupleTo2DHistoSave3(events,inHisto1,inHisto2,inHisto3,inHisto4,inHisto5,inHisto6,inHisto7,nBinsX,minX,maxX,nBinsY,minY,maxY,canvas,outfile,plotTitle="",XaxisTitle="",YaxisTitle="",cuts="",cuts2="",cuts3="",cuts4="",cuts5="",cuts6="",stats=0):
	events.Draw("{0}:{1}>>{2}({3},{4},{5},{6},{7},{8})".format(inHisto2,inHisto1,"histo",nBinsX,minX,maxX,nBinsY,minY,maxY),cuts)
	histo = ROOT.gROOT.FindObject("histo")
	events.Draw("{0}:{1}>>{2}({3},{4},{5},{6},{7},{8})".format(inHisto3,inHisto1,"histo2",nBinsX,minX,maxX,nBinsY,minY,maxY),cuts2)
	histo2 = ROOT.gROOT.FindObject("histo2")
	events.Draw("{0}:{1}>>{2}({3},{4},{5},{6},{7},{8})".format(inHisto4,inHisto1,"histo3",nBinsX,minX,maxX,nBinsY,minY,maxY),cuts3)
	histo3 = ROOT.gROOT.FindObject("histo3")
	events.Draw("{0}:{1}>>{2}({3},{4},{5},{6},{7},{8})".format(inHisto5,inHisto1,"histo4",nBinsX,minX,maxX,nBinsY,minY,maxY),cuts4)
	histo4 = ROOT.gROOT.FindObject("histo4")
	events.Draw("{0}:{1}>>{2}({3},{4},{5},{6},{7},{8})".format(inHisto6,inHisto1,"histo5",nBinsX,minX,maxX,nBinsY,minY,maxY),cuts5)
	histo5 = ROOT.gROOT.FindObject("histo5")
	events.Draw("{0}:{1}>>{2}({3},{4},{5},{6},{7},{8})".format(inHisto7,inHisto1,"histo6",nBinsX,minX,maxX,nBinsY,minY,maxY),cuts6)
	histo6 = ROOT.gROOT.FindObject("histo6")

	histoTot = TH2F("histoTot","histoTot",nBinsX,minX,maxX,nBinsY,minY,maxY)
	for i in range (0,nBinsX):
		for j in range (0,nBinsY):
			tot = histo.GetBinContent(i+1,j+1) + histo2.GetBinContent(i+1,j+1) + histo3.GetBinContent(i+1,j+1) + histo4.GetBinContent(i+1,j+1) + histo5.GetBinContent(i+1,j+1) + histo6.GetBinContent(i+1,j+1)
			histoTot.SetBinContent(i+1,j+1,tot)

	histoTot.Draw("COLZ")
	histoTot.SetTitle(plotTitle)
	histoTot.GetXaxis().SetTitle(XaxisTitle)
	histoTot.GetYaxis().SetTitle(YaxisTitle)
	histoTot.SetStats(stats)
	canvas.Print(outfile+".png")	

def tupleTo2DHistoSave4(events,inHisto1,inHisto2,inHisto3,inHisto4,inHisto5,inHisto6,inHisto7,inHisto8,inHisto9,inHisto10,inHisto11,inHisto12,inHisto13,nBinsX,minX,maxX,nBinsY,minY,maxY,canvas,outfile,plotTitle="",XaxisTitle="",YaxisTitle="",cuts="",cuts2="",cuts3="",cuts4="",cuts5="",cuts6="",cuts7="",cuts8="",cuts9="",cuts10="",cuts11="",cuts12="",stats=0):
	events.Draw("{0}:{1}>>{2}({3},{4},{5},{6},{7},{8})".format(inHisto2,inHisto1,"histo",nBinsX,minX,maxX,nBinsY,minY,maxY),cuts)
	histo = ROOT.gROOT.FindObject("histo")
	events.Draw("{0}:{1}>>{2}({3},{4},{5},{6},{7},{8})".format(inHisto3,inHisto1,"histo2",nBinsX,minX,maxX,nBinsY,minY,maxY),cuts2)
	histo2 = ROOT.gROOT.FindObject("histo2")
	events.Draw("{0}:{1}>>{2}({3},{4},{5},{6},{7},{8})".format(inHisto4,inHisto1,"histo3",nBinsX,minX,maxX,nBinsY,minY,maxY),cuts3)
	histo3 = ROOT.gROOT.FindObject("histo3")
	events.Draw("{0}:{1}>>{2}({3},{4},{5},{6},{7},{8})".format(inHisto5,inHisto1,"histo4",nBinsX,minX,maxX,nBinsY,minY,maxY),cuts4)
	histo4 = ROOT.gROOT.FindObject("histo4")
	events.Draw("{0}:{1}>>{2}({3},{4},{5},{6},{7},{8})".format(inHisto6,inHisto1,"histo5",nBinsX,minX,maxX,nBinsY,minY,maxY),cuts5)
	histo5 = ROOT.gROOT.FindObject("histo5")
	events.Draw("{0}:{1}>>{2}({3},{4},{5},{6},{7},{8})".format(inHisto7,inHisto1,"histo6",nBinsX,minX,maxX,nBinsY,minY,maxY),cuts6)
	histo6 = ROOT.gROOT.FindObject("histo6")
	events.Draw("{0}:{1}>>{2}({3},{4},{5},{6},{7},{8})".format(inHisto8,inHisto1,"histo7",nBinsX,minX,maxX,nBinsY,minY,maxY),cuts7)
	histo7 = ROOT.gROOT.FindObject("histo7")
	events.Draw("{0}:{1}>>{2}({3},{4},{5},{6},{7},{8})".format(inHisto9,inHisto1,"histo8",nBinsX,minX,maxX,nBinsY,minY,maxY),cuts8)
	histo8 = ROOT.gROOT.FindObject("histo8")
	events.Draw("{0}:{1}>>{2}({3},{4},{5},{6},{7},{8})".format(inHisto10,inHisto1,"histo9",nBinsX,minX,maxX,nBinsY,minY,maxY),cuts9)
	histo9 = ROOT.gROOT.FindObject("histo9")
	events.Draw("{0}:{1}>>{2}({3},{4},{5},{6},{7},{8})".format(inHisto11,inHisto1,"histo10",nBinsX,minX,maxX,nBinsY,minY,maxY),cuts10)
	histo10 = ROOT.gROOT.FindObject("histo10")
	events.Draw("{0}:{1}>>{2}({3},{4},{5},{6},{7},{8})".format(inHisto12,inHisto1,"histo11",nBinsX,minX,maxX,nBinsY,minY,maxY),cuts11)
	histo11 = ROOT.gROOT.FindObject("histo11")
	events.Draw("{0}:{1}>>{2}({3},{4},{5},{6},{7},{8})".format(inHisto13,inHisto1,"histo12",nBinsX,minX,maxX,nBinsY,minY,maxY),cuts12)
	histo12 = ROOT.gROOT.FindObject("histo12")

	histoTot = TH2F("histoTot","histoTot",nBinsX,minX,maxX,nBinsY,minY,maxY)
	for i in range (0,nBinsX):
		for j in range (0,nBinsY):
			tot = histo.GetBinContent(i+1,j+1) + histo2.GetBinContent(i+1,j+1) + histo3.GetBinContent(i+1,j+1) + histo4.GetBinContent(i+1,j+1) + histo5.GetBinContent(i+1,j+1) + histo6.GetBinContent(i+1,j+1) +  histo7.GetBinContent(i+1,j+1) + histo8.GetBinContent(i+1,j+1) + histo9.GetBinContent(i+1,j+1) + histo10.GetBinContent(i+1,j+1) + histo11.GetBinContent(i+1,j+1) + histo12.GetBinContent(i+1,j+1)
			histoTot.SetBinContent(i+1,j+1,tot)

	histoTot.Draw("COLZ")
	histoTot.SetTitle(plotTitle)
	histoTot.GetXaxis().SetTitle(XaxisTitle)
	histoTot.GetYaxis().SetTitle(YaxisTitle)
	histoTot.SetStats(stats)

	canvas.Print(outfile+".png")

def tupleTo2DHistoSave5(events,inHisto1,inHisto2,inHisto3,inHisto4,inHisto5,inHisto6,inHisto7,inHisto8,inHisto9,nBinsX,minX,maxX,nBinsY,minY,maxY,canvas,outfile,plotTitle="",XaxisTitle="",YaxisTitle="",cuts="",cuts2="",cuts3="",cuts4="",cuts5="",cuts6="",cuts7="",cuts8="",stats=0):
	events.Draw("{0}:{1}>>{2}({3},{4},{5},{6},{7},{8})".format(inHisto2,inHisto1,"histo",nBinsX,minX,maxX,nBinsY,minY,maxY),cuts)
	histo = ROOT.gROOT.FindObject("histo")
	events.Draw("{0}:{1}>>{2}({3},{4},{5},{6},{7},{8})".format(inHisto3,inHisto1,"histo2",nBinsX,minX,maxX,nBinsY,minY,maxY),cuts2)
	histo2 = ROOT.gROOT.FindObject("histo2")
	events.Draw("{0}:{1}>>{2}({3},{4},{5},{6},{7},{8})".format(inHisto4,inHisto1,"histo3",nBinsX,minX,maxX,nBinsY,minY,maxY),cuts3)
	histo3 = ROOT.gROOT.FindObject("histo3")
	events.Draw("{0}:{1}>>{2}({3},{4},{5},{6},{7},{8})".format(inHisto5,inHisto1,"histo4",nBinsX,minX,maxX,nBinsY,minY,maxY),cuts4)
	histo4 = ROOT.gROOT.FindObject("histo4")
	events.Draw("{0}:{1}>>{2}({3},{4},{5},{6},{7},{8})".format(inHisto6,inHisto1,"histo5",nBinsX,minX,maxX,nBinsY,minY,maxY),cuts5)
	histo5 = ROOT.gROOT.FindObject("histo5")
	events.Draw("{0}:{1}>>{2}({3},{4},{5},{6},{7},{8})".format(inHisto7,inHisto1,"histo6",nBinsX,minX,maxX,nBinsY,minY,maxY),cuts6)
	histo6 = ROOT.gROOT.FindObject("histo6")
	events.Draw("{0}:{1}>>{2}({3},{4},{5},{6},{7},{8})".format(inHisto8,inHisto1,"histo7",nBinsX,minX,maxX,nBinsY,minY,maxY),cuts7)
	histo7 = ROOT.gROOT.FindObject("histo7")
	events.Draw("{0}:{1}>>{2}({3},{4},{5},{6},{7},{8})".format(inHisto9,inHisto1,"histo8",nBinsX,minX,maxX,nBinsY,minY,maxY),cuts8)
	histo8 = ROOT.gROOT.FindObject("histo8")

	histoTot = TH2F("histoTot","histoTot",nBinsX,minX,maxX,nBinsY,minY,maxY)
	for i in range (0,nBinsX):
		for j in range (0,nBinsY):
			tot = histo.GetBinContent(i+1,j+1) + histo2.GetBinContent(i+1,j+1) + histo3.GetBinContent(i+1,j+1) + histo4.GetBinContent(i+1,j+1) + histo5.GetBinContent(i+1,j+1) + histo6.GetBinContent(i+1,j+1) +  histo7.GetBinContent(i+1,j+1) + histo8.GetBinContent(i+1,j+1)
			histoTot.SetBinContent(i+1,j+1,tot)

	histoTot.Draw("COLZ")
	histoTot.SetTitle(plotTitle)
	histoTot.GetXaxis().SetTitle(XaxisTitle)
	histoTot.GetYaxis().SetTitle(YaxisTitle)
	histoTot.SetStats(stats)

	canvas.Print(outfile+".png")

def saveTuple2DPlot(inHisto1,inHisto2,nBinsX,minX,maxX,nBinsY,minY,maxY,outfile,canvas,cuts="",opts="",log=0):
	events.Draw("{0}:{1}>>({2},{3},{4},{5},{6},{7})".format(inHisto2,inHisto1,nBinsX,minX,maxX,nBinsY,minY,maxY),cuts,opts)
	canvas.SetLogy(log)
	canvas.Print(outfile+".pdf")

def openPDF(outfile,canvas):
	canvas.Print(outfile+".pdf[")

def closePDF(outfile,canvas):
	canvas.Print(outfile+".pdf]")

thetaRange = 0.025
zMax = 50

tupleTo2DHistoSave(events,"uncVZ","-(eleL1tthetaY+eleL2tthetaY)","eleL1bthetaY+eleL2bthetaY",50,-30,zMax,50,-thetaRange,thetaRange,c,outfile+"_L1elescattering","L1 Electron Scattering Angle vs Vertex Z","uncVZ [mm]","theta_y [away from beam]","")

tupleTo2DHistoSave5(events,"uncVZ","-(eleL1tInthetaY+eleL2tthetaY)+(posL1bthetaY+posL2bthetaY)","-(eleL1tInthetaY+eleL2tInthetaY)+(posL1bthetaY+posL2bthetaY)",
	"(eleL1bInthetaY+eleL2bthetaY)-(posL1tthetaY+posL2tthetaY)","(eleL1bInthetaY+eleL2bInthetaY)+(posL1tthetaY+posL2tthetaY)",
	"-(posL1tInthetaY+posL2tthetaY)+(eleL1bthetaY+eleL2bthetaY)","-(posL1tInthetaY+posL2tInthetaY)+(eleL1bthetaY+eleL2bthetaY)",
	"(posL1bInthetaY+posL2bthetaY)-(eleL1tthetaY+eleL2tthetaY)","(posL1bInthetaY+posL2bInthetaY)+(eleL1tthetaY+eleL2tthetaY)",
	50,-30,zMax,50,-thetaRange,thetaRange,c,outfile+"_L1eleposInscattering","L1 Electron Inactive/Active - Positron Active/Inactive Scattering Angle vs Vertex Z","uncVZ [mm]","theta_y [away from beam]",
	"(eleL1tInthetaY+eleL2tthetaY)>-9998&&(posL1bthetaY+posL2bthetaY)>-9998&&!eleHasL1","(eleL1tInthetaY+eleL2tInthetaY)>-9998&&(posL1bthetaY+posL2bthetaY)>-9998&&!eleHasL1",
	"(eleL1bInthetaY+eleL2bthetaY)>-9998&&(posL1tthetaY+posL2tthetaY)>-9998&&!eleHasL1","(eleL1bInthetaY+eleL2bInthetaY)>-9998&&(posL1tthetaY+posL2tthetaY)>-9998&&!eleHasL1",
	"(posL1tInthetaY+posL2tthetaY)>-9998&&(eleL1bthetaY+eleL2bthetaY)>-9998&&!posHasL1","(posL1tInthetaY+posL2tInthetaY)>-9998&&(eleL1bthetaY+eleL2bthetaY)>-9998&&!posHasL1",
	"(posL1bInthetaY+posL2bthetaY)>-9998&&(eleL1tthetaY+eleL2tthetaY)>-9998&&!posHasL1","(posL1bInthetaY+posL2bInthetaY)>-9998&&(eleL1tthetaY+eleL2tthetaY)>-9998&&!posHasL1")

tupleTo2DHistoSave(events,"uncVZ","-(posL1tthetaY+posL2tthetaY)","posL1bthetaY+posL2bthetaY",50,-30,zMax,50,-thetaRange,thetaRange,c,outfile+"_L1posscattering","L1 Positron Scattering Angle vs Vertex Z","uncVZ [mm]","theta_y [away from beam]","")
tupleTo2DHistoSave(events,"uncVZ","-((eleL1tthetaY+eleL2tthetaY)-(posL1bthetaY+posL2bthetaY))","(eleL1bthetaY+eleL2bthetaY)-(posL1tthetaY+posL2tthetaY)",50,-30,zMax,50,-thetaRange,thetaRange,c,outfile+"_L1eleposscattering","L1 Electron - Positron Scattering Angle vs Vertex Z","uncVZ [mm]","theta_y [away from beam]","(eleL1tthetaY+eleL2tthetaY)>-9998&&(posL1bthetaY+posL2bthetaY)>-9998","(eleL1bthetaY+eleL2bthetaY)>-9998&&(posL1tthetaY+posL2tthetaY)>-9998")
tupleTo2DHistoSave2(events,"uncVZ","-(eleL1tInthetaY+eleL2tthetaY)","eleL1bInthetaY+eleL2bthetaY","-(eleL1tInthetaY+eleL2tInthetaY)","(eleL1bInthetaY+eleL2bInthetaY)",50,-30,zMax,50,-thetaRange,thetaRange,c,outfile+"_L1eledeadscattering","L1 Electron Inactive Scattering Angle vs Vertex Z","uncVZ [mm]","theta_y [away from beam]","")
tupleTo2DHistoSave3(events,"uncVZ","-(eleL1tInthetaY+eleL2tthetaY)","eleL1bInthetaY+eleL2bthetaY","-(eleL1tInthetaY+eleL2tInthetaY)","(eleL1bInthetaY+eleL2bInthetaY)","-(eleL1tthetaY+eleL2tthetaY)","(eleL1bthetaY+eleL2bthetaY)",50,-30,zMax,50,-thetaRange,thetaRange,c,outfile+"_L1eledeadscattering2","L1 Electron Scattering Angle vs Vertex Z","uncVZ [mm]","theta_y [away from beam]","")
tupleTo2DHistoSave2(events,"uncVZ","-(posL1tInthetaY+posL2tthetaY)","posL1bInthetaY+posL2bthetaY","-(posL1tInthetaY+posL2tInthetaY)","(posL1bInthetaY+posL2bInthetaY)",50,-30,zMax,50,-thetaRange,thetaRange,c,outfile+"_L1posdeadscattering","L1 Positron Inactive Scattering Angle vs Vertex Z","uncVZ [mm]","theta_y [away from beam]","")
tupleTo2DHistoSave3(events,"uncVZ","-(posL1tInthetaY+posL2tthetaY)","posL1bInthetaY+posL2bthetaY","-(posL1tInthetaY+posL2tInthetaY)","(posL1bInthetaY+posL2bInthetaY)","-(posL1tthetaY+eleL2tthetaY)","(posL1bthetaY+posL2bthetaY)",50,-30,zMax,50,-thetaRange,thetaRange,c,outfile+"_L1posdeadscattering2","L1 Positron Scattering Angle vs Vertex Z","uncVZ [mm]","theta_y [away from beam]","")

tupleTo2DHistoSave4(events,"uncVZ","-((eleL1tInthetaY+eleL2tthetaY)-(posL1bthetaY+posL2bthetaY))","-((eleL1tInthetaY+eleL2tInthetaY)-(posL1bthetaY+posL2bthetaY))",
	"-((eleL1tInthetaY+eleL2tInthetaY)-(posL1bInthetaY+posL2bthetaY))","-((eleL1tInthetaY+eleL2tInthetaY)-(posL1bInthetaY+posL2bInthetaY))",
	"-((eleL1tInthetaY+eleL2tthetaY)-(posL1tInthetaY+posL2tthetaY))","-((eleL1tInthetaY+eleL2tthetaY)-(posL1tInthetaY+posL2tInthetaY))",
	"-((posL1tInthetaY+posL2tthetaY)-(eleL1bthetaY+eleL2bthetaY))","-((posL1tInthetaY+posL2tInthetaY)-(eleL1bthetaY+eleL2bthetaY))",
	"-((posL1tInthetaY+posL2tInthetaY)-(eleL1bInthetaY+eleL2bthetaY))","-((posL1tInthetaY+posL2tInthetaY)-(eleL1bInthetaY+eleL2bInthetaY))",
	"-((posL1tInthetaY+posL2tthetaY)-(eleL1tInthetaY+eleL2tthetaY))","-((posL1tInthetaY+posL2tthetaY)-(eleL1tInthetaY+eleL2tInthetaY))",
	50,-30,zMax,50,-thetaRange,thetaRange,c,outfile+"_L1eleposdeadscattering",
	"L1 Electron - Positron Scattering Angle vs Vertex Z","uncVZ [mm]","theta_y [away from beam]",
	"(eleL1tInthetaY+eleL2tthetaY)>-9998&&(posL1bthetaY+posL2bthetaY)>-9998","(eleL1tInthetaY+eleL2tInthetaY)>-9998&&(posL1bthetaY+posL2bthetaY)>-9998",
	"(eleL1tInthetaY+eleL2tInthetaY)>-9998&&(posL1bInthetaY+posL2bthetaY)>-9998","(eleL1tInthetaY+eleL2tthetaY)>-9998&&(posL1bInthetaY+posL2bInthetaY)>-9998",
	"(eleL1tInthetaY+eleL2tthetaY)>-9998&&(posL1bInthetaY+posL2bthetaY)>-9998","(eleL1tInthetaY+eleL2tthetaY)>-9998&&(posL1bInthetaY+posL2bInthetaY)>-9998",
	"(posL1tInthetaY+posL2tthetaY)>-9998&&(eleL1bthetaY+eleL2bthetaY)>-9998","(posL1tInthetaY+posL2tInthetaY)>-9998&&(eleL1bthetaY+eleL2bthetaY)>-9998",
	"(posL1tInthetaY+posL2tInthetaY)>-9998&&(eleL1bInthetaY+eleL2bthetaY)>-9998","(posL1tInthetaY+posL2tthetaY)>-9998&&(eleL1bInthetaY+eleL2bInthetaY)>-9998",
	"(posL1tInthetaY+posL2tthetaY)>-9998&&(eleL1bInthetaY+eleL2bthetaY)>-9998","(posL1tInthetaY+posL2tthetaY)>-9998&&(eleL1bInthetaY+eleL2bInthetaY)>-9998",
	)

openPDF(outfile,c)
saveTuple2DPlot("uncM","uncVZ",50,0,0.1,50,50,50,outfile,c,"","COLZ")
#saveTuple2DPlot("eleL1tthetaX","eleL1tthetaY",50,-thetaRange,thetaRange,50,-thetaRange,thetaRange,outfile,c,"","COLZ")
#saveTuple2DPlot("eleL1bthetaX","eleL1bthetaY",50,-thetaRange,thetaRange,50,-thetaRange,thetaRange,outfile,c,"","COLZ")
#saveTuple2DPlot("posL1tthetaX","posL1tthetaY",50,-thetaRange,thetaRange,50,-thetaRange,thetaRange,outfile,c,"","COLZ")
#saveTuple2DPlot("posL1bthetaX","posL1bthetaY",50,-thetaRange,thetaRange,50,-thetaRange,thetaRange,outfile,c,"","COLZ")
#saveTuple2DPlot("eleL2tthetaX","eleL2tthetaY",50,-thetaRange,thetaRange,50,-thetaRange,thetaRange,outfile,c,"","COLZ")
#saveTuple2DPlot("eleL2bthetaX","eleL2bthetaY",50,-thetaRange,thetaRange,50,-thetaRange,thetaRange,outfile,c,"","COLZ")
#saveTuple2DPlot("posL2tthetaX","posL2tthetaY",50,-thetaRange,thetaRange,50,-thetaRange,thetaRange,outfile,c,"","COLZ")
#saveTuple2DPlot("posL2bthetaX","posL2bthetaY",50,-thetaRange,thetaRange,50,-thetaRange,thetaRange,outfile,c,"","COLZ")
#saveTuple2DPlot("eleL1tthetaX","eleL2tthetaY",50,-thetaRange,thetaRange,50,-thetaRange,thetaRange,outfile,c,"","COLZ")
#saveTuple2DPlot("eleL1bthetaX","eleL2bthetaY",50,-thetaRange,thetaRange,50,-thetaRange,thetaRange,outfile,c,"","COLZ")
#saveTuple2DPlot("posL1tthetaX","posL2tthetaY",50,-thetaRange,thetaRange,50,-thetaRange,thetaRange,outfile,c,"","COLZ")
#saveTuple2DPlot("posL1bthetaX","posL2bthetaY",50,-thetaRange,thetaRange,50,-thetaRange,thetaRange,outfile,c,"","COLZ")
saveTuple2DPlot("eleTrkExtrpXAxialTopL1","eleTrkExtrpYAxialTopL1",50,-20,20,50,0,10,outfile,c,"!eleHasL1","COLZ")
saveTuple2DPlot("eleTrkExtrpXStereoTopL1","eleTrkExtrpYStereoTopL1",50,-20,20,50,0,10,outfile,c,"!eleHasL1","COLZ")
saveTuple2DPlot("eleTrkExtrpXAxialBotL1","eleTrkExtrpYAxialBotL1",50,-20,20,50,-10,0,outfile,c,"!eleHasL1","COLZ")
saveTuple2DPlot("eleTrkExtrpXStereoBotL1","eleTrkExtrpYStereoBotL1",50,-20,20,50,-10,0,outfile,c,"!eleHasL1","COLZ")
saveTuple2DPlot("posTrkExtrpXAxialTopL1","posTrkExtrpYAxialTopL1",50,-20,20,50,0,10,outfile,c,"!posHasL1","COLZ")
saveTuple2DPlot("posTrkExtrpXStereoTopL1","posTrkExtrpYStereoTopL1",50,-20,20,50,0,10,outfile,c,"!posHasL1","COLZ")
saveTuple2DPlot("posTrkExtrpXAxialBotL1","posTrkExtrpYAxialBotL1",50,-20,20,50,-10,0,outfile,c,"!posHasL1","COLZ")
saveTuple2DPlot("posTrkExtrpXStereoBotL1","posTrkExtrpYStereoBotL1",50,-20,20,50,-10,0,outfile,c,"!posHasL1","COLZ")
saveTuple2DPlot("uncVZ","eleL1tthetaY",50,-20,zMax,50,-thetaRange,thetaRange,outfile,c,"","COLZ")
saveTuple2DPlot("uncVZ","eleL1bthetaY",50,-20,zMax,50,-thetaRange,thetaRange,outfile,c,"","COLZ")
saveTuple2DPlot("uncVZ","posL1tthetaY",50,-20,zMax,50,-thetaRange,thetaRange,outfile,c,"","COLZ")
saveTuple2DPlot("uncVZ","posL1bthetaY",50,-20,zMax,50,-thetaRange,thetaRange,outfile,c,"","COLZ")
saveTuple2DPlot("uncVZ","eleL2tthetaY",50,-20,zMax,50,-thetaRange,thetaRange,outfile,c,"","COLZ")
saveTuple2DPlot("uncVZ","eleL2bthetaY",50,-20,zMax,50,-thetaRange,thetaRange,outfile,c,"","COLZ")
saveTuple2DPlot("uncVZ","posL2tthetaY",50,-20,zMax,50,-thetaRange,thetaRange,outfile,c,"","COLZ")
saveTuple2DPlot("uncVZ","posL2bthetaY",50,-20,zMax,50,-thetaRange,thetaRange,outfile,c,"","COLZ")
saveTuple2DPlot("uncVZ","eleL3tthetaY",50,-20,zMax,50,-thetaRange,thetaRange,outfile,c,"","COLZ")
saveTuple2DPlot("uncVZ","eleL3bthetaY",50,-20,zMax,50,-thetaRange,thetaRange,outfile,c,"","COLZ")
saveTuple2DPlot("uncVZ","posL3tthetaY",50,-20,zMax,50,-thetaRange,thetaRange,outfile,c,"","COLZ")
saveTuple2DPlot("uncVZ","posL3bthetaY",50,-20,zMax,50,-thetaRange,thetaRange,outfile,c,"","COLZ")
saveTuple2DPlot("uncVZ","eleL4tthetaY",50,-20,zMax,50,-thetaRange,thetaRange,outfile,c,"","COLZ")
saveTuple2DPlot("uncVZ","eleL4bthetaY",50,-20,zMax,50,-thetaRange,thetaRange,outfile,c,"","COLZ")
saveTuple2DPlot("uncVZ","posL4tthetaY",50,-20,zMax,50,-thetaRange,thetaRange,outfile,c,"","COLZ")
saveTuple2DPlot("uncVZ","posL4bthetaY",50,-20,zMax,50,-thetaRange,thetaRange,outfile,c,"","COLZ")
saveTuple2DPlot("uncVZ","eleL5tthetaY",50,-20,zMax,50,-thetaRange,thetaRange,outfile,c,"","COLZ")
saveTuple2DPlot("uncVZ","eleL5bthetaY",50,-20,zMax,50,-thetaRange,thetaRange,outfile,c,"","COLZ")
saveTuple2DPlot("uncVZ","posL5tthetaY",50,-20,zMax,50,-thetaRange,thetaRange,outfile,c,"","COLZ")
saveTuple2DPlot("uncVZ","posL5bthetaY",50,-20,zMax,50,-thetaRange,thetaRange,outfile,c,"","COLZ")
saveTuple2DPlot("uncVZ","eleL1tthetaY+eleL2tthetaY",50,-20,zMax,50,-thetaRange,thetaRange,outfile,c,"","COLZ")
saveTuple2DPlot("uncVZ","eleL1bthetaY+eleL2bthetaY",50,-20,zMax,50,-thetaRange,thetaRange,outfile,c,"","COLZ")
saveTuple2DPlot("uncVZ","posL1tthetaY+posL2tthetaY",50,-20,zMax,50,-thetaRange,thetaRange,outfile,c,"","COLZ")
saveTuple2DPlot("uncVZ","posL1bthetaY+posL2bthetaY",50,-20,zMax,50,-thetaRange,thetaRange,outfile,c,"","COLZ")
saveTuple2DPlot("uncVZ","eleL1tthetaY+eleL2tthetaY+eleL3tthetaY+eleL4tthetaY",50,-20,zMax,50,-thetaRange,thetaRange,outfile,c,"","COLZ")
saveTuple2DPlot("uncVZ","eleL1bthetaY+eleL2bthetaY+eleL3bthetaY+eleL4bthetaY",50,-20,zMax,50,-thetaRange,thetaRange,outfile,c,"","COLZ")
saveTuple2DPlot("uncVZ","posL1tthetaY+posL2tthetaY+posL3tthetaY+posL4tthetaY",50,-20,zMax,50,-thetaRange,thetaRange,outfile,c,"","COLZ")
saveTuple2DPlot("uncVZ","posL1bthetaY+posL2bthetaY+posL3bthetaY+posL4bthetaY",50,-20,zMax,50,-thetaRange,thetaRange,outfile,c,"","COLZ")
saveTuple2DPlot("uncVZ","eleL1tthetaY-posL1bthetaY",50,-20,zMax,50,-thetaRange,thetaRange,outfile,c,"eleL1tthetaY>-9998 && posL1bthetaY>-9998","COLZ")
saveTuple2DPlot("uncVZ","eleL1bthetaY-posL1tthetaY",50,-20,zMax,50,-thetaRange,thetaRange,outfile,c,"eleL1bthetaY>-9998 && posL1tthetaY>-9998","COLZ")
saveTuple2DPlot("uncVZ","eleL2tthetaY-posL2bthetaY",50,-20,zMax,50,-thetaRange,thetaRange,outfile,c,"eleL2tthetaY>-9998 && posL2bthetaY>-9998","COLZ")
saveTuple2DPlot("uncVZ","eleL2bthetaY-posL2tthetaY",50,-20,zMax,50,-thetaRange,thetaRange,outfile,c,"eleL2bthetaY>-9998 && posL2tthetaY>-9998","COLZ")
saveTuple2DPlot("uncVZ","eleL3tthetaY-posL3bthetaY",50,-20,zMax,50,-thetaRange,thetaRange,outfile,c,"eleL3tthetaY>-9998 && posL3bthetaY>-9998","COLZ")
saveTuple2DPlot("uncVZ","eleL3bthetaY-posL3tthetaY",50,-20,zMax,50,-thetaRange,thetaRange,outfile,c,"eleL3bthetaY>-9998 && posL3tthetaY>-9998","COLZ")
saveTuple2DPlot("uncVZ","eleL4tthetaY-posL4bthetaY",50,-20,zMax,50,-thetaRange,thetaRange,outfile,c,"eleL4tthetaY>-9998 && posL4bthetaY>-9998","COLZ")
saveTuple2DPlot("uncVZ","eleL4bthetaY-posL4tthetaY",50,-20,zMax,50,-thetaRange,thetaRange,outfile,c,"eleL4bthetaY>-9998 && posL4tthetaY>-9998","COLZ")
saveTuple2DPlot("uncVZ","(eleL1tthetaY+eleL2tthetaY)-(posL1bthetaY+posL2bthetaY)",50,-20,zMax,50,-thetaRange,thetaRange,outfile,c,"(eleL1tthetaY+eleL2tthetaY)>-9998 && (posL1bthetaY+posL2bthetaY)>-9998","COLZ")
saveTuple2DPlot("uncVZ","(eleL1bthetaY+eleL2bthetaY)-(posL1tthetaY+posL2tthetaY)",50,-20,zMax,50,-thetaRange,thetaRange,outfile,c,"(eleL1bthetaY+eleL2bthetaY)>-9998 && (posL1tthetaY+posL2tthetaY)>-9998","COLZ")
saveTuple2DPlot("uncVZ","(eleL1tthetaY+eleL2tthetaY+eleL3tthetaY+eleL4tthetaY)-(posL1bthetaY+posL2bthetaY+posL3bthetaY+posL4bthetaY)",50,-20,zMax,50,-thetaRange,thetaRange,outfile,c,"(eleL1tthetaY+eleL2tthetaY+eleL3tthetaY+eleL4tthetaY)>-9998 && (posL1bthetaY+posL2bthetaY+posL3bthetaY+posL4bthetaY)>-9998","COLZ")
saveTuple2DPlot("uncVZ","(eleL1bthetaY+eleL2bthetaY+eleL3bthetaY+eleL4bthetaY)-(posL1tthetaY+posL2tthetaY+posL3tthetaY+posL4tthetaY)",50,-20,zMax,50,-thetaRange,thetaRange,outfile,c,"(eleL1bthetaY+eleL2bthetaY+eleL3bthetaY+eleL4bthetaY)>-9998 && (posL1tthetaY+posL2tthetaY+posL3tthetaY+posL4tthetaY)>-9998","COLZ")

saveTuple2DPlot("eleTrkExtrpYAxialTopL1","eleL1tInthetaY",50,0,3,50,-thetaRange,thetaRange,outfile,c,"!eleHasL1","COLZ")
saveTuple2DPlot("eleTrkExtrpYAxialBotL1","eleL1bInthetaY",50,-3,0,50,-thetaRange,thetaRange,outfile,c,"!eleHasL1","COLZ")
saveTuple2DPlot("eleTrkExtrpYStereoTopL1","eleL1tInthetaY",50,0,3,50,-thetaRange,thetaRange,outfile,c,"!eleHasL1","COLZ")
saveTuple2DPlot("eleTrkExtrpYStereoBotL1","eleL1bInthetaY",50,-3,0,50,-thetaRange,thetaRange,outfile,c,"!eleHasL1","COLZ")
saveTuple2DPlot("posTrkExtrpYAxialTopL1","posL1tInthetaY",50,0,3,50,-thetaRange,thetaRange,outfile,c,"!eleHasL1","COLZ")
saveTuple2DPlot("posTrkExtrpYAxialBotL1","posL1bInthetaY",50,-3,0,50,-thetaRange,thetaRange,outfile,c,"!eleHasL1","COLZ")
saveTuple2DPlot("posTrkExtrpYStereoTopL1","posL1tInthetaY",50,0,3,50,-thetaRange,thetaRange,outfile,c,"!eleHasL1","COLZ")
saveTuple2DPlot("posTrkExtrpYStereoBotL1","posL1bInthetaY",50,-3,0,50,-thetaRange,thetaRange,outfile,c,"!eleHasL1","COLZ")

saveTuple2DPlot("uncVZ","eleTrkExtrpYAxialTopL1",50,-20,zMax,50,0,3,outfile,c,"!eleHasL1","COLZ")
saveTuple2DPlot("uncVZ","eleTrkExtrpYStereoTopL1",50,-20,zMax,50,0,3,outfile,c,"!eleHasL1","COLZ")
saveTuple2DPlot("uncVZ","posTrkExtrpYAxialTopL1",50,-20,zMax,50,0,3,outfile,c,"!posHasL1","COLZ")
saveTuple2DPlot("uncVZ","posTrkExtrpYStereoTopL1",50,-20,zMax,50,0,3,outfile,c,"!posHasL1","COLZ")
saveTuple2DPlot("uncVZ","eleTrkExtrpYAxialBotL1",50,-20,zMax,50,-3,0,outfile,c,"!eleHasL1","COLZ")
saveTuple2DPlot("uncVZ","eleTrkExtrpYStereoBotL1",50,-20,zMax,50,-3,0,outfile,c,"!eleHasL1","COLZ")
saveTuple2DPlot("uncVZ","posTrkExtrpYAxialBotL1",50,-20,zMax,50,-3,0,outfile,c,"!posHasL1","COLZ")
saveTuple2DPlot("uncVZ","posTrkExtrpYStereoBotL1",50,-20,zMax,50,-3,0,outfile,c,"!posHasL1","COLZ")

saveTuple2DPlot("uncVZ","eleTrkZ0",50,-20,zMax,50,-2,2,outfile,c,"!eleHasL1","COLZ")
saveTuple2DPlot("uncVZ","eleTrkZ0",50,-20,zMax,50,-2,2,outfile,c,"","COLZ")
saveTuple2DPlot("uncVZ","posTrkZ0",50,-20,zMax,50,-2,2,outfile,c,"!posHasL1","COLZ")
saveTuple2DPlot("uncVZ","posTrkZ0",50,-20,zMax,50,-2,2,outfile,c,"","COLZ")

saveTuple2DPlot("eleTrkZ0","eleTrkExtrpYAxialTopL1",50,-2,2,50,0,3,outfile,c,"","COLZ")
saveTuple2DPlot("eleTrkZ0","eleTrkExtrpYStereoTopL1",50,-2,2,50,0,3,outfile,c,"","COLZ")
saveTuple2DPlot("posTrkZ0","posTrkExtrpYAxialTopL1",50,-2,2,50,0,3,outfile,c,"","COLZ")
saveTuple2DPlot("posTrkZ0","posTrkExtrpYStereoTopL1",50,-2,2,50,0,3,outfile,c,"","COLZ")
saveTuple2DPlot("eleTrkZ0","eleTrkExtrpYAxialBotL1",50,-2,2,50,-3,0,outfile,c,"","COLZ")
saveTuple2DPlot("eleTrkZ0","eleTrkExtrpYStereoBotL1",50,-2,2,50,-3,0,outfile,c,"","COLZ")
saveTuple2DPlot("posTrkZ0","posTrkExtrpYAxialBotL1",50,-2,2,50,-3,0,outfile,c,"","COLZ")
saveTuple2DPlot("posTrkZ0","posTrkExtrpYStereoBotL1",50,-2,2,50,-3,0,outfile,c,"","COLZ")

saveTuple2DPlot("eleTrkZ0","eleTrkExtrpYAxialTopL1",50,-2,2,50,0,3,outfile,c,"!eleHasL1","COLZ")
saveTuple2DPlot("eleTrkZ0","eleTrkExtrpYStereoTopL1",50,-2,2,50,0,3,outfile,c,"!eleHasL1","COLZ")
saveTuple2DPlot("posTrkZ0","posTrkExtrpYAxialTopL1",50,-2,2,50,0,3,outfile,c,"!posHasL1","COLZ")
saveTuple2DPlot("posTrkZ0","posTrkExtrpYStereoTopL1",50,-2,2,50,0,3,outfile,c,"!posHasL1","COLZ")
saveTuple2DPlot("eleTrkZ0","eleTrkExtrpYAxialBotL1",50,-2,2,50,-3,0,outfile,c,"!eleHasL1","COLZ")
saveTuple2DPlot("eleTrkZ0","eleTrkExtrpYStereoBotL1",50,-2,2,50,-3,0,outfile,c,"!eleHasL1","COLZ")
saveTuple2DPlot("posTrkZ0","posTrkExtrpYAxialBotL1",50,-2,2,50,-3,0,outfile,c,"!posHasL1","COLZ")
saveTuple2DPlot("posTrkZ0","posTrkExtrpYStereoBotL1",50,-2,2,50,-3,0,outfile,c,"!posHasL1","COLZ")

saveTuple2DPlot("uncVZ","eleL1tInthetaY",50,-20,zMax,50,-thetaRange,thetaRange,outfile,c,"!eleHasL1","COLZ")
saveTuple2DPlot("uncVZ","eleL1bInthetaY",50,-20,zMax,50,-thetaRange,thetaRange,outfile,c,"!eleHasL1","COLZ")
saveTuple2DPlot("uncVZ","posL1tInthetaY",50,-20,zMax,50,-thetaRange,thetaRange,outfile,c,"!posHasL1","COLZ")
saveTuple2DPlot("uncVZ","posL1bInthetaY",50,-20,zMax,50,-thetaRange,thetaRange,outfile,c,"!posHasL1","COLZ")
saveTuple2DPlot("uncVZ","eleL2tInthetaY",50,-20,zMax,50,-thetaRange,thetaRange,outfile,c,"!eleHasL1","COLZ")
saveTuple2DPlot("uncVZ","eleL2bInthetaY",50,-20,zMax,50,-thetaRange,thetaRange,outfile,c,"!eleHasL1","COLZ")
saveTuple2DPlot("uncVZ","posL2tInthetaY",50,-20,zMax,50,-thetaRange,thetaRange,outfile,c,"!posHasL1","COLZ")
saveTuple2DPlot("uncVZ","posL2bInthetaY",50,-20,zMax,50,-thetaRange,thetaRange,outfile,c,"!posHasL1","COLZ")
saveTuple2DPlot("uncVZ","eleL1tInthetaY+eleL2tInthetaY",50,-20,zMax,50,-thetaRange,thetaRange,outfile,c,"!eleHasL1","COLZ")
saveTuple2DPlot("uncVZ","eleL1bInthetaY+eleL2bInthetaY",50,-20,zMax,50,-thetaRange,thetaRange,outfile,c,"!eleHasL1","COLZ")
saveTuple2DPlot("uncVZ","posL1tInthetaY+posL2tInthetaY",50,-20,zMax,50,-thetaRange,thetaRange,outfile,c,"!posHasL1","COLZ")
saveTuple2DPlot("uncVZ","posL1bInthetaY+posL2bInthetaY",50,-20,zMax,50,-thetaRange,thetaRange,outfile,c,"!posHasL1","COLZ")
saveTuple2DPlot("uncVZ","eleL1tInthetaY+eleL2tthetaY",50,-20,zMax,50,-thetaRange,thetaRange,outfile,c,"!eleHasL1","COLZ")
saveTuple2DPlot("uncVZ","eleL1bInthetaY+eleL2bthetaY",50,-20,zMax,50,-thetaRange,thetaRange,outfile,c,"!eleHasL1","COLZ")
saveTuple2DPlot("uncVZ","posL1tInthetaY+posL2tthetaY",50,-20,zMax,50,-thetaRange,thetaRange,outfile,c,"!posHasL1","COLZ")
saveTuple2DPlot("uncVZ","posL1bInthetaY+posL2bthetaY",50,-20,zMax,50,-thetaRange,thetaRange,outfile,c,"!posHasL1","COLZ")
saveTuple2DPlot("uncVZ","eleL1tInthetaY-posL1bthetaY",50,-20,zMax,50,-thetaRange,thetaRange,outfile,c,"!eleHasL1 && eleL1tInthetaY>-9998 && posL1bthetaY>-9998","COLZ")
saveTuple2DPlot("uncVZ","eleL1bInthetaY-posL1tthetaY",50,-20,zMax,50,-thetaRange,thetaRange,outfile,c,"!eleHasL1 && eleL1bInthetaY>-9998 && posL2tthetaY>-9998","COLZ")
saveTuple2DPlot("uncVZ","eleL1tthetaY-posL1bInthetaY",50,-20,zMax,50,-thetaRange,thetaRange,outfile,c,"!posHasL1 && eleL1tthetaY>-9998 && posL1bInthetaY>-9998","COLZ")
saveTuple2DPlot("uncVZ","eleL1bthetaY-posL1tInthetaY",50,-20,zMax,50,-thetaRange,thetaRange,outfile,c,"!posHasL1 && eleL1bthetaY>-9998 && posL2tInthetaY>-9998","COLZ")
saveTuple2DPlot("uncVZ","(eleL1tInthetaY+eleL2tInthetaY)-(posL1bthetaY+posL2bthetaY)",50,-20,zMax,50,-thetaRange,thetaRange,outfile,c,"!eleHasL1 && eleL1tInthetaY+eleL2tInthetaY>-9998 && posL1bthetaY+posL2bthetaY>-9998","COLZ")
saveTuple2DPlot("uncVZ","(eleL1tInthetaY+eleL2tthetaY)-(posL1bthetaY+posL2bthetaY)",50,-20,zMax,50,-thetaRange,thetaRange,outfile,c,"!eleHasL1 && eleL1tInthetaY+eleL2tthetaY>-9998 && posL1bthetaY+posL2bthetaY>-9998","COLZ")
saveTuple2DPlot("uncVZ","(eleL1bInthetaY+eleL2bInthetaY)-(posL1tthetaY+posL2tthetaY)",50,-20,zMax,50,-thetaRange,thetaRange,outfile,c,"!eleHasL1 && eleL1bInthetaY+eleL2bInthetaY>-9998 && posL1tthetaY+posL2tthetaY>-9998","COLZ")
saveTuple2DPlot("uncVZ","(eleL1bInthetaY+eleL2bthetaY)-(posL1tthetaY+posL2tthetaY)",50,-20,zMax,50,-thetaRange,thetaRange,outfile,c,"!eleHasL1 && eleL1bInthetaY+eleL2bthetaY>-9998 && posL1tthetaY+posL2tthetaY>-9998","COLZ")
saveTuple2DPlot("uncVZ","(eleL1tthetaY+eleL2tthetaY)-(posL1bInthetaY+posL2bInthetaY)",50,-20,zMax,50,-thetaRange,thetaRange,outfile,c,"!posHasL1 && eleL1tthetaY+eleL2tthetaY>-9998 && posL1bInthetaY+posL2bInthetaY>-9998","COLZ")
saveTuple2DPlot("uncVZ","(eleL1tthetaY+eleL2tthetaY)-(posL1bInthetaY+posL2bthetaY)",50,-20,zMax,50,-thetaRange,thetaRange,outfile,c,"!posHasL1 && eleL1tthetaY+eleL2tthetaY>-9998 && posL1bInthetaY+posL2bthetaY>-9998","COLZ")
saveTuple2DPlot("uncVZ","(eleL1bthetaY+eleL2bthetaY)-(posL1tInthetaY+posL2tInthetaY)",50,-20,zMax,50,-thetaRange,thetaRange,outfile,c,"!posHasL1 && eleL1bthetaY+eleL2bthetaY>-9998 && posL1tInthetaY+posL2tInthetaY>-9998","COLZ")
saveTuple2DPlot("uncVZ","(eleL1bthetaY+eleL2bthetaY)-(posL1tInthetaY+posL2tthetaY)",50,-20,zMax,50,-thetaRange,thetaRange,outfile,c,"!posHasL1 && eleL1bthetaY+eleL2bthetaY>-9998 && posL1tInthetaY+posL2tthetaY>-9998","COLZ")

#saveTuple2DPlot("uncChisq","eleL1tthetaY",50,0,10,50,-thetaRange,thetaRange,outfile,c,"","COLZ")
#saveTuple2DPlot("uncChisq","eleL1bthetaY",50,0,10,50,-thetaRange,thetaRange,outfile,c,"","COLZ")
#saveTuple2DPlot("uncChisq","posL1tthetaY",50,0,10,50,-thetaRange,thetaRange,outfile,c,"","COLZ")
#saveTuple2DPlot("uncChisq","posL1bthetaY",50,0,10,50,-thetaRange,thetaRange,outfile,c,"","COLZ")
#saveTuple2DPlot("uncChisq","eleL2tthetaY",50,0,10,50,-thetaRange,thetaRange,outfile,c,"","COLZ")
#saveTuple2DPlot("uncChisq","eleL2bthetaY",50,0,10,50,-thetaRange,thetaRange,outfile,c,"","COLZ")
#saveTuple2DPlot("uncChisq","posL2tthetaY",50,0,10,50,-thetaRange,thetaRange,outfile,c,"","COLZ")
#saveTuple2DPlot("uncChisq","posL2bthetaY",50,0,10,50,-thetaRange,thetaRange,outfile,c,"","COLZ")
#saveTuple2DPlot("uncChisq","eleL1tthetaY+eleL2tthetaY",50,0,10,50,-thetaRange,thetaRange,outfile,c,"","COLZ")
#saveTuple2DPlot("uncChisq","eleL1bthetaY+eleL2bthetaY",50,0,10,50,-thetaRange,thetaRange,outfile,c,"","COLZ")
#saveTuple2DPlot("uncChisq","posL1tthetaY+posL2tthetaY",50,0,10,50,-thetaRange,thetaRange,outfile,c,"","COLZ")
#saveTuple2DPlot("uncChisq","posL1bthetaY+posL2bthetaY",50,0,10,50,-thetaRange,thetaRange,outfile,c,"","COLZ")
#saveTuple2DPlot("uncChisq","eleL1tthetaY-posL1bthetaY",50,0,10,50,-thetaRange,thetaRange,outfile,c,"eleL1tthetaY>-9998 && posL1bthetaY>-9998","COLZ")
#saveTuple2DPlot("uncChisq","eleL1bthetaY-posL1tthetaY",50,0,10,50,-thetaRange,thetaRange,outfile,c,"eleL1bthetaY>-9998 && posL1tthetaY>-9998","COLZ")
#saveTuple2DPlot("uncChisq","eleL2tthetaY-posL2bthetaY",50,0,10,50,-thetaRange,thetaRange,outfile,c,"eleL2tthetaY>-9998 && posL2bthetaY>-9998","COLZ")
#saveTuple2DPlot("uncChisq","eleL2bthetaY-posL2tthetaY",50,0,10,50,-thetaRange,thetaRange,outfile,c,"eleL2bthetaY>-9998 && posL2tthetaY>-9998","COLZ")
#saveTuple2DPlot("uncChisq","eleL1tthetaY+eleL2tthetaY-(posL1bthetaY+posL2bthetaY)",50,0,10,50,-thetaRange,thetaRange,outfile,c,"eleL1tthetaY+eleL2tthetaY->-9998 && posL1bthetaY+posL2bthetaY>-9998","COLZ")
#saveTuple2DPlot("uncChisq","eleL1bthetaY+eleL2bthetaY-(posL1tthetaY+posL2tthetaY)",50,0,10,50,-thetaRange,thetaRange,outfile,c,"eleL1bthetaY+eleL2bthetaY->-9998 && posL1tthetaY+posL2tthetaY>-9998","COLZ")

#saveTuple2DPlot("bscChisq","eleL1tthetaY",50,0,10,50,-thetaRange,thetaRange,outfile,c,"","COLZ")
#saveTuple2DPlot("bscChisq","eleL1bthetaY",50,0,10,50,-thetaRange,thetaRange,outfile,c,"","COLZ")
#saveTuple2DPlot("bscChisq","posL1tthetaY",50,0,10,50,-thetaRange,thetaRange,outfile,c,"","COLZ")
#saveTuple2DPlot("bscChisq","posL1bthetaY",50,0,10,50,-thetaRange,thetaRange,outfile,c,"","COLZ")
#saveTuple2DPlot("bscChisq","eleL2tthetaY",50,0,10,50,-thetaRange,thetaRange,outfile,c,"","COLZ")
#saveTuple2DPlot("bscChisq","eleL2bthetaY",50,0,10,50,-thetaRange,thetaRange,outfile,c,"","COLZ")
#saveTuple2DPlot("bscChisq","posL2tthetaY",50,0,10,50,-thetaRange,thetaRange,outfile,c,"","COLZ")
#saveTuple2DPlot("bscChisq","posL2bthetaY",50,0,10,50,-thetaRange,thetaRange,outfile,c,"","COLZ")
#saveTuple2DPlot("bscChisq","eleL1tthetaY+eleL2tthetaY",50,0,10,50,-thetaRange,thetaRange,outfile,c,"","COLZ")
#saveTuple2DPlot("bscChisq","eleL1bthetaY+eleL2bthetaY",50,0,10,50,-thetaRange,thetaRange,outfile,c,"","COLZ")
#saveTuple2DPlot("bscChisq","posL1tthetaY+posL2tthetaY",50,0,10,50,-thetaRange,thetaRange,outfile,c,"","COLZ")
#saveTuple2DPlot("bscChisq","posL1bthetaY+posL2bthetaY",50,0,10,50,-thetaRange,thetaRange,outfile,c,"","COLZ")
#saveTuple2DPlot("bscChisq","eleL1tthetaY-posL1bthetaY",50,0,10,50,-thetaRange,thetaRange,outfile,c,"eleL1tthetaY>-9998 && posL1bthetaY>-9998","COLZ")
#saveTuple2DPlot("bscChisq","eleL1bthetaY-posL1tthetaY",50,0,10,50,-thetaRange,thetaRange,outfile,c,"eleL1bthetaY>-9998 && posL1tthetaY>-9998","COLZ")
#saveTuple2DPlot("bscChisq","eleL2tthetaY-posL2bthetaY",50,0,10,50,-thetaRange,thetaRange,outfile,c,"eleL2tthetaY>-9998 && posL2bthetaY>-9998","COLZ")
#saveTuple2DPlot("bscChisq","eleL2bthetaY-posL2tthetaY",50,0,10,50,-thetaRange,thetaRange,outfile,c,"eleL2bthetaY>-9998 && posL2tthetaY>-9998","COLZ")
#saveTuple2DPlot("bscChisq","eleL1tthetaY+eleL2tthetaY-(posL1bthetaY+posL2bthetaY)",50,0,10,50,-thetaRange,thetaRange,outfile,c,"eleL1tthetaY+eleL2tthetaY->-9998 && posL1bthetaY+posL2bthetaY>-9998","COLZ")
#saveTuple2DPlot("bscChisq","eleL1bthetaY+eleL2bthetaY-(posL1tthetaY+posL2tthetaY)",50,0,10,50,-thetaRange,thetaRange,outfile,c,"eleL1bthetaY+eleL2bthetaY->-9998 && posL1tthetaY+posL2tthetaY>-9998","COLZ")

saveTuplePlot("eleHasTruthMatch",2,0,2,outfile,c,1)
saveTuplePlot("posHasTruthMatch",2,0,2,outfile,c,1)
saveTuplePlot("elepdgid",35,-12,23,outfile,c,1)
saveTuplePlot("pospdgid",35,-12,23,outfile,c,1)
saveTuplePlot("eleparentID",642,-12,630,outfile,c,1)
saveTuplePlot("posparentID",642,-12,630,outfile,c,1)
saveTuplePlot("eleNTruthHits",12,0,12,outfile,c,1)
saveTuplePlot("posNTruthHits",12,0,12,outfile,c,1)
saveTuplePlot("eleNBadTruthHits",12,0,12,outfile,c,1)
saveTuplePlot("posNBadTruthHits",12,0,12,outfile,c,1)
saveTuplePlot("elePurity",50,0,1.1,outfile,c,1)
saveTuplePlot("posPurity",50,0,1.1,outfile,c,1)

closePDF(outfile,c)
