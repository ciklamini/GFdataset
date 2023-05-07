'''

'''
import pandas as pd
import dash
import dash_vtk
from dash import html
import numpy as np
import vtk
from dash_vtk.utils import to_mesh_state

# geo_struct = 'Beam2D'
# geo_struct = 'Beam3D'
geo_struct = 'fibonacci'
# geo_struct = 'plane'

if      geo_struct == 'Beam2D':     vtk_type = 9
elif    geo_struct == 'Beam3D':     vtk_type = 12
elif    geo_struct == 'fibonacci':  vtk_type = 12
elif    geo_struct == 'plane':      vtk_type = 10

vtu_file = geo_struct + '.vtu'
    
vtk_file_path = vtu_file # without states

reader = vtk.vtkXMLUnstructuredGridReader()
reader.SetFileName(vtk_file_path)
reader.Update() 
mesh_state =to_mesh_state(reader.GetOutput(), field_to_keep= 'Logarithmic_strain_Min_Principal')
rng = [0,1]
cs_name = 'Greens'
app = dash.Dash(__name__)
server = app.server
vtk_view = dash_vtk.View(
    [
         dash_vtk.GeometryRepresentation(
            [
                dash_vtk.Mesh(state = mesh_state),       
                dash_vtk.PointCloudRepresentation(
                    # xyz=points_01,
                    # scalars=point_values,
                    # colorDataRange=[min_elevation, max_elevation],
                    property={"pointSize": 7, 
                              "symbol": 'circle', }, ),                        
             ],

            property={"edgeVisibility": True, "opacity": .9872},
            # colorMapPreset=cs_name,
            colorDataRange=rng
        )
    ],
    background=[1, 1, 1],
)

app.layout = html.Div(
    style={"height": "calc(100vh - 16px)"},
    children=[html.Div(vtk_view,
                       style={"height": "100%", "width": "100%", })],
    
)
if __name__ == "__main__":    app.run_server(debug=True)
