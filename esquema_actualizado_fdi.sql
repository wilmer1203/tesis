-- =====================================================
-- 🗄️ ESQUEMA ACTUALIZADO - SISTEMA ODONTOLÓGICO v4.2
-- =====================================================
-- Incluye nuevas tablas FDI implementadas
-- Fecha: 2025-09-13
-- Estado: Con catálogo FDI completo implementado
-- =====================================================

-- ==========================================
-- 📊 CONSULTA PARA VERIFICAR ESTADO ACTUAL
-- ==========================================

-- 🔍 Verificar todas las tablas existentes
SELECT 
    schemaname,
    tablename,
    tableowner,
    hasindexes,
    hasrules,
    hastriggers
FROM pg_tables 
WHERE schemaname = 'public'
ORDER BY tablename;

-- 🦷 Verificar catálogo FDI implementado
SELECT 
    'dientes' as tabla,
    COUNT(*) as total_registros,
    MIN(numero_fdi) as min_fdi,
    MAX(numero_fdi) as max_fdi
FROM dientes
UNION ALL
SELECT 
    'condiciones_diente' as tabla,
    COUNT(*) as total_registros,
    NULL as min_fdi,
    NULL as max_fdi
FROM condiciones_diente;

-- 🏗️ Verificar estructura de nuevas tablas FDI
SELECT 
    table_name,
    column_name,
    data_type,
    is_nullable,
    column_default
FROM information_schema.columns 
WHERE table_name IN ('dientes', 'condiciones_diente')
ORDER BY table_name, ordinal_position;

-- ==========================================
-- 🗄️ ESQUEMA ACTUAL COMPLETO
-- ==========================================

-- 👥 TABLA: usuarios (Supabase Auth integrada)
CREATE TABLE IF NOT EXISTS usuarios (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    nombre_completo VARCHAR(200),
    rol_id UUID REFERENCES roles(id),
    activo BOOLEAN DEFAULT true,
    fecha_creacion TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- 🏷️ TABLA: roles 
CREATE TABLE IF NOT EXISTS roles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nombre VARCHAR(50) UNIQUE NOT NULL,
    descripcion TEXT,
    permisos JSONB,
    activo BOOLEAN DEFAULT true,
    fecha_creacion TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- 👨‍⚕️ TABLA: personal
CREATE TABLE IF NOT EXISTS personal (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    usuario_id UUID REFERENCES usuarios(id),
    primer_nombre VARCHAR(100) NOT NULL,
    segundo_nombre VARCHAR(100),
    primer_apellido VARCHAR(100) NOT NULL,
    segundo_apellido VARCHAR(100),
    tipo_documento VARCHAR(20) DEFAULT 'CI',
    numero_documento VARCHAR(20) UNIQUE NOT NULL,
    telefono_1 VARCHAR(20),
    telefono_2 VARCHAR(20),
    email VARCHAR(255),
    direccion TEXT,
    fecha_nacimiento DATE,
    genero VARCHAR(20),
    tipo_personal VARCHAR(50) NOT NULL, -- odontologo, administrador, asistente
    especialidad VARCHAR(100),
    numero_colegio VARCHAR(50),
    acepta_pacientes_nuevos BOOLEAN DEFAULT true,
    estado_laboral VARCHAR(50) DEFAULT 'activo',
    salario_base DECIMAL(15,2),
    comision_porcentaje DECIMAL(5,2),
    activo BOOLEAN DEFAULT true,
    fecha_ingreso DATE DEFAULT CURRENT_DATE,
    fecha_creacion TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- 🏥 TABLA: pacientes
CREATE TABLE IF NOT EXISTS pacientes (
    numero_historia VARCHAR(20) PRIMARY KEY, -- Auto: HC000001, HC000002...
    tipo_documento VARCHAR(20) DEFAULT 'CI',
    numero_documento VARCHAR(20) UNIQUE NOT NULL,
    primer_nombre VARCHAR(100) NOT NULL,
    segundo_nombre VARCHAR(100),
    primer_apellido VARCHAR(100) NOT NULL,
    segundo_apellido VARCHAR(100),
    fecha_nacimiento DATE NOT NULL,
    edad INTEGER, -- Calculado automáticamente
    genero VARCHAR(20) NOT NULL,
    celular_1 VARCHAR(20),
    celular_2 VARCHAR(20),
    email VARCHAR(255),
    direccion_completa TEXT,
    contacto_emergencia JSONB, -- {nombre, telefono, relacion}
    informacion_medica JSONB, -- {alergias, medicamentos, condiciones}
    observaciones_generales TEXT,
    activo BOOLEAN DEFAULT true,
    registrado_por UUID REFERENCES usuarios(id),
    fecha_registro TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- 🦷 TABLA: servicios
CREATE TABLE IF NOT EXISTS servicios (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    codigo VARCHAR(20) UNIQUE NOT NULL, -- Auto: SER001, SER002...
    nombre VARCHAR(200) NOT NULL,
    descripcion TEXT,
    categoria VARCHAR(100) NOT NULL,
    precio_base DECIMAL(15,2) NOT NULL,
    precio_minimo DECIMAL(15,2),
    precio_maximo DECIMAL(15,2),
    duracion_estimada INTEGER, -- minutos
    instrucciones_preparacion TEXT,
    activo BOOLEAN DEFAULT true,
    fecha_creacion TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- 📅 TABLA: consultas (NÚCLEO - Sistema sin citas)
CREATE TABLE IF NOT EXISTS consultas (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    numero_consulta VARCHAR(30) UNIQUE NOT NULL, -- Auto: YYYYMMDD001, YYYYMMDD002...
    numero_historia VARCHAR(20) REFERENCES pacientes(numero_historia),
    primer_odontologo_id UUID REFERENCES usuarios(id),
    fecha_programada TIMESTAMPTZ NOT NULL, -- Momento de llegada
    orden_llegada_general INTEGER, -- Orden global del día
    orden_cola_odontologo INTEGER, -- Orden en cola específica
    tipo_consulta VARCHAR(50) DEFAULT 'general',
    estado VARCHAR(50) DEFAULT 'programada', -- programada, en_progreso, completada, cancelada
    motivo_consulta TEXT,
    observaciones_administrativas TEXT,
    fecha_inicio_atencion TIMESTAMPTZ,
    fecha_fin_atencion TIMESTAMPTZ,
    costo_total_estimado DECIMAL(15,2),
    costo_total_final DECIMAL(15,2),
    saldo_pendiente DECIMAL(15,2) DEFAULT 0,
    fecha_creacion TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- 🔧 TABLA: intervenciones (Múltiples odontólogos por consulta)
CREATE TABLE IF NOT EXISTS intervenciones (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    consulta_id UUID REFERENCES consultas(id),
    servicio_id UUID REFERENCES servicios(id),
    odontologo_id UUID REFERENCES usuarios(id),
    procedimiento_realizado TEXT NOT NULL,
    dientes_tratados JSONB, -- Array de números FDI
    materiales_utilizados JSONB,
    observaciones_tecnicas TEXT,
    complicaciones TEXT,
    recomendaciones TEXT,
    precio_final DECIMAL(15,2) NOT NULL,
    fecha_intervencion TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    duracion_minutos INTEGER,
    requiere_seguimiento BOOLEAN DEFAULT false,
    fecha_proximo_control DATE
);

-- 💳 TABLA: pagos
CREATE TABLE IF NOT EXISTS pagos (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    numero_recibo VARCHAR(30) UNIQUE NOT NULL, -- Auto: REC202509001, REC202509002...
    consulta_id UUID REFERENCES consultas(id),
    monto_total DECIMAL(15,2) NOT NULL,
    monto_pagado DECIMAL(15,2) NOT NULL,
    saldo_pendiente DECIMAL(15,2) DEFAULT 0, -- Calculado automáticamente
    metodo_pago VARCHAR(50) NOT NULL,
    detalles_pago JSONB, -- Referencia, banco, etc.
    descuento_aplicado DECIMAL(15,2) DEFAULT 0,
    impuesto_aplicado DECIMAL(15,2) DEFAULT 0,
    observaciones_pago TEXT,
    fecha_pago TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    procesado_por UUID REFERENCES usuarios(id),
    estado_pago VARCHAR(50) DEFAULT 'completado'
);

-- ==========================================
-- 🦷 NUEVAS TABLAS FDI - IMPLEMENTADAS v4.2
-- ==========================================

-- 🦷 TABLA: dientes (Catálogo FDI profesional)
CREATE TABLE IF NOT EXISTS dientes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    numero_fdi INTEGER UNIQUE NOT NULL, -- 11-18, 21-28, 31-38, 41-48
    nombre_diente VARCHAR(200) NOT NULL,
    cuadrante INTEGER NOT NULL, -- 1, 2, 3, 4
    tipo_diente VARCHAR(50) NOT NULL, -- incisivo, canino, premolar, molar
    coordenadas_svg JSONB, -- {x, y} para posicionamiento visual
    superficies_disponibles JSONB, -- ["mesial", "distal", "lingual", "vestibular", "oclusal/incisal"]
    descripcion_anatomica TEXT,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT valid_numero_fdi CHECK (
        numero_fdi IN (
            11, 12, 13, 14, 15, 16, 17, 18, -- Cuadrante 1
            21, 22, 23, 24, 25, 26, 27, 28, -- Cuadrante 2  
            31, 32, 33, 34, 35, 36, 37, 38, -- Cuadrante 3
            41, 42, 43, 44, 45, 46, 47, 48  -- Cuadrante 4
        )
    ),
    CONSTRAINT valid_cuadrante CHECK (cuadrante IN (1, 2, 3, 4)),
    CONSTRAINT valid_tipo_diente CHECK (tipo_diente IN ('incisivo', 'canino', 'premolar', 'molar'))
);

-- 🎨 TABLA: condiciones_diente (Estados dentales profesionales)
CREATE TABLE IF NOT EXISTS condiciones_diente (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nombre VARCHAR(100) NOT NULL,
    codigo VARCHAR(10) UNIQUE NOT NULL, -- SAO, CAR, OBT, COR, etc.
    color_hex VARCHAR(7) NOT NULL, -- #16a34a, #dc2626, etc.
    descripcion TEXT,
    categoria VARCHAR(50) NOT NULL, -- normal, patologia, restauracion, protesis, etc.
    es_urgente BOOLEAN DEFAULT false,
    instrucciones_tratamiento TEXT,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT valid_color_hex CHECK (color_hex ~ '^#[0-9A-Fa-f]{6}$'),
    CONSTRAINT valid_categoria CHECK (categoria IN ('normal', 'patologia', 'restauracion', 'protesis', 'ausencia', 'especialidad', 'trauma', 'periodontal'))
);

-- 📋 TABLA: odontogramas (Versionado automático)
CREATE TABLE IF NOT EXISTS odontogramas (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    numero_historia VARCHAR(20) REFERENCES pacientes(numero_historia),
    version INTEGER NOT NULL DEFAULT 1,
    id_version_anterior UUID REFERENCES odontogramas(id),
    id_intervencion_origen UUID REFERENCES intervenciones(id),
    es_version_actual BOOLEAN DEFAULT true,
    motivo_nueva_version TEXT,
    tipo_odontograma VARCHAR(50) DEFAULT 'adulto', -- adulto, pediatrico
    dientes_estados JSONB NOT NULL, -- {numero_fdi: {condicion, codigo, superficie, color}}
    notas_generales TEXT,
    observaciones_clinicas TEXT,
    fecha_creacion TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    odontologo_id UUID REFERENCES usuarios(id),
    
    CONSTRAINT valid_tipo_odontograma CHECK (tipo_odontograma IN ('adulto', 'pediatrico')),
    CONSTRAINT unique_version_actual_per_patient UNIQUE (numero_historia, es_version_actual) DEFERRABLE INITIALLY DEFERRED
);

-- 🩺 TABLA: historial_medico (Evolución clínica)
CREATE TABLE IF NOT EXISTS historial_medico (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    numero_historia VARCHAR(20) REFERENCES pacientes(numero_historia),
    consulta_id UUID REFERENCES consultas(id),
    tipo_entrada VARCHAR(50) NOT NULL, -- consulta, control, urgencia, seguimiento
    sintomas_principales TEXT,
    diagnostico_preliminar TEXT,
    diagnostico_definitivo TEXT,
    tratamiento_realizado TEXT,
    medicamentos_prescritos JSONB,
    recomendaciones TEXT,
    proximo_control DATE,
    observaciones_evolucion TEXT,
    signos_vitales JSONB, -- {presion, pulso, temperatura}
    fecha_entrada TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    registrado_por UUID REFERENCES usuarios(id),
    
    CONSTRAINT valid_tipo_entrada CHECK (tipo_entrada IN ('consulta', 'control', 'urgencia', 'seguimiento', 'cirugia', 'interconsulta'))
);

-- 📷 TABLA: imagenes_clinicas (Radiografías y fotografías)
CREATE TABLE IF NOT EXISTS imagenes_clinicas (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    numero_historia VARCHAR(20) REFERENCES pacientes(numero_historia),
    consulta_id UUID REFERENCES consultas(id),
    tipo_imagen VARCHAR(50) NOT NULL, -- radiografia, fotografia, scanner
    subtipo VARCHAR(100), -- panoramica, periapical, bite-wing, etc.
    url_archivo TEXT NOT NULL,
    nombre_archivo VARCHAR(255),
    tamano_archivo INTEGER, -- bytes
    formato_archivo VARCHAR(10), -- jpg, png, dicom
    dientes_visibles JSONB, -- Array de números FDI
    hallazgos_importantes TEXT,
    fecha_toma TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    tomada_por UUID REFERENCES usuarios(id),
    es_imagen_principal BOOLEAN DEFAULT false,
    
    CONSTRAINT valid_tipo_imagen CHECK (tipo_imagen IN ('radiografia', 'fotografia', 'scanner', 'modelo_3d')),
    CONSTRAINT valid_formato CHECK (formato_archivo IN ('jpg', 'jpeg', 'png', 'dicom', 'pdf'))
);

-- ⚙️ TABLA: configuracion_sistema (Settings dinámicos)
CREATE TABLE IF NOT EXISTS configuracion_sistema (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    clave VARCHAR(100) UNIQUE NOT NULL,
    valor JSONB NOT NULL,
    descripcion TEXT,
    categoria VARCHAR(50) NOT NULL,
    es_publico BOOLEAN DEFAULT false, -- Si puede ser accedido sin autenticación
    modificado_por UUID REFERENCES usuarios(id),
    fecha_modificacion TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT valid_categoria_config CHECK (categoria IN ('general', 'ui', 'notificaciones', 'integraciones', 'seguridad', 'reportes'))
);

-- 📊 TABLA: auditoria (Log completo del sistema)
CREATE TABLE IF NOT EXISTS auditoria (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tabla_afectada VARCHAR(100) NOT NULL,
    registro_id UUID, -- ID del registro afectado
    accion VARCHAR(20) NOT NULL, -- INSERT, UPDATE, DELETE
    datos_anteriores JSONB,
    datos_nuevos JSONB,
    usuario_id UUID REFERENCES usuarios(id),
    ip_address INET,
    user_agent TEXT,
    modulo VARCHAR(50), -- pacientes, consultas, pagos, etc.
    descripcion_accion TEXT,
    fecha_accion TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT valid_accion CHECK (accion IN ('INSERT', 'UPDATE', 'DELETE', 'SELECT', 'LOGIN', 'LOGOUT'))
);

-- ==========================================
-- 🚀 ÍNDICES PARA PERFORMANCE OPTIMIZADA
-- ==========================================

-- Índices principales
CREATE INDEX IF NOT EXISTS idx_pacientes_documento ON pacientes(numero_documento);
CREATE INDEX IF NOT EXISTS idx_pacientes_nombres ON pacientes(primer_nombre, primer_apellido);
CREATE INDEX IF NOT EXISTS idx_consultas_fecha ON consultas(fecha_programada);
CREATE INDEX IF NOT EXISTS idx_consultas_estado ON consultas(estado);
CREATE INDEX IF NOT EXISTS idx_consultas_odontologo ON consultas(primer_odontologo_id);
CREATE INDEX IF NOT EXISTS idx_intervenciones_consulta ON intervenciones(consulta_id);
CREATE INDEX IF NOT EXISTS idx_pagos_consulta ON pagos(consulta_id);
CREATE INDEX IF NOT EXISTS idx_personal_tipo ON personal(tipo_personal);
CREATE INDEX IF NOT EXISTS idx_servicios_categoria ON servicios(categoria);

-- Índices FDI nuevos
CREATE INDEX IF NOT EXISTS idx_dientes_cuadrante ON dientes(cuadrante);
CREATE INDEX IF NOT EXISTS idx_dientes_tipo ON dientes(tipo_diente);
CREATE INDEX IF NOT EXISTS idx_dientes_fdi ON dientes(numero_fdi);
CREATE INDEX IF NOT EXISTS idx_condiciones_categoria ON condiciones_diente(categoria);
CREATE INDEX IF NOT EXISTS idx_condiciones_urgente ON condiciones_diente(es_urgente);
CREATE INDEX IF NOT EXISTS idx_odontogramas_paciente ON odontogramas(numero_historia);
CREATE INDEX IF NOT EXISTS idx_odontogramas_actual ON odontogramas(es_version_actual) WHERE es_version_actual = true;
CREATE INDEX IF NOT EXISTS idx_historial_paciente ON historial_medico(numero_historia);
CREATE INDEX IF NOT EXISTS idx_imagenes_paciente ON imagenes_clinicas(numero_historia);

-- Índices de auditoría
CREATE INDEX IF NOT EXISTS idx_auditoria_tabla ON auditoria(tabla_afectada);
CREATE INDEX IF NOT EXISTS idx_auditoria_fecha ON auditoria(fecha_accion);
CREATE INDEX IF NOT EXISTS idx_auditoria_usuario ON auditoria(usuario_id);

-- ==========================================
-- 🤖 TRIGGERS AUTOMÁTICOS IMPLEMENTADOS
-- ==========================================

-- Triggers para auto-numeración (ya implementados)
-- - trigger_generar_numero_historia
-- - trigger_generar_numero_consulta  
-- - trigger_generar_numero_recibo

-- Triggers para cálculos automáticos
-- - trigger_calcular_edad_paciente
-- - trigger_calcular_saldo_pendiente

-- Triggers para timestamps
-- - trigger_*_fecha_actualizacion (en múltiples tablas)

-- ==========================================
-- 📈 VISTAS OPTIMIZADAS
-- ==========================================

-- Vista: Personal completo con roles
CREATE OR REPLACE VIEW vista_personal_completo AS
SELECT 
    p.id,
    p.primer_nombre || ' ' || p.primer_apellido as nombre_completo,
    p.numero_documento,
    p.tipo_personal,
    p.especialidad,
    p.acepta_pacientes_nuevos,
    p.estado_laboral,
    u.email,
    r.nombre as rol_nombre,
    p.activo,
    p.fecha_ingreso
FROM personal p
LEFT JOIN usuarios u ON p.usuario_id = u.id
LEFT JOIN roles r ON u.rol_id = r.id
WHERE p.activo = true;

-- Vista: Consultas del día con información completa
CREATE OR REPLACE VIEW vista_consultas_dia AS
SELECT 
    c.id,
    c.numero_consulta,
    c.numero_historia,
    p.primer_nombre || ' ' || p.primer_apellido as nombre_paciente,
    c.primer_odontologo_id,
    pe.primer_nombre || ' ' || pe.primer_apellido as nombre_odontologo,
    c.fecha_programada,
    c.orden_llegada_general,
    c.orden_cola_odontologo,
    c.estado,
    c.tipo_consulta,
    c.motivo_consulta,
    c.costo_total_final,
    c.saldo_pendiente
FROM consultas c
JOIN pacientes p ON c.numero_historia = p.numero_historia
LEFT JOIN personal pe ON c.primer_odontologo_id = pe.usuario_id
WHERE DATE(c.fecha_programada) = CURRENT_DATE
ORDER BY c.orden_llegada_general;

-- Vista: Estadísticas FDI por cuadrante
CREATE OR REPLACE VIEW vista_estadisticas_fdi AS
SELECT 
    cuadrante,
    COUNT(*) as total_dientes,
    COUNT(CASE WHEN tipo_diente = 'incisivo' THEN 1 END) as incisivos,
    COUNT(CASE WHEN tipo_diente = 'canino' THEN 1 END) as caninos,
    COUNT(CASE WHEN tipo_diente = 'premolar' THEN 1 END) as premolares,
    COUNT(CASE WHEN tipo_diente = 'molar' THEN 1 END) as molares,
    STRING_AGG(CAST(numero_fdi AS TEXT), ', ' ORDER BY numero_fdi) as dientes_fdi
FROM dientes
GROUP BY cuadrante
ORDER BY cuadrante;

-- ==========================================
-- 🔒 ROW LEVEL SECURITY (PREPARADO)
-- ==========================================

-- Habilitar RLS en tablas sensibles (comentado para implementar gradualmente)
/*
ALTER TABLE pacientes ENABLE ROW LEVEL SECURITY;
ALTER TABLE consultas ENABLE ROW LEVEL SECURITY;
ALTER TABLE intervenciones ENABLE ROW LEVEL SECURITY;
ALTER TABLE pagos ENABLE ROW LEVEL SECURITY;
ALTER TABLE odontogramas ENABLE ROW LEVEL SECURITY;
ALTER TABLE historial_medico ENABLE ROW LEVEL SECURITY;

-- Políticas por rol (ejemplo)
CREATE POLICY "gerente_full_access" ON pacientes FOR ALL TO gerente;
CREATE POLICY "admin_crud_pacientes" ON pacientes FOR SELECT, INSERT, UPDATE TO administrador;
CREATE POLICY "odontologo_read_own_patients" ON consultas FOR SELECT TO odontologo 
    USING (primer_odontologo_id = auth.uid());
*/

-- ==========================================
-- 📝 DATOS INICIALES ESENCIALES
-- ==========================================

-- Roles del sistema (4 roles básicos)
INSERT INTO roles (id, nombre, descripcion, permisos) VALUES
('550e8400-e29b-41d4-a716-446655440001', 'gerente', 'Acceso total al sistema', '{"all": ["*"]}'),
('550e8400-e29b-41d4-a716-446655440002', 'administrador', 'Gestión operativa', '{"pacientes": ["crear", "leer", "actualizar"], "consultas": ["crear", "leer", "actualizar"], "pagos": ["crear", "leer", "actualizar"]}'),
('550e8400-e29b-41d4-a716-446655440003', 'odontologo', 'Atención clínica', '{"consultas": ["leer", "actualizar"], "odontologia": ["crear", "leer", "actualizar"], "pacientes": ["leer"]}'),
('550e8400-e29b-41d4-a716-446655440004', 'asistente', 'Apoyo básico', '{"consultas": ["leer"], "pacientes": ["leer"]}')
ON CONFLICT (id) DO NOTHING;

-- ==========================================
-- 📊 RESUMEN DEL ESQUEMA v4.2
-- ==========================================

/*
TABLAS PRINCIPALES: 15 tablas
- usuarios, roles, personal (3) - Gestión de usuarios
- pacientes, consultas, intervenciones, pagos (4) - Flujo principal  
- servicios (1) - Catálogo
- dientes, condiciones_diente, odontogramas (3) - FDI avanzado
- historial_medico, imagenes_clinicas (2) - Historia clínica
- configuracion_sistema, auditoria (2) - Sistema

CARACTERÍSTICAS:
✅ Auto-numeración: HC, consultas, recibos
✅ Catálogo FDI: 32 dientes profesionales  
✅ Versionado: Odontogramas automático
✅ Triggers: 12+ funciones automáticas
✅ Índices: 20+ índices optimizados
✅ Vistas: 3 vistas especializadas
✅ RLS: Preparado para activar
✅ Auditoría: Log completo de cambios

ESTADO: ✅ IMPLEMENTADO Y FUNCIONANDO
*/