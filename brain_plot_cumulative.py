import sys
from BrainGraphicsFrameWidget import BrainGraphicsFrameWidget
from brain_plot_utils import *
import pandas as pd

if __name__ == '__main__':
    sys.path.append('/Users/m/PTSA_NEW_GIT')

    # app = QtGui.QApplication(['QVTKRenderWindowInteractor'])

    w = BrainGraphicsFrameWidget()
    w.resize(1000, 1000)
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

    pos_significant_color = [255, 0, 0]
    neg_significant_color = [0, 0, 255]
    non_significant_color = [128, 128, 128]
    flipping_color = [0, 255, 0]

    ttest_table_df_filename = 'ttest_table_params.csv'

    tdf = pd.DataFrame.from_csv(ttest_table_df_filename)
    coords_tdf = pd.DataFrame.from_csv('coords_' + ttest_table_df_filename)

    # significant POS
    interesting_tdf = tdf[(tdf.p <= 0.01) & (tdf.t > 0) & (tdf.N > 5)]
    # interesting_tdf = tdf[(tdf.p <= 0.01) & (tdf.t > 0) ]


    interesting_coords_tdf = coords_tdf[coords_tdf.subject.isin(interesting_tdf.index)
                                        &
                                        (coords_tdf.tagName.isin(interesting_tdf.stimAnodeTag)
                                         | coords_tdf.tagName.isin(interesting_tdf.stimCathodeTag))
                                        # & (coords_tdf.eType == 'D')
                                        ]

    # interesting_tdf = tdf[(tdf.p<0.01) & (tdf.t>0) ][['t','x','y','z','eType']]




    tdf_pos = interesting_coords_tdf[['x', 'y', 'z']]

    # significant NEG
    neg_interesting_tdf = tdf[(tdf.p <= 0.01) & (tdf.t < 0.0) & (tdf.N > 5)]
    # interesting_tdf = tdf[(tdf.p <= 0.01) & (tdf.t > 0) ]


    neg_interesting_coords_tdf = coords_tdf[coords_tdf.subject.isin(neg_interesting_tdf.index)
                                            &
                                            (coords_tdf.tagName.isin(neg_interesting_tdf.stimAnodeTag)
                                             | coords_tdf.tagName.isin(neg_interesting_tdf.stimCathodeTag))
                                            # & (coords_tdf.eType == 'D')
                                            ]

    # interesting_tdf = tdf[(tdf.p<0.01) & (tdf.t>0) ][['t','x','y','z','eType']]




    tdf_neg = neg_interesting_coords_tdf[['x', 'y', 'z']]

    print 'negative df = ', tdf_neg
    print 'positive df = ', tdf_pos

    # removing electrodes that are flip between sig pos and sig neg

    tdf_neg_filt = tdf_neg[~tdf_neg.index.isin(tdf_pos.index)]
    tdf_pos_filt = tdf_pos[~tdf_pos.index.isin(tdf_neg.index)]

    tdf_flip = tdf_neg[tdf_neg.index.isin(tdf_pos.index)]

    # tdf_neg_filt = tdf_neg
    # tdf_pos_filt = tdf_pos


    print tdf_neg_filt
    print tdf_pos_filt

    ni_tdf = tdf[(tdf.p > 0.01)]

    ni_coords_tdf = coords_tdf[coords_tdf.subject.isin(ni_tdf.index)
                               &
                               (coords_tdf.tagName.isin(ni_tdf.stimAnodeTag)
                                | coords_tdf.tagName.isin(ni_tdf.stimCathodeTag))
                               & (coords_tdf.eType == 'D')
                               ]

    tdf_ni = ni_coords_tdf[['x', 'y', 'z']]

    r1111_coords_tdf = coords_tdf[coords_tdf.subject.isin(['R1111M'])
                                  &
                                  (coords_tdf.tagName.isin(['LPOG10', 'LPOG2', 'LPOG1', 'LPOG9'])
                                   )
                                  ]

    tdf_r1111 = r1111_coords_tdf[['x', 'y', 'z']]

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
    lh.set_opacity(1.3)

    rh = Hemisphere(hemi='r')
    # rh.set_color(c=[1,0,0])
    rh.set_opacity(1.3)

    w.add_display_object('lh', lh)
    w.add_display_object('rh', rh)

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
    ni_elec.set_electrodes_color(c=non_significant_color)
    # w.add_actor('depth_elec',depth_elec.get_actor())
    w.add_display_object('ni_elec', ni_elec)

    # significant positive elec
    i_elec = Electrodes(shape='sphere')
    # elec.set_electrodes_locations(loc_array=[[0,0,0]])
    i_elec.set_electrodes_locations(loc_array=tdf_pos_filt.values)
    i_elec.set_electrodes_color(c=pos_significant_color)
    # w.add_actor('depth_elec',depth_elec.get_actor())
    w.add_display_object('i_elec', i_elec)

    # # significant negative elec
    # neg_i_elec = Electrodes(shape='sphere')
    # # elec.set_electrodes_locations(loc_array=[[0,0,0]])
    # neg_i_elec.set_electrodes_locations(loc_array=tdf_neg_filt.values)
    # neg_i_elec.set_electrodes_color(c=neg_significant_color)
    # # w.add_actor('depth_elec',depth_elec.get_actor())
    # w.add_display_object('neg_i_elec', neg_i_elec)

    # # flipping elec
    # flip_i_elec = Electrodes(shape='sphere')
    # # elec.set_electrodes_locations(loc_array=[[0,0,0]])
    # flip_i_elec.set_electrodes_locations(loc_array=tdf_flip.values)
    # flip_i_elec.set_electrodes_color(c=flipping_color)
    # # w.add_actor('depth_elec',depth_elec.get_actor())
    # w.add_display_object('flip_i_elec', flip_i_elec)



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
