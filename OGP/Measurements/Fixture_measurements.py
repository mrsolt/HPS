import numpy as np
import math
import Al_utils

def get_oriball():
	oriball = np.empty([3])
	oriball[0] = Al_utils.getAvg(np.array(310.94616))
	oriball[1] = Al_utils.getAvg(np.array(-010.32844))
	oriball[2] = Al_utils.getAvg(np.array(-005.97164))
	return oriball

def get_diagball():
	diagball = np.empty([3])
	diagball[0] = Al_utils.getAvg(np.array(307.50722))
	diagball[1] = Al_utils.getAvg(np.array(-035.30469))
	diagball[2] = Al_utils.getAvg(np.array(-031.36259))
	return diagball

def get_axiball():
	axiball = np.empty([3])
	axiball[0] = Al_utils.getAvg(np.array(-001.09806))
	axiball[1] = Al_utils.getAvg(np.array(032.33209))
	axiball[2] = Al_utils.getAvg(np.array(-005.93123))
	return axiball

def get_fixbasis():
	return Al_utils.make_basis(get_oriball(),get_axiball(),get_diagball())

def get_base_plane():
	base_plane = np.array([5])
	base_plane = []
	base_plane[0] = Al_utils.getAvg(np.array(131.00182))
	base_plane[1] = Al_utils.getAvg(np.array(041.48503))
	base_plane[2] = Al_utils.getAvg(np.array(-022.66134))
	base_plane[3] = Al_utils.getAvg(np.array(-090.01501))
	base_plane[4] = Al_utils.getAvg(np.array(044.82793))
	return base_plane

def get_normal_base_plane():
	return Al_utils.normal_vector(math.radians(get_base_plane()[3]),math.radians(get_base_plane()[4]))

def get_oripin():
	slotpin_center = np.empty([3])
	slotpin_center[0] = Al_utils.getAvg(np.array(183.78659))
	slotpin_center[1] = Al_utils.getAvg(np.array(039.45869))
	slotpin_center[2] = Al_utils.getAvg(np.array(-021.06598))
	return Al_utils.project_point_to_plane(slotpin_center,np.array([get_base_plane()[0],get_base_plane()[1],get_base_plane()[2]]),get_normal_base_plane())
	#return slotpin_center
	#return project_pin_to_base(slotpin_center,base_plane)

def get_axipin():
	holepin_center = np.empty([3])
	holepin_center[0] = Al_utils.getAvg(np.array(074.57738))
	holepin_center[1] = Al_utils.getAvg(np.array(039.54237))
	holepin_center[2] = Al_utils.getAvg(np.array(-021.12858))
	return Al_utils.project_point_to_plane(holepin_center,np.array([get_base_plane()[0],get_base_plane()[1],get_base_plane()[2]]),get_normal_base_plane())
	#return holepin_center
	#return project_pin_to_base(holepin_center,base_normal)

def get_pin_basis_top():
	return Al_utils.make_pin_basis(get_oripin(),get_axipin(),get_normal_base_plane())

def get_pin_basis_bot():
	return Al_utils.make_pin_basis(get_axipin(),get_oripin(),get_normal_base_plane())


