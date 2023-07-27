'''
name: MCGReadRemcomPaths.py
author: Artan Salihu
version: 1.0
status: development
contact: artan.salihuATtuwien.ac.at
website: https://www.artansalihu.com, https://mcg-deep-wrt.netlify.app/deep-wrt/utilities/
date: 2022-09-10
license: MIT
dependencies: pandas, sqlite3, numpy, json, codec, os, glob
description: This tool reads the path information from a sqlite database file obtained from the ray-tracing simulation of Remcom Wireless Insite (WI) when using X3D model. It returns a dictionary of the paths. The dictionary can be saved into a json file. The json file can be used in Matlab.
Usage:
1. Install the dependencies.
2. Run the script.
3. Change the parameters in the main function.
4. Run the main function.
5. The results are saved into a json file.

You can also import the function get_queries_paths_remcom into your own script and use it as follows: 
from MCGReadRemcomPaths import get_queries_paths_remcom
get_queries_paths_remcom(sqlite_db_path_file_name, file_path_json, num_paths=0, save=True)

Parameters:
sqlite_db_path_file_name (str): The path to the sqlite database file.
file_path_json (str): The path to the json file.
num_paths (int):  Select only top-num_paths. If num_paths=0, selects all the paths.

Returns:
dictionary: A dictionary of the paths. The dictionary can be saved into a json file.

In case of multiple files, you can use the following script:
import os
import glob
import json
from MCGReadRemcomPaths import get_queries_paths_remcom_multiple(files, files_json, num_paths=0, save=True)

In case of reading only Power (p2m) files, you can use the following script:


'''

import sqlite3
import pandas as pd
import codecs, json 
import numpy as np
import os
import glob

def get_queries_paths_remcom(sqlite_db_path_file_name, file_path_json, num_paths=0, save=True):
  """Get the queried results.
  num_paths (int):  Select only top-num_paths. If num_paths=0, selects all the paths.
  save (bool): If true, then it saves into a json file. Note that json file is not very well serialized for use in matlab structures.
              If false, then this returns a dictionary only.
  """

  # sqlite db file
  #sqlite_db_path_file_name = "VCS_WI_Project_01.Case2_4x2_X3D.sqlite"

  # # Be sure to close the connection
  # con.close()
  table1 = 'channel'
  table2 = 'path'
  table3 = 'path_utd'
  table4 = 'rx'
  table5 = 'tx'
  t1_q1 = 'channel_id'
  t1_q2 = 'tx_id'
  t1_q3 = 'rx_id'
  t2_q1 = 'path_id'
  t2_q2 = 'foliage_distance'
  t3_q1 = 'tx_sub_antenna'
  t3_q2 = 'received_power'
  t3_q3 = 'time_of_arrival'
  t3_q4 = 'departure_phi'
  t3_q5 = 'departure_theta'
  t3_q6 = 'arrival_phi'
  t3_q7 = 'arrival_theta'
  t3_q8 = 'freespace_path_loss'
  t3_q9 = 'freespace_path_loss_woa'
  t3_q10 = 'cir_phs'
  t4_q1 = 'x'
  t4_q2 = 'y'
  t4_q3 = 'z'
  t5_q1 = 'x'
  t5_q2 = 'y'
  t5_q3 = 'z'
  t1_forKey1 = 'channel_id'
  t1_forKey2 = 'rx_id'
  t1_forKey3 = 'tx_id'
  t2_forKey1 = 'channel_id'
  t2_forKey2 = 'path_id'
  t3_forKey1 = 'path_id'
  t4_forKey1 = 'rx_id'
  t5_forKey1 = 'tx_id'

  sql_query_request = (f'SELECT {table1}.{t1_q1}, {table1}.{t1_q2} as bs_id, {table1}.{t1_q3} as ue_id,'
                        f'{table2}.{t2_q1}, '
                        f'{table3}.{t3_q1} as bs_sub_antenna, {table3}.{t3_q2}, {table3}.{t3_q3}, {table3}.{t3_q4}, {table3}.{t3_q5}, {table3}.{t3_q6}, {table3}.{t3_q7}, {table3}.{t3_q8}, {table3}.{t3_q9}, {table3}.{t3_q10}, '
                        f'{table4}.{t4_q1} as ue_x, {table4}.{t4_q2} as ue_y, {table4}.{t4_q3} as ue_z, '
                        f'{table5}.{t5_q1} as bs_x, {table5}.{t5_q2} bs_y, {table5}.{t5_q3} bs_z '
                        f'FROM {table1} '
                        f'INNER JOIN {table2} '
                        f'ON {table1}.{t1_forKey1} = {table2}.{t2_forKey1} '
                        f'INNER JOIN {table3} '
                        f'ON {table2}.{t2_forKey2} = {table3}.{t3_forKey1} '
                        f'INNER JOIN {table4} '
                        f'ON {table1}.{t1_forKey2} = {table4}.{t4_forKey1} '
                        f'INNER JOIN {table5} '
                        f'ON {table1}.{t1_forKey3} = {table5}.{t5_forKey1} '
                        )

  print(sql_query_request)
  #f'WHERE {table3}.{t3_forKey1}<100 OR {table3}.{t3_forKey1} = 750 OR {table3}.{t3_forKey1} = 251'

  # Get the sqlite query results. Put into a DataFrame
  con = sqlite3.connect(sqlite_db_path_file_name)

  df = pd.read_sql_query(sql_query_request, con)

  con.close()

  # Inject a sequence column to count the number of paths for each antenna element between a base station and a user location.
  df['sequence']=df.groupby(['channel_id','bs_id','ue_id','bs_sub_antenna']).cumcount()

  if save==True:
    # Now filter the number of paths
    if num_paths>0:
      mask = (df['sequence'] < num_paths)
      df = df.loc[mask]

    cols_to_save = []
    for col in df.columns:
      if ((col!='tx_id') and (col!='rx_id')): # choose those not interested to get.
        cols_to_save.append(col)

    # Create a dictionary 
    dict2 = df.groupby(['ue_id','bs_id','bs_sub_antenna'])[cols_to_save].apply(lambda x: x.set_index('sequence').to_dict(orient='index')).to_dict()

    # Convert to list to save in json
    result = dict2.items()  
    data = list(result)
  
    # Convert list to an array just in case
    numpyArray = np.array(data, dtype=object)


    json.dump(data, codecs.open(file_path_json, 'w', encoding='utf-8'), 
          separators=(',', ':'), 
          sort_keys=False, 
          indent=4)
    
    return dict2

  return df

# For multiple sqlite files and output multiple json files
def get_queries_paths_remcom_multiple(sqlite_db_path_file_name_list, file_path_json_list, num_paths=1, save=True):
  '''
  Arguments:
    sqlite_db_path_file_name_list: list of sqlite db file names
    file_path_json_list: list of json file names
    num_paths: number of paths to get
    save: save to json file or not

    Returns:
    dict2: dictionary of the paths
  '''
  for i in range(len(sqlite_db_path_file_name_list)):
    get_queries_paths_remcom(sqlite_db_path_file_name=sqlite_db_path_file_name_list[i]+'.sqlite', file_path_json=sqlite_db_path_file_name_list[i]+'.json', num_paths=num_paths, save=save)


# To read p2m files only for the Received Power
def read_p2m_power(file_list):
    '''
    This function reads the p2m files and returns a dictionary of the dataframes (for the Power only). Check the p2m file format to see the columns.
    Arguments:
        file_list: list of p2m file names
    Returns:
        data_dict: dictionary of the dataframes
    '''
    data_dict = {}
    for file in file_list:
        parts = file.split('.')
        key = '.'.join(parts[1:-1])  # Include only the second and third parts of the file name (e.g. power.t001_15.r014
        df = pd.read_csv(file+'.p2m', delimiter=' ', skiprows=3, usecols=[0, 5], names=['ID', 'Power'])
        data_dict[key] = df
    return data_dict

if __name__ == '__main__':
    
    #1. Case 1 - Single sqlite file and single json file
    get_queries_paths_remcom(sqlite_db_path_file_name="RIS_Remcom_Le.RIS_Remcom_Le_Zero.sqlite", file_path_json='test.json', num_paths=1, save=True)

    #2. Case 2 - Multiple sqlite files and multiple json files
    # # Define the list of sqlite db file names. Json file names will be derived from the sqlite db file names (without .sqlite part).
    # sqlite_db_path_file_name_list = [r'./RIS_Remcom_Le_Zero/RIS_Remcom_Le.RIS_Remcom_Le_Zero', r'./RIS_Remcom_Le_Zero 2/RIS_Remcom_Le_ARTAN.RIS_Remcom_Le_Zero 2']

    # get_queries_paths_remcom_multiple(sqlite_db_path_file_name_list=sqlite_db_path_file_name_list, file_path_json_list=sqlite_db_path_file_name_list, num_paths=1, save=True)

    #3. Case 3 - Read p2m files for the Received Power
    # # Define the list of p2m file names.
    # file_list = [r'./RIS_Remcom_Le_Zero/RIS_Remcom_Le.power.t001_15.r014', r'./RIS_Remcom_Le_Zero 2/RIS_Remcom_Le_ARTAN.power.t001_15.r014']

    # data_dict = read_p2m_power(file_list=file_list)

    # print(data_dict)
    # import matplotlib.pyplot as plt

    # for file, df in data_dict.items():
    #   plt.plot(df['ID'], df['Power'], label=file)
      
    # plt.xlabel('ID')
    # plt.ylabel('Power (dBm)')
    # plt.grid()
    # plt.tight_layout()
    # plt.legend()
    # plt.rc('text', usetex=True)
    # plt.rc('font', family='serif', size=12)
    # # Save the figure to a folder named Results. If the folder does not exist, it will be created.
    # if not os.path.exists('Results'):
    #     os.makedirs('Results')
    # plt.savefig('Results/Power.png', dpi=300)
    # plt.show()

    