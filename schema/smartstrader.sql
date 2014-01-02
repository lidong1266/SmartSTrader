-- phpMyAdmin SQL Dump
-- version 4.0.4
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Jan 02, 2014 at 01:54 AM
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
  PRIMARY KEY (`sid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

--
-- Truncate table before insert `stock_symbols`
--

TRUNCATE TABLE `stock_symbols`;
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
