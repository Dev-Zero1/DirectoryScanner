import File
import mysql.connector
import os
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
def push(file,logPath):
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
  try:
    mc.execute(command, values)
    db.commit()
    File.logError(file,("sendRequestSuccess: "+command+"\n"),logPath) 
  except:
    File.logError(file,("sendRequestFailed: "+command+"\n"),logPath)
    
  command = "INSERT INTO filecontent VALUES (%s,%s)"  
  values = (f.fileID,'')
  try:
    mc.execute(command, values)
    db.commit() 
    File.logError(file,("sendRequestSuccess: "+command+"\n"),logPath)
    
  except:
    File.logError(file,("sendRequestFailed: "+command+"\n"),logPath)
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
  ##File.displayFile(file)
  tempDir = file.fileDir
  
  if(tempDir == 'C:\\'):
    tempDir = tempDir[:len(tempDir)-1]
    
  ##sql requires strings to handle escape chars for directories, these are formatted \ to \\
  tempDir = file.fileDir.replace('\\', '\\\\')
  print('fileType = '+ file.fileType)
  if file.fileType != 'folder':
    selectWhere = "SELECT * from files WHERE"
    cond1 = f" ( fileDir = '{tempDir}\\\\'" 
    cond2 = f" AND fileName = '{file.fileName}'"
    cond3 = f" AND fileSize_bytes = {file.fileSize}"
    cond4 = f" AND lastModified = '{file.fileLastModified}');"
    cmd = selectWhere + cond1 + cond2 + cond3 +cond4
  else:
    selectWhere = "SELECT * from files WHERE"
    cond1 = f" ( fileDir = '{tempDir}\\\\'" 
    cond2 = f" AND fileName = '{file.fileName}'"
    cond3 = f" AND fileSize_bytes = {file.fileSize});"
    ##cond4 = f" AND lastModified = '{file.fileLastModified}');"    
    cmd = selectWhere + cond1 + cond2 + cond3
    
  File.logError(file,("fetchRequest: "+cmd+"\n"),logPath) 
  mc.execute(cmd)
  
  result = mc.fetchall()
  
  if len(result) >= 1:
    ##don't put in the DB if one already exists with the same data.
    File.logError(file,"Duplicate File results returned for this Directory\File. ",logPath)
  else:
    File.logError(file,"Duplicate Files not found, creating file record.",logPath)
    push(file,logPath)
    
##------------------------------------------------------
##
##------------------------------------------------------     
def pushFileContent(file, logPath):
  
  credentials = setCredentials() 
  db = mysql.connector.connect(
    host="localhost",
    user=credentials[0],
    password=credentials[1],
    database="directoryScanner"
    )
  f = file
  extList = ['xml','html','htm','css','js','txt','log','config','ini','bat','cif','ach','dat','cs','resx','md','csv','py']
  
  if f.fileType in extList:    
    fullPath = os.path.join(f.fileDir, f.fileName)
    
    with open(fullPath, 'r') as reader:
      try:
        filecontent = reader.readlines()
        fc = ''
        for line in filecontent:
          fc += line
        if f.fileType == 'config' or f.fileType == 'xml':
          i = fc.index('<')
          fc = fc[i:]
        print(fc)
        mc = db.cursor() 
        cmd = "UPDATE filecontent SET fileTxt = %s WHERE fileId = %s"  
        values = (fc,f.fileID)
        print(values)
        try:
          mc.execute(cmd, values)
          db.commit()
          print(("sendRequestSuccess: "+cmd+"\n"))
          File.logError(file,("sendRequestSuccess: "+cmd+"\n"),logPath) 
        except:
          File.logError(file,("sendRequestFailed: "+cmd+"\n"),logPath)
          print("sendRequestFailed: "+cmd+"\n")
      except UnicodeDecodeError:
        File.logError(file,("parseRequestFailed: "+fullPath+"\n"),logPath)
        print("parseRequestFailed: "+fullPath+"\n")
    


