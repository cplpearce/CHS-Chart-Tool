# Verison: 0.2b.1
import csv                                                                  # output into csv
import os                                                                   # for os.walk and pathing
import re                                                                   # for metadata tag snatching
import fnmatch                                                              # filename match
import datetime                                                             # time 'yo              
import arcpy                                                                # table_to_table
import Tkinter, tkFileDialog                                                # for file dialogs

time.sleep(.5)
print('')
time.sleep(.5)
print('')
time.sleep(.5)
print('')
print('####################################################')               # flash and pizaz!
time.sleep(.1)    
print(' ______     __  __     __     __    __     ______    ') 
time.sleep(.1)  
print('/\  ___\   /\ \_\ \   /\ \   /\ "-./  \   /\  __ \   ')
time.sleep(.1)  
print('\ \ \____  \ \  __ \  \ \ \  \ \ \-./\ \  \ \ \_\ \  ')
time.sleep(.1)  
print(' \ \_____\  \ \_\ \_\  \ \_\  \ \_\ \ \_\  \ \_____\ ')
time.sleep(.1)  
print('  \/_____/   \/_/\/_/   \/_/   \/_/  \/_/   \/_____/ ')      
time.sleep(.1)                       
print('')     
print('####################################################')
time.sleep(1)   
print(' HYDROGRAPHIC  CHART  METADATA  SCRAPER  WRITTEN IN ')
print(' PYTHON   2.7  SCANS A DIRECTORY FOR ALL .KAP FILES ')
print(' STRIPS   &  WRITES  ALL  METADATA  TO  A  CSV   AT ')
print(' THE ROOT OF THE  SCRIPT AND CONVERTS IT TO A DBASE ')
print(' TABLE - THEN  JOINS IT  TO  A  FIELD  IN  YOUR GDB ')
print('####################################################')
time.sleep(.5)
print('')
time.sleep(.5)
print('')


countKAPs = 0                                                               # count of all KAPs, pre processing
countRecords = 0                                                            # count the records processed                                                           # set a filename var
    
root = Tkinter.Tk()                                                         # tkinter loads with a window/GUI, we need to load it...
root.withdraw()                                                             # and hide it, withdraw == hide

def whatstheplan():                                                         # XXXXX  PROMPUT USER INPUT  XXXXX
    print('')
    print('Choose your task: ')
    print('    a) Update Nautical Chart Metadata on the SDE')
    print('    b) Decollar a Chart Directory (*.KAP)')
    print('    c) Update SDE Chart Mosaics With New Charts')
    print('')
    userChoice = raw_input('    (a), (b), or (c): ')
    while userChoice.lower() not in ['a', 'b', 'c']:
        print('')
        time.sleep(.1)
        print('')
        time.sleep(.1)
        print('')
        time.sleep(.1)                      
        print('Party foul, [{}] is not a correct input'.format(userChoice))
        print('')
        print('Choose your task: ')
        print('    a) Update Nautical Chart Metadata on the SDE')
        print('    b) Decollar a Chart Directory (*.KAP)')
        print('    c) Update SDE Chart Mosaics With New Charts')
        print('')
        userChoice = raw_input('    (a), (b), or (c): ')
    else:
        if userChoice.lower() == 'a':
            processMetadata()                                               # lets get the metadata!
        elif userChoice.lower() == 'b':
            decollarCharts()                                                # lets decollar the charts!
        elif userChoice.lower() == 'c':
            updateMosaics()                                                 # lets update the mosaics!
    print('')
    time.sleep(.5)
    print('')
    time.sleep(.5)
    print('')
    time.sleep(.5) 
    
def processMetadata():                                                      # XXXXX  GET CHART METADATA  XXXXX

    os.system('cls')
    print('You have selected [Update Nautical Chart Metadata on the SDE]')
    print('')
    print('Please select target directory containing .KAP files')           # prompt the user
    time.sleep(2)
    chartDirectory = tkFileDialog.askdirectory()                            # get the chart directory
    print('This may take some time, please be patient.')
    time.sleep(1)                                                           # pause

    dictMetadata = {}                                                       # metadata to be written to csv
    rn = datetime.datetime.now().strftime('%y%m%d')                         # get the date time group as 'rn' (right now)   
    
    
    # <========= this is your SDE connection - if it ever changes, change this var! =========>
    dbSDEbase = r'\\mce-geo-gds.mce.mil.ca\sds\10_DATACUBE\HYDROGRAPHIC\CHS\CHS on DATACUBE_RASTER.sde'

    arcpy.env.overwriteOutput = True                                        # overwrite old data with arcpy tools
    arcpy.env.scratchWorkspace = r'in_memory'                               # write a gdb to in_memory
    arcpy.env.workspace = dbSDEbase                                         # set the SDE as our workspace
    scratchGDB = arcpy.env.scratchGDB                                       # write to the scratch gdb
    tempGDBdir = 'in_memory/tempGDB'                                        # declare its location
    
    listSDEMosaics = arcpy.ListDatasets('*CHS*', 'Mosaic')                  # get all the CHS datasets in the SDE

    dictTags = {                                                            # list of keys to be RE'd over all the KAP files
    'CRR': '',                                                              # copyright
    'NA': '',                                                               # ?
    'NU': '',                                                               # ?
    'SC': '',                                                               # ?
    'UN': '',                                                               # ?
    'SD': '',                                                               # ?
    'SE': '',                                                               # ?
    'RE': '',                                                               # ?
    'ED': '',                                                               # ?
    'NE': '',                                                               # ?
    'ND': ''                                                                # ?
    }

    listREs = [                                                             # list of regular expressions to pull metadata
    r'(?:CRR/)(.+?)(VER|BSB)',                                              # ?
    r'(?:NA=)(.+?)[\,|\n]+',                                                # ?
    r'(?:NU=)(.+?)[\,|\n]+',                                                # ?
    r'(?:SC=)(.+?)[\,|\n]+',                                                # ?
    r'(?:UN=)(.+?)[\,|\n]+',                                                # ?
    r'(?:SD=)(.+?)[\,|\n]+',                                                # ?
    r'(?:SE=)(.+?)[\,|\n]+',                                                # ?
    r'(?:RE=)(.+?)[\,|\n]+',                                                # ?
    r'(?:ED=)(.+?)[\,|\n]+',                                                # ?
    r'(?:NE=)(.+?)[\,|\n]+',                                                # ?
    r'(?:ND=)(.+?)[\,|\n]+'                                                 # ?
    ]

    def getKAP(chartDirectory):
        listKAPs = []                                                       # a list for *all* the KAP files, duplicates included
        listUniqueKAPS = []                                                 # a list of the unique KAP files
        global countKAPs                                                    # mention our global var countKAPs for the user
            
        for root, dirnames, filenames in os.walk(chartDirectory):           # for here, with dir names, walk thru each dir for files (dir = input var)
            for filename in fnmatch.filter(filenames, r'*.KAP'):            # for .KAP files
                countKAPs += 1                                              # count the KAP files found
                if filename in listUniqueKAPS:                              # for pre-existing (duplicates)...
                    pass                                                    # pass
                else:   
                    listKAPs.append(os.path.join(root, filename))           # add the found KAP files to the listKAPs list
                    listUniqueKAPS.append(filename)                         # note the unique filenale
    
    
        getLines(listKAPs)                                                  # get dem lines bro
            
    def getLines(KAPs):                                                     # open the KAP file, get the KAP chart name and first 25 lines and send it to getTags(x,y) 
        for kap in KAPs:                                                    # for the KAPs in listKAPs
            tempString = ''                                                 # concatinate our ten strings together
            with open(kap, 'rt') as okap:                                   # [with open()] each KAP file as 'read text' as okap
                for lines in range(25):                                     # read the first ten lines
                    tempString = tempString + okap.readline().decode(       # grab the lines and add them to the tempString var
                    'ascii',
                    errors='ignore'
                    )                                                       
                                        
            getTags(os.path.basename(kap), tempString)                      # run the getTags function, BUT key in the KAP by filename, not path + filename
            
    def getTags(kap, tempString):                                           # this function pulls the metadata tags from tempString and cleans them up!
        listKAPMetadata = []                                                # metadata of each particular kap that resets on iteration
        for expression in listREs:                                          # iterate over our prewritten regex statements
            match = re.search(expression, tempString, flags=re.DOTALL)      # matching each against tempString with the DOTALL flag

            try:                                                            # if match == TRUE, try         
                cleanMatch = re.sub(r'\r?\n', '', match.group(1))           # remove those icky \n and \r newlines as a new var called cleanMatch
                cleanMatch = re.sub(r'(\,|\t|\s\s\s)', '', cleanMatch)      # lets throw out excessive spacing too!  and tabs!  and commas!  out!
                listKAPMetadata.append(cleanMatch)                          # write that bad boy to the listKAPMetadata list
            except:                                                         # uh-oh
                listKAPMetadata.append(r'NULL')                             # append the error or lack of a value as 'NULL'
                
            dictMetadata[kap] = listKAPMetadata                             # now push all the metadata to the dictMetadata dictionary, key'd by KAP file
            
        writeTags(dictMetadata)                                             # write the metadata to dictMetadata
                
    def writeTags(dictMetadata):                                            # this function pushes all the tags into a list for writing to the new csv      
            
        global filename
        filename = 'NauticalChartMetadata-' + str(rn) + '.csv'              # create the filename string
        
        with open(filename, 'wb') as csvFile:                               # begin writing the csv as filename, in workbook mode (mode 'wb' removes double lines)
            writer = csv.writer(csvFile, delimiter = ',')                   # create the csv writer object with a comma delimiter
            headers = (                                                     # list the headers
            'CHART',                                                
            'CRR',
            'NA',
            'NU',
            'SC',
            'UN',
            'SD',
            'SE',
            'RE',
            'ED',
            'NE',
            'ND'
            )                                       
            
            writer.writerow(headers)                                        # write the headers
            
            global countRecords                                             # find our countRecords var
            countRecords += 1                                               # count 'em!
            
            for k, di in dictMetadata.iteritems():                          # for keys (k), and dictionary items (di) in the dictionary dictMetadata

                stringToWrite = k[:-4]                                      # create a string, starting with the kap file name
                for x in di:                                                # for the item (x) in dictionary items (di), 
                    stringToWrite = stringToWrite + ',' + x                 # load the string, and add the new item and a comma
                listWrite = stringToWrite.split(',')                        # split the string by commas (writer iterates, needs a list not a string)
                writer.writerow(listWrite)                                  # write the list!       
            
    def UpdateGDB():
        print('Converting CSV to dBASE table!  Chimo!')                     # update the user
        tableName = 'NCM' + str(rn)                                         # give the dBASE table a name
        tableNameFull = str(scratchGDB + '/' + tableName + '.dbf')          # get the full table name and extension
        print('This may take some time, please be patient.')                # update the user
        print('Converting to dBASE...')                                     # update the user
        arcpy.TableToTable_conversion(filename, scratchGDB, tableName)      # convert it to a dBASE table :D

        print('Adding aliases...')                                          # update the user
        listFields = [                                                      # list of field names in computer speak and english (field name/alias)
        ['CHART', 'Chart Number'],
        ['CRR', 'Copyright'],           
        ['NA', 'Chart Name'],
        ['NU', 'Chart Number'],
        ['SC', 'Scale'],            
        ['UN', 'Units'],
        ['SD', 'Sounding Datum'],
        ['SE', 'Source Edition'],   
        ['RE', 'Raster Edition'],
        ['ED', 'Chart Edition'],                        
        ['NE', 'NTM Edition'],
        ['ND', 'NTM Date']
        ]                               
        
        for field in listFields:                                            # alter the table names!
            arcpy.AlterField_management(                                    # arcpy AlterField
            tableNameFull,                                                  # get the dBASE table name + dir
            field[0],                                                       # look for field X
            field[0],                                                       # rename it, to the same        
            field[1]                                                        # add an alias, as ref'd in listFields
            )                                                                   
        
        for mosaics in listSDEMosaics:                                      # for the mosaics in the SDE
            try:                                                            # try (in case schema issue)
                print('Updating Mosaic: {}'.format(mosaics))                # tell the user which one we're on
                arcpy.JoinField_management(                                 # arcpy join the field (permamnent join)
                mosaics,                                                    # on the mosaics in the SDE
                r'Name',                                                    # match on the mosaic chart field 'Name',
                tableNameFull,                                              # with a dBASE table found here, and
                r'CHART'                                                    # match on the CHART value in the dBASE table
                )
                
            except:
                print('Schema Issue on: {}'.format(mosaics))                # inform user of schema issue
                pass
        pass
    
    getKAP(chartDirectory)                                                  # process those charts!
    UpdateGDB()                                                             # update the SDE!
    
    print('')
    print('Complete!')
    os.system('pause')
    print('')
    print('####################################################')
    print(' Charts Found:     ' + str(countKAPs))
    print(' Charts Processed: ' + str(countRecords))

    if countKAPs > countRecords:
        print('======================================')
        print(' Chart Duplicates: ' + str(countKAPs - countRecords))
        
    print('####################################################')
    print('')
    print('Closing in 10 seconds...')
    time.sleep(5)
    exit

def decollarCharts():                                                       # XXXXX  DECOLLAR      KAPs  XXXXX
    
    print('')
    time.sleep(.5)
    print('Decollaring Chosen...')
    time.sleep(.5)
    print('')
    time.sleep(.5)  
    print('')
    time.sleep(.5)
    print('')
    time.sleep(.5)
    print('')
    print('Please select target directory containing .KAP files')           # prompt the user
    time.sleep(2)
    chartDirectory = tkFileDialog.askdirectory()                            # get the chart directory
    print('')
    time.sleep(.5)
    print('Crawling directory, please be patient.')
    time.sleep(1)                                                           # pause
    print('')
    time.sleep(.5)    
    rn = datetime.datetime.now().strftime('%y%m%d')                         # get the date time group as 'rn' (right now)

    arcpy.env.overwriteOutput = True                                        # overwrite old data with arcpy tools

    countKAPs = 0                                                           # count of all KAPs, pre processing
    countRecords = 0                                                        # count the records processed
        
    def getKAP(dir):
        listKAPs = []                                                       # a list for *all* the KAP files, duplicates included
        listUniqueKAPS = []                                                 # a list of the unique KAP files to skip when itering all KAPs
        global countKAPs                                                    # mention our global var countKAPs for the user
            
        for root, dirnames, filenames in os.walk(dir):                      # for here, with dir names, walk thru each dir for files (dir = input var)
            for filename in fnmatch.filter(filenames, r'*.KAP'):            # for .KAP files
                countKAPs += 1                                              # count the KAP files found
                if filename in listUniqueKAPS:                              # for pre-existing (duplicates)...
                    pass                                                    # pass
                else:   
                    listKAPs.append(os.path.join(root, filename))           # add the found KAP files to the listKAPs list
                    listUniqueKAPS.append(filename)                         # note the unique filenale

        getLines(listKAPs)                                                  # get dem lines bro
        
    def getLines(KAPs):                                                     # open the KAP file, get the coodinate data for the decollaring
        print('Parsing KAP file lines.')
        listCoords = []                                                     # list of coords
        for kap in KAPs:                                                    # for the KAPs in listKAPs
            tempString = ''                                                 # strings placeholder
            tempCoord = [kap]                                               # coords placeholder
            with open(kap, 'rt') as okap:                                   # [with open()] each KAP file as 'read text' as okap
                while tempString[:4] != r'DTM/':                            # until we readline to DTM/
                    tempString = okap.readline().decode(                    # skip useless lines
                    'ascii',
                    errors='ignore'
                    )                                                       
                    if tempString[:3] == 'PLY':                             # unless it's PLY/X
                        tempCoord.append(tempString.split(',')[1:])
                    else:
                        pass
                    
                listCoords.append(tempCoord)   
                               
        clipKAPs(listCoords)                                                # run the clipKAPs function to begin clipping KAPs (duh!)

    def clipKAPs(coords):
    
        print(coords)

        print('')
        
        print('Creating feature classes and clipping.')
        
        print('')
        
        print('Clipping {} KAP files.'.format(len(coords)))
        
        print(len(coords))
        
        for coord in coords:
        
            try:
                coordinates = [coord[1:]]
                print(coord[1:])
                # create polygon
                fc = arcpy.management.CreateFeatureclass(
                'in_memory',
                'POLYGON',
                spatial_reference=4326
                )
                print('1')
                collar = fc[0]
                
                with arcpy.da.InsertCursor(
                collar,
                ['SHAPE@']
                ) as cursor:
                    cursor.insertRow(coordinates)
                print('2')
                extent = arcpy.sa.Raster(coord[0])
                extent = extent.extent
                print('3')
                arcpy.Clip_management(coord[0], extent, 'C:\\clip.tif', collar, '256', 'NONE', 'NO_MAINTAIN_EXTENT')
                print('Clipped!')
                # clip KAPs
            except:
                print('Encountered an error with {}'.format(coord[1]))
            
    
    getKAP(chartDirectory)
        
    # print('')
    # print('Complete!')
    # os.system('pause')
    # print('')
    # print('####################################################')
    # print(' Charts Found:     ' + str(countKAPs))
    # print(' Charts Processed: ' + str(countRecords))

    # if countKAPs > countRecords:
        # print('======================================')
        # print(' Chart Duplicates: ' + str(countKAPs - countRecords))
        
    # print('####################################################')
    # print('')
    # print('Closing in 10 seconds...')
    # time.sleep(5)
    # exit
    
def updateMosaics():                                                        # XXXXX  UPDATE SDE MOSACIS  XXXXX
    pass
    
whatstheplan()                                                              # start this bad boi!



