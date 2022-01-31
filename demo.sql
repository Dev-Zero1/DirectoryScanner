use directoryscanner;

select * from filecontent;
select * from files;
-- ---------------------------------------------------------------
-- query to pull any CU's directories
-- ---------------------------------------------------------------
select * from files
WHERE fileDir LIKE '%C:%testFileDirectories%CCCU%'
order by fileDir;

select * from files
WHERE fileDir LIKE '%C:%testFileDirectories%EXCU%'
order by fileDir;

select * from files
WHERE fileDir LIKE '%C:%testFileDirectories%TRYCU%'
order by fileDir;

select * from files
WHERE fileDir LIKE '%C:%testFileDirectories%MYCU%'
order by fileDir;

select * from files
WHERE fileDir LIKE '%C:%testFileDirectories%ECCU%'
order by fileDir;
-- ---------------------------------------------------------------
-- query to pull a specific CU's files for migration data
-- ---------------------------------------------------------------
select * from files
WHERE fileDir LIKE '%C:%testFileDirectories%ECCU%fileTypeTest%'
order by filename;
-- ---------------------------------------------------------------
-- ---------------------------------------------------------------