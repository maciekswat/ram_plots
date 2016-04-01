import sys

sys.path.append('/Users/m/RAM_UTILS_GIT')

import glob
import shutil
import os
from os.path import *

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import QtGui
from brain_plot_utils import *

import ui_GraphicsFrame
from collections import OrderedDict
import pandas as pd

from JSONUtils import JSONNode

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
        self.ren.SetBackground(1.,1.,1.)
        self.renWin = self.qvtkWidget.GetRenderWindow()
        self.renWin.AddRenderer(self.ren)

        self.bounds_array=[]

        self.bounds_min = None

        self.bounds_max = None

        self.slider_min = None
        self.slider_max = None
        self.slider_pos = None
        self.normals ={
            'x':np.array([1.,0.,0.],dtype=np.float),
            'y':np.array([0.,1.,0.],dtype=np.float),
            'z':np.array([0.,0.,1.],dtype=np.float),

        }

        self.normals_flip ={
            'x':np.array([-1.,0.,0.],dtype=np.float),
            'y':np.array([0.,-1.,0.],dtype=np.float),
            'z':np.array([0.,0.,-1.],dtype=np.float),

        }


        self.camera_setting_dir = os.getcwd()

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

        self.render_scene()

    @pyqtSignature("")
    def on_cut_plane_pos_S_sliderReleased(self):
        print 'slider_released'
        self.render_scene()

    @pyqtSignature("bool")
    def on_flip_visible_part_RB_toggled(self,flag):
        self.render_scene()

    @pyqtSignature("bool")
    def on_cut_plane_CB_toggled(self,flag):
        print 'got this flag=',flag
        self.render_scene()


    @pyqtSignature("")
    def on_save_camera_PB_clicked(self):
        print 'print clicked save_cam'
        self.save_camera_setting()

    @pyqtSignature("")
    def on_load_camera_PB_clicked(self):
        self.load_camera_settings()



    @pyqtSignature("")
    def on_photoshoot_PB_clicked(self):
        self.photoshoot()

    @pyqtSignature("")
    def on_camera_setting_dir_PB_clicked(self):
        print 'on_camera_setting_dir_PB_clicked'
        dirname = QFileDialog.getExistingDirectory(self, 'Save Camera Setting Dir', self.camera_setting_dir)

        self.camera_setting_LE.setText(dirname)

    def photoshoot(self,camera_setting_dir='',output_dir=''):


        if not output_dir:
            output_dir = os.getcwd()

        if not isdir(output_dir):
            os.makedirs(output_dir)

        if not camera_setting_dir:
            camera_setting_dir = str(self.camera_setting_LE.text())

        if not camera_setting_dir:

            camera_setting_dir = join(os.getcwd(),'camera_settings')

        camera_files = glob.glob(join(camera_setting_dir,'*.camera.json'))
        print camera_files

        screenshot_core_name = str(self.screenshot_core_name_LE.text())
        for c_file in camera_files:
            self.load_camera_settings(c_file)

            screenshot_filename = join(output_dir,screenshot_core_name+'_'+ basename(c_file)+'.png')
            self.take_screenshot(screenshot_filename)
            # self.take_screenshot(c_file+'.png')

    def take_screenshot(self,screenshot_filename=''):
        if not screenshot_filename:
            return

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
        writer.SetFileName(screenshot_filename)

        writer.Write()



    def save_camera_setting(self,filename=''):

        filename = QFileDialog.getSaveFileName(self, 'Save Camera Setting File', self.camera_setting_dir)
        filename = abspath(str(filename))

        self.camera_setting_dir = dirname(filename)



        cam = self.qvtkWidget.GetRenderWindow().GetRenderers().GetFirstRenderer().GetActiveCamera()
        cam_node = JSONNode()
        clipping_range_node = cam_node.add_child_node('clipping_range')
        clipping_range = cam.GetClippingRange()
        clipping_range_node['min'] = clipping_range[0]
        clipping_range_node['max'] = clipping_range[1]
        
        focal_point = cam.GetFocalPoint()
        focal_point_node = cam_node.add_child_node('focal_point')
        focal_point_node['x'] = focal_point[0]
        focal_point_node['y'] = focal_point[1]
        focal_point_node['z'] = focal_point[2]
        
        position =  cam.GetPosition()
        position_node = cam_node.add_child_node('position')
        position_node['x'] = position[0]
        position_node['y'] = position[1]
        position_node['z'] = position[2]
        

        view_up =  cam.GetViewUp()
        view_up_node = cam_node.add_child_node('view_up')
        view_up_node['x'] = view_up[0]
        view_up_node['y'] = view_up[1]
        view_up_node['z'] = view_up[2]
        

        print cam_node.output()


        cam_node.write(filename)
        # cam_node.write('default.camera.json')

        # # top view
        # cam.SetClippingRange((312.385, 827.346))
        # cam.SetFocalPoint(23.9803, -13.4557, 27.6483)
        # cam.SetPosition(-2.03758, 20.7186, 539.993)
        # cam.SetViewUp(0.0346923, 0.997298, -0.0647596)

        pass

    def load_camera_settings(self,filename=''):
        if not filename:
            filename = 'default.camera.json'

        cam = self.qvtkWidget.GetRenderWindow().GetRenderers().GetFirstRenderer().GetActiveCamera()

        cam_node = JSONNode.read(filename)
        cam.SetClippingRange(float(cam_node['clipping_range']['min']),float(cam_node['clipping_range']['max']))
        cam.SetFocalPoint(float(cam_node['focal_point']['x']),float(cam_node['focal_point']['y']),float(cam_node['focal_point']['z']))
        cam.SetPosition(float(cam_node['position']['x']),float(cam_node['position']['y']),float(cam_node['position']['z']))
        cam.SetViewUp(float(cam_node['view_up']['x']),float(cam_node['view_up']['y']),float(cam_node['view_up']['z']))


        self.render_scene()
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

    def add_display_object(self, obj_name, obj):
        self.display_obj_dict[obj_name]=obj

    def cut_mapper(self,mapper):

        cut_normal = [0.,0.,0.]

        normal = self.normals[str(self.cut_axis_CB.currentText()).lower()]

        if self.flip_visible_part_RB.isChecked():
            normal  = self.normals_flip[str(self.cut_axis_CB.currentText()).lower()]

        print normal
        clipPlane = vtk.vtkPlane()

        pos = self.cut_plane_pos_S.value()
        slider_fraction = float(pos) / (self.cut_plane_pos_S.maximum()-self.cut_plane_pos_S.minimum())

        axis_txt = str(self.cut_axis_CB.currentText()).lower()
        if self.bounds_min is not None and self.bounds_max is not None:
            if axis_txt =='x':
                origin = [self.bounds_min[0]+(self.bounds_max[1]-self.bounds_min[0])*slider_fraction,0.,0.]
            elif axis_txt =='y':
                origin = [0.,self.bounds_min[2]+(self.bounds_max[3]-self.bounds_min[2])*slider_fraction,0.]
            elif axis_txt =='z':
                origin = [0.,0.,self.bounds_min[4]+(self.bounds_max[5]-self.bounds_min[4])*slider_fraction]
            else:
                raise RuntimeError('axis string has to be x, y or z')


        clipPlane.SetNormal(*normal)
        clipPlane.SetOrigin(*origin)


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
        w.resize(1000,1000)
        #
        # # tal_path = '/Users/m/data/eeg/R1111M/tal/R1111M_talLocs_database_bipol.mat'
        # tal_path = '/Users/m/data/eeg/R1111M/tal/R1111M_talLocs_database_monopol.mat'
        #
        #
        # from ptsa.data.readers import TalReader
        # tal_reader = TalReader(filename=tal_path, struct_name='talStruct')
        # tal_structs = tal_reader.read()
        #
        # tal_structs = tal_structs[(tal_structs.tagName=='LPOG2') |  (tal_structs.tagName=='LPOG10')]
        # print
        # 28    3.810593 -66.054467 -23.321447 -15.071706     G

        #
        # depth_lh_elec_data, depth_rh_elec_data = extract_electrode_positions_for_single_subject(tal_structs=tal_structs, electrode_types=['D'])
        # strip_lh_elec_data, strip_rh_elec_data = extract_electrode_positions_for_single_subject(tal_structs=tal_structs, electrode_types=['S'])
        # grid_lh_elec_data, grid_rh_elec_data = extract_electrode_positions_for_single_subject(tal_structs=tal_structs, electrode_types=['G'])
        #

        # lh = Hemisphere(hemi='l')
        # lh.set_opacity(0.5)
        #
        # rh = Hemisphere(hemi='r')
        # # rh.set_color(c=[1,0,0])
        # rh.set_opacity(0.5)
        #
        # w.add_display_object('lh',lh)
        # w.add_display_object('rh',rh)
        #
        #
        # # w.add_actor('lh',lh.get_actor())
        # # w.add_actor('rh',rh.get_actor())
        #
        # w.add_bounds(lh.get_bounds())
        # w.add_bounds(rh.get_bounds())
        #
        #
        # depth_elec = Electrodes(shape='cone')
        # # elec.set_electrodes_locations(loc_array=[[0,0,0]])
        # depth_elec.set_electrodes_locations(loc_array=depth_lh_elec_data)
        # depth_elec.set_electrodes_color(c=[0,255,0])
        # # w.add_actor('depth_elec',depth_elec.get_actor())
        #
        # w.add_display_object('depth_elec',depth_elec)
        #
        #
        #
        # strip_elec = Electrodes(shape='sphere')
        # # elec.set_electrodes_locations(loc_array=[[0,0,0]])
        # strip_elec.set_electrodes_locations(loc_array=strip_lh_elec_data)
        # strip_elec.set_electrodes_color(c=[255,255,0])
        # # w.add_actor('strip_elec',strip_elec.get_actor())
        # w.add_display_object('strip_elec',strip_elec)
        #
        #
        # grid_elec = Electrodes(shape='sphere')
        # # elec.set_electrodes_locations(loc_array=[[0,0,0]])
        # grid_elec.set_electrodes_locations(loc_array=grid_lh_elec_data)
        #
        # grid_elec.color_electrodes_by_scalars(scalar_array=np.arange(len(grid_lh_elec_data))/10.0)
        # # grid_elec.set_electrodes_color(c=[255,0,0])
        # # w.add_actor('grid_elec',grid_elec.get_actor())
        # w.add_display_object('grid_elec',grid_elec)
        #
        # w.display()
        #

        # # working stuff
        # tdf = pd.DataFrame.from_csv('ttest_table_with_location.csv')
        #
        #
        # interesting_tdf = tdf[tdf.p<0.05][['t','x','y','z','eType']]
        # d_tdf_pos = interesting_tdf[(interesting_tdf.eType=='D') & (interesting_tdf.t>0.)][['x','y','z']]
        # g_tdf_pos = interesting_tdf[(interesting_tdf.eType=='G') & (interesting_tdf.t>0.)][['x','y','z']]
        # s_tdf_pos = interesting_tdf[(interesting_tdf.eType=='S') & (interesting_tdf.t>0.)][['x','y','z']]
        #
        # d_tdf_neg = interesting_tdf[(interesting_tdf.eType=='D') & (interesting_tdf.t<=0.)][['x','y','z']]
        # g_tdf_neg = interesting_tdf[(interesting_tdf.eType=='G') & (interesting_tdf.t<=0.)][['x','y','z']]
        # s_tdf_neg = interesting_tdf[(interesting_tdf.eType=='S') & (interesting_tdf.t<=0.)][['x','y','z']]



        # tdf = pd.DataFrame.from_csv('ttest_table_params_with_location.csv')


        ttest_table_df_filename = 'ttest_table_params.csv'

        tdf = pd.DataFrame.from_csv(ttest_table_df_filename)
        coords_tdf = pd.DataFrame.from_csv('coords_'+ttest_table_df_filename)

        interesting_tdf = tdf[(tdf.p<=0.01) & (tdf.t>0) & (tdf.N>5)]
        # interesting_tdf = tdf[(tdf.p <= 0.01) & (tdf.t > 0) ]


        interesting_coords_tdf =  coords_tdf[ coords_tdf.subject.isin(interesting_tdf.index)
                          &
                          (coords_tdf.tagName.isin(interesting_tdf.stimAnodeTag)
                           | coords_tdf.tagName.isin(interesting_tdf.stimCathodeTag))
                          # & (coords_tdf.eType=='D')
        ]


        # interesting_tdf = tdf[(tdf.p<0.01) & (tdf.t>0) ][['t','x','y','z','eType']]




        tdf_pos = interesting_coords_tdf[['x','y','z']]




        ni_tdf = tdf[(tdf.p>0.01) ]


        ni_coords_tdf =  coords_tdf[ coords_tdf.subject.isin(ni_tdf.index)
                          &
                          (coords_tdf.tagName.isin(ni_tdf.stimAnodeTag)
                           | coords_tdf.tagName.isin(ni_tdf.stimCathodeTag))
                            # & (coords_tdf.eType == 'D')
        ]


        tdf_ni = ni_coords_tdf[['x','y','z']]



        r1111_coords_tdf =  coords_tdf[ coords_tdf.subject.isin(['R1111M'])
                          &
                          (coords_tdf.tagName.isin(['LPOG10','LPOG2','LPOG1','LPOG9'])
                           )
        ]


        tdf_r1111 = r1111_coords_tdf[['x','y','z']]



        # d_tdf_neg = interesting_tdf[(interesting_tdf.eType=='D') & (interesting_tdf.t<=0.)][['x','y','z']]
        # g_tdf_neg = interesting_tdf[(interesting_tdf.eType=='G') & (interesting_tdf.t<=0.)][['x','y','z']]
        # s_tdf_neg = interesting_tdf[(interesting_tdf.eType=='S') & (interesting_tdf.t<=0.)][['x','y','z']]


        # non_interesting_tdf = tdf[(tdf.p>0.05)  ][['t','x','y','z','eType']]
        # d_tdf_ni = non_interesting_tdf[(non_interesting_tdf.eType=='D') ][['x','y','z']]
        # g_tdf_ni = non_interesting_tdf[(non_interesting_tdf.eType=='G') ][['x','y','z']]
        # s_tdf_ni = non_interesting_tdf[(non_interesting_tdf.eType=='S') ][['x','y','z']]
        #

        # s_tdf_r1111m = tdf[(tdf.stimAnodeTag=='LPOG10') & (tdf.stimCathodeTag=='LPOG2') ][['t','x','y','z','eType']]




        # depth_lh_elec_data, depth_rh_elec_data


        lh = Hemisphere(hemi='l')
        lh.set_opacity(0.2)

        rh = Hemisphere(hemi='r')
        # rh.set_color(c=[1,0,0])
        rh.set_opacity(0.2)

        w.add_display_object('lh',lh)
        w.add_display_object('rh',rh)


        # w.add_actor('lh',lh.get_actor())
        # w.add_actor('rh',rh.get_actor())

        w.add_bounds(lh.get_bounds())
        w.add_bounds(rh.get_bounds())


        # # non significant
        # depth_elec_ni = Electrodes(shape='cone')
        # # elec.set_electrodes_locations(loc_array=[[0,0,0]])
        # depth_elec_ni.set_electrodes_locations(loc_array=d_tdf_ni.values)
        # depth_elec_ni.set_electrodes_color(c=[0,255,0])
        # # w.add_actor('depth_elec',depth_elec.get_actor())
        # w.add_display_object('depth_elec_neg',depth_elec_ni)
        #
        #
        #
        # strip_elec_ni = Electrodes(shape='sphere')
        # # elec.set_electrodes_locations(loc_array=[[0,0,0]])
        # strip_elec_ni.set_electrodes_locations(loc_array=s_tdf_ni.values)
        # strip_elec_ni.set_electrodes_color(c=[0,255,0])
        # # w.add_actor('strip_elec',strip_elec.get_actor())
        # w.add_display_object('strip_elec_neg',strip_elec_ni)
        #
        #
        # grid_elec_ni = Electrodes(shape='sphere')
        # # elec.set_electrodes_locations(loc_array=[[0,0,0]])
        # grid_elec_ni.set_electrodes_locations(loc_array=g_tdf_ni.values)
        #
        # # grid_elec.color_electrodes_by_scalars(scalar_array=np.arange(len(grid_lh_elec_data))/10.0)
        # grid_elec_ni.set_electrodes_color(c=[0,255,0])
        # # w.add_actor('grid_elec',grid_elec.get_actor())
        # w.add_display_object('grid_elec_neg',grid_elec_ni)



        ni_elec = Electrodes(shape='sphere')
        # elec.set_electrodes_locations(loc_array=[[0,0,0]])
        ni_elec.set_electrodes_locations(loc_array=tdf_ni.values)
        ni_elec.set_electrodes_color(c=[255,255,0])
        # w.add_actor('depth_elec',depth_elec.get_actor())
        w.add_display_object('ni_elec',ni_elec)




        i_elec = Electrodes(shape='sphere')
        # elec.set_electrodes_locations(loc_array=[[0,0,0]])
        i_elec.set_electrodes_locations(loc_array=tdf_pos.values)
        i_elec.set_electrodes_color(c=[255,0,0])
        # w.add_actor('depth_elec',depth_elec.get_actor())
        w.add_display_object('i_elec',i_elec)

        #
        # r1111_elec = Electrodes(shape='sphere')
        # # elec.set_electrodes_locations(loc_array=[[0,0,0]])
        # r1111_elec.set_electrodes_locations(loc_array=tdf_r1111.values)
        # r1111_elec.set_electrodes_color(c=[0,0,255])
        # # w.add_actor('depth_elec',depth_elec.get_actor())
        # w.add_display_object('r1111_elec',r1111_elec)




        # strip_elec = Electrodes(shape='sphere')
        # # elec.set_electrodes_locations(loc_array=[[0,0,0]])
        # strip_elec.set_electrodes_locations(loc_array=s_tdf_pos.values)
        # strip_elec.set_electrodes_color(c=[255,0,0])
        # # w.add_actor('strip_elec',strip_elec.get_actor())
        # w.add_display_object('strip_elec',strip_elec)
        #
        #
        # grid_elec = Electrodes(shape='sphere')
        # # elec.set_electrodes_locations(loc_array=[[0,0,0]])
        # grid_elec.set_electrodes_locations(loc_array=g_tdf_pos.values)
        #
        # # grid_elec.color_electrodes_by_scalars(scalar_array=np.arange(len(grid_lh_elec_data))/10.0)
        # grid_elec.set_electrodes_color(c=[255,0,0])
        # # w.add_actor('grid_elec',grid_elec.get_actor())
        # w.add_display_object('grid_elec',grid_elec)


        # r1111_elec = Electrodes(shape='sphere')
        # # elec.set_electrodes_locations(loc_array=[[0,0,0]])
        # r1111_elec.set_electrodes_locations(loc_array=s_tdf_r1111m.values)
        #
        # # grid_elec.color_electrodes_by_scalars(scalar_array=np.arange(len(grid_lh_elec_data))/10.0)
        # r1111_elec.set_electrodes_color(c=[255,255,0])
        # # w.add_actor('grid_elec',grid_elec.get_actor())
        # w.add_display_object('r1111_elec',r1111_elec)






        # depth_elec_neg = Electrodes(shape='cone')
        # # elec.set_electrodes_locations(loc_array=[[0,0,0]])
        # depth_elec_neg.set_electrodes_locations(loc_array=d_tdf_neg.values)
        # depth_elec_neg.set_electrodes_color(c=[0,0,255])
        # # w.add_actor('depth_elec',depth_elec.get_actor())
        # w.add_display_object('depth_elec_neg',depth_elec_neg)
        #
        #
        #
        # strip_elec_neg = Electrodes(shape='sphere')
        # # elec.set_electrodes_locations(loc_array=[[0,0,0]])
        # strip_elec_neg.set_electrodes_locations(loc_array=s_tdf_neg.values)
        # strip_elec_neg.set_electrodes_color(c=[0,0,255])
        # # w.add_actor('strip_elec',strip_elec.get_actor())
        # w.add_display_object('strip_elec_neg',strip_elec_neg)
        #
        #
        # grid_elec_neg = Electrodes(shape='sphere')
        # # elec.set_electrodes_locations(loc_array=[[0,0,0]])
        # grid_elec_neg.set_electrodes_locations(loc_array=g_tdf_neg.values)
        #
        # # grid_elec.color_electrodes_by_scalars(scalar_array=np.arange(len(grid_lh_elec_data))/10.0)
        # grid_elec_neg.set_electrodes_color(c=[0,0,255])
        # # w.add_actor('grid_elec',grid_elec.get_actor())
        # w.add_display_object('grid_elec_neg',grid_elec_neg)



        w.display()



