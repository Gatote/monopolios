-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 18-05-2023 a las 05:16:19
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
CREATE DEFINER=`admin`@`localhost` PROCEDURE `Cobrar_Parada_Libre` (IN `Nombre_Jugador` VARCHAR(30))   BEGIN
	SET @dinero_parada_libre = (SELECT ACOMULADO_PARADA_LIBRE FROM VARIABLES);
	IF (SELECT IMPUESTOS_PARA_PARADA_LIBRE FROM variables) = 1 THEN
    	UPDATE jugadores SET DINERO = DINERO + @dinero_parada_libre WHERE NOMBRE = Nombre_Jugador;
        UPDATE variables SET ACOMULADO_PARADA_LIBRE = 0;
        INSERT INTO movimientos (ACCION) VALUES (CONCAT(Nombre_Jugador, " cobró $", @dinero_parada_libre, " de parada libre!"));
    END IF;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `Comprar_Casa` (IN `Nombre_Propiedad` VARCHAR(30))   BEGIN
    SET @es_ferrocarril_o_servicio = (SELECT IF(color = 'servicio' OR color = 'negro', 1, 0) from propiedades where nombre = nombre_propiedad);
    SET @numero_casas = (SELECT NIVEL_RENTA FROM propiedades WHERE nombre = Nombre_Propiedad);
    IF NOT @es_ferrocarril_o_servicio THEN
    	IF @numero_casas BETWEEN 2 AND 5 then
        
        
        
            UPDATE jugadores SET dinero = dinero - (SELECT costo_casa FROM propiedades WHERE nombre = Nombre_Propiedad) WHERE nombre = (SELECT dueño FROM propiedades WHERE nombre = Nombre_Propiedad);
            UPDATE propiedades SET nivel_renta = nivel_renta + 1 WHERE nombre = Nombre_Propiedad;
            INSERT INTO movimientos(ACCION) VALUES(CONCAT(Nombre_Propiedad, ' tiene una casa mas!'));
        END IF;
	END IF;
END$$

CREATE DEFINER=`admin`@`localhost` PROCEDURE `Comprar_Propiedad` (IN `nombre_jugador` VARCHAR(30), IN `vdinero_jugador` INT(6), IN `nombre_propiedad` VARCHAR(30), IN `vcosto_propiedad` INT(6))   BEGIN
    IF vdinero_jugador >= vcosto_propiedad THEN
        UPDATE propiedades SET dueño = nombre_jugador WHERE nombre = nombre_propiedad;
        UPDATE jugadores SET dinero = dinero - vcosto_propiedad WHERE nombre = nombre_jugador;
        INSERT INTO movimientos (accion) VALUES (concat(nombre_jugador, ' compró ', nombre_propiedad));
    END IF;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `Consultar_Dinero_Neto` (IN `Nombre_Jugador` VARCHAR(30))   SELECT (SELECT dinero FROM jugadores WHERE nombre COLLATE utf8mb4_general_ci = Nombre_Jugador COLLATE utf8mb4_general_ci) + 
(IFNULL((SELECT SUM(hipoteca) FROM propiedades WHERE dueño COLLATE utf8mb4_general_ci = Nombre_Jugador COLLATE utf8mb4_general_ci AND hipotecado = 0), 0))$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `Consultar_Numero_Casas` (IN `Nombre_Propiedad` VARCHAR(30))   BEGIN
	set @nombre_propiedad = Nombre_Propiedad;
    SELECT nivel_renta FROM propiedades WHERE nombre = @nombre_propiedad;
END$$

CREATE DEFINER=`admin`@`localhost` PROCEDURE `Consultar_Renta` (IN `Nombre_Propiedad` VARCHAR(30))   BEGIN
    SET @nombre_propiedad = Nombre_Propiedad;
    SET @es_ferrocarril = (SELECT IF(color = 'negro', 1, 0) from propiedades where nombre = nombre_propiedad);
	set @nombre_jugador = (SELECT dueño FROM `propiedades` WHERE nombre COLLATE utf8mb4_general_ci = @nombre_propiedad COLLATE utf8mb4_general_ci);
    SET @color_propiedad = (SELECT color FROM `propiedades` WHERE nombre COLLATE utf8mb4_general_ci = @nombre_propiedad COLLATE utf8mb4_general_ci);
    set @numero_propiedades_color = (SELECT count(*) FROM `propiedades` WHERE color = @color_propiedad);
    set @numero_propiedades_obtenidas = (SELECT count(*) FROM `propiedades` WHERE dueño COLLATE utf8mb4_general_ci = @nombre_jugador COLLATE utf8mb4_general_ci);

	if @es_ferrocarril THEN
    	if @numero_propiedades_obtenidas = 1 THEN
            SELECT 25;
        elseif @numero_propiedades_obtenidas = 2 THEN
            SELECT 50;
        elseif @numero_propiedades_obtenidas = 3 THEN
            SELECT 100;
        elseif @numero_propiedades_obtenidas = 4 THEN
            SELECT 200;
        END IF;
    ELSE
        if @numero_propiedades_color = @numero_propiedades_obtenidas THEN
            (SELECT renta_grupo FROM propiedades WHERE nombre = Nombre_Propiedad);
        else

            SET @nivel_renta = (SELECT nivel_renta FROM propiedades WHERE nombre = Nombre_Propiedad);
            IF @nivel_renta = 1 THEN
                (SELECT renta FROM propiedades WHERE nombre = Nombre_Propiedad);
            ELSEIF @nivel_renta = 2 THEN
                (SELECT renta_grupo FROM propiedades WHERE nombre = Nombre_Propiedad);
            ELSEIF @nivel_renta = 3 THEN
                (SELECT renta_1 FROM propiedades WHERE nombre = Nombre_Propiedad);
            ELSEIF @nivel_renta = 4 THEN
                (SELECT renta_2 FROM propiedades WHERE nombre = Nombre_Propiedad);
            ELSEIF @nivel_renta = 5 THEN
                (SELECT renta_3 FROM propiedades WHERE nombre = Nombre_Propiedad);
            ELSEIF @nivel_renta = 6 THEN
                (SELECT renta_4 FROM propiedades WHERE nombre = Nombre_Propiedad);
            ELSEIF @nivel_renta = 7 THEN
                (SELECT renta_5 FROM propiedades WHERE nombre = Nombre_Propiedad);
            END IF;
        END IF;
    END IF;
END$$

CREATE DEFINER=`admin`@`localhost` PROCEDURE `Crear_Jugador` (IN `vnombre` VARCHAR(30), IN `vpass` VARCHAR(50), IN `vdinero` INT(6), IN `vpasiva` VARCHAR(50))  COMMENT 'agregar un jugador y asignarle pasiva' BEGIN
    IF vnombre = '' OR vpass = '' THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Nombre y contraseña son obligatorios';
    ELSE
        IF vpasiva <> '' THEN
            INSERT INTO jugadores (nombre, contraseña, dinero, pasiva, turnos_restantes) 
            VALUES (vnombre, vpass, vdinero, vpasiva, 0);
            INSERT INTO movimientos (ACCION) 
            VALUES (CONCAT(vnombre, ' se unió, Dinero: $', vdinero, ' Pasiva: ', vpasiva));
        ELSE
            INSERT INTO jugadores (nombre, contraseña, dinero, pasiva, turnos_restantes) 
            VALUES (vnombre, vpass, vdinero, vpasiva, 0);
            INSERT INTO movimientos (ACCION) 
            VALUES (CONCAT(vnombre, ' se unió, Dinero: $', vdinero));
        END IF;
    END IF;
END$$

CREATE DEFINER=`admin`@`localhost` PROCEDURE `Dar_Propiedad_Trato` (IN `Nombre_Propiedad` VARCHAR(30), IN `Nombre_Jugador_Receptor` VARCHAR(30))   BEGIN
	SET @color = (SELECT color FROM propiedades WHERE nombre = Nombre_Propiedad);
	SET @dueno_anterior = (SELECT dueño FROM propiedades WHERE nombre = Nombre_Propiedad);
	UPDATE propiedades SET dueño = Nombre_Jugador_Receptor WHERE nombre = Nombre_Propiedad;
	UPDATE propiedades SET nivel_renta = 1 WHERE color = @color;
    INSERT INTO movimientos (accion) VALUES(concat(@dueno_anterior, " dio ", Nombre_Propiedad, " a ", Nombre_Jugador_Receptor)); 
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `Deshipotecar_Propiedad` (IN `Nombre_Propiedad` VARCHAR(30))   BEGIN
    UPDATE propiedades SET hipotecado = 0 where nombre = Nombre_Propiedad;
    UPDATE jugadores SET dinero = dinero - (SELECT costo_deshipoteca FROM propiedades WHERE nombre = Nombre_Propiedad);
    INSERT INTO movimientos (accion) VALUES (CONCAT((SELECT dueño FROM propiedades WHERE nombre = Nombre_Propiedad), ' deshipotecó ', Nombre_Propiedad));
END$$

CREATE DEFINER=`admin`@`localhost` PROCEDURE `Hipotecar_Propiedad` (IN `Nombre_Propiedad` VARCHAR(30))   BEGIN
    UPDATE propiedades SET hipotecado = 1 where nombre = Nombre_Propiedad;
    UPDATE jugadores SET dinero = dinero + (SELECT hipoteca FROM propiedades WHERE nombre = Nombre_Propiedad);
    INSERT INTO movimientos (accion) VALUES (CONCAT((SELECT dueño FROM propiedades WHERE nombre = Nombre_Propiedad), ' hipoteco ', Nombre_Propiedad));
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `Montar_Grupo_Color` (IN `Nombre_Propiedad` VARCHAR(30))   BEGIN
	set @nombre_propiedad = Nombre_Propiedad;
    SET @nombre_jugador = (SELECT dueño FROM propiedades WHERE NOMBRE = @nombre_propiedad);
	SET @color_propiedad = (SELECT COLOR FROM propiedades WHERE NOMBRE = @nombre_propiedad);
    set @numero_propiedades_color = (SELECT count(*) FROM `propiedades` WHERE color = @color_propiedad);
    set @numero_propiedades_obtenidas = (SELECT count(*) FROM `propiedades` WHERE dueño COLLATE utf8mb4_general_ci = @nombre_jugador COLLATE utf8mb4_general_ci and color = @color_propiedad);
    IF @numero_propiedades_color = @numero_propiedades_obtenidas THEN
    	UPDATE propiedades SET nivel_renta = 2 WHERE color = @color_propiedad;
        INSERT into movimientos(accion) VALUES (concat(@nombre_jugador, ' hizo el grupo de color ', @color_propiedad, '!'));
    	SELECT concat('Montaste el grupo de color ', @color_propiedad) AS Mensaje;
    ELSE
    	SELECT concat('No tienes todas las propiedades disponibles', @color_propiedad) AS Mensaje;
    END IF;
END$$

CREATE DEFINER=`admin`@`localhost` PROCEDURE `Nuevo_Juego` (IN `v_impuestos_para_parada_libre` BOOLEAN, IN `v_dinero_inicio_personaliazdo` BOOLEAN, IN `v_dinero_inicio` INT, IN `v_bono_salida` BOOLEAN, IN `v_pasivas_activas` BOOLEAN, IN `v_modo_exponencial` BOOLEAN, IN `v_jugador_moderador` VARCHAR(30), IN `v_tratos_con_propiedades_disponibles` BOOLEAN)   BEGIN
    TRUNCATE TABLE jugadores;
    TRUNCATE TABLE MOVIMIENTOS;
    SELECT 'Limpiadas tablas de jugadores y movimientos' AS COMPLETADO;
    INSERT INTO movimientos (accion) VALUES ('Comienza el juego'); 
    UPDATE propiedades SET dueño = NULL, hipotecado = 0, nivel_renta = 1;
    UPDATE variables SET impuestos_para_parada_libre = v_impuestos_para_parada_libre, dinero_inicio_personalizado = v_dinero_inicio_personaliazdo, dinero_inicio = v_dinero_inicio, acomulado_parada_libre = 0, bono_salida = v_bono_salida, pasivas_activas = v_pasivas_activas, modo_exponencial = v_modo_exponencial, jugador_moderador = v_jugador_moderador, multiplicador_exponencial = 1, tratos_con_propiedades_disponibles = v_tratos_con_propiedades_disponibles;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `Pagar_A_Banco` (IN `Nombre_Jugador` VARCHAR(30), IN `Monto_A_Pagar` INT(6))   BEGIN
	UPDATE jugadores SET DINERO = DINERO - Monto_A_Pagar WHERE nombre = Nombre_Jugador;
    INSERT INTO movimientos (accion) VALUES (CONCAT(Nombre_Jugador, ' pago ', Monto_A_Pagar, ' al banco'));
END$$

CREATE DEFINER=`admin`@`localhost` PROCEDURE `Pagar_A_Jugador` (IN `jugador1` VARCHAR(50), IN `jugador2` VARCHAR(50), IN `monto` INT(6))  COMMENT 'Función para pagar jugador A x monto a jugador B' BEGIN
    UPDATE jugadores SET DINERO = DINERO - monto WHERE nombre = jugador1;
    UPDATE jugadores SET DINERO = DINERO + monto WHERE nombre = jugador2;
    INSERT INTO movimientos (accion) VALUES (CONCAT(jugador1, ' pagó $', monto, ' a ', jugador2));
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `Pagar_Carcel` (IN `Nombre_Jugador` VARCHAR(30))   BEGIN
	UPDATE jugadores SET dinero = dinero - 50 WHERE nombre = Nombre_Jugador;
    INSERT INTO movimientos (accion) VALUES (CONCAT(Nombre_Jugador, ' pago salida de carcel')); 
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `Pagar_impuestos` (IN `Nombre_Jugador` VARCHAR(30), IN `Monto_A_Pagar` INT(6), IN `Impuestos_Para_Parada_Libre` BOOLEAN)   BEGIN
	IF Impuestos_Para_Parada_libre = 1 THEN
        UPDATE jugadores SET dinero = dinero - Monto_A_Pagar where nombre = Nombre_Jugador;
        UPDATE variables SET acomulado_parada_libre = acomulado_parada_libre + Monto_A_Pagar;
        INSERT INTO movimientos (accion) VALUES (CONCAT('Premio parada libre: $', (SELECT acomulado_parada_libre FROM variables)));
        INSERT INTO movimientos (accion) VALUES (CONCAT(Nombre_Jugador, ' sumó $', Monto_A_Pagar, ' a parada libre'));
    ELSE
        UPDATE jugadores SET dinero = dinero - Monto_A_Pagar where nombre = Nombre_Jugador;
        INSERT INTO movimientos (accion) VALUES (CONCAT(Nombre_Jugador, ' pagó $', Monto_A_Pagar, ' de impuestos'));
    END IF;
END$$

CREATE DEFINER=`admin`@`localhost` PROCEDURE `Pagar_Trato` (IN `Nombre_Jugador` VARCHAR(30), IN `Cantidad_Dinero` INT(6), IN `Nombre_Jugador_Receptor` VARCHAR(30))   BEGIN
	UPDATE jugadores SET dinero = dinero - Cantidad_Dinero WHERE nombre = Nombre_Jugador;
    UPDATE jugadores SET dinero = dinero + Cantidad_Dinero WHERE nombre = Nombre_JUgador_Receptor;
    INSERT INTO movimientos (accion) VALUES (CONCAT(Nombre_Jugador, ' pagó $', Cantidad_Dinero, ' a ', Nombre_Jugador_Receptor, ' por trato'));
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

CREATE DEFINER=`root`@`localhost` PROCEDURE `Recibir_Dinero_Vuelta` (IN `nombre_jugador` VARCHAR(30))   BEGIN
	IF (SELECT modo_exponencial FROM variables) = 0 THEN
	    UPDATE jugadores SET dinero = dinero + 200 WHERE nombre = nombre_jugador;
    	INSERT INTO movimientos (accion) VALUES (CONCAT(nombre_jugador, ' recibio $200 por dar una vuelta!'));
    ELSE
	    UPDATE jugadores SET dinero = dinero + 200 WHERE nombre = nombre_jugador;
    	INSERT INTO movimientos (accion) VALUES (CONCAT(nombre_jugador, ' recibio $200 por dar una vuelta!'));
    	IF (SELECT JUGADOR_MODERADOR FROM VARIABLES) = nombre_jugador THEN
	    	UPDATE VARIABLES SET multiplicador_exponencial = multiplicador_exponencial * 2;
    		INSERT INTO movimientos (accion) VALUES (CONCAT('Rentas ahora son x', (SELECT multiplicador_exponencial FROM variables)));
        END IF;
    END IF;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `Recibir_Dinero_Vuelta_Doble` (IN `Nombre_Jugador` VARCHAR(30))   BEGIN
	IF (SELECT modo_exponencial FROM variables) = 0 OR (SELECT modo_exponencial FROM variables) THEN
	    UPDATE jugadores SET dinero = dinero + 400 WHERE nombre = nombre_jugador;
    	INSERT INTO movimientos (accion) VALUES (CONCAT(nombre_jugador, ' recibio $400 por caer en salida!'));
    ELSE
	    UPDATE jugadores SET dinero = dinero + 400 WHERE nombre = nombre_jugador;
    	INSERT INTO movimientos (accion) VALUES (CONCAT(nombre_jugador, ' recibio $400 por caer en salida!'));
    	IF (SELECT JUGADOR_MODERADOR FROM VARIABLES) = nombre_jugador THEN
	    	UPDATE VARIABLES SET multiplicador_exponencial = multiplicador_exponencial * 3;
    		INSERT INTO movimientos (accion) VALUES (CONCAT('Rentas ahora son x', (SELECT multiplicador_exponencial FROM variables)));
        END IF;
    END IF;
END$$

CREATE DEFINER=`admin`@`localhost` PROCEDURE `Rendirse_Abandono` (IN `Nombre_Jugador` VARCHAR(30))   BEGIN
    UPDATE propiedades SET dueño = NULL where dueño = Nombre_Jugador;
    UPDATE jugadores SET dinero = 0, activo = 0 where nombre = Nombre_Jugador;
    INSERT INTO movimientos (accion) VALUES (CONCAT(Nombre_Jugador, ' se rindió y todo su dinero y propiedades pasan a ser del banco')); 
END$$

CREATE DEFINER=`admin`@`localhost` PROCEDURE `Rendirse_Compartir` (IN `Nombre_Jugador` VARCHAR(30))   BEGIN

SET NAMES 'utf8mb4';
SET @Nombre_Jugador = Nombre_Jugador;
SET @Dinero_Jugador = (SELECT dinero FROM jugadores WHERE nombre COLLATE utf8mb4_general_ci = @Nombre_Jugador COLLATE utf8mb4_general_ci);
SET @Dinero_Propiedades = IFNULL((SELECT SUM(hipoteca) FROM propiedades WHERE dueño COLLATE utf8mb4_general_ci = @Nombre_Jugador COLLATE utf8mb4_general_ci), 0);
SET @Dinero_Neto = @Dinero_Jugador + @Dinero_Propiedades;
SET @Numero_Jugadores_Activos = (SELECT count(*) - 1 FROM jugadores WHERE activo COLLATE latin1_general_ci = 1 COLLATE latin1_general_ci);
SET @Dinero_Para_Jugadores = FLOOR(@Dinero_Neto / @Numero_Jugadores_Activos);
#SELECT @Nombre_Jugador, @Dinero_Para_Jugadores;


	UPDATE jugadores set activo = 0 WHERE nombre = @Nombre_Jugador;
	INSERT INTO movimientos (accion) VALUES (CONCAT(Nombre_Jugador, ' se rindio, compartiendo ', @Dinero_Para_Jugadores, ' a todos los jugadores'));
	UPDATE jugadores SET dinero = dinero + @Dinero_Para_Jugadores WHERE activo = 1;
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

CREATE DEFINER=`root`@`localhost` PROCEDURE `Vender_Casa` (IN `Nombre_Propiedad` VARCHAR(30))   BEGIN
    UPDATE jugadores SET dinero = dinero + (SELECT costo_casa / 2 FROM propiedades WHERE nombre = Nombre_Propiedad) WHERE nombre = (SELECT dueño FROM propiedades WHERE nombre = Nombre_Propiedad);
	UPDATE propiedades SET nivel_renta = nivel_renta - 1 WHERE nombre = Nombre_Propiedad;
    INSERT INTO movimientos(ACCION) VALUES(CONCAT(Nombre_Propiedad, ' tiene una casa menos!'));

END$$

--
-- Funciones
--
CREATE DEFINER=`admin`@`localhost` FUNCTION `contarRegistros` () RETURNS INT(11)  BEGIN
    DECLARE count INT;
    SELECT COUNT(*) INTO count FROM nombre_tabla;
    RETURN count;
END$$

DELIMITER ;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `jugadores`
--

CREATE TABLE `jugadores` (
  `nombre` varchar(30) NOT NULL,
  `contraseña` varchar(50) NOT NULL,
  `dinero` int(11) NOT NULL,
  `pasiva` varchar(50) DEFAULT NULL,
  `turnos_restantes` int(2) DEFAULT NULL,
  `activo` tinyint(1) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

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
(1, 'Comienza el juego', '2023-05-17 21:05:38');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `pasivas`
--

CREATE TABLE `pasivas` (
  `id` int(2) NOT NULL,
  `nombre` varchar(50) NOT NULL,
  `descripcion` varchar(100) NOT NULL,
  `enfriamiento` int(2) NOT NULL,
  `extras` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `pasivas`
--

INSERT INTO `pasivas` (`id`, `nombre`, `descripcion`, `enfriamiento`, `extras`) VALUES
(1, 'Bonos', 'Obtener 100$.', 2, 'Puede se robado por otros jugadores1'),
(2, 'Cambio de roles', 'Cambiar la posición del token con otro jugador.', 3, 'El otro jugador no realiza ninguna acción, no afecta en el primer turno para la salida'),
(3, 'Compra ventajosa', 'Propiedades por mitad de precio', 0, 'Al ganar subasta tambíen se paga la mitad de lo establecido.'),
(4, 'Constructor', 'Se obtiene un casa gratis', 3, 'Se activa al obtener un grupo de color, pero se pueden acumular 2, no incluye hoteles.'),
(5, 'Dia de suerte', 'No pagar renta.', 5, 'Puede anular \'Bonanza\''),
(6, 'Doble recompensa', 'Duplicar dinero obtenido.', 3, 'Se puedee usar en \'parada libre\', entre otros, no aplica en rentas.'),
(7, 'Duelo', 'Ambos tiran los dados y el que pierde le paga 100$ al otro jugador.', 3, 'el jugador que usa la habilidad está con ventaja de de 3'),
(8, 'Inmunidad a impuestos', 'No pagar impuestos, bonos por grupos de color, y cartas de fortuna y arca comunal.', 0, 'no incluye renta de casas y hoteles.'),
(9, 'Movilidad', '+1 dado con 3 casillas en la jugada, se cuenta como dado adicional.', 3, 'Se puede usar con el dado veloz (dado rojo)'),
(10, 'Policia', 'Poder encarcelar a un jugador o encarcelarse a si mismo.', 4, 'No pagar por salida de la carcel, cobrar mientras está en la carcel (en caso de aplicar)'),
(11, 'Propiedades iniciales', '4 propiedades aleatorias gratis al comenzar.', 0, 'Se puede elegir una, pero se reduce el numero a 3 propiedades'),
(12, 'Rentabilidad Aumentada.', 'Al momento de cobrar renta se cobra como con 3 casas.', 4, 'El numero de casas adicional es fijo, se puede robar y evadir por otros jugadores'),
(13, 'Reposicionamiento', 'Mover el token a una casilla.', 5, 'Se debe realizar la acción de la misma (sin limites), no hay excepcion de casilla'),
(14, 'Saqueador', 'Robar una transacción', 4, 'No aplica al pagar renta propia, en la compra de una propiedad el que la compró recibe su propiedad.'),
(15, 'Señor de las cartas', 'Tomar carta y poder guardarla en secreto (max 2)', 2, 'Se puede dar a otro jugador.');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `propiedades`
--

CREATE TABLE `propiedades` (
  `id` int(11) NOT NULL,
  `nombre` varchar(30) NOT NULL,
  `color` varchar(20) NOT NULL,
  `precio` int(6) NOT NULL,
  `renta` int(4) DEFAULT NULL,
  `renta_grupo` int(4) DEFAULT NULL,
  `renta_1` int(4) DEFAULT NULL,
  `renta_2` int(4) DEFAULT NULL,
  `renta_3` int(4) DEFAULT NULL,
  `renta_4` int(4) DEFAULT NULL,
  `renta_5` int(4) DEFAULT NULL,
  `costo_casa` int(6) DEFAULT NULL,
  `hipoteca` int(6) NOT NULL,
  `costo_deshipoteca` int(6) NOT NULL,
  `dueño` varchar(30) DEFAULT NULL,
  `hipotecado` tinyint(1) NOT NULL DEFAULT 0,
  `nivel_renta` int(1) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `propiedades`
--

INSERT INTO `propiedades` (`id`, `nombre`, `color`, `precio`, `renta`, `renta_grupo`, `renta_1`, `renta_2`, `renta_3`, `renta_4`, `renta_5`, `costo_casa`, `hipoteca`, `costo_deshipoteca`, `dueño`, `hipotecado`, `nivel_renta`) VALUES
(1, 'Avenida Mediterraneo', 'Marron', 60, 2, 4, 10, 30, 90, 160, 250, 50, 30, 33, NULL, 0, 1),
(2, 'Avenida Baltica', 'Marron', 60, 4, 8, 20, 60, 180, 320, 450, 50, 30, 33, NULL, 0, 1),
(3, 'Ferrocarril de Reading', 'Negro', 200, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 100, 110, NULL, 0, 1),
(4, 'Avenida Oriental', 'Celeste', 100, 6, 12, 30, 90, 270, 400, 550, 50, 50, 55, NULL, 0, 1),
(5, 'Avenida Vermont', 'Celeste', 100, 6, 12, 30, 90, 270, 0, 550, 50, 50, 55, NULL, 0, 1),
(6, 'Avenida Connecticut', 'Celeste', 120, 6, 12, 40, 100, 300, 450, 600, 50, 60, 66, NULL, 0, 1),
(7, 'Plaza San Carlos', 'Morado', 140, 10, 20, 50, 150, 450, 625, 750, 100, 70, 77, NULL, 0, 1),
(8, 'Compañía de Electricidad', 'Servicio', 150, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 75, 83, NULL, 0, 1),
(9, 'Avenida Estados', 'Morado', 140, 10, 20, 50, 150, 450, 625, 750, 100, 70, 77, NULL, 0, 1),
(10, 'Avenida Virginia', 'Morado', 160, 12, 24, 60, 180, 500, 500, 700, 100, 80, 88, NULL, 0, 1),
(11, 'Ferrocarril Pensilvania', 'Negro', 200, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 100, 110, NULL, 0, 1),
(12, 'Avenida San James', 'Naranja', 180, 14, 28, 70, 200, 550, 750, 950, 100, 90, 99, NULL, 0, 1),
(13, 'Avenida Tennessee', 'Naranja', 180, 14, 28, 70, 20, 550, 750, 950, 100, 90, 99, NULL, 0, 1),
(14, 'Avenida Nueva York', 'Naranja', 200, 16, 32, 80, 220, 600, 800, 1000, 100, 100, 110, NULL, 0, 1),
(15, 'Avenida Kentucky', 'Rojo', 220, 18, 36, 90, 250, 700, 875, 1050, 150, 110, 110, NULL, 0, 1),
(16, 'Avenida Indiana', 'Rojo', 220, 18, 36, 90, 250, 700, 875, 1050, 150, 110, 110, NULL, 0, 1),
(17, 'Avenida Illinois', 'Rojo', 240, 20, 40, 100, 300, 750, 925, 1100, 150, 120, 142, NULL, 0, 1),
(18, 'Ferrocarril B&O', 'Negro', 200, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 100, 110, NULL, 0, 1),
(19, 'Avenida Atlantico', 'Amarillo', 260, 22, 44, 110, 330, 800, 975, 1150, 150, 130, 143, NULL, 0, 1),
(20, 'Avenida Ventnor', 'Amarillo', 260, 22, 44, 110, 330, 800, 975, 1150, 150, 130, 143, NULL, 0, 1),
(21, 'Compañía de Agua', 'Servicio', 150, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 75, 83, NULL, 0, 1),
(22, 'Jardines Marvin', 'Amarillo', 280, 24, 48, 120, 360, 850, 1025, 1200, 150, 140, 154, NULL, 0, 1),
(23, 'Avenida Pacifico', 'Verde', 300, 26, 52, 130, 390, 900, 1100, 1275, 200, 150, 165, NULL, 0, 1),
(24, 'Avenida Carolina del Norte', 'Verde', 300, 26, 52, 130, 390, 900, 1100, 1275, 200, 150, 165, NULL, 0, 1),
(25, 'Avenida Pensilvania', 'Verde', 320, 28, 56, 150, 450, 1000, 1200, 1400, 200, 160, 175, NULL, 0, 1),
(26, 'Ferrocarril Via Rápida', 'Negro', 200, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 100, 110, NULL, 0, 1),
(27, 'Plaza Park', 'Azul', 350, 35, 70, 175, 500, 1100, 1300, 1500, 200, 175, 193, NULL, 0, 1),
(28, 'El Muelle', 'Azul', 400, 50, 100, 200, 600, 1400, 1700, 2000, 200, 200, 220, NULL, 0, 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `variables`
--

CREATE TABLE `variables` (
  `impuestos_para_parada_libre` tinyint(1) NOT NULL DEFAULT 0,
  `acomulado_parada_libre` int(5) DEFAULT NULL,
  `dinero_inicio_personalizado` tinyint(1) NOT NULL DEFAULT 0,
  `dinero_inicio` int(5) NOT NULL DEFAULT 1500,
  `bono_salida` tinyint(1) NOT NULL DEFAULT 0,
  `pasivas_activas` tinyint(1) NOT NULL DEFAULT 0,
  `modo_exponencial` tinyint(1) NOT NULL DEFAULT 0,
  `jugador_moderador` varchar(30) DEFAULT NULL,
  `multiplicador_exponencial` int(4) NOT NULL DEFAULT 1,
  `tratos_con_propiedades_disponibles` tinyint(1) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `variables`
--

INSERT INTO `variables` (`impuestos_para_parada_libre`, `acomulado_parada_libre`, `dinero_inicio_personalizado`, `dinero_inicio`, `bono_salida`, `pasivas_activas`, `modo_exponencial`, `jugador_moderador`, `multiplicador_exponencial`, `tratos_con_propiedades_disponibles`) VALUES
(0, 0, 0, 1500, 0, 0, 0, NULL, 1, 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `version`
--

CREATE TABLE `version` (
  `version` varchar(50) NOT NULL,
  `txt` longtext DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `version`
--

INSERT INTO `version` (`version`, `txt`) VALUES
('0.1', '-- phpMyAdmin SQL Dump\r\n-- version 5.2.1\r\n-- https://www.phpmyadmin.net/\r\n--\r\n-- Servidor: 127.0.0.1\r\n-- Tiempo de generación: 14-05-2023 a las 23:16:25\r\n-- Versión del servidor: 10.4.28-MariaDB\r\n-- Versión de PHP: 8.2.4\r\n\r\nSET SQL_MODE = \"NO_AUTO_VALUE_ON_ZERO\";\r\nSTART TRANSACTION;\r\nSET time_zone = \"+00:00\";\r\n\r\n\r\n/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;\r\n/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;\r\n/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;\r\n/*!40101 SET NAMES utf8mb4 */;\r\n\r\n--\r\n-- Base de datos: `monopolios`\r\n--\r\n\r\nDELIMITER $$\r\n--\r\n-- Procedimientos\r\n--\r\nCREATE DEFINER=`root`@`localhost` PROCEDURE `Comprar_Casa` (IN `Nombre_Propiedad` VARCHAR(30))   BEGIN\r\n    UPDATE jugadores SET dinero = dinero - (SELECT costo_casa FROM propiedades WHERE nombre = Nombre_Propiedad) WHERE nombre = (SELECT dueño FROM propiedades WHERE nombre = Nombre_Propiedad);\r\n	UPDATE propiedades SET nivel_renta = nivel_renta + 1 WHERE nombre = Nombre_Propiedad;\r\n    INSERT INTO movimientos(ACCION) VALUES(CONCAT(Nombre_Propiedad, \' tiene una casa mas!\'));\r\n\r\nEND$$\r\n\r\nCREATE DEFINER=`admin`@`localhost` PROCEDURE `Comprar_Propiedad` (IN `nombre_jugador` VARCHAR(30), IN `vdinero_jugador` INT(6), IN `nombre_propiedad` VARCHAR(30), IN `vcosto_propiedad` INT(6))   BEGIN\r\n    IF vdinero_jugador >= vcosto_propiedad THEN\r\n        UPDATE propiedades SET dueño = nombre_jugador WHERE nombre = nombre_propiedad;\r\n        UPDATE jugadores SET dinero = dinero - vcosto_propiedad WHERE nombre = nombre_jugador;\r\n        INSERT INTO movimientos (accion) VALUES (concat(nombre_jugador, \' compró \', nombre_propiedad));\r\n    END IF;\r\nEND$$\r\n\r\nCREATE DEFINER=`root`@`localhost` PROCEDURE `Consultar_Dinero_Neto` (IN `Nombre_Jugador` VARCHAR(30))   SELECT (SELECT dinero FROM jugadores WHERE nombre COLLATE utf8mb4_general_ci = Nombre_Jugador COLLATE utf8mb4_general_ci) + \r\n(IFNULL((SELECT SUM(hipoteca) FROM propiedades WHERE dueño COLLATE utf8mb4_general_ci = Nombre_Jugador COLLATE utf8mb4_general_ci AND hipotecado = 0), 0))$$\r\n\r\nCREATE DEFINER=`admin`@`localhost` PROCEDURE `Crear_Jugador` (IN `vnombre` VARCHAR(30), IN `vpass` VARCHAR(50), IN `vdinero` INT(6), IN `vpasiva` VARCHAR(50))  COMMENT \'agregar un jugador y asignarle pasiva\' BEGIN\r\n    IF vnombre = \'\' OR vpass = \'\' THEN\r\n        SIGNAL SQLSTATE \'45000\' SET MESSAGE_TEXT = \'Nombre y contraseña son obligatorios\';\r\n    ELSE\r\n        IF vpasiva <> \'\' THEN\r\n            INSERT INTO jugadores (nombre, contraseña, dinero, pasiva, turnos_restantes) \r\n            VALUES (vnombre, vpass, vdinero, vpasiva, 0);\r\n            INSERT INTO movimientos (ACCION) \r\n            VALUES (CONCAT(vnombre, \' se unió, Dinero: $\', vdinero, \' Pasiva: \', vpasiva));\r\n        ELSE\r\n            INSERT INTO jugadores (nombre, contraseña, dinero, pasiva, turnos_restantes) \r\n            VALUES (vnombre, vpass, vdinero, vpasiva, 0);\r\n            INSERT INTO movimientos (ACCION) \r\n            VALUES (CONCAT(vnombre, \' se unió, Dinero: $\', vdinero));\r\n        END IF;\r\n    END IF;\r\nEND$$\r\n\r\nCREATE DEFINER=`admin`@`localhost` PROCEDURE `Hipotecar_Propiedad` (IN `Nombre_Propiedad` VARCHAR(30))   BEGIN\r\n    UPDATE propiedades SET hipotecado = 1 where nombre = Nombre_Propiedad;\r\n    UPDATE jugadores SET dinero = dinero + (SELECT hipoteca FROM propiedades WHERE nombre = Nombre_Propiedad);\r\n    INSERT INTO movimientos (accion) VALUES (CONCAT((SELECT dueño FROM propiedades WHERE nombre = Nombre_Propiedad), \' hipoteco \', Nombre_Propiedad));\r\nEND$$\r\n\r\nCREATE DEFINER=`admin`@`localhost` PROCEDURE `Nuevo_Juego` (IN `v_impuestos_para_parada_libre` BOOLEAN, IN `v_dinero_inicio_personaliazdo` BOOLEAN, IN `v_dinero_inicio` INT, IN `v_bono_salida` BOOLEAN, IN `v_pasivas_activas` BOOLEAN, IN `v_modo_exponencial` BOOLEAN, IN `v_jugador_moderador` VARCHAR(30))   BEGIN\r\n    TRUNCATE TABLE jugadores;\r\n    TRUNCATE TABLE MOVIMIENTOS;\r\n    SELECT \'Limpiadas tablas de jugadores y movimientos\' AS COMPLETADO;\r\n    INSERT INTO movimientos (accion) VALUES (\'Comienza el juego\'); \r\n    UPDATE propiedades SET dueño = NULL, hipotecado = 0, nivel_renta = 1;\r\n    UPDATE variables SET impuestos_para_parada_libre = v_impuestos_para_parada_libre, dinero_inicio_personalizado = v_dinero_inicio_personaliazdo, dinero_inicio = v_dinero_inicio, acomulado_parada_libre = 0, bono_salida = v_bono_salida, pasivas_activas = v_pasivas_activas, modo_exponencial = v_modo_exponencial, jugador_moderador = v_jugador_moderador, multiplicador_exponencial = 1;\r\nEND$$\r\n\r\nCREATE DEFINER=`root`@`localhost` PROCEDURE `Pagar_A_Banco` (IN `Nombre_Jugador` VARCHAR(30), IN `Monto_A_Pagar` INT(6))   BEGIN\r\n	UPDATE jugadores SET DINERO = DINERO - Monto_A_Pagar WHERE nombre = Nombre_Jugador;\r\n    INSERT INTO movimientos (accion) VALUES (CONCAT(Nombre_Jugador, \' pago \', Monto_A_Pagar, \' al banco\'));\r\nEND$$\r\n\r\nCREATE DEFINER=`admin`@`localhost` PROCEDURE `Pagar_A_Jugador` (IN `jugador1` VARCHAR(50), IN `jugador2` VARCHAR(50), IN `monto` INT(6))  COMMENT \'Función para pagar jugador A x monto a jugador B\' BEGIN\r\n    UPDATE jugadores SET DINERO = DINERO - monto WHERE nombre = jugador1;\r\n    UPDATE jugadores SET DINERO = DINERO + monto WHERE nombre = jugador2;\r\n    INSERT INTO movimientos (accion) VALUES (CONCAT(jugador1, \' pagó $\', monto, \' a \', jugador2));\r\nEND$$\r\n\r\nCREATE DEFINER=`root`@`localhost` PROCEDURE `Pagar_Carcel` (IN `Nombre_Jugador` VARCHAR(30))   BEGIN\r\n	UPDATE jugadores SET dinero = dinero - 50 WHERE nombre = Nombre_Jugador;\r\n    INSERT INTO movimientos (accion) VALUES (CONCAT(Nombre_Jugador, \' pago salida de carcel\')); \r\nEND$$\r\n\r\nCREATE DEFINER=`root`@`localhost` PROCEDURE `Pagar_impuestos` (IN `Nombre_Jugador` VARCHAR(30), IN `Monto_A_Pagar` INT(6), IN `Impuestos_Para_Parada_Libre` BOOLEAN)   BEGIN\r\n	IF Impuestos_Para_Parada_libre = 1 THEN\r\n        UPDATE jugadores SET dinero = dinero - Monto_A_Pagar where nombre = Nombre_Jugador;\r\n        UPDATE variables SET acomiulado_parada_libre = acomulado_parada_libre + Monto_A_Pagar;\r\n        INSERT INTO movimientos (accion) VALUES (CONCAT(Nombre_Jugador, \' sumó \', Monto_A_Pagar, \' a parada libre\'));\r\n        INSERT INTO movimientos (accion) VALUES (CONCAT(\'Premio parada libre: \', (SELECT parada_libre FROM variables)));\r\n    ELSE\r\n        UPDATE jugadores SET dinero = dinero - Monto_A_Pagar where nombre = Nombre_Jugador;\r\n        INSERT INTO movimientos (accion) VALUES (CONCAT(Nombre_Jugador, \' pagó \', Monto_A_Pagar, \' de impuestos\'));\r\n    END IF;\r\nEND$$\r\n\r\nCREATE DEFINER=`root`@`localhost` PROCEDURE `Pago_A_Banco` (IN `nombre_jugador` VARCHAR(30), IN `monto_a_pagar` INT(6), IN `razón` VARCHAR(30))   BEGIN\r\n    IF razon = \'carcel\' THEN\r\n        UPDATE jugadores SET dinero = dinero - 50 where nombre = nombre_jugador;\r\n        INSERT INTO movimientos (accion) VALUES (CONCAT(nombre_jugador, \' pagó salida de la carcel\'));\r\n    ELSE\r\n        UPDATE jugadores SET dinero = dinero - monto_a_pagar where nombre = nombre_jugador;\r\n        INSERT INTO movimientos (accion) VALUES (CONCAT(nombre_jugador, \' pagó al banco \', monto_a_pagar, \' por \', razon));\r\n    END IF;\r\nEND$$\r\n\r\nCREATE DEFINER=`root`@`localhost` PROCEDURE `Recibir_Dinero_Banco` (IN `v1` VARCHAR(30), IN `v2` INT(6), IN `v3` VARCHAR(20))   BEGIN\r\n    UPDATE jugadores SET dinero = dinero + v2 WHERE nombre = v1;\r\n    INSERT INTO movimientos (accion) VALUES (CONCAT(v1, \' recibio \', v2, \' del banco  por \', v3));\r\nEND$$\r\n\r\nCREATE DEFINER=`root`@`localhost` PROCEDURE `Recibir_Dinero_Vuelta` (IN `nombre_jugador` VARCHAR(30))   BEGIN\r\n	IF (SELECT modo_exponencial FROM variables) = 0 THEN\r\n	    UPDATE jugadores SET dinero = dinero + 200 WHERE nombre = nombre_jugador;\r\n    	INSERT INTO movimientos (accion) VALUES (CONCAT(nombre_jugador, \' recibio $200 por dar una vuelta!\'));\r\n    ELSE\r\n	    UPDATE jugadores SET dinero = dinero + 200 WHERE nombre = nombre_jugador;\r\n    	INSERT INTO movimientos (accion) VALUES (CONCAT(nombre_jugador, \' recibio $200 por dar una vuelta!\'));\r\n    	IF (SELECT JUGADOR_MODERADOR FROM VARIABLES) = nombre_jugador THEN\r\n	    	UPDATE VARIABLES SET multiplicador_exponencial = multiplicador_exponencial * 2;\r\n    		INSERT INTO movimientos (accion) VALUES (CONCAT(\'Rentas ahora son x\', (SELECT multiplicador_exponencial FROM variables)));\r\n        END IF;\r\n    END IF;\r\nEND$$\r\n\r\nCREATE DEFINER=`root`@`localhost` PROCEDURE `Recibir_Dinero_Vuelta_Doble` (IN `Nombre_Jugador` VARCHAR(30))   BEGIN \r\n    UPDATE jugadores SET dinero = dinero + 400 WHERE nombre = Nombre_Jugador;\r\n    INSERT INTO MOVIMIENTOS(ACCION) VALUES(CONCAT(Nombre_Jugador, \' recibio $400 por vuelta doble!\'));\r\nEND$$\r\n\r\nCREATE DEFINER=`admin`@`localhost` PROCEDURE `Rendirse_Abandono` (IN `Nombre_Jugador` VARCHAR(30))   BEGIN\r\n    UPDATE propiedades SET dueño = NULL where dueño = Nombre_Jugador;\r\n    UPDATE jugadores SET dinero = 0, activo = 0 where nombre = Nombre_Jugador;\r\n    INSERT INTO movimientos (accion) VALUES (CONCAT(Nombre_Jugador, \' se rindió y todo su dinero y propiedades pasan a ser del banco\')); \r\nEND$$\r\n\r\nCREATE DEFINER=`admin`@`localhost` PROCEDURE `Rendirse_Compartir` (IN `Nombre_Jugador` VARCHAR(30))   BEGIN\r\n\r\nSET NAMES \'utf8mb4\';\r\nSET @Nombre_Jugador = Nombre_Jugador;\r\nSET @Dinero_Jugador = (SELECT dinero FROM jugadores WHERE nombre COLLATE utf8mb4_general_ci = @Nombre_Jugador COLLATE utf8mb4_general_ci);\r\nSET @Dinero_Propiedades = IFNULL((SELECT SUM(hipoteca) FROM propiedades WHERE dueño COLLATE utf8mb4_general_ci = @Nombre_Jugador COLLATE utf8mb4_general_ci), 0);\r\nSET @Dinero_Neto = @Dinero_Jugador + @Dinero_Propiedades;\r\nSET @Numero_Jugadores_Activos = (SELECT count(*) - 1 FROM jugadores WHERE activo COLLATE latin1_general_ci = 1 COLLATE latin1_general_ci);\r\nSET @Dinero_Para_Jugadores = FLOOR(@Dinero_Neto / @Numero_Jugadores_Activos);\r\n#SELECT @Nombre_Jugador, @Dinero_Para_Jugadores;\r\n\r\n\r\n	UPDATE jugadores set activo = 0 WHERE nombre = @Nombre_Jugador;\r\n	INSERT INTO movimientos (accion) VALUES (CONCAT(Nombre_Jugador, \' se rindio, compartiendo \', @Dinero_Para_Jugadores, \' a todos los jugadores\'));\r\n	UPDATE jugadores SET dinero = dinero + @Dinero_Para_Jugadores WHERE activo = 1;\r\n	UPDATE jugadores SET dinero = 0 WHERE nombre = Nombre_Jugador;\r\n	UPDATE propiedades SET dueño = NULL, hipotecado = 0 WHERE dueño = Nombre_Jugador;\r\n\r\nEND$$\r\n\r\nCREATE DEFINER=`admin`@`localhost` PROCEDURE `Tirar_Dado` (IN `jugador` VARCHAR(50))  COMMENT \'restar 1 al enfriamiento de la habilidad del jugador\' BEGIN\r\n    IF ((SELECT turnos_restantes FROM jugadores WHERE nombre = jugador) > 0) THEN\r\n        UPDATE jugadores SET turnos_restantes = turnos_restantes - 1 WHERE nombre = jugador;\r\n        INSERT INTO movimientos (ACCION) VALUES(CONCAT(JUGADOR, \' tiró los dados, \', (SELECT turnos_restantes FROM jugadores where nombre = jugador) ,\' turnos restantes\'));\r\n    ELSE\r\n        INSERT INTO movimientos (ACCION) VALUES(CONCAT(JUGADOR, \' tiró los dados, \', (SELECT turnos_restantes FROM jugadores where nombre = jugador) ,\' turnos restantes\'));\r\n    END IF;\r\nEND$$\r\n\r\nCREATE DEFINER=`admin`@`localhost` PROCEDURE `Usar_Pasiva` (IN `jugador` VARCHAR(50))   BEGIN\r\n  IF (SELECT turnos_restantes FROM jugadores WHERE nombre = jugador) = 0 THEN\r\n    UPDATE jugadores SET turnos_restantes = (SELECT pasivas.enfriamiento FROM pasivas INNER JOIN jugadores ON pasivas.nombre = jugadores.pasiva WHERE jugadores.nombre = jugador) WHERE nombre = jugador;\r\n    INSERT INTO movimientos (ACCION) VALUES (CONCAT(jugador, \' usó \', (SELECT pasiva FROM jugadores WHERE nombre = jugador)));\r\n  END IF;\r\nEND$$\r\n\r\nCREATE DEFINER=`admin`@`localhost` PROCEDURE `validar_usuario` (IN `vnombre` VARCHAR(30), IN `vpass` VARCHAR(50))   SELECT count(*) FROM jugadores where nombre = vnombre AND contraseña = vpass$$\r\n\r\nCREATE DEFINER=`root`@`localhost` PROCEDURE `Vender_Casa` (IN `Nombre_Propiedad` VARCHAR(30))   BEGIN\r\n    UPDATE jugadores SET dinero = dinero + (SELECT costo_casa / 2 FROM propiedades WHERE nombre = Nombre_Propiedad) WHERE nombre = (SELECT dueño FROM propiedades WHERE nombre = Nombre_Propiedad);\r\n	UPDATE propiedades SET nivel_renta = nivel_renta - 1 WHERE nombre = Nombre_Propiedad;\r\n    INSERT INTO movimientos(ACCION) VALUES(CONCAT(Nombre_Propiedad, \' tiene una casa menos!\'));\r\n\r\nEND$$\r\n\r\nDELIMITER ;\r\n\r\n-- --------------------------------------------------------\r\n\r\n--\r\n-- Estructura de tabla para la tabla `jugadores`\r\n--\r\n\r\nCREATE TABLE `jugadores` (\r\n  `nombre` varchar(30) NOT NULL,\r\n  `contraseña` varchar(50) NOT NULL,\r\n  `dinero` int(11) NOT NULL,\r\n  `pasiva` varchar(50) DEFAULT NULL,\r\n  `turnos_restantes` int(2) DEFAULT NULL,\r\n  `activo` tinyint(1) NOT NULL DEFAULT 1\r\n) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;\r\n\r\n--\r\n-- Volcado de datos para la tabla `jugadores`\r\n--\r\n\r\nINSERT INTO `jugadores` (`nombre`, `contraseña`, `dinero`, `pasiva`, `turnos_restantes`, `activo`) VALUES\r\n(\'gato\', \'gato\', 1364, NULL, 0, 1),\r\n(\'polo\', \'gato\', 1196, NULL, 0, 1);\r\n\r\n-- --------------------------------------------------------\r\n\r\n--\r\n-- Estructura de tabla para la tabla `movimientos`\r\n--\r\n\r\nCREATE TABLE `movimientos` (\r\n  `id` int(11) NOT NULL,\r\n  `accion` varchar(100) NOT NULL,\r\n  `tiempo` datetime NOT NULL DEFAULT current_timestamp()\r\n) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;\r\n\r\n--\r\n-- Volcado de datos para la tabla `movimientos`\r\n--\r\n\r\nINSERT INTO `movimientos` (`id`, `accion`, `tiempo`) VALUES\r\n(1, \'Comienza el juego\', \'2023-05-14 14:07:37\'),\r\n(2, \'gato se unió, Dinero: $1500\', \'2023-05-14 14:07:37\'),\r\n(3, \'polo se unió, Dinero: $1500\', \'2023-05-14 14:07:45\'),\r\n(4, \'Rentas ahora son x2\', \'2023-05-14 14:07:55\'),\r\n(5, \'Rentas ahora son x4\', \'2023-05-14 14:09:22\'),\r\n(6, \'Rentas ahora son x8\', \'2023-05-14 14:10:03\'),\r\n(7, \'Rentas ahora son x16\', \'2023-05-14 14:15:15\'),\r\n(8, \'polo recibio $200 por dar una vuelta!\', \'2023-05-14 14:16:22\'),\r\n(9, \'polo recibio $200 por dar una vuelta!\', \'2023-05-14 14:16:25\'),\r\n(10, \'gato recibio $200 por dar una vuelta!\', \'2023-05-14 14:16:31\'),\r\n(11, \'Rentas ahora son x32\', \'2023-05-14 14:16:31\'),\r\n(12, \'polo compró Avenida Mediterraneo dinero: 1840\', \'2023-05-14 14:27:02\'),\r\n(13, \'polo compró Avenida Baltica dinero: 1780\', \'2023-05-14 14:27:04\'),\r\n(14, \'polo compró Ferrocarril de Reading dinero: 1580\', \'2023-05-14 14:27:06\'),\r\n(15, \'polo compró Avenida Oriental dinero: 1480\', \'2023-05-14 14:27:22\'),\r\n(16, \'polo compró Compañía de Electricidad dinero: 1330\', \'2023-05-14 14:27:27\'),\r\n(17, \'gato pagó $2 a polo\', \'2023-05-14 14:59:02\'),\r\n(18, \'gato pagó $64 a polo\', \'2023-05-14 15:00:48\'),\r\n(19, \'polo compró Ferrocarril Pensilvania dinero: 1196\', \'2023-05-14 15:03:20\'),\r\n(20, \'gato compró Avenida Vermont dinero: 1534\', \'2023-05-14 15:04:20\'),\r\n(21, \'Avenida Vermont tiene una casa mas!\', \'2023-05-14 15:04:24\'),\r\n(22, \'Avenida Vermont tiene una casa mas!\', \'2023-05-14 15:04:27\'),\r\n(23, \'gato compró Avenida Connecticut\', \'2023-05-14 15:04:59\'),\r\n(24, \'Avenida Vermont tiene una casa menos!\', \'2023-05-14 15:05:18\'),\r\n(25, \'Avenida Vermont tiene una casa menos!\', \'2023-05-14 15:05:20\');\r\n\r\n-- --------------------------------------------------------\r\n\r\n--\r\n-- Estructura de tabla para la tabla `pasivas`\r\n--\r\n\r\nCREATE TABLE `pasivas` (\r\n  `id` int(2) NOT NULL,\r\n  `nombre` varchar(50) NOT NULL,\r\n  `descripcion` varchar(100) NOT NULL,\r\n  `enfriamiento` int(2) NOT NULL,\r\n  `extras` varchar(100) NOT NULL\r\n) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;\r\n\r\n--\r\n-- Volcado de datos para la tabla `pasivas`\r\n--\r\n\r\nINSERT INTO `pasivas` (`id`, `nombre`, `descripcion`, `enfriamiento`, `extras`) VALUES\r\n(1, \'Bonos\', \'Obtener 100$.\', 2, \'Puede se robado por otros jugadores1\'),\r\n(2, \'Cambio de roles\', \'Cambiar la posición del token con otro jugador.\', 3, \'El otro jugador no realiza ninguna acción, no afecta en el primer turno para la salida\'),\r\n(3, \'Compra ventajosa\', \'Propiedades por mitad de precio\', 0, \'Al ganar subasta tambíen se paga la mitad de lo establecido.\'),\r\n(4, \'Constructor\', \'Se obtiene un casa gratis\', 3, \'Se activa al obtener un grupo de color, pero se pueden acumular 2, no incluye hoteles.\'),\r\n(5, \'Dia de suerte\', \'No pagar renta.\', 5, \'Puede anular \\\'Bonanza\\\'\'),\r\n(6, \'Doble recompensa\', \'Duplicar dinero obtenido.\', 3, \'Se puedee usar en \\\'parada libre\\\', entre otros, no aplica en rentas.\'),\r\n(7, \'Duelo\', \'Ambos tiran los dados y el que pierde le paga 100$ al otro jugador.\', 3, \'el jugador que usa la habilidad está con ventaja de de 3\'),\r\n(8, \'Inmunidad a impuestos\', \'No pagar impuestos, bonos por grupos de color, y cartas de fortuna y arca comunal.\', 0, \'no incluye renta de casas y hoteles.\'),\r\n(9, \'Movilidad\', \'+1 dado con 3 casillas en la jugada, se cuenta como dado adicional.\', 3, \'Se puede usar con el dado veloz (dado rojo)\'),\r\n(10, \'Policia\', \'Poder encarcelar a un jugador o encarcelarse a si mismo.\', 4, \'No pagar por salida de la carcel, cobrar mientras está en la carcel (en caso de aplicar)\'),\r\n(11, \'Propiedades iniciales\', \'4 propiedades aleatorias gratis al comenzar.\', 0, \'Se puede elegir una, pero se reduce el numero a 3 propiedades\'),\r\n(12, \'Rentabilidad Aumentada.\', \'Al momento de cobrar renta se cobra como con 3 casas.\', 4, \'El numero de casas adicional es fijo, se puede robar y evadir por otros jugadores\'),\r\n(13, \'Reposicionamiento\', \'Mover el token a una casilla.\', 5, \'Se debe realizar la acción de la misma (sin limites), no hay excepcion de casilla\'),\r\n(14, \'Saqueador\', \'Robar una transacción\', 4, \'No aplica al pagar renta propia, en la compra de una propiedad el que la compró recibe su propiedad.\'),\r\n(15, \'Señor de las cartas\', \'Tomar carta y poder guardarla en secreto (max 2)\', 2, \'Se puede dar a otro jugador.\');\r\n\r\n-- --------------------------------------------------------\r\n\r\n--\r\n-- Estructura de tabla para la tabla `propiedades`\r\n--\r\n\r\nCREATE TABLE `propiedades` (\r\n  `id` int(11) NOT NULL,\r\n  `nombre` varchar(30) NOT NULL,\r\n  `color` varchar(20) NOT NULL,\r\n  `precio` int(6) NOT NULL,\r\n  `renta` int(4) NOT NULL,\r\n  `renta_grupo` int(4) NOT NULL,\r\n  `renta_1` int(4) NOT NULL,\r\n  `renta_2` int(4) NOT NULL,\r\n  `renta_3` int(4) NOT NULL,\r\n  `renta_4` int(4) NOT NULL,\r\n  `renta_5` int(4) NOT NULL,\r\n  `costo_casa` int(6) DEFAULT NULL,\r\n  `hipoteca` int(6) NOT NULL,\r\n  `costo_deshipoteca` int(6) NOT NULL,\r\n  `dueño` varchar(30) DEFAULT NULL,\r\n  `hipotecado` tinyint(1) NOT NULL DEFAULT 0,\r\n  `nivel_renta` int(1) NOT NULL DEFAULT 1\r\n) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;\r\n\r\n--\r\n-- Volcado de datos para la tabla `propiedades`\r\n--\r\n\r\nINSERT INTO `propiedades` (`id`, `nombre`, `color`, `precio`, `renta`, `renta_grupo`, `renta_1`, `renta_2`, `renta_3`, `renta_4`, `renta_5`, `costo_casa`, `hipoteca`, `costo_deshipoteca`, `dueño`, `hipotecado`, `nivel_renta`) VALUES\r\n(1, \'Avenida Mediterraneo\', \'Marron\', 60, 2, 0, 0, 0, 0, 0, 0, 50, 30, 33, \'polo\', 0, 1),\r\n(2, \'Avenida Baltica\', \'Marron\', 60, 4, 0, 0, 0, 0, 0, 0, 50, 30, 33, \'polo\', 0, 1),\r\n(3, \'Ferrocarril de Reading\', \'Negro\', 200, 6, 0, 0, 0, 0, 0, 0, NULL, 100, 110, \'polo\', 0, 1),\r\n(4, \'Avenida Oriental\', \'Celeste\', 100, 6, 0, 0, 0, 0, 0, 0, 50, 50, 55, \'polo\', 0, 1),\r\n(5, \'Avenida Vermont\', \'Celeste\', 100, 8, 0, 0, 0, 0, 0, 0, 50, 50, 55, \'gato\', 0, 1),\r\n(6, \'Avenida Connecticut\', \'Celeste\', 120, 10, 0, 0, 0, 0, 0, 0, 50, 60, 66, \'gato\', 0, 1),\r\n(7, \'Plaza San Carlos\', \'Morado\', 140, 10, 0, 0, 0, 0, 0, 0, 100, 70, 77, NULL, 0, 1),\r\n(8, \'Compañía de Electricidad\', \'Servicio\', 150, 1, 0, 0, 0, 0, 0, 0, NULL, 75, 83, \'polo\', 0, 1),\r\n(9, \'Avenida Estados\', \'Morado\', 140, 0, 0, 0, 0, 0, 0, 0, 100, 70, 77, NULL, 0, 1),\r\n(10, \'Avenida Virginia\', \'Morado\', 160, 0, 0, 0, 0, 0, 0, 0, 100, 80, 88, NULL, 0, 1),\r\n(11, \'Ferrocarril Pensilvania\', \'Negro\', 200, 0, 0, 0, 0, 0, 0, 0, NULL, 100, 110, \'polo\', 0, 1),\r\n(12, \'Avenida San James\', \'Naranja\', 180, 0, 0, 0, 0, 0, 0, 0, 100, 90, 99, NULL, 0, 1),\r\n(13, \'Avenida Tennessee\', \'Naranja\', 180, 0, 0, 0, 0, 0, 0, 0, 100, 90, 99, NULL, 0, 1),\r\n(14, \'Avenida Nueva York\', \'Naranja\', 200, 0, 0, 0, 0, 0, 0, 0, 100, 100, 110, NULL, 0, 1),\r\n(15, \'Avenida Kentucky\', \'Rojo\', 220, 0, 0, 0, 0, 0, 0, 0, 150, 110, 110, NULL, 0, 1),\r\n(16, \'Avenida Indiana\', \'Rojo\', 220, 0, 0, 0, 0, 0, 0, 0, 150, 110, 110, NULL, 0, 1),\r\n(17, \'Avenida Illinois\', \'Rojo\', 240, 0, 0, 0, 0, 0, 0, 0, 150, 120, 142, NULL, 0, 1),\r\n(18, \'Ferrocarril B&O\', \'Negro\', 200, 0, 0, 0, 0, 0, 0, 0, NULL, 100, 110, NULL, 0, 1),\r\n(19, \'Avenida Atlantico\', \'Amarillo\', 260, 0, 0, 0, 0, 0, 0, 0, 150, 130, 143, NULL, 0, 1),\r\n(20, \'Avenida Ventnor\', \'Amarillo\', 260, 0, 0, 0, 0, 0, 0, 0, 150, 130, 143, NULL, 0, 1),\r\n(21, \'Compañía de Agua\', \'Servicio\', 150, 0, 0, 0, 0, 0, 0, 0, NULL, 75, 83, NULL, 0, 1),\r\n(22, \'Jardines Marvin\', \'Amarillo\', 280, 0, 0, 0, 0, 0, 0, 0, 150, 140, 154, NULL, 0, 1),\r\n(23, \'Avenida Pacifico\', \'Verde\', 300, 0, 0, 0, 0, 0, 0, 0, 200, 150, 165, NULL, 0, 1),\r\n(24, \'Avenida Carolina del Norte\', \'Verde\', 300, 0, 0, 0, 0, 0, 0, 0, 200, 150, 165, NULL, 0, 1),\r\n(25, \'Avenida Pensilvania\', \'Verde\', 320, 0, 0, 0, 0, 0, 0, 0, 200, 160, 175, NULL, 0, 1),\r\n(26, \'Ferrocarril Via Rápida\', \'Negro\', 200, 0, 0, 0, 0, 0, 0, 0, NULL, 100, 110, NULL, 0, 1),\r\n(27, \'Plaza Park\', \'Azul\', 350, 0, 0, 0, 0, 0, 0, 0, 200, 175, 193, NULL, 0, 1),\r\n(28, \'El Muelle\', \'Azul\', 400, 0, 0, 0, 0, 0, 0, 0, 200, 200, 220, NULL, 0, 1);\r\n\r\n-- --------------------------------------------------------\r\n\r\n--\r\n-- Estructura de tabla para la tabla `variables`\r\n--\r\n\r\nCREATE TABLE `variables` (\r\n  `impuestos_para_parada_libre` tinyint(1) NOT NULL DEFAULT 0,\r\n  `acomulado_parada_libre` int(5) DEFAULT NULL,\r\n  `dinero_inicio_personalizado` tinyint(1) NOT NULL DEFAULT 0,\r\n  `dinero_inicio` int(5) NOT NULL DEFAULT 1500,\r\n  `bono_salida` tinyint(1) NOT NULL DEFAULT 0,\r\n  `pasivas_activas` tinyint(1) NOT NULL DEFAULT 0,\r\n  `modo_exponencial` tinyint(1) NOT NULL DEFAULT 0,\r\n  `jugador_moderador` varchar(30) DEFAULT NULL,\r\n  `multiplicador_exponencial` int(4) NOT NULL DEFAULT 1\r\n) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;\r\n\r\n--\r\n-- Volcado de datos para la tabla `variables`\r\n--\r\n\r\nINSERT INTO `variables` (`impuestos_para_parada_libre`, `acomulado_parada_libre`, `dinero_inicio_personalizado`, `dinero_inicio`, `bono_salida`, `pasivas_activas`, `modo_exponencial`, `jugador_moderador`, `multiplicador_exponencial`) VALUES\r\n(0, 0, 0, 1500, 1, 0, 1, \'gato\', 32);\r\n\r\n-- --------------------------------------------------------\r\n\r\n--\r\n-- Estructura de tabla para la tabla `version`\r\n--\r\n\r\nCREATE TABLE `version` (\r\n  `txt` varchar(10000) DEFAULT NULL\r\n) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;\r\n\r\n--\r\n-- Índices para tablas volcadas\r\n--\r\n\r\n--\r\n-- Indices de la tabla `movimientos`\r\n--\r\nALTER TABLE `movimientos`\r\n  ADD PRIMARY KEY (`id`);\r\n\r\n--\r\n-- Indices de la tabla `pasivas`\r\n--\r\nALTER TABLE `pasivas`\r\n  ADD PRIMARY KEY (`id`);\r\n\r\n--\r\n-- Indices de la tabla `propiedades`\r\n--\r\nALTER TABLE `propiedades`\r\n  ADD PRIMARY KEY (`id`);\r\n\r\n--\r\n-- AUTO_INCREMENT de las tablas volcadas\r\n--\r\n\r\n--\r\n-- AUTO_INCREMENT de la tabla `movimientos`\r\n--\r\nALTER TABLE `movimientos`\r\n  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=26;\r\n\r\n--\r\n-- AUTO_INCREMENT de la tabla `pasivas`\r\n--\r\nALTER TABLE `pasivas`\r\n  MODIFY `id` int(2) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;\r\n\r\n--\r\n-- AUTO_INCREMENT de la tabla `propiedades`\r\n--\r\nALTER TABLE `propiedades`\r\n  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=29;\r\nCOMMIT;\r\n\r\n/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;\r\n/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;\r\n/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;\r\n');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `movimientos`
--
ALTER TABLE `movimientos`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `pasivas`
--
ALTER TABLE `pasivas`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `propiedades`
--
ALTER TABLE `propiedades`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `movimientos`
--
ALTER TABLE `movimientos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `pasivas`
--
ALTER TABLE `pasivas`
  MODIFY `id` int(2) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT de la tabla `propiedades`
--
ALTER TABLE `propiedades`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=29;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
