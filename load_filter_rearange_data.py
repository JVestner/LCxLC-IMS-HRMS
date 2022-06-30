"""
Created on Mon Sep 10 14:03:08 2018

@author: Jochen Vestner

© Jochen Vestner 2019

"""

###### script to load, filter and rearange rawdata
import pandas as pd
import numpy as np
import pickle
import os
import time

def fun(x):
    return np.sum(x)

import base64
import datetime
import io
import dash_html_components as html
import pandas as pd



## load data
def loaddata(file, modtime):
    print('loading data... please wait...')
    t = time.time()

    #path = '/home/jochen/python/20180910_plotly_dash/LCxLCxIM'
    #os.chdir(path)
    #file = 'AJD_IMSDirect170720_06.pickle'
    #modtime = 0.58 # 28.2 sec = 0.47 min

    with open(file, 'rb') as handle:
        df = pd.read_pickle(handle)
    print('loaded... start processing... please  wait...')

    ## filter
    condi1 = [a.size != 0 for a in df['intensity array']]
    condi2 = df.function == 1
    condi3 = [type(a) != list for a in df['drift time']]
    condi = condi1 & condi2 & condi3
    df = df[condi]

    df.drop(['count', 'function', 'process','total ion current', 'scan'], axis = 1 , inplace=True)

    ## rearrange 2d indices
    idx1d = np.arange(0,df['scan start time'].max(),modtime)
    df['rt1d']  = np.nan
    df['rt2d']  = np.nan

    for i,idx in enumerate(idx1d):
        #condi = (idx-modtime <= df_summall.index) & (df_summall.index<= idx)
        condi = (idx <= df['scan start time']) & (df['scan start time'] <= idx + modtime)
        df.loc[condi, 'rt1d'] = idx
        df.loc[condi, 'rt2d'] = df[condi]['scan start time']-idx

    ## calculate tics


    df['tic'] = df['intensity array'].apply(fun)

    print('Done. This took: ' + str(round((time.time() - t)/60,1)) + ' min')
    return df
