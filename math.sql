-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Nov 03, 2024 at 10:39 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `math`
--

-- --------------------------------------------------------

--
-- Table structure for table `questions`
--

CREATE TABLE `questions` (
  `id` int(11) NOT NULL,
  `question_text` text NOT NULL,
  `correct_answer` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `questions`
--

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

--
-- Table structure for table `scores`
--

CREATE TABLE `scores` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `gender` enum('male','female','other','prefer_not_to_say') DEFAULT NULL,
  `score` decimal(5,2) NOT NULL,
  `date_taken` timestamp NOT NULL DEFAULT current_timestamp(),
  `proficiency` varchar(255) DEFAULT NULL,
  `teacher_id` int(11) DEFAULT NULL,
  `total_time_spent` int(11) DEFAULT NULL,
  `time_per_question` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`time_per_question`))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `scores`
--

INSERT INTO `scores` (`id`, `user_id`, `gender`, `score`, `date_taken`, `proficiency`, `teacher_id`, `total_time_spent`, `time_per_question`) VALUES
(54, 9, NULL, 67.00, '2024-10-27 14:38:46', 'Proficient', NULL, 43, '[2, 1, 2, 1, 2, 2, 1, 1, 1, 1, 1, 1, 2, 2, 1, 3, 1, 1, 1, 1, 2, 1, 2, 2, 2, 2, 1, 2, 1]'),
(55, 13, NULL, 72.00, '2024-10-31 05:12:11', 'Proficient', NULL, 47, '[2, 1, 2, 2, 1, 2, 1, 1, 2, 1, 1, 2, 1, 2, 2, 1, 1, 1, 2, 2, 2, 1, 3, 1, 2, 2, 2, 3, 1]'),
(56, 13, NULL, 60.00, '2024-10-31 05:13:19', 'Nearly Proficient', NULL, 44, '[2, 1, 2, 2, 1, 1, 2, 1, 1, 2, 2, 3, 1, 1, 1, 2, 1, 6, 1, 1, 3, 2, 2, 1, 1, 1]'),
(60, 9, NULL, 60.00, '2024-11-03 05:43:21', 'Nearly Proficient', NULL, 50, '[2, 1, 2, 3, 2, 2, 2, 2, 1, 1, 3, 4, 3, 1, 2, 1, 2, 2, 1, 3, 1, 2, 2, 1, 2, 2]');

-- --------------------------------------------------------

--
-- Table structure for table `teachers`
--

CREATE TABLE `teachers` (
  `id` int(11) NOT NULL,
  `fullname` varchar(255) NOT NULL,
  `section` varchar(255) NOT NULL,
  `secret_key` varchar(255) NOT NULL,
  `password_hash` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `teachers`
--

INSERT INTO `teachers` (`id`, `fullname`, `section`, `secret_key`, `password_hash`) VALUES
(4, 'john mark', 'sampagita', 'GAGO_GAGO_SI_JOREL', 'pbkdf2:sha256:600000$wdsf5lqgsjjFRq2q$6272b216dee8e6ae8501b8b0e7dad4add7c385d697abd0e076509b4d96372041'),
(5, 'jm', 'rose', 'GAGO_GAGO_SI_JOREL', 'pbkdf2:sha256:600000$m0dEpJuV0GRj16uO$24b825bade1f8b4040169d54fc1dcf580abcad49789efc580d0b61cbfc1e7e09'),
(6, 'natoy', 'marijuana', 'GAGO_GAGO_SI_JOREL', 'pbkdf2:sha256:600000$uXJmZaNPBD4VicCY$d8d989d1d85605ad2ab349a2a4539b8f1d26c7be53700f223bc2490ccb0a7782');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `fullname` varchar(255) NOT NULL,
  `section` varchar(100) NOT NULL,
  `age` int(3) NOT NULL,
  `gender` enum('male','female','other','prefer_not_to_say') NOT NULL,
  `password_hash` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `username`, `fullname`, `section`, `age`, `gender`, `password_hash`) VALUES
(9, 'jm', 'jm', 'marijuana', 13, 'male', '$2b$12$Hs56s3nszPHiKztj7HAOpuYm2U7oAA7G38YIVSW6DGMAdsWyb6j2y'),
(10, 'john', 'john', 'sunflower', 15, 'male', '$2b$12$yByoYJ5erHv0Y7THJfPL5.ZOel6uwqq/zaGfMCfZlidIoxZgaL5IO'),
(11, 'anne', 'anne', 'sampagita', 14, 'female', '$2b$12$vVgBfWmIRdSpH6F6AVcI7ORs8cOgbj.q.3rq4czX44ObvLiVeZ.ga'),
(12, 'jaryl', 'jaryl', 'marijuana', 11, 'female', '$2b$12$3pOVYatu.I2UfAEVF6C.ve/NFDi2W53Fo.xYKNf0V8CNorsPGsayG'),
(13, 'man', 'man', 'marijuana', 12, 'female', '$2b$12$cSycFQVt89eBxxXXDALV9e79AdnhSlQxM.cYXiVyrZvoN/yKXrA3C');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `questions`
--
ALTER TABLE `questions`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `scores`
--
ALTER TABLE `scores`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `fk_teacher_id` (`teacher_id`);

--
-- Indexes for table `teachers`
--
ALTER TABLE `teachers`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `questions`
--
ALTER TABLE `questions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=41;

--
-- AUTO_INCREMENT for table `scores`
--
ALTER TABLE `scores`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=61;

--
-- AUTO_INCREMENT for table `teachers`
--
ALTER TABLE `teachers`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `scores`
--
ALTER TABLE `scores`
  ADD CONSTRAINT `fk_teacher_id` FOREIGN KEY (`teacher_id`) REFERENCES `teachers` (`id`),
  ADD CONSTRAINT `scores_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
