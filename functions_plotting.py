#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 10 14:03:08 2018

@author: Jochen Vestner

© Jochen Vestner 2019

"""



import numpy as np
import plotly.graph_objs as go



def scatterown(x,y,z,zz, color, colorscale, xmin, xmax, ymin, ymax, zmin, zmax):
    return {'data': [go.Scatter3d(
                            x=x,
                            y=y,
                            z=z,
                            #text = hl,
                            hoverinfo = ['all'],
                            mode='markers',
                            marker=dict(
                                color= color,#'white',#zz,
                                colorscale = colorscale,#  'Viridis',# ["#FFE1A1", "#683531"],
                                showscale = True,
                                size= zz/zz.min()*1,
                                 #    showscale = True,
                                line=dict(
                                    #color= zz,# 'transparent',#zz,#'rgba(217, 217, 217, 0.14)',
                                    width=0#0.5
                                    ),
                                #opacity=0.8
                                ),
                            opacity=0.8

                            #)
                        )],
            'layout':  go.Layout(
                            margin=dict(
                                l=0,
                                r=0,
                                b=0,
                                t=0
                            ),
                            height= 800,
                            scene = dict(
                                xaxis = dict(title='1D RT [min]', range=[xmin, xmax]),
                                yaxis = dict(title='2D RT [min]',range=[ymin, ymax]),
                                zaxis = dict(title='drift time [ms]',range=[zmin, zmax])
                                ),

                            )#{
                     #'height': 800,
                     #'xaxis': dict(range=[xmin, xmax], title='1D RT [min]'),
                     #'yaxis': dict(range=[ymin, ymax], title='2D RT [min]'),
                     #'zaxis': dict(range=[zmin, zmax], title='drift time [ms]'),
                      #}
            }



def make_annotation_item(x, y):
    return dict(x=x, y=y,
                xref='x', yref='y',
                #xref='paper', yref='paper',
                font=dict(color='black'),
                xanchor='left',
                yanchor='top',
                text=str(x),
                showarrow=False)



def ownbar(newms, newintens, maxmz, xclick, yclick, zclick):
    #vertical lines for massspec 'bars'
    shapes = list()
    for i,j in zip(newms, newintens):
        shapes.append({'type': 'line',
                       'xref': 'x',
                       'yref': 'y',
                       'x0': i,
                       'y0': 0,
                       'x1': i,
                       'y1': j,
                       'line' : {'color': 'grey'}
                       })

    #ANNOTATIONS = [make_annotation_item(x=newms[0], y=newintens[0])]
    ANNOTATIONS = [make_annotation_item(x=round(newms[i],5), y=newintens[i]) for i in range(len(newms)) ]

    #return {'data' : [go.Bar(
    return {'data' : [go.Scatter(
                        x = newms,
                        y = newintens,
                        mode = 'markers',
                        marker = dict(
                                symbol = 'square',
                                color = 'grey'
                                ),

                        ),
                    #go.Bar(
                    #    x = newms,
                    #    y = newintens,
                    #    marker = dict(
                    #            color = 'grey'
                    #            ),
                    #    #width= 0.5
                    #    )
                    ],
                 'layout': {
                    'title': '1D RT: ' + str(round(xclick,2))+ 'min' + '      2D RT: ' + str(round(yclick,2)) + 'min' + '      drift time: ' + str(round(zclick,2)) +'ms',
                     'xaxis': dict(range=[0, maxmz]),
                     'annotations': ANNOTATIONS,
                     'shapes': shapes
                   }
            }
