"""
A simple VTK widget for PyQt v4, the Qt v4 bindings for Python.
See http://www.trolltech.com for Qt documentation, and
http://www.riverbankcomputing.co.uk for PyQt.

This class is based on the vtkGenericRenderWindowInteractor and is
therefore fairly powerful.  It should also play nicely with the
vtk3DWidget code.

Created by Prabhu Ramachandran, May 2002
Based on David Gobbi's QVTKRenderWidget.py

Changes by Gerard Vermeulen Feb. 2003
 Win32 support.

Changes by Gerard Vermeulen, May 2003
 Bug fixes and better integration with the Qt framework.

Changes by Phil Thompson, Nov. 2006
 Ported to PyQt v4.
 Added support for wheel events.

Changes by Phil Thompson, Oct. 2007
 Bug fixes.

Changes by Phil Thompson, Mar. 2008
 Added cursor support.
"""

import sys
import os
import numpy as np

# import Configuration

MODULENAME = '---- QVTKRenderWindowInteractor_mac.py: '


def setVTKPaths():
    import sys
    from os import environ
    import string
    import sys
    platform = sys.platform
    if platform == 'win32':
        sys.path.insert(0, environ["PYTHON_DEPS_PATH"])
        # sys.path.append(environ["VTKPATH"])
        # sys.path.append(environ["VTKPATH1"])
        # sys.path.append(environ["PYQT_PATH"])
        # sys.path.append(environ["SIP_PATH"])
        # sys.path.append(environ["SIP_UTILS_PATH"])


#   else:
#      swig_path_list=string.split(environ["VTKPATH"])
#      for swig_path in swig_path_list:
#         sys.path.append(swig_path)

# print "PATH=",sys.path
setVTKPaths()
# print "PATH=",sys.path  


from PyQt4 import QtCore, QtGui, QtOpenGL
import vtk


# class QVTKRenderWindowInteractor(QtOpenGL.QGLWidget):  # Windows & Linux (I think)
class QVTKRenderWindowInteractor(QtGui.QWidget):  # Mac

    """ A QVTKRenderWindowInteractor for Python and Qt.  Uses a
    vtkGenericRenderWindowInteractor to handle the interactions.  Use
    GetRenderWindow() to get the vtkRenderWindow.  Create with the
    keyword stereo=1 in order to generate a stereo-capable window.

    The user interface is summarized in vtkInteractorStyle.h:

    - Keypress j / Keypress t: toggle between joystick (position
    sensitive) and trackball (motion sensitive) styles. In joystick
    style, motion occurs continuously as long as a mouse button is
    pressed. In trackball style, motion occurs when the mouse button
    is pressed and the mouse pointer moves.

    - Keypress c / Keypress o: toggle between camera and object
    (actor) modes. In camera mode, mouse events affect the camera
    position and focal point. In object mode, mouse events affect
    the actor that is under the mouse pointer.

    - Button 1: rotate the camera around its focal point (if camera
    mode) or rotate the actor around its origin (if actor mode). The
    rotation is in the direction defined from the center of the
    renderer's viewport towards the mouse position. In joystick mode,
    the magnitude of the rotation is determined by the distance the
    mouse is from the center of the render window.

    - Button 2: pan the camera (if camera mode) or translate the actor
    (if object mode). In joystick mode, the direction of pan or
    translation is from the center of the viewport towards the mouse
    position. In trackball mode, the direction of motion is the
    direction the mouse moves. (Note: with 2-button mice, pan is
    defined as <Shift>-Button 1.)

    - Button 3: zoom the camera (if camera mode) or scale the actor
    (if object mode). Zoom in/increase scale if the mouse position is
    in the top half of the viewport; zoom out/decrease scale if the
    mouse position is in the bottom half. In joystick mode, the amount
    of zoom is controlled by the distance of the mouse pointer from
    the horizontal centerline of the window.

    - Keypress 3: toggle the render window into and out of stereo
    mode.  By default, red-blue stereo pairs are created. Some systems
    support Crystal Eyes LCD stereo glasses; you have to invoke
    SetStereoTypeToCrystalEyes() on the rendering window.  Note: to
    use stereo you also need to pass a stereo=1 keyword argument to
    the constructor.

    - Keypress e: exit the application.

    - Keypress f: fly to the picked point

    - Keypress p: perform a pick operation. The render window interactor
    has an internal instance of vtkCellPicker that it uses to pick. 

    - Keypress r: reset the camera view along the current view
    direction. Centers the actors and moves the camera so that all actors
    are visible.

    - Keypress s: modify the representation of all actors so that they
    are surfaces. 

    - Keypress u: invoke the user-defined function. Typically, this
    keypress will bring up an interactor that you can type commands in.

    - Keypress w: modify the representation of all actors so that they
    are wireframe.
    """

    # Map between VTK and Qt cursors.
    _CURSOR_MAP = {
        0: QtCore.Qt.ArrowCursor,  # VTK_CURSOR_DEFAULT
        1: QtCore.Qt.ArrowCursor,  # VTK_CURSOR_ARROW
        2: QtCore.Qt.SizeBDiagCursor,  # VTK_CURSOR_SIZENE
        3: QtCore.Qt.SizeFDiagCursor,  # VTK_CURSOR_SIZENWSE
        4: QtCore.Qt.SizeBDiagCursor,  # VTK_CURSOR_SIZESW
        5: QtCore.Qt.SizeFDiagCursor,  # VTK_CURSOR_SIZESE
        6: QtCore.Qt.SizeVerCursor,  # VTK_CURSOR_SIZENS
        7: QtCore.Qt.SizeHorCursor,  # VTK_CURSOR_SIZEWE
        8: QtCore.Qt.SizeAllCursor,  # VTK_CURSOR_SIZEALL
        9: QtCore.Qt.PointingHandCursor,  # VTK_CURSOR_HAND
        10: QtCore.Qt.CrossCursor,  # VTK_CURSOR_CROSSHAIR
    }

    def __init__(self, parent=None, wflags=QtCore.Qt.WindowFlags(), **kw):
        # the current button
        self._ActiveButton = QtCore.Qt.NoButton

        # private attributes
        self.__oldFocus = None
        self.__saveX = 0
        self.__saveY = 0
        self.__saveModifiers = QtCore.Qt.NoModifier
        self.__saveButtons = QtCore.Qt.NoButton

        # do special handling of some keywords:
        # stereo, rw

        stereo = 0

        if kw.has_key('stereo'):
            if kw['stereo']:
                stereo = 1

        rw = None

        if kw.has_key('rw'):
            rw = kw['rw']

        # create qt-level widget
        QtGui.QWidget.__init__(self, parent, wflags | QtCore.Qt.MSWindowsOwnDC)
        # QtOpenGL.QGLWidget.__init__(self, parent)

        if rw:  # user-supplied render window
            #            print MODULENAME, ' predefd rw'
            self._RenderWindow = rw
        else:
            #            print MODULENAME, ' NOT predefd rw'
            self._RenderWindow = vtk.vtkRenderWindow()
        # print MODULENAME,'   winSize = ',self._RenderWindow.GetSize()
        #        ---- QVTKRenderWindowInteractor_mac.py:   NOT predefd rw
        #        ---- QVTKRenderWindowInteractor_mac.py:     winSize =  (0, 0)

        self._RenderWindow.SetWindowInfo(str(int(self.winId())))

        if stereo:  # stereo mode
            self._RenderWindow.StereoCapableWindowOn()
            self._RenderWindow.SetStereoTypeToCrystalEyes()

        self._Iren = vtk.vtkGenericRenderWindowInteractor()
        self._Iren.SetRenderWindow(self._RenderWindow)

        self._Iren.SetRenderWindow(self._RenderWindow)

        # self.interactorStyle=vtk.vtkInteractorStyleJoystickCamera()
        self.interactorStyle = vtk.vtkInteractorStyleSwitch()
        # self.interactorStyle.SetCurrentStyleToTrackballActor()
        self.interactorStyle.SetCurrentStyleToTrackballCamera()
        self._Iren.SetInteractorStyle(self.interactorStyle)

        # do all the necessary qt setup
        self.setAttribute(QtCore.Qt.WA_OpaquePaintEvent)
        self.setAttribute(QtCore.Qt.WA_PaintOnScreen)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        self.setMouseTracking(True)  # get all mouse events
        self.setFocusPolicy(QtCore.Qt.WheelFocus)
        self.setSizePolicy(QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding))

        self._Timer = QtCore.QTimer(self)
        self.connect(self._Timer, QtCore.SIGNAL('timeout()'), self.TimerEvent)

        self._Iren.AddObserver('CreateTimerEvent', self.CreateTimer)
        self._Iren.AddObserver('DestroyTimerEvent', self.DestroyTimer)
        self._Iren.GetRenderWindow().AddObserver('CursorChangedEvent',
                                                 self.CursorChangedEvent)

        self.mousePressEventFcn = self.mousePressEvent2DStyle

    #        print MODULENAME,'   winSize2 = ',self._RenderWindow.GetSize()   # still (0,0)

    def __getattr__(self, attr):
        """Makes the object behave like a vtkGenericRenderWindowInteractor"""
        if attr == '__vtk__':
            return lambda t=self._Iren: t
        elif hasattr(self._Iren, attr):
            return getattr(self._Iren, attr)
        else:
            raise AttributeError, self.__class__.__name__ + \
                                  " has no attribute named " + attr

    def CreateTimer(self, obj, evt):
        self._Timer.start(10)

    def DestroyTimer(self, obj, evt):
        self._Timer.stop()
        return 1

    def TimerEvent(self):
        self._Iren.TimerEvent()

    def CursorChangedEvent(self, obj, evt):
        """Called when the CursorChangedEvent fires on the render window."""
        # This indirection is needed since when the event fires, the current
        # cursor is not yet set so we defer this by which time the current
        # cursor should have been set.
        QtCore.QTimer.singleShot(0, self.ShowCursor)

    def HideCursor(self):
        """Hides the cursor."""
        self.setCursor(QtCore.Qt.BlankCursor)

    def ShowCursor(self):
        """Shows the cursor."""
        vtk_cursor = self._Iren.GetRenderWindow().GetCurrentCursor()
        qt_cursor = self._CURSOR_MAP.get(vtk_cursor, QtCore.Qt.ArrowCursor)
        self.setCursor(cursor)

    def sizeHint(self):
        return QtCore.QSize(400, 400)

    #         width = Configuration.getSetting("GraphicsWinWidth")
    #         height = Configuration.getSetting("GraphicsWinHeight")
    #         return QtCore.QSize(width, height)    # some testing for Rountree/EPA

    def paintEngine(self):
        return None

    def paintEvent(self, ev):
        self._RenderWindow.Render()

    def resizeEvent(self, ev):
        # print "resize event"
        w = self.width()
        h = self.height()

        self._RenderWindow.SetSize(w, h)
        self._Iren.SetSize(w, h)

    #        print MODULENAME,'   resizeEvent(), winSize = ',self._RenderWindow.GetSize()  #  winSize =  (650, 400)


    def _GetCtrlShift(self, ev):
        ctrl = shift = False

        if hasattr(ev, 'modifiers'):
            if ev.modifiers() & QtCore.Qt.ShiftModifier:
                shift = True
            if ev.modifiers() & QtCore.Qt.ControlModifier:
                ctrl = True
        else:
            if self.__saveModifiers & QtCore.Qt.ShiftModifier:
                shift = True
            if self.__saveModifiers & QtCore.Qt.ControlModifier:
                ctrl = True

        return ctrl, shift

    def enterEvent(self, ev):
        pass
        # if not self.hasFocus():
        # self.__oldFocus = self.focusWidget()
        # self.setFocus()

        # ctrl, shift = self._GetCtrlShift(ev)
        # self._Iren.SetEventInformationFlipY(self.__saveX, self.__saveY,
        # ctrl, shift, chr(0), 0, None)
        # self._Iren.EnterEvent()

    def leaveEvent(self, ev):
        if self.__saveButtons == QtCore.Qt.NoButton and self.__oldFocus:
            self.__oldFocus.setFocus()
            self.__oldFocus = None

        ctrl, shift = self._GetCtrlShift(ev)
        self._Iren.SetEventInformationFlipY(self.__saveX, self.__saveY,
                                            ctrl, shift, chr(0), 0, None)
        self._Iren.LeaveEvent()

    def closeEvent(self, _ev):
        print 'QVTK INTERACTOR CLOSE EVENT'
        # cleaning up to release memory - notice that if we do not do this cleanup this widget will not be destroyed and will take sizeable portion of the memory 
        # not a big deal for a single simulation but repeated runs can easily exhaust all system memory
        super(QVTKRenderWindowInteractor, self).close()

        self._Iren.RemoveObservers('CreateTimerEvent')
        self._Iren.RemoveObservers('DestroyTimerEvent')
        self._Iren.GetRenderWindow().RemoveObservers('CursorChangedEvent')
        self.mousePressEventFcn = None

    def setMouseInteractionSchemeTo2D(self):
        self.mousePressEventFcn = self.mousePressEvent2DStyle

    def setMouseInteractionSchemeTo3D(self):
        self.mousePressEventFcn = self.mousePressEvent3DStyle

    def mousePressEvent2DStyle(self, ev):

        ctrl, shift = self._GetCtrlShift(ev)
        repeat = 0
        if ev.type() == QtCore.QEvent.MouseButtonDblClick:
            repeat = 1
        shift = True
        self._Iren.SetEventInformationFlipY(ev.x(), ev.y(),
                                            ctrl, shift, chr(0), repeat, None)
        shift = False

        self._ActiveButton = ev.button()
        if self._ActiveButton == QtCore.Qt.LeftButton:
            self._Iren.LeftButtonPressEvent()
        elif self._ActiveButton == QtCore.Qt.RightButton:
            self._Iren.RightButtonPressEvent()
        elif self._ActiveButton == QtCore.Qt.MidButton:
            self._Iren.MiddleButtonPressEvent()

    def mousePressEvent3DStyle(self, ev):
        ctrl, shift = self._GetCtrlShift(ev)
        repeat = 0
        if ev.type() == QtCore.QEvent.MouseButtonDblClick:
            repeat = 1

        self._Iren.SetEventInformationFlipY(ev.x(), ev.y(),
                                            ctrl, shift, chr(0), repeat, None)
        self._ActiveButton = ev.button()
        if self._ActiveButton == QtCore.Qt.LeftButton:
            self._Iren.LeftButtonPressEvent()
        elif self._ActiveButton == QtCore.Qt.RightButton:
            self._Iren.RightButtonPressEvent()
        elif self._ActiveButton == QtCore.Qt.MidButton:
            self._Iren.MiddleButtonPressEvent()

    def mousePressEvent(self, ev):

        print self.GetRenderWindow()
        rw = self.GetRenderWindow()
        active_camera = rw.GetRenderers().GetFirstRenderer().GetActiveCamera()
        print active_camera
        self.mousePressEventFcn(ev)



        # ctrl, shift = self._GetCtrlShift(ev)
        # repeat = 0
        # if ev.type() == QtCore.QEvent.MouseButtonDblClick:
        # repeat = 1
        # shift=True    
        # self._Iren.SetEventInformationFlipY(ev.x(), ev.y(),
        # ctrl, shift, chr(0), repeat, None)
        # shift=False
        # self._ActiveButton = ev.button()
        # if self._ActiveButton == QtCore.Qt.LeftButton:
        # self._Iren.LeftButtonPressEvent()
        # elif self._ActiveButton == QtCore.Qt.RightButton:
        # self._Iren.RightButtonPressEvent()
        # elif self._ActiveButton == QtCore.Qt.MidButton:
        # self._Iren.MiddleButtonPressEvent()

    def mouseReleaseEvent(self, ev):
        ctrl, shift = self._GetCtrlShift(ev)
        self._Iren.SetEventInformationFlipY(ev.x(), ev.y(),
                                            ctrl, shift, chr(0), 0, None)

        if self._ActiveButton == QtCore.Qt.LeftButton:
            self._Iren.LeftButtonReleaseEvent()
        elif self._ActiveButton == QtCore.Qt.RightButton:
            self._Iren.RightButtonReleaseEvent()
        elif self._ActiveButton == QtCore.Qt.MidButton:
            self._Iren.MiddleButtonReleaseEvent()

    def mouseMoveEvent(self, ev):
        self.__saveModifiers = ev.modifiers()
        self.__saveButtons = ev.buttons()
        self.__saveX = ev.x()
        self.__saveY = ev.y()

        ctrl, shift = self._GetCtrlShift(ev)
        self._Iren.SetEventInformationFlipY(ev.x(), ev.y(),
                                            ctrl, shift, chr(0), 0, None)
        self._Iren.MouseMoveEvent()

    def resetCamera(self):
        # ctrl, shift = self._GetCtrlShift(ev)
        # if ev.key() < 256:
        # key = str(ev.text())
        # else:
        # key = chr(0)
        ctrl, shift = 0, 0
        key = str('r')
        self._Iren.SetEventInformationFlipY(self.__saveX, self.__saveY,
                                            ctrl, shift, key, 0, None)
        self._Iren.KeyPressEvent()
        self._Iren.CharEvent()

    def keyPressEvent(self, ev):
        ctrl, shift = self._GetCtrlShift(ev)
        if ev.key() < 256:
            key = str(ev.text())
        else:
            key = chr(0)
        self._Iren.SetEventInformationFlipY(self.__saveX, self.__saveY,
                                            ctrl, shift, key, 0, None)
        self._Iren.KeyPressEvent()
        self._Iren.CharEvent()

    def keyReleaseEvent(self, ev):
        ctrl, shift = self._GetCtrlShift(ev)
        if ev.key() < 256:
            key = chr(ev.key())
        else:
            key = chr(0)
        self._Iren.SetEventInformationFlipY(self.__saveX, self.__saveY,
                                            ctrl, shift, key, 0, None)
        self._Iren.KeyReleaseEvent()

    def zoomIn(self):

        self._Iren.MouseWheelForwardEvent()

    def zoomOut(self):

        self._Iren.MouseWheelBackwardEvent()

    def wheelEvent(self, ev):
        if ev.delta() >= 0:
            self._Iren.MouseWheelForwardEvent()
        else:
            self._Iren.MouseWheelBackwardEvent()

    def GetRenderWindow(self):
        return self._RenderWindow

    def Render(self):
        self.update()


def QVTKRenderWidgetConeExample():
    """A simple example that uses the QVTKRenderWindowInteractor class."""

    # every QT app needs an app
    app = QtGui.QApplication(['QVTKRenderWindowInteractor'])

    vreader = vtk.vtkXMLPolyDataReader()
    vreader.SetFileName('lh.vtk')
    vreader
    reader1 = VTKFileReader()
    reader1.initialize(vtkFile_l)

    # create the widget
    widget = QVTKRenderWindowInteractor()

    widget.setMouseInteractionSchemeTo3D()

    widget.Initialize()
    widget.Start()
    # if you dont want the 'q' key to exit comment this.
    widget.AddObserver("ExitEvent", lambda o, e, a=app: a.quit())

    ren = vtk.vtkRenderer()
    widget.GetRenderWindow().AddRenderer(ren)

    cone = vtk.vtkConeSource()
    cone.SetResolution(8)

    coneMapper = vtk.vtkPolyDataMapper()

    VTK_MAJOR_VERSION = vtk.vtkVersion.GetVTKMajorVersion()
    if VTK_MAJOR_VERSION >= 6:
        coneMapper.SetInputData(cone.GetOutput())
    else:
        coneMapper.SetInput(cone.GetOutput())

    coneActor = vtk.vtkActor()
    coneActor.SetMapper(coneMapper)

    ren.AddActor(coneActor)

    # show the widget
    widget.show()
    # start event processing
    app.exec_()


def extract_electrode_positions(tal_path, electrode_types=['D', 'G', 'S'], hemi=['R','L']):
    from ptsa.data.readers import TalReader
    tal_reader = TalReader(filename=tal_path)
    tal_structs = tal_reader.read()

    electrode_types_lower = map(lambda t: t.lower(), electrode_types)

    electrode_type_selector = np.array(map(lambda eType: eType.lower() in electrode_types_lower, tal_structs.eType))

    h_data = tal_structs[['avgSurf','eType']]


    h_data = h_data[electrode_type_selector]




    return h_data

def divergent_color_lut(table_size=20, table_range=[0, 1]):
    ctf = vtk.vtkColorTransferFunction()
    ctf.SetColorSpaceToDiverging()
    # Green to tan.
    ctf.AddRGBPoint(0.0, 0.085, 0.532, 0.201)
    ctf.AddRGBPoint(0.5, 0.865, 0.865, 0.865)
    ctf.AddRGBPoint(1.0, 0.677, 0.492, 0.093)

    lut = vtk.vtkLookupTable()
    lut.SetNumberOfTableValues(table_size)
    lut.Build()

    for i in range(0, table_size):
        rgb = list(ctf.GetColor(float(i) / table_size)) + [1]
        lut.SetTableValue(i, rgb)

    lut.SetTableRange(table_range[0], table_range[1])

    return lut

def cut_brain_hemi(hemi_elec_data,hemi_poly_data):

    depth_elec_data = hemi_elec_data[ (hemi_elec_data.eType=='D') | (hemi_elec_data.eType=='d')]
    print depth_elec_data
    print

    x_coords = np.array([avg_surf.x_snap for avg_surf in depth_elec_data.avgSurf],dtype=np.float)
    y_coords = np.array([avg_surf.y_snap for avg_surf in depth_elec_data.avgSurf],dtype=np.float)
    z_coords = np.array([avg_surf.z_snap for avg_surf in depth_elec_data.avgSurf],dtype=np.float)

    x_min, x_max = np.min(x_coords),np.max(x_coords)
    y_min, y_max = np.min(y_coords),np.max(y_coords)
    z_min, z_max = np.min(z_coords),np.max(z_coords)

    clipPlane = vtk.vtkPlane()
    clipPlane.SetNormal(0.0, 0.0, 1.0)
    # clipPlane.SetOrigin(0, 0, np.max(z_coords))
    # clipPlane.SetOrigin(np.max(x_coords), np.max(y_coords), np.max(z_coords))

    clipPlane.SetOrigin(0, 0, -500)

    clipper = vtk.vtkClipPolyData()
    clipper.SetInputData(hemi_poly_data)
    clipper.SetClipFunction(clipPlane)

    return clipper



def get_hemi_polydata(hemi='lh'):

    vreader = vtk.vtkPolyDataReader()
    # vreader.SetFileName('lh.vtk')
    if hemi.startswith('l'):
        vreader.SetFileName('lh.pial.vtk')
    elif hemi.startswith('r'):
        vreader.SetFileName('rh.pial.vtk')
    else:
        raise RuntimeError('hemi argument must begin with letter "l" or "r" ')

    vreader.Update()

    pd = vreader.GetOutput()

    return pd


def get_electrode_vis_data(hemi_data, lut):

    electrode_points = vtk.vtkPoints()
    electrode_colors = vtk.vtkUnsignedCharArray()
    electrode_colors.SetNumberOfComponents(3)

    num_electrodes = len(hemi_data)

    for i, avg_surf in enumerate(hemi_data.avgSurf):
        # print avg_surf
        # electrode_points.InsertNextPoint(avg_surf.x_snap, avg_surf.y_snap, avg_surf.z_snap)
        electrode_points.InsertNextPoint(avg_surf.x_snap, avg_surf.y_snap, avg_surf.z_snap)

        # electrode_colors.InsertNextTupleValue((255, 0, 0))
        color_tuple = [0, 0, 0]
        lut.GetColor(i, color_tuple)
        # lut.GetColor(num_electrodes,color_tuple)

        color_tuple = map(lambda x: int(round(x * 255)), color_tuple)

        electrode_colors.InsertNextTupleValue(color_tuple)

    return electrode_points, electrode_colors


def BrainPlotExample(lh_elec_data=None, rh_elec_data=None, electrode_types=['D', 'G', 'S']):
    """A simple example that uses the QVTKRenderWindowInteractor class."""

    vtk_major_version = vtk.vtkVersion().GetVTKMajorVersion()

    import numpy as np
    # every QT app needs an app
    app = QtGui.QApplication(['QVTKRenderWindowInteractor'])
    widget = QVTKRenderWindowInteractor()

    widget.setMouseInteractionSchemeTo3D()

    widget.Initialize()
    widget.Start()
    # if you dont want the 'q' key to exit comment this.
    widget.AddObserver("ExitEvent", lambda o, e, a=app: a.quit())

    ren = vtk.vtkRenderer()
    widget.GetRenderWindow().AddRenderer(ren)



    # vreader = vtk.vtkPolyDataReader()
    # # vreader.SetFileName('lh.vtk')
    # vreader.SetFileName('lh.pial.vtk')
    # vreader.Update()
    #
    # pd = vreader.GetOutput()
    # # rps = vtk.vtkRegularPolygonSource(pd)

    l_pd = get_hemi_polydata(hemi='l')
    r_pd = get_hemi_polydata(hemi='r')

    # brain cutter
    # if len(electrode_types)==1 and electrode_types[0].lower()=='d':
    #     # will cut brain
    #     clipper = cut_brain_hemi(lh_elec_data,pd)

    # clipPlane = vtk.vtkPlane()
    # clipPlane.SetNormal(1.0, -1.0, -1.0)
    # clipPlane.SetOrigin(0, 0, 0)
    #
    # clipper = vtk.vtkClipPolyData()
    # clipper.SetInputData(pd)
    # clipper.SetClipFunction(clipPlane)
    #

    l_brain_mapper = vtk.vtkPolyDataMapper()
    r_brain_mapper = vtk.vtkPolyDataMapper()

    if vtk_major_version <= 5:

        l_brain_mapper.SetInput(l_pd)
        r_brain_mapper.SetInput(r_pd)

    else:
        l_brain_mapper.SetInputData(l_pd)
        r_brain_mapper.SetInputData(r_pd)

    # brain cutter
    # brain_mapper = vtk.vtkPolyDataMapper()
    #
    # if vtk_major_version <= 5:
    #
    #     # brain_mapper.SetInput(clipper)
    #     brain_mapper.SetInputConnection(clipper.GetOutputPort())
    #
    # else:
    #     brain_mapper.SetInputConnection(clipper.GetOutputPort())

    brain_opacity = 0.2

    l_brain_actor = vtk.vtkActor()
    l_brain_actor.SetMapper(l_brain_mapper)
    l_brain_actor.GetProperty().SetOpacity(brain_opacity)
    ren.AddActor(l_brain_actor)



    r_brain_actor = vtk.vtkActor()
    r_brain_actor.SetMapper(r_brain_mapper)
    r_brain_actor.GetProperty().SetOpacity(brain_opacity)

    ren.AddActor(r_brain_actor)


    #

    cam = widget.GetRenderWindow().GetRenderers().GetFirstRenderer().GetActiveCamera()
    # inside left hemisphere
    cam.SetClippingRange((342.503, 551.901))
    cam.SetFocalPoint(-33.7454, -18.4959, 15.5496)
    cam.SetPosition(396.483, -24.5132, 77.7444)
    cam.SetViewUp(-0.137778, 0.192088, 0.971658)

    # # # outside left hemisphere
    # # cam.SetClippingRange(280.84, 629.522)
    # # cam.SetFocalPoint(-33.7454, -18.4959, 15.5496)
    # # cam.SetPosition(-423.573, 88.4119, 175.569)
    # # cam.SetViewUp(0.378739, -0.00424452, 0.925494)
    #
    #
    # from the top left hemisphere
    # cam.SetClippingRange(296.138, 610.266)
    # cam.SetFocalPoint(-33.7454, -18.4959, 15.5496)
    # cam.SetPosition(1.36993, -35.0308, 448.556)
    # cam.SetViewUp(-0.086411, -0.995777, -0.0310175)


    electrodeGrid = vtk.vtkUnstructuredGrid()

    l_e_pts = vtk.vtkPoints()
    lh_e_colors = vtk.vtkUnsignedCharArray()
    lh_e_colors.SetNumberOfComponents(3)

    num_electrodes = len(lh_elec_data)

    lut = vtk.vtkLookupTable()
    lut.SetTableRange(0, num_electrodes)
    lut.Build()

    # lut = divergent_color_lut(table_range=[0, num_electrodes])
    lut = divergent_color_lut(table_range=[0, 120])


    lh_e_pts , lh_e_colors = get_electrode_vis_data(hemi_data=lh_elec_data, lut=lut)
    rh_e_pts , rh_e_colors = get_electrode_vis_data(hemi_data=rh_elec_data, lut=lut)


    # print lh_elec_data
    # for i, avg_surf in enumerate(lh_elec_data.avgSurf):
    #     print avg_surf
    #     # electrode_points.InsertNextPoint(avg_surf.x_snap, avg_surf.y_snap, avg_surf.z_snap)
    #     electrode_points.InsertNextPoint(avg_surf.x, avg_surf.y, avg_surf.z)
    #
    #     # electrode_colors.InsertNextTupleValue((255, 0, 0))
    #     color_tuple = [0, 0, 0]
    #     lut.GetColor(i, color_tuple)
    #     # lut.GetColor(num_electrodes,color_tuple)
    #
    #     color_tuple = map(lambda x: int(round(x * 255)), color_tuple)
    #
    #     electrode_colors.InsertNextTupleValue(color_tuple)

    e_glyph_shape = vtk.vtkSphereSource()

    


    # cone.SetResolution(5)
    # cone.SetHeight(2)
    e_glyph_shape.SetRadius(3.0)

    l_glyphs = vtk.vtkGlyph3D()
    l_glyphs.SetSourceConnection(e_glyph_shape.GetOutputPort())
    l_glyphs.SetColorModeToColorByScalar()

    l_centroidsPD = vtk.vtkPolyData()
    l_centroidsPD.SetPoints(lh_e_pts)
    l_centroidsPD.GetPointData().SetScalars(lh_e_colors)

    r_glyphs = vtk.vtkGlyph3D()
    r_glyphs.SetSourceConnection(e_glyph_shape.GetOutputPort())
    r_glyphs.SetColorModeToColorByScalar()

    r_centroidsPD = vtk.vtkPolyData()
    r_centroidsPD.SetPoints(rh_e_pts)
    r_centroidsPD.GetPointData().SetScalars(rh_e_colors)


    if vtk_major_version == 5:

        l_glyphs.SetInput(l_centroidsPD)
        r_glyphs.SetInput(r_centroidsPD)
        
    else:
        l_glyphs.SetInputData(l_centroidsPD)
        r_glyphs.SetInputData(r_centroidsPD)

    l_glyphs.ScalingOff()  # IMPORTANT
    l_glyphs.Update()
    
    r_glyphs.ScalingOff()  # IMPORTANT
    r_glyphs.Update()
    

    l_glyphsMapper = vtk.vtkPolyDataMapper()
    l_glyphsMapper.SetInputConnection(l_glyphs.GetOutputPort())
    
    r_glyphsMapper = vtk.vtkPolyDataMapper()
    r_glyphsMapper.SetInputConnection(r_glyphs.GetOutputPort())
    
    
    l_electrodes_actor = vtk.vtkActor()
    l_electrodes_actor.SetMapper(l_glyphsMapper)
    ren.AddActor(l_electrodes_actor)

    r_electrodes_actor = vtk.vtkActor()
    r_electrodes_actor.SetMapper(r_glyphsMapper)
    ren.AddActor(r_electrodes_actor)


    ####################### AXES
    axes = vtk.vtkAxesActor()
    transform = vtk.vtkTransform()
    transform.Translate(-0.0, 0.0, 0.0)
    transform.Scale(100.0, 100.0, 100.0)

    axes.SetUserTransform(transform)

    axes.AxisLabelsOff()

    ren.AddActor(axes)
    widget.resize(600,600)

    # show the widget
    widget.raise_()

    widget.show()

    # start event processing
    app.exec_()


if __name__ == "__main__":
    # QVTKRenderWidgetConeExample()
    sys.path.append('/Users/m/PTSA_NEW_GIT')

    # tal_path = '/Users/m/data/eeg/R1111M/tal/R1111M_talLocs_database_bipol.mat'
    tal_path = '/Users/m/data/eeg/R1060M/tal/R1060M_talLocs_database_bipol.mat'

    electrode_types =['D','S','G']
    lh_elec_data, rh_elec_data = extract_electrode_positions(tal_path=tal_path, electrode_types=electrode_types)

    BrainPlotExample(lh_elec_data=lh_elec_data, rh_elec_data=rh_elec_data,electrode_types=electrode_types)
