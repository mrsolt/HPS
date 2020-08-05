# This allows matplotlib plots to be shown inline
#%matplotlib inline

import sys
tmpargv = sys.argv
sys.argv = []
import getopt
sys.argv = tmpargv

import numpy as np
import root_numpy as rnp
import matplotlib.pyplot as plt

#List arguments
def print_usage():
    print "\nUsage: {0} <output file base name> <input background file> <input text file name>".format(sys.argv[0])
    print "Arguments: "
    print '\t-t: tree name (default ntuple)'
    print '\t-h: this help message'
    print

treename = "ntuple"
options, remainder = getopt.gnu_getopt(sys.argv[1:], 't:h')

# Parse the command line argumentz
for opt, arg in options:
		if opt=='-t':
			treename = str(arg)
		if opt=='-h':
			print_usage()
			sys.exit(0)

# Use the Bayesian Methods for Hackers design
plt.style.use('bmh')


outfile = str(remainder[0])
input_back = str(remainder[1])
input_sig = str(remainder[2])

branch_names = """uncVZ, eleTrkZ0, posTrkZ0""".split(",")
branch_names = [c.strip() for c in branch_names]
branch_names = (b.replace(" ", "_") for b in branch_names)
branch_names = list(b.replace("-", "_") for b in branch_names)

signal = rnp.root2array(input_sig,treename,branch_names)
signal = rnp.rec2array(signal)

backgr = rnp.root2array(input_back,treename,branch_names)
backgr = rnp.rec2array(backgr)

features = rnp.list_branches(input_sig)

print '\n'.join(str(feature) for feature in features)

ap_uncVZ = signal[:,0]
ap_eleZ0 = signal[:,1]
ap_posZ0 = signal[:,2]

backgr_uncVZ = backgr[:,0]
backgr_eleZ0 = backgr[:,1]
backgr_posZ0 = backgr[:,2]

fig, (ax0, ax1, ax2) = plt.subplots(nrows=1, ncols=3, figsize=(20,8))

ax0.hist2d(ap_eleZ0, ap_posZ0, bins=150, range=[[-5, 5], [-5, 5]]);
ax0.set_xlabel("eleZ0 (mm)", fontsize=20)
ax0.set_ylabel("posZ0 (mm)", fontsize=20)
ax0.set_title("Signal", fontsize=20)

ax1.hist2d(backgr_eleZ0, backgr_posZ0, bins=150, range=[[-5, 5], [-5, 5]]);
ax1.set_xlabel("eleZ0 (mm)", fontsize=20)
ax1.set_ylabel("posZ0 (mm)", fontsize=20)
ax1.set_title("Background", fontsize=20)

ax2.hist(ap_uncVZ, bins=150, range=(-20, 70), alpha=0.8, normed=True, histtype="stepfilled", label="Signal");
ax2.hist(backgr_uncVZ, bins=150, range=(-20, 70), alpha=0.8, normed=True, histtype="stepfilled", label="Background");
ax2.set_xlabel("uncVZ (mm)", fontsize=20)
ax2.legend(loc=2)

fig.savefig(outfile+".pdf",bbox_inches='tight')

# Create the targets
y_signal = np.ones(len(signal))
y_backgr = np.zeros(len(backgr))

signal_zip = zip(signal, y_signal)
backgr_zip = zip(backgr, y_backgr)

X_merge = np.concatenate((signal_zip, backgr_zip))
np.random.shuffle(X_merge)

X_list, y_list = map(list, zip(*X_merge))

X = np.array(X_list)
print "Shape of X: " + str(X.shape)

y = np.array(y_list)
print "Shape of y: " + str(y.shape)


from sklearn.ensemble import RandomForestClassifier
from collections import OrderedDict

RANDOM_STATE = 123

forest_clfs = [
    ("RandomForestClassifier, max_features='sqrt'",
        RandomForestClassifier(warm_start=True, oob_score=True,
                               max_features="sqrt",
                               random_state=RANDOM_STATE)),
    ("RandomForestClassifier, max_features='log2'",
        RandomForestClassifier(warm_start=True, max_features='log2',
                               oob_score=True,
                               random_state=RANDOM_STATE)),
    ("RandomForestClassifier, max_features=None",
        RandomForestClassifier(warm_start=True, max_features=None,
                               oob_score=True,
                               random_state=RANDOM_STATE))
]

# Map a classifier name to a list of (<n_estimators>, <error rate>) pairs.
error_rate = OrderedDict((label, []) for label, _ in forest_clfs)

# Range of `n_estimators` values to explore.
min_estimators = 10
max_estimators = 200

for label, clf in forest_clfs:
    for i in range(min_estimators, max_estimators + 1):
        clf.set_params(n_estimators=i)
        clf.fit(X, y)

        # Record the OOB error for each `n_estimators=i` setting.
        oob_error = 1 - clf.oob_score_
        error_rate[label].append((i, oob_error))



fig = plt.figure(figsize=(15, 8))
ax = fig.add_subplot(111)

# Generate the "OOB error rate" vs. "n_estimators" plot.
for label, clf_err in error_rate.items():
    xs, ys = zip(*clf_err)
    ax.plot(xs, ys, label=label)

ax.set_xlim(min_estimators, max_estimators)
ax.set_xlabel("Number of Estimators", fontsize=20)
ax.set_ylabel("OOB error rate", fontsize=20)
ax.legend(loc=1, fontsize=20);

fig.savefig(outfile+".pdf",bbox_inches='tight')

signal_test = rnp.root2array(input_sig,treename,branch_names)
signal_test = rnp.rec2array(signal_test)

backgr_test = rnp.root2array(input_back,treename,branch_names)
backgr_test = rnp.rec2array(backgr)

features_test = rnp.list_branches(input_sig)

print '\n'.join(str(feature) for feature in features_test)

# Create the targets
y_signal_test = np.ones(len(signal_test))
y_backgr_test = np.zeros(len(backgr_test))

signal_zip_test = zip(signal_test, y_signal_test)
backgr_zip_test = zip(backgr_test, y_backgr_test)

X_merge_test = np.concatenate((signal_zip_test, backgr_zip_test))
np.random.shuffle(X_merge_test)

X_list_test, y_list_test = map(list, zip(*X_merge_test))

X_test = np.array(X_list_test)
print "Shape of X: " + str(X_test.shape)

y_test = np.array(y_list_test)
print "Shape of y: " + str(y_test.shape)


from sklearn.ensemble import RandomForestClassifier

RANDOM_STATE = 123

#
forest_clf = RandomForestClassifier(max_features='sqrt', n_jobs=-1, n_estimators=160, random_state=RANDOM_STATE)
forest_clf.fit(X, y)



importances = forest_clf.feature_importances_
std = np.std([clf.feature_importances_ for clf in forest_clf.estimators_], axis=0)
indices = np.argsort(importances)[::-1]
fig, ax0 = plt.subplots(figsize=(15, 8))
sorted_features = []
[sorted_features.append(features_test[index]) for index in indices]
ax0.bar(range(len(importances)), importances[indices], yerr=std[indices], align="center", alpha=0.5)
plt.xticks(range(len(importances)), sorted_features, rotation='vertical');

fig.savefig(outfile+".pdf",bbox_inches='tight')

y_predictions = forest_clf.predict(X_test)
cm = metrics.confusion_matrix(y_test, y_predictions)
cm_normalized = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
cmap=plt.cm.Blues
plt.imshow(cm_normalized, interpolation='nearest', cmap=cmap)
plt.colorbar()
plt.tight_layout()
plt.ylabel('True label')
plt.xlabel('Predicted label');

fig.savefig(outfile+".pdf",bbox_inches='tight')

ap_uncVZ_test = signal_test[:,0]
ap_eleZ0_test = signal_test[:,1]
ap_posZ0_test = signal_test[:,2]

backgr_uncVZ_test = backgr_test[:,0]
backgr_eleZ0_test = backgr_test[:,1]
backgr_posZ0_test = backgr_test[:,2]

fig, (ax0, ax1) = plt.subplots(ncols=2, figsize=(20,8))

ax0.scatter(X_test[:,1], X_test[:,2], c=y_predictions, alpha=0.6)
ax0.set_xlabel("eleZ0 (mm)", fontsize=20)
ax0.set_ylabel("posZ0 (mm)", fontsize=20)

ax1.hist(X_test[:, 0][y_predictions == 1], bins=150, range=(-20, 70), alpha=0.8, histtype="stepfilled", label="Identified as signal")
ax1.hist(X_test[:, 0][y_test == 1], bins=150, range=(-20, 70), alpha=0.8, histtype="stepfilled", label="signal")
ax1.legend(loc=2)
ax1.set_xlabel("uncVZ (mm)", fontsize=20);

fig.savefig(outfile+".pdf",bbox_inches='tight')