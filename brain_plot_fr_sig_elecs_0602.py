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
    df = df [ (df.eType=='G') | (df.eType=='S')]

    n_elecs_tot_left = len(df[df.apply(lambda x: x['x']<0.0, axis=1)])
    n_elecs_tot_right = len(df[df.apply(lambda x: x['x']>0.0, axis=1)])

    print 'Number of surf and grid elecs in LH: ', n_elecs_tot_left
    print 'Number of surf and grid elecs in RH: ', n_elecs_tot_right
    
    mask = df['t']>2.0
    
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




    print



    lh = Hemisphere(hemi='l')
    lh.set_opacity(1.0)

    rh = Hemisphere(hemi='r')
    # rh.set_color(c=[1,0,0])
    rh.set_opacity(1.0)

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


    pr_elec_non_sig_obj = Electrodes(shape='sphere')
    pr_elec_non_sig_obj.set_electrodes_locations(loc_array=non_sig_elecs)
    pr_elec_non_sig_obj.set_electrodes_color(c=non_significant_color)
    w.add_display_object('pr_elec_non_sig_obj', pr_elec_non_sig_obj)


    pr_elec_sig_obj = Electrodes(shape='sphere')
    pr_elec_sig_obj .set_electrodes_locations(loc_array=sig_elecs)
    pr_elec_sig_obj .set_electrodes_color(c=significant_color)
    w.add_display_object('pr_elec_sig_obj', pr_elec_sig_obj )




    # if flip_elecs is not None:
    #     pr_elec_flip_obj = Electrodes(shape='sphere')
    #     pr_elec_flip_obj .set_electrodes_locations(loc_array=flip_elecs)
    #     pr_elec_flip_obj .set_electrodes_color(c=flipping_color)
    #     w.add_display_object('pr_elec_flip_obj', pr_elec_flip_obj )
    #



    w.display()
    #
    #
    #
    #
    #
    #
    #
