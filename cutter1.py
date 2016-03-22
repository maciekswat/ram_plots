import vtk


# superquadricSource = vtk.vtkSuperquadricSource()
# superquadricSource.SetPhiRoundness(3.1)
# superquadricSource.SetThetaRoundness(2.2)

superquadricSource = vtk.vtkSphereSource()



clipPlane = vtk.vtkPlane()
clipPlane.SetNormal(1.0, -1.0, -1.0)
clipPlane.SetOrigin(0, 0, 0)

clipper = vtk.vtkClipPolyData()
clipper.SetInputConnection(superquadricSource.GetOutputPort())
clipper.SetClipFunction(clipPlane)

superquadricMapper = vtk.vtkPolyDataMapper()
superquadricMapper.SetInputConnection(clipper.GetOutputPort())

superquadricActor = vtk.vtkActor()
superquadricActor.SetMapper(superquadricMapper)

#create renderers and add actors of plane and cube
ren = vtk.vtkRenderer()


#create renderers and add actors of plane and cube
ren.AddActor(superquadricActor)
#Add renderer to renderwindow and render
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren)
renWin.SetSize(600, 600)
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)
ren.SetBackground(0, 0, 0)
renWin.Render()
iren.Start()