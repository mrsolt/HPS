import numpy as np
import math
import Al_utils

def change_to_uchannel_basis(arr):
	array = np.copy(arr)
	rot = np.array([[0,1,0],[-1,0,0],[0,0,1]])
	trans = (get_L1_bottom_slot_cone_draw()+get_L1_bottom_hole_cone_draw())/2.
	return (rot).dot(array-trans)

def get_L1_bottom_slot_cone_draw():
	L1_bottom_slot_cone_draw = np.empty([3])
	L1_bottom_slot_cone_draw[0] = 0.
	L1_bottom_slot_cone_draw[1] = 0.
	L1_bottom_slot_cone_draw[2] = 0.
	return L1_bottom_slot_cone_draw

def get_L1_bottom_hole_cone_draw():
	L1_bottom_hole_cone_draw = np.empty([3])
	L1_bottom_hole_cone_draw[0] = 228.587
	L1_bottom_hole_cone_draw[1] = 0.
	L1_bottom_hole_cone_draw[2] = 0.
	return L1_bottom_hole_cone_draw

def get_L1_bottom_slot_cone():
	L1_bottom_slot_cone = np.empty([3])
	L1_bottom_slot_cone[0] = 0.
	L1_bottom_slot_cone[1] = 0.
	L1_bottom_slot_cone[2] = 0.
	return change_to_uchannel_basis(L1_bottom_slot_cone)

def get_L1_bottom_hole_cone():
	L1_bottom_hole_cone = np.empty([3])
	L1_bottom_hole_cone[0] = 228.587
	L1_bottom_hole_cone[1] = 0.
	L1_bottom_hole_cone[2] = 0.
	return change_to_uchannel_basis(L1_bottom_hole_cone)

def get_L3_bottom_slot_cone():
	L3_bottom_slot_cone = np.empty([3])
	L3_bottom_slot_cone[0] = 0.
	L3_bottom_slot_cone[1] = 200.
	L3_bottom_slot_cone[2] = 0.
	return change_to_uchannel_basis(L3_bottom_slot_cone)

def get_L3_bottom_hole_cone():
	L3_bottom_hole_cone = np.empty([3])
	L3_bottom_hole_cone[0] = 228.587
	L3_bottom_hole_cone[1] = 200.
	L3_bottom_hole_cone[2] = 0.
	return change_to_uchannel_basis(L3_bottom_hole_cone)

def get_beam_bottom_L0():
	beam_bottom_L0 = np.empty([3])
	beam_bottom_L0[0] = 85.966
	beam_bottom_L0[1] = -46.0186
	beam_bottom_L0[2] = 8.423
	return change_to_uchannel_basis(beam_bottom_L0)

def get_beam_bottom_L1():
	beam_bottom_L1 = np.empty([3])
	beam_bottom_L1[0] = 86.195
	beam_bottom_L1[1] = 3.981
	beam_bottom_L1[2] = 8.067
	return change_to_uchannel_basis(beam_bottom_L1)

def get_L0_bottom_slot_pin():
	L0_bottom_slot_pin = np.empty([3])
	L0_bottom_slot_pin[0] = 31.020
	L0_bottom_slot_pin[1] = -49.987
	L0_bottom_slot_pin[2] = -43.091
	return change_to_uchannel_basis(L0_bottom_slot_pin)

def get_L0_bottom_hole_pin():
	L0_bottom_hole_pin = np.empty([3])
	L0_bottom_hole_pin[0] = 140.239
	L0_bottom_hole_pin[1] = -49.987
	L0_bottom_hole_pin[2] = -43.091
	return change_to_uchannel_basis(L0_bottom_hole_pin)

def get_L1_bottom_slot_pin():
	L1_bottom_slot_pin = np.empty([3])
	L1_bottom_slot_pin[0] = 31.248
	L1_bottom_slot_pin[1] = 0.013
	L1_bottom_slot_pin[2] = -43.447
	return change_to_uchannel_basis(L1_bottom_slot_pin)

def get_L1_bottom_hole_pin():
	L1_bottom_hole_pin = np.empty([3])
	L1_bottom_hole_pin[0] = 140.468
	L1_bottom_hole_pin[1] = 0.013
	L1_bottom_hole_pin[2] = -43.447
	return change_to_uchannel_basis(L1_bottom_hole_pin)

def get_L1_top_slot_cone():
	L1_top_slot_cone = np.empty([3])
	L1_top_slot_cone[0] = 0.
	L1_top_slot_cone[1] = 0.
	L1_top_slot_cone[2] = 0.
	return L1_top_slot_cone

def get_L1_top_hole_cone():
	L1_top_hole_cone = np.empty([3])
	L1_top_hole_cone[0] = 228.587
	L1_top_hole_cone[1] = 0.
	L1_top_hole_cone[2] = 0.
	return change_to_uchannel_basis(L1_top_hole_cone)

def get_L3_top_slot_cone():
	L3_top_slot_cone = np.empty([3])
	L3_top_slot_cone[0] = 0.
	L3_top_slot_cone[1] = 200.
	L3_top_slot_cone[2] = 0.
	return change_to_uchannel_basis(L3_top_slot_cone)

def get_L3_top_hole_cone():
	L3_top_hole_cone = np.empty([3])
	L3_top_hole_cone[0] = 228.587
	L3_top_hole_cone[1] = 200.
	L3_top_hole_cone[2] = 0.
	return change_to_uchannel_basis(L3_top_hole_cone)

def get_beam_top_L0():
	beam_top_L0 = np.empty([3])
	beam_top_L0[0] = 142.621
	beam_top_L0[1] = -53.957
	beam_top_L0[2] = 8.423
	return change_to_uchannel_basis(beam_top_L0)

def get_beam_top_L1():
	beam_top_L1 = np.empty([3])
	beam_top_L1[0] = 142.392
	beam_top_L1[1] = -3.956
	beam_top_L1[2] = 8.067
	return change_to_uchannel_basis(beam_top_L1)

def get_L0_top_slot_pin():
	L0_top_slot_pin = np.empty([3])
	L0_top_slot_pin[0] = 88.348
	L0_top_slot_pin[1] = -49.987
	L0_top_slot_pin[2] = -43.091
	return change_to_uchannel_basis(L0_top_slot_pin)

def get_L0_top_hole_pin():
	L0_top_hole_pin = np.empty([3])
	L0_top_hole_pin[0] = 197.569
	L0_top_hole_pin[1] = -49.987
	L0_top_hole_pin[2] = -43.091
	return change_to_uchannel_basis(L0_top_hole_pin)

def get_L1_top_slot_pin():
	L1_top_slot_pin = np.empty([3])
	L1_top_slot_pin[0] = 88.119
	L1_top_slot_pin[1] = 0.013
	L1_top_slot_pin[2] = -43.447
	return change_to_uchannel_basis(L1_top_slot_pin)

def get_L1_top_hole_pin():
	L1_top_hole_pin = np.empty([3])
	L1_top_hole_pin[0] = 197.339
	L1_top_hole_pin[1] = 0.013
	L1_top_hole_pin[2] = -43.447
	return change_to_uchannel_basis(L1_top_hole_pin)

def get_global_L0t_axial():
	L0t_axial = np.empty([3])
	L0t_axial[0] = 1.1566
	L0t_axial[1] = 7.7625
	L0t_axial[2] = 38.362
	return L0t_axial

def get_global_L0t_stereo():
	L0t_stereo = np.empty([3])
	L0t_stereo[0] = 2.1622
	L0t_stereo[1] = 7.7237
	L0t_stereo[2] = 45.929
	return L0t_stereo

def get_global_L0b_axial():
	L0b_axial = np.empty([3])
	L0b_axial[0] = 1.8596
	L0b_axial[1] = -7.7625
	L0b_axial[2] = 61.589
	return L0b_axial

def get_global_L0b_stereo():
	L0b_stereo = np.empty([3])
	L0b_stereo[0] = 2.4023
	L0b_stereo[1] = -7.7237
	L0b_stereo[2] = 53.975
	return L0b_stereo

def get_global_L1t_axial():
	L1t_axial = np.empty([3])
	L1t_axial[0] = 2.4281
	L1t_axial[1] = 8.0625
	L1t_axial[2] = 88.346
	return L1t_axial

def get_global_L1t_stereo():
	L1t_stereo = np.empty([3])
	L1t_stereo[0] = 3.4338
	L1t_stereo[1] = 8.0237
	L1t_stereo[2] = 95.914
	return L1t_stereo

def get_global_L1b_axial():
	L1b_axial = np.empty([3])
	L1b_axial[0] = 3.1365
	L1b_axial[1] = -8.0625
	L1b_axial[2] = 111.57
	return L1b_axial

def get_global_L1b_stereo():
	L1b_stereo = np.empty([3])
	L1b_stereo[0] = 3.6792
	L1b_stereo[1] = -8.0237
	L1b_stereo[2] = 103.96
	return L1b_stereo

def get_L2t_physical():
	return 1.296

def get_L2b_physical():
	return -1.296

def get_L3t_physical():
	return 2.796

def get_L3b_physical():
	return -2.796