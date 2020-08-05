


def M_QF(k,omega):
    for i in range(0,4):
        for j in range(0,4):
	    M[i][j] = 0
    M[0][0] = cos(omega)
    M[1][0] = 1/sqrt(abs(k))*sin(omega)
    M[0][1] = -sqrt(abs(k))*sin(omega)
    M[1][1] = cos(omega)
    M[2][2] = cos(omega)
    M[3][2] = 1/sqrt(abs(k))*sin(omega)
    M[2][3] = sqrt(abs(k))*sin(omega)
    M[3][3] = cos(omega)
    return M

def M_QD(k,omega):
    for i in range(0,4):
        for j in range(0,4):
	    M[i][j] = 0
    M[0][0] = cos(omega)
    M[1][0] = 1/sqrt(abs(k))*sin(omega)
    M[0][1] = sqrt(abs(k))*sin(omega)
    M[1][1] = cos(omega)
    M[2][2] = cos(omega)
    M[3][2] = 1/sqrt(abs(k))*sin(omega)
    M[2][3] = -sqrt(abs(k))*sin(omega)
    M[3][3] = cos(omega)
    return M

def M_drift(l):
    for i in range(0,4):
        for j in range(0,4):
	    M[i][j] = 0
    M[0][0] = 1.0
    M[1][1] = 1.0
    M[2][2] = 1.0
    M[3][3] = 1.0
    M[1][0] = l
    M[3][2] = l
    return M

def M_dipole(l,R):
    for i in range(0,4):
        for j in range(0,4):
	    M[i][j] = 0
    M[0][0] = cos(l/R)
    M[1][0] = R*sin(l/R)
    M[0][1] = -1/R*sin(l/R)
    M[1][1] = cos(l/R)
    M[2][2] = 1.0
    M[3][2] = l
    M[3][3] = 1.0
    return M

def M_edge(phi,R):
    for i in range(0,4):
        for j in range(0,4):
	    M[i][j] = 0
    M[0][0] = 1.0
    M[0][1] = tan(phi)/R
    M[1][1] = 1.0
    M[2][2] = 1.0
    M[2][3] = -tan(phi)/R
    M[3][3] = 1.0
    return M
