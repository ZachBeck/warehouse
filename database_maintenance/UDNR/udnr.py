import arcpy, os

# Run commands as user SDE to compress and analyze database and system tables
sdeconnection = r'C:\Scheduled\UDNR\DNR_sde@UDNR@itdb104sp.dts.utah.gov.sde'
arcpy.Compress_management(sdeconnection)
print "Compress Complete"
arcpy.AnalyzeDatasets_management(sdeconnection,"SYSTEM")
print "Analyze System Tables Complete"

userconnections = [r'C:\Scheduled\UDNR\DNR_DPR@UDNR@itdb104sp.dts.utah.gov.sde',\
                    r'C:\Scheduled\UDNR\DNR_DWR@UDNR@itdb104sp.dts.utah.gov.sde',\
                    r'C:\Scheduled\UDNR\DNR_FFSL@UDNR@itdb104sp.dts.utah.gov.sde',\
                    r'C:\Scheduled\UDNR\DNR_OGM@UDNR@itdb104sp.dts.utah.gov.sde',\
                    r'C:\Scheduled\UDNR\DNR_UGS@UDNR@itdb104sp.dts.utah.gov.sde',\
                    r'C:\Scheduled\UDNR\DNR_WRE@UDNR@itdb104sp.dts.utah.gov.sde',\
                    r'C:\Scheduled\UDNR\DNR_WRT@UDNR@itdb104sp.dts.utah.gov.sde']

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
    print "Analyze Complete"