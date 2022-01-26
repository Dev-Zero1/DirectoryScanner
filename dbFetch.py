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
  ##fetch("Select * from files")

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
  
##  for row in result:
##    print(row[1]) ##fileName
##    print("---------------------")
##    print(row[2])##fileDir
##    print(row[3])##fileType
##    print(row[4])##fileLastModified
##    print(row[5])##fileCreated
##    print(str(row[6])+'\n')##fileSize
  


##  print(mc.rowcount, "record successfully inserted.")
    
    
    


