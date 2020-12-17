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

DROP TABLE IF EXISTS `alembic_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alembic_version`
--

LOCK TABLES `alembic_version` WRITE;
/*!40000 ALTER TABLE `alembic_version` DISABLE KEYS */;
INSERT INTO `alembic_version` VALUES ('74c653238174');
/*!40000 ALTER TABLE `alembic_version` ENABLE KEYS */;
UNLOCK TABLES;

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
  `number_of_seats` int DEFAULT NULL,
  `sound` varchar(255) DEFAULT NULL,
  `phone_admin` varchar(255) DEFAULT NULL,
  `phone_light` varchar(255) DEFAULT NULL,
  `phone_sound` varchar(255) DEFAULT NULL,
  `razgruzka` varchar(255) DEFAULT NULL,
  `typehall_id` int DEFAULT NULL,
  `address` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `city_id` (`city_id`),
  KEY `typehall_id` (`typehall_id`),
  CONSTRAINT `arena_ibfk_1` FOREIGN KEY (`city_id`) REFERENCES `city` (`id`),
  CONSTRAINT `arena_ibfk_2` FOREIGN KEY (`typehall_id`) REFERENCES `typehall` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=52 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `arena`
--

LOCK TABLES `arena` WRITE;
/*!40000 ALTER TABLE `arena` DISABLE KEYS */;
INSERT INTO `arena` VALUES (1,'БКЗ. Большой Концертынй Зал',NULL,'2020-12-17 17:00:23',NULL,14,NULL,NULL,3727,'Meyer Sound Milo',' 8 (812) 275-13-00',NULL,NULL,NULL,7,NULL),(2,'ВКЗ. Воронежский концертный зал',NULL,'2020-12-17 17:00:30',NULL,12,NULL,NULL,782,NULL,'+7 (473) 254-56-66',NULL,NULL,NULL,7,NULL),(3,'Крокус',NULL,'2020-11-13 23:57:11',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(4,'Театр золотое кольцо',NULL,'2020-12-17 17:00:48',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,6,NULL),(5,'EventHall','Площадка в торговом центре','2020-12-17 17:00:57',NULL,12,NULL,'ClayPaky',5000,'Meyer Sound Mica','8 (473) 228-02-01',NULL,NULL,NULL,7,NULL),(6,'Тинькофф Арена',NULL,'2020-11-13 23:57:48',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(8,'Барвиха','В барвихенском dрайоне','2020-12-17 17:01:12',NULL,13,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,1,NULL),(14,'КЗ Губернский','','2020-11-14 20:24:29','2020-11-14 20:24:29',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(25,'ДК Яуза',NULL,NULL,'2020-11-20 19:57:37',27,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(26,'ДК Салют',NULL,NULL,'2020-11-20 20:06:20',13,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(27,'АЗЛК',NULL,NULL,'2020-11-20 20:07:44',13,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(28,'КДЦ Сатурн',NULL,NULL,'2020-11-20 20:07:58',30,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(29,'ДК Металлист',NULL,NULL,'2020-11-20 20:32:57',33,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(30,'КДЦ Губернский',NULL,NULL,'2020-11-20 20:33:19',34,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(31,'Театр Оперы и Балета РК',NULL,NULL,'2020-11-20 20:33:54',35,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(32,'Вятская Филармония',NULL,NULL,'2020-11-20 20:34:16',36,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(33,'Бекстейдж','','2020-12-17 19:23:48','2020-11-20 20:34:38',13,'','',NULL,'','','','','',8,''),(34,'ДК Якова Ухсая',NULL,NULL,'2020-11-20 20:35:06',38,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(35,'ДК ХХХ-летия Победы',NULL,NULL,'2020-11-20 20:35:33',39,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(36,'КЗ Сары Садыковой',NULL,NULL,'2020-11-20 20:35:50',40,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(37,'ОДК Пролетарка',NULL,NULL,'2020-11-20 20:36:18',33,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(38,'ДК Гагарина',NULL,NULL,'2020-11-20 20:36:38',42,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(39,'КЦ Зеленоград',NULL,NULL,'2020-11-20 20:36:59',24,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(40,'ДК Мир',NULL,NULL,'2020-11-20 20:37:17',43,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(41,'ДК Калинина','','2020-12-17 19:11:30','2020-11-20 20:37:35',44,'','',NULL,'','','','','',2,''),(42,'ДС Звездный',NULL,NULL,'2020-11-20 20:38:17',46,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(43,'ДИ Нефтяник','','2020-12-17 19:11:19','2020-11-20 20:38:38',48,'','',NULL,'','','','','',2,''),(44,'Дворец Искуств',NULL,NULL,'2020-11-20 20:38:56',49,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL);
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
-- Dumping data for table `arena_city`
--

LOCK TABLES `arena_city` WRITE;
/*!40000 ALTER TABLE `arena_city` DISABLE KEYS */;
/*!40000 ALTER TABLE `arena_city` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `artist`
--

DROP TABLE IF EXISTS `artist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `artist` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `sound_engineer` varchar(255) DEFAULT NULL,
  `administrator` varchar(255) DEFAULT NULL,
  `edit_artist` datetime DEFAULT NULL,
  `created_artist` datetime DEFAULT NULL,
  `light` varchar(255) DEFAULT NULL,
  `phone_light` varchar(255) DEFAULT NULL,
  `phone_sound` varchar(255) DEFAULT NULL,
  `phone_administrator` varchar(255) DEFAULT NULL,
  `monitor_engineer` varchar(255) DEFAULT NULL,
  `phone_monitor` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `artist`
--

LOCK TABLES `artist` WRITE;
/*!40000 ALTER TABLE `artist` DISABLE KEYS */;
INSERT INTO `artist` VALUES (1,'Валерий Меладзе','Дмитрий Голякин','Георгий Симонян','2020-11-23 19:40:08',NULL,'Вальковец Михаил',NULL,'89037450820','','',''),(6,'Сумишевский','Алексей','Какой то Андрей','2020-11-23 15:40:33','2020-11-20 19:55:38','Игоряныч',NULL,'','','',''),(7,'Королев','Сыряный Артём','Сыряный Артём','2020-11-23 15:40:11','2020-11-20 19:56:02','Какой то Алексей',NULL,'','','',''),(8,'Трофим','Юрий Андропов','Анна Андрон','2020-11-29 22:49:00','2020-11-20 19:56:15','НЕТ',NULL,'','','','');
/*!40000 ALTER TABLE `artist` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `association`
--

DROP TABLE IF EXISTS `association`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `association` (
  `users_id` int DEFAULT NULL,
  `roles_id` int DEFAULT NULL,
  KEY `users_id` (`users_id`),
  KEY `roles_id` (`roles_id`),
  CONSTRAINT `association_ibfk_1` FOREIGN KEY (`users_id`) REFERENCES `users` (`id`),
  CONSTRAINT `association_ibfk_2` FOREIGN KEY (`roles_id`) REFERENCES `roles` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `association`
--

LOCK TABLES `association` WRITE;
/*!40000 ALTER TABLE `association` DISABLE KEYS */;
INSERT INTO `association` VALUES (3,1),(5,1),(9,1),(10,1);
/*!40000 ALTER TABLE `association` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `city`
--

DROP TABLE IF EXISTS `city`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `city` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `edit_city` datetime DEFAULT NULL,
  `created_city` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=50 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `city`
--

LOCK TABLES `city` WRITE;
/*!40000 ALTER TABLE `city` DISABLE KEYS */;
INSERT INTO `city` VALUES (12,'Воронеж','2020-11-14 16:38:36','2020-11-14 10:57:09'),(13,'Москва','2020-11-14 17:24:15','2020-11-14 10:57:12'),(14,'Санкт-Петербург','2020-11-14 10:57:22','2020-11-14 10:57:22'),(19,'Иваново','2020-11-14 20:23:21','2020-11-14 20:23:21'),(24,'Зеленоград',NULL,NULL),(25,'Люберцы',NULL,NULL),(26,'Электросталь',NULL,NULL),(27,'Мытищи',NULL,NULL),(28,'Тула',NULL,NULL),(29,'Коломна',NULL,NULL),(30,'Раменское',NULL,NULL),(31,'Красногорск',NULL,NULL),(32,'Химки',NULL,NULL),(33,'Тверь',NULL,NULL),(34,'Смоленск',NULL,NULL),(35,'Сыктывкар',NULL,NULL),(36,'Киров',NULL,NULL),(37,'Белгород',NULL,NULL),(38,'Чебоксары',NULL,NULL),(39,'Йошкар-Ола',NULL,NULL),(40,'Набережые Челны','2020-11-20 20:29:52',NULL),(41,'Саратов',NULL,NULL),(42,'Сергиев Посад',NULL,NULL),(43,'Реутов',NULL,NULL),(44,'Королев',NULL,NULL),(45,'Псков',NULL,NULL),(46,'Новый Уренгой',NULL,NULL),(47,'Великие Луки',NULL,NULL),(48,'Сургут',NULL,NULL),(49,'Нижневартовск',NULL,NULL);
/*!40000 ALTER TABLE `city` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `equipment`
--

DROP TABLE IF EXISTS `equipment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `equipment` (
  `id` int NOT NULL AUTO_INCREMENT,
  `edit_equipment` datetime DEFAULT NULL,
  `created_equipment` datetime DEFAULT NULL,
  `category_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `category_id` (`category_id`),
  CONSTRAINT `equipment_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES `equipmentcategory` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `equipment`
--

LOCK TABLES `equipment` WRITE;
/*!40000 ALTER TABLE `equipment` DISABLE KEYS */;
/*!40000 ALTER TABLE `equipment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `equipmentcategory`
--

DROP TABLE IF EXISTS `equipmentcategory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `equipmentcategory` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `edit_equipmentcategory` datetime DEFAULT NULL,
  `created_equipmentcategory` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `equipmentcategory`
--

LOCK TABLES `equipmentcategory` WRITE;
/*!40000 ALTER TABLE `equipmentcategory` DISABLE KEYS */;
INSERT INTO `equipmentcategory` VALUES (1,'Звуковое оборудование','2020-12-08 22:14:00','2020-12-08 21:55:46'),(2,'Световое ооборудование',NULL,'2020-12-08 21:55:46'),(3,'Экранное оборудование',NULL,'2020-12-08 21:55:46');
/*!40000 ALTER TABLE `equipmentcategory` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `event`
--

DROP TABLE IF EXISTS `event`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `event` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `artist_id` int DEFAULT NULL,
  `date_event` date DEFAULT NULL,
  `description` varchar(500) DEFAULT NULL,
  `city_id` int DEFAULT NULL,
  `arena_id` int DEFAULT NULL,
  `manager_id` int DEFAULT NULL,
  `edit_event` datetime DEFAULT NULL,
  `created_event` datetime DEFAULT NULL,
  `tour_id` int DEFAULT NULL,
  `time_event` time DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `artist_id` (`artist_id`),
  KEY `city_id` (`city_id`),
  KEY `arena_id` (`arena_id`),
  KEY `manager_id` (`manager_id`),
  KEY `tour_id` (`tour_id`),
  CONSTRAINT `event_ibfk_1` FOREIGN KEY (`artist_id`) REFERENCES `artist` (`id`),
  CONSTRAINT `event_ibfk_2` FOREIGN KEY (`city_id`) REFERENCES `city` (`id`),
  CONSTRAINT `event_ibfk_3` FOREIGN KEY (`arena_id`) REFERENCES `arena` (`id`),
  CONSTRAINT `event_ibfk_4` FOREIGN KEY (`manager_id`) REFERENCES `manager` (`id`),
  CONSTRAINT `event_ibfk_5` FOREIGN KEY (`tour_id`) REFERENCES `tour` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `event`
--

LOCK TABLES `event` WRITE;
/*!40000 ALTER TABLE `event` DISABLE KEYS */;
INSERT INTO `event` VALUES (1,'Ноябрский Тур',1,'2020-11-15','Добавить описание для!',14,1,3,'2020-11-16 19:25:37',NULL,15,'19:00:00'),(5,'Королев',7,'2020-11-22',NULL,27,25,1,'2020-11-20 20:11:06',NULL,2,'19:00:00'),(6,'Королев',7,'2020-11-12',NULL,30,28,2,'2020-11-20 20:17:01',NULL,14,'19:00:00'),(7,'Сум',6,'2020-12-28','',33,29,3,'2020-11-20 20:39:28',NULL,NULL,'19:00:00'),(8,'',6,'2020-12-26','',34,30,3,'2020-11-20 21:06:05',NULL,3,'19:00:00'),(9,'',6,'2020-12-25','',35,31,3,'2020-11-20 21:07:55',NULL,3,'19:00:00'),(15,'wefwfew',1,'2020-11-11','wfew',37,1,1,'2020-11-23 16:03:28',NULL,14,'19:00:00'),(17,'сольник',8,'2020-12-30','пьяная встреча нового года',12,2,1,'2020-11-23 17:26:22',NULL,NULL,'22:30:00');
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
-- Table structure for table `manager`
--

DROP TABLE IF EXISTS `manager`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `manager` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `edit_manager` datetime DEFAULT NULL,
  `created_manager` datetime DEFAULT NULL,
  `phone` varchar(255) DEFAULT NULL,
  `address` varchar(255) DEFAULT NULL,
  `birthday` date DEFAULT NULL,
  `photo` varchar(255) DEFAULT NULL,
  `facebook` varchar(255) DEFAULT NULL,
  `instagram` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `manager`
--

LOCK TABLES `manager` WRITE;
/*!40000 ALTER TABLE `manager` DISABLE KEYS */;
INSERT INTO `manager` VALUES (1,'Вестимый Андрей Петрович','2020-12-16 23:24:26','2020-11-16 17:58:28','+79192320772','Воронежская область, Новоусманский район, с. Новая Усмань д.1, кв. 1.','1992-02-18','managers/vesti_1.jpg','https://ru-ru.facebook.com/vestimyandrey','https://www.instagram.com/vestimyandrey'),(2,'Двухголовый Николай Николаевич','2020-12-16 01:18:21','2020-11-16 17:59:06','+7-910-245-38-65','мкр. Подклетное','1979-12-11',NULL,'',''),(3,'Медведев Роман Владимрович','2020-12-16 23:36:28','2020-11-16 20:59:38','+7-905-650-06-09',NULL,'1977-09-10','managers/medvedev.jpg',NULL,NULL),(4,'Домников Сергей Михайлович','2020-12-16 23:37:23','2020-11-23 20:22:04','89050636477','','1977-01-07',NULL,'https://www.facebook.com/profile.php?id=100003423698675',''),(5,'Бахметов Андрей Александрович','2020-12-16 23:35:55','2020-12-08 21:33:45','+7-962-968-41-09','','1977-09-08','managers/bahmetov.jpg','',''),(6,'Вальковец Михаил Петрович','2020-12-16 23:36:07','2020-12-16 01:05:08','+7-930-404-99-88',NULL,'1977-08-18','managers/vetz.jpg',NULL,NULL);
/*!40000 ALTER TABLE `manager` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `managerphoto`
--

DROP TABLE IF EXISTS `managerphoto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `managerphoto` (
  `id` int NOT NULL AUTO_INCREMENT,
  `url` varchar(255) NOT NULL,
  `created_managerphoto` datetime DEFAULT NULL,
  `edit_managerphoto` datetime DEFAULT NULL,
  `manager_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `manager_id` (`manager_id`),
  CONSTRAINT `managerphoto_ibfk_1` FOREIGN KEY (`manager_id`) REFERENCES `manager` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `managerphoto`
--

LOCK TABLES `managerphoto` WRITE;
/*!40000 ALTER TABLE `managerphoto` DISABLE KEYS */;
INSERT INTO `managerphoto` VALUES (7,'managers/vesti_1.jpg','2020-12-15 21:54:13','2020-12-15 21:54:24',1),(8,'managers/domi.jpg','2020-12-15 21:56:21','2020-12-15 21:56:33',4),(9,'managers/medvedev.jpg','2020-12-15 21:58:48','2020-12-15 21:58:58',3),(10,'managers/bahmetov.jpg','2020-12-15 22:00:24','2020-12-15 22:00:36',5),(12,'managers/dvuhg.jpg','2020-12-15 22:04:42','2020-12-15 22:05:21',2),(13,'managers/vetz.jpg','2020-12-15 22:12:00','2020-12-15 22:12:09',6),(14,'managers/bahmeto.jpg','2020-12-16 20:15:22',NULL,NULL),(15,'managers/domi.jpg','2020-12-16 20:16:09',NULL,NULL),(16,'managers/domin.jpg','2020-12-16 20:17:49',NULL,NULL),(17,'managers/vesti_1.jpg','2020-12-16 20:22:42',NULL,NULL);
/*!40000 ALTER TABLE `managerphoto` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `photoartist`
--

DROP TABLE IF EXISTS `photoartist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `photoartist` (
  `id` int NOT NULL AUTO_INCREMENT,
  `url` varchar(255) NOT NULL,
  `artist_id` int DEFAULT NULL,
  `edit_imgarena` datetime DEFAULT NULL,
  `created_imgarena` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `artist_id` (`artist_id`),
  CONSTRAINT `photoartist_ibfk_1` FOREIGN KEY (`artist_id`) REFERENCES `artist` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `photoartist`
--

LOCK TABLES `photoartist` WRITE;
/*!40000 ALTER TABLE `photoartist` DISABLE KEYS */;
INSERT INTO `photoartist` VALUES (1,'img/artist/meladze.jpeg',NULL,'2020-11-16 20:25:15','2020-11-16 20:23:16'),(2,'img/artist/meladze.jpg',1,'2020-11-16 20:25:08','2020-11-16 20:24:55'),(3,'img/artist/viktor-korolev-zhena-i-deti-lichnaia-zhizn-780.jpg',7,'2020-11-20 20:13:52','2020-11-20 20:13:06'),(4,'img/artist/yaroslav-sumishevskii.jpg',6,'2020-11-20 20:15:08','2020-11-20 20:14:54'),(5,'img/artist/uzn_16012810065.jpg',8,'2020-11-20 20:16:00','2020-11-20 20:15:49');
/*!40000 ALTER TABLE `photoartist` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `roles`
--

DROP TABLE IF EXISTS `roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `roles` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(250) NOT NULL,
  `description` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `roles`
--

LOCK TABLES `roles` WRITE;
/*!40000 ALTER TABLE `roles` DISABLE KEYS */;
INSERT INTO `roles` VALUES (1,'admin','Администратор'),(2,'users','users'),(3,'edit','Edit');
/*!40000 ALTER TABLE `roles` ENABLE KEYS */;
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
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tour`
--

LOCK TABLES `tour` WRITE;
/*!40000 ALTER TABLE `tour` DISABLE KEYS */;
INSERT INTO `tour` VALUES (1,'Ноябрский тур',NULL,NULL),(2,'Королев',NULL,NULL),(3,'Сумишевский',NULL,NULL),(14,'qeqweqeqw',NULL,NULL),(15,'123214',NULL,NULL);
/*!40000 ALTER TABLE `tour` ENABLE KEYS */;
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
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `typehall`
--

LOCK TABLES `typehall` WRITE;
/*!40000 ALTER TABLE `typehall` DISABLE KEYS */;
INSERT INTO `typehall` VALUES (1,'Клубы',NULL),(2,'Дом культуры',NULL),(3,'уличные площадки',NULL),(4,'Цирк',NULL),(5,'Филармония',NULL),(6,'Театр',NULL),(7,'Концертный зал',NULL),(8,'Ресторан',NULL);
/*!40000 ALTER TABLE `typehall` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(250) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `active` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  CONSTRAINT `users_chk_1` CHECK ((`active` in (0,1)))
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (3,'admin','admin@admin.ru','$2b$12$NM5gLgPCvn650S5f1LRToO7Zvrlk.pfzzVIUxKcbX3fjCsisDimhC',1),(5,'Vestimy','vestimyandrey@gmail.com','$2b$12$SV3G.U1zGVXZswyui9CnQuyFBK4jsS9hV.mO46k.gIfz82cCLpFbO',1),(9,'test','test@test.ru','$2b$12$5rGdZYJCo2.ITqX/V31HROE6cryyDWim2cguiV2PuWUiABvObWyaa',1),(10,'test2','test2@test2.ru','$2b$12$eREj3whjdVZaFaW0Zdm0weZT5NkxfrHAGKuY3o5N3uMkhLh.qK8PS',1),(11,'test3','test3@test3.ru','test3',NULL),(12,'test4','test4@test4.ru','test4',NULL),(13,'test5','test5@test5.ru','$2b$12$1BL2L538Z6gKXvSVlhoTgOfXUwjR5qQrJ9iP.OVfufjGubFwoYSjC',1);
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

-- Dump completed on 2020-12-17 22:45:48
