import numpy as np
import os
import sys
import re
import osr
from osgeo import ogr, gdal
from shapely.geometry import LineString, MultiLineString, mapping, shape, base, box, Point, MultiPolygon, Polygon
from shapely.prepared import prep


def ver_check():
    version_num = int(gdal.VersionInfo('VERSION_NUM'))
    if version_num < 1100000:
        sys.exit('ERROR: Python bindings of GDAL 1.10 or later required')


def read_gjsons(smaller, larger):
    thedir = os.getcwd() + '/jsons/'
    for json in [smaller, larger]:
        os.system('ogr2ogr -nlt LINESTRING -skipfailures ' + thedir +
                  json[:-8] + '.shp ' + thedir + json + ' OGRGeoJSON')
    driver = ogr.GetDriverByName("ESRI Shapefile")
    smallines = driver.Open(thedir + smaller[:-8] + '.shp', 0)
    largelines = driver.Open(thedir + larger[:-8] + '.shp', 0)
    return(smallines, largelines)


def lines_to_multilines(layer):
    linelist = []
    coordsline = []
    for feature in layer:
        geom = feature.GetGeometryRef()
        coordstring = str(geom)[12:-1]
        coordlist = str.split(coordstring, ',')
        coordlist = list([tuple([float(i) for i in str.split(x, ' ')]) for x in coordlist])
        coordline = LineString(coordlist)
        linelist.append(coordline)
        coordsline.append(list(coordline.coords))
    merged = MultiLineString(linelist)
    return(merged, coordsline)


def trim_and_merge(smaller, larger):
    layer = smaller.GetLayer()
    smallermerged = lines_to_multilines(layer)[0]
    smallbb = smallermerged.bounds
    smallbbpoly = prep(box(smallbb[0], smallbb[1], smallbb[2], smallbb[3]))
    biglayer = larger.GetLayer()
    largermerged, points = lines_to_multilines(biglayer)
    finalpoints = points[0]
    for extralist in points[1:]:
        finalpoints = finalpoints + extralist
    hits = filter(smallbbpoly.contains, [Point(x) for x in finalpoints])
    hits = [x for x in list(hits)]
    trimmedlarge = LineString(hits)
    finallist = list(smallermerged)
    finallist.append(trimmedlarge)
    final = MultiLineString(finallist)
    return(final)


def make_and_write_ta(merged):
    polygons = [Polygon(x) for x in list(merged)]
    multipoly = MultiPolygon(polygons)
    driver = ogr.GetDriverByName('Esri Shapefile')
    ds = driver.CreateDataSource('my.shp')
    layer = ds.CreateLayer('', None, ogr.wkbPolygon)
    layer.CreateField(ogr.FieldDefn('id', ogr.OFTInteger))
    defn = layer.GetLayerDefn()
    feat = ogr.Feature(defn)
    feat.SetField('id', 1)
    geom = ogr.CreateGeometryFromWkb(multipoly.wkb)
    feat.SetGeometry(geom)
    layer.CreateFeature(feat)
    feat = geom = None
    # Save and close everything
    ds = layer = feat = geom = None
