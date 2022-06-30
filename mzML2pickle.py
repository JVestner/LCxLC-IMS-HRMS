# -*- coding: utf-8 -*-
"""
Created on Tue Aug  1 15:16:05 2017

@author: Jochen Vestner

Convert mzMl to Pandas Dataframe and save as pickle

© Jochen Vestner 2019

"""

# created from 20170801_new_dataimport_faster.py



#%%
import time
import os
import pickle
import pandas as pd
import numpy as np
from pyteomics import mzml, auxiliary
import re


def mzML2pickle(file):


    #path = '/home/jochen/python/20170720_LC_IM_MS'
    #os.chdir(path)
    #file = 'AJD_IMSDirect170718_19b.mzML'
    #file = 'AJD_IMSDirect170718_19b_first1000scans.mzML'

    #with mzml.read(file) as reader:
    #     auxiliary.print_tree(next(reader))

    #with mzml.read(file) as reader:
    #     idx = [feat['index'] for feat in reader]

    print('Importing file: ' + file + ' ... Please wait ...' )
    #df= pd.DataFrame([], columns=['function', 'process', 'scan', 'count',  'scan start time',  'm/z array', 'intensity array', 'drift time', 'total ion current'])


    def dfmaker(a):
        if (a['index']/1000).is_integer() == True :
            print(a['index'])
        ids = a['id']
        function = int(re.findall(r'\d+', ids.split(' ')[0])[0])
        process =  int(re.findall(r'\d+', ids.split(' ')[1])[0])
        scan =  int(re.findall(r'\d+', ids.split(' ')[2])[0])
        counts = a['count']
        #idx = a['index']
        scantime = a['scanList']['scan'][0]['scan start time'].real
        intensities = a['intensity array']
        mzs = a['m/z array']

        if  'ion mobility drift time' in  a['scanList']['scan'][0].keys():
            drifttime = a['scanList']['scan'][0]['ion mobility drift time'].real
        else:
            drifttime = []

        if  'total ion current' in  a.keys():
            tic = a['total ion current']
        else:
            tic = []

        #df.loc[a['index']] = pd.Series({'function': function,'process': process, 'scan': scan, 'count' : counts,'scan start time' : scantime,  'm/z array' : mzs, 'intensity array' : intensities, 'drift time' : drifttime,  'total ion current': tic})
        s=pd.Series({'function': function,'process': process, 'scan': scan, 'count' : counts,'scan start time' : scantime,  'm/z array' : mzs, 'intensity array' : intensities, 'drift time' : drifttime,  'total ion current': tic})

        return s

    t1 = time.clock()

    #df=pd.concat(map(dfmaker, mzml.read(file)), axis = 1).transpose()
    with mzml.read(file) as reader:
        df=pd.concat(map(dfmaker, reader), axis = 1).transpose()

    t2 = time.clock()
    print('loading and conversion of data took: ' + str(round((t2 - t1) / 60)) + ' minutes')
    print('---------------------------------------------------')
    df.to_pickle(file[0:-4]+'pickle')
    t3 = time.clock()
    print('Saving as pickle took: ' + str(round((t3 - t2) / 60)) + ' minutes')
    print('---------------------------------------------------')
    print('Total time: ' + str(round((t3 - t1) / 60)) + ' minutes')


    #%%
    #with open('20170801_all_spectra_in_pd_Dataframe_new', 'rb') as handle:
    #    b = pickle.load(handle)
