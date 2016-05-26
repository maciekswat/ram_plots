import sys
from BrainGraphicsFrameWidget import BrainGraphicsFrameWidget
import pandas as pd
from brain_plot_utils import *

# to preprocess ps data use dataframe_constructor_monopolar.py  - make sure to set
# ttest_table_df_filename = ps_aggregator_significance_table_xxx.csv

def get_electrode_positions(df):

    anodes_df = df[['xAvgSurf_anode', 'yAvgSurf_anode', 'zAvgSurf_anode']]

    anodes = np.array(anodes_df.values)

    cathodes_df = df[['xAvgSurf_cathode', 'yAvgSurf_cathode', 'zAvgSurf_cathode']]

    cathodes = np.array(cathodes_df.values)

    anodes_and_cathodes = np.vstack((anodes,cathodes))

    sel = np.isnan(anodes_and_cathodes)

    sel = ~np.apply_along_axis(np.any, 1, sel)

    anodes_and_cathodes = anodes_and_cathodes[sel,:]

    return anodes_and_cathodes



if __name__=='__main__':
    sys.path.append('/Users/m/PTSA_NEW_GIT')


    w = BrainGraphicsFrameWidget()
    w.resize(1000,1000)


    # tdf = pd.DataFrame.from_csv('ttest_table_params_with_location.csv')

    pos_significant_color = [255,0,0]
    neg_significant_color = [0, 0, 255]
    non_significant_color = [128, 128, 128]
    flipping_color = [0,255,0]

    pval_thresh=0.01
    N_min=5

    # ttest_table_df_filename = 'ttest_table_params.csv'

    # ttest_table_df_filename = 'ps_aggregator_significance_table.csv'
    ttest_table_df_filename = 'ps_aggregator_significance_table_05_26.csv'

    # tdf = pd.read_excel(ttest_table_df_filename)
    tdf = pd.DataFrame.from_csv(ttest_table_df_filename)
    # coords_tdf = pd.DataFrame.from_csv('coords_'+ttest_table_df_filename)


    # significant POS
    pos_tdf = tdf[(tdf.p<=pval_thresh) & (tdf.t>0) & (tdf.N>N_min)
                  & (tdf.eType == 'D')
    ][['Subject','stimAnodeTag','stimCathodeTag','xAvgSurf_anode', 'yAvgSurf_anode', 'zAvgSurf_anode','xAvgSurf_cathode', 'yAvgSurf_cathode', 'zAvgSurf_cathode']].drop_duplicates()

    pos_elecs = get_electrode_positions(pos_tdf)
    

    # significant NEG
    neg_tdf = tdf[(tdf.p<=pval_thresh) & (tdf.t<0) & (tdf.N>N_min)
                  & (tdf.eType == 'D')
    ][['Subject','stimAnodeTag','stimCathodeTag','xAvgSurf_anode', 'yAvgSurf_anode', 'zAvgSurf_anode','xAvgSurf_cathode', 'yAvgSurf_cathode', 'zAvgSurf_cathode']].drop_duplicates()

    neg_elecs = get_electrode_positions(neg_tdf)

    # non-significant
    ns_tdf = tdf[(tdf.p>pval_thresh) &  (tdf.N>N_min)
                  & (tdf.eType == 'D')
    ][['Subject','stimAnodeTag','stimCathodeTag','xAvgSurf_anode', 'yAvgSurf_anode', 'zAvgSurf_anode','xAvgSurf_cathode', 'yAvgSurf_cathode', 'zAvgSurf_cathode']].drop_duplicates()

    ns_elecs = get_electrode_positions(ns_tdf)


    # # non flipping
    neg_in_pos_sel = neg_tdf['stimAnodeTag'].isin(pos_tdf['stimAnodeTag']) \
                     & neg_tdf['stimCathodeTag'].isin(pos_tdf['stimCathodeTag']) \
                     & neg_tdf['Subject'].isin(pos_tdf['Subject'])


    pos_in_neg_sel = pos_tdf['stimAnodeTag'].isin(neg_tdf['stimAnodeTag']) \
                     & pos_tdf['stimCathodeTag'].isin(neg_tdf['stimCathodeTag']) \
                     & pos_tdf['Subject'].isin(neg_tdf['Subject'])

    flip_tdf = pd.merge(pos_tdf, neg_tdf, how='inner') #, on=['stimAnodeTag', 'stimCathodeTag','Subject'])


    subject_set = set(list(neg_tdf.Subject.unique()) + list(pos_tdf.Subject.unique()) + list(ns_tdf.Subject.unique()) + list(flip_tdf.Subject.unique()))
    print subject_set
    print 'Total '+str(len(subject_set))+' subjects'



    neg_tdf_filt = neg_tdf[~neg_in_pos_sel]
    pos_tdf_filt = pos_tdf[~pos_in_neg_sel]

    # flip_tdf = neg_tdf[neg_in_pos_sel]
    # # flip_tdf = flip_tdf.append(pos_tdf[pos_in_neg_sel])


    flip_elecs = get_electrode_positions(flip_tdf)

    # axial_slice = AxialSlice(fname='/Users/m/RAM_PLOTS_GIT/datasets/axial-mni-7.0.vtk')
    axial_slice = AxialSlice(fname='/Users/m/RAM_PLOTS_GIT/datasets/axial-tal-13.0.vtk')
    w.add_display_object('axial_slice',axial_slice)

    plane_points = axial_slice.get_plane_points()
    max_distance = 15.0

    pr_ni_list = []
    for el in ns_elecs:
        pr_el,pr_dist = project_electrode_onto_plane(el,plane_points)
        if pr_dist<=max_distance:
            pr_ni_list.append(pr_el)

    pr_elec_ni_obj = Electrodes(shape='sphere')
    pr_elec_ni_obj.set_electrodes_locations(loc_array=np.array(pr_ni_list))
    pr_elec_ni_obj.set_electrodes_color(c=non_significant_color)
    w.add_display_object('pr_elec_ni_obj', pr_elec_ni_obj)


    pr_neg_list = []
    for el in neg_elecs:
        pr_el,pr_dist = project_electrode_onto_plane(el,plane_points)
        if pr_dist<=max_distance:
            pr_neg_list.append(pr_el)

    pr_elec_neg_obj = Electrodes(shape='sphere')
    pr_elec_neg_obj.set_electrodes_locations(loc_array=np.array(pr_neg_list))
    pr_elec_neg_obj.set_electrodes_color(c=neg_significant_color)
    w.add_display_object('pr_elec_neg_obj', pr_elec_neg_obj)


    pr_pos_list = []
    for el in pos_elecs:
        pr_el,pr_dist = project_electrode_onto_plane(el,plane_points)
        if pr_dist<=max_distance:
            pr_pos_list.append(pr_el)

    print 'pr_pos_list=',np.array(pr_pos_list)
    pr_elec_pos_obj = Electrodes(shape='sphere')
    pr_elec_pos_obj .set_electrodes_locations(loc_array=np.array(pr_pos_list))
    pr_elec_pos_obj .set_electrodes_color(c=pos_significant_color)
    w.add_display_object('pr_elec_pos_obj', pr_elec_pos_obj )

    #

    pr_flip_list = []
    for el in flip_elecs:
        # pr_el=el
        # pr_flip_list.append(pr_el)
        pr_el,pr_dist = project_electrode_onto_plane(el,plane_points)
        print pr_dist
        if pr_dist<=max_distance:
            pr_flip_list.append(pr_el)

    print 'pr_flip_list=',np.array(pr_flip_list)
    pr_elec_flip_obj = Electrodes(shape='sphere')
    pr_elec_flip_obj.set_electrodes_locations(loc_array=np.array(pr_flip_list))
    pr_elec_flip_obj.set_electrodes_color(c=flipping_color)
    w.add_display_object('pr_elec_flip_obj', pr_elec_flip_obj )




    w.display(cut_plane_on=False)



