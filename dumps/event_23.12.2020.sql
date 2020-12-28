-- MySQL dump 10.13  Distrib 8.0.22, for Linux (x86_64)
--
-- Host: localhost    Database: mydb
-- ------------------------------------------------------
-- Server version	8.0.22-0ubuntu0.20.04.3

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
-- Table structure for table `alembic_version`
--


--
-- Table structure for table `arena`
--

DROP TABLE IF EXISTS `arena`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `arena` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `description` varchar(500) DEFAULT NULL,
  `edit_arena` datetime DEFAULT NULL,
  `created_arena` datetime DEFAULT NULL,
  `city_id` int DEFAULT NULL,
  `hall_size` varchar(255) DEFAULT NULL,
  `light` varchar(255) DEFAULT NULL,
  `number_of_seats` varchar(255) DEFAULT NULL,
  `sound` varchar(255) DEFAULT NULL,
  `phone_admin` varchar(255) DEFAULT NULL,
  `phone_light` varchar(255) DEFAULT NULL,
  `phone_sound` varchar(255) DEFAULT NULL,
  `razgruzka` varchar(255) DEFAULT NULL,
  `typehall_id` int DEFAULT NULL,
  `address` varchar(255) DEFAULT NULL,
  `img` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `city_id` (`city_id`),
  KEY `typehall_id` (`typehall_id`),
  CONSTRAINT `arena_ibfk_1` FOREIGN KEY (`city_id`) REFERENCES `city` (`id`),
  CONSTRAINT `arena_ibfk_2` FOREIGN KEY (`typehall_id`) REFERENCES `typehall` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=78 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `arena`
--

LOCK TABLES `arena` WRITE;
/*!40000 ALTER TABLE `arena` DISABLE KEYS */;
INSERT INTO `arena` VALUES (1,'БКЗ. Большой Концертынй Зал',NULL,'2020-12-17 17:00:23',NULL,14,NULL,NULL,'3727','Meyer Sound Milo',' 8 (812) 275-13-00',NULL,NULL,NULL,7,NULL,NULL),(2,'ВКЗ. Воронежский концертный зал',NULL,'2020-12-17 17:00:30',NULL,12,NULL,NULL,'782',NULL,'+7 (473) 254-56-66',NULL,NULL,NULL,7,NULL,NULL),(3,'Крокус',NULL,'2020-11-13 23:57:11',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(4,'Театр золотое кольцо','','2020-12-22 14:46:21',NULL,13,'','',NULL,'','','','','',6,'',NULL),(5,'EventHall','Площадка в торговом центре','2020-12-22 17:09:37',NULL,12,'','ClayPaky','5000','Meyer Sound Mica','8 (473) 228-02-01','','','',7,'',NULL),(6,'Тинькофф Арена','','2020-12-22 12:59:26',NULL,14,'','',NULL,'','','','','',7,'',NULL),(8,'Барвиха','В барвихенском dрайоне','2020-12-17 17:01:12',NULL,13,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,1,NULL,NULL),(14,'КЗ Губернский','','2020-12-22 13:01:33','2020-11-14 20:24:29',19,'','',NULL,'','','','','',2,'',NULL),(25,'ДК Яуза',NULL,NULL,'2020-11-20 19:57:37',27,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(26,'ДК Салют',NULL,NULL,'2020-11-20 20:06:20',13,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(27,'АЗЛК','','2020-12-22 17:10:56','2020-11-20 20:07:44',13,'','','','','','','','',2,'',NULL),(28,'КДЦ Сатурн',NULL,NULL,'2020-11-20 20:07:58',30,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(29,'ДК Металлист',NULL,NULL,'2020-11-20 20:32:57',33,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(30,'КДЦ Губернский',NULL,NULL,'2020-11-20 20:33:19',34,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(31,'Театр Оперы и Балета РК',NULL,NULL,'2020-11-20 20:33:54',35,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(32,'Вятская Филармония',NULL,NULL,'2020-11-20 20:34:16',36,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(33,'Бекстейдж','','2020-12-17 19:23:48','2020-11-20 20:34:38',13,'','',NULL,'','','','','',8,'',NULL),(34,'ДК Якова Ухсая',NULL,NULL,'2020-11-20 20:35:06',38,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(35,'ДК ХХХ-летия Победы',NULL,NULL,'2020-11-20 20:35:33',39,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(36,'КЗ Сары Садыковой',NULL,NULL,'2020-11-20 20:35:50',40,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(37,'ОДК Пролетарка',NULL,NULL,'2020-11-20 20:36:18',33,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(38,'ДК Гагарина',NULL,NULL,'2020-11-20 20:36:38',42,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(39,'КЦ Зеленоград',NULL,NULL,'2020-11-20 20:36:59',24,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(40,'ДК Мир',NULL,NULL,'2020-11-20 20:37:17',43,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(41,'ДК Калинина','','2020-12-17 19:11:30','2020-11-20 20:37:35',44,'','',NULL,'','','','','',2,'',NULL),(42,'ДС Звездный',NULL,NULL,'2020-11-20 20:38:17',46,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(43,'ДИ Нефтяник','','2020-12-17 19:11:19','2020-11-20 20:38:38',48,'','',NULL,'','','','','',2,'',NULL),(44,'Дворец Искуств',NULL,NULL,'2020-11-20 20:38:56',49,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(52,'Триумф','','2020-12-18 19:21:02','2020-12-18 19:16:43',25,'','',NULL,'','','','','',2,'',NULL),(53,'ДК Карла Маркса','','2020-12-18 19:37:54','2020-12-18 19:37:54',26,'','','','','','','','',2,'',NULL),(54,'Городской концертный зал','','2020-12-18 19:46:18','2020-12-18 19:46:18',28,'','','','','','','','',7,'',NULL),(55,'Конькобежный центр','','2020-12-18 19:48:51','2020-12-18 19:48:51',29,'','','','','','','','',9,'',NULL),(56,'ДК Подмосковье','','2020-12-18 19:53:10','2020-12-18 19:53:10',31,'','','','','','','','',2,'',NULL),(57,'Ласточка','','2020-12-21 21:06:15','2020-12-21 21:06:15',13,'','','','','','','','',8,'',NULL);
/*!40000 ALTER TABLE `arena` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `arena_city`
--

DROP TABLE IF EXISTS `arena_city`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `arena_city` (
  `city_id` int DEFAULT NULL,
  `arena_id` int DEFAULT NULL,
  KEY `city_id` (`city_id`),
  KEY `arena_id` (`arena_id`),
  CONSTRAINT `arena_city_ibfk_1` FOREIGN KEY (`city_id`) REFERENCES `city` (`id`),
  CONSTRAINT `arena_city_ibfk_2` FOREIGN KEY (`arena_id`) REFERENCES `arena` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;







--
-- Table structure for table `event`
--

DROP TABLE IF EXISTS `event`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `event` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `artist_id` int DEFAULT NULL,
  `date_event` date DEFAULT NULL,
  `description` varchar(500) DEFAULT NULL,
  `city_id` int DEFAULT NULL,
  `arena_id` int DEFAULT NULL,
  `edit_event` datetime DEFAULT NULL,
  `created_event` datetime DEFAULT NULL,
  `tour_id` int DEFAULT NULL,
  `time_event` time DEFAULT NULL,
  `typeevent_id` int DEFAULT NULL,
  `user_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `artist_id` (`artist_id`),
  KEY `city_id` (`city_id`),
  KEY `arena_id` (`arena_id`),
  KEY `tour_id` (`tour_id`),
  KEY `typeevent_id` (`typeevent_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `event_ibfk_1` FOREIGN KEY (`artist_id`) REFERENCES `artist` (`id`),
  CONSTRAINT `event_ibfk_2` FOREIGN KEY (`city_id`) REFERENCES `city` (`id`),
  CONSTRAINT `event_ibfk_3` FOREIGN KEY (`arena_id`) REFERENCES `arena` (`id`),
  CONSTRAINT `event_ibfk_5` FOREIGN KEY (`tour_id`) REFERENCES `tour` (`id`),
  CONSTRAINT `event_ibfk_6` FOREIGN KEY (`typeevent_id`) REFERENCES `typeevent` (`id`),
  CONSTRAINT `event_ibfk_7` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=42 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `event`
--

LOCK TABLES `event` WRITE;
/*!40000 ALTER TABLE `event` DISABLE KEYS */;
INSERT INTO `event` VALUES (1,'Ноябрский Тур',1,'2020-11-15','Добавить описание для!',14,1,'2020-11-16 19:25:37',NULL,15,'19:00:00',1,14),(5,'',1,'2020-11-22','',14,1,'2020-11-20 20:11:06',NULL,2,'19:00:00',1,NULL),(6,'Королев',7,'2020-11-12',NULL,30,28,'2020-11-20 20:17:01',NULL,14,'19:00:00',NULL,15),(7,'Сум',6,'2020-12-28','',33,29,'2020-11-20 20:39:28',NULL,NULL,'19:00:00',NULL,5),(8,'',6,'2020-12-26','',34,30,'2020-11-20 21:06:05',NULL,3,'19:00:00',NULL,5),(9,'',6,'2020-12-25','',35,31,'2020-11-20 21:07:55',NULL,3,'19:00:00',NULL,5),(15,'wefwfew',1,'2020-11-11','wfew',37,1,'2020-11-23 16:03:28',NULL,14,'19:00:00',NULL,NULL),(17,'сольник',8,'2020-12-30','пьяная встреча нового года',12,2,'2020-11-23 17:26:22',NULL,NULL,'19:00:00',NULL,14),(18,'',6,'2020-01-03','',24,39,'2020-12-18 19:00:47',NULL,16,'19:00:00',NULL,NULL),(20,'',11,'2020-01-03','',25,52,'2020-12-18 19:36:17',NULL,17,'19:00:00',NULL,NULL),(21,'',6,'2020-01-04','',26,53,'2020-12-18 19:38:21',NULL,16,'19:00:00',NULL,NULL),(22,'',11,'2020-01-04','',27,25,'2020-12-18 19:39:11',NULL,17,'19:00:00',NULL,NULL),(23,'',7,'2020-01-05','',27,25,'2020-12-18 19:41:12',NULL,18,'19:00:00',NULL,15),(24,'',8,'2020-01-05','',28,54,'2020-12-18 19:46:45',NULL,NULL,'19:00:00',NULL,NULL),(25,'',11,'2020-01-05','',29,55,'2020-12-18 19:49:12',NULL,17,'19:00:00',NULL,NULL),(26,'',6,'2020-01-06','',30,28,'2020-12-18 19:49:52',NULL,16,'19:00:00',NULL,5),(27,'',6,'2020-01-07','',31,56,'2020-12-18 19:53:26',NULL,16,'19:00:00',NULL,5),(28,'',6,'2020-01-08','',13,26,'2020-12-18 19:54:32',NULL,16,'19:00:00',NULL,5),(29,'',7,'2020-01-08','',30,28,'2020-12-18 19:55:53',NULL,18,'19:00:00',NULL,15),(30,'',6,'2020-01-17','',13,27,'2020-12-21 21:16:16',NULL,NULL,'19:00:00',1,5),(31,'',1,'2020-01-19','',13,57,'2020-12-21 21:17:33',NULL,NULL,'19:00:00',2,15),(32,'',8,'2020-01-20','',24,39,'2020-12-21 21:18:28',NULL,NULL,'19:00:00',1,14),(33,'',6,'2020-01-23','',29,55,'2020-12-21 21:19:10',NULL,NULL,'19:00:00',1,5),(35,'',33,'2020-01-26','',13,26,'2020-12-21 21:20:21',NULL,NULL,'19:00:00',1,5),(36,'',1,'2020-01-29','',28,54,'2020-12-21 21:20:53',NULL,NULL,'19:00:00',1,15),(37,'',6,'2020-02-01','',33,29,'2020-12-21 21:21:43',NULL,NULL,'19:00:00',1,5),(38,'',6,'2020-02-03','',34,30,'2020-12-21 21:22:37',NULL,NULL,'19:00:00',1,5),(39,'',6,'2020-02-05','',35,31,'2020-12-21 21:23:12',NULL,NULL,'19:00:00',1,5),(40,'',6,'2020-02-07','',36,32,'2020-12-21 21:27:13',NULL,NULL,'19:00:00',1,5),(41,'',1,'2020-02-07','',13,33,'2020-12-21 21:27:48',NULL,NULL,'21:00:00',2,15);
/*!40000 ALTER TABLE `event` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `imgarena`
--

DROP TABLE IF EXISTS `imgarena`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `imgarena` (
  `id` int NOT NULL AUTO_INCREMENT,
  `url` varchar(255) NOT NULL,
  `arena_id` int DEFAULT NULL,
  `created_imgarena` datetime DEFAULT NULL,
  `edit_imgarena` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `arena_id` (`arena_id`),
  CONSTRAINT `imgarena_ibfk_1` FOREIGN KEY (`arena_id`) REFERENCES `arena` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `imgarena`
--

LOCK TABLES `imgarena` WRITE;
/*!40000 ALTER TABLE `imgarena` DISABLE KEYS */;
INSERT INTO `imgarena` VALUES (5,'1355832_66716607.png',14,'2020-11-15 08:30:28','2020-11-15 08:31:02'),(6,'70fb5bd5a12daac4f282fd919e5f723f.jpg',5,'2020-11-15 08:53:53','2020-11-15 08:54:11'),(7,'Voronezhsky_dramatichesky_teatr_2008.jpg',2,'2020-11-15 19:09:42','2020-11-15 19:09:53'),(8,'3b0d99fd-889a-445e-9163-f2a605cffdd6.jpeg',1,'2020-11-16 19:43:55','2020-11-16 19:44:04'),(9,'unnamed.jpg',NULL,'2020-11-16 20:11:01',NULL),(10,'img/arena/unnamed.jpg',NULL,'2020-11-16 20:11:57',NULL),(11,'img/arena/Voronezhsky_dramatichesky_teatr_2008.jpg',NULL,'2020-11-16 20:12:32',NULL);
/*!40000 ALTER TABLE `imgarena` ENABLE KEYS */;
UNLOCK TABLES;




--
-- Table structure for table `tour`
--

DROP TABLE IF EXISTS `tour`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tour` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `created_tour` datetime DEFAULT NULL,
  `edit_tour` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tour`
--

LOCK TABLES `tour` WRITE;
/*!40000 ALTER TABLE `tour` DISABLE KEYS */;
INSERT INTO `tour` VALUES (1,'Ноябрский тур',NULL,NULL),(2,'Королев',NULL,NULL),(3,'Сумишевский',NULL,NULL),(14,'qeqweqeqw',NULL,NULL),(15,'123214',NULL,NULL),(16,'Ярослав сумишевский','2020-12-18 22:57:33',NULL),(17,'Январский тур Белорусских','2020-12-18 22:57:33',NULL),(18,'Январский тур Королев','2020-12-18 22:57:33',NULL);
/*!40000 ALTER TABLE `tour` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `typeevent`
--

DROP TABLE IF EXISTS `typeevent`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `typeevent` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `description` varchar(500) DEFAULT NULL,
  `edit_typeevent` datetime DEFAULT NULL,
  `created_edit_typeevent` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `typeevent`
--

LOCK TABLES `typeevent` WRITE;
/*!40000 ALTER TABLE `typeevent` DISABLE KEYS */;
INSERT INTO `typeevent` VALUES (1,'Концерт',NULL,NULL,'2020-12-18 10:37:08'),(2,'Корпаратив',NULL,NULL,'2020-12-18 10:37:18');
/*!40000 ALTER TABLE `typeevent` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `typehall`
--

DROP TABLE IF EXISTS `typehall`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `typehall` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `description` varchar(500) DEFAULT NULL,
  `create_time` datetime DEFAULT NULL,
  `edit_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `typehall`
--

LOCK TABLES `typehall` WRITE;
/*!40000 ALTER TABLE `typehall` DISABLE KEYS */;
INSERT INTO `typehall` VALUES (1,'Клубы',NULL,NULL,NULL),(2,'Дом культуры',NULL,NULL,NULL),(3,'уличные площадки',NULL,NULL,NULL),(4,'Цирк',NULL,NULL,NULL),(5,'Филармония',NULL,NULL,NULL),(6,'Театр',NULL,NULL,NULL),(7,'Концертный зал',NULL,NULL,NULL),(8,'Ресторан',NULL,NULL,NULL),(9,'Спортивная арена',NULL,NULL,NULL);
/*!40000 ALTER TABLE `typehall` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--


/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-12-22 21:16:15
