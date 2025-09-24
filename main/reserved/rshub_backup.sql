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
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `project_tasks`
--

LOCK TABLES `project_tasks` WRITE;
/*!40000 ALTER TABLE `project_tasks` DISABLE KEYS */;
INSERT INTO `project_tasks` VALUES (19,'project0 task0','fWNqfVZYK9h8W5TPzV2fua0ioerPy5',7),(20,'project0 task1','cmNbvCi4zHIZK1LxByiHHPADxSrOyM',7),(21,'project0 task2','4I5V40SvJqqhrOyUuB1mlZyXaLXTqA',7),(23,'project1 task1','7bTfMZUplQWjW4ZRQspT21aeAtcl5S',8),(24,'project1 task2','mTm2Ylc44fD2RbEW47kCzcGk74jxrF',8),(25,'project2 task0','4OnGvrn4b1qzL3dOAqHuW8t5McZMvE',9),(26,'project2 task1','hhKQgYJAmPikU3VZ3XDFbinpRpxdZv',9),(27,'project2 task2','PAOMPq8rJOYuEsDOlccCrlDTX3jlUU',9),(32,'project1 task0','10Z5DzTsVohd6q1NRhXqOcYO7De3pN',8);
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
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `task_status`
--

LOCK TABLES `task_status` WRITE;
/*!40000 ALTER TABLE `task_status` DISABLE KEYS */;
INSERT INTO `task_status` VALUES (19,'fWNqfVZYK9h8W5TPzV2fua0ioerPy5','running','2025-01-12 11:29:08'),(20,'cmNbvCi4zHIZK1LxByiHHPADxSrOyM','in queue','2025-01-12 09:59:08'),(21,'4I5V40SvJqqhrOyUuB1mlZyXaLXTqA','in queue','2025-01-12 09:59:08'),(23,'7bTfMZUplQWjW4ZRQspT21aeAtcl5S','in queue','2025-01-12 09:59:08'),(24,'mTm2Ylc44fD2RbEW47kCzcGk74jxrF','in queue','2025-01-12 09:59:08'),(25,'4OnGvrn4b1qzL3dOAqHuW8t5McZMvE','in queue','2025-01-12 09:59:08'),(26,'hhKQgYJAmPikU3VZ3XDFbinpRpxdZv','in queue','2025-01-12 09:59:08'),(27,'PAOMPq8rJOYuEsDOlccCrlDTX3jlUU','in queue','2025-01-12 09:59:08'),(32,'10Z5DzTsVohd6q1NRhXqOcYO7De3pN','in queue','2025-01-12 12:47:02');
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
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `task_times`
--

LOCK TABLES `task_times` WRITE;
/*!40000 ALTER TABLE `task_times` DISABLE KEYS */;
INSERT INTO `task_times` VALUES (19,'fWNqfVZYK9h8W5TPzV2fua0ioerPy5','2025-01-12 17:57:00','2025-01-12 18:34:00'),(20,'cmNbvCi4zHIZK1LxByiHHPADxSrOyM','2025-01-12 17:57:00',NULL),(21,'4I5V40SvJqqhrOyUuB1mlZyXaLXTqA','2025-01-12 17:57:00',NULL),(23,'7bTfMZUplQWjW4ZRQspT21aeAtcl5S','2025-01-12 17:57:00',NULL),(24,'mTm2Ylc44fD2RbEW47kCzcGk74jxrF','2025-01-12 17:57:00',NULL),(25,'4OnGvrn4b1qzL3dOAqHuW8t5McZMvE','2025-01-12 17:57:00',NULL),(26,'hhKQgYJAmPikU3VZ3XDFbinpRpxdZv','2025-01-12 17:57:00',NULL),(27,'PAOMPq8rJOYuEsDOlccCrlDTX3jlUU','2025-01-12 17:57:00',NULL),(32,'10Z5DzTsVohd6q1NRhXqOcYO7De3pN','2025-01-12 20:46:00',NULL);
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
INSERT INTO `tokens` VALUES (2,'wkyo!vmv9@*o0g8wemo?sbjqbs4mg@',1,2);
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
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tokentmp`
--

LOCK TABLES `tokentmp` WRITE;
/*!40000 ALTER TABLE `tokentmp` DISABLE KEYS */;
INSERT INTO `tokentmp` VALUES (1,'7ft3joitcnh4vmvwczn4n196kjl38c','2024-11-24 08:13:01',NULL),(2,'j70fa4vcmuetvvca7crueuem5qf8av','2024-11-24 08:14:59',NULL),(3,'a50u8rl5tgdrsw7lktxwyvgdz2i0it','2024-11-24 08:23:28',NULL),(4,'nae2m5p0bst0g6p23mu8q60zben0ut','2025-01-12 07:07:56',2),(5,'hphpkekh6oia6n14504byhk20zzdau','2025-01-12 07:22:27',NULL),(10,'rtloywfegws5dsyrwafzfmo11e1k5z','2025-01-12 08:30:23',8),(11,'wm96gfhd470a4z6fee7u2sld7hvb7y','2025-01-12 09:57:55',2);
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
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_projects`
--

LOCK TABLES `user_projects` WRITE;
/*!40000 ALTER TABLE `user_projects` DISABLE KEYS */;
INSERT INTO `user_projects` VALUES (7,'project0',2),(8,'project1',2),(9,'project2',2);
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
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (2,'User1','$2b$12$V8Sp8ivnC0PtYuy8eH0iSuSF63d6ry4wjmBGtcaZJfktrryDgDx0K','jiayang.23@intl.zju.edu.cn','浙江大学','嘉阳','陈','male','中国','manager','Web safety',0,1,'2025-01-12 07:07:56'),(8,'User2','$2b$12$/Rh7/Glf.eQsaBuKi6OzquYUn3TULUAWgcSOiqeXyxOhhtdXjyedO','2812104715@qq.com','浙江大学','嘉阳','陈','male','中国','manager','Web safety',100,0,'2025-01-12 08:30:23');
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

-- Dump completed on 2025-01-12 20:48:30
