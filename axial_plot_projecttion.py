import sys
from BrainGraphicsFrameWidget import BrainGraphicsFrameWidget
import pandas as pd
from brain_plot_utils import *

if __name__=='__main__':
        sys.path.append('/Users/m/PTSA_NEW_GIT')


        w = BrainGraphicsFrameWidget()
        w.resize(1000,1000)


        # tdf = pd.DataFrame.from_csv('ttest_table_params_with_location.csv')

        pos_significant_color = [255,0,0]
        neg_significant_color = [0, 0, 255]
        non_significant_color = [128, 128, 128]
        flipping_color = [0,255,0]

        ttest_table_df_filename = 'ttest_table_params.csv'

        tdf = pd.DataFrame.from_csv(ttest_table_df_filename)
        coords_tdf = pd.DataFrame.from_csv('coords_'+ttest_table_df_filename)

        # significant POS
        interesting_tdf = tdf[(tdf.p<=0.01) & (tdf.t>0) & (tdf.N>5)]
        # interesting_tdf = tdf[(tdf.p <= 0.01) & (tdf.t > 0) ]


        interesting_coords_tdf =  coords_tdf[ coords_tdf.subject.isin(interesting_tdf.index)
                          &
                          (coords_tdf.tagName.isin(interesting_tdf.stimAnodeTag)
                           | coords_tdf.tagName.isin(interesting_tdf.stimCathodeTag))
                          & (coords_tdf.eType=='D')
        ]


        # interesting_tdf = tdf[(tdf.p<0.01) & (tdf.t>0) ][['t','x','y','z','eType']]




        tdf_pos = interesting_coords_tdf[['x','y','z']]


        # significant NEG
        neg_interesting_tdf = tdf[(tdf.p <= 0.01) & (tdf.t < 0.0) & (tdf.N > 5)]
        # interesting_tdf = tdf[(tdf.p <= 0.01) & (tdf.t > 0) ]


        neg_interesting_coords_tdf = coords_tdf[coords_tdf.subject.isin(neg_interesting_tdf.index)
                                            &
                                            (coords_tdf.tagName.isin(neg_interesting_tdf.stimAnodeTag)
                                             | coords_tdf.tagName.isin(neg_interesting_tdf.stimCathodeTag))
            & (coords_tdf.eType=='D')
                                            ]

        # interesting_tdf = tdf[(tdf.p<0.01) & (tdf.t>0) ][['t','x','y','z','eType']]




        tdf_neg = neg_interesting_coords_tdf[['x', 'y', 'z']]


        print 'negative df = ',tdf_neg
        print 'positive df = ',tdf_pos


        # removing electrodes that are flip between sig pos and sig neg

        tdf_neg_filt = tdf_neg[~tdf_neg.index.isin(tdf_pos.index)]
        tdf_pos_filt = tdf_pos[~tdf_pos.index.isin(tdf_neg.index)]

        tdf_flip = tdf_neg[tdf_neg.index.isin(tdf_pos.index)]

        # tdf_neg_filt = tdf_neg
        # tdf_pos_filt = tdf_pos


        print tdf_neg_filt
        print tdf_pos_filt


        ni_tdf = tdf[(tdf.p>0.01) ]


        ni_coords_tdf =  coords_tdf[ coords_tdf.subject.isin(ni_tdf.index)
                          &
                          (coords_tdf.tagName.isin(ni_tdf.stimAnodeTag)
                           | coords_tdf.tagName.isin(ni_tdf.stimCathodeTag))
                            & (coords_tdf.eType == 'D')
        ]


        tdf_ni = ni_coords_tdf[['x','y','z']]



        r1111_coords_tdf =  coords_tdf[ coords_tdf.subject.isin(['R1111M'])
                          &
                          (coords_tdf.tagName.isin(['LPOG10','LPOG2','LPOG1','LPOG9'])
                           )
        ]


        tdf_r1111 = r1111_coords_tdf[['x','y','z']]

        # # snapping electrodes to the surface
        # neg_elec_locs = tdf_neg_filt.values
        # pulled_els, orig_els = pull_electrodes_to_surface(neg_elec_locs, max_distance=10.0)
        # neg_elec_locs = pulled_els + orig_els
        #
        # # artificial plane pts
        #
        # art_elecs = np.array([0.,0.,0.])
        # for i in range(-70,70,10):
        #     for j in range(-70,70,10):
        #         e = np.array([i*1.0,j*1.,-i-j*1.])
        #         art_elecs = np.vstack((art_elecs,e))
        #
        # art_elec_obj = Electrodes(shape='sphere')
        # art_elec_obj.set_electrodes_locations(loc_array=art_elecs)
        # art_elec_obj.set_electrodes_color(c=neg_significant_color)
        # w.add_display_object('art_elec_obj', art_elec_obj)



        # axial_slice = AxialSlice(fname='/Users/m/RAM_PLOTS_GIT/datasets/axial-mni-7.0.vtk')
        axial_slice = AxialSlice(fname='/Users/m/RAM_PLOTS_GIT/datasets/axial-tal-7.0.vtk')
        w.add_display_object('axial_slice',axial_slice)

        plane_points = axial_slice.get_plane_points()


        pr_ni_list = []
        for el in tdf_ni.values:
            pr_el,pr_dist = project_electrode_onto_plane(el,plane_points)
            if pr_dist<=10.0:
                pr_ni_list.append(pr_el)

        pr_elec_ni_obj = Electrodes(shape='sphere')
        pr_elec_ni_obj.set_electrodes_locations(loc_array=np.array(pr_ni_list))
        pr_elec_ni_obj.set_electrodes_color(c=non_significant_color)
        w.add_display_object('pr_elec_ni_obj', pr_elec_ni_obj)


        pr_neg_list = []
        for el in tdf_neg.values:
            pr_el,pr_dist = project_electrode_onto_plane(el,plane_points)
            if pr_dist<=10.0:
                pr_neg_list.append(pr_el)

        pr_elec_neg_obj = Electrodes(shape='sphere')
        pr_elec_neg_obj.set_electrodes_locations(loc_array=np.array(pr_neg_list))
        pr_elec_neg_obj.set_electrodes_color(c=neg_significant_color)
        w.add_display_object('pr_elec_neg_obj', pr_elec_neg_obj)



        pr_pos_list = []
        for el in tdf_pos.values:
            pr_el,pr_dist = project_electrode_onto_plane(el,plane_points)
            if pr_dist<=10.0:
                pr_pos_list.append(pr_el)

        pr_elec_pos_obj = Electrodes(shape='sphere')
        pr_elec_pos_obj .set_electrodes_locations(loc_array=np.array(pr_pos_list))
        pr_elec_pos_obj .set_electrodes_color(c=pos_significant_color)
        w.add_display_object('pr_elec_pos_obj', pr_elec_pos_obj )




        # # el=[18, 32, 21]
        # # pr_el,pr_dist = project_electrode_onto_plane(el,axial_slice.get_plane_points())
        # # # pr_elecs = np.array([pr_el])
        # # pr_elecs = np.vstack((el,pr_el))
        #
        #
        # pr_elec_obj = Electrodes(shape='sphere')
        # pr_elec_obj.set_electrodes_locations(loc_array=pr_elecs)
        # pr_elec_obj.set_electrodes_color(c=pos_significant_color)
        # w.add_display_object('pr_elec_obj', pr_elec_obj)

        w.display(cut_plane_on=False)

        # # neg_i_elec = Electrodes(shape='sphere')
        # # neg_i_elec.set_electrodes_locations(loc_array=neg_elec_locs)
        # # neg_i_elec.set_electrodes_color(c=neg_significant_color)
        # # w.add_display_object('neg_i_elec', neg_i_elec)
        #
        #
        #
        # # # axial_slice = AxialSlice(fname='/Users/m/RAM_PLOTS_GIT/datasets/axial-mni-7.0.vtk')
        # # axial_slice = AxialSlice(fname='/Users/m/RAM_PLOTS_GIT/datasets/axial-tal-7.0.vtk')
        # # w.add_display_object('axial_slice',axial_slice)
        #
        # a=np.array([0.,0.,0.])
        # b=np.array([1.,1.,-2.])
        # c=np.array([4.,2.,-6.])
        #
        # el=[18, 32, 21]
        # pr_el,pr_dist = project_electrode_onto_plane([18, 32, 21],[a,b,c])
        #
        # pr_elecs = np.vstack((el,pr_el))
        # # pr_elecs = np.vstack((pr_el,pr_el))
        #
        # pr_elec_obj = Electrodes(shape='sphere')
        # pr_elec_obj.set_electrodes_locations(loc_array=pr_elecs)
        # pr_elec_obj.set_electrodes_color(c=pos_significant_color)
        # w.add_display_object('pr_elec_obj', pr_elec_obj)
        #
        #
        #
        #
        # w.display(cut_plane_on=False)
        #
        #
        #
