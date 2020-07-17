import numpy as np
import math

def make_basis(oriball,axiball,diaball):
	basis = np.empty([3,3])

	basis[0] = axiball-oriball
	basis[1] = diaball-oriball
	basis[1] = orthogonalize(basis[0],basis[1])
	basis[2] = np.cross(basis[0],basis[1])

	basis[0] = basis[0]/np.linalg.norm(basis[0])
	basis[1] = basis[1]/np.linalg.norm(basis[1])
	basis[2] = basis[2]/np.linalg.norm(basis[2])
	return [oriball,basis,oriball,axiball,diaball]

def make_pin_basis(holepin,slotpin,normal):
	basis = np.empty([3,3])
	basis[0] = slotpin-holepin
	basis[1] = normal
	basis[1] = orthogonalize(basis[0],basis[1])
	basis[2] = np.cross(basis[0],basis[1])

	basis[0] = basis[0]/np.linalg.norm(basis[0])
	basis[1] = basis[1]/np.linalg.norm(basis[1])
	basis[2] = basis[2]/np.linalg.norm(basis[2])
	return [holepin,basis,holepin,slotpin,normal]

def normal_vector(az,el):
	if (el<0):
		az = az+math.pi
		el = -1.0*el
	normal = np.array([math.cos(az)*math.cos(el),
		math.sin(az)*math.cos(el),
		math.sin(el)])
	return normal


def orthogonalize(vec1,vec2): #return vector orthogonal to vec1, in the plane of vec1 and vec2
	return vec2 - (vec1.dot(vec2)/vec1.dot(vec1))*vec1

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
	basis[2] = orthogonalize(basis[0],basis[2])
	basis[1] = np.cross(basis[2],basis[0])

	basis[0] = basis[0]/np.linalg.norm(basis[0])
	basis[1] = basis[1]/np.linalg.norm(basis[1])
	basis[2] = basis[2]/np.linalg.norm(basis[2])
	return [upst_mid,basis,holeupst,holedownst,slotupst,slotdownst]

def make_rotation(ux, uy, uz):
	rotvec = np.array([ux,uy,uz])
	angle = np.linalg.norm(rotvec)
	if (angle==0):
		return np.identity(3)
	rotvec = rotvec/angle
	matrix = math.cos(angle)*np.identity(3) +\
			math.sin(angle)*np.cross(np.identity(3),rotvec) +\
			(1.0-math.cos(angle))*np.outer(rotvec, rotvec)
	#print np.cross(np.identity(3),rotvec)
	#print np.outer(rotvec, rotvec)
	return matrix

def get_uchbasis(stepdict,uch,pos_name):
	uch_basis = make_uch_basis(stepdict[uch+'1'+pos_name],
				stepdict[uch+'2'+pos_name],
				stepdict[uch+'3'+pos_name],
				stepdict[uch+'4'+pos_name])
	return uch_basis

def make_parametrized_basis(x,y,z,ux,uy,uz):
	origin = np.array([x,y,z])
	rotation = make_rotation(ux,uy,uz)
	return [origin,rotation]

def make_height_basis(y,tilt,roll):
	origin = np.array([0.0,y,0.0])
	#rotation = make_rotation(0.0,0.0,roll).dot(make_rotation(tilt,0.0,0.0))
	#rotation = make_rotation(tilt,0.0,0.0).dot(make_rotation(0.0,0.0,roll))
	rotation = make_rotation(tilt,0.0,roll)
	return [origin,rotation]

def transform_pt(meas_basis,fixture_basis,meas_point):
	if meas_point.size!=3:
		return
	point = np.copy(meas_point)
	#print point.shape
	point = point-meas_basis[0]
	point = meas_basis[1].dot(point)
	point = point.dot(fixture_basis[1])
	point = point+fixture_basis[0]
	return point


def transform_pts(meas_basis,fixture_basis,meas_points):
	points = np.copy(meas_points)
	for i in range(0,points.shape[0]):
		points[i,:] = transform_pt(meas_basis,fixture_basis,points[i,:])
	return points

def transform_vec(meas_basis,fixture_basis,meas_vec):
	if meas_vec.size!=3:
		return
	vec = np.copy(meas_vec)
	vec = meas_basis[1].dot(vec)
	vec = vec.dot(fixture_basis[1])
	#vec = fixture_basis[1].dot(vec)
	return vec

def transform_vecs(meas_basis,fixture_basis,meas_vecs):
	vecs = np.copy(meas_vecs)
	for i in range(0,vecs.shape[0]):
		vecs[i,:] = transform_vec(meas_basis,fixture_basis,vecs[i,:])
	return vecs

def transform_basis(meas_basis,fixture_basis,basis_meas):
	origin = transform_pt(meas_basis,fixture_basis,basis_meas[0])
	rotation = transform_vecs(meas_basis,fixture_basis,basis_meas[1])
	#rotation = transform_vec(meas_basis,fixture_basis,basis_meas[1].T).T
	#rotation = np.copy(basis_meas[1].T)
	#for i in range(0,rotation.shape[1]):
	#	rotation[:,i] = transform_vec(meas_basis,fixture_basis,rotation[:,i])
	return [origin,rotation]

def reverse_basis(input_basis):
	#origin = transform_pt(meas_basis,fixture_basis,np.array([0.0, 0.0, 0.0]))
	basis_vecs = input_basis[1].T
	#print basis_vecs
	#print -1.0*input_basis[0]
	basis_origin = input_basis[1].dot(-1.0*input_basis[0])
	#print basis_origin
	return [basis_origin,basis_vecs]

def transform_plane(meas_basis,fixture_basis,meas_plane):
	point = meas_plane[0]*meas_plane[1]
	transformed_point = transform_pt(meas_basis,fixture_basis,point)
	vec = transform_vec(meas_basis,fixture_basis,meas_plane[0])
	distance = transformed_point.dot(vec)
	return [vec, distance]

def make_sensor_basis(sensor):
	rotation = make_rotation(sensor[3],sensor[4],sensor[5])
	origin = rotation.T.dot(-sensor[0:3])
	curvature = np.copy(sensor[6:9])
	return [origin,rotation,curvature]

def find_sensor_intersection(sensor,module_basis,edge_y,x):
	sensor_x = 0;
	sensor_y = edge_y;
	sensor_z = sensor[2][0]*sensor_x*sensor_x + sensor[2][1]*sensor_y*sensor_y + sensor[2][2]*sensor_x*sensor_y

	global_pt = transform_pt(sensor,module_basis,np.array([sensor_x,sensor_y,sensor_z]))
	return global_pt

def find_sensor_residuals(module_basis,sensor,points):
	npoints = points.shape[0]
	#print npoints
	#print points
	transformed_points = transform_pts(module_basis,sensor,points)
	residuals = np.empty([npoints,2])
	for i in range(0,npoints):
		sensor_x = transformed_points[i,0]
		sensor_y = transformed_points[i,1]
		residuals[i,0] = sensor_y - math.copysign(20.17,sensor_y)
		residuals[i,1] = transformed_points[i,2]- ( sensor[2][0]*sensor_x*sensor_x + sensor[2][1]*sensor_y*sensor_y + sensor[2][2]*sensor_x*sensor_y)

	#print transformed_points
	residuals_surveyframe = np.zeros([npoints,3])
	residuals_surveyframe[:,1] = residuals[:,0]
	residuals_surveyframe[:,2] = residuals[:,1]
	#print residuals
	#temp = np.array([[0,0,1]])
	#print temp
	#print transform_pts(sensor,module_basis,temp)
	#print residuals_surveyframe
	residuals_surveyframe = transform_vecs(sensor,module_basis,residuals_surveyframe)
	#print residuals_surveyframe
	print residuals_surveyframe[:,1:3].T
	return residuals
