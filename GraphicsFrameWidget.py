from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import QtGui
from brain_plot_utils import *

import ui_GraphicsFrame
from collections import OrderedDict

# import ui_configurationdlg  # the file generated by 'pyuic4' using the .ui Designer file
#
# MAC = "qt_mac_set_native_menubar" in dir()
#
# MODULENAME = '------- ConfigurationDialog.py: '
#
#
# class ConfigurationDialog(QDialog, ui_configurationdlg.Ui_CC3DPrefs, ConfigurationPageBase):
#
#     def __init__(self, parent = None, name = None, modal = False):
#         QDialog.__init__(self, parent)
#         self.setModal(modal)
#
#         self.paramCC3D = {}   #  dict for ALL parameters on CC3D Preferences dialog
#
#         self.initParams()  # read params from QSession file
#
#         self.setupUi(self)   # in ui_configurationdlg.Ui_CC3DPrefs



class GraphicsFrameWidget(QtGui.QFrame,ui_GraphicsFrame.Ui_GraphicsFrame):
    # def __init__(self, parent=None, wflags=QtCore.Qt.WindowFlags(), **kw):
    def __init__(self, parent=None, originatingWidget=None):
        self.app = QtGui.QApplication(['QVTKRenderWindowInteractor']) # qt app must be constructed here

        QtGui.QFrame.__init__(self, parent)
        self.setupUi(self)

        self.cut_axis_CB.setEnabled(self.cut_plane_CB.isChecked())
        self.cut_plane_pos_S.setEnabled(self.cut_plane_CB.isChecked())



        self.actors_dict={}

        self.display_obj_dict=OrderedDict()

        self.setMinimumSize(100, 100) #needs to be defined to resize smaller than 400x400
        self.resize(600, 600)


        # print '\n\n\n\n\n CREATING NEW GRAPHICS FRAME WIDGET ',self


        # self.allowSaveLayout = True
        self.is_screenshot_widget = False
        self.qvtkWidget = QVTKRenderWindowInteractor(self)   # a QWidget
        self.qvtkWidget.setMouseInteractionSchemeTo3D()

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        # spacer_item = self.verticalLayout.takeAt(1)
        self.verticalLayout.addWidget(self.qvtkWidget)
        # self.verticalLayout.addItem(spacer_item)

        # MDIFIX
        self.parentWidget = originatingWidget
        # self.parentWidget = parent


        self.plane = None
        self.planePos = None

        # self.lineEdit = QtGui.QLineEdit()

        # self.__initCrossSectionActions()
        # self.cstb = self.initCrossSectionToolbar()

        # layout = QtGui.QBoxLayout(QtGui.QBoxLayout.TopToBottom)
        # # layout.addWidget(self.cstb)
        # layout.addWidget(self.qvtkWidget)
        # self.setLayout(layout)
        # self.setMinimumSize(100, 100) #needs to be defined to resize smaller than 400x400
        # self.resize(600, 600)
        #
        # self.qvtkWidget.Initialize()
        # self.qvtkWidget.Start()

        self.ren = vtk.vtkRenderer()
        self.renWin = self.qvtkWidget.GetRenderWindow()
        self.renWin.AddRenderer(self.ren)

        self.bounds_array=[]

        self.bounds_min = None

        self.bounds_max = None

        self.slider_min = None
        self.slider_max = None
        self.slider_pos = None


    def display(self):

        self.render_scene()

        self.raise_()

        self.show()

        # start event processing
        self.app.exec_()


    def add_actor(self,actor_name, actor):
        self.ren.AddActor(actor)
        self.actors_dict[actor_name]=actor

    @pyqtSignature("")
    def on_savePB_clicked(self):
        print 'THIS IS SAVE SLOT'
        self.take_screenshot()


    def take_screenshot(self,filename=''):
        if not filename:

            filename=str(self.screenshotLE.text())


        if filename =='':
            return
        else:

            ren = self.qvtkWidget.GetRenderWindow().GetRenderers().GetFirstRenderer()
            renderLarge = vtk.vtkRenderLargeImage()
            if vtk_major_version <= 5:
                renderLarge.SetInputData(ren)
            else:
                renderLarge.SetInput(ren)


            renderLarge.SetMagnification(1)

            # We write out the image which causes the rendering to occur. If you
            # watch your screen you might see the pieces being rendered right
            # after one another.
            writer = vtk.vtkPNGWriter()
            writer.SetInputConnection(renderLarge.GetOutputPort())
            # # # print "GOT HERE fileName=",fileName
            writer.SetFileName(filename)

            writer.Write()

    @pyqtSignature("QString")
    def on_cut_axis_CB_currentIndexChanged(self,axis):

        axis_txt = str(axis)
        print 'axis changed to ',axis_txt
        self.slider_min = None
        self.slider_max = None
        self.slider_pos = None



        print self.cut_plane_pos_S.minimum()
        print self.cut_plane_pos_S.maximum()

        axis_min_max_tuple = self.get_min_max(axis=axis_txt)
        if axis_min_max_tuple[0] is None:
            return

        self.slider_min = axis_min_max_tuple[0]
        self.slider_max = axis_min_max_tuple[1]

        print 'slider_min,slider_max=',(self.slider_min, self.slider_max)

    def save_camera_setting(self,filename=''):
        pass

    def load_camera_settings(self,filename=''):
        pass

    def add_bounds(self,bounds):
        self.bounds_array.append(bounds)

        self.compute_bounds()

        print 'self.bounds_min=',self.bounds_min
        print 'self.bounds_max=',self.bounds_max

    def compute_bounds(self):
        if len(self.bounds_array):
            bounds_np = np.array(self.bounds_array, dtype=np.float)
# shape=(len(self.bounds_array),len(self.bounds_array[0])),
            self.bounds_min = np.amin(bounds_np,axis=0)
            self.bounds_max = np.amax(bounds_np,axis=0)

    def get_min_max(self,axis='x'):

        if self.bounds_max is  None or self.bounds_min is  None:
            return None, None

        if axis.lower()=='x':
            return self.bounds_min[0],self.bounds_max[1]
        elif axis.lower()=='y':
            return self.bounds_min[2],self.bounds_max[3]
        elif axis.lower()=='z':
            return self.bounds_min[4],self.bounds_max[5]

        raise RuntimeError('axis string has to be x, y or z')

    @pyqtSignature("")
    def on_cut_plane_pos_S_sliderReleased(self):
        print 'slider_released'

        print self.cut_plane_pos_S.value()

        self.render_scene()

    @pyqtSignature("bool")
    def on_cut_plane_CB_toggled(self,flag):
        print 'got this flag=',flag
        self.render_scene()

    def add_display_object(self, obj_name, obj):
        self.display_obj_dict[obj_name]=obj

    def cut_mapper(self,mapper):
        clipPlane = vtk.vtkPlane()
        clipPlane.SetNormal(1.0, -1.0, -1.0)
        clipPlane.SetOrigin(0, 0, 0)

        clipper = vtk.vtkClipPolyData()
        clipper.SetInputData(mapper.GetInput())
        clipper.SetClipFunction(clipPlane)


        mapper.SetInputConnection(clipper.GetOutputPort())

        return mapper

    def render_scene(self):
        self.ren.RemoveAllViewProps()



        for disp_obj_name, disp_obj in self.display_obj_dict.items():
            mapper = disp_obj.get_polydata_mapper()

            if self.cut_plane_CB.isChecked():
                mapper = self.cut_mapper(mapper)



            actor = vtk.vtkActor()
            actor.SetMapper(mapper)

            if disp_obj.get_opacity() is not None:
                actor.GetProperty().SetOpacity(disp_obj.get_opacity())

            if disp_obj.get_color() is not None:
                actor.GetProperty().SetColor(disp_obj.get_color())

            # from random import random
            # actor.GetProperty().SetColor([random(),random(),random()])

            self.add_actor(disp_obj_name,actor)



        self.qvtkWidget.update()

if __name__=='__main__':
        sys.path.append('/Users/m/PTSA_NEW_GIT')

        # app = QtGui.QApplication(['QVTKRenderWindowInteractor'])

        w = GraphicsFrameWidget()

        tal_path = '/Users/m/data/eeg/R1111M/tal/R1111M_talLocs_database_bipol.mat'
        depth_lh_elec_data, depth_rh_elec_data = extract_electrode_positions_for_single_subject(tal_path=tal_path, electrode_types=['D'])
        strip_lh_elec_data, strip_rh_elec_data = extract_electrode_positions_for_single_subject(tal_path=tal_path, electrode_types=['S'])
        grid_lh_elec_data, grid_rh_elec_data = extract_electrode_positions_for_single_subject(tal_path=tal_path, electrode_types=['G'])



        lh = Hemisphere(hemi='l')
        lh.set_opacity(0.1)

        rh = Hemisphere(hemi='r')
        rh.set_color(c=[1,0,0])
        rh.set_opacity(0.1)

        w.add_display_object('lh',lh)
        w.add_display_object('rh',rh)


        # w.add_actor('lh',lh.get_actor())
        # w.add_actor('rh',rh.get_actor())

        w.add_bounds(lh.get_bounds())
        w.add_bounds(rh.get_bounds())


        depth_elec = Electrodes(shape='cone')
        # elec.set_electrodes_locations(loc_array=[[0,0,0]])
        depth_elec.set_electrodes_locations(loc_array=depth_lh_elec_data)
        depth_elec.set_electrodes_color(c=[0,255,0])
        # w.add_actor('depth_elec',depth_elec.get_actor())

        w.add_display_object('depth_elec',depth_elec)



        strip_elec = Electrodes(shape='sphere')
        # elec.set_electrodes_locations(loc_array=[[0,0,0]])
        strip_elec.set_electrodes_locations(loc_array=strip_lh_elec_data)
        strip_elec.set_electrodes_color(c=[255,255,0])
        # w.add_actor('strip_elec',strip_elec.get_actor())
        w.add_display_object('strip_elec',strip_elec)


        grid_elec = Electrodes(shape='sphere')
        # elec.set_electrodes_locations(loc_array=[[0,0,0]])
        grid_elec.set_electrodes_locations(loc_array=grid_lh_elec_data)

        grid_elec.color_electrodes_by_scalars(scalar_array=np.arange(len(grid_lh_elec_data))/10.0)
        # grid_elec.set_electrodes_color(c=[255,0,0])
        # w.add_actor('grid_elec',grid_elec.get_actor())
        w.add_display_object('grid_elec',grid_elec)

        w.display()



