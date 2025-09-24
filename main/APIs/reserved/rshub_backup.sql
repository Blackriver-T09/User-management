-- MySQL dump 10.13  Distrib 8.0.37, for Win64 (x86_64)
--
-- Host: localhost    Database: rshub
-- ------------------------------------------------------
-- Server version	8.0.37

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `project_tasks`
--

DROP TABLE IF EXISTS `project_tasks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `project_tasks` (
  `ProjectTaskId` int NOT NULL AUTO_INCREMENT,
  `TaskName` varchar(50) NOT NULL,
  `TaskPath` varchar(100) NOT NULL,
  `user_project_id` int DEFAULT NULL,
  PRIMARY KEY (`ProjectTaskId`),
  UNIQUE KEY `ix_project_tasks_TaskPath` (`TaskPath`),
  KEY `user_project_id` (`user_project_id`),
  CONSTRAINT `project_tasks_ibfk_1` FOREIGN KEY (`user_project_id`) REFERENCES `user_projects` (`UserProjectId`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `project_tasks`
--

LOCK TABLES `project_tasks` WRITE;
/*!40000 ALTER TABLE `project_tasks` DISABLE KEYS */;
INSERT INTO `project_tasks` VALUES (10,'project0 task0','32IhRbkTlQtV0TyebYzU4GdM0ikwmm',4),(11,'project0 task1','42cuYVi3gQcDNtD1UduN9ujtNcH5DF',4),(12,'project0 task2','T32R6xtcTPqGyvXYMcTrtstVF5bPYW',4),(13,'project1 task0','nwjVBvdaT6XHGVbPdrczPMey4lOKoC',5),(14,'project1 task1','rE4HDsxQ2IWoGsnr80Ky741V1Mawc4',5),(15,'project1 task2','eDgPMiumVophCLv5b1em4BPYZVSheq',5),(16,'project2 task0','AbUz9Wbzg65Ddwi79szCLS3wyhJBWs',6),(17,'project2 task1','EfJ6fppBzyGPh2xZwaY3hLCt2zD53m',6),(18,'project2 task2','3eVCDMIgLutelODKfbVlLyebbpl304',6);
/*!40000 ALTER TABLE `project_tasks` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `task_status`
--

DROP TABLE IF EXISTS `task_status`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `task_status` (
  `StatusId` int NOT NULL AUTO_INCREMENT,
  `TaskPath` varchar(100) NOT NULL,
  `Status` varchar(50) NOT NULL,
  `UpdatedAt` datetime NOT NULL,
  PRIMARY KEY (`StatusId`),
  UNIQUE KEY `TaskPath` (`TaskPath`),
  CONSTRAINT `task_status_ibfk_1` FOREIGN KEY (`TaskPath`) REFERENCES `project_tasks` (`TaskPath`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `task_status`
--

LOCK TABLES `task_status` WRITE;
/*!40000 ALTER TABLE `task_status` DISABLE KEYS */;
INSERT INTO `task_status` VALUES (10,'32IhRbkTlQtV0TyebYzU4GdM0ikwmm','in queue','2024-11-24 10:22:40'),(11,'42cuYVi3gQcDNtD1UduN9ujtNcH5DF','in queue','2024-11-24 10:22:40'),(12,'T32R6xtcTPqGyvXYMcTrtstVF5bPYW','in queue','2024-11-24 10:22:40'),(13,'nwjVBvdaT6XHGVbPdrczPMey4lOKoC','in queue','2024-11-24 10:22:40'),(14,'rE4HDsxQ2IWoGsnr80Ky741V1Mawc4','in queue','2024-11-24 10:22:40'),(15,'eDgPMiumVophCLv5b1em4BPYZVSheq','in queue','2024-11-24 10:22:40'),(16,'AbUz9Wbzg65Ddwi79szCLS3wyhJBWs','in queue','2024-11-24 10:22:40'),(17,'EfJ6fppBzyGPh2xZwaY3hLCt2zD53m','in queue','2024-11-24 10:22:40'),(18,'3eVCDMIgLutelODKfbVlLyebbpl304','in queue','2024-11-24 10:22:40');
/*!40000 ALTER TABLE `task_status` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `task_times`
--

DROP TABLE IF EXISTS `task_times`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `task_times` (
  `TimeId` int NOT NULL AUTO_INCREMENT,
  `TaskPath` varchar(100) NOT NULL,
  `StartTime` datetime NOT NULL,
  `EndTime` datetime DEFAULT NULL,
  PRIMARY KEY (`TimeId`),
  UNIQUE KEY `TaskPath` (`TaskPath`),
  CONSTRAINT `task_times_ibfk_1` FOREIGN KEY (`TaskPath`) REFERENCES `project_tasks` (`TaskPath`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `task_times`
--

LOCK TABLES `task_times` WRITE;
/*!40000 ALTER TABLE `task_times` DISABLE KEYS */;
INSERT INTO `task_times` VALUES (10,'32IhRbkTlQtV0TyebYzU4GdM0ikwmm','2024-11-24 18:22:00',NULL),(11,'42cuYVi3gQcDNtD1UduN9ujtNcH5DF','2024-11-24 18:22:00',NULL),(12,'T32R6xtcTPqGyvXYMcTrtstVF5bPYW','2024-11-24 18:22:00',NULL),(13,'nwjVBvdaT6XHGVbPdrczPMey4lOKoC','2024-11-24 18:22:00',NULL),(14,'rE4HDsxQ2IWoGsnr80Ky741V1Mawc4','2024-11-24 18:22:00',NULL),(15,'eDgPMiumVophCLv5b1em4BPYZVSheq','2024-11-24 18:22:00',NULL),(16,'AbUz9Wbzg65Ddwi79szCLS3wyhJBWs','2024-11-24 18:22:00',NULL),(17,'EfJ6fppBzyGPh2xZwaY3hLCt2zD53m','2024-11-24 18:22:00',NULL),(18,'3eVCDMIgLutelODKfbVlLyebbpl304','2024-11-24 18:22:00',NULL);
/*!40000 ALTER TABLE `task_times` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tokens`
--

DROP TABLE IF EXISTS `tokens`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tokens` (
  `TokenId` int NOT NULL AUTO_INCREMENT,
  `Token` varchar(50) NOT NULL,
  `Level` int NOT NULL,
  `user_id` int DEFAULT NULL,
  PRIMARY KEY (`TokenId`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `tokens_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`UserId`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tokens`
--

LOCK TABLES `tokens` WRITE;
/*!40000 ALTER TABLE `tokens` DISABLE KEYS */;
INSERT INTO `tokens` VALUES (1,'3a6fb5xolo*q*#sgxt!!2r73n?$?co',1,1);
/*!40000 ALTER TABLE `tokens` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tokentmp`
--

DROP TABLE IF EXISTS `tokentmp`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tokentmp` (
  `tokenid` int NOT NULL AUTO_INCREMENT,
  `tempToken` varchar(255) NOT NULL,
  `createdAt` datetime DEFAULT NULL,
  `userId` int DEFAULT NULL,
  PRIMARY KEY (`tokenid`),
  UNIQUE KEY `tempToken` (`tempToken`),
  KEY `userId` (`userId`),
  CONSTRAINT `tokentmp_ibfk_1` FOREIGN KEY (`userId`) REFERENCES `users` (`UserId`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tokentmp`
--

LOCK TABLES `tokentmp` WRITE;
/*!40000 ALTER TABLE `tokentmp` DISABLE KEYS */;
INSERT INTO `tokentmp` VALUES (1,'7ft3joitcnh4vmvwczn4n196kjl38c','2024-11-24 08:13:01',1),(2,'j70fa4vcmuetvvca7crueuem5qf8av','2024-11-24 08:14:59',1),(3,'a50u8rl5tgdrsw7lktxwyvgdz2i0it','2024-11-24 08:23:28',1);
/*!40000 ALTER TABLE `tokentmp` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_projects`
--

DROP TABLE IF EXISTS `user_projects`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_projects` (
  `UserProjectId` int NOT NULL AUTO_INCREMENT,
  `ProjectName` varchar(50) NOT NULL,
  `user_id` int DEFAULT NULL,
  PRIMARY KEY (`UserProjectId`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `user_projects_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`UserId`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_projects`
--

LOCK TABLES `user_projects` WRITE;
/*!40000 ALTER TABLE `user_projects` DISABLE KEYS */;
INSERT INTO `user_projects` VALUES (4,'project0',1),(5,'project1',1),(6,'project2',1);
/*!40000 ALTER TABLE `user_projects` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `UserId` int NOT NULL AUTO_INCREMENT,
  `Username` varchar(50) NOT NULL,
  `Password` varchar(255) NOT NULL,
  `Email` varchar(50) NOT NULL,
  `Organization` varchar(50) DEFAULT NULL,
  `FirstName` varchar(50) DEFAULT NULL,
  `LastName` varchar(50) DEFAULT NULL,
  `Gender` varchar(10) DEFAULT NULL,
  `Country` varchar(50) DEFAULT NULL,
  `Affiliation` varchar(100) DEFAULT NULL,
  `ResearchArea` varchar(100) DEFAULT NULL,
  `Credits` int DEFAULT NULL,
  `Activated` tinyint(1) NOT NULL,
  `createdAt` datetime NOT NULL,
  PRIMARY KEY (`UserId`),
  UNIQUE KEY `Username` (`Username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'User1','$2b$12$nAjTlFa1u8CBJQ2f1Zh.dOhRAjlzzA6rWIBHkMc7gSjyWybDx.qBW','jiayang.23@intl.zju.edu.cn','浙江大学','嘉阳','陈','male','中国','manager','Web safety',100,1,'2024-11-24 08:13:01');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-11-24 20:32:21
