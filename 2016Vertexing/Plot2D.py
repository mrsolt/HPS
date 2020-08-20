import sys
tmpargv = sys.argv
sys.argv = []
import numpy as np
import getopt
import ROOT
from ROOT import gROOT, TFile, TTree, TChain, gDirectory, TLine, gStyle, TCanvas, TLegend, TH1F, TF1, TLatex, TGraph
sys.argv = tmpargv

#List arguments
def print_usage():
	print ("\nUsage: {0} <output file base name> <input file> <label>".format(sys.argv[0]))
	print ('\t-z: plot zcut (default false)')
	print ('\t-r: is L1L2 (default false)')
	print ('\t-t: is L2L2 (default false)')
	print ('\t-s: plot shaded region (default false)')
	print ('\t-h: this help message')
	print

plotZcut = False
isL1L2 = False
isL2L2 = False
Shaded = False

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'zrtsh')

# Parse the command line arguments
for opt, arg in options:
		if opt=='-z':
			plotZcut = True
		if opt=='-r':
			isL1L2 = True
		if opt=='-t':
			isL2L2 = True
		if opt=='-s':
			Shaded = True
		if opt=='-h':
			print_usage()
			sys.exit(0)

gStyle.SetOptStat(0)
c = TCanvas("c","c",800,600)

def openPDF(outfile,canvas):
	c.Print(outfile+".pdf[")

def closePDF(outfile,canvas):
	c.Print(outfile+".pdf]")

outfile = remainder[0]
outfileroot = TFile(remainder[0]+".root","RECREATE")

file = TFile(remainder[1])
events = file.Get("ntuple")

label = ""
label = str(remainder[2])

if(isL2L2):
	events.Draw("uncVZ:uncM>>histo(100,0,0.2,100,-50,50)")
	histo = gDirectory.FindObject("histo")

else:
	events.Draw("uncVZ:uncM>>histo(100,0,0.2,100,-30,30)")
	histo = gDirectory.FindObject("histo")

histo.GetXaxis().SetTitle("Reconstructed e+e- Mass (GeV)")
histo.GetYaxis().SetTitle("Reconstructed z (mm)")
histo.SetTitle("Final Selection {0}".format(label))
histo.GetXaxis().SetLabelSize(0.05)
histo.GetYaxis().SetLabelSize(0.05)
#histo.GetZaxis().SetLabelSize(0.05)
histo.GetXaxis().SetTitleOffset(0.8)
histo.GetXaxis().SetTitleSize(0.06)
histo.GetYaxis().SetTitleOffset(0.8)
histo.GetYaxis().SetTitleSize(0.06)
histo.Draw("COLZ")
c.SetLogz(1)

openPDF(outfile,c)

outfileroot.cd()

c.Print(outfile+".pdf")
c.Write()
histo.Write("histo")

closePDF(outfile,c)

if(plotZcut):
	outfilezcut = outfile + "_zcut"
	openPDF(outfilezcut,c)

	if(isL1L2):
		#fz_10per = TF1("fz_10per","{0}+{1}*x+{2}*x^2+{3}*x^3+{4}*x^4+{5}*x^5".format(-133,8211,-162000,1480000,-6406000,10560000),0.05,0.150) #L1L2 10%
		#fz_scaled = TF1("fz_scaled","{0}+{1}*x+{2}*x^2+{3}*x^3+{4}*x^4+{5}*x^5".format(-156.8,9720,-191100,1736000,-7433000,12040000),0.05,0.150) #L1L2 scaled 100%
		#fz_mc = TF1("fz_mc","{0}+{1}*x+{2}*x^2+{3}*x^3+{4}*x^4+{5}*x^5".format(25.23,47.14,-2987,12370,0,0),0.05,0.150) #L1L2 MC
		#fz_10per = TF1("fz_10per","{0}+{1}*x+{2}*x^2+{3}*x^3+{4}*x^4+{5}*x^5".format(-162,9927,-2.028e5,1.952e6,-9.05e6,1.627e7),0.05,0.150) #L1L2 10%
		#fz_scaled = TF1("fz_scaled","{0}+{1}*x+{2}*x^2+{3}*x^3+{4}*x^4+{5}*x^5".format(-199.6,1.224e4,-2.501e5,2.411e6,-1.117e7,2.001e7),0.05,0.150) #L1L2 scaled 100%
		#fz_mc = TF1("fz_mc","{0}+{1}*x+{2}*x^2+{3}*x^3+{4}*x^4+{5}*x^5".format(15.5,146.2,5740,-1.857e5,1.49e6,-3.796e6),0.05,0.150) #L1L2 MC
		fz_10per = TF1("fz_10per","{0}+{1}*x+{2}*x^2+{3}*x^3+{4}*x^4+{5}*x^5".format(-164.9,1.012e4,-2.087e5,2.039e6,-9.614e6,1.761e7),0.05,0.150) #L1L2 10%
		fz_scaled = TF1("fz_scaled","{0}+{1}*x+{2}*x^2+{3}*x^3+{4}*x^4+{5}*x^5".format(-205.6,1.258e4,-2.595e5,2.538e6,-1.197e7,2.19e7),0.05,0.150) #L1L2 scaled 100%
		fz_mc = TF1("fz_mc","{0}+{1}*x+{2}*x^2+{3}*x^3+{4}*x^4+{5}*x^5".format(74.12,-2922,7.02e4,-8.567e5,4.936e6,-1.075e7),0.05,0.150) #L1L2 MC

	elif(isL2L2):
		fz_10per = TF1("fz_10per","{0}+{1}*x+{2}*x^2+{3}*x^3+{4}*x^4+{5}*x^5".format(-168.1,1.14e4,-2.278e5,2.051e6,-8.728e6,1.438e7),0.05,0.150) #L2L2 10%
		fz_scaled = TF1("fz_scaled","{0}+{1}*x+{2}*x^2+{3}*x^3+{4}*x^4+{5}*x^5".format(-238.7,1.572e4,-3.165e5,2.912e6,-1.28e7,2.198e7),0.05,0.150) #L2L2 scaled 100%
		fz_mc = TF1("fz_mc","{0}+{1}*x+{2}*x^2+{3}*x^3+{4}*x^4+{5}*x^5".format(-816,5.006e4,-1.118e6,1.18e7,-5.97e7,1.169e8),0.05,0.150) #L2L2 MC

	else:
		#fz_10per = TF1("fz_10per","{0}+{1}*x+{2}*x^2+{3}*x^3+{4}*x^4+{5}*x^5".format(-2.308,1227,-29030,285300,-1296000,2229000),0.05,0.150) #L1L1 10%
		#fz_scaled = TF1("fz_scaled","{0}+{1}*x+{2}*x^2+{3}*x^3+{4}*x^4+{5}*x^5".format(1.628,1301,-31950,318900,-1456000,2497000),0.05,0.150) #L1L1 scaled 100%
		#fz_mc = TF1("fz_mc","{0}+{1}*x+{2}*x^2+{3}*x^3+{4}*x^4+{5}*x^5".format(22.23,48.63,-5150,49760,-169900,141700),0.05,0.150) #L1L1 MC
		#fz_10per = TF1("fz_10per","{0}+{1}*x+{2}*x^2+{3}*x^3+{4}*x^4+{5}*x^5".format(-3.413,1360,-3.276e4,3.292e5,-1.535e6,2.733e6),0.05,0.150) #L1L1 10%
		#fz_scaled = TF1("fz_scaled","{0}+{1}*x+{2}*x^2+{3}*x^3+{4}*x^4+{5}*x^5".format(1.809,1373,-3.444e4,3.503e5,-1.633e6,2.886e6),0.05,0.150) #L1L1 scaled 100%
		#fz_mc = TF1("fz_mc","{0}+{1}*x+{2}*x^2+{3}*x^3+{4}*x^4+{5}*x^5".format(19.42,245.1,-9846,1.011e5,-4.354e5,6.71e5),0.05,0.150) #L1L1 MC
		#fz_10per = TF1("fz_10per","{0}+{1}*x+{2}*x^2+{3}*x^3+{4}*x^4+{5}*x^5".format(19,53.04,-2566,-4258,2.345e5,-8.994e5),0.05,0.150) #L1L1 10%
		fz_10per= TF1("fz_10per","{0}+{1}*x+{2}*x^2+{3}*x^3+{4}*x^4+{5}*x^5".format(-0.4738,1551,-3.835e4,3.930e5,-1.865e6,3.373e6),0.05,0.150) #L1L1 100%
		fz_scaled = TF1("fz_scaled","{0}+{1}*x+{2}*x^2+{3}*x^3+{4}*x^4+{5}*x^5".format(26.85,-124.3,593.6,-3.954e4,4.451e5,-1.393e6),0.05,0.150) #L1L1 scaled 100%
		fz_mc = TF1("fz_mc","{0}+{1}*x+{2}*x^2+{3}*x^3+{4}*x^4+{5}*x^5".format(23.55,152.9,-9489,1.091e5,-5.19e5,9.013e5),0.05,0.150) #L1L1 MC

	histo.SetStats(0)
	histo.Draw("COLZ")

	fz_10per.SetLineColor(1)
	fz_scaled.SetLineColor(2)
	fz_mc.SetLineColor(4)

	fz_10per.Draw("same")
	fz_scaled.Draw("same")
	fz_mc.Draw("same")

	legend = TLegend(.68,.66,.92,.87)
	legend.SetBorderSize(0)
	legend.SetFillColor(0)
	legend.SetFillStyle(0)
	legend.SetTextFont(42)
	legend.SetTextSize(0.05)
	if(isL1L2 or isL2L2):
		legend.AddEntry(fz_10per,"10% Data","LP")
	else:
		legend.AddEntry(fz_10per,"100% Data","LP")
	legend.AddEntry(fz_scaled,"Scaled Data","LP")
	legend.AddEntry(fz_mc,"MC","LP")
	legend.Draw("same")

	c.Print(outfilezcut+".pdf")
	c.Write()

	closePDF(outfilezcut,c)

	if(Shaded):
		c.Clear()
		c.SetLogz(1)
		outfileshade = outfile + "_shade"
		openPDF(outfileshade,c)
		#f1 = TF1("f1","{0}+{1}*x+{2}*x^2+{3}*x^3+{4}*x^4+{5}*x^5".format(26.85,-124.3,593.6,-3.954e4,4.451e5,-1.393e6),0.06,0.150) #L1L1
		#f2 = TF1("f2","{0}+{1}*x+{2}*x^2".format(-6.75285,952.9,-3060.59),0.060,0.150) #L1L1
		#f1 = TF1("f1","{0}+{1}*x+{2}*x^2+{3}*x^3+{4}*x^4+{5}*x^5".format(-164.9,1.012e4,-2.087e5,2.039e6,-9.614e6,1.761e7),0.06,0.150) #L1L2
		#f2 = TF1("f2","{0}+{1}*x+{2}*x^2+{3}*x^3+{4}*x^4+{5}*x^5".format(166.199,-10.4546*1e3,0.269357*1e6,-0.00290368*1e9,1.44026e-05*1e12,-2.71387e-08*1e15),0.060,0.150) #L1L2
		f1 = TF1("f1","{0}+{1}*x+{2}*x^2+{3}*x^3+{4}*x^4+{5}*x^5".format(-168.1,1.14e4,-2.278e5,2.051e6,-8.728e6,1.438e7),0.06,0.150) #L2L2
		f2 = TF1("f2","{0}+{1}*x+{2}*x^2+{3}*x^3+{4}*x^4+{5}*x^5".format(-1219.51,55315.5,-917374,7.54833e+06,-3.03114e+07,4.70832e+07),0.060,0.150) #L2L2
		f2.SetFillColor(5)
		f2.SetFillStyle(3001)
		f2.SetLineColor(3)
		f1.SetLineColor(1)

		gr = TGraph()
		gr.SetFillColor(f2.GetFillColor())
		gr.SetFillStyle(f2.GetFillStyle())

		c.Update()

		xmin = 0.06 #c.GetUxmin()
		xmax = 0.15 #c.GetUxmax()
		ymin = 0 #c.GetUymin()
		ymax = 150 #c.GetUymax()

		npx = f2.GetNpx()
		npoints = 0
		dx = (xmax-xmin)/npx
		x = xmin+0.5*dx
		while (x <= xmax):
			y = f2.Eval(x)
			if (y < ymin): y = ymin
			if (y > ymax): y = ymax
			gr.SetPoint(npoints,x,y)
			npoints = npoints + 1
			x = x + dx

		x = xmax-0.5*dx
		while (x >= xmin):
			y = f1.Eval(x)
			#print y
			if (y < ymin): y = ymin
			if (y > ymax): y = ymax
			gr.SetPoint(npoints,x,y)
			npoints = npoints + 1
			x = x - dx

		#cut = "event!=138205858&&event!=26862757&&event!=134296298&&event!=105453502&&event!=25752733&&event!=4393084&&event!=81085838&&event!=9714720"
		cut = ""
		events.Draw("uncVZ:uncM>>histo2(100,0,0.2,180,-30,150)",cut)
		histo2 = gDirectory.FindObject("histo2")
		histo2.GetXaxis().SetTitle("Reconstructed e+e- Mass (GeV)")
		histo2.GetYaxis().SetTitle("Reconstructed z (mm)")
		histo2.SetTitle("Reconctructed Z vs Mass {0}".format(label))
		histo2.GetXaxis().SetLabelSize(0.05)
		histo2.GetYaxis().SetLabelSize(0.05)
		#histo2.GetZaxis().SetLabelSize(0.05)
		histo2.GetXaxis().SetTitleOffset(0.8)
		histo2.GetXaxis().SetTitleSize(0.06)
		histo2.GetYaxis().SetTitleOffset(0.8)
		histo2.GetYaxis().SetTitleSize(0.06)
		histo2.Draw("COLZ")
		f1.Draw("same")
		#f2.Draw("same")
		gr.Draw("f same") #draw graph with fill area option
		c.Print(outfileshade+".pdf")
		c.Write()

		closePDF(outfileshade,c)

outfileroot.Close()
