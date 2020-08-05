import os 
from os.path import dirname
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotUtils
from DataParser import DataParser
from CsvParser  import CsvParser
from matplotlib.backends.backend_pdf import PdfPages

plt.style.use('ggplot')

output = "test"
#signal_file = '/nfs/slac/g/hps2/mrsolt/hps/Data2016/MachineLearing/AnalysisWorkshopML/ap-beam_100MeV_4e9.csv'
#background_file = '/nfs/slac/g/hps2/mrsolt/hps/Data2016/MachineLearing/AnalysisWorkshopML/tritrig-wab-beam_100MeV_L1L1_tight.csv'
signal_file = '~/CS230/cs230-project/notebooks/datasets/ap_100MeV_L1L1_tight_08mm.csv'
background_file = '~/CS230/cs230-project/notebooks/datasets/tritrig-wab-beam_100MeV_L1L1_tight.csv'

background = CsvParser(background_file)
signal     = CsvParser(signal_file)

myData     = DataParser(signal=signal, background=background)

X_train, Y_train, X_test, Y_test, classes = myData.load_dataset()
print(Y_train.shape)
print(Y_test.shape)

X_train = X_train.T
Y_train = Y_train.T
X_test = X_test.T
Y_test = Y_test.T

from sklearn.ensemble import RandomForestClassifier
n_estimators = 100
max_depth = 10
clf = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth, oob_score=True, random_state=0)

min_estimators = 10
max_estimators = 100
spacing = 10
n = int((max_estimators - min_estimators) / spacing) + 1
depth = [3,5,7,10]

PDFname = output + "_err.pdf"
pp = PdfPages(PDFname)

fig, ((ax0, ax1)) = plt.subplots(nrows=1, ncols=2, figsize=(20,8))
#ax = fig.add_subplot(111)

for j in depth:
    error_rate = []
    error_rate_test = []
    estim = []
    for i in range(n):
        estimators = min_estimators + spacing * i
        clf.set_params(n_estimators=estimators,max_depth=j)
        clf.fit(X_train, Y_train)
        estim.append(estimators)
        print("Maximum Depth {0}. Number of Estimators {1}".format(j,estimators))
        # Record the OOB error for each `n_estimators=i` setting.
        oob_error = 1 - clf.oob_score_
        oob_error_test = 1 - clf.score(X_test, Y_test)
        error_rate.append(oob_error)
        error_rate_test.append(oob_error_test)

        # Generate the "OOB error rate" vs. "n_estimators" plot.
    ax0.plot(estim, error_rate, label="Max Depth = {0}".format(j))
    ax1.plot(estim, error_rate_test, label="Max Depth = {0}".format(j))
    del estim
    del error_rate
    del error_rate_test

ax0.set_xlim(min_estimators, max_estimators)
ax0.set_xlabel("Number of Estimators", fontsize=20)
ax0.set_ylabel("OOB error rate", fontsize=20)
ax0.set_title("OOB Error Rate Training", fontsize=20)
ax0.legend(loc=1, fontsize=20)

ax1.set_xlim(min_estimators, max_estimators)
ax1.set_xlabel("Number of Estimators", fontsize=20)
ax1.set_ylabel("OOB error rate", fontsize=20)
ax1.set_title("OOB Error Rate Testing", fontsize=20)
ax1.legend(loc=1, fontsize=20)

pp.savefig(fig)
pp.close()