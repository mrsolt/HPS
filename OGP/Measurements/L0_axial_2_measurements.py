import numpy as np
import math
import Al_utils

def get_sensor_origin():
	sensor_origin = np.empty([3])
	sensor_origin[0] = Al_utils.getAvg(np.array(129.55768))
	sensor_origin[1] = Al_utils.getAvg(np.array(013.28766))
	sensor_origin[2] = Al_utils.getAvg(np.array(010.69635))
	return sensor_origin

def get_sensor_plane():
	sensor_plane = np.empty([5])
	sensor_plane[0] = Al_utils.getAvg(np.array(129.07913))
	sensor_plane[1] = Al_utils.getAvg(np.array(012.81650))
	sensor_plane[2] = Al_utils.getAvg(np.array(011.17015))
	sensor_plane[3] = Al_utils.getAvg(np.array(-090.10058))
	sensor_plane[4] = Al_utils.getAvg(np.array(-044.97451))
	return sensor_plane

def get_sensor_normal():
	return Al_utils.normal_vector(math.radians(get_sensor_plane()[3]),math.radians(get_sensor_plane()[4]))

def get_sensor_active_edge():
	sensor_active_edge = np.empty([5])
	sensor_active_edge[0] = Al_utils.getAvg(np.array(129.32598))
	sensor_active_edge[1] = Al_utils.getAvg(np.array(008.31806))
	sensor_active_edge[2] = Al_utils.getAvg(np.array(015.67105))
	sensor_active_edge[3] = Al_utils.getAvg(np.array(179.80910))
	sensor_active_edge[4] = Al_utils.getAvg(np.array(-000.05970))
	return sensor_active_edge

def get_sensor_active_edge_vector():
	return Al_utils.normal_vector(math.radians(get_sensor_active_edge()[3]),math.radians(get_sensor_active_edge()[4]))

def get_sensor_physical_edge():
	sensor_physical_edge = np.empty([5])
	sensor_physical_edge[0] = Al_utils.getAvg(np.array(130.00989))
	sensor_physical_edge[1] = Al_utils.getAvg(np.array(008.06279))
	sensor_physical_edge[2] = Al_utils.getAvg(np.array(015.87027))
	sensor_physical_edge[3] = Al_utils.getAvg(np.array(-179.73143))
	sensor_physical_edge[4] = Al_utils.getAvg(np.array(000.07184))
	return sensor_physical_edge

def get_sensor_physical_edge_vector():
	return Al_utils.normal_vector(math.radians(get_sensor_physical_edge()[3]),math.radians(get_sensor_physical_edge()[4]))

def get_sensor_basis():
	basis = np.empty([3,3])
	basis[0] = get_sensor_active_edge_vector()
	basis[2] = get_sensor_normal()
	basis[0] = Al_utils.orthogonalize(basis[2],basis[0])
	basis[1] = np.cross(basis[2],basis[0])

	basis[0] = basis[0]/np.linalg.norm(basis[0])
	basis[1] = basis[1]/np.linalg.norm(basis[1])
	basis[2] = basis[2]/np.linalg.norm(basis[2])
	return [get_sensor_origin(),basis,get_sensor_active_edge(),get_sensor_active_edge_vector(),get_sensor_physical_edge(),get_sensor_physical_edge_vector()]