-- Archivo 03: Datos de demostración
-- Requiere haber ejecutado antes:
-- 01_poncho_schema_clean.sql
-- 02_poncho_seed_base.sql


SET NAMES utf8mb4;
USE poncho;
SET FOREIGN_KEY_CHECKS = 0;

-- EVENTO DEMO


INSERT INTO events
(
  year,
  season,
  display_name,
  catalog_open_at,
  onsite_start_at,
  onsite_end_at,
  registration_close_at,
  status,
  is_visible_to_students
)
VALUES
(
  2027,
  'PRIMAVERA',
  'Primavera 2027',
  NOW(),
  NOW(),
  DATE_ADD(NOW(), INTERVAL 8 HOUR),
  DATE_ADD(NOW(), INTERVAL 8 HOUR),
  'ONSITE',
  TRUE
)
ON DUPLICATE KEY UPDATE
  display_name = VALUES(display_name),
  catalog_open_at = VALUES(catalog_open_at),
  onsite_start_at = VALUES(onsite_start_at),
  onsite_end_at = VALUES(onsite_end_at),
  registration_close_at = VALUES(registration_close_at),
  status = VALUES(status),
  is_visible_to_students = VALUES(is_visible_to_students);

SET @event_id := (
  SELECT id
  FROM events
  WHERE year = 2027
    AND season = 'PRIMAVERA'
  LIMIT 1
);



-- PROYECTO DEMO 1


INSERT INTO project
(
  general_name,
  name,
  id_partner,
  id_modality,
  id_week_days,
  id_schedule,
  slots,
  schedule_description,
  team_owners,
  objectives,
  activities,
  clave,
  competencies,
  location,
  duration,
  audience,
  max_hours,
  comments,
  season,
  academy_mode,
  academy_group_id
)
SELECT
  'Vinculación Ciudadana',
  'Reconocimiento de los Derechos Humanos con enfoque de cultura de paz',
  95,
  1,
  1,
  3,
  30,
  'Lunes, miércoles y viernes con sesiones de dos horas.',
  'Equipo de vinculación',
  'Diseñar propuestas sociales alcanzables para fortalecer la cultura de paz y la corresponsabilidad social.',
  'Taller de inducción, lluvia de ideas, laboratorio de proyectos y diseño de una propuesta final.',
  'WA1067',
  'Corresponsabilidad social, análisis del entorno, trabajo colaborativo y comunicación.',
  'En línea',
  '10 semanas',
  'Niñas, niños y adolescentes',
  120,
  'Proyecto de ejemplo para demostrar el catálogo, registro y asignación de tokens.',
  'Primavera 2027',
  'ALL',
  NULL
WHERE NOT EXISTS (
  SELECT 1
  FROM project
  WHERE general_name = 'Vinculación Ciudadana'
    AND name = 'Reconocimiento de los Derechos Humanos con enfoque de cultura de paz'
);

SET @project_1 := (
  SELECT id
  FROM project
  WHERE general_name = 'Vinculación Ciudadana'
    AND name = 'Reconocimiento de los Derechos Humanos con enfoque de cultura de paz'
  ORDER BY id DESC
  LIMIT 1
);



-- PROYECTO DEMO 2


INSERT INTO project
(
  general_name,
  name,
  id_partner,
  id_modality,
  id_week_days,
  id_schedule,
  slots,
  schedule_description,
  team_owners,
  objectives,
  activities,
  clave,
  competencies,
  location,
  duration,
  audience,
  max_hours,
  comments,
  season,
  academy_mode,
  academy_group_id
)
SELECT
  'Laboratorio de Datos',
  'Análisis de participación estudiantil en eventos académicos',
  9,
  3,
  1,
  1,
  25,
  'Sesiones matutinas con reuniones de seguimiento.',
  'Equipo de analítica',
  'Analizar datos de participación para generar indicadores útiles para la toma de decisiones.',
  'Limpieza de datos, construcción de indicadores, visualización y presentación de hallazgos.',
  'DATA101',
  'Análisis de datos, visualización, pensamiento crítico y comunicación efectiva.',
  'Campus',
  '8 semanas',
  'Estudiantes interesados en datos y tecnología',
  80,
  'Proyecto de ejemplo orientado a estudiantes de tecnología y análisis de datos.',
  'Primavera 2027',
  'CUSTOM',
  NULL
WHERE NOT EXISTS (
  SELECT 1
  FROM project
  WHERE general_name = 'Laboratorio de Datos'
    AND name = 'Análisis de participación estudiantil en eventos académicos'
);

SET @project_2 := (
  SELECT id
  FROM project
  WHERE general_name = 'Laboratorio de Datos'
    AND name = 'Análisis de participación estudiantil en eventos académicos'
  ORDER BY id DESC
  LIMIT 1
);

INSERT IGNORE INTO project_partner_pref (project_id, partner_id)
VALUES
  (@project_2, 9),
  (@project_2, 10),
  (@project_2, 21);



-- PROYECTO DEMO 3


INSERT INTO project
(
  general_name,
  name,
  id_partner,
  id_modality,
  id_week_days,
  id_schedule,
  slots,
  schedule_description,
  team_owners,
  objectives,
  activities,
  clave,
  competencies,
  location,
  duration,
  audience,
  max_hours,
  comments,
  season,
  academy_mode,
  academy_group_id
)
SELECT
  'Diseño con Impacto',
  'Campaña visual para comunicación social',
  4,
  2,
  3,
  2,
  20,
  'Trabajo mixto con sesiones vespertinas.',
  'Equipo creativo',
  'Desarrollar materiales visuales para comunicar una problemática social de forma clara y atractiva.',
  'Investigación visual, bocetaje, propuesta gráfica, validación y entrega final.',
  'DIS202',
  'Creatividad, diseño centrado en usuario, comunicación visual y trabajo interdisciplinario.',
  'Campus',
  '6 semanas',
  'Estudiantes de diseño, comunicación y áreas afines',
  60,
  'Proyecto de ejemplo para demostrar proyectos con enfoque creativo.',
  'Primavera 2027',
  'GROUP',
  2
WHERE NOT EXISTS (
  SELECT 1
  FROM project
  WHERE general_name = 'Diseño con Impacto'
    AND name = 'Campaña visual para comunicación social'
);

SET @project_3 := (
  SELECT id
  FROM project
  WHERE general_name = 'Diseño con Impacto'
    AND name = 'Campaña visual para comunicación social'
  ORDER BY id DESC
  LIMIT 1
);



-- ACTIVAR PROYECTOS EN EL EVENTO


INSERT INTO event_projects
(
  event_id,
  project_id,
  slots_total,
  status,
  notes
)
VALUES
  (@event_id, @project_1, 30, 'ACTIVE', 'Proyecto demo activo'),
  (@event_id, @project_2, 25, 'ACTIVE', 'Proyecto demo activo'),
  (@event_id, @project_3, 20, 'ACTIVE', 'Proyecto demo activo')
ON DUPLICATE KEY UPDATE
  slots_total = VALUES(slots_total),
  status = VALUES(status),
  notes = VALUES(notes);

SET @ep_1 := (
  SELECT id FROM event_projects
  WHERE event_id = @event_id AND project_id = @project_1
  LIMIT 1
);

SET @ep_2 := (
  SELECT id FROM event_projects
  WHERE event_id = @event_id AND project_id = @project_2
  LIMIT 1
);

SET @ep_3 := (
  SELECT id FROM event_projects
  WHERE event_id = @event_id AND project_id = @project_3
  LIMIT 1
);



-- TOKENS DEMO DE PROYECTO
-- Estos tokens permiten probar el registro de alumnos.


INSERT INTO project_tokens
(
  event_project_id,
  token_value,
  status,
  expires_at
)
VALUES
  (@ep_1, 'DEMO-P1-001', 'AVAILABLE', DATE_ADD(NOW(), INTERVAL 24 HOUR)),
  (@ep_1, 'DEMO-P1-002', 'AVAILABLE', DATE_ADD(NOW(), INTERVAL 24 HOUR)),
  (@ep_1, 'DEMO-P1-003', 'AVAILABLE', DATE_ADD(NOW(), INTERVAL 24 HOUR)),

  (@ep_2, 'DEMO-P2-001', 'AVAILABLE', DATE_ADD(NOW(), INTERVAL 24 HOUR)),
  (@ep_2, 'DEMO-P2-002', 'AVAILABLE', DATE_ADD(NOW(), INTERVAL 24 HOUR)),
  (@ep_2, 'DEMO-P2-003', 'AVAILABLE', DATE_ADD(NOW(), INTERVAL 24 HOUR)),

  (@ep_3, 'DEMO-P3-001', 'AVAILABLE', DATE_ADD(NOW(), INTERVAL 24 HOUR)),
  (@ep_3, 'DEMO-P3-002', 'AVAILABLE', DATE_ADD(NOW(), INTERVAL 24 HOUR)),
  (@ep_3, 'DEMO-P3-003', 'AVAILABLE', DATE_ADD(NOW(), INTERVAL 24 HOUR))
ON DUPLICATE KEY UPDATE
  status = 'AVAILABLE',
  expires_at = DATE_ADD(NOW(), INTERVAL 24 HOUR),
  reserved_by_request_id = NULL,
  reserved_at = NULL,
  reserved_until = NULL,
  used_by_request_id = NULL,
  used_at = NULL,
  revoked_at = NULL,
  revoke_reason = NULL;


SET FOREIGN_KEY_CHECKS = 1;
