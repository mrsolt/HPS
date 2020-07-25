import sys
tmpargv = sys.argv
sys.argv = []
import getopt
import ROOT
from ROOT import gROOT, TFile, TTree, TChain, gDirectory, TLine, gStyle, TCanvas, TLegend, TH1F, TF1
sys.argv = tmpargv

#List arguments
def print_usage():
    print "\nUsage: {0} <output file base name> <input A' text file>".format(sys.argv[0])
    print "Arguments: "
    print '\t-c: z bin size'
    print '\t-d: number of fitted z bins'
    print '\t-s: save fitted histograms'
    print '\t-m: minimum uncVZ'
    print '\t-n: maximum uncVZ'
    print '\t-f: fraction of events'
    print '\t-h: this help message'
    print

#minVZ = 7
#maxVZ = 32
minVZ = 60
maxVZ = 120
nZ = 25
zBin = 2
saveFits = False
frac = 0.9
beamY = 0. #-0.0768593640179

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'c:d:sm:n:f:h')

# Parse the command line argumentz
for opt, arg in options:
		if opt=='-c':
			zBin = float(arg)
		if opt=='-d':
			nZ = float(arg)
		if opt=='-s':
			saveFits = True
		if opt=='-m':
			minVZ = float(arg)
		if opt=='-n':
			maxVZ = float(arg)
		if opt=='-f':
			frac = float(arg)
		if opt=='-h':
			print_usage()
			sys.exit(0)

gStyle.SetOptStat(0)
gStyle.SetOptFit(1011)
c = TCanvas("c","c",800,600)

def draw2DHisto(events,nBins,minX,maxX,minY,maxY,outfile,canvas,fitfuncpos,fitfuncneg,cut="",XaxisTitle="Reconstructed z (mm)",YaxisTitle="Z0 (mm)",plotTitle="",stats=0):
	events.Draw("{1}:{0}>>histo({2},{3},{4},{5},{6},{7})".format("uncVZ","eleTrkZ0",nBins,minX,maxX,nBins,minY,maxY))
	events.Draw("{1}:{0}>>histo2({2},{3},{4},{5},{6},{7})".format("uncVZ","posTrkZ0",nBins,minX,maxX,nBins,minY,maxY))
	events.Draw("{1}:{0}>>histocut({2},{3},{4},{5},{6},{7})".format("uncVZ","eleTrkZ0",nBins,minX,maxX,nBins,minY,maxY),cut)
	events.Draw("{1}:{0}>>histocut2({2},{3},{4},{5},{6},{7})".format("uncVZ","posTrkZ0",nBins,minX,maxX,nBins,minY,maxY),cut)
	histo = ROOT.gROOT.FindObject("histo")
	histo2 = ROOT.gROOT.FindObject("histo2")
	histocut = ROOT.gROOT.FindObject("histocut")
	histocut2 = ROOT.gROOT.FindObject("histocut2")
	histo.Add(histo2)
	histocut.Add(histocut2)
	fitfuncpos.SetParameter(0,mass)
	fitfuncneg.SetParameter(0,mass)
	canvas.SetLogz()
	histo.Draw("COLZ")
	histo.SetTitle(plotTitle+" No IP Cut")
	histo.GetXaxis().SetTitle(XaxisTitle)
	histo.GetYaxis().SetTitle(YaxisTitle)
	histo.SetStats(stats)
	fitfuncpos.Draw("same")
	fitfuncneg.Draw("same")
	#canvas.Write()
	canvas.Print(outfile+".pdf")
	histocut.Draw("COLZ")
	histocut.SetTitle(plotTitle+" With IP Cut")
	histocut.GetXaxis().SetTitle(XaxisTitle)
	histocut.GetYaxis().SetTitle(YaxisTitle)
	histocut.SetStats(stats)
	#canvas.Write()
	fitfuncpos.Draw("same")
	fitfuncneg.Draw("same")
	canvas.Print(outfile+".pdf")
	del histo
	del histo2
	del histocut
	del histocut2

def drawHisto(histo,minX,maxX,XaxisTitle="",YaxisTitle="",plotTitle="",stats=0):
	histo.Fit("pol1")
	fit = histo.GetFunction("pol1")
	histo.Draw("")
	#histo.GetXaxis().SetRangeUser(-5,150)
	histo.GetYaxis().SetRangeUser(minX,maxX)
	histo.SetTitle(plotTitle)
	histo.GetXaxis().SetTitle(XaxisTitle)
	histo.GetYaxis().SetTitle(YaxisTitle)
	histo.SetStats(stats)
	return [fit.GetParameter(0),fit.GetParameter(1),fit.GetParError(0),fit.GetParError(1)]

def saveHisto(histo,minX,maxX,outfile,canvas,XaxisTitle="",YaxisTitle="",plotTitle="",stats=0):
	x0, x1, x0Err, x1Err = drawHisto(histo,minX,maxX,XaxisTitle,YaxisTitle,plotTitle,stats)
	canvas.Write()
	canvas.Print(outfile+".pdf")
	return [x0, x1, x0Err, x1Err]

def fitSlice(events,inHisto2,nBinsX,minX,maxX,nBinsY,minY,maxY,outfile,canvas,index=0,z=0,zRange=9999,saveFits=False,frac1=0.9,beamY=0.):
	ex = "Null Fit"
	if(index == 0):
		bound = ">"
		events.Draw("{0}-{8}:{1}>>histo({2},{3},{4},{5},{6},{7})".format(inHisto2,"eleTrkZ0",nBinsX,minX,maxX,nBinsY,minY,maxY,beamY),"uncVZ>{0}-{1}&&uncVZ<{0}+{1}&&{2}{3}{4}".format(z,zRange,"eleTrkZ0",bound,beamY))
		events.Draw("{0}-{8}:{1}>>histo2({2},{3},{4},{5},{6},{7})".format(inHisto2,"posTrkZ0",nBinsX,minX,maxX,nBinsY,minY,maxY,beamY),"uncVZ>{0}-{1}&&uncVZ<{0}+{1}&&{2}{3}{4}".format(z,zRange,"posTrkZ0",bound,beamY))
	elif(index == 1):
		bound = "<"
		events.Draw("{0}+{8}:{1}>>histo({2},{3},{4},{5},{6},{7})".format(inHisto2,"-eleTrkZ0",nBinsX,minX,maxX,nBinsY,minY,maxY,beamY),"uncVZ>{0}-{1}&&uncVZ<{0}+{1}&&{2}{3}{4}".format(z,zRange,"eleTrkZ0",bound,beamY))
		events.Draw("{0}+{8}:{1}>>histo2({2},{3},{4},{5},{6},{7})".format(inHisto2,"-posTrkZ0",nBinsX,minX,maxX,nBinsY,minY,maxY,beamY),"uncVZ>{0}-{1}&&uncVZ<{0}+{1}&&{2}{3}{4}".format(z,zRange,"posTrkZ0",bound,beamY))
	histo = ROOT.gROOT.FindObject("histo")
	histo2 = ROOT.gROOT.FindObject("histo2")
	histo.Add(histo2)
	histo1D = histo.ProjectionX()

	cut1 = 0
	n1 = (1 - frac1) * histo.Integral()
	for i in range(nBinsX):
		integral = histo1D.Integral(1,i+1)
		if (integral > n1):
			if(i == 0):
				cut1 = histo1D.GetBinCenter(i+1)
			else:
				val = (n1 - integral) / (integral - histo1D.Integral(1,i))
				cut1 = (histo1D.GetBinCenter(i+1) - histo1D.GetBinCenter(i)) * val + histo1D.GetBinCenter(i)
			break

	del histo
	del histo2
	del histo1D
	return cut1

def openPDF(outfile,canvas):
	c.Print(outfile+".pdf[")

def closePDF(outfile,canvas):
	c.Print(outfile+".pdf]")

nBins = 200

outfile = remainder[0]
outfileroot = TFile(remainder[0]+".root","RECREATE")

apfile = open(remainder[1],"r")
apfiles = []
apevents = []
masses = []

for line in (raw.strip().split() for raw in apfile):
	apfiles.append(TFile(line[0]))

for i in range(len(apfiles)):
	apevents.append(apfiles[i].Get("ntuple"))
	apevents[i].Draw("triM>>dummy({0},{1},{2})".format(1000,0,1))
	dummy = ROOT.gROOT.FindObject("dummy")
	masses.append(dummy.GetMean())
	del dummy

plot = "uncVZ"
minX = -5
maxX = -minX

#openPDF(outfile,c)

#for i in [0,1]:
#	histoMassCut1x0 = TH1F("histoMassCut1x0","histoMassCut1x0",len(masses),masses[0],masses[len(masses)-1])
#	histoMassCut1x1 = TH1F("histoMassCut1x1","histoMassCut1x1",len(masses),masses[0],masses[len(masses)-1])
#	for j in range(len(masses)):
#		mass = masses[j]
#		histoCut1 = TH1F("histoCut1","histoCut1",nZ,minVZ,maxVZ)
#		for k in range(nZ):
#			z = minVZ + (k+0.5) * (maxVZ - minVZ)/float(nZ)
#			cut1 = fitSlice(apevents[j],plot,nBins,minX,maxX,nBins,minVZ,maxVZ,outfile,c,i,z0mean,z,zBin,saveFits,frac)
#			histoCut1.SetBinContent(k+1,cut1)
#		outfileroot.cd()
#		x0Cut1, x1Cut1, _, _ = saveHisto(histoCut1,-1,5,outfile,c,"z [mm]","Fitted Cut","Fitted Cuts {0} A' mass {1:.3f} GeV Cut 1".format(plot,mass))
#		histoMassCut1x0.SetBinContent(j+1,x0Cut1)
#		histoMassCut1x1.SetBinContent(j+1,x1Cut1)
#	if(i == 0):
#		side = "Positive"
#	else:
#		side = "Negative"

#	histoMassCut1x0.GetXaxis().SetTitle("Mass (GeV)")
#	histoMassCut1x0.SetTitle("Cut 1 x0 {0}".format(side))
#	histoMassCut1x0.Fit("pol1")
#	fitx0 = histoMassCut1x0.GetFunction("pol1")
#	if(i == 0):
#		x0_cut1_pos_x0 = fitx0.GetParameter(0)
#		x1_cut1_pos_x0 = fitx0.GetParameter(1)
#	else:
#		x0_cut1_neg_x0 = fitx0.GetParameter(0)
#		x1_cut1_neg_x0 = fitx0.GetParameter(1)
#	histoMassCut1x0.Draw()
#	c.Write()
#	c.Print(outfile+".pdf")

#	histoMassCut1x1.GetXaxis().SetTitle("Mass (GeV)")
#	histoMassCut1x1.SetTitle("Cut 1 x1 {0}".format(side))
#	histoMassCut1x1.Fit("pol1")
#	fitx1 = histoMassCut1x1.GetFunction("pol1")
#	if(i == 0):
#		x0_cut1_pos_x1 = fitx1.GetParameter(0)
#		x1_cut1_pos_x1 = fitx1.GetParameter(1)
#	else:
#		x0_cut1_neg_x1 = fitx1.GetParameter(0)
#		x1_cut1_neg_x1 = fitx1.GetParameter(1)
#	histoMassCut1x1.Draw()
#	c.Write()
#	c.Print(outfile+".pdf")

#	del histoMassCut1x0
#	del histoMassCut1x1
#	del fitx0
#	del fitx1

#outfileroot.Close()
#closePDF(outfile,c)


#x0_cut1_pos = "({0}+{1}*uncM)".format(x0_cut1_pos_x0,x1_cut1_pos_x0)
#x1_cut1_pos = "({0}+{1}*uncM)".format(x0_cut1_pos_x1,x1_cut1_pos_x1)
#cut1_pos = "({0}+{1}*uncVZ)".format(x0_cut1_pos,x1_cut1_pos)

#x0_cut1_neg = "({0}+{1}*uncM)".format(x0_cut1_neg_x0,x1_cut1_neg_x0)
#x1_cut1_neg = "({0}+{1}*uncM)".format(x0_cut1_neg_x1,x1_cut1_neg_x1)
#cut1_neg = "({0}+{1}*uncVZ)".format(x0_cut1_neg,x1_cut1_neg)

#cut = "(eleTrkZ0>{0}&&-posTrkZ0>{1})||(posTrkZ0>{0}&&-eleTrkZ0>{1})".format(cut1_pos,cut1_neg)

openPDF(outfile,c)

histoMassCut1x0pos = TH1F("histoMassCut1x0pos","histoMassCut1x0pos",len(masses),masses[0],masses[len(masses)-1])
histoMassCut1x1pos = TH1F("histoMassCut1x1pos","histoMassCut1x1pos",len(masses),masses[0],masses[len(masses)-1])
histoMassCut1x0neg = TH1F("histoMassCut1x0neg","histoMassCut1x0neg",len(masses),masses[0],masses[len(masses)-1])
histoMassCut1x1neg = TH1F("histoMassCut1x1neg","histoMassCut1x1neg",len(masses),masses[0],masses[len(masses)-1])
histoslope = TH1F("histoslope","histoslope",len(masses),masses[0],masses[len(masses)-1])
histointercept = TH1F("histointercept","histointercept",len(masses),masses[0],masses[len(masses)-1])
histoxintercept = TH1F("histoxintercept","histoxintercept",len(masses),masses[0],masses[len(masses)-1])
for j in range(len(masses)):
	mass = masses[j]
	histoCut1pos = TH1F("histoCut1pos","histoCut1pos",nZ,minVZ,maxVZ)
	histoCut1neg = TH1F("histoCut1neg","histoCut1neg",nZ,minVZ,maxVZ)
	for k in range(nZ):
		z = minVZ + (k+0.5) * (maxVZ - minVZ)/float(nZ)
		cut1pos = fitSlice(apevents[j],plot,nBins,minX,maxX,nBins,minVZ,maxVZ,outfile,c,0,z,zBin,saveFits,frac,beamY)
		cut1neg = fitSlice(apevents[j],plot,nBins,minX,maxX,nBins,minVZ,maxVZ,outfile,c,1,z,zBin,saveFits,frac,beamY)
		histoCut1pos.SetBinContent(k+1,cut1pos)
		histoCut1neg.SetBinContent(k+1,cut1neg)
	outfileroot.cd()
	#x0Cut1pos, x1Cut1pos, _, _ = saveHisto(histoCut1pos,-1,1,outfile,c,"z [mm]","Fitted Cut","Fitted Cuts {0} A' mass {1:.3f} GeV Cut 1".format(plot,mass))
	#x0Cut1neg, x1Cut1neg, _, _ = saveHisto(histoCut1neg,-1,1,outfile,c,"z [mm]","Fitted Cut","Fitted Cuts {0} A' mass {1:.3f} GeV Cut 1".format(plot,mass))
	x0Cut1pos, x1Cut1pos, _, _ = saveHisto(histoCut1pos,-5,5,outfile,c,"z [mm]","Fitted Cut","Fitted Cuts {0} A' mass {1:.3f} GeV Cut 1".format(plot,mass))
	x0Cut1neg, x1Cut1neg, _, _ = saveHisto(histoCut1neg,-5,5,outfile,c,"z [mm]","Fitted Cut","Fitted Cuts {0} A' mass {1:.3f} GeV Cut 1".format(plot,mass))
	histoMassCut1x0pos.SetBinContent(j+1,x0Cut1pos)
	histoMassCut1x1pos.SetBinContent(j+1,x1Cut1pos)
	histoMassCut1x0neg.SetBinContent(j+1,x0Cut1neg)
	histoMassCut1x1neg.SetBinContent(j+1,x1Cut1neg)
	slope = (x1Cut1pos+x1Cut1neg)/2.
	intercept = (x0Cut1pos+x0Cut1neg)/(2.)
	xintercept = -(x0Cut1pos+x0Cut1neg)/(2.*slope)
	histoslope.SetBinContent(j+1,slope)
	histointercept.SetBinContent(j+1,intercept)
	histoxintercept.SetBinContent(j+1,xintercept)

histoMassCut1x0pos.GetXaxis().SetTitle("Mass (GeV)")
histoMassCut1x0pos.SetTitle("Cut 1 x0 Positive")
#histoMassCut1x0pos.GetYaxis().SetRangeUser(-0.5,0)
histoMassCut1x0pos.GetYaxis().SetRangeUser(-1.5,0)
#histoMassCut1x0pos.Fit("pol1")
histoMassCut1x0pos.Fit("pol0")
#fitx0pos = histoMassCut1x0pos.GetFunction("pol1")
fitx0pos = histoMassCut1x0pos.GetFunction("pol0")
histoMassCut1x0neg.GetXaxis().SetTitle("Mass (GeV)")
histoMassCut1x0neg.SetTitle("Cut 1 x0 Negative")
#histoMassCut1x0neg.GetYaxis().SetRangeUser(-0.5,0)
histoMassCut1x0neg.GetYaxis().SetRangeUser(-1.5,0)
#histoMassCut1x0neg.Fit("pol1")
histoMassCut1x0neg.Fit("pol0")
#fitx0neg = histoMassCut1x0neg.GetFunction("pol1")
fitx0neg = histoMassCut1x0neg.GetFunction("pol0")

x0_cut1_pos_x0 = fitx0pos.GetParameter(0)
#x1_cut1_pos_x0 = fitx0pos.GetParameter(1)
x1_cut1_pos_x0 = 0
x0_cut1_neg_x0 = fitx0neg.GetParameter(0)
#x1_cut1_neg_x0 = fitx0neg.GetParameter(1)
x1_cut1_neg_x0 = 0

histoMassCut1x0pos.Draw()
c.Write()
c.Print(outfile+".pdf")
histoMassCut1x0neg.Draw()
c.Write()
c.Print(outfile+".pdf")

histoMassCut1x1pos.GetXaxis().SetTitle("Mass (GeV)")
histoMassCut1x1pos.SetTitle("Cut 1 x1 Positive")
histoMassCut1x1pos.GetYaxis().SetRangeUser(0,0.05)
histoMassCut1x1pos.SetBinError(1,0)
histoMassCut1x1pos.SetBinError(2,0)
histoMassCut1x1pos.SetBinError(3,0)
histoMassCut1x1pos.SetBinError(4,0)
histoMassCut1x1pos.SetBinError(5,0)
histoMassCut1x1pos.SetBinError(6,0)
expfit=TF1("expfit","[0]+[1]/x^1",0.06,0.15)
expfit.SetParameters(0.035,-1)
histoMassCut1x1pos.Fit("expfit")
fitx1pos = histoMassCut1x1pos.GetFunction("expfit")
#histoMassCut1x1pos.Fit("pol1")
#fitx1pos = histoMassCut1x1pos.GetFunction("pol1")
histoMassCut1x1neg.GetXaxis().SetTitle("Mass (GeV)")
histoMassCut1x1neg.SetTitle("Cut 1 x1 Negative")
histoMassCut1x1neg.GetYaxis().SetRangeUser(0,0.05)
histoMassCut1x1neg.SetBinError(1,0)
histoMassCut1x1neg.SetBinError(2,0)
histoMassCut1x1neg.SetBinError(3,0)
histoMassCut1x1neg.SetBinError(4,0)
histoMassCut1x1neg.SetBinError(5,0)
histoMassCut1x1neg.SetBinError(6,0)
histoMassCut1x1neg.Fit("expfit")
fitx1neg = histoMassCut1x1neg.GetFunction("expfit")
#histoMassCut1x1neg.Fit("pol1")
#fitx1neg = histoMassCut1x1pos.GetFunction("pol1")

x0_cut1_pos_x1 = fitx1pos.GetParameter(0)
x1_cut1_pos_x1 = fitx1pos.GetParameter(1)
x0_cut1_neg_x1 = fitx1neg.GetParameter(0)
x1_cut1_neg_x1 = fitx1neg.GetParameter(1)

histoMassCut1x1pos.Draw()
c.Write()
c.Print(outfile+".pdf")

histoMassCut1x1neg.Draw()
c.Write()
c.Print(outfile+".pdf")
histoslope.GetXaxis().SetTitle("Mass (GeV)")
histoslope.SetTitle("Slope")
histoslope.GetYaxis().SetRangeUser(0,0.05)
#expfit=TF1("expfit","[0]+[1]/x^3",0.06,0.15)
#expfit.SetParameters(0.035,-1)
histoslope.Fit("expfit")
fitslope = histoslope.GetFunction("expfit")
histointercept.GetXaxis().SetTitle("Mass (GeV)")
histointercept.SetTitle("Y Intercept")
histointercept.GetYaxis().SetRangeUser(-0.5,0)
histointercept.SetBinError(1,0)
histointercept.SetBinError(2,0)
histointercept.SetBinError(3,0)
histointercept.SetBinError(4,0)
histointercept.Fit("pol0")
fitintercept = histointercept.GetFunction("pol0")
histoxintercept.GetXaxis().SetTitle("Mass (GeV)")
histoxintercept.SetTitle("X Intercept")
histoxintercept.GetYaxis().SetRangeUser(5,8)
#histoxintercept.Fit("pol1")
#fitxintercept = histoxintercept.GetFunction("pol1")

histoslope.Draw()
c.Write()
c.Print(outfile+".pdf")

histointercept.Draw()
c.Write()
c.Print(outfile+".pdf")

histoxintercept.Draw()
c.Write()
c.Print(outfile+".pdf")

#slope_x0 = fitslope.GetParameter(0)
#slope_x1 = fitslope.GetParameter(1)
#intercept_x0 = fitintercept.GetParameter(0)
#intercept_x1 = fitintercept.GetParameter(1)
#intercept_x1 = 0

#print("slope_x0 = {0}".format(slope_x0))
#print("slope_x1 = {0}".format(slope_x1))
#print("intercept_x0 = {0}".format(intercept_x0))
#print("intercept_x1 = {0}".format(intercept_x1))

#eleZ0_up = "(eleTrkZ0-{4}>{0}+{1}*uncM+{2}*(uncVZ)+{3}*uncM*(uncVZ))".format(intercept_x0,intercept_x1,slope_x0,slope_x1,beamY)
#posZ0_up = "(posTrkZ0-{4}>{0}+{1}*uncM+{2}*(uncVZ)+{3}*uncM*(uncVZ))".format(intercept_x0,intercept_x1,slope_x0,slope_x1,beamY)

#eleZ0_down = "(-eleTrkZ0+{4}>{0}+{1}*uncM+{2}*(uncVZ)+{3}*uncM*(uncVZ))".format(intercept_x0,intercept_x1,slope_x0,slope_x1,beamY)
#posZ0_down = "(-posTrkZ0+{4}>{0}+{1}*uncM+{2}*(uncVZ)+{3}*uncM*(uncVZ))".format(intercept_x0,intercept_x1,slope_x0,slope_x1,beamY)

#cut = "(({0}&&{1})||({2}&&{3}))".format(eleZ0_up,posZ0_down,posZ0_up,eleZ0_down)

mpos = fitx0pos.GetParameter(0)
mneg = fitx0neg.GetParameter(0)
m0 = fitintercept.GetParameter(0)
a0 = x0_cut1_pos_x1
a1 = x1_cut1_pos_x1
b0 = x0_cut1_neg_x1
b1 = x1_cut1_neg_x1

print("mpos = {0}".format(mpos))
print("mneg = {0}".format(mneg))
print("m0 = {0}".format(m0))
print("a0 = {0}".format(a0))
print("a1 = {0}".format(a1))
print("b0 = {0}".format(b0))
print("b1 = {0}".format(b1))

#fitfuncpos = TF1("fitfuncpos","{0}+({1}+{2}/[0]^1)*x".format(m0,a0,a1),6,100)
#fitfuncneg = TF1("fitfuncneg","-({0}+({1}+{2}/[0]^1)*x)".format(m0,b0,b1),6,100)

#eleZ0_up = "(eleTrkZ0>{0}+{1}*(uncVZ)+{2}*1/uncM^1*(uncVZ))".format(m0,a0,a1)
#posZ0_up = "(posTrkZ0>{0}+{1}*(uncVZ)+{2}*1/uncM^1*(uncVZ))".format(m0,a0,a1)

#eleZ0_down = "(-eleTrkZ0>{0}+{1}*(uncVZ)+{2}*1/uncM^1*(uncVZ))".format(m0,b0,b1)
#posZ0_down = "(-posTrkZ0>{0}+{1}*(uncVZ)+{2}*1/uncM^1*(uncVZ))".format(m0,b0,b1)

fitfuncpos = TF1("fitfuncpos","{0}+({1}+{2}/[0]^1)*x".format(mpos,a0,a1),6,100)
fitfuncneg = TF1("fitfuncneg","-({0}+({1}+{2}/[0]^1)*x)".format(mneg,b0,b1),6,100)

eleZ0_up = "(eleTrkZ0>{0}+{1}*(uncVZ)+{2}*1/uncM^1*(uncVZ))".format(mpos,a0,a1)
posZ0_up = "(posTrkZ0>{0}+{1}*(uncVZ)+{2}*1/uncM^1*(uncVZ))".format(mpos,a0,a1)

eleZ0_down = "(-eleTrkZ0>{0}+{1}*(uncVZ)+{2}*1/uncM^1*(uncVZ))".format(mneg,b0,b1)
posZ0_down = "(-posTrkZ0>{0}+{1}*(uncVZ)+{2}*1/uncM^1*(uncVZ))".format(mneg,b0,b1)

cut = "(({0}&&{1})||({2}&&{3}))".format(eleZ0_up,posZ0_down,posZ0_up,eleZ0_down)

outfileroot.Close()
closePDF(outfile,c)

#a0 = x0_cut1_pos_x0
#a1 = x1_cut1_pos_x0
#a2 = x0_cut1_pos_x1
#a3 = x1_cut1_pos_x1
#b0 = x0_cut1_neg_x0
#b1 = x1_cut1_neg_x0
#b2 = x0_cut1_neg_x1
#b3 = x1_cut1_neg_x1

#print("a0 = {0}".format(a0))
#print("a1 = {0}".format(a1))
#print("a2 = {0}".format(a2))
#print("a3 = {0}".format(a3))
#print("b0 = {0}".format(b0))
#print("b1 = {0}".format(b1))
#print("b2 = {0}".format(b2))
#print("b3 = {0}".format(b3))

#eleZ0_up = "(eleTrkZ0>{0}+{1}*uncM+{2}*(uncVZ)+{3}*uncM*(uncVZ))".format(a0,a1,a2,a3)
#posZ0_up = "(posTrkZ0>{0}+{1}*uncM+{2}*(uncVZ)+{3}*uncM*(uncVZ))".format(a0,a1,a2,a3)

#eleZ0_down = "(-eleTrkZ0>{0}+{1}*uncM+{2}*(uncVZ)+{3}*uncM*(uncVZ))".format(b0,b1,b2,b3)
#posZ0_down = "(-posTrkZ0>{0}+{1}*uncM+{2}*(uncVZ)+{3}*uncM*(uncVZ))".format(b0,b1,b2,b3)

#cut = "(({0}&&{1})||({2}&&{3}))".format(eleZ0_up,posZ0_down,posZ0_up,eleZ0_down)

openPDF(outfile+"_2D",c)

for i in range(len(masses)):
	mass = masses[i]
	#draw2DHisto(apevents[i],nBins,0,60,minX,maxX,outfile+"_2D",c,fitfuncpos,fitfuncneg,cut,plotTitle="Z0 vs VZ {0:0.0f} MeV A' ".format(mass*1000))
	draw2DHisto(apevents[i],nBins,30,120,minX,maxX,outfile+"_2D",c,fitfuncpos,fitfuncneg,cut,plotTitle="Z0 vs VZ {0:0.0f} MeV A' ".format(mass*1000))

closePDF(outfile+"_2D",c)
print(cut)