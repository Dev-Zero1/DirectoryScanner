import File

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
  import mysql.connector
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
  import mysql.connector
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

    
    
    


