import sys
tmpargv = sys.argv
sys.argv = []
import getopt
import ROOT
from ROOT import gROOT, TFile, gDirectory, gStyle, TCanvas, TH1, TLegend, TPad, TLatex
sys.argv = tmpargv

#List arguments
def print_usage():
	print "\nUsage: {0} <output file base name> <input file name>".format(sys.argv[0])
	print "Arguments: "
	print '\t-g: number of sigma of fit (default 1)'
	print '\t-h: this help message'
	print

nsig = 1.

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'g:h')

# Parse the command line arguments
for opt, arg in options:
		if opt=='-g':
			nsig = float(arg)
		if opt=='-h':
			print_usage()
			sys.exit(0)

def openPDF(outfile,canvas):
	c.Print(outfile+".pdf[")

def closePDF(outfile,canvas):
	c.Print(outfile+".pdf]")

def savehisto(histo1,histo2,label1,label2,outfile,canvas,XaxisTitle="",YaxisTitle="",plotTitle="",stats=0,logY=1):
	canvas.Clear()
	RatioMin = 0.2
	RatioMax = 2.2
	#canvas.SetLogy(logY)

	top = TPad("top","top",0,0.42,1,1)
	top.SetLogy(logY)

	bot = TPad("bot","bot",0,0,1,0.38)

	top.Draw()
	top.SetBottomMargin(0)
	#top.SetTopMargin(gStyle.GetPadTopMargin()*topScale)
	bot.Draw()
	bot.SetTopMargin(0)
	bot.SetBottomMargin(0.4)
	top.cd()

	histo1.SetTitle(plotTitle)
	histo1.GetXaxis().SetTitle(XaxisTitle)
	histo1.GetYaxis().SetTitle("dN/dz (0.5 mm)^{-1}")
	histo1.GetXaxis().SetLabelSize(0.05)
	histo1.GetYaxis().SetLabelSize(0.05)
	histo1.GetZaxis().SetLabelSize(0.05)
	histo1.GetXaxis().SetTitleOffset(0.8)
	histo1.GetXaxis().SetTitleSize(0.06)
	histo1.GetYaxis().SetTitleOffset(0.8)
	histo1.GetYaxis().SetTitleSize(0.06)
	histo1.SetStats(stats)
	histo2.SetStats(stats)
	histo1.Sumw2()
	histo2.Sumw2()
	histo1.Scale(1/float(histo1.GetEntries()))
	histo2.Scale(1/float(histo2.GetEntries()))
	histo1.Scale(1/float(histo2.GetMaximum()))
	histo2.Scale(1/float(histo2.GetMaximum()))
	maximum = histo1.GetMaximum()
	if(histo2.GetMaximum() > maximum):
		maximum = histo2.GetMaximum()
	histo1.GetYaxis().SetRangeUser(0.000001,1.2*maximum)
	histo1.Draw("E1")
	histo2.SetLineColor(2)
	histo2.Draw("sameE1")
	legend = TLegend(.68,.66,.92,.87)
	legend.SetBorderSize(0)
	legend.SetFillColor(0)
	legend.SetFillStyle(0)
	legend.SetTextFont(42)
	legend.SetTextSize(0.035)
	legend.AddEntry(histo1,label1,"LP")
	legend.AddEntry(histo2,label2,"LP")
	legend.Draw("")

	bot.cd()
	reference = histo2.Clone("reference")
	reference.GetYaxis().SetTitle("Ratio")
	#reference.GetYaxis().SetTitleSize(0.06)
	reference.GetYaxis().SetLabelSize(0.1)
	#reference.GetXaxis().SetTitleSize(0.1)
	reference.GetXaxis().SetLabelSize(0.1)

	reference.GetXaxis().SetTitleOffset(0.8)
	reference.GetXaxis().SetTitleSize(0.12)
	reference.GetYaxis().SetTitleOffset(0.4)
	reference.GetYaxis().SetTitleSize(0.1)

	reference.GetXaxis().SetTitle(XaxisTitle)
	reference.GetYaxis().SetRangeUser(RatioMin,RatioMax)
	reference.GetYaxis().SetNdivisions(508)
	reference.GetYaxis().SetDecimals(True)
	reference.Draw("axis")
	ratio = histo1.Clone("Ratio"+histo1.GetName())
	ratio.Divide(reference)
	ratio.SetLineColor(1)
	ratio.DrawCopy("pe same")
	canvas.Print(outfile+".pdf")
	outfileroot.cd()
	canvas.Write()
	histo1.Write("{0} {1}".format(histo1.GetTitle(),label1))
	histo2.Write("{0} {1}".format(histo2.GetTitle(),label2))

def savegraph(graph1,graph2,label1,label2,outfile,canvas,xmin,xmax,ymin,ymax,XaxisTitle="",YaxisTitle="",plotTitle="",logY=0):
	canvas.Clear()
	#canvas.SetLogy(logY)
	graph1.SetTitle(plotTitle)
	graph1.GetXaxis().SetTitle(XaxisTitle)
	graph1.GetYaxis().SetTitle(YaxisTitle)
	graph1.GetXaxis().SetLabelSize(0.05)
	graph1.GetYaxis().SetLabelSize(0.05)
	#graph1.GetZaxis().SetLabelSize(0.05)
	graph1.GetXaxis().SetTitleOffset(0.8)
	graph1.GetXaxis().SetTitleSize(0.06)
	graph1.GetYaxis().SetTitleOffset(0.8)
	graph1.GetYaxis().SetTitleSize(0.06)
	graph1.GetXaxis().SetRangeUser(xmin,xmax)
	graph1.GetYaxis().SetRangeUser(ymin,ymax)
	graph1.Draw("AP")
	graph2.SetMarkerColor(2)
	graph2.SetLineColor(2)
	graph2.Draw("Psame")
	legend = TLegend(.68,.66,.92,.87)
	legend.SetBorderSize(0)
	legend.SetFillColor(0)
	legend.SetFillStyle(0)
	legend.SetTextFont(42)
	legend.SetTextSize(0.05)
	legend.AddEntry(graph1,label1,"P")
	legend.AddEntry(graph2,label2,"P")
	legend.Draw("")
	canvas.Print(outfile+".pdf")
	outfileroot.cd()
	canvas.Write()
	graph1.Write("{0} {1}".format(graph1.GetTitle(),label1))
	graph2.Write("{0} {1}".format(graph2.GetTitle(),label2))

def savegraph3(graph1,graph2,graph3,label1,label2,label3,outfile,canvas,xmin,xmax,ymin,ymax,XaxisTitle="",YaxisTitle="",plotTitle="",logY=0):
	canvas.Clear()
	#canvas.SetLogy(logY)
	graph1.SetTitle(plotTitle)
	graph1.GetXaxis().SetTitle(XaxisTitle)
	graph1.GetYaxis().SetTitle(YaxisTitle)
	graph1.GetXaxis().SetLabelSize(0.05)
	graph1.GetYaxis().SetLabelSize(0.05)
	#graph1.GetZaxis().SetLabelSize(0.05)
	graph1.GetXaxis().SetTitleOffset(0.8)
	graph1.GetXaxis().SetTitleSize(0.06)
	graph1.GetYaxis().SetTitleOffset(0.8)
	graph1.GetYaxis().SetTitleSize(0.06)
	graph1.GetXaxis().SetRangeUser(xmin,xmax)
	graph1.GetYaxis().SetRangeUser(ymin,ymax)
	graph1.Draw("AP")
	graph3.SetMarkerColor(4)
	graph3.SetLineColor(4)
	graph3.Draw("Psame")
	graph2.SetMarkerColor(2)
	graph2.SetLineColor(2)
	graph2.Draw("Psame")
	legend = TLegend(.68,.66,.92,.87)
	legend.SetBorderSize(0)
	legend.SetFillColor(0)
	legend.SetFillStyle(0)
	legend.SetTextFont(42)
	legend.SetTextSize(0.05)
	legend.AddEntry(graph1,label1,"P")
	legend.AddEntry(graph3,label2,"P")
	legend.AddEntry(graph2,label3,"P")
	legend.Draw("")
	canvas.Print(outfile+".pdf")
	outfileroot.cd()
	canvas.Write()

#gStyle.SetOptStat(0)
gStyle.SetOptStat(110011)
c = TCanvas("c","c",800,600)

outfile = remainder[0]
outfileroot = TFile(remainder[0]+".root","RECREATE")
infile1 = TFile(remainder[1])
infile2 = TFile(remainder[2])
label1 = remainder[3]
label2 = remainder[4]

infile1.cd()
histos1 = []
for h in infile1.GetListOfKeys():
	h = h.ReadObj()
	if(h.ClassName() == "TCanvas"):
		continue
	plotHisto = True
	for i in range(len(histos1)):
		if(histos1[i].GetTitle() == h.GetTitle()):
			plotHisto = False
			continue
	if(not plotHisto): continue
	#if(h.GetFunction("fitfunc") is not None):
	#	h.GetListOfFunctions().Remove(h.GetFunction("fitfunc"))
	#if(h.GetFunction("fitfunc2") is not None):
	#	h.GetListOfFunctions().Remove(h.GetFunction("fitfunc2"))
	#if(h.GetFunction("fitfunc3") is not None):
	#	h.GetListOfFunctions().Remove(h.GetFunction("fitfunc3"))
	if(h.ClassName() == "TH1F" or h.ClassName() == "TH1D"):
		for f in h.GetListOfFunctions():
			h.GetListOfFunctions().Remove(h.GetFunction(f.GetName()))
		#h.GetFunction("fitfunc").SetLineColor(4)
		histos1.append(h)
infile2.cd()
histos2 = []
histos2_2D = []
for h in infile2.GetListOfKeys():
	h = h.ReadObj()
	if(h.ClassName() == "TCanvas"):
		continue
	plotHisto = True
	for i in range(len(histos2)):
		if(histos2[i].GetTitle() == h.GetTitle()):
			plotHisto = False
			continue
	for i in range(len(histos2_2D)):
		if(histos2_2D[i].GetTitle() == h.GetTitle()):
			plotHisto = False
			continue
	if(not plotHisto): continue
	#if(h.GetFunction("fitfunc") is not None):
	#	h.GetListOfFunctions().Remove(h.GetFunction("fitfunc"))
	#if(h.GetFunction("fitfunc2") is not None):
	#	h.GetListOfFunctions().Remove(h.GetFunction("fitfunc2"))
	#if(h.GetFunction("fitfunc3") is not None):
	#	h.GetListOfFunctions().Remove(h.GetFunction("fitfunc3"))
	if(h.ClassName() == "TH1F" or h.ClassName() == "TH1D"):
		for f in h.GetListOfFunctions():
			h.GetListOfFunctions().Remove(h.GetFunction(f.GetName()))
		histos2.append(h)
	if(h.ClassName() == "TH2F" or h.ClassName() == "TH2D"):
		histos2_2D.append(h)

openPDF(outfile,c)
for i in range(len(histos1)):
	savehisto(histos1[i],histos2[i],label1,label2,outfile,c,histos1[i].GetXaxis().GetTitle(),"",histos1[i].GetTitle())

infile1.cd()
graph1 = infile1.Get("mean")
graph1.GetListOfFunctions().Remove(graph1.GetFunction("pol5"))
infile2.cd()
graph2 = infile2.Get("mean")
graph2.GetListOfFunctions().Remove(graph2.GetFunction("pol5"))
savegraph(graph1,graph2,label1,label2,outfile,c,0,0.15,-5,-3.5,graph1.GetXaxis().GetTitle(),graph1.GetYaxis().GetTitle(),graph1.GetTitle())
del graph1
del graph2

infile1.cd()
graph1 = infile1.Get("sigma")
graph1.GetListOfFunctions().Remove(graph1.GetFunction("pol5"))
infile2.cd()
graph2 = infile2.Get("sigma")
graph2.GetListOfFunctions().Remove(graph2.GetFunction("pol5"))
savegraph(graph1,graph2,label1,label2,outfile,c,0,0.15,0,5,graph1.GetXaxis().GetTitle(),graph1.GetYaxis().GetTitle(),graph1.GetTitle())
del graph1
del graph2

infile1.cd()
graph1 = infile1.Get("breakz")
graph1.GetListOfFunctions().Remove(graph1.GetFunction("pol5"))
infile2.cd()
graph2 = infile2.Get("breakz")
graph2.GetListOfFunctions().Remove(graph2.GetFunction("pol5"))
savegraph(graph1,graph2,label1,label2,outfile,c,0,0.15,0,3,graph1.GetXaxis().GetTitle(),graph1.GetYaxis().GetTitle(),graph1.GetTitle())
del graph1
del graph2

infile1.cd()
graph1 = infile1.Get("zcut")
graph1.GetListOfFunctions().Remove(graph1.GetFunction("pol5"))
infile2.cd()
graph2 = infile2.Get("zcut")
graph2.GetListOfFunctions().Remove(graph2.GetFunction("pol5"))
savegraph(graph1,graph2,label1,label2,outfile,c,0,0.15,-4.3,40,graph1.GetXaxis().GetTitle(),graph1.GetYaxis().GetTitle(),graph1.GetTitle())
del graph1
del graph2

infile1.cd()
graph1 = infile1.Get("zcutscaled")
graph1.GetListOfFunctions().Remove(graph1.GetFunction("pol5"))
infile2.cd()
graph2 = infile2.Get("zcutscaled")
graph2.GetListOfFunctions().Remove(graph2.GetFunction("pol5"))
savegraph(graph1,graph2,label1,label2,outfile,c,0,0.15,-4.3,40,graph1.GetXaxis().GetTitle(),graph1.GetYaxis().GetTitle(),graph1.GetTitle())
del graph1
del graph2

infile1.cd()
graph1 = infile1.Get("zcut")
graph1.GetListOfFunctions().Remove(graph1.GetFunction("pol5"))
graph2 = infile1.Get("zcutscaled")
graph2.GetListOfFunctions().Remove(graph2.GetFunction("pol5"))
infile2.cd()
graph3 = infile2.Get("zcut")
graph3.GetListOfFunctions().Remove(graph3.GetFunction("pol5"))
savegraph3(graph1,graph2,graph3,"Data 10%","Data Scaled","MC",outfile,c,0,0.15,-4.3,40,graph1.GetXaxis().GetTitle(),graph1.GetYaxis().GetTitle(),graph1.GetTitle())
del graph1
del graph2
del graph3

infile1.cd()
graph1 = infile1.Get("zcut")
graph1.GetListOfFunctions().Remove(graph1.GetFunction("pol5"))
graph2 = infile1.Get("zcutscaled")
graph2.GetListOfFunctions().Remove(graph2.GetFunction("pol5"))
graph3 = infile1.Get("maxZ")
savegraph3(graph1,graph2,graph3,"Data 10%","Maximum Z","Data Scaled",outfile,c,0,0.15,-4.3,40,graph1.GetXaxis().GetTitle(),graph1.GetYaxis().GetTitle(),graph1.GetTitle())
del graph1
del graph2
del graph3

infile1.cd()
graph1 = infile1.Get("zcut")
graph1.GetListOfFunctions().Remove(graph1.GetFunction("pol5"))
graph2 = infile1.Get("zcut2")
graph2.GetListOfFunctions().Remove(graph2.GetFunction("pol5"))
graph3 = infile1.Get("zcut3")
graph3.GetListOfFunctions().Remove(graph3.GetFunction("pol5"))
savegraph3(graph1,graph2,graph3,"Data 10% Nominal","Data 10% -{0}#sigma".format(nsig),"Data 10% +{0}#sigma".format(nsig),outfile,c,0,0.15,-4.3,40,graph1.GetXaxis().GetTitle(),graph1.GetYaxis().GetTitle(),"Zcut Data 10% +/-{0}#sigma".format(nsig))
del graph1
del graph2
del graph3

infile2.cd()
graph1 = infile2.Get("zcut")
graph1.GetListOfFunctions().Remove(graph1.GetFunction("pol5"))
graph2 = infile2.Get("zcut2")
graph2.GetListOfFunctions().Remove(graph2.GetFunction("pol5"))
graph3 = infile2.Get("zcut3")
graph3.GetListOfFunctions().Remove(graph3.GetFunction("pol5"))
savegraph3(graph1,graph2,graph3,"MC 10% Nominal","MC 10% -{0}#sigma".format(nsig),"MC 10% +{0}#sigma".format(nsig),outfile,c,0,0.15,-4.3,40,graph1.GetXaxis().GetTitle(),graph1.GetYaxis().GetTitle(),"Zcut MC +/-{0}#sigma".format(nsig))
del graph1
del graph2
del graph3

infile1.cd()
graph1 = infile1.Get("zcutscaled")
graph1.GetListOfFunctions().Remove(graph1.GetFunction("pol5"))
graph2 = infile1.Get("zcutscaled2")
graph2.GetListOfFunctions().Remove(graph2.GetFunction("pol5"))
graph3 = infile1.Get("zcutscaled3")
graph3.GetListOfFunctions().Remove(graph3.GetFunction("pol5"))
savegraph3(graph1,graph2,graph3,"Data 10% Nominal","Data 10% -{0}#sigma".format(nsig),"Data 10% +{0}#sigma".format(nsig),outfile,c,0,0.15,-4.3,40,graph1.GetXaxis().GetTitle(),graph1.GetYaxis().GetTitle(),"Zcut Scaled Data 10% +/-{0}#sigma".format(nsig))
del graph1
del graph2
del graph3

closePDF(outfile,c)
outfileroot.Close()
