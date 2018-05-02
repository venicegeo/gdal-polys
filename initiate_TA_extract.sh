#!/bin/bash
#Used to modify parameters and run a tidal area extract on output geojsons.
pip3 install shapely \
python3 run_TA_extract.py \
    --small_lines '03AUG2017_Coastline.geojson' \
    --large_lines 'Bandar_Abbas_OSM.geojson' \
    --out_name 'TA_Extract.shp' \
