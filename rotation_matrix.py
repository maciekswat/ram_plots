import numpy as np
from numpy import cross, eye, dot
from scipy.linalg import expm3, norm

def RotMat(axis, theta):
    return expm3(cross(eye(3), axis/norm(axis)*theta))

# v, axis, theta = [3,5,0], [4,4,1], 1.2

v, axis, theta = [1,0,0], [0,0,1], np.pi/2.0

R0 = RotMat(axis, theta)
print dot(R0,v)
