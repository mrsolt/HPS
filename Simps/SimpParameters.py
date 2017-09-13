#!/usr/bin/env python
#Author Matt Solt mrsolt@slac.stanford.edu
import sys
import getopt
import numpy as np

N_c = 3 #Number of flavors
dvMassConstraint = False #Dark Vector mass constraint
epsLBConstraint = False #Lower Bound on epsilon constraint
eBeam = 2.3 #Beam energy in GeV


def print_usage():
    print "\nUsage: {0} <output file basename>".format(sys.argv[0])
    print "Arguments: "
    print '\t-e: use this beam energy'
    print '\t-d: apply dark vector mass constraint'
    print '\t-E: appy lower bound on epsilon'
    print '\t-h: this help message'
    print

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'dEe:h')

# Parse the command line arguments
for opt, arg in options:
	if opt=='-d':
            dvMassConstraint = True
	if opt=='-E':
            epsLBConstraint = True
	if opt=='-e':
            eBeam = float(arg)
	if opt=='-h':
            print_usage()
            sys.exit(0)

if len(remainder)!=1:
    print_usage()
    sys.exit(0)

outfile = remainder[0]

# Effective Field Theory prediction of dark vector mass
def darkVectorMassConstraint(f_pi,N_c):
	return 4*np.pi*f_pi/np.sqrt(N_c)

# Suppresses annihilations of 2 dark pions -> A'* -> ff_bar
def epsUpperBound(eps):
	return eps < 0.01

# Suppresses the semi-annihilation 2 dark pions -> A' + dark pion
def apMassLowerBound(m_a,m_pi):
	return m_a > 2 * m_pi

# Visible signal at HPS
def darkVectorMassUpperBound(m_V,m_pi):
	return m_V < 2 * m_pi

# Perturbativity of meson theory requires this
def darkPionMasstoCouplingUpperBound(m_pi,f_pi):
	return m_pi/f_pi < 4*np.pi

# Assumption from naturalness arguments
def alphaDark(alphaDark):
	return alphaDark == 0.01

# Suppresses annihilations of 2 dark pions -> A'* -> ff_bar
def epsLowerBound(eps,m_a):
	return eps > 10**-6.3 * np.sqrt(m_a/0.01)

aDark = 0.01
apMassMin = 0.025 #GeV
apMassMax = 0.200 #GeV
apMassStep = 0.025 #GeV
dvMassMin = 0.025 #GeV
dvMassMax = 0.200 #GeV
dvMassStep = 0.025 #GeV
pionMassMin = 0.025 #GeV
pionMassMax = 0.200 #GeV
pionMassStep = 0.025 #GeV
epsMin = 10**-7
epsMax = 0.01
epsStep = np.sqrt(10) #Step size multiplying the previous value by this factor

NapMass = int((apMassMax - apMassMin)/apMassStep)
NdvMass = int((dvMassMax - dvMassMin)/dvMassStep)
NpionMass = int((pionMassMax - pionMassMin)/pionMassStep)
Neps = 10 #np.log10(epsMax) - np.log10(epsMin)
Nfpi = 10

textfile = open(outfile + ".txt","w")
outputText = False

for i in range (NapMass):
	m_a = apMassMin + i * apMassStep
	for j in range (NdvMass):
		m_V = dvMassMin + j * dvMassStep
		for k in range (NpionMass):
			m_pi = pionMassMin + k * pionMassStep
			fpiMin = m_pi/10
			fpiMax = m_pi
			fpiStep = (fpiMax - fpiMin)/Nfpi
			for l in range (Neps):
				eps = epsMin * epsStep**l
				for m in range (Nfpi):
					f_pi = fpiMin + m * fpiStep
					if (not epsUpperBound(eps)): continue
					if (not apMassLowerBound(m_a,m_pi)): continue
					if (not darkVectorMassUpperBound(m_V,m_pi)): continue
					if (not darkPionMasstoCouplingUpperBound(m_pi,f_pi)): continue
					if (not epsLowerBound(eps,m_a) and epsLBConstraint): continue
					dvMassContraint = darkVectorMassConstraint(f_pi,N_c)
					if ((m_V > 5*dvMassContraint or m_V < 1/5*dvMassContraint) and dvMassConstraint): continue
					outputText = True
					#textfile.write(str(m_a) + " " + str(m_V) + " " + str(m_pi) + " " + str(eps) + " " + str(f_pi) + " " + str(aDark) + "\n")
		if (outputText is True): textfile.write(str(m_a) + " " + str(m_V) + " " + str(m_pi) + "\n")
		outputText = False

textfile.close()