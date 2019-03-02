import sys
tmpargv = sys.argv
sys.argv = []
import getopt
from array import array
import ROOT
from ROOT import gROOT, TFile, TTree, TChain, gDirectory, TLine, gStyle, TCanvas, TLegend, TH2F
sys.argv = tmpargv

#List arguments
def print_usage():
    print "\nUsage: {0} <output file base name> <input file name>".format(sys.argv[0])
    print "Arguments: "
    print '\t-m: minimum uncVZ'
    print '\t-n: maximum uncVZ'
    print '\t-h: this help message'
    print

def getPlotX(string):
	arr = string.split(" ")
	return arr[0]

def getPlotY(string):
	arr = string.split(" ")
	if(len(arr) < 2): return ""
	else: return arr[1]

def getMinX(string):
	arr = string.split(" ")
	if(len(arr) < 3): return -9999
	else: return float(arr[2])

def getMaxX(string):
	arr = string.split(" ")
	if(len(arr) < 4): return -9999
	else: return float(arr[3])

def getMinY(string):
	arr = string.split(" ")
	if(len(arr) < 5): return -9999
	else: return float(arr[4])

def getMaxY(string):
	arr = string.split(" ")
	if(len(arr) < 6): return -9999
	else: return float(arr[5])

def getCut(string):
	arr = string.split(" ")
	if(len(arr) < 7): return ""
	else: return arr[6]

def getMin(string):
	arr = string.split(" ")
	if(len(arr) < 2): return -9999
	else: return float(arr[1])

def getMax(string):
	arr = string.split(" ")
	if(len(arr) < 3): return -9999
	else: return float(arr[2])

def openPDF(outfile,canvas):
	c.Print(outfile+".pdf[")

def closePDF(outfile,canvas):
	c.Print(outfile+".pdf]")

def saveTuplePlot2D(events,inHisto1,inHisto2,nBinsX,minX,maxX,nBinsY,minY,maxY,outfile,canvas,XaxisTitle="",YaxisTitle="",plotTitle="",cut="",stats=1,logY=0):
	events.Draw("{0}:{1}>>histo({2},{3},{4},{5},{6},{7})".format(inHisto2,inHisto1,nBinsX,minX,maxX,nBinsY,minY,maxY),cut)
	histo = ROOT.gROOT.FindObject("histo")
	histo.SetTitle(plotTitle)
	histo.GetXaxis().SetTitle(XaxisTitle)
	histo.GetYaxis().SetTitle(YaxisTitle)
	histo.SetStats(stats)
	histo.Draw("COLZ")
	canvas.SetLogy(logY)
	canvas.Print(outfile+".pdf")
	del histo

def plotVert(events,inHisto,nBinsX,minX,maxX,nBinsY,minY,maxY,outfile,canvas,XaxisTitle="",plotTitle="",cut="",stats=0,logY=0):
	events.Draw("{0}>>histoBad({1},{2},{3})".format("Bad"+inHisto,nBinsX,minX,maxX),cut)
	histoBad = ROOT.gROOT.FindObject("histoBad")
	events.Draw("{0}>>histoTruth({1},{2},{3})".format("Truth"+inHisto,nBinsX,minX,maxX),cut)
	histoTruth = ROOT.gROOT.FindObject("histoTruth")
	#histoBad = getHisto(events,"Bad"+inHisto,nBinsX,minX,maxX,cut)
	#histoTruth = getHisto(events,"Truth"+inHisto,nBinsX,minX,maxX,cut)
	maximum = histoBad.GetMaximum()
	if(histoTruth.GetMaximum() > maximum):
		maximum = histoTruth.GetMaximum()
	histoBad.SetTitle(plotTitle)
	histoBad.GetXaxis().SetTitle(XaxisTitle)
	histoBad.SetStats(stats)
	histoBad.GetYaxis().SetRangeUser(0,1.2*maximum)
	histoBad.Draw()
	canvas.SetLogy(logY)
	histoTruth.SetLineColor(2)
	histoTruth.Draw("same")
	legend = TLegend(.68,.66,.92,.87)
	legend.SetBorderSize(0)
	legend.SetFillColor(0)
	legend.SetFillStyle(0)
	legend.SetTextFont(42)
	legend.SetTextSize(0.035)
	legend.AddEntry(histoBad,"Bad Fit","LP")
	legend.AddEntry(histoTruth,"Truth Fit","LP")
	legend.Draw()
	canvas.Print(outfile+".pdf")
	saveTuplePlot2D(events,"Bad"+inHisto,"BaduncVZ",nBinsX,minX,maxX,nBinsY,minY,maxY,outfile,canvas,"Bad "+XaxisTitle,"Bad uncVZ [mm]",plotTitle,cut)
	saveTuplePlot2D(events,"Bad"+inHisto,"TruthuncVZ",nBinsX,minX,maxX,nBinsY,minY,maxY,outfile,canvas,"Bad "+XaxisTitle,"Truth uncVZ [mm]",plotTitle,cut)
	saveTuplePlot2D(events,"Truth"+inHisto,"BaduncVZ",nBinsX,minX,maxX,nBinsY,minY,maxY,outfile,canvas,"Truth "+XaxisTitle,"Bad uncVZ [mm]",plotTitle,cut)
	saveTuplePlot2D(events,"Truth"+inHisto,"TruthuncVZ",nBinsX,minX,maxX,nBinsY,minY,maxY,outfile,canvas,"Truth "+XaxisTitle,"Truth uncVZ [mm]",plotTitle,cut)
	del histoBad
	del histoTruth
	del legend

def plotPart(events,inHisto,nBinsX,minX,maxX,nBinsY,minY,maxY,outfile,canvas,XaxisTitle="",plotTitle="",cut="",stats=0,logY=0):
	events.Draw("{0}>>histoEleBad({1},{2},{3})".format("eleBad"+inHisto,nBinsX,minX,maxX),cut)
	histoEleBad = ROOT.gROOT.FindObject("histoEleBad")
	events.Draw("{0}>>histoEleTruth({1},{2},{3})".format("eleTruth"+inHisto,nBinsX,minX,maxX),cut)
	histoEleTruth = ROOT.gROOT.FindObject("histoEleTruth")
	events.Draw("{0}>>histoPosBad({1},{2},{3})".format("posBad"+inHisto,nBinsX,minX,maxX),cut)
	histoPosBad = ROOT.gROOT.FindObject("histoPosBad")
	events.Draw("{0}>>histoPosTruth({1},{2},{3})".format("posTruth"+inHisto,nBinsX,minX,maxX),cut)
	histoPosTruth = ROOT.gROOT.FindObject("histoPosTruth")
	#histoEleBad = getHisto(events,"eleBad"+inHisto,nBinsX,minX,maxX,cut)
	#histoEleTruth = getHisto(events,"eleTruth"+inHisto,nBinsX,minX,maxX,cut)
	#histoPosBad = getHisto(events,"posBad"+inHisto,nBinsX,minX,maxX,cut)
	#histoPosTruth = getHisto(events,"posTruth"+inHisto,nBinsX,minX,maxX,cut)
	maximumEle = histoEleBad.GetMaximum()
	if(histoEleTruth.GetMaximum() > maximumEle):
		maximumEle = histoEleTruth.GetMaximum()
	maximumPos = histoPosBad.GetMaximum()
	if(histoPosTruth.GetMaximum() > maximumPos):
		maximumPos = histoPosTruth.GetMaximum()
	histoEleBad.SetTitle("Ele "+plotTitle)
	histoEleBad.GetXaxis().SetTitle(XaxisTitle)
	histoEleBad.SetStats(stats)
	histoEleBad.GetYaxis().SetRangeUser(0,1.2*maximumEle)
	histoEleBad.Draw()
	canvas.SetLogy(logY)
	histoEleTruth.SetLineColor(2)
	histoEleTruth.Draw("same")
	legend = TLegend(.68,.66,.92,.87)
	legend.SetBorderSize(0)
	legend.SetFillColor(0)
	legend.SetFillStyle(0)
	legend.SetTextFont(42)
	legend.SetTextSize(0.035)
	legend.AddEntry(histoEleBad,"Bad Fit","LP")
	legend.AddEntry(histoEleTruth,"Truth Fit","LP")
	legend.Draw()
	canvas.Print(outfile+".pdf")
	histoPosBad.SetTitle("Pos "+plotTitle)
	histoPosBad.GetXaxis().SetTitle(XaxisTitle)
	histoPosBad.SetStats(stats)
	histoPosBad.GetYaxis().SetRangeUser(0,1.2*maximumPos)
	histoPosBad.Draw()
	canvas.SetLogy(logY)
	histoPosTruth.SetLineColor(2)
	histoPosTruth.Draw("same")
	legend.Draw()
	canvas.Print(outfile+".pdf")
	saveTuplePlot2D(events,"eleBad"+inHisto,"BaduncVZ",nBinsX,minX,maxX,nBinsY,minY,maxY,outfile,canvas,"Bad Ele "+XaxisTitle,"Bad uncVZ [mm]",plotTitle,cut)
	saveTuplePlot2D(events,"eleBad"+inHisto,"TruthuncVZ",nBinsX,minX,maxX,nBinsY,minY,maxY,outfile,canvas,"Bad Ele "+XaxisTitle,"Truth uncVZ [mm]",plotTitle,cut)
	saveTuplePlot2D(events,"eleTruth"+inHisto,"BaduncVZ",nBinsX,minX,maxX,nBinsY,minY,maxY,outfile,canvas,"Truth Ele "+XaxisTitle,"Bad uncVZ [mm]",plotTitle,cut)
	saveTuplePlot2D(events,"eleTruth"+inHisto,"TruthuncVZ",nBinsX,minX,maxX,nBinsY,minY,maxY,outfile,canvas,"Truth Ele "+XaxisTitle,"Truth uncVZ [mm]",plotTitle,cut)
	saveTuplePlot2D(events,"posBad"+inHisto,"BaduncVZ",nBinsX,minX,maxX,nBinsY,minY,maxY,outfile,canvas,"Bad Pos "+XaxisTitle,"Bad uncVZ [mm]",plotTitle,cut)
	saveTuplePlot2D(events,"posBad"+inHisto,"TruthuncVZ",nBinsX,minX,maxX,nBinsY,minY,maxY,outfile,canvas,"Bad Pos "+XaxisTitle,"Truth uncVZ [mm]",plotTitle,cut)
	saveTuplePlot2D(events,"posTruth"+inHisto,"BaduncVZ",nBinsX,minX,maxX,nBinsY,minY,maxY,outfile,canvas,"Truth Pos "+XaxisTitle,"Bad uncVZ [mm]",plotTitle,cut)
	saveTuplePlot2D(events,"posTruth"+inHisto,"TruthuncVZ",nBinsX,minX,maxX,nBinsY,minY,maxY,outfile,canvas,"Truth Pos "+XaxisTitle,"Truth uncVZ [mm]",plotTitle,cut)
	del histoEleBad
	del histoEleTruth
	del histoPosBad
	del histoPosTruth
	del legend

def getHisto(events,inHisto,nBinsX,minX,maxX,cut=""):
	events.Draw("{0}>>histo({1},{2},{3})".format(inHisto,nBinsX,minX,maxX),cut)
	histo = ROOT.gROOT.FindObject("histo")
	print histo
	print inHisto
	return histo

minVZ = -30
maxVZ = 80
maxTheta = 0.03
minTheta = -maxTheta

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'm:n:h')

# Parse the command line arguments
for opt, arg in options:
		if opt=='-m':
			minVZ = float(arg)
		if opt=='-n':
			maxVZ = float(arg)
		if opt=='-h':
			print_usage()
			sys.exit(0)

gStyle.SetOptStat(110011)
c = TCanvas("c","c",800,600)

outfile = remainder[0]
events = TChain("ntuple")
for i in range(1,len(remainder)):
    events.Add(remainder[i])

nBins = 100
minX = ""
maxX = ""
minY = ""
maxY = ""

isoEle = "eleMinPositiveIso+0.5*(eleTrkZ0+0.5*elePY/eleP)*sign(elePY)"
isoPos = "posMinPositiveIso+0.5*(posTrkZ0+0.5*posPY/posP)*sign(posPY)"

minx = -30
maxx = -minx
miny = -8
maxy = -miny
maxTheta = 0.03
minTheta = -maxTheta
#vertcuts = "BaduncP<9999"
vertcuts = "(pow((BaduncVX-(BaduncVZ-0.5)*BaduncPX/BaduncPZ-0.1)*cos(-0.5)-(BaduncVY-(BaduncVZ-0.5)*BaduncPY/BaduncPZ)*sin(-0.5),2)/0.4356+pow((BaduncVX-(BaduncVZ-0.5)*BaduncPX/BaduncPZ)*sin(-0.5)+(BaduncVY-(BaduncVZ-0.5)*BaduncPY/BaduncPZ)*cos(-0.5),2)/0.3249)<1&&eleBadHasL1&&posBadHasL1&&isPair1&&max(eleBadMatchChisq,posBadMatchChisq)<10&&max(abs(eleBadClT-eleBadTrkT-{1}),abs(posBadClT-posBadTrkT-{1}))<4&&abs(eleBadClT-posBadClT)<2&&eleBadClY*posBadClY<0&&BadbscChisq<10&&BadbscChisq-BaduncChisq<5&&max(eleBadTrkChisq/eleBadNTrackHits,posBadTrkChisq/posBadNTrackHits)<5&&abs(eleBadP-posBadP)/(eleBadP+posBadP)<0.5&&eleBadP<{0}*0.75&&BaduncP<{0}*1.15&&BaduncP>{0}*0.8&&eleBadHasL2&&posBadHasL2&&abs(eleBadPhiKink1)<0.0001&&abs(posBadPhiKink1)<0.0001&&abs(eleBadPhiKink2)<0.002&&abs(posBadPhiKink2)<0.002&&abs(eleBadPhiKink3)<0.002&&abs(posBadPhiKink3)<0.002&&abs(eleBadLambdaKink1)<0.002&&abs(posBadLambdaKink1)<0.002&&abs(eleBadLambdaKink2)<0.004&&abs(posBadLambdaKink2)<0.004&&abs(eleBadLambdaKink3)<0.004&&abs(posBadLambdaKink3)<0.004".format(1.05,43)

cuts = []
cuts.append("BaduncP<9999")
#cuts.append("BaduncP>0.8")
#cuts.append("elePurity<0.99||posPurity<0.99")
#cuts.append("elePurity>0.99&&posPurity<0.99")
#cuts.append("elePurity<0.99&&posPurity>0.99")
#cuts.append("elePurity<0.99&&posPurity<0.99")

plotsvert = []
plotsvert.append("uncVZ {0} {1}".format(minVZ,maxVZ))
plotsvert.append("uncCovZZ 0 400")
plotsvert.append("uncVX -1 1")
plotsvert.append("uncVY -1 1")
plotsvert.append("uncM 0 0.1")
plotsvert.append("uncChisq 0 20")
plotsvert.append("bscChisq 0 20")
plotsvert.append("tarChisq 0 50")
plotsvert.append("uncTargProjX -1 1")
plotsvert.append("uncTargProjY -1 1")

plotspart = []
plotspart.append("TrkChisq 0 50")
plotspart.append("TrkZ0 -5 5")
plotspart.append("MinPositiveIso 0 10")
#plotspart.append("LambdaKink0 -0.01 0.01")
plotspart.append("LambdaKink1 -0.01 0.01")
plotspart.append("LambdaKink2 -0.01 0.01")
plotspart.append("LambdaKink3 -0.01 0.01")
#plotspart.append("LambdaKink4 -0.01 0.01")
#plotspart.append("LambdaKink5 -0.01 0.01")
#plotspart.append("LambdaKink6 -0.01 0.01")
#plotspart.append("PhiKink0 -0.01 0.01")
plotspart.append("PhiKink1 -0.01 0.01")
plotspart.append("PhiKink2 -0.01 0.01")
plotspart.append("PhiKink3 -0.01 0.01")
#plotspart.append("PhiKink4 -0.01 0.01")
#plotspart.append("PhiKink5 -0.01 0.01")
#plotspart.append("PhiKink6 -0.01 0.01")

plots2D = []
plots2D.append("eleL1tthetaY+eleL2tthetaY BaduncVZ {0} {1} {2} {3}".format(minTheta,maxTheta,minVZ,maxVZ))
plots2D.append("posL1tthetaY+posL2tthetaY BaduncVZ {0} {1} {2} {3}".format(minTheta,maxTheta,minVZ,maxVZ))
plots2D.append("eleL1tthetaY+eleL2tthetaY TruthuncVZ {0} {1} {2} {3}".format(minTheta,maxTheta,minVZ,maxVZ))
plots2D.append("posL1tthetaY+posL2tthetaY TruthuncVZ {0} {1} {2} {3}".format(minTheta,maxTheta,minVZ,maxVZ))
plots2D.append("eleL3tthetaY+eleL4tthetaY BaduncVZ {0} {1} {2} {3}".format(minTheta,maxTheta,minVZ,maxVZ))
plots2D.append("posL3tthetaY+posL4tthetaY BaduncVZ {0} {1} {2} {3}".format(minTheta,maxTheta,minVZ,maxVZ))
plots2D.append("eleL3tthetaY+eleL4tthetaY TruthuncVZ {0} {1} {2} {3}".format(minTheta,maxTheta,minVZ,maxVZ))
plots2D.append("posL3tthetaY+posL4tthetaY TruthuncVZ {0} {1} {2} {3}".format(minTheta,maxTheta,minVZ,maxVZ))

#rootfile = TFile(outfile+".root","recreate")

openPDF(outfile,c)

for i in range(len(cuts)):
	for j in range(len(plotsvert)):
		plot = getPlotX(plotsvert[j])
		minX = getMin(plotsvert[j])
		maxX = getMax(plotsvert[j])
		if(i != 0):
			plotVert(events,plot,nBins,minX,maxX,nBins,minVZ,maxVZ,outfile,c,plot,plot+" "+cuts[i],cuts[i])
			plotVert(events,plot,nBins,minX,maxX,nBins,minVZ,maxVZ,outfile,c,plot,plot+" With Vert Cuts "+cuts[i],cuts[i]+"&&"+vertcuts)
		else:
			plotVert(events,plot,nBins,minX,maxX,nBins,minVZ,maxVZ,outfile,c,plot,plot,cuts[i])
			plotVert(events,plot,nBins,minX,maxX,nBins,minVZ,maxVZ,outfile,c,plot,plot+" With Vert Cuts",cuts[i]+"&&"+vertcuts)

	for j in range(len(plotspart)):
		plot = getPlotX(plotspart[j])
		minX = getMin(plotspart[j])
		maxX = getMax(plotspart[j])
		if(i != 0):
			plotPart(events,plot,nBins,minX,maxX,nBins,minVZ,maxVZ,outfile,c,plot,plot+" "+cuts[i],cuts[i])
			plotPart(events,plot,nBins,minX,maxX,nBins,minVZ,maxVZ,outfile,c,plot,plot+" With Vert Cuts "+cuts[i],cuts[i]+"&&"+vertcuts)
		else:
			plotPart(events,plot,nBins,minX,maxX,nBins,minVZ,maxVZ,outfile,c,plot,plot,cuts[i])
			plotPart(events,plot,nBins,minX,maxX,nBins,minVZ,maxVZ,outfile,c,plot,plot+" With Vert Cuts",cuts[i]+"&&"+vertcuts)

	for j in range(0,len(plots2D)):
		x = getPlotX(plots2D[j])
		y = getPlotY(plots2D[j])
		minX = getMinX(plots2D[j])
		maxX = getMaxX(plots2D[j])
		minY = getMinY(plots2D[j])
		maxY = getMaxY(plots2D[j])
		if(i != 0):
			saveTuplePlot2D(events,x,y,nBins,minX,maxX,nBins,minY,maxY,outfile,c,x,y,y+" vs "+x+" "+cuts[i],cuts[i],1)
		else:
			saveTuplePlot2D(events,x,y,nBins,minX,maxX,nBins,minY,maxY,outfile,c,x,y,y+" vs "+x,cuts[i],1)

closePDF(outfile,c)
#rootfile.Close()