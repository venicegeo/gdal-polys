# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Polygon_Generator
                                 A QGIS plugin
 Produces detected changes polygon for tidal areas.
                             -------------------
        begin                : 2018-03-30
        copyright            : (C) 2018 by Brandon Rasmussen
        email                : brasmussen@exogenesis.earth
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load Polygon_Generator class from file Polygon_Generator.

    :param iface: A QGIS interface instance.
    :type iface: QgisInterface
    """
    #
    from .poly_generation import Polygon_Generator
    return Polygon_Generator(iface)
