# test.py
Tests the upperlimit.so Python module:
```
$ ./test.py
upperlim,iflag = upperlim(cl,if_bn,fc,mub,fb,[n])

Wrapper for ``upperlim``.

Parameters
----------
cl : input float
if_bn : input int
fc : input rank-1 array('f') with bounds (n + 2)
mub : input float
fb : input rank-1 array('f') with bounds (n + 2)

Other Parameters
----------------
n : input int, optional
    Default: (len(fc)-2)

Returns
-------
upperlim : float
iflag : int

[ 0.       0.05263  0.47368  1.     ]
(4.8026652336120605, 0)
2.59603526141e-42
```
The last number printed (2.59603526141e-42) should be the same number printed by `./SimpleExample`.

# dotrials.py
Runs the toy Monte Carlo for the look-elsewhere correction.
The background PDF is hard-coded to match the shape fitted by the analysis.
The output contains a plot of local vs. global p-value; you need to look up the minimum local p-value from the analysis to get the global p-value.

# toystats.py
Optimum interval demo.
Tests optimum interval, profile likelihood, and Feldman-Cousins cut-and-count methods.

# fitvtx.py
Runs the analysis.
Requires input files:
* Data: from applyCut.py.
* Mass resolution/efficiency for A': from apeff.py.
* Background tails: from fittails_mc.py.
* Radiative fraction: from radfrac.py.
