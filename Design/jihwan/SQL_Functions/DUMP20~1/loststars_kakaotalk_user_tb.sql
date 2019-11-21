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
-- Table structure for table `kakaotalk_user_tb`
--

DROP TABLE IF EXISTS `kakaotalk_user_tb`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `kakaotalk_user_tb` (
  `id` varchar(45) NOT NULL,
  `user_id` varchar(45) DEFAULT NULL,
  `sex` varchar(45) DEFAULT NULL,
  `age` varchar(45) DEFAULT NULL,
  `profile_image` varchar(400) DEFAULT NULL,
  `kakao_id` varchar(45) DEFAULT NULL,
  `city` varchar(45) DEFAULT NULL,
  `start_date` varchar(45) DEFAULT NULL,
  `end_date` varchar(45) DEFAULT NULL,
  `appeal_tag` varchar(45) DEFAULT NULL,
  `dialog_state` varchar(45) DEFAULT NULL,
  `user_state` varchar(45) DEFAULT NULL,
  `open_cnt` int(8) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `kakaotalk_user_tb`
--

LOCK TABLES `kakaotalk_user_tb` WRITE;
/*!40000 ALTER TABLE `kakaotalk_user_tb` DISABLE KEYS */;
INSERT INTO `kakaotalk_user_tb` VALUES ('10a','사나','여자','20','http://img.hani.co.kr/imgdb/resize/2019/0502/00503582_20190502.JPG','cw0516','베를린','2019-11-10','2019-11-12','#어필태그','state?','기존',1),('11b','아이린','여자','25','http://www.gangel.kr/files/attach/images/287/119/339/001/f5238e8b402a63e0ad2c9f1c742706ae.jpg','cw0516','서울','2019-11-09','2019-11-15','#어필태그','state?','기존',1),('12c','제니','여자','30','http://sccdn.chosun.com/news/html/2019/04/21/2019042201001668800114261.jpg','cw0516','파리','2019-11-16','2019-11-17','#어필태그','state?','기존',1),('13d','아이유','여자','32','https://dimg.donga.com/wps/NEWS/IMAGE/2019/10/21/97986591.2.jpg','cw0516','베를린','2019-11-16','2019-11-18','#어필태그','state?','기존',1),('14e','슬기','여자','23','http://www.breaknews.com/imgdata/breaknews_com/201709/2017092149551948.jpg','cw0516','파리','2019-11-05','2019-11-12','#어필태그','state?','기존',1),('25f','아이린','여자','23','https://img.sbs.co.kr/newsnet/etv/upload/2019/05/17/30000628031_700.jpg','cw0516','파리','2019-11-18','2019-11-20','#어필태그','state?','기존',1);
/*!40000 ALTER TABLE `kakaotalk_user_tb` ENABLE KEYS */;
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
