-- MySQL dump 10.13  Distrib 8.0.17, for Win64 (x86_64)
--
-- Host: localhost    Database: loststars
-- ------------------------------------------------------
-- Server version	8.0.17

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
-- Table structure for table `facebook_user_tb`
--

DROP TABLE IF EXISTS `facebook_user_tb`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `facebook_user_tb` (
  `id` varchar(45) NOT NULL,
  `user_id` varchar(32) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `sex` varchar(4) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `age` int(4) unsigned DEFAULT NULL,
  `profile_image` varchar(400) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `kakao_id` varchar(64) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `city` varchar(10) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `start_date` varchar(10) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `end_date` varchar(10) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `appeal_tag` varchar(64) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `dialog_state` varchar(32) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `user_state` varchar(32) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `open_cnt` int(8) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `facebook_user_tb`
--

LOCK TABLES `facebook_user_tb` WRITE;
/*!40000 ALTER TABLE `facebook_user_tb` DISABLE KEYS */;
INSERT INTO `facebook_user_tb` VALUES ('20a','정연','여자',25,'https://img.theqoo.net/img/AUeTv.jpg','cw0516','베를린','2019-11-13','2019-11-14','#어필태그','state?','기존',1),('21b','나연','여자',26,'https://imgbntnews.hankyung.com/bntdata/images/photo/201904/4b90991e001492e32229c985ccb99fd4.jpg','cw0516','베를린','2019-11-10','2019-11-12','#어필태그','state?','기존',1),('22c','지효','여자',27,'http://www.kgirls.net/files/attach/images/214/852/056/0df68fd8ed6714fd23c893675c6ca48b.jpg','cw0516','서울','2019-11-07','2019-11-12','#어필태그','state?','기존',1),('23d','다현','여자',28,'https://img.hankyung.com/photo/201811/03.18321655.1.jpg','cw0516','서울','2019-11-14','2019-11-15','#어필태그','state?','기존',1),('24e','모모','여자',29,'https://upload.wikimedia.org/wikipedia/commons/thumb/0/0b/180717_%EC%97%B4%EB%A6%B0%EC%9D%8C%EC%95%85%ED%9A%8C_%ED%8A%B8%EC%99%80%EC%9D%B4%EC%8A%A4_%283%29_%28cropped%29.jpg/330px-180717_%EC%97%B4%EB%A6%B0%EC%9D%8C%EC%95%85%ED%9A%8C_%ED%8A%B8%EC%99%80%EC%9D%B4%EC%8A%A4_%283%29_%28cropped%29.jpg','cw0516','파리','2019-11-17','2019-11-19','#어필태그','state?','기존',1);
/*!40000 ALTER TABLE `facebook_user_tb` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-11-22  4:19:28
