#!/usr/bin/env python
# * coding: utf8 *
'''
udwr.py

A module that contains a template for database maintenance pallets
'''

import arcpy
from forklift.models import Pallet
from os.path import join
from traceback import format_exc


class UdwrPallet(Pallet):
    def ship(self):
        try:
            # Run commands as user SDE to compress and analyze database and system tables
            sdeconnection = join(self.garage, 'UDWR', 'DNR_sde@UDWR@udwr.agrc.utah.gov.sde')
            arcpy.Compress_management(sdeconnection)
            print('Compress Complete')
            arcpy.AnalyzeDatasets_management(sdeconnection, 'SYSTEM')
            print('Analyze System Tables Complete')

            userconnections = [join(self.garage, 'UDWR', 'DNR_DWRADMIN@UDWR@itdb104sp.dts.utah.gov.sde')]

            for con in userconnections:
                # set workspace
                # the user in this workspace must be the owner of the data to analyze.
                workspace = con

                # set the workspace environment
                arcpy.env.workspace = workspace

                # NOTE: Analyze Datasets can accept a Python list of datasets.

                # Get a list of all the datasets the user has access to.
                # First, get all the stand alone tables, feature classes and rasters.
                dataList = arcpy.ListTables() + arcpy.ListFeatureClasses() + arcpy.ListRasters()

                # Next, for feature datasets get all of the datasets and featureclasses
                # from the list and add them to the master list.
                for dataset in arcpy.ListDatasets('', 'Feature'):
                    arcpy.env.workspace = join(workspace, dataset)
                    dataList += arcpy.ListFeatureClasses() + arcpy.ListDatasets()

                # reset the workspace
                arcpy.env.workspace = workspace

                # Execute analyze datasets
                # Note: to use the 'SYSTEM' option the workspace user must be an administrator.
                arcpy.AnalyzeDatasets_management(workspace, 'NO_SYSTEM', dataList, 'ANALYZE_BASE', 'ANALYZE_DELTA', 'ANALYZE_ARCHIVE')
                print('Analyze Complete')

        except Exception:
            self.send_email('michaelfoulger@utah.gov', 'Error with {}'.format(__file__), format_exc())
            raise
