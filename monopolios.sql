-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 11-05-2023 a las 15:49:46
-- Versión del servidor: 10.4.28-MariaDB
-- Versión de PHP: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `monopolios`
--

DELIMITER $$
--
-- Procedimientos
--
CREATE DEFINER=`admin`@`localhost` PROCEDURE `Comprar_Propiedad` (IN `jugador` VARCHAR(50), IN `monto` INT(6))   BEGIN
	UPDATE jugadores SET DINERO = DINERO - monto WHERE NOMBRE = jugador;
    INSERT INTO movimientos (ACCION) VALUES(CONCAT(jugador,' compró una propiedad por $', monto, ', Dinero $', (SELECT DINERO FROM JUGADORES WHERE NOMBRE = jugador)));
END$$

CREATE DEFINER=`admin`@`localhost` PROCEDURE `Crear_Jugador` (IN `vnombre` VARCHAR(30), IN `vpass` VARCHAR(50), IN `vdinero` INT(6), IN `vpasiva` VARCHAR(50))  COMMENT 'agregar un jugador y asignarle pasiva' BEGIN
    IF vnombre = '' OR vpass = '' THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Nombre y contraseña son obligatorios';
    ELSE
        INSERT INTO jugadores (nombre, contraseña, dinero, pasiva, turnos_restantes) 
        VALUES (vnombre, vpass, vdinero, vpasiva, 0);
        INSERT INTO movimientos (ACCION) 
        VALUES (CONCAT(vnombre, ' se unió al juego, Dinero: $', vdinero, ' Pasiva: ', vpasiva));
    END IF;
END$$

CREATE DEFINER=`admin`@`localhost` PROCEDURE `Nuevo_Juego` (IN `confirmar1` VARCHAR(9), IN `confirmar2` VARCHAR(9))   IF confirmar1 = 'Confirmar' AND confirmar2 = 'Confirmar' THEN
    TRUNCATE TABLE jugadores;
    TRUNCATE TABLE MOVIMIENTOS;
    SELECT 'Limpiadas tablas de jugadores y movimientos' AS COMPLETADO;
    INSERT INTO movimientos (accion) VALUES ('Comienza el juego'); 
END IF$$

CREATE DEFINER=`admin`@`localhost` PROCEDURE `Pagar_A_Jugador` (IN `jugador1` VARCHAR(50), IN `jugador2` VARCHAR(50), IN `monto` INT(6))  COMMENT 'Función para pagar jugador A x monto a jugador B' BEGIN
    UPDATE jugadores SET DINERO = DINERO - monto WHERE nombre = jugador1;
    UPDATE jugadores SET DINERO = DINERO + monto WHERE nombre = jugador2;
    INSERT INTO movimientos (accion) VALUES (CONCAT(jugador1, ' pagó $', monto, ' a ', jugador2));
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `Pago_A_Banco` (IN `nombre_jugador` VARCHAR(30), IN `monto_a_pagar` INT(6), IN `razón` VARCHAR(30))   BEGIN
    IF razon = 'carcel' THEN
        UPDATE jugadores SET dinero = dinero - 50 where nombre = nombre_jugador;
        INSERT INTO movimientos (accion) VALUES (CONCAT(nombre_jugador, ' pagó salida de la carcel'));
    ELSE
        UPDATE jugadores SET dinero = dinero - monto_a_pagar where nombre = nombre_jugador;
        INSERT INTO movimientos (accion) VALUES (CONCAT(nombre_jugador, ' pagó al banco ', monto_a_pagar, ' por ', razon));
    END IF;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `Recibir_Dinero_Banco` (IN `v1` VARCHAR(30), IN `v2` INT(6), IN `v3` VARCHAR(20))   BEGIN
    UPDATE jugadores SET dinero = dinero + v2 WHERE nombre = v1;
    INSERT INTO movimientos (accion) VALUES (CONCAT(v1, ' recibio ', v2, ' del banco  por ', v3));
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `Recibir_Dinero_Banco_Vuelta` (IN `nombre_jugador` VARCHAR(30))   BEGIN
    UPDATE jugadores SET dinero = dinero + 100 WHERE nombre = nombre_jugador;
    #UPDATE jugadores SET dinero = dinero - 100 WHERE NOT nombre = nombre_jugador;
    INSERT INTO movimientos (accion) VALUES (CONCAT(nombre_jugador, ' recibio $100 por dar una vuelta!'));
END$$

CREATE DEFINER=`admin`@`localhost` PROCEDURE `Tirar_Dado` (IN `jugador` VARCHAR(50))  COMMENT 'restar 1 al enfriamiento de la habilidad del jugador' BEGIN
    IF ((SELECT turnos_restantes FROM jugadores WHERE nombre = jugador) > 0) THEN
        UPDATE jugadores SET turnos_restantes = turnos_restantes - 1 WHERE nombre = jugador;
        INSERT INTO movimientos (ACCION) VALUES(CONCAT(JUGADOR, ' tiró los dados, ', (SELECT turnos_restantes FROM jugadores where nombre = jugador) ,' turnos restantes'));
    ELSE
        INSERT INTO movimientos (ACCION) VALUES(CONCAT(JUGADOR, ' tiró los dados, ', (SELECT turnos_restantes FROM jugadores where nombre = jugador) ,' turnos restantes'));
    END IF;
END$$

CREATE DEFINER=`admin`@`localhost` PROCEDURE `Usar_Pasiva` (IN `jugador` VARCHAR(50))   BEGIN
  IF (SELECT turnos_restantes FROM jugadores WHERE nombre = jugador) = 0 THEN
    UPDATE jugadores SET turnos_restantes = (SELECT pasivas.enfriamiento FROM pasivas INNER JOIN jugadores ON pasivas.nombre = jugadores.pasiva WHERE jugadores.nombre = jugador) WHERE nombre = jugador;
    INSERT INTO movimientos (ACCION) VALUES (CONCAT(jugador, ' usó ', (SELECT pasiva FROM jugadores WHERE nombre = jugador)));
  END IF;
END$$

CREATE DEFINER=`admin`@`localhost` PROCEDURE `validar_usuario` (IN `vnombre` VARCHAR(30), IN `vpass` VARCHAR(50))   SELECT count(*) FROM jugadores where nombre = vnombre AND contraseña = vpass$$

DELIMITER ;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `jugadores`
--

CREATE TABLE `jugadores` (
  `nombre` varchar(30) NOT NULL,
  `contraseña` varchar(50) NOT NULL,
  `dinero` int(11) NOT NULL,
  `pasiva` varchar(50) NOT NULL,
  `turnos_restantes` int(2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `jugadores`
--

INSERT INTO `jugadores` (`nombre`, `contraseña`, `dinero`, `pasiva`, `turnos_restantes`) VALUES
('Bruno', 'bruno', 1500, 'EspacioGratis', 0),
('Gato', 'gato', 1500, 'Duelo', 0),
('Polo', 'polo', 1500, 'Duelo', 0);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `movimientos`
--

CREATE TABLE `movimientos` (
  `accion` varchar(100) NOT NULL,
  `tiempo` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `movimientos`
--

INSERT INTO `movimientos` (`accion`, `tiempo`) VALUES
('Comienza el juego', '2023-05-11 07:21:07'),
('Gato se unió al juego, Dinero: $1500 Pasiva: Duelo', '2023-05-11 07:39:33'),
('Polo se unió al juego, Dinero: $1500 Pasiva: Duelo', '2023-05-11 07:39:39'),
('Bruno se unió al juego, Dinero: $1500 Pasiva: EspacioGratis', '2023-05-11 07:40:19');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `pasivas`
--

CREATE TABLE `pasivas` (
  `nombre` varchar(50) NOT NULL,
  `descripcion` varchar(100) NOT NULL,
  `enfriamiento` int(2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `pasivas`
--

INSERT INTO `pasivas` (`nombre`, `descripcion`, `enfriamiento`) VALUES
('Duelo', 'Retar a jugador con los dados con ventaja de 3, el perdedor paga $100 al ganador', 3),
('EspacioGratis', 'Recibir 3 propiedades aleatorias', 15),
('No pagar renta', 'No pagar renta', 5);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `jugadores`
--
ALTER TABLE `jugadores`
  ADD PRIMARY KEY (`nombre`),
  ADD KEY `pasiva` (`pasiva`);

--
-- Indices de la tabla `pasivas`
--
ALTER TABLE `pasivas`
  ADD PRIMARY KEY (`nombre`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
