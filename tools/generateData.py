# generateData.py | python3
# Nate Beatty | February, 2013
# For the IntlPop! project
#
# Parses CSV data from the given input directory
# and outputs a series of javascript files appropriate
# for use in the IntlPop! 3.0 web application.
#
# Run to download data from the UN and generate JSON data files
# which are automatically placed in the web application directory.
# The following will generate 2010 files from csv's in the tmp dir:
#
# $ python3 generateData.py 2010 
#
# If you need to download the data from the UN, run with the -d option:
#
# $ python3 generateData.py -d 2010
#
# Note that downloading all of the data from the UN will take a while
# and download speeds depend on your internet connection. 

import requests
import sys
import os
import xlrd
import csv
import shutil
import codecs
import json

TMP_DIR = 'tmp' # The directory containing the CSV files
OUT_DIR = '../api/countrydata' # Where the JSON output files will be created

# CSV FileNames (should be within the TMP_DIR)
# Edit these filenames to reflect your own naming convention if necessary
f_POPULATION_BY_AGE_MALE = 'POPULATION_BY_AGE_MALE.CSV'
f_POPULATION_BY_AGE_FEMALE = 'POPULATION_BY_AGE_FEMALE.CSV'
f_DEATHS_BY_AGE_MALE = 'DEATHS_BY_AGE_MALE.CSV'
f_DEATHS_BY_AGE_FEMALE = 'DEATHS_BY_AGE_FEMALE.CSV'
f_BIRTHS_BY_AGE_OF_MOTHER = 'BIRTHS_BY_AGE_OF_MOTHER.CSV'
f_IMR_BOTH_SEXES = 'IMR_BOTH_SEXES.CSV'
f_NET_NUMBER_OF_MIGRANTS = 'NET_NUMBER_OF_MIGRANTS.CSV'

UNDataFiles = [
  ['POPULATION_BY_AGE_MALE', 'http://esa.un.org/unpd/wpp/Excel-Data/DB03_Population_ByAgeSex_Quinquennial/WPP2010_DB3_F2_POPULATION_BY_AGE_MALE.XLS'],
  ['POPULATION_BY_AGE_FEMALE','http://esa.un.org/unpd/wpp/Excel-Data/DB03_Population_ByAgeSex_Quinquennial/WPP2010_DB3_F3_POPULATION_BY_AGE_FEMALE.XLS'],
  ['DEATHS_BY_AGE_MALE', 'http://esa.un.org/unpd/wpp/Excel-Data/DB05_Mortality_IndicatorsByAge/WPP2010_DB5_F2_DEATHS_BY_AGE_MALE.XLS'],
  ['DEATHS_BY_AGE_FEMALE', 'http://esa.un.org/unpd/wpp/Excel-Data/DB05_Mortality_IndicatorsByAge/WPP2010_DB5_F3_DEATHS_BY_AGE_FEMALE.XLS'],
  ['BIRTHS_BY_AGE_OF_MOTHER', 'http://esa.un.org/unpd/wpp/Excel-Data/DB06_Fertility_IndicatorsByAge/WPP2010_DB6_F1_BIRTHS_BY_AGE_OF_MOTHER.XLS'],
  ['IMR_BOTH_SEXES', 'http://esa.un.org/unpd/wpp/Excel-Data/DB01_Period_Indicators/WPP2010_DB1_F06_1_IMR_BOTH_SEXES.XLS'],
  ['NET_NUMBER_OF_MIGRANTS', 'http://esa.un.org/unpd/wpp/Excel-Data/DB01_Period_Indicators/WPP2010_DB1_F19_NET_NUMBER_OF_MIGRANTS.XLS']
]

POPULATION_BY_AGE_MALE = 'POPULATION_BY_AGE_MALE'
POPULATION_BY_AGE_FEMALE = 'POPULATION_BY_AGE_FEMALE'
DEATHS_BY_AGE_MALE = 'DEATHS_BY_AGE_MALE'
DEATHS_BY_AGE_FEMALE = 'DEATHS_BY_AGE_FEMALE'
BIRTHS_BY_AGE_OF_MOTHER = 'BIRTHS_BY_AGE_OF_MOTHER'
IMR_BOTH_SEXES = 'IMR_BOTH_SEXES'
NET_NUMBER_OF_MIGRANTS = 'NET_NUMBER_OF_MIGRANTS'


validYears = [2000, 2005, 2010]
validOptions = ['-d', '-c']

# Checks that command line arguments are valid
# 
# @return true if valid, false otherwise.
def validArgs():
  if len(sys.argv) not in [2, 3, 4] or int(sys.argv[-1]) not in validYears:
    return False
  if len(sys.argv) == 3 and sys.argv[1] not in validOptions:
    return False
  if len(sys.argv) == 4 and sys.argv[2] not in validOptions:
    return False
  return True

# Prints a usage message
def printUsage():
  print('Usage: python parseData date\nDate can be 2000, 2005, or 2010.')

# Takes a string of numerical characters and removes spaces, etc.
# to turn them into proper integers. Returns an int value
# 
# @param value The numerical value read from the CSV file. This number
# may contain negatives, spaces, commas, etc.
#
# @return int An integer interpretation of the value parameter
def intify(value):
  newInt = int(float(str(value).strip().replace(' ','')))
  return newInt

################################
#  Data File Download Methods  #
################################

def removeTmpFiles():
  if os.path.exists(TMP_DIR):
    print('Removing old temp files.')
    for the_file in os.listdir(TMP_DIR):
      file_path = os.path.join(TMP_DIR, the_file)
      try:
        if os.path.isfile(file_path):
            os.unlink(file_path)
      except:
        print('There was a problem removing the old data files.')
        exit(1)
  else:
    try:
      print('Creating temp directory at ' + TMP_DIR)
      os.makedirs(TMP_DIR)
    except:
      print('Could not generate output file directory.')
      exit(1)


def downloadXLSData():
  for item in UNDataFiles:
    file_url = item[1]
    file_path = os.path.join(TMP_DIR, item[0] + '.xls')
    with open(file_path, "wb") as f:
      print("Downloading %s" % item[0])
      response = requests.get(file_url, stream=True)
      total_length = intify(response.headers.get('content-length'))
      encoding = response.headers.get('content-encoding')
      cache_control = response.headers.get('cache-control')

      if total_length is None:
        f.write(response.content)
      elif encoding == 'gzip' or cache_control == 'private':
        print(' Some fields in the response headers were invalid.\n Attempting to download anyway.')
        f.write(response.content)
      else:
        dl = 0
        total_length = int(total_length)
        for data in response.iter_content():
          dl += len(data)
          f.write(data)
          done = int(50 * dl / total_length)
          sys.stdout.write("\r Progress: " + str(total_length) + " /%10d  [%3.2f%%]" % (dl, dl * 100. / total_length))
          sys.stdout.flush()
      f.close()
      print('')
  # make sure the files are valid
  for item in UNDataFiles:
    file_path = os.path.join(TMP_DIR, item[0] + '.xls')
    if not os.path.exists(file_path) or not os.path.isfile(file_path):
      print('Some data files were not downloaded.')
      exit(1)
    try:
      file_size = os.path.getsize(file_path)
    except:
      print('There was a problem downloading the data files.')
      exit(1)
    if file_size <= 0:
      print('There was a problem downloading the data files.')
      exit(1)


def makeCSVFiles():
  for item in UNDataFiles:
    print('Generating CSV file for ' + item[0])
    xls_path = os.path.join(TMP_DIR, item[0] + '.xls')
    csv_path = os.path.join(TMP_DIR, item[0] + '.csv')
    with xlrd.open_workbook(xls_path) as wb:
      sh = wb.sheet_by_index(0)
      with open(csv_path, 'w', newline='') as f:
        c = csv.writer(f)
        for r in range(sh.nrows):
          c.writerow(sh.row_values(r))


##################################
#  Data File Generation Methods  #
##################################

# Generates files for the given year
# 
# @param year The year of the desired output data Must be 
# an integer equal to either 2000, 2005, or 2010.
def generateFiles(year):
  # Create output directory
  if os.path.exists(OUT_DIR):
    print('Removing old data files.')
    for the_file in os.listdir(OUT_DIR):
      file_path = os.path.join(OUT_DIR, the_file)
      try:
        if os.path.isfile(file_path):
            os.unlink(file_path)
      except:
        print('There was a problem removing the old data files.')
        exit(1)
  else:
    try:
      print('Creating output directory at ' + OUT_DIR)
      os.makedirs(OUT_DIR)
    except:
      print('Could not generate output file directory.')
      exit(1)
  
  print('Generating files for year %s data.' % (str(year)))
  # Make a file for each country based on the male population data
  dataFile = codecs.open(os.path.join(TMP_DIR, f_POPULATION_BY_AGE_MALE), 'r', encoding='latin1')
  data = csv.reader(dataFile)

  for row in data:
    if len(row) <= 0: continue # Just in case some "phantom" rows exist from MS CSV export
    if (row[0] == '' or row[0] == 'Index'): continue # Only parse rows that contain data
    if int(float(row[5])) == year: # Only record the requested year
      countryName = row[2]
      countryCode = int(float(row[4]))

      filePath = os.path.join(OUT_DIR, '%s_%s.json' % (str(year), countryCode))

      f = open(filePath, 'w') # Make the new file

      # Write some preliminary stuff
      f.write('{\n')
      f.write('  "name": "%s",\n' % (countryName))
      f.write('  "countryId": %s,\n' % (str(countryCode)))
      f.write('  "startYear": %s,\n' % (str(year)))

      f.close()
  dataFile.close()

# Appends male and female population data for the given year
# to all of the .js files in the output directory. This method
# should be called immediately after `generateFiles`.
#
# @param year The year of the desired output data Must be 
# an integer equal to either 2000, 2005, or 2010.
def appendPopData(year):
  # Start with male population
  print('Parsing male population data.')
  dataFile = codecs.open(os.path.join(TMP_DIR, f_POPULATION_BY_AGE_MALE), 'r', encoding='latin1')
  data = csv.reader(dataFile)
  for row in data:
    if len(row) <= 0: continue
    if (row[0] == '' or row[0] == 'Index'): continue # Only parse rows that contain data
    if int(float(row[5])) == year: # Only record the selected year
      filePath = os.path.join(OUT_DIR, '%s_%s.json' % (str(year), int(float(row[4]))))
      f = open(filePath, 'a')
      f.write('  "malePop": [') # Write an open array to file
      for i in range(6, 28):
        f.write(str(intify(row[i])))
        if i < 27:
          f.write(',')
      f.write('],\n')
      f.close()
  dataFile.close()
  # Now fill in the female population
  print('Parsing female population data.')
  dataFile = codecs.open(os.path.join(TMP_DIR, f_POPULATION_BY_AGE_FEMALE), 'r', encoding='latin1')
  data = csv.reader(dataFile)
  for row in data:
    if len(row) <= 0: continue # Just in case some "phantom" rows exist from MS CSV export
    if (row[0] == '' or row[0] == 'Index'): continue # Only parse rows that contain data
    if int(float(row[5])) == year: # Only record the selected year
      filePath = os.path.join(OUT_DIR, '%s_%s.json' % (str(year), int(float(row[4]))))
      f = open(filePath, 'a')
      f.write('  "femalePop": [') # Write an open array to file
      for i in range(6, 28):
        f.write(str(intify(row[i])))
        if i < 27:
          f.write(',')
      f.write('],\n')
      f.close()
  dataFile.close()

# Appends the birth data for the given year to the .js files
# in the output directory. Make sure that `generateFiles` has
# been called previously.
#
# @param year The year of the desired output data Must be 
# an integer equal to either 2000, 2005, or 2010.
def appendBirthData(year):
  # Parse through the birth data and append it to the file
  print('Parsing birth data.')
  dataFile = codecs.open(os.path.join(TMP_DIR, f_BIRTHS_BY_AGE_OF_MOTHER), 'r', encoding='latin1')
  data = csv.reader(dataFile)
  for row in data:
    if len(row) <= 0: continue # Just in case some "phantom" rows exist from MS CSV export
    if (row[0] == '' or row[0] == 'Index'): continue # Only parse rows that contain data
    if int(row[5].split('-')[1]) == year: # Only record the selected year
      filePath = os.path.join(OUT_DIR, '%s_%s.json' % (str(year), int(float(row[4]))))
      f = open(filePath, 'a')
      f.write('  "births": [') # Write an open array to file
      for i in range(6, 13):
        f.write(str(intify(row[i])))
        if i < 12:
          f.write(',')
      f.write('],\n')
      f.close()
  dataFile.close()

# Appends both the male and female mortality data to the .js files
# in the OUT_DIR. Make sure that `generateFiles` has been called.
#
# @param year The year of the desired output data Must be 
# an integer equal to either 2000, 2005, or 2010.
def appendMortalityData(year):
  # Start with the female mortality data
  print('Parsing female mortality data.')
  dataFile = codecs.open(os.path.join(TMP_DIR, f_DEATHS_BY_AGE_FEMALE), 'r', encoding='latin1')
  data = csv.reader(dataFile)
  for row in data:
    if len(row) <= 0: continue # Just in case some "phantom" rows exist from MS CSV export
    if (row[0] == '' or row[0] == 'Index'): continue # Only parse rows that contain data
    if int(row[5].split('-')[1]) == year: # Only record the selected year
      filePath = os.path.join(OUT_DIR, '%s_%s.json' % (str(year), int(float(row[4]))))
      f = open(filePath, 'a')
      f.write('  "femaleMortality": [') # Write an open array to file
      for i in range(6, 26):
        f.write(str(intify(row[i])))
        if i < 25:
          f.write(',')
      f.write('],\n')
      f.close()
  dataFile.close()

  # Now parse and append the male mortality data
  print('Parsing male mortality data.')
  dataFile = codecs.open(os.path.join(TMP_DIR, f_DEATHS_BY_AGE_MALE), 'r', encoding='latin1')
  data = csv.reader(dataFile)
  for row in data:
    if len(row) <= 0: continue # Just in case some "phantom" rows exist from MS CSV export
    if (row[0] == '' or row[0] == 'Index'): continue # Only parse rows that contain data
    if int(row[5].split('-')[1]) == year: # Only record the selected year
      filePath = os.path.join(OUT_DIR, '%s_%s.json' % (str(year), int(float(row[4]))))
      f = open(filePath, 'a')
      f.write('  "maleMortality": [') # Write an open array to file
      for i in range(6, 26):
        f.write(str(intify(row[i])))
        if i < 25:
          f.write(',')
      f.write('],\n')
      f.close()
  dataFile.close()

  # Now parse and append the infant mortality data
  print('Parsing infant mortality data.')
  dataFile = codecs.open(os.path.join(TMP_DIR, f_IMR_BOTH_SEXES), 'r', encoding='latin1')
  data = csv.reader(dataFile)
  for row in data:
    if len(row) <= 0: continue # Just in case some "phantom" rows exist from MS CSV export
    if (row[0] == '' or row[0] == 'Index'): continue # Only parse rows that contain data
    filePath = os.path.join(OUT_DIR, '%s_%s.json' % (str(year), int(float(row[4]))))
    f = open(filePath, 'a')
    index = int(((year - 1955) / 5) + 5)
    f.write('  "infantMortality": %i,\n' % intify(row[index]))
    f.close()
  dataFile.close()

def appendMigrationData(year):
  print('Parsing migration data.')
  dataFile = codecs.open(os.path.join(TMP_DIR, f_NET_NUMBER_OF_MIGRANTS), 'r', encoding='latin1')
  data = csv.reader(dataFile)
  for row in data:
    if len(row) <= 0: continue # Just in case some "phantom" rows exist from MS CSV export
    if (row[0] == '' or row[0] == 'Index'): continue # Only parse rows that contain data
    filePath = os.path.join(OUT_DIR, '%s_%s.json' % (str(year), int(float(row[4]))))
    f = open(filePath, 'a')
    index = int(((year - 1955) / 5) + 5)
    f.write('  "netMigration": %i\n' % intify(row[index]))
    f.close()
  dataFile.close()

# Iterates through all of the files in the output directory
# and closes them all with an unindented right curly brace
def endFiles():
  print('Finishing up country files.')
  for fileName in os.listdir(OUT_DIR):
    f = open(os.path.join(OUT_DIR, fileName), 'a')
    f.write('}\n')
    f.close

#################################
#  Country List Helper Methods  #
#################################

def createCountryList(year):
  print('Generating the country list json.')

  countries = []
  
  dataFile = codecs.open(os.path.join(TMP_DIR, f_POPULATION_BY_AGE_MALE), 'r', encoding='latin1')
  data = csv.reader(dataFile)
  for row in data:
    if len(row) <= 0: continue # Just in case some "phantom" rows exist from MS CSV export
    if (row[0] == '' or row[0] == 'Index'): continue # Only parse rows that contain data
    if int(float(row[5])) == year: # Only record the requested year
      countryName = row[2]
      countryCode = row[4]
      fileName = '%s_%s.json' % (str(year), countryCode)
      country = dict()
      country['id'] = int(float(countryCode))
      country['name'] = countryName
      country['alias'] = countryName
      country['filename'] = fileName
      countries.append(country)
  dataFile.close()

  output_dir = os.path.split(OUT_DIR)[0]
  filePath = os.path.join(output_dir, 'countrylist.json')
  listFile = open(filePath, 'w') # Make the new file
  json.dump(countries, listFile)
  listFile.close()

##################
#  Main Program  #
##################

print('\nIntlPop! Data File Generator\n============================\n')

if not validArgs():
  printUsage()
  quit() # Stop program execution if a valid date is not provided

dataYear = int(sys.argv[-1])

if '-d' in sys.argv:
  removeTmpFiles()
  downloadXLSData()
  makeCSVFiles()

if '-c' in sys.argv:
  createCountryList(dataYear)

generateFiles(dataYear) # Start the files
# Add data
appendPopData(dataYear)
appendBirthData(dataYear)
appendMortalityData(dataYear)
appendMigrationData(dataYear)
endFiles() # End the files

print()