# Version: 0.5b.1
import csv                                                                                                      # output into csv
import os                                                                                                       # for os.walk and pathing
import re                                                                                                       # for metadata tag snatching
import fnmatch                                                                                                  # filename match
import datetime                                                                                                 # time 'yo
import arcpy                                                                                                    # table_to_table
import Tkinter, tkFileDialog                                                                                    # for file dialogs

time.sleep(.2)                                                                                                  # sleep to wow the user
print('')                                                                                                       # blank line
time.sleep(.2)                                                                                                  # sleep to wow the user
print('')                                                                                                       # blank line
time.sleep(.2)                                                                                                  # sleep to wow the user
print('')                                                                                                       # blank line
print('#################################################### ')                                                  # flash and pizaz!
time.sleep(.1)                                                                                                  #
print(' ______     __  __     __     __    __     ______    ')                                                  #  ______     __  __     __     __    __     ______
time.sleep(.1)                                                                                                  # /\  ___\   /\ \_\ \   /\ \   /\ "-./  \   /\  __ \
print('/\  ___\   /\ \_\ \   /\ \   /\ "-./  \   /\  __ \   ')                                                  # \ \ \____  \ \  __ \  \ \ \  \ \ \-./\ \  \ \ \_\ \
time.sleep(.1)                                                                                                  #  \ \_____\  \ \_\ \_\  \ \_\  \ \_\ \ \_\  \ \_____\
print('\ \ \____  \ \  __ \  \ \ \  \ \ \-./\ \  \ \ \_\ \  ')                                                  #   \/_____/   \/_/\/_/   \/_/   \/_/  \/_/   \/_____/
time.sleep(.1)                                                                                                  #
print(' \ \_____\  \ \_\ \_\  \ \_\  \ \_\ \ \_\  \ \_____\ ')                                                  #
time.sleep(.1)                                                                                                  #
print('  \/_____/   \/_/\/_/   \/_/   \/_/  \/_/   \/_____/ ')                                                  #
time.sleep(.1)                                                                                                  #
print('')                                                                                                       # blank line
print('####################################################')                                                   #
time.sleep(1)                                                                                                   #
print('')                                                                                                       # blank line
print(' HYDROGRAPHIC  CHART  TOOL  WRITTEN IN PYTHON   2.7 ')                                                   #
print(' A) DECOLLAR NAUTICAL CHARTS IN  A TARGET DIRECTORY ')                                                   #
print(' B) UPDATE  TARGET   SDE  WITH  DECOLLARED   CHARTS ')                                                   #
print(' C) STRIP  METADATA  FROM .KAPS AND UPDATE THE  SDE ')                                                   #
print('')                                                                                                       # blank space
print('####################################################')                                                   #
time.sleep(.2)                                                                                                  # sleep to wow the user
print('')                                                                                                       # blank line
time.sleep(.2)                                                                                                  # sleep to wow the user
print('')                                                                                                       # blank line

root = Tkinter.Tk()                                                                                             # tkinter loads with a window/GUI, we need to load it...
root.withdraw()                                                                                                 # and hide it, withdraw == hide

def getKAPs():

    listKAPs = []                                                                                               # a list for *all* the KAP files, duplicates included
    listUniqueKAPS = []                                                                                         # a list of the unique KAP files to skip when itering all KAPs
    message('Please select target directory containing .KAP files')                                             # prompt the user
    time.sleep(2)                                                                                               # sleep to let the user read
    chartDirectory = tkFileDialog.askdirectory()                                                                # prompt directory with tkinter
    message('Crawling directory, please be patient.')                                                           # inform user
    for root, dirnames, filenames in os.walk(chartDirectory):                                                   # for here, with dir names, walk thru each dir for files (dir = input var)
        for filename in fnmatch.filter(filenames, r'*.KAP'):                                                    # for .KAP files
            if filename in listUniqueKAPS:                                                                      # for pre-existing (duplicates)...
                pass                                                                                            # pass
            else:
                listKAPs.append(os.path.join(root, filename))                                                   # add the found KAP files to the listKAPs list
                listUniqueKAPS.append(filename)                                                                 # note the unique filenale
    return(listKAPs)

def message(x):
    print('')
    time.sleep(.1)
    print(x)

def whatstheplan():                                                                                             # XXXXX  PROMPUT USER INPUT  XXXXX

    print('')                                                                                                   # begin the choosing
    print('Choose your task: ')                                                                                 # user input begins
    print('    a) Decollar a Chart Directory (*.KAP)')                                                          # decollar charts
    print('    b) Update SDE Chart Mosaics With New Decollared Charts')                                         # update SDE with decollared charts
    print('    c) Update Nautical Chart Metadata on the SDE')                                                   # update SDE with metadata
    print('')                                                                                                   # blank line
    userChoice = raw_input('    (a), (b), or (c): ')                                                            # user choice
    while userChoice.lower() not in ['a', 'b', 'c']:                                                            # lower ther input for conisitency and while: so input is predefined
        print('')                                                                                               # blank space
        time.sleep(.1)                                                                                          # sleep to wow the user
        print('')                                                                                               # blank space
        time.sleep(.1)                                                                                          # sleep to wow the user
        print('')                                                                                               # blank space
        time.sleep(.1)                                                                                          # sleep to wow the user
        print('Error: Incorrect entry, [{}] is not a selectable input'.format(userChoice))                      # if the user is a knob retry
        print('')                                                                                               # blank space
        print('Choose your task: ')                                                                             # second chance at input
        print('    a) Decollar a Chart Directory (*.KAP)')                                                      # decoallr
        print('    b) Update SDE Chart Mosaics With New Decollared Charts')                                     # update charts
        print('    c) Update Nautical Chart Metadata on the SDE')                                               # update metadata
        print('')                                                                                               # blank space
        userChoice = raw_input('    (a), (b), or (c): ')                                                        # ask the user to choose
    else:                                                                                                       # if the user picks a predefined var, run function X
        if userChoice.lower() == 'a':                                                                           # if a
            decollarCharts()                                                                                    # lets decollar the charts!
        elif userChoice.lower() == 'b':                                                                         # if b
            updateMosaics()                                                                                     # lets get the metadata!
        elif userChoice.lower() == 'c':                                                                         # if c
            processMetadata()                                                                                   # lets update the mosaics!

    print(''), time.sleep(.2)                                                                                   # give us some breathing room
    break * 3

def processMetadata():                                                                                          # XXXXX  GET CHART METADATA  XXXXX

    try:                                                                                                        # error checking
        error = 'can\'t initialize script'                                                                      # error message var

        countVars = {                                                                                           # decalre the counts in a mutable dict, as global/local vars are shit on python 2.7
        'countKAPs' : 0,                                                                                        # count of all KAPs, pre processing
        'countComplete' : 0                                                                                     # count the records processed
        }

        message('You have selected [Update Nautical Chart Metadata on the SDE].')                               # update the user

        dictMetadata = {}                                                                                       # metadata to be written to csv
        rn = datetime.datetime.now().strftime('%y%m%d')                                                         # get the date time group as 'rn' (right now)

        # <========= this is your SDE connection - if it ever changes, change this var! =========>
        dbSDEbase = r'\\mce-geo-gds.mce.mil.ca\sds\10_DATACUBE\HYDROGRAPHIC\CHS\CHS on DATACUBE_RASTER.sde'

        arcpy.env.overwriteOutput = True                                                                        # overwrite old data with arcpy tools
        #arcpy.env.scratchWorkspace = r'in_memory'                                                              # write a gdb to in_memory
        arcpy.env.workspace = dbSDEbase                                                                         # set the SDE as our workspace
        scratchGDB = arcpy.env.scratchGDB                                                                       # write to the scratch gdb
        tempGDBdir = 'tempGDB'                                                                                  # declare its location

        listSDEMosaics = arcpy.ListDatasets('*CHS*', 'Mosaic')                                                  # get all the CHS datasets in the SDE

        countMosaicsUpdated = 0                                                                                 # a count for the mosaics updated

        dictTags = {                                                                                            # list of keys to be RE'd over all the KAP files
        'CRR': '',                                                                                              # copyright
        'NA': '',                                                                                               # chart name
        'NU': '',                                                                                               # chart number
        'SC': '',                                                                                               # scale
        'UN': '',                                                                                               # units
        'SD': '',                                                                                               # sounding datum
        'SE': '',                                                                                               # aource edition
        'RE': '',                                                                                               # raster edition
        'ED': '',                                                                                               # chart edition
        'NE': '',                                                                                               # NTM edition
        'ND': ''                                                                                                # NTM date
        }

        # REGEX malarky
        listREs = [                                                                                             # list of regular expressions to pull metadata
        r'(?:CRR/)(.+?)(VER|BSB)',                                                                              # when found CRR > Stop at VER or BSB or newline
        r'(?:NA=)(.+?)[\,|\n]+',                                                                                # when NA is found, stop at a space or comma or newline
        r'(?:NU=)(.+?)[\,|\n]+',                                                                                # when NU is found, stop at a space or comma or newline
        r'(?:SC=)(.+?)[\,|\n]+',                                                                                # when SC is found, stop at a space or comma or newline
        r'(?:UN=)(.+?)[\,|\n]+',                                                                                # when UN is found, stop at a space or comma or newline
        r'(?:SD=)(.+?)[\,|\n]+',                                                                                # when SD is found, stop at a space or comma or newline
        r'(?:SE=)(.+?)[\,|\n]+',                                                                                # when SE is found, stop at a space or comma or newline
        r'(?:RE=)(.+?)[\,|\n]+',                                                                                # when RE is found, stop at a space or comma or newline
        r'(?:ED=)(.+?)[\,|\n]+',                                                                                # when ED is found, stop at a space or comma or newline
        r'(?:NE=)(.+?)[\,|\n]+',                                                                                # when NE is found, stop at a space or comma or newline
        r'(?:ND=)(.+?)[\,|\n]+'                                                                                 # when ND is found, stop at a space or comma or newline
        ]

        error = 'can\'t read the directory - ensure connection is valid or folders named with valid chars.'     # directory os walk issue

        listKAPs = getKAPs()                                                                                    # get the list of .KAP files

        countVars['countKAPs'] = len(listKAPs)                                                                  # count the KAP files found

        # open the KAP file, get the KAP chart name and first 25 lines and send it to getTags(x,y)
        for kap in listKAPs:                                                                                    # for the KAPs in listKAPs

            error = 'can\'t iterate KAP files with REGEX - potentially invalid KAP file: {}.'.format(kap)       # error if kap file is corrupt or misconfigured

            tempString = ''                                                                                     # set a temp string var

            with open(kap, 'rt') as okap:                                                                       # [with open()] each KAP file as 'read text' as okap
                for lines in range(25):                                                                         # read the first 25 lines
                    tempString = tempString + okap.readline().decode(                                           # grab the lines and add them to the tempString var
                    'ascii',
                    errors='ignore'
                    )

            kap = os.path.basename(kap)                                                                         # now that we've got the files, we just need the KAP name

            listKAPMetadata = []                                                                                # metadata of each particular kap that resets on iteration

            for expression in listREs:                                                                          # iterate over our prewritten regex statements
                match = re.search(expression, tempString, flags=re.DOTALL)                                      # matching each against tempString with the DOTALL flag

                try:                                                                                            # if match == TRUE, try
                    cleanMatch = re.sub(r'\r?\n', '', match.group(1))                                           # remove those icky \n and \r newlines as a new var called cleanMatch
                    cleanMatch = re.sub(r'(\,|\t|\s\s\s)', '', cleanMatch)                                      # lets throw out excessive spacing too!  and tabs!  and commas!  out!
                    listKAPMetadata.append(cleanMatch)                                                          # write that bad boy to the listKAPMetadata list
                except:                                                                                         # uh-oh
                    listKAPMetadata.append(r'NULL')                                                             # append the error or lack of a value as 'NULL'

            dictMetadata[kap] = listKAPMetadata                                                                 # now push all the metadata to the dictMetadata dictionary, key'd by KAP file

        error = 'can\'t write file: {} - possibly a permission/directory issue?  Is it open?'                   # write csv error

        filename = 'NauticalChartMetadata-' + str(rn) + '.csv'                                                  # create the filename string

        with open(filename, 'wb') as csvFile:                                                                   # begin writing the csv as filename, in workbook mode (mode 'wb' vs 'w' removes double lines)
            writer = csv.writer(csvFile, delimiter = ',')                                                       # create the csv writer object with a comma delimiter
            headers = (                                                                                         # list the headers
            'CHART',                                                                                            # chart filename number
            'CRR',                                                                                              # copyright
            'NA',                                                                                               # chart name
            'NU',                                                                                               # chart number
            'SC',                                                                                               # scale
            'UN',                                                                                               # units
            'SD',                                                                                               # sounding datum
            'SE',                                                                                               # aource edition
            'RE',                                                                                               # raster edition
            'ED',                                                                                               # chart edition
            'NE',                                                                                               # NTM edition
            'ND'                                                                                                # NTM date
            )

            writer.writerow(headers)                                                                            # write the headers

            for k, di in dictMetadata.iteritems():                                                              # for keys (k), and dictionary items (di) in the dictionary dictMetadata
                countVars['countComplete'] += 1                                                                 # count 'em!
                stringToWrite = k[:-4]                                                                          # create a string, starting with the kap file name
                for x in di:                                                                                    # for the item (x) in dictionary items (di),
                    stringToWrite = stringToWrite + ',' + x                                                     # load the string, and add the new item and a comma
                listWrite = stringToWrite.split(',')                                                            # split the string by commas (writer iterates, needs a list not a string)
                writer.writerow(listWrite)                                                                      # write the list!

        message('Converting CSV to dBASE table!  Chimo!')                                                       # update the user

        tableName = 'NCM' + str(rn)                                                                             # give the dBASE table a name
        tableNameFull = str(scratchGDB + '/' + tableName + '.dbf')                                              # get the full table name and extension
        message('This may take some time, please be patient.')                                                  # update the user
        error = 'can\'t convert csv to dBASE table - I/O error?'                                                # convert table error
        arcpy.TableToTable_conversion(filename, scratchGDB, tableName)                                          # convert it to a dBASE table :D
        message('Adding aliases...')                                                                            # update the user
        listFields = [                                                                                          # list of field names in computer speak and english (field name/alias)
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

        error = 'can\'t alter field names of dBASE file before pairing it with the SDE.'                        # error for updating/altering field names
        for field in listFields:                                                                                # alter the table names!
            arcpy.AlterField_management(                                                                        # arcpy AlterField
            tableNameFull,                                                                                      # get the dBASE table name + dir
            field[0],                                                                                           # look for field X
            field[0],                                                                                           # rename it, to the same
            field[1]                                                                                            # add an alias, as ref'd in listFields
            )

        error = 'can\'t process mosaics - potential arcpy issue, SDE issue, or KAP file issue...  Sorry.'       # it could be anything at this point

        try:
            for mosaics in listSDEMosaics:                                                                      # for the mosaics in the SDE
                try:                                                                                            # try (in case schema issue)
                    print('Updating Mosaic: {}'.format(mosaics))                                                # tell the user which one we're on
                    arcpy.JoinField_management(                                                                 # arcpy join the field (permamnent join)
                    mosaics,                                                                                    # on the mosaics in the SDE
                    r'Name',                                                                                    # match on the mosaic chart field 'Name',
                    tableNameFull,                                                                              # with a dBASE table found here, and
                    r'CHART'                                                                                    # match on the CHART value in the dBASE table
                    )
                    time.sleep(1)                                                                               # pause
                    countMosaicsUpdated += 1                                                                    # count updated mosaics
                    print('')                                                                                   # pause

                except TypeError:
                    print('Schema Issue on: {}'.format(mosaics))                                                # inform user of schema issue
                    time.sleep(1)                                                                               # pause
                    print('')                                                                                   # pause
                    pass

        except TypeError:                                                                                       # you failed, here's why
            message('Error: Couldn\'t connect to SDE!')                                                         # inform the user SDE connection issue
            message('This portion of the Nautical Chart tool is for the MCE LAN network!')                      # inform user network this tool should run on
            pass

    except :
        message('Error: {}'.format(error))                                                                      # print error

    if arcpy.Exists(scratchGDB):                                                                                # BEGONE SCRATCH GDB
        arcpy.Delete_management(scratchGDB)
    if os.path.isdir(scratchGDB):                                                                               # BEGONE HARDER IF YOU WON'T GO THE LEGIT WAY!
        shutil.rmtree(scratchGDB)

    message('Finished.')
    os.system('pause')
    print('')
    print('####################################################')
    print(' Charts Found:        {}'.format(str(countVars['countKAPs'])))                                       # tell user charts found
    print(' Charts Processed:    {}'.format(str(countVars['countComplete'])))                                   # tell user charts processed

    print(' SDE Mosaics Updated: {}'.format(str(countMosaicsUpdated)))                                          # tell user mosaics updated

    if countVars['countKAPs'] > countVars['countComplete']:                                                     # if there were more charts found than processed alert the user
        print('======================================')
        print(' Chart Duplicates: {}'.format(
        str(countVars['countKAPs'] - countVars['countComplete'])))                                              # and if there were any duplicates

    print('####################################################')
    print('')
    print('Closing in 5 seconds...')
    time.sleep(5)
    exit

def decollarCharts():                                                                                           # XXXXX  DECOLLAR      KAPs  XXXXX
    countVars = {
    'countKAPs' : 0,                                                                                            # count of all KAPs, pre processing
    'countComplete' : 0                                                                                         # count the records processed
    }

    print('')
    print('You have selected [Decollar a Chart Directory (*.KAP)]')
    print('')
    print('')
    print('')
    print('')
    print('Please select target directory containing .KAP files')                                               # prompt the user
    chartDirectory = tkFileDialog.askdirectory()                                                                # get the chart directory
    print('')
    print('Please select target directory to save decollared .KAP files')
    time.sleep(2)
    decollarDirectory = tkFileDialog.askdirectory()
    print('')
    print('Crawling directory, please be patient.')                                                             # pause

    rn = datetime.datetime.now().strftime('%y%m%d')                                                             # get the date time group as 'rn' (right now)

    arcpy.env.overwriteOutput = True                                                                            # overwrite old data with arcpy tools

    def getKAP(dir):

        listKAPs = []                                                                                           # a list for *all* the KAP files, duplicates included
        listUniqueKAPS = []                                                                                     # a list of the unique KAP files to skip when itering all KAPs

        for root, dirnames, filenames in os.walk(dir):                                                          # for here, with dir names, walk thru each dir for files (dir = input var)
            for filename in fnmatch.filter(filenames, r'*.KAP'):                                                # for .KAP files
                countVars['countKAPs'] += 1                                                                     # count the KAP files found
                if filename in listUniqueKAPS:                                                                  # for pre-existing (duplicates)...
                    pass                                                                                        # pass
                else:
                    listKAPs.append(os.path.join(root, filename))                                               # add the found KAP files to the listKAPs list
                    listUniqueKAPS.append(filename)                                                             # note the unique filenale

        getLines(listKAPs)                                                                                      # get dem lines bro

    def getLines(KAPs):                                                                                         # open the KAP file, get the coodinate data for the decollaring
        print('')                                                                                               # blank line
        print('Parsing KAP file lines.')                                                                        # inform user of progress
        listCoords = []                                                                                         # declare our list of coords
        for kap in KAPs:                                                                                        # for the KAPs in listKAPs
            tempString = ''                                                                                     # strings placeholder
            tempCoord = [kap]                                                                                   # coords placeholder
            with open(kap, 'rt') as okap:                                                                       # [with open()] each KAP file as 'read text' as okap
                while tempString[:4] != r'DTM/':                                                                # until we readline to DTM/ (the line after the PLY/ list)
                    tempString = okap.readline().decode(                                                        # skip useless lines
                    'ascii',                                                                                    # formatted in ascii
                    errors='ignore'                                                                             # if a symbol isn't correct, ignore
                    )
                    if tempString[:3] == 'PLY':                                                                 # !!!unless it's PLY/X!!! (a series of xy coords or polygon)
                        tempCoord.append(tempString[:-2].split(',')[1:])                                        # add the temp string with edits to the temp list

                listCoords.append(tempCoord)                                                                    # add our list of unique chart coordinates to the list

        clipKAPs(listCoords)                                                                                    # run the clipKAPs function to begin clipping KAPs (duh!)

    def clipKAPs(coords):                                                                                       # begin the great decollaring

        print('')                                                                                               # blank line
        print('Creating feature classes and clipping {} KAP files'.format(len(coords)))                         # inform user of progress and amount of charts to process

        for coord in coords:                                                                                    # for coordinates found

            basePath, baseName = os.path.split(coord[0])                                                        # create basepath/name, by os.path splitting

            error = ''                                                                                          # our own little error reporter!

            try:                                                                                                # try because shit goes awry and we can't always remain on top
                error = 'parsing directory of the KAP file.  Check the path is windows compliant'               # we couldn't figure out the directory string
                commonPath = os.path.join(                                                                      # common path is our chart folder, twice up...
                str(coord[0]).split(os.path.sep)[-3],                                                           # ie. Charts\Atl001\BSB\Chart.KAP...
                str(coord[0]).split(os.path.sep)[-2]                                                            # get only the Atl1001 and BSB names!
                )

                rn = datetime.datetime.now().strftime('%y%m%d')                                                 # get the date time group as 'rn' (right now)

                error = 'creating string for new directory.  Try looking for bad directory characters.'         # we couldn't
                newChartDir = os.path.join(                                                                     # the new chart dir is the user input...
                '{}/DECOLLAR-{}/{}'.format(                                                                     # userinput\DECOLLAR + date + common path
                decollarDirectory,
                rn,                                                                                             # 'rn' (right now)
                commonPath))                                                                                    # last two folders, reverse recursive

                error = 'trying to create a new directory.  It may exist but that wasn\t the problem.'          # something went wrong making the new directory
                try:                                                                                            # try making a new directory
                    os.makedirs(newChartDir)                                                                    # make dirs allows recursive
                    print('')                                                                                   # blank line
                    print('Creating: {}'.format(newChartDir))                                                  # inform user of new directory being made
                except WindowsError:                                                                            # folder already exists!
                    pass                                                                                        # if the chart exists windows has a personal issue with it

                listPoints = []                                                                                 # declare the list points list

                error = ' iterating on the KAP PLY\ lines threw an error.  KAP may be corrupt.'                 # iterating coordinates error
                for xy in coord[1:]:                                                                            # for the xy data in our KAP file (tagged with PLY)...
                    xyint = map(float, xy)                                                                      # xyint-eger is an Esri 'map' object, a float with the xy coords...
                    x = xyint[1]                                                                                # x will be the second coord
                    y = xyint[0]                                                                                # y will be the first coord
                    listPoints.append(arcpy.Point(x, y))                                                        # add this xy to a point list

                error = ' creating an Arcpy array with the given KAP PLY/ data.  Check the KAP for errors.'     # can't create an array - KAP error?
                array = arcpy.Array(listPoints)                                                                 # arcpy create an array of the above points

                cSystem = 'Geographic Coordinate Systems/World/WGS 1984'                                        # coordinate system is WGS 84 (geographic)
                polygon = arcpy.Polygon(array)                                                                  # polygon is the array
                error = ' creating the new feature class.  May be an issue with in_memory data or overwriting.' # inform user if the featureclass can't be made
                collar = arcpy.CreateFeatureclass_management(                                                   # create feature class @...
                'in_memory',                                                                                    # in_memory (quick, erased when done)
                'tempFC',                                                                                       # called tempFC (we're in a loop so it'll reset)
                'POLYGON',                                                                                      # it's a polygon
                '',                                                                                             # blank var
                'DISABLED',                                                                                     # disabled
                'DISABLED',                                                                                     # disabled (don't worry about it, Z vals)
                cSystem)                                                                                        # our previously designated WGS84 Geographic coord system

                error = 'creating a cursor in our featureclass. Check the KAP file for PLY/ errors'             # we can't update the feature class
                cursor = arcpy.da.InsertCursor(collar, ['SHAPE@'])                                              # in our new FC in memory create a pointer
                cursor.insertRow([polygon])                                                                     # with the pointer insert each row of our array
                del cursor                                                                                      # then delete the cursor

                error = 'getting the extent of the input KAP file.  Check arcpy or the KAP file.'               # error on extent
                extentKAP = arcpy.sa.Raster(coord[0])                                                           # the extent is the extent (arcpy is stupid) of our raster
                extent = extentKAP.extent                                                                       # the var extent, is the extent, of our rasters extent...

                error = 'naming the new TIF file.  Something is wrong with the file directory or KAP file.'     # this is a string format, if this goes wrong god have mercy on your soul
                outputKAP = '{}/{}.TIF'.format(newChartDir, baseName[:-4])                                      # output TIF is the chart dir and filename in TIF format (slice removes .KAP)

                error = 'Arcpy clip error: either write permissions the KAP file.  Check if they\'re open.'     # arcpy error on clip, god only knows.
                arcpy.Clip_management(                                                                          # arcpy clip raster
                coord[0],                                                                                       # specify the kap (coord[0] = kap directory and filename)
                str(extent)[:-16],                                                                              # we slice the last 16 because of NaN x 3 + whitespace.  It ain't Javascript.
                outputKAP,                                                                                      # the output KAP or TIF technically
                collar,                                                                                         # the collar is our previously made feactureclass in memory
                '256',                                                                                          # no data is black, different versions of arc handle this differently
                'ClippingGeometry',                                                                             # we're clipping based on the feature class
                'MAINTAIN_EXTENT'                                                                               # this is on by default
                )

                print('')                                                                                       # blank line
                print('Finished Decollaring: {}'.format(baseName[:-4]))                                         # inform user of progress
                countVars['countComplete'] += 1                                                                 # add to the dict countComplete for metrics

            except:                                                                                             # this is a bad except I know, errors will be identified in time
                print('')                                                                                       # blank line
                print('Error on chart: {}'.format(baseName[:-4]))                                               # inform user if there is an exception!
                print('')                                                                                       # blank line
                print('Error with: {}'.format(error))                                                            # report error type

    getKAP(chartDirectory)                                                                                      # start this monster up!

    print('')                                                                                                   # blank line
    print('Finished: {}/{} KAP charts decollared!'.format(countVars['countComplete'], countVars['countKAPs']))  # inform user of good/bad news

def updateMosaics():                                                                                            # XXXXX  UPDATE SDE MOSACIS  XXXXX
    pass

whatstheplan()                                                                                                  # start this bad boi!
