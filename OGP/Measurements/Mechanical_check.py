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

fixbasis = Fixture_measurements.get_fixbasis()
pinbasis_fixbasis_top = Fixture_measurements.get_pin_basis_top()
pinbasis_fixbasis_bot = Fixture_measurements.get_pin_basis_bot()

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

top_L0_pinbasis_ubasis = Al_utils.transform_basis(top_L0_pinbasis,null_basis,top_ubasis)
top_L1_pinbasis_ubasis = Al_utils.transform_basis(top_L1_pinbasis,null_basis,top_ubasis)
top_L2_pinbasis_ubasis = Al_utils.transform_basis(top_L2_pinbasis,null_basis,top_ubasis)
top_L3_pinbasis_ubasis = Al_utils.transform_basis(top_L3_pinbasis,null_basis,top_ubasis)
bot_L0_pinbasis_ubasis = Al_utils.transform_basis(bot_L0_pinbasis,null_basis,bot_ubasis)
bot_L1_pinbasis_ubasis = Al_utils.transform_basis(bot_L1_pinbasis,null_basis,bot_ubasis)
bot_L2_pinbasis_ubasis = Al_utils.transform_basis(bot_L2_pinbasis,null_basis,bot_ubasis)
bot_L3_pinbasis_ubasis = Al_utils.transform_basis(bot_L3_pinbasis,null_basis,bot_ubasis)

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
print "L0 axial top Active- z beam: " + str(Nominal_Position_Data.get_beam_top_L0()[0]) + " y vert: " + str(Nominal_Position_Data.get_beam_top_L0()[2]-0.75) + " Nominal Measurements"

print ""
print "L0 stereo top- z beam: " + str(L0_stereo_top_physical_edge_ubasis[0]) + "  y vert: " + str(L0_stereo_top_physical_edge_ubasis[2]) + "  stereo angle: " + str(L0_stereo_top_physical_edge_vector_ubasis[2]/L0_stereo_top_physical_edge_vector_ubasis[1]) + "  Fixture Measurements in Uchannel frame"
print "L0 stereo top- z beam: " + str(Top_uchannel_measurements.get_L0_stereo_backedge()[0]) + "  y vert: " + str(Top_uchannel_measurements.get_L0_stereo_backedge()[2])+ "  stereo angle: " + str(Top_uchannel_measurements.get_L0_stereo_backedge_normal()[2]/Top_uchannel_measurements.get_L0_stereo_backedge_normal()[1]) + "  Uchannel Measurements in Uchannel frame"
print "L0 stereo top Active- z beam: " + str(L0_stereo_top_active_edge_ubasis[0]) + "  y vert: " + str(L0_stereo_top_active_edge_ubasis[2]) + "  stereo angle: " + str(L0_stereo_top_active_edge_vector_ubasis[2]/L0_stereo_top_active_edge_vector_ubasis[1]) + "  Fixture Measurements in Uchannel frame"
print ""
print "L1 axial top- z beam: " + str(L1_axial_top_physical_edge_ubasis[0]) + "  y vert: " + str(L1_axial_top_physical_edge_ubasis[2]) + "  stereo angle: " + str(L1_axial_top_physical_edge_vector_ubasis[2]/L1_axial_top_physical_edge_vector_ubasis[1]) + "  Fixture Measurements in Uchannel frame"
print "L1 axial top- z beam: " + str(Top_uchannel_measurements.get_L1_axial_frontedge()[0]) + "  y vert: " + str(Top_uchannel_measurements.get_L1_axial_frontedge()[2])+ "  stereo angle: " + str(Top_uchannel_measurements.get_L1_axial_frontedge_normal()[2]/Top_uchannel_measurements.get_L1_axial_frontedge_normal()[1]) + "  Uchannel Measurements in Uchannel frame"
print "L1 axial top Active- z beam: " + str(L1_axial_top_active_edge_ubasis[0]) + "  y vert: " + str(L1_axial_top_active_edge_ubasis[2]) + "  stereo angle: " + str(L1_axial_top_active_edge_vector_ubasis[2]/L1_axial_top_active_edge_vector_ubasis[1]) + "  Fixture Measurements in Uchannel frame"
print "L1 axial top Active- z beam: " + str(Nominal_Position_Data.get_beam_top_L1()[0]) + " y vert: " + str(Nominal_Position_Data.get_beam_top_L1()[2]-1.5+0.4) + " Nominal Measurements"
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
print "L0 axial bot Active- z beam: " + str(Nominal_Position_Data.get_beam_bottom_L0()[0]) + " y vert: " + str(Nominal_Position_Data.get_beam_bottom_L0()[2]-0.75) + " Nominal Measurements"
print ""
print "L0 stereo bot- z beam: " + str(L0_stereo_bot_physical_edge_ubasis[0]) + "  y vert: " + str(L0_stereo_bot_physical_edge_ubasis[2]) + "  stereo angle: " + str(L0_stereo_bot_physical_edge_vector_ubasis[2]/L0_stereo_bot_physical_edge_vector_ubasis[1]) + "  Fixture Measurements in Uchannel frame"
print "L0 stereo bot- z beam: " + str(Bottom_uchannel_measurements.get_L0_stereo_frontedge()[0]) + "  y vert: " + str(Bottom_uchannel_measurements.get_L0_stereo_frontedge()[2])+ "  stereo angle: " + str(Bottom_uchannel_measurements.get_L0_stereo_frontedge_normal()[2]/Bottom_uchannel_measurements.get_L0_stereo_frontedge_normal()[1]) + "  Uchannel Measurements in Uchannel frame"
print "L0 stereo bot Active- z beam: " + str(L0_stereo_bot_active_edge_ubasis[0]) + "  y vert: " + str(L0_stereo_bot_active_edge_ubasis[2]) + "  stereo angle: " + str(L0_stereo_bot_active_edge_vector_ubasis[2]/L0_stereo_bot_active_edge_vector_ubasis[1]) + "  Fixture Measurements in Uchannel frame"
print ""
print "L1 axial bot- z beam: " + str(L1_axial_bot_physical_edge_ubasis[0]) + "  y vert: " + str(L1_axial_bot_physical_edge_ubasis[2]) + "  stereo angle: " + str(L1_axial_bot_physical_edge_vector_ubasis[2]/L1_axial_bot_physical_edge_vector_ubasis[1]) + "  Fixture Measurements in Uchannel frame"
print "L1 axial bot- z beam: " + str(Bottom_uchannel_measurements.get_L1_axial_backedge()[0]) + "  y vert: " + str(Bottom_uchannel_measurements.get_L1_axial_backedge()[2])+ "  stereo angle: " + str(Bottom_uchannel_measurements.get_L1_axial_backedge_normal()[2]/Bottom_uchannel_measurements.get_L1_axial_backedge_normal()[1]) + "  Uchannel Measurements in Uchannel frame"
print "L1 axial bot Active- z beam: " + str(L1_axial_bot_active_edge_ubasis[0]) + "  y vert: " + str(L1_axial_bot_active_edge_ubasis[2]) + "  stereo angle: " + str(L1_axial_bot_active_edge_vector_ubasis[2]/L1_axial_bot_active_edge_vector_ubasis[1]) + "  Fixture Measurements in Uchannel frame"
print "L1 axial bot Active- z beam: " + str(Nominal_Position_Data.get_beam_bottom_L1()[0]) + " y vert: " + str(Nominal_Position_Data.get_beam_bottom_L1()[2]-1.5+0.4) + " Nominal Measurements"
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

print ""

L0_slim_edge = -0.25
L2_edge = 1.0
L0_beam_y = Nominal_Position_Data.get_beam_top_L0()[2]-0.5
L1_beam_y = Nominal_Position_Data.get_beam_top_L0()[2]-1.25+0.4
L2_beam_y = Nominal_Position_Data.get_beam_top_L0()[2]-3.0+0.7+L2_edge
L3_beam_y = Nominal_Position_Data.get_beam_top_L0()[2]-4.5+0.7+L2_edge

L0_axial_top_y_physical_edge_fixture = L0_axial_top_physical_edge_ubasis[2] - L0_beam_y
L0_axial_top_y_physical_edge_uchannel = Top_uchannel_measurements.get_L0_axial_frontedge()[2] - L0_beam_y
L0_axial_top_y_active_edge_fixture = L0_axial_top_active_edge_ubasis[2] - L0_slim_edge - L0_beam_y
L0_axial_top_y_active_edge_uchannel = Top_uchannel_measurements.get_L0_axial_frontedge()[2] - L0_beam_y

L1_axial_top_y_physical_edge_fixture = L1_axial_top_physical_edge_ubasis[2] - L1_beam_y
L1_axial_top_y_physical_edge_uchannel = Top_uchannel_measurements.get_L1_axial_frontedge()[2] - L1_beam_y
L1_axial_top_y_active_edge_fixture = L1_axial_top_active_edge_ubasis[2] - L0_slim_edge - L1_beam_y
L1_axial_top_y_active_edge_uchannel = Top_uchannel_measurements.get_L1_axial_frontedge()[2] - L1_beam_y

#L2_axial_top_y_physical_edge_fixture = L2_axial_top_physical_edge_ubasis[2] - L2_beam_y
L2_axial_top_y_physical_edge_uchannel = Top_uchannel_measurements.get_L2_axial_frontedge()[2] - L2_beam_y
#L2_axial_top_y_active_edge_fixture = L2_axial_top_active_edge_ubasis[2] - L2_beam_y
L2_axial_top_y_active_edge_uchannel = Top_uchannel_measurements.get_L2_axial_frontedge()[2] - L2_beam_y

#L3_axial_top_y_physical_edge_fixture = L3_axial_top_physical_edge_ubasis[2] - L3_beam_y
L3_axial_top_y_physical_edge_uchannel = Top_uchannel_measurements.get_L3_axial_frontedge()[2] - L3_beam_y
#L3_axial_top_y_active_edge_fixture = L3_axial_top_active_edge_ubasis[2] - L3_beam_y
L3_axial_top_y_active_edge_uchannel = Top_uchannel_measurements.get_L3_axial_frontedge()[2] - L3_beam_y

L0_axial_bot_y_physical_edge_fixture = L0_axial_bot_physical_edge_ubasis[2] - L0_beam_y
L0_axial_bot_y_physical_edge_uchannel = Bottom_uchannel_measurements.get_L0_axial_backedge()[2] - L0_beam_y
L0_axial_bot_y_active_edge_fixture = L0_axial_bot_active_edge_ubasis[2] - L0_slim_edge - L0_beam_y
L0_axial_bot_y_active_edge_uchannel = Bottom_uchannel_measurements.get_L0_axial_backedge()[2] - L0_beam_y

L1_axial_bot_y_physical_edge_fixture = L1_axial_bot_physical_edge_ubasis[2] - L1_beam_y
L1_axial_bot_y_physical_edge_uchannel = Bottom_uchannel_measurements.get_L1_axial_backedge()[2] - L1_beam_y
L1_axial_bot_y_active_edge_fixture = L1_axial_bot_active_edge_ubasis[2] - L0_slim_edge - L1_beam_y
L1_axial_bot_y_active_edge_uchannel = Bottom_uchannel_measurements.get_L1_axial_backedge()[2] - L1_beam_y

#L2_axial_bot_y_physical_edge_fixture = L2_axial_bot_physical_edge_ubasis[2] - L2_beam_y
L2_axial_bot_y_physical_edge_uchannel = Bottom_uchannel_measurements.get_L2_axial_backedge()[2] - L2_beam_y
#L2_axial_bot_y_active_edge_fixture = L2_axial_bot_active_edge_ubasis[2] - L2_beam_y
L2_axial_bot_y_active_edge_uchannel = Bottom_uchannel_measurements.get_L2_axial_backedge()[2] - L2_beam_y

#L3_axial_bot_y_physical_edge_fixture = L3_axial_bot_physical_edge_ubasis[2] - L3_beam_y
L3_axial_bot_y_physical_edge_uchannel = Bottom_uchannel_measurements.get_L3_axial_backedge()[2] - L3_beam_y
#L3_axial_bot_y_active_edge_fixture = L3_axial_bot_active_edge_ubasis[2] - L3_beam_y
L3_axial_bot_y_active_edge_uchannel = Bottom_uchannel_measurements.get_L3_axial_backedge()[2] - L3_beam_y


print "L0 top physical " + str(L0_axial_top_y_physical_edge_fixture) + " " + str(L0_axial_top_y_physical_edge_uchannel)
print "L0 top active " + str(L0_axial_top_y_active_edge_fixture) + " " + str(L0_axial_top_y_active_edge_uchannel)

print "L1 top physical " + str(L1_axial_top_y_physical_edge_fixture) + " " + str(L1_axial_top_y_physical_edge_uchannel)
print "L1 top active " + str(L1_axial_top_y_active_edge_fixture) + " " + str(L1_axial_top_y_active_edge_uchannel)

print "L2 top physical " + str(L2_axial_top_y_physical_edge_uchannel)
print "L2 top active " + str(L2_axial_top_y_active_edge_uchannel)

print "L3 top physical " + str(L3_axial_top_y_physical_edge_uchannel)
print "L3 top active " + str(L3_axial_top_y_active_edge_uchannel)

print ""

print "L0 bot physical " + str(L0_axial_bot_y_physical_edge_fixture) + " " + str(L0_axial_bot_y_physical_edge_uchannel)
print "L0 bot active " + str(L0_axial_bot_y_active_edge_fixture) + " " + str(L0_axial_bot_y_active_edge_uchannel)

print "L1 bot physical " + str(L1_axial_bot_y_physical_edge_fixture) + " " + str(L1_axial_bot_y_physical_edge_uchannel)
print "L1 bot active " + str(L1_axial_bot_y_active_edge_fixture) + " " + str(L1_axial_bot_y_active_edge_uchannel)

print "L2 bot physical " + str(L2_axial_bot_y_physical_edge_uchannel)
print "L2 bot active " + str(L2_axial_bot_y_active_edge_uchannel)

print "L3 bot physical " + str(L3_axial_bot_y_physical_edge_uchannel)
print "L3 bot active " + str(L3_axial_bot_y_active_edge_uchannel)

print ""

print "New top wire w.r.t. L0 axial physical edge " + str(Top_uchannel_measurements.get_wire_par()[2] - Top_uchannel_measurements.get_L0_axial_frontedge()[2]) + "  Sho top wire w.r.t. L0 axial physical edge " + str(Sho_measurements.get_top_wire_y_wrt_L1())
print "New bot wire w.r.t. L0 axial physical edge " + str(Bottom_uchannel_measurements.get_wire_par()[2] - Bottom_uchannel_measurements.get_L0_axial_backedge()[2]) + "  Sho bot wire w.r.t. L0 axial physical edge " + str(Sho_measurements.get_bot_wire_y_wrt_L1())

print ""

print "New top wire w.r.t. UChannel " + str(Top_uchannel_measurements.get_wire_par()[2]) + "  Sho top wire w.r.t. UChannel " + str(Sho_measurements.get_top_wire_y_ubasis())
print "New bot wire w.r.t. UChannel " + str(Bottom_uchannel_measurements.get_wire_par()[2]) + "  Sho bot wire w.r.t. UChannel " + str(Sho_measurements.get_bot_wire_y_ubasis())

print ""

print "Top Physical move from Uchannel " + str(Top_uchannel_measurements.get_wire_par()[2] - Top_uchannel_measurements.get_L0_axial_frontedge()[2]-0.5)
print "Bot Physical move from Uchannel " + str(Bottom_uchannel_measurements.get_wire_par()[2] - Bottom_uchannel_measurements.get_L0_axial_backedge()[2]-0.5)

print "Top Active move " + str(Top_uchannel_measurements.get_wire_par()[2] - L0_axial_top_active_edge_ubasis[2]-0.75)
print "Bot Active move " + str(Bottom_uchannel_measurements.get_wire_par()[2] - L0_axial_bot_active_edge_ubasis[2]-0.75)

print "Top Physical move " + str(Top_uchannel_measurements.get_wire_par()[2] - L0_axial_top_physical_edge_ubasis[2]-0.5)
print "Bot Physical move " + str(Bottom_uchannel_measurements.get_wire_par()[2] - L0_axial_bot_physical_edge_ubasis[2]-0.5)