-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Oct 19, 2024 at 11:22 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

SET NAMES utf8mb4;

-- Database: `mathalino`
CREATE DATABASE IF NOT EXISTS `math`;
USE `math`;

-- --------------------------------------------------------

-- Table structure for table `questions`
CREATE TABLE `questions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `question_text` text NOT NULL,
  `correct_answer` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dumping data for table `questions`
INSERT INTO `questions` (`id`, `question_text`, `correct_answer`) VALUES
(1, '1 + 1 = ', '2'),
(2, '2 + 2 = ', '4'),
(3, '3 + 3 = ', '6'),
(4, '4 + 4 = ', '8'),
(5, '5 + 5 = ', '10'),
(6, '6 + 6 = ', '12'),
(7, '7 + 7 = ', '14'),
(8, '8 + 8 = ', '16'),
(9, '9 + 9 = ', '18'),
(10, '10 + 10 = ', '20'),
(11, '10 - 1 = ', '9'),
(12, '10 - 2 = ', '8'),
(13, '10 - 3 = ', '7'),
(14, '10 - 4 = ', '6'),
(15, '10 - 5 = ', '5'),
(16, '10 - 6 = ', '4'),
(17, '10 - 7 = ', '3'),
(18, '10 - 8 = ', '2'),
(19, '10 - 9 = ', '1'),
(20, '10 - 10 = ', '0'),
(21, '2 * 2 = ', '4'),
(22, '3 * 3 = ', '9'),
(23, '4 * 4 = ', '16'),
(24, '5 * 5 = ', '25'),
(25, '6 * 6 = ', '36'),
(26, '7 * 7 = ', '49'),
(27, '8 * 8 = ', '64'),
(28, '9 * 9 = ', '81'),
(29, '10 * 10 = ', '100'),
(30, '11 * 11 = ', '121'),
(31, '10 / 2 = ', '5'),
(32, '10 / 5 = ', '2'),
(33, '20 / 4 = ', '5'),
(34, '20 / 10 = ', '2'),
(35, '50 / 5 = ', '10'),
(36, '50 / 10 = ', '5'),
(37, '100 / 10 = ', '10'),
(38, '100 / 20 = ', '5'),
(39, '100 / 25 = ', '4'),
(40, '100 / 50 = ', '2');

-- --------------------------------------------------------

-- Table structure for table `scores`
CREATE TABLE `scores` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `score` decimal(5,2) NOT NULL,
  `date_taken` timestamp NOT NULL DEFAULT current_timestamp(),
  `proficiency` varchar(255) DEFAULT NULL,
  `teacher_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `fk_teacher_id` (`teacher_id`),
  CONSTRAINT `fk_teacher_id` FOREIGN KEY (`teacher_id`) REFERENCES `teachers` (`id`),
  CONSTRAINT `scores_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dumping data for table `scores`
INSERT INTO `scores` (`id`, `user_id`, `score`, `date_taken`, `proficiency`, `teacher_id`) VALUES
(14, 9, 7.00, '2024-10-19 08:59:07', 'Not Proficient', NULL),
(15, 9, 10.00, '2024-10-19 08:59:42', 'Not Proficient', NULL),
(16, 9, 7.00, '2024-10-19 08:59:59', 'Not Proficient', NULL),
(17, 9, 10.00, '2024-10-19 09:00:19', 'Not Proficient', NULL);

-- --------------------------------------------------------

-- Table structure for table `teachers`
CREATE TABLE `teachers` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `fullname` varchar(255) NOT NULL,
  `section` varchar(255) NOT NULL,
  `secret_key` varchar(255) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dumping data for table `teachers`
INSERT INTO `teachers` (`id`, `fullname`, `section`, `secret_key`, `password_hash`) VALUES
(4, 'John Mark', 'sunflower', 'GAGO_GAGO_SI_JOREL', 'pbkdf2:sha256:600000$NdjjmSx2OxCOCV2v$69a191a6df0d12f36fb26fed4528fad688c6839068d2e3665de5462d8be674d3');

-- --------------------------------------------------------

-- Table structure for table `users`
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `fullname` varchar(255) NOT NULL,
  `section` varchar(100) NOT NULL,
  `age` int(3) NOT NULL,
  `gender` enum('male','female','other','prefer_not_to_say') NOT NULL,
  `password_hash` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dumping data for table `users`
INSERT INTO `users` (`id`, `username`, `fullname`, `section`, `age`, `gender`, `password_hash`) VALUES
(1, 'admin', '', '', 0, 'male', '$2b$12$fahQinHrKWtrzXSrAh6CQeEUhg6Y6Ykr4XqEKIAX7M6NbGvQe.NmO'),
(2, 'jboy', '', '', 0, 'male', '$2b$12$zvwkLR6jMdziNr6fB33OTu5XGK0NMKKUBzwwdF/lJGmvrDGLzUm8q'),
(3, 'anne', '', '', 0, 'male', '$2b$12$Vxc8xff6C0n3lbQPCSI0G.T5J5YFjkFLpNp.QqdfW7ZJ7o5e3RJta'),
(9, 'john mark', 'John Mark', 'rose', 13, 'male', '$2b$12$MnUbtptLNZ3ldmK92qkxguJLxlXpiUqWXqHaaxfMNNuJsEGU02Emu');

COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;