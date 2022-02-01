use directoryscanner;

select * from filecontent where fileTxt != '';
select * from files;
-- ---------------------------------------------------------------
-- query to pull any CU's directories
-- ---------------------------------------------------------------
select f.fileId, f.fileName, fc.fileTxt, f.fileType,f.fileDir 
FROM files as f join filecontent as fc on f.fileId = fc.fileId
WHERE fileDir LIKE '%C:%testFileDirectories%CCCU%'
and fileTxt != ''
order by filetype;

select f.fileId, f.fileName, fc.fileTxt, f.fileType,f.fileDir 
FROM files as f join filecontent as fc on f.fileId = fc.fileId
WHERE fileDir LIKE '%C:%testFileDirectories%EXCU%'
and fileTxt != ''
order by filetype;

select f.fileId, f.fileName, fc.fileTxt, f.fileType,f.fileDir 
FROM files as f join filecontent as fc on f.fileId = fc.fileId
WHERE fileDir LIKE '%C:%testFileDirectories%TRYCU%'
and fileTxt != ''
order by filetype;

select f.fileId, f.fileName, fc.fileTxt, f.fileType,f.fileDir 
FROM files as f join filecontent as fc on f.fileId = fc.fileId
WHERE fileDir LIKE '%C:%testFileDirectories%MYCU%'
and fileTxt != ''
order by filetype;

select f.fileId, f.fileName, fc.fileTxt, f.fileType,f.fileDir 
FROM files as f join filecontent as fc on f.fileId = fc.fileId
WHERE fileDir LIKE '%C:%testFileDirectories%ECCU%'
and fileTxt != ''
order by filetype;
-- ---------------------------------------------------------------
-- query to pull file content
-- includes names, directories, type, and  id 
-- ---------------------------------------------------------------




-- ---------------------------------------------------------------
-- query to pull files with no content
-- includes names, directories, type, and id
-- ---------------------------------------------------------------
select f.fileId, f.fileName, fc.fileTxt, f.fileType,f.fileDir
FROM files as f join filecontent as fc on f.fileId = fc.fileId
and fileTxt = ''
order by f.fileDir,f.fileType;
