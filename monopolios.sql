-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 13-05-2023 a las 02:59:00
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
CREATE DEFINER=`admin`@`localhost` PROCEDURE `Comprar_Propiedad` (IN `nombre_jugador` VARCHAR(30), IN `vdinero_jugador` INT(6), IN `nombre_propiedad` VARCHAR(30), IN `vcosto_propiedad` INT(6))   BEGIN
    IF vdinero_jugador >= vcosto_propiedad THEN
        UPDATE propiedades SET dueño = nombre_jugador WHERE nombre = nombre_propiedad;
        UPDATE jugadores SET dinero = dinero - vcosto_propiedad WHERE nombre = nombre_jugador;
        INSERT INTO movimientos (accion) VALUES (concat(nombre_jugador, ' compró ', nombre_propiedad, ' dinero: ',  (SELECT dinero FROM jugadores WHERE nombre = nombre_jugador)));
    END IF;
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

CREATE DEFINER=`admin`@`localhost` PROCEDURE `hipotecar_propiedad` (IN `Nombre_Propiedad` VARCHAR(30))   BEGIN
    UPDATE propiedades SET hipotecado = 1 where nombre = Nombre_Propiedad;
    UPDATE jugadores SET dinero = dinero + (SELECT hipoteca FROM propiedades WHERE nombre = Nombre_Propiedad);
    INSERT INTO movimientos (accion) VALUES (CONCAT((SELECT dueño FROM propiedades WHERE nombre = Nombre_Propiedad), ' hipoteco ', Nombre_Propiedad));
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

CREATE DEFINER=`admin`@`localhost` PROCEDURE `Rendirse_Abandono` (IN `Nombre_Jugador` VARCHAR(30))   BEGIN
    UPDATE propiedades SET dueño = NULL where dueño = Nombre_Jugador;
    INSERT INTO movimientos (accion) VALUES (CONCAT(Nombre_Jugador, ' se rindió y todo su dinero y propiedades pasan a ser del banco')); 
END$$

CREATE DEFINER=`admin`@`localhost` PROCEDURE `Rendirse_Compartir` (IN `Nombre_Jugador` VARCHAR(30))   BEGIN
INSERT INTO movimientos (accion) VALUES (CONCAT(Nombre_Jugador, ' se rindio, compartiendo ', (SELECT FLOOR(((SELECT dinero FROM jugadores WHERE nombre = 'Gato') + (SELECT ((SELECT dinero FROM jugadores WHERE nombre = 'Gato') + (SELECT COALESCE((SELECT sum(precio) FROM propiedades WHERE dueño = 'Gato' AND hipotecado = 0), 0))) / (SELECT COUNT(nombre) - 1 FROM jugadores))) / (SELECT COUNT(nombre) - 1 FROM jugadores))), ' a todos los jugadores'));

	UPDATE jugadores SET dinero = dinero + (SELECT FLOOR(((SELECT dinero FROM jugadores WHERE nombre = 'Gato') + (SELECT ((SELECT dinero FROM jugadores WHERE nombre = 'Gato') + (SELECT COALESCE((SELECT sum(precio) FROM propiedades WHERE dueño = 'Gato' AND hipotecado = 0), 0))) / (SELECT COUNT(nombre) - 1 FROM jugadores))) / (SELECT COUNT(nombre) - 1 FROM jugadores)));


UPDATE jugadores SET dinero = 0 WHERE nombre = Nombre_Jugador;

UPDATE propiedades SET dueño = NULL, hipotecado = 0 WHERE dueño = Nombre_Jugador;

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
('Bruno', 'bruno', 1500, 'Bonos', 0),
('Gato', 'gato', 1500, 'Bonos', 0),
('Polo', 'polo', 1500, 'Bonos', 0);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `movimientos`
--

CREATE TABLE `movimientos` (
  `id` int(11) NOT NULL,
  `accion` varchar(100) NOT NULL,
  `tiempo` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `movimientos`
--

INSERT INTO `movimientos` (`id`, `accion`, `tiempo`) VALUES
(1, 'Comienza el juego', '2023-05-12 18:46:39'),
(2, 'Gato se unió al juego, Dinero: $1500 Pasiva: Bonos', '2023-05-12 18:46:52'),
(3, 'Bruno se unió al juego, Dinero: $1500 Pasiva: Bonos', '2023-05-12 18:47:00'),
(4, 'Polo se unió al juego, Dinero: $1500 Pasiva: Bonos', '2023-05-12 18:47:09');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `pasivas`
--

CREATE TABLE `pasivas` (
  `nombre` varchar(50) NOT NULL,
  `descripcion` varchar(100) NOT NULL,
  `enfriamiento` int(2) NOT NULL,
  `extras` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `pasivas`
--

INSERT INTO `pasivas` (`nombre`, `descripcion`, `enfriamiento`, `extras`) VALUES
('Bonos', 'Obtener 100$.', 2, 'Puede se robado por otros jugadores1'),
('Cambio de roles', 'Cambiar la posición del token con otro jugador.', 3, 'El otro jugador no realiza ninguna acción, no afecta en el primer turno para la salida'),
('Compra ventajosa', 'Propiedades por mitad de precio', 0, 'Al ganar subasta tambíen se paga la mitad de lo establecido.'),
('Constructor', 'Se obtiene un casa gratis', 3, 'Se activa al obtener un grupo de color, pero se pueden acumular 2, no incluye hoteles.'),
('Dia de suerte', 'No pagar renta.', 5, 'Puede anular \'Bonanza\''),
('Doble recompensa', 'Duplicar dinero obtenido.', 3, 'Se puedee usar en \'parada libre\', entre otros, no aplica en rentas.'),
('Duelo', 'Ambos tiran los dados y el que pierde le paga 100$ al otro jugador.', 3, 'el jugador que usa la habilidad está con ventaja de de 3'),
('Inmunidad a impuestos', 'No pagar impuestos, bonos por grupos de color, y cartas de fortuna y arca comunal.', 0, 'no incluye renta de casas y hoteles.'),
('Movilidad', '+1 dado con 3 casillas en la jugada, se cuenta como dado adicional.', 3, 'Se puede usar con el dado veloz (dado rojo)'),
('Policia', 'Poder encarcelar a un jugador o encarcelarse a si mismo.', 4, 'No pagar por salida de la carcel, cobrar mientras está en la carcel (en caso de aplicar)'),
('Propiedades iniciales', '4 propiedades aleatorias gratis al comenzar.', 0, 'Se puede elegir una, pero se reduce el numero a 3 propiedades'),
('Rentabilidad Aumentada.', 'Al momento de cobrar renta se cobra como con 3 casas.', 4, 'El numero de casas adicional es fijo, se puede robar y evadir por otros jugadores'),
('Reposicionamiento', 'Mover el token a una casilla.', 5, 'Se debe realizar la acción de la misma (sin limites), no hay excepcion de casilla'),
('Saqueador', 'Robar una transacción', 4, 'No aplica al pagar renta propia, en la compra de una propiedad el que la compró recibe su propiedad.'),
('Señor de las cartas', 'Tomar carta y poder guardarla en secreto (max 2)', 2, 'Se puede dar a otro jugador.');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `propiedades`
--

CREATE TABLE `propiedades` (
  `nombre` varchar(30) NOT NULL,
  `color` varchar(20) NOT NULL,
  `precio` int(6) NOT NULL,
  `costo_casa` int(6) DEFAULT NULL,
  `hipoteca` int(6) NOT NULL,
  `costo_deshipoteca` int(6) NOT NULL,
  `dueño` varchar(30) DEFAULT NULL,
  `hipotecado` tinyint(1) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `propiedades`
--

INSERT INTO `propiedades` (`nombre`, `color`, `precio`, `costo_casa`, `hipoteca`, `costo_deshipoteca`, `dueño`, `hipotecado`) VALUES
('Avenida Mediterraneo', 'Marron', 60, 50, 30, 33, NULL, 0),
('Avenida Baltica', 'Marron', 60, 50, 30, 33, NULL, 0),
('Ferrocarril de Reading', 'Negro', 200, NULL, 100, 110, NULL, 0),
('Avenida Oriental', 'Celeste', 100, 50, 50, 55, NULL, 0),
('Avenida Vermont', 'Celeste', 100, 50, 50, 55, NULL, 0),
('Avenida Connecticut', 'Celeste', 120, 50, 60, 66, NULL, 0),
('Plaza San Carlos', 'Morado', 140, 100, 70, 77, NULL, 0),
('Compañía de Electricidad', 'Servicio', 150, NULL, 75, 83, NULL, 0),
('Avenida Estados', 'Morado', 140, 100, 70, 77, NULL, 0),
('Avenida Virginia', 'Morado', 160, 100, 80, 88, NULL, 0),
('Ferrocarril Pensilvania', 'Negro', 200, NULL, 100, 110, NULL, 0),
('Avenida San James', 'Naranja', 180, 100, 90, 99, NULL, 0),
('Avenida Tennessee', 'Naranja', 180, 100, 90, 99, NULL, 0),
('Avenida Nueva York', 'Naranja', 200, 100, 100, 110, NULL, 0),
('Avenida Kentucky', 'Rojo', 220, 150, 110, 110, NULL, 0),
('Avenida Indiana', 'Rojo', 220, 150, 110, 110, NULL, 0),
('Avenida Illinois', 'Rojo', 240, 150, 120, 142, NULL, 0),
('Ferrocarril B&O', 'Negro', 200, NULL, 100, 110, NULL, 0),
('Avenida Atlantico', 'Amarillo', 260, 150, 130, 143, NULL, 0),
('Avenida Ventnor', 'Amarillo', 260, 150, 130, 143, NULL, 0),
('Compañía de Agua', 'Servicio', 150, NULL, 75, 83, NULL, 0),
('Jardines Marvin', 'Amarillo', 280, 150, 140, 154, NULL, 0),
('Avenida Pacifico', 'Verde', 300, 200, 150, 165, NULL, 0),
('Avenida Carolina del Norte', 'Verde', 300, 200, 150, 165, NULL, 0),
('Avenida Pensilvania', 'Verde', 320, 200, 160, 175, NULL, 0),
('Ferrocarril Via Rápida', 'Negro', 200, NULL, 100, 110, NULL, 0),
('Plaza Park', 'Azul', 350, 200, 175, 193, NULL, 0),
('El Muelle', 'Azul', 400, 200, 200, 220, NULL, 0);

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
-- Indices de la tabla `movimientos`
--
ALTER TABLE `movimientos`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `pasivas`
--
ALTER TABLE `pasivas`
  ADD PRIMARY KEY (`nombre`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `movimientos`
--
ALTER TABLE `movimientos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
