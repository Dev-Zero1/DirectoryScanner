CREATE DATABASE directoryscanner;
use directoryscanner;

-- SET FOREIGN_KEY_CHECKS = 0;
-- SET @tempArray = NULL;
-- SELECT GROUP_CONCAT('`', table_name, '`') INTO @tempArray
-- FROM information_schema.tables WHERE table_schema = (SELECT DATABASE());
-- SELECT IFNULL(@tempArray,'dummy') INTO @tempArray;
-- SET @tempArray = CONCAT('DROP TABLE IF EXISTS ', @tempArray);
-- PREPARE stmt FROM @tempArray;
-- EXECUTE stmt;
-- DEALLOCATE PREPARE stmt;
-- SET FOREIGN_KEY_CHECKS = 1;

##DROP TABLE IF EXISTS `files`;

CREATE TABLE `files` (
  `fileId` int NOT NULL AUTO_INCREMENT,
  `fileName` varchar(150) NOT NULL,
  `fileDir` varchar(250) NOT NULL,
  `fileType` varchar(50) NOT NULL,  
  `lastModified` datetime NOT NULL,
  `fileCreated` datetime NOT NULL,
  `fileScannedAt` datetime NOT NULL,
  `fileSize_bytes` bigint unsigned,
  PRIMARY KEY (`fileId`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;

