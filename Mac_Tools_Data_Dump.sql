-- MySQL dump 10.13  Distrib 8.0.24, for Win64 (x86_64)
--
-- Host: localhost    Database: mac_tools
-- ------------------------------------------------------
-- Server version	8.0.24

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
-- Temporary view structure for view `allcustomerpayments`
--

DROP TABLE IF EXISTS `allcustomerpayments`;
/*!50001 DROP VIEW IF EXISTS `allcustomerpayments`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `allcustomerpayments` AS SELECT 
 1 AS `customerid`,
 1 AS `firstname`,
 1 AS `lastname`,
 1 AS `paymentid`,
 1 AS `amountowed`,
 1 AS `last_payed`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `customer`
--

DROP TABLE IF EXISTS `customer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `customer` (
  `customerid` varchar(4) NOT NULL,
  `firstname` varchar(25) NOT NULL,
  `lastname` varchar(25) NOT NULL,
  `company` varchar(25) NOT NULL,
  `address` varchar(32) NOT NULL,
  `city` varchar(32) NOT NULL,
  `state` char(2) NOT NULL,
  `postalcode` varchar(5) NOT NULL,
  `phone` char(10) NOT NULL,
  `fax` varchar(15) DEFAULT NULL,
  `email` varchar(32) DEFAULT NULL,
  PRIMARY KEY (`customerid`),
  KEY `idx_company` (`company`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customer`
--

LOCK TABLES `customer` WRITE;
/*!40000 ALTER TABLE `customer` DISABLE KEYS */;
INSERT INTO `customer` VALUES ('1','Tim','Robinson','\"Robinson Autobody Shop\"','\"123 that st\"','cuba','NY','12345','1234567890',NULL,NULL),('10','Austin','Parker','\"Cornings Customs\"','\"31 Parker St\"','Corning','Ny','23456','6077381567',NULL,NULL),('11','john','smith','\"Monroe Muffler\"','\"that street\"','houghton','Ny','12345','1231231234',NULL,NULL),('2','Dan','Robinson','\"Robinson Autobody Shop\"','\"123 this st\"','Cuba','NY','12345','6071234567',NULL,NULL),('3','Adam','McMillan','\"Robinson Autobody Shop\"','\"31 Leonard Ave\"','Houghton','NY','12345','6078278272',NULL,NULL),('4','William','Dibble','\"Monroe Muffler\"','\"124 East Church St\"','Troy','Pa','16947','6077381474',NULL,NULL),('5','Trevor','Mann','\"Cornings Customs\"','\"12 Center way St\"','Corning','Ny','23456','2341232543',NULL,NULL),('6','Justin','belmont','\"Monroe Muffler\"','\"31 Saunders Ln\"','Gillett','Pa','16925','6077422942',NULL,NULL),('7','Dave','Wess','\"Monroe Muffler\"','\"36 Locust Rd\"','Gillett','PA','16925','5705274942',NULL,NULL),('8','Dave','Stuart','\"Cornings Customs\"','\"11 Main Street\"','Corning','Ny','23456','6075851473',NULL,NULL),('9','Donald','Deagan','\"Cornings Customs\"','\"25 Parker St\"','Corning','Ny','23456','6075852169',NULL,NULL);
/*!40000 ALTER TABLE `customer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `invoice`
--

DROP TABLE IF EXISTS `invoice`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `invoice` (
  `invoiceid` int NOT NULL,
  `customerid` varchar(4) NOT NULL,
  `invoicedate` date NOT NULL,
  `billingaddress` varchar(32) DEFAULT NULL,
  `billingcity` varchar(32) DEFAULT NULL,
  `billingstate` char(2) DEFAULT NULL,
  `billingpostalcode` varchar(5) DEFAULT NULL,
  `total` decimal(6,2) NOT NULL,
  PRIMARY KEY (`invoiceid`),
  KEY `FK_customerids` (`customerid`),
  KEY `idx_invoice` (`invoiceid`),
  CONSTRAINT `FK_customerids` FOREIGN KEY (`customerid`) REFERENCES `customer` (`customerid`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `invoice`
--

LOCK TABLES `invoice` WRITE;
/*!40000 ALTER TABLE `invoice` DISABLE KEYS */;
INSERT INTO `invoice` VALUES (1,'1','2021-05-05','\"123 that st\"','cuba','NY','12345',49.99),(2,'5','2021-05-05','\"12 Center way St\"','Corning','Ny','23456',249.97),(3,'3','2021-05-05','\"31 Leonard Ave\"','Houghton','NY','12345',109.97),(4,'2','2021-05-05','\"123 this st\"','Cuba','NY','12345',99.98),(5,'2','2021-05-05','\"123 this st\"','Cuba','NY','12345',595.97),(6,'4','2021-05-05','\"124 East Church St\"','Troy','Pa','16947',325.98),(7,'6','2021-05-05','\"31 Saunders Ln\"','Gillett','Pa','16925',110.98),(8,'8','2021-05-05','\"11 Main Street\"','Corning','Ny','23456',125.98),(9,'7','2021-05-05','\"36 Locust Rd\"','Gillett','PA','16925',69.99),(10,'8','2021-05-05','\"11 Main Street\"','Corning','Ny','23456',499.99),(11,'9','2021-05-05','\"25 Parker St\"','Corning','Ny','23456',229.97),(12,'10','2021-05-05','\"31 Parker St\"','Corning','Ny','23456',99.99),(13,'11','2021-05-05','\"that street\"','houghton','Ny','12345',89.99);
/*!40000 ALTER TABLE `invoice` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `invoiceline`
--

DROP TABLE IF EXISTS `invoiceline`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `invoiceline` (
  `invoicelineid` int NOT NULL AUTO_INCREMENT,
  `invoiceid` int NOT NULL,
  `toolnumber` varchar(15) NOT NULL,
  `quantity` int NOT NULL,
  `unitprice` decimal(6,2) NOT NULL,
  PRIMARY KEY (`invoicelineid`),
  KEY `FK_invoiceid` (`invoiceid`),
  KEY `FK_toolnumber` (`toolnumber`),
  CONSTRAINT `FK_invoiceid` FOREIGN KEY (`invoiceid`) REFERENCES `invoice` (`invoiceid`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `FK_toolnumber` FOREIGN KEY (`toolnumber`) REFERENCES `tool` (`toolnumber`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `invoiceline`
--

LOCK TABLES `invoiceline` WRITE;
/*!40000 ALTER TABLE `invoiceline` DISABLE KEYS */;
INSERT INTO `invoiceline` VALUES (2,1,'CC3',1,49.99),(3,2,'CC3',2,99.98),(4,2,'HG150',1,149.99),(5,3,'CC3',1,49.99),(6,3,'L68250',2,59.98),(7,4,'AM40QUICKSILVER',2,99.98),(8,5,'MCF894',1,499.99),(9,5,'WSC7G',1,69.99),(10,5,'CC3',1,49.99),(11,6,'CC3',1,49.99),(12,6,'DCC020IB',1,299.99),(13,7,'L39320',1,79.99),(14,7,'L50550',1,30.99),(15,8,'CC3',1,49.99),(16,8,'SBT59800',1,99.99),(17,9,'WSC7G',1,69.99),(18,10,'MCF894',1,499.99),(19,11,'CHP4LT',2,179.98),(20,11,'AM40QUICKSILVER',1,49.99),(21,12,'SBT59800',1,99.99),(22,13,'CHP4LT',1,89.99);
/*!40000 ALTER TABLE `invoiceline` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `paymentlog`
--

DROP TABLE IF EXISTS `paymentlog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `paymentlog` (
  `paymentid` varchar(4) NOT NULL,
  `lastpayed` datetime NOT NULL,
  `amount` decimal(7,2) NOT NULL,
  PRIMARY KEY (`paymentid`,`lastpayed`),
  KEY `idx_log` (`lastpayed`),
  CONSTRAINT `FK_paymentid` FOREIGN KEY (`paymentid`) REFERENCES `payments` (`paymentid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `paymentlog`
--

LOCK TABLES `paymentlog` WRITE;
/*!40000 ALTER TABLE `paymentlog` DISABLE KEYS */;
INSERT INTO `paymentlog` VALUES ('1','2021-05-05 12:37:05',20.00),('1','2021-05-05 12:51:17',15.00),('10','2021-05-05 12:37:05',18.00),('11','2021-05-05 14:02:11',15.00),('2','2021-05-05 12:37:05',30.00),('2','2021-05-05 12:54:48',15.00),('3','2021-05-05 12:37:05',80.00),('4','2021-05-05 12:37:05',50.00),('5','2021-05-05 12:37:05',25.00),('6','2021-05-05 12:37:05',25.19),('7','2021-05-05 12:37:05',19.00),('8','2021-05-05 12:37:05',27.00),('9','2021-05-05 12:37:05',40.00);
/*!40000 ALTER TABLE `paymentlog` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `payments`
--

DROP TABLE IF EXISTS `payments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `payments` (
  `customerid` varchar(4) NOT NULL,
  `amountowed` decimal(7,2) NOT NULL,
  `paymentid` varchar(4) NOT NULL,
  `nextpayment` date DEFAULT NULL,
  PRIMARY KEY (`paymentid`),
  UNIQUE KEY `customerid` (`customerid`),
  CONSTRAINT `FK_customerid` FOREIGN KEY (`customerid`) REFERENCES `customer` (`customerid`),
  CONSTRAINT `payments_chk_1` CHECK ((`amountowed` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `payments`
--

LOCK TABLES `payments` WRITE;
/*!40000 ALTER TABLE `payments` DISABLE KEYS */;
INSERT INTO `payments` VALUES ('1',14.99,'1','2021-05-19'),('10',81.99,'10','2021-05-19'),('11',74.99,'11','2021-05-19'),('2',650.95,'2','2021-05-19'),('3',29.97,'3','2021-05-19'),('4',275.98,'4','2021-05-19'),('5',224.97,'5','2021-05-19'),('6',85.79,'6','2021-05-19'),('7',50.99,'7','2021-05-19'),('8',598.97,'8','2021-05-19'),('9',189.97,'9','2021-05-19');
/*!40000 ALTER TABLE `payments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tool`
--

DROP TABLE IF EXISTS `tool`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tool` (
  `toolnumber` varchar(15) NOT NULL,
  `name` varchar(100) NOT NULL,
  `onhand` int NOT NULL,
  `barcode` varchar(20) DEFAULT NULL,
  `unitprice` decimal(6,2) DEFAULT NULL,
  PRIMARY KEY (`toolnumber`),
  KEY `idx_tool` (`toolnumber`),
  CONSTRAINT `tool_chk_1` CHECK ((`onhand` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tool`
--

LOCK TABLES `tool` WRITE;
/*!40000 ALTER TABLE `tool` DISABLE KEYS */;
INSERT INTO `tool` VALUES ('AM40QUICKSILVER','\"4\"\" QUICKSILVER FOLDING KNIFE\"',10,NULL,49.99),('CC3','ANTI-FREEZE HYDROMETER',4,'0089658770800',49.99),('CHP4LT','LED LIGHTED HOOK AND PICK SET',4,'CHP4LT',89.99),('DCC020IB','CORDED/CORDLESS AIR INFLATOR',2,'0885911532143',299.99),('HG150','DUAL TEMPATURE HEAT GUN',3,'0018139341505',149.99),('L39320','TRANSITION OIL COOLER DISCONNECT SET',5,'0083045392255',79.99),('L50550','\"FILTER PLIERS 2\"\" TO 4-1/2\"\"\"',4,'0083045505556',30.99),('L68250','DOUBLE ENDED TRIM HOOK',5,'0083045682455',29.99),('MCF894','\"1/2\"\" BRUSHLESS MID-TORQUE IMPACT WRENCH\"',2,'885911668804',499.99),('SBT59800','SERPENTINE BELT TOOL',2,'0083045598053',99.99),('WSC7G','WIRE STRIPPER',7,'0613364199718',69.99);
/*!40000 ALTER TABLE `tool` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Final view structure for view `allcustomerpayments`
--

/*!50001 DROP VIEW IF EXISTS `allcustomerpayments`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`Hunter`@`%` SQL SECURITY DEFINER */
/*!50001 VIEW `allcustomerpayments` AS select `customer`.`customerid` AS `customerid`,`customer`.`firstname` AS `firstname`,`customer`.`lastname` AS `lastname`,`paymentlog`.`paymentid` AS `paymentid`,`payments`.`amountowed` AS `amountowed`,max(`paymentlog`.`lastpayed`) AS `last_payed` from ((`paymentlog` join `payments` on((`paymentlog`.`paymentid` = `payments`.`paymentid`))) join `customer`) where ((`customer`.`customerid` = `payments`.`customerid`) and (`payments`.`paymentid` = `paymentlog`.`paymentid`)) group by `customer`.`customerid` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-05-08  5:40:38
