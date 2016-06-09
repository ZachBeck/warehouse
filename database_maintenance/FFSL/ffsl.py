import arcpy, os
from os.path import dirname, join

current_folder = dirname(__file__)

# Run commands as user SDE to compress and analyze database and system tables
sdeconnection = join(current_folder, 'DNR_sde@FFSL@itdb104sp.dts.utah.gov.sde')
arcpy.Compress_management(sdeconnection)
print "Compress Complete"
arcpy.AnalyzeDatasets_management(sdeconnection,"SYSTEM")
print "Analyze System Tables Complete"

userconnections = [join(current_folder, 'DNR_Fire@FFSL@itdb104sp.dts.utah.gov.sde'),
                   join(current_folder, 'DNR_Forestry@FFSL@itdb104sp.dts.utah.gov.sde'),
                   join(current_folder, 'DNR_Lands@FFSL@itdb104sp.dts.utah.gov.sde')]

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
        dataList += arcpy.ListFeatureClasses() + arcpy.ListDatasets("", "Feature")


    # reset the workspace
    arcpy.env.workspace = workspace

    # Get the user name for the workspace
    userName = arcpy.Describe(workspace).connectionProperties.user.lower()

    # remove any datasets that are not owned by the connected user.
    userDataList = [ds for ds in dataList if ds.lower().find(".%s." % userName) > -1]


    # Execute analyze datasets
    # Note: to use the "SYSTEM" option the workspace user must be an administrator.
    if len(dataList) > 0:
        arcpy.AnalyzeDatasets_management(workspace, "NO_SYSTEM", dataList, "ANALYZE_BASE","ANALYZE_DELTA","ANALYZE_ARCHIVE")
        print "Analyze Complete"
