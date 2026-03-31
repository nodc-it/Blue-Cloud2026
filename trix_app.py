import os
import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import dash
from dash import Dash, html, dcc, Input, Output, callback, dash_table
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cartopy.mpl.gridliner as gridliner
import matplotlib.ticker as mticker
import cartopy.mpl.ticker as cartopyticker
import cmocean
import xarray as xr
import netCDF4 as nc
from collections import OrderedDict
import ipywidgets as widgets
from IPython.display import display, HTML

# Load data - assuming 2003-2012 period is selected
base_dir = r"C:\Users\nreyessuarez\OneDrive - OGS\Documenti\GitHub\Blue-Cloud\MEI_VLab\DIVA_climatologies\2003-2012"

ds_DIN = xr.open_dataset(os.path.join(base_dir, 'Water_body_dissolved_inorganic_nitrogen_DIN_med_2003-2012_final_4Danl.nc'), decode_cf=True, chunks="auto")
ds_CHL = xr.open_dataset(os.path.join(base_dir, 'Water_body_chlorophyll-a_med_2003-2012_final_4Danl.nc'), decode_cf=True, chunks="auto")
ds_TP = xr.open_dataset(os.path.join(base_dir, 'Water_body_total_phosphorus_med_2003-2012_final_4Danl.nc'), decode_cf=True, chunks="auto")
ds_DO = xr.open_dataset(os.path.join(base_dir, 'Water_body_calculatedDOsaturation_med_2003-2012_final_4Danl.nc'), decode_cf=True, chunks="auto")

# Extract variables
CHLF = ds_CHL['Water body chlorophyll-a_L1']
DINF = ds_DIN['Water body dissolved inorganic nitrogen (DIN)_L1']
TPF = ds_TP['Water body total phosphorus_L1']
DOF = ds_DO['calculatedDOsaturation_L1']

# Convert units
TP = 30.97376 * TPF  # umol/l to mg/m3
DIN = 14.00672 * DINF  # umol/l to mg/m3
DO = abs(100 - DOF)
CHL = CHLF

# Calculate TRIX
TRIX = abs((np.log10(CHL * DIN * TP * DO) + 1.5) / 1.2)

# Load coordinates
df_coords = pd.read_csv(r"C:\Users\nreyessuarez\OneDrive - OGS\Documenti\GitHub\Blue-Cloud\MEI_VLab\DIVA_climatologies\12M_med.csv")

# TRIX categories
data = OrderedDict(
    [
        ("Conditions", ["Oligotrophic", "Oligotrophic", "Oligotrophic", "Eutrophic"]),
        ("TRIX units", ["< 4", "4 - 5", "5 - 6", "> 6"]),
        ("Trophic state", ["Elevated", "Good", "Mediocre", "Bad"]),
    ]
)

df_table = pd.DataFrame(
    OrderedDict([(name, col_data) for (name, col_data) in data.items()])
)

# Initialize Dash app
app = Dash(__name__)

# Layout
app.layout = html.Div([
    html.H1('TRIX Trophic State Index', style={'textAlign': 'center'}),
    html.Div([
        html.Div([
            html.Label('Select Season:'),
            dcc.Dropdown(
                id='season-dropdown',
                options=[
                    {'label': 'JFM (Jan-Mar)', 'value': 0},
                    {'label': 'AMJ (Apr-Jun)', 'value': 1},
                    {'label': 'JAS (Jul-Sep)', 'value': 2},
                    {'label': 'OND (Oct-Dec)', 'value': 3},
                ],
                value=0,
                clearable=False
            )
        ], style={'width': '48%', 'display': 'inline-block'}),
        html.Div([
            html.Label('Select Depth:'),
            dcc.Dropdown(
                id='depth-dropdown',
                options=[{'label': f'{depth} m', 'value': i} for i, depth in enumerate(TRIX.depth.values)],
                value=0,
                clearable=False
            )
        ], style={'width': '48%', 'display': 'inline-block', 'float': 'right'})
    ]),
    html.Div([
        dcc.Graph(id='trix-map', style={'height': '600px'})
    ]),
    html.Div([
        dash_table.DataTable(
            data=df_table.to_dict('records'),
            columns=[{'id': c, 'name': c} for c in df_table.columns],
            style_table={'width': '50%', 'margin': 'auto'},
            style_cell={'textAlign': 'center'}
        )
    ], style={'marginTop': '20px'})
])

@app.callback(
    Output('trix-map', 'figure'),
    [Input('season-dropdown', 'value'),
     Input('depth-dropdown', 'value')]
)
def update_map(season_idx, depth_idx):
    # Get TRIX data for selected season and depth
    trix_data = TRIX.isel(time=season_idx, depth=depth_idx).values

    # Flatten for plotting
    z_values = np.ravel(trix_data)
    lon_values, lat_values = np.meshgrid(TRIX.lon.values, TRIX.lat.values)
    lon_values = lon_values.ravel()
    lat_values = lat_values.ravel()

    # Round coordinates for merging
    df_coords_rounded = df_coords.copy()
    df_coords_rounded['X'] = df_coords_rounded['X'].round(2)
    df_coords_rounded['Y'] = df_coords_rounded['Y'].round(2)

    # Create meshgrid DataFrame
    meshgrid_df = pd.DataFrame({
        'lon': lon_values.round(2),
        'lat': lat_values.round(2),
        'z': z_values
    })

    # Merge with coordinates
    merged_df = pd.merge(df_coords_rounded, meshgrid_df, left_on=['X', 'Y'], right_on=['lon', 'lat'], how='left')

    # Handle NaN values
    merged_df['z'] = merged_df['z'].fillna(-999)

    # Create map
    fig = go.Figure()

    # Add scattermapbox for TRIX values
    fig.add_trace(go.Scattermapbox(
        lon=merged_df['X'],
        lat=merged_df['Y'],
        mode='markers',
        marker=dict(
            size=5,
            color=merged_df['z'],
            colorscale=[
                (0.00, "rgba(0,0,0,0)"),
                (0.14, "#5B2C6F"),
                (0.28, "#3498DB"),
                (0.42, "#1ABC9C"),
                (0.56, "#27AE60"),
                (0.70, "#F1C40F"),
                (0.84, "#E67E22"),
                (1.00, "#E74C3C")
            ],
            showscale=True,
            cmin=4,
            cmax=6,
            colorbar=dict(title="TRIX Value"),
            opacity=1
        ),
        text=[f'TRIX: {z:.2f}' if z != -999 else 'No data' for z in merged_df['z']],
        hoverinfo='text'
    ))

    # Update layout
    fig.update_layout(
        mapbox=dict(
            style="satellite",
            center={"lon": 15.22, "lat": 43.14},
            zoom=4
        ),
        title=f'TRIX Trophic State Index - Season {season_idx}, Depth {TRIX.depth.values[depth_idx]}m',
        margin={"r":0,"t":50,"l":0,"b":0}
    )

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)