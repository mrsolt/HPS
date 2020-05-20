import numpy as np
import math

def make_basis(oriball,axiball,diaball):
	basis = np.empty([3,3])
	axiball = [math.sqrt((axiball[0]-oriball[0])**2+(axiball[1]-oriball[1])**2+(axiball[2]-oriball[2])**2),0,0]
	diaball = [0,math.sqrt((diaball[0]-oriball[0])**2+(diaball[1]-oriball[1])**2+(diaball[2]-oriball[2])**2),0]
	#diaball = [0,1.0,0]
	oriball = oriball-oriball
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

#def make_uch_basis(holeupst,holedownst,slotupst,slotdownst):
#	upst_mid = (holeupst+slotupst)/2.0
#	downst_mid = (holedownst+slotdownst)/2.0
#	upst_vec = (slotupst-holeupst)
#	downst_vec = (slotdownst-holedownst)
#	upst_vec = upst_vec/np.linalg.norm(upst_vec)
#	downst_vec = downst_vec/np.linalg.norm(downst_vec)
#	basis = np.empty([3,3])

#	basis[0] = upst_vec+downst_vec
#	basis[2] = downst_mid-upst_mid
#	basis[2] = orthogonalize(basis[0],basis[2])
#	basis[1] = np.cross(basis[2],basis[0])

#	basis[0] = basis[0]/np.linalg.norm(basis[0])
#	basis[1] = basis[1]/np.linalg.norm(basis[1])
#	basis[2] = basis[2]/np.linalg.norm(basis[2])
#	return [upst_mid,basis,holeupst,holedownst,slotupst,slotdownst]

def make_uch_basis(holeupst,holedownst,slotupst,slotdownst):
	upst_mid = (holeupst+slotupst)/2.0
	downst_mid = (holedownst+slotdownst)/2.0
	upst_vec = (slotupst-holeupst)
	downst_vec = (slotdownst-holedownst)
	upst_vec = upst_vec/np.linalg.norm(upst_vec)
	downst_vec = downst_vec/np.linalg.norm(downst_vec)
	basis = np.empty([3,3])

	downst_mid = [math.sqrt((downst_mid[0]-upst_mid[0])**2+(downst_mid[1]-upst_mid[1])**2+(downst_mid[2]-upst_mid[2])**2),0,0]
	upst_mid = upst_mid - upst_mid

	basis[0] = upst_vec+downst_vec
	basis[2] = downst_mid-upst_mid
	basis[2] = orthogonalize(basis[0],basis[2])
	basis[1] = np.cross(basis[2],basis[0])

	#basis[0] = downst_mid-upst_mid
	#basis[1] = upst_vec+downst_vec
	#basis[1] = orthogonalize(basis[0],basis[1])
	#basis[2] = np.cross(basis[0],basis[1])

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

def get_uch_mount(stepdict,layer):
	holepin = np.empty([3])
	slotpin = np.empty([3])
	normal = np.empty([3])
	#holepin[0]=stepdict[layer+' hole pin intersection']['X Location'][1]
	#holepin[1]=stepdict[layer+' hole pin intersection']['Y Location'][1]
	#holepin[2]=stepdict[layer+' hole pin intersection']['Z Location'][1]
	#slotpin[0]=stepdict[layer+' slot pin intersection']['X Location'][1]
	#slotpin[1]=stepdict[layer+' slot pin intersection']['Y Location'][1]
	#slotpin[2]=stepdict[layer+' slot pin intersection']['Z Location'][1]
	#az = math.radians(stepdict[layer+' plane, touch']['XY Angle'][1])
	#el = math.radians(stepdict[layer+' plane, touch']['Elevation'][1])
	if (el<0):
		az = az+math.pi
		el = -1.0*el
	normal = np.array([math.cos(az)*math.cos(el),
		math.sin(az)*math.cos(el),
		math.sin(el)])
	#print l1normal
	basis = make_pin_basis(holepin, slotpin, normal)
	return basis

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
	#print "Old point " + str(point)
	#print point.shape
	point = point-meas_basis[0]
	#print "Point 1 " + str(point)
	point = meas_basis[1].dot(point)
	#print "Point 2 " + str(point)
	point = point.dot(fixture_basis[1])
	point = point+fixture_basis[0]
	#print "New point " + str(point)
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
	transformed_points = transform_pts(module_basis,sensor,points)
	residuals = np.empty([npoints,2])
	for i in range(0,npoints):
		sensor_x = transformed_points[i,0]
		sensor_y = transformed_points[i,1]
		residuals[i,0] = sensor_y - math.copysign(20.17,sensor_y)
		residuals[i,1] = transformed_points[i,2]- ( sensor[2][0]*sensor_x*sensor_x + sensor[2][1]*sensor_y*sensor_y + sensor[2][2]*sensor_x*sensor_y)

	residuals_surveyframe = np.zeros([npoints,3])
	residuals_surveyframe[:,1] = residuals[:,0]
	residuals_surveyframe[:,2] = residuals[:,1]
	residuals_surveyframe = transform_vecs(sensor,module_basis,residuals_surveyframe)
	return residuals

def project_point_to_plane(point,plane_point,normal):
	t = (normal[0]*(point[0]-plane_point[0])+normal[1]*(point[1]-plane_point[1])+normal[2]*(point[2]-plane_point[2]))/(normal[0]**2+normal[1]**2+normal[2]**2)
	newpoint = np.array([normal[0]*t+point[0],normal[1]*t+point[1],normal[2]*t+point[2]])
	return newpoint

def getAvg(arr):
	sum = 0
	for i in range(len(arr)):
		sum = sum + arr[i]
	return sum/len(arr)

def ubasisTop_to_JLab(point,isL0):
	newpoint = np.empty([3])
	theta = 0.0305
	x = -point[1] - 25.594
	y = -(point[2] - 8.423)
	z = point[0] + 92.884
	if(isL0):
	    x = (x*np.cos(theta)-z*np.sin(theta))
	newpoint[0] = x
	newpoint[1] = y
	newpoint[2] = z
	return newpoint

def ubasisBot_to_JLab(point,isL0):
	newpoint = np.empty([3])
	theta = 0.0305
	x = point[1] - 25.110
	y = point[2] - 8.423
	z = point[0] + 108.75
	if(isL0):
	    x = (x*np.cos(theta)-z*np.sin(theta))
	newpoint[0] = x
	newpoint[1] = y
	newpoint[2] = z
	return newpoint

def UChannelToJlabPoint(point):
	return point

def UChannelToJlabVec(vec):
	return vec

def UChannelToJlabZ(z):
	return z

def UChannelToJlabYTop(y):
	return -(y - 8.423)

def UChannelToJlabYBot(y):
	return y - 8.423