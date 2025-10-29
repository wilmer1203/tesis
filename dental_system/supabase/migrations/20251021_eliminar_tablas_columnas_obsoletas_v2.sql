-- Limpieza de Base de Datos - Eliminacion de Tablas y Columnas Obsoletas
-- Fecha: 2025-10-21
-- IMPORTANTE: Este script es DESTRUCTIVO - Hacer backup antes de ejecutar

BEGIN;

-- PASO 1: ELIMINAR COLUMNAS OBSOLETAS

-- TABLA: condiciones_diente
ALTER TABLE condiciones_diente
  DROP COLUMN IF EXISTS observaciones CASCADE,
  DROP COLUMN IF EXISTS material_utilizado CASCADE,
  DROP COLUMN IF EXISTS tecnica_utilizada CASCADE,
  DROP COLUMN IF EXISTS color_material CASCADE,
  DROP COLUMN IF EXISTS fecha_tratamiento CASCADE;

-- TABLA: consultas
ALTER TABLE consultas
  DROP COLUMN IF EXISTS odontologo_preferido_id CASCADE,
  DROP COLUMN IF EXISTS notas_internas CASCADE,
  DROP COLUMN IF EXISTS fecha_inicio_atencion CASCADE,
  DROP COLUMN IF EXISTS fecha_fin_atencion CASCADE;

-- TABLA: dientes
ALTER TABLE dientes
  DROP COLUMN IF EXISTS numero_diente_pediatrico CASCADE,
  DROP COLUMN IF EXISTS descripcion_anatomica CASCADE,
  DROP COLUMN IF EXISTS coordenadas_svg CASCADE,
  DROP COLUMN IF EXISTS forma_base CASCADE,
  DROP COLUMN IF EXISTS imagenes_clinicas CASCADE;

-- PASO 2: ELIMINAR TABLAS OBSOLETAS

DROP TABLE IF EXISTS auditoria CASCADE;
DROP TABLE IF EXISTS cola_atencion CASCADE;
DROP TABLE IF EXISTS configuracion_sistema CASCADE;
DROP TABLE IF EXISTS notificaciones_sistema CASCADE;

-- PASO 3: VERIFICACION POST-ELIMINACION

CREATE OR REPLACE VIEW verificacion_limpieza AS
SELECT
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as size_pretty
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY tablename;

SELECT * FROM verificacion_limpieza;

COMMIT;
