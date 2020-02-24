import sys
tmpargv = sys.argv
sys.argv = []
import getopt
import array
import ROOT
from ROOT import gROOT, TFile, TTree, TChain, gDirectory, TLine, gStyle, TCanvas, TLegend, TH1F, TF1, TGraphErrors, TMultiGraph
sys.argv = tmpargv

#List arguments
def print_usage():
    print "\nUsage: {0} <output file base name> <input A' text file>".format(sys.argv[0])
    print "Arguments: "
    print '\t-h: this help message'
    print

zbin = 5.
zTarg = -4.3
maxZ = 80
options, remainder = getopt.gnu_getopt(sys.argv[1:], 'h')

# Parse the command line arguments
for opt, arg in options:
		if opt=='-h':
			print_usage()
			sys.exit(0)

gStyle.SetOptStat(0)
gStyle.SetOptFit(1011)
c = TCanvas("c","c",800,600)

def saveTupleFitPlot(events,inHisto,nBins,mass,minX,maxX,outfile,canvas):
	events.Draw("{0}>>histo({1},{2},{3})".format(inHisto,nBins,minX,maxX))
	histo = ROOT.gROOT.FindObject("histo")
	histo.SetTitle("{0} {1:.0f} A' mass".format(inHisto,mass))
	histo.GetXaxis().SetTitle("{0} (mm)".format(inHisto))
	f1 = TF1("f1","gaus",histo.GetMean()-1*histo.GetRMS(),histo.GetMean()+1*histo.GetRMS())
	histo.Fit("f1","R")
	histo.Draw("PE")
	canvas.Print(outfile+".pdf")
	mean = f1.GetParameter(1)
	sigma = f1.GetParameter(2)
	meanerror = f1.GetParError(1)
	sigmaerror = f1.GetParError(2)
	del f1
	del histo
	return mean, sigma, meanerror, sigmaerror

def saveTupleFitPlotsZ(events,inHisto,nBins,mass,minX,maxX,zbin,zTarg,maxZ,outfile,canvas):
	events.Draw("{0}:triEndZ>>histo({1},{2},{3},{1},{4},{5})".format(inHisto,nBins,zTarg,maxZ,minX,maxX))
	histo = ROOT.gROOT.FindObject("histo")
	histo.SetTitle("{0} vs Truth Z".format(inHisto))
	histo.GetXaxis().SetTitle("Truth Z (mm)")
	histo.GetYaxis().SetTitle("{0} (mm)".format(inHisto))
	histo.Draw("COLZ")
	canvas.Print(outfile+".pdf")
	z = array.array('d')
	fittedmean = array.array('d')
	fittedsigma = array.array('d')
	fittedmeanerror = array.array('d')
	fittedsigmaerror = array.array('d')
	zErr = array.array('d')
	nbins = int((maxZ-zTarg)/zbin)
	for i in range(nbins):
		zmin = zTarg + i * zbin
		zmax = zmin + zbin
		zErr.append(0.0)
		z.append(zmin + zbin/2.)
		events.Draw("{0}>>histo2({1},{2},{3})".format(inHisto,nBins,minX,maxX),"triEndZ>{0}&&triEndZ<{1}".format(zmin,zmax))
		histo2 = ROOT.gROOT.FindObject("histo2")
		mean, sigma, meanerror, sigmaerror = getFitZ(histo2)
		fittedmean.append(mean)
		fittedsigma.append(sigma)
		fittedmeanerror.append(meanerror)
		fittedsigmaerror.append(sigmaerror)
		del histo2

	gr_mean = TGraphErrors(len(z),z,fittedmean,zErr,fittedmeanerror)
	gr_sigma = TGraphErrors(len(z),z,fittedsigma,zErr,fittedsigmaerror)

	gr_mean.Draw("AP")
	gr_mean.SetTitle("{0} Fitted Mean {1:.0f} MeV A'".format(plot,mass))
	gr_mean.GetXaxis().SetTitle("Truth Z (mm)")
	gr_mean.GetYaxis().SetTitle("Mean (mm)")
	gr_mean.GetYaxis().SetRangeUser(-0.4,0)
	canvas.Print(outfile+".pdf")
	canvas.Write()
	gr_sigma.Draw("AP")
	gr_sigma.SetTitle("{0} Fitted Sigma {1:.0f} MeV A'".format(plot,mass))
	gr_sigma.GetXaxis().SetTitle("Truth Z (mm)")
	gr_sigma.GetYaxis().SetTitle("Sigma (mm)")
	gr_sigma.GetYaxis().SetRangeUser(0,0.4)
	canvas.Print(outfile+".pdf")
	canvas.Write()
	del histo
	del gr_mean
	del gr_sigma

def getFitZ(histo):
	f1 = TF1("f1","gaus",histo.GetMean()-1*histo.GetRMS(),histo.GetMean()+1*histo.GetRMS())
	histo.Fit(f1,"R")
	if(f1 != None):
		mean = f1.GetParameter(1)
		sigma = f1.GetParameter(2)
		meanerror = f1.GetParError(1)
		sigmaerror = f1.GetParError(2)
		del f1
		del histo
		return mean, sigma, meanerror, sigmaerror
	else:
		del f1
		del histo
		return 0, 0, 0, 0
	
def openPDF(outfile,canvas):
	c.Print(outfile+".pdf[")

def closePDF(outfile,canvas):
	c.Print(outfile+".pdf]")

def getPlot(string):
	arr = string.split(" ")
	return arr[0]

def getMin(string):
	arr = string.split(" ")
	if(len(arr) < 2): return ""
	else: return float(arr[1])

def getMax(string):
	arr = string.split(" ")
	if(len(arr) < 3): return ""
	else: return float(arr[2])


nBins = 50

outfile = remainder[0]
outfileroot = TFile(remainder[0]+".root","RECREATE")

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

plots = []
plots.append("uncVX -1 1")
plots.append("uncVY -0.5 0.5")
plots.append("uncVX-(uncVZ-{0})*uncPX/uncPZ -1 1".format(zTarg))
plots.append("uncVY-(uncVZ-{0})*uncPY/uncPZ -0.5 0.5".format(zTarg))

openPDF(outfile,c)
outfileroot.cd()
for i in range(len(plots)):
	fittedmean = array.array('d')
	fittedsigma = array.array('d')
	fittedmeanerror = array.array('d')
	fittedsigmaerror = array.array('d')
	for j in range(len(mass)):
		plot = getPlot(plots[i])
		minX = getMin(plots[i])
		maxX = getMax(plots[i])
		mean, sigma, meanerror, sigmaerror = saveTupleFitPlot(events[j],plot,nBins,mass[j],minX,maxX,outfile,c)
		saveTupleFitPlotsZ(events[j],plot,nBins,mass[j],minX,maxX,zbin,zTarg,maxZ,outfile,c)
		fittedmean.append(mean)
		fittedsigma.append(sigma)
		fittedmeanerror.append(meanerror)
		fittedsigmaerror.append(sigmaerror)

	gr_mean = TGraphErrors(len(mass),mass,fittedmean,masserror,fittedmeanerror)
	gr_sigma = TGraphErrors(len(mass),mass,fittedsigma,masserror,fittedsigmaerror)

	gr_mean.SetTitle("{0} Mean ".format(plot))
	gr_mean.GetXaxis().SetTitle("Truth Mass (MeV)")
	gr_mean.GetYaxis().SetTitle("Mean (mm)")
	gr_mean.GetYaxis().SetRangeUser(-0.4,0)
	gr_mean.Draw("AP")
	c.Print(outfile+".pdf")
	c.Write()

	gr_sigma.SetTitle("{0} Sigma ".format(plot))
	gr_sigma.GetXaxis().SetTitle("Truth Mass (MeV)")
	gr_sigma.GetYaxis().SetTitle("Sigma (mm)")
	gr_sigma.GetYaxis().SetRangeUser(0,0.4)
	gr_sigma.Draw("AP")

	c.Print(outfile+".pdf")
	c.Write()

	del fittedmean
	del fittedsigma
	del fittedmeanerror
	del fittedsigmaerror

closePDF(outfile,c)
outfileroot.Close()