#!/usr/bin/env python
# * coding: utf8 *
'''
HistoricalSitesPallet.py

A module that contains a pallet definition for updating the historical sites in SGID from the UDSH database
'''


from forklift.models import Pallet
from os.path import join
import arcpy


class HistoricalSitesPallet(Pallet):
    def ship(self):
        field = 'PresenceYN'

        self.sgid = join(self.garage, 'SGID_History@SGID10.sde')
        self.udsh = join(self.garage, 'DC_cures_user@UDSHSpatial_New.sde')

        pts = join(self.udsh, 'UDSHSpatial_New.UDSH.IMACS_SITE_POINT')
        line = join(self.udsh, 'UDSHSpatial_New.UDSH.IMACS_SITE_LINE')
        poly = join(self.udsh, 'UDSHSpatial_New.UDSH.IMACS_SITE_POLYGON')
        archSites = join(self.sgid, 'SGID10.HISTORY.ArchaeologySites')

        self.log.info('creating layer')
        archSitesFL = arcpy.MakeFeatureLayer_management(archSites)

        self.log.info('selecting by location: points')
        arcpy.SelectLayerByLocation_management(archSitesFL, 'INTERSECT', pts, '', 'NEW_SELECTION')
        self.log.info('selecting by location: lines')
        arcpy.SelectLayerByLocation_management(archSitesFL, 'INTERSECT', line, '', 'ADD_TO_SELECTION')
        self.log.info('selecting by location: polygons')
        arcpy.SelectLayerByLocation_management(archSitesFL, 'INTERSECT', poly, '', 'ADD_TO_SELECTION')

        self.log.info('calculating new values for: ' + field)
        arcpy.CalculateField_management(archSitesFL, field, '"Site(s) Present"', 'PYTHON')
        arcpy.SelectLayerByAttribute_management(archSitesFL, 'SWITCH_SELECTION')
        arcpy.CalculateField_management(archSitesFL, field, '"Site Presence Unknown"', 'PYTHON')

        self.log.info('deleting layer')
        arcpy.Delete_management(archSitesFL)
