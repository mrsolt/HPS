import numpy as np
#import root_numpy as rnp
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.colors import LogNorm
from sklearn.metrics import roc_curve, auc
import scipy
#from scipy.optimize import curve_fit
plt.style.use('ggplot')

def MakePlots(clf, X, Y, param_min, param_max, n_test, param_list=None, uncVZi=0, clf_cut=0.5, threshold_min=0.9, 
	nBins=100, fpr_max=0.25, PDFbasename="", compareROC=True):

	y_predictions = clf.predict(X)
	y_predictions_proba = clf.predict_proba(X)
	print("Making ROC Curves.")
	clf_cut_test, tpr_at_threshold = MakeRocCurves(X, Y, y_predictions_proba, n_test, fpr_max=fpr_max, threshold_min=threshold_min, 
		PDFbasename=PDFbasename, compare=compareROC)
	print("Classifier cut {0}. True positive rate at threshold {1}".format(clf_cut_test, tpr_at_threshold))
	print("ROC Curves Complete. Making Classifier Output Plots")
	MakeClassifierOutputPlots(X, Y, y_predictions_proba, uncVZi=uncVZi, 
		minVZ=param_min[uncVZi], maxVZ=param_max[uncVZi], clf_cut=clf_cut, 
		threshold_min=threshold_min, nBins=nBins, PDFbasename=PDFbasename)
	print("Classifier Output Plots Complete. Making Z Plots.")
	MakeZPlots(X, Y, y_predictions_proba, uncVZi=uncVZi, minVZ=param_min[uncVZi], 
		maxVZ=param_max[uncVZi], threshold_min=threshold_min, nBins=nBins, 
		PDFbasename=PDFbasename)
	MakeClassifierOutputPlots(X, Y, y_predictions_proba, uncVZi=uncVZi, 
		minVZ=param_min[uncVZi], maxVZ=param_max[uncVZi], clf_cut=clf_cut_test, 
		threshold_min=threshold_min, nBins=nBins, PDFbasename=PDFbasename+"_clftestcut")
	#MakePhysicsPlots(X_train, Y_train, y_predictions, y_predictions_proba, param_list, 
	#	param_min, param_max, uncVZi=uncVZi, clf_cut=clf_cut, threshold_min=threshold_min, 
	#	nBins=nBins, PDFbasename=PDFbasename+"_train")
	print("Plots Complete.")
	return clf_cut_test, tpr_at_threshold

def MakeClassifierOutputPlots(X, Y, y_predictions_proba, uncVZi=0, minVZ=-4.3, maxVZ=80, 
	clf_cut=0.5, threshold_min=0.9, nBins=100, PDFbasename=""):
	PDFbasename = PDFbasename + "_classoutput"
	PDFname = PDFbasename + ".pdf"
	pp = PdfPages(PDFname)

	fig, ((ax0, ax1), (ax2, ax3), (ax4, ax5)) = plt.subplots(nrows=3, ncols=2, figsize=(20,24))
	zcut = 17

	#ax0.hist(X[:, uncVZi][Y[:,0] == 0], bins=nBins, range=(minVZ, maxVZ), alpha=0.8, histtype="stepfilled", label="Background")
	#ax0.hist(X[:, uncVZi][np.logical_and(y_predictions_proba[:,1] < clf_cut, Y[:,0] == 1)], bins=nBins, range=(minVZ, maxVZ), alpha=0.8, histtype="stepfilled", label="Signal Identified as Background")
	ax0.hist(X[:, uncVZi][np.logical_and(y_predictions_proba[:,1] < clf_cut, Y[:,0] == 0)], bins=nBins, range=(minVZ, maxVZ), alpha=0.8, histtype="stepfilled", label="Correctly Classified Background")
	ax0.hist(X[:, uncVZi][np.logical_and(y_predictions_proba[:,1] > clf_cut, Y[:,0] == 1)], nBins, range=(minVZ, maxVZ), alpha=0.8, histtype="stepfilled", label="Correctly Classified Signal")
	ax0.hist(X[:, uncVZi][np.logical_and(y_predictions_proba[:,1] > clf_cut, Y[:,0] == 0)], bins=nBins, range=(minVZ, maxVZ), alpha=0.8, histtype="stepfilled", label="Incorrectly Classified Background")

	ax1.hist(X[:, uncVZi][Y[:,0] == 1], bins=nBins, range=(minVZ, maxVZ), alpha=0.8, histtype="stepfilled", label="Signal")
	ax1.hist(X[:, uncVZi][np.logical_and(y_predictions_proba[:,1] > clf_cut, Y[:,0] == 0)], bins=nBins, range=(minVZ, maxVZ), alpha=0.8, histtype="stepfilled", label="Background Identified as Signal")

	ax2.hist(X[:, uncVZi][Y[:,0] == 0], bins=nBins, range=(minVZ, maxVZ), alpha=0.8, histtype="stepfilled", label="Background")
	ax2.hist(X[:, uncVZi][np.logical_and(y_predictions_proba[:,1] < clf_cut, Y[:,0] == 0)], bins=nBins, range=(minVZ, maxVZ), alpha=0.8, histtype="stepfilled", label="Background Identified as Background")
	ax3.hist(X[:, uncVZi][Y[:,0] == 1], bins=nBins, range=(minVZ, maxVZ), alpha=0.8, histtype="stepfilled", label="Signal")
	n, bins, _ = ax3.hist(X[:, uncVZi][np.logical_and(y_predictions_proba[:,1] > clf_cut, Y[:,0] == 1)], nBins, range=(minVZ, maxVZ), alpha=0.8, histtype="stepfilled", label="Signal Identified as Signal")

	ax4.hist(y_predictions_proba[:,1][Y[:,0] == 0], bins=nBins, range=(0, 1), alpha=0.8, histtype="stepfilled", label="Background")
	ax4.hist(y_predictions_proba[:,1][Y[:,0] == 1], bins=nBins, range=(0, 1), alpha=0.8, histtype="stepfilled", label="Signal")

	ax5.hist(y_predictions_proba[:,1][Y[:,0] == 0], bins=nBins, range=(threshold_min, 1), alpha=0.8, histtype="stepfilled", label="Background")
	ax5.hist(y_predictions_proba[:,1][Y[:,0] == 1], bins=nBins, range=(threshold_min, 1), alpha=0.8, histtype="stepfilled", label="Signal")

	ax0.set_yscale("log")
	ax1.set_yscale("log")
	ax2.set_yscale("log")
	ax3.set_yscale("log")
	ax4.set_yscale("log")
	ax5.set_yscale("log")

	ax0.set_ylim(0.5)
	ax1.set_ylim(0.5)
	ax2.set_ylim(0.5)
	ax3.set_ylim(0.5)
	ax4.set_ylim(0.5)
	ax5.set_ylim(0.5)

	ax0.legend(loc=1)
	ax1.legend(loc=1)
	ax2.legend(loc=1)
	ax3.legend(loc=1)
	ax4.legend(loc=1)
	ax5.legend(loc=1)

	ax0.set_xlabel("Measured Decay Length (mm)", fontsize=20)
	ax1.set_xlabel("Measured Decay Length (mm)", fontsize=20)
	ax2.set_xlabel("Measured Decay Length (mm)", fontsize=20)
	ax3.set_xlabel("Measured Decay Length (mm)", fontsize=25)
	ax4.set_xlabel("Classifier Output", fontsize=25)
	ax5.set_xlabel("Classifier Output", fontsize=20)

	pp.savefig(fig)
	pp.close()

	bin_width = bins[1] - bins[0]
	zCut_bin = int((zcut-minVZ)/(maxVZ-minVZ)*nBins)
	signal_yield_old = bin_width * sum(n[zCut_bin:nBins])
	signal_yield_new = bin_width * sum(n[0:nBins])
	#print (zCut_bin)
	#print (signal_yield_old)
	#print (signal_yield_new)
	#print (signal_yield_new/signal_yield_old)

def f(x, a, b):
	return 1/(1 + a * np.exp(np.log((1-x)/x) * b))

def MakeRocCurves(X, Y, y_predictions_proba, n_test, fpr_max=0.25, threshold_min=0.9, PDFbasename="", compare=True):
	PDFbasename = PDFbasename + "_roc"
	PDFname = PDFbasename + ".pdf"
	pp = PdfPages(PDFname) 

	fpr, tpr, threshold = roc_curve(Y, y_predictions_proba[:,1])
	roc_auc = auc(fpr, tpr)
	roc_auc_max = auc(fpr, tpr)
	popt, pcov = scipy.optimize.curve_fit(f, fpr, tpr)
	zcut = 0.5
	fpr_at_zcut = zcut/float(n_test)
	tpr_at_threshold = f(fpr_at_zcut,*popt)
	clf_cut = 9999.
	for i in range(len(fpr)):
		if(fpr[i] > fpr_at_zcut):
			clf_cut = threshold[i]
			tpr_at_threshold = tpr[i]
			break
	print("tpr_at_threshold {0}".format(tpr_at_threshold))

	fig, ((ax0, ax1),(ax2, ax3)) = plt.subplots(nrows=2, ncols=2, figsize=(20,16))
	ax0.set_title('ROC Curve; AUC = ' + str(roc_auc),fontsize=20)
	ax0.plot(fpr, tpr, label = 'roc')
	#ax0.plot(fpr, f(fpr,*popt), label='fit: a=%5.3f, b=%5.3f' % tuple(popt))
	ax0.set_ylabel('True Positive Rate',fontsize=20)
	ax0.set_xlabel('False Positive Rate',fontsize=20)
	ax0.legend(loc=4,fontsize=20)

	ax1.set_title('ROC Curve Zoom',fontsize=20)
	ax1.plot(fpr, tpr, label = 'roc')
	#ax1.plot(fpr, f(fpr,*popt), label='fit: a=%5.3f, b=%5.3f' % tuple(popt))
	ax1.set_xlim([0.0000001, 1])
	ax1.set_ylim([0.1, 1])
	ax1.set_ylabel('True Positive Rate',fontsize=20)
	ax1.set_xlabel('False Positive Rate',fontsize=20)
	ax1.legend(loc=4,fontsize=20)
	ax1.set_xscale("log")
	ax1.set_yscale("log")

	#ax2.set_title('False Positive Rate vs Threshold',fontsize=20)
	#ax2.plot(threshold, fpr, label = '')
	#ax2.set_xlabel('Classifier Threshold',fontsize=20)
	#ax2.set_ylabel('False Positive Rate',fontsize=20)

	ax3.set_title('False Positive Rate vs Threshold',fontsize=20)
	ax3.plot(threshold, fpr, label = '')
	ax3.set_xlim([0, 1])
	ax3.set_ylim([0.0000001, 1])
	ax3.set_xlabel('Classifier Threshold',fontsize=20)
	ax3.set_ylabel('False Positive Rate',fontsize=20)
	ax3.set_yscale("log")

	#ax4.set_title('True Positive Rate vs Threshold',fontsize=20)
	#ax4.plot(threshold, tpr, label = '')
	#ax4.set_xlim([0, 1])
	#ax4.set_ylim([0, 1])
	#ax4.set_ylabel('True Positive Rate',fontsize=20)
	#ax4.set_xlabel('Classifier Threshold',fontsize=20)

	ax2.set_title('True Positive Rate vs Threshold',fontsize=20)
	ax2.plot(threshold, tpr, label = '')
	ax2.set_xlim([0, 1])
	ax2.set_ylim([0.01, 1])
	ax2.set_ylabel('True Positive Rate',fontsize=20)
	ax2.set_xlabel('Classifier Threshold',fontsize=20)
	ax2.set_yscale("log")

	#ax0.set_yscale("log")
	#ax1.set_yscale("log")
	#ax2.set_yscale("log")
	#ax3.set_yscale("log")
	#ax4.set_yscale("log")
	#ax5.set_yscale("log")

	#ax0.set_xscale("log")
	#ax1.set_xscale("log")
	#ax2.set_xscale("log")
	#ax3.set_xscale("log")
	#ax4.set_xscale("log")
	#ax5.set_xscale("log")

	pp.savefig(fig)

	if(compare):
		fpr2 = []
		tpr2 = []
		total_bak = 0
		total_sig = 0
		for i in range(len(Y[:, 0])):
			if(Y[i, 0] == 0):
				total_bak = total_bak + 1
			if(Y[i, 0] == 1):
				total_sig = total_sig + 1
		print("Making ROC Curve Comparison.")
		nz = 500
		zmin = -40.
		zmax = 40.
		for j in range(nz):
			count_fpr = 0
			count_tpr = 0
			zcut = zmin + (zmax - zmin) / nz * (j + 0.5)
			for i in range(len(Y[:, 0])):
				y = Y[i,0]
				z = X[i,0]
				if(y == 0 and z > zcut):
					count_fpr = count_fpr + 1
				if(y == 1 and z > zcut):
					count_tpr = count_tpr + 1
			fpr2.append(count_fpr/total_bak)
			tpr2.append(count_tpr/total_sig)
		tpr_at_threshold2 = 0
		for i in range(len(fpr2)):
			if(fpr2[i] > fpr_at_zcut):
				tpr_at_threshold2 = tpr2[i]
				break
		print("tpr_at_threshold2 {0}".format(tpr_at_threshold2))
    
		fig2, ((ax6, ax7)) = plt.subplots(nrows=1, ncols=2, figsize=(20,8))
		ax6.set_title('ROC Curve',fontsize=20)
		ax6.plot(fpr, tpr, label = 'Random Forest (RF)')
		#ax6.plot(fpr, f(fpr,*popt), label='RF fit: a=%5.3f, b=%5.3f' % tuple(popt))
		ax6.plot(fpr2, tpr2, label = '"Traditional" Zcut')
		ax6.set_ylabel('True Positive Rate',fontsize=20)
		ax6.set_xlabel('False Positive Rate',fontsize=20)
		ax6.legend(loc=4,fontsize=20)

		#ax7.set_title('ROC Curve; AUC = ' + str(roc_auc),fontsize=20)
		#ax7.plot(fpr, tpr, label = 'Random Forest')
		#ax7.plot(fpr2, tpr2, label = '"Traditional" Zcut')
		#ax7.set_xlim([0.0000001, 1])
		#ax7.set_ylabel('True Positive Rate',fontsize=20)
		#ax7.set_xlabel('False Positive Rate',fontsize=20)
		#ax7.legend(loc=4,fontsize=20)

		#ax7.set_xscale("log")

		#ax8.set_title('ROC Curve',fontsize=20)
		#ax8.plot(fpr, tpr, label = 'Random Forest')
		#ax8.plot(fpr2, tpr2, label = '"Traditional" Zcut')
		#ax8.set_ylabel('True Positive Rate',fontsize=20)
		#ax8.set_xlabel('False Positive Rate',fontsize=20)

		#ax8.set_xscale("log")
		#ax8.set_yscale("log")
		#ax8.legend(loc=4,fontsize=20)

		ax7.set_title('ROC Curve',fontsize=20)
		ax7.plot(fpr, tpr, label = 'Random Forest (RF)')
		#ax7.plot(fpr, f(fpr,*popt), label='RF fit: a=%5.3f, b=%5.3f' % tuple(popt))
		ax7.plot(fpr2, tpr2, label = '"Traditional" Zcut')
		ax7.set_xlim([0.0000001, 1])
		ax7.set_ylim([0.1, 1])
		ax7.set_ylabel('True Positive Rate',fontsize=20)
		ax7.set_xlabel('False Positive Rate',fontsize=20)
		ax7.legend(loc=4,fontsize=20)

		ax7.set_xscale("log")
		ax7.set_yscale("log")

		print("ROC Curve Comparison Complete.")

		pp.savefig(fig2)
	pp.close()
	return clf_cut, tpr_at_threshold

def MakeZPlots(X, Y, y_predictions_proba, uncVZi=0, minVZ=-4.3, maxVZ=80, 
	threshold_min=0.9, nBins=100, PDFbasename=""):
	PDFbasename = PDFbasename + "_zplots"
	PDFname = PDFbasename + ".pdf"
	pp = PdfPages(PDFname)

	fig, ((ax0, ax1),(ax2, ax3),(ax4, ax5)) = plt.subplots(nrows=3, ncols=2, figsize=(20,24))
	#ax0.scatter(y_predictions_proba[:,1], X[:,uncVZi], c=Y[:,0], alpha=0.6)
	#ax1.scatter(y_predictions_proba[:,1], X[:,uncVZi], c=Y[:,0], alpha=0.6)
	ax0.set_xlim(0,1)
	ax0.set_ylim(minVZ, maxVZ)
	ax0.set_xlabel("Classifier Output", fontsize=20)
	ax0.set_ylabel("Measured Decay Length (mm)", fontsize=20)
	ax1.set_xlabel("Classifier Output", fontsize=20)
	ax1.set_ylabel("Measured Decay Length (mm)", fontsize=20)
	ax1.set_xlim(threshold_min,1)
	ax1.set_ylim(minVZ, maxVZ)

	ax2.hist2d(y_predictions_proba[:,1][Y[:,0] == 1], X[:,uncVZi][Y[:,0] == 1], bins=nBins, range=[[0,1],[minVZ, maxVZ]], alpha=0.6, cmin=0.5)
	ax3.hist2d(y_predictions_proba[:,1][Y[:,0] == 1], X[:,uncVZi][Y[:,0] == 1], bins=nBins, range=[[threshold_min,1],[minVZ, maxVZ]], alpha=0.6, cmin=0.5)
	ax2.set_xlabel("Classifier Output", fontsize=20)
	ax2.set_ylabel("Measured Decay Length (mm)", fontsize=20)
	ax2.set_title("Signal", fontsize=20)
	ax3.set_xlabel("Classifier Output", fontsize=20)
	ax3.set_ylabel("Measured Decay Length (mm)", fontsize=20)
	ax3.set_title("Signal", fontsize=20)

	ax4.hist2d(y_predictions_proba[:,1][Y[:,0] == 0], X[:,uncVZi][Y[:,0] == 0], bins=nBins, range=[[0,1],[minVZ, maxVZ]], alpha=0.6, cmin=0.5, norm=LogNorm())
	ax5.hist2d(y_predictions_proba[:,1][Y[:,0] == 0], X[:,uncVZi][Y[:,0] == 0], bins=nBins, range=[[threshold_min,1],[minVZ, maxVZ]], alpha=0.6, cmin=0.5)
	ax4.set_xlabel("Classifier Output", fontsize=20)
	ax4.set_ylabel("Measured Decay Length (mm)", fontsize=20)
	ax4.set_title("Background", fontsize=20)
	ax5.set_xlabel("Classifier Output", fontsize=20)
	ax5.set_ylabel("Measured Decay Length (mm)", fontsize=20)
	ax5.set_title("Background", fontsize=20)

	#ax4.set_zscale("log")
	ax4.set_xlabel("Classifier Output", fontsize=25)
	ax4.set_ylabel("Measured Decay Length (mm)", fontsize=25)
	ax4.set_title("Background", fontsize=30)

	pp.savefig(fig)
	pp.close()

def MakePhysicsPlots(X, Y, y_predictions, y_predictions_proba, param_list, 
	param_min, param_max, uncVZi=0, clf_cut=0.5, threshold_min=0.9, nBins=100, PDFbasename=""):
	PDFbasename = PDFbasename + "_physicsplots"
	PDFname = PDFbasename + ".pdf"
	pp = PdfPages(PDFname)

	i = 0
	for name in param_list:
		fig, ((ax0, ax1),(ax2, ax3), (ax4, ax5)) = plt.subplots(nrows=3, ncols=2, figsize=(20,24))
		fig2, ((ax6, ax7), (ax8, ax9), (ax10, ax11)) = plt.subplots(nrows=3, ncols=2, figsize=(20,24))

		ax0.hist(X[:, i][Y[:,0] == 0], bins=150, alpha=0.8, range=(param_min[i], param_max[i]), histtype="stepfilled", label="Background")
		ax0.hist(X[:, i][Y[:,0] == 1], bins=150, alpha=0.8, range=(param_min[i], param_max[i]), histtype="stepfilled", label="Signal")
		ax1.hist(X[:, i][y_predictions_proba[:,1] < clf_cut], bins=150, alpha=0.8, range=(param_min[i], param_max[i]), histtype="stepfilled", label="Identified as Background")
		ax1.hist(X[:, i][y_predictions_proba[:,1] > clf_cut], bins=150, alpha=0.8, range=(param_min[i], param_max[i]), histtype="stepfilled", label="Identified as Signal")

		ax0.set_title(name, fontsize=20)
		ax0.set_xlabel(name, fontsize=20)
		ax0.legend(loc=2)
		ax1.set_title(name, fontsize=20)
		ax1.set_xlabel(name, fontsize=20)
		ax1.legend(loc=2)
    
		ax2.scatter(X[:, i], X[:, uncVZi], c=y_predictions,label = name)
		ax3.scatter(X[:, i], X[:, uncVZi], c=y_predictions_proba[:,1] > clf_cut,label = name)
    
		ax2.set_title('Signal and Background', fontsize=20)
		ax2.set_xlabel(name, fontsize=20)
		ax2.set_ylabel('Measured Decay Length (mm)', fontsize=20)  
		ax2.set_xlim(param_min[i], param_max[i])
		ax2.set_ylim(param_min[uncVZi], param_max[uncVZi])
		ax3.set_title('Identified Signal and Background', fontsize=20)
		ax3.set_xlabel(name, fontsize=20)
		ax3.set_ylabel('Measured Decay Length (mm)', fontsize=20)
		ax3.set_xlim(param_min[i], param_max[i])
		ax3.set_ylim(param_min[uncVZi], param_max[uncVZi])
    
		ax4.hist2d(X[:, i][Y[:,0] == 0], X[:, uncVZi][Y[:,0] == 0], range=[[param_min[i], param_max[i]],[param_min[uncVZi], param_max[uncVZi]]], bins=150, alpha=0.6, label="Background", cmin=0.5)
		ax5.hist2d(X[:, i][Y[:,0] == 1], X[:, uncVZi][Y[:,0] == 1], range=[[param_min[i], param_max[i]],[param_min[uncVZi], param_max[uncVZi]]], bins=150, alpha=0.6, label="Signal", cmin=0.5)
    
		ax4.set_title('Background', fontsize=20)
		ax4.set_xlabel(name, fontsize=20)
		ax4.set_ylabel('Measured Decay Length (mm)', fontsize=20)
		ax5.set_title('Signal', fontsize=20)
		ax5.set_xlabel(name, fontsize=20)
		ax5.set_ylabel('Measured Decay Length (mm)', fontsize=20)
    
		ax6.hist2d(X[:, i][y_predictions_proba[:,1] < clf_cut], X[:, uncVZi][y_predictions_proba[:,1] < clf_cut], range=[[param_min[i], param_max[i]],[param_min[uncVZi], param_max[uncVZi]]], bins=150, alpha=0.6, label="Identified as Background", cmin=0.5)
		ax7.hist2d(X[:, i][y_predictions_proba[:,1] > clf_cut], X[:, uncVZi][y_predictions_proba[:,1] > clf_cut], range=[[param_min[i], param_max[i]],[param_min[uncVZi], param_max[uncVZi]]], bins=150, alpha=0.6, label="Identified as Signal", cmin=0.5)
    
		ax6.set_title('Identified Background', fontsize=20)
		ax6.set_xlabel(name, fontsize=20)
		ax6.set_ylabel('Measured Decay Length (mm)', fontsize=20)
		ax7.set_title('Identified Signal', fontsize=20)
		ax7.set_xlabel(name, fontsize=20)
		ax7.set_ylabel('Measured Decay Length (mm)', fontsize=20)
    
		ax8.hist2d(y_predictions_proba[:,1][Y[:,0] == 0], X[:, i][Y[:,0] == 0], range=[[0,1],[param_min[i], param_max[i]]], bins=150, alpha=0.6, label="Background", cmin=0.5)
		ax9.hist2d(y_predictions_proba[:,1][Y[:,0] == 1], X[:, i][Y[:,0] == 1], range=[[0,1],[param_min[i], param_max[i]]], bins=150, alpha=0.6, label="Signal", cmin=0.5)
    
		ax8.set_title('Background', fontsize=20)
		ax8.set_xlabel('Classifier Output', fontsize=20)
		ax8.set_ylabel(name, fontsize=20)
		ax9.set_title('Signal', fontsize=20)
		ax9.set_xlabel('Classifier Output', fontsize=20)
		ax9.set_ylabel(name, fontsize=20)
    
		ax10.hist2d(y_predictions_proba[:,1][Y[:,0] == 0], X[:, i][Y[:,0] == 0], range=[[threshold_min,1],[param_min[i], param_max[i]]], bins=150, alpha=0.6, label="Background", cmin=0.5)
		ax11.hist2d(y_predictions_proba[:,1][Y[:,0] == 1], X[:, i][Y[:,0] == 1], range=[[threshold_min,1],[param_min[i], param_max[i]]], bins=150, alpha=0.6, label="Signal", cmin=0.5)
    
		ax10.set_title('Background', fontsize=20)
		ax10.set_xlabel('Classifier Output', fontsize=20)
		ax10.set_ylabel(name, fontsize=20)
		ax11.set_title('Signal', fontsize=20)
		ax11.set_xlabel('Classifier Output', fontsize=20)
		ax11.set_ylabel(name, fontsize=20)
    
		i = i + 1
		pp.savefig(fig)
		pp.savefig(fig2)
	pp.close()