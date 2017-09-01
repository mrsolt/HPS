#!/usr/bin/env python
import sys
tmpargv = sys.argv
sys.argv = []
import getopt
import ROOT
from ROOT import gROOT, TFile, TTree, TChain, gDirectory, TLine, gStyle, TCanvas, TLegend
sys.argv = tmpargv

def print_usage():
    print "\nUsage: {0} <output pdf file base name> <input root file>".format(sys.argv[0])
    print "Arguments: "
    print '\t-h: this help message'
    print

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'h')

# Parse the command line arguments
for opt, arg in options:
        if opt=='-h':
            print_usage()
            sys.exit(0)

gStyle.SetOptStat(0)
c = TCanvas("c","c",800,600)

outfile = remainder[0]
tupleFile = TFile(remainder[1])

eleBeamEvents = tupleFile.Get("eleBeamNtuple")
ApEvents = tupleFile.Get("ApNtuple")
RhoEvents = tupleFile.Get("RhoNtuple")
eleRecoilEvents = tupleFile.Get("eleRecoilNtuple")
WRecoilEvents = tupleFile.Get("WRecoilNtuple")
posDecayEvents = tupleFile.Get("posDecayNtuple")
eleDecayEvents = tupleFile.Get("eleDecayNtuple")
PionEvents = tupleFile.Get("PionNtuple")

eleBeamEvents.Draw("E>>beamE(10000,0,10)")
beamE = ROOT.gROOT.FindObject("beamE")
ebeam = beamE.GetMean()

c.Print("Ap_"+outfile+".pdf[")

ApEvents.Draw("E>>(50,0,{0})".format(ebeam))
c.Print("Ap_"+outfile+".pdf")
ApEvents.Draw("Px>>(50,0,{0})".format(ebeam))
c.Print("Ap_"+outfile+".pdf")
ApEvents.Draw("Py>>(50,0,{0})".format(ebeam))
c.Print("Ap_"+outfile+".pdf")
ApEvents.Draw("Pz>>(50,0,{0})".format(ebeam))
c.Print("Ap_"+outfile+".pdf")
ApEvents.Draw("m>>(50,0,{0})".format(ebeam))
c.Print("Ap_"+outfile+".pdf")

c.Print("Ap_"+outfile+".pdf]")

c.Print("Rho_"+outfile+".pdf[")

RhoEvents.Draw("E>>(50,0,{0})".format(ebeam))
c.Print("Rho_"+outfile+".pdf")
RhoEvents.Draw("Px>>(50,0,{0})".format(ebeam))
c.Print("Rho_"+outfile+".pdf")
RhoEvents.Draw("Py>>(50,0,{0})".format(ebeam))
c.Print("Rho_"+outfile+".pdf")
RhoEvents.Draw("Pz>>(50,0,{0})".format(ebeam))
c.Print("Rho_"+outfile+".pdf")
RhoEvents.Draw("m>>(50,0,{0})".format(ebeam))
c.Print("Rho_"+outfile+".pdf")

c.Print("Rho_"+outfile+".pdf]")

c.Print("eleRecoil_"+outfile+".pdf[")

eleRecoilEvents.Draw("E>>(50,0,{0})".format(ebeam))
c.Print("eleRecoil_"+outfile+".pdf")
eleRecoilEvents.Draw("Px>>(50,0,{0})".format(ebeam))
c.Print("eleRecoil_"+outfile+".pdf")
eleRecoilEvents.Draw("Py>>(50,0,{0})".format(ebeam))
c.Print("eleRecoil_"+outfile+".pdf")
eleRecoilEvents.Draw("Pz>>(50,0,{0})".format(ebeam))
c.Print("eleRecoil_"+outfile+".pdf")
eleRecoilEvents.Draw("m>>(50,0,{0})".format(ebeam))
c.Print("eleRecoil_"+outfile+".pdf")

c.Print("eleRecoil_"+outfile+".pdf]")

c.Print("posDecay_"+outfile+".pdf[")

posDecayEvents.Draw("E>>(50,0,{0})".format(ebeam))
c.Print("posDecay_"+outfile+".pdf")
posDecayEvents.Draw("Px>>(50,0,{0})".format(ebeam))
c.Print("posDecay_"+outfile+".pdf")
posDecayEvents.Draw("Py>>(50,0,{0})".format(ebeam))
c.Print("posDecay_"+outfile+".pdf")
posDecayEvents.Draw("Pz>>(50,0,{0})".format(ebeam))
c.Print("posDecay_"+outfile+".pdf")
posDecayEvents.Draw("m>>(50,0,{0})".format(ebeam))
c.Print("posDecay_"+outfile+".pdf")

c.Print("posDecay_"+outfile+".pdf]")

c.Print("eleDecay_"+outfile+".pdf[")

eleDecayEvents.Draw("E>>(50,0,{0})".format(ebeam))
c.Print("eleDecay_"+outfile+".pdf")
eleDecayEvents.Draw("Px>>(50,0,{0})".format(ebeam))
c.Print("eleDecay_"+outfile+".pdf")
eleDecayEvents.Draw("Py>>(50,0,{0})".format(ebeam))
c.Print("eleDecay_"+outfile+".pdf")
eleDecayEvents.Draw("Pz>>(50,0,{0})".format(ebeam))
c.Print("eleDecay_"+outfile+".pdf")
eleDecayEvents.Draw("m>>(50,0,{0})".format(ebeam))
c.Print("eleDecay_"+outfile+".pdf")

c.Print("eleDecay_"+outfile+".pdf]")

c.Print("Pion_"+outfile+".pdf[")

PionEvents.Draw("E>>(50,0,{0})".format(ebeam))
c.Print("Pion_"+outfile+".pdf")
PionEvents.Draw("Px>>(50,0,{0})".format(ebeam))
c.Print("Pion_"+outfile+".pdf")
PionEvents.Draw("Py>>(50,0,{0})".format(ebeam))
c.Print("Pion_"+outfile+".pdf")
PionEvents.Draw("Pz>>(50,0,{0})".format(ebeam))
c.Print("Pion_"+outfile+".pdf")
PionEvents.Draw("m>>(50,0,{0})".format(ebeam))
c.Print("Pion_"+outfile+".pdf")

c.Print("Pion_"+outfile+".pdf]")
