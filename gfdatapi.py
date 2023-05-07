'''
meshstate s kombinaci 
points 

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

geo_struct_b2 = 'Beam2D.vtu'
geo_struct_b3 = 'Beam3D.vtu'
geo_struct_fs = 'fibonacci.vtu'
geo_struct_pl = 'plane.vtu'

app = dash.Dash(__name__)
server = app.server
def defVTKfile(VTU_FILE:str):
    vtk_file_path = VTU_FILE # without states

    reader = vtk.vtkXMLUnstructuredGridReader()
    reader.SetFileName(vtk_file_path)
    reader.Update() 
    mesh_state =to_mesh_state(reader.GetOutput(), field_to_keep= 'Logarithmic_strain_Min_Principal')
    rng = [0,1]
    cs_name = 'Greens'
    
    vtk_view = dash_vtk.View(
        [dash_vtk.GeometryRepresentation(
            [
                    dash_vtk.Mesh(state = mesh_state),       
                    dash_vtk.PointCloudRepresentation(
                        property={"pointSize": 7, 
                                  "symbol": 'circle', }, ),                        
                 ],
    
                property={"edgeVisibility": True, "opacity": .9872},
                colorDataRange=rng
            )
        ],
        background=[1, 1, 1],
    )
    return vtk_view
vtk_view_b2 = defVTKfile(geo_struct_b2)
vtk_view_b3 = defVTKfile(geo_struct_b3)
vtk_view_fs = defVTKfile(geo_struct_fs)
vtk_view_pl = defVTKfile(geo_struct_pl)
app.layout = html.Div(
    style={"height": "calc(100vh - 16px)"},
    children=[html.Div(vtk_view_b2, style={"height": "100%", "width": "100%", }),
              html.Div(vtk_view_b3, style={"height": "100%", "width": "100%", }),
              html.Div(vtk_view_fs, style={"height": "100%", "width": "100%", }),
              html.Div(vtk_view_pl, style={"height": "100%", "width": "100%", })],
    
)
if __name__ == "__main__":    app.run_server(debug=True)
