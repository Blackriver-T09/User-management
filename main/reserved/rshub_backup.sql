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
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `project_tasks`
--

LOCK TABLES `project_tasks` WRITE;
/*!40000 ALTER TABLE `project_tasks` DISABLE KEYS */;
INSERT INTO `project_tasks` VALUES (1,'task1','eLLCQoJ2vnfdGceD4aaGFYxmKTEj9k',1),(2,'task2','s3Dkc71NICNaM6qRBASGBMpbwlf5KX',1),(3,'task3','klDoGa7cMGvI7yZAygaz9qps457GlL',1);
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
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `task_status`
--

LOCK TABLES `task_status` WRITE;
/*!40000 ALTER TABLE `task_status` DISABLE KEYS */;
INSERT INTO `task_status` VALUES (1,'eLLCQoJ2vnfdGceD4aaGFYxmKTEj9k','complete','2024-08-12 15:07:31'),(2,'s3Dkc71NICNaM6qRBASGBMpbwlf5KX','complete','2024-08-12 15:09:18'),(3,'klDoGa7cMGvI7yZAygaz9qps457GlL','in queue','2024-08-12 15:19:56');
/*!40000 ALTER TABLE `task_status` ENABLE KEYS */;
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
INSERT INTO `tokens` VALUES (1,'k!*ijl?jfx88hl!4cyadxt2bfa*chc',1,1),(2,'bw879?wepc#f56!!*@231vqd@@fg7z',1,2);
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
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tokentmp`
--

LOCK TABLES `tokentmp` WRITE;
/*!40000 ALTER TABLE `tokentmp` DISABLE KEYS */;
INSERT INTO `tokentmp` VALUES (5,'2i91gmbs9mrzob8atu6tbeyrbgo6fi','2024-08-12 14:11:44',1),(6,'esxo99mvl6mazefeoqeaabqakcidc5','2024-08-12 15:45:13',1),(7,'fp8232s9e869uu3f9mjqqfcm9lhfs0','2024-08-12 16:03:03',1),(8,'feagmot7mx0uc9q93rjvo6xv0yg9fd','2024-08-12 16:04:59',1),(9,'x9uvab55bzjympfospjv7ta8a2ihn0','2024-08-12 16:05:15',1),(10,'rge1clfbl65z15eyubz8qvfnh9z3d7','2024-08-12 16:08:07',1),(11,'86ez8lrvfdxzwskrscke8a3r5s9idn','2024-08-12 16:09:31',1),(12,'psl66h4n4d70kwqf3d3l3o1qy0axst','2024-08-12 17:29:51',1);
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
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_projects`
--

LOCK TABLES `user_projects` WRITE;
/*!40000 ALTER TABLE `user_projects` DISABLE KEYS */;
INSERT INTO `user_projects` VALUES (1,'Project1',1);
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
  PRIMARY KEY (`UserId`),
  UNIQUE KEY `Username` (`Username`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'heihe','$2b$12$Qb3zlqyQlXNhWBsKhh02quo32x50PLepbDcYziiEqq525ICJLcOGe','jiayang.23@intl.zju.edu.cn','浙江大学','嘉阳','陈','male','中国','manager','Web safety',100),(2,'User1','$2b$12$BN9CpUUDxUlXkb1V38j49egAinsXI5nvEkt/hbbrDLVTojvYr8Cva','jiayang.23@intl.zju.edu.cn','浙江大学','嘉阳','陈','male','中国','manager','Web safety',100);
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

-- Dump completed on 2024-08-13  1:39:44
