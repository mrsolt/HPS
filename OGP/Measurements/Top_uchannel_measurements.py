import numpy as np
import math
import Al_utils

def get_L1_hole_ball():
	L1_hole_ball = np.empty([3])
	L1_hole_ball[0] = Al_utils.getAvg(np.array(-008.19979))
	L1_hole_ball[1] = Al_utils.getAvg(np.array(078.80410))
	L1_hole_ball[2] = Al_utils.getAvg(np.array(-005.08007))
	return L1_hole_ball

def get_L3_hole_ball():
	L3_hole_ball = np.empty([3])
	L3_hole_ball[0] = Al_utils.getAvg(np.array(-008.31601))
	L3_hole_ball[1] = Al_utils.getAvg(np.array(278.81141))
	L3_hole_ball[2] = Al_utils.getAvg(np.array(-005.06400))
	return L3_hole_ball

def get_L3_slot_ball():
	L3_slot_ball = np.empty([3])
	L3_slot_ball[0] = Al_utils.getAvg(np.array(228.59313))
	L3_slot_ball[1] = Al_utils.getAvg(np.array(278.97321))
	L3_slot_ball[2] = Al_utils.getAvg(np.array(-005.08610))
	return L3_slot_ball

def get_L1_slot_ball():
	L1_slot_ball = np.empty([3])
	L1_slot_ball[0] = Al_utils.getAvg(np.array(228.71093))
	L1_slot_ball[1] = Al_utils.getAvg(np.array(078.95369))
	L1_slot_ball[2] = Al_utils.getAvg(np.array(-005.12178))
	return L1_slot_ball

def get_ubasis():
	return Al_utils.make_uch_basis(get_L1_hole_ball(),get_L3_hole_ball(),get_L1_slot_ball(),get_L3_slot_ball())

def get_ball_plane():
	ball_plane = np.empty([5])
	ball_plane[0] = Al_utils.getAvg(np.array(110.19706))
	ball_plane[1] = Al_utils.getAvg(np.array(178.88560))
	ball_plane[2] = Al_utils.getAvg(np.array(-005.08799))
	ball_plane[3] = Al_utils.getAvg(np.array(136.19320))
	ball_plane[4] = Al_utils.getAvg(np.array(-089.98930))
	return ball_plane

def get_ball_plane_normal():
	return normal_vector(math.radians(ball_plane()[3]),math.radians(ball_plane()[4]))

def get_L0_base_plane():
	L0_base_plane = np.empty([5])
	L0_base_plane[0] = Al_utils.getAvg(np.array(-049.61108))
	L0_base_plane[1] = Al_utils.getAvg(np.array(-026.88467))
	L0_base_plane[2] = Al_utils.getAvg(np.array(-043.03394))
	L0_base_plane[3] = Al_utils.getAvg(np.array(-155.09495))
	L0_base_plane[4] = Al_utils.getAvg(np.array(089.91094))
	return L0_base_plane

def get_L0_base_normal():
	return Al_utils.normal_vector(math.radians(get_L0_base_plane()[3]),math.radians(get_L0_base_plane()[4]))

def get_L1_base_plane():
	L1_base_plane = np.empty([5])
	L1_base_plane[0] = Al_utils.getAvg(np.array(-000.52467))
	L1_base_plane[1] = Al_utils.getAvg(np.array(-026.86136))
	L1_base_plane[2] = Al_utils.getAvg(np.array(-043.32792))
	L1_base_plane[3] = Al_utils.getAvg(np.array(007.95920))
	L1_base_plane[4] = Al_utils.getAvg(np.array(-089.92725))
	return L1_base_plane

def get_L1_base_normal():
	return Al_utils.normal_vector(math.radians(get_L1_base_plane()[3]),math.radians(get_L1_base_plane()[4]))

def get_L2_base_plane():
	L2_base_plane = np.empty([5])
	L2_base_plane[0] = Al_utils.getAvg(np.array(099.52317))
	L2_base_plane[1] = Al_utils.getAvg(np.array(004.65000))
	L2_base_plane[2] = Al_utils.getAvg(np.array(-052.90355))
	L2_base_plane[3] = Al_utils.getAvg(np.array(-019.02397))
	L2_base_plane[4] = Al_utils.getAvg(np.array(+089.98850))
	return L2_base_plane

def get_L2_base_normal():
	return Al_utils.normal_vector(math.radians(get_L2_base_plane()[3]),math.radians(get_L2_base_plane()[4]))

def get_L3_base_plane():
	L3_base_plane = np.empty([5])
	L3_base_plane[0] = Al_utils.getAvg(np.array(200.81385))
	L3_base_plane[1] = Al_utils.getAvg(np.array(004.52916))
	L3_base_plane[2] = Al_utils.getAvg(np.array(-054.39683))
	L3_base_plane[3] = Al_utils.getAvg(np.array(057.72003))
	L3_base_plane[4] = Al_utils.getAvg(np.array(089.99680))
	return L3_base_plane

def get_L3_base_normal():
	return Al_utils.normal_vector(math.radians(get_L3_base_plane()[3]),math.radians(get_L3_base_plane()[4]))

def get_L0_slot_pin():
	L0_slot_pin = np.empty([3])
	L0_slot_pin[0] = Al_utils.getAvg(np.array(-049.99813))
	L0_slot_pin[1] = Al_utils.getAvg(np.array(-083.37671))
	L0_slot_pin[2] = Al_utils.getAvg(np.array(-040.59105))
	return Al_utils.project_point_to_plane(L0_slot_pin,np.array([get_L0_base_plane()[0],get_L0_base_plane()[1],get_L0_base_plane()[2]]),get_L0_base_normal())

def get_L0_hole_pin():
	L0_hole_pin = np.empty([3])
	L0_hole_pin[0] = Al_utils.getAvg(np.array(-050.03663))
	L0_hole_pin[1] = Al_utils.getAvg(np.array(025.87813))
	L0_hole_pin[2] = Al_utils.getAvg(np.array(-040.43726))
	return Al_utils.project_point_to_plane(L0_hole_pin,np.array([get_L0_base_plane()[0],get_L0_base_plane()[1],get_L0_base_plane()[2]]),get_L0_base_normal())

def get_L0_pin_basis():
	return Al_utils.make_pin_basis(get_L0_hole_pin(),get_L0_slot_pin(),get_L0_base_normal())

def get_L1_slot_pin():
	L1_slot_pin = np.empty([3])
	L1_slot_pin[0] = Al_utils.getAvg(np.array(-000.01248))
	L1_slot_pin[1] = Al_utils.getAvg(np.array(-082.99361))
	L1_slot_pin[2] = Al_utils.getAvg(np.array(-041.01801))
	return Al_utils.project_point_to_plane(L1_slot_pin,np.array([get_L1_base_plane()[0],get_L1_base_plane()[1],get_L1_base_plane()[2]]),get_L1_base_normal())

def get_L1_hole_pin():
	L1_hole_pin = np.empty([3])
	L1_hole_pin[0] = Al_utils.getAvg(np.array(-000.01490))
	L1_hole_pin[1] = Al_utils.getAvg(np.array(026.21862))
	L1_hole_pin[2] = Al_utils.getAvg(np.array(-040.82364))
	return Al_utils.project_point_to_plane(L1_hole_pin,np.array([get_L1_base_plane()[0],get_L1_base_plane()[1],get_L1_base_plane()[2]]),get_L1_base_normal())

def get_L1_pin_basis():
	return Al_utils.make_pin_basis(get_L1_hole_pin(),get_L1_slot_pin(),get_L1_base_normal())

def get_L2_slot_pin():
	L2_slot_pin = np.empty([3])
	L2_slot_pin[0] = Al_utils.getAvg(np.array(090.54022))
	L2_slot_pin[1] = Al_utils.getAvg(np.array(-095.18730))
	L2_slot_pin[2] = Al_utils.getAvg(np.array(-050.90029))
	return Al_utils.project_point_to_plane(L2_slot_pin,np.array([get_L2_base_plane()[0],get_L2_base_plane()[1],get_L2_base_plane()[2]]),get_L2_base_normal())

def get_L2_hole_pin():
	L2_hole_pin = np.empty([3])
	L2_hole_pin[0] = Al_utils.getAvg(np.array(090.39442))
	L2_hole_pin[1] = Al_utils.getAvg(np.array(095.27847))
	L2_hole_pin[2] = Al_utils.getAvg(np.array(-050.50742))
	return Al_utils.project_point_to_plane(L2_hole_pin,np.array([get_L2_base_plane()[0],get_L2_base_plane()[1],get_L2_base_plane()[2]]),get_L2_base_normal())

def get_L2_pin_basis():
	return Al_utils.make_pin_basis(get_L2_hole_pin(),get_L2_slot_pin(),get_L2_base_normal())

def get_L3_slot_pin():
	L3_slot_pin = np.empty([3])
	L3_slot_pin[0] = Al_utils.getAvg(np.array(190.59638))
	L3_slot_pin[1] = Al_utils.getAvg(np.array(-095.13107))
	L3_slot_pin[2] = Al_utils.getAvg(np.array(-052.28276))
	return Al_utils.project_point_to_plane(L3_slot_pin,np.array([get_L3_base_plane()[0],get_L3_base_plane()[1],get_L3_base_plane()[2]]),get_L3_base_normal())

def get_L3_hole_pin():
	L3_hole_pin = np.empty([3])
	L3_hole_pin[0] = Al_utils.getAvg(np.array(190.46626))
	L3_hole_pin[1] = Al_utils.getAvg(np.array(095.33256))
	L3_hole_pin[2] = Al_utils.getAvg(np.array(-052.22790))
	return Al_utils.project_point_to_plane(L3_hole_pin,np.array([get_L3_base_plane()[0],get_L3_base_plane()[1],get_L3_base_plane()[2]]),get_L3_base_normal())

def get_L3_pin_basis():
	return Al_utils.make_pin_basis(get_L3_hole_pin(),get_L3_slot_pin(),get_L3_base_normal())

def get_L0_axial_frontedge():
	L0_axial_frontedge = np.empty([5])
	L0_axial_frontedge[0] = Al_utils.getAvg(np.array(-054.10317))
	L0_axial_frontedge[1] = Al_utils.getAvg(np.array(-028.23454))
	L0_axial_frontedge[2] = Al_utils.getAvg(np.array(007.87369))
	L0_axial_frontedge[3] = Al_utils.getAvg(np.array(-089.99495))
	L0_axial_frontedge[4] = Al_utils.getAvg(np.array(-000.09450))
	return L0_axial_frontedge

def get_L0_axial_frontedge_normal():
	return Al_utils.normal_vector(math.radians(get_L0_axial_frontedge()[3]),math.radians(get_L0_axial_frontedge()[4]))

def get_L0_stereo_backedge():
	L0_stereo_backedge = np.empty([5])
	L0_stereo_backedge[0] = Al_utils.getAvg(np.array(-046.06317))
	L0_stereo_backedge[1] = Al_utils.getAvg(np.array(-033.23801))
	L0_stereo_backedge[2] = Al_utils.getAvg(np.array(008.43861))
	L0_stereo_backedge[3] = Al_utils.getAvg(np.array(090.03305))
	L0_stereo_backedge[4] = Al_utils.getAvg(np.array(-005.86217))
	return L0_stereo_backedge

def get_L0_stereo_backedge_normal():
	return Al_utils.normal_vector(math.radians(get_L0_stereo_backedge()[3]),math.radians(get_L0_stereo_backedge()[4]))

def get_L1_axial_frontedge():
	L1_axial_frontedge = np.empty([5])
	L1_axial_frontedge[0] = Al_utils.getAvg(np.array(-004.12675))
	L1_axial_frontedge[1] = Al_utils.getAvg(np.array(-029.39622))
	L1_axial_frontedge[2] = Al_utils.getAvg(np.array(007.65318))
	L1_axial_frontedge[3] = Al_utils.getAvg(np.array(089.99464))
	L1_axial_frontedge[4] = Al_utils.getAvg(np.array(-000.13704))
	return L1_axial_frontedge

def get_L1_axial_frontedge_normal():
	return Al_utils.normal_vector(math.radians(get_L1_axial_frontedge()[3]),math.radians(get_L1_axial_frontedge()[4]))

def get_L1_stereo_backedge():
	L1_stereo_backedge = np.empty([5])
	L1_stereo_backedge[0] = Al_utils.getAvg(np.array(003.85449))
	L1_stereo_backedge[1] = Al_utils.getAvg(np.array(-030.54125))
	L1_stereo_backedge[2] = Al_utils.getAvg(np.array(007.95288))
	L1_stereo_backedge[3] = Al_utils.getAvg(np.array(-090.05359))
	L1_stereo_backedge[4] = Al_utils.getAvg(np.array(005.82243))
	return L1_stereo_backedge

def get_L1_stereo_backedge_normal():
	return Al_utils.normal_vector(math.radians(get_L1_stereo_backedge()[3]),math.radians(get_L1_stereo_backedge()[4]))

def get_L2_axial_frontedge():
	L2_axial_frontedge = np.empty([5])
	L2_axial_frontedge[0] = Al_utils.getAvg(np.array(095.83884))
	L2_axial_frontedge[1] = Al_utils.getAvg(np.array(-030.49663))
	L2_axial_frontedge[2] = Al_utils.getAvg(np.array(007.18202))
	L2_axial_frontedge[3] = Al_utils.getAvg(np.array(-090.03573))
	L2_axial_frontedge[4] = Al_utils.getAvg(np.array(-000.00170))
	return L2_axial_frontedge

def get_L2_axial_frontedge_normal():
	return Al_utils.normal_vector(math.radians(get_L2_axial_frontedge()[3]),math.radians(get_L2_axial_frontedge()[4]))

def get_L2_stereo_backedge():
	L2_stereo_backedge = np.empty([5])
	L2_stereo_backedge[0] = Al_utils.getAvg(np.array(104.55273))
	L2_stereo_backedge[1] = Al_utils.getAvg(np.array(-029.05215))
	L2_stereo_backedge[2] = Al_utils.getAvg(np.array(007.32574))
	L2_stereo_backedge[3] = Al_utils.getAvg(np.array(090.08280))
	L2_stereo_backedge[4] = Al_utils.getAvg(np.array(-005.68423))
	return L2_stereo_backedge

def get_L2_stereo_backedge_normal():
	return Al_utils.normal_vector(math.radians(get_L2_stereo_backedge()[3]),math.radians(get_L2_stereo_backedge()[4]))

def get_L3_axial_frontedge():
	L3_axial_frontedge = np.empty([5])
	L3_axial_frontedge[0] = Al_utils.getAvg(np.array(195.91052))
	L3_axial_frontedge[1] = Al_utils.getAvg(np.array(-031.14810))
	L3_axial_frontedge[2] = Al_utils.getAvg(np.array(005.68903))
	L3_axial_frontedge[3] = Al_utils.getAvg(np.array(090.04888))
	L3_axial_frontedge[4] = Al_utils.getAvg(np.array(-000.01110))
	return L3_axial_frontedge

def get_L3_axial_frontedge_normal():
	return Al_utils.normal_vector(math.radians(get_L3_axial_frontedge()[3]),math.radians(get_L3_axial_frontedge()[4]))

def get_L3_stereo_backedge():
	L3_stereo_backedge = np.empty([5])
	L3_stereo_backedge[0] = Al_utils.getAvg(np.array(204.36921))
	L3_stereo_backedge[1] = Al_utils.getAvg(np.array(-027.26169))
	L3_stereo_backedge[2] = Al_utils.getAvg(np.array(005.66099))
	L3_stereo_backedge[3] = Al_utils.getAvg(np.array(-089.88909))
	L3_stereo_backedge[4] = Al_utils.getAvg(np.array(005.73007))
	return L3_stereo_backedge

def get_L3_stereo_backedge_normal():
	return Al_utils.normal_vector(math.radians(get_L3_stereo_backedge()[3]),math.radians(get_L3_stereo_backedge()[4]))

def get_wire_par():
	wire_par = np.empty([5])
	wire_par[0] = Al_utils.getAvg(np.array(-079.93253))
	wire_par[1] = Al_utils.getAvg(np.array(-014.31121))
	wire_par[2] = Al_utils.getAvg(np.array(015.87547))
	wire_par[3] = Al_utils.getAvg(np.array(090.21338))
	wire_par[4] = Al_utils.getAvg(np.array(000.00139))
	return wire_par

def get_wire_diag():
	wire_diag = np.empty([5])
	wire_diag[0] = Al_utils.getAvg(np.array(-080.20192))
	wire_diag[1] = Al_utils.getAvg(np.array(-014.03084))
	wire_diag[2] = Al_utils.getAvg(np.array(016.17538))
	wire_diag[3] = Al_utils.getAvg(np.array(-089.81303))
	wire_diag[4] = Al_utils.getAvg(np.array(-008.92167))
	return wire_diag
