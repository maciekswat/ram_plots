import sys
from BrainGraphicsFrameWidget import BrainGraphicsFrameWidget
import pandas as pd
from brain_plot_utils import *

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

    ttest_table_df_filename = 'ps_aggregator_significance_table.csv'

    # tdf = pd.read_excel(ttest_table_df_filename)
    tdf = pd.DataFrame.from_csv(ttest_table_df_filename)
    # coords_tdf = pd.DataFrame.from_csv('coords_'+ttest_table_df_filename)


    # significant POS
    pos_tdf = tdf[(tdf.p<=pval_thresh) & (tdf.t>0) & (tdf.N>N_min)
                  # & (tdf.eType == 'D')
    ]

    pos_elecs = get_electrode_positions(pos_tdf)
    

    # significant NEG
    neg_tdf = tdf[(tdf.p<=pval_thresh) & (tdf.t<0) & (tdf.N>N_min)
                  # & (tdf.eType == 'D')
    ]

    neg_elecs = get_electrode_positions(neg_tdf)

    # non-significant
    ns_tdf = tdf[(tdf.p>pval_thresh) &  (tdf.N>N_min)
                  # & (tdf.eType == 'D')
    ]

    ns_elecs = get_electrode_positions(ns_tdf)


    # # non flipping
    neg_in_pos_sel = neg_tdf['stimAnodeTag'].isin(pos_tdf['stimAnodeTag']) \
                     & neg_tdf['stimCathodeTag'].isin(pos_tdf['stimCathodeTag']) \
                     & neg_tdf['Subject'].isin(pos_tdf['Subject'])


    pos_in_neg_sel = pos_tdf['stimAnodeTag'].isin(neg_tdf['stimAnodeTag']) \
                     & pos_tdf['stimCathodeTag'].isin(neg_tdf['stimCathodeTag']) \
                     & pos_tdf['Subject'].isin(neg_tdf['Subject'])


    neg_tdf_filt = neg_tdf[~neg_in_pos_sel]
    pos_tdf_filt = pos_tdf[~pos_in_neg_sel]

    flip_tdf = neg_tdf[neg_in_pos_sel]
    flip_tdf = flip_tdf.append(pos_tdf[pos_in_neg_sel])

    flip_elecs = get_electrode_positions(flip_tdf)

    flip_elecs = np.array([[ 30.45000643, -38.83419803,  -9.9914955 ],
    [ 36.02000618, -38.5808654,  -10.00418042]],dtype=np.float)


    # # axial_slice = AxialSlice(fname='/Users/m/RAM_PLOTS_GIT/datasets/axial-mni-7.0.vtk')
    # axial_slice = AxialSlice(fname='/Users/m/RAM_PLOTS_GIT/datasets/axial-tal-10.0.vtk')
    # w.add_display_object('axial_slice',axial_slice)


    lh = Hemisphere(hemi='l')
    lh.set_opacity(0.1)

    rh = Hemisphere(hemi='r')
    # rh.set_color(c=[1,0,0])
    rh.set_opacity(0.1)

    w.add_display_object('lh',lh)
    w.add_display_object('rh',rh)


    # w.add_actor('lh',lh.get_actor())
    # w.add_actor('rh',rh.get_actor())

    w.add_bounds(lh.get_bounds())
    w.add_bounds(rh.get_bounds())





    # pr_elec_ni_obj = Electrodes(shape='sphere')
    # pr_elec_ni_obj.set_electrodes_locations(loc_array=ns_elecs)
    # pr_elec_ni_obj.set_electrodes_color(c=non_significant_color)
    # w.add_display_object('pr_elec_ni_obj', pr_elec_ni_obj)



    # pr_elec_neg_obj = Electrodes(shape='sphere')
    # pr_elec_neg_obj.set_electrodes_locations(loc_array=neg_elecs)
    # pr_elec_neg_obj.set_electrodes_color(c=neg_significant_color)
    # w.add_display_object('pr_elec_neg_obj', pr_elec_neg_obj)




    # pr_elec_pos_obj = Electrodes(shape='sphere')
    # pr_elec_pos_obj .set_electrodes_locations(loc_array=pos_elecs)
    # pr_elec_pos_obj .set_electrodes_color(c=pos_significant_color)
    # w.add_display_object('pr_elec_pos_obj', pr_elec_pos_obj )





    pr_elec_flip_obj = Electrodes(shape='sphere')
    pr_elec_flip_obj .set_electrodes_locations(loc_array=flip_elecs)
    pr_elec_flip_obj .set_electrodes_color(c=flipping_color)
    w.add_display_object('pr_elec_flip_obj', pr_elec_flip_obj )




    w.display()







