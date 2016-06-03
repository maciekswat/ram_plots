import sys
from BrainGraphicsFrameWidget import BrainGraphicsFrameWidget
import pandas as pd
from brain_plot_utils import *

# to preprocess ps data use dataframe_constructor_monopolar.py  - make sure to set
# ttest_table_df_filename = ps_aggregator_significance_table_xxx.csv

def get_electrode_positions(df):

    elecs_df = df[['x','y','z']]

    elecs = np.array(elecs_df.values)


    sel = np.isnan(elecs)

    sel = ~np.apply_along_axis(np.any, 1, sel)

    elecs = elecs[sel,:]

    return elecs



if __name__=='__main__':
    sys.path.append('/Users/m/PTSA_NEW_GIT')


    w = BrainGraphicsFrameWidget()
    w.resize(1000,1000)


    significant_color = [255,0,0]
    neg_significant_color = [0, 0, 255]
    non_significant_color = [128, 128, 128]
    flipping_color = [0,255,0]

    df_filename = 'electrodes-R1001P-R1175N.csv'
    df = pd.read_csv(df_filename)

    # sig_elecs_df = df[np.abs(df['t'])>3.5]
    df = df [ (df.eType=='D') ]

    n_elecs_tot_left = len(df[df.apply(lambda x: x['x']<0.0, axis=1)])
    n_elecs_tot_right = len(df[df.apply(lambda x: x['x']>0.0, axis=1)])

    print 'Number of surf and grid elecs in LH: ', n_elecs_tot_left
    print 'Number of surf and grid elecs in RH: ', n_elecs_tot_right


    
    mask = df['t']>3.0
    
    sig_elecs_df = df[mask]
    non_sig_elecs_df = df[~mask]

    sig_elecs = get_electrode_positions(sig_elecs_df)
    non_sig_elecs = get_electrode_positions(non_sig_elecs_df)


    n_sig_elecs_left = len(sig_elecs_df[sig_elecs_df.apply(lambda x: x['x']<0.0, axis=1)])
    n_sig_elecs_right = len(sig_elecs_df[sig_elecs_df.apply(lambda x: x['x']>0.0, axis=1)])

    print 'LH SIG PERCENTAGE=', n_sig_elecs_left/float(n_elecs_tot_left) *100,'%'
    print 'RH SIG PERCENTAGE=', n_sig_elecs_right/float(n_elecs_tot_right) *100,'%'


    print 'Number of SIGNIFICANT surf and grid elecs in LH: ', n_sig_elecs_left
    print 'Number of SIGNIFICANT surf and grid elecs in RH: ', n_sig_elecs_right




    # axial_slice = AxialSlice(fname='/Users/m/RAM_PLOTS_GIT/datasets/axial-mni-7.0.vtk')
    axial_slice = AxialSlice(fname='/Users/m/RAM_PLOTS_GIT/datasets/axial-tal-13.0.vtk')
    w.add_display_object('axial_slice',axial_slice)

    plane_points = axial_slice.get_plane_points()
    max_distance = 30.0

    # pr_ni_list = []
    # for el in ns_elecs:
    #     pr_el,pr_dist = project_electrode_onto_plane(el,plane_points)
    #     if pr_dist<=max_distance:
    #         pr_ni_list.append(pr_el)
    #
    # pr_elec_ni_obj = Electrodes(shape='sphere')
    # pr_elec_ni_obj.set_electrodes_locations(loc_array=np.array(pr_ni_list))
    # pr_elec_ni_obj.set_electrodes_color(c=non_significant_color)
    # w.add_display_object('pr_elec_ni_obj', pr_elec_ni_obj)
    #


    pr_sig_list = []
    for el in sig_elecs:
        pr_el,pr_dist = project_electrode_onto_plane(el,plane_points)
        if pr_dist<=max_distance:
            pr_sig_list.append(pr_el)

    print 'pr_sig_list=',np.array(pr_sig_list)
    pr_elec_sig_obj = Electrodes(shape='sphere')
    pr_elec_sig_obj .set_electrodes_locations(loc_array=np.array(pr_sig_list))
    pr_elec_sig_obj .set_electrodes_color(c=significant_color)
    w.add_display_object('pr_elec_sig_obj', pr_elec_sig_obj )

    #

    # pr_flip_list = []
    # for el in flip_elecs:
    #     # pr_el=el
    #     # pr_flip_list.append(pr_el)
    #     pr_el,pr_dist = project_electrode_onto_plane(el,plane_points)
    #     print pr_dist
    #     if pr_dist<=max_distance:
    #         pr_flip_list.append(pr_el)
    #
    # print 'pr_flip_list=',np.array(pr_flip_list)
    # pr_elec_flip_obj = Electrodes(shape='sphere')
    # pr_elec_flip_obj.set_electrodes_locations(loc_array=np.array(pr_flip_list))
    # pr_elec_flip_obj.set_electrodes_color(c=flipping_color)
    # w.add_display_object('pr_elec_flip_obj', pr_elec_flip_obj )
    #



    w.display(cut_plane_on=False)



