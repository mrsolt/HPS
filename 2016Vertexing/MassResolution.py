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
zTarg =-4.3
maxZ = 100
options, remainder = getopt.gnu_getopt(sys.argv[1:], 'h')

# Parse the command line arguments
for opt, arg in options:
		if opt=='-h':
			print_usage()
			sys.exit(0)

gStyle.SetOptStat(0)
gStyle.SetOptFit(1011)
c = TCanvas("c","c",800,600)

def saveTupleFitPlot(events,inHisto,mass,nBins,minX,maxX,outfile,canvas):
	events.Draw("{0}>>histo({1},{2},{3})".format(inHisto,nBins,minX,maxX))
	histo = ROOT.gROOT.FindObject("histo")
	histo.SetTitle("Reconstructed Mass {0:.0f} MeV A'".format(mass))
	histo.GetXaxis().SetTitle("Reconstructed Mass (MeV)")
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

def saveTupleFitPlotsZ(events,inHisto,mass,nBins,minX,maxX,zbin,zTarg,maxZ,outfile,canvas):
	events.Draw("{0}:triEndZ>>histo({1},{2},{3},{1},{4},{5})".format(inHisto,nBins,zTarg,maxZ,minX,maxX))
	histo = ROOT.gROOT.FindObject("histo")
	histo.SetTitle("Reconstructed Mass {0:.0f} MeV A' vs Truth Z".format(mass))
	histo.GetXaxis().SetTitle("Truth Z (mm)")
	histo.GetYaxis().SetTitle("Reconstructed Mass (MeV)")
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
		zErr.append(zbin)
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
	gr_mean.SetTitle("Fitted Mass - Truth Mass Mean {0:.0f} MeV A'".format(mass))
	gr_mean.GetXaxis().SetTitle("Truth Z (mm)")
	gr_mean.GetYaxis().SetTitle("Mean (MeV)")
	gr_mean.GetYaxis().SetRangeUser(-5,5)
	canvas.Print(outfile+".pdf")
	gr_sigma.Draw("AP")
	gr_sigma.SetTitle("Fitted Mass Resolution {0:.0f} MeV A'".format(mass))
	gr_sigma.GetXaxis().SetTitle("Truth Z (mm)")
	gr_sigma.GetYaxis().SetTitle("Sigma (MeV)")
	gr_sigma.GetYaxis().SetRangeUser(0,8)
	canvas.Print(outfile+".pdf")
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

moller_mass_data = 0.04887*1000
moller_mass_res_data = 0.002704*1000
moller_mass_mc = 0.04846*1000
moller_mass_res_mc = 0.001807*1000

ratio = moller_mass_res_data / moller_mass_res_mc

moller_mass_data_err = 0.00001*1000
moller_mass_res_data_err = 0.000007*1000
moller_mass_mc_err = 0.001*1000
moller_mass_res_mc_err = 0.000003*1000

moller_mass_data_arr = array.array('d')
moller_mass_res_data_arr = array.array('d')
moller_mass_mc_arr = array.array('d')
moller_mass_res_mc_arr = array.array('d')

moller_mass_data_err_arr = array.array('d')
moller_mass_res_data_err_arr = array.array('d')
moller_mass_mc_err_arr = array.array('d')
moller_mass_res_mc_err_arr = array.array('d')

moller_mass_data_arr.append(moller_mass_data)
moller_mass_res_data_arr.append(moller_mass_res_data)
moller_mass_mc_arr.append(moller_mass_mc)
moller_mass_res_mc_arr.append(moller_mass_res_mc)

moller_mass_data_err_arr.append(moller_mass_data_err)
moller_mass_res_data_err_arr.append(moller_mass_res_data_err)
moller_mass_mc_err_arr.append(moller_mass_mc_err)
moller_mass_res_mc_err_arr.append(moller_mass_res_mc_err)

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
fittedsigmascaled = array.array('d')
fittedmeanerror = array.array('d')
fittedsigmaerror = array.array('d')
fittedsigmascalederror = array.array('d')

openPDF(outfile,c)
for i in range(len(mass)):
	mean, sigma, meanerror, sigmaerror = saveTupleFitPlot(events[i],"(uncM*1000-{0:.0f})".format(mass[i]),mass[i],nBins,minX,maxX,outfile,c)
	saveTupleFitPlotsZ(events[i],"(uncM*1000-{0:.0f})".format(mass[i]),mass[i],nBins,minX,maxX,zbin,zTarg,maxZ,outfile,c)
	fittedmean.append(mean)
	fittedsigma.append(sigma)
	fittedsigmascaled.append(sigma*ratio)
	fittedmeanerror.append(meanerror)
	fittedsigmaerror.append(sigmaerror)
	fittedsigmascalederror.append(sigmaerror*ratio)

gr_mean = TGraphErrors(len(mass),mass,fittedmean,masserror,fittedmeanerror)
gr_sigma = TGraphErrors(len(mass),mass,fittedsigma,masserror,fittedsigmaerror)
gr_sigma_scaled = TGraphErrors(len(mass),mass,fittedsigmascaled,masserror,fittedsigmascalederror)
gr_moller_data = TGraphErrors(1,moller_mass_data_arr,moller_mass_res_data_arr,moller_mass_data_err_arr,moller_mass_res_data_err_arr)
gr_moller_mc = TGraphErrors(1,moller_mass_mc_arr,moller_mass_res_mc_arr,moller_mass_mc_err_arr,moller_mass_res_mc_err_arr)

gr_mean.Draw("AP")
gr_mean.SetTitle("Fitted Mass - Truth Mass Mean")
gr_mean.GetXaxis().SetTitle("Truth Mass (MeV)")
gr_mean.GetYaxis().SetTitle("Mean (MeV)")
c.Print(outfile+".pdf")
mg = TMultiGraph()
#gr_sigma.Draw("AP")
#gr_sigma.Fit("pol1")
mg.SetTitle("Fitted Mass Resolution")
#mg.GetXaxis().SetTitle("Truth Mass (MeV)")
#mg.GetYaxis().SetTitle("Sigma (MeV)")
#gr_sigma.SetTitle("Fitted Mass Resolution")
gr_sigma.SetTitle("A' MC")
gr_sigma.GetXaxis().SetTitle("Truth Mass (MeV)")
gr_sigma.GetYaxis().SetTitle("Sigma (MeV)")
gr_sigma.SetLineColor(4)
gr_sigma.SetMarkerColor(4)
gr_sigma.SetMarkerStyle(31)
gr_sigma_scaled.SetLineColor(2)
gr_sigma_scaled.SetMarkerColor(2)
gr_sigma_scaled.SetTitle("A' MC Scaled")
gr_sigma_scaled.SetMarkerStyle(31)
#gr_sigma.Draw("AP")
#gr_sigma_scaled.Draw("P")
gr_sigma_scaled.Fit("pol1")
gr_moller_data.SetMarkerStyle(22)
gr_moller_data.SetMarkerColor(6)
gr_moller_data.SetLineColor(6)
gr_moller_data.SetTitle("Moller Data")
gr_moller_mc.SetMarkerStyle(21)
gr_moller_mc.SetLineColor(7)
gr_moller_mc.SetMarkerColor(7)
gr_moller_mc.SetTitle("Moller MC")
#gr_moller_data.Draw("P")
#gr_moller_mc.Draw("P")
mg.Add(gr_sigma)
mg.Add(gr_sigma_scaled)
mg.Add(gr_moller_data)
mg.Add(gr_moller_mc)
mg.Draw("AP")
#legend = TLegend(.08,.46,.42,.87)
#legend.SetBorderSize(0)
#legend.SetFillColor(0)
#legend.SetFillStyle(0)
#legend.SetTextFont(42)
#legend.SetTextSize(0.035)
#legend.AddEntry(gr_sigma,"A' MC Res","LP")
#legend.AddEntry(gr_sigma_scaled,"A' MC Res Scaled","LP")
#legend.AddEntry(gr_moller_data,"Moller Res Data","LP")
#legend.AddEntry(gr_moller_mc,"Moller Res MC","LP")
#mg.Add(legend)
mg.Draw("AP")
c.BuildLegend(.1,.56,.35,.87)
c.Print(outfile+".pdf")

closePDF(outfile,c)