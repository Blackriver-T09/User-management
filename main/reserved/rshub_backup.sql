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
INSERT INTO `project_tasks` VALUES (1,'project0 task0','vyUPrXjZnWFEC5WSKF92coGt5DjvVc',1),(2,'project0 task1','23XYbFWAuZvYOmx1aXT3UbESDaiWrq',1),(3,'project0 task2','3mdD7hVABVwvcasUR4AJIZikoVTQW6',1),(4,'project1 task0','h8tHhX6WwYycuCGWqNpCufkzXLJoAj',2),(5,'project1 task1','7iYCbs7L3N6t2TJ4qwSvIhxWjp7nBe',2),(6,'project1 task2','bFBOe6evXvEiFkrFYeqJdw8dWNDQ5o',2),(7,'project2 task0','T1FkvLmtv6Zh1gCfXmzeazt4sO4XHr',3),(8,'project2 task1','JhBhjomwm8gCOvJfqlgQX2LU1wYqgL',3),(9,'project2 task2','RQ5cSzZVsarXbdheyOkmc6GjnEEzVA',3),(10,'project0 task0','XgS7Qr5SiljOXGJwr1v1CNIfQxpo1Z',1),(11,'project0 task1','SLVWF2YFa7AawmDR8KACx7jksV1t7Q',1),(12,'project0 task2','ooDGrUSQodJaijyEVDcRYSfa4ftdDc',1),(13,'project1 task0','qDK1L9oUcMi2ofjBrrsBhN3kRB2F5f',2),(14,'project1 task1','tV6nFiQYyOnPQ4F0kvZWOXu10ME0kJ',2),(15,'project1 task2','1qtrl0h2AbjFjpGS0DfLZQxaERfLV2',2),(16,'project2 task0','fs3JEWGbjZUGfTvHfHMuvlMF1ll6PU',3),(17,'project2 task1','5KLp7yn6UEg9gF0mh1HVeZULNX5qxs',3),(18,'project2 task2','4VXuCcUp7EkezRlKn8Cx8IZHRZ2ar6',3);
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
INSERT INTO `task_status` VALUES (1,'vyUPrXjZnWFEC5WSKF92coGt5DjvVc','in queue','2024-09-24 15:50:28'),(2,'23XYbFWAuZvYOmx1aXT3UbESDaiWrq','in queue','2024-09-24 15:50:28'),(3,'3mdD7hVABVwvcasUR4AJIZikoVTQW6','in queue','2024-09-24 15:50:28'),(4,'h8tHhX6WwYycuCGWqNpCufkzXLJoAj','in queue','2024-09-24 15:50:28'),(5,'7iYCbs7L3N6t2TJ4qwSvIhxWjp7nBe','in queue','2024-09-24 15:50:28'),(6,'bFBOe6evXvEiFkrFYeqJdw8dWNDQ5o','in queue','2024-09-24 15:50:28'),(7,'T1FkvLmtv6Zh1gCfXmzeazt4sO4XHr','in queue','2024-09-24 15:50:28'),(8,'JhBhjomwm8gCOvJfqlgQX2LU1wYqgL','in queue','2024-09-24 15:50:28'),(9,'RQ5cSzZVsarXbdheyOkmc6GjnEEzVA','in queue','2024-09-24 15:50:28'),(10,'XgS7Qr5SiljOXGJwr1v1CNIfQxpo1Z','in queue','2024-09-24 16:22:07'),(11,'SLVWF2YFa7AawmDR8KACx7jksV1t7Q','in queue','2024-09-24 16:22:07'),(12,'ooDGrUSQodJaijyEVDcRYSfa4ftdDc','in queue','2024-09-24 16:22:07'),(13,'qDK1L9oUcMi2ofjBrrsBhN3kRB2F5f','in queue','2024-09-24 16:22:07'),(14,'tV6nFiQYyOnPQ4F0kvZWOXu10ME0kJ','in queue','2024-09-24 16:22:07'),(15,'1qtrl0h2AbjFjpGS0DfLZQxaERfLV2','in queue','2024-09-24 16:22:07'),(16,'fs3JEWGbjZUGfTvHfHMuvlMF1ll6PU','in queue','2024-09-24 16:22:07'),(17,'5KLp7yn6UEg9gF0mh1HVeZULNX5qxs','in queue','2024-09-24 16:22:07'),(18,'4VXuCcUp7EkezRlKn8Cx8IZHRZ2ar6','in queue','2024-09-24 16:22:07');
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
INSERT INTO `task_times` VALUES (1,'vyUPrXjZnWFEC5WSKF92coGt5DjvVc','2024-09-24 23:50:00',NULL),(2,'23XYbFWAuZvYOmx1aXT3UbESDaiWrq','2024-09-24 23:50:00',NULL),(3,'3mdD7hVABVwvcasUR4AJIZikoVTQW6','2024-09-24 23:50:00',NULL),(4,'h8tHhX6WwYycuCGWqNpCufkzXLJoAj','2024-09-24 23:50:00',NULL),(5,'7iYCbs7L3N6t2TJ4qwSvIhxWjp7nBe','2024-09-24 23:50:00',NULL),(6,'bFBOe6evXvEiFkrFYeqJdw8dWNDQ5o','2024-09-24 23:50:00',NULL),(7,'T1FkvLmtv6Zh1gCfXmzeazt4sO4XHr','2024-09-24 23:50:00',NULL),(8,'JhBhjomwm8gCOvJfqlgQX2LU1wYqgL','2024-09-24 23:50:00',NULL),(9,'RQ5cSzZVsarXbdheyOkmc6GjnEEzVA','2024-09-24 23:50:00',NULL),(10,'XgS7Qr5SiljOXGJwr1v1CNIfQxpo1Z','2024-09-25 00:21:00',NULL),(11,'SLVWF2YFa7AawmDR8KACx7jksV1t7Q','2024-09-25 00:21:00',NULL),(12,'ooDGrUSQodJaijyEVDcRYSfa4ftdDc','2024-09-25 00:21:00',NULL),(13,'qDK1L9oUcMi2ofjBrrsBhN3kRB2F5f','2024-09-25 00:21:00',NULL),(14,'tV6nFiQYyOnPQ4F0kvZWOXu10ME0kJ','2024-09-25 00:21:00',NULL),(15,'1qtrl0h2AbjFjpGS0DfLZQxaERfLV2','2024-09-25 00:21:00',NULL),(16,'fs3JEWGbjZUGfTvHfHMuvlMF1ll6PU','2024-09-25 00:21:00',NULL),(17,'5KLp7yn6UEg9gF0mh1HVeZULNX5qxs','2024-09-25 00:21:00',NULL),(18,'4VXuCcUp7EkezRlKn8Cx8IZHRZ2ar6','2024-09-25 00:21:00',NULL);
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
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tokens`
--

LOCK TABLES `tokens` WRITE;
/*!40000 ALTER TABLE `tokens` DISABLE KEYS */;
INSERT INTO `tokens` VALUES (1,'g2!4ubt#mn!kyocbzh**#?6p6@*x3j',1,1),(2,'6*dt7danjhrz!*wnc?wrrtw#r*oof5',1,2);
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
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tokentmp`
--

LOCK TABLES `tokentmp` WRITE;
/*!40000 ALTER TABLE `tokentmp` DISABLE KEYS */;
INSERT INTO `tokentmp` VALUES (1,'1cdngl0hj3jb1vsfodtslxansccgvm','2024-09-23 07:44:16',1),(2,'kf49r7wmzkuzodlssc1xvi8g5p9wk6','2024-09-23 07:45:43',1),(3,'i3q951t1bbtz0h9kxxzkpul9pxlxnq','2024-09-23 07:46:09',2),(4,'vo9g62wbrpa43s02ejwd40q1bzvder','2024-09-23 07:47:07',2),(5,'zpo0t77vbo86oe0cwmdu3s7yhblauu','2024-09-23 13:08:26',1);
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
INSERT INTO `user_projects` VALUES (1,'project0',1),(2,'project1',1),(3,'project2',1),(4,'project0',1),(5,'project1',1),(6,'project2',1);
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
  PRIMARY KEY (`UserId`),
  UNIQUE KEY `Username` (`Username`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'User1','$2b$12$pJRK8WdIsHLRX0te4z357eGYKHFMRxgHg2N4hmgxgXRKOcalqV/iG','jiayang.23@intl.zju.edu.cn','浙江大学','嘉阳','陈','male','中国','manager','Web safety',100,1),(2,'User2','$2b$12$B1xqOZZT5KWqJMWiA2Red.MgUbKfNYo/X6giHLyo1ehsvCHaMX3nu','jiayang.23@intl.zju.edu.cn','浙江大学','嘉阳','陈','male','中国','manager','Web safety',100,1);
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

-- Dump completed on 2024-09-25  0:26:58
