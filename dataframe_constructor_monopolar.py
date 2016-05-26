from os.path import *
import sys
sys.path.append('/Users/m/PTSA_NEW_GIT')
from ptsa.data.readers import TalReader,TalStimOnlyReader

mount_point = '/Volumes/rhino_root'

from brain_plot_utils import *

import pandas as pd
import numpy as np

# def extract_electrode_positions(tal_path, electrode_types=['D', 'G', 'S']):
#     from ptsa.data.readers import TalReader
#     tal_reader = TalReader(filename=tal_path)
#     tal_structs = tal_reader.read()
#
#     lh_selector = np.array(map(lambda loc: loc.upper().startswith('L'), tal_structs.tagName))
#     rh_selector = np.array(map(lambda loc: loc.upper().startswith('R'), tal_structs.tagName))
#
#     electrode_types_lower = map(lambda t: t.lower(), electrode_types)
#
#     electrode_type_selector = np.array(map(lambda eType: eType.lower() in electrode_types_lower, tal_structs.eType))
#
#     lh_data = tal_structs[['avgSurf','eType']]
#     rh_data = tal_structs[['avgSurf','eType']]
#
#     lh_data = lh_data[lh_selector & electrode_type_selector]
#     rh_data = rh_data[rh_selector & electrode_type_selector]
#
#     return lh_data,rh_data
#
# def append_to_combined(combined,*arrays):
#     tmp_array = None
#     for array in arrays:
#
#         if array is None: continue
#
#         if tmp_array is None:
#             if len(array):
#                 tmp_array = array
#         elif array is not None and len(array):
#             tmp_array = np.vstack(tmp_array,array)
#
#     if combined is None  and tmp_array is not None and len(tmp_array):
#         combined = tmp_array
#     elif tmp_array is not None and  len(tmp_array):
#         try:
#             combined = np.vstack((combined,tmp_array))
#         except:
#             print combined
#             print tmp_array
#     return combined

def get_elec_data_coords_array(hemi_data):
    dtype_avgSurf = [('x_snap', '<f8'), ('y_snap', '<f8'),('z_snap', '<f8')]

    if hemi_data is not None and len(hemi_data):
        tmp_array = np.array([((hemi_data.avgSurf.x_snap,hemi_data.avgSurf.y_snap,hemi_data.avgSurf.z_snap),hemi_data.eType[0],hemi_data.tagName[0])],
                         dtype=[('avgSurf', dtype_avgSurf),('eType','|S256'),('tagName','|S256')])

        return tmp_array
    else:
        return None



def get_tal_structs_row(subject,anode_tag,cathode_tag):

        # '/Users/m/data/eeg/R1111M/tal/R1111M_talLocs_database_bipol.mat'
        # tal_path = join(mount_point,'data/eeg/',subject,'tal',subject+'_talLocs_database_bipol.mat')
        tal_path = str(join(mount_point,'data/eeg/',subject,'tal',subject+'_talLocs_database_monopol.mat'))

        tal_reader = TalReader(filename=tal_path,struct_name='talStruct')

        tal_structs = tal_reader.read()

        # sel = tal_structs[np.where(tal_structs.tagName == anode_tag+'-'+cathode_tag)]
        sel = tal_structs[np.where((tal_structs.tagName == anode_tag)|(tal_structs.tagName == cathode_tag))]
        if not len(sel):
            sel = tal_structs[np.where((tal_structs.tagName == anode_tag)|(tal_structs.tagName == cathode_tag))]

        if not len(sel):

            tal_path = str(join(mount_point,'data/eeg/',subject,'tal',subject+'_talLocs_database_stimOnly.mat'))
            tal_reader = TalStimOnlyReader(filename=tal_path)
            tal_structs = tal_reader.read()

            sel = tal_structs[np.where((tal_structs.tagName == anode_tag)|(tal_structs.tagName == cathode_tag))]
            if not len(sel):
                sel = tal_structs[np.where((tal_structs.tagName == anode_tag)|(tal_structs.tagName == cathode_tag))]

        return sel

def construct_elec_dataframe(df):


    tal_structs = None
    subject = ''

    lh_selector = None
    rh_selector = None

    lh_data_combined = None
    rh_data_combined = None


    x = np.zeros(shape=(len(tdf['Subject'])),dtype=np.float)
    y = np.zeros(shape=(len(tdf['Subject'])),dtype=np.float)
    z = np.zeros(shape=(len(tdf['Subject'])),dtype=np.float)
    eType = np.zeros(shape=(len(tdf['Subject'])),dtype='|S256')


    monopol_elec_data = []

    for index, row in df.iterrows():

        if subject != row['Subject']:

            subject = row['Subject']
            print subject

        #     # '/Users/m/data/eeg/R1111M/tal/R1111M_talLocs_database_bipol.mat'
        #     tal_path = join(mount_point,'data/eeg/',subject,'tal',subject+'_talLocs_database_bipol.mat')
        #     tal_reader = TalReader(filename=tal_path)
        #     tal_structs = tal_reader.read()
        #
        # sel = tal_structs[np.where(tal_structs.tagName == row['stimAnodeTag']+'-'+row['stimCathodeTag'])]
        # if not len(sel):
        #     sel = tal_structs[np.where(tal_structs.tagName == row['stimCathodeTag']+'-'+row['stimAnodeTag'])]

        sel = get_tal_structs_row(subject=subject,anode_tag=row['stimAnodeTag'],cathode_tag=row['stimCathodeTag'])

        for s in sel:
            monopol_elec_data.append([subject,s.tagName,s.avgSurf.x,s.avgSurf.y,s.avgSurf.z,s.eType])


        # try:
        #     x[index] = sel[0].avgSurf.x_snap
        #     y[index] = sel[0].avgSurf.y_snap
        #     z[index] = sel[0].avgSurf.z_snap
        #     eType[index] = sel[0].eType
        #
        #     # df.x[index] = sel[0].avgSurf.x_snap
        #     # df.y[index] = sel[0].avgSurf.y_snap
        #     # df.z[index] = sel[0].avgSurf.z_snap
        #     # df.eType[index] = sel[0].eType
        # except IndexError:
        #     print row
        #
        # except AttributeError:
        #     print row
        #
        # df['x']=x
        # df['y']=y
        # df['z']=z
        # df['eType']=eType


    monopolar_df = pd.DataFrame(monopol_elec_data,columns=['subject','tagName','x','y','z','eType'])

    monopolar_df = monopolar_df.drop_duplicates(cols=['subject','tagName'])

    return monopolar_df



def extend_elec_dataframe(df):


    tal_structs = None
    subject = ''

    lh_selector = None
    rh_selector = None

    lh_data_combined = None
    rh_data_combined = None


    x = np.zeros(shape=(len(tdf['Subject'])),dtype=np.float)
    y = np.zeros(shape=(len(tdf['Subject'])),dtype=np.float)
    z = np.zeros(shape=(len(tdf['Subject'])),dtype=np.float)
    eType = np.zeros(shape=(len(tdf['Subject'])),dtype='|S256')


    monopol_elec_data = []

    for count, (index, row) in enumerate(df.iterrows()):
        # print count, index, row

        if subject != row['Subject']:

            subject = row['Subject']
            print subject


        sel = get_tal_structs_row(subject=subject,anode_tag=row['stimAnodeTag'],cathode_tag=row['stimCathodeTag'])

        for s in sel:
            monopol_elec_data.append([subject,s.tagName,s.avgSurf.x,s.avgSurf.y,s.avgSurf.z,s.eType])

        if len(sel):
            x[count] = sel[0].avgSurf.x
            y[count] = sel[0].avgSurf.y
            z[count] = sel[0].avgSurf.z
            eType[count] = sel[0].eType
        else:
            x[count] = np.nan
            y[count] = np.nan
            z[count] = np.nan
            eType[count] = ''


    df['x'] = x
    df['y'] = y
    df['z'] = z
    df['eType'] = eType

    return df
# # EXTENSION FO DATAFRAME
# ttest_table_df_filename = 'ttest_table_params.csv'
#
# tdf = pd.read_csv(ttest_table_df_filename)
#
# elec_coord_tdf = extend_elec_dataframe(tdf)
#
# print elec_coord_tdf
#
# # EXTENSION FO DATAFRAME

# # ORIGINAL CODE
# ttest_table_df_filename = 'ttest_table_params.csv'
#
# tdf = pd.read_csv(ttest_table_df_filename)
#
# elec_coord_tdf = construct_elec_dataframe(tdf)
#
# elec_coord_tdf.to_csv('coords_'+ttest_table_df_filename)
#
#
# print new_tdf
#
# new_tdf.to_csv('ttest_table_params_with_location.csv')





ttest_table_df_filename = 'ps_aggregator_significance_table_05_26'

tdf = pd.read_excel(ttest_table_df_filename+'.xlsx')

tdf.to_csv(ttest_table_df_filename+'.csv')


# elec_coord_tdf = construct_elec_dataframe(tdf)
#
# elec_coord_tdf.to_csv('coords_'+ttest_table_df_filename+'.csv')


# print new_tdf

# new_tdf.to_csv('ttest_table_params_with_location_latest.csv')

