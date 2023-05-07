'''
meshstate s kombinaci 
points 

'''
import pandas as pd
import dash
import dash_vtk
from dash import html
import numpy as np

# geo_struct = 'Beam2D'
# geo_struct = 'Beam3D'
geo_struct = 'fibonacci'
# geo_struct = 'plane'

if      geo_struct == 'Beam2D':     vtk_type = 9
elif    geo_struct == 'Beam3D':     vtk_type = 12
elif    geo_struct == 'fibonacci':  vtk_type = 12
elif    geo_struct == 'plane':      vtk_type = 10

# https://kitware.github.io/vtk-examples/site/VTKBook/08Chapter8/
# https://kitware.github.io/vtk-examples/site/VTKBook/05Chapter5/
vtu_file = geo_struct + '.vtu'

nodes = pd.read_csv('nodes_'+geo_struct+'.csv')
nodes = nodes[['X', 'Y', 'Z']]
xyz = list(nodes.values)
points_01= [item for sublist in xyz for item in sublist]
point_values =  [item for sublist in np.random.rand(len(xyz),1).tolist() for item in sublist]
# %%
elements = pd.read_csv('elements_'+geo_struct+'.csv')
elements = elements.loc[:, elements.columns != 'ID']
elements = elements -min(elements.min().values)
elements['count']=elements.shape[1]
elements['type']=vtk_type
df_offset = elements['count']
del elements['count']
df_offset = df_offset.cumsum()
df_type = elements['type']
del elements['type']
# elements['count']=10
# %%
l1 = '<VTKFile type="UnstructuredGrid" version="0.1" byte_order="LittleEndian"> \n'
l2 = '<UnstructuredGrid> \n'
l3 = '<Piece NumberOfPoints="' + str(len(nodes)) + '" NumberOfCells="'+ str(len(elements)) +'"> \n'
l4 = '<Points> \n'
l5 = '<DataArray type="Float64" NumberOfComponents="3" format="ascii"> \n'
l6 =  nodes.to_string(header=False, index=False) 
l7 = '\n</DataArray> \n'
l8 = '</Points> \n'
l81 = '<PointData Tensors="" Vectors="" Scalars="">'
l82 = '<DataArray type="Float32" Name="Logarithmic_strain_Min_Principal" format="ascii">'
l83 = pd.DataFrame(point_values).to_string(header=False, index=False)
l84 = '</DataArray>'
l85 = '</PointData>'
l9 = '<Cells> \n'
l10 = '<DataArray type="Int32" Name="connectivity" format="ascii"> \n'
l11 =  elements.to_string(header=False, index=False) 
l11a = '\n</DataArray>\n'
l12 = '\n<DataArray type="Int32" Name="offsets" format="ascii">\n'
l13 = df_offset.to_string(header=False, index=False)
l14 = '\n</DataArray>\n'
l15 = '<DataArray type="UInt8" Name="types" format="ascii">\n'
l16 = df_type.to_string(header=False, index=False) 
l17 ='\n</DataArray>\n'
l18 ='</Cells>\n'
l19 ='</Piece>\n'
l20 ='</UnstructuredGrid>\n'
l21 ='</VTKFile>\n'

lines = [l1, l2,l3, l4, l5, l6, l7, l8,
         l81,l82,l83,l84, l85,         
         l9, l10, l11,l11a,
         l12, l13, l14, l15, l16,l17,l18,l19,l20,l21]
with open(vtu_file, 'w') as f:
    
    f.writelines(lines)
    
vtk_file_path = vtu_file # without states
import vtk
from dash_vtk.utils import to_mesh_state
reader = vtk.vtkXMLUnstructuredGridReader()
reader.SetFileName(vtk_file_path)
reader.Update() 
# mesh_state =to_mesh_state(reader.GetOutput(), )
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
                    xyz=points_01,
                    scalars=point_values,
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
