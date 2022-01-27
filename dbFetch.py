import File
import mysql.connector

def setCredentials():
  credFile = 'C:\\Python\\Scripts\\sqlData\\sqlInfo.csv'
  ##this file has my username and password separated by comma
  ##aids in keeping my credentials for the database off the github repo
  with open(credFile, mode ='r')as myFile:
    lines = myFile.readlines()
    lines = lines[0].split(",")
    return lines

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
  command = "INSERT INTO files VALUES (%s,%s, %s, %s,%s,%s,%s)"
  values = (f.fileID, f.fileName,f.fileDir,f.fileType,f.fileLastModified,f.fileCreated,f.fileSize)
  mc.execute(command, values)
  db.commit()

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


def checkIfExists(file):
  credentials = setCredentials() 
  db = mysql.connector.connect(
    host="localhost",
    user=credentials[0],
    password=credentials[1],
    database="directoryScanner"
  )
  mc = db.cursor()
  cmd = "select * from files "
  +f"WHERE  fileDir = '{file.fileDir}' "
  +f"AND fileName = '{file.fileName}' "
  +f"AND fileSize = '{file.fileSize}' "
  +f"AND lastModified = '{file.fileLastModified}' "
  +"order by fileScannedAt desc limit 1 "
  mc.execute(cmd)
  result = mc.fetchall()
  
  if len(result) >= 1:
    ##don't put in the DB if one already exists with the same data.
    ##update the lastModified time in the DB
  else:
    push(file)
    
    
    


