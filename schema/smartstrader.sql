-- phpMyAdmin SQL Dump
-- version 4.0.4
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Jan 02, 2014 at 02:07 AM
-- Server version: 5.6.12-log
-- PHP Version: 5.4.16

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `smartstrader`
--
CREATE DATABASE IF NOT EXISTS `smartstrader` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `smartstrader`;

-- --------------------------------------------------------

--
-- Table structure for table `stock_symbols`
--

DROP TABLE IF EXISTS `stock_symbols`;
CREATE TABLE IF NOT EXISTS `stock_symbols` (
  `sid` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `symbol` varchar(8) NOT NULL,
  `cname` varchar(64) NOT NULL,
  `fname` varchar(64) NOT NULL,
  `brief` varchar(512) NOT NULL,
  `firsttrade` date NOT NULL,
  `52weeklow` decimal(10,0) NOT NULL,
  `52weekhigh` decimal(10,0) NOT NULL,
  `lastpriceopen` decimal(10,0) NOT NULL COMMENT 'last trade day''s open price',
  `lastpriceclose` decimal(10,0) NOT NULL,
  `lastpricehigh` decimal(10,0) NOT NULL,
  `lastpricelow` decimal(10,0) NOT NULL,
  PRIMARY KEY (`sid`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=2 ;

--
-- Truncate table before insert `stock_symbols`
--

TRUNCATE TABLE `stock_symbols`;
--
-- Dumping data for table `stock_symbols`
--

INSERT INTO `stock_symbols` (`sid`, `symbol`, `cname`, `fname`, `brief`, `firsttrade`, `52weeklow`, `52weekhigh`, `lastpriceopen`, `lastpriceclose`, `lastpricehigh`, `lastpricelow`) VALUES
(1, 'QIHU', '', '', '', '0000-00-00', '0', '0', '0', '0', '0', '0');

-- --------------------------------------------------------

--
-- Table structure for table `trade_daily_history`
--

DROP TABLE IF EXISTS `trade_daily_history`;
CREATE TABLE IF NOT EXISTS `trade_daily_history` (
  `sid` int(11) NOT NULL,
  `openprice` decimal(10,0) NOT NULL,
  `closeprice` decimal(10,0) NOT NULL,
  `highprice` decimal(10,0) NOT NULL,
  `lowprice` decimal(10,0) NOT NULL,
  `volume` int(11) NOT NULL,
  `tradeday` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Truncate table before insert `trade_daily_history`
--

TRUNCATE TABLE `trade_daily_history`;
-- --------------------------------------------------------

--
-- Table structure for table `trade_minute_history`
--

DROP TABLE IF EXISTS `trade_minute_history`;
CREATE TABLE IF NOT EXISTS `trade_minute_history` (
  `sid` int(10) unsigned NOT NULL,
  `price` decimal(10,4) NOT NULL,
  `server_time` datetime NOT NULL,
  `client_time` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Truncate table before insert `trade_minute_history`
--

TRUNCATE TABLE `trade_minute_history`;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
