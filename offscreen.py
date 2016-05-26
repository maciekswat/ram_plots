import vtk
from vtk import (vtkSphereSource, vtkPolyDataMapper, vtkActor, vtkRenderer,
        vtkRenderWindow, vtkWindowToImageFilter, vtkPNGWriter)

sphereSource = vtkSphereSource()
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(sphereSource.GetOutputPort())

actor = vtkActor()
actor.SetMapper(mapper)

renderer = vtkRenderer()
renderWindow = vtkRenderWindow()
renderWindow.SetOffScreenRendering(1)
renderWindow.AddRenderer(renderer)

renderer.AddActor(actor)
renderer.SetBackground(1, 1, 1)

renderWindow.Render()

windowToImageFilter = vtkWindowToImageFilter()
windowToImageFilter.SetInput(renderWindow)
windowToImageFilter.Update()

writer = vtkPNGWriter()
writer.SetFileName("sphere.png")
writer.SetInputConnection(windowToImageFilter.GetOutputPort())
writer.Write()


exp = vtk.vtkGL2PSExporter()
exp.SetFileFormatToPDF()
exp.SetRenderWindow(renderWindow)
exp.SetFilePrefix('cone_pdf')
# Turn off compression so PIL can read file.
exp.CompressOff()
# exp.SetSortToBSP()
exp.DrawBackgroundOn()
exp.Write()