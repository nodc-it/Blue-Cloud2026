# TRIX Trophic State Index Interactive App

This is an interactive web application built with Plotly Dash that visualizes the TRIX (Trophic State Index) for the Mediterranean Sea.

## Features

- **Time Selector**: Choose from 4 seasonal periods (JFM, AMJ, JAS, OND)
- **Depth Selector**: Select from 8 depth levels (0m, 5m, 10m, 20m, 30m, 50m, 75m, 100m)
- **Interactive Map**: Satellite map showing TRIX values with color coding
- **TRIX Categories Table**: Reference table showing trophic state classifications

## TRIX Index

The TRIX index combines four water quality parameters:
- Chlorophyll-a (phytoplankton biomass)
- Dissolved Inorganic Nitrogen (DIN)
- Total Phosphorus (TP)
- Dissolved Oxygen saturation deviation

TRIX values indicate trophic state:
- < 4: Oligotrophic (Elevated)
- 4-5: Oligotrophic (Good)
- 5-6: Oligotrophic (Mediocre)
- > 6: Eutrophic (Bad)

## Data Source

The app uses climatological data from DIVA analysis for the Mediterranean Sea (2003-2012 period).

## Running the App

1. Ensure Python dependencies are installed:
   ```bash
   pip install dash plotly pandas numpy xarray netcdf4
   ```

2. Run the application:
   ```bash
   python trix_app.py
   ```

3. Open your browser to `http://127.0.0.1:8050/`

## Files

- `trix_app.py`: Main Dash application
- Data files in `MEI_VLab/DIVA_climatologies/2003-2012/`
- Coordinate file: `MEI_VLab/DIVA_climatologies/12M_med.csv`