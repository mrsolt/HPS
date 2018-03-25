import sys
tmpargv = sys.argv
sys.argv = []
import getopt
import ROOT
from ROOT import gROOT, TFile, TTree, TChain, gDirectory, TLine, gStyle, TCanvas, TLegend, TH1F
sys.argv = tmpargv

tupleName = "ntuple"
ebeam = 1.05

#List arguments
def print_usage():
    print "\nUsage: {0} <output file base name> <input file name>".format(sys.argv[0])
    print "Arguments: "
    print '\t-h: this help message'
    print

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'ht:e:')

# Parse the command line arguments
for opt, arg in options:
		if opt=='-t':
			tupleName = str(arg)
		if opt=='-e':
			ebeam = arg
		if opt=='-h':
			print_usage()
			sys.exit(0)

#gStyle.SetOptStat(0)
c = TCanvas("c","c",800,600)

outfile = remainder[0]

file1 = TFile(remainder[1])
file2 = TFile(remainder[2])
title1 = remainder[3]
title2 = remainder[4]

events1 = file1.Get(tupleName)
events2= file2.Get(tupleName)

def saveTuplePlot(events1,events2,inHisto,title1,title2,nBins,minX,maxX,outfile,canvas,XaxisTitle="",YaxisTitle="",plotTitle="",stats=0,logY=0):
	events1.Draw("{0}>>histo1({1},{2},{3})".format(inHisto,nBins,minX,maxX))
	histo1 = ROOT.gROOT.FindObject("histo1")
	events2.Draw("{0}>>histo2({1},{2},{3})".format(inHisto,nBins,minX,maxX))
	histo2 = ROOT.gROOT.FindObject("histo2")
	legend = TLegend(.68,.66,.92,.87)
	legend.SetBorderSize(0)
	legend.SetFillColor(0)
	legend.SetFillStyle(0)
	legend.SetTextFont(42)
	legend.SetTextSize(0.035)
	legend.AddEntry(histo1,title1,"LP")
	legend.AddEntry(histo2,title2,"LP")
	maximum = histo1.GetMaximum()
	if(maximum < histo2.GetMaximum()): maximum = histo2.GetMaximum()
	histo1.SetTitle(plotTitle)
	histo1.GetXaxis().SetTitle(XaxisTitle)
	histo1.GetYaxis().SetTitle(YaxisTitle)
	histo1.GetYaxis().SetRangeUser(0,maximum*1.2)
	histo1.SetStats(stats)
	histo1.SetLineColor(4)
	histo1.Draw()
	histo2.SetLineColor(2)
	histo2.Draw("same")
	legend.Draw("same")
	canvas.SetLogy(logY)
	canvas.Print(outfile+".pdf")
	del histo1
	del histo2
	del legend

def saveTuplePlot2D(events,inHisto1,inHisto2,nBinsX,minX,maxX,nBinsY,minY,maxY,outfile,canvas,XaxisTitle="",YaxisTitle="",plotTitle="",stats=0,logY=0):
	events.Draw("{0}:{1}>>histo({2},{3},{4},{5},{6},{7})".format(inHisto2,inHisto1,nBinsX,minX,maxX,nBinsY,minY,maxY))
	histo = ROOT.gROOT.FindObject("histo")
	histo.SetTitle(plotTitle)
	histo.GetXaxis().SetTitle(XaxisTitle)
	histo.GetYaxis().SetTitle(YaxisTitle)
	histo.SetStats(stats)
	histo.Draw("COLZ")
	canvas.SetLogy(logY)
	canvas.Print(outfile+".pdf")
	del histo

def openPDF(outfile,canvas):
	canvas.Print(outfile+".pdf[")

def closePDF(outfile,canvas):
	canvas.Print(outfile+".pdf]")

nBins = 50
minVZ = -20
maxVZ = 125
minMass = 0
maxMass = 0.1 * ebeam


minTrkZ0 = -10
maxTrkZ0 = 10
minTrkD0 = -5
maxTrkD0 = 5
minTrkPhi = -0.01
maxTrkPhi = 0.01
minTrkOmega = -0.001
maxTrkOmega = 0.001
minTrkLambda = -0.1
maxTrkLambda = 0.1

ParametersList = []
ParametersList.append("uncVZ")
ParametersList.append("nPos")
ParametersList.append("nCl")
ParametersList.append("nEcalHits")
ParametersList.append("nSVTHits")
ParametersList.append("nEcalCl")
ParametersList.append("nEcalClele")
ParametersList.append("nEcalClpos")
ParametersList.append("nSVTHitsL1")
ParametersList.append("uncP")
ParametersList.append("uncChisq")
ParametersList.append("bscChisq")
ParametersList.append("uncM")
ParametersList.append("(uncVZ-0.5)/sqrt(uncCovZZ)")
ParametersList.append("abs(eleClT-eleTrkT-43)")
ParametersList.append("abs(posClT-posTrkT-43)")
ParametersList.append("abs(eleClT-posClT)")
ParametersList.append("bscChisq-uncChisq")
ParametersList.append("min(eleMinPositiveIso+0.5*(eleTrkZ0+0.5*elePY/eleP)*sign(elePY),posMinPositiveIso+0.5*(posTrkZ0+0.5*posPY/posP)*sign(posPY))")
ParametersList.append("abs(eleP-posP)/(eleP+posP)")
ParametersList.append("posTrkD0+0.5*posPX/posP")
ParametersList.append("eleTrkChisq/(2*eleNTrackHits-5)+posTrkChisq/(2*posNTrackHits-5)")
ParametersList.append("(pow((uncVX-(uncVZ)*uncPX/uncPZ-0.1)*cos(-0.2)-(uncVY-(uncVZ)*uncPY/uncPZ)*sin(-0.2),2)/0.64+pow((uncVX-(uncVZ)*uncPX/uncPZ)*sin(-0.2)+(uncVY-(uncVZ)*uncPY/uncPZ)*cos(-0.2),2)/0.16)")
ParametersList.append("posHasL1&&min(eleMinPositiveIso+0.33*(eleTrkZ0+0.5*elePY/eleP)*sign(elePY),posMinPositiveIso+0.5*(posTrkZ0+0.5*posPY/posP)*sign(posPY))")
ParametersList.append("eleHasL1&&!posHasL1&&min(eleMinPositiveIso+0.5*(eleTrkZ0+0.5*elePY/eleP)*sign(elePY),posMinPositiveIso+0.33*(posTrkZ0+0.5*posPY/posP)*sign(posPY))")
ParametersList.append("min(eleMinPositiveIso+0.33*(eleTrkZ0+0.5*elePY/eleP)*sign(elePY),posMinPositiveIso+0.33*(posTrkZ0+0.5*posPY/posP)*sign(posPY))")
ParametersList.append("eleClE/eleP")
ParametersList.append("posClE/posP")
ParametersList.append("sqrt(eleTrkZ0*eleTrkZ0+posTrkZ0*posTrkZ0)")
ParametersList.append("(atan(eleClY/(eleClX-42.5))-atan(posClY/(posClX-42.5)))*180/3.14+180")
ParametersList.append("sqrt(pow(uncVY-(uncVZ)*uncPY/uncPZ,2)+pow(uncVX-(uncVZ)*uncPX/uncPZ,2))")
ParametersList.append("sqrt(pow(bscVY-(bscVZ)*bscPY/bscPZ,2)+pow(bscVX-(bscVZ)*bscPX/bscPZ,2))")
ParametersList.append("bscVY")
ParametersList.append("sqrt(bscVX*bscVX+bscVY*bscVY)")
ParametersList.append("uncVY")
ParametersList.append("sqrt(uncVX*uncVX+uncVY*uncVY)")
ParametersList.append("uncVX-(uncVZ-0.5)*uncPX/uncPZ")
ParametersList.append("uncVY-(uncVZ-0.5)*uncPY/uncPZ")
ParametersList.append("sqrt((uncVX-(uncVZ-0.5)*uncPX/uncPZ)**2+(uncVY-(uncVZ-0.5)*uncPY/uncPZ)**2)")

ParametersListMin = []
ParametersListMin.append(minVZ)
ParametersListMin.append(0)
ParametersListMin.append(0)
ParametersListMin.append(0)
ParametersListMin.append(0)
ParametersListMin.append(0)
ParametersListMin.append(0)
ParametersListMin.append(0)
ParametersListMin.append(0)
ParametersListMin.append(0)
ParametersListMin.append(0)
ParametersListMin.append(0)
ParametersListMin.append(0)
ParametersListMin.append(0)
ParametersListMin.append(0)
ParametersListMin.append(0)
ParametersListMin.append(0)
ParametersListMin.append(-10)
ParametersListMin.append("")
ParametersListMin.append(0)
ParametersListMin.append(-6)
ParametersListMin.append(0)
ParametersListMin.append("")
ParametersListMin.append("")
ParametersListMin.append("")
ParametersListMin.append("")
ParametersListMin.append(0)
ParametersListMin.append(0)
ParametersListMin.append(0)
ParametersListMin.append("")
ParametersListMin.append("")
ParametersListMin.append("")
ParametersListMin.append(-2)
ParametersListMin.append(0)
ParametersListMin.append(-2)
ParametersListMin.append(0)
ParametersListMin.append(-2)
ParametersListMin.append(-1.5)
ParametersListMin.append(0)

ParametersListMax = []
ParametersListMax.append(maxVZ)
ParametersListMax.append(10)
ParametersListMax.append(10)
ParametersListMax.append(100)
ParametersListMax.append(1000)
ParametersListMax.append(10)
ParametersListMax.append(10)
ParametersListMax.append(10)
ParametersListMax.append(100)
ParametersListMax.append(1.5)
ParametersListMax.append(20)
ParametersListMax.append(20)
ParametersListMax.append(0.1)
ParametersListMax.append(30)
ParametersListMax.append(5)
ParametersListMax.append(5)
ParametersListMax.append(5)
ParametersListMax.append(10)
ParametersListMax.append("")
ParametersListMax.append(1)
ParametersListMax.append(6)
ParametersListMax.append(10)
ParametersListMax.append("")
ParametersListMax.append("")
ParametersListMax.append("")
ParametersListMax.append("")
ParametersListMax.append(1.5)
ParametersListMax.append(1.5)
ParametersListMax.append(10)
ParametersListMax.append("")
ParametersListMax.append("")
ParametersListMax.append("")
ParametersListMax.append(2)
ParametersListMax.append(3)
ParametersListMax.append(2)
ParametersListMax.append(3)
ParametersListMax.append(2)
ParametersListMax.append(1.5)
ParametersListMax.append(5)


TrackParametersList = []
#Track Parameters
TrackParametersList.append("TrkZ0")
TrackParametersList.append("TrkD0")
TrackParametersList.append("TrkPhi")
TrackParametersList.append("TrkOmega")
TrackParametersList.append("TrkLambda")
TrackParametersList.append("TrkT")
TrackParametersList.append("TrkChisq")
TrackParametersList.append("P")
TrackParametersList.append("TrkHits")
TrackParametersList.append("LambdaKink1")
TrackParametersList.append("LambdaKink2")
TrackParametersList.append("PhiKink1")
TrackParametersList.append("PhiKink2")
TrackParametersList.append("MatchChisq")
TrackParametersList.append("ClT")
TrackParametersList.append("TrkExtrpYAxialTopL1")
TrackParametersList.append("TrkExtrpYStereoTopL1")
TrackParametersList.append("TrkExtrpYAxialBotL1")
TrackParametersList.append("TrkExtrpYStereoBotL1")

TrackParametersListMin = []
TrackParametersListMin.append(-8)
TrackParametersListMin.append(-6)
TrackParametersListMin.append(-0.07)
TrackParametersListMin.append(-0.0003)
TrackParametersListMin.append(-0.08)
TrackParametersListMin.append(-10)
TrackParametersListMin.append(0)
TrackParametersListMin.append(0)
TrackParametersListMin.append(0)
TrackParametersListMin.append(-0.002)
TrackParametersListMin.append(-0.002)
TrackParametersListMin.append(-0.0002)
TrackParametersListMin.append(-0.0002)
TrackParametersListMin.append(0)
TrackParametersListMin.append(35)
TrackParametersListMin.append(0)
TrackParametersListMin.append(0)
TrackParametersListMin.append(0)
TrackParametersListMin.append(0)

TrackParametersListMax = []
TrackParametersListMax.append(8)
TrackParametersListMax.append(6)
TrackParametersListMax.append(0.07)
TrackParametersListMax.append(0.0003)
TrackParametersListMax.append(0.08)
TrackParametersListMax.append(10)
TrackParametersListMax.append(60)
TrackParametersListMax.append(1.5)
TrackParametersListMax.append(6)
TrackParametersListMax.append(0.002)
TrackParametersListMax.append(0.002)
TrackParametersListMax.append(0.0002)
TrackParametersListMax.append(0.0002)
TrackParametersListMax.append(10)
TrackParametersListMax.append(50)
TrackParametersListMax.append(1)
TrackParametersListMax.append(1)
TrackParametersListMax.append(1)
TrackParametersListMax.append(1)

Parameters2DList = []
Parameters2DList.append("bscVY")
Parameters2DList.append("bscVX")
Parameters2DList.append("eleClY")
Parameters2DList.append("eleClX")
Parameters2DList.append("posClY")
Parameters2DList.append("posClX")
Parameters2DList.append("uncVY-(uncVZ-0.5)*uncPY/uncPZ")
Parameters2DList.append("uncVX-(uncVZ-0.5)*uncPX/uncPZ")

Parameters2DListMin = []
Parameters2DListMin.append(-2)
Parameters2DListMin.append(-2)
Parameters2DListMin.append(-100)
Parameters2DListMin.append(-200)
Parameters2DListMin.append(-100)
Parameters2DListMin.append(-200)
Parameters2DListMin.append(-1.5)
Parameters2DListMin.append(-2)

Parameters2DListMax = []
Parameters2DListMax.append(2)
Parameters2DListMax.append(2)
Parameters2DListMax.append(100)
Parameters2DListMax.append(250)
Parameters2DListMax.append(100)
Parameters2DListMax.append(250)
Parameters2DListMax.append(1.5)
Parameters2DListMax.append(2)

#mychain = gDirectory.Get("ntuple")
#entries = mychain.GetEntriesFast()
#for entry in xrange(entries):
#	nb = mychain.GetEntry(entry)
#	event = mychain.event
#	uncVZ = mychain.uncVZ
#	if(uncVZ > 90): print str(uncVZ) + "   " + str(event)


openPDF(outfile,c)

#Basic Vertex Plots
saveTuplePlot2D(events1,"uncM","uncVZ",nBins,minMass,maxMass,nBins,minVZ,maxVZ,outfile,c,"uncM","uncVZ",title1,1)
saveTuplePlot2D(events2,"uncM","uncVZ",nBins,minMass,maxMass,nBins,minVZ,maxVZ,outfile,c,"uncM","uncVZ",title2,1)

for i in range(len(ParametersList)):
	par = ParametersList[i]
	minimum = ParametersListMin[i]
	maximum = ParametersListMax[i]
	saveTuplePlot(events1,events2,par,title1,title2,nBins,minimum,maximum,outfile,c,par,"",par)
	saveTuplePlot2D(events1,"uncVZ",par,nBins,minVZ,maxVZ,nBins,minimum,maximum,outfile,c,"uncVZ",par,title1,1)
	saveTuplePlot2D(events2,"uncVZ",par,nBins,minVZ,maxVZ,nBins,minimum,maximum,outfile,c,"uncVZ",par,title2,1)

#Basic Track Plots
for i in range(len(TrackParametersList)):
	ele = "ele" + TrackParametersList[i]
	pos = "pos" + TrackParametersList[i]
	minimum = TrackParametersListMin[i]
	maximum = TrackParametersListMax[i]
	saveTuplePlot(events1,events2,ele,title1,title2,nBins,minimum,maximum,outfile,c,ele,"",ele)
	saveTuplePlot2D(events1,"uncVZ",ele,nBins,minVZ,maxVZ,nBins,minimum,maximum,outfile,c,"uncVZ",ele,title1,1)
	saveTuplePlot2D(events2,"uncVZ",ele,nBins,minVZ,maxVZ,nBins,minimum,maximum,outfile,c,"uncVZ",ele,title2,1)
	saveTuplePlot2D(events1,"uncVZ",pos,nBins,minVZ,maxVZ,nBins,minimum,maximum,outfile,c,"uncVZ",pos,title1,1)
	saveTuplePlot2D(events2,"uncVZ",pos,nBins,minVZ,maxVZ,nBins,minimum,maximum,outfile,c,"uncVZ",pos,title2,1)

for i in range(len(Parameters2DList)/2):
	par2 = Parameters2DList[2*i]
	par1 = Parameters2DList[2*i+1]
	minimum2 = Parameters2DListMin[2*i]
	maximum2 = Parameters2DListMax[2*i]
	minimum1 = Parameters2DListMin[2*i+1]
	maximum1 = Parameters2DListMax[2*i+1]
	saveTuplePlot2D(events1,par1,par2,nBins,minimum1,maximum1,nBins,minimum2,maximum2,outfile,c,par1,par2,title1,1)
	saveTuplePlot2D(events2,par1,par2,nBins,minimum1,maximum1,nBins,minimum2,maximum2,outfile,c,par1,par2,title2,1)

closePDF(outfile,c)
