#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 11 15:26:20 2018

@author: Jochen Vestner

Watch out! This version uses global variables!
The app should therefore only be used from a single user! Not in production!

© Jochen Vestner 2019
"""

import time

import os
import dash
from dash import dcc #import dash_core_components as dcc  # 220709 changed as installation wasn't working anymore
from dash import html # import dash_html_components as html # 220709 see above
from dash.dependencies import Input, Output, State#, Event
import glob
import numpy as np
import pandas as pd
#from functions_loading import parse_contents
#path = '/home/jochen/pyhton/20180917_lclcim_dash_app/app_final_withglobalvar'#/home/jochen/pyhton/2018091720180917_lclcim_dash_app'
#os.chdir(path)


from load_filter_rearange_data import loaddata
from functions_plotting import scatterown, ownbar
from mzML2pickle import mzML2pickle
import decimal

#df_original = pd.DataFrame([])
#global df_original
#/home/jochen/python/20180910_plotly_dash/LCxLCxIM
defaultpath = os.getcwd()#
defaultmodtime = 0.58


df_original = pd.DataFrame([])
previousmassrange = []


app = dash.Dash()

app.layout = html.Div([
    html.H1('LCxLCxIM Data Analysis'),

    html.Div([

        html.Div([
                dcc.Graph(
                    id='LCLCIM',
                    #figure=scatterown(x,y,z,zz,colorscale, xmin,xmax, ymin, ymax, zmin, zmax),
                    #style={'height': 500},
                )
        ],className="six columns"),


        html.Div([
                html.Div([
                        html.Div([
                                html.Div([dcc.Input(placeholder='Enter directory...', id='path-input',value = defaultpath, style = {'width': '98%'} )], className='eight columns'),
                                html.Button('change directory', id='button-directory', className='four columns'),
                                ], className = 'row'),

                        html.Div([
                                html.Div(dcc.Dropdown(id='mzML-selector'), className='eight columns'),
                                html.Button('convert mzML to pickle', id='button-convert', className='four columns')
                                ],className="row"),
                        html.Div([
                                html.Div(dcc.Dropdown(id='pickle-selector'), className='eight columns'),
                                html.Button('load into app', id='button-load', className='four columns')
                                ],className="row"),

                        html.Div([
                                html.Div([dcc.Input(placeholder='Enter modulation time to load data...', value = defaultmodtime, id='modulation-input',# value = 0.58,
                                                    type = 'number', step=0.1, style = {'width': '100%'})], className='eight columns'),
                                html.Div('Modulation time', style = {'display': 'inline-block',
                                                                    'text-align': 'center' ,
                                                                     'marginTop':'0.5%'
                                                                     },
                                        className='four columns'),
                                ], className = 'row'),

                        html.Div([
                                html.Button('----------------------------------------------- show / refresh 3D plot --------------------------------------------------------',
                                            id='button-refresh', style = {'width': '100%'})
                                ], className = 'row'),

                        html.Div([dcc.Graph(
                                id='massspec',
                                #animate=True,
                                #style={'height': 300},
                                ),]),

                        html.Div([
                                html.Div('Intensity min:', className='two columns'),
                                html.Div([dcc.Input(placeholder='', id='intens-min', type = 'number',
                                                    style = {'width': '90%'})], className='three columns'),
                                html.Div('Intensity max:', className='two columns'),
                                html.Div([dcc.Input(placeholder='', id='intens-max', type = 'number',
                                                    style = {'width': '90%'})], className='three columns'),
                                ],className="row"),

                        html.Div([
                                html.Div('1D RT min:', className='two columns'),
                                html.Div([dcc.Input(placeholder='x axis min', id='xmin-input', type = 'number',
                                                    style = {'width': '90%'}, step=1)], className='three columns'),
                                html.Div('2D RT max:', className='two columns'),
                                html.Div([dcc.Input(placeholder='x axis max', id='xmax-input',  type = 'number',
                                                    style = {'width': '90%'}, step=1)], className='three columns'),
                                ],className="row"),

                        html.Div([
                                html.Div('2D RT min:', className='two columns'),
                                html.Div([dcc.Input(placeholder='y axis min', id='ymin-input', type = 'number',
                                                    style = {'width': '90%'}, step=0.1)], className='three columns'),
                                html.Div('2D RT max:', className='two columns'),
                                html.Div([dcc.Input(placeholder='y axis max', id='ymax-input', type = 'number',
                                                    style = {'width': '90%'}, step=0.1)], className='three columns'),
                                ],className="row"),

                        html.Div([
                                html.Div('drift time min:', className='two columns'),
                                html.Div([dcc.Input(placeholder='z axis min', id='zmin-input', type = 'number',
                                                    style = {'width': '90%'}, step=0.1)], className='three columns'),
                                html.Div('drift time max:', className='two columns'),
                                html.Div([dcc.Input(placeholder='z axis max', id='zmax-input', type = 'number',
                                                    style = {'width': '90%'}, step=0.1)], className='three columns'),
                                ],className="row"),

                        html.Div([
                                html.Div('max MZ:', className='two columns'),
                                html.Div([dcc.Input(placeholder='max mz', id='maxmz-input', type = 'number', value = 2000,
                                                    style = {'width': '90%'}, step=1)], className='three columns'),
                                html.Div('mass range:', className='two columns'),
                                html.Div([dcc.Input(placeholder='', id='massrange-input', type = 'text', value = 'TIC',
                                                    style = {'width': '90%'})], className='three columns'),
                                ],className="row"),


                        ])
                    ],className="six columns")#,

    ],className="row"),

    html.Div(id='hidden-div', style={'display':'none'}),
    html.Div(id='hidden-div1', style={'display':'none'}),
    html.Div(id='hidden-div2', style={'display':'none'}),
])



@app.callback(
        Output('pickle-selector', 'options'),#Output('hidden-div', 'children'),
        [Input('button-directory', 'n_clicks')],
        [State('path-input', 'value')])
def update_pickles(n_clicks, value):
    if not value:
        value = os.getcwd()

    os.chdir(value)
    files = glob.glob("*.pickle")
    d = [{'label': i, 'value': i} for i in files]
    return d


@app.callback(
        Output('mzML-selector', 'options'),#Output('hidden-div', 'children'),
        [Input('button-directory', 'n_clicks')],
        [State('path-input', 'value')])
def update_mzMLs(n_clicks, value):
    if not value:
        value = os.getcwd()

    os.chdir(value)
    files = glob.glob("*.mzML")
    d = [{'label': i, 'value': i} for i in files]
    return d

#/home/jochen/python/20180910_plotly_dash/LCxLCxIM
#/home/jochen/python/20170720_LC_IM_MS/data_for_PAPER

@app.callback(
        Output('button-load', 'disabled'),
        [Input('modulation-input','value')])
def blockbutton(modtime):
    if not modtime:
        return True

    return False#{'disabled' : False}


@app.callback(
        Output('hidden-div', 'children'),#
        [Input('button-load', 'n_clicks') ],
        [State('pickle-selector', 'value'), State('modulation-input','value')],
        #[Event('button-load','click')]
        )
def load(click, file, modtime):
    global df_original

    if not file:
        #f = np.arange(0,5)
        #
        #global df_original
        df_original = pd.DataFrame([])

        return #df_original.to_json(date_format='iso', orient='split') #scatterown(f,f,f,f,colorscale,0,1,0,1,0,1)

    #modtime = 0.58
    #global df_original

    df_original = loaddata(file, modtime)

    return 'data loaded'#df_original.to_json(date_format='iso', orient='split')


@app.callback(
        Output('hidden-div1', 'children'),#
        [Input('button-convert', 'n_clicks') ],
        [State('mzML-selector', 'value')],
        #[Event('button-load','click')]
        )
def convert(click, file):
    if not file:
        return
    mzML2pickle(file)
    return

@app.callback(
        Output('intens-min', 'value'),
        [Input('hidden-div', 'children')])
def fun1(n_clicks):
    print('min callback')
    if df_original.empty:
        return 0
    return 0 #round(df_original['tic'].max()/10)

@app.callback(
        Output('intens-max', 'value'),
        [Input('hidden-div', 'children')])
def fun2(n_clicks):
    print('max callback')
    if df_original.empty:
        return 1
    return round(df_original['tic'].max())


@app.callback(
        Output('xmin-input', 'value'),
        [Input('hidden-div', 'children')])
def fun3(n_clicks):
    if df_original.empty:
        return 0
    return round(df_original['rt1d'].min(),1)

@app.callback(
        Output('xmax-input', 'value'),
        [Input('hidden-div', 'children')])
def fun4(n_clicks):
    if df_original.empty:
        return 1
    return round(df_original['rt1d'].max(),1)

@app.callback(
        Output('ymin-input', 'value'),
        [Input('hidden-div', 'children')])
def fun5(n_clicks):
    if df_original.empty:
        return 0
    return round(df_original['rt2d'].min(),1)

@app.callback(
        Output('ymax-input', 'value'),
        [Input('hidden-div', 'children')])
def fun6(n_clicks):
    if df_original.empty:
        return 1
    return round(df_original['rt2d'].max(),1)

@app.callback(
        Output('zmin-input', 'value'),
        [Input('hidden-div', 'children')])
def fun7(n_clicks):
    if df_original.empty:
        return 0
    return round(df_original['drift time'].min(),1)

@app.callback(
        Output('zmax-input', 'value'),
        [Input('hidden-div', 'children')])
def fun8(n_clicks):
    if df_original.empty:
        return 1
    return round(df_original['drift time'].max(),1)


#@app.callback(
#        Output('massrange-input', 'value'),
#        [Input('hidden-div', 'children')])
#def fun9(value):
#    return 'TIC'


@app.callback(
        Output('LCLCIM', 'figure'),#Output(component_id='LCLCIM', component_property='figure'), #Output('LCLCIM', 'figure'),#Output('hidden-div2', 'children'),#          #Output('LCLCIM', 'figure'),#
        [Input('button-refresh', 'n_clicks'),
         ],
        [State('intens-min', 'value'),
        State('intens-max', 'value'),
        State('xmin-input', 'value'),
        State('xmax-input', 'value'),
        State('ymin-input', 'value'),
        State('ymax-input', 'value'),
        State('zmin-input', 'value'),
        State('zmax-input', 'value'),
        State('massrange-input', 'value')],
        #[Event('button-refresh', 'click')]
        )#[Input('button-refresh', 'n_clicks')])
def refresh(n_clicks, thresh, maxthresh, xmin, xmax, ymin, ymax, zmin, zmax, massrange):
    print('scatterplot callback')
    colorscale =  'Rainbow'

    if df_original.empty:
        f = np.arange(1,5)
        #colorscale = [[0, 'rgb(0, 0, 0)']]
        color ='white'
        return scatterown(f,f,f,f,color, colorscale,xmin,xmax, ymin, ymax, zmin, zmax)

    if not thresh:
        thresh = df_original['tic'].max()/10 # df_original['tic'].min()#
    if not maxthresh:
        maxthresh = df_original['tic'].max()
    if not xmin:
        xmin = df_original['rt1d'].min()
    if not xmax:
        xmin = df_original['rt1d'].max()
    if not ymin:
        ymin = df_original['rt2d'].min()
    if not ymax:
        ymin = df_original['rt2d'].max()
    if not zmin:
        zmin = df_original['drift time'].min()
    if not zmax:
        zmin = df_original['drift time'].max()

    if massrange == 'TIC':

        x = df_original.loc[(df_original['tic'] >= thresh) ,'rt1d']#df_summall.index.values
        y = df_original.loc[(df_original['tic'] >= thresh) ,'rt2d']#df_summall['drift time'].values
        z = df_original.loc[(df_original['tic'] >= thresh) ,'drift time']#df_summall['TIC'].values
        zz = df_original.loc[(df_original['tic'] >= thresh) ,'tic']
        zz[zz > maxthresh] = maxthresh

        return scatterown(x,y,z,zz,zz,colorscale, xmin,xmax, ymin, ymax, zmin, zmax)

    else:
        global previousmassrange

        print(previousmassrange)

        #if not previousmassrange:
        if not previousmassrange or previousmassrange != massrange: # changed 20190719 bug report magriet

            previousmassrange = massrange

            print('... processing ... this takes a while ... ')
            t = time.time()

            masses = list(map(float, massrange.split()))

            def roundit(mass):
                return 5*pow(10,decimal.Decimal(str(mass)).as_tuple().exponent - 1)


            def fun2(x):
                return  np.array([(x >= mass - roundit(mass)) & (x <= mass + roundit(mass)) for mass in masses]).any(axis = 0)

            # this takes a while
            condi = df_original['m/z array'].apply(fun2)#.apply(fun3)
            df_original['eic'] = [j[i].sum() for i,j in zip(condi, df_original['intensity array'])]
            print('Done. This took: ' + str(round((time.time() - t)/60,1)) + ' min')
            #thresh = df_original['eic'].max()/10            # changed 20190719
            #maxthresh = df_original['eic'].max()            # changed 20190719

        x = df_original.loc[(df_original['eic'] > thresh) ,'rt1d']
        y = df_original.loc[(df_original['eic'] > thresh) ,'rt2d']
        z = df_original.loc[(df_original['eic'] > thresh) ,'drift time']
        zz = df_original.loc[(df_original['eic'] > thresh) ,'eic']
        zz[zz > maxthresh] = maxthresh


        print(previousmassrange)

        return scatterown(x,y,z,zz,zz,colorscale, xmin,xmax, ymin, ymax, zmin, zmax)


###################################################################

###################################################################
#289 441 577  729 865 1017 584 1153 652  728  720 796  864 1008




@app.callback(
    Output('massspec', 'figure'),
    [Input('LCLCIM', 'clickData')],
    [State('maxmz-input', 'value')]
    )
def display_click_data(clickData, mzmax):
    #mzmax = 2000
    global df_original
    #df = pd.read_json(jsonified_data, orient='split')

    if not clickData:
        newms = np.repeat(0,5)
        newintens = np.repeat(0,5)
        xclick = 0
        yclick = 0
        zclick = 0
        return ownbar(newms, newintens, mzmax, xclick, yclick, zclick )

    xclick = clickData['points'][0]['x']
    yclick = clickData['points'][0]['y']
    zclick = clickData['points'][0]['z']
    print('xyz coords:')
    print(xclick,yclick,zclick)
    condi1 = df_original['rt1d'] == xclick
    condi2 = df_original['rt2d'] == yclick
    condi3 = df_original['drift time'] == zclick
    condi = condi1 & condi2 & condi3
    newintens = df_original.loc[condi,'intensity array'].values[0]
    newms = df_original.loc[condi,'m/z array'].values[0]
    print(newms)
    print(newintens)

    return ownbar(newms, newintens, mzmax, xclick, yclick, zclick)#json.dumps(clickData, indent=2)



# CSS.

#app.css.append_css({
#        #'external_url': 'https://cdn.rawgit.com/plotly/dash-app-stylesheets/2d266c578d2a6e8850ebce48fdb52759b2aef506/stylesheet-oil-and-gas.css'
#        "external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"
#        })

# Loading screen CSS
#app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/brPBPO.css"})

#app.css.append_css({
#    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
#    })


if __name__ == '__main__':
    #app.run_server(host = '0.0.0.0', port = 5000, debug = False)#app.run_server(debug = True)
    app.run_server(host = '0.0.0.0', port = 8080, debug = False)#app.run_server(debug = True)
