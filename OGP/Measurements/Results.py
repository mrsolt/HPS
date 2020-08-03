import numpy as np
import math
import Bottom_uchannel_measurements
import Top_uchannel_measurements
import L0_axial_1_measurements
import L0_stereo_1_measurements
import L0_axial_2_measurements
import L0_stereo_2_measurements
import L0_axial_3_measurements
import L0_stereo_3_measurements
import L0_axial_5_measurements
import L0_stereo_5_measurements
import Fixture_measurements
import Nominal_Position_Data
import Sho_measurements
import Al_utils

output = "results.txt"

null_basis = Al_utils.make_basis(np.array([0.0, 0.0, 0.0]), #ball basis in ball frame
		np.array([1.0, 0.0, 0.0]),
		np.array([0.0, 1.0, 0.0]))

#Sensor measurements in the fixture frame
L0_axial_top = L0_axial_1_measurements.get_sensor_basis()
L0_stereo_top = L0_stereo_1_measurements.get_sensor_basis()
L1_axial_top = L0_axial_3_measurements.get_sensor_basis()
L1_stereo_top = L0_stereo_3_measurements.get_sensor_basis()

L0_axial_bot = L0_axial_2_measurements.get_sensor_basis()
L0_stereo_bot = L0_stereo_2_measurements.get_sensor_basis()
L1_axial_bot = L0_axial_5_measurements.get_sensor_basis()
L1_stereo_bot = L0_stereo_5_measurements.get_sensor_basis()

fixbasis = Fixture_measurements.get_fixbasis()
pinbasis_fixbasis_top = Fixture_measurements.get_pin_basis_top()
pinbasis_fixbasis_bot = Fixture_measurements.get_pin_basis_bot()

#Measurements of pins in the empty Uchannel
top_ubasis = Top_uchannel_measurements.get_ubasis()
top_L0_pinbasis = Top_uchannel_measurements.get_L0_pin_basis()
top_L1_pinbasis = Top_uchannel_measurements.get_L1_pin_basis()
top_L2_pinbasis = Top_uchannel_measurements.get_L2_pin_basis()
top_L3_pinbasis = Top_uchannel_measurements.get_L3_pin_basis()

bot_ubasis = Bottom_uchannel_measurements.get_ubasis()
bot_L0_pinbasis = Bottom_uchannel_measurements.get_L0_pin_basis()
bot_L1_pinbasis = Bottom_uchannel_measurements.get_L1_pin_basis()
bot_L2_pinbasis = Bottom_uchannel_measurements.get_L2_pin_basis()
bot_L3_pinbasis = Bottom_uchannel_measurements.get_L3_pin_basis()

#Measured pinbasis in the UChannel basis
top_L0_pinbasis_ubasis = Al_utils.transform_basis(top_L0_pinbasis,null_basis,top_ubasis)
top_L1_pinbasis_ubasis = Al_utils.transform_basis(top_L1_pinbasis,null_basis,top_ubasis)
top_L2_pinbasis_ubasis = Al_utils.transform_basis(top_L2_pinbasis,null_basis,top_ubasis)
top_L3_pinbasis_ubasis = Al_utils.transform_basis(top_L3_pinbasis,null_basis,top_ubasis)
bot_L0_pinbasis_ubasis = Al_utils.transform_basis(bot_L0_pinbasis,null_basis,bot_ubasis)
bot_L1_pinbasis_ubasis = Al_utils.transform_basis(bot_L1_pinbasis,null_basis,bot_ubasis)
bot_L2_pinbasis_ubasis = Al_utils.transform_basis(bot_L2_pinbasis,null_basis,bot_ubasis)
bot_L3_pinbasis_ubasis = Al_utils.transform_basis(bot_L3_pinbasis,null_basis,bot_ubasis)

#Sensor measurements transformed in the pin basis
L0_axial_top_origin_pinbasis = Al_utils.transform_pt(pinbasis_fixbasis_top,fixbasis,L0_axial_top[0])
L0_axial_top_normal_pinbasis = Al_utils.transform_vec(pinbasis_fixbasis_top,fixbasis,L0_axial_top[1][2])
L0_stereo_top_origin_pinbasis = Al_utils.transform_pt(pinbasis_fixbasis_top,fixbasis,L0_stereo_top[0])
L0_stereo_top_normal_pinbasis = Al_utils.transform_vec(pinbasis_fixbasis_top,fixbasis,L0_stereo_top[1][2])
L1_axial_top_origin_pinbasis = Al_utils.transform_pt(pinbasis_fixbasis_top,fixbasis,L1_axial_top[0])
L1_axial_top_normal_pinbasis = Al_utils.transform_vec(pinbasis_fixbasis_top,fixbasis,L1_axial_top[1][2])
L1_stereo_top_origin_pinbasis = Al_utils.transform_pt(pinbasis_fixbasis_top,fixbasis,L1_stereo_top[0])
L1_stereo_top_normal_pinbasis = Al_utils.transform_vec(pinbasis_fixbasis_top,fixbasis,L1_stereo_top[1][2])

L0_axial_bot_origin_pinbasis = Al_utils.transform_pt(pinbasis_fixbasis_top,fixbasis,L0_axial_bot[0])
L0_axial_bot_normal_pinbasis = Al_utils.transform_vec(pinbasis_fixbasis_top,fixbasis,L0_axial_bot[1][2])
L0_stereo_bot_origin_pinbasis = Al_utils.transform_pt(pinbasis_fixbasis_top,fixbasis,L0_stereo_bot[0])
L0_stereo_bot_normal_pinbasis = Al_utils.transform_vec(pinbasis_fixbasis_top,fixbasis,L0_stereo_bot[1][2])
L1_axial_bot_origin_pinbasis = Al_utils.transform_pt(pinbasis_fixbasis_top,fixbasis,L1_axial_bot[0])
L1_axial_bot_normal_pinbasis = Al_utils.transform_vec(pinbasis_fixbasis_top,fixbasis,L1_axial_bot[1][2])
L1_stereo_bot_origin_pinbasis = Al_utils.transform_pt(pinbasis_fixbasis_top,fixbasis,L1_stereo_bot[0])
L1_stereo_bot_normal_pinbasis = Al_utils.transform_vec(pinbasis_fixbasis_top,fixbasis,L1_stereo_bot[1][2])

#Sensor measurements transformed in the Uchannel basis
L0_axial_top_origin_ubasis = Al_utils.transform_pt(top_L0_pinbasis_ubasis,top_ubasis,L0_axial_top_origin_pinbasis)
L0_axial_top_normal_ubasis = Al_utils.transform_vec(top_L0_pinbasis_ubasis,top_ubasis,L0_axial_top_normal_pinbasis)
L0_stereo_top_origin_ubasis = Al_utils.transform_pt(top_L0_pinbasis_ubasis,top_ubasis,L0_stereo_top_origin_pinbasis)
L0_stereo_top_normal_ubasis = Al_utils.transform_vec(top_L0_pinbasis_ubasis,top_ubasis,L0_stereo_top_normal_pinbasis)
L1_axial_top_origin_ubasis = Al_utils.transform_pt(top_L1_pinbasis_ubasis,top_ubasis,L1_axial_top_origin_pinbasis)
L1_axial_top_normal_ubasis = Al_utils.transform_vec(top_L1_pinbasis_ubasis,top_ubasis,L1_axial_top_normal_pinbasis)
L1_stereo_top_origin_ubasis = Al_utils.transform_pt(top_L1_pinbasis_ubasis,top_ubasis,L1_stereo_top_origin_pinbasis)
L1_stereo_top_normal_ubasis = Al_utils.transform_vec(top_L1_pinbasis_ubasis,top_ubasis,L1_stereo_top_normal_pinbasis)

L0_axial_bot_origin_ubasis = Al_utils.transform_pt(bot_L0_pinbasis_ubasis,bot_ubasis,L0_axial_bot_origin_pinbasis)
L0_axial_bot_normal_ubasis = Al_utils.transform_vec(bot_L0_pinbasis_ubasis,bot_ubasis,L0_axial_bot_normal_pinbasis)
L0_stereo_bot_origin_ubasis = Al_utils.transform_pt(bot_L0_pinbasis_ubasis,bot_ubasis,L0_stereo_bot_origin_pinbasis)
L0_stereo_bot_normal_ubasis = Al_utils.transform_vec(bot_L0_pinbasis_ubasis,bot_ubasis,L0_stereo_bot_normal_pinbasis)
L1_axial_bot_origin_ubasis = Al_utils.transform_pt(bot_L1_pinbasis_ubasis,bot_ubasis,L1_axial_bot_origin_pinbasis)
L1_axial_bot_normal_ubasis = Al_utils.transform_vec(bot_L1_pinbasis_ubasis,bot_ubasis,L1_axial_bot_normal_pinbasis)
L1_stereo_bot_origin_ubasis = Al_utils.transform_pt(bot_L1_pinbasis_ubasis,bot_ubasis,L1_stereo_bot_origin_pinbasis)
L1_stereo_bot_normal_ubasis = Al_utils.transform_vec(bot_L1_pinbasis_ubasis,bot_ubasis,L1_stereo_bot_normal_pinbasis)

#Active edge positions in the pin basis
L0_axial_top_active_edge_pinbasis = Al_utils.transform_pt(pinbasis_fixbasis_top,fixbasis,np.array([L0_axial_top[2][0],L0_axial_top[2][1],L0_axial_top[2][2]]))
L0_stereo_top_active_edge_pinbasis = Al_utils.transform_pt(pinbasis_fixbasis_top,fixbasis,np.array([L0_stereo_top[2][0],L0_stereo_top[2][1],L0_stereo_top[2][2]]))
L1_axial_top_active_edge_pinbasis = Al_utils.transform_pt(pinbasis_fixbasis_top,fixbasis,np.array([L1_axial_top[2][0],L1_axial_top[2][1],L1_axial_top[2][2]]))
L1_stereo_top_active_edge_pinbasis = Al_utils.transform_pt(pinbasis_fixbasis_top,fixbasis,np.array([L1_stereo_top[2][0],L1_stereo_top[2][1],L1_stereo_top[2][2]]))

L0_axial_bot_active_edge_pinbasis = Al_utils.transform_pt(pinbasis_fixbasis_top,fixbasis,np.array([L0_axial_bot[2][0],L0_axial_bot[2][1],L0_axial_bot[2][2]]))
L0_stereo_bot_active_edge_pinbasis = Al_utils.transform_pt(pinbasis_fixbasis_top,fixbasis,np.array([L0_stereo_bot[2][0],L0_stereo_bot[2][1],L0_stereo_bot[2][2]]))
L1_axial_bot_active_edge_pinbasis = Al_utils.transform_pt(pinbasis_fixbasis_top,fixbasis,np.array([L1_axial_bot[2][0],L1_axial_bot[2][1],L1_axial_bot[2][2]]))
L1_stereo_bot_active_edge_pinbasis = Al_utils.transform_pt(pinbasis_fixbasis_top,fixbasis,np.array([L1_stereo_bot[2][0],L1_stereo_bot[2][1],L1_stereo_bot[2][2]]))

L0_axial_top_active_edge_vector_pinbasis = Al_utils.transform_vec(fixbasis,pinbasis_fixbasis_top,np.array([L0_axial_top[3][0],L0_axial_top[3][1],L0_axial_top[3][2]]))
L0_stereo_top_active_edge_vector_pinbasis = Al_utils.transform_vec(fixbasis,pinbasis_fixbasis_top,np.array([L0_stereo_top[3][0],L0_stereo_top[3][1],L0_stereo_top[3][2]]))
L1_axial_top_active_edge_vector_pinbasis = Al_utils.transform_vec(fixbasis,pinbasis_fixbasis_top,np.array([L1_axial_top[3][0],L1_axial_top[3][1],L1_axial_top[3][2]]))
L1_stereo_top_active_edge_vector_pinbasis = Al_utils.transform_vec(fixbasis,pinbasis_fixbasis_top,np.array([L1_stereo_top[3][0],L1_stereo_top[3][1],L1_stereo_top[3][2]]))

L0_axial_bot_active_edge_vector_pinbasis = Al_utils.transform_vec(fixbasis,pinbasis_fixbasis_top,np.array([L0_axial_bot[3][0],L0_axial_bot[3][1],L0_axial_bot[3][2]]))
L0_stereo_bot_active_edge_vector_pinbasis = Al_utils.transform_vec(fixbasis,pinbasis_fixbasis_top,np.array([L0_stereo_bot[3][0],L0_stereo_bot[3][1],L0_stereo_bot[3][2]]))
L1_axial_bot_active_edge_vector_pinbasis = Al_utils.transform_vec(fixbasis,pinbasis_fixbasis_top,np.array([L1_axial_bot[3][0],L1_axial_bot[3][1],L1_axial_bot[3][2]]))
L1_stereo_bot_active_edge_vector_pinbasis = Al_utils.transform_vec(fixbasis,pinbasis_fixbasis_top,np.array([L1_stereo_bot[3][0],L1_stereo_bot[3][1],L1_stereo_bot[3][2]]))

#Physical edge positions in the pin basis
L0_axial_top_physical_edge_pinbasis = Al_utils.transform_pt(pinbasis_fixbasis_top,fixbasis,np.array([L0_axial_top[4][0],L0_axial_top[4][1],L0_axial_top[4][2]]))
L0_stereo_top_physical_edge_pinbasis = Al_utils.transform_pt(pinbasis_fixbasis_top,fixbasis,np.array([L0_stereo_top[4][0],L0_stereo_top[4][1],L0_stereo_top[4][2]]))
L1_axial_top_physical_edge_pinbasis = Al_utils.transform_pt(pinbasis_fixbasis_top,fixbasis,np.array([L1_axial_top[4][0],L1_axial_top[4][1],L1_axial_top[4][2]]))
L1_stereo_top_physical_edge_pinbasis = Al_utils.transform_pt(pinbasis_fixbasis_top,fixbasis,np.array([L1_stereo_top[4][0],L1_stereo_top[4][1],L1_stereo_top[4][2]]))

L0_axial_bot_physical_edge_pinbasis = Al_utils.transform_pt(pinbasis_fixbasis_top,fixbasis,np.array([L0_axial_bot[4][0],L0_axial_bot[4][1],L0_axial_bot[4][2]]))
L0_stereo_bot_physical_edge_pinbasis = Al_utils.transform_pt(pinbasis_fixbasis_top,fixbasis,np.array([L0_stereo_bot[4][0],L0_stereo_bot[4][1],L0_stereo_bot[4][2]]))
L1_axial_bot_physical_edge_pinbasis = Al_utils.transform_pt(pinbasis_fixbasis_top,fixbasis,np.array([L1_axial_bot[4][0],L1_axial_bot[4][1],L1_axial_bot[4][2]]))
L1_stereo_bot_physical_edge_pinbasis = Al_utils.transform_pt(pinbasis_fixbasis_top,fixbasis,np.array([L1_stereo_bot[4][0],L1_stereo_bot[4][1],L1_stereo_bot[4][2]]))

L0_axial_top_physical_edge_vector_pinbasis = Al_utils.transform_vec(fixbasis,pinbasis_fixbasis_top,np.array([L0_axial_top[5][0],L0_axial_top[5][1],L0_axial_top[5][2]]))
L0_stereo_top_physical_edge_vector_pinbasis = Al_utils.transform_vec(fixbasis,pinbasis_fixbasis_top,np.array([L0_stereo_top[5][0],L0_stereo_top[5][1],L0_stereo_top[5][2]]))
L1_axial_top_physical_edge_vector_pinbasis = Al_utils.transform_vec(fixbasis,pinbasis_fixbasis_top,np.array([L1_axial_top[5][0],L1_axial_top[5][1],L1_axial_top[5][2]]))
L1_stereo_top_physical_edge_vector_pinbasis = Al_utils.transform_vec(fixbasis,pinbasis_fixbasis_top,np.array([L1_stereo_top[5][0],L1_stereo_top[5][1],L1_stereo_top[5][2]]))

L0_axial_bot_physical_edge_vector_pinbasis = Al_utils.transform_vec(fixbasis,pinbasis_fixbasis_top,np.array([L0_axial_bot[5][0],L0_axial_bot[5][1],L0_axial_bot[5][2]]))
L0_stereo_bot_physical_edge_vector_pinbasis = Al_utils.transform_vec(fixbasis,pinbasis_fixbasis_top,np.array([L0_stereo_bot[5][0],L0_stereo_bot[5][1],L0_stereo_bot[5][2]]))
L1_axial_bot_physical_edge_vector_pinbasis = Al_utils.transform_vec(fixbasis,pinbasis_fixbasis_top,np.array([L1_axial_bot[5][0],L1_axial_bot[5][1],L1_axial_bot[5][2]]))
L1_stereo_bot_physical_edge_vector_pinbasis = Al_utils.transform_vec(fixbasis,pinbasis_fixbasis_top,np.array([L1_stereo_bot[5][0],L1_stereo_bot[5][1],L1_stereo_bot[5][2]]))

#Active edge positions in the pin basis
L0_axial_top_active_edge_ubasis = Al_utils.transform_pt(top_L0_pinbasis_ubasis,top_ubasis,L0_axial_top_active_edge_pinbasis)
L0_stereo_top_active_edge_ubasis = Al_utils.transform_pt(top_L0_pinbasis_ubasis,top_ubasis,L0_stereo_top_active_edge_pinbasis)
L1_axial_top_active_edge_ubasis = Al_utils.transform_pt(top_L1_pinbasis_ubasis,top_ubasis,L1_axial_top_active_edge_pinbasis)
L1_stereo_top_active_edge_ubasis = Al_utils.transform_pt(top_L1_pinbasis_ubasis,top_ubasis,L1_stereo_top_active_edge_pinbasis)

L0_axial_bot_active_edge_ubasis = Al_utils.transform_pt(bot_L0_pinbasis_ubasis,bot_ubasis,L0_axial_bot_active_edge_pinbasis)
L0_stereo_bot_active_edge_ubasis = Al_utils.transform_pt(bot_L0_pinbasis_ubasis,bot_ubasis,L0_stereo_bot_active_edge_pinbasis)
L1_axial_bot_active_edge_ubasis = Al_utils.transform_pt(bot_L1_pinbasis_ubasis,bot_ubasis,L1_axial_bot_active_edge_pinbasis)
L1_stereo_bot_active_edge_ubasis = Al_utils.transform_pt(bot_L1_pinbasis_ubasis,bot_ubasis,L1_stereo_bot_active_edge_pinbasis)

L0_axial_top_active_edge_vector_ubasis = Al_utils.transform_vec(top_L0_pinbasis_ubasis,top_ubasis,L0_axial_top_active_edge_vector_pinbasis)
L0_stereo_top_active_edge_vector_ubasis = Al_utils.transform_vec(top_L0_pinbasis_ubasis,top_ubasis,L0_stereo_top_active_edge_vector_pinbasis)
L1_axial_top_active_edge_vector_ubasis = Al_utils.transform_vec(top_L1_pinbasis_ubasis,top_ubasis,L1_axial_top_active_edge_vector_pinbasis)
L1_stereo_top_active_edge_vector_ubasis = Al_utils.transform_vec(top_L1_pinbasis_ubasis,top_ubasis,L1_stereo_top_active_edge_vector_pinbasis)

L0_axial_bot_active_edge_vector_ubasis = Al_utils.transform_vec(bot_L0_pinbasis_ubasis,bot_ubasis,L0_axial_bot_active_edge_vector_pinbasis)
L0_stereo_bot_active_edge_vector_ubasis = Al_utils.transform_vec(bot_L0_pinbasis_ubasis,bot_ubasis,L0_stereo_bot_active_edge_vector_pinbasis)
L1_axial_bot_active_edge_vector_ubasis = Al_utils.transform_vec(bot_L1_pinbasis_ubasis,bot_ubasis,L1_axial_bot_active_edge_vector_pinbasis)
L1_stereo_bot_active_edge_vector_ubasis = Al_utils.transform_vec(bot_L1_pinbasis_ubasis,bot_ubasis,L1_stereo_bot_active_edge_vector_pinbasis)

#Physical edge positions in the pin basis
L0_axial_top_physical_edge_ubasis = Al_utils.transform_pt(top_L0_pinbasis_ubasis,top_ubasis,L0_axial_top_physical_edge_pinbasis)
L0_stereo_top_physical_edge_ubasis = Al_utils.transform_pt(top_L0_pinbasis_ubasis,top_ubasis,L0_stereo_top_physical_edge_pinbasis)
L1_axial_top_physical_edge_ubasis = Al_utils.transform_pt(top_L1_pinbasis_ubasis,top_ubasis,L1_axial_top_physical_edge_pinbasis)
L1_stereo_top_physical_edge_ubasis = Al_utils.transform_pt(top_L1_pinbasis_ubasis,top_ubasis,L1_stereo_top_physical_edge_pinbasis)

L0_axial_bot_physical_edge_ubasis = Al_utils.transform_pt(bot_L0_pinbasis_ubasis,bot_ubasis,L0_axial_bot_physical_edge_pinbasis)
L0_stereo_bot_physical_edge_ubasis = Al_utils.transform_pt(bot_L0_pinbasis_ubasis,bot_ubasis,L0_stereo_bot_physical_edge_pinbasis)
L1_axial_bot_physical_edge_ubasis = Al_utils.transform_pt(bot_L1_pinbasis_ubasis,bot_ubasis,L1_axial_bot_physical_edge_pinbasis)
L1_stereo_bot_physical_edge_ubasis = Al_utils.transform_pt(bot_L1_pinbasis_ubasis,bot_ubasis,L1_stereo_bot_physical_edge_pinbasis)

L0_axial_top_physical_edge_vector_ubasis = Al_utils.transform_vec(top_L0_pinbasis_ubasis,top_ubasis,L0_axial_top_physical_edge_vector_pinbasis)
L0_stereo_top_physical_edge_vector_ubasis = Al_utils.transform_vec(top_L0_pinbasis_ubasis,top_ubasis,L0_stereo_top_physical_edge_vector_pinbasis)
L1_axial_top_physical_edge_vector_ubasis = Al_utils.transform_vec(top_L1_pinbasis_ubasis,top_ubasis,L1_axial_top_physical_edge_vector_pinbasis)
L1_stereo_top_physical_edge_vector_ubasis = Al_utils.transform_vec(top_L1_pinbasis_ubasis,top_ubasis,L1_stereo_top_physical_edge_vector_pinbasis)

L0_axial_bot_physical_edge_vector_ubasis = Al_utils.transform_vec(bot_L0_pinbasis_ubasis,bot_ubasis,L0_axial_bot_physical_edge_vector_pinbasis)
L0_stereo_bot_physical_edge_vector_ubasis = Al_utils.transform_vec(bot_L0_pinbasis_ubasis,bot_ubasis,L0_stereo_bot_physical_edge_vector_pinbasis)
L1_axial_bot_physical_edge_vector_ubasis = Al_utils.transform_vec(bot_L1_pinbasis_ubasis,bot_ubasis,L1_axial_bot_physical_edge_vector_pinbasis)
L1_stereo_bot_physical_edge_vector_ubasis = Al_utils.transform_vec(bot_L1_pinbasis_ubasis,bot_ubasis,L1_stereo_bot_physical_edge_vector_pinbasis)

Al_utils.transform_pt(pinbasis_fixbasis_top,fixbasis,L0_axial_top[0])
L0_axial_top_normal_pinbasis = Al_utils.transform_vec(pinbasis_fixbasis_top,fixbasis,L0_axial_top[1][2])

L0_axial_top_origin_JLab = Al_utils.ubasisTop_to_JLab(L0_axial_top_origin_ubasis,True)
L0_axial_top_normal_JLab = Al_utils.UChannelToJlabVec(L0_axial_top_normal_ubasis)
L0_stereo_top_origin_JLab = Al_utils.ubasisTop_to_JLab(L0_stereo_top_origin_ubasis,True)
L0_stereo_top_normal_JLab = Al_utils.UChannelToJlabVec(L0_stereo_top_normal_ubasis)

L1_axial_top_origin_JLab = Al_utils.ubasisTop_to_JLab(L1_axial_top_origin_ubasis,False)
L1_axial_top_normal_JLab = Al_utils.UChannelToJlabVec(L1_axial_top_normal_ubasis)
L1_stereo_top_origin_JLab = Al_utils.ubasisTop_to_JLab(L1_stereo_top_origin_ubasis,False)
L1_stereo_top_normal_JLab = Al_utils.UChannelToJlabVec(L1_stereo_top_normal_ubasis)

L0_axial_bot_origin_JLab = Al_utils.ubasisBot_to_JLab(L0_axial_bot_origin_ubasis,True)
L0_axial_bot_normal_JLab = Al_utils.UChannelToJlabVec(L0_axial_bot_normal_ubasis)
L0_stereo_bot_origin_JLab = Al_utils.ubasisBot_to_JLab(L0_stereo_bot_origin_ubasis,True)
L0_stereo_bot_normal_JLab = Al_utils.UChannelToJlabVec(L0_stereo_bot_normal_ubasis)

L1_axial_bot_origin_JLab = Al_utils.ubasisBot_to_JLab(L1_axial_bot_origin_ubasis,False)
L1_axial_bot_normal_JLab = Al_utils.UChannelToJlabVec(L1_axial_bot_normal_ubasis)
L1_stereo_bot_origin_JLab = Al_utils.ubasisBot_to_JLab(L1_stereo_bot_origin_ubasis,False)
L1_stereo_bot_normal_JLab = Al_utils.UChannelToJlabVec(L1_stereo_bot_normal_ubasis)

L2_axial_top_z = Al_utils.UChannelToJlabZ(Top_uchannel_measurements.get_L2_axial_frontedge()[0])
L2_axial_top_y = Al_utils.UChannelToJlabYTop(Top_uchannel_measurements.get_L2_axial_frontedge()[2])
L2_stereo_top_z = Al_utils.UChannelToJlabZ(Top_uchannel_measurements.get_L2_stereo_backedge()[0])
L2_stereo_top_y = Al_utils.UChannelToJlabYTop(Top_uchannel_measurements.get_L2_stereo_backedge()[2])

L3_axial_top_z = Al_utils.UChannelToJlabZ(Top_uchannel_measurements.get_L3_axial_frontedge()[0])
L3_axial_top_y = Al_utils.UChannelToJlabYTop(Top_uchannel_measurements.get_L3_axial_frontedge()[2])
L3_stereo_top_z = Al_utils.UChannelToJlabZ(Top_uchannel_measurements.get_L3_stereo_backedge()[0])
L3_stereo_top_y = Al_utils.UChannelToJlabYTop(Top_uchannel_measurements.get_L3_stereo_backedge()[2])

L2_axial_bot_z = Al_utils.UChannelToJlabZ(Bottom_uchannel_measurements.get_L2_axial_backedge()[0])
L2_axial_bot_y = Al_utils.UChannelToJlabYBot(Bottom_uchannel_measurements.get_L2_axial_backedge()[2])
L2_stereo_bot_z = Al_utils.UChannelToJlabZ(Bottom_uchannel_measurements.get_L2_stereo_frontedge()[0])
L2_stereo_bot_y = Al_utils.UChannelToJlabYBot(Bottom_uchannel_measurements.get_L2_stereo_frontedge()[2])

L3_axial_bot_z = Al_utils.UChannelToJlabZ(Bottom_uchannel_measurements.get_L3_axial_backedge()[0])
L3_axial_bot_y = Al_utils.UChannelToJlabYBot(Bottom_uchannel_measurements.get_L3_axial_backedge()[2])
L3_stereo_bot_z = Al_utils.UChannelToJlabZ(Bottom_uchannel_measurements.get_L3_stereo_frontedge()[0])
L3_stereo_bot_y = Al_utils.UChannelToJlabYBot(Bottom_uchannel_measurements.get_L3_stereo_frontedge()[2])

L0_axial_top_origin_JLab_residual = np.empty([3])
L0_axial_top_origin_JLab_residual[0] = Nominal_Position_Data.get_global_L0t_axial()[0] - L0_axial_top_origin_JLab[0]
L0_axial_top_origin_JLab_residual[1] = Nominal_Position_Data.get_global_L0t_axial()[1] - L0_axial_top_origin_JLab[1]
L0_axial_top_origin_JLab_residual[2] = Nominal_Position_Data.get_global_L0t_axial()[2] - L0_axial_top_origin_JLab[2]
L0_stereo_top_origin_JLab_residual = np.empty([3])
L0_stereo_top_origin_JLab_residual[0] = Nominal_Position_Data.get_global_L0t_stereo()[0] - L0_stereo_top_origin_JLab[0]
L0_stereo_top_origin_JLab_residual[1] = Nominal_Position_Data.get_global_L0t_stereo()[1] - L0_stereo_top_origin_JLab[1]
L0_stereo_top_origin_JLab_residual[2] = Nominal_Position_Data.get_global_L0t_stereo()[2] - L0_stereo_top_origin_JLab[2]

L1_axial_top_origin_JLab_residual = np.empty([3])
L1_axial_top_origin_JLab_residual[0] = Nominal_Position_Data.get_global_L1t_axial()[0] - L1_axial_top_origin_JLab[0]
L1_axial_top_origin_JLab_residual[1] = Nominal_Position_Data.get_global_L1t_axial()[1] - L1_axial_top_origin_JLab[1]
L1_axial_top_origin_JLab_residual[2] = Nominal_Position_Data.get_global_L1t_axial()[2] - L1_axial_top_origin_JLab[2]
L1_stereo_top_origin_JLab_residual = np.empty([3])
L1_stereo_top_origin_JLab_residual[0] = Nominal_Position_Data.get_global_L1t_stereo()[0] - L1_stereo_top_origin_JLab[0]
L1_stereo_top_origin_JLab_residual[1] = Nominal_Position_Data.get_global_L1t_stereo()[1] - L1_stereo_top_origin_JLab[1]
L1_stereo_top_origin_JLab_residual[2] = Nominal_Position_Data.get_global_L1t_stereo()[2] - L1_stereo_top_origin_JLab[2]

L0_axial_bot_origin_JLab_residual = np.empty([3])
L0_axial_bot_origin_JLab_residual[0] = Nominal_Position_Data.get_global_L0b_axial()[0] - L0_axial_bot_origin_JLab[0]
L0_axial_bot_origin_JLab_residual[1] = Nominal_Position_Data.get_global_L0b_axial()[1] - L0_axial_bot_origin_JLab[1]
L0_axial_bot_origin_JLab_residual[2] = Nominal_Position_Data.get_global_L0b_axial()[2] - L0_axial_bot_origin_JLab[2]
L0_stereo_bot_origin_JLab_residual = np.empty([3])
L0_stereo_bot_origin_JLab_residual[0] = Nominal_Position_Data.get_global_L0b_stereo()[0] - L0_stereo_bot_origin_JLab[0]
L0_stereo_bot_origin_JLab_residual[1] = Nominal_Position_Data.get_global_L0b_stereo()[1] - L0_stereo_bot_origin_JLab[1]
L0_stereo_bot_origin_JLab_residual[2] = Nominal_Position_Data.get_global_L0b_stereo()[2] - L0_stereo_bot_origin_JLab[2]

L1_axial_bot_origin_JLab_residual = np.empty([3])
L1_axial_bot_origin_JLab_residual[0] = Nominal_Position_Data.get_global_L1b_axial()[0] - L1_axial_bot_origin_JLab[0]
L1_axial_bot_origin_JLab_residual[1] = Nominal_Position_Data.get_global_L1b_axial()[1] - L1_axial_bot_origin_JLab[1]
L1_axial_bot_origin_JLab_residual[2] = Nominal_Position_Data.get_global_L1b_axial()[2] - L1_axial_bot_origin_JLab[2]
L1_stereo_bot_origin_JLab_residual = np.empty([3])
L1_stereo_bot_origin_JLab_residual[0] = Nominal_Position_Data.get_global_L1b_stereo()[0] - L1_stereo_bot_origin_JLab[0]
L1_stereo_bot_origin_JLab_residual[1] = Nominal_Position_Data.get_global_L1b_stereo()[1] - L1_stereo_bot_origin_JLab[1]
L1_stereo_bot_origin_JLab_residual[2] = Nominal_Position_Data.get_global_L1b_stereo()[2] - L1_stereo_bot_origin_JLab[2]

outfile = open(output,"w")

outfile.write("L0 Top pinbasis in uchannel frame\n")
outfile.write(str(top_L0_pinbasis)+"\n")

outfile.write("L1 Top pinbasis in uchannel frame\n")
outfile.write(str(top_L1_pinbasis)+"\n")

outfile.write("L2 Top pinbasis in uchannel frame\n")
outfile.write(str(top_L2_pinbasis)+"\n")

outfile.write("L3 Top pinbasis in uchannel frame\n")
outfile.write(str(top_L3_pinbasis)+"\n")

outfile.write("L0 Bot pinbasis in uchannel frame\n")
outfile.write(str(bot_L0_pinbasis)+"\n")

outfile.write("L1 Bot pinbasis in uchannel frame\n")
outfile.write(str(bot_L1_pinbasis)+"\n")

outfile.write("L2 Bot pinbasis in uchannel frame\n")
outfile.write(str(bot_L2_pinbasis)+"\n")

outfile.write("L3 Bot pinbasis in uchannel frame\n")
outfile.write(str(bot_L3_pinbasis)+"\n")

outfile.write("\n")

outfile.write("L0 Top Axial sensor in fixture frame\n")
outfile.write(str(L0_axial_top)+"\n")
outfile.write("L0 Top Stereo sensor in fixture frame\n")
outfile.write(str(L0_stereo_top)+"\n")

outfile.write("L1 Top Axial sensor in fixture frame\n")
outfile.write(str(L1_axial_top)+"\n")
outfile.write("L1 Top Stereo sensor in fixture frame\n")
outfile.write(str(L1_stereo_top)+"\n")

#outfile.write("L2 Top Axial sensor in fixture frame\n")
#outfile.write(str(L2_axial_top)+"\n")
#outfile.write("L2 Top Stereo sensor in fixture frame\n")
#outfile.write(str(L2_stereo_top)+"\n")

#outfile.write("L3 Top Axial sensor in fixture frame\n")
#outfile.write(str(L3_axial_top)+"\n")
#outfile.write("L3 Top Stereo sensor in fixture frame\n")
#outfile.write(str(L3_stereo_top)+"\n")

outfile.write("L0 Bot Axial sensor in fixture frame\n")
outfile.write(str(L0_axial_bot)+"\n")
outfile.write("L0 Bot Stereo sensor in fixture frame\n")
outfile.write(str(L0_stereo_bot)+"\n")

outfile.write("L1 Bot Axial sensor in fixture frame\n")
outfile.write(str(L1_axial_bot)+"\n")
outfile.write("L1 Bot Stereo sensor in fixture frame\n")
outfile.write(str(L1_stereo_bot)+"\n")

#outfile.write("L2 Bot Axial sensor in fixture frame\n")
#outfile.write(str(L2_axial_bot)+"\n")
#outfile.write("L2 Bot Stereo sensor in fixture frame\n")
#outfile.write(str(L2_stereo_bot)+"\n")

#outfile.write("L3 Bot Axial sensor in fixture frame\n")
#outfile.write(str(L3_axial_bot)+"\n")
#outfile.write("L3 Bot Stereo sensor in fixture frame\n")
#outfile.write(str(L3_stereo_bot)+"\n")

outfile.write("\n")

outfile.write("L0 Top Axial sensor in pin frame\n")
#outfile.write("Origin: "+str(L0_axial_top_origin_pinbasis)+"  Normal: "+str(L0_axial_top_origin_pinbasis)+"  Stereo Angle: "+str(L0_axial_top_active_edge_vector_pinbasis[2]/L0_axial_top_active_edge_vector_pinbasis[1])+"\n")
outfile.write("Origin: "+str(L0_axial_top_origin_pinbasis)+"  Normal: "+str(L0_axial_top_normal_pinbasis)+"  Stereo Angle: "+str(L0_axial_top_active_edge_vector_pinbasis[2]/L0_axial_top_active_edge_vector_pinbasis[1])+"\n")
outfile.write("L0 Top Stereo sensor in pin frame\n")
#outfile.write("Origin: "+str(L0_stereo_top_origin_pinbasis)+"  Normal: "+str(L0_stereo_top_origin_pinbasis)+"  Stereo Angle: "+str(L0_stereo_top_active_edge_vector_pinbasis[2]/L0_stereo_top_active_edge_vector_pinbasis[1])+"\n")
outfile.write("Origin: "+str(L0_stereo_top_origin_pinbasis)+"  Normal: "+str(L0_stereo_top_normal_pinbasis)+"  Stereo Angle: "+str(L0_stereo_top_active_edge_vector_pinbasis[2]/L0_stereo_top_active_edge_vector_pinbasis[1])+"\n")

outfile.write("L1 Top Axial sensor in pin frame\n")
#outfile.write("Origin: "+str(L1_axial_top_origin_pinbasis)+"  Normal: "+str(L1_axial_top_origin_pinbasis)+"  Stereo Angle: "+str(L1_axial_top_active_edge_vector_pinbasis[2]/L1_axial_top_active_edge_vector_pinbasis[1])+"\n")
outfile.write("Origin: "+str(L1_axial_top_origin_pinbasis)+"  Normal: "+str(L1_axial_top_normal_pinbasis)+"  Stereo Angle: "+str(L1_axial_top_active_edge_vector_pinbasis[2]/L1_axial_top_active_edge_vector_pinbasis[1])+"\n")
outfile.write("L1 Top Stereo sensor in pin frame\n")
#outfile.write("Origin: "+str(L1_stereo_top_origin_pinbasis)+"  Normal: "+str(L1_stereo_top_origin_pinbasis)+"  Stereo Angle: "+str(L1_stereo_top_active_edge_vector_pinbasis[2]/L1_stereo_top_active_edge_vector_pinbasis[1])+"\n")
outfile.write("Origin: "+str(L1_stereo_top_origin_pinbasis)+"  Normal: "+str(L1_stereo_top_normal_pinbasis)+"  Stereo Angle: "+str(L1_stereo_top_active_edge_vector_pinbasis[2]/L1_stereo_top_active_edge_vector_pinbasis[1])+"\n")

#outfile.write("L2 Top Axial sensor in pin frame\n")
#outfile.write("Origin: "+str(L2_axial_top_origin_pinbasis)+"  Normal: "+str(L2_axial_top_origin_pinbasis)+"  Stereo Angle: "+str(L2_axial_top_active_edge_vector_pinbasis[2]/L2_axial_top_active_edge_vector_pinbasis[1])+"\n")
#outfile.write("L2 Top Stereo sensor in pin frame\n")
#outfile.write("Origin: "+str(L2_stereo_top_origin_pinbasis)+"  Normal: "+str(L2_stereo_top_origin_pinbasis)+"  Stereo Angle: "+str(L2_stereo_top_active_edge_vector_pinbasis[2]/L2_stereo_top_active_edge_vector_pinbasis[1])+"\n")

#outfile.write("L3 Top Axial sensor in pin frame\n")
#outfile.write("Origin: "+str(L3_axial_top_origin_pinbasis)+"  Normal: "+str(L3_axial_top_origin_pinbasis)+"  Stereo Angle: "+str(L3_axial_top_active_edge_vector_pinbasis[2]/L3_axial_top_active_edge_vector_pinbasis[1])+"\n")
#outfile.write("L3 Top Stereo sensor in pin frame\n")
#outfile.write("Origin: "+str(L3_stereo_top_origin_pinbasis)+"  Normal: "+str(L3_stereo_top_origin_pinbasis)+"  Stereo Angle: "+str(L3_stereo_top_active_edge_vector_pinbasis[2]/L3_stereo_top_active_edge_vector_pinbasis[1])+"\n")

outfile.write("L0 Bot Axial sensor in pin frame\n")
#outfile.write("Origin: "+str(L0_axial_bot_origin_pinbasis)+"  Normal: "+str(L0_axial_bot_origin_pinbasis)+"  Stereo Angle: "+str(L0_axial_bot_active_edge_vector_pinbasis[2]/L0_axial_bot_active_edge_vector_pinbasis[1])+"\n")
outfile.write("Origin: "+str(L0_axial_bot_origin_pinbasis)+"  Normal: "+str(L0_axial_bot_normal_pinbasis)+"  Stereo Angle: "+str(L0_axial_bot_active_edge_vector_pinbasis[2]/L0_axial_bot_active_edge_vector_pinbasis[1])+"\n")
outfile.write("L0 Bot Stereo sensor in pin frame\n")
#outfile.write("Origin: "+str(L0_stereo_bot_origin_pinbasis)+"  Normal: "+str(L0_stereo_bot_origin_pinbasis)+"  Stereo Angle: "+str(L0_stereo_bot_active_edge_vector_pinbasis[2]/L0_stereo_bot_active_edge_vector_pinbasis[1])+"\n")
outfile.write("Origin: "+str(L0_stereo_bot_origin_pinbasis)+"  Normal: "+str(L0_stereo_bot_normal_pinbasis)+"  Stereo Angle: "+str(L0_stereo_bot_active_edge_vector_pinbasis[2]/L0_stereo_bot_active_edge_vector_pinbasis[1])+"\n")

outfile.write("L1 Bot Axial sensor in pin frame\n")
#outfile.write("Origin: "+str(L1_axial_bot_origin_pinbasis)+"  Normal: "+str(L1_axial_bot_origin_pinbasis)+"  Stereo Angle: "+str(L1_axial_bot_active_edge_vector_pinbasis[2]/L1_axial_bot_active_edge_vector_pinbasis[1])+"\n")
outfile.write("Origin: "+str(L1_axial_bot_origin_pinbasis)+"  Normal: "+str(L1_axial_bot_normal_pinbasis)+"  Stereo Angle: "+str(L1_axial_bot_active_edge_vector_pinbasis[2]/L1_axial_bot_active_edge_vector_pinbasis[1])+"\n")
outfile.write("L1 Bot Stereo sensor in pin frame\n")
#outfile.write("Origin: "+str(L1_stereo_bot_origin_pinbasis)+"  Normal: "+str(L1_stereo_bot_origin_pinbasis)+"  Stereo Angle: "+str(L1_stereo_bot_active_edge_vector_pinbasis[2]/L1_stereo_bot_active_edge_vector_pinbasis[1])+"\n")
outfile.write("Origin: "+str(L1_stereo_bot_origin_pinbasis)+"  Normal: "+str(L1_stereo_bot_normal_pinbasis)+"  Stereo Angle: "+str(L1_stereo_bot_active_edge_vector_pinbasis[2]/L1_stereo_bot_active_edge_vector_pinbasis[1])+"\n")

#outfile.write("L2 Bot Axial sensor in pin frame\n")
#outfile.write("Origin: "+str(L2_axial_bot_origin_pinbasis)+"  Normal: "+str(L2_axial_bot_origin_pinbasis)+"  Stereo Angle: "+str(L2_axial_bot_active_edge_vector_pinbasis[2]/L2_axial_bot_active_edge_vector_pinbasis[1])+"\n")
#outfile.write("L2 Bot Stereo sensor in pin frame\n")
#outfile.write("Origin: "+str(L2_stereo_bot_origin_pinbasis)+"  Normal: "+str(L2_stereo_bot_origin_pinbasis)+"  Stereo Angle: "+str(L2_stereo_bot_active_edge_vector_pinbasis[2]/L2_stereo_bot_active_edge_vector_pinbasis[1])+"\n")

#outfile.write("L3 Bot Axial sensor in pin frame\n")
#outfile.write("Origin: "+str(L3_axial_bot_origin_pinbasis)+"  Normal: "+str(L3_axial_bot_origin_pinbasis)+"  Stereo Angle: "+str(L3_axial_bot_active_edge_vector_pinbasis[2]/L3_axial_bot_active_edge_vector_pinbasis[1])+"\n")
#outfile.write("L3 Bot Stereo sensor in pin frame\n")
#outfile.write("Origin: "+str(L3_stereo_bot_origin_pinbasis)+"  Normal: "+str(L3_stereo_bot_origin_pinbasis)+"  Stereo Angle: "+str(L3_stereo_bot_active_edge_vector_pinbasis[2]/L3_stereo_bot_active_edge_vector_pinbasis[1])+"\n")

outfile.write("\n")

outfile.write("L0 Top Axial sensor in uchannel frame\n")
#outfile.write("Origin: "+str(L0_axial_top_origin_ubasis)+"  Normal: "+str(L0_axial_top_origin_ubasis)+"  Stereo Angle: "+str(L0_axial_top_active_edge_vector_ubasis[2]/L0_axial_top_active_edge_vector_ubasis[1])+"\n")
outfile.write("Origin: "+str(L0_axial_top_origin_ubasis)+"  Normal: "+str(L0_axial_top_normal_ubasis)+"  Stereo Angle: "+str(L0_axial_top_active_edge_vector_ubasis[2]/L0_axial_top_active_edge_vector_ubasis[1])+"\n")
outfile.write("L0 Top Stereo sensor in uchannel frame\n")
#outfile.write("Origin: "+str(L0_stereo_top_origin_ubasis)+"  Normal: "+str(L0_stereo_top_origin_ubasis)+"  Stereo Angle: "+str(L0_stereo_top_active_edge_vector_ubasis[2]/L0_stereo_top_active_edge_vector_ubasis[1])+"\n")
outfile.write("Origin: "+str(L0_stereo_top_origin_ubasis)+"  Normal: "+str(L0_stereo_top_normal_ubasis)+"  Stereo Angle: "+str(L0_stereo_top_active_edge_vector_ubasis[2]/L0_stereo_top_active_edge_vector_ubasis[1])+"\n")

outfile.write("L1 Top Axial sensor in uchannel frame\n")
#outfile.write("Origin: "+str(L1_axial_top_origin_ubasis)+"  Normal: "+str(L1_axial_top_origin_ubasis)+"  Stereo Angle: "+str(L1_axial_top_active_edge_vector_ubasis[2]/L1_axial_top_active_edge_vector_ubasis[1])+"\n")
outfile.write("Origin: "+str(L1_axial_top_origin_ubasis)+"  Normal: "+str(L1_axial_top_normal_ubasis)+"  Stereo Angle: "+str(L1_axial_top_active_edge_vector_ubasis[2]/L1_axial_top_active_edge_vector_ubasis[1])+"\n")
outfile.write("L1 Top Stereo sensor in uchannel frame\n")
#outfile.write("Origin: "+str(L1_stereo_top_origin_ubasis)+"  Normal: "+str(L1_stereo_top_origin_ubasis)+"  Stereo Angle: "+str(L1_stereo_top_active_edge_vector_ubasis[2]/L1_stereo_top_active_edge_vector_ubasis[1])+"\n")
outfile.write("Origin: "+str(L1_stereo_top_origin_ubasis)+"  Normal: "+str(L1_stereo_top_normal_ubasis)+"  Stereo Angle: "+str(L1_stereo_top_active_edge_vector_ubasis[2]/L1_stereo_top_active_edge_vector_ubasis[1])+"\n")

#outfile.write("L2 Top Axial sensor in uchannel frame\n")
#outfile.write("Origin: "+str(L2_axial_top_origin_ubasis)+"  Normal: "+str(L2_axial_top_origin_ubasis)+"  Stereo Angle: "+str(L2_axial_top_active_edge_vector_ubasis[2]/L2_axial_top_active_edge_vector_ubasis[1])+"\n")
#outfile.write("L2 Top Stereo sensor in uchannel frame\n")
#outfile.write("Origin: "+str(L2_stereo_top_origin_ubasis)+"  Normal: "+str(L2_stereo_top_origin_ubasis)+"  Stereo Angle: "+str(L2_stereo_top_active_edge_vector_ubasis[2]/L2_stereo_top_active_edge_vector_ubasis[1])+"\n")

#outfile.write("L3 Top Axial sensor in uchannel frame\n")
#outfile.write("Origin: "+str(L3_axial_top_origin_ubasis)+"  Normal: "+str(L3_axial_top_origin_ubasis)+"  Stereo Angle: "+str(L3_axial_top_active_edge_vector_ubasis[2]/L3_axial_top_active_edge_vector_ubasis[1])+"\n")
#outfile.write("L3 Top Stereo sensor in uchannel frame\n")
#outfile.write("Origin: "+str(L3_stereo_top_origin_ubasis)+"  Normal: "+str(L3_stereo_top_origin_ubasis)+"  Stereo Angle: "+str(L3_stereo_top_active_edge_vector_ubasis[2]/L3_stereo_top_active_edge_vector_ubasis[1])+"\n")

outfile.write("L0 Bot Axial sensor in uchannel frame\n")
#outfile.write("Origin: "+str(L0_axial_bot_origin_ubasis)+"  Normal: "+str(L0_axial_bot_origin_ubasis)+"  Stereo Angle: "+str(L0_axial_bot_active_edge_vector_ubasis[2]/L0_axial_bot_active_edge_vector_ubasis[1])+"\n")
outfile.write("Origin: "+str(L0_axial_bot_origin_ubasis)+"  Normal: "+str(L0_axial_bot_normal_ubasis)+"  Stereo Angle: "+str(L0_axial_bot_active_edge_vector_ubasis[2]/L0_axial_bot_active_edge_vector_ubasis[1])+"\n")
outfile.write("L0 Bot Stereo sensor in uchannel frame\n")
#outfile.write("Origin: "+str(L0_stereo_bot_origin_ubasis)+"  Normal: "+str(L0_stereo_bot_origin_ubasis)+"  Stereo Angle: "+str(L0_stereo_bot_active_edge_vector_ubasis[2]/L0_stereo_bot_active_edge_vector_ubasis[1])+"\n")
outfile.write("Origin: "+str(L0_stereo_bot_origin_ubasis)+"  Normal: "+str(L0_stereo_bot_normal_ubasis)+"  Stereo Angle: "+str(L0_stereo_bot_active_edge_vector_ubasis[2]/L0_stereo_bot_active_edge_vector_ubasis[1])+"\n")

outfile.write("L1 Bot Axial sensor in uchannel frame\n")
#outfile.write("Origin: "+str(L1_axial_bot_origin_ubasis)+"  Normal: "+str(L1_axial_bot_origin_ubasis)+"  Stereo Angle: "+str(L1_axial_bot_active_edge_vector_ubasis[2]/L1_axial_bot_active_edge_vector_ubasis[1])+"\n")
outfile.write("Origin: "+str(L1_axial_bot_origin_ubasis)+"  Normal: "+str(L1_axial_bot_normal_ubasis)+"  Stereo Angle: "+str(L1_axial_bot_active_edge_vector_ubasis[2]/L1_axial_bot_active_edge_vector_ubasis[1])+"\n")
outfile.write("L1 Bot Stereo sensor in uchannel frame\n")
#outfile.write("Origin: "+str(L1_stereo_bot_origin_ubasis)+"  Normal: "+str(L1_stereo_bot_origin_ubasis)+"  Stereo Angle: "+str(L1_stereo_bot_active_edge_vector_ubasis[2]/L1_stereo_bot_active_edge_vector_ubasis[1])+"\n")
outfile.write("Origin: "+str(L1_stereo_bot_origin_ubasis)+"  Normal: "+str(L1_stereo_bot_normal_ubasis)+"  Stereo Angle: "+str(L1_stereo_bot_active_edge_vector_ubasis[2]/L1_stereo_bot_active_edge_vector_ubasis[1])+"\n")

#outfile.write("L2 Bot Axial sensor in uchannel frame\n")
#outfile.write("Origin: "+str(L2_axial_bot_origin_ubasis)+"  Normal: "+str(L2_axial_bot_origin_ubasis)+"  Stereo Angle: "+str(L2_axial_bot_active_edge_vector_ubasis[2]/L2_axial_bot_active_edge_vector_ubasis[1])+"\n")
#outfile.write("L2 Bot Stereo sensor in uchannel frame\n")
#outfile.write("Origin: "+str(L2_stereo_bot_origin_ubasis)+"  Normal: "+str(L2_stereo_bot_origin_ubasis)+"  Stereo Angle: "+str(L2_stereo_bot_active_edge_vector_ubasis[2]/L2_stereo_bot_active_edge_vector_ubasis[1])+"\n")

#outfile.write("L3 Bot Axial sensor in uchannel frame\n")
#outfile.write("Origin: "+str(L3_axial_bot_origin_ubasis)+"  Normal: "+str(L3_axial_bot_origin_ubasis)+"  Stereo Angle: "+str(L3_axial_bot_active_edge_vector_ubasis[2]/L3_axial_bot_active_edge_vector_ubasis[1])+"\n")
#outfile.write("L3 Bot Stereo sensor in uchannel frame\n")
#outfile.write("Origin: "+str(L3_stereo_bot_origin_ubasis)+"  Normal: "+str(L3_stereo_bot_origin_ubasis)+"  Stereo Angle: "+str(L3_stereo_bot_active_edge_vector_ubasis[2]/L3_stereo_bot_active_edge_vector_ubasis[1])+"\n")

outfile.write("\n")

outfile.write("L0 Top Axial sensor in uchannel frame uchannel measurement\n")
outfile.write("Z: "+str(Top_uchannel_measurements.get_L0_axial_frontedge()[0])+"  Y: "+str(Top_uchannel_measurements.get_L0_axial_frontedge()[2])+"\n")
outfile.write("L0 Top Stereo sensor in uchannel frame uchannel measurement\n")
outfile.write("Z: "+str(Top_uchannel_measurements.get_L0_stereo_backedge()[0])+"  Y: "+str(Top_uchannel_measurements.get_L0_stereo_backedge()[2])+"\n")

outfile.write("L1 Top Axial sensor in uchannel frame uchannel measurement\n")
outfile.write("Z: "+str(Top_uchannel_measurements.get_L1_axial_frontedge()[0])+"  Y: "+str(Top_uchannel_measurements.get_L1_axial_frontedge()[2])+"\n")
outfile.write("L1 Top Stereo sensor in uchannel frame uchannel measurement\n")
outfile.write("Z: "+str(Top_uchannel_measurements.get_L1_stereo_backedge()[0])+"  Y: "+str(Top_uchannel_measurements.get_L1_stereo_backedge()[2])+"\n")

outfile.write("L2 Top Axial sensor in uchannel frame uchannel measurement\n")
outfile.write("Z: "+str(Top_uchannel_measurements.get_L2_axial_frontedge()[0])+"  Y: "+str(Top_uchannel_measurements.get_L2_axial_frontedge()[2])+"\n")
outfile.write("L2 Top Stereo sensor in uchannel frame uchannel measurement\n")
outfile.write("Z: "+str(Top_uchannel_measurements.get_L2_stereo_backedge()[0])+"  Y: "+str(Top_uchannel_measurements.get_L2_stereo_backedge()[2])+"\n")

outfile.write("L3 Top Axial sensor in uchannel frame uchannel measurement\n")
outfile.write("Z: "+str(Top_uchannel_measurements.get_L3_axial_frontedge()[0])+"  Y: "+str(Top_uchannel_measurements.get_L3_axial_frontedge()[2])+"\n")
outfile.write("L3 Top Stereo sensor in uchannel frame uchannel measurement\n")
outfile.write("Z: "+str(Top_uchannel_measurements.get_L3_stereo_backedge()[0])+"  Y: "+str(Top_uchannel_measurements.get_L3_stereo_backedge()[2])+"\n")

outfile.write("L0 Bot Axial sensor in uchannel frame uchannel measurement\n")
outfile.write("Z: "+str(Bottom_uchannel_measurements.get_L0_axial_backedge()[0])+"  Y: "+str(Bottom_uchannel_measurements.get_L0_axial_backedge()[2])+"\n")
outfile.write("L0 Bot Stereo sensor in uchannel frame uchannel measurement\n")
outfile.write("Z: "+str(Bottom_uchannel_measurements.get_L0_stereo_frontedge()[0])+"  Y: "+str(Bottom_uchannel_measurements.get_L0_stereo_frontedge()[2])+"\n")

outfile.write("L1 Bot Axial sensor in uchannel frame uchannel measurement\n")
outfile.write("Z: "+str(Bottom_uchannel_measurements.get_L1_axial_backedge()[0])+"  Y: "+str(Bottom_uchannel_measurements.get_L1_axial_backedge()[2])+"\n")
outfile.write("L1 Bot Stereo sensor in uchannel frame uchannel measurement\n")
outfile.write("Z: "+str(Bottom_uchannel_measurements.get_L1_stereo_frontedge()[0])+"  Y: "+str(Bottom_uchannel_measurements.get_L1_stereo_frontedge()[2])+"\n")

outfile.write("L2 Bot Axial sensor in uchannel frame uchannel measurement\n")
outfile.write("Z: "+str(Bottom_uchannel_measurements.get_L2_axial_backedge()[0])+"  Y: "+str(Bottom_uchannel_measurements.get_L2_axial_backedge()[2])+"\n")
outfile.write("L2 Bot Stereo sensor in uchannel frame uchannel measurement\n")
outfile.write("Z: "+str(Bottom_uchannel_measurements.get_L2_stereo_frontedge()[0])+"  Y: "+str(Bottom_uchannel_measurements.get_L2_stereo_frontedge()[2])+"\n")

outfile.write("L3 Bot Axial sensor in uchannel frame uchannel measurement\n")
outfile.write("Z: "+str(Bottom_uchannel_measurements.get_L3_axial_backedge()[0])+"  Y: "+str(Bottom_uchannel_measurements.get_L3_axial_backedge()[2])+"\n")
outfile.write("L3 Bot Stereo sensor in uchannel frame uchannel measurement\n")
outfile.write("Z: "+str(Bottom_uchannel_measurements.get_L3_stereo_frontedge()[0])+"  Y: "+str(Bottom_uchannel_measurements.get_L3_stereo_frontedge()[2])+"\n")

outfile.write("\n")

outfile.write("Horizontal Wire Top in uchannel frame uchannel measurement\n")
outfile.write("Position "+str(Top_uchannel_measurements.get_wire_par())+"  Stereo angle: "+str(Top_uchannel_measurements.get_wire_par_normal()[2]/Top_uchannel_measurements.get_wire_par_normal()[1])+"\n")
outfile.write("Sho top wire w.r.t. UChannel " + str(Sho_measurements.get_top_wire_y_ubasis())+"  Difference: "+str(Top_uchannel_measurements.get_wire_par()[2]-Sho_measurements.get_top_wire_y_ubasis())+"\n")
outfile.write("Diagonal Wire Top in uchannel frame uchannel measurement\n")
outfile.write("Position "+str(Top_uchannel_measurements.get_wire_diag())+"  Stereo angle: "+str(Top_uchannel_measurements.get_wire_diag_normal()[2]/Top_uchannel_measurements.get_wire_diag_normal()[1])+"\n")

outfile.write("Horizontal Wire Bot in uchannel frame uchannel measurement\n")
outfile.write("Position "+str(Bottom_uchannel_measurements.get_wire_par())+"  Stereo angle: "+str(Bottom_uchannel_measurements.get_wire_par_normal()[2]/Bottom_uchannel_measurements.get_wire_par_normal()[1])+"\n")
outfile.write("Sho bot wire w.r.t. UChannel " + str(Sho_measurements.get_bot_wire_y_ubasis())+"  Difference: "+str(Bottom_uchannel_measurements.get_wire_par()[2]-Sho_measurements.get_bot_wire_y_ubasis())+"\n")
outfile.write("Diagonal Wire Bot in uchannel frame uchannel measurement\n")
outfile.write("Position "+str(Bottom_uchannel_measurements.get_wire_diag())+"  Stereo angle: "+str(Bottom_uchannel_measurements.get_wire_diag_normal()[2]/Bottom_uchannel_measurements.get_wire_diag_normal()[1])+"\n")

outfile.write("\n")

outfile.write("L0 Top Axial sensor residuals (fixture - uchannel)\n")
outfile.write("Z: "+str(L0_axial_top_physical_edge_ubasis[0]-Top_uchannel_measurements.get_L0_axial_frontedge()[0])+"  Y: "+str(L0_axial_top_physical_edge_ubasis[2]-Top_uchannel_measurements.get_L0_axial_frontedge()[2])+"\n")
outfile.write("L0 Top Stereo sensor residuals (fixture - uchannel)\n")
outfile.write("Z: "+str(L0_stereo_top_physical_edge_ubasis[0]-Top_uchannel_measurements.get_L0_stereo_backedge()[0])+"  Y: "+str(L0_stereo_top_physical_edge_ubasis[2]-Top_uchannel_measurements.get_L0_stereo_backedge()[2])+"\n")

outfile.write("L1 Top Axial sensor residuals (fixture - uchannel)\n")
outfile.write("Z: "+str(L1_axial_top_physical_edge_ubasis[0]-Top_uchannel_measurements.get_L1_axial_frontedge()[0])+"  Y: "+str(L1_axial_top_physical_edge_ubasis[2]-Top_uchannel_measurements.get_L1_axial_frontedge()[2])+"\n")
outfile.write("L1 Top Stereo sensor residuals (fixture - uchannel)\n")
outfile.write("Z: "+str(L1_stereo_top_physical_edge_ubasis[0]-Top_uchannel_measurements.get_L1_stereo_backedge()[0])+"  Y: "+str(L1_stereo_top_physical_edge_ubasis[2]-Top_uchannel_measurements.get_L1_stereo_backedge()[2])+"\n")

#outfile.write("L2 Top Axial sensor residuals (fixture - uchannel)\n")
#outfile.write("Z: "+str(L2_axial_top_physical_edge_ubasis[0]-Top_uchannel_measurements.get_L2_axial_frontedge()[0])+"  Y: "+str(L2_axial_top_physical_edge_ubasis[2]-Top_uchannel_measurements.get_L2_axial_frontedge()[2])+"\n")
#outfile.write("L2 Top Stereo sensor residuals (fixture - uchannel)\n")
#outfile.write("Z: "+str(L2_stereo_top_physical_edge_ubasis[0]-Top_uchannel_measurements.get_L2_stereo_backedge()[0])+"  Y: "+str(L2_stereo_top_physical_edge_ubasis[2]-Top_uchannel_measurements.get_L2_stereo_backedge()[2])+"\n")

#outfile.write("L3 Top Axial sensor residuals (fixture - uchannel)\n")
#outfile.write("Z: "+str(L3_axial_top_physical_edge_ubasis[0]-Top_uchannel_measurements.get_L3_axial_frontedge()[0])+"  Y: "+str(L3_axial_top_physical_edge_ubasis[2]-Top_uchannel_measurements.get_L3_axial_frontedge()[2])+"\n")
#outfile.write("L3 Top Stereo sensor residuals (fixture - uchannel)\n")
#outfile.write("Z: "+str(L3_stereo_top_physical_edge_ubasis[0]-Top_uchannel_measurements.get_L3_stereo_backedge()[0])+"  Y: "+str(L3_stereo_top_physical_edge_ubasis[2]-Top_uchannel_measurements.get_L3_stereo_backedge()[2])+"\n")

outfile.write("L0 Bot Axial sensor residuals (fixture - uchannel)\n")
outfile.write("Z: "+str(L0_axial_bot_physical_edge_ubasis[0]-Bottom_uchannel_measurements.get_L0_axial_backedge()[0])+"  Y: "+str(L0_axial_bot_physical_edge_ubasis[2]-Bottom_uchannel_measurements.get_L0_axial_backedge()[2])+"\n")
outfile.write("L0 Bot Stereo sensor residuals (fixture - uchannel)\n")
outfile.write("Z: "+str(L0_stereo_bot_physical_edge_ubasis[0]-Bottom_uchannel_measurements.get_L0_stereo_frontedge()[0])+"  Y: "+str(L0_stereo_bot_physical_edge_ubasis[2]-Bottom_uchannel_measurements.get_L0_stereo_frontedge()[2])+"\n")

outfile.write("L1 Bot Axial sensor residuals (fixture - uchannel)\n")
outfile.write("Z: "+str(L1_axial_bot_physical_edge_ubasis[0]-Bottom_uchannel_measurements.get_L1_axial_backedge()[0])+"  Y: "+str(L1_axial_bot_physical_edge_ubasis[2]-Bottom_uchannel_measurements.get_L1_axial_backedge()[2])+"\n")
outfile.write("L1 Bot Stereo sensor residuals (fixture - uchannel)\n")
outfile.write("Z: "+str(L1_stereo_bot_physical_edge_ubasis[0]-Bottom_uchannel_measurements.get_L1_stereo_frontedge()[0])+"  Y: "+str(L1_stereo_bot_physical_edge_ubasis[2]-Bottom_uchannel_measurements.get_L1_stereo_frontedge()[2])+"\n")

#outfile.write("L2 Bot Axial sensor residuals (fixture - uchannel)\n")
#outfile.write("Z: "+str(L2_axial_bot_physical_edge_ubasis[0]-Bottom_uchannel_measurements.get_L2_axial_backedge()[0])+"  Y: "+str(L2_axial_bot_physical_edge_ubasis[2]-Bottom_uchannel_measurements.get_L2_axial_backedge()[2])+"\n")
#outfile.write("L2 Bot Stereo sensor residuals (fixture - uchannel)\n")
#outfile.write("Z: "+str(L2_stereo_bot_physical_edge_ubasis[0]-Bottom_uchannel_measurements.get_L2_stereo_frontedge()[0])+"  Y: "+str(L2_stereo_bot_physical_edge_ubasis[2]-Bottom_uchannel_measurements.get_L2_stereo_frontedge()[2])+"\n")

#outfile.write("L3 Bot Axial sensor residuals (fixture - uchannel)\n")
#outfile.write("Z: "+str(L3_axial_bot_physical_edge_ubasis[0]-Bottom_uchannel_measurements.get_L3_axial_backedge()[0])+"  Y: "+str(L3_axial_bot_physical_edge_ubasis[2]-Bottom_uchannel_measurements.get_L3_axial_backedge()[2])+"\n")
#outfile.write("L3 Bot Stereo sensor residuals (fixture - uchannel)\n")
#outfile.write("Z: "+str(L3_stereo_bot_physical_edge_ubasis[0]-Bottom_uchannel_measurements.get_L3_stereo_frontedge()[0])+"  Y: "+str(L3_stereo_bot_physical_edge_ubasis[2]-Bottom_uchannel_measurements.get_L3_stereo_frontedge()[2])+"\n")

outfile.write("\n")

outfile.write("L0 Top Axial sensor in JLab frame\n")
#outfile.write("Origin: "+str(L0_axial_top_origin_JLab)+"  Normal: "+str(L0_axial_top_origin_JLab)+"\n")
outfile.write("Origin: "+str(L0_axial_top_origin_JLab)+"  Normal: "+str(L0_axial_top_normal_JLab)+"\n")
outfile.write("L0 Top Stereo sensor in JLab frame\n")
#outfile.write("Origin: "+str(L0_stereo_top_origin_JLab)+"  Normal: "+str(L0_stereo_top_origin_JLab)+"\n")
outfile.write("Origin: "+str(L0_stereo_top_origin_JLab)+"  Normal: "+str(L0_stereo_top_normal_JLab)+"\n")

outfile.write("L1 Top Axial sensor in JLab frame\n")
#outfile.write("Origin: "+str(L1_axial_top_origin_JLab)+"  Normal: "+str(L1_axial_top_origin_JLab)+"\n")
outfile.write("Origin: "+str(L1_axial_top_origin_JLab)+"  Normal: "+str(L1_axial_top_normal_JLab)+"\n")
outfile.write("L1 Top Stereo sensor in JLab frame\n")
#outfile.write("Origin: "+str(L1_stereo_top_origin_JLab)+"  Normal: "+str(L1_stereo_top_origin_JLab)+"\n")
outfile.write("Origin: "+str(L1_stereo_top_origin_JLab)+"  Normal: "+str(L1_stereo_top_normal_JLab)+"\n")

outfile.write("L2 Top Axial sensor in JLab frame\n")
outfile.write("Z: "+str(L2_axial_top_z)+"  Y: "+str(L2_axial_top_y)+"\n")
outfile.write("L2 Top Stereo sensor in JLab frame\n")
outfile.write("Z: "+str(L2_stereo_top_z)+"  Y: "+str(L2_stereo_top_y)+"\n")

outfile.write("L3 Top Axial sensor in JLab frame\n")
outfile.write("Z: "+str(L3_axial_top_z)+"  Y: "+str(L3_axial_top_y)+"\n")
outfile.write("L3 Top Stereo sensor in JLab frame\n")
outfile.write("Z: "+str(L3_stereo_top_z)+"  Y: "+str(L3_stereo_top_y)+"\n")

outfile.write("L0 Bot Axial sensor in JLab frame\n")
#outfile.write("Origin: "+str(L0_axial_bot_origin_JLab)+"  Normal: "+str(L0_axial_bot_origin_JLab)+"\n")
outfile.write("Origin: "+str(L0_axial_bot_origin_JLab)+"  Normal: "+str(L0_axial_bot_normal_JLab)+"\n")
outfile.write("L0 Bot Stereo sensor in JLab frame\n")
#outfile.write("Origin: "+str(L0_stereo_bot_origin_JLab)+"  Normal: "+str(L0_stereo_bot_origin_JLab)+"\n")
outfile.write("Origin: "+str(L0_stereo_bot_origin_JLab)+"  Normal: "+str(L0_stereo_bot_normal_JLab)+"\n")

outfile.write("L1 Bot Axial sensor in JLab frame\n")
#outfile.write("Origin: "+str(L1_axial_bot_origin_JLab)+"  Normal: "+str(L1_axial_bot_origin_JLab)+"\n")
outfile.write("Origin: "+str(L1_axial_bot_origin_JLab)+"  Normal: "+str(L1_axial_bot_normal_JLab)+"\n")
outfile.write("L1 Bot Stereo sensor in JLab frame\n")
#outfile.write("Origin: "+str(L1_stereo_bot_origin_JLab)+"  Normal: "+str(L1_stereo_bot_origin_JLab)+"\n")
outfile.write("Origin: "+str(L1_stereo_bot_origin_JLab)+"  Normal: "+str(L1_stereo_bot_normal_JLab)+"\n")

outfile.write("L2 Bot Axial sensor in JLab frame\n")
outfile.write("Z: "+str(L2_axial_bot_z)+"  Y: "+str(L2_axial_bot_y)+"\n")
outfile.write("L2 Bot Stereo sensor in JLab frame\n")
outfile.write("Z: "+str(L2_stereo_bot_z)+"  Y: "+str(L2_stereo_bot_y)+"\n")

outfile.write("L3 Bot Axial sensor in JLab frame\n")
outfile.write("Z: "+str(L3_axial_bot_z)+"  Y: "+str(L3_axial_bot_y)+"\n")
outfile.write("L3 Bot Stereo sensor in JLab frame\n")
outfile.write("Z: "+str(L3_stereo_bot_z)+"  Y: "+str(L3_stereo_bot_y)+"\n")

outfile.write("\n")

outfile.write("L0 Top Axial sensor residual in JLab frame\n")
outfile.write("Origin: x "+str(L0_axial_top_origin_JLab_residual[0])+"  y "+str(L0_axial_top_origin_JLab_residual[1])+"  z "+str(L0_axial_top_origin_JLab_residual[2])+"\n")
outfile.write("L0 Top Stereo sensor residual in JLab frame\n")
outfile.write("Origin: x "+str(L0_stereo_top_origin_JLab_residual[0])+"  y "+str(L0_stereo_top_origin_JLab_residual[1])+"  z "+str(L0_stereo_top_origin_JLab_residual[2])+"\n")

outfile.write("L1 Top Axial sensor residual in JLab frame\n")
outfile.write("Origin: x "+str(L1_axial_top_origin_JLab_residual[0])+"  y "+str(L1_axial_top_origin_JLab_residual[1])+"  z "+str(L1_axial_top_origin_JLab_residual[2])+"\n")
outfile.write("L1 Top Stereo sensor residual in JLab frame\n")
outfile.write("Origin: x "+str(L1_stereo_top_origin_JLab_residual[0])+"  y "+str(L1_stereo_top_origin_JLab_residual[1])+"  z "+str(L1_stereo_top_origin_JLab_residual[2])+"\n")

outfile.write("L2 Top Axial sensor residual in JLab frame\n")
outfile.write("Z: "+str(L2_axial_top_z)+"  Y: "+str(L2_axial_top_y - Nominal_Position_Data.get_L2t_physical())+"\n")
outfile.write("L2 Top Stereo sensor residual in JLab frame\n")
outfile.write("Z: "+str(L2_stereo_top_z)+"  Y: "+str(L2_stereo_top_y)+"\n")

outfile.write("L3 Top Axial sensor residual in JLab frame\n")
outfile.write("Z: "+str(L3_axial_top_z)+"  Y: "+str(L3_axial_top_y - Nominal_Position_Data.get_L3t_physical())+"\n")
outfile.write("L3 Top Stereo sensor residual in JLab frame\n")
outfile.write("Z: "+str(L3_stereo_top_z)+"  Y: "+str(L3_stereo_top_y)+"\n")

outfile.write("L0 Bot Axial sensor residual in JLab frame\n")
outfile.write("Origin: x "+str(L0_axial_bot_origin_JLab_residual[0])+"  y "+str(L0_axial_bot_origin_JLab_residual[1])+"  z "+str(L0_axial_bot_origin_JLab_residual[2])+"\n")
outfile.write("L0 Bot Stereo sensor residual in JLab frame\n")
outfile.write("Origin: x "+str(L0_stereo_bot_origin_JLab_residual[0])+"  y "+str(L0_stereo_bot_origin_JLab_residual[1])+"  z "+str(L0_stereo_bot_origin_JLab_residual[2])+"\n")

outfile.write("L1 Bot Axial sensor residual in JLab frame\n")
outfile.write("Origin: x "+str(L1_axial_bot_origin_JLab_residual[0])+"  y "+str(L1_axial_bot_origin_JLab_residual[1])+"  z "+str(L1_axial_bot_origin_JLab_residual[2])+"\n")
outfile.write("L1 Bot Stereo sensor residual in JLab frame\n")
outfile.write("Origin: x "+str(L1_stereo_bot_origin_JLab_residual[0])+"  y "+str(L1_stereo_bot_origin_JLab_residual[1])+"  z "+str(L1_stereo_bot_origin_JLab_residual[2])+"\n")

outfile.write("L2 Bot Axial sensor residual in JLab frame\n")
outfile.write("Z: "+str(L2_axial_bot_z)+"  Y: "+str(L2_axial_bot_y - Nominal_Position_Data.get_L2b_physical())+"\n")
outfile.write("L2 Bot Stereo sensor residual in JLab frame\n")
outfile.write("Z: "+str(L2_stereo_bot_z)+"  Y: "+str(L2_stereo_bot_y)+"\n")

outfile.write("L3 Bot Axial sensor residual in JLab frame\n")
outfile.write("Z: "+str(L3_axial_bot_z)+"  Y: "+str(L3_axial_bot_y - Nominal_Position_Data.get_L3b_physical())+"\n")
outfile.write("L3 Bot Stereo sensor residual in JLab frame\n")
outfile.write("Z: "+str(L3_stereo_bot_z)+"  Y: "+str(L3_stereo_bot_y)+"\n")

outfile.close()

print "Saved results to {0}".format(output)