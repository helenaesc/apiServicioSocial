
-- Archivo 02: Datos base del sistema
-- Requiere haber ejecutado antes: 01_poncho_schema_clean.sql

SET NAMES utf8mb4;
USE poncho;
SET FOREIGN_KEY_CHECKS = 0;

-- CONFIGURACIONES GLOBALES


INSERT INTO app_settings (k, v)
VALUES
  ('TOKEN_TTL_HOURS', '4'),
  ('ACCESS_CODE_TTL_MINUTES', '5'),
  ('PASS_SESSION_TTL_MINUTES', '2'),
  ('SESSION_MAX_HOURS', '8'),
  ('EXPORT_MAX_ROWS_HINT', '5000')
ON DUPLICATE KEY UPDATE
  v = VALUES(v);



-- CATÁLOGOS: DÍAS, MODALIDAD, HORARIO, ESTATUS LEGACY


INSERT INTO week_days (id, name)
VALUES
  (1, 'entre semana'),
  (2, 'fines de semana'),
  (3, 'mixto')
ON DUPLICATE KEY UPDATE
  name = VALUES(name);

INSERT INTO modality (id, name)
VALUES
  (1, 'en linea'),
  (2, 'presencial'),
  (3, 'mixto')
ON DUPLICATE KEY UPDATE
  name = VALUES(name);

INSERT INTO schedule (id, name)
VALUES
  (1, 'matutino'),
  (2, 'vespertino'),
  (3, 'mixto')
ON DUPLICATE KEY UPDATE
  name = VALUES(name);

INSERT INTO status (id, name)
VALUES
  (1, 'pendiente'),
  (2, 'aceptado'),
  (3, 'rechazado')
ON DUPLICATE KEY UPDATE
  name = VALUES(name);



-- CATÁLOGO DE CARRERAS / PROGRAMAS


INSERT INTO partner (id, name)
VALUES
  (4, 'LAD'),
  (5, 'LPS'),
  (6, 'ICT'),
  (7, 'IDM'),
  (8, 'IRS'),
  (9, 'ITC'),
  (10, 'ITD'),
  (12, 'LDI'),
  (13, 'LC'),
  (14, 'LNB'),
  (15, 'LAE'),
  (16, 'ING'),
  (17, 'IAG'),
  (18, 'IAL'),
  (19, 'IBT'),
  (20, 'IC'),
  (21, 'IDS'),
  (22, 'IE'),
  (23, 'IFI'),
  (24, 'IID'),
  (25, 'IIS'),
  (26, 'IM'),
  (27, 'IMD'),
  (28, 'IMT'),
  (29, 'INA'),
  (30, 'IQ'),
  (31, 'NEG'),
  (32, 'BGB'),
  (34, 'LAF'),
  (35, 'LDE'),
  (36, 'LDO'),
  (37, 'LEM'),
  (38, 'LIN'),
  (39, 'LIT'),
  (40, 'HCM'),
  (41, 'LEI'),
  (42, 'LLE'),
  (43, 'LTM'),
  (44, 'CPF'),
  (45, 'LHD'),
  (46, 'LED'),
  (47, 'LRI'),
  (64, 'AAD'),
  (65, 'ARQ'),
  (66, 'BA'),
  (67, 'LUB'),
  (68, 'CIS'),
  (69, 'BIR'),
  (70, 'LEC'),
  (71, 'LTP'),
  (72, 'BIE'),
  (73, 'BME'),
  (74, 'SLD'),
  (75, 'LBC'),
  (76, 'MC'),
  (77, 'MO'),
  (78, 'BBA'),
  (79, 'BFI'),
  (80, 'BM'),
  (95, 'Sin preferencia')
ON DUPLICATE KEY UPDATE
  name = VALUES(name);



-- GRUPOS DE CARRERAS


INSERT INTO partner_group (id, name)
VALUES
  (1, 'Ingeniería y Ciencias Computación'),
  (2, 'Arq, Arte y Diseño'),
  (3, 'Todas las carreras de negocios'),
  (4, 'Humanidades y Educación'),
  (5, 'Medicina y Ciencias de la Salud'),
  (6, 'Ciencias Sociales y Gobierno')
ON DUPLICATE KEY UPDATE
  name = VALUES(name);

INSERT INTO partner_group_member (group_id, partner_id)
VALUES
  -- Arq, Arte y Diseño
  (2, 4),
  (2, 12),
  (2, 64),
  (2, 65),
  (2, 66),
  (2, 67),

  -- Medicina y Ciencias de la Salud
  (5, 5),
  (5, 14),
  (5, 74),
  (5, 75),
  (5, 76),
  (5, 77),

  -- Ingeniería y Ciencias Computación
  (1, 6),
  (1, 7),
  (1, 8),
  (1, 9),
  (1, 10),
  (1, 16),
  (1, 17),
  (1, 18),
  (1, 19),
  (1, 20),
  (1, 21),
  (1, 22),
  (1, 23),
  (1, 24),
  (1, 25),
  (1, 26),
  (1, 27),
  (1, 28),
  (1, 29),
  (1, 30),
  (1, 72),
  (1, 73),

  -- Negocios
  (3, 15),
  (3, 31),
  (3, 32),
  (3, 34),
  (3, 35),
  (3, 36),
  (3, 37),
  (3, 38),
  (3, 39),
  (3, 44),
  (3, 78),
  (3, 79),
  (3, 80),

  -- Humanidades y Educación
  (4, 13),
  (4, 40),
  (4, 41),
  (4, 42),
  (4, 43),
  (4, 45),

  -- Ciencias Sociales y Gobierno
  (6, 46),
  (6, 47),
  (6, 68),
  (6, 69),
  (6, 70),
  (6, 71)
ON DUPLICATE KEY UPDATE
  partner_id = VALUES(partner_id);



-- USUARIO ADMINISTRADOR INICIAL
-- Correo: admin@tuapp.com
-- Contraseña: @dminKey1
-- Recomendación: cambiar la contraseña al instalar en ambiente real.


INSERT INTO admin_users
(
  full_name,
  email,
  password_hash,
  role,
  status
)
VALUES
(
  'Admin Principal',
  'admin@tuapp.com',
  'scrypt:32768:8:1$kRWGPibV9jmx7OHU$290429efa4c49f02ef7d4d309b5ecc03d95c131efa92ed49c1180ba7bd3df809227b9d82526806fc3f6f4a0923ac495302e846f1dfe13c417021cae87ae9a156',
  'ADMIN',
  'ACTIVE'
)
ON DUPLICATE KEY UPDATE
  full_name = VALUES(full_name),
  password_hash = VALUES(password_hash),
  role = VALUES(role),
  status = VALUES(status);



-- USUARIO STAFF DE DEMOSTRACIÓN BÁSICA
-- Correo: staff@tuapp.com
-- Contraseña: @dminKey1
-- Se puede eliminar o cambiar después.


INSERT INTO admin_users
(
  full_name,
  email,
  password_hash,
  role,
  status
)
VALUES
(
  'Staff Demo',
  'staff@tuapp.com',
  'scrypt:32768:8:1$kRWGPibV9jmx7OHU$290429efa4c49f02ef7d4d309b5ecc03d95c131efa92ed49c1180ba7bd3df809227b9d82526806fc3f6f4a0923ac495302e846f1dfe13c417021cae87ae9a156',
  'STAFF',
  'ACTIVE'
)
ON DUPLICATE KEY UPDATE
  full_name = VALUES(full_name),
  password_hash = VALUES(password_hash),
  role = VALUES(role),
  status = VALUES(status);


SET FOREIGN_KEY_CHECKS = 1;
