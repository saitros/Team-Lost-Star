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
-- Table structure for table `facebook_user_tb`
--

DROP TABLE IF EXISTS `facebook_user_tb`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `facebook_user_tb` (
  `id` varchar(255) NOT NULL,
  `user_id` varchar(32) COLLATE utf8_bin DEFAULT NULL,
  `sex` varchar(4) COLLATE utf8_bin DEFAULT NULL,
  `age` int(4) unsigned DEFAULT NULL,
  `profile_image` varchar(255) COLLATE utf8_bin DEFAULT NULL,
  `kakao_id` varchar(64) COLLATE utf8_bin DEFAULT NULL,
  `country` varchar(32) COLLATE utf8_bin DEFAULT NULL,
  `city` varchar(32) COLLATE utf8_bin DEFAULT NULL,
  `start_date` varchar(10) COLLATE utf8_bin DEFAULT NULL,
  `end_date` varchar(10) COLLATE utf8_bin DEFAULT NULL,
  `appeal_tag` varchar(255) COLLATE utf8_bin DEFAULT NULL,
  `dialog_state` varchar(32) COLLATE utf8_bin DEFAULT NULL,
  `user_state` varchar(32) COLLATE utf8_bin DEFAULT NULL,
  `open_cnt` int(8) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `kakaotalk_user_tb`
--

DROP TABLE IF EXISTS `kakaotalk_user_tb`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `kakaotalk_user_tb` (
  `id` varchar(255) NOT NULL,
  `user_id` varchar(32) COLLATE utf8_bin DEFAULT NULL,
  `sex` varchar(4) COLLATE utf8_bin DEFAULT NULL,
  `age` int(4) unsigned DEFAULT NULL,
  `profile_image` varchar(255) COLLATE utf8_bin DEFAULT NULL,
  `kakao_id` varchar(64) COLLATE utf8_bin DEFAULT NULL,
  `country` varchar(10) COLLATE utf8_bin DEFAULT NULL,
  `city` varchar(10) COLLATE utf8_bin DEFAULT NULL,
  `start_date` varchar(10) COLLATE utf8_bin DEFAULT NULL,
  `end_date` varchar(10) COLLATE utf8_bin DEFAULT NULL,
  `appeal_tag` varchar(64) COLLATE utf8_bin DEFAULT NULL,
  `dialog_state` varchar(32) COLLATE utf8_bin DEFAULT NULL,
  `user_state` varchar(32) COLLATE utf8_bin DEFAULT NULL,
  `open_cnt` int(8) NOT NULL DEFAULT '0',
  `show_count` int(8) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `telegram_user_tb`
--

DROP TABLE IF EXISTS `telegram_user_tb`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `telegram_user_tb` (
  `id` varchar(255) NOT NULL,
  `user_id` varchar(32) COLLATE utf8_bin DEFAULT NULL,
  `sex` varchar(4) COLLATE utf8_bin DEFAULT NULL,
  `age` int(4) unsigned DEFAULT NULL,
  `profile_image` varchar(255) COLLATE utf8_bin DEFAULT NULL,
  `kakao_id` varchar(64) COLLATE utf8_bin DEFAULT NULL,
  `country` varchar(10) COLLATE utf8_bin DEFAULT ' ',
  `city` varchar(10) COLLATE utf8_bin DEFAULT NULL,
  `start_date` varchar(10) COLLATE utf8_bin DEFAULT NULL,
  `end_date` varchar(10) COLLATE utf8_bin DEFAULT NULL,
  `appeal_tag` varchar(64) COLLATE utf8_bin DEFAULT NULL,
  `dialog_state` varchar(32) COLLATE utf8_bin DEFAULT NULL,
  `user_state` varchar(32) COLLATE utf8_bin DEFAULT NULL,
  `is_end` int(1) DEFAULT NULL,
  `open_cnt` int(8) NOT NULL DEFAULT '1',
  `match_idx` int(8) DEFAULT NULL,
  `match_photo_id` varchar(45) DEFAULT NULL,
  `match_info_id` varchar(45) DEFAULT NULL,
  `matched_list` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-11-16  0:07:06
