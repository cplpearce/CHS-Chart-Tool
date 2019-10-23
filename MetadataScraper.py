# Version: 0.2b.4
import csv                                                                                              # output into csv
import os                                                                                               # for os.walk and pathing
import re                                                                                               # for metadata tag snatching
import fnmatch                                                                                          # filename match
import datetime                                                                                         # time 'yo              
import arcpy                                                                                            # table_to_table
import Tkinter, tkFileDialog                                                                            # for file dialogs

time.sleep(.5)                          
print('')                           
time.sleep(.5)                          
print('')                           
time.sleep(.5)                          
print('')                           
print('####################################################')                                           # flash and pizaz!
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
print('')                           
print(' HYDROGRAPHIC  CHART  TOOL  WRITTEN IN PYTHON   2.7 ')                           
print(' A) DECOLLAR NAUTICAL CHARTS IN  A TARGET DIRECTORY ')                           
print(' B) UPDATE  TARGET   SDE  WITH  DECOLLARED   CHARTS ')                           
print(' C) STRIP  METADATA  FROM .KAPS AND UPDATE THE  SDE ')                           
print('')                           
print('####################################################')                           
time.sleep(.5)                          
print('')                           
time.sleep(.5)                          
print('')                           

root = Tkinter.Tk()                                                                                     # tkinter loads with a window/GUI, we need to load it...
root.withdraw()                                                                                         # and hide it, withdraw == hide

def whatstheplan():                                                                                     # XXXXX  PROMPUT USER INPUT  XXXXX

	print('')                                                                                           # begin the choosing
	print('Choose your task: ')                                                                         # user input begins
	print('    a) Decollar a Chart Directory (*.KAP)')                                                  # decollar charts
	print('    b) Update SDE Chart Mosaics With New Decollared Charts')                                 # update SDE with decollared charts
	print('    c) Update Nautical Chart Metadata on the SDE')                                           # update SDE with metadata
	print('')                                                                                           # 
	userChoice = raw_input('    (a), (b), or (c): ')                                                    # user choice
	while userChoice.lower() not in ['a', 'b', 'c']:                                                    # lower ther input for conisitency and while: so input is predefined
		print('')                                                                                       # 
		time.sleep(.1)                                                                                  # 
		print('')                                                                                       # 
		time.sleep(.1)                                                                                  # 
		print('')                                                                                       # 
		time.sleep(.1)                                                                                  # 
		print('Error: Incorrect entry, [{}] is not a selectable input'.format(userChoice))              # if the user is a knob retry
		print('')                                                                                       # 
		print('Choose your task: ')                                                                     # 
		print('    a) Decollar a Chart Directory (*.KAP)')                                              # 
		print('    b) Update SDE Chart Mosaics With New Decollared Charts')                             # 
		print('    c) Update Nautical Chart Metadata on the SDE')                                       # 
		print('')                                                                                       # 
		userChoice = raw_input('    (a), (b), or (c): ')                                                # 
	else:                                                                                               # 
		if userChoice.lower() == 'a':                                                                   # 
			decollarCharts()                                                                            # lets get the metadata!
		elif userChoice.lower() == 'b':                             
			updateMosaics()                                                                             # lets decollar the charts!
		elif userChoice.lower() == 'c':                             
			processMetadata()                                                                           # lets update the mosaics!
                    
	print('')               
	time.sleep(.5)              
	print('')               
	time.sleep(.5)              
	print('')               
	time.sleep(.5)              
                    
def processMetadata():                                                                                  # XXXXX  GET CHART METADATA  XXXXX
                
	countVars = {                           
	'countKAPs' : 0,                                                                                    # count of all KAPs, pre processing
	'countComplete' : 0                                                                                 # count the records processed
	}               
                    
	print('')                           
	time.sleep(.5)                          
	print('You have selected [Update Nautical Chart Metadata on the SDE].')                         
	time.sleep(.5)                          
	print('')                           
	print('Please select target directory containing .KAP files')                                       # prompt the user
	chartDirectory = tkFileDialog.askdirectory()                            
	print('')                           
	time.sleep(.5)                          
	print('Crawling directory, please be patient.')                         
	time.sleep(1)                                                                                       # pause
	print('')                                                                                           # pause
	dictMetadata = {}                                                                                   # metadata to be written to csv
	rn = datetime.datetime.now().strftime('%y%m%d')                                                     # get the date time group as 'rn' (right now)   

	# <========= this is your SDE connection - if it ever changes, change this var! =========>
	dbSDEbase = r'\\mce-geo-gds.mce.mil.ca\sds\10_DATACUBE\HYDROGRAPHIC\CHS\CHS on DATACUBE_RASTER.sde'

	arcpy.env.overwriteOutput = True                                                                    # overwrite old data with arcpy tools
	#arcpy.env.scratchWorkspace = r'in_memory'                                                          # write a gdb to in_memory
	arcpy.env.workspace = dbSDEbase                                                                     # set the SDE as our workspace
	scratchGDB = arcpy.env.scratchGDB                                                                   # write to the scratch gdb
	tempGDBdir = 'tempGDB'                                                                              # declare its location
                
	listSDEMosaics = arcpy.ListDatasets('*CHS*', 'Mosaic')                                              # get all the CHS datasets in the SDE
                
	countMosaicsUpdated = 0                                                                             # a count for the mosaics updated
                
	dictTags = {                                                                                        # list of keys to be RE'd over all the KAP files
	'CRR': '',                                                                                          # copyright
	'NA': '',                                                                                           # ?
	'NU': '',                                                                                           # ?
	'SC': '',                                                                                           # ?
	'UN': '',                                                                                           # ?
	'SD': '',                                                                                           # ?
	'SE': '',                                                                                           # ?
	'RE': '',                                                                                           # ?
	'ED': '',                                                                                           # ?
	'NE': '',                                                                                           # ?
	'ND': ''                                                                                            # ?
	}                           
                
	listREs = [                                                                                         # list of regular expressions to pull metadata
	r'(?:CRR/)(.+?)(VER|BSB)',                                                                          # ?
	r'(?:NA=)(.+?)[\,|\n]+',                                                                            # ?
	r'(?:NU=)(.+?)[\,|\n]+',                                                                            # ?
	r'(?:SC=)(.+?)[\,|\n]+',                                                                            # ?
	r'(?:UN=)(.+?)[\,|\n]+',                                                                            # ?
	r'(?:SD=)(.+?)[\,|\n]+',                                                                            # ?
	r'(?:SE=)(.+?)[\,|\n]+',                                                                            # ?
	r'(?:RE=)(.+?)[\,|\n]+',                                                                            # ?
	r'(?:ED=)(.+?)[\,|\n]+',                                                                            # ?
	r'(?:NE=)(.+?)[\,|\n]+',                                                                            # ?
	r'(?:ND=)(.+?)[\,|\n]+'                                                                             # ?
	]                           

	def getKAP(chartDirectory):                         
		listKAPs = []                                                                                   # a list for *all* the KAP files, duplicates included
		listUniqueKAPS = []                                                                             # a list of the unique KAP files
                
		for root, dirnames, filenames in os.walk(chartDirectory):                                       # for here, with dir names, walk thru each dir for files (dir = input var)
			for filename in fnmatch.filter(filenames, r'*.KAP'):                                        # for .KAP files
				countVars['countKAPs'] += 1                                                                          # count the KAP files found
				if filename in listUniqueKAPS:                                                          # for pre-existing (duplicates)...
					pass                                                                                # pass
				else:                               
					listKAPs.append(os.path.join(root, filename))                                       # add the found KAP files to the listKAPs list
					listUniqueKAPS.append(filename)                                                     # note the unique filenale

		getLines(listKAPs)                                                                              # get dem lines bro

	def getLines(KAPs):                                                                                 # open the KAP file, get the KAP chart name and first 25 lines and send it to getTags(x,y) 
		for kap in KAPs:                                                                                # for the KAPs in listKAPs
			tempString = ''                                                                             # concatinate our ten strings together
			with open(kap, 'rt') as okap:                                                               # [with open()] each KAP file as 'read text' as okap
				for lines in range(25):                                                                 # read the first ten lines
					tempString = tempString + okap.readline().decode(                                   # grab the lines and add them to the tempString var
					'ascii',                            
					errors='ignore'                         
					)                                                                                   

			getTags(os.path.basename(kap), tempString)                                                  # run the getTags function, BUT key in the KAP by filename, not path + filename

	def getTags(kap, tempString):                                                                       # this function pulls the metadata tags from tempString and cleans them up!
		listKAPMetadata = []                                                                            # metadata of each particular kap that resets on iteration
		for expression in listREs:                                                                      # iterate over our prewritten regex statements
			match = re.search(expression, tempString, flags=re.DOTALL)                                  # matching each against tempString with the DOTALL flag
                            
			try:                                                                                        # if match == TRUE, try         
				cleanMatch = re.sub(r'\r?\n', '', match.group(1))                                       # remove those icky \n and \r newlines as a new var called cleanMatch
				cleanMatch = re.sub(r'(\,|\t|\s\s\s)', '', cleanMatch)                                  # lets throw out excessive spacing too!  and tabs!  and commas!  out!
				listKAPMetadata.append(cleanMatch)                                                      # write that bad boy to the listKAPMetadata list
			except:                                                                                     # uh-oh
				listKAPMetadata.append(r'NULL')                                                         # append the error or lack of a value as 'NULL'
                
			dictMetadata[kap] = listKAPMetadata                                                         # now push all the metadata to the dictMetadata dictionary, key'd by KAP file

		writeTags(dictMetadata)                                                                         # write the metadata to dictMetadata

	def writeTags(dictMetadata):                                                                        # this function pushes all the tags into a list for writing to the new csv      

		global filename                         
		filename = 'NauticalChartMetadata-' + str(rn) + '.csv'                                          # create the filename string

		with open(filename, 'wb') as csvFile:                                                           # begin writing the csv as filename, in workbook mode (mode 'wb' removes double lines)
			writer = csv.writer(csvFile, delimiter = ',')                                               # create the csv writer object with a comma delimiter
			headers = (                                                                                 # list the headers
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

			writer.writerow(headers)                                                                    # write the headers

			countVars['countComplete'] += 1                                                             # count 'em!

			for k, di in dictMetadata.iteritems():                                                      # for keys (k), and dictionary items (di) in the dictionary dictMetadata

				stringToWrite = k[:-4]                                                                  # create a string, starting with the kap file name
				for x in di:                                                                            # for the item (x) in dictionary items (di), 
					stringToWrite = stringToWrite + ',' + x                                             # load the string, and add the new item and a comma
				listWrite = stringToWrite.split(',')                                                    # split the string by commas (writer iterates, needs a list not a string)
				writer.writerow(listWrite)                                                              # write the list!       

	def UpdateGDB():                            
		print('Converting CSV to dBASE table!  Chimo!')                                                 # update the user
		time.sleep(1)                                                                                   # pause
		print('')                                                                                       # pause
		tableName = 'NCM' + str(rn)                                                                     # give the dBASE table a name
		tableNameFull = str(scratchGDB + '/' + tableName + '.dbf')                                      # get the full table name and extension
		print('This may take some time, please be patient.')                                            # update the user
		time.sleep(1)                                                                                   # pause
		print('')                                                                                       # pause
		print('Converting to dBASE...')                                                                 # update the user
		time.sleep(1)                                                                                   # pause
		print('')                                                                                       # pause
		arcpy.TableToTable_conversion(filename, scratchGDB, tableName)                                  # convert it to a dBASE table :D

		print('Adding aliases...')                                                                      # update the user
		time.sleep(1)                                                                                   # pause
		print('')                                                                                       # pause
		listFields = [                                                                                  # list of field names in computer speak and english (field name/alias)
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

		for field in listFields:                                                                        # alter the table names!
			arcpy.AlterField_management(                                                                # arcpy AlterField
			tableNameFull,                                                                              # get the dBASE table name + dir
			field[0],                                                                                   # look for field X
			field[0],                                                                                   # rename it, to the same        
			field[1]                                                                                    # add an alias, as ref'd in listFields
			)                                                                                               

		global countMosaicsUpdated                          

		try:                            
			for mosaics in listSDEMosaics:                                                              # for the mosaics in the SDE
				try:                                                                                    # try (in case schema issue)
					print('Updating Mosaic: {}'.format(mosaics))                                        # tell the user which one we're on
					arcpy.JoinField_management(                                                         # arcpy join the field (permamnent join)
					mosaics,                                                                            # on the mosaics in the SDE
					r'Name',                                                                            # match on the mosaic chart field 'Name',
					tableNameFull,                                                                      # with a dBASE table found here, and
					r'CHART'                                                                            # match on the CHART value in the dBASE table
					)                           
					time.sleep(1)                                                                       # pause
					countMosaicsUpdated += 1                                                            # count updated mosaics
					print('')                                                                           # pause

				except TypeError:                           
					print('Schema Issue on: {}'.format(mosaics))                                        # inform user of schema issue
					time.sleep(1)                                                                       # pause
					print('')                                                                           # pause
					pass                            

		except TypeError:                                                                               # you failed, here's why
			print('Error: Couldn\'t connect to SDE!')
			print('This portion of the Nautical Chart tool is for the MCE LAN network!')
			pass
	
	getKAP(chartDirectory)                                                                              # process those charts!
	UpdateGDB()                                                                                         # update the SDE!

	if arcpy.Exists(scratchGDB):                                                                        # BEGONE SCRATCH GDB
		arcpy.Delete_management(scratchGDB)                                                             
	if os.path.isdir(scratchGDB):                                                                       # BEGONE HARDER IF YOU WON'T GO THE LEGIT WAY!
		shutil.rmtree(scratchGDB)               

	print('')               
	print('Complete!')              
	os.system('pause')              
	print('')               
	print('####################################################')               
	print(' Charts Found:        {}'.format(str(countVars['countKAPs'])))                               # tell user charts found
	print(' Charts Processed:    {}'.format(str(countVars['countComplete'])))                           # tell user charts processed

	print(' SDE Mosaics Updated: {}'.format(str(countMosaicsUpdated)))                                  # tell user mosaics updated

	if countVars['countKAPs'] > countVars['countComplete']:                                             # if there were more charts found than processed alert the user
		print('======================================')             
		print(' Chart Duplicates: {}'.format(               
		str(countVars['countKAPs'] - countVars['countComplete'])))                                      # and if there were any duplicates

	print('####################################################')               
	print('')               
	print('Closing in 10 seconds...')               
	time.sleep(5)               
	exit                

def decollarCharts():                                                                                   # XXXXX  DECOLLAR      KAPs  XXXXX
	countVars = {                           
	'countKAPs' : 0,                                                                                    # count of all KAPs, pre processing
	'countComplete' : 0                                                                                 # count the records processed
	}                           

	print('')                               
	print('You have selected [Decollar a Chart Directory (*.KAP)]')                             
	print('')                               
	print('')                               
	print('')                               
	print('')                           
	print('Please select target directory containing .KAP files')                                       # prompt the user
	chartDirectory = tkFileDialog.askdirectory()                                                        # get the chart directory
	print('')                           
	print('Please select target directory to save decollared .KAP files')                           
	time.sleep(2)                           
	decollarDirectory = tkFileDialog.askdirectory()                         
	print('')                           
	print('Crawling directory, please be patient.')                                                     # pause
                
	rn = datetime.datetime.now().strftime('%y%m%d')                                                     # get the date time group as 'rn' (right now)
                
	arcpy.env.overwriteOutput = True                                                                    # overwrite old data with arcpy tools
                
	def getKAP(dir):                            
                
		listKAPs = []                                                                                   # a list for *all* the KAP files, duplicates included
		listUniqueKAPS = []                                                                             # a list of the unique KAP files to skip when itering all KAPs
                
		for root, dirnames, filenames in os.walk(dir):                                                  # for here, with dir names, walk thru each dir for files (dir = input var)
			for filename in fnmatch.filter(filenames, r'*.KAP'):                                        # for .KAP files        
				countVars['countKAPs'] += 1                                                                          # count the KAP files found
				if filename in listUniqueKAPS:                                                          # for pre-existing (duplicates)...
					pass                                                                                # pass
				else:                               
					listKAPs.append(os.path.join(root, filename))                                       # add the found KAP files to the listKAPs list
					listUniqueKAPS.append(filename)                                                     # note the unique filenale
                
		getLines(listKAPs)                                                                              # get dem lines bro
                
	def getLines(KAPs):                                                                                 # open the KAP file, get the coodinate data for the decollaring
		print('')                           
		print('Parsing KAP file lines.')                            
		listCoords = []                                                                                 # list of coords
		for kap in KAPs:                                                                                # for the KAPs in listKAPs
			tempString = ''                                                                             # strings placeholder
			tempCoord = [kap]                                                                           # coords placeholder
			with open(kap, 'rt') as okap:                                                               # [with open()] each KAP file as 'read text' as okap
				while tempString[:4] != r'DTM/':                                                        # until we readline to DTM/
					tempString = okap.readline().decode(                                                # skip useless lines
					'ascii',                            
					errors='ignore'                         
					)                                                                                   
					if tempString[:3] == 'PLY':                                                         # unless it's PLY/X
						tempCoord.append(tempString[:-2].split(',')[1:])                                # add the temp string with edits to the temp list    
					else:                           
						pass                            

				listCoords.append(tempCoord)                                                            

		clipKAPs(listCoords)                                                                            # run the clipKAPs function to begin clipping KAPs (duh!)

	def clipKAPs(coords):                                                                               # begin the great decollaring

		print('')                   
		print('Creating feature classes and clipping {} KAP files'.format(len(coords)))                       

		for coord in coords:                                                                            # for coordinates found 

			basePath, baseName = os.path.split(coord[0])                                                # create basepath/name, by os.path splitting

			try:                                                                                        # try because shit goes awry and we can't always remain on top
				commonPath = os.path.join(                          
				str(coord[0]).split(os.path.sep)[-3],                           
				str(coord[0]).split(os.path.sep)[-2]                            
				)                           

				rn = datetime.datetime.now().strftime('%y%m%d')                                         # get the date time group as 'rn' (right now) 

				newChartDir = os.path.join(                             
				'{}/DECOLLAR-{}/{}'.format(                             
				decollarDirectory,                              
				rn,                                                                                     # 'rn' (right now)   
				commonPath))                                                                            # last two folders, reverse recursive

				try:                                                                                    # try making a new directory
					os.makedirs(newChartDir)                            
					print('')                           
					print('Creating: {})'.format(newChartDir))                          
				except WindowsError:                                                                    # folder already exists!
					pass

				listPoints = []
			
				for xy in coord[1:]:
					xyint = map(float, xy)
					x = xyint[1]
					y = xyint[0]
					listPoints.append(arcpy.Point(x, y))
			
				array = arcpy.Array(listPoints)
							
				cSystem = 'Geographic Coordinate Systems/World/WGS 1984'       
				polygon = arcpy.Polygon(array)
				collar = arcpy.CreateFeatureclass_management(
				'in_memory',
				'tempFC',
				'POLYGON',
				'',
				'DISABLED',
				'DISABLED',
				cSystem)
				
				cursor = arcpy.da.InsertCursor(collar, ['SHAPE@'])
				cursor.insertRow([polygon])
				del cursor

				extentKAP = arcpy.sa.Raster(coord[0])
				extent = extentKAP.extent
				
				outputKAP = '{}/{}.TIF'.format(newChartDir, baseName[:-4])        
				
				arcpy.Clip_management(
				coord[0],
				str(extent)[:-16],
				outputKAP,
				collar,
				'256',  
				'ClippingGeometry',
				'MAINTAIN_EXTENT'
				)
				
				print('')
				print('Finished Decollaring: {}'.format(baseName[:-4]))
				countVars['countComplete'] += 1
				
			except:
				print('Error on chart: {}'.format(baseName[:-4]))
		
	getKAP(chartDirectory)
	
    print('')
    print('Finished: {}/{} KAP charts decollared!'.format(countVars['countComplete'], countVars['countKAPs']))
	
def updateMosaics():                                                                                    # XXXXX  UPDATE SDE MOSACIS  XXXXX
	pass                            

whatstheplan()                                                                                          # start this bad boi!
