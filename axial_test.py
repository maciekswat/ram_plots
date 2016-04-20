import sys
import vtk

def mkVtkIdList(it, offset=0):
    vil = vtk.vtkIdList()
    for i in it:
        vil.InsertNextId(int(i)+offset)
    return vil

sys.path.append('/Users/m/PTSA_NEW_GIT')

from ptsa.data.MatlabIO import read_single_matlab_matrix_as_numpy_structured_array, deserialize_objects_from_matlab_format
fname='mni_depth_slice.mat'

# vs = read_single_matlab_matrix_as_numpy_structured_array(file_name=fname, object_name='vs' ,verbose=False)

obj_dict=deserialize_objects_from_matlab_format(fname, 'vs','fs','cs')

vs=obj_dict['vs']
fs=obj_dict['fs']
cs=obj_dict['cs']

vertices  = vtk.vtkPoints()
faces   = vtk.vtkCellArray()
scalars = vtk.vtkFloatArray()
polydata    = vtk.vtkPolyData()

vs0=vs[0]
for i in xrange(vs0.shape[0]):
    vertices.InsertPoint(i, vs0[i])

fs0=fs[0]
for i in xrange(fs0.shape[0]):
    faces.InsertNextCell(mkVtkIdList(fs0[i],offset=-1))


cs0 = cs[0]
for i in xrange(cs0.shape[0]):
    scalars.InsertTuple1(i, cs0[i])

lut = vtk.vtkLookupTable()
lut.SetNumberOfTableValues(256)
for i in xrange(256):
    lut.SetTableValue(i,i,i,i,1)
# lut.SetValueRange(0, 255)
# lut.SetHueRange(0,1)
lut.Build()

print lut
# We now assign the pieces to the vtkPolyData.
polydata.SetPoints(vertices)
polydata.SetPolys(faces)

polydata.GetPointData().SetScalars(scalars)


pd_writer = vtk.vtkPolyDataWriter()
pd_writer.SetFileName('axial_mni-17.vtk')
pd_writer.SetInputData(polydata)
pd_writer.Write()

pd_reader = vtk.vtkPolyDataReader()
pd_reader.SetFileName('axial_mni-17.vtk')

polydata = pd_reader.GetOutputPort()

# Now we'll look at it.
mapper = vtk.vtkPolyDataMapper()
if vtk.VTK_MAJOR_VERSION <= 5:
    mapper.SetInput(polydata)
else:
    mapper.SetInputConnection(polydata)


# # Now we'll look at it.
# mapper = vtk.vtkPolyDataMapper()
# if vtk.VTK_MAJOR_VERSION <= 5:
#     mapper.SetInput(polydata)
# else:
#     mapper.SetInputData(polydata)


mapper.SetScalarRange(0, 255)
mapper.SetLookupTable(lut)

actor = vtk.vtkActor()
actor.SetMapper(mapper)


# The usual rendering stuff.
camera = vtk.vtkCamera()
camera.SetPosition(0, 0, 1)
camera.SetFocalPoint(0, 0, 0)

renderer = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(renderer)

iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)
#
renderer.AddActor(actor)
renderer.SetActiveCamera(camera)
renderer.ResetCamera()
renderer.SetBackground(1, 1, 1)

renWin.SetSize(1000, 1000)

# interact with data
renWin.Render()
iren.Start()
#
#
#
#
# # print vs