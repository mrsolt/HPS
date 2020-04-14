import sys
tmpargv = sys.argv
sys.argv = []
import getopt
import numpy as np
import array
import ROOT
import random
from ROOT import gROOT, TFile, TTree, TChain, gDirectory, TLine, gStyle, TCanvas, TLegend, TH1F, TF1, TGraphErrors, TMultiGraph, TGraph
sys.argv = tmpargv

#List arguments
def print_usage():
    print "\nUsage: {0} <output file base name> <input A' text file>".format(sys.argv[0])
    print "Arguments: "
    print '\t-h: this help message'
    print

zbin = 5.
zTarg = -4.3
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

def SmearHisto(events,nBins,minX,maxX,mass,isTar=False):
	smear_Top5hits = 0.0589307 
	smear_Top6hits = 0.0433669 
	smear_Bot5hits = 0.0551252 
	smear_Bot6hits = 0.045657 
	histo = TH1F("histo","histo",nBins,minX,maxX)
	eleP = array.array('d',[0])
	posP = array.array('d',[0])
	uncM = array.array('d',[0])
	tarM = array.array('d',[0])
	eleNTrackHits = array.array('d',[0])
	posNTrackHits = array.array('d',[0])
	eleTrkLambda = array.array('d',[0])

	events.Branch("eleP",eleP,"eleP/D")
	events.Branch("posP",posP,"posP/D")
	events.Branch("uncM",uncM,"uncM/D")
	events.Branch("tarM",tarM,"tarM/D")
	events.Branch("eleNTrackHits",eleNTrackHits,"eleNTrackHits/I")
	events.Branch("posNTrackHits",posNTrackHits,"posNTrackHits/I")
	events.Branch("eleTrkLambda",eleTrkLambda,"eleTrkLambda/D")

	nevents = events.GetEntries()

	ntop5 = 0
	ntop6 = 0
	nbot5 = 0
	nbot6 = 0

	for entry in xrange(nevents):
		events.GetEntry(entry)
		if(events.eleTrkLambda > 0):
			if(events.eleNTrackHits == 5):
				ele_smear = smear_Top5hits
				ntop5 = ntop5 + 1
			else:
				ele_smear = smear_Top6hits
				ntop6 = ntop6 + 1
			if(events.posNTrackHits == 5):
				pos_smear = smear_Bot5hits
				nbot5 = nbot5 + 1
			else:
				pos_smear = smear_Bot6hits
				nbot6 = nbot6 + 1
		else:
			if(events.eleNTrackHits == 5):
				ele_smear = smear_Bot5hits
				nbot5 = nbot5 + 1
			else:
				ele_smear = smear_Bot6hits
				nbot6 = nbot6 + 1
			if(events.posNTrackHits == 5):
				pos_smear = smear_Top5hits
				ntop5 = ntop5 + 1
			else:
				pos_smear = smear_Top6hits
				ntop6 = ntop6 + 1

		P_positron_Smear = random.gauss(events.posP, events.posP*pos_smear)
		P_electron_Smear = random.gauss(events.eleP, events.eleP*ele_smear)

		#print("Electron: Nhits = {0}  Slope = {1:0.3f}  Smear: {2}  Ele Smear = {3}".format(events.eleNTrackHits,events.eleTrkLambda,ele_smear,P_electron_Smear))
		#print("Positron: Nhits = {0}  Slope = {1:0.3f}  Semar: {2}  Pos Smear = {3}".format(events.posNTrackHits,events.posTrkLambda,pos_smear,P_positron_Smear))

		if(not isTar):
			MSmear = np.sqrt((P_positron_Smear/events.posP)*(P_electron_Smear/events.eleP))*events.uncM
		else:
			MSmear = np.sqrt((P_positron_Smear/events.posP)*(P_electron_Smear/events.eleP))*events.tarM
		histo.Fill(MSmear*1000-mass)
	print("Is tar: {5}  Mass: {0}  N5hitstop: {1}  N6hitstop: {2}  N5hitsbot: {3}  N6hitsbot: {4}".format(mass,ntop5,ntop6,nbot5,nbot6,isTar))

	return histo


def saveTupleFitPlotSmeared(events,inHisto,mass,nBins,minX,maxX,outfile,canvas,isTar=False):
	histo = SmearHisto(events,nBins,minX,maxX,mass,isTar)
	histo.SetTitle("Reconstructed Mass Smeared {0:.0f} MeV A'".format(mass))
	histo.GetXaxis().SetTitle("Reconstructed Mass (MeV)")
	f1 = TF1("f1","gaus",histo.GetMean()-1.5*histo.GetRMS(),histo.GetMean()+1.5*histo.GetRMS())
	histo.Fit("f1","R")
	histo.Draw("PE")
	canvas.Print(outfile+".pdf")
	mean = f1.GetParameter(1)
	sigma = f1.GetParameter(2)
	meanerror = f1.GetParError(1)
	sigmaerror = f1.GetParError(2)
	outfileroot.cd()
	canvas.Write()
	del f1
	del histo
	return mean, sigma, meanerror, sigmaerror

def saveTupleFitPlot(events,inHisto,mass,nBins,minX,maxX,outfile,canvas):
	events.Draw("{0}>>histo({1},{2},{3})".format(inHisto,nBins,minX,maxX))
	histo = ROOT.gROOT.FindObject("histo")
	histo.SetTitle("Reconstructed Mass {0:.0f} MeV A'".format(mass))
	histo.GetXaxis().SetTitle("Reconstructed Mass (MeV)")
	window = (1.5-1.0)*(mass - 50)/(150-50) + 1.0
	f1 = TF1("f1","gaus",histo.GetMean()-window*histo.GetRMS(),histo.GetMean()+window*histo.GetRMS())
	histo.Fit("f1","R")
	histo.Draw("PE")
	canvas.Print(outfile+".pdf")
	mean = f1.GetParameter(1)
	sigma = f1.GetParameter(2)
	meanerror = f1.GetParError(1)
	sigmaerror = f1.GetParError(2)
	outfileroot.cd()
	canvas.Write()
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
	outfileroot.cd()
	canvas.Write()
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
	gr_mean.SetTitle("Fitted Mass - Truth Mass Mean {0:.0f} MeV A'".format(mass))
	gr_mean.GetXaxis().SetTitle("Truth Z (mm)")
	gr_mean.GetYaxis().SetTitle("Mean (MeV)")
	gr_mean.GetYaxis().SetRangeUser(-5,5)
	canvas.Print(outfile+".pdf")
	outfileroot.cd()
	canvas.Write()
	gr_sigma.Draw("AP")
	gr_sigma.SetTitle("Fitted Mass Resolution {0:.0f} MeV A'".format(mass))
	gr_sigma.GetXaxis().SetTitle("Truth Z (mm)")
	gr_sigma.GetYaxis().SetTitle("Sigma (MeV)")
	gr_sigma.GetYaxis().SetRangeUser(0,8)
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

moller_mass_data = 0.048812*1000
moller_mass_res_data = 0.002598*1000
moller_mass_mc = 0.048487*1000
moller_mass_res_mc = 0.001817*1000
moller_mass_smeared_mc = 0.048406*1000
moller_mass_res_smeared_mc = 0.002462*1000

ratio = moller_mass_res_data / moller_mass_res_mc

moller_mass_data_err = 0.0 #0.00001*1000
moller_mass_res_data_err = 0.0 #0.000007*1000
moller_mass_mc_err = 0.0 #0.001*1000
moller_mass_res_mc_err = 0.0 #0.000003*1000
moller_mass_mc_smeared_err = 0.0
moller_mass_res_mc_smeared_err = 0.0

moller_mass_data_arr = array.array('d')
moller_mass_res_data_arr = array.array('d')
moller_mass_mc_arr = array.array('d')
moller_mass_res_mc_arr = array.array('d')
moller_mass_mc_smeared_arr = array.array('d')
moller_mass_res_mc_smeared_arr = array.array('d')

moller_mass_data_err_arr = array.array('d')
moller_mass_res_data_err_arr = array.array('d')
moller_mass_mc_err_arr = array.array('d')
moller_mass_res_mc_err_arr = array.array('d')
moller_mass_mc_smeared_err_arr = array.array('d')
moller_mass_res_mc_smeared_err_arr = array.array('d')

moller_mass_data_arr.append(moller_mass_data)
moller_mass_res_data_arr.append(moller_mass_res_data)
moller_mass_mc_arr.append(moller_mass_mc)
moller_mass_res_mc_arr.append(moller_mass_res_mc)
moller_mass_mc_smeared_arr.append(moller_mass_smeared_mc)
moller_mass_res_mc_smeared_arr.append(moller_mass_res_smeared_mc)

moller_mass_data_err_arr.append(moller_mass_data_err)
moller_mass_res_data_err_arr.append(moller_mass_res_data_err)
moller_mass_mc_err_arr.append(moller_mass_mc_smeared_err)
moller_mass_res_mc_err_arr.append(moller_mass_res_mc_smeared_err)
moller_mass_mc_smeared_err_arr.append(moller_mass_mc_smeared_err)
moller_mass_res_mc_smeared_err_arr.append(moller_mass_res_mc_smeared_err)


#moller_mass_data = 0.048812*1000
moller_mass_res_data_targ = 0.001945*1000
#moller_mass_mc = 0.048487*1000
moller_mass_res_mc_targ = 0.000957*1000
#moller_mass_smeared_mc = 0.048406*1000
#moller_mass_res_smeared_mc = 0.002462*1000

ratio_targ = moller_mass_res_data_targ / moller_mass_res_mc_targ

nBins = 200
maxX = 15.
minX = -maxX

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


fittedmean = array.array('d')
fittedsigma = array.array('d')
fittedsigmascaled = array.array('d')
fittedmeansmeared = array.array('d')
fittedsigmasmeared = array.array('d')
fittedmeanerror = array.array('d')
fittedsigmaerror = array.array('d')
fittedsigmascalederror = array.array('d')
fittedmeansmearederror = array.array('d')
fittedsigmasmearederror = array.array('d')

fittedmean_targ = array.array('d')
fittedsigma_targ = array.array('d')
fittedsigmascaled_targ = array.array('d')
fittedmeansmeared_targ = array.array('d')
fittedsigmasmeared_targ = array.array('d')
fittedmeanerror_targ = array.array('d')
fittedsigmaerror_targ = array.array('d')
fittedsigmascalederror_targ = array.array('d')
fittedmeansmearederror_targ = array.array('d')
fittedsigmasmearederror_targ = array.array('d')

openPDF(outfile,c)
for i in range(len(mass)):
	mean, sigma, meanerror, sigmaerror = saveTupleFitPlot(events[i],"(uncM*1000-{0:.0f})".format(mass[i]),mass[i],nBins,minX,maxX,outfile,c)
	meansmeared, sigmasmeared, meansmearderror, sigmasmearederror = saveTupleFitPlotSmeared(events[i],"(uncM*1000-{0:.0f})".format(mass[i]),mass[i],nBins,minX,maxX,outfile,c)
	mean_targ, sigma_targ, meanerror_targ, sigmaerror_targ = saveTupleFitPlot(events[i],"(tarM*1000-{0:.0f})".format(mass[i]),mass[i],nBins,minX,maxX,outfile,c)
	meansmeared_targ, sigmasmeared_targ, meansmearderror_targ, sigmasmearederror_targ = saveTupleFitPlotSmeared(events[i],"(tarM*1000-{0:.0f})".format(mass[i]),mass[i],nBins,minX,maxX,outfile,c,True)
	#saveTupleFitPlotsZ(events[i],"(uncM*1000-{0:.0f})".format(mass[i]),mass[i],nBins,minX,maxX,zbin,zTarg,maxZ,outfile,c)
	fittedmean.append(mean)
	fittedsigma.append(sigma)
	fittedsigmascaled.append(sigma*ratio)
	fittedmeansmeared.append(meansmeared) 
	fittedsigmasmeared.append(sigmasmeared) 
	fittedmeanerror.append(meanerror)
	fittedsigmaerror.append(sigmaerror)
	fittedsigmascalederror.append(sigmaerror*ratio)
	fittedmeansmearederror.append(meansmearderror) 
	fittedsigmasmearederror.append(sigmasmearederror) 

	fittedmean_targ.append(mean_targ)
	fittedsigma_targ.append(sigma_targ)
	fittedsigmascaled_targ.append(sigma_targ*ratio_targ)
	fittedmeansmeared_targ.append(meansmeared_targ) 
	fittedsigmasmeared_targ.append(sigmasmeared_targ) 
	fittedmeanerror_targ.append(meanerror_targ)
	fittedsigmaerror_targ.append(sigmaerror_targ)
	fittedsigmascalederror_targ.append(sigmaerror_targ*ratio_targ)
	fittedmeansmearederror_targ.append(meansmearderror_targ) 
	fittedsigmasmearederror_targ.append(sigmasmearederror_targ) 


gr_mean = TGraphErrors(len(mass),mass,fittedmean,masserror,fittedmeanerror)
gr_mean_smeared = TGraphErrors(len(mass),mass,fittedmeansmeared,masserror,fittedmeansmearederror)

gr_sigma = TGraphErrors(len(mass),mass,fittedsigma,masserror,fittedsigmaerror)
gr_sigma_smeared = TGraphErrors(len(mass),mass,fittedsigmasmeared,masserror,fittedsigmasmearederror)
gr_sigma_scaled = TGraphErrors(len(mass),mass,fittedsigmascaled,masserror,fittedsigmascalederror)
gr_sigma_targ = TGraphErrors(len(mass),mass,fittedsigma_targ,masserror,fittedsigmaerror_targ)
gr_sigma_smeared_targ = TGraphErrors(len(mass),mass,fittedsigmasmeared_targ,masserror,fittedsigmasmearederror_targ)
gr_sigma_scaled_targ = TGraphErrors(len(mass),mass,fittedsigmascaled_targ,masserror,fittedsigmascalederror_targ)

#gr_moller_data = TGraphErrors(1,moller_mass_data_arr,moller_mass_res_data_arr,moller_mass_data_err_arr,moller_mass_res_data_err_arr)
#gr_moller_mc = TGraphErrors(1,moller_mass_mc_arr,moller_mass_res_mc_arr,moller_mass_mc_err_arr,moller_mass_res_mc_err_arr)
#gr_moller_mc_smeared = TGraphErrors(1,moller_mass_mc_smeared_arr,moller_mass_res_mc_smeared_arr,moller_mass_mc_smeared_err_arr,moller_mass_res_mc_smeared_err_arr)

outfileroot.cd()
c.Clear()
gr_mean.SetTitle("Fitted Mass - Truth Mass Mean")
gr_mean.GetXaxis().SetTitle("Truth Mass (MeV)")
gr_mean.GetYaxis().SetTitle("Fitted Mean (MeV)")
gr_mean.Draw("AP")
gr_mean_smeared.SetLineColor(2)
gr_mean_smeared.SetMarkerColor(2)
gr_mean_smeared.Draw("Psame")
legend = TLegend(.08,.46,.42,.87)
legend.SetBorderSize(0)
legend.SetFillColor(0)
legend.SetFillStyle(0)
legend.SetTextFont(42)
legend.SetTextSize(0.035)
legend.AddEntry(gr_mean,"A' MC","LP")
legend.AddEntry(gr_mean_smeared,"A' MC Smeared","LP")
legend.Draw()
c.Print(outfile+".pdf")
c.Write()
c.Clear()
mg = TMultiGraph()

mg.SetTitle("Fitted Mass Resolution")

gr_sigma.SetTitle("Unc")
gr_sigma.GetXaxis().SetTitle("Truth Mass (MeV)")
gr_sigma.GetYaxis().SetTitle("Sigma (MeV)")
gr_sigma.SetLineColor(4)
gr_sigma.SetMarkerColor(4)
gr_sigma.SetMarkerStyle(31)
gr_sigma_scaled.SetLineColor(2)
gr_sigma_scaled.SetMarkerColor(2)
gr_sigma_scaled.SetTitle("Unc Scaled")
gr_sigma_scaled.SetMarkerStyle(31)

#gr_sigma_smeared.Fit("pol1")
gr_sigma_smeared.SetLineColor(28)
gr_sigma_smeared.SetMarkerColor(28)
gr_sigma_smeared.SetTitle("Unc Smeared")
gr_sigma_smeared.SetMarkerStyle(28)

#gr_sigma_smeared.Fit("pol1")
gr_sigma_targ.SetMarkerStyle(22)
gr_sigma_targ.SetMarkerColor(6)
gr_sigma_targ.SetLineColor(6)
gr_sigma_targ.SetTitle("Tar")
gr_sigma_smeared_targ.SetMarkerStyle(21)
gr_sigma_smeared_targ.SetLineColor(7)
gr_sigma_smeared_targ.SetMarkerColor(7)
gr_sigma_smeared_targ.SetTitle("Tar Smeared")
gr_sigma_scaled_targ.SetMarkerStyle(21)
gr_sigma_scaled_targ.SetLineColor(9)
gr_sigma_scaled_targ.SetMarkerColor(9)
gr_sigma_scaled_targ.SetTitle("Tar Scaled")

mg.Add(gr_sigma)
mg.Add(gr_sigma_scaled)
mg.Add(gr_sigma_smeared)
mg.Add(gr_sigma_targ)
mg.Add(gr_sigma_smeared_targ)
mg.Add(gr_sigma_scaled_targ)
mg.Draw("AP")

mg.GetXaxis().SetTitle("Truth Mass (MeV)")
mg.GetYaxis().SetTitle("Sigma (MeV)")
mg.GetXaxis().SetLimits(0,200)
mg.SetMinimum(0)
mg.SetMaximum(10)
c.BuildLegend(.1,.56,.35,.87)
c.Print(outfile+".pdf")
c.Write()

c.Clear()
mg2 = TMultiGraph()

mg2.SetTitle("Fitted Mass Resolution")

fittedsigma_rafo = array.array('d')
fittedsigma_rafo.append(1.15176)
fittedsigma_rafo.append(1.21732)
fittedsigma_rafo.append(1.29698)
fittedsigma_rafo.append(1.39461)
fittedsigma_rafo.append(1.48885)
fittedsigma_rafo.append(1.57288)
fittedsigma_rafo.append(1.67372)
fittedsigma_rafo.append(1.74502)
fittedsigma_rafo.append(1.86953)
fittedsigma_rafo.append(1.97314)
fittedsigma_rafo.append(2.06126)
fittedsigma_rafo.append(2.14772)
fittedsigma_rafo.append(2.28835)
fittedsigma_rafo.append(0)
fittedsigma_rafo.append(2.49713)
fittedsigma_rafo.append(2.62154)
fittedsigma_rafo.append(2.73272)
fittedsigma_rafo.append(2.84772)
fittedsigma_rafo.append(2.97061)
fittedsigma_rafo.append(3.03863)
fittedsigma_rafo.append(0)
fittedsigma_rafo.append(3.61197)


fittedsigmasmeared_rafo = array.array('d')
fittedsigmasmeared_rafo.append(2.14523)
fittedsigmasmeared_rafo.append(2.32694)
fittedsigmasmeared_rafo.append(2.50276)
fittedsigmasmeared_rafo.append(2.70645)
fittedsigmasmeared_rafo.append(2.88588)
fittedsigmasmeared_rafo.append(3.08217)
fittedsigmasmeared_rafo.append(3.30482)
fittedsigmasmeared_rafo.append(3.50827)
fittedsigmasmeared_rafo.append(3.73348)
fittedsigmasmeared_rafo.append(3.95888)
fittedsigmasmeared_rafo.append(4.19713)
fittedsigmasmeared_rafo.append(4.45267)
fittedsigmasmeared_rafo.append(4.68864)
fittedsigmasmeared_rafo.append(0)
fittedsigmasmeared_rafo.append(5.19711)
fittedsigmasmeared_rafo.append(5.43123)
fittedsigmasmeared_rafo.append(5.65723)
fittedsigmasmeared_rafo.append(5.96279)
fittedsigmasmeared_rafo.append(6.17555)
fittedsigmasmeared_rafo.append(6.42349)
fittedsigmasmeared_rafo.append(0)
fittedsigmasmeared_rafo.append(7.65201)

fittedsigmascaled_rafo = array.array('d')
for i in range(len(fittedsigma_rafo)):
	fittedsigmascaled_rafo.append(fittedsigma_rafo[i]*ratio_targ)

gr_sigma_rafo = TGraph(len(mass),mass,fittedsigma_rafo)
gr_sigma_smeared_rafo = TGraph(len(mass),mass,fittedsigmasmeared_rafo)
gr_sigma_scaled_rafo = TGraph(len(mass),mass,fittedsigmascaled_rafo)

gr_sigma_rafo.SetTitle("Rafo")
gr_sigma_rafo.GetXaxis().SetTitle("Truth Mass (MeV)")
gr_sigma_rafo.GetYaxis().SetTitle("Sigma (MeV)")
gr_sigma_rafo.SetLineColor(4)
gr_sigma_rafo.SetMarkerColor(4)
gr_sigma_rafo.SetMarkerStyle(31)
gr_sigma_scaled_rafo.SetLineColor(2)
gr_sigma_scaled_rafo.SetMarkerColor(2)
gr_sigma_scaled_rafo.SetTitle("Rafo Scaled")
gr_sigma_scaled_rafo.SetMarkerStyle(31)

#gr_sigma_smeared.Fit("pol1")
gr_sigma_smeared_rafo.SetLineColor(28)
gr_sigma_smeared_rafo.SetMarkerColor(28)
gr_sigma_smeared_rafo.SetTitle("Rafo Smeared")
gr_sigma_smeared_rafo.SetMarkerStyle(28)

gr_sigma_targ2 = TGraphErrors(len(mass),mass,fittedsigma_targ,masserror,fittedsigmaerror_targ)
gr_sigma_smeared_targ2 = TGraphErrors(len(mass),mass,fittedsigmasmeared_targ,masserror,fittedsigmasmearederror_targ)
gr_sigma_scaled_targ2 = TGraphErrors(len(mass),mass,fittedsigmascaled_targ,masserror,fittedsigmascalederror_targ)

gr_sigma_targ2.SetMarkerStyle(22)
gr_sigma_targ2.SetMarkerColor(6)
gr_sigma_targ2.SetLineColor(6)
gr_sigma_targ2.SetTitle("Tar")
gr_sigma_smeared_targ2.SetMarkerStyle(21)
gr_sigma_smeared_targ2.SetLineColor(7)
gr_sigma_smeared_targ2.SetMarkerColor(7)
gr_sigma_smeared_targ2.SetTitle("Tar Smeared")
gr_sigma_scaled_targ2.SetMarkerStyle(21)
gr_sigma_scaled_targ2.SetLineColor(9)
gr_sigma_scaled_targ2.SetMarkerColor(9)
gr_sigma_scaled_targ2.SetTitle("Tar Scaled")

mg2.Add(gr_sigma_rafo)
mg2.Add(gr_sigma_scaled_rafo)
mg2.Add(gr_sigma_smeared_rafo)
mg2.Add(gr_sigma_targ2)
mg2.Add(gr_sigma_smeared_targ2)
mg2.Add(gr_sigma_scaled_targ2)
mg2.Draw("AP")

mg2.GetXaxis().SetTitle("Truth Mass (MeV)")
mg2.GetYaxis().SetTitle("Sigma (MeV)")
mg2.GetXaxis().SetLimits(0,200)
mg2.SetMinimum(0)
mg2.SetMaximum(10)
c.BuildLegend(.1,.56,.35,.87)
c.Print(outfile+".pdf")
c.Write()

closePDF(outfile,c)
outfileroot.Close()