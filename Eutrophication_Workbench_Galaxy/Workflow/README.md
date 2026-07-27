# Modification and Optimisation

## Step 0 

Modifications are about the date. 
The next step is waiting for the format "YYYY-MM-DD", so we changed the input prompt to be clear about the expected format. 

```
year_from = input("Enter start year/month/day (YYYYMMDD): ").strip()
year_to = input("Enter end year/month/day (YYYYMMDD): ").strip()

if not year_from:
    year_from = "20100101"
if not year_to:
    year_to = "20100131"
```

inaly, we modify the name structure to use a consistent separator between each parameter. 
Before that, you had both "-" and "_".
We replaced "-" in "_to_". 

```
filename : "02_BC_EWB_CW_PR_{depth_from}m_to_{depth_to}m_{year_from}_to_{year_to}"
```

## Sept 1

### Metadata

The goal was to be able to extract metadata from the filename. 
We try to find a match with a specific pattern. Then we save : 

- Depth min
- Depth max
- Date min
- Date max

We take care about the date format because next steps in this notebook expect the YYYY-MM-DD format.

```
# MetaData
import yaml

# Open the YAML file
with open('../../2_CWduplicates-tool/Configuration_files/Config_Profiles/cw_user_config.yaml', 'r') as fichier:
    donnees = yaml.safe_load(fichier)
    
operator_name = donnees["default"]["operator"]["name"]
file_name = donnees["default"]["output"]["filename"]

match = re.search(r'(\d+)m_to_(\d+)m_(\d{8})_to_(\d{8})$', file_name)
if match:
    metadata_depth_min = int(match.group(1))
    metadata_depth_max = int(match.group(2))
    
    # YYYYMMDD → YYYY-MM-DD
    raw_min = match.group(3)
    raw_max = match.group(4)
    metadata_date_min = f"{raw_min[:4]}-{raw_min[4:6]}-{raw_min[6:8]}"
    metadata_date_max = f"{raw_max[:4]}-{raw_max[4:6]}-{raw_max[6:8]}"
    
    print(f"Depth min : {metadata_depth_min}")
    print(f"Depth max : {metadata_depth_max}")
    print(f"Date min : {metadata_date_min}")
    print(f"Date max : {metadata_date_max}")
```
### BDI List 

Instead of having a filter of BDI we create a list of every BDI. 
Before this modification, you had to do it manually for each BDI. 

```
source_bdi_list = ["BEACON_EMODNET_CHEMISTRY", "BEACON_CMEMS_BGC", "BEACON_WOD"]
```

### QUERY BUIDLER

We build a query for each BDI : 

```
queries = {}
for bdi in source_bdi_list:
```

We use the metadata defined at the beginning of the file and then add this query into our dictionary 
"queries" with the BDI name as the Key. 

```
# query.add_range_filter("TIME", "1921-10-15T00:00:00", "2023-12-31T23:59:59") # full time range
    # You can adjust the date range as needed. The format is ISO 8601.
    date_min = f"{metadata_date_min}T00:00:00"
    date_max = f"{metadata_date_max}T23:59:59"
    query.add_range_filter("TIME", date_min, date_max)

    # Depth range from 0 to 10000 meters (you can adjust as needed)
    query.add_range_filter("DEPTH", metadata_depth_min, metadata_depth_max) 

    # comment when only querying merged data, the filter give a file per BDI
    query.add_equals_filter("SOURCE_BDI", bdi)

    # Alternatively, you can use a polygon filter to define a custom area. Below the polygon represents the North-East Atlantic area:
    # query.add_polygon_filter("LONGITUDE", "LATITUDE", [[-42, 24.30], [-42, 48], [-0.5, 48], [-0.5, 41], [-5,37], [-5, 24.30], [-42, 24.30]])

    query.add_range_filter("LATITUDE", -90, 90) # Latitude range from -90 to 90 for full range (you can adjust as needed)
    query.add_range_filter("LONGITUDE", -180, 180) # Longitude range from -180 to 180 for full range (you can adjust as needed)
    
    queries[bdi] = query
```

### OUTPUT FORMAT

We create a Parquet file for each query built above.
The name of each Parquet file is derived from its metadata. 

```
list_parquet_file = {}

for bdi in queries:
    # Extract min/max DEPTH and TIME from the actual data
    min_depth = str(metadata_depth_min)
    max_depth = str(metadata_depth_max)
    min_time = date_min.replace(":", "").replace("-", "")[:8]
    max_time = date_max.replace(":", "").replace("-", "")[:8]

    run_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Construct filename following the naming convention: 
    # <PROJECT>_<WORKBENCH>_<BEACON INSTANCE>_<SOURCE BDI>_<featuretype>_<UNIT>_<minDEPTH>_to_<maxDEPTH>_<minTIME>_to_<maxTIME>_<version TIMESTAMP<.Format
    filename = f"BC_EWB_MERGED_{bdi}_{feature_type}_{unit}_{min_depth}m_to_{max_depth}m_{min_time}_to_{max_time}_v{run_timestamp}"
    
    queries[bdi].to_parquet(f"{filename}.parquet")
    list_parquet_file[filename] = bdi
```

For the output of these Parquet files, we need to respect the following folder mapping because CW expects for these exact names. If the names do not match or if the folders are empty, then CW will fail.

```folder_map = {
    "BEACON_CMEMS_BGC": "EUTRO_CMEMS",
    "BEACON_EMODNET_CHEMISTRY": "EUTRO_EC",
    "BEACON_WOD": "EUTRO_WOD",
}
```

Finaly, we move each file into the correct folder. 

```
for item in list_parquet_file:
    dst_sub = folder_map.get(list_parquet_file[item])
    if dst_sub is None:
        raise ValueError(f"Unknown source_bdi: {list_parquet_file[item]}")
        
    dst_dir = in_raw / dst_sub
    move(f"{item}.parquet", dst_dir / f"{item}.parquet")
```