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
    print "\nUsage: {0} <output file base name> <input file name> ...".format(sys.argv[0])
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
isSignal = False
fulltruth = False

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'x:y:z:sfh')

# Parse the command line arguments
for opt, arg in options:
		if opt=='-f':
			fulltruth = True
		if opt=='-s':
			isSignal = True
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
events = TChain("ntuple")
#events = TChain("tree")
for i in range(1,len(remainder)):
    events.Add(remainder[i])

uncVX = array('d',[0])
uncVY = array('d',[0])
uncVZ = array('d',[0])
uncP = array('d',[0])
uncChisq = array('d',[0])
uncM = array('d',[0])
uncTargProjX = array('d',[0])
uncTargProjY = array('d',[0])
uncTargProjXErr = array('d',[0])
uncTargProjYErr = array('d',[0])
uncCovXX = array('d',[0])
uncCovYY = array('d',[0])
uncCovZZ = array('d',[0])
bscChisq = array('d',[0])
tarChisq = array('d',[0])
eleP = array('d',[0])
eleTrkChisq = array('d',[0])
eleTrkHits = array('d',[0])
eleTrkD0 = array('d',[0])
eleTrkLambda = array('d',[0])
eleTrkZ0 = array('d',[0])
eleTrkD0Err = array('d',[0])
eleTrkLambdaErr = array('d',[0])
eleTrkZ0Err = array('d',[0])
posP = array('d',[0])
posTrkChisq = array('d',[0])
posTrkHits = array('d',[0])
posTrkD0 = array('d',[0])
posTrkLambda = array('d',[0])
posTrkZ0 = array('d',[0])
posTrkD0Err = array('d',[0])
posTrkLambdaErr = array('d',[0])
posTrkZ0Err = array('d',[0])
eleL1tthetaY = array('d',[0])
eleL2tthetaY = array('d',[0])
eleL1bthetaY = array('d',[0])
eleL2bthetaY = array('d',[0])
posL1tthetaY = array('d',[0])
posL2tthetaY = array('d',[0])
posL1bthetaY = array('d',[0])
posL2bthetaY = array('d',[0])

events.Branch("uncVX",uncVX,"uncVX")
events.Branch("uncVY",uncVY,"uncVY")
events.Branch("uncVZ",uncVZ,"uncVZ")
events.Branch("uncP",uncP,"uncP")
events.Branch("uncChisq",uncChisq,"uncChisq")
events.Branch("uncM",uncM,"uncM")
events.Branch("uncTargProjX",uncTargProjX,"uncTargProjX")
events.Branch("uncTargProjY",uncTargProjY,"uncTargProjY")
events.Branch("uncTargProjXErr",uncTargProjXErr,"uncTargProjXErr")
events.Branch("uncTargProjYErr",uncTargProjYErr,"uncTargProjYErr")
events.Branch("uncCovXX",uncCovXX,"uncCovXX")
events.Branch("uncCovYY",uncCovYY,"uncCovYY")
events.Branch("uncCovZZ",uncCovZZ,"uncCovZZ")
events.Branch("bscChisq",bscChisq,"bscChisq")
events.Branch("tarChisq",tarChisq,"tarChisq")
events.Branch("eleP",eleP,"eleP")
events.Branch("eleTrkChisq",eleTrkChisq,"eleTrkChisq")
events.Branch("eleTrkHits",eleTrkHits,"eleTrkHits")
events.Branch("eleTrkD0",eleTrkD0,"eleTrkD0")
events.Branch("eleTrkLambda",eleTrkLambda,"eleTrkLambda")
events.Branch("eleTrkZ0",eleTrkZ0,"eleTrkZ0")
events.Branch("eleTrkD0Err",eleTrkD0Err,"eleTrkD0Err")
events.Branch("eleTrkLambdaErr",eleTrkLambdaErr,"eleTrkLambdaErr")
events.Branch("eleTrkZ0Err",eleTrkZ0Err,"eleTrkZ0Err")
events.Branch("posP",posP,"posP")
events.Branch("posTrkChisq",posTrkChisq,"posTrkChisq")
events.Branch("posTrkHits",posTrkHits,"posTrkHits")
events.Branch("posTrkD0",posTrkD0,"posTrkD0")
events.Branch("posTrkLambda",posTrkLambda,"posTrkLambda")
events.Branch("posTrkZ0",posTrkZ0,"posTrkZ0")
events.Branch("posTrkD0Err",posTrkD0Err,"posTrkD0Err")
events.Branch("posTrkLambdaErr",posTrkLambdaErr,"posTrkLambdaErr")
events.Branch("posTrkZ0Err",posTrkZ0Err,"posTrkZ0Err")
events.Branch("eleL1tthetaY",eleL1tthetaY,"eleL1tthetaY")
events.Branch("eleL2tthetaY",eleL2tthetaY,"eleL2tthetaY")
events.Branch("eleL1bthetaY",eleL1bthetaY,"eleL1bthetaY")
events.Branch("eleL2bthetaY",eleL2bthetaY,"eleL2bthetaY")
events.Branch("posL1tthetaY",posL1tthetaY,"posL1tthetaY")
events.Branch("posL2tthetaY",posL2tthetaY,"posL2tthetaY")
events.Branch("posL1bthetaY",posL1bthetaY,"posL1bthetaY")
events.Branch("posL2bthetaY",posL2bthetaY,"posL2bthetaY")

with open(outfile+'.csv', mode='w') as output_file:
    file_writer = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    file_writer.writerow(["truthZ","vx","vy","vz","vxPull","vyPull",
    	"vzPull","uncP","uncChisq","uncM","projX","projY","projXPull",
    	"projYPull","bscChisq","tarChisq","eleP","eleChisqDOF","eleTrkD0",
    	"eleTrkTanLambda","eleZ0","eleTrkD0Err","eleTrkTanLambdaErr",
    	"eleTrkZ0Err","posP","posChisqDOF","posTrkD0","posTrkTanLambda",
    	"posZ0","posTrkD0Err","posTrkTanLambdaErr","posTrkZ0Err","signal"])
    for entry in xrange(events.GetEntries()):
        events.GetEntry(entry)
        truthZ = 0
        signal = "0"
        if(isSignal):
        	signal = "1"
        #	truthZ = events.
        vx = events.uncVX - xBeam
        vy = events.uncVY - yBeam
        vz = events.uncVZ - zTarg
        vxPull = (events.uncVX - xBeam) / np.sqrt(events.uncCovXX)
        vyPull = (events.uncVY - yBeam) / np.sqrt(events.uncCovYY)
        vzPull = (events.uncVZ - zTarg) / np.sqrt(events.uncCovZZ)
        projX = events.uncTargProjX - xBeam
        projY = events.uncTargProjY - yBeam
        projXPull = (events.uncTargProjX - xBeam) / events.uncTargProjXErr
        projYPull = (events.uncTargProjY - yBeam) / events.uncTargProjXErr
        eleChisqDOF = events.eleTrkChisq / (2 * events.eleTrkHits - 5)
        posChisqDOF = events.posTrkChisq / (2 * events.posTrkHits - 5)
        eleZ0 = events.eleTrkZ0 - zTarg * events.eleTrkLambda
        posZ0 = events.posTrkZ0 - zTarg * events.posTrkLambda
        
        if(not fulltruth):
            file_writer.writerow([str(truthZ), str(vx),str(vy),str(vz), str(vxPull), str(vyPull), str(vzPull), str(events.uncP), str(events.uncChisq), 
            	str(events.uncM), str(projX), str(projY), str(projXPull), str(projYPull), str(events.bscChisq), str(events.tarChisq),
            	str(events.eleP), str(eleChisqDOF), str(events.eleTrkD0), str(events.eleTrkLambda), str(eleZ0), 
            	str(events.eleTrkD0Err), str(events.eleTrkLambdaErr), str(events.eleTrkZ0Err),
            	str(events.posP), str(posChisqDOF), str(events.posTrkD0), str(events.posTrkLambda), str(posZ0), 
            	str(events.posTrkD0Err), str(events.posTrkLambdaErr), str(events.posTrkZ0Err),signal])

        else:
    	    file_writer.writerow([str(truthZ), str(vx),str(vy),str(vz), str(vxPull), str(vyPull), str(vzPull), str(events.uncP), str(events.uncChisq), 
            	str(events.uncM), str(projX), str(projY), str(projXPull), str(projYPull), str(events.bscChisq), str(events.tarChisq),
            	str(events.eleP), str(eleChisqDOF), str(events.eleTrkD0), str(events.eleTrkLambda), str(eleZ0), 
            	str(events.eleTrkD0Err), str(events.eleTrkLambdaErr), str(events.eleTrkZ0Err),
            	str(events.posP), str(posChisqDOF), str(events.posTrkD0), str(events.posTrkLambda), str(posZ0), 
            	str(events.posTrkD0Err), str(events.posTrkLambdaErr), str(events.posTrkZ0Err),
            	str(events.eleL1tthetaY), str(events.eleL2tthetaY), str(events.eleL1bthetaY), str(events.eleL2bthetaY), 
            	str(events.posL1tthetaY), str(events.posL2tthetaY), str(events.posL1bthetaY), str(events.posL2bthetaY)])
