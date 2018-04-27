import numpy as np
import os
import sys
import re
from osgeo import ogr, gdal
from shapely.geometry import  LineString,MultiLineString, mapping, shape, base, box
from shapely.prepared import prep

def ver_check():
	version_num = int(gdal.VersionInfo('VERSION_NUM'))
	if version_num < 1100000:
	    sys.exit('ERROR: Python bindings of GDAL 1.10 or later required')
def read_gjsons(smaller,larger):
	thedir=os.getcwd()+'/jsons/'
	for json in [smaller, larger]:
		os.system('ogr2ogr -nlt LINESTRING -skipfailures ' + thedir + json[:-8] + '.shp ' + thedir + json + ' OGRGeoJSON')
	driver = ogr.GetDriverByName("ESRI Shapefile")
	smallines=driver.Open(thedir + smaller[:-8]+'.shp',0)
	largelines=driver.Open(thedir + larger[:-8] + '.shp',0)
	return(smallines,largelines)

def lines_to_multilines(layer):
	linelist=[]
	for feature in layer:
	    geom= feature.GetGeometryRef()
	    coordstring=str(geom)[12:-1]
	    coordlist=str.split(coordstring,',')
	    coordlist=list([tuple([float(i) for i in str.split(x,' ')]) for x in coordlist])
	    coordline=LineString(coordlist)
	    linelist.append(coordline)
	merged=MultiLineString(linelist)
	return(merged)

def trim_and_merge(smaller,larger):
	layer=smaller.GetLayer()
	smallermerged=lines_to_multilines(layer)
	smallbb=smallermerged.bounds
	print(smallbb)
	smallbbpoly=prep(box(smallbb[0],smallbb[1],smallbb[2],smallbb[3]))
	biglayer=larger.GetLayer()
	largermerged=lines_to_multilines(biglayer)
	hits = filter(smallbbpoly.contains, largermerged)
	print(hits)
