-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 28-04-2022 a las 06:54:51
-- Versión del servidor: 10.4.19-MariaDB
-- Versión de PHP: 8.0.7

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `proyecto_ia`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `user`
--

CREATE TABLE `user` (
  `User` varchar(100) NOT NULL,
  `Password` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `user_preferences`
--

CREATE TABLE `user_preferences` (
  `Id` int(11) NOT NULL,
  `UserId` varchar(50) NOT NULL,
  `MovieId` varchar(200) NOT NULL,
  `Value` double DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `user_preferences`
--

INSERT INTO `user_preferences` (`Id`, `UserId`, `MovieId`, `Value`) VALUES
(1, 'jdeleon', '#Titanic', 1),
(2, 'jdeleon', 'Fast and Furious', 1),
(3, 'pcuevas', 'Spiderman', 1),
(4, 'pcuevas', 'Spiderman', 1),
(5, 'jdeleon', 'Dr. Strange', 0.5);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `user_preferences`
--
ALTER TABLE `user_preferences`
  ADD PRIMARY KEY (`Id`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `user_preferences`
--
ALTER TABLE `user_preferences`
  MODIFY `Id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;


/*Creación de la tabla csv para guardar la información*/

CREATE TABLE `csv` (
	`movie_title` VARCHAR(50) PRIMARY KEY,
	`num_voted_users` VARCHAR(50) NOT NULL,
	`imdb_score` VARCHAR(5) NOT NULL,
	`director_name` VARCHAR(50) NOT NULL,
	`actor_1_name` VARCHAR(50) NOT NULL,
	`actor_2_name` VARCHAR(50) NOT NULL,
	`actor_3_name` VARCHAR(50) NOT NULL,
	`genres` VARCHAR(100) NOT NULL,
	`plot_keywords` VARCHAR(100) NOT NULL
)