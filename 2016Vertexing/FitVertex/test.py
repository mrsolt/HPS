#!/usr/bin/env python

import upperlimit
import numpy
print upperlimit.upperlim.__doc__
fc = numpy.array([0,0.05263,0.47368,1])
print fc
output = upperlimit.upperlim(0.9, 1, fc, 0., fc)
print output
print (1.e-42/1.85)*output[0]
