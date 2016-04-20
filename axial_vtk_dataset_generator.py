import sys
import vtk

import numpy as np

def mkVtkIdList(it, offset=0):
    vil = vtk.vtkIdList()
    for i in it:
        vil.InsertNextId(int(i)+offset)
    return vil


class MNI_2_TAL(object):
    """
    This transformation is based on mni2tal.m and mni2tal_matrix.m Matlab functions form EEG Toolbox
    """

    def __init__(self):
        self.MNI_2_TAL_ABOVE = np.matrix([[0.9900,0.0,0.],
                            [0.,0.9688,0.0460],
                            [0.,-0.0485,0.9189]], dtype=np.float)


        self.MNI_2_TAL_BELOW = np.matrix([[0.9900,0.0,0.],
                            [0.,0.9688,0.0420],
                            [0.,-0.0485,0.8390]], dtype=np.float)

    def transform(self,mni_coords):

        if mni_coords[2] > 0.0:

            return np.squeeze(np.array(np.dot(self.MNI_2_TAL_ABOVE,mni_coords.T)))

        else:

            return np.squeeze(np.array(np.dot(self.MNI_2_TAL_BELOW,mni_coords.T)))


# def mni2tal(mni_coords):
#
#     if mni_coords[2] > 0.0:
#         MNI_2_TAL = np.matrix([[0.9900,0.0,0.],
#                             [0.,0.9688,0.0460],
#                             [0.,-0.0485,0.9189]], dtype=np.float)
#     else:
#
#         MNI_2_TAL = np.matrix([[0.9900,0.0,0.],
#                             [0.,0.9688,0.0420],
#                             [0.,-0.0485,0.8390]], dtype=np.float)




# MNI_2_TAL_ABOVE = np.matrix([[0.9900,0.0,0.],
#                             [0.,0.9688,0.0460],
#                             [0.,-0.0485,0.9189]], dtype=np.float)
#
# mni_coords=np.array([10.,12.,14.]).T
#
#
# # print MNI_2_TAL_ABOVE*mni_coords
#
# print mni_coords.T
#
#
# sys.exit()

sys.path.append('/Users/m/PTSA_NEW_GIT')

from ptsa.data.MatlabIO import read_single_matlab_matrix_as_numpy_structured_array, deserialize_objects_from_matlab_format
fname='mni_depth_slice.mat'

# vs = read_single_matlab_matrix_as_numpy_structured_array(file_name=fname, object_name='vs' ,verbose=False)

obj_dict=deserialize_objects_from_matlab_format(fname, 'vs','fs','cs')

vs=obj_dict['vs']
fs=obj_dict['fs']
cs=obj_dict['cs']

TRANSFORM_TO_TAL=True

for n in xrange(len(vs)):

    vertices = vtk.vtkPoints()
    faces = vtk.vtkCellArray()
    scalars = vtk.vtkFloatArray()
    polydata = vtk.vtkPolyData()

    # vsn = vs[n]
    # for i in xrange(vsn.shape[0]):
    #     vertices.InsertPoint(i, vsn[i])

    vsn = vs[n]
    if TRANSFORM_TO_TAL:
        MNI_2_TAL_TRANSFORM=MNI_2_TAL()

        for i in xrange(vsn.shape[0]):
            mni_coords=vsn[i]
            tal_coords = MNI_2_TAL_TRANSFORM.transform(mni_coords)
            vertices.InsertPoint(i, tal_coords)

    else:

        for i in xrange(vsn.shape[0]):
            vertices.InsertPoint(i, vsn[i])


    fsn = fs[n]
    for i in xrange(fsn.shape[0]):
        faces.InsertNextCell(mkVtkIdList(fsn[i], offset=-1)) # offset is -1 because matlab counts from 1

    csn = cs[n]
    for i in xrange(csn.shape[0]):
        scalars.InsertTuple1(i, csn[i])

    # We now assign the pieces to the vtkPolyData.
    polydata.SetPoints(vertices)
    polydata.SetPolys(faces)

    polydata.GetPointData().SetScalars(scalars)


    pd_writer = vtk.vtkPolyDataWriter()
    if TRANSFORM_TO_TAL:
        pd_writer.SetFileName('axial-tal%s.vtk'%vsn[0,2])
    else:
        pd_writer.SetFileName('axial-mni%s.vtk'%vsn[0,2])

    pd_writer.SetInputData(polydata)
    pd_writer.Write()

