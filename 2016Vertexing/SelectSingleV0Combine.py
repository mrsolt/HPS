import sys
tmpargv = sys.argv
sys.argv = []
import getopt
#import utilities as utils
import ROOT
from ROOT import gROOT, TFile, gDirectory, gStyle, TCanvas, TH1, TLegend, TPad, TLatex
sys.argv = tmpargv

#List arguments
def print_usage():
	print "\nUsage: {0} <output file base name> <input file name>".format(sys.argv[0])
	print "Arguments: "
	print '\t-y: plot label'
	print '\t-h: this help message'
	print

Label = ""

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'y:h')

# Parse the command line arguments
for opt, arg in options:
		if opt=='-y':
			Label=str(arg)
		if opt=='-h':
			print_usage()
			sys.exit(0)

def saveCutFlow(histo,histo2,histo3,histo4,outfile,outfileroot,canvas,XaxisTitle="",YaxisTitle="",plotTitle="",stats=0):
	#outfileroot.cd()
	RatioMin = 0.2
	RatioMax = 2.2
	canvas.Clear()

	canvas.SetLogy(1)
	histo.SetLineColor(1)
	histo.Draw()
	histo.SetTitle(plotTitle)
	histo.GetXaxis().SetTitle(XaxisTitle)
	histo.GetYaxis().SetTitle(YaxisTitle)
	histo.SetStats(stats)
	histo2.SetLineColor(2)
	histo2.Draw("same")
	histo3.SetLineColor(4)
	#histo3.Draw("same")
	histo4.SetLineColor(6)
	#histo4.Draw("same")
	legend = TLegend(.08,.66,.42,.87)
	legend.SetBorderSize(0)
	legend.SetFillColor(0)
	legend.SetFillStyle(0)
	legend.SetTextFont(42)
	legend.SetTextSize(0.035)
	legend.AddEntry(histo,"Data Before Single V0","LP")
	legend.AddEntry(histo2,"Data After Single V0","LP")
	#legend.AddEntry(histo3,"MC Before Single V0","LP")
	#legend.AddEntry(histo4,"MC After Single V0","LP")
	legend.Draw("same")
	canvas.Print(outfile+".pdf")
	canvas.Write()
	#canvas.SetLogy(0)
	#canvas.Print(outfile+".pdf")
	#canvas.Write()
	canvas.Clear()

	top = TPad("top","top",0,0.42,1,1)
	top.SetLogy(1)

	bot = TPad("bot","bot",0,0,1,0.38)

	top.Draw()
	top.SetBottomMargin(0)
	#top.SetTopMargin(gStyle.GetPadTopMargin()*topScale)
	bot.Draw()
	bot.SetTopMargin(0)
	bot.SetBottomMargin(0.4)
	top.cd()

	canvas.SetLogy(1)
	histo4.SetTitle("Data/MC Comparison Final Selection")
	#histo4.GetXaxis().SetTitle(XaxisTitle)
	histo4.GetXaxis().SetTitle("dN/dz (mm^{-1} )")
	histo4.GetYaxis().SetTitle(YaxisTitle)
	#histo4.GetYaxis().SetLabelSize(0.06)
	histo4.GetXaxis().SetTitleOffset(0.7)
	histo4.GetXaxis().SetTitleSize(0.06)
	histo4.GetYaxis().SetLabelSize(0.08)
	histo2.SetLineColor(1)
	histo4.SetLineColor(2)
	histo2.Scale(1/histo2.Integral())
	histo4.Scale(1/histo4.Integral())
	histo4.Draw()
	histo2.Draw("same")
	legend2 = TLegend(.68,.66,.99,.87)
	legend2.SetBorderSize(0)
	legend2.SetFillColor(0)
	legend2.SetFillStyle(0)
	legend2.SetTextFont(42)
	legend2.SetTextSize(0.07)
	legend2.AddEntry(histo2,"Data","LP")
	legend2.AddEntry(histo4,"MC","LP")
	legend2.Draw()
	bot.cd()
	reference = histo4.Clone("reference")
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
	ratio = histo2.Clone("Ratio"+histo2.GetName())
	ratio.Divide(reference)
	ratio.DrawCopy("pe same")
	canvas.Print(outfile+".pdf")
	canvas.Write()
	#canvas.SetLogy(0)
	#canvas.Print(outfile+".pdf")
	#canvas.Write()

	canvas.Clear()

	top = TPad("top","top",0,0.42,1,1)
	top.SetLogy(1)

	bot = TPad("bot","bot",0,0,1,0.38)

	top.Draw()
	top.SetBottomMargin(0)
	#top.SetTopMargin(gStyle.GetPadTopMargin()*topScale)
	bot.Draw()
	bot.SetTopMargin(0)
	bot.SetBottomMargin(0.4)

	top.cd()

	canvas.SetLogy(1)
	histo.SetLineColor(1)
	histo3.SetLineColor(2)
	histo.Scale(1/histo.Integral())
	histo3.Scale(1/histo3.Integral())
	histo3.SetTitle("Data/MC Comparison Tight Cuts")
	histo3.GetXaxis().SetTitle(XaxisTitle)
	histo3.GetYaxis().SetTitle(YaxisTitle)
	histo.Scale(1/histo.Integral())
	histo3.Scale(1/histo3.Integral())
	histo3.Draw()
	histo.Draw("same")
	legend2.Draw()
	bot.cd()
	reference2 = histo3.Clone("reference")
	reference2.GetYaxis().SetTitle("Ratio")
	reference2.GetYaxis().SetTitleSize(0.06)
	reference2.GetYaxis().SetLabelSize(0.1)
	reference2.GetXaxis().SetTitleSize(0.1)
	reference2.GetXaxis().SetLabelSize(0.1)
	reference2.GetXaxis().SetTitle(XaxisTitle)
	reference2.GetYaxis().SetRangeUser(RatioMin,RatioMax)
	reference2.GetYaxis().SetNdivisions(508)
	reference2.GetYaxis().SetDecimals(True)
	reference2.Draw("axis")
	ratio2 = histo2.Clone("Ratio2"+histo.GetName())
	ratio2.Divide(reference)
	ratio2.DrawCopy("pe same")
	canvas.Print(outfile+".pdf")
	canvas.Write()
	#canvas.SetLogy(0)
	#canvas.Print(outfile+".pdf")
	#canvas.Write()



def openPDF(outfile,canvas):
	c.Print(outfile+".pdf[")

def closePDF(outfile,canvas):
	c.Print(outfile+".pdf]")

gStyle.SetOptStat(110011)
c = TCanvas("c","c",800,600)

plots = []
plots.append("uncVZ")
plots.append("uncM")

plotlabels = []
plotlabels.append("Reconstructed z [mm]")
plotlabels.append("Reconstructed Mass [GeV]")

outfile = remainder[0]
outfileroot = TFile(remainder[0]+".root","RECREATE")
infiledata = TFile(remainder[1])
infilemc = TFile(remainder[2])

openPDF(outfile,c)

c.SetLogy(0)

for i in range(len(plots)):
	plot = plots[i]
	plotlabel = plotlabels[i]
	infiledata.cd()
	histo_pre_data = infiledata.Get("{0} Before".format(plot))
	histo_post_data = infiledata.Get("{0} After".format(plot))
	infilemc.cd()
	histo_pre_mc = infilemc.Get("{0} Before".format(plot))
	histo_post_mc = infilemc.Get("{0} After".format(plot))
	outfileroot.cd()
	histo_pre_data.Write("{0} Before Data".format(plot))
	histo_post_data.Write("{0} After Data".format(plot))
	histo_pre_mc.Write("{0} Before MC".format(plot))
	histo_post_mc.Write("{0} After MC".format(plot))
	saveCutFlow(histo_pre_data,histo_post_data,histo_pre_mc,histo_post_mc,outfile,outfileroot,c,XaxisTitle=plotlabel,plotTitle="Remove Duplicates")

closePDF(outfile,c)
outfileroot.Close()
