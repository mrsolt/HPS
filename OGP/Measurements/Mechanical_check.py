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
import Al_utils

null_basis = Al_utils.make_basis(np.array([0.0, 0.0, 0.0]), #ball basis in ball frame
		np.array([1.0, 0.0, 0.0]),
		np.array([0.0, 1.0, 0.0]))

L0_axial_top = L0_axial_1_measurements.get_sensor_basis()
L0_stereo_top = L0_stereo_1_measurements.get_sensor_basis()
L1_axial_top = L0_axial_3_measurements.get_sensor_basis()
L1_stereo_top = L0_stereo_3_measurements.get_sensor_basis()

L0_axial_bot = L0_axial_2_measurements.get_sensor_basis()
L0_stereo_bot = L0_stereo_2_measurements.get_sensor_basis()
L1_axial_bot = L0_axial_5_measurements.get_sensor_basis()
L1_stereo_bot = L0_stereo_5_measurements.get_sensor_basis()

#L0_axial_top_origin_fixbasis = L0_axial_1_measurements.get_sensor_origin()
#L0_axial_top_normal_fixbasis = L0_axial_1_measurements.get_sensor_normal()
#L0_stereo_top_origin_fixbasis = L0_stereo_1_measurements.get_sensor_origin()
#L0_stereo_top_normal_fixbasis = L0_stereo_1_measurements.get_sensor_normal()

#L0_axial_bot_origin_fixbasis = L0_axial_2_measurements.get_sensor_origin()
#L0_axial_bot_normal_fixbasis = L0_axial_2_measurements.get_sensor_normal()
#L0_stereo_bot_origin_fixbasis = L0_stereo_2_measurements.get_sensor_origin()
#L0_stereo_bot_normal_fixbasis = L0_stereo_2_measurements.get_sensor_normal()

#L1_axial_top_origin_fixbasis = L0_axial_3_measurements.get_sensor_origin()
#L1_axial_top_normal_fixbasis = L0_axial_3_measurements.get_sensor_normal()
#L1_stereo_top_origin_fixbasis = L0_stereo_3_measurements.get_sensor_origin()
#L1_stereo_top_normal_fixbasis = L0_stereo_3_measurements.get_sensor_normal()

#L1_axial_bot_origin_fixbasis = L0_axial_5_measurements.get_sensor_origin()
#L1_axial_bot_normal_fixbasis = L0_axial_5_measurements.get_sensor_normal()
#L1_stereo_bot_origin_fixbasis = L0_stereo_5_measurements.get_sensor_origin()
#L1_stereo_bot_normal_fixbasis = L0_stereo_5_measurements.get_sensor_normal()

#slotpin_fixbasis = Fixture_measurements.get_slotpin()
#holepin_fixbasis = Fixture_measurements.get_holepin()
#base_normal_fixbasis = Fixture_measurements.get_normal_base_plane()
fixbasis = Fixture_measurements.get_fixbasis()
pinbasis_fixbasis_top = Fixture_measurements.get_pin_basis_top()
pinbasis_fixbasis_bot = Fixture_measurements.get_pin_basis_bot()

#L0_top_slotpin_ubasis = Top_uchannel_measurements.get_L0_slot_pin()
#L0_top_holepin_ubasis = Top_uchannel_measurements.get_L0_hole_pin()
#L1_top_slotpin_ubasis = Top_uchannel_measurements.get_L1_slot_pin()
#L1_top_holepin_ubasis = Top_uchannel_measurements.get_L1_hole_pin()
#L2_top_slotpin_ubasis = Top_uchannel_measurements.get_L2_slot_pin()
#L2_top_holepin_ubasis = Top_uchannel_measurements.get_L2_hole_pin()
#L3_top_slotpin_ubasis = Top_uchannel_measurements.get_L3_slot_pin()
#L3_top_holepin_ubasis = Top_uchannel_measurements.get_L3_hole_pin()

#L0_bot_slotpin_ubasis = Bottom_uchannel_measurements.get_L0_slot_pin()
#L0_bot_holepin_ubasis = Bottom_uchannel_measurements.get_L0_hole_pin()
#L1_bot_slotpin_ubasis = Bottom_uchannel_measurements.get_L1_slot_pin()
#L1_bot_holepin_ubasis = Bottom_uchannel_measurements.get_L1_hole_pin()
#L2_bot_slotpin_ubasis = Bottom_uchannel_measurements.get_L2_slot_pin()
#L2_bot_holepin_ubasis = Bottom_uchannel_measurements.get_L2_hole_pin()
#L3_bot_slotpin_ubasis = Bottom_uchannel_measurements.get_L3_slot_pin()
#L3_bot_holepin_ubasis = Bottom_uchannel_measurements.get_L3_hole_pin()

#pinbasis_fixbasis = Al_utils.make_pin_basis(holepin_fixbasis,slotpin_fixbasis,base_normal_fixbasis)
#pinbasis_ubasis = Al_utils.make_pin_basis(L0_bot_holepin_ubasis,L0_bot_slotpin_ubasis,Bottom_uchannel_measurements.get_L0_base_normal())

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

#pinbasis2 = Al_utils.transform_basis(fixbasis,null_basis,pinbasis)
#pinbasis3 = Al_utils.transform_basis(bot_ubasis,null_basis,pinbasis_ubasis)

#sensor_basis = [L0_axial_top_origin_fixbasis,Al_utils.make_rotation(L0_axial_top_normal_fixbasis[0],L0_axial_top_normal_fixbasis[1],L0_axial_top_normal_fixbasis[2])]
#pinbasis2 = Al_utils.transform_basis(bot_ubasis,null_basis,pinbasis)
#sensor_basis2 = Al_utils.transform_basis(fixbasis,null_basis,sensor_basis)

#sensor_origin_pinbasis = Al_utils.transform_pt(pinbasis,sensor_basis2,L0_axial_top_origin_fixbasis)
#sensor_normal_pinbasis = Al_utils.transform_vec(pinbasis,sensor_basis2,L0_axial_top_normal_fixbasis)

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


#print top_L0_pinbasis[0]
#print L0_axial_top_physical_edge_pinbasis 
#print L0_axial_top_origin_pinbasis 
#print L0_axial_top[2]
#print L0_axial_top[0]
#print ""



#bot_L0_pinbasis_ubasis = Al_utils.transform_basis(bot_ubasis,null_basis,bot_L0_pinbasis)
#top_L0_pinbasis_ubasis = Al_utils.transform_basis(top_ubasis,null_basis,top_L0_pinbasis)

top_L0_pinbasis_ubasis = Al_utils.transform_basis(top_L0_pinbasis,null_basis,top_ubasis)
top_L1_pinbasis_ubasis = Al_utils.transform_basis(top_L1_pinbasis,null_basis,top_ubasis)
top_L2_pinbasis_ubasis = Al_utils.transform_basis(top_L2_pinbasis,null_basis,top_ubasis)
top_L3_pinbasis_ubasis = Al_utils.transform_basis(top_L3_pinbasis,null_basis,top_ubasis)
bot_L0_pinbasis_ubasis = Al_utils.transform_basis(bot_L0_pinbasis,null_basis,bot_ubasis)
bot_L1_pinbasis_ubasis = Al_utils.transform_basis(bot_L1_pinbasis,null_basis,bot_ubasis)
bot_L2_pinbasis_ubasis = Al_utils.transform_basis(bot_L2_pinbasis,null_basis,bot_ubasis)
bot_L3_pinbasis_ubasis = Al_utils.transform_basis(bot_L3_pinbasis,null_basis,bot_ubasis)

#Al_utils.transform_pt(top_L0_pinbasis_ubasis,L0_axial_top,L0_axial_top_origin_pinbasis)

#sensor_origin_ubasis = Al_utils.transform_pt(bot_ubasis,bot_L0_pinbasis_ubasis,sensor_origin_pinbasis)
#sensor_normal_ubasis = Al_utils.transform_vec(bot_ubasis,bot_L0_pinbasis_ubasis,sensor_normal_pinbasis)

L0_axial_top_origin_ubasis = Al_utils.transform_pt(top_L0_pinbasis_ubasis,top_ubasis,L0_axial_top_origin_pinbasis)
L0_stereo_top_origin_ubasis = Al_utils.transform_pt(top_L0_pinbasis_ubasis,top_ubasis,L0_stereo_top_origin_pinbasis)
L1_axial_top_origin_ubasis = Al_utils.transform_pt(top_L1_pinbasis_ubasis,top_ubasis,L1_axial_top_origin_pinbasis)
L1_stereo_top_origin_ubasis = Al_utils.transform_pt(top_L1_pinbasis_ubasis,top_ubasis,L1_stereo_top_origin_pinbasis)

L0_axial_bot_origin_ubasis = Al_utils.transform_pt(bot_L0_pinbasis_ubasis,bot_ubasis,L0_axial_bot_origin_pinbasis)
L0_stereo_bot_origin_ubasis = Al_utils.transform_pt(bot_L0_pinbasis_ubasis,bot_ubasis,L0_stereo_bot_origin_pinbasis)
L1_axial_bot_origin_ubasis = Al_utils.transform_pt(bot_L1_pinbasis_ubasis,bot_ubasis,L1_axial_bot_origin_pinbasis)
L1_stereo_bot_origin_ubasis = Al_utils.transform_pt(bot_L1_pinbasis_ubasis,bot_ubasis,L1_stereo_bot_origin_pinbasis)

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

print "L0 axial top- z beam: " + str(L0_axial_top_physical_edge_ubasis[0]) + "  y vert: " + str(L0_axial_top_physical_edge_ubasis[2]) + "  stereo angle: " + str(L0_axial_top_physical_edge_vector_ubasis[2]/L0_axial_top_physical_edge_vector_ubasis[1]) + "  Fixture Measurements in Uchannel frame"
print "L0 axial top- z beam: " + str(Top_uchannel_measurements.get_L0_axial_frontedge()[0]) + "  y vert: " + str(Top_uchannel_measurements.get_L0_axial_frontedge()[2])+ "  stereo angle: " + str(Top_uchannel_measurements.get_L0_axial_frontedge_normal()[2]/Top_uchannel_measurements.get_L0_axial_frontedge_normal()[1]) + "  Uchannel Measurements in Uchannel frame"
print "L0 axial top Active- z beam: " + str(L0_axial_top_active_edge_ubasis[0]) + "  y vert: " + str(L0_axial_top_active_edge_ubasis[2]) + "  stereo angle: " + str(L0_axial_top_active_edge_vector_ubasis[2]/L0_axial_top_active_edge_vector_ubasis[1]) + "  Fixture Measurements in Uchannel frame"

print ""
print "L0 stereo top- z beam: " + str(L0_stereo_top_physical_edge_ubasis[0]) + "  y vert: " + str(L0_stereo_top_physical_edge_ubasis[2]) + "  stereo angle: " + str(L0_stereo_top_physical_edge_vector_ubasis[2]/L0_stereo_top_physical_edge_vector_ubasis[1]) + "  Fixture Measurements in Uchannel frame"
print "L0 stereo top- z beam: " + str(Top_uchannel_measurements.get_L0_stereo_backedge()[0]) + "  y vert: " + str(Top_uchannel_measurements.get_L0_stereo_backedge()[2])+ "  stereo angle: " + str(Top_uchannel_measurements.get_L0_stereo_backedge_normal()[2]/Top_uchannel_measurements.get_L0_stereo_backedge_normal()[1]) + "  Uchannel Measurements in Uchannel frame"
print "L0 stereo top Active- z beam: " + str(L0_stereo_top_active_edge_ubasis[0]) + "  y vert: " + str(L0_stereo_top_active_edge_ubasis[2]) + "  stereo angle: " + str(L0_stereo_top_active_edge_vector_ubasis[2]/L0_stereo_top_active_edge_vector_ubasis[1]) + "  Fixture Measurements in Uchannel frame"
print ""
print "L1 axial top- z beam: " + str(L1_axial_top_physical_edge_ubasis[0]) + "  y vert: " + str(L1_axial_top_physical_edge_ubasis[2]) + "  stereo angle: " + str(L1_axial_top_physical_edge_vector_ubasis[2]/L1_axial_top_physical_edge_vector_ubasis[1]) + "  Fixture Measurements in Uchannel frame"
print "L1 axial top- z beam: " + str(Top_uchannel_measurements.get_L1_axial_frontedge()[0]) + "  y vert: " + str(Top_uchannel_measurements.get_L1_axial_frontedge()[2])+ "  stereo angle: " + str(Top_uchannel_measurements.get_L1_axial_frontedge_normal()[2]/Top_uchannel_measurements.get_L1_axial_frontedge_normal()[1]) + "  Uchannel Measurements in Uchannel frame"
print "L1 axial top Active- z beam: " + str(L1_axial_top_active_edge_ubasis[0]) + "  y vert: " + str(L1_axial_top_active_edge_ubasis[2]) + "  stereo angle: " + str(L1_axial_top_active_edge_vector_ubasis[2]/L1_axial_top_active_edge_vector_ubasis[1]) + "  Fixture Measurements in Uchannel frame"
print ""
print "L1 stereo top- z beam: " + str(L1_stereo_top_physical_edge_ubasis[0]) + "  y vert: " + str(L1_stereo_top_physical_edge_ubasis[2]) + "  stereo angle: " + str(L1_stereo_top_physical_edge_vector_ubasis[2]/L1_stereo_top_physical_edge_vector_ubasis[1]) + "  Fixture Measurements in Uchannel frame"
print "L1 stereo top- z beam: " + str(Top_uchannel_measurements.get_L1_stereo_backedge()[0]) + "  y vert: " + str(Top_uchannel_measurements.get_L1_stereo_backedge()[2])+ "  stereo angle: " + str(Top_uchannel_measurements.get_L1_stereo_backedge_normal()[2]/Top_uchannel_measurements.get_L1_stereo_backedge_normal()[1]) + "  Uchannel Measurements in Uchannel frame"
print "L1 stereo top Active- z beam: " + str(L1_stereo_top_active_edge_ubasis[0]) + "  y vert: " + str(L1_stereo_top_active_edge_ubasis[2]) + "  stereo angle: " + str(L1_stereo_top_active_edge_vector_ubasis[2]/L1_stereo_top_active_edge_vector_ubasis[1]) + "  Fixture Measurements in Uchannel frame"
print ""
print "L2 axial top- z beam: " + str(Top_uchannel_measurements.get_L2_axial_frontedge()[0]) + "  y vert: " + str(Top_uchannel_measurements.get_L2_axial_frontedge()[2])+ "  stereo angle: " + str(Top_uchannel_measurements.get_L2_axial_frontedge_normal()[2]/Top_uchannel_measurements.get_L2_axial_frontedge_normal()[1]) + "  Uchannel Measurements in Uchannel frame"
print ""
print "L2 stereo top- z beam: " + str(Top_uchannel_measurements.get_L2_stereo_backedge()[0]) + "  y vert: " + str(Top_uchannel_measurements.get_L2_stereo_backedge()[2])+ "  stereo angle: " + str(Top_uchannel_measurements.get_L2_stereo_backedge_normal()[2]/Top_uchannel_measurements.get_L2_stereo_backedge_normal()[1]) + "  Uchannel Measurements in Uchannel frame"
print ""
print "L3 axial top- z beam: " + str(Top_uchannel_measurements.get_L3_axial_frontedge()[0]) + "  y vert: " + str(Top_uchannel_measurements.get_L3_axial_frontedge()[2])+ "  stereo angle: " + str(Top_uchannel_measurements.get_L3_axial_frontedge_normal()[2]/Top_uchannel_measurements.get_L3_axial_frontedge_normal()[1]) + "  Uchannel Measurements in Uchannel frame"
print ""
print "L3 stereo top- z beam: " + str(Top_uchannel_measurements.get_L3_stereo_backedge()[0]) + "  y vert: " + str(Top_uchannel_measurements.get_L3_stereo_backedge()[2])+ "  stereo angle: " + str(Top_uchannel_measurements.get_L3_stereo_backedge_normal()[2]/Top_uchannel_measurements.get_L3_stereo_backedge_normal()[1]) + "  Uchannel Measurements in Uchannel frame"
print ""

print "L0 axial bot- z beam: " + str(L0_axial_bot_physical_edge_ubasis[0]) + "  y vert: " + str(L0_axial_bot_physical_edge_ubasis[2]) + "  stereo angle: " + str(L0_axial_bot_physical_edge_vector_ubasis[2]/L0_axial_bot_physical_edge_vector_ubasis[1]) + "  Fixture Measurements in Uchannel frame"
print "L0 axial bot- z beam: " + str(Bottom_uchannel_measurements.get_L0_axial_backedge()[0]) + "  y vert: " + str(Bottom_uchannel_measurements.get_L0_axial_backedge()[2])+ "  stereo angle: " + str(Bottom_uchannel_measurements.get_L0_axial_backedge_normal()[2]/Bottom_uchannel_measurements.get_L0_axial_backedge_normal()[1]) + "  Uchannel Measurements in Uchannel frame"
print "L0 axial bot Active- z beam: " + str(L0_axial_bot_active_edge_ubasis[0]) + "  y vert: " + str(L0_axial_bot_active_edge_ubasis[2]) + "  stereo angle: " + str(L0_axial_bot_active_edge_vector_ubasis[2]/L0_axial_bot_active_edge_vector_ubasis[1]) + "  Fixture Measurements in Uchannel frame"
print ""
print "L0 stereo bot- z beam: " + str(L0_stereo_bot_physical_edge_ubasis[0]) + "  y vert: " + str(L0_stereo_bot_physical_edge_ubasis[2]) + "  stereo angle: " + str(L0_stereo_bot_physical_edge_vector_ubasis[2]/L0_stereo_bot_physical_edge_vector_ubasis[1]) + "  Fixture Measurements in Uchannel frame"
print "L0 stereo bot- z beam: " + str(Bottom_uchannel_measurements.get_L0_stereo_frontedge()[0]) + "  y vert: " + str(Bottom_uchannel_measurements.get_L0_stereo_frontedge()[2])+ "  stereo angle: " + str(Bottom_uchannel_measurements.get_L0_stereo_frontedge_normal()[2]/Bottom_uchannel_measurements.get_L0_stereo_frontedge_normal()[1]) + "  Uchannel Measurements in Uchannel frame"
print "L0 stereo bot Active- z beam: " + str(L0_stereo_bot_active_edge_ubasis[0]) + "  y vert: " + str(L0_stereo_bot_active_edge_ubasis[2]) + "  stereo angle: " + str(L0_stereo_bot_active_edge_vector_ubasis[2]/L0_stereo_bot_active_edge_vector_ubasis[1]) + "  Fixture Measurements in Uchannel frame"
print ""
print "L1 axial bot- z beam: " + str(L1_axial_bot_physical_edge_ubasis[0]) + "  y vert: " + str(L1_axial_bot_physical_edge_ubasis[2]) + "  stereo angle: " + str(L1_axial_bot_physical_edge_vector_ubasis[2]/L1_axial_bot_physical_edge_vector_ubasis[1]) + "  Fixture Measurements in Uchannel frame"
print "L1 axial bot- z beam: " + str(Bottom_uchannel_measurements.get_L1_axial_backedge()[0]) + "  y vert: " + str(Bottom_uchannel_measurements.get_L1_axial_backedge()[2])+ "  stereo angle: " + str(Bottom_uchannel_measurements.get_L1_axial_backedge_normal()[2]/Bottom_uchannel_measurements.get_L1_axial_backedge_normal()[1]) + "  Uchannel Measurements in Uchannel frame"
print "L1 axial bot Active- z beam: " + str(L1_axial_bot_active_edge_ubasis[0]) + "  y vert: " + str(L1_axial_bot_active_edge_ubasis[2]) + "  stereo angle: " + str(L1_axial_bot_active_edge_vector_ubasis[2]/L1_axial_bot_active_edge_vector_ubasis[1]) + "  Fixture Measurements in Uchannel frame"
print ""
print "L1 stereo bot- z beam: " + str(L1_stereo_bot_physical_edge_ubasis[0]) + "  y vert: " + str(L1_stereo_bot_physical_edge_ubasis[2]) + "  stereo angle: " + str(L1_stereo_bot_physical_edge_vector_ubasis[2]/L1_stereo_bot_physical_edge_vector_ubasis[1]) + "  Fixture Measurements in Uchannel frame"
print "L1 stereo bot- z beam: " + str(Bottom_uchannel_measurements.get_L1_stereo_frontedge()[0]) + "  y vert: " + str(Bottom_uchannel_measurements.get_L1_stereo_frontedge()[2])+ "  stereo angle: " + str(Bottom_uchannel_measurements.get_L1_stereo_frontedge_normal()[2]/Bottom_uchannel_measurements.get_L1_stereo_frontedge_normal()[1]) + "  Uchannel Measurements in Uchannel frame"
print "L1 stereo bot Active- z beam: " + str(L1_stereo_bot_active_edge_ubasis[0]) + "  y vert: " + str(L1_stereo_bot_active_edge_ubasis[2]) + "  stereo angle: " + str(L1_stereo_bot_active_edge_vector_ubasis[2]/L1_stereo_bot_active_edge_vector_ubasis[1]) + "  Fixture Measurements in Uchannel frame"
print ""
print "L2 axial bot- z beam: " + str(Bottom_uchannel_measurements.get_L2_axial_backedge()[0]) + "  y vert: " + str(Bottom_uchannel_measurements.get_L2_axial_backedge()[2])+ "  stereo angle: " + str(Bottom_uchannel_measurements.get_L2_axial_backedge_normal()[2]/Bottom_uchannel_measurements.get_L2_axial_backedge_normal()[1]) + "  Uchannel Measurements in Uchannel frame"
print ""
print "L2 stereo bot- z beam: " + str(Bottom_uchannel_measurements.get_L2_stereo_frontedge()[0]) + "  y vert: " + str(Bottom_uchannel_measurements.get_L2_stereo_frontedge()[2])+ "  stereo angle: " + str(Bottom_uchannel_measurements.get_L2_stereo_frontedge_normal()[2]/Bottom_uchannel_measurements.get_L2_stereo_frontedge_normal()[1]) + "  Uchannel Measurements in Uchannel frame"
print ""
print "L3 axial bot- z beam: " + str(Bottom_uchannel_measurements.get_L3_axial_backedge()[0]) + "  y vert: " + str(Bottom_uchannel_measurements.get_L3_axial_backedge()[2])+ "  stereo angle: " + str(Bottom_uchannel_measurements.get_L3_axial_backedge_normal()[2]/Bottom_uchannel_measurements.get_L3_axial_backedge_normal()[1]) + "  Uchannel Measurements in Uchannel frame"
print ""
print "L3 stereo bot- z beam: " + str(Bottom_uchannel_measurements.get_L3_stereo_frontedge()[0]) + "  y vert: " + str(Bottom_uchannel_measurements.get_L3_stereo_frontedge()[2])+ "  stereo angle: " + str(Bottom_uchannel_measurements.get_L3_stereo_frontedge_normal()[2]/Bottom_uchannel_measurements.get_L3_stereo_frontedge_normal()[1]) + "  Uchannel Measurements in Uchannel frame"

#print L0_axial_top[0]
#print ""
#print pinbasis_fixbasis_top
#print ""
#print fixbasis
#print ""
#print top_L0_pinbasis[0]
#print ""
#print L0_axial_top_origin_pinbasis
#print ""
#print top_L0_pinbasis_ubasis
#print ""
#print top_ubasis
#print ""
#print L0_axial_top_origin_ubasis
#print ""
#print Top_uchannel_measurements.get_L0_axial_frontedge()
#print ""
#print L0_axial_top_physical_edge_ubasis
#print ""
#print Top_uchannel_measurements.get_L0_axial_frontedge_normal()
#print ""
#print L0_axial_top_physical_edge_vector_ubasis
#print Top_uchannel_measurements.get_L0_stereo_backedge_normal()
#print ""
#print L0_stereo_top_physical_edge_vector_ubasis



#print L0_axial_top_active_edge_ubasis
#print L0_stereo_top_active_edge_ubasis
#print L1_axial_top_active_edge_ubasis
#print L1_stereo_top_active_edge_ubasis
#print L0_axial_bot_active_edge_ubasis
#print L0_stereo_bot_active_edge_ubasis
#print L1_axial_bot_active_edge_ubasis
#print L1_stereo_bot_active_edge_ubasis
#print ""

#print L0_axial_top_physical_edge_ubasis
#print Top_uchannel_measurements.get_L0_axial_frontedge()
#print L0_stereo_top_physical_edge_ubasis
#print Top_uchannel_measurements.get_L0_stereo_backedge()
#print L1_axial_top_physical_edge_ubasis
#print Top_uchannel_measurements.get_L1_axial_frontedge()
#print L1_stereo_top_physical_edge_ubasis
#print Top_uchannel_measurements.get_L1_stereo_backedge()
#print L0_axial_bot_physical_edge_ubasis
#print Bottom_uchannel_measurements.get_L0_axial_backedge()
#print L0_stereo_bot_physical_edge_ubasis
#print Bottom_uchannel_measurements.get_L0_stereo_frontedge()
#print L1_axial_bot_physical_edge_ubasis
#print Bottom_uchannel_measurements.get_L1_axial_backedge()
#print L1_stereo_bot_physical_edge_ubasis
#print Bottom_uchannel_measurements.get_L1_stereo_frontedge()
#print ""


#print L0_axial_top_origin_ubasis
#print Top_uchannel_measurements.get_L0_axial_frontedge()
#print L1_axial_top_origin_ubasis
#print Top_uchannel_measurements.get_L1_axial_frontedge()
#print L0_stereo_top_origin_ubasis
#print Top_uchannel_measurements.get_L0_stereo_backedge()
#print L1_stereo_top_origin_ubasis
#print Top_uchannel_measurements.get_L1_stereo_backedge()
#print ""

#print L0_axial_bot_origin_ubasis
#print Bottom_uchannel_measurements.get_L0_axial_backedge()
#print L1_axial_bot_origin_ubasis
#print Bottom_uchannel_measurements.get_L1_axial_backedge()
#print L0_stereo_bot_origin_ubasis
#print Bottom_uchannel_measurements.get_L0_stereo_frontedge()
#print L1_stereo_bot_origin_ubasis
#print Bottom_uchannel_measurements.get_L1_stereo_frontedge()
#print ""

#print L0_axial_top_origin_pinbasis
#print L0_axial_top_normal_pinbasis
#print L0_stereo_top_origin_pinbasis
#print L0_stereo_top_normal_pinbasis
#print L1_axial_top_origin_pinbasis
#print L1_axial_top_normal_pinbasis
#print L1_stereo_top_origin_pinbasis
#print L1_stereo_top_normal_pinbasis

#print L0_axial_bot_origin_pinbasis
#print L0_axial_bot_normal_pinbasis
#print L0_stereo_bot_origin_pinbasis
#print L0_stereo_bot_normal_pinbasis
#print L1_axial_bot_origin_pinbasis
#print L1_axial_bot_normal_pinbasis
#print L1_stereo_bot_origin_pinbasis
#print L1_stereo_bot_normal_pinbasis

#print fixbasis
#print pinbasis_fixbasis_top

#print ""

#print Top_uchannel_measurements.get_L0_axial_frontedge()
#print Top_uchannel_measurements.get_L1_axial_frontedge()
#print Top_uchannel_measurements.get_L2_axial_frontedge()
#print Top_uchannel_measurements.get_L3_axial_frontedge()

#print Top_uchannel_measurements.get_L0_axial_frontedge_normal()
#print L0_axial_top_physical_edge_vector_ubasis
#print Top_uchannel_measurements.get_L1_axial_frontedge_normal()
#print L1_axial_top_physical_edge_vector_ubasis
#print Top_uchannel_measurements.get_L2_axial_frontedge_normal()
#print Top_uchannel_measurements.get_L3_axial_frontedge_normal()

#print ""

#print Bottom_uchannel_measurements.get_L0_axial_backedge()
#print Bottom_uchannel_measurements.get_L1_axial_backedge()
#print Bottom_uchannel_measurements.get_L2_axial_backedge()
#print Bottom_uchannel_measurements.get_L3_axial_backedge()

#print Bottom_uchannel_measurements.get_L0_axial_backedge_normal()
#print L0_axial_bot_physical_edge_vector_ubasis
#print Bottom_uchannel_measurements.get_L1_axial_backedge_normal()
#print L1_axial_bot_physical_edge_vector_ubasis
#print Bottom_uchannel_measurements.get_L2_axial_backedge_normal()
#print Bottom_uchannel_measurements.get_L3_axial_backedge_normal()

#print ""

#print Top_uchannel_measurements.get_L0_stereo_backedge_normal()
#print L0_stereo_top_physical_edge_vector_ubasis
#print Top_uchannel_measurements.get_L1_stereo_backedge_normal()
#print L1_stereo_top_physical_edge_vector_ubasis

#print Bottom_uchannel_measurements.get_L0_stereo_frontedge_normal()
#print L0_stereo_bot_physical_edge_vector_ubasis
#print Bottom_uchannel_measurements.get_L1_stereo_frontedge_normal()
#print L1_stereo_bot_physical_edge_vector_ubasis

#print ""

#print L0_axial_top[5]
#print L0_axial_top_physical_edge_vector_pinbasis
#print L0_axial_top_physical_edge_vector_ubasis

#print ""

#print L0_axial_top[0]
#print L0_axial_top_origin_pinbasis
#print L0_axial_top_origin_ubasis
