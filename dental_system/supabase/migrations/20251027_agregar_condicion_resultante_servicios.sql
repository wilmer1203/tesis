-- =====================================================
-- MIGRACIÓN: Agregar campo condicion_resultante a tabla servicios
-- =====================================================
-- Fecha: 2025-10-27
-- Propósito: Mapeo automático servicio → condición de diente
-- Evita errores humanos al olvidar seleccionar condición manualmente
-- =====================================================

-- PASO 1: Agregar columna condicion_resultante
-- Permite NULL porque servicios preventivos (boca completa) no modifican odontograma
ALTER TABLE servicios
ADD COLUMN IF NOT EXISTS condicion_resultante VARCHAR(50) NULL;

-- PASO 2: Agregar constraint para validar condiciones
-- Solo permite valores válidos del catálogo de condiciones
ALTER TABLE servicios
ADD CONSTRAINT check_condicion_resultante_valida
CHECK (
    condicion_resultante IS NULL OR
    condicion_resultante IN (
        'sano', 'caries', 'obturacion', 'corona', 'puente', 'implante',
        'ausente', 'extraccion_indicada', 'endodoncia', 'protesis',
        'fractura', 'mancha', 'desgaste', 'sensibilidad', 'movilidad',
        'impactado', 'en_erupcion', 'retenido', 'supernumerario', 'otro'
    )
);

-- PASO 3: Poblar condiciones por defecto según tipo de servicio
-- ============================================================

-- RESTAURATIVA: Obturaciones → "obturacion"
UPDATE servicios
SET condicion_resultante = 'obturacion'
WHERE (
    LOWER(nombre) LIKE '%obturaci%' OR
    LOWER(nombre) LIKE '%empaste%' OR
    LOWER(nombre) LIKE '%resina%'
)
AND condicion_resultante IS NULL;

-- CIRUGÍA: Extracciones → "ausente"
UPDATE servicios
SET condicion_resultante = 'ausente'
WHERE (
    LOWER(nombre) LIKE '%extracci%' OR
    LOWER(nombre) LIKE '%exodoncia%'
)
AND condicion_resultante IS NULL;

-- ENDODONCIA: Tratamiento de conducto → "endodoncia"
UPDATE servicios
SET condicion_resultante = 'endodoncia'
WHERE (
    LOWER(nombre) LIKE '%endodoncia%' OR
    LOWER(nombre) LIKE '%conducto%'
)
AND condicion_resultante IS NULL;

-- PRÓTESIS: Coronas → "corona"
UPDATE servicios
SET condicion_resultante = 'corona'
WHERE (
    LOWER(nombre) LIKE '%corona%' AND
    LOWER(nombre) NOT LIKE '%puente%'
)
AND condicion_resultante IS NULL;

-- PRÓTESIS: Puentes → "puente"
UPDATE servicios
SET condicion_resultante = 'puente'
WHERE LOWER(nombre) LIKE '%puente%'
AND condicion_resultante IS NULL;

-- IMPLANTES: Implantes dentales → "implante"
UPDATE servicios
SET condicion_resultante = 'implante'
WHERE LOWER(nombre) LIKE '%implante%'
AND condicion_resultante IS NULL;

-- PRÓTESIS: Prótesis removibles → "protesis"
UPDATE servicios
SET condicion_resultante = 'protesis'
WHERE (
    LOWER(nombre) LIKE '%pr%tesis%' OR
    LOWER(nombre) LIKE '%dentadura%'
)
AND condicion_resultante IS NULL;

-- PREVENTIVA: Servicios de boca completa → NULL (no modifican odontograma)
UPDATE servicios
SET condicion_resultante = NULL
WHERE alcance_servicio = 'boca_completa'
AND condicion_resultante IS NOT NULL;

-- PASO 4: Comentar en BD para referencia futura
COMMENT ON COLUMN servicios.condicion_resultante IS
'Condición que resulta en el odontograma después de aplicar este servicio. NULL = no modifica odontograma (ej: limpieza, blanqueamiento)';

-- PASO 5: Crear índice para búsquedas rápidas
CREATE INDEX IF NOT EXISTS idx_servicios_condicion_resultante
ON servicios(condicion_resultante)
WHERE condicion_resultante IS NOT NULL;

-- =====================================================
-- RESULTADO ESPERADO:
-- =====================================================
-- Servicios preventivos (limpieza, blanqueamiento): condicion_resultante = NULL
-- Obturaciones: condicion_resultante = 'obturacion'
-- Extracciones: condicion_resultante = 'ausente'
-- Endodoncias: condicion_resultante = 'endodoncia'
-- Coronas: condicion_resultante = 'corona'
-- Puentes: condicion_resultante = 'puente'
-- Implantes: condicion_resultante = 'implante'
-- Prótesis removibles: condicion_resultante = 'protesis'
-- =====================================================
