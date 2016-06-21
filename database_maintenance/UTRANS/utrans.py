#!/usr/bin/env python
# * coding: utf8 *
'''
utrans.py

A module that contains a template for database maintenance pallets
'''

from forklift.models import Pallet
from os.path import join, dirname
from traceback import format_exc

current_folder = dirname(__file__)


class UtransPallet(Pallet):
    def ship(self):
        try:
            #: code goes here, remove pass
            #: remember to update the paths to database connection files like this:
            #: join(self.garage, current_folder, 'connection_file.sde')
            # Run commands as user SDE to compress and analyze database and system tables

            # sdeconnection = r'C:\Scheduled\UTRANS\DC_sde@UTRANS@utrans.agrc.utah.gov.sde'
            sdeconnection = join(self.garage, 'UTRANS', 'DC_sde@UTRANS@utrans.agrc.utah.gov.sde')

            arcpy.Compress_management(sdeconnection)
            self.log.info("Compress Complete")

            arcpy.AnalyzeDatasets_management(sdeconnection,"SYSTEM")
            self.log.info("Analyze System Tables Complete")

            userconnections = [join(self.garage, 'UTRANS', 'DC_TRANSADMIN@UTRANS@utrans.agrc.utah.gov.sde')]

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
                for dataset in arcpy.ListDatasets("", "Feature"):
                    arcpy.env.workspace = os.path.join(workspace,dataset)
                    dataList += arcpy.ListFeatureClasses() + arcpy.ListDatasets()

                # reset the workspace
                arcpy.env.workspace = workspace

                # Get the user name for the workspace
                userName = arcpy.Describe(workspace).connectionProperties.user.lower()

                # remove any datasets that are not owned by the connected user.
                userDataList = [ds for ds in dataList if ds.lower().find(".%s." % userName) > -1]

                # Execute analyze datasets
                # Note: to use the "SYSTEM" option the workspace user must be an administrator.
                arcpy.AnalyzeDatasets_management(workspace, "NO_SYSTEM", dataList, "ANALYZE_BASE","ANALYZE_DELTA","ANALYZE_ARCHIVE")
                self.log.info("Analyze Complete")
        except Exception as e:
            self.send_email('michaelfoulger@utah.gov', 'Error with {}'.format(__file__), format_exc())
            raise e
