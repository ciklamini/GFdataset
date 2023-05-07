# -*- coding: utf-8 -*-

import networkx as nx
import dash
from dash import dcc  
from dash import html
import numpy as np
import plotly.graph_objects as go
import pandas as pd

H = nx.gnm_random_graph(30,15,4)
pos = nx.random_layout(H,dim=3)
xyz = [list(pos[i]) for i in pos]
flat_xyz =  [item for sublist in xyz for item in sublist]
pt = pd.DataFrame(xyz, columns = ['x', 'y', 'z'], dtype='float64')
pt[['u', 'v','w']] = pt.diff()
pt0 = pt.loc[1:,['u', 'v','w']]
pn = np.linalg.norm(pt.loc[1:,['u', 'v','w']].values,axis=1)
pt2 = pt.loc[1:,['u', 'v','w']].T / pn
pt3 = pt2.T
pt.loc[1:,['u', 'v','w']]  = pt3
shift_ = 2
app = dash.Dash(__name__) 
server = app.server
fig = go.Figure(data=go.Cone( 
                                u=pt.loc[1:, 'u'] , 
                                v=pt.loc[1:, 'v'] , 
                                w=pt.loc[1:, 'w'] 
                              ))  

fig.add_trace(
    go.Scatter3d(
        x=pt['x'],
        y=pt['y'],
        z=pt['z']
    ))
fig.add_trace(
    go.Scatter3d(
        x=pt['x'],
        y=pt['y'],
        z=pt['z'], 
        mode='lines',
    ))


app.layout = html.Div(children=[
    html.H1(children='Random Graph 060523'),
    dcc.Graph(id='',figure=fig),
    ],
        
    style={"width": "100%", "height": "1200px"
           }  
)
if __name__ == "__main__":    app.run_server(debug=True)
