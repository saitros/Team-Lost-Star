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
-- Table structure for table `telegram_user_tb`
--

DROP TABLE IF EXISTS `telegram_user_tb`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `telegram_user_tb` (
  `id` varchar(45) NOT NULL,
  `user_id` varchar(45) DEFAULT NULL,
  `sex` varchar(10) DEFAULT NULL,
  `age` varchar(10) DEFAULT NULL,
  `city` varchar(45) DEFAULT NULL,
  `start_date` varchar(45) DEFAULT '여행 시작일',
  `end_date` varchar(45) DEFAULT '여행 종료일',
  `appeal_tag` varchar(100) DEFAULT NULL,
  `dialog_state` varchar(45) DEFAULT NULL,
  `is_end` int(1) DEFAULT NULL,
  `user_state` int(1) DEFAULT NULL,
  `profile_image` varchar(400) DEFAULT NULL,
  `open_cnt` int(8) DEFAULT '1',
  `match_idx` int(8) DEFAULT NULL,
  `match_photo_id` varchar(45) DEFAULT NULL,
  `match_info_id` varchar(45) DEFAULT NULL,
  `matched_list` varchar(100) DEFAULT NULL,
  `kakao_id` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='	';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `telegram_user_tb`
--

LOCK TABLES `telegram_user_tb` WRITE;
/*!40000 ALTER TABLE `telegram_user_tb` DISABLE KEYS */;
INSERT INTO `telegram_user_tb` VALUES ('740140183','정훈이','남자','532','서울','2019-11-01','2019-11-30','피앙새구합니다 그녀의맘속으로 동행... 아니 왕복은 없습니다 편도항공권뿐만 존재합니다....:)','match',0,1,'https://i.imgur.com/QZRKAF8.jpg',1,1,'2241',NULL,'f23,k11,f22','hun'),('964322422','chanwookim','남자','25','파리','2019-11-01','2019-11-30','#여행마스터','start',0,1,'https://i.imgur.com/SQWgaWo.jpg',2,1,'3775',NULL,'k25f,k14e,f24e,k12c','cw0516');
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

-- Dump completed on 2019-11-22  4:19:28
