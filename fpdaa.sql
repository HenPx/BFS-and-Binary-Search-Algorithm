-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 18, 2023 at 08:07 PM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `fpdaa`
--

-- --------------------------------------------------------

--
-- Table structure for table `product`
--

CREATE TABLE `product` (
  `namaPemilik` varchar(100) DEFAULT NULL,
  `kategori` varchar(100) DEFAULT NULL,
  `namaBarang` varchar(100) DEFAULT NULL,
  `tahun` int(5) DEFAULT NULL,
  `warna` varchar(100) DEFAULT NULL,
  `harga` decimal(12,2) DEFAULT NULL,
  `deskripsi` mediumtext DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `product`
--

INSERT INTO `product` (`namaPemilik`, `kategori`, `namaBarang`, `tahun`, `warna`, `harga`, `deskripsi`) VALUES
('hen', 'Fashion', 'baju', 2020, 'biru', 15000.00, 'i ni baju agak kurang bagus ya dik'),
('hen', 'Fashion', 'baju', 2020, 'biru', 15000.00, 'i ni baju agak kurang bagus ya dik'),
('mahen', 'Elektronik', 'kiu', 2020, 'sugeng', 2020.00, 'hai kami akan melakukan'),
('kiu', 'Elektronik', 'kiu', 2020, 'sugengj', 20209.00, 'hai kami akan mhelakukan'),
('kiu', 'Elektronik', 'kiu', 2020, 'sugengj', 20209.00, 'hai kami akan mhelakukan'),
('hen', 'Elektronik', 'baju batik yang luar biasa', 2020, 'biru', 29191919.00, 'bajuuuu bagusssss'),
('mahen', 'Elektronik', 'mahen', 10, 'mahen', 10.00, 'bagus'),
('mahen', 'Elektronik', 'koka', 2020, 'kao', 2919.00, 'barang jelek'),
('mahen', 'Elektronik', 'kok', 2020, 'kao', 2919.00, 'barang jelek'),
('mahen', 'Elektronik', 'baju keren', 2022, 'red', 20000.00, 'baju ini sangat cantik');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
