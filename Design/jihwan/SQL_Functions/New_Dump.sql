-- MySQL dump 10.13  Distrib 8.0.18, for Win64 (x86_64)
--
-- Host: localhost    Database: tripdb_01
-- ------------------------------------------------------
-- Server version	8.0.18

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Dumping data for table `facebook_user_tb`
--

LOCK TABLES `facebook_user_tb` WRITE;
/*!40000 ALTER TABLE `facebook_user_tb` DISABLE KEYS */;
INSERT INTO `facebook_user_tb` VALUES ('20','가','여자',25,'http://','가','베를린','2019-11-13','2019-11-14','#테스트, #테스트2','state?','기존',1,NULL),('21','나','여자',26,'http://','나','베를린','2019-11-10','2019-11-12','#테스트, #테스트2','state?','기존',1,NULL),('22','다','남자',27,'http://','다','서울','2019-11-07','2019-11-12','#테스트, #테스트2','state?','기존',1,NULL),('23','라','여자',28,'http://','라','서울','2019-11-14','2019-11-15','#테스트, #테스트2','state?','기존',1,NULL),('24','마','남자',29,'http://','마','파리','2019-11-17','2019-11-19','#테스트, #테스트2','state?','기존',1,NULL);
/*!40000 ALTER TABLE `facebook_user_tb` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `kakaotalk_user_tb`
--

LOCK TABLES `kakaotalk_user_tb` WRITE;
/*!40000 ALTER TABLE `kakaotalk_user_tb` DISABLE KEYS */;
INSERT INTO `kakaotalk_user_tb` VALUES ('10','D','남자',20,'http://','KD','베를린','2019-11-10','2019-11-12','#테스트, #테스트2','state?','기존',1,NULL),('11','E','남자',25,'http://','KE','서울','2019-11-09','2019-11-15','#테스트, #테스트2','state?','기존',1,NULL),('12','F','여자',30,'http://','KF','파리','2019-11-16','2019-11-17','#테스트, #테스트2','state?','기존',1,NULL),('13','G','남자',32,'http://','KG','베를린','2019-11-16','2019-11-18','#테스트, #테스트2','state?','기존',1,NULL),('14','H','남자',23,'http://','KH','파리','2019-11-05','2019-11-12','#테스트, #테스트2','state?','기존',1,NULL),('24','J','남자',23,'http://','KH','파리','2019-11-07','2019-11-10','#테스트, #테스트2','state?','기존',1,NULL),('25','Y','남자',23,'http://','KH','파리','2019-11-18','2019-11-20','#테스트, #테스트2','state?','기존',1,NULL);
/*!40000 ALTER TABLE `kakaotalk_user_tb` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `telegram_user_tb`
--

LOCK TABLES `telegram_user_tb` WRITE;
/*!40000 ALTER TABLE `telegram_user_tb` DISABLE KEYS */;
INSERT INTO `telegram_user_tb` VALUES ('1','hwanlee','남',23,'http://','leejh','파리','2019-11-11','2019-11-17','#술한잔, #체력왕','state?','기존',1,NULL),('2','lee',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'new_member',0,NULL),('3','A','남자',20,'http://','KA','파리','2019-11-13','2019-11-17','#지금은4시, #졸립다','state?','기존',2,NULL),('4','B','여자',22,'http://','KB','파리','2019-11-15','2019-11-18','#테스트, #테스트2','state?','기존',1,NULL),('5','C','여자',21,'http://','KC','베를린','2019-11-12','2019-11-15','#테스트, #테스트2','state?','기존',1,NULL);
/*!40000 ALTER TABLE `telegram_user_tb` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-11-18  4:02:29
