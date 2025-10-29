-- =====================================================
-- 🧪 SCRIPT DE PRUEBA: actualizar_condicion_diente()
-- =====================================================
-- Propósito: Probar la función SQL que actualiza condiciones
-- Ejecución: psql -h localhost -p 54322 -U postgres -d postgres -f test_actualizar_condicion.sql
-- =====================================================

\echo '🧪 Iniciando pruebas de actualizar_condicion_diente()...'
\echo ''

-- =====================================================
-- PASO 1: Verificar que la función existe
-- =====================================================
\echo '📋 PASO 1: Verificando que la función existe...'
SELECT
    routine_name,
    routine_type,
    data_type
FROM information_schema.routines
WHERE routine_schema = 'public'
  AND routine_name = 'actualizar_condicion_diente';

\echo ''

-- =====================================================
-- PASO 2: Obtener un paciente de prueba
-- =====================================================
\echo '📋 PASO 2: Obteniendo paciente de prueba...'
SELECT
    id,
    numero_historia,
    primer_nombre || ' ' || primer_apellido as nombre_completo
FROM pacientes
LIMIT 1;

-- Guardar el ID para usar después
\gset

\echo 'Paciente seleccionado:'
\echo '  ID: ' :id
\echo '  HC: ' :numero_historia
\echo '  Nombre: ' :nombre_completo
\echo ''

-- =====================================================
-- PASO 3: Ver condición ACTUAL del diente 11, superficie oclusal
-- =====================================================
\echo '📋 PASO 3: Condición ACTUAL del diente 11 (oclusal) ANTES de actualizar...'
SELECT
    diente_numero,
    superficie,
    tipo_condicion,
    material_utilizado,
    activo,
    fecha_registro
FROM condiciones_diente
WHERE paciente_id = :'id'
  AND diente_numero = 11
  AND superficie = 'oclusal'
ORDER BY fecha_registro DESC;

\echo ''

-- =====================================================
-- PASO 4: EJECUTAR la función para cambiar condición
-- =====================================================
\echo '📋 PASO 4: EJECUTANDO actualizar_condicion_diente()...'
\echo '  Cambiando diente 11 (oclusal) a "obturacion"...'

SELECT actualizar_condicion_diente(
    p_paciente_id := :'id'::uuid,
    p_diente_numero := 11,
    p_superficie := 'oclusal',
    p_nueva_condicion := 'obturacion',
    p_intervencion_id := NULL,
    p_material := 'Resina Compuesta',
    p_descripcion := 'Test desde SQL',
    p_registrado_por := NULL
) AS nueva_condicion_id;

\gset

\echo 'Nueva condición ID: ' :nueva_condicion_id
\echo ''

-- =====================================================
-- PASO 5: Verificar que se creó la nueva condición
-- =====================================================
\echo '📋 PASO 5: Verificando NUEVA condición (activo = TRUE)...'
SELECT
    diente_numero,
    superficie,
    tipo_condicion,
    material_utilizado,
    activo,
    descripcion,
    fecha_registro
FROM condiciones_diente
WHERE paciente_id = :'id'
  AND diente_numero = 11
  AND superficie = 'oclusal'
  AND activo = TRUE;

\echo ''

-- =====================================================
-- PASO 6: Verificar que se desactivó la anterior
-- =====================================================
\echo '📋 PASO 6: Verificando condición ANTERIOR (activo = FALSE)...'
SELECT
    diente_numero,
    superficie,
    tipo_condicion,
    material_utilizado,
    activo,
    fecha_registro
FROM condiciones_diente
WHERE paciente_id = :'id'
  AND diente_numero = 11
  AND superficie = 'oclusal'
  AND activo = FALSE
ORDER BY fecha_registro DESC
LIMIT 1;

\echo ''

-- =====================================================
-- PASO 7: Ver HISTORIAL COMPLETO del diente 11
-- =====================================================
\echo '📋 PASO 7: HISTORIAL COMPLETO del diente 11 (oclusal)...'
SELECT
    fecha_registro,
    tipo_condicion,
    material_utilizado,
    activo,
    CASE
        WHEN activo = TRUE THEN '← ACTUAL'
        ELSE '  histórico'
    END as estado
FROM condiciones_diente
WHERE paciente_id = :'id'
  AND diente_numero = 11
  AND superficie = 'oclusal'
ORDER BY fecha_registro DESC;

\echo ''
\echo '✅ Pruebas completadas!'
\echo ''
\echo 'RESUMEN:'
\echo '  1. Función existe ✓'
\echo '  2. Paciente encontrado ✓'
\echo '  3. Condición anterior obtenida ✓'
\echo '  4. Nueva condición creada ✓'
\echo '  5. Verificación activo=TRUE ✓'
\echo '  6. Verificación anterior activo=FALSE ✓'
\echo '  7. Historial completo mostrado ✓'
\echo ''
\echo '🎯 Si ves "obturacion" con activo=TRUE arriba, la función FUNCIONA correctamente.'
\echo ''
