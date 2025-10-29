-- =====================================================
-- MIGRACIÓN: Agregar campo alcance_servicio
-- =====================================================
-- Fecha: 2025-01-10
-- Propósito: Diferenciar servicios por alcance de aplicación

-- PASO 1: Agregar columna alcance_servicio
ALTER TABLE servicios
ADD COLUMN alcance_servicio VARCHAR(20) DEFAULT 'superficie_especifica' NOT NULL;

-- PASO 2: Agregar constraint para validar valores
ALTER TABLE servicios
ADD CONSTRAINT chk_alcance_servicio
CHECK (alcance_servicio IN ('superficie_especifica', 'diente_completo', 'boca_completa'));

-- PASO 3: Crear índice para optimizar búsquedas por alcance
CREATE INDEX idx_servicios_alcance ON servicios(alcance_servicio);

-- PASO 4: Actualizar servicios existentes con alcance correcto
UPDATE servicios SET alcance_servicio = 'diente_completo'
WHERE nombre ILIKE '%extracci%'
   OR nombre ILIKE '%implante%'
   OR nombre ILIKE '%exodoncia%';

UPDATE servicios SET alcance_servicio = 'boca_completa'
WHERE nombre ILIKE '%blanqueamiento%'
   OR nombre ILIKE '%limpieza dental%'
   OR nombre ILIKE '%limpieza bucal%'
   OR nombre ILIKE '%profilaxis%'
   OR nombre ILIKE '%fluorización%';

-- PASO 5: Comentarios descriptivos
COMMENT ON COLUMN servicios.alcance_servicio IS '
Alcance de aplicación del servicio:
- superficie_especifica: Se aplica a superficies individuales (oclusal, mesial, etc.)
- diente_completo: Se aplica al diente completo (extracción, corona, implante)
- boca_completa: Se aplica a toda la boca (blanqueamiento, limpieza, profilaxis)
';

-- =====================================================
-- VERIFICACIÓN
-- =====================================================
-- Mostrar distribución de servicios por alcance
SELECT
    alcance_servicio,
    COUNT(*) as total_servicios,
    STRING_AGG(nombre, ', ' ORDER BY nombre LIMIT 3) as ejemplos
FROM servicios
GROUP BY alcance_servicio
ORDER BY alcance_servicio;
