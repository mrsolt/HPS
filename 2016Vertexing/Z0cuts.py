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
    print '\t-h: this help message'
    print

minVZ = 5
maxVZ = 60
nZ = 20
zBin = 5
saveFits = False

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'c:d:sm:n:h')

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
		if opt=='-h':
			print_usage()
			sys.exit(0)

gStyle.SetOptStat(0)
gStyle.SetOptFit(1011)
c = TCanvas("c","c",800,600)

def draw2DHisto(events,nBins,minX,maxX,minY,maxY,outfile,canvas,cut="",XaxisTitle="Reconstructed z (mm)",YaxisTitle="Z0 (mm)",plotTitle="",stats=0):
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
	canvas.SetLogz()
	histo.Draw("COLZ")
	histo.SetTitle(plotTitle+" No IP Cut")
	histo.GetXaxis().SetTitle(XaxisTitle)
	histo.GetYaxis().SetTitle(YaxisTitle)
	histo.SetStats(stats)
	#canvas.Write()
	canvas.Print(outfile+".pdf")
	histocut.Draw("COLZ")
	histocut.SetTitle(plotTitle+" With IP Cut")
	histocut.GetXaxis().SetTitle(XaxisTitle)
	histocut.GetYaxis().SetTitle(YaxisTitle)
	histocut.SetStats(stats)
	#canvas.Write()
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

def fitSlice(events,inHisto2,nBinsX,minX,maxX,nBinsY,minY,maxY,outfile,canvas,index=0,z0mean=-0.1,z=0,zRange=9999,saveFits=False):
	ex = "Null Fit"
	if(index == 0):
		bound = ">"
		events.Draw("{0}:{1}>>histo({2},{3},{4},{5},{6},{7})".format(inHisto2,"eleTrkZ0",nBinsX,minX,maxX,nBinsY,minY,maxY),"uncVZ>{0}-{1}&&uncVZ<{0}+{1}&&{2}{3}{4}".format(z,zRange,"eleTrkZ0",bound,z0mean))
		events.Draw("{0}:{1}>>histo2({2},{3},{4},{5},{6},{7})".format(inHisto2,"posTrkZ0",nBinsX,minX,maxX,nBinsY,minY,maxY),"uncVZ>{0}-{1}&&uncVZ<{0}+{1}&&{2}{3}{4}".format(z,zRange,"posTrkZ0",bound,z0mean))
	elif(index == 1):
		bound = "<"
		events.Draw("{0}:{1}>>histo({2},{3},{4},{5},{6},{7})".format(inHisto2,"-eleTrkZ0",nBinsX,minX,maxX,nBinsY,minY,maxY),"uncVZ>{0}-{1}&&uncVZ<{0}+{1}&&{2}{3}{4}".format(z,zRange,"eleTrkZ0",bound,z0mean))
		events.Draw("{0}:{1}>>histo2({2},{3},{4},{5},{6},{7})".format(inHisto2,"-posTrkZ0",nBinsX,minX,maxX,nBinsY,minY,maxY),"uncVZ>{0}-{1}&&uncVZ<{0}+{1}&&{2}{3}{4}".format(z,zRange,"posTrkZ0",bound,z0mean))
	histo = ROOT.gROOT.FindObject("histo")
	histo2 = ROOT.gROOT.FindObject("histo2")
	histo.Add(histo2)
	histo1D = histo.ProjectionX()

	#histo1D.Fit("gaus","gaus","",histo1D.GetMean()-1.5*histo1D.GetRMS(),histo1D.GetMean()+1.5*histo1D.GetRMS())
	#fit = histo1D.GetFunction("gaus")
	
	#histo1D.Fit("landau")
	#fit = histo1D.GetFunction("landau")
	#if saveFits:
	#	canvas.Print(outfile+".pdf")

	fitpar = []
	mean = 0
	meanErr = 0
	sigma = 0
	sigmaErr = 0

	cut1 = 0
	frac1 = 0.9
	n1 = (1 - frac1) * histo.Integral()
	for i in range(nBinsX):
		integral = histo1D.Integral(1,i+1)
		if (integral > n1):
			if(i == 0):
				cut1 = histo1D.GetBinCenter(i+1)
			else:
				#val = (n1*frac1 - integral) / (integral - histo1D.Integral(1,i))
				val = (n1 - integral) / (integral - histo1D.Integral(1,i))
				cut1 = (histo1D.GetBinCenter(i+1) - histo1D.GetBinCenter(i)) * val + histo1D.GetBinCenter(i)
			break

	#cut2 = 9999
	#frac2 = 0.95
	#n2 = frac2 * histo.Integral()
	#for i in range(nBinsX):
	#	integral = histo1D.Integral(1,i+1)
	#	if (integral > n2):
	#		if(i == 0):
	#			cut2 = histo1D.GetBinCenter(i+1)
	#		else:
	#			val = (n2 - integral) / (integral - histo1D.Integral(1,i))
	#			cut2 = (histo1D.GetBinCenter(i+1) - histo1D.GetBinCenter(i)) * val + histo1D.GetBinCenter(i)
	#		break

	#try:
	#	mean = fit.GetParameter(1)
	#	meanErr = fit.GetParError(1)
	#	sigma = fit.GetParameter(2)
	#	sigmaErr = fit.GetParError(2)
	#except Exception as ex:

	#	print(ex)
	fitpar.append(mean)
	fitpar.append(meanErr)
	fitpar.append(sigma)
	fitpar.append(sigmaErr)
	fitpar.append(cut1)
	#fitpar.append(cut2)
	del histo
	del histo2
	del histo1D
	#del fit
	return fitpar

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
z0mean = -0.1
side = ""

openPDF(outfile,c)

for i in [0,1]:
	histoMassMeanx0 = TH1F("histoMassMeanx0","histoMassMeanx0",len(masses),masses[0],masses[len(masses)-1])
	histoMassSigmax0 = TH1F("histoMassSigmax0","histoMassSigmax0",len(masses),masses[0],masses[len(masses)-1])
	histoMassMeanx1 = TH1F("histoMassMeanx1","histoMassMeanx1",len(masses),masses[0],masses[len(masses)-1])
	histoMassSigmax1 = TH1F("histoMassSigmax1","histoMassSigmax1",len(masses),masses[0],masses[len(masses)-1])
	histoMassCut1x0 = TH1F("histoMassCut1x0","histoMassCut1x0",len(masses),masses[0],masses[len(masses)-1])
	histoMassCut1x1 = TH1F("histoMassCut1x1","histoMassCut1x1",len(masses),masses[0],masses[len(masses)-1])
	#histoMassCut2x0 = TH1F("histoMassCut2x0","histoMassCut2x0",len(masses),masses[0],masses[len(masses)-1])
	#histoMassCut2x1 = TH1F("histoMassCut2x1","histoMassCut2x1",len(masses),masses[0],masses[len(masses)-1])
	for j in range(len(masses)):
		mass = masses[j]
		histoMean = TH1F("histoMean","histoMean",nZ,minVZ,maxVZ)
		histoSigma = TH1F("histoSigma","histoSigma",nZ,minVZ,maxVZ)
		histoCut1 = TH1F("histoCut1","histoCut1",nZ,minVZ,maxVZ)
		#histoCut2 = TH1F("histoCut2","histoCut2",nZ,minVZ,maxVZ)
		for k in range(nZ):
			z = minVZ + (k+0.5) * (maxVZ - minVZ)/float(nZ)
			params = fitSlice(apevents[j],plot,nBins,minX,maxX,nBins,minVZ,maxVZ,outfile,c,i,z0mean,z,zBin,saveFits)
			histoMean.SetBinContent(k+1,params[0])
			histoMean.SetBinError(k+1,params[1])
			histoSigma.SetBinContent(k+1,params[2])
			histoSigma.SetBinError(k+1,params[3])
			#histoCut.SetBinContent(k+1,params[0]-3*params[2])
			histoCut1.SetBinContent(k+1,params[4])
			#histoCut2.SetBinContent(k+1,params[5])
		outfileroot.cd()
		#x0Mean, x1Mean, x0MeanErr, x1MeanErr = saveHisto(histoMean,0,3,outfile,c,"z [mm]","Fitted Mean","Fitted Means {0} A' mass {1:.2f} GeV".format(plot,mass))
		#x0Sigma, x1Sigma, x0SigmaErr, x1SigmaErr = saveHisto(histoSigma,0,1,outfile,c,"z [mm]","Fitted Sigma","Fitted Sigmas {0} A' mass {1:.2f} GeV".format(plot,mass))
		x0Cut1, x1Cut1, _, _ = saveHisto(histoCut1,-1,5,outfile,c,"z [mm]","Fitted Cut","Fitted Cuts {0} A' mass {1:.3f} GeV Cut 1".format(plot,mass))
		#x0Cut2, x1Cut2, _, _ = saveHisto(histoCut2,-1,5,outfile,c,"z [mm]","Fitted Cut","Fitted Cuts {0} A' mass {1:.3f} GeV Cut 2".format(plot,mass))
		#histoMassMeanx0.SetBinContent(j+1,x0Mean)
		#histoMassMeanx0.SetBinError(j+1,x0MeanErr)
		#histoMassMeanx1.SetBinContent(j+1,x1Mean)
		#histoMassMeanx1.SetBinError(j+1,x1MeanErr)
		#histoMassSigmax0.SetBinContent(j+1,x0Sigma)
		#histoMassSigmax0.SetBinError(j+1,x0SigmaErr)
		#histoMassSigmax1.SetBinContent(j+1,x1Sigma)
		#histoMassSigmax1.SetBinError(j+1,x1SigmaErr)
		histoMassCut1x0.SetBinContent(j+1,x0Cut1)
		histoMassCut1x1.SetBinContent(j+1,x1Cut1)
		#histoMassCut2x0.SetBinContent(j+1,x0Cut2)
		#histoMassCut2x1.SetBinContent(j+1,x1Cut2)
		del histoMean
		del histoSigma
		#del histoCut1
		#del histoCut2
	if(i == 0):
		side = "Positive"
	else:
		side = "Negative"
	#histoMassMeanx0.Fit("pol1")
	#histoMassMeanx0.GetXaxis().SetTitle("Mass (GeV)")
	#histoMassMeanx0.SetTitle("Mean x0 {0}".format(side))
	#histoMassMeanx0.Draw()
	#c.Write()
	#c.Print(outfile+".pdf")
	#histoMassMeanx1.GetXaxis().SetTitle("Mass (GeV)")
	#histoMassMeanx1.SetTitle("Mean x1 {0}".format(side))
	#histoMassMeanx1.Fit("pol1")
	#histoMassMeanx1.Draw()
	#c.Write()
	#c.Print(outfile+".pdf")
	#histoMassSigmax0.GetXaxis().SetTitle("Mass (GeV)")
	#histoMassSigmax0.SetTitle("Sigma x0 {0}".format(side))
	#histoMassSigmax0.Fit("pol1")
	#histoMassSigmax0.Draw()
	#c.Write()
	#c.Print(outfile+".pdf")
	#histoMassSigmax1.GetXaxis().SetTitle("Mass (GeV)")
	#histoMassSigmax1.SetTitle("Sigma x1 {0}".format(side))
	#histoMassSigmax1.Fit("pol1")
	#histoMassSigmax1.Draw()
	#c.Write()
	#c.Print(outfile+".pdf")
	histoMassCut1x0.GetXaxis().SetTitle("Mass (GeV)")
	histoMassCut1x0.SetTitle("Cut 1 x0 {0}".format(side))
	histoMassCut1x0.Fit("pol1")
	fitx0 = histoMassCut1x0.GetFunction("pol1")
	if(i == 0):
		x0_cut1_pos_x0 = fitx0.GetParameter(0)
		x1_cut1_pos_x0 = fitx0.GetParameter(1)
	else:
		x0_cut1_neg_x0 = fitx0.GetParameter(0)
		x1_cut1_neg_x0 = fitx0.GetParameter(1)
	histoMassCut1x0.Draw()
	c.Write()
	c.Print(outfile+".pdf")
	#histoMassCut2x0.GetXaxis().SetTitle("Mass (GeV)")
	#histoMassCut2x0.SetTitle("Cut 2 x0 {0}".format(side))
	#histoMassCut2x0.Fit("pol1")
	#histoMassCut2x0.Draw()
	#c.Write()
	#c.Print(outfile+".pdf")
	histoMassCut1x1.GetXaxis().SetTitle("Mass (GeV)")
	histoMassCut1x1.SetTitle("Cut 1 x1 {0}".format(side))
	histoMassCut1x1.Fit("pol1")
	fitx1 = histoMassCut1x1.GetFunction("pol1")
	if(i == 0):
		x0_cut1_pos_x1 = fitx1.GetParameter(0)
		x1_cut1_pos_x1 = fitx1.GetParameter(1)
	else:
		x0_cut1_neg_x1 = fitx1.GetParameter(0)
		x1_cut1_neg_x1 = fitx1.GetParameter(1)
	histoMassCut1x1.Draw()
	c.Write()
	c.Print(outfile+".pdf")
	#histoMassCut2x1.GetXaxis().SetTitle("Mass (GeV)")
	#histoMassCut2x1.SetTitle("Cut 2 x1 {0}".format(side))
	#histoMassCut2x1.Fit("pol1")
	#histoMassCut2x1.Draw()
	#c.Write()
	#c.Print(outfile+".pdf")
	#del histoMassMeanx0
	#del histoMassMeanx1
	#del histoMassSigmax0
	#del histoMassSigmax1
	del histoMassCut1x0
	del histoMassCut1x1
	#del histoMassCut2x0
	#del histoMassCut2x1
	del fitx0
	del fitx1

outfileroot.Close()
closePDF(outfile,c)

x0_cut1_pos = "({0}+{1}*uncM)".format(x0_cut1_pos_x0,x1_cut1_pos_x0)
x1_cut1_pos = "({0}+{1}*uncM)".format(x0_cut1_pos_x1,x1_cut1_pos_x1)
cut1_pos = "({0}+{1}*uncVZ)".format(x0_cut1_pos,x1_cut1_pos)

x0_cut1_neg = "({0}+{1}*uncM)".format(x0_cut1_neg_x0,x1_cut1_neg_x0)
x1_cut1_neg = "({0}+{1}*uncM)".format(x0_cut1_neg_x1,x1_cut1_neg_x1)
cut1_neg = "({0}+{1}*uncVZ)".format(x0_cut1_neg,x1_cut1_neg)

cut = "(eleTrkZ0>{0}&&-posTrkZ0>{1})||(posTrkZ0>{0}&&-eleTrkZ0>{1})".format(cut1_pos,cut1_neg)

openPDF(outfile+"_2D",c)

for i in range(len(masses)):
	mass = masses[i]
	draw2DHisto(apevents[i],nBins,minVZ,maxVZ,minX,maxX,outfile+"_2D",c,cut,plotTitle="VZ vs Z0 {0:.3f} GeV A' ".format(mass))

closePDF(outfile+"_2D",c)