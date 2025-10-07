-- =====================================================
-- 🔄 MIGRACIÓN: SIMPLIFICAR ODONTOGRAMA A MODELO PLANO
-- =====================================================
-- Fecha: 2025-10-07
-- Objetivo: Eliminar complejidad de sistema de versiones
--           Modelo directo: paciente → condiciones_diente
-- =====================================================

BEGIN;

-- =====================================================
-- PASO 1: RESPALDAR DATOS ACTUALES
-- =====================================================

-- Crear tabla temporal con datos actuales
CREATE TEMP TABLE condiciones_backup AS
SELECT
    c.id,
    o.paciente_id,
    d.numero_diente as diente_numero,
    c.tipo_condicion,
    c.caras_afectadas,
    c.severidad,
    c.descripcion,
    c.observaciones,
    c.material_utilizado,
    c.color_material,
    c.fecha_tratamiento,
    c.estado,
    c.fecha_registro,
    c.registrado_por,
    c.intervencion_origen_id,
    c.color_hex
FROM condiciones_diente c
JOIN odontograma o ON c.odontograma_id = o.id
JOIN dientes d ON c.diente_id = d.id
WHERE o.es_version_actual = TRUE  -- Solo versiones actuales
  AND c.estado = 'actual';         -- Solo condiciones activas

-- Log de respaldo
DO $$
BEGIN
    RAISE NOTICE 'Respaldadas % condiciones actuales', (SELECT COUNT(*) FROM condiciones_backup);
END $$;


-- =====================================================
-- PASO 2: ELIMINAR TABLA ODONTOGRAMA (YA NO NECESARIA)
-- =====================================================

-- Primero eliminar constraint FK en condiciones_diente
ALTER TABLE condiciones_diente
DROP CONSTRAINT IF EXISTS condiciones_diente_odontograma_id_fkey;

-- Eliminar tabla odontograma completa
DROP TABLE IF EXISTS odontograma CASCADE;

RAISE NOTICE 'Tabla odontograma eliminada';


-- =====================================================
-- PASO 3: RECREAR TABLA CONDICIONES_DIENTE SIMPLIFICADA
-- =====================================================

-- Eliminar tabla vieja
DROP TABLE IF EXISTS condiciones_diente CASCADE;

-- Crear tabla nueva PLANA
CREATE TABLE condiciones_diente (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    -- 🔗 RELACIONES DIRECTAS (SIN odontograma intermedio)
    paciente_id UUID REFERENCES pacientes(id) ON DELETE CASCADE NOT NULL,
    diente_numero INTEGER NOT NULL,  -- 11-48 FDI directo (sin FK a tabla dientes)
    superficie VARCHAR(20) NOT NULL CHECK (superficie IN ('oclusal', 'mesial', 'distal', 'vestibular', 'lingual', 'incisal')),

    -- 🦷 CONDICIÓN DEL DIENTE
    tipo_condicion VARCHAR(50) NOT NULL CHECK (tipo_condicion IN (
        'sano', 'caries', 'obturacion', 'corona', 'puente', 'implante',
        'ausente', 'extraccion_indicada', 'endodoncia', 'protesis',
        'fractura', 'mancha', 'desgaste', 'sensibilidad', 'movilidad',
        'impactado', 'en_erupcion', 'retenido', 'supernumerario', 'otro'
    )),
    severidad VARCHAR(20) DEFAULT 'leve' CHECK (severidad IN ('leve', 'moderada', 'severa')),

    -- 📝 DETALLES DE LA INTERVENCIÓN
    descripcion TEXT,
    observaciones TEXT,
    material_utilizado VARCHAR(100),
    tecnica_utilizada VARCHAR(100),
    color_material VARCHAR(50),
    fecha_tratamiento DATE,

    -- 👨‍⚕️ TRAZABILIDAD
    intervencion_id UUID REFERENCES intervenciones(id) ON DELETE SET NULL,
    registrado_por UUID REFERENCES usuarios(id),
    fecha_registro TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL,

    -- ✅ ESTADO (activo = actual, false = histórico)
    activo BOOLEAN DEFAULT TRUE NOT NULL,

    -- 🎨 RENDERIZADO
    color_hex VARCHAR(7) DEFAULT '#90EE90',  -- Verde = sano por defecto

    -- 📊 METADATA
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,

    -- Constraint: Un diente-superficie solo puede tener UNA condición activa
    CONSTRAINT unique_active_condition UNIQUE (paciente_id, diente_numero, superficie, activo)
        WHERE (activo = TRUE)
);

-- Índices para rendimiento
CREATE INDEX idx_condiciones_paciente_activo ON condiciones_diente(paciente_id, activo);
CREATE INDEX idx_condiciones_intervencion ON condiciones_diente(intervencion_id);
CREATE INDEX idx_condiciones_diente_numero ON condiciones_diente(diente_numero);
CREATE INDEX idx_condiciones_fecha ON condiciones_diente(fecha_registro DESC);

-- Comentarios de documentación
COMMENT ON TABLE condiciones_diente IS 'Condiciones odontológicas por paciente (modelo plano simplificado)';
COMMENT ON COLUMN condiciones_diente.activo IS 'TRUE = condición actual, FALSE = histórico';
COMMENT ON COLUMN condiciones_diente.diente_numero IS 'Número FDI directo (11-48 para adultos)';

RAISE NOTICE 'Tabla condiciones_diente recreada (modelo plano)';


-- =====================================================
-- PASO 4: RESTAURAR DATOS DESDE RESPALDO
-- =====================================================

INSERT INTO condiciones_diente (
    paciente_id,
    diente_numero,
    superficie,
    tipo_condicion,
    severidad,
    descripcion,
    observaciones,
    material_utilizado,
    color_material,
    fecha_tratamiento,
    fecha_registro,
    registrado_por,
    intervencion_id,
    color_hex,
    activo
)
SELECT
    cb.paciente_id,
    cb.diente_numero,
    UNNEST(cb.caras_afectadas) as superficie,  -- Expandir array de caras
    cb.tipo_condicion,
    cb.severidad,
    cb.descripcion,
    cb.observaciones,
    cb.material_utilizado,
    cb.color_material,
    cb.fecha_tratamiento,
    cb.fecha_registro,
    cb.registrado_por,
    cb.intervencion_origen_id,
    cb.color_hex,
    TRUE  -- Todas activas (son las actuales del respaldo)
FROM condiciones_backup cb;

-- Log de migración
DO $$
DECLARE
    total_migradas INTEGER;
BEGIN
    SELECT COUNT(*) INTO total_migradas FROM condiciones_diente;
    RAISE NOTICE 'Migradas % condiciones al nuevo modelo', total_migradas;
END $$;


-- =====================================================
-- PASO 5: FUNCIÓN PARA AUTO-CREAR ODONTOGRAMA INICIAL
-- =====================================================

CREATE OR REPLACE FUNCTION crear_odontograma_inicial()
RETURNS TRIGGER AS $$
DECLARE
    diente INTEGER;
    superficie TEXT;
    total_creadas INTEGER := 0;
BEGIN
    -- Crear 32 dientes × 5 superficies = 160 condiciones "sano"
    FOR diente IN
        -- Cuadrante 1 (Superior Derecho): 18-11
        SELECT unnest(ARRAY[18, 17, 16, 15, 14, 13, 12, 11])
        UNION ALL
        -- Cuadrante 2 (Superior Izquierdo): 21-28
        SELECT unnest(ARRAY[21, 22, 23, 24, 25, 26, 27, 28])
        UNION ALL
        -- Cuadrante 3 (Inferior Izquierdo): 31-38
        SELECT unnest(ARRAY[31, 32, 33, 34, 35, 36, 37, 38])
        UNION ALL
        -- Cuadrante 4 (Inferior Derecho): 41-48
        SELECT unnest(ARRAY[41, 42, 43, 44, 45, 46, 47, 48])
    LOOP
        FOR superficie IN SELECT unnest(ARRAY['oclusal', 'mesial', 'distal', 'vestibular', 'lingual'])
        LOOP
            INSERT INTO condiciones_diente (
                paciente_id,
                diente_numero,
                superficie,
                tipo_condicion,
                severidad,
                descripcion,
                color_hex,
                activo
            ) VALUES (
                NEW.id,
                diente,
                superficie,
                'sano',
                'leve',
                'Condición inicial',
                '#90EE90',  -- Verde
                TRUE
            );

            total_creadas := total_creadas + 1;
        END LOOP;
    END LOOP;

    RAISE NOTICE 'Odontograma inicial creado para paciente %: % condiciones', NEW.numero_historia, total_creadas;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION crear_odontograma_inicial() IS 'Crea automáticamente 160 condiciones "sano" al crear un paciente';


-- =====================================================
-- PASO 6: TRIGGER PARA AUTO-CREAR AL INSERTAR PACIENTE
-- =====================================================

DROP TRIGGER IF EXISTS trigger_crear_odontograma_inicial ON pacientes;

CREATE TRIGGER trigger_crear_odontograma_inicial
    AFTER INSERT ON pacientes
    FOR EACH ROW
    EXECUTE FUNCTION crear_odontograma_inicial();

COMMENT ON TRIGGER trigger_crear_odontograma_inicial ON pacientes IS
    'Auto-crea odontograma con 160 condiciones "sano" al crear paciente nuevo';

RAISE NOTICE 'Trigger de auto-creación de odontograma configurado';


-- =====================================================
-- PASO 7: FUNCIÓN HELPER PARA ACTUALIZAR CONDICIÓN
-- =====================================================

CREATE OR REPLACE FUNCTION actualizar_condicion_diente(
    p_paciente_id UUID,
    p_diente_numero INTEGER,
    p_superficie VARCHAR(20),
    p_nueva_condicion VARCHAR(50),
    p_intervencion_id UUID DEFAULT NULL,
    p_material VARCHAR(100) DEFAULT NULL,
    p_descripcion TEXT DEFAULT NULL,
    p_registrado_por UUID DEFAULT NULL
) RETURNS UUID AS $$
DECLARE
    nueva_condicion_id UUID;
BEGIN
    -- PASO 1: Desactivar condición anterior (marcar como histórica)
    UPDATE condiciones_diente
    SET activo = FALSE,
        updated_at = CURRENT_TIMESTAMP
    WHERE paciente_id = p_paciente_id
      AND diente_numero = p_diente_numero
      AND superficie = p_superficie
      AND activo = TRUE;

    -- PASO 2: Insertar nueva condición como activa
    INSERT INTO condiciones_diente (
        paciente_id,
        diente_numero,
        superficie,
        tipo_condicion,
        material_utilizado,
        descripcion,
        intervencion_id,
        registrado_por,
        activo
    ) VALUES (
        p_paciente_id,
        p_diente_numero,
        p_superficie,
        p_nueva_condicion,
        p_material,
        p_descripcion,
        p_intervencion_id,
        p_registrado_por,
        TRUE
    ) RETURNING id INTO nueva_condicion_id;

    RETURN nueva_condicion_id;
END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION actualizar_condicion_diente IS
    'Actualiza condición de un diente: desactiva anterior + crea nueva (mantiene historial)';


-- =====================================================
-- PASO 8: VISTA PARA ODONTOGRAMA ACTUAL DEL PACIENTE
-- =====================================================

CREATE OR REPLACE VIEW vista_odontograma_actual AS
SELECT
    c.paciente_id,
    p.numero_historia,
    p.nombres || ' ' || p.apellidos as paciente_nombre,
    c.diente_numero,
    c.superficie,
    c.tipo_condicion,
    c.severidad,
    c.material_utilizado,
    c.color_hex,
    c.fecha_registro,
    c.intervencion_id
FROM condiciones_diente c
JOIN pacientes p ON c.paciente_id = p.id
WHERE c.activo = TRUE
ORDER BY p.numero_historia, c.diente_numero, c.superficie;

COMMENT ON VIEW vista_odontograma_actual IS 'Odontograma actual (solo condiciones activas) de todos los pacientes';


-- =====================================================
-- PASO 9: LIMPIEZA Y VERIFICACIÓN
-- =====================================================

-- Eliminar tabla temporal
DROP TABLE IF EXISTS condiciones_backup;

-- Estadísticas finales
DO $$
DECLARE
    total_pacientes INTEGER;
    total_condiciones INTEGER;
    total_activas INTEGER;
BEGIN
    SELECT COUNT(*) INTO total_pacientes FROM pacientes;
    SELECT COUNT(*) INTO total_condiciones FROM condiciones_diente;
    SELECT COUNT(*) INTO total_activas FROM condiciones_diente WHERE activo = TRUE;

    RAISE NOTICE '============================================';
    RAISE NOTICE 'MIGRACIÓN COMPLETADA EXITOSAMENTE';
    RAISE NOTICE '============================================';
    RAISE NOTICE 'Pacientes en sistema: %', total_pacientes;
    RAISE NOTICE 'Condiciones totales: %', total_condiciones;
    RAISE NOTICE 'Condiciones activas: %', total_activas;
    RAISE NOTICE 'Condiciones históricas: %', total_condiciones - total_activas;
    RAISE NOTICE '============================================';
END $$;

COMMIT;

-- =====================================================
-- 🎯 RESULTADO ESPERADO:
-- =====================================================
-- ✅ Tabla odontograma eliminada
-- ✅ Tabla condiciones_diente simplificada (modelo plano)
-- ✅ Datos migrados preservando condiciones actuales
-- ✅ Trigger auto-crea 160 condiciones "sano" al crear paciente
-- ✅ Función helper para actualizar condiciones manteniendo historial
-- ✅ Vista para consultar odontograma actual rápidamente
-- =====================================================
