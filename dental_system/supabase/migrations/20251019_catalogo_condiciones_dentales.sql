-- ============================================================================
-- MIGRACIÓN: CATÁLOGO DE CONDICIONES DENTALES V3.0
-- ============================================================================
-- Fecha: 2025-10-19
-- Propósito: Eliminar mapeo hardcodeado de servicios a condiciones
-- Autor: Sistema Odontológico - Refactorización V3.0
--
-- CAMBIOS PRINCIPALES:
-- 1. Crear tabla catalogo_condiciones (condiciones disponibles del sistema)
-- 2. Agregar campo condicion_resultante a tabla servicios
-- 3. Crear función SQL actualizar_condiciones_batch (transaccional)
-- 4. Poblar datos iniciales de condiciones y servicios
-- ============================================================================

-- ============================================================================
-- PASO 1: CREAR TABLA CATÁLOGO DE CONDICIONES
-- ============================================================================

CREATE TABLE IF NOT EXISTS catalogo_condiciones (
    -- Identificador único (código legible)
    codigo VARCHAR(50) PRIMARY KEY,

    -- Información básica
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,

    -- Categorización
    categoria VARCHAR(50) NOT NULL
        CHECK (categoria IN ('normal', 'patologia', 'restauracion', 'protesis', 'ausencia')),

    -- Visualización
    color_hex VARCHAR(7) DEFAULT '#90EE90' NOT NULL,
    icono_emoji VARCHAR(10) DEFAULT '🦷',

    -- Reglas de negocio
    prioridad INTEGER DEFAULT 1 NOT NULL
        CHECK (prioridad BETWEEN 1 AND 10),
    es_estado_final BOOLEAN DEFAULT false NOT NULL,
    permite_reversion BOOLEAN DEFAULT true NOT NULL,

    -- Control
    activo BOOLEAN DEFAULT true NOT NULL,

    -- Auditoría
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Índices para búsquedas rápidas
CREATE INDEX idx_catalogo_condiciones_activo
ON catalogo_condiciones(activo)
WHERE activo = true;

CREATE INDEX idx_catalogo_condiciones_prioridad
ON catalogo_condiciones(prioridad DESC)
WHERE activo = true;

CREATE INDEX idx_catalogo_condiciones_categoria
ON catalogo_condiciones(categoria);

-- Comentarios
COMMENT ON TABLE catalogo_condiciones IS
'Catálogo centralizado de condiciones dentales disponibles en el sistema';

COMMENT ON COLUMN catalogo_condiciones.codigo IS
'Código único identificador de la condición (usado como FK)';

COMMENT ON COLUMN catalogo_condiciones.prioridad IS
'Prioridad de la condición (1=baja, 10=crítica). Usado para resolver conflictos cuando múltiples servicios afectan mismo diente/superficie';

COMMENT ON COLUMN catalogo_condiciones.es_estado_final IS
'Indica si esta condición es irreversible (ej: ausente). Previene aplicar tratamientos posteriores';

COMMENT ON COLUMN catalogo_condiciones.permite_reversion IS
'Permite cambiar esta condición a otra en el futuro';

-- ============================================================================
-- PASO 2: POBLAR CATÁLOGO INICIAL DE CONDICIONES
-- ============================================================================

INSERT INTO catalogo_condiciones
(codigo, nombre, descripcion, categoria, color_hex, icono_emoji, prioridad, es_estado_final, permite_reversion)
VALUES
-- Estados normales
('sano', 'Sano',
 'Diente sin patologías, obturaciones o tratamientos previos',
 'normal', '#90EE90', '✅', 1, false, true),

-- Patologías
('caries', 'Caries',
 'Lesión cariosa activa que requiere tratamiento restaurativo',
 'patologia', '#FF6B6B', '🦠', 3, false, true),

('fractura', 'Fractura',
 'Fractura dental que requiere evaluación y tratamiento',
 'patologia', '#FF4500', '💥', 4, false, true),

('extraccion_indicada', 'Extracción Indicada',
 'Diente marcado para extracción futura',
 'patologia', '#DC143C', '⚠️', 4, false, true),

-- Restauraciones
('obturacion', 'Obturación',
 'Restauración dental con resina, amalgama u otro material',
 'restauracion', '#C0C0C0', '🔧', 5, false, true),

('endodoncia', 'Endodoncia',
 'Tratamiento de conducto radicular completado',
 'restauracion', '#FF8C00', '🦷', 6, false, true),

-- Prótesis
('corona', 'Corona',
 'Corona dental protésica cementada',
 'protesis', '#FFD700', '👑', 7, false, true),

('puente', 'Puente',
 'Pieza dental forma parte de un puente protésico',
 'protesis', '#9370DB', '🌉', 7, false, false),

('implante', 'Implante',
 'Implante dental osteointegrado',
 'protesis', '#32CD32', '🔩', 7, false, false),

('protesis', 'Prótesis',
 'Prótesis dental removible o fija',
 'protesis', '#DDA0DD', '🦾', 7, false, true),

-- Ausencia (prioridad MÁXIMA)
('ausente', 'Ausente/Extraído',
 'Diente ausente por extracción, agenesia o pérdida',
 'ausencia', '#D3D3D3', '❌', 10, true, false)

ON CONFLICT (codigo) DO NOTHING;

-- ============================================================================
-- PASO 3: MODIFICAR TABLA SERVICIOS
-- ============================================================================

-- Agregar campo condicion_resultante (FK a catálogo)
ALTER TABLE servicios
ADD COLUMN IF NOT EXISTS condicion_resultante VARCHAR(50) NULL;

-- Crear constraint de FK (permite NULL para servicios preventivos)
ALTER TABLE servicios
ADD CONSTRAINT fk_servicios_condicion_resultante
FOREIGN KEY (condicion_resultante)
REFERENCES catalogo_condiciones(codigo)
ON DELETE SET NULL;

-- Índice para búsquedas rápidas
CREATE INDEX IF NOT EXISTS idx_servicios_condicion_resultante
ON servicios(condicion_resultante)
WHERE condicion_resultante IS NOT NULL;

-- Comentario
COMMENT ON COLUMN servicios.condicion_resultante IS
'Condición dental resultante al aplicar este servicio. NULL = servicio preventivo que no modifica el odontograma';

-- ============================================================================
-- PASO 4: POBLAR SERVICIOS EXISTENTES CON CONDICIONES
-- ============================================================================

-- Actualizar servicios restaurativos
UPDATE servicios
SET condicion_resultante = 'obturacion'
WHERE condicion_resultante IS NULL
  AND (
    nombre ILIKE '%obturacion%' OR
    nombre ILIKE '%obturació%' OR
    nombre ILIKE '%resina%' OR
    nombre ILIKE '%amalgama%' OR
    nombre ILIKE '%restauracion%' OR
    nombre ILIKE '%restauració%'
  );

-- Actualizar servicios de extracción
UPDATE servicios
SET condicion_resultante = 'ausente'
WHERE condicion_resultante IS NULL
  AND (
    nombre ILIKE '%extraccion%' OR
    nombre ILIKE '%extracció%' OR
    nombre ILIKE '%exodoncia%' OR
    nombre ILIKE '%cirugia%' OR
    nombre ILIKE '%cirugía%'
  );

-- Actualizar servicios de endodoncia
UPDATE servicios
SET condicion_resultante = 'endodoncia'
WHERE condicion_resultante IS NULL
  AND (
    nombre ILIKE '%endodoncia%' OR
    nombre ILIKE '%conducto%' OR
    nombre ILIKE '%tratamiento de conducto%'
  );

-- Actualizar servicios protésicos - corona
UPDATE servicios
SET condicion_resultante = 'corona'
WHERE condicion_resultante IS NULL
  AND nombre ILIKE '%corona%';

-- Actualizar servicios protésicos - puente
UPDATE servicios
SET condicion_resultante = 'puente'
WHERE condicion_resultante IS NULL
  AND nombre ILIKE '%puente%';

-- Actualizar servicios protésicos - implante
UPDATE servicios
SET condicion_resultante = 'implante'
WHERE condicion_resultante IS NULL
  AND nombre ILIKE '%implante%';

-- Actualizar servicios protésicos - prótesis general
UPDATE servicios
SET condicion_resultante = 'protesis'
WHERE condicion_resultante IS NULL
  AND (nombre ILIKE '%protesis%' OR nombre ILIKE '%prótesis%');

-- Los servicios preventivos quedan con NULL (correcto):
-- - Limpieza
-- - Profilaxis
-- - Consulta
-- - Blanqueamiento
-- - Radiografía
-- - etc.

-- ============================================================================
-- PASO 5: FUNCIÓN SQL BATCH PARA ACTUALIZACIÓN TRANSACCIONAL
-- ============================================================================

CREATE OR REPLACE FUNCTION actualizar_condiciones_batch(
    actualizaciones JSONB -- Array de objetos con datos de actualización
)
RETURNS TABLE (
    exitosos INTEGER,
    fallidos INTEGER,
    ids_creados UUID[]
)
LANGUAGE plpgsql
AS $$
DECLARE
    actualizacion JSONB;
    exitosos_count INTEGER := 0;
    fallidos_count INTEGER := 0;
    ids_array UUID[] := ARRAY[]::UUID[];
    nuevo_id UUID;
    error_msg TEXT;
BEGIN
    -- Iterar sobre cada actualización en el array
    FOR actualizacion IN
        SELECT * FROM jsonb_array_elements(actualizaciones)
    LOOP
        BEGIN
            -- Marcar condición anterior como inactiva (histórico)
            UPDATE condiciones_diente
            SET activo = FALSE,
                updated_at = CURRENT_TIMESTAMP
            WHERE paciente_id = (actualizacion->>'paciente_id')::UUID
              AND diente_numero = (actualizacion->>'diente_numero')::INTEGER
              AND superficie = actualizacion->>'superficie'
              AND activo = TRUE;

            -- Insertar nueva condición (activa)
            INSERT INTO condiciones_diente (
                paciente_id,
                diente_numero,
                superficie,
                tipo_condicion,
                intervencion_id,
                material_utilizado,
                descripcion,
                registrado_por,
                activo,
                fecha_registro
            ) VALUES (
                (actualizacion->>'paciente_id')::UUID,
                (actualizacion->>'diente_numero')::INTEGER,
                actualizacion->>'superficie',
                actualizacion->>'nueva_condicion',
                NULLIF(actualizacion->>'intervencion_id', '')::UUID,
                NULLIF(actualizacion->>'material', ''),
                NULLIF(actualizacion->>'descripcion', ''),
                NULLIF(actualizacion->>'registrado_por', '')::UUID,
                TRUE,
                CURRENT_TIMESTAMP
            ) RETURNING id INTO nuevo_id;

            -- Registrar éxito
            ids_array := array_append(ids_array, nuevo_id);
            exitosos_count := exitosos_count + 1;

        EXCEPTION
            WHEN OTHERS THEN
                -- Capturar error pero continuar con otras actualizaciones
                GET STACKED DIAGNOSTICS error_msg = MESSAGE_TEXT;

                RAISE WARNING 'Error actualizando diente % superficie %: %',
                    actualizacion->>'diente_numero',
                    actualizacion->>'superficie',
                    error_msg;

                fallidos_count := fallidos_count + 1;
        END;
    END LOOP;

    -- Retornar resultados
    RETURN QUERY SELECT exitosos_count, fallidos_count, ids_array;
END;
$$;

-- Comentario
COMMENT ON FUNCTION actualizar_condiciones_batch IS
'Actualiza múltiples condiciones dentales en batch. Marca condiciones anteriores como inactivas (activo=FALSE) e inserta nuevas condiciones activas. Retorna conteo de éxitos/fallos y array de IDs creados.';

-- ============================================================================
-- PASO 6: TRIGGER PARA ACTUALIZACIÓN AUTOMÁTICA DE TIMESTAMPS
-- ============================================================================

CREATE OR REPLACE FUNCTION actualizar_timestamp_catalogo_condiciones()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$;

CREATE TRIGGER trigger_actualizar_timestamp_catalogo
BEFORE UPDATE ON catalogo_condiciones
FOR EACH ROW
EXECUTE FUNCTION actualizar_timestamp_catalogo_condiciones();

-- ============================================================================
-- PASO 7: VERIFICACIÓN DE MIGRACIÓN
-- ============================================================================

-- Verificar tabla catalogo_condiciones
DO $$
DECLARE
    count_condiciones INTEGER;
BEGIN
    SELECT COUNT(*) INTO count_condiciones FROM catalogo_condiciones WHERE activo = true;
    RAISE NOTICE '✅ Catálogo de condiciones creado: % condiciones activas', count_condiciones;
END $$;

-- Verificar campo en servicios
DO $$
DECLARE
    count_servicios_con_condicion INTEGER;
    count_servicios_preventivos INTEGER;
BEGIN
    SELECT COUNT(*) INTO count_servicios_con_condicion
    FROM servicios
    WHERE condicion_resultante IS NOT NULL;

    SELECT COUNT(*) INTO count_servicios_preventivos
    FROM servicios
    WHERE condicion_resultante IS NULL;

    RAISE NOTICE '✅ Servicios actualizados: % con condición, % preventivos',
        count_servicios_con_condicion,
        count_servicios_preventivos;
END $$;

-- ============================================================================
-- ROLLBACK (si es necesario - COMENTADO por seguridad)
-- ============================================================================

/*
-- Para revertir esta migración (usar con PRECAUCIÓN):

-- Eliminar función
DROP FUNCTION IF EXISTS actualizar_condiciones_batch(JSONB);
DROP FUNCTION IF EXISTS actualizar_timestamp_catalogo_condiciones();

-- Eliminar campo de servicios
ALTER TABLE servicios DROP CONSTRAINT IF EXISTS fk_servicios_condicion_resultante;
ALTER TABLE servicios DROP COLUMN IF EXISTS condicion_resultante;

-- Eliminar tabla catálogo
DROP TABLE IF EXISTS catalogo_condiciones CASCADE;
*/

-- ============================================================================
-- FIN DE MIGRACIÓN
-- ============================================================================
