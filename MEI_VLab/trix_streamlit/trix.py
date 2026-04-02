# -*- coding: utf-8 -*-
'''

pip install cmocean
pip install plotly
pip install netCDF4


 -- Start STREAMLIT server --
 
cd my/path/to/streamlit/trix_streamlit
streamlit run trix.py
'''

import streamlit as st
# from streamlit_option_menu import option_menu
import pandas as pd
import numpy as np
import cmocean
import xarray as xr 
import netCDF4 as nc
import matplotlib.pyplot as plt
import plotly.express as px 
import plotly.graph_objs as go

st.set_page_config(
    page_title="TRIX",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)

#START HIDE the TOP an burger menu!
st.markdown("""
<style>
	[data-testid="stDecoration"] {
		display: none;
	}
    .reportview-container {
            margin-top: -2em;
        }
        #MainMenu {visibility: hidden;}
        .stDeployButton {display:none;}
        footer {visibility: hidden;}
        #stDecoration {display:none;}

</style>""",
unsafe_allow_html=True)

ms = st.session_state
if "themes" not in ms: 
  ms.themes = {"current_theme": "dark",
                    "refreshed": True,
                    
                    "light": {"theme.base": "dark",
                              "button_face": "🌜"},

                    "dark":  {"theme.base": "light",
                              "button_face": "🌞"},
                    }


if ms.themes["current_theme"]=="dark":
    hide_streamlit_style = """
        <style>
            #root > div:nth-child(1) > div > div > div > div > section > div {padding-top: 0.5rem;}
            .stSelectbox div[data-baseweb="select"] > div:first-child {
                    background-color: Chocolate;
                    border-color: #ff0000;
                }
            body
        </style>
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        </style>
    
        """
else:
    hide_streamlit_style = """
        <style>
            #root > div:nth-child(1) > div > div > div > div > section > div {padding-top: 0.5rem;}
            .stSelectbox div[data-baseweb="select"] > div:first-child {
                    background-color: gray;
                    border-color: #000000;
                }
            body
        </style>
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        </style>
    
        """

st.markdown(hide_streamlit_style, unsafe_allow_html=True)

#st.markdown('<style>body{background-color: Blue;}</style>',unsafe_allow_html=True) 
#STOP HIDE the TOP an burger menu!

#https://streamlit-emoji-shortcodes-streamlit-app-gwckff.streamlit.app/
st.sidebar.title("Streamlit TRIX 🌐")

   
    

choice = st.sidebar.selectbox('Select....', options=["","Home","TRIX"], index=0)

def ChangeTheme():
  previous_theme = ms.themes["current_theme"]
  tdict = ms.themes["light"] if ms.themes["current_theme"] == "light" else ms.themes["dark"]
  for vkey, vval in tdict.items(): 
    if vkey.startswith("theme"): st._config.set_option(vkey, vval)

  ms.themes["refreshed"] = False
  if previous_theme == "dark": ms.themes["current_theme"] = "light"
  elif previous_theme == "light": ms.themes["current_theme"] = "dark"
        
def welcome():
    st.title(':blue[Welcome to TRIX] 🌐')
    
    btn_face = ms.themes["light"]["button_face"] if ms.themes["current_theme"] == "light" else ms.themes["dark"]["button_face"]
    st.write (':blue[\nChange Theme:]')
    st.button(btn_face, on_click=ChangeTheme)

    if ms.themes["refreshed"] == False:
      ms.themes["refreshed"] = True
      st.rerun()
    
    st.title("TROPHIC STATE INDEX - TRIX")
    st.write("The trophic state depends on the availability of nitrogen and phosphorus for primary production, which in terms determines the phytoplankton biomass and oxygen saturation. In TRIX the nutrients are represented ideally by total nitrogen and total phosphorus; chlorophyll-a is a substitute parameter for phytoplankton biomass, as production is not routinely measured; and the deviation of oxygen saturation from 100% (aD%O) in the productive layer indicates the production intensity of the system. This encompasses both phases of active photosynthesis and phases of prevailing respiration.(European Commission. Joint Research Centre., 2016).")
      



def trix():
    st.title('TRIX system')
    uplCount=0
    cols = st.columns(4)
    with cols[0]:
        uploaded_DIN = st.file_uploader("Choose a file DIN", type="nc")
    with cols[1]:
        uploaded_CHL = st.file_uploader("Choose a file CHL", type="nc")
    with cols[2]:
        uploaded_TP = st.file_uploader("Choose a file TP", type="nc")
    with cols[3]:
        uploaded_DO = st.file_uploader("Choose a file DO", type="nc")
    if uploaded_DIN is not None:
        ds_DIN = xr.open_dataset(uploaded_DIN, decode_cf=True, chunks="auto")
        uplCount+=1
    if uploaded_CHL is not None:
        ds_CHL = xr.open_dataset(uploaded_CHL, decode_cf=True, chunks="auto")
        uplCount+=1
    if uploaded_TP is not None:
        ds_TP = xr.open_dataset(uploaded_TP, decode_cf=True, chunks="auto")
        uplCount+=1
    if uploaded_DO is not None:
        ds_DO = xr.open_dataset(uploaded_DO, decode_cf=True, chunks="auto")
        uplCount+=1
    
    if uplCount==4:
        st.write('Files uploaded!')
        CHLF = ds_CHL['Water body chlorophyll-a_L1']
        DINF = ds_DIN['Water body dissolved inorganic nitrogen (DIN)_L1']
        TPF = ds_TP['Water body total phosphorus_L1']
        DOF = ds_DO['calculatedDOsaturation_L1']
        with cols[0]:
            st.write('total phosphorus units:', TPF.units)
        with cols[1]:
            st.write('dissolved inorganic nitrogen units:', DINF.units)
        with cols[2]:
            st.write('chlorophyll-a units:', CHLF.units)
        with cols[3]:
            st.write('dissolved oxygen saturation units:', DOF.units)
        TP = 30.97376*TPF #convert from umol/l to mg/m3
        DIN = 14.00672*DINF #convert from umol/l to mg/m3
        DO = abs(100 - DOF)
        CHL=CHLF
        TRIX = abs((np.log10(CHL*DIN*TP*DO)+1.5)/1.2)
        
        #st.write(TRIX.depth.values)
        from collections import OrderedDict
        # TRIX eutrophication indicator conditions and categories
        data = OrderedDict(
            [
                ("Conditions", ["Oligotrophic", "Oligotrophic", "Oligotrophic", "Eutrophic"]),
                ("TRIX units", ["< 4", "4 << 5", "5 << 6", "> 6"]),
                ("Trophic state", ["Elevated", "Good", "Mediocre", "Bad"]),
            ]
        )
        
        # Create a DataFrame to display in the app's table
        df = pd.DataFrame(
            OrderedDict([(name, col_data) for (name, col_data) in data.items()])
        )
        #st.write(df)

        
        colsB = st.columns(2)
        with colsB[0]:
            
            i = st.radio(
                "Select Season and Depth:",
                [0,1,2,3],
                captions=[
                        "JAN/FEB/MAR", "APR/MAY/JUN", "JUL/AOU/SEP", "OCT/NOV/DEC"
                    ],horizontal=True
                
            )
        
        r = range(0, len(TRIX.depth))
        a = list(r)
        with colsB[1]:
            j = st.select_slider("Depth", options=a)
        df = pd.read_csv("12M_med.csv")
        # Flatten the data for scattermapbox
        z_values = np.ravel(TRIX[int(i), int(j), :, :])
        lon_values, lat_values = np.meshgrid(TRIX.lon, TRIX.lat)
        lon_values = lon_values.ravel()
        lat_values = lat_values.ravel()
        
        # Round and prepare coordinate comparison
        df['X'] = df['X'].round(2)
        df['Y'] = df['Y'].round(2)
             
        #Handle NaN values in z_values
        nan_mask = np.isnan(z_values)
        z_values_with_transparency = np.where(nan_mask, -999, z_values)
        
        #Create a DataFrame for the meshgrid values
        meshgrid_df = pd.DataFrame({
            'lon': lon_values,
            'lat': lat_values,
            'z': z_values_with_transparency
        })
        
        # Merge the meshgrid data with df to get corresponding z values
        merged_df = pd.merge(df, meshgrid_df, left_on=['X', 'Y'], right_on=['lon', 'lat'], how='left')
        
    
        # Handle cases where merged z values might be NaN
        merged_df.fillna({'z':-999}, inplace=True)
        #st.write(merged_df)
        
        # Create a scattermapbox trace for the heatmap
        heatmap_trace = go.Scattermap(
            lon=df['X'],
            lat=df['Y'],
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
                colorbar=dict(title="TRIX"),
                opacity=1
            ),
            text=merged_df['z'],
            connectgaps=True
        )
    
        # Create the figure
        fig = go.Figure(data=[heatmap_trace])
    
       
        fig.update_layout(
            mapbox=dict(
                style="satellite",
                center={"lon": 15.22, "lat": 43.14},
                zoom=3
            ),
            title_text='TRIX by Season',
            height=1300,
            width=1300,
        )
        st.plotly_chart(fig)



if choice=="TRIX":
    trix()
elif choice=="Test2":
    welcome()
else:
    welcome()