import numpy as np
import math
import Al_utils

def get_L1_hole_ball():
	L1_hole_ball = np.empty([3])
	L1_hole_ball[0] = Al_utils.getAvg(np.array([228.01042]))
	L1_hole_ball[1] = Al_utils.getAvg(np.array([095.26798]))
	L1_hole_ball[2] = Al_utils.getAvg(np.array([-005.16258]))
	return L1_hole_ball

def get_L3_hole_ball():
	L3_hole_ball = np.empty([3])
	L3_hole_ball[0] = Al_utils.getAvg(np.array([227.42535]))
	L3_hole_ball[1] = Al_utils.getAvg(np.array([295.25953]))
	L3_hole_ball[2] = Al_utils.getAvg(np.array([-005.11076]))
	return L3_hole_ball

def get_L3_slot_ball():
	L3_slot_ball = np.empty([3])
	L3_slot_ball[0] = Al_utils.getAvg(np.array([-009.09437]))
	L3_slot_ball[1] = Al_utils.getAvg(np.array([294.63087]))
	L3_slot_ball[2] = Al_utils.getAvg(np.array([-005.05414]))
	return L3_slot_ball

def get_L1_slot_ball():
	L1_slot_ball = np.empty([3])
	L1_slot_ball[0] = Al_utils.getAvg(np.array([-008.64929]))
	L1_slot_ball[1] = Al_utils.getAvg(np.array([094.62686]))
	L1_slot_ball[2] = Al_utils.getAvg(np.array([-005.09499]))
	return L1_slot_ball

def get_ubasis():
	return Al_utils.make_uch_basis(get_L1_hole_ball(),get_L3_hole_ball(),get_L1_slot_ball(),get_L3_slot_ball())

def get_ball_plane():
	ball_plane = np.empty([5])
	ball_plane[0] = Al_utils.getAvg(np.array([138.71886]))
	ball_plane[1] = Al_utils.getAvg(np.array([-089.97994]))
	ball_plane[2] = Al_utils.getAvg(np.array([109.42303]))
	ball_plane[3] = Al_utils.getAvg(np.array([194.94631]))
	ball_plane[4] = Al_utils.getAvg(np.array([-005.10562]))
	return ball_plane

def get_ball_plane_normal():
	return normal_vector(math.radians(ball_plane()[3]),math.radians(ball_plane()[4]))

def get_L0_base_plane():
	L0_base_plane = np.empty([5])
	L0_base_plane[0] = Al_utils.getAvg(np.array([-052.85242]))
	L0_base_plane[1] = Al_utils.getAvg(np.array([033.38944]))
	L0_base_plane[2] = Al_utils.getAvg(np.array([-043.02304]))
	L0_base_plane[3] = Al_utils.getAvg(np.array([-026.69071]))
	L0_base_plane[4] = Al_utils.getAvg(np.array([089.95514]))
	return L0_base_plane

def get_L0_base_normal():
	return Al_utils.normal_vector(math.radians(get_L0_base_plane()[3]),math.radians(get_L0_base_plane()[4]))

def get_L1_base_plane():
	L1_base_plane = np.empty([5])
	L1_base_plane[0] = Al_utils.getAvg(np.array([000.16933]))
	L1_base_plane[1] = Al_utils.getAvg(np.array([028.70117]))
	L1_base_plane[2] = Al_utils.getAvg(np.array([-043.39205]))
	L1_base_plane[3] = Al_utils.getAvg(np.array([-173.04428]))
	L1_base_plane[4] = Al_utils.getAvg(np.array([-089.95476]))
	return L1_base_plane

def get_L1_base_normal():
	return Al_utils.normal_vector(math.radians(get_L1_base_plane()[3]),math.radians(get_L1_base_plane()[4]))

def get_L2_base_plane():
	L2_base_plane = np.empty([5])
	L2_base_plane[0] = Al_utils.getAvg(np.array([099.37643]))
	L2_base_plane[1] = Al_utils.getAvg(np.array([006.55192]))
	L2_base_plane[2] = Al_utils.getAvg(np.array([-052.94695]))
	L2_base_plane[3] = Al_utils.getAvg(np.array([029.38887]))
	L2_base_plane[4] = Al_utils.getAvg(np.array([089.98048]))
	return L2_base_plane

def get_L2_base_normal():
	return Al_utils.normal_vector(math.radians(get_L2_base_plane()[3]),math.radians(get_L2_base_plane()[4]))

def get_L3_base_plane():
	L3_base_plane = np.empty([5])
	L3_base_plane[0] = Al_utils.getAvg(np.array([199.20859]))
	L3_base_plane[1] = Al_utils.getAvg(np.array([004.68735]))
	L3_base_plane[2] = Al_utils.getAvg(np.array([-054.42996]))
	L3_base_plane[3] = Al_utils.getAvg(np.array([169.79848]))
	L3_base_plane[4] = Al_utils.getAvg(np.array([089.97868]))
	return L3_base_plane

def get_L3_base_normal():
	return Al_utils.normal_vector(math.radians(get_L3_base_plane()[3]),math.radians(get_L3_base_plane()[4]))

def get_L0_slot_pin():
	L0_slot_pin = np.empty([3])
	L0_slot_pin[0] = Al_utils.getAvg(np.array([-050.06542]))
	L0_slot_pin[1] = Al_utils.getAvg(np.array([083.15080]))
	L0_slot_pin[2] = Al_utils.getAvg(np.array([-040.52812]))
	return Al_utils.project_point_to_plane(L0_slot_pin,np.array([get_L0_base_plane()[0],get_L0_base_plane()[1],get_L0_base_plane()[2]]),get_L0_base_normal())

def get_L0_hole_pin():
	L0_hole_pin = np.empty([3])
	L0_hole_pin[0] = Al_utils.getAvg(np.array([-049.95689]))
	L0_hole_pin[1] = Al_utils.getAvg(np.array([-026.08166]))
	L0_hole_pin[2] = Al_utils.getAvg(np.array([-040.53846]))
	return Al_utils.project_point_to_plane(L0_hole_pin,np.array([get_L0_base_plane()[0],get_L0_base_plane()[1],get_L0_base_plane()[2]]),get_L0_base_normal())

def get_L0_pin_basis():
	return Al_utils.make_pin_basis(get_L0_hole_pin(),get_L0_slot_pin(),get_L0_base_normal())

def get_L1_slot_pin():
	L1_slot_pin = np.empty([3])
	L1_slot_pin[0] = Al_utils.getAvg(np.array([000.08896]))
	L1_slot_pin[1] = Al_utils.getAvg(np.array([083.00259]))
	L1_slot_pin[2] = Al_utils.getAvg(np.array([-040.90393]))
	return Al_utils.project_point_to_plane(L1_slot_pin,np.array([get_L1_base_plane()[0],get_L1_base_plane()[1],get_L1_base_plane()[2]]),get_L1_base_normal())

def get_L1_hole_pin():
	L1_hole_pin = np.empty([3])
	L1_hole_pin[0] = Al_utils.getAvg(np.array([000.02759]))
	L1_hole_pin[1] = Al_utils.getAvg(np.array([-026.20199]))
	L1_hole_pin[2] = Al_utils.getAvg(np.array([-040.80448]))
	return Al_utils.project_point_to_plane(L1_hole_pin,np.array([get_L1_base_plane()[0],get_L1_base_plane()[1],get_L1_base_plane()[2]]),get_L1_base_normal())

def get_L1_pin_basis():
	return Al_utils.make_pin_basis(get_L1_hole_pin(),get_L1_slot_pin(),get_L1_base_normal())

def get_L2_slot_pin():
	L2_slot_pin = np.empty([3])
	L2_slot_pin[0] = Al_utils.getAvg(np.array([109.56114]))
	L2_slot_pin[1] = Al_utils.getAvg(np.array([095.24083]))
	L2_slot_pin[2] = Al_utils.getAvg(np.array([-050.66193]))
	return Al_utils.project_point_to_plane(L2_slot_pin,np.array([get_L2_base_plane()[0],get_L2_base_plane()[1],get_L2_base_plane()[2]]),get_L2_base_normal())

def get_L2_hole_pin():
	L2_hole_pin = np.empty([3])
	L2_hole_pin[0] = Al_utils.getAvg(np.array([109.59399]))
	L2_hole_pin[1] = Al_utils.getAvg(np.array([-095.22943]))
	L2_hole_pin[2] = Al_utils.getAvg(np.array([-050.61693]))
	return Al_utils.project_point_to_plane(L2_hole_pin,np.array([get_L2_base_plane()[0],get_L2_base_plane()[1],get_L2_base_plane()[2]]),get_L2_base_normal())

def get_L2_pin_basis():
	return Al_utils.make_pin_basis(get_L2_hole_pin(),get_L2_slot_pin(),get_L2_base_normal())

def get_L3_slot_pin():
	L3_slot_pin = np.empty([3])
	L3_slot_pin[0] = Al_utils.getAvg(np.array([209.57712]))
	L3_slot_pin[1] = Al_utils.getAvg(np.array([095.21149]))
	L3_slot_pin[2] = Al_utils.getAvg(np.array([-052.13761]))
	return Al_utils.project_point_to_plane(L3_slot_pin,np.array([get_L3_base_plane()[0],get_L3_base_plane()[1],get_L3_base_plane()[2]]),get_L3_base_normal())

def get_L3_hole_pin():
	L3_hole_pin = np.empty([3])
	L3_hole_pin[0] = Al_utils.getAvg(np.array([209.60144]))
	L3_hole_pin[1] = Al_utils.getAvg(np.array([-095.27477]))
	L3_hole_pin[2] = Al_utils.getAvg(np.array([-052.14511]))
	return Al_utils.project_point_to_plane(L3_hole_pin,np.array([get_L3_base_plane()[0],get_L3_base_plane()[1],get_L3_base_plane()[2]]),get_L3_base_normal())

def get_L3_pin_basis():
	return Al_utils.make_pin_basis(get_L3_hole_pin(),get_L3_slot_pin(),get_L3_base_normal())

def get_L0_axial_backedge():
	L0_axial_backedge = np.empty([5])
	L0_axial_backedge[0] = Al_utils.getAvg(np.array([-046.00619]))
	L0_axial_backedge[1] = Al_utils.getAvg(np.array([028.31449]))
	L0_axial_backedge[2] = Al_utils.getAvg(np.array([007.87054]))
	L0_axial_backedge[3] = Al_utils.getAvg(np.array([089.98729]))
	L0_axial_backedge[4] = Al_utils.getAvg(np.array([000.28382]))
	return L0_axial_backedge

def get_L0_axial_backedge_normal():
	return Al_utils.normal_vector(math.radians(get_L0_axial_backedge()[3]),math.radians(get_L0_axial_backedge()[4]))

def get_L0_stereo_frontedge():
	L0_stereo_frontedge = np.empty([5])
	L0_stereo_frontedge[0] = Al_utils.getAvg(np.array([-054.05355]))
	L0_stereo_frontedge[1] = Al_utils.getAvg(np.array([029.07547]))
	L0_stereo_frontedge[2] = Al_utils.getAvg(np.array([008.05889]))
	L0_stereo_frontedge[3] = Al_utils.getAvg(np.array([090.01825]))
	L0_stereo_frontedge[4] = Al_utils.getAvg(np.array([005.73210]))
	return L0_stereo_frontedge

def get_L0_stereo_frontedge_normal():
	return Al_utils.normal_vector(math.radians(get_L0_stereo_frontedge()[3]),math.radians(get_L0_stereo_frontedge()[4]))

def get_L1_axial_backedge():
	L1_axial_backedge = np.empty([5])
	L1_axial_backedge[0] = Al_utils.getAvg(np.array([004.12062]))
	L1_axial_backedge[1] = Al_utils.getAvg(np.array([027.66142]))
	L1_axial_backedge[2] = Al_utils.getAvg(np.array([007.47369]))
	L1_axial_backedge[3] = Al_utils.getAvg(np.array([089.93871]))
	L1_axial_backedge[4] = Al_utils.getAvg(np.array([000.27258]))
	return L1_axial_backedge

def get_L1_axial_backedge_normal():
	return Al_utils.normal_vector(math.radians(get_L1_axial_backedge()[3]),math.radians(get_L1_axial_backedge()[4]))

def get_L1_stereo_frontedge():
	L1_stereo_frontedge = np.empty([5])
	L1_stereo_frontedge[0] = Al_utils.getAvg(np.array([-003.90185]))
	L1_stereo_frontedge[1] = Al_utils.getAvg(np.array([026.32962]))
	L1_stereo_frontedge[2] = Al_utils.getAvg(np.array([007.43349]))
	L1_stereo_frontedge[3] = Al_utils.getAvg(np.array([-089.99489]))
	L1_stereo_frontedge[4] = Al_utils.getAvg(np.array([-005.77888]))
	return L1_stereo_frontedge

def get_L1_stereo_frontedge_normal():
	return Al_utils.normal_vector(math.radians(get_L1_stereo_frontedge()[3]),math.radians(get_L1_stereo_frontedge()[4]))

def get_L2_axial_backedge():
	L2_axial_backedge = np.empty([5])
	L2_axial_backedge[0] = Al_utils.getAvg(np.array([103.97422]))
	L2_axial_backedge[1] = Al_utils.getAvg(np.array([025.96446]))
	L2_axial_backedge[2] = Al_utils.getAvg(np.array([007.11466]))
	L2_axial_backedge[3] = Al_utils.getAvg(np.array([-090.07016]))
	L2_axial_backedge[4] = Al_utils.getAvg(np.array([000.02069]))
	return L2_axial_backedge

def get_L2_axial_backedge_normal():
	return Al_utils.normal_vector(math.radians(get_L2_axial_backedge()[3]),math.radians(get_L2_axial_backedge()[4]))

def get_L2_stereo_frontedge():
	L2_stereo_frontedge = np.empty([5])
	L2_stereo_frontedge[0] = Al_utils.getAvg(np.array([095.62154])) 
	L2_stereo_frontedge[1] = Al_utils.getAvg(np.array([023.65861]))
	L2_stereo_frontedge[2] = Al_utils.getAvg(np.array([006.69231]))
	L2_stereo_frontedge[3] = Al_utils.getAvg(np.array([090.24821]))
	L2_stereo_frontedge[4] = Al_utils.getAvg(np.array([005.70024]))
	return L2_stereo_frontedge

def get_L2_stereo_frontedge_normal():
	return Al_utils.normal_vector(math.radians(get_L2_stereo_frontedge()[3]),math.radians(get_L2_stereo_frontedge()[4]))

def get_L3_axial_backedge():
	L3_axial_backedge = np.empty([5])
	L3_axial_backedge[0] = Al_utils.getAvg(np.array([204.14190]))
	L3_axial_backedge[1] = Al_utils.getAvg(np.array([030.59347]))
	L3_axial_backedge[2] = Al_utils.getAvg(np.array([005.66258]))
	L3_axial_backedge[3] = Al_utils.getAvg(np.array([089.91021]))
	L3_axial_backedge[4] = Al_utils.getAvg(np.array([000.03891]))
	return L3_axial_backedge

def get_L3_axial_backedge_normal():
	return Al_utils.normal_vector(math.radians(get_L3_axial_backedge()[3]),math.radians(get_L3_axial_backedge()[4]))

def get_L3_stereo_frontedge():
	L3_stereo_frontedge = np.empty([5])
	L3_stereo_frontedge[0] = Al_utils.getAvg(np.array([195.61621]))
	L3_stereo_frontedge[1] = Al_utils.getAvg(np.array([031.22585]))
	L3_stereo_frontedge[2] = Al_utils.getAvg(np.array([005.99629]))
	L3_stereo_frontedge[3] = Al_utils.getAvg(np.array([089.99429]))
	L3_stereo_frontedge[4] = Al_utils.getAvg(np.array([005.74861]))
	return L3_stereo_frontedge

def get_L3_stereo_frontedge_normal():
	return Al_utils.normal_vector(math.radians(get_L3_stereo_frontedge()[3]),math.radians(get_L3_stereo_frontedge()[4]))

def get_wire_par():
	wire_par = np.empty([5])
	wire_par[0] = Al_utils.getAvg(np.array([-081.49162]))
	wire_par[1] = Al_utils.getAvg(np.array([017.13384]))
	wire_par[2] = Al_utils.getAvg(np.array([015.83889]))
	wire_par[3] = Al_utils.getAvg(np.array([-089.87309]))
	wire_par[4] = Al_utils.getAvg(np.array([000.00876]))
	return wire_par

def get_wire_par_normal():
	return Al_utils.normal_vector(math.radians(get_wire_par()[3]),math.radians(get_wire_par()[4]))

def get_wire_diag():
	wire_diag = np.empty([5])
	wire_diag[0] = Al_utils.getAvg(np.array([-081.89325]))
	wire_diag[1] = Al_utils.getAvg(np.array([016.51584]))
	wire_diag[2] = Al_utils.getAvg(np.array([015.74494]))
	wire_diag[3] = Al_utils.getAvg(np.array([-089.9457]))
	wire_diag[4] = Al_utils.getAvg(np.array([008.91128]))
	return wire_diag

def get_wire_diag_normal():
	return Al_utils.normal_vector(math.radians(get_wire_diag()[3]),math.radians(get_wire_diag()[4]))