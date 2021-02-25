#                                                                                    
# CHS Chart Tool written for Python 3.6.8+ ArcGIS Pro                                
#                                                                                    
# RC 1.0                                                                             
#                                                                                    
# written 20191120 | clinton.pearce@forces.gc.ca                                     
#                                                                                    
# Potential to add:                                                                  
#   > When updating the mosaic (final step), check the Chart Edition so we're not    
#     needlessly updating records                                                    
#                                                                                                                                                               
# params: 0-debug | 1-raw KAPs | 2-output dir | 3-TIF dir name | 4-db location  
#                                                                                    
# a sample KAP file header below...
#==========================================================================
# !
# CRR/© Fisheries and Oceans Canada 2019 / © Pêches et Océans Canada 2019
# VER/3.07
# BSB/NA=HAVRE-AUX-MAISONS,NU=495501,RA=5969,4171,DU=254
# KNP/SC=10000,GD=NAD83,PR=Mercator,PP=47.500000,PI=1.000,SK=0.000000
# TA=90.000000,UN=METRES,SD=Lower Low Water Large Tide,DX=1.000000
# DY=1.000000
# KNQ/EC=RF,GD=NAR,VC=HHLT,SC=LLLT,PC=MC,P1=0.000000,P2=47.500000
# P3=NOT_APPLICABLE,P4=NOT_APPLICABLE,GC=UB,RM=INVERSE
# CED/SE=20180615,RE=3001,ED=06/15/2018
# NTM/NE=20190329,ND=02/28/2019
# ...
# ...
# $ **there are a ton of lines here in between** $
# $ **for decollaring we only care about the PLY lines** $
# $ **these hold the collar/surround coordinates** $
# REF/100,4019,1302,47.410835440708,-61.820851809497
# PLY/1,47.388333300070,-61.870000000000
# PLY/2,47.410826430974,-61.870000000000
# PLY/3,47.410835440708,-61.820851809497
# PLY/4,47.388333300070,-61.820851809497
# PLY/5,47.388333300070,-61.870000000000
# DTM/-0.000,-0.000
#==========================================================================

import os
import shutil
import re
import datetime
import time
import arcpy
from arcpy.sa import *
import fnmatch
import csv

# disable ESRI's bullshit multithreader
arcpy.env.parallelProcessingFactor = "0"

boolDEBUG = arcpy.GetParameterAsText(0)
dirKAPS = arcpy.GetParameterAsText(1)
directoryDecollared = arcpy.GetParameterAsText(2)
tempDir = arcpy.GetParameterAsText(3)
dirGDB = arcpy.GetParameterAsText(4)
tifFolderName = arcpy.GetParameterAsText(5)
if tifFolderName == "":
    tifFolderName = "Converted CHS Charts"
mosaicFilter = arcpy.GetParameterAsText(6)
if mosaicFilter == "":
    mosaicFilter = "*rm_*"

def timeCalc():
    '''
    return the time right now at call time in YYMMDD format
    '''
    return(datetime.datetime.now().strftime("%Y%m"))

# return the time right now, in HH:MM:SS format - used for messages
def clock():
    return(datetime.datetime.now().strftime("%H:%M:%S"))

def monitor(title, incr=True, phaseCurrent=None, subPhase=""):
    #global phaseCount
    #if phaseCurrent == None:
    #    phaseCurrent = phaseCount
    if incr:
        phaseCount = phaseCount + 1
    return("{}{}) {}".format(phaseCount, subPhase, title))

def msg(x):
    arcpy.AddMessage("{}: {}".format(clock(), x))

def msgMajor(x, phaseCurr=None):
    # if phaseCurr == None:
    #    phaseCurr = phase
    arcpy.AddMessage(".")
    arcpy.AddMessage("=================================================================")
    arcpy.AddMessage("{}| {}".format(clock(), x))
    arcpy.AddMessage("=================================================================")

def msgMinor(x):
    arcpy.AddMessage(".")
    arcpy.AddMessage("{}: {}".format(clock(), x))

def msgWarn(x, phaseCurr=None):
    # if phaseCurr == None:
    #     phaseCurr = phase
    arcpy.AddMessage("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    arcpy.AddMessage("!                  WARNING ERROR!                          !")
    arcpy.AddMessage("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    arcpy.AddMessage("{}| {}".format(clock(), x))
    arcpy.AddMessage("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

    
def getFiles(input_directory, file_extension):
    '''
    input a directory and file extension, return a list of the collection and the file type
    '''
    list_files = []

    for root, dirnames, filenames in os.walk(input_directory):
            for filename in fnmatch.filter(filenames, file_extension):
                file_path = os.path.normpath(os.path.join(root, filename))
                file_name = os.path.basename(file_path[:-4])
                collection = file_path.split(os.sep)[-3].lower()
                mosaic = collection.replace("-", "_").lower()
                list_files.append([file_path, file_name, collection, mosaic])

    return(tuple(list_files))

# list of regular expressions to pull metadata
listREs = [
# when NU is found, stop at a space or comma or newline
'(?:NU=)(.+?)[\,|\n]+',
# when found CRR > Stop at VER or BSB or newline
'(?:CRR\/)(.+?)(VER|BSB)',
# when NA is found, stop at a space or comma or newline
'(?:NA=)(.+?)[\,|\n]+',
# when SC is found, stop at a space or comma or newline
'(?:SC=)(.+?)[\,|\n]+',
# when UN is found, stop at a space or comma or newline
'(?:UN=)(.+?)[\,|\n]+',
# when SD is found, stop at a space or comma or newline
'(?:SD=)(.+?)[\,|\n]+',
# when SE is found, stop at a space or comma or newline
'(?:SE=)(.+?)[\,|\n]+',
# when RE is found, stop at a space or comma or newline
'(?:RE=)(.+?)[\,|\n]+',
# when ED is found, stop at a space or comma or newline
'(?:ED=)(.+?)[\,|\n]+',
# when NE is found, stop at a space or comma or newline
'(?:NE=)(.+?)[\,|\n]+',
# when ND is found, stop at a space or comma or newline
'(?:ND=)(.+?)[\,|\n]+'
]

# list of field names in computer speak and english (field name/alias)
listFields = [
["NU", "Chart Number", "TEXT"],
["CRR", "Copyright", "TEXT"],
["NA", "Chart Name", "TEXT"],
["SC", "Scale", "LONG"],
["UN", "Units", "TEXT"],
["SD", "Sounding Datum", "TEXT"],
["SE", "Source Edition", "TEXT"],
["RE", "Raster Edition", "TEXT"],
["ED", "Chart Edition", "TEXT"],
["NE", "NTM Edition", "TEXT"],
["ND", "NTM Date", "TEXT"]
]

if boolDEBUG == "Yes":
    debug = True
elif boolDEBUG == "No":
    debug = False
else:
    pass
if debug == True: msgMajor("!!! DEBUGGING ENABLED - CONSOLE LOG WILL BE EXPANSIVE !!!")

arcpy.env.workspace = dirGDB
arcpy.env.overwriteOutput = True

rn =  timeCalc()

directoryDecollared = os.path.normpath(
    os.path.join(directoryDecollared, tifFolderName)
    )

tempScratch = "{}\{}".format(tempDir, "tempScratch")

if os.path.isdir(tempScratch):
    # kill the old folder
    try:
        shutil.rmtree(tempScratch)
        msg("Previous Temp Directory deleted...")
    except OSError:
        pass

    # make the new temp folder
    try:
        os.mkdir(tempScratch)
    except OSError:
        pass
    except WindowsError:
        pass
    # and throw a database in it
    tempGDB = arcpy.CreateFileGDB_management(tempScratch, "Temp.gdb")
    msg("Created new temp dir @ location: {}".format(tempScratch))

else:
    # if it doesn't exist there, create the folder and our database
    os.mkdir(tempScratch)
    tempGDB = arcpy.CreateFileGDB_management(tempScratch, "Temp.gdb")
    msg("Created new temp dir @ location: {}".format(tempScratch))

listMosaics = sorted(arcpy.ListDatasets(mosaicFilter, "Mosaic"))
msgMinor("Mosaics found in Database: {}".format(listMosaics))

kapFiles = sorted(getFiles(dirKAPS, "*.KAP"))
msgMinor("KAP Files Found: {}".format(len(kapFiles)))

# build the folder structure
collections = [c[2] for c in kapFiles]
for collection in collections:
    collectionFolder = os.path.normpath(os.path.join(
        directoryDecollared, collection, "BSBCHART"
        ))
    if not os.path.isdir(collectionFolder): msg(
        "Creating folder {}".format(collectionFolder)
        )
    if not os.path.isdir(collectionFolder): os.makedirs(
        collectionFolder
        )

# check for KAPs that aren't updated
existingUpdatedCharts = {}

# don't update existing charts
chartsToSkip = []

##   C A L C U L A T E   W O R K L O A D   ##

for mosaic in listMosaics:
    # get the file paths if they match the raster
    kapImportsCheck = [kap for kap in kapFiles if kap[3] == mosaic]
    mosaicFP = "{}/Footprint".format(mosaic)
    try:
        try:
            mosaicCursorCheck = arcpy.da.SearchCursor(mosaic, ["Name", "RE"])
        except TypeError:
            mosaicCursorCheck = arcpy.da.SearchCursor(mosaicFP, ["Name", "RE"])
        existingUpdatedCharts[mosaic] = [r for r in mosaicCursorCheck]
    except RuntimeError:
        # if a mosiac is missing the Name or ED field it'll shit the bed
        pass
    
    chartAndEdition = []
    
    for kap in kapImportsCheck:
        tempStringCheck = ""
        with open(kap[0], encoding="ANSI") as okap:
            for lines in range(100):
                tempStringCheck = tempStringCheck + okap.readline()
        kapMetadata = []
        shortListREs = [listREs[0], listREs[7]]
        for expression in shortListREs:
            match = re.search(expression, tempStringCheck, flags=re.DOTALL)
            try:
                # remove those shitty \n and \r newlines as a new var called cleanMatch
                cleanMatch = re.sub(r"\r?\n", "", match.group(1))
                # lets throw out excessive spacing too!  and tabs!  and commas!  gtfo!
                cleanMatch = re.sub(r"(\,|\t|\s\s\s)", "", cleanMatch)
                # write that bad boy to the kapMetadata list
                kapMetadata.append(cleanMatch)
            except:
                # append the error or lack of a value as "NULL"
                kapMetadata.append(r"NoData")
        # now push all the metadata to the chartAndEdition list
        chartAndEdition.append(kapMetadata)
    try:
        for chart in chartAndEdition:
            for existingChart in existingUpdatedCharts[mosaic]:
                # if the chart name, and chart edition match
                if chart[0] == existingChart[0] and chart[1] == existingChart[1]:
                    chartsToSkip.append(existingChart[0])
        chartsToSkip = sorted(chartsToSkip)
    except KeyError:
        pass
    except IndexError:
        pass
    
    del mosaicCursorCheck

# remove existing updated charts from workload
kapFilesToProcess = []
for chart in kapFiles:
    if chart[1] not in chartsToSkip: kapFilesToProcess.append(chart)        

msgMinor("KAP files that were previously decollared and are the latest release: {}".format(len(chartsToSkip)))

if kapFilesToProcess == 0: msgMinor("No KAP Files to process - all mosaics up to date...")
if kapFilesToProcess != 0: msgMinor("KAP files to decollar: {}".format(len(kapFilesToProcess)))

kapCounter = len(kapFilesToProcess)
errorCharts = []

##   P R O C E S S I N G   ##

for mosaic in listMosaics:
        
    # get mosaic field data and open a cursor in the footprint to write records
    # get the fields from the mosaic to check what's missing and needs to be added
    mosaicFields = [field.name for field in arcpy.ListFields(mosaic)]
    # for field in our list of CHS fields
    msgMinor("Ensuring all fields are created...")
    for field in listFields:
        # if it"s not in our list of mosaic fields
        if field[0] not in mosaicFields:
            if debug: msgMinor("**Field {} missing, adding...".format(field[1]))
            arcpy.AddField_management(mosaic, field[0], field[2], field_alias=field[1])
    listOfFields = [field[0] for field in listFields]
    listOfFields.insert(0, "Name")
    if debug: msgMinor("**Fields to compare in mosaic: {}".format(listOfFields))

    finalTifDirectory = os.path.normpath(
            os.path.join(
                directoryDecollared,
                mosaic.replace("_", "-"),
                "BSBCHART",
                )
            )
    
    tempTifDir = os.path.join(tempScratch, "tempTIF")
    
    if os.path.isdir(tempTifDir):
        pass
    else:
        os.mkdir(tempTifDir)

    # get a list of charts for this mosaic
    chartIterator = [kap for kap in kapFilesToProcess if kap[3] == mosaic]
    
    msgMinor("Charts to process for Mosaic {}: {}".format(mosaic, len(chartIterator)))
    
    if len(chartIterator) == 0:
        continue
    
    for kap in chartIterator:            
 
        ##   D E C O L L A R   B E G I N S   ##

        msgMajor("{}/{} remaining to process on Mosaic: {}.".format(kapCounter, len(kapFilesToProcess), mosaic))
        msgMinor("Chart Details:\nDirectory: {}\nName: {}\nCollection: {} \nMosaic: {}".format(kap[0], kap[1], kap[2], kap[3]))
        kapCounter = kapCounter - 1
    
        msgMinor("Decollaring Chart: {}".format(kap[1]))
        arcpy.RasterToOtherFormat_conversion(kap[0], tempTifDir, "TIFF")
        time.sleep(3)
        msgMinor("Converted {} to TIF @ {}".format(kap[1], tempTifDir))
        tifFileName = kap[1] + ".TIF"
        tempTifPath = os.path.join(tempTifDir, tifFileName)
        msgMinor("TIF {} Created @ {}".format(tifFileName, tempTifPath))
        coord = []
        msgMinor("Reading: ...{}".format(kap[0][-26:]))
        # string that keeps adding line after line in the KAP file until it finds 
        # DTM (the line right after the surround)
        tempString = ""
        # [with open()] each KAP file in "read text" mode, as okap
        with open(kap[0], encoding="ANSI") as okap:
            # until we readline to DTM/ (the line after the PLY/ list)
            while tempString[:4] != r"DTM/":
                tempString = okap.readline()
                # !!!unless it"s PLY/X!!! (a series of xy coords or polygon)
                if tempString[:3] == "PLY":
                    # add the temp string with edits to the temp list
                    coord.append(tempString[:-2].split(",")[1:])

        listPoints = []
        if debug: msgMinor(str("XY Points of the collar shapefile:"))
        for xy in coord:
            # xyint-eger is an Esri "map" object, a float with the xy coords...
            xyint = list(map(float, xy))
            # x will be the second coord
            x = xyint[1]
            # y will be the first coord
            y = xyint[0]
            # add this xy to a point list
            listPoints.append(arcpy.Point(x, y))
            if debug: msg(str("{}, {}".format(x, y)))
        # add the first coord again to close the polygon
        listPoints.append(listPoints[0])
        # arcpy create an array of the above points
        array = arcpy.Array(listPoints)
        # polygon is the array
        polygon = arcpy.Polygon(array)
        # coordinate system is WGS 84 (geographic)
        cSystem = arcpy.SpatialReference(4326)

        msgMinor("Coordinate system of KAP file: {}".format(cSystem.name))
        msgMinor("Coordinate system of Collar: {}".format(cSystem.name))
        msgMinor("Creating temp shapefile of {} for extent...".format(kap[1]))
        # create feature class @...
        collar = arcpy.CreateFeatureclass_management(
            # temp
            tempScratch,
            # called tempFC (we're in a loop so it'll reset)
            "tempFC",
            # it"s a polygon
            "POLYGON",
            # blank var
            "",
            # disabled
            "DISABLED",
            # disabled (don"t worry about it, Z vals)
            "DISABLED",
            # our previously designated WGS84 Geographic coord system
            cSystem)
        # in our new FC in memory create a pointer
        cursor = arcpy.da.InsertCursor(collar, ["SHAPE@"])
        # with the pointer insert each row of our array
        cursor.insertRow([polygon])
        # then delete the cursor
        del cursor
        d = arcpy.Describe(tempTifPath)
        xmin, ymin, xmax, ymax = d.extent.XMin, d.extent.YMin, d.extent.XMax, d.extent.YMax
        f = arcpy.Describe(collar)
        f_xmin, f_ymin, f_xmax, f_ymax = f.extent.XMin, f.extent.YMin, f.extent.XMax, f.extent.YMax
        # print our raster extent for debug checking
        if debug: msgMinor("**Processing Extent of CHS Chart {}: {} {} {} {}".format(
        tifFileName,
        xmin,
        xmax,
        ymin,
        ymax)
        )
        # print our raster extent for debug checking
        if debug: msgMinor("**Processing Extent of the collar: {} {} {} {}".format(
        f_xmin,
        f_xmax,
        f_ymin,
        f_ymax)
        )
        extent = "{} {} {} {}".format(xmin, ymin, xmax, ymax)
        # output TIF is the chart dir and filename in TIF format (slice removes .KAP)
        finalOutputTif = "{}\\{}.tif".format(finalTifDirectory, kap[1])
        if debug: msgMinor("TIF Export {}".format(finalOutputTif))
        msgMinor("Clipping TIF...")
        # arcpy clip raster
        if str(f_xmin) != "nan":
            try:
                arcpy.Clip_management(
                tempTifPath,
                extent,
                finalOutputTif,
                collar,
                "250",
                # we"re clipping based on the feature class
                "ClippingGeometry",
                # this is on by default
                "NO_MAINTAIN_EXTENT"
                )
            
            except:
                errorCharts.append(kap[0])
                msgWarn("Issue working with chart {}".format(kap[0]))
                msg("This issue is rare but can be caused with errors")
                msg("while copying the chart.  This chart is being logged")
                msg("and you can verify each chart after the")
                msg("script completes.")
                        
        else:
            msgWarn('Error with chart: {}'.format(kap[0][-26:]))
            errorCharts.append('{}'.format(kap[0]))                                                           
            arcpy.RasterToOtherFormat_conversion(kap[0], finalTifDirectory, "TIFF")
                    
        msgMinor("Chart {} decollared!".format(kap[1]))
        
        msgMinor("Deleting temp files...")

        tif = "{}\\{}{}".format(finalTifDirectory, kap[1], ".TIF")

        try:
            msgMinor("Adding TIF:")
            msg("{}".format(tif))
            arcpy.management.AddRastersToMosaicDataset(
            mosaic,
            "Raster Dataset",
            tif,
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "SUBFOLDERS",
            "OVERWRITE_DUPLICATES"
            )
        except:
            if debug: msg("**Adding TIF {} to Mosaic {}...".format(tif, mosaic))
            arcpy.management.AddRastersToMosaicDataset(
            mosaic,
            "Raster Dataset",
            tif
            )
            

        ##       D E C O L L A R   E N D S       ##
        ###########################################
        ##   T I F   I M P O R T   B E G I N S   ##

        msgMinor("Adding chart {} to mosaic...".format(kap[1]))
        try:
            arcpy.management.AddRastersToMosaicDataset(
            mosaic,
            "Raster Dataset",
            tif,
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "SUBFOLDERS",
            "OVERWRITE_DUPLICATES"
            )
        except:
            arcpy.management.AddRastersToMosaicDataset(
            mosaic,
            "Raster Dataset",
            tif
            )
            
        ##          T I F   I M P O R T   E N D S          ##
        #####################################################
        ##   M E T A D A T A   U P D A T E   B E G I N S   ##
        
        msg("Parsing {}.KAP for Metadata".format(kap[1]))
        tempString = ""
        with open(kap[0], encoding="ANSI") as okap:
            for lines in range(100):
                tempString = tempString + okap.readline()
        listKAPMetadata = []
        for expression in listREs:
            match = re.search(expression, tempString, flags=re.DOTALL)
            try:
                # remove those icky \n and \r newlines as a new var called cleanMatch
                cleanMatch = re.sub(r"\r?\n", "", match.group(1))
                # lets throw out excessive spacing too!  and tabs!  and commas!  out!
                cleanMatch = re.sub(r"(\,|\t|\s\s\s)", "", cleanMatch)
                # write that bad boy to the listKAPMetadata list
                listKAPMetadata.append(cleanMatch)
            except:
                # append the error or lack of a value as "NULL"
                listKAPMetadata.append(r"NoData")
        listKAPMetadata.insert(0, kap[1])
        
        msgMinor("Metadata found:")
        for metadataValue in listKAPMetadata:
            msg(metadataValue)
        
        mosaicFP = "{}/Footprint".format(mosaic)

        try:
            # create an update cursor to parse the rows and make changes, NOT join fields as that makes numerous extra fields...
            cursorMosaic = arcpy.da.UpdateCursor(mosaic, listOfFields)
        except TypeError:
            cursorMosaic = arcpy.da.UpdateCursor(mosaicFP, listOfFields)
        
        # for row in the mosaic
        for row in cursorMosaic:
            if str(row[0]) == str(listKAPMetadata[0]):
                msg("Updating metadata...")
                for i in range(1, 12):
                    row[i] = listKAPMetadata[i]
                cursorMosaic.updateRow(row)
                del cursorMosaic
                break 
        """    
        except arcpy.ExecuteError:
            msgMinor("Due to a failure, removing last added raster...")
            arcpy.RemoveRastersFromMosaicDataset_management(mosaic, "Name='{}'".format(str(kap[1])))            
            if os.path.exists(finalOutputTif):
                arcpy.Delete_management(finalOutputTif)
            msg("Removal successful.")
        """
        
        ##   M E T A D A T A   U P D A T E   E N D S   ##
        
    if debug: msgMinor("**Building Foorprints...")
    arcpy.BuildFootprints_management(
        mosaic,
        "#",
        "RADIOMETRY",
        1,
        255,
        "#",
        -400,
        "NO_MAINTAIN_EDGES",
        "SKIP_DERIVED_IMAGES",
        "UPDATE_BOUNDARY",
        2000,
        100,
        "NONE"
        )
        
try:
    if len(errorCharts) != 0:
        msgMajor("Errors with the following charts:")
        for x in errorCharts:
            msg(x)
except NameError:
    pass