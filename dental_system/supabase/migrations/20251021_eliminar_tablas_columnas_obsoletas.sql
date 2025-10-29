-- ========================================
-- 🗑️ LIMPIEZA DE BASE DE DATOS
-- Eliminación de Tablas y Columnas Obsoletas
-- ========================================
-- Fecha: 2025-10-21
-- Autor: Claude Code
-- Propósito: Eliminar estructuras no utilizadas en el sistema

-- ⚠️ IMPORTANTE: Este script es DESTRUCTIVO
-- Hacer backup antes de ejecutar
-- Ejecutar en ambiente de desarrollo primero

BEGIN;

-- ========================================
-- PASO 1: ELIMINAR COLUMNAS OBSOLETAS
-- ========================================

-- 🔧 TABLA: condiciones_diente
-- Columnas usadas solo en versión antigua del sistema
ALTER TABLE condiciones_diente
  DROP COLUMN IF EXISTS observaciones CASCADE,           -- Redundante con 'descripcion'
  DROP COLUMN IF EXISTS material_utilizado CASCADE,      -- Se registra en intervenciones_servicios
  DROP COLUMN IF EXISTS tecnica_utilizada CASCADE,       -- No se usa
  DROP COLUMN IF EXISTS color_material CASCADE,          -- No se usa
  DROP COLUMN IF EXISTS fecha_tratamiento CASCADE;       -- Ya tenemos fecha_registro

-- 🔧 TABLA: consultas
-- Columnas que NO se usan en el flujo actual
ALTER TABLE consultas
  DROP COLUMN IF EXISTS odontologo_preferido_id CASCADE, -- No se usa en sistema de colas
  DROP COLUMN IF EXISTS notas_internas CASCADE,          -- Redundante con 'observaciones'
  DROP COLUMN IF EXISTS fecha_inicio_atencion CASCADE,   -- Redundante con fecha_creacion
  DROP COLUMN IF EXISTS fecha_fin_atencion CASCADE;      -- Redundante con fecha_actualizacion

-- 🔧 TABLA: dientes
-- Columnas innecesarias en catálogo simplificado
ALTER TABLE dientes
  DROP COLUMN IF EXISTS numero_diente_pediatrico CASCADE,  -- No se usa
  DROP COLUMN IF EXISTS descripcion_anatomica CASCADE,     -- Información excesiva
  DROP COLUMN IF EXISTS coordenadas_svg CASCADE,           -- Frontend maneja esto
  DROP COLUMN IF EXISTS forma_base CASCADE,                -- No se usa
  DROP COLUMN IF EXISTS imagenes_clinicas CASCADE;         -- No se usa

-- ========================================
-- PASO 2: ELIMINAR TABLAS OBSOLETAS
-- ========================================

-- ❌ TABLA: auditoria
-- No se implementó el sistema de auditoría
DROP TABLE IF EXISTS auditoria CASCADE;

-- ❌ TABLA: cola_atencion
-- Sistema de colas se maneja directamente en tabla 'consultas'
DROP TABLE IF EXISTS cola_atencion CASCADE;

-- ❌ TABLA: configuracion_sistema
-- Configuraciones se manejan en variables de entorno
DROP TABLE IF EXISTS configuracion_sistema CASCADE;

-- ❌ TABLA: notificaciones_sistema
-- No existe esta tabla, pero por si acaso
DROP TABLE IF EXISTS notificaciones_sistema CASCADE;

-- ========================================
-- PASO 3: ELIMINAR ARCHIVOS PYTHON ASOCIADOS
-- ========================================

-- 📝 NOTA: Los siguientes archivos deben eliminarse manualmente:
--
-- dental_system/supabase/tablas/auditoria.py
-- dental_system/supabase/tablas/cola_atencion.py
-- dental_system/supabase/tablas/configuracion_sistema.py
--
-- Y actualizar dental_system/supabase/tablas/__init__.py
-- Eliminando los imports correspondientes

-- ========================================
-- PASO 4: VERIFICACIÓN POST-ELIMINACIÓN
-- ========================================

-- Crear vista temporal para verificar tablas restantes
CREATE OR REPLACE VIEW verificacion_limpieza AS
SELECT
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as tamaño
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY tablename;

-- Mostrar resultado
SELECT * FROM verificacion_limpieza;

COMMIT;

-- ========================================
-- 📊 RESULTADO ESPERADO
-- ========================================
--
-- ✅ COLUMNAS ELIMINADAS: 15 columnas
--    - condiciones_diente: 5 columnas
--    - consultas: 4 columnas
--    - dientes: 5 columnas
--
-- ✅ TABLAS ELIMINADAS: 4 tablas
--    - auditoria
--    - cola_atencion
--    - configuracion_sistema
--    - notificaciones_sistema (si existía)
--
-- ⚠️ IMPACTO:
--    - Reducción estimada de espacio: ~15-20%
--    - Queries más rápidos (menos columnas)
--    - Esquema más limpio y mantenible
--
-- 🔄 ROLLBACK:
--    Si algo sale mal: ROLLBACK;
--    O restaurar desde backup
-- ========================================
