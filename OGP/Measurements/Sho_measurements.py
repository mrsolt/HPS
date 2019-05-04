import numpy as np
import math
import Al_utils

null_basis = Al_utils.make_basis(np.array([0.0, 0.0, 0.0]), #ball basis in ball frame
		np.array([1.0, 0.0, 0.0]),
		np.array([0.0, 1.0, 0.0]))

def get_L1_hole_ball_top():
	L1_hole_ball_top = np.empty([3])
	L1_hole_ball_top[0] = 0000.0334
	L1_hole_ball_top[1] = -0000.0114
	L1_hole_ball_top[2] = -0000.3202
	return L1_hole_ball_top

def get_L3_hole_ball_top():
	L3_hole_ball_top = np.empty([3])
	L3_hole_ball_top[0] = 0000.0818
	L3_hole_ball_top[1] = 0200.0064
	L3_hole_ball_top[2] = -0000.3454
	return L3_hole_ball_top

def get_L3_slot_ball_top():
	L3_slot_ball_top = np.empty([3])
	L3_slot_ball_top[0] = 0236.9037
	L3_slot_ball_top[1] = 0200.0143
	L3_slot_ball_top[2] = -0000.2989
	return L3_slot_ball_top

def get_L1_slot_ball_top():
	L1_slot_ball_top = np.empty([3])
	L1_slot_ball_top[0] = 0236.9279
	L1_slot_ball_top[1] = -0000.0069
	L1_slot_ball_top[2] = -0000.2589
	return L1_slot_ball_top

def get_L2_axial_top_origin():
	L2_axial_top_origin = np.empty([3])
	L2_axial_top_origin[0] = 0074.0304
	L2_axial_top_origin[1] = 0095.8261
	L2_axial_top_origin[2] = 0006.5138
	return L2_axial_top_origin

def get_L2_stereo_top_origin():
	L2_stereo_top_origin = np.empty([3])
	L2_stereo_top_origin[0] = 0074.0203
	L2_stereo_top_origin[1] = 0104.4187
	L2_stereo_top_origin[2] = 0011.1575
	return L2_stereo_top_origin

def get_L3_axial_top_origin():
	L3_axial_top_origin = np.empty([3])
	L3_axial_top_origin[0] = 0073.9407
	L3_axial_top_origin[1] = 0196.0696
	L3_axial_top_origin[2] = 0000.0026
	return L3_axial_top_origin

def get_L3_stereo_top_origin():
	L3_stereo_top_origin = np.empty([3])
	L3_stereo_top_origin[0] = 0073.8904
	L3_stereo_top_origin[1] = 0204.2933
	L3_stereo_top_origin[2] = 0009.6764
	return L3_stereo_top_origin

def get_L1_hole_ball_bottom():
	L1_hole_ball_bottom = np.empty([3])
	L1_hole_ball_bottom[0] = 0236.6762
	L1_hole_ball_bottom[1] = 0000.0117
	L1_hole_ball_bottom[2] = -0000.2109
	return L1_hole_ball_bottom

def get_L3_hole_ball_bottom():
	L3_hole_ball_bottom = np.empty([3])
	L3_hole_ball_bottom[0] = 236.5985
	L3_hole_ball_bottom[1] = 0200.0085
	L3_hole_ball_bottom[2] = -0000.1959
	return L3_hole_ball_bottom

def get_L3_slot_ball_bottom():
	L3_slot_ball_bottom = np.empty([3])
	L3_slot_ball_bottom[0] = 0000.1013
	L3_slot_ball_bottom[1] = 0200.0025
	L3_slot_ball_bottom[2] = -0000.1672
	return L3_slot_ball_bottom

def get_L1_slot_ball_bottom():
	L1_slot_ball_bottom = np.empty([3])
	L1_slot_ball_bottom[0] = 0000.0141
	L1_slot_ball_bottom[1] = -0000.0139
	L1_slot_ball_bottom[2] = -0000.1482
	return L1_slot_ball_bottom

def get_L2_axial_bottom_origin():
	L2_axial_bottom_origin = np.empty([3])
	L2_axial_bottom_origin[0] = 0016.0664
	L2_axial_bottom_origin[1] = 0104.0344
	L2_axial_bottom_origin[2] = 0006.4833
	return L2_axial_bottom_origin

def get_L2_stereo_bottom_origin():
	L2_stereo_bottom_origin = np.empty([3])
	L2_stereo_bottom_origin[0] = 0015.5825
	L2_stereo_bottom_origin[1] = 0095.8391
	L2_stereo_bottom_origin[2] = 0002.1365
	return L2_stereo_bottom_origin

def get_L3_axial_bottom_origin():
	L3_axial_bottom_origin = np.empty([3])
	L3_axial_bottom_origin[0] = 0015.9962
	L3_axial_bottom_origin[1] = 0203.8623
	L3_axial_bottom_origin[2] = 0004.9942 
	return L3_axial_bottom_origin

def get_L3_stereo_bottom_origin():
	L3_stereo_bottom_origin = np.empty([3])
	L3_stereo_bottom_origin[0] = 0016.0508 
	L3_stereo_bottom_origin[1] = 0195.8337 
	L3_stereo_bottom_origin[2] = 0000.6187
	return L3_stereo_bottom_origin

def make_uch_basis(holeupst,holedownst,slotupst,slotdownst):
	upst_mid = (holeupst+slotupst)/2.0
	downst_mid = (holedownst+slotdownst)/2.0
	upst_vec = (slotupst-holeupst)
	downst_vec = (slotdownst-holedownst)
	upst_vec = upst_vec/np.linalg.norm(upst_vec)
	downst_vec = downst_vec/np.linalg.norm(downst_vec)
	basis = np.empty([3,3])

	basis[0] = upst_vec+downst_vec
	basis[2] = downst_mid-upst_mid
	basis[2] = Al_utils.orthogonalize(basis[0],basis[2])
	basis[1] = np.cross(basis[2],basis[0])

	#basis[0] = downst_mid-upst_mid
	#basis[1] = upst_vec+downst_vec
	#basis[1] = orthogonalize(basis[0],basis[1])
	#basis[2] = np.cross(basis[0],basis[1])

	basis[0] = basis[0]/np.linalg.norm(basis[0])
	basis[1] = basis[1]/np.linalg.norm(basis[1])
	basis[2] = basis[2]/np.linalg.norm(basis[2])
	return [upst_mid,basis,holeupst,holedownst,slotupst,slotdownst]

uchannel_basis_top_sho = make_uch_basis(get_L1_hole_ball_top(),get_L3_hole_ball_top(),get_L1_slot_ball_top(),get_L3_slot_ball_top())
uchannel_basis_top = Al_utils.make_uch_basis(get_L1_hole_ball_top(),get_L3_hole_ball_top(),get_L1_slot_ball_top(),get_L3_slot_ball_top())

print uchannel_basis_top
print uchannel_basis_top_sho

uchannel_basis_bot_sho = make_uch_basis(get_L1_hole_ball_bottom(),get_L3_hole_ball_bottom(),get_L1_slot_ball_bottom(),get_L3_slot_ball_bottom())
uchannel_basis_bot = Al_utils.make_uch_basis(get_L1_hole_ball_bottom(),get_L3_hole_ball_bottom(),get_L1_slot_ball_bottom(),get_L3_slot_ball_bottom())

uchannel_basis_top_shift = Al_utils.transform_basis(uchannel_basis_top_sho,null_basis,uchannel_basis_top)
uchannel_basis_bot_shift = Al_utils.transform_basis(uchannel_basis_bot_sho,null_basis,uchannel_basis_bot)

print uchannel_basis_top_shift 

print str((uchannel_basis_top_sho[1].dot((get_L2_axial_top_origin() - uchannel_basis_top_sho[0]))).dot(uchannel_basis_top_shift[1])+uchannel_basis_top_shift[0])

def get_L2_axial_top():
	return Al_utils.transform_pt(uchannel_basis_top_shift,uchannel_basis_top,get_L2_axial_top_origin())

def get_L2_stereo_top():
	return Al_utils.transform_pt(uchannel_basis_top_shift,uchannel_basis_top,get_L2_stereo_top_origin())

def get_L3_axial_top():
	return Al_utils.transform_pt(uchannel_basis_top_shift,uchannel_basis_top,get_L3_axial_top_origin())

def get_L3_stereo_top():
	return Al_utils.transform_pt(uchannel_basis_top_shift,uchannel_basis_top,get_L3_stereo_top_origin())

def get_L2_axial_bot():
	return Al_utils.transform_pt(uchannel_basis_bot_shift,uchannel_basis_bot,get_L2_axial_bottom_origin())

def get_L2_stereo_bot():
	return Al_utils.transform_pt(uchannel_basis_bot_shift,uchannel_basis_bot,get_L2_stereo_bottom_origin())

def get_L3_axial_bot():
	return Al_utils.transform_pt(uchannel_basis_bot_shift,uchannel_basis_bot,get_L3_axial_bottom_origin())

def get_L3_stereo_bot():
	return Al_utils.transform_pt(uchannel_basis_bot_shift,uchannel_basis_bot,get_L3_stereo_bottom_origin())

print get_L2_axial_top()
print get_L2_stereo_top()
print get_L3_axial_top()
print get_L3_stereo_top()

print get_L2_axial_bot()
print get_L2_stereo_bot()
print get_L3_axial_bot()
print get_L3_stereo_bot()