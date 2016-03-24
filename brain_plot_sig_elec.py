from os.path import *
import sys
sys.path.append('/Users/m/PTSA_NEW_GIT')
from ptsa.data.readers import TalReader

mount_point = '/Volumes/rhino_root'

from brain_plot_utils import *

import pandas as pd
import numpy as np

def extract_electrode_positions(tal_path, electrode_types=['D', 'G', 'S']):
    from ptsa.data.readers import TalReader
    tal_reader = TalReader(filename=tal_path)
    tal_structs = tal_reader.read()

    lh_selector = np.array(map(lambda loc: loc.upper().startswith('L'), tal_structs.tagName))
    rh_selector = np.array(map(lambda loc: loc.upper().startswith('R'), tal_structs.tagName))

    electrode_types_lower = map(lambda t: t.lower(), electrode_types)

    electrode_type_selector = np.array(map(lambda eType: eType.lower() in electrode_types_lower, tal_structs.eType))

    lh_data = tal_structs[['avgSurf','eType']]
    rh_data = tal_structs[['avgSurf','eType']]

    lh_data = lh_data[lh_selector & electrode_type_selector]
    rh_data = rh_data[rh_selector & electrode_type_selector]

    return lh_data,rh_data

def append_to_combined(combined,*arrays):
    tmp_array = None
    for array in arrays:

        if array is None: continue

        if tmp_array is None:
            if len(array):
                tmp_array = array
        elif array is not None and len(array):
            tmp_array = np.vstack(tmp_array,array)

    if combined is None  and tmp_array is not None and len(tmp_array):
        combined = tmp_array
    elif tmp_array is not None and  len(tmp_array):
        try:
            combined = np.vstack((combined,tmp_array))
        except:
            print combined
            print tmp_array
    return combined

def get_elec_data_coords_array(hemi_data):
    dtype_avgSurf = [('x_snap', '<f8'), ('y_snap', '<f8'),('z_snap', '<f8')]

    if hemi_data is not None and len(hemi_data):
        tmp_array = np.array([((hemi_data.avgSurf.x_snap,hemi_data.avgSurf.y_snap,hemi_data.avgSurf.z_snap),hemi_data.eType[0],hemi_data.tagName[0])],
                         dtype=[('avgSurf', dtype_avgSurf),('eType','|S256'),('tagName','|S256')])

        return tmp_array
    else:
        return None




def construct_significant_elec_info(df):


    tal_structs = None
    subject = ''

    lh_selector = None
    rh_selector = None

    lh_data_combined = None
    rh_data_combined = None



    for index, row in df.iterrows():

        if subject != row['Subject']:

            subject = row['Subject']

            # '/Users/m/data/eeg/R1111M/tal/R1111M_talLocs_database_bipol.mat'
            tal_path = join(mount_point,'data/eeg/',subject,'tal',subject+'_talLocs_database_bipol.mat')
            tal_reader = TalReader(filename=tal_path)
            tal_structs = tal_reader.read()

            lh_selector = np.array(map(lambda loc: loc.upper().startswith('L'), tal_structs.tagName))
            rh_selector = np.array(map(lambda loc: loc.upper().startswith('R'), tal_structs.tagName))


            lh_data = tal_structs[['avgSurf','eType','tagName']]
            rh_data = tal_structs[['avgSurf','eType','tagName']]

            lh_data = lh_data[lh_selector]
            rh_data = rh_data[rh_selector]

        lh_sel = get_elec_data_coords_array(lh_data[np.where(lh_data.tagName == row['stimAnodeTag']+'-'+row['stimCathodeTag'])])

        lh_sel_flip = get_elec_data_coords_array(lh_data[np.where(lh_data.tagName == row['stimCathodeTag']+'-'+row['stimAnodeTag'])])

        rh_sel = get_elec_data_coords_array(rh_data[np.where(rh_data.tagName == row['stimAnodeTag']+'-'+row['stimCathodeTag'])])

        rh_sel_flip = get_elec_data_coords_array(rh_data[np.where(rh_data.tagName == row['stimCathodeTag']+'-'+row['stimAnodeTag'])])




        lh_data_combined = append_to_combined(lh_data_combined,lh_sel,lh_sel_flip)
        rh_data_combined = append_to_combined(rh_data_combined,rh_sel,rh_sel_flip)

        # lh_sel_stack = vstack_arrays(lh_sel,lh_sel_flip)
        # rh_sel_stack = vstack_arrays(rh_sel,rh_sel_flip)
        #
        #
        # lh_tmp = np.vstack((lh_sel,lh_sel_flip))
        # rh_tmp = np.vstack((rh_sel,rh_sel_flip))
        #
        # if not lh_data_combined:
        #     lh_data_combined = lh_tmp
        # else:
        #     lh_data_combined = np.vstack((lh_data_combined,lh_tmp))
        #
        # if not rh_data_combined:
        #     rh_data_combined = rh_tmp
        # else:
        #     rh_data_combined = np.vstack((rh_data_combined,rh_tmp))



    print rh_data_combined
    print lh_data_combined

    return lh_data_combined, rh_data_combined



tdf = pd.read_csv('ttest_table.csv')

print tdf.Subject

sel_tdf = tdf[tdf.p<0.05]



sel_tdf = sel_tdf.sort_values(by=['Subject'], ascending=[True], inplace=False)
print sel_tdf



lh_data_combined, rh_data_combined = construct_significant_elec_info(df=sel_tdf)

electrode_types =['D','S','G']
# lh_elec_data, rh_elec_data = extract_electrode_positions(tal_path=tal_path, electrode_types=electrode_types)

# BrainPlotExample(lh_elec_data=lh_data_combined.view(np.recarray), rh_elec_data=rh_data_combined.view(np.recarray),electrode_types=electrode_types, filename='combined_electrodes.png')
BrainPlotExample(lh_elec_data=lh_data_combined.view(np.recarray), rh_elec_data=rh_data_combined.view(np.recarray),electrode_types=electrode_types)
