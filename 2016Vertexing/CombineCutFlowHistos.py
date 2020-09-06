import sys
tmpargv = sys.argv
sys.argv = []
import getopt
#import utilities as utils
import ROOT
from ROOT import gROOT, TFile, gDirectory, gStyle, TCanvas, TH1, TLegend, TLatex, TPad
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

def openPDF(outfile,canvas):
	c.Print(outfile+".pdf[")

def closePDF(outfile,canvas):
	c.Print(outfile+".pdf]")

def saveCutFlow(histos,histos2,histos3,histos4,outfile,canvas,inHisto,labels,XaxisTitle="",YaxisTitle="",plotTitle="",stats=0,logY=0):
	RatioMin = 0.
	RatioMax = 1.
	outfileroot.cd()
	canvas.Clear()
	histos[0].SetTitle(plotTitle + " Inclusive")
	histos[0].GetXaxis().SetTitle(XaxisTitle)
	histos[0].GetYaxis().SetTitle(YaxisTitle)
	histos[0].GetXaxis().SetLabelSize(0.05)
	histos[0].GetYaxis().SetLabelSize(0.05)
	histos[0].GetZaxis().SetLabelSize(0.03)
	histos[0].GetXaxis().SetTitleOffset(0.8)
	histos[0].GetXaxis().SetTitleSize(0.06)
	histos[0].GetYaxis().SetTitleOffset(0.8)
	histos[0].GetYaxis().SetTitleSize(0.06)
	histos[0].SetStats(stats)
	color = 1
	if(inHisto == "uncVZ"):
		for i in range(len(histos4)):
			canvas.SetLogy(0)
			histos4[i].Draw("COLZ")
			histos4[i].SetTitle("Vz vs Mass " + labels[i] + " Exclusive")
			histos4[i].GetXaxis().SetTitle("Mass [GeV]")
			histos4[i].GetYaxis().SetTitle("Reconstructed z [mm]")
			histos4[i].GetXaxis().SetLabelSize(0.05)
			histos4[i].GetYaxis().SetLabelSize(0.05)
			histos4[i].GetZaxis().SetLabelSize(0.03)
			histos4[i].GetXaxis().SetTitleOffset(0.8)
			histos4[i].GetXaxis().SetTitleSize(0.06)
			histos4[i].GetYaxis().SetTitleOffset(0.8)
			histos4[i].GetYaxis().SetTitleSize(0.06)
			histos4[i].SetStats(stats)
			canvas.Print(outfile+".pdf")
			canvas.Write()
			histos4[i].Write("Vz vs Mass " + labels[i] + " Exclusive")
			canvas.SetLogy(logY)

	for i in range(len(histos)):
		if(color == 5 or color == 10):
			color = color + 1
		histos[i].SetLineColor(color)
		color = color + 1
		if(i == 0):
			histos[i].GetYaxis().SetTitle("dN/dz (mm^{-1} )")
			histos[i].Draw("")
		elif(i == 3):
			continue
		else:
			histos[i].Draw("same")
		histos[i].Write(labels[i]+" "+inHisto)
	legend = TLegend(.10,.46,.44,.87)
	if(inHisto == "uncM"):
		legend = TLegend(.58,.46,.92,.87)
	legend.SetBorderSize(0)
	legend.SetFillColor(0)
	legend.SetFillStyle(0)
	legend.SetTextFont(42)
	legend.SetTextSize(0.035)
	for i in range(len(labels)):
		if(i == 3):
			continue
		legend.AddEntry(histos[i],labels[i],"LP")
	legend.Draw("")
	canvas.SetLogy(logY)
	canvas.Print(outfile+".pdf")
	canvas.Write()
	canvas.SetLogy(0)
	canvas.Print(outfile+".pdf")
	canvas.Write()
	canvas.SetLogy(logY)
	for i in range(len(histos2)):
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

		histos[0].SetLineColor(1)
		histos[0].Draw()
		histos[0].SetTitle(plotTitle + " " + labels[i] + " Exclusive")
		histos[0].GetXaxis().SetTitle(XaxisTitle)
		histos[0].GetYaxis().SetTitle(YaxisTitle)
		if(inHisto == "uncVZ"):
			histos[0].GetYaxis().SetTitle("dN/dz (mm^{-1} )")
		histos[0].SetStats(stats)
		histos2[i].SetLineColor(2)
		histos2[i].Draw("same")
		histos3[i].SetLineColor(4)
		histos3[i].Draw("same")
		legend3 = TLegend(.10,.66,.44,.87)
		if(inHisto == "uncM"):
			legend3 = TLegend(.58,.66,.92,.87)
		legend3.SetBorderSize(0)
		legend3.SetFillColor(0)
		legend3.SetFillStyle(0)
		legend3.SetTextFont(42)
		legend3.SetTextSize(0.05)
		legend3.AddEntry(histos[0],labels[0],"LP")
		legend3.AddEntry(histos2[i],"Without " + labels[i],"LP")
		legend3.AddEntry(histos3[i],"With " + labels[i],"LP")
		legend3.Draw("same")

		bot.cd()
		#reference = histos[0].Clone("reference")
		reference = histos2[i].Clone("reference")
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
		#ratio = histos[0].Clone("Ratio"+histos[0].GetName())
		ratio = histos3[i].Clone("Ratio"+histos3[i].GetName())
		ratio.Divide(reference)
		ratio.SetLineColor(1)
		ratio.DrawCopy("pe same")
		#ratio.DrawCopy("hist p same")
		#ratio2 = histos2[i].Clone("Ratio"+histos2[i].GetName())
		#ratio2.Divide(reference)
		#ratio2.SetLineColor(2)
		#ratio2.DrawCopy("pe same")
		#ratio3 = histos3[i].Clone("Ratio"+histos3[i].GetName())
		#ratio3.Divide(reference)
		#ratio3.SetLineColor(4)
		#ratio3.DrawCopy("pe same")
		#legend.Draw()

		canvas.Print(outfile+".pdf")
		canvas.Write()
		top.cd()
		top.SetLogy(0)
		canvas.Print(outfile+".pdf")
		canvas.Write()
		canvas.SetLogy(logY)
		histos2[i].Write("Without " + labels[i]+" "+inHisto)
		histos3[i].Write("With " + labels[i]+" "+inHisto)

	canvas.Clear()
	histos2[0].SetTitle(plotTitle + " Exclusive")
	histos2[0].GetXaxis().SetTitle(XaxisTitle)
	histos2[0].GetYaxis().SetTitle(YaxisTitle)
	histos2[0].SetStats(stats)
	color = 1
	for i in range(len(histos2)):
		if(color == 5 or color == 10):
			color = color + 1
		histos2[i].SetLineColor(color)
		color = color + 1
		if(i == 0):
			histos2[i].Draw("")
			maximum = histos2[0].GetMaximum()
		else:
			histos2[i].Draw("same")
			if(histos2[i].GetMaximum() > maximum):
				maximum = histos2[i].GetMaximum()
	histos2[0].GetYaxis().SetRangeUser(0.1,1.2*maximum)
	legend2 = TLegend(.08,.46,.42,.87)
	if(inHisto == "uncM"):
		legend2 = TLegend(.58,.46,.92,.87)
	legend2.SetBorderSize(0)
	legend2.SetFillColor(0)
	legend2.SetFillStyle(0)
	legend2.SetTextFont(42)
	legend2.SetTextSize(0.035)
	for i in range(len(labels)):
		legend2.AddEntry(histos2[i],labels[i],"LP")
	legend2.Draw("")
	canvas.SetLogy(logY)
	canvas.Print(outfile+".pdf")
	canvas.Write()
	canvas.SetLogy(0)
	canvas.Print(outfile+".pdf")
	canvas.Write()
	canvas.SetLogy(logY)

def saveCuts(histos5,outfile,canvas,label,index,XaxisTitle,logY=1):
	outfileroot.cd()
	canvas.Clear()
	for i in range(len(histos5)):
		canvas.SetLogy(logY)
		histos5[i].Draw()
		histos5[i].SetTitle(label[index[i]] + " Exclusive")
		histos5[i].GetXaxis().SetTitle(XaxisTitle[i])
		canvas.Print(outfile+".pdf")
		canvas.Write()
		histos5[i].Write(XaxisTitle[i] + " Exclusive")

gStyle.SetOptStat(110011)
c = TCanvas("c","c",800,600)

label = []
label.append("Preselection")
label.append("e+e- Layer Requirement")
label.append("V0 Projection 2#sigma")
label.append("Unconstrained Vertex #chi^{2} < 4")
label.append("V0 momentum > 1.85 GeV")
label.append("Isolation Cut")
label.append("Impact Parameter Cuts")

plots = []
plots.append("uncVZ")
plots.append("uncM")
plots.append("uncP")

plotlabels = []
plotlabels.append("Reconstructed z [mm]")
plotlabels.append("Reconstructed Mass [GeV]")
plotlabels.append("V0 Momentum [GeV]")

setlog = []
setlog.append(1)
setlog.append(1)
setlog.append(0)

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
infiles = []
for i in range(1,len(remainder)):
	infiles.append(TFile(remainder[i]))

openPDF(outfile,c)

histo_2D = infiles[0].Get("histo_2D")

for i in range(1,len(infiles)):
	file = infiles[i]
	file.cd()
	histo_2D.Add(file.Get("histo_2D"))

c.SetLogz(1)
c.SetLogy(0)
outfileroot.cd()
histo_2D.Draw("COLZ")
histo_2D.SetTitle("Vz vs Mass All Cuts")
histo_2D.GetXaxis().SetTitle("Mass [GeV]")
histo_2D.GetYaxis().SetTitle("Reconstructed z [mm]")
histo_2D.GetXaxis().SetLabelSize(0.05)
histo_2D.GetYaxis().SetLabelSize(0.05)
histo_2D.GetZaxis().SetLabelSize(0.03)
histo_2D.GetXaxis().SetTitleOffset(0.8)
histo_2D.GetXaxis().SetTitleSize(0.06)
histo_2D.GetYaxis().SetTitleOffset(0.8)
histo_2D.GetYaxis().SetTitleSize(0.06)
histo_2D.SetStats(0)
c.Print(outfile+".pdf")
c.Write()

for k in range(len(plots)):
	plot = plots[k]
	plotlabel = plotlabels[k]
	histos = []
	histos2 = []
	histos3 = []
	histos4 = []
	for i in infiles[0].GetListOfKeys():
		infiles[0].cd()
		h = i.ReadObj()
		if((h.ClassName() != "TH1F") and (h.ClassName() != "TH1D") and (h.ClassName() != "TH2F") and (h.ClassName() != "TH2D")):
			continue
		if(not(plot in h.GetName())):
			continue
		for j in range(1,len(infiles)):
			infiles[j].cd()
			if(infiles[j].Get(h.GetName()) == None):
				print h.GetName()
				continue
			h.Add(infiles[j].Get(h.GetName()))
		if("histos" in h.GetName()):
			histos.append(h)
		elif("histo2" in h.GetName()):
			histos2.append(h)
		elif("histo3" in h.GetName()):
			histos3.append(h)
		elif("histo4" in h.GetName()):
			histos4.append(h)

	saveCutFlow(histos,histos2,histos3,histos4,outfile,c,plot,label,XaxisTitle=plotlabel,YaxisTitle="",plotTitle=plotlabel+ " {0}".format(Label),stats=0,logY=setlog[k])
	del histos
	del histos2
	del histos3
	del histos4

histos5 = []
for i in infiles[0].GetListOfKeys():
	infiles[0].cd()
	h = i.ReadObj()
	if((h.ClassName() != "TH1F") and (h.ClassName() != "TH1D") and (h.ClassName() != "TH2F") and (h.ClassName() != "TH2D")):
		continue
	if(not ("histo5" in h.GetName())):
		continue
	for j in range(1,len(infiles)):
		infiles[j].cd()
		if(infiles[j].Get(h.GetName()) == None):
			print h.GetName()
			continue
		h.Add(infiles[j].Get(h.GetName()))
	histos5.append(h)
saveCuts(histos5,outfile,c,label,index,xlabel)
del histos5

histo_cutflow = infiles[0].Get("histo_cutflow")

for i in range(1,len(infiles)):
	file = infiles[i]
	file.cd()
	histo_cutflow.Add(file.Get("histo_cutflow"))

histo_cutflow.Draw()
histo_cutflow.SetTitle("Cut Flow")
histo_cutflow.GetXaxis().SetTitle("Cut")
c.Print(outfile+".pdf")
outfileroot.cd()
histo_cutflow.Write("histo_cutflow")

closePDF(outfile,c)
outfileroot.Close()
