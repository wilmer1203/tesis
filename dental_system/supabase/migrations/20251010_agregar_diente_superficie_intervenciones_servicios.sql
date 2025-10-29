-- =====================================================
-- MIGRACIÓN: Agregar diente_numero y superficie a intervenciones_servicios
-- =====================================================
-- Fecha: 2025-10-10
-- Propósito: Permitir detalle específico por diente y superficie en servicios

-- PASO 1: Agregar columnas diente_numero y superficie
ALTER TABLE intervenciones_servicios
ADD COLUMN diente_numero INTEGER,
ADD COLUMN superficie VARCHAR(20);

-- PASO 2: Crear índices para optimizar búsquedas
CREATE INDEX idx_interv_servicios_diente ON intervenciones_servicios(diente_numero);
CREATE INDEX idx_interv_servicios_diente_superficie ON intervenciones_servicios(diente_numero, superficie);

-- PASO 3: Agregar comentarios descriptivos
COMMENT ON COLUMN intervenciones_servicios.diente_numero IS 'Número FDI del diente (11-48). NULL para servicios de boca completa.';
COMMENT ON COLUMN intervenciones_servicios.superficie IS 'Superficie específica del diente (oclusal, mesial, distal, vestibular, lingual). NULL para servicio de diente completo o boca completa.';

-- PASO 4: Modificar constraint de precios para permitir valores de 0 cuando sea necesario
ALTER TABLE intervenciones_servicios
DROP CONSTRAINT IF EXISTS chk_interv_serv_precios;

ALTER TABLE intervenciones_servicios
ADD CONSTRAINT chk_interv_serv_precios
CHECK (
    precio_unitario_bs >= 0 AND
    precio_unitario_usd >= 0 AND
    precio_total_bs = (cantidad::numeric * precio_unitario_bs) AND
    precio_total_usd = (cantidad::numeric * precio_unitario_usd)
);

-- PASO 5: Comentario en tabla dientes_especificos (legacy)
COMMENT ON COLUMN intervenciones_servicios.dientes_especificos IS 'DEPRECADO: Array de dientes. Usar diente_numero en su lugar para mayor detalle.';

-- =====================================================
-- VERIFICACIÓN
-- =====================================================
-- Mostrar estructura actualizada de la tabla
SELECT
    column_name,
    data_type,
    is_nullable,
    column_default
FROM information_schema.columns
WHERE table_name = 'intervenciones_servicios'
ORDER BY ordinal_position;
