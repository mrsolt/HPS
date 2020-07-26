import sys
tmpargv = sys.argv
sys.argv = []
import getopt
import numpy as np
import array
import ROOT
import random
from ROOT import gROOT, TFile, TTree, TChain, gDirectory, TLine, gStyle, TCanvas, TLegend, TH1F, TF1, TGraphErrors, TMultiGraph
sys.argv = tmpargv

#List arguments
def print_usage():
    print "\nUsage: {0} <output file base name> <input A' text file>".format(sys.argv[0])
    print "Arguments: "
    print '\t-r: is L1L2 (default false)'
    print '\t-s: is L2L2 (default false)'
    print '\t-y: label'
    print '\t-h: this help message'
    print

zbin = 5.
zTarg = -4.3
maxZ = 100
L1L2 = False
L2L2 = False
label = ""

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'rsy:h')

# Parse the command line arguments
for opt, arg in options:
		if opt=='-r':
			L1L2 = True
		if opt=='-s':
			L2L2 = True
		if opt=='-y':
			label = float(arg)
		if opt=='-h':
			print_usage()
			sys.exit(0)

if(L1L2):
	label = "L1L2"
elif(L2L2):
	label = "L2L2"
else:
	label = "L1L1"

gStyle.SetOptStat(0)
gStyle.SetOptFit(1011)
c = TCanvas("c","c",800,600)

def SmearHisto(events,nBins,minX,maxX,mass):
	smear_Top5hits = 0.0589307 
	smear_Top6hits = 0.0433669 
	smear_Bot5hits = 0.0551252 
	smear_Bot6hits = 0.045657 
	histo = TH1F("histo","histo",nBins,minX,maxX)
	eleP = array.array('d',[0])
	posP = array.array('d',[0])
	uncM = array.array('d',[0])
	eleNTrackHits = array.array('d',[0])
	posNTrackHits = array.array('d',[0])
	eleTrkLambda = array.array('d',[0])

	events.Branch("eleP",eleP,"eleP/D")
	events.Branch("posP",posP,"posP/D")
	events.Branch("uncM",uncM,"uncM/D")
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
		eleTrkhits = events.eleNTrackHits
		posTrkhits = events.posNTrackHits
		if(L2L2):
			eleTrkhits = 5
			posTrkhits = 5
		if(L1L2):
			L1L2frac = (events.uncM-0.06) * (0.85-0.5)/(0.15-0.06) + 0.5
			rndmele = random.random()
			rndmpos = random.random()         
			if(rndmele < L1L2frac):
				eleTrkhits = 5
			else:
				eleTrkhits = 6
			if(rndmpos < L1L2frac):
				posTrkhits = 5
			else:
				posTrkhits = 6
		if(events.eleTrkLambda > 0):
			if(eleTrkhits == 5):
				ele_smear = smear_Top5hits
				ntop5 = ntop5 + 1
			else:
				ele_smear = smear_Top6hits
				ntop6 = ntop6 + 1
			if(posTrkhits == 5):
				pos_smear = smear_Bot5hits
				nbot5 = nbot5 + 1
			else:
				pos_smear = smear_Bot6hits
				nbot6 = nbot6 + 1
		else:
			if(eleTrkhits == 5):
				ele_smear = smear_Bot5hits
				nbot5 = nbot5 + 1
			else:
				ele_smear = smear_Bot6hits
				nbot6 = nbot6 + 1
			if(posTrkhits == 5):
				pos_smear = smear_Top5hits
				ntop5 = ntop5 + 1
			else:
				pos_smear = smear_Top6hits
				ntop6 = ntop6 + 1

		P_positron_Smear = random.gauss(events.posP, events.posP*pos_smear)
		P_electron_Smear = random.gauss(events.eleP, events.eleP*ele_smear)

		#print("Electron: Nhits = {0}  Slope = {1:0.3f}  Smear: {2}  Ele Smear = {3}".format(events.eleNTrackHits,events.eleTrkLambda,ele_smear,P_electron_Smear))
		#print("Positron: Nhits = {0}  Slope = {1:0.3f}  Semar: {2}  Pos Smear = {3}".format(events.posNTrackHits,events.posTrkLambda,pos_smear,P_positron_Smear))

		MSmear = np.sqrt((P_positron_Smear/events.posP)*(P_electron_Smear/events.eleP))*events.uncM
		histo.Fill(MSmear*1000-mass)
	print("Mass: {0}  N5hitstop: {1}  N6hitstop: {2}  N5hitsbot: {3}  N6hitsbot: {4}".format(mass,ntop5,ntop6,nbot5,nbot6))

	return histo


def saveTupleFitPlotSmeared(events,inHisto,mass,nBins,minX,maxX,outfile,canvas):
	histo = SmearHisto(events,nBins,minX,maxX,mass)
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

nBins = 50
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

openPDF(outfile,c)
for i in range(len(mass)):
	mean, sigma, meanerror, sigmaerror = saveTupleFitPlot(events[i],"(uncM*1000-{0:.0f})".format(mass[i]),mass[i],nBins,minX,maxX,outfile,c)
	meansmeared, sigmasmeared, meansmearderror, sigmasmearederror = saveTupleFitPlotSmeared(events[i],"(uncM*1000-{0:.0f})".format(mass[i]),mass[i],nBins,minX,maxX,outfile,c)
	saveTupleFitPlotsZ(events[i],"(uncM*1000-{0:.0f})".format(mass[i]),mass[i],nBins,minX,maxX,zbin,zTarg,maxZ,outfile,c)
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


gr_mean = TGraphErrors(len(mass),mass,fittedmean,masserror,fittedmeanerror)
gr_mean_smeared = TGraphErrors(len(mass),mass,fittedmeansmeared,masserror,fittedmeansmearederror)
gr_sigma = TGraphErrors(len(mass),mass,fittedsigma,masserror,fittedsigmaerror)
gr_sigma_smeared = TGraphErrors(len(mass),mass,fittedsigmasmeared,masserror,fittedsigmasmearederror)
gr_sigma_scaled = TGraphErrors(len(mass),mass,fittedsigmascaled,masserror,fittedsigmascalederror)
gr_moller_data = TGraphErrors(1,moller_mass_data_arr,moller_mass_res_data_arr,moller_mass_data_err_arr,moller_mass_res_data_err_arr)
gr_moller_mc = TGraphErrors(1,moller_mass_mc_arr,moller_mass_res_mc_arr,moller_mass_mc_err_arr,moller_mass_res_mc_err_arr)
gr_moller_mc_smeared = TGraphErrors(1,moller_mass_mc_smeared_arr,moller_mass_res_mc_smeared_arr,moller_mass_mc_smeared_err_arr,moller_mass_res_mc_smeared_err_arr)

outfileroot.cd()
c.Clear()
gr_mean_smeared.SetTitle("Fitted Mass - Truth Mass Mean")
gr_mean_smeared.GetXaxis().SetTitle("Truth Mass (MeV)")
gr_mean_smeared.GetYaxis().SetTitle("Fitted Mean (MeV)")
gr_mean_smeared.Draw("AP")
gr_mean.SetLineColor(2)
gr_mean.SetMarkerColor(2)
gr_mean.Draw("Psame")
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
#gr_sigma.Draw("AP")
#gr_sigma.Fit("pol1")
mg.SetTitle("Fitted Mass Resolution {0}".format(label))
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
gr_sigma_smeared.Fit("pol4")
gr_sigma_smeared.SetLineColor(28)
gr_sigma_smeared.SetMarkerColor(28)
gr_sigma_smeared.SetTitle("A' MC Smeared")
gr_sigma_smeared.SetMarkerStyle(28)
#gr_sigma_scaled.Fit("pol1")
gr_sigma_smeared.Fit("pol4")
gr_moller_data.SetMarkerStyle(22)
gr_moller_data.SetMarkerColor(6)
gr_moller_data.SetLineColor(6)
gr_moller_data.SetTitle("Moller Data")
gr_moller_mc.SetMarkerStyle(21)
gr_moller_mc.SetLineColor(7)
gr_moller_mc.SetMarkerColor(7)
gr_moller_mc.SetTitle("Moller MC")
gr_moller_mc_smeared.SetMarkerStyle(21)
gr_moller_mc_smeared.SetLineColor(9)
gr_moller_mc_smeared.SetMarkerColor(9)
gr_moller_mc_smeared.SetTitle("Moller MC Smeared")
#gr_moller_data.Draw("P")
#gr_moller_mc.Draw("P")
mg.Add(gr_sigma)
mg.Add(gr_sigma_scaled)
mg.Add(gr_sigma_smeared)
mg.Add(gr_moller_data)
mg.Add(gr_moller_mc)
mg.Add(gr_moller_mc_smeared)
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
mg.GetXaxis().SetTitle("Truth Mass (MeV)")
mg.GetYaxis().SetTitle("Sigma (MeV)")
mg.GetXaxis().SetLimits(0,200)
mg.SetMinimum(0)
mg.SetMaximum(10)
c.BuildLegend(.1,.56,.35,.87)
c.Print(outfile+".pdf")
c.Write()

closePDF(outfile,c)
outfileroot.Close()