import sys
from BrainGraphicsFrameWidget import BrainGraphicsFrameWidget

if __name__=='__main__':
        sys.path.append('/Users/m/PTSA_NEW_GIT')

        # app = QtGui.QApplication(['QVTKRenderWindowInteractor'])

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




        lh = Hemisphere(hemi='l')
        lh.set_opacity(1.3)

        rh = Hemisphere(hemi='r')
        # rh.set_color(c=[1,0,0])
        rh.set_opacity(1.3)
        #
        # w.add_display_object('lh',lh)
        # w.add_display_object('rh',rh)


        # w.add_actor('lh',lh.get_actor())
        # w.add_actor('rh',rh.get_actor())
        #
        w.add_bounds(lh.get_bounds())
        w.add_bounds(rh.get_bounds())





        axial_slice = AxialSlice(fname='/Users/m/RAM_PLOTS_GIT/datasets/axial-mni-7.0.vtk')
        w.add_display_object('axial_slice',axial_slice)





        w.display(cut_plane_on=False)



