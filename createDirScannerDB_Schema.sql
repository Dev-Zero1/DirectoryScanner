use directoryscanner;

SET FOREIGN_KEY_CHECKS = 0;
SET @tempArray = NULL;
SELECT GROUP_CONCAT('`', table_name, '`') INTO @tempArray
FROM information_schema.tables WHERE table_schema = (SELECT DATABASE());
SELECT IFNULL(@tempArray,'dummy') INTO @tempArray;
SET @tempArray = CONCAT('DROP TABLE IF EXISTS ', @tempArray);
PREPARE stmt FROM @tempArray;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;
SET FOREIGN_KEY_CHECKS = 1;

DROP TABLE IF EXISTS `files`;

CREATE TABLE `files` (
  `fileId` int(11) NOT NULL AUTO_INCREMENT,
  `fileName` varchar(50) NOT NULL,
  `fileDir` varchar(50) NOT NULL,
  `fileType` varchar(50) NOT NULL,  
  `lastModified` datetime NOT NULL,
  `fileSize` int(11),
  PRIMARY KEY (`fileId`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;

-- INSERT INTO `files` VALUES
-- (1,'index.html', 'C:\\inetpub\\wwroot\\','html','2019-01-01 00:00:00', 1),
-- (2,'articles.html', 'C:\\inetpub\\wwroot\\','html','2019-01-02 00:00:00', 1),
-- (3,'data.xml', 'C:\\inetpub\\wwroot\\data','xml','2019-01-02 00:00:00', 1),
-- (4,'img.png', 'C:\\inetpub\\wwroot\\images','png','2019-01-02 00:00:00', 1);

