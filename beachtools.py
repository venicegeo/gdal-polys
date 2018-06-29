import numpy as np
import os
import sys
import re
import osr
try:
    from osgeo import gdal, ogr, osr
except:
    import gdal, ogr, osr
from shapely.geometry import LineString, MultiLineString, mapping, shape, base, box, Point, MultiPolygon, Polygon
from shapely.prepared import prep
from shapely import ops


def read_gjsons(smaller, larger):
    '''Reads in raw geojsons stored in jsons directory'''
    #thedir = os.getcwd() + '/jsons/'
    for json in [smaller, larger]:
        outShp = json[:-8] + '.shp'
        exeString = 'ogr2ogr -nlt LINESTRING -skipfailures %s.shp %s' % (json[:-8], json)
        print 'Converting geojson to shapefile.  System Command: %s' % exeString
        os.system(exeString)
    driver = ogr.GetDriverByName("ESRI Shapefile")
    smallines = driver.Open(smaller[:-8] + '.shp', 0)
    largelines = driver.Open(larger[:-8] + '.shp', 0)
    return(smallines, largelines)


def lines_to_multilines(layer):
    '''Converts open geojson layers to shapely MultiLineString objects'''
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
    '''Reindexes and combines lines to form continuous shapes after trimming the larger vector'''
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

    def reindex_trimmed(trimmed=trimmedlarge, other=smallermerged):
        targetpoint = Point(list(trimmed.coords)[0])
        finallist = list(other)
        distlist = []
        indexlist = []
        index = 0
        for linestring in finallist:
            endpoints = [list(linestring.coords)[0], list(linestring.coords)[-1]]
            for point in endpoints:
                indexlist.append(index)
                dist = targetpoint.distance(Point(point))
                distlist.append(dist)
            index += 1
        targetindex = np.where(distlist == np.min(distlist))[0][0]
        if targetindex % 2 == 0:
            modifier = 0
        else:
            modifier = 1
        lineindex = indexlist[targetindex]
        targetlinecoords = finallist[lineindex].coords[:]
        targetlinecoords[(modifier * -1)] = targetpoint.coords[0]
        finallist[lineindex] = LineString(targetlinecoords)
        combinedlist = MultiLineString([trimmed, finallist[lineindex]])
        combined = ops.linemerge(combinedlist)
        del finallist[lineindex]
        finallist.insert(lineindex - 1, combined)
        final = MultiLineString(finallist)
        return(final)
    final = reindex_trimmed()
    return(final)


def make_and_write_ta(merged, out_name):
    '''Forms a MultiPolygon from a MultiLineString, georeferences it,
     and calculates its area before writing it to a shape file.'''
    polygons = [Polygon(x) for x in list(merged)]
    multipoly = MultiPolygon(polygons)
    driver = ogr.GetDriverByName('Esri Shapefile')
    ds = driver.CreateDataSource(out_name)
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
    os.system('ogr2ogr -a_srs EPSG:4326 ' + out_name + ' ' + out_name)

    def get_UTM_info(multipoly=multipoly):
        latlon = list(multipoly.bounds)[0:2]
        if latlon[0] < 0:
            hemi = 0
        else:
            hemi = 1
        zoneval = int(1 + (latlon[1] + 180.0) / 6.0)
        return(hemi, zoneval)
    hemi, zoneval = get_UTM_info()
    t_srs = '"+proj=utm +zone=' + str(zoneval) + ' +datum=WGS84"'
    warpcommand = 'ogr2ogr -t_srs ' + t_srs + '-overwrite ' + \
        out_name[:-4] + '_utm.shp ' + ' ' + out_name
    os.system(warpcommand)
    os.system('ogrinfo -sql "SELECT SUM(OGR_GEOM_AREA) AS TOTAL_AREA FROM ' +
              out_name[:-4] + '_utm' + '" ' + out_name[:-4] + '_utm.shp' + '| grep "TOTAL_AREA"')
    return(multipoly)
