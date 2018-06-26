#!/bin/bash
#Used to modify parameters and run a tidal area extract on output geojsons.
pip3 install shapely
pip3 install gdal
pip3 install numpy
python3 run_TA_extract.py \
    --small_lines '/home/Landsat1.geojson' \
    --large_lines '/home/Landsat2.geojson' \
    --out_name 'GBDX_TA.shp' \
