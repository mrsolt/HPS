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

def saveCutFlow(histo,histo2,histo3,histo4,histo5,histo6,label,outfile,outfileroot,canvas,XaxisTitle="",YaxisTitle="",plotTitle="",stats=0):
	#outfileroot.cd()
	canvas.Clear()
	RatioMin = 0.2
	RatioMax = 2.2

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
	histo3.Draw("same")
	histo4.SetLineColor(6)
	histo4.Draw("same")
	histo5.SetLineColor(7)
	histo5.Draw("same")
	histo6.SetLineColor(8)
	histo6.Draw("same")
	legend = TLegend(.08,.66,.42,.87)
	legend.SetBorderSize(0)
	legend.SetFillColor(0)
	legend.SetFillStyle(0)
	legend.SetTextFont(42)
	legend.SetTextSize(0.035)
	legend.AddEntry(histo,"Data Preselection","LP")
	legend.AddEntry(histo2,"Data W/O {0}".format(label),"LP")
	legend.AddEntry(histo3,"Data Tight Cuts","LP")
	legend.AddEntry(histo4,"MC Preselection","LP")
	legend.AddEntry(histo5,"MC W/O {0}".format(label),"LP")
	legend.AddEntry(histo6,"MC Tight Cuts","LP")
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

	if(label == "Preselection"):
		histo5.SetTitle("Data/MC Compare {0}".format(label))
		histo5.GetYaxis().SetTitle("dN/dz (mm^{-1} )")
	else:
		histo5.SetTitle("Data/MC Compare Without {0}".format(label))
		histo5.GetYaxis().SetTitle(YaxisTitle)
	histo5.GetXaxis().SetTitle(XaxisTitle)
	histo5.GetXaxis().SetLabelSize(0.05)
	histo5.GetYaxis().SetLabelSize(0.05)
	#histo5.GetZaxis().SetLabelSize(0.05)
	histo5.GetXaxis().SetTitleOffset(0.8)
	histo5.GetXaxis().SetTitleSize(0.06)
	histo5.GetYaxis().SetTitleOffset(0.8)
	histo5.GetYaxis().SetTitleSize(0.06)
	histo2.Scale(1./histo2.Integral())
	histo5.Scale(1./histo5.Integral())
	histo2.SetLineColor(1)
	histo5.SetLineColor(2)
	histo5.Draw()
	histo2.Draw("same")
	legend2 = TLegend(.68,.66,.99,.87)
	legend2.SetBorderSize(0)
	legend2.SetFillColor(0)
	legend2.SetFillStyle(0)
	legend2.SetTextFont(42)
	legend2.SetTextSize(0.05)
	legend2.AddEntry(histo2,"Data","LP")
	legend2.AddEntry(histo5,"MC","LP")
	legend2.Draw("same")
	bot.cd()
	reference = histo5.Clone("reference")
	reference.GetYaxis().SetTitle("Ratio")
	reference.GetYaxis().SetTitleSize(0.06)
	reference.GetYaxis().SetLabelSize(0.1)
	reference.GetXaxis().SetTitleSize(0.1)
	reference.GetXaxis().SetLabelSize(0.1)
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

def saveCuts(histo,histo2,outfile,outfileroot,canvas,XaxisTitle="",plotTitle="",stats=0):
	#outfileroot.cd()
	canvas.Clear()
	RatioMin = 0.2
	RatioMax = 2.2

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

	histo.SetTitle(plotTitle)
	histo.GetXaxis().SetTitle(XaxisTitle)
	histo.GetXaxis().SetLabelSize(0.05)
	histo.GetYaxis().SetLabelSize(0.05)
	#histo.GetZaxis().SetLabelSize(0.05)
	histo.GetXaxis().SetTitleOffset(0.8)
	histo.GetXaxis().SetTitleSize(0.06)
	histo.GetYaxis().SetTitleOffset(0.8)
	histo.GetYaxis().SetTitleSize(0.06)
	histo2.Scale(1./histo2.Integral())
	histo.Scale(1./histo.Integral())
	histo.SetLineColor(1)
	histo2.SetLineColor(2)
	histo2.Draw()
	histo.Draw("same")
	legend = TLegend(.68,.66,.99,.87)
	legend.SetBorderSize(0)
	legend.SetFillColor(0)
	legend.SetFillStyle(0)
	legend.SetTextFont(42)
	legend.SetTextSize(0.05)
	legend.AddEntry(histo,"Data","LP")
	legend.AddEntry(histo2,"MC","LP")
	legend.Draw("same")
	bot.cd()
	reference = histo2.Clone("reference")
	reference.GetYaxis().SetTitle("Ratio")
	reference.GetYaxis().SetTitleSize(0.06)
	reference.GetYaxis().SetLabelSize(0.1)
	reference.GetXaxis().SetTitleSize(0.1)
	reference.GetXaxis().SetLabelSize(0.1)
	reference.GetXaxis().SetTitle(XaxisTitle)
	reference.GetYaxis().SetRangeUser(RatioMin,RatioMax)
	reference.GetYaxis().SetNdivisions(508)
	reference.GetYaxis().SetDecimals(True)
	reference.Draw("axis")
	ratio = histo.Clone("Ratio"+histo.GetName())
	ratio.Divide(reference)
	ratio.DrawCopy("pe same")
	canvas.Print(outfile+".pdf")
	canvas.Write()

def openPDF(outfile,canvas):
	c.Print(outfile+".pdf[")

def closePDF(outfile,canvas):
	c.Print(outfile+".pdf]")

gStyle.SetOptStat(110011)
c = TCanvas("c","c",800,600)

labels = []
labels.append("Preselection")
labels.append("e+e- Layer Requirement")
labels.append("V0 Projection 2#sigma")
labels.append("Unconstrained Vertex #chi^{2} < 4")
labels.append("V0 momentum > 1.85 GeV")
labels.append("Isolation Cut")
labels.append("Impact Parameter Cuts")

plots = []
plots.append("uncVZ")
plots.append("uncM")
plots.append("uncP")

plotlabels = []
plotlabels.append("Reconstructed z [mm]")
plotlabels.append("Reconstructed Mass [GeV]")
plotlabels.append("V0 Momentum [GeV]")

xlabel = []
xlabel.append("Passes Layer Requirement")
xlabel.append("V0 Projection to Target N#sigma")
xlabel.append("Unconstrainced #chi^{2}")
xlabel.append("V0 Momentum (GeV)")
xlabel.append("Electron Isolation Cut Value (mm)")
xlabel.append("Positron Isolation Cut Value (mm)")
xlabel.append("Electron Track Z0 (mm)")
xlabel.append("Positron Track Z0 (mm)")

index = []
index.append(1)
index.append(2)
index.append(3)
index.append(4)
index.append(5)
index.append(5)
index.append(6)
index.append(6)

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
	histo_pre_data = infiledata.Get("Preselection {0}".format(plot))
	histo_tight_data = infiledata.Get("With V0 momentum > 1.85 GeV {0}".format(plot))
	infilemc.cd()
	histo_pre_mc = infilemc.Get("Preselection {0}".format(plot))
	histo_tight_mc = infilemc.Get("With V0 momentum > 1.85 GeV {0}".format(plot))
	outfileroot.cd()
	histo_pre_data.Write("Preselection {0} Data".format(plot))
	histo_tight_data.Write("Tight {0} Data".format(plot))
	histo_pre_mc.Write("Preselection {0} MC".format(plot))
	histo_tight_mc.Write("Tight {0} MC".format(plot))
	for j in range(len(labels)):
		label = labels[j]
		title = "Without {0} {1}".format(label,plot)
		infiledata.cd()
		histo_n1_data = infiledata.Get(title)
		infilemc.cd()
		histo_n1_mc = infilemc.Get(title)
		outfileroot.cd()
		histo_n1_data.Write(title+" Data")
		histo_n1_mc.Write(title+" MC")
		saveCutFlow(histo_pre_data,histo_n1_data,histo_tight_data,histo_pre_mc,histo_n1_mc,histo_tight_mc,label,outfile,outfileroot,c,XaxisTitle=plotlabel,plotTitle="Data/MC Compare {0}".format(label))

for i in range(len(xlabel)):
	infiledata.cd()
	histo_data = infiledata.Get("{0} Exclusive".format(xlabel[i]))
	infilemc.cd()
	histo_mc = infilemc.Get("{0} Exclusive".format(xlabel[i]))
	outfileroot.cd()
	histo_data.Write("{0} Exclusive".format(xlabel[i]))
	histo_mc.Write("{0} Exclusive".format(xlabel[i]))
	saveCuts(histo_data,histo_mc,outfile,outfileroot,c,XaxisTitle=xlabel[i],plotTitle="Data/MC Compare Without {0}".format(labels[index[i]]))

infiledata.cd()
histo_cutflow_data = infiledata.Get("histo_cutflow")
infilemc.cd()
histo_cutflow_mc = infilemc.Get("histo_cutflow")

c.Clear()
histo_cutflow_data.Scale(1./histo_cutflow_data.Integral())
histo_cutflow_mc.Scale(1./histo_cutflow_mc.Integral())
histo_cutflow_data.Draw()
histo_cutflow_data.SetTitle("Cut Flow")
histo_cutflow_data.GetXaxis().SetTitle("Cut")
histo_cutflow_mc.SetLineColor(2)
histo_cutflow_mc.Draw("same")
legend = TLegend(.68,.66,.99,.87)
legend.SetBorderSize(0)
legend.SetFillColor(0)
legend.SetFillStyle(0)
legend.SetTextFont(42)
legend.SetTextSize(0.07)
legend.AddEntry(histo_cutflow_data,"Data","LP")
legend.AddEntry(histo_cutflow_mc,"MC","LP")
legend.Draw()
c.Print(outfile+".pdf")
outfileroot.cd()
c.Write()
histo_cutflow_data.Write("histo_cutflow_data")
histo_cutflow_mc.Write("histo_cutflow_mc")

closePDF(outfile,c)
outfileroot.Close()
