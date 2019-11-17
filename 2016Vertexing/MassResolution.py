import sys
tmpargv = sys.argv
sys.argv = []
import getopt
import array
import ROOT
from ROOT import gROOT, TFile, TTree, TChain, gDirectory, TLine, gStyle, TCanvas, TLegend, TH1F, TF1, TGraphErrors
sys.argv = tmpargv

#List arguments
def print_usage():
    print "\nUsage: {0} <output file base name> <input A' text file>".format(sys.argv[0])
    print "Arguments: "
    print '\t-h: this help message'
    print

zbin = 5.
zTarg =-4.3
maxZ = 100
options, remainder = getopt.gnu_getopt(sys.argv[1:], 'h')

# Parse the command line arguments
for opt, arg in options:
		if opt=='-h':
			print_usage()
			sys.exit(0)

gStyle.SetOptStat(0)
c = TCanvas("c","c",800,600)

def saveTupleFitPlot(events,inHisto,mass,nBins,minX,maxX,outfile,canvas):
	events.Draw("{0}>>histo({1},{2},{3})".format(inHisto,nBins,minX,maxX))
	histo = ROOT.gROOT.FindObject("histo")
	histo.SetTitle("Reconstructed Mass {0} MeV A'".format(mass))
	histo.GetXaxis().SetTitle("Reconstructed Mass (MeV)")
	f1 = TF1("f1","gaus")
	histo.Fit("f1")
	histo.Draw()
	canvas.Print(outfile+".pdf")
	del histo
	return f1.GetParameter(1), f1.GetParameter(2), f1.GetParError(1), f1.GetParError(2)

def saveTupleFitPlotsZ(events,inHisto,mass,nBins,minX,maxX,zbin,zTarg,maxZ,outfile,canvas):
	events.Draw("{0}:triEndZ>>histo({1},{2},{3},{1},{4},{5})".format(inHisto,nBins,zTarg,maxZ,minX,maxX))
	histo = ROOT.gROOT.FindObject("histo")
	histo.SetTitle("Reconstructed Mass {0} MeV A' vs Truth Z".format(mass))
	histo.GetXaxis().SetTitle("Truth Z (mm)")
	histo.GetYaxis().SetTitle("Reconstructed Mass (MeV)")
	histo.Draw("COLZ")
	canvas.Print(outfile+".pdf")
	z = array.array('d')
	fittedmean = array.array('d')
	fittedsigma = array.array('d')
	fittedmeanerror = array.array('d')
	fittedsigmaerror = array.array('d')
	nbins = int((maxZ-zTarg)/zbin)
	for i in range(nbins):
		zmin = zTarg + i * zbin
		zmax = zmin + zbin
		print zmin
		print zmax
		z.append(zmin + zbin/2.)
		events.Draw("{0}>>histo2({1},{2},{3}),triEndZ>{4}&&triEndZ<{5}".format(inHisto,nBins,minX,maxX,zmin,zmax))
		histo2 = ROOT.gROOT.FindObject("histo2")
		print histo2
		mean, sigma, meanerror, sigmaerror = getFitZ(histo2)
		fittedmean.append(mean)
		fittedsigma.append(sigma)
		fittedmeanerror.append(meanerror)
		fittedsigmaerror.append(sigmaerror)
		del histo2

	gr_mean = TGraphErrors(len(z),z,fittedmean,masserror,fittedmeanerror)
	gr_sigma = TGraphErrors(len(z),z,fittedsigma,masserror,fittedsigmaerror)

	gr_mean.Draw("ALP")
	gr_mean.SetTitle("Fitted Mass - Truth Mass Mean {0} MeV A'".format(mass))
	gr_mean.GetXaxis().SetTitle("Truth Z (mm)")
	gr_mean.GetYaxis().SetTitle("Mean (MeV)")
	canvas.Print(outfile+".pdf")
	gr_sigma.Draw("ALP")
	gr_sigma.SetTitle("Fitted Mass Resolution {0} MeV A'".format(mass))
	gr_sigma.GetXaxis().SetTitle("Truth Z (mm)")
	gr_sigma.GetYaxis().SetTitle("Sigma (MeV)")
	canvas.Print(outfile+".pdf")
	del histo
	del gr_mean
	del gr_sigma

def getFitZ(histo):
	f1 = TF1("f1","gaus")
	histo.Fit("f1")
	print f1
	if(f1 != None):
		return f1.GetParameter(1), f1.GetParameter(2), f1.GetParError(1), f1.GetParError(2)
	else:
		return 0, 0, 0, 0
	
def openPDF(outfile,canvas):
	c.Print(outfile+".pdf[")

def closePDF(outfile,canvas):
	c.Print(outfile+".pdf]")


nBins = 50
maxX = 15.
minX = -maxX

outfile = remainder[0]

apfile = open(remainder[1],"r")
apfiles = []
events = []
mass = array.array('d')

for line in (raw.strip().split() for raw in apfile):
	apfiles.append(TFile(line[0]))

masserror = array.array('d')
for i in range(len(apfiles)):
	events.append(apfiles[i].Get("ntuple"))
	events[i].Draw("triM>>dummy({0},{1},{2})".format(1000,0,1))
	dummy = ROOT.gROOT.FindObject("dummy")
	mass.append(dummy.GetMean()*1000)
	masserror.append(0.0)
	del dummy


fittedmean = array.array('d')
fittedsigma = array.array('d')
fittedmeanerror = array.array('d')
fittedsigmaerror = array.array('d')

openPDF(outfile,c)
for i in range(len(mass)):
	mean, sigma, meanerror, sigmaerror = saveTupleFitPlot(events[i],"(uncM*1000-{0})".format(mass[i]),mass[i],nBins,minX,maxX,outfile,c)
	saveTupleFitPlotsZ(events[i],"(uncM*1000-{0})".format(mass[i]),mass[i],nBins,minX,maxX,zbin,zTarg,maxZ,outfile,c)
	fittedmean.append(mean)
	fittedsigma.append(sigma)
	fittedmeanerror.append(meanerror)
	fittedsigmaerror.append(sigmaerror)

gr_mean = TGraphErrors(len(mass),mass,fittedmean,masserror,fittedmeanerror)
gr_sigma = TGraphErrors(len(mass),mass,fittedsigma,masserror,fittedsigmaerror)

gr_mean.Draw("AP")
gr_mean.SetTitle("Fitted Mass - Truth Mass Mean")
gr_mean.GetXaxis().SetTitle("Truth Mass (MeV)")
gr_mean.GetYaxis().SetTitle("Mean (MeV)")
c.Print(outfile+".pdf")
gr_sigma.Draw("AP")
gr_sigma.SetTitle("Fitted Mass Resolution")
gr_sigma.GetXaxis().SetTitle("Truth Mass (MeV)")
gr_sigma.GetYaxis().SetTitle("Sigma (MeV)")
c.Print(outfile+".pdf")

closePDF(outfile,c)