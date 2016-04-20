import sys
import vtk

def mkVtkIdList(it, offset=0):
    vil = vtk.vtkIdList()
    for i in it:
        vil.InsertNextId(int(i)+offset)
    return vil

sys.path.append('/Users/m/PTSA_NEW_GIT')


lut = vtk.vtkLookupTable()
lut.SetNumberOfTableValues(256)
for i in xrange(256):
    lut.SetTableValue(i,i,i,i,1)
lut.Build()


pd_reader = vtk.vtkPolyDataReader()
pd_reader.SetFileName('axial_mni-8.0.vtk')

polydata = pd_reader.GetOutputPort()

# Now we'll look at it.
mapper = vtk.vtkPolyDataMapper()
if vtk.VTK_MAJOR_VERSION <= 5:
    mapper.SetInput(polydata)
else:
    mapper.SetInputConnection(polydata)


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