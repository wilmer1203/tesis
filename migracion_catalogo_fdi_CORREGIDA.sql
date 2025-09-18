-- 🦷 MIGRACIÓN CORREGIDA: CATÁLOGO FDI COMPATIBLE CON ESQUEMA EXISTENTE
-- Versión: 1.1 - AJUSTADA AL ESQUEMA esquema_final_corregido.sql
-- Fecha: Septiembre 2025

-- ==========================================
-- ⚠️ NOTAS IMPORTANTES:
-- Esta migración respeta EXACTAMENTE el esquema existente
-- Los campos nuevos se agregan solo si no existen
-- ==========================================

-- ==========================================
-- 🔧 PASO 1: AGREGAR CAMPOS FALTANTES A TABLA dientes
-- ==========================================

-- Agregar campos para sistema FDI avanzado
ALTER TABLE dientes ADD COLUMN IF NOT EXISTS coordenadas_svg JSONB;
ALTER TABLE dientes ADD COLUMN IF NOT EXISTS superficies_disponibles TEXT[];

-- Crear índice para performance de búsquedas FDI
CREATE INDEX IF NOT EXISTS idx_dientes_numero_diente ON dientes(numero_diente);
CREATE INDEX IF NOT EXISTS idx_dientes_tipo ON dientes(tipo_diente);

-- ==========================================
-- 📊 PASO 2: POBLAR CATÁLOGO DE DIENTES FDI (ESQUEMA COMPATIBLE)
-- ==========================================

-- Limpiar datos existentes para evitar conflictos
DELETE FROM dientes WHERE numero_diente BETWEEN 11 AND 48;

-- Insertar 32 dientes FDI usando campos del esquema existente
INSERT INTO dientes (
    numero_diente, 
    nombre, 
    tipo_diente, 
    ubicacion, 
    cuadrante,
    caras,
    coordenadas_svg,
    superficies_disponibles,
    es_temporal,
    posicion_en_cuadrante
) VALUES

-- 🔸 CUADRANTE 1: Superior Derecho (11-18)
(11, 'Incisivo Central Superior Derecho', 'incisivo', 'superior_derecha', 1, 
 ARRAY['mesial', 'distal', 'lingual', 'vestibular', 'incisal'], 
 '{"x": 120, "y": 50}', 
 ARRAY['mesial', 'distal', 'lingual', 'vestibular', 'incisal'], FALSE, 1),

(12, 'Incisivo Lateral Superior Derecho', 'incisivo', 'superior_derecha', 1, 
 ARRAY['mesial', 'distal', 'lingual', 'vestibular', 'incisal'], 
 '{"x": 150, "y": 52}', 
 ARRAY['mesial', 'distal', 'lingual', 'vestibular', 'incisal'], FALSE, 2),

(13, 'Canino Superior Derecho', 'canino', 'superior_derecha', 1, 
 ARRAY['mesial', 'distal', 'lingual', 'vestibular', 'incisal'], 
 '{"x": 180, "y": 55}', 
 ARRAY['mesial', 'distal', 'lingual', 'vestibular', 'incisal'], FALSE, 3),

(14, 'Primer Premolar Superior Derecho', 'premolar', 'superior_derecha', 1, 
 ARRAY['mesial', 'distal', 'lingual', 'vestibular', 'oclusal'], 
 '{"x": 210, "y": 58}', 
 ARRAY['mesial', 'distal', 'lingual', 'vestibular', 'oclusal'], FALSE, 4),

(15, 'Segundo Premolar Superior Derecho', 'premolar', 'superior_derecha', 1, 
 ARRAY['mesial', 'distal', 'lingual', 'vestibular', 'oclusal'], 
 '{"x": 240, "y": 60}', 
 ARRAY['mesial', 'distal', 'lingual', 'vestibular', 'oclusal'], FALSE, 5),

(16, 'Primer Molar Superior Derecho', 'molar', 'superior_derecha', 1, 
 ARRAY['mesial', 'distal', 'lingual', 'vestibular', 'oclusal'], 
 '{"x": 270, "y": 65}', 
 ARRAY['mesial', 'distal', 'lingual', 'vestibular', 'oclusal'], FALSE, 6),

(17, 'Segundo Molar Superior Derecho', 'molar', 'superior_derecha', 1, 
 ARRAY['mesial', 'distal', 'lingual', 'vestibular', 'oclusal'], 
 '{"x": 300, "y": 70}', 
 ARRAY['mesial', 'distal', 'lingual', 'vestibular', 'oclusal'], FALSE, 7),

(18, 'Tercer Molar Superior Derecho', 'molar', 'superior_derecha', 1, 
 ARRAY['mesial', 'distal', 'lingual', 'vestibular', 'oclusal'], 
 '{"x": 330, "y": 75}', 
 ARRAY['mesial', 'distal', 'lingual', 'vestibular', 'oclusal'], FALSE, 8),

-- 🔸 CUADRANTE 2: Superior Izquierdo (21-28)
(21, 'Incisivo Central Superior Izquierdo', 'incisivo', 'superior_izquierda', 2, 
 ARRAY['mesial', 'distal', 'lingual', 'vestibular', 'incisal'], 
 '{"x": 80, "y": 50}', 
 ARRAY['mesial', 'distal', 'lingual', 'vestibular', 'incisal'], FALSE, 1),

(22, 'Incisivo Lateral Superior Izquierdo', 'incisivo', 'superior_izquierda', 2, 
 ARRAY['mesial', 'distal', 'lingual', 'vestibular', 'incisal'], 
 '{"x": 50, "y": 52}', 
 ARRAY['mesial', 'distal', 'lingual', 'vestibular', 'incisal'], FALSE, 2),

(23, 'Canino Superior Izquierdo', 'canino', 'superior_izquierda', 2, 
 ARRAY['mesial', 'distal', 'lingual', 'vestibular', 'incisal'], 
 '{"x": 20, "y": 55}', 
 ARRAY['mesial', 'distal', 'lingual', 'vestibular', 'incisal'], FALSE, 3),

(24, 'Primer Premolar Superior Izquierdo', 'premolar', 'superior_izquierda', 2, 
 ARRAY['mesial', 'distal', 'lingual', 'vestibular', 'oclusal'], 
 '{"x": -10, "y": 58}', 
 ARRAY['mesial', 'distal', 'lingual', 'vestibular', 'oclusal'], FALSE, 4),

(25, 'Segundo Premolar Superior Izquierdo', 'premolar', 'superior_izquierda', 2, 
 ARRAY['mesial', 'distal', 'lingual', 'vestibular', 'oclusal'], 
 '{"x": -40, "y": 60}', 
 ARRAY['mesial', 'distal', 'lingual', 'vestibular', 'oclusal'], FALSE, 5),

(26, 'Primer Molar Superior Izquierdo', 'molar', 'superior_izquierda', 2, 
 ARRAY['mesial', 'distal', 'lingual', 'vestibular', 'oclusal'], 
 '{"x": -70, "y": 65}', 
 ARRAY['mesial', 'distal', 'lingual', 'vestibular', 'oclusal'], FALSE, 6),

(27, 'Segundo Molar Superior Izquierdo', 'molar', 'superior_izquierda', 2, 
 ARRAY['mesial', 'distal', 'lingual', 'vestibular', 'oclusal'], 
 '{"x": -100, "y": 70}', 
 ARRAY['mesial', 'distal', 'lingual', 'vestibular', 'oclusal'], FALSE, 7),

(28, 'Tercer Molar Superior Izquierdo', 'molar', 'superior_izquierda', 2, 
 ARRAY['mesial', 'distal', 'lingual', 'vestibular', 'oclusal'], 
 '{"x": -130, "y": 75}', 
 ARRAY['mesial', 'distal', 'lingual', 'vestibular', 'oclusal'], FALSE, 8),

-- 🔸 CUADRANTE 3: Inferior Izquierdo (31-38)
(31, 'Incisivo Central Inferior Izquierdo', 'incisivo', 'inferior_izquierda', 3, 
 ARRAY['mesial', 'distal', 'lingual', 'vestibular', 'incisal'], 
 '{"x": 80, "y": 150}', 
 ARRAY['mesial', 'distal', 'lingual', 'vestibular', 'incisal'], FALSE, 1),

(32, 'Incisivo Lateral Inferior Izquierdo', 'incisivo', 'inferior_izquierda', 3, 
 ARRAY['mesial', 'distal', 'lingual', 'vestibular', 'incisal'], 
 '{"x": 50, "y": 148}', 
 ARRAY['mesial', 'distal', 'lingual', 'vestibular', 'incisal'], FALSE, 2),

(33, 'Canino Inferior Izquierdo', 'canino', 'inferior_izquierda', 3, 
 ARRAY['mesial', 'distal', 'lingual', 'vestibular', 'incisal'], 
 '{"x": 20, "y": 145}', 
 ARRAY['mesial', 'distal', 'lingual', 'vestibular', 'incisal'], FALSE, 3),

(34, 'Primer Premolar Inferior Izquierdo', 'premolar', 'inferior_izquierda', 3, 
 ARRAY['mesial', 'distal', 'lingual', 'vestibular', 'oclusal'], 
 '{"x": -10, "y": 142}', 
 ARRAY['mesial', 'distal', 'lingual', 'vestibular', 'oclusal'], FALSE, 4),

(35, 'Segundo Premolar Inferior Izquierdo', 'premolar', 'inferior_izquierda', 3, 
 ARRAY['mesial', 'distal', 'lingual', 'vestibular', 'oclusal'], 
 '{"x": -40, "y": 140}', 
 ARRAY['mesial', 'distal', 'lingual', 'vestibular', 'oclusal'], FALSE, 5),

(36, 'Primer Molar Inferior Izquierdo', 'molar', 'inferior_izquierda', 3, 
 ARRAY['mesial', 'distal', 'lingual', 'vestibular', 'oclusal'], 
 '{"x": -70, "y": 135}', 
 ARRAY['mesial', 'distal', 'lingual', 'vestibular', 'oclusal'], FALSE, 6),

(37, 'Segundo Molar Inferior Izquierdo', 'molar', 'inferior_izquierda', 3, 
 ARRAY['mesial', 'distal', 'lingual', 'vestibular', 'oclusal'], 
 '{"x": -100, "y": 130}', 
 ARRAY['mesial', 'distal', 'lingual', 'vestibular', 'oclusal'], FALSE, 7),

(38, 'Tercer Molar Inferior Izquierdo', 'molar', 'inferior_izquierda', 3, 
 ARRAY['mesial', 'distal', 'lingual', 'vestibular', 'oclusal'], 
 '{"x": -130, "y": 125}', 
 ARRAY['mesial', 'distal', 'lingual', 'vestibular', 'oclusal'], FALSE, 8),

-- 🔸 CUADRANTE 4: Inferior Derecho (41-48)
(41, 'Incisivo Central Inferior Derecho', 'incisivo', 'inferior_derecha', 4, 
 ARRAY['mesial', 'distal', 'lingual', 'vestibular', 'incisal'], 
 '{"x": 120, "y": 150}', 
 ARRAY['mesial', 'distal', 'lingual', 'vestibular', 'incisal'], FALSE, 1),

(42, 'Incisivo Lateral Inferior Derecho', 'incisivo', 'inferior_derecha', 4, 
 ARRAY['mesial', 'distal', 'lingual', 'vestibular', 'incisal'], 
 '{"x": 150, "y": 148}', 
 ARRAY['mesial', 'distal', 'lingual', 'vestibular', 'incisal'], FALSE, 2),

(43, 'Canino Inferior Derecho', 'canino', 'inferior_derecha', 4, 
 ARRAY['mesial', 'distal', 'lingual', 'vestibular', 'incisal'], 
 '{"x": 180, "y": 145}', 
 ARRAY['mesial', 'distal', 'lingual', 'vestibular', 'incisal'], FALSE, 3),

(44, 'Primer Premolar Inferior Derecho', 'premolar', 'inferior_derecha', 4, 
 ARRAY['mesial', 'distal', 'lingual', 'vestibular', 'oclusal'], 
 '{"x": 210, "y": 142}', 
 ARRAY['mesial', 'distal', 'lingual', 'vestibular', 'oclusal'], FALSE, 4),

(45, 'Segundo Premolar Inferior Derecho', 'premolar', 'inferior_derecha', 4, 
 ARRAY['mesial', 'distal', 'lingual', 'vestibular', 'oclusal'], 
 '{"x": 240, "y": 140}', 
 ARRAY['mesial', 'distal', 'lingual', 'vestibular', 'oclusal'], FALSE, 5),

(46, 'Primer Molar Inferior Derecho', 'molar', 'inferior_derecha', 4, 
 ARRAY['mesial', 'distal', 'lingual', 'vestibular', 'oclusal'], 
 '{"x": 270, "y": 135}', 
 ARRAY['mesial', 'distal', 'lingual', 'vestibular', 'oclusal'], FALSE, 6),

(47, 'Segundo Molar Inferior Derecho', 'molar', 'inferior_derecha', 4, 
 ARRAY['mesial', 'distal', 'lingual', 'vestibular', 'oclusal'], 
 '{"x": 300, "y": 130}', 
 ARRAY['mesial', 'distal', 'lingual', 'vestibular', 'oclusal'], FALSE, 7),

(48, 'Tercer Molar Inferior Derecho', 'molar', 'inferior_derecha', 4, 
 ARRAY['mesial', 'distal', 'lingual', 'vestibular', 'oclusal'], 
 '{"x": 330, "y": 125}', 
 ARRAY['mesial', 'distal', 'lingual', 'vestibular', 'oclusal'], FALSE, 8);

-- ==========================================
-- 🔧 PASO 3: AGREGAR CAMPOS FALTANTES A condiciones_diente
-- ==========================================

-- Agregar campos para sistema de condiciones avanzado
ALTER TABLE condiciones_diente ADD COLUMN IF NOT EXISTS nombre_condicion VARCHAR(100);
ALTER TABLE condiciones_diente ADD COLUMN IF NOT EXISTS codigo_condicion VARCHAR(10);
ALTER TABLE condiciones_diente ADD COLUMN IF NOT EXISTS categoria VARCHAR(50) DEFAULT 'normal';
ALTER TABLE condiciones_diente ADD COLUMN IF NOT EXISTS es_urgente BOOLEAN DEFAULT FALSE;
ALTER TABLE condiciones_diente ADD COLUMN IF NOT EXISTS color_hex VARCHAR(7) DEFAULT '#16a34a';

-- Crear índices para performance
CREATE INDEX IF NOT EXISTS idx_condiciones_tipo ON condiciones_diente(tipo_condicion);
CREATE INDEX IF NOT EXISTS idx_condiciones_codigo ON condiciones_diente(codigo_condicion);
CREATE INDEX IF NOT EXISTS idx_condiciones_urgente ON condiciones_diente(es_urgente);

-- ==========================================
-- 🎨 PASO 4: POBLAR CATÁLOGO DE CONDICIONES MÉDICAS
-- ==========================================

-- Actualizar condiciones existentes con códigos y colores profesionales
UPDATE condiciones_diente SET 
    codigo_condicion = 'SAO',
    nombre_condicion = 'Sano',
    categoria = 'normal',
    es_urgente = FALSE,
    color_hex = '#16a34a'
WHERE tipo_condicion = 'sano';

UPDATE condiciones_diente SET 
    codigo_condicion = 'CAR',
    nombre_condicion = 'Caries',
    categoria = 'patologia',
    es_urgente = TRUE,
    color_hex = '#dc2626'
WHERE tipo_condicion = 'caries';

UPDATE condiciones_diente SET 
    codigo_condicion = 'OBT',
    nombre_condicion = 'Obturado',
    categoria = 'restauracion',
    es_urgente = FALSE,
    color_hex = '#2563eb'
WHERE tipo_condicion = 'obturacion';

UPDATE condiciones_diente SET 
    codigo_condicion = 'COR',
    nombre_condicion = 'Corona',
    categoria = 'protesis',
    es_urgente = FALSE,
    color_hex = '#d97706'
WHERE tipo_condicion = 'corona';

UPDATE condiciones_diente SET 
    codigo_condicion = 'AUS',
    nombre_condicion = 'Ausente',
    categoria = 'ausencia',
    es_urgente = FALSE,
    color_hex = '#6b7280'
WHERE tipo_condicion = 'ausente';

-- Agregar nuevas condiciones avanzadas si no existen
INSERT INTO condiciones_diente (
    tipo_condicion, codigo_condicion, nombre_condicion, categoria, es_urgente, color_hex,
    descripcion, severidad
) VALUES
('endodoncia', 'ENDO', 'Endodoncia', 'especialidad', FALSE, '#7c3aed', 'Tratamiento endodóntico realizado', 'leve'),
('implante', 'IMP', 'Implante', 'protesis', FALSE, '#059669', 'Implante osteointegrado', 'leve'),
('fractura', 'FRAC', 'Fracturado', 'trauma', TRUE, '#ea580c', 'Fractura dental', 'severa'),
('movilidad', 'MOV', 'Movilidad', 'periodontal', TRUE, '#e11d48', 'Movilidad dental patológica', 'moderada')
ON CONFLICT (tipo_condicion) DO NOTHING;

-- ==========================================
-- 📊 PASO 5: CREAR ÍNDICES PARA PERFORMANCE AVANZADA
-- ==========================================

-- Índices compuestos para consultas complejas
CREATE INDEX IF NOT EXISTS idx_dientes_cuadrante_tipo ON dientes(cuadrante, tipo_diente);
CREATE INDEX IF NOT EXISTS idx_condiciones_categoria_urgente ON condiciones_diente(categoria, es_urgente);

-- Índices para campos JSONB
CREATE INDEX IF NOT EXISTS idx_dientes_coordenadas_svg ON dientes USING GIN (coordenadas_svg);

-- ==========================================
-- ✅ PASO 6: VERIFICACIÓN DE MIGRACIÓN
-- ==========================================

-- Verificar que se insertaron los 32 dientes FDI
SELECT 
    cuadrante,
    COUNT(*) as total_dientes,
    STRING_AGG(CAST(numero_diente AS TEXT), ', ' ORDER BY numero_diente) as dientes_fdi
FROM dientes 
WHERE numero_diente BETWEEN 11 AND 48
GROUP BY cuadrante 
ORDER BY cuadrante;

-- Verificar condiciones con códigos
SELECT 
    categoria,
    COUNT(*) as total_condiciones,
    STRING_AGG(CONCAT(codigo_condicion, ':', nombre_condicion), ', ') as condiciones
FROM condiciones_diente 
WHERE codigo_condicion IS NOT NULL
GROUP BY categoria 
ORDER BY categoria;

-- ==========================================
-- 📝 PASO 7: COMENTARIOS Y DOCUMENTACIÓN
-- ==========================================

COMMENT ON COLUMN dientes.coordenadas_svg IS '📍 Coordenadas SVG para posicionamiento preciso del diente en el odontograma';
COMMENT ON COLUMN dientes.superficies_disponibles IS '🦷 Array de superficies anatómicas disponibles para este tipo de diente';
COMMENT ON COLUMN condiciones_diente.codigo_condicion IS '🏷️ Código estándar médico de la condición (SAO, CAR, OBT, etc.)';
COMMENT ON COLUMN condiciones_diente.categoria IS '📂 Categoría médica: normal, patologia, restauracion, protesis, ausencia, etc.';
COMMENT ON COLUMN condiciones_diente.es_urgente IS '🚨 Indica si la condición requiere atención médica urgente';
COMMENT ON COLUMN condiciones_diente.color_hex IS '🎨 Color hexadecimal para representación visual en UI médica';

-- ==========================================
-- 🎉 MIGRACIÓN COMPLETADA EXITOSAMENTE
-- ==========================================

-- Mostrar resumen final
SELECT 
    '🎉 MIGRACIÓN FDI COMPLETADA' as estado,
    (SELECT COUNT(*) FROM dientes WHERE numero_diente BETWEEN 11 AND 48) as dientes_fdi,
    (SELECT COUNT(*) FROM condiciones_diente WHERE codigo_condicion IS NOT NULL) as condiciones_con_codigo,
    CURRENT_TIMESTAMP as fecha_migracion;