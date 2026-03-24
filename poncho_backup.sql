-- MySQL dump 10.13  Distrib 8.0.45, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: poncho
-- ------------------------------------------------------
-- Server version	8.0.45

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
-- Current Database: `poncho`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `poncho` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;

USE `poncho`;

--
-- Table structure for table `app_settings`
--

DROP TABLE IF EXISTS `app_settings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `app_settings` (
  `k` varchar(60) COLLATE utf8mb4_unicode_ci NOT NULL,
  `v` varchar(225) COLLATE utf8mb4_unicode_ci NOT NULL,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`k`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `app_settings`
--

LOCK TABLES `app_settings` WRITE;
/*!40000 ALTER TABLE `app_settings` DISABLE KEYS */;
INSERT INTO `app_settings` VALUES ('TOKEN_TTL_HOURS','24','2026-03-22 16:00:41');
/*!40000 ALTER TABLE `app_settings` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `email_verification_codes`
--

DROP TABLE IF EXISTS `email_verification_codes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `email_verification_codes` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `id_user` bigint NOT NULL,
  `code_hash` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `expires_at` datetime NOT NULL,
  `used` tinyint(1) DEFAULT '0',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `id_user` (`id_user`),
  CONSTRAINT `email_verification_codes_ibfk_1` FOREIGN KEY (`id_user`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `email_verification_codes`
--

LOCK TABLES `email_verification_codes` WRITE;
/*!40000 ALTER TABLE `email_verification_codes` DISABLE KEYS */;
/*!40000 ALTER TABLE `email_verification_codes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `enrolment`
--

DROP TABLE IF EXISTS `enrolment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `enrolment` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `id_student` bigint NOT NULL,
  `id_project` int NOT NULL,
  `enrolment_date` datetime DEFAULT CURRENT_TIMESTAMP,
  `id_status` tinyint DEFAULT NULL,
  `id_token` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `id_student` (`id_student`),
  KEY `id_project` (`id_project`),
  KEY `id_status` (`id_status`),
  KEY `id_token` (`id_token`),
  CONSTRAINT `enrolment_ibfk_1` FOREIGN KEY (`id_student`) REFERENCES `users` (`id`),
  CONSTRAINT `enrolment_ibfk_2` FOREIGN KEY (`id_project`) REFERENCES `project` (`id`),
  CONSTRAINT `enrolment_ibfk_3` FOREIGN KEY (`id_status`) REFERENCES `status` (`id`),
  CONSTRAINT `enrolment_ibfk_4` FOREIGN KEY (`id_token`) REFERENCES `token` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `enrolment`
--

LOCK TABLES `enrolment` WRITE;
/*!40000 ALTER TABLE `enrolment` DISABLE KEYS */;
/*!40000 ALTER TABLE `enrolment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `modality`
--

DROP TABLE IF EXISTS `modality`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `modality` (
  `id` tinyint NOT NULL AUTO_INCREMENT,
  `name` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `modality`
--

LOCK TABLES `modality` WRITE;
/*!40000 ALTER TABLE `modality` DISABLE KEYS */;
INSERT INTO `modality` VALUES (1,'en linea'),(3,'mixto'),(2,'presencial');
/*!40000 ALTER TABLE `modality` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `partner`
--

DROP TABLE IF EXISTS `partner`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `partner` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=96 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `partner`
--

LOCK TABLES `partner` WRITE;
/*!40000 ALTER TABLE `partner` DISABLE KEYS */;
INSERT INTO `partner` VALUES (4,'LAD'),(5,'LPS'),(6,'ICT'),(7,'IDM'),(8,'IRS'),(9,'ITC'),(10,'ITD'),(12,'LDI'),(13,'LC'),(14,'LNB'),(15,'LAE'),(16,'ING'),(17,'IAG'),(18,'IAL'),(19,'IBT'),(20,'IC'),(21,'IDS'),(22,'IE'),(23,'IFI'),(24,'IID'),(25,'IIS'),(26,'IM'),(27,'IMD'),(28,'IMT'),(29,'INA'),(30,'IQ'),(31,'NEG'),(32,'BGB'),(34,'LAF'),(35,'LDE'),(36,'LDO'),(37,'LEM'),(38,'LIN'),(39,'LIT'),(40,'HCM'),(41,'LEI'),(42,'LLE'),(43,'LTM'),(44,'CPF'),(45,'LHD'),(46,'LED'),(47,'LRI'),(64,'AAD'),(65,'ARQ'),(66,'BA'),(67,'LUB'),(68,'CIS'),(69,'BIR'),(70,'LEC'),(71,'LTP'),(72,'BIE'),(73,'BME'),(74,'SLD'),(75,'LBC'),(76,'MC'),(77,'MO'),(78,'BBA'),(79,'BFI'),(80,'BM'),(95,'Sin preferencia');
/*!40000 ALTER TABLE `partner` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `partner_group`
--

DROP TABLE IF EXISTS `partner_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `partner_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(60) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_partner_group_name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `partner_group`
--

LOCK TABLES `partner_group` WRITE;
/*!40000 ALTER TABLE `partner_group` DISABLE KEYS */;
INSERT INTO `partner_group` VALUES (2,'Arq, Arte y Diseño'),(6,'Ciencias Sociales y Gobierno '),(4,'Humanidades y Educación'),(1,'Ingeniería y Ciencias Computación'),(5,'Medicina y Ciencias de la Salud'),(3,'Todas las carreras de negocios');
/*!40000 ALTER TABLE `partner_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `partner_group_member`
--

DROP TABLE IF EXISTS `partner_group_member`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `partner_group_member` (
  `group_id` int NOT NULL,
  `partner_id` int NOT NULL,
  PRIMARY KEY (`group_id`,`partner_id`),
  KEY `partner_id` (`partner_id`),
  CONSTRAINT `partner_group_member_ibfk_1` FOREIGN KEY (`group_id`) REFERENCES `partner_group` (`id`) ON DELETE CASCADE,
  CONSTRAINT `partner_group_member_ibfk_2` FOREIGN KEY (`partner_id`) REFERENCES `partner` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `partner_group_member`
--

LOCK TABLES `partner_group_member` WRITE;
/*!40000 ALTER TABLE `partner_group_member` DISABLE KEYS */;
INSERT INTO `partner_group_member` VALUES (2,4),(5,5),(1,6),(1,7),(1,8),(1,9),(1,10),(2,12),(4,13),(5,14),(3,15),(1,16),(1,17),(1,18),(1,19),(1,20),(1,21),(1,22),(1,23),(1,24),(1,25),(1,26),(1,27),(1,28),(1,29),(1,30),(3,31),(3,32),(3,34),(3,35),(3,36),(3,37),(3,38),(3,39),(4,40),(4,41),(4,42),(4,43),(3,44),(4,45),(6,46),(6,47),(2,64),(2,65),(2,66),(2,67),(6,68),(6,69),(6,70),(6,71),(1,72),(1,73),(5,74),(5,75),(5,76),(5,77),(3,78),(3,79),(3,80);
/*!40000 ALTER TABLE `partner_group_member` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `project`
--

DROP TABLE IF EXISTS `project`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `project` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `id_partner` int NOT NULL,
  `id_modality` tinyint NOT NULL,
  `id_week_days` tinyint NOT NULL,
  `id_schedule` tinyint NOT NULL,
  `slots` int NOT NULL,
  `schedule_description` varchar(256) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `team_owners` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `objectives` text COLLATE utf8mb4_unicode_ci,
  `activities` text COLLATE utf8mb4_unicode_ci,
  `clave` varchar(30) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `competencies` text COLLATE utf8mb4_unicode_ci,
  `location` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `duration` varchar(80) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `audience` varchar(120) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `max_hours` int DEFAULT NULL,
  `comments` text COLLATE utf8mb4_unicode_ci,
  `season` varchar(40) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `academy_mode` enum('ALL','GROUP','CUSTOM') COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'ALL',
  `academy_group_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `id_partner` (`id_partner`),
  KEY `id_modality` (`id_modality`),
  KEY `id_week_days` (`id_week_days`),
  KEY `id_schedule` (`id_schedule`),
  KEY `fk_project_academy_group` (`academy_group_id`),
  CONSTRAINT `fk_project_academy_group` FOREIGN KEY (`academy_group_id`) REFERENCES `partner_group` (`id`),
  CONSTRAINT `project_ibfk_1` FOREIGN KEY (`id_partner`) REFERENCES `partner` (`id`),
  CONSTRAINT `project_ibfk_2` FOREIGN KEY (`id_modality`) REFERENCES `modality` (`id`),
  CONSTRAINT `project_ibfk_3` FOREIGN KEY (`id_week_days`) REFERENCES `week_days` (`id`),
  CONSTRAINT `project_ibfk_4` FOREIGN KEY (`id_schedule`) REFERENCES `schedule` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `project`
--

LOCK TABLES `project` WRITE;
/*!40000 ALTER TABLE `project` DISABLE KEYS */;
INSERT INTO `project` VALUES (1,'Reconocimiento de los Derechos Humanos con enfoque de cultura de paz.',95,1,1,3,1,'Por acordar con OSF. Lunes, miércoles y viernes con sesiones de dos horas','Vinculación Ciudadana El Salto','Crear proyectos alcanzables que favorezcan y apoyen la transformación de contextos de violencia.','1. Capacitar a través de un taller de inducción .\n2. Generar lluvia de ideas de propuestas.\n3. Desarrollar un laboratorio de proyectos.\n4. Diseñar un proyecto productivo.','WA1067 Grupo 407','El alumnado adquirió las herramientas necesarias para reconocer y aplicar correctamente los principios de la corresponsabilidad social y el trabajo humanitario.','En línea','10 semanas','Niñas, niños y adolescentes',120,'El alumnado adquirirá herramientas y conocerá los espacios donde podrá aplicar su prototipo. Además, se le presentarán los estándares nacionales e internacionales, fomentando la sensibilización y el reconocimiento de las violencias hacia niñas, niños y adolescentes, con el fin de favorecer la transición hacia una cultura de paz y la creación de entornos seguros para estos grupos vulnerables.','Febrero - Junio','ALL',NULL);
/*!40000 ALTER TABLE `project` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `project_partner_pref`
--

DROP TABLE IF EXISTS `project_partner_pref`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `project_partner_pref` (
  `project_id` int NOT NULL,
  `partner_id` int NOT NULL,
  PRIMARY KEY (`project_id`,`partner_id`),
  KEY `fk_ppp_partner` (`partner_id`),
  CONSTRAINT `fk_ppp_partner` FOREIGN KEY (`partner_id`) REFERENCES `partner` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_ppp_project` FOREIGN KEY (`project_id`) REFERENCES `project` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `project_partner_pref`
--

LOCK TABLES `project_partner_pref` WRITE;
/*!40000 ALTER TABLE `project_partner_pref` DISABLE KEYS */;
/*!40000 ALTER TABLE `project_partner_pref` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `schedule`
--

DROP TABLE IF EXISTS `schedule`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `schedule` (
  `id` tinyint NOT NULL AUTO_INCREMENT,
  `name` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `schedule`
--

LOCK TABLES `schedule` WRITE;
/*!40000 ALTER TABLE `schedule` DISABLE KEYS */;
INSERT INTO `schedule` VALUES (1,'matutino'),(3,'mixto'),(2,'vespertino');
/*!40000 ALTER TABLE `schedule` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `status`
--

DROP TABLE IF EXISTS `status`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `status` (
  `id` tinyint NOT NULL AUTO_INCREMENT,
  `name` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `status`
--

LOCK TABLES `status` WRITE;
/*!40000 ALTER TABLE `status` DISABLE KEYS */;
INSERT INTO `status` VALUES (2,'aceptado'),(1,'pendiente'),(3,'rechazado');
/*!40000 ALTER TABLE `status` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `token`
--

DROP TABLE IF EXISTS `token`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `token` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `id_project` int DEFAULT NULL,
  `token` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `used` tinyint(1) DEFAULT '0',
  `revoked` tinyint(1) NOT NULL DEFAULT '0',
  `expires_at` datetime DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `token` (`token`),
  KEY `id_project` (`id_project`),
  CONSTRAINT `token_ibfk_1` FOREIGN KEY (`id_project`) REFERENCES `project` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `token`
--

LOCK TABLES `token` WRITE;
/*!40000 ALTER TABLE `token` DISABLE KEYS */;
INSERT INTO `token` VALUES (1,1,'J95HWJKNYW',0,1,NULL,'2026-03-22 14:40:38'),(2,1,'2XUDS4GZXW',0,0,'2026-03-24 15:21:38','2026-03-23 15:21:38');
/*!40000 ALTER TABLE `token` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `first_name` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `second_name` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `p_last_name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `m_last_name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `enrolment_number` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `phone_number` varchar(12) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `password` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `salt` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  `admin` tinyint(1) NOT NULL DEFAULT '0',
  `degree` varchar(5) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `semester` tinyint DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `enrolment_number` (`enrolment_number`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `week_days`
--

DROP TABLE IF EXISTS `week_days`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `week_days` (
  `id` tinyint NOT NULL AUTO_INCREMENT,
  `name` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `week_days`
--

LOCK TABLES `week_days` WRITE;
/*!40000 ALTER TABLE `week_days` DISABLE KEYS */;
INSERT INTO `week_days` VALUES (1,'entre semana'),(2,'fines de semana'),(3,'mixto');
/*!40000 ALTER TABLE `week_days` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'poncho'
--

--
-- Dumping routines for database 'poncho'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-03-23 17:47:55
