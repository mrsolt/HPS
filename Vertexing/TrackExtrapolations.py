import sys
tmpargv = sys.argv
sys.argv = []
import getopt
import ROOT
from ROOT import gROOT, TFile, TTree, TChain, gDirectory, TLine, gStyle, TCanvas, TLegend, TH2F, TLine
sys.argv = tmpargv

#List arguments
def print_usage():
    print "\nUsage: {0} <output file base name> <ap input file name> <tritrig input file name>".format(sys.argv[0])
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
infile2 = TFile(remainder[2])

events_ap = infile.Get("ntuple")
events_tritrig = infile2.Get("ntuple")

def tupleToHisto(events,inHisto,histo,nBins,minX,maxX):
	events.Draw("{0}>>{1}({2},{3},{4})".format(inHisto,histo,nBins,minX,maxX))
	histo = ROOT.gROOT.FindObject(histo)
	return histo

def saveTuplePlot(inHisto,nBins,minX,maxX,outfile,canvas,log=0):
	events.Draw("{0}>>({1},{2},{3})".format(inHisto,nBins,minX,maxX))
	canvas.SetLogy(log)
	canvas.Print(outfile+".pdf")

def tupleTo2DHistoSave(events,inHisto1,inHisto2,nBinsX,minX,maxX,nBinsY,minY,maxY,canvas,outfile,line1,line2,plotTitle="",XaxisTitle="",YaxisTitle="",cuts="",stats=0):
	events.Draw("{0}:{1}>>{2}({3},{4},{5},{6},{7},{8})".format(inHisto2,inHisto1,"histo",nBinsX,minX,maxX,nBinsY,minY,maxY),cuts)
	histo = ROOT.gROOT.FindObject("histo")
	histo.Draw("COLZ")
	histo.SetTitle(plotTitle)
	histo.GetXaxis().SetTitle(XaxisTitle)
	histo.GetYaxis().SetTitle(YaxisTitle)
	histo.SetStats(stats)
	line1.Draw("same")
	line2.Draw("same")
	canvas.Print(outfile+".png")

line1 = TLine(-2,1.5,7,1.5)	
line1.SetLineColor(2)
line1.SetLineWidth(5)
line2 = TLine(-2,0.995,7,1.895)	
line2.SetLineColor(2)
line2.SetLineWidth(5)

tupleTo2DHistoSave(events_ap,"eleTrkExtrpXAxialTopL1","eleTrkExtrpYAxialTopL1",50,-2,7,50,0,4,c,outfile+"_ap_eleL1taxial",line1,line2,"Electron L1t Axial Track Extrapolation L1L2 50 MeV A's","x [mm]","y [mm]","!eleHasL1")
tupleTo2DHistoSave(events_tritrig,"eleTrkExtrpXAxialTopL1","eleTrkExtrpYAxialTopL1",50,-2,7,50,0,4,c,outfile+"_trident_eleL1taxial",line1,line2,"Electron L1t Axial Track Extrapolation L1L2 Background","x [mm]","y [mm]","!eleHasL1")

tupleTo2DHistoSave(events_ap,"eleTrkExtrpXStereoTopL1","eleTrkExtrpYStereoTopL1",50,-2,7,50,0,4,c,outfile+"_ap_eleL1tstereo",line1,line2,"Electron L1t Stereo Track Extrapolation L1L2 50 MeV A's","x [mm]","y [mm]","!eleHasL1")
tupleTo2DHistoSave(events_tritrig,"eleTrkExtrpXStereoTopL1","eleTrkExtrpYStereoTopL1",50,-2,7,50,0,4,c,outfile+"_trident_eleL1tstereo",line1,line2,"Electron L1t Stereo Track Extrapolation L1L2 Background","x [mm]","y [mm]","!eleHasL1")

tupleTo2DHistoSave(events_ap,"eleTrkExtrpXAxialBotL1","eleTrkExtrpYAxialBotL1",50,-2,7,50,-4,0,c,outfile+"_ap_eleL1baxial",line1,line2,"Electron L1b Axial Track Extrapolation L1L2 50 MeV A's","x [mm]","y [mm]","!eleHasL1")
tupleTo2DHistoSave(events_tritrig,"eleTrkExtrpXAxialBotL1","eleTrkExtrpYAxialBotL1",50,-2,7,50,-4,0,c,outfile+"_trident_eleL1baxial",line1,line2,"Electron L1b Axial Track Extrapolation L1L2 Background","x [mm]","y [mm]","!eleHasL1")

tupleTo2DHistoSave(events_ap,"eleTrkExtrpXStereoBotL1","eleTrkExtrpYStereoBotL1",50,-2,7,50,-4,0,c,outfile+"_ap_eleL1bstereo",line1,line2,"Electron L1b Stereo Track Extrapolation L1L2 50 MeV A's","x [mm]","y [mm]","!eleHasL1")
tupleTo2DHistoSave(events_tritrig,"eleTrkExtrpXStereoBotL1","eleTrkExtrpYStereoBotL1",50,-2,7,50,-4,0,c,outfile+"_trident_eleL1bstereo",line1,line2,"Electron L1b Stereo Track Extrapolation L1L2 Background","x [mm]","y [mm]","!eleHasL1")

tupleTo2DHistoSave(events_ap,"posTrkExtrpXAxialTopL1","posTrkExtrpYAxialTopL1",50,-2,7,50,0,4,c,outfile+"_ap_posL1taxial",line1,line2,"Positron L1t Axial Track Extrapolation L1L2 50 MeV A's","x [mm]","y [mm]","!posHasL1")
tupleTo2DHistoSave(events_tritrig,"posTrkExtrpXAxialTopL1","posTrkExtrpYAxialTopL1",50,-2,7,50,0,4,c,outfile+"_trident_posL1taxial",line1,line2,"Positron L1t Axial Track Extrapolation L1L2 Background","x [mm]","y [mm]","!posHasL1")

tupleTo2DHistoSave(events_ap,"posTrkExtrpXStereoTopL1","posTrkExtrpYStereoTopL1",50,-2,7,50,0,4,c,outfile+"_ap_posL1tstereo",line1,line2,"Positron L1t Stereo Track Extrapolation L1L2 50 MeV A's","x [mm]","y [mm]","!posHasL1")
tupleTo2DHistoSave(events_tritrig,"posTrkExtrpXStereoTopL1","posTrkExtrpYStereoTopL1",50,-2,7,50,0,4,c,outfile+"_trident_posL1tstereo",line1,line2,"Positron L1t Stereo Track Extrapolation L1L2 Background","x [mm]","y [mm]","!posHasL1")

tupleTo2DHistoSave(events_ap,"posTrkExtrpXAxialBotL1","posTrkExtrpYAxialBotL1",50,-2,7,50,-4,0,c,outfile+"_ap_posL1baxial",line1,line2,"Positron L1b Axial Track Extrapolation L1L2 50 MeV A's","x [mm]","y [mm]","!posHasL1")
tupleTo2DHistoSave(events_tritrig,"posTrkExtrpXAxialBotL1","posTrkExtrpYAxialBotL1",50,-2,7,50,-4,0,c,outfile+"_trident_posL1baxial",line1,line2,"Positron L1b Axial Track Extrapolation L1L2 Background","x [mm]","y [mm]","!posHasL1")

tupleTo2DHistoSave(events_ap,"posTrkExtrpXStereoBotL1","posTrkExtrpYStereoBotL1",50,-2,7,50,-4,0,c,outfile+"_ap_posL1bstereo",line1,line2,"Positron L1b Stereo Track Extrapolation L1L2 50 MeV A's","x [mm]","y [mm]","!posHasL1")
tupleTo2DHistoSave(events_tritrig,"posTrkExtrpXStereoBotL1","posTrkExtrpYStereoBotL1",50,-2,7,50,-4,0,c,outfile+"_trident_posL1bstereo",line1,line2,"Positron L1b Stereo Track Extrapolation L1L2 Background","x [mm]","y [mm]","!posHasL1")
