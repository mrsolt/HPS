import sys
tmpargv = sys.argv
sys.argv = []
import numpy as np
import getopt
import ROOT
from ROOT import gROOT, TFile, TTree, TChain, gDirectory, TLine, gStyle, TCanvas, TLegend, TH1F, TF1, TLatex, TEllipse
sys.argv = tmpargv

#List arguments
def print_usage():
    print "\nUsage: {0} <output file base name> <input file> <label>".format(sys.argv[0])
    print '\t-z: target position (default -4.3 mm)'
    print '\t-j: uncVX mean (default 0)'
    print '\t-k: uncVX sigma (default 9999)'
    print '\t-m: uncVY mean (default 0)'
    print '\t-n: uncVY sigma (default 9999)'
    print '\t-o: uncTargProjX mean (default 0)'
    print '\t-p: uncTargProjX sigma (default 9999)'
    print '\t-a: uncTargProjY mean (default 0)'
    print '\t-b: uncTargProjY sigma (default 9999)'
    print '\t-d: is data (default false)'
    print '\t-c: is MC (default false)'
    print '\t-h: this help message'
    print

zTarg = -4.3
uncVX = 0.
uncVXSig = 9999.
uncVY = 0.
uncVYSig = 9999.
uncTargProjX = 0.
uncTargProjXSig = 9999.
uncTargProjY = 0.
uncTargProjYSig = 9999.
isData = False
isMC = False

angleMC = 0.111025680707
angleData = 0.0386557750132

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'z:j:k:m:n:o:p:a:b:dch')

# Parse the command line arguments
for opt, arg in options:
		if opt=='-z':
			zTarg = float(arg)
		if opt=='-j':
			uncVX=float(arg)
		if opt=='-k':
			uncVXSig=float(arg)
		if opt=='-m':
			uncVY=float(arg)
		if opt=='-n':
			uncVYSig=float(arg)
		if opt=='-o':
			uncTargProjX=float(arg)
		if opt=='-p':
			uncTargProjXSig=float(arg)
		if opt=='-a':
			uncTargProjY=float(arg)
		if opt=='-b':
			uncTargProjYSig=float(arg)
		if opt=='-d':
			isData = True
		if opt=='-c':
			isMC = True
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

xProj = "(uncVX-(uncVZ-{0})*uncPX/uncPZ)".format(zTarg)
yProj = "(uncVY-(uncVZ-{0})*uncPY/uncPZ)".format(zTarg)

events.Draw("uncVY:uncVX>>V0_pos(100,-1.5,1.5,100,-1,1)")
#events.Draw("uncTargProjY:uncTargProjX>>V0_proj(100,-1.5,1.5,100,-1,1)")
events.Draw("{1}:{0}>>V0_proj(100,-1.5,1.5,100,-1,1)".format(xProj,yProj))

events.Draw("(uncVY-{2})/{3}:(uncVX-{0})/{1}>>V0_pos_sig(100,-4,4,100,-4,4)".format(uncVX,uncVXSig,uncVY,uncVYSig))

V0_pos = gDirectory.FindObject("V0_pos")
V0_proj = gDirectory.FindObject("V0_proj")
V0_pos_sig = gDirectory.FindObject("V0_pos_sig")

V0_proj.Fit("pol1","pol1","",-0.5,0.5)
fit = V0_proj.GetFunction("pol1")
angle = np.arctan(fit.GetParameter(1))
print("Angle = {0} rad".format(angle))
if(isData):
	angle = angleData
if(isMC):
	angle = angleMC
print("Angle = {0} rad".format(angle))
xProj_rot = "{0}*cos({2})-{1}*sin({2})".format(xProj,yProj,-angle)
yProj_rot = "{0}*sin({2})+{1}*cos({2})".format(xProj,yProj,-angle)

events.Draw("{1}:{0}>>V0_proj_rot(100,-1.5,1.5,100,-1,1)".format(xProj_rot,yProj_rot))
V0_proj_rot = gDirectory.FindObject("V0_proj_rot")

openPDF(outfile,c)

outfileroot.cd()
c.SetLogz(1)

V0_pos.GetXaxis().SetTitle("x (mm)")
V0_pos.GetYaxis().SetTitle("y (mm)")
V0_pos.SetTitle("V0 Position {0}".format(label))
V0_pos.Draw("COLZ")
c.Print(outfile+".pdf")
c.Write()

V0_proj.GetXaxis().SetTitle("x (mm)")
V0_proj.GetYaxis().SetTitle("y (mm)")
V0_proj.SetTitle("V0 Projection To Target {0}".format(label))
V0_proj.Draw("COLZ")
V0_proj.Fit("pol1")
c.Print(outfile+".pdf")
c.Write()

V0_proj_rot.GetXaxis().SetTitle("x (mm)")
V0_proj_rot.GetYaxis().SetTitle("y (mm)")
V0_proj_rot.SetTitle("Rotated V0 Projection To Target {0}".format(label))
V0_proj_rot.Draw("COLZ")
c.Print(outfile+".pdf")
c.Write()

V0_pos_sig.GetXaxis().SetTitle("x-#mu_{x}/#sigma_{x}")
V0_pos_sig.GetYaxis().SetTitle("y-#mu_{x}/#sigma_{y}")
V0_pos_sig.SetTitle("V0 Position N#sigma {0}".format(label))
V0_pos_sig.Draw("COLZ")
c.Print(outfile+".pdf")
c.Write()

events.Draw("({5}-{2})/{3}:({4}-{0})/{1}>>V0_proj_sig(100,-4,4,100,-4,4)".format(uncTargProjX,uncTargProjXSig,uncTargProjY,uncTargProjYSig,xProj_rot,yProj_rot))
V0_proj_sig = gDirectory.FindObject("V0_proj_sig")
V0_proj_sig.GetXaxis().SetTitle("x-#mu_{x}/#sigma_{x}")
V0_proj_sig.GetYaxis().SetTitle("y-#mu_{y}/#sigma_{y}")
V0_proj_sig.SetTitle("Rotated V0 Projection To Target N#sigma {0}".format(label))
V0_proj_sig.Draw("COLZ")
ell = TEllipse(0, 0, 2, 2,0,360,0)
ell.SetLineColor(2)
ell.SetLineWidth(3)
ell.SetFillColorAlpha(0,0)
ell.SetFillStyle(4000)
ell.Draw("same")
c.Print(outfile+".pdf")
c.Write()
V0_proj_sig.Write("V0_proj_sig")


closePDF(outfile,c)
outfileroot.Close()