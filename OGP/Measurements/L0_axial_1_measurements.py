import numpy as np
import math
import Al_utils

def get_sensor_origin():
	sensor_origin = np.empty([3])
	sensor_origin[0] = Al_utils.getAvg(np.array([129.47191,129.47163,129.47141]))
	sensor_origin[1] = Al_utils.getAvg(np.array([013.19470,013.19415,013.19412]))
	sensor_origin[2] = Al_utils.getAvg(np.array([010.71328,010.71388,010.71387]))
	return sensor_origin

def get_sensor_plane():
	sensor_plane = np.empty([5])
	sensor_plane[0] = Al_utils.getAvg(np.array([129.07857,129.07863,129.07877]))
	sensor_plane[1] = Al_utils.getAvg(np.array([012.76791,012.77240,012.77170]))
	sensor_plane[2] = Al_utils.getAvg(np.array([011.12108,011.12545,011.12469]))
	sensor_plane[3] = Al_utils.getAvg(np.array([-090.02415,-090.02296,-090.01908]))
	sensor_plane[4] = Al_utils.getAvg(np.array([-045.05348,-045.05431,-045.05588]))
	return sensor_plane

def get_sensor_normal():
	return Al_utils.normal_vector(math.radians(get_sensor_plane()[3]),math.radians(get_sensor_plane()[4]))

def get_sensor_active_edge():
	sensor_active_edge = np.empty([5])
	sensor_active_edge[0] = Al_utils.getAvg(np.array([129.07765,129.07791,129.07824]))
	sensor_active_edge[1] = Al_utils.getAvg(np.array([008.21418,008.21371,008.21387]))
	sensor_active_edge[2] = Al_utils.getAvg(np.array([015.68143,015.68197,015.68236]))
	sensor_active_edge[3] = Al_utils.getAvg(np.array([000.21938,000.22045,000.22171]))
	sensor_active_edge[4] = Al_utils.getAvg(np.array([-000.22102,-000.21866,-000.21956]))
	return sensor_active_edge

def get_sensor_active_edge_vector():
	return Al_utils.normal_vector(math.radians(get_sensor_active_edge()[3]),math.radians(get_sensor_active_edge()[4]))

def get_sensor_physical_edge():
	sensor_physical_edge = np.empty([5])
	sensor_physical_edge[0] = Al_utils.getAvg(np.array([129.27365,129.27408,129.28433]))
	sensor_physical_edge[1] = Al_utils.getAvg(np.array([007.99606,007.99541,007.99547]))
	sensor_physical_edge[2] = Al_utils.getAvg(np.array([015.88155,015.88181,015.88182]))
	sensor_physical_edge[3] = Al_utils.getAvg(np.array([179.95414,179.95392,179.95454]))
	sensor_physical_edge[4] = Al_utils.getAvg(np.array([-000.02556,-000.02576,-000.02558]))
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