import sys
tmpargv = sys.argv
sys.argv = []
import getopt
from array import array
import ROOT
from ROOT import TFile, TChain
sys.argv = tmpargv
import csv
import numpy as np

#List arguments
def print_usage():
    print "\nUsage: {0} <output file base name> <input file name 0> <input file name 1> ".format(sys.argv[0])
    print "Arguments: "
    print '\t-f: use full truth info'
    print '\t-s: is signal MC'
    print '\t-x: x position of beam'
    print '\t-y: y position of beam'
    print '\t-z: target position in z'
    print '\t-h: this help message'
    print

xBeam = -0.224
yBeam = -0.08
zTarg = -4.3

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'x:y:z:h')

# Parse the command line arguments
for opt, arg in options:
		if opt=='-x':
			xBeam = float(arg)
		if opt=='-y':
			yBeam = float(arg)
		if opt=='-z':
			zTarg = float(arg)
		if opt=='-h':
			print_usage()
			sys.exit(0)

outfile = remainder[0]
file0 = TFile(remainder[1])
file1 = TFile(remainder[2])
events0 = file0.Get("ntuple")
events1 = file1.Get("tree")

uncVY = array('d',[0])
uncVZ = array('d',[0])
uncM = array('d',[0])
uncTargProjY = array('d',[0])
uncCovYY = array('d',[0])
uncCovZZ = array('d',[0])
eleTrkLambda = array('d',[0])
eleTrkZ0 = array('d',[0])
posTrkLambda = array('d',[0])
posTrkZ0 = array('d',[0])

events0.Branch("uncVY",uncVY,"uncVY")
events0.Branch("uncVZ",uncVZ,"uncVZ")
events0.Branch("uncM",uncM,"uncM")
events0.Branch("uncTargProjY",uncTargProjY,"uncTargProjY")
events0.Branch("uncCovYY",uncCovYY,"uncCovYY")
events0.Branch("uncCovZZ",uncCovZZ,"uncCovZZ")
events0.Branch("eleTrkLambda",eleTrkLambda,"eleTrkLambda")
events0.Branch("eleTrkZ0",eleTrkZ0,"eleTrkZ0")
events0.Branch("posTrkLambda",posTrkLambda,"posTrkLambda")
events0.Branch("posTrkZ0",posTrkZ0,"posTrkZ0")

events1.Branch("uncVY",uncVY,"uncVY")
events1.Branch("uncVZ",uncVZ,"uncVZ")
events1.Branch("uncM",uncM,"uncM")
events1.Branch("uncTargProjY",uncTargProjY,"uncTargProjY")
events1.Branch("uncCovYY",uncCovYY,"uncCovYY")
events1.Branch("uncCovZZ",uncCovZZ,"uncCovZZ")
events1.Branch("eleTrkLambda",eleTrkLambda,"eleTrkLambda")
events1.Branch("eleTrkZ0",eleTrkZ0,"eleTrkZ0")
events1.Branch("posTrkLambda",posTrkLambda,"posTrkLambda")
events1.Branch("posTrkZ0",posTrkZ0,"posTrkZ0")


with open(outfile+'.csv', mode='w') as output_file:
    file_writer = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    file_writer.writerow(["vy","vz","vyPull","vzPull","uncM","projY","eleTrkTanLambda","eleZ0","posTrkTanLambda","posZ0","signal"])
    for entry in xrange(events0.GetEntries()):
        events0.GetEntry(entry)
        signal = "0"
        vy = events0.uncVY - yBeam
        vz = events0.uncVZ - zTarg
        vyPull = (events0.uncVY - yBeam) / np.sqrt(events0.uncCovYY)
        vzPull = (events0.uncVZ - zTarg) / np.sqrt(events0.uncCovZZ)
        projY = events0.uncTargProjY - yBeam
        eleZ0 = events0.eleTrkZ0 - zTarg * events0.eleTrkLambda
        posZ0 = events0.posTrkZ0 - zTarg * events0.posTrkLambda
        
        file_writer.writerow([str(vy),str(vz),  str(vyPull), str(vzPull), str(events0.uncM), str(projY), str(events0.eleTrkLambda), str(eleZ0), 
            str(events0.posTrkLambda), str(posZ0), signal])

    for entry in xrange(events1.GetEntries()):
        events1.GetEntry(entry)
        signal = "1"
        vy = events1.uncVY - yBeam
        vz = events1.uncVZ - zTarg
        vyPull = (events1.uncVY - yBeam) / np.sqrt(events1.uncCovYY)
        vzPull = (events1.uncVZ - zTarg) / np.sqrt(events1.uncCovZZ)
        projY = events1.uncTargProjY - yBeam
        eleZ0 = events1.eleTrkZ0 - zTarg * events1.eleTrkLambda
        posZ0 = events1.posTrkZ0 - zTarg * events1.posTrkLambda
        
        file_writer.writerow([str(vy),str(vz),  str(vyPull), str(vzPull), str(events1.uncM), str(projY), str(events1.eleTrkLambda), str(eleZ0), 
            str(events1.posTrkLambda), str(posZ0), signal])