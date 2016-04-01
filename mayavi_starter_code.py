import pandas as pd


ttest_table_df_filename = 'ttest_table_params.csv'

tdf = pd.DataFrame.from_csv(ttest_table_df_filename)
coords_tdf = pd.DataFrame.from_csv('coords_'+ttest_table_df_filename)

tdf.to_excel('ttest_table_params.xlsx')
coords_tdf.to_excel('coords_ttest_table_params.xlsx')




interesting_tdf = tdf[(tdf.p<=0.01) & (tdf.t>0) ]


interesting_coords_tdf =  coords_tdf[ coords_tdf.subject.isin(interesting_tdf.index)
                  &
                  (coords_tdf.tagName.isin(interesting_tdf.stimAnodeTag)
                   | coords_tdf.tagName.isin(interesting_tdf.stimCathodeTag))
]


# interesting_tdf = tdf[(tdf.p<0.01) & (tdf.t>0) ][['t','x','y','z','eType']]




tdf_pos = interesting_coords_tdf[['x','y','z']]




ni_tdf = tdf[(tdf.p>0.01) ]


ni_coords_tdf =  coords_tdf[ coords_tdf.subject.isin(ni_tdf.index)
                  &
                  (coords_tdf.tagName.isin(ni_tdf.stimAnodeTag)
                   | coords_tdf.tagName.isin(ni_tdf.stimCathodeTag))
]


tdf_ni = ni_coords_tdf[['x','y','z']]



r1111_coords_tdf =  coords_tdf[ coords_tdf.subject.isin(['R1111M'])
                  &
                  (coords_tdf.tagName.isin(['LPOG10','LPOG2','LPOG1','LPOG9'])
                   )
]


tdf_r1111 = r1111_coords_tdf[['x','y','z']]


print 'tdf_r1111=',tdf_r1111