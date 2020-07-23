import sys
tmpargv = sys.argv
sys.argv = []
import getopt
import ROOT
from ROOT import gROOT, TFile, TTree, TChain, gDirectory, TLine, gStyle, TCanvas, TLegend, TH1F
sys.argv = tmpargv

#List arguments
def print_usage():
    print "\nUsage: {0} <output file base name> <input file name>".format(sys.argv[0])
    print '\t-m: minimum uncVZ'
    print '\t-n: maximum uncVZ'
    print '\t-b: number of bins'
    print '\t-e: beam energy'
    print '\t-t: track time diff offset'
    print '\t-x: beam x position'
    print '\t-y: beam y position'
    print '\t-z: target z position'
    print '\t-p: plot 2D plots'
    print '\t-a: plot in mass slices'
    print '\t-d: use data'
    print '\t-l: use L1L2'
    print '\t-h: this help message'
    print

#Default Values
minVZ = -40
maxVZ = 40
nBins = 100
energy = 2.3
trackTDiff = 43 #only for MC, should be ~55 for data
beamX =  -0.091683900354
beamY = -0.0768593640179
uncVXSig = 0.215941433591
uncVYSig = 0.0880585145088
targZ = -4.3
plot2D = False
plotMassSlices = False
L1L2 = False
useData = False
nentries = 99999999999999
minMass = 0.03
maxMass = 0.15
massBin = 0.01
nMass = int((maxMass - minMass) / massBin + 1)

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'm:n:b:e:t:x:y:z:s:dlpah')

# Parse the command line arguments
for opt, arg in options:
		if opt=='-m':
			minVZ = float(arg)
		if opt=='-n':
			maxVZ = float(arg)
		if opt=='-b':
			nBins = float(arg)
		if opt=='-e':
			energy = float(arg)
		if opt=='-t':
			trackTDiff = float(arg)
		if opt=='-x':
			beamX = float(arg)
		if opt=='-y':
			beamY = float(arg)
		if opt=='-z':
			targZ = float(arg)
		if opt=='-s':
			nentries = int(arg)
		if opt=='-p':
			plot2D = True
		if opt=='-a':
			plotMassSlices = True
		if opt=='-d':
			useData = True
		if opt=='-l':
			L1L2 = True
		if opt=='-h':
			print_usage()
			sys.exit(0)

gStyle.SetOptStat(0)
c = TCanvas("c","c",800,600)

#Save plot to pdf and root file
def saveTuplePlot(events,inHisto,nBins,minX,maxX,outfile,canvas,XaxisTitle="",YaxisTitle="",plotTitle="",nentries=0,stats=0,logY=0,cuts=""):
	events.Draw("{0}>>histo({1},{2},{3})".format(inHisto,nBins,minX,maxX),cuts,"",nentries)
	histo = ROOT.gROOT.FindObject("histo")
	histo.SetTitle(plotTitle)
	histo.GetXaxis().SetTitle(XaxisTitle)
	histo.GetYaxis().SetTitle(YaxisTitle)
	histo.SetStats(stats)
	histo.Draw()
	canvas.SetLogy(logY)
	canvas.Print(outfile+".pdf")
	histo.Write(plotTitle)
	del histo


#Save 2D plot to pdf and root file
def saveTuplePlot2D(events,inHisto1,inHisto2,nBinsX,minX,maxX,nBinsY,minY,maxY,outfile,canvas,XaxisTitle="",YaxisTitle="",plotTitle="",nentries=0,stats=0,logY=0,cuts=""):
	events.Draw("{0}:{1}>>histo({2},{3},{4},{5},{6},{7})".format(inHisto2,inHisto1,nBinsX,minX,maxX,nBinsY,minY,maxY),cuts,"",nentries)
	histo = ROOT.gROOT.FindObject("histo")
	histo.SetTitle(plotTitle)
	histo.GetXaxis().SetTitle(XaxisTitle)
	histo.GetYaxis().SetTitle(YaxisTitle)
	histo.SetStats(stats)
	histo.Draw("COLZ")
	canvas.SetLogy(logY)
	canvas.SetLogz(1)
	canvas.Print(outfile+".pdf")
	histo.Write(plotTitle)
	del histo

def openPDF(outfile,canvas):
	c.Print(outfile+".pdf[")

def closePDF(outfile,canvas):
	c.Print(outfile+".pdf]")

#Grab name of plot
def getPlot(string):
	arr = string.split(" ")
	return arr[0]

#Grab name of 2D plot
def getPlot2D(string):
	arr = string.split(" ")
	if(len(arr) < 2): return ""
	else: return arr[1]

#Get minimum x value
def getMinX(string):
	arr = string.split(" ")
	if(len(arr) < 2): return -9999
	else: return float(arr[1])

#Get maximum x value
def getMaxX(string):
	arr = string.split(" ")
	if(len(arr) < 3): return -9999
	else: return float(arr[2])

#Get minimum x value for 2D plot
def getMinX2D(string):
	arr = string.split(" ")
	if(len(arr) < 3): return -9999
	else: return float(arr[2])

#Get maximum x value for 2D plot
def getMaxX2D(string):
	arr = string.split(" ")
	if(len(arr) < 4): return -9999
	else: return float(arr[3])

#Get minimum y value for 2D plot
def getMinY(string):
	arr = string.split(" ")
	if(len(arr) < 5): return -9999
	else: return float(arr[4])

#Get maximum y value for 2D plot
def getMaxY(string):
	arr = string.split(" ")
	if(len(arr) < 6): return -9999
	else: return float(arr[5])

#Base name of outfile
outfile = remainder[0]

#Create a TChain
#Loop over all files
events = TChain("ntuple")
for i in range(1,len(remainder)):
    events.Add(remainder[i])

#List of cuts
cuts = ""
#Example list of cuts
#cuts="isPair1&&max(eleMatchChisq,posMatchChisq)<10&&max(abs(eleClT-eleTrkT-{1}),abs(posClT-posTrkT-{1}))<4&&abs(eleClT-posClT)<2&&
    #bscChisq<10&&bscChisq-uncChisq<5&&eleP<{0}*0.75&&uncP<{0}*1.15&&uncP>{0}*0.8&&eleHasL2&&posHasL2".format(energy,trackTDiff)

eleiso = "eleMinPositiveIso+0.5*((eleTrkZ0+{0}*elePY/eleP)*sign(elePY)-3*(eleTrkZ0Err+abs({0}*eleTrkLambdaErr)+abs(2*{0}*eleTrkLambda*eleTrkOmegaErr/eleTrkOmega)))".format(targZ)
posiso = "posMinPositiveIso+0.5*((posTrkZ0+{0}*posPY/posP)*sign(posPY)-3*(posTrkZ0Err+abs({0}*posTrkLambdaErr)+abs(2*{0}*posTrkLambda*posTrkOmegaErr/posTrkOmega)))".format(targZ)

#x0_cut1_pos_x0 = -0.2289
#x1_cut1_pos_x0 = -1.09

#x0_cut1_neg_x0 = -0.0009241
#x1_cut1_neg_x0 = -1.612

#x0_cut1_pos_x1 = 0.009205
#x1_cut1_pos_x1 = 0.2069

#x0_cut1_neg_x1 = 0.0091
#x1_cut1_neg_x1 = 0.2341

m0 = -0.201776054859
a0 = 0.0518988558564
a1 = -0.00230111045957
b0 = 0.0471576968062
b1 = -0.00108639651791

dz = "0."
if(useData):
	dz = "((-3.517-13.41*uncM+88.16*uncM^2-173.1*uncM^3)-(-3.14-27.2*uncM+144*uncM^2-257.1*uncM^3))"
	beamX = -0.113246598948
	beamY = -0.0860657518949
	uncVXSig = 0.318293608185
	uncVYSig = 0.0992756085509
	trackTDiff = 56

if(L1L2):
	#x0_cut1_pos_x0 = -0.3187
	#x1_cut1_pos_x0 = -0.9498

	#x0_cut1_neg_x0 = -0.09418
	#x1_cut1_neg_x0 = -0.7761

	#x0_cut1_pos_x1 = 0.02095
	#x1_cut1_pos_x1 = 0.05914

	#x0_cut1_neg_x1 = 0.02016
	#x1_cut1_neg_x1 = 0.05854

	m0 = -0.167438502208
	a0 = 0.016762652862
	a1 = 0.00033162637213
	b0 = 0.0207347770085
	b1 = 0.000331699098944

	eleisoL1 = "eleMinPositiveIso+0.5*((eleTrkZ0+{0}*elePY/eleP)*sign(elePY)-3*(eleTrkZ0Err+abs({0}*eleTrkLambdaErr)+abs(2*{0}*eleTrkLambda*eleTrkOmegaErr/eleTrkOmega)))".format(targZ)
	posisoL1 = "posMinPositiveIso+0.5*((posTrkZ0+{0}*posPY/posP)*sign(posPY)-3*(posTrkZ0Err+abs({0}*posTrkLambdaErr)+abs(2*{0}*posTrkLambda*posTrkOmegaErr/posTrkOmega)))".format(targZ)

	eleisoL2 = "eleMinPositiveIsoL2+1/3.*((eleTrkZ0+{0}*elePY/eleP)*sign(elePY)-3*(eleTrkZ0Err+abs({0}*eleTrkLambdaErr)+abs(2*{0}*eleTrkLambda*eleTrkOmegaErr/eleTrkOmega)))".format(targZ)
	posisoL2 = "posMinPositiveIsoL2+1/3.*((posTrkZ0+{0}*posPY/posP)*sign(posPY)-3*(posTrkZ0Err+abs({0}*posTrkLambdaErr)+abs(2*{0}*posTrkLambda*posTrkOmegaErr/posTrkOmega)))".format(targZ)

	uncVXSig = 1.25 * uncVXSig
	uncVYSig = 1.5 * uncVYSig

#x0_cut1_pos = "({0}+{1}*uncM)".format(x0_cut1_pos_x0,x1_cut1_pos_x0)
#x1_cut1_pos = "({0}+{1}*uncM)".format(x0_cut1_pos_x1,x1_cut1_pos_x1)
#cut1_pos = "({0}+{1}*(uncVZ+{2}))".format(x0_cut1_pos,x1_cut1_pos,dz)

#x0_cut1_neg = "({0}+{1}*uncM)".format(x0_cut1_neg_x0,x1_cut1_neg_x0)
#x1_cut1_neg = "({0}+{1}*uncM)".format(x0_cut1_neg_x1,x1_cut1_neg_x1)
#cut1_neg = "({0}+{1}*(uncVZ+{2}))".format(x0_cut1_neg,x1_cut1_neg,dz)

cut1_pos = "({0}+{1}*(uncVZ+{3})+{2}*1/uncM^1*(uncVZ+{3}))".format(m0,a0,a1,dz)
cut1_neg = "({0}+{1}*(uncVZ+{3})+{2}*1/uncM^1*(uncVZ+{3}))".format(m0,b0,b1,dz)

rootfile = TFile(outfile+".root","recreate")

#List of plots
plots = []
plots.append("uncVZ {0} {1}".format(minVZ,maxVZ))
plots.append("uncVY -0.6 0.6")
plots.append("uncVX -1.5 1.5")
plots.append("uncM 0 {0}".format(0.1*energy))
plots.append("uncP 0 {0}".format(1.6*energy))
plots.append("uncChisq 0 5")
plots.append("bscChisq 0 40")
plots.append("eleP 0 {0}".format(1.6*energy))
plots.append("posP 0 {0}".format(1.6*energy))
plots.append("eleTrkChisq/(2*eleNTrackHits-5) 0 6")
plots.append("posTrkChisq/(2*posNTrackHits-5) 0 6")
plots.append("eleTrkChisq/(2*eleNTrackHits-5)+posTrkChisq/(2*posNTrackHits-5) 0 12")
plots.append("eleClT-eleTrkT-{0} -10 10".format(trackTDiff))
plots.append("posClT-posTrkT-{0} -10 10".format(trackTDiff))
plots.append("eleTrkZ0 -2 2")
plots.append("posTrkZ0 -2 2")
#plots.append("eleClE/eleP 0 2")
#plots.append("posClE/posP 0 2")
plots.append("eleMatchChisq 0 10")
plots.append("posMatchChisq 0 10")
plots.append("eleMatchChisq+posMatchChisq 0 20")
plots.append("bscChisq-uncChisq 0 40")
plots.append("nPos 0 10")
plots.append("(eleP-posP)/uncP -1 1")
plots.append("uncTargProjX-{0} -1 1".format(beamX))
plots.append("uncTargProjY-{0} -0.5 0.5".format(beamY))
plots.append("(uncVX-(uncVZ-{1})*uncPX/uncPZ)-{0} -1 1".format(beamX,targZ))
plots.append("(uncVY-(uncVZ-{1})*uncPY/uncPZ)-{0} -0.5 0.5".format(beamY,targZ))
plots.append("sqrt((abs(uncVX-{0})/(3*{1}))^2+(abs(uncVY-{2})/(3*{3}))^2) 0 2".format(beamX,uncVXSig,beamY,uncVYSig))
plots.append("sqrt((abs((uncVX-(uncVZ-{4})*uncPX/uncPZ)-{0})/(2*{1}))^2+(abs((uncVY-(uncVZ-{4})*uncPY/uncPZ)-{2})/(2*{3}))^2) 0 2".format(beamX,uncVXSig,beamY,uncVYSig,targZ))
plots.append("(uncVZ-{0})/sqrt(uncCovZZ) -20 20".format(targZ))
plots.append("sqrt(uncCovZZ) 0 10")
if(not L1L2):
	plots.append("{0} -3 7".format(eleiso))
	plots.append("{0} -3 7".format(posiso))
else:
	plots.append("{0} -3 7".format(eleisoL1))
	plots.append("{0} -3 7".format(posisoL1))
	plots.append("{0} -3 7".format(eleisoL2))
	plots.append("{0} -3 7".format(posisoL2))
plots.append("eleTrkZ0-{0} -1 4".format(cut1_pos))
plots.append("posTrkZ0-{0} -1 4".format(cut1_pos))
plots.append("-eleTrkZ0-{0} -1 4".format(cut1_neg))
plots.append("-posTrkZ0-{0} -1 4".format(cut1_neg))
plots.append("nSVTHitsL1 0 500")
plots.append("nSVTHitsL1b 0 500")
plots.append("eleNHitsShared 0 7")
plots.append("posNHitsShared 0 7")
plots.append("eleNHitsShared+posNHitsShared 0 14")
plots.append("run 5000 9000")

#List of 2D plots
plots2D = []
plots2D.append("uncM uncVZ 0 {2} {0} {1}".format(minVZ,maxVZ,0.1*energy))

openPDF(outfile,c)

#Loop over list of 2D plots
for i in range(len(plots2D)):
	plot1 = getPlot(plots2D[i]) #x axis variable
	plot2 = getPlot2D(plots2D[i]) #y axis variable
	minX = getMinX2D(plots2D[i])
	maxX = getMaxX2D(plots2D[i])
	minY = getMinY(plots2D[i])
	maxY = getMaxY(plots2D[i])
	saveTuplePlot2D(events,plot1,plot2,nBins,minX,maxX,nBins,minY,maxY,outfile,c,plot1,plot2,plot2+" vs "+plot1,nentries,cuts=cuts)


#Loop over list of plots
for i in range(len(plots)):
	plot = getPlot(plots[i]) #variable to be plotted
	minX = getMinX(plots[i])
	maxX = getMaxX(plots[i])
	saveTuplePlot(events,plot,nBins,minX,maxX,outfile,c,plot,"",plot,nentries,cuts=cuts)
	if(plot2D): saveTuplePlot2D(events,"uncVZ",plot,nBins,minVZ,maxVZ,nBins,minX,maxX,outfile,c,"uncVZ",plot,plot+" vs uncVZ",nentries,cuts=cuts)

	#Loop over list of plots
if(plotMassSlices):
	for j in range(nMass):
		mass = minMass + j * massBin
		for i in range(len(plots)):
			plot = getPlot(plots[i]) #variable to be plotted
			minX = getMinX(plots[i])
			maxX = getMaxX(plots[i])
			massCut = "abs(uncM-{0})<{1}/2".format(mass,massBin)
			if(cuts == ""): cut = massCut
			else: cut = cuts + "&&" + massCut
			saveTuplePlot(events,plot,nBins,minX,maxX,outfile,c,plot,"",plot+" {0:.3f} < uncM < {1:.3f} GeV".format(mass-massBin/2.,mass+massBin/2.),nentries,cuts=cut)
			if(plot2D): saveTuplePlot2D(events,"uncVZ",plot,nBins,minVZ,maxVZ,nBins,minX,maxX,outfile,c,"uncVZ",plot,plot+" vs uncVZ {0:.3f} < uncM < {1:.3f} GeV".format(mass-massBin/2.,mass+massBin/2.),nentries,cuts=cut)

closePDF(outfile,c)

rootfile.Close()