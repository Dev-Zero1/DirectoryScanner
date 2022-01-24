import File

def setCredentials():
  credFile = 'C:\\Python\\Scripts\\sqlData\\sqlInfo.csv'
  ##this file has my username and password separated by comma
  ##aids in keeping my credentials for the database off the github repo
  with open(credFile, mode ='r')as myFile:
    lines = myFile.readlines()
    lines = lines[0].split(",")
    return lines

def fetch():
  file = File.make_blankFile() 
  import mysql.connector
  credentials = setCredentials()
  
  db = mysql.connector.connect(
    host="localhost",
    user=credentials[0],
    password=credentials[1],
    database="directoryScanner"
  )

  mc = db.cursor()
  
##
##  command = "INSERT INTO files VALUES (%d,%s, %s, %s,%s,%d)"
##  values = ("John", "Highway 21")
##  mc.execute(command, values)
##
##  db.commit()
##
##  print(mc.rowcount, "record successfully inserted.")



  mc.execute("SELECT * FROM files")
  result = mc.fetchall()

  for row in result:
      print(row[1]) ##fileName
      print("---------------------")
      print(row[2])##fileDir
      print(row[3])##fileType
      print(row[4])##fileLastModified
      print(str(row[5])+'\n')##fileSize


