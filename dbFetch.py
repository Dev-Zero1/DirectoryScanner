import File
import mysql.connector
##------------------------------------------------------
##
##------------------------------------------------------ 
def setCredentials():
  credFile = 'C:\\Python\\Scripts\\sqlData\\sqlInfo.csv'
  ##this file has my username and password separated by comma
  ##aids in keeping my credentials for the database off the github repo
  with open(credFile, mode ='r')as myFile:
    lines = myFile.readlines()
    lines = lines[0].split(",")
    return lines
##------------------------------------------------------
##
##------------------------------------------------------ 
def push(file):
  f = file  
  credentials = setCredentials()
  
  db = mysql.connector.connect(
    host="localhost",
    user=credentials[0],
    password=credentials[1],
    database="directoryScanner"
  )

  mc = db.cursor()
  command = "INSERT INTO files VALUES (%s,%s, %s, %s,%s,%s,%s,%s)"  
  values = (f.fileID, f.fileName,File.formatCurrentDir(f.fileDir),f.fileType,f.fileLastModified,f.fileCreated,f.timeNow,f.fileSize)
  mc.execute(command, values)
  db.commit()
##------------------------------------------------------
##
##------------------------------------------------------ 
def fetch(cmd):
  credentials = setCredentials()
  
  db = mysql.connector.connect(
    host="localhost",
    user=credentials[0],
    password=credentials[1],
    database="directoryScanner"
  )
  mc = db.cursor()
  mc.execute(cmd)
  result = mc.fetchall()
  return result

##------------------------------------------------------
##
##------------------------------------------------------ 
def checkIfExists(file,logPath):
  credentials = setCredentials() 
  db = mysql.connector.connect(
    host="localhost",
    user=credentials[0],
    password=credentials[1],
    database="directoryScanner"
  )
  mc = db.cursor()
  File.displayFile(file)
  tempDir = file.fileDir
  
  if(tempDir == 'C:\\'):
    tempDir = tempDir[:len(tempDir)-1]
    
  ##sql requires strings to handle escape chars for directories, these are formatted \ to \\
  tempDir = file.fileDir.replace('\\', '\\\\')

  selectWhere = "SELECT * from files WHERE"
  cond1 = f" ( fileDir = '{tempDir}'"   ##<<<<<<<<<<<  '\\' ?
  cond2 = f" AND fileName = '{file.fileName}'"
  cond3 = f" AND fileSize_bytes = {file.fileSize}"
  cond4 = f" AND lastModified = '{file.fileLastModified}');"
  
  cmd = selectWhere + cond1 + cond2 + cond3 + cond4
  File.logError(file,("fetchRequest: "+cmd+"\n"),logPath) 
  mc.execute(cmd)
  
  result = mc.fetchall()
  
  if len(result) >= 1:
    ##don't put in the DB if one already exists with the same data.
    ##update the lastModified time in the DB
    File.logError(file,"Duplicate File results returned for this Directory\File. ",logPath)
    ##cmd = "Update "
  else:
    File.logError(file,"Duplicate Files not found, creating file record.",logPath)
    push(file)
    
##------------------------------------------------------
##
##------------------------------------------------------     
    


