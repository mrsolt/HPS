#matplotlib inline

import sys
tmpargv = sys.argv
sys.argv = []
import getopt
sys.argv = tmpargv

import random

import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

from sklearn import datasets
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.metrics import classification_report, roc_auc_score

from root_numpy import root2array, rec2array

import pandas.core.common as com
from pandas.core.index import Index

from pandas.tools import plotting
from pandas.tools.plotting import scatter_matrix

from sklearn.cross_validation import train_test_split

from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.metrics import classification_report, roc_auc_score

from sklearn.metrics import roc_curve, auc
from root_numpy import array2root

#List arguments
def print_usage():
    print "\nUsage: {0} <output file base name> <input background file> <input text file name>".format(sys.argv[0])
    print "Arguments: "
    print '\t-t: tree name (default ntuple)'
    print '\t-h: this help message'
    print
            
def signal_background(data1, data2, column=None, grid=True,xlabelsize=None, xrot=None, ylabelsize=None,
                      yrot=None, ax=None, sharex=False,sharey=False, figsize=None,layout=None, bins=10, **kwds):
    if 'alpha' not in kwds:
        kwds['alpha'] = 0.5

    if column is not None:
        if not isinstance(column, (list, np.ndarray, Index)):
            column = [column]
        data1 = data1[column]
        data2 = data2[column]
        
    data1 = data1._get_numeric_data()
    data2 = data2._get_numeric_data()
    naxes = len(data1.columns)

    fig, axes = plt.subplots(#naxes=naxes, #ax=ax, squeeze=False,
                                   sharex=sharex,
                                   sharey=sharey,
                                   figsize=figsize)#,
#                                   layout=layout)
    #_axes = plotting._flatten(axes)
    _axes = axes

    for i, col in enumerate(com._try_sort(data1.columns)):
        #ax = _axes[i]
        ax =_axes
        low = min(data1[col].min(), data2[col].min())
        high = max(data1[col].max(), data2[col].max())
        ax.hist(data1[col].dropna().values,
                bins=bins, range=(low,high), **kwds)
        ax.hist(data2[col].dropna().values,
                bins=bins, range=(low,high), **kwds)
        ax.set_title(col)
        ax.grid(grid)

    #plotting._set_ticks_props(axes, xlabelsize=xlabelsize, xrot=xrot,
    #                          ylabelsize=ylabelsize, yrot=yrot)
    fig.subplots_adjust(wspace=0.3, hspace=0.7)

    return axes

def correlations(data, **kwds):
    """Calculate pairwise correlation between features.
    
    Extra arguments are passed on to DataFrame.corr()
    """
    # simply call df.corr() to get a table of
    # correlation values if you do not need
    # the fancy plotting
    corrmat = data.corr(**kwds)

    fig, ax1 = plt.subplots(ncols=1, figsize=(6,5))
    
    opts = {'cmap': plt.get_cmap("RdBu"),
            'vmin': -1, 'vmax': +1}
    heatmap1 = ax1.pcolor(corrmat, **opts)
    plt.colorbar(heatmap1, ax=ax1)

    ax1.set_title("Correlations")

    labels = corrmat.columns.values
    for ax in (ax1,):
        # shift location of ticks to center of the bins
        ax.set_xticks(np.arange(len(labels))+0.5, minor=False)
        ax.set_yticks(np.arange(len(labels))+0.5, minor=False)
        ax.set_xticklabels(labels, minor=False, ha='right', rotation=70)
        ax.set_yticklabels(labels, minor=False)
        
    plt.tight_layout()

def compare_train_test(clf, X_train, y_train, X_test, y_test, bins=30):
    decisions = []
    for X,y in ((X_train, y_train), (X_test, y_test)):
        d1 = clf.decision_function(X[y>0.5]).ravel()
        d2 = clf.decision_function(X[y<0.5]).ravel()
        decisions += [d1, d2]
        
    low = min(np.min(d) for d in decisions)
    high = max(np.max(d) for d in decisions)
    low_high = (low,high)
    
    plt.hist(decisions[0],
             color='r', alpha=0.5, range=low_high, bins=bins,
             histtype='stepfilled', normed=True,
             label='S (train)')
    plt.hist(decisions[1],
             color='b', alpha=0.5, range=low_high, bins=bins,
             histtype='stepfilled', normed=True,
             label='B (train)')

    hist, bins = np.histogram(decisions[2],
                              bins=bins, range=low_high, normed=True)
    scale = len(decisions[2]) / sum(hist)
    err = np.sqrt(hist * scale) / scale
    
    width = (bins[1] - bins[0])
    center = (bins[:-1] + bins[1:]) / 2
    plt.errorbar(center, hist, yerr=err, fmt='o', c='r', label='S (test)')
    
    hist, bins = np.histogram(decisions[3],
                              bins=bins, range=low_high, normed=True)
    scale = len(decisions[2]) / sum(hist)
    err = np.sqrt(hist * scale) / scale

    plt.errorbar(center, hist, yerr=err, fmt='o', c='b', label='B (test)')

    plt.xlabel("BDT output")
    plt.ylabel("Arbitrary units")
    plt.legend(loc='best')

treename = "ntuple"
options, remainder = getopt.gnu_getopt(sys.argv[1:], 't:h')

# Parse the command line argumentz
for opt, arg in options:
		if opt=='-t':
			treename = str(arg)
		if opt=='-h':
			print_usage()
			sys.exit(0)

branch_names = """uncVZ, eleTrkZ0, posTrkZ0""".split(",")
branch_names = [c.strip() for c in branch_names]
branch_names = (b.replace(" ", "_") for b in branch_names)
branch_names = list(b.replace("-", "_") for b in branch_names)

outfile = str(remainder[0])
input_back = str(remainder[1])
input_sig = str(remainder[2])

signal = root2array(input_sig,treename,branch_names)
signal = rec2array(signal)

backgr = root2array(input_back,treename,branch_names)
backgr = rec2array(backgr)

X = np.concatenate((signal, backgr))
y = np.concatenate((np.ones(signal.shape[0]),np.zeros(backgr.shape[0])))

df = pd.DataFrame(np.hstack((X, y.reshape(y.shape[0], -1))),columns=branch_names+['y'])

signal_background(df[df.y<0.5], df[df.y>0.5],bins=20)
df.ix[random.sample(df.index, 1000)].plot(kind='scatter',x='uncVZ', y='eleTrkZ0',c='y', cmap='autumn')
df.boxplot(by='y',return_type='axes')

bg = df.y < 0.5
sig = df.y > 0.5

correlations(df[bg].drop('y', 1))
correlations(df[sig].drop('y', 1))

X_dev,X_eval, y_dev,y_eval = train_test_split(X, y,test_size=0.33, random_state=42)
X_train,X_test, y_train,y_test = train_test_split(X_dev, y_dev,test_size=0.33, random_state=492)

dt = DecisionTreeClassifier(max_depth=3,min_samples_leaf=0.05*len(X_train))
dt = DecisionTreeClassifier(max_depth=3,min_samples_leaf=100)
bdt = AdaBoostClassifier(dt,algorithm='SAMME',n_estimators=50,learning_rate=0.5)

bdt.fit(X_train, y_train)

#AdaBoostClassifier(algorithm='SAMME',base_estimator=DecisionTreeClassifier(compute_importances=None, criterion='gini',max_depth=3, max_features=None, max_leaf_nodes=None,
            #min_density=None, 
#            min_samples_leaf=10000,min_samples_split=2, random_state=None, splitter='best'),learning_rate=0.5, n_estimators=50, random_state=None)

y_predicted = bdt.predict(X_test)
print classification_report(y_test, y_predicted,target_names=["background", "signal"])
print "Area under ROC curve: %.4f"%(roc_auc_score(y_test,bdt.decision_function(X_test)))

y_predicted = bdt.predict(X_train)
print classification_report(y_train, y_predicted,target_names=["background", "signal"])
print "Area under ROC curve: %.4f"%(roc_auc_score(y_train,bdt.decision_function(X_train)))

decisions = bdt.decision_function(X_test)
# Compute ROC curve and area under the curve
fpr, tpr, thresholds = roc_curve(y_test, decisions)
roc_auc = auc(fpr, tpr)

plt.plot(fpr, tpr, lw=1, label='ROC (area = %0.2f)'%(roc_auc))

plt.plot([0, 1], [0, 1], '--', color=(0.6, 0.6, 0.6), label='Luck')
plt.xlim([-0.05, 1.05])
plt.ylim([-0.05, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver operating characteristic')
plt.legend(loc="lower right")
plt.grid()
plt.show()

compare_train_test(bdt, X_train, y_train, X_test, y_test)
y_predicted = bdt.decision_function(X)
y_predicted.dtype = [('y', np.float64)]

array2root(y_predicted, outfile+".root", "BDToutput")