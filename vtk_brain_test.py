__author__ = 'm'

import vtk
vtkFile_l = 'lh.vtk'
vtkFile_r = 'rh.vtk'
from QVTK

# # Create the MayaVi engine and start it.
# engine = Engine()
# engine.start()
# scene = engine.new_scene()
#
# # Read in VTK file and add as source
# reader1 = VTKFileReader()
# reader1.initialize(vtkFile_l)
# engine.add_source(reader1)
#
# # Add Surface Module
# surface = Surface()
# engine.add_module(surface)
#
# # Move the camera
# scene.scene.camera.elevation(90)
# scene.scene.camera.azimuth(-180)
#
# # Save scene to image file
# scene.scene.save_png('image.png')
#
# # Create a GUI instance and start the event loop.
# # This stops the window from closing
# from pyface.api import GUI
# gui = GUI()
# gui.start_event_loop()