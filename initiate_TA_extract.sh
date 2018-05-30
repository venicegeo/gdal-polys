#!/bin/bash
#Used to modify parameters and run a tidal area extract on output geojsons.
pip3 install shapely
pip3 install gdal
pip3 install numpy
python3 run_TA_extract.py \
    --small_lines '14AUG2017_GBDX.geojson' \
    --large_lines 'Bandar_Abbas_OSM.geojson' \
    --out_name 'GBDX_TA.shp' \
