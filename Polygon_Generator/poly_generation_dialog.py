#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Polygon_GeneratorDialog
                                 A QGIS plugin
 Produces detected changes polygon for tidal areas.
                             -------------------
        begin                : 2018-03-30
        git sha              : $Format:%H$
        copyright            : (C) 2018 by Brandon Rasmussen
        email                : brasmussen@exogenesis.earth
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import os

from PyQt4 import QtGui, uic

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'poly_generation_dialog_base.ui'))


class Polygon_GeneratorDialog(QtGui.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(Polygon_GeneratorDialog, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
