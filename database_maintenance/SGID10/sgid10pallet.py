#!/usr/bin/env python
# * coding: utf8 *
'''
sgid10pallet.py

A module that contains a template for database maintenance pallets
'''

import arcpy
from forklift.models import Pallet
from os.path import join
from traceback import format_exc


class Sgid10Pallet(Pallet):

    def ship(self):
        try:
            # Run commands as user SDE to compress and analyze database and system tables
            sdeconnection = join(self.garage, 'SGID10', 'sde@SGID10@sgid.agrc.utah.gov.sde')
            arcpy.Compress_management(sdeconnection)
            self.log.info('Compress Complete')

            # System table analyze was giving problems so it had to go for now.
            #arcpy.AnalyzeDatasets_management(sdeconnection,'SYSTEM')
            #print 'Analyze System Tables Complete'

            userconnections = [join(self.garage, 'SGID10', 'SGID_Biosciense@SGID10@sgid.agrc.utah.gov.sde'),
                               join(self.garage, 'SGID10', 'SGID_Boundaries@SGID10@sgid.agrc.utah.gov.sde'),
                               join(self.garage, 'SGID10', 'SGID_Cadastre@SGID10@sgid.agrc.utah.gov.sde'),
                               join(self.garage, 'SGID10', 'SGID_Climate@SGID10@sgid.agrc.utah.gov.sde'),
                               join(self.garage, 'SGID10', 'SGID_Demographics@SGID10@sgid.agrc.utah.gov.sde'),
                               join(self.garage, 'SGID10', 'SGID_Economy@SGID10@sgid.agrc.utah.gov.sde'),
                               join(self.garage, 'SGID10', 'SGID_Elevation@SGID10@sgid.agrc.utah.gov.sde'),
                               join(self.garage, 'SGID10', 'SGID_Energy@SGID10@sgid.agrc.utah.gov.sde'),
                               join(self.garage, 'SGID10', 'SGID_Environment@SGID10@sgid.agrc.utah.gov.sde'),
                               join(self.garage, 'SGID10', 'SGID_Farming@SGID10@sgid.agrc.utah.gov.sde'),
                               join(self.garage, 'SGID10', 'SGID_Geoscience@SGID10@sgid.agrc.utah.gov.sde'),
                               join(self.garage, 'SGID10', 'SGID_Health@SGID10@sgid.agrc.utah.gov.sde'),
                               join(self.garage, 'SGID10', 'SGID_History@SGID10@sgid.agrc.utah.gov.sde'),
                               join(self.garage, 'SGID10', 'SGID_Indices@SGID10@sgid.agrc.utah.gov.sde'),
                               join(self.garage, 'SGID10', 'SGID_Location@SGID10@sgid.agrc.utah.gov.sde'),
                               join(self.garage, 'SGID10', 'SGID_Planning@SGID10@sgid.agrc.utah.gov.sde'),
                               join(self.garage, 'SGID10', 'SGID_Political@SGID10@sgid.agrc.utah.gov.sde'), join(
                                   self.garage, 'SGID10', 'SGID_Raster@SGID10@sgid.agrc.utah.gov.sde'), join(
                                       self.garage, 'SGID10', 'SGID_Recreation@SGID10@sgid.agrc.utah.gov.sde'),
                               join(self.garage, 'SGID10', 'SGID_Society@SGID10@sgid.agrc.utah.gov.sde'), join(
                                   self.garage, 'SGID10', 'SGID_Transportation@SGID10@sgid.agrc.utah.gov.sde'), join(
                                       self.garage, 'SGID10', 'SGID_Utilities@SGID10@sgid.agrc.utah.gov.sde'), join(
                                           self.garage, 'SGID10', 'SGID_Water@SGID10@sgid.agrc.utah.gov.sde')]

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
                    dataList += arcpy.ListFeatureClasses() + arcpy.ListDatasets('', 'Feature')

                # reset the workspace
                arcpy.env.workspace = workspace

                # Get the user name for the workspace
                userName = arcpy.Describe(workspace).connectionProperties.user.lower()

                # remove any datasets that are not owned by the connected user.
                userDataList = [ds for ds in dataList if ds.lower().find('.%s.' % userName) > -1]

                # Execute analyze datasets
                # Note: to use the 'SYSTEM' option the workspace user must be an administrator.
                if len(dataList) > 0:
                    arcpy.AnalyzeDatasets_management(workspace, 'NO_SYSTEM', userDataList, 'ANALYZE_BASE',
                                                     'ANALYZE_DELTA', 'ANALYZE_ARCHIVE')
                    self.log.info('Analyze Complete')

        except Exception as e:
            self.send_email('michaelfoulger@utah.gov', 'Error with {}'.format(__file__), format_exc())
            raise e
