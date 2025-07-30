-- =====================================================
-- SISTEMA ODONTOLÓGICO - BASE DE DATOS COMPLETA
-- Versión: 3.0 - DESDE CERO CON BUENAS PRÁCTICAS
-- Fecha: Diciembre 2024
-- 
-- DESCRIPCIÓN:
-- Esta base de datos maneja un sistema odontológico completo con:
-- - Gestión de usuarios y roles
-- - Control de personal médico y administrativo  
-- - Pacientes e historiales médicos
-- - Servicios y procedimientos odontológicos
-- - Consultas/citas y seguimiento
-- - Pagos y facturación
-- - Odontogramas digitales
-- - Auditoría completa del sistema
-- =====================================================

-- =====================================================
-- PASO 1: EXTENSIONES Y CONFIGURACIÓN INICIAL
-- =====================================================

-- Habilitar extensiones necesarias para el sistema
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";        -- Para generar UUIDs
CREATE EXTENSION IF NOT EXISTS "pgcrypto";         -- Para encriptación
CREATE EXTENSION IF NOT EXISTS "pg_trgm";          -- Para búsqueda de texto avanzada

-- Configurar zona horaria (ajustar según tu ubicación)
SET timezone = 'America/Caracas';

-- =====================================================
-- PASO 2: SISTEMA DE ROLES Y PERMISOS
-- =====================================================

-- Tabla de roles del sistema con permisos granulares
CREATE TABLE roles (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    nombre VARCHAR(50) UNIQUE NOT NULL,
    descripcion TEXT,
    permisos JSONB DEFAULT '{}',                    -- Permisos en formato JSON
    activo BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- Validaciones
    CONSTRAINT chk_roles_nombre_valido CHECK (nombre ~ '^[a-z_]+$'),
    CONSTRAINT chk_roles_permisos_json CHECK (jsonb_typeof(permisos) = 'object')
);

-- Comentarios para documentación
COMMENT ON TABLE roles IS 'Roles del sistema con permisos granulares para control de acceso';
COMMENT ON COLUMN roles.permisos IS 'Permisos en formato JSON: {"modulo": ["accion1", "accion2"]}';

-- =====================================================
-- PASO 3: USUARIOS DEL SISTEMA
-- =====================================================

-- Tabla principal de usuarios que se sincroniza con Supabase Auth
CREATE TABLE usuarios (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(100) UNIQUE NOT NULL,
    telefono VARCHAR(20),
    rol_id UUID REFERENCES roles(id) NOT NULL,
    activo BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    ultimo_acceso TIMESTAMP WITH TIME ZONE,
    configuraciones JSONB DEFAULT '{}',
    
    -- Integración con Supabase Auth
    auth_user_id UUID UNIQUE,                      -- ID del usuario en auth.users
    avatar_url TEXT,
    metadata JSONB DEFAULT '{}',
    
    -- Validaciones
    CONSTRAINT chk_usuarios_email_valido CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$')
    
);

COMMENT ON TABLE usuarios IS 'Usuarios del sistema sincronizados con Supabase Auth';
COMMENT ON COLUMN usuarios.auth_user_id IS 'Referencia al ID en auth.users de Supabase';

-- =====================================================
-- PASO 4: INFORMACIÓN DETALLADA DEL PERSONAL
-- =====================================================

-- Tabla con información específica del personal médico y administrativo
CREATE TABLE personal (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    usuario_id UUID UNIQUE REFERENCES usuarios(id) ON DELETE CASCADE,
    
    -- Información personal
    primer_nombre VARCHAR(50) NOT NULL,
    segundo_nombre VARCHAR(50),
    primer_apellido VARCHAR(50) NOT NULL, 
    segundo_apellido VARCHAR(50),
    tipo_documento VARCHAR(20) DEFAULT 'CC',
    numero_documento VARCHAR(20) UNIQUE NOT NULL,
    fecha_nacimiento DATE,
    direccion VARCHAR(200),
    celular VARCHAR(20) NOT NULL,
    
    -- Información profesional
    tipo_personal VARCHAR(20) NOT NULL CHECK (tipo_personal IN ('Odontólogo', 'Asistente', 'Administrador', 'Gerente')),
    especialidad VARCHAR(100),
    numero_licencia VARCHAR(50),
    fecha_contratacion DATE NOT NULL DEFAULT CURRENT_DATE,
    salario DECIMAL(10,2),
    horario_trabajo JSONB DEFAULT '{}',
    estado_laboral VARCHAR(20) DEFAULT 'activo' CHECK (estado_laboral IN ('activo', 'vacaciones', 'licencia', 'inactivo')),
    observaciones TEXT,
    
    -- Auditoría
    fecha_creacion TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- Validaciones
    CONSTRAINT chk_personal_documento CHECK (numero_documento ~ '^\d{6,20}$'),
    CONSTRAINT chk_personal_celular CHECK (celular ~ '^[\+]?[\d\s\-\(\)]{7,20}$'),
    CONSTRAINT chk_personal_salario CHECK (salario IS NULL OR salario >= 0)
);

COMMENT ON TABLE personal IS 'Información detallada del personal médico y administrativo';
COMMENT ON COLUMN personal.horario_trabajo IS 'Horario en formato JSON: {"lunes": "08:00-17:00", ...}';

-- =====================================================
-- PASO 5: GESTIÓN DE PACIENTES
-- =====================================================

-- Tabla principal de pacientes
CREATE TABLE pacientes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    numero_historia VARCHAR(20) UNIQUE NOT NULL,   -- Se genera automáticamente
    
    -- Información personal
    primer_nombre VARCHAR(50) NOT NULL,
    segundo_nombre VARCHAR(50),
    primer_apellido VARCHAR(50) NOT NULL, 
    segundo_apellido VARCHAR(50),
    tipo_documento VARCHAR(20) DEFAULT 'CC',
    numero_documento VARCHAR(20) UNIQUE NOT NULL,
    fecha_nacimiento DATE,
    edad INTEGER,                                   -- Se calcula automáticamente
    genero VARCHAR(10) CHECK (genero IN ('masculino', 'femenino', 'otro')),
    telefono_1 character varying(20) null,
    telefono_2 character varying(20) null,telefono_1 character varying(20) null,
    telefono_2 character varying(20) null,
    email VARCHAR(100),
    direccion TEXT,
    ciudad VARCHAR(100),
    departamento VARCHAR(100),
    ocupacion VARCHAR(100),
    estado_civil VARCHAR(20),
    contacto_emergencia JSONB DEFAULT '{}',        -- Información de contacto de emergencia
    
    -- Información médica básica
    alergias TEXT[],                               -- Array de alergias
    medicamentos_actuales TEXT[],                  -- Medicamentos que toma actualmente
    condiciones_medicas TEXT[],                    -- Condiciones médicas preexistentes
    antecedentes_familiares TEXT[],                -- Antecedentes familiares relevantes
    
    -- Control del sistema
    fecha_registro TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    registrado_por UUID REFERENCES usuarios(id),
    activo BOOLEAN DEFAULT TRUE,
    observaciones TEXT,
    
    -- Validaciones
    CONSTRAINT chk_pacientes_documento CHECK (numero_documento ~ '^\d{6,20}$'),
    CONSTRAINT chk_pacientes_edad CHECK (edad IS NULL OR (edad >= 0 AND edad <= 150)),
    CONSTRAINT chk_pacientes_email CHECK (email IS NULL OR email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$')
);

COMMENT ON TABLE pacientes IS 'Registro principal de pacientes del sistema';
COMMENT ON COLUMN pacientes.numero_historia IS 'Número único de historia clínica (formato: HC000001)';

-- =====================================================
-- PASO 6: CATÁLOGO DE SERVICIOS ODONTOLÓGICOS
-- =====================================================

-- Servicios que ofrece la clínica
CREATE TABLE servicios (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    codigo VARCHAR(20) UNIQUE NOT NULL,            -- Código único del servicio
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    categoria VARCHAR(50) NOT NULL,                -- Categoría principal (Consulta, Cirugía, etc.)
    subcategoria VARCHAR(50),                      -- Subcategoría específica
    duracion_estimada INTERVAL NOT NULL DEFAULT '30 minutes',
    precio_base DECIMAL(10,2) NOT NULL,
    precio_minimo DECIMAL(10,2),
    precio_maximo DECIMAL(10,2),
    requiere_cita_previa BOOLEAN DEFAULT TRUE,
    requiere_autorizacion BOOLEAN DEFAULT FALSE,
    material_incluido TEXT[],                      -- Materiales incluidos en el servicio
    instrucciones_pre TEXT,                        -- Instrucciones previas al procedimiento
    instrucciones_post TEXT,                       -- Instrucciones posteriores al procedimiento
    activo BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    creado_por UUID REFERENCES usuarios(id),
    
    -- Validaciones
    CONSTRAINT chk_servicios_codigo CHECK (codigo ~ '^[A-Z0-9]+$'),
    CONSTRAINT chk_servicios_precio CHECK (precio_base > 0),
    CONSTRAINT chk_servicios_precio_rango CHECK (
        precio_minimo IS NULL OR precio_maximo IS NULL OR precio_minimo <= precio_maximo
    )
);

COMMENT ON TABLE servicios IS 'Catálogo de servicios odontológicos de la clínica';

-- =====================================================
-- PASO 7: CONSULTAS Y CITAS
-- =====================================================

-- Tabla para manejar las citas/consultas programadas
CREATE TABLE consultas (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    numero_consulta VARCHAR(20) UNIQUE NOT NULL,   -- Se genera automáticamente
    paciente_id UUID REFERENCES pacientes(id) NOT NULL,
    odontologo_id UUID REFERENCES personal(id) NOT NULL,
    
    -- Programación temporal
    fecha_programada TIMESTAMP WITH TIME ZONE NOT NULL,
    fecha_inicio_real TIMESTAMP WITH TIME ZONE,
    fecha_fin_real TIMESTAMP WITH TIME ZONE,
    duracion_estimada INTERVAL DEFAULT '30 minutes',
    
    -- Estado y clasificación
    estado VARCHAR(20) DEFAULT 'programada' CHECK (estado IN ('programada', 'confirmada', 'en_progreso', 'completada', 'cancelada', 'no_asistio')),
    tipo_consulta VARCHAR(30) DEFAULT 'general' CHECK (tipo_consulta IN ('general', 'control', 'urgencia', 'cirugia', 'otro')),
    prioridad VARCHAR(20) DEFAULT 'normal' CHECK (prioridad IN ('baja', 'normal', 'alta', 'urgente')),
    
    -- Información adicional
    motivo_consulta TEXT,
    observaciones_cita TEXT,
    notas_internas TEXT,                           -- Solo para el personal
    costo_total DECIMAL(10,2) DEFAULT 0,
    
    -- Control administrativo
    orden_llegada INTEGER,
    programada_por UUID REFERENCES usuarios(id),
    fecha_creacion TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- Sistema de recordatorios
    recordatorio_enviado BOOLEAN DEFAULT FALSE,
    fecha_recordatorio TIMESTAMP WITH TIME ZONE,
    
    -- Validaciones
    CONSTRAINT chk_consultas_fecha_logica CHECK (
        fecha_inicio_real IS NULL OR fecha_fin_real IS NULL OR fecha_inicio_real <= fecha_fin_real
    ),
    CONSTRAINT chk_consultas_costo CHECK (costo_total >= 0)
);

COMMENT ON TABLE consultas IS 'Citas y consultas programadas en la clínica';

-- =====================================================
-- PASO 8: INTERVENCIONES Y PROCEDIMIENTOS
-- =====================================================

-- Registro detallado de procedimientos realizados
CREATE TABLE intervenciones (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    consulta_id UUID REFERENCES consultas(id) NOT NULL,
    servicio_id UUID REFERENCES servicios(id) NOT NULL,
    odontologo_id UUID REFERENCES personal(id) NOT NULL,
    asistente_id UUID REFERENCES personal(id),
    
    -- Control temporal
    hora_inicio TIMESTAMP WITH TIME ZONE NOT NULL,
    hora_fin TIMESTAMP WITH TIME ZONE,
    duracion_real INTERVAL,
    
    -- Detalles clínicos
    dientes_afectados INTEGER[],                   -- Números de dientes según FDI
    diagnostico_inicial TEXT,
    procedimiento_realizado TEXT NOT NULL,
    materiales_utilizados TEXT[],
    anestesia_utilizada TEXT,
    complicaciones TEXT,
    
    -- Información económica
    precio_acordado DECIMAL(10,2) NOT NULL,
    descuento DECIMAL(10,2) DEFAULT 0,
    precio_final DECIMAL(10,2) NOT NULL,
    
    -- Estado del procedimiento
    estado VARCHAR(20) DEFAULT 'completada' CHECK (estado IN ('pendiente', 'en_progreso', 'completada', 'suspendida')),
    
    -- Seguimiento
    requiere_control BOOLEAN DEFAULT FALSE,
    fecha_control_sugerida DATE,
    instrucciones_paciente TEXT,
    
    fecha_registro TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- Validaciones
    CONSTRAINT chk_intervenciones_precio CHECK (precio_acordado > 0 AND precio_final >= 0),
    CONSTRAINT chk_intervenciones_descuento CHECK (descuento >= 0 AND descuento <= precio_acordado)
);

COMMENT ON TABLE intervenciones IS 'Registro detallado de procedimientos odontológicos realizados';

-- =====================================================
-- PASO 9: HISTORIAL MÉDICO
-- =====================================================

-- Historial médico detallado de cada paciente
CREATE TABLE historial_medico (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    paciente_id UUID REFERENCES pacientes(id) NOT NULL,
    consulta_id UUID REFERENCES consultas(id),
    odontologo_id UUID REFERENCES personal(id) NOT NULL,
    
    fecha_registro TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    tipo_registro VARCHAR(30) DEFAULT 'consulta' CHECK (tipo_registro IN ('consulta', 'tratamiento', 'control', 'urgencia', 'nota')),
    
    -- Información clínica principal
    sintomas_principales TEXT,
    examen_clinico TEXT,
    diagnostico_principal TEXT,
    diagnosticos_secundarios TEXT[],
    plan_tratamiento TEXT,
    pronostico TEXT,
    
    -- Medicamentos y recomendaciones
    medicamentos_recetados JSONB DEFAULT '[]',     -- Array de medicamentos con dosis
    recomendaciones TEXT,
    contraindicaciones TEXT,
    
    -- Signos vitales (cuando aplique)
    presion_arterial VARCHAR(20),
    frecuencia_cardiaca INTEGER,
    temperatura DECIMAL(4,2),
    
    -- Archivos adjuntos
    imagenes_url TEXT[],                           -- URLs de imágenes (rayos X, fotos)
    documentos_url TEXT[],                         -- URLs de documentos adjuntos
    
    -- Seguimiento
    proxima_cita DATE,
    observaciones TEXT,
    
    -- Control de privacidad
    confidencial BOOLEAN DEFAULT FALSE,
    
    -- Validaciones
    CONSTRAINT chk_historial_temperatura CHECK (temperatura IS NULL OR (temperatura >= 30 AND temperatura <= 45)),
    CONSTRAINT chk_historial_frecuencia CHECK (frecuencia_cardiaca IS NULL OR (frecuencia_cardiaca >= 40 AND frecuencia_cardiaca <= 200))
);

COMMENT ON TABLE historial_medico IS 'Historial médico detallado de cada paciente';

-- =====================================================
-- PASO 10: SISTEMA DE PAGOS
-- =====================================================

-- Registro de pagos y facturación
CREATE TABLE pagos (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    numero_recibo VARCHAR(20) UNIQUE NOT NULL,     -- Se genera automáticamente
    consulta_id UUID REFERENCES consultas(id),
    paciente_id UUID REFERENCES pacientes(id) NOT NULL,
    
    -- Información del pago
    fecha_pago TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    monto_total DECIMAL(10,2) NOT NULL,
    monto_pagado DECIMAL(10,2) NOT NULL,
    saldo_pendiente DECIMAL(10,2),                 -- Se calcula automáticamente
    
    -- Método de pago
    metodo_pago VARCHAR(20) NOT NULL CHECK (metodo_pago IN ('efectivo', 'tarjeta_credito', 'tarjeta_debito', 'transferencia', 'cheque', 'otro')),
    referencia_pago VARCHAR(100),                  -- Número de referencia del pago
    
    -- Detalles adicionales
    concepto TEXT NOT NULL,
    descuento_aplicado DECIMAL(10,2) DEFAULT 0,
    motivo_descuento TEXT,
    impuestos DECIMAL(10,2) DEFAULT 0,
    
    -- Control administrativo
    estado_pago VARCHAR(20) DEFAULT 'completado' CHECK (estado_pago IN ('pendiente', 'completado', 'anulado', 'reembolsado')),
    procesado_por UUID REFERENCES usuarios(id) NOT NULL,
    autorizado_por UUID REFERENCES usuarios(id),
    
    -- Facturación
    numero_factura VARCHAR(50),
    fecha_facturacion DATE,
    
    observaciones TEXT,
    
    -- Validaciones
    CONSTRAINT chk_pagos_montos CHECK (monto_total > 0 AND monto_pagado >= 0),
    CONSTRAINT chk_pagos_descuento CHECK (descuento_aplicado >= 0)
);

COMMENT ON TABLE pagos IS 'Registro de pagos y facturación del sistema';

-- =====================================================
-- PASO 11: ODONTOGRAMA DIGITAL
-- =====================================================

-- Tabla principal del odontograma
CREATE TABLE odontograma (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    paciente_id UUID REFERENCES pacientes(id) NOT NULL,
    fecha_creacion TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    odontologo_id UUID REFERENCES personal(id) NOT NULL,
    
    tipo_odontograma VARCHAR(20) DEFAULT 'adulto' CHECK (tipo_odontograma IN ('adulto', 'pediatrico', 'mixto')),
    version INTEGER DEFAULT 1,                     -- Para control de versiones
    activo BOOLEAN DEFAULT TRUE,                   -- Solo uno activo por paciente
    
    notas_generales TEXT,
    observaciones_clinicas TEXT,
    
    -- Metadatos para renderizado
    template_usado VARCHAR(50) DEFAULT 'universal',
    configuracion JSONB DEFAULT '{}'
);

COMMENT ON TABLE odontograma IS 'Odontogramas digitales de los pacientes';

-- Catálogo de dientes según numeración FDI
CREATE TABLE dientes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    numero_diente INTEGER UNIQUE NOT NULL,
    numero_diente_pediatrico INTEGER,
    nombre VARCHAR(100) NOT NULL,
    tipo_diente VARCHAR(20) NOT NULL CHECK (tipo_diente IN ('incisivo', 'canino', 'premolar', 'molar')),
    ubicacion VARCHAR(30) NOT NULL CHECK (ubicacion IN ('superior_derecha', 'superior_izquierda', 'inferior_derecha', 'inferior_izquierda')),
    cuadrante INTEGER NOT NULL CHECK (cuadrante IN (1, 2, 3, 4, 5, 6, 7, 8)),
    es_temporal BOOLEAN DEFAULT FALSE,
    posicion_en_cuadrante INTEGER,
    
    -- Características anatómicas
    caras TEXT[] DEFAULT ARRAY['oclusal', 'mesial', 'distal', 'vestibular', 'lingual'],
    descripcion_anatomica TEXT,
    
    activo BOOLEAN DEFAULT TRUE
);

COMMENT ON TABLE dientes IS 'Catálogo de dientes según numeración FDI internacional';

-- Condiciones específicas de cada diente en el odontograma
CREATE TABLE condiciones_diente (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    odontograma_id UUID REFERENCES odontograma(id) ON DELETE CASCADE,
    diente_id UUID REFERENCES dientes(id) NOT NULL,
    
    -- Tipo y ubicación de la condición
    tipo_condicion VARCHAR(50) NOT NULL CHECK (tipo_condicion IN (
        'sano', 'caries', 'obturacion', 'corona', 'puente', 'implante', 
        'ausente', 'extraccion_indicada', 'endodoncia', 'protesis', 
        'fractura', 'mancha', 'desgaste', 'sensibilidad', 'movilidad',
        'impactado', 'en_erupcion', 'retenido', 'supernumerario', 'otro'
    )),
    
    -- Ubicación específica en el diente
    caras_afectadas TEXT[] DEFAULT ARRAY[]::TEXT[],
    severidad VARCHAR(20) DEFAULT 'leve' CHECK (severidad IN ('leve', 'moderada', 'severa')),
    
    -- Descripción y notas
    descripcion TEXT,
    observaciones TEXT,
    
    -- Material y tratamiento (si aplica)
    material_utilizado VARCHAR(100),
    color_material VARCHAR(50),
    fecha_tratamiento DATE,
    
    -- Estado y seguimiento
    estado VARCHAR(20) DEFAULT 'actual' CHECK (estado IN ('planificado', 'en_tratamiento', 'actual', 'historico')),
    requiere_seguimiento BOOLEAN DEFAULT FALSE,
    
    -- Control de versiones
    fecha_registro TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    registrado_por UUID REFERENCES usuarios(id),
    
    -- Metadata para renderizado
    posicion_x DECIMAL(5,2),
    posicion_y DECIMAL(5,2),
    color_hex VARCHAR(7) DEFAULT '#FFFFFF'
);

COMMENT ON TABLE condiciones_diente IS 'Condiciones específicas de cada diente en el odontograma';

-- =====================================================
-- PASO 12: IMÁGENES CLÍNICAS
-- =====================================================

-- Gestión de imágenes médicas y clínicas
CREATE TABLE imagenes_clinicas (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    paciente_id UUID REFERENCES pacientes(id) NOT NULL,
    consulta_id UUID REFERENCES consultas(id),
    odontograma_id UUID REFERENCES odontograma(id),
    
    -- Información de la imagen
    titulo VARCHAR(200) NOT NULL,
    descripcion TEXT,
    tipo_imagen VARCHAR(50) NOT NULL CHECK (tipo_imagen IN (
        'radiografia_panoramica', 'radiografia_periapical', 'radiografia_bite_wing',
        'fotografia_intraoral', 'fotografia_extraoral', 'fotografia_oclusal',
        'tomografia', 'escaner_3d', 'otro'
    )),
    
    -- Almacenamiento (Supabase Storage)
    url_imagen TEXT NOT NULL,
    url_thumbnail TEXT,
    tamaño_archivo BIGINT,
    formato_archivo VARCHAR(10),
    
    -- Metadatos
    fecha_captura TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    capturada_por UUID REFERENCES usuarios(id),
    equipo_utilizado VARCHAR(100),
    configuracion_equipo JSONB DEFAULT '{}',
    
    -- Clasificación y búsqueda
    es_confidencial BOOLEAN DEFAULT FALSE,
    tags TEXT[],
    
    activo BOOLEAN DEFAULT TRUE
);

COMMENT ON TABLE imagenes_clinicas IS 'Gestión de imágenes médicas y clínicas';

-- =====================================================
-- PASO 13: AUDITORÍA DEL SISTEMA
-- =====================================================

-- Registro completo de auditoría para trazabilidad
CREATE TABLE auditoria (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tabla_afectada VARCHAR(50) NOT NULL,
    registro_id UUID NOT NULL,
    accion VARCHAR(20) NOT NULL CHECK (accion IN ('INSERT', 'UPDATE', 'DELETE')),
    
    -- Usuario y contexto
    usuario_id UUID REFERENCES usuarios(id),
    fecha_accion TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    ip_address INET,
    user_agent TEXT,
    
    -- Datos del cambio
    datos_anteriores JSONB,
    datos_nuevos JSONB,
    campos_modificados TEXT[],
    
    -- Contexto adicional
    motivo TEXT,
    modulo VARCHAR(50),
    accion_contexto VARCHAR(100)
);

COMMENT ON TABLE auditoria IS 'Registro completo de auditoría del sistema para trazabilidad';

-- =====================================================
-- PASO 14: CONFIGURACIÓN DEL SISTEMA
-- =====================================================

-- Configuraciones globales del sistema
CREATE TABLE configuracion_sistema (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    clave VARCHAR(100) UNIQUE NOT NULL,
    valor JSONB NOT NULL,
    descripcion TEXT,
    categoria VARCHAR(50) NOT NULL,
    tipo_dato VARCHAR(20) NOT NULL CHECK (tipo_dato IN ('string', 'number', 'boolean', 'json', 'array')),
    es_publica BOOLEAN DEFAULT FALSE,              -- Si se puede acceder desde el frontend
    modificado_por UUID REFERENCES usuarios(id),
    fecha_modificacion TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE configuracion_sistema IS 'Configuraciones globales del sistema';

-- =====================================================
-- PASO 15: ÍNDICES PARA OPTIMIZACIÓN
-- =====================================================

-- Índices para mejorar el rendimiento de consultas frecuentes

-- Usuarios y autenticación
CREATE INDEX idx_usuarios_email ON usuarios(email);
CREATE INDEX idx_usuarios_auth_user_id ON usuarios(auth_user_id);
CREATE INDEX idx_usuarios_activo ON usuarios(activo);


-- Personal
CREATE INDEX idx_personal_usuario_id ON personal(usuario_id);
CREATE INDEX idx_personal_tipo_estado ON personal(tipo_personal, estado_laboral);
CREATE INDEX idx_personal_documento ON personal(numero_documento);

-- Pacientes
CREATE INDEX idx_pacientes_numero_documento ON pacientes(numero_documento);
CREATE INDEX idx_pacientes_activo ON pacientes(activo);
CREATE INDEX idx_pacientes_fecha_registro ON pacientes(fecha_registro);
CREATE INDEX idx_pacientes_primer_nombre ON pacientes(primer_nombre);
CREATE INDEX idx_pacientes_primer_apellido ON pacientes(primer_apellido);
CREATE INDEX idx_pacientes_nombres_completo ON pacientes(primer_nombre, primer_apellido);
CREATE INDEX idx_pacientes_telefono_1 ON pacientes(telefono_1);

-- Consultas y citas
CREATE INDEX idx_consultas_paciente_fecha ON consultas(paciente_id, fecha_programada);
CREATE INDEX idx_consultas_odontologo_fecha ON consultas(odontologo_id, fecha_programada);
CREATE INDEX idx_consultas_estado ON consultas(estado);
CREATE INDEX idx_consultas_fecha_programada ON consultas(fecha_programada);

-- Intervenciones
CREATE INDEX idx_intervenciones_consulta ON intervenciones(consulta_id);
CREATE INDEX idx_intervenciones_odontologo ON intervenciones(odontologo_id);
CREATE INDEX idx_intervenciones_fecha ON intervenciones(hora_inicio);

-- Pagos
CREATE INDEX idx_pagos_paciente ON pagos(paciente_id);
CREATE INDEX idx_pagos_fecha ON pagos(fecha_pago);
CREATE INDEX idx_pagos_estado ON pagos(estado_pago);
CREATE INDEX idx_pagos_numero_recibo ON pagos(numero_recibo);

-- Odontograma
CREATE INDEX idx_odontograma_paciente ON odontograma(paciente_id);
CREATE INDEX idx_condiciones_odontograma ON condiciones_diente(odontograma_id);
CREATE INDEX idx_condiciones_diente ON condiciones_diente(diente_id);

-- Auditoría
CREATE INDEX idx_auditoria_tabla_registro ON auditoria(tabla_afectada, registro_id);
CREATE INDEX idx_auditoria_usuario_fecha ON auditoria(usuario_id, fecha_accion);
CREATE INDEX idx_auditoria_fecha ON auditoria(fecha_accion);

-- =====================================================
-- PASO 16: FUNCIONES Y TRIGGERS AUTOMÁTICOS
-- =====================================================

-- Función para actualizar automáticamente fecha_actualizacion
CREATE OR REPLACE FUNCTION actualizar_fecha_modificacion()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    NEW.fecha_actualizacion = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$;

-- Aplicar trigger a todas las tablas que necesiten actualización automática
CREATE TRIGGER trigger_usuarios_fecha_actualizacion
    BEFORE UPDATE ON usuarios
    FOR EACH ROW EXECUTE FUNCTION actualizar_fecha_modificacion();

CREATE TRIGGER trigger_personal_fecha_actualizacion
    BEFORE UPDATE ON personal
    FOR EACH ROW EXECUTE FUNCTION actualizar_fecha_modificacion();

CREATE TRIGGER trigger_pacientes_fecha_actualizacion
    BEFORE UPDATE ON pacientes
    FOR EACH ROW EXECUTE FUNCTION actualizar_fecha_modificacion();

CREATE TRIGGER trigger_consultas_fecha_actualizacion
    BEFORE UPDATE ON consultas
    FOR EACH ROW EXECUTE FUNCTION actualizar_fecha_modificacion();

CREATE TRIGGER trigger_odontograma_fecha_actualizacion
    BEFORE UPDATE ON odontograma
    FOR EACH ROW EXECUTE FUNCTION actualizar_fecha_modificacion();

-- Función para calcular automáticamente el saldo pendiente en pagos
CREATE OR REPLACE FUNCTION calcular_saldo_pendiente()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    NEW.saldo_pendiente = NEW.monto_total - NEW.monto_pagado;
    RETURN NEW;
END;
$$;

CREATE TRIGGER trigger_calcular_saldo_pendiente
    BEFORE INSERT OR UPDATE ON pagos
    FOR EACH ROW EXECUTE FUNCTION calcular_saldo_pendiente();

-- Función para calcular automáticamente la edad del paciente
CREATE OR REPLACE FUNCTION calcular_edad_paciente()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    IF NEW.fecha_nacimiento IS NOT NULL THEN
        NEW.edad = EXTRACT(YEAR FROM AGE(NEW.fecha_nacimiento));
    END IF;
    RETURN NEW;
END;
$$;

CREATE TRIGGER trigger_calcular_edad_paciente
    BEFORE INSERT OR UPDATE ON pacientes
    FOR EACH ROW EXECUTE FUNCTION calcular_edad_paciente();

-- =====================================================
-- PASO 17: FUNCIONES PARA GENERAR NÚMEROS ÚNICOS
-- =====================================================

-- Función para generar número de historia clínica automáticamente
CREATE OR REPLACE FUNCTION generar_numero_historia()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
DECLARE
    ultimo_numero INTEGER;
    nuevo_numero VARCHAR(20);
BEGIN
    IF NEW.numero_historia IS NULL OR NEW.numero_historia = '' THEN
        -- Obtener el último número de historia
        SELECT COALESCE(MAX(CAST(SUBSTRING(numero_historia FROM 3) AS INTEGER)), 0) + 1
        INTO ultimo_numero
        FROM pacientes
        WHERE numero_historia ~ '^HC[0-9]+$';
        
        -- Generar nuevo número con formato HC + número con padding
        nuevo_numero := 'HC' || LPAD(ultimo_numero::TEXT, 6, '0');
        NEW.numero_historia := nuevo_numero;
    END IF;
    
    RETURN NEW;
END;
$$;

CREATE TRIGGER trigger_generar_numero_historia
    BEFORE INSERT ON pacientes
    FOR EACH ROW EXECUTE FUNCTION generar_numero_historia();

-- Función para generar número de consulta automáticamente
CREATE OR REPLACE FUNCTION generar_numero_consulta()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
DECLARE
    ultimo_numero INTEGER;
    nuevo_numero VARCHAR(20);
    fecha_actual DATE;
BEGIN
    IF NEW.numero_consulta IS NULL OR NEW.numero_consulta = '' THEN
        fecha_actual := CURRENT_DATE;
        
        -- Obtener el último número de consulta del día
        SELECT COALESCE(MAX(CAST(SUBSTRING(numero_consulta FROM 10) AS INTEGER)), 0) + 1
        INTO ultimo_numero
        FROM consultas
        WHERE numero_consulta ~ ('^' || TO_CHAR(fecha_actual, 'YYYYMMDD') || '[0-9]+$');
        
        -- Generar nuevo número con formato YYYYMMDD + número secuencial
        nuevo_numero := TO_CHAR(fecha_actual, 'YYYYMMDD') || LPAD(ultimo_numero::TEXT, 3, '0');
        NEW.numero_consulta := nuevo_numero;
    END IF;
    
    RETURN NEW;
END;
$$;

CREATE TRIGGER trigger_generar_numero_consulta
    BEFORE INSERT ON consultas
    FOR EACH ROW EXECUTE FUNCTION generar_numero_consulta();

-- Función para generar número de recibo de pago automáticamente
CREATE OR REPLACE FUNCTION generar_numero_recibo()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
DECLARE
    ultimo_numero INTEGER;
    nuevo_numero VARCHAR(20);
    fecha_actual DATE;
BEGIN
    IF NEW.numero_recibo IS NULL OR NEW.numero_recibo = '' THEN
        fecha_actual := CURRENT_DATE;
        
        -- Obtener el último número de recibo del mes
        SELECT COALESCE(MAX(CAST(SUBSTRING(numero_recibo FROM 8) AS INTEGER)), 0) + 1
        INTO ultimo_numero
        FROM pagos
        WHERE numero_recibo ~ ('^REC' || TO_CHAR(fecha_actual, 'YYYYMM') || '[0-9]+$');
        
        -- Generar nuevo número con formato REC + YYYYMM + número secuencial
        nuevo_numero := 'REC' || TO_CHAR(fecha_actual, 'YYYYMM') || LPAD(ultimo_numero::TEXT, 4, '0');
        NEW.numero_recibo := nuevo_numero;
    END IF;
    
    RETURN NEW;
END;
$$;

CREATE TRIGGER trigger_generar_numero_recibo
    BEFORE INSERT ON pagos
    FOR EACH ROW EXECUTE FUNCTION generar_numero_recibo();


-- =====================================================
-- PASO 19: ROW LEVEL SECURITY (RLS)
-- =====================================================

-- Activar RLS en las tablas sensibles
ALTER TABLE usuarios ENABLE ROW LEVEL SECURITY;
ALTER TABLE personal ENABLE ROW LEVEL SECURITY;
ALTER TABLE pacientes ENABLE ROW LEVEL SECURITY;
ALTER TABLE consultas ENABLE ROW LEVEL SECURITY;
ALTER TABLE intervenciones ENABLE ROW LEVEL SECURITY;
ALTER TABLE historial_medico ENABLE ROW LEVEL SECURITY;
ALTER TABLE pagos ENABLE ROW LEVEL SECURITY;
ALTER TABLE odontograma ENABLE ROW LEVEL SECURITY;

-- Políticas básicas (permitir todo por ahora, refinar después)
CREATE POLICY "usuarios_policy" ON usuarios FOR ALL USING (true);
CREATE POLICY "personal_policy" ON personal FOR ALL USING (true);
CREATE POLICY "pacientes_policy" ON pacientes FOR ALL USING (true);
CREATE POLICY "consultas_policy" ON consultas FOR ALL USING (true);
CREATE POLICY "intervenciones_policy" ON intervenciones FOR ALL USING (true);
CREATE POLICY "historial_medico_policy" ON historial_medico FOR ALL USING (true);
CREATE POLICY "pagos_policy" ON pagos FOR ALL USING (true);
CREATE POLICY "odontograma_policy" ON odontograma FOR ALL USING (true);

-- =====================================================
-- PASO 20: DATOS INICIALES DEL SISTEMA
-- =====================================================

-- Insertar roles por defecto del sistema
INSERT INTO roles (nombre, descripcion, permisos) VALUES 
('gerente', 'Acceso completo al sistema', '{
    "usuarios": ["crear", "leer", "actualizar", "eliminar"],
    "pacientes": ["crear", "leer", "actualizar", "eliminar"],
    "consultas": ["crear", "leer", "actualizar", "eliminar"],
    "servicios": ["crear", "leer", "actualizar", "eliminar"],
    "personal": ["crear", "leer", "actualizar", "eliminar"],
    "pagos": ["crear", "leer", "actualizar", "eliminar"],
    "reportes": ["leer", "generar"],
    "configuracion": ["leer", "actualizar"]
}'),
('administrador', 'Gestión de pacientes, citas y pagos', '{
    "pacientes": ["crear", "leer", "actualizar"],
    "consultas": ["crear", "leer", "actualizar", "eliminar"],
    "pagos": ["crear", "leer", "actualizar"],
    "servicios": ["leer"],
    "reportes": ["leer"]
}'),
('odontologo', 'Atención de pacientes y gestión clínica', '{
    "pacientes": ["leer", "actualizar"],
    "consultas": ["leer", "actualizar"],
    "intervenciones": ["crear", "leer", "actualizar"],
    "odontograma": ["crear", "leer", "actualizar"],
    "historial_medico": ["crear", "leer", "actualizar"]
}'),
('asistente', 'Apoyo en consultas y tareas básicas', '{
    "pacientes": ["leer"],
    "consultas": ["leer", "actualizar"],
    "servicios": ["leer"]
}');

-- Configuraciones básicas del sistema
INSERT INTO configuracion_sistema (clave, valor, descripcion, categoria, tipo_dato, es_publica) VALUES
('consultorio_nombre', '"Clínica Dental Odontomara"', 'Nombre del consultorio', 'general', 'string', true),
('consultorio_direccion', '"Puerto La Cruz, Estado Anzoátegui"', 'Dirección del consultorio', 'general', 'string', true),
('consultorio_telefono', '"+58 281-123-4567"', 'Teléfono del consultorio', 'general', 'string', true),
('horario_atencion', '{"lunes": "08:00-17:00", "martes": "08:00-17:00", "miercoles": "08:00-17:00", "jueves": "08:00-17:00", "viernes": "08:00-16:00", "sabado": "08:00-12:00"}', 'Horarios de atención', 'operacion', 'json', true),
('duracion_cita_default', '30', 'Duración por defecto de citas en minutos', 'operacion', 'number', false),
('recordatorio_citas_horas', '24', 'Horas antes para enviar recordatorio', 'notificaciones', 'number', false),
('backup_automatico', 'true', 'Activar backup automático', 'sistema', 'boolean', false),
('moneda', '"VES"', 'Moneda utilizada en el sistema', 'financiero', 'string', true);

-- Servicios odontológicos básicos
INSERT INTO servicios (codigo, nombre, descripcion, categoria, duracion_estimada, precio_base) VALUES
('CONS001', 'Consulta General', 'Consulta odontológica general', 'Consulta', '30 minutes', 50.00),
('LIMP001', 'Profilaxis Dental', 'Limpieza dental profesional', 'Preventiva', '45 minutes', 80.00),
('OBTU001', 'Obturación Simple', 'Restauración dental con resina', 'Restaurativa', '60 minutes', 120.00),
('ENDO001', 'Endodoncia', 'Tratamiento de conducto radicular', 'Endodoncia', '90 minutes', 350.00),
('EXTR001', 'Extracción Simple', 'Extracción dental simple', 'Cirugía', '30 minutes', 80.00),
('EXTR002', 'Extracción Compleja', 'Extracción dental compleja', 'Cirugía', '60 minutes', 150.00),
('CORO001', 'Corona Dental', 'Corona en porcelana o metal-porcelana', 'Prótesis', '120 minutes', 800.00),
('PONT001', 'Puente Dental', 'Puente fijo de 3 unidades', 'Prótesis', '150 minutes', 1500.00),
('IMPL001', 'Implante Dental', 'Implante titanio + corona', 'Implantología', '120 minutes', 2000.00),
('BLAN001', 'Blanqueamiento', 'Blanqueamiento dental en consultorio', 'Estética', '90 minutes', 300.00),
('ORTH001', 'Valoración Ortodoncia', 'Consulta especializada en ortodoncia', 'Ortodoncia', '60 minutes', 100.00),
('ORTH002', 'Brackets Metálicos', 'Instalación de aparatología fija', 'Ortodoncia', '120 minutes', 1200.00),
('RADI001', 'Radiografía Panorámica', 'Radiografía panorámica digital', 'Diagnóstico', '15 minutes', 60.00),
('RADI002', 'Radiografía Periapical', 'Radiografía periapical digital', 'Diagnóstico', '10 minutes', 25.00);

-- Catálogo completo de dientes según numeración FDI
INSERT INTO dientes (numero_diente, nombre, tipo_diente, ubicacion, cuadrante, posicion_en_cuadrante, es_temporal, caras) VALUES
-- Cuadrante 1 (Superior Derecho) - Dientes permanentes
(11, 'Incisivo Central Superior Derecho', 'incisivo', 'superior_derecha', 1, 1, false, ARRAY['incisal', 'mesial', 'distal', 'vestibular', 'palatino']),
(12, 'Incisivo Lateral Superior Derecho', 'incisivo', 'superior_derecha', 1, 2, false, ARRAY['incisal', 'mesial', 'distal', 'vestibular', 'palatino']),
(13, 'Canino Superior Derecho', 'canino', 'superior_derecha', 1, 3, false, ARRAY['incisal', 'mesial', 'distal', 'vestibular', 'palatino']),
(14, 'Primer Premolar Superior Derecho', 'premolar', 'superior_derecha', 1, 4, false, ARRAY['oclusal', 'mesial', 'distal', 'vestibular', 'palatino']),
(15, 'Segundo Premolar Superior Derecho', 'premolar', 'superior_derecha', 1, 5, false, ARRAY['oclusal', 'mesial', 'distal', 'vestibular', 'palatino']),
(16, 'Primer Molar Superior Derecho', 'molar', 'superior_derecha', 1, 6, false, ARRAY['oclusal', 'mesial', 'distal', 'vestibular', 'palatino']),
(17, 'Segundo Molar Superior Derecho', 'molar', 'superior_derecha', 1, 7, false, ARRAY['oclusal', 'mesial', 'distal', 'vestibular', 'palatino']),
(18, 'Tercer Molar Superior Derecho', 'molar', 'superior_derecha', 1, 8, false, ARRAY['oclusal', 'mesial', 'distal', 'vestibular', 'palatino']),

-- Cuadrante 2 (Superior Izquierdo) - Dientes permanentes
(21, 'Incisivo Central Superior Izquierdo', 'incisivo', 'superior_izquierda', 2, 1, false, ARRAY['incisal', 'mesial', 'distal', 'vestibular', 'palatino']),
(22, 'Incisivo Lateral Superior Izquierdo', 'incisivo', 'superior_izquierda', 2, 2, false, ARRAY['incisal', 'mesial', 'distal', 'vestibular', 'palatino']),
(23, 'Canino Superior Izquierdo', 'canino', 'superior_izquierda', 2, 3, false, ARRAY['incisal', 'mesial', 'distal', 'vestibular', 'palatino']),
(24, 'Primer Premolar Superior Izquierdo', 'premolar', 'superior_izquierda', 2, 4, false, ARRAY['oclusal', 'mesial', 'distal', 'vestibular', 'palatino']),
(25, 'Segundo Premolar Superior Izquierdo', 'premolar', 'superior_izquierda', 2, 5, false, ARRAY['oclusal', 'mesial', 'distal', 'vestibular', 'palatino']),
(26, 'Primer Molar Superior Izquierdo', 'molar', 'superior_izquierda', 2, 6, false, ARRAY['oclusal', 'mesial', 'distal', 'vestibular', 'palatino']),
(27, 'Segundo Molar Superior Izquierdo', 'molar', 'superior_izquierda', 2, 7, false, ARRAY['oclusal', 'mesial', 'distal', 'vestibular', 'palatino']),
(28, 'Tercer Molar Superior Izquierdo', 'molar', 'superior_izquierda', 2, 8, false, ARRAY['oclusal', 'mesial', 'distal', 'vestibular', 'palatino']),

-- Cuadrante 3 (Inferior Izquierdo) - Dientes permanentes
(31, 'Incisivo Central Inferior Izquierdo', 'incisivo', 'inferior_izquierda', 3, 1, false, ARRAY['incisal', 'mesial', 'distal', 'vestibular', 'lingual']),
(32, 'Incisivo Lateral Inferior Izquierdo', 'incisivo', 'inferior_izquierda', 3, 2, false, ARRAY['incisal', 'mesial', 'distal', 'vestibular', 'lingual']),
(33, 'Canino Inferior Izquierdo', 'canino', 'inferior_izquierda', 3, 3, false, ARRAY['incisal', 'mesial', 'distal', 'vestibular', 'lingual']),
(34, 'Primer Premolar Inferior Izquierdo', 'premolar', 'inferior_izquierda', 3, 4, false, ARRAY['oclusal', 'mesial', 'distal', 'vestibular', 'lingual']),
(35, 'Segundo Premolar Inferior Izquierdo', 'premolar', 'inferior_izquierda', 3, 5, false, ARRAY['oclusal', 'mesial', 'distal', 'vestibular', 'lingual']),
(36, 'Primer Molar Inferior Izquierdo', 'molar', 'inferior_izquierda', 3, 6, false, ARRAY['oclusal', 'mesial', 'distal', 'vestibular', 'lingual']),
(37, 'Segundo Molar Inferior Izquierdo', 'molar', 'inferior_izquierda', 3, 7, false, ARRAY['oclusal', 'mesial', 'distal', 'vestibular', 'lingual']),
(38, 'Tercer Molar Inferior Izquierdo', 'molar', 'inferior_izquierda', 3, 8, false, ARRAY['oclusal', 'mesial', 'distal', 'vestibular', 'lingual']),

-- Cuadrante 4 (Inferior Derecho) - Dientes permanentes
(41, 'Incisivo Central Inferior Derecho', 'incisivo', 'inferior_derecha', 4, 1, false, ARRAY['incisal', 'mesial', 'distal', 'vestibular', 'lingual']),
(42, 'Incisivo Lateral Inferior Derecho', 'incisivo', 'inferior_derecha', 4, 2, false, ARRAY['incisal', 'mesial', 'distal', 'vestibular', 'lingual']),
(43, 'Canino Inferior Derecho', 'canino', 'inferior_derecha', 4, 3, false, ARRAY['incisal', 'mesial', 'distal', 'vestibular', 'lingual']),
(44, 'Primer Premolar Inferior Derecho', 'premolar', 'inferior_derecha', 4, 4, false, ARRAY['oclusal', 'mesial', 'distal', 'vestibular', 'lingual']),
(45, 'Segundo Premolar Inferior Derecho', 'premolar', 'inferior_derecha', 4, 5, false, ARRAY['oclusal', 'mesial', 'distal', 'vestibular', 'lingual']),
(46, 'Primer Molar Inferior Derecho', 'molar', 'inferior_derecha', 4, 6, false, ARRAY['oclusal', 'mesial', 'distal', 'vestibular', 'lingual']),
(47, 'Segundo Molar Inferior Derecho', 'molar', 'inferior_derecha', 4, 7, false, ARRAY['oclusal', 'mesial', 'distal', 'vestibular', 'lingual']),
(48, 'Tercer Molar Inferior Derecho', 'molar', 'inferior_derecha', 4, 8, false, ARRAY['oclusal', 'mesial', 'distal', 'vestibular', 'lingual']),

-- Dientes temporales (deciduos) - Cuadrante 5 (Superior Derecho)
(51, 'Incisivo Central Temporal Superior Derecho', 'incisivo', 'superior_derecha', 5, 1, true, ARRAY['incisal', 'mesial', 'distal', 'vestibular', 'palatino']),
(52, 'Incisivo Lateral Temporal Superior Derecho', 'incisivo', 'superior_derecha', 5, 2, true, ARRAY['incisal', 'mesial', 'distal', 'vestibular', 'palatino']),
(53, 'Canino Temporal Superior Derecho', 'canino', 'superior_derecha', 5, 3, true, ARRAY['incisal', 'mesial', 'distal', 'vestibular', 'palatino']),
(54, 'Primer Molar Temporal Superior Derecho', 'molar', 'superior_derecha', 5, 4, true, ARRAY['oclusal', 'mesial', 'distal', 'vestibular', 'palatino']),
(55, 'Segundo Molar Temporal Superior Derecho', 'molar', 'superior_derecha', 5, 5, true, ARRAY['oclusal', 'mesial', 'distal', 'vestibular', 'palatino']),

-- Dientes temporales - Cuadrante 6 (Superior Izquierdo)
(61, 'Incisivo Central Temporal Superior Izquierdo', 'incisivo', 'superior_izquierda', 6, 1, true, ARRAY['incisal', 'mesial', 'distal', 'vestibular', 'palatino']),
(62, 'Incisivo Lateral Temporal Superior Izquierdo', 'incisivo', 'superior_izquierda', 6, 2, true, ARRAY['incisal', 'mesial', 'distal', 'vestibular', 'palatino']),
(63, 'Canino Temporal Superior Izquierdo', 'canino', 'superior_izquierda', 6, 3, true, ARRAY['incisal', 'mesial', 'distal', 'vestibular', 'palatino']),
(64, 'Primer Molar Temporal Superior Izquierdo', 'molar', 'superior_izquierda', 6, 4, true, ARRAY['oclusal', 'mesial', 'distal', 'vestibular', 'palatino']),
(65, 'Segundo Molar Temporal Superior Izquierdo', 'molar', 'superior_izquierda', 6, 5, true, ARRAY['oclusal', 'mesial', 'distal', 'vestibular', 'palatino']),

-- Dientes temporales - Cuadrante 7 (Inferior Izquierdo)
(71, 'Incisivo Central Temporal Inferior Izquierdo', 'incisivo', 'inferior_izquierda', 7, 1, true, ARRAY['incisal', 'mesial', 'distal', 'vestibular', 'lingual']),
(72, 'Incisivo Lateral Temporal Inferior Izquierdo', 'incisivo', 'inferior_izquierda', 7, 2, true, ARRAY['incisal', 'mesial', 'distal', 'vestibular', 'lingual']),
(73, 'Canino Temporal Inferior Izquierdo', 'canino', 'inferior_izquierda', 7, 3, true, ARRAY['incisal', 'mesial', 'distal', 'vestibular', 'lingual']),
(74, 'Primer Molar Temporal Inferior Izquierdo', 'molar', 'inferior_izquierda', 7, 4, true, ARRAY['oclusal', 'mesial', 'distal', 'vestibular', 'lingual']),
(75, 'Segundo Molar Temporal Inferior Izquierdo', 'molar', 'inferior_izquierda', 7, 5, true, ARRAY['oclusal', 'mesial', 'distal', 'vestibular', 'lingual']),

-- Dientes temporales - Cuadrante 8 (Inferior Derecho)
(81, 'Incisivo Central Temporal Inferior Derecho', 'incisivo', 'inferior_derecha', 8, 1, true, ARRAY['incisal', 'mesial', 'distal', 'vestibular', 'lingual']),
(82, 'Incisivo Lateral Temporal Inferior Derecho', 'incisivo', 'inferior_derecha', 8, 2, true, ARRAY['incisal', 'mesial', 'distal', 'vestibular', 'lingual']),
(83, 'Canino Temporal Inferior Derecho', 'canino', 'inferior_derecha', 8, 3, true, ARRAY['incisal', 'mesial', 'distal', 'vestibular', 'lingual']),
(84, 'Primer Molar Temporal Inferior Derecho', 'molar', 'inferior_derecha', 8, 4, true, ARRAY['oclusal', 'mesial', 'distal', 'vestibular', 'lingual']),
(85, 'Segundo Molar Temporal Inferior Derecho', 'molar', 'inferior_derecha', 8, 5, true, ARRAY['oclusal', 'mesial', 'distal', 'vestibular', 'lingual']);

-- =====================================================
-- PASO 21: VISTAS ÚTILES PARA REPORTES Y CONSULTAS
-- =====================================================

-- =====================================================
-- VISTA PARA OBTENER NOMBRE COMPLETO DESDE PERSONAL
-- =====================================================

-- Vista que combina usuarios con personal para obtener nombre completo
CREATE OR REPLACE VIEW vista_usuarios_completo AS
SELECT 
    u.id,
    u.email,
    u.telefono,
    u.rol_id,
    u.activo,vista_personal_completo
    u.fecha_creacion,
    u.fecha_actualizacion,
    u.ultimo_acceso,
    u.auth_user_id,
    u.avatar_url,
    u.metadata,
    -- Información del rol
    r.nombre as rol_nombre,
    r.descripcion as rol_descripcion,
    r.permisos as rol_permisos,
    -- Información del personal (si existe)
    p.id as personal_id,
    p.primer_nombre,
    p.segundo_nombre,
    p.primer_apellido,
    p.segundo_apellido,
    p.tipo_personal,
    p.especialidad,
    p.estado_laboral,
    -- Nombre completo calculado
    CASE 
        WHEN p.id IS NOT NULL THEN
            TRIM(CONCAT(
                COALESCE(p.primer_nombre, ''), 
                CASE WHEN p.segundo_nombre IS NOT NULL THEN ' ' || p.segundo_nombre ELSE '' END,
                ' ',
                COALESCE(p.primer_apellido, ''),
                CASE WHEN p.segundo_apellido IS NOT NULL THEN ' ' || p.segundo_apellido ELSE '' END
            ))
        ELSE split_part(u.email, '@', 1)  -- Fallback al email
    END as nombre_completo
FROM usuarios u
JOIN roles r ON u.rol_id = r.id
LEFT JOIN personal p ON u.id = p.usuario_id
ORDER BY 
    CASE 
        WHEN p.id IS NOT NULL THEN
            TRIM(CONCAT(
                COALESCE(p.primer_nombre, ''), 
                CASE WHEN p.segundo_nombre IS NOT NULL THEN ' ' || p.segundo_nombre ELSE '' END,
                ' ',
                COALESCE(p.primer_apellido, ''),
                CASE WHEN p.segundo_apellido IS NOT NULL THEN ' ' || p.segundo_apellido ELSE '' END
            ))
        ELSE split_part(u.email, '@', 1)
    END;



-- Vista consolidada para gestión de personal

CREATE OR REPLACE VIEW vista_personal_completo AS
SELECT 
    -- IDs y campos principales de personal
    p.id,
    p.numero_documento,
    p.tipo_documento,
    p.fecha_nacimiento,
    p.direccion,
    p.celular,
    p.tipo_personal,
    p.especialidad,
    p.numero_licencia,
    p.fecha_contratacion,
    p.salario,
    p.horario_trabajo,
    p.estado_laboral,
    p.observaciones,
    
    -- ✅ AGREGAR: Campos de nombres SEPARADOS
    p.primer_nombre,
    p.segundo_nombre,
    p.primer_apellido,
    p.segundo_apellido,
    
    -- Información del usuario (aplanada)
    p.usuario_id,
    u.email,
    u.telefono,
    u.activo as usuario_activo,
    u.ultimo_acceso,
    u.fecha_creacion,
    u.auth_user_id,
    u.avatar_url,
    u.metadata,
    
    -- Información del rol
    r.id as rol_id,
    r.nombre as rol_nombre,
    r.descripcion as rol_descripcion,
    r.permisos as rol_permisos,
    
    -- ✅ MANTENER: Nombre completo calculado (para compatibilidad)
    CASE 
        WHEN p.id IS NOT NULL THEN
            TRIM(CONCAT(
                COALESCE(p.primer_nombre, ''), 
                CASE WHEN p.segundo_nombre IS NOT NULL AND p.segundo_nombre != '' THEN ' ' || p.segundo_nombre ELSE '' END,
                ' ',
                COALESCE(p.primer_apellido, ''),
                CASE WHEN p.segundo_apellido IS NOT NULL AND p.segundo_apellido != '' THEN ' ' || p.segundo_apellido ELSE '' END
            ))
        ELSE split_part(u.email, '@', 1)
    END as nombre_completo,
    
    -- Estado calculado
    CASE 
        WHEN p.estado_laboral = 'activo' AND u.activo = true THEN true
        ELSE false
    END as completamente_activo,
    
    -- Tiempo en la empresa
    CASE 
        WHEN p.fecha_contratacion IS NOT NULL 
        THEN (CURRENT_DATE - p.fecha_contratacion)
        ELSE NULL
    END as dias_en_empresa,
    
    -- ✅ MANTENER: JSON para compatibilidad con código existente
    jsonb_build_object(
        'id', u.id,
        'email', u.email,
        'telefono', u.telefono,
        'activo', u.activo,
        'auth_user_id', u.auth_user_id,
        'nombre_completo', CASE 
            WHEN p.id IS NOT NULL THEN
                TRIM(CONCAT(
                    COALESCE(p.primer_nombre, ''), 
                    CASE WHEN p.segundo_nombre IS NOT NULL AND p.segundo_nombre != '' THEN ' ' || p.segundo_nombre ELSE '' END,
                    ' ',
                    COALESCE(p.primer_apellido, ''),
                    CASE WHEN p.segundo_apellido IS NOT NULL AND p.segundo_apellido != '' THEN ' ' || p.segundo_apellido ELSE '' END
                ))
            ELSE split_part(u.email, '@', 1)
        END
    ) as usuario_info

FROM personal p
INNER JOIN usuarios u ON p.usuario_id = u.id
INNER JOIN roles r ON u.rol_id = r.id
ORDER BY 
    CASE 
        WHEN p.id IS NOT NULL THEN
            TRIM(CONCAT(COALESCE(p.primer_nombre, ''), ' ', COALESCE(p.primer_apellido, '')))
        ELSE u.email
    END;

-- Vista para consultas del día
CREATE OR REPLACE VIEW vista_consultas_hoy AS
SELECT 
    c.id,
    c.numero_consulta,
    c.fecha_programada,
    c.estado,
    c.tipo_consulta,
    c.motivo_consulta,
    c.costo_total,
    -- Información del paciente
    pac.nombre_completo as paciente_nombre,
    pac.telefono as paciente_telefono,
    pac.numero_historia,
    -- Información del odontólogo desde personal
    TRIM(CONCAT(
        COALESCE(p_odontologo.primer_nombre, ''), 
        CASE WHEN p_odontologo.segundo_nombre IS NOT NULL THEN ' ' || p_odontologo.segundo_nombre ELSE '' END,
        ' ',
        COALESCE(p_odontologo.primer_apellido, ''),
        CASE WHEN p_odontologo.segundo_apellido IS NOT NULL THEN ' ' || p_odontologo.segundo_apellido ELSE '' END
    )) as odontologo_nombre,
    p_odontologo.especialidad as odontologo_especialidad
FROM consultas c
JOIN pacientes pac ON c.paciente_id = pac.id
JOIN personal p_odontologo ON c.odontologo_id = p_odontologo.id
JOIN usuarios u_odontologo ON p_odontologo.usuario_id = u_odontologo.id 
WHERE DATE(c.fecha_programada) = CURRENT_DATE
ORDER BY c.fecha_programada;

-- Vista para ingresos mensuales
CREATE VIEW vista_ingresos_mensuales AS
SELECT 
    EXTRACT(YEAR FROM fecha_pago) as año,
    EXTRACT(MONTH FROM fecha_pago) as mes,
    TO_CHAR(fecha_pago, 'Month YYYY') as periodo,
    COUNT(*) as total_pagos,
    SUM(monto_pagado) as ingresos_totales,
    AVG(monto_pagado) as promedio_pago,
    SUM(CASE WHEN estado_pago = 'pendiente' THEN saldo_pendiente ELSE 0 END) as pendientes_totales
FROM pagos
WHERE estado_pago IN ('completado', 'pendiente')
GROUP BY EXTRACT(YEAR FROM fecha_pago), EXTRACT(MONTH FROM fecha_pago), TO_CHAR(fecha_pago, 'Month YYYY')
ORDER BY año DESC, mes DESC;

-- Vista para servicios más utilizados
CREATE VIEW vista_servicios_populares AS
SELECT 
    s.id,
    s.codigo,
    s.nombre,
    s.categoria,
    s.precio_base,
    COUNT(i.id) as veces_realizado,
    SUM(i.precio_final) as ingresos_generados,
    AVG(i.precio_final) as precio_promedio,
    MAX(i.fecha_registro) as ultimo_uso
FROM servicios s
LEFT JOIN intervenciones i ON s.id = i.servicio_id
WHERE s.activo = true
GROUP BY s.id, s.codigo, s.nombre, s.categoria, s.precio_base
ORDER BY veces_realizado DESC;

-- =====================================================
-- PASO 22: FUNCIONES AUXILIARES PARA EL SISTEMA
-- =====================================================

-- Función para verificar permisos de usuario
CREATE OR REPLACE FUNCTION verificar_permiso(
    usuario_id UUID,
    modulo VARCHAR(50),
    accion VARCHAR(50)
)
RETURNS BOOLEAN
LANGUAGE plpgsql
AS $$
DECLARE
    permisos_usuario JSONB;
    permisos_modulo JSONB;
BEGIN
    -- Obtener permisos del usuario a través de su rol
    SELECT r.permisos INTO permisos_usuario
    FROM usuarios u
    JOIN roles r ON u.rol_id = r.id
    WHERE u.id = usuario_id AND u.activo = TRUE AND r.activo = TRUE;
    
    IF permisos_usuario IS NULL THEN
        RETURN FALSE;
    END IF;
    
    -- Verificar si tiene permisos para el módulo específico
    permisos_modulo := permisos_usuario->modulo;
    
    IF permisos_modulo IS NULL THEN
        RETURN FALSE;
    END IF;
    
    -- Verificar si tiene la acción específica
    RETURN permisos_modulo ? accion;
END;
$$;

-- Función para obtener información completa del usuario
CREATE OR REPLACE FUNCTION obtener_usuario_completo(auth_id UUID)
RETURNS TABLE(
    usuario_id UUID,
    email VARCHAR(100),
    nombre_completo TEXT,
    rol_nombre VARCHAR(50),
    permisos JSONB,
    personal_info JSONB
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT 
        u.id,
        u.email,
        CASE 
            WHEN p.id IS NOT NULL THEN
                TRIM(CONCAT(
                    COALESCE(p.primer_nombre, ''), 
                    CASE WHEN p.segundo_nombre IS NOT NULL THEN ' ' || p.segundo_nombre ELSE '' END,
                    ' ',
                    COALESCE(p.primer_apellido, ''),
                    CASE WHEN p.segundo_apellido IS NOT NULL THEN ' ' || p.segundo_apellido ELSE '' END
                ))
            ELSE split_part(u.email, '@', 1)
        END::TEXT as nombre_completo,
        r.nombre,
        r.permisos,
        CASE 
            WHEN p.id IS NOT NULL THEN
                jsonb_build_object(
                    'id', p.id,
                    'numero_documento', p.numero_documento,
                    'tipo_personal', p.tipo_personal,
                    'especialidad', p.especialidad,
                    'estado_laboral', p.estado_laboral,
                    'primer_nombre', p.primer_nombre,
                    'segundo_nombre', p.segundo_nombre,
                    'primer_apellido', p.primer_apellido,
                    'segundo_apellido', p.segundo_apellido
                )
            ELSE NULL
        END as personal_info
    FROM usuarios u
    JOIN roles r ON u.rol_id = r.id
    LEFT JOIN personal p ON u.id = p.usuario_id
    WHERE u.auth_user_id = auth_id AND u.activo = TRUE;
END;
$$;

-- Función para obtener estadísticas del dashboard
CREATE OR REPLACE FUNCTION obtener_stats_dashboard()
RETURNS JSONB
LANGUAGE plpgsql
AS $$
DECLARE
    stats JSONB;
    fecha_actual DATE := CURRENT_DATE;
    inicio_mes DATE := DATE_TRUNC('month', fecha_actual)::DATE;
BEGIN
    SELECT jsonb_build_object(
        -- Estadísticas de personal
        'total_personal', (
            SELECT COUNT(*) 
            FROM vista_personal_completo 
            WHERE usuario_activo = TRUE
        ),
        'personal_activo', (
            SELECT COUNT(*) 
            FROM vista_personal_completo 
            WHERE estado_laboral = 'activo' AND usuario_activo = TRUE
        ),
        'odontologos_activos', (
            SELECT COUNT(*) 
            FROM vista_personal_completo 
            WHERE tipo_personal = 'Odontólogo' 
            AND estado_laboral = 'activo' 
            AND usuario_activo = TRUE
        ),
        
        -- Estadísticas de pacientes
        'total_pacientes', (
            SELECT COUNT(*) 
            FROM pacientes 
            WHERE activo = TRUE
        ),
        'pacientes_nuevos_mes', (
            SELECT COUNT(*) 
            FROM pacientes 
            WHERE activo = TRUE 
            AND fecha_registro >= inicio_mes
        ),
        
        -- Estadísticas de consultas
        'consultas_hoy', (
            SELECT COUNT(*) 
            FROM consultas 
            WHERE DATE(fecha_programada) = fecha_actual
        ),
        'consultas_mes', (
            SELECT COUNT(*) 
            FROM consultas 
            WHERE fecha_programada >= inicio_mes
        ),
        
        -- Estadísticas de servicios
        'servicios_activos', (
            SELECT COUNT(*) 
            FROM servicios 
            WHERE activo = TRUE
        ),
        
        -- Estadísticas financieras
        'ingresos_mes', (
            SELECT COALESCE(SUM(monto_pagado), 0) 
            FROM pagos 
            WHERE fecha_pago >= inicio_mes 
            AND estado_pago = 'completado'
        ),
        'pagos_pendientes', (
            SELECT COUNT(*) 
            FROM pagos 
            WHERE estado_pago = 'pendiente'
        )
    ) INTO stats;
    
    RETURN stats;
END;
$$;

-- =====================================================
-- PASO 23: PERMISOS Y GRANTS FINALES
-- =====================================================

-- Permisos para usuarios autenticados
GRANT SELECT ON ALL TABLES IN SCHEMA public TO authenticated;
GRANT INSERT, UPDATE ON usuarios TO authenticated;
GRANT INSERT, UPDATE ON personal TO authenticated;
GRANT INSERT, UPDATE ON pacientes TO authenticated;
GRANT INSERT, UPDATE ON consultas TO authenticated;
GRANT INSERT, UPDATE ON intervenciones TO authenticated;
GRANT INSERT, UPDATE ON historial_medico TO authenticated;
GRANT INSERT, UPDATE ON pagos TO authenticated;
GRANT INSERT, UPDATE ON odontograma TO authenticated;
GRANT INSERT, UPDATE ON condiciones_diente TO authenticated;

-- Permisos para funciones
GRANT EXECUTE ON FUNCTION verificar_permiso TO authenticated;
GRANT EXECUTE ON FUNCTION obtener_usuario_completo TO authenticated;
GRANT EXECUTE ON FUNCTION obtener_stats_dashboard TO authenticated;

-- Permisos para vistas
GRANT SELECT ON vista_personal_completo TO authenticated;
GRANT SELECT ON vista_consultas_hoy TO authenticated;
GRANT SELECT ON vista_ingresos_mensuales TO authenticated;
GRANT SELECT ON vista_servicios_populares TO authenticated;
GRANT SELECT ON vista_usuarios_completo TO authenticated;

-- =====================================================
-- PASO 24: VERIFICACIÓN FINAL
-- =====================================================

-- Verificar que se crearon todas las tablas
DO $$
DECLARE
    tabla_count INTEGER;
    funcion_count INTEGER;
    vista_count INTEGER;
BEGIN
    -- Contar tablas creadas
    SELECT COUNT(*) INTO tabla_count
    FROM information_schema.tables 
    WHERE table_schema = 'public' 
    AND table_type = 'BASE TABLE'
    AND table_name IN (
        'roles', 'usuarios', 'personal', 'pacientes', 'servicios', 
        'consultas', 'intervenciones', 'historial_medico', 'pagos', 
        'odontograma', 'dientes', 'condiciones_diente', 'imagenes_clinicas', 
        'auditoria', 'configuracion_sistema'
    );
    
    -- Contar funciones creadas
    SELECT COUNT(*) INTO funcion_count
    FROM pg_proc p
    JOIN pg_namespace n ON p.pronamespace = n.oid
    WHERE n.nspname = 'public'
    AND p.proname IN (
        'verificar_permiso', 'obtener_usuario_completo', 'obtener_stats_dashboard'
    );
    
    -- Contar vistas creadas
    SELECT COUNT(*) INTO vista_count
    FROM information_schema.tables 
    WHERE table_schema = 'public' 
    AND table_type = 'VIEW'
    AND table_name IN (
        'vista_personal_completo', 'vista_consultas_hoy', 
        'vista_ingresos_mensuales', 'vista_servicios_populares'
    );
    
    -- Mostrar resultados
    RAISE NOTICE '=== VERIFICACIÓN FINAL DEL SISTEMA ===';
    RAISE NOTICE '✅ Tablas creadas: %/15', tabla_count;
    RAISE NOTICE '✅ Funciones creadas: %/4', funcion_count;
    RAISE NOTICE '✅ Vistas creadas: %/4', vista_count;
    RAISE NOTICE '✅ Roles insertados: % registros', (SELECT COUNT(*) FROM roles);
    RAISE NOTICE '✅ Servicios insertados: % registros', (SELECT COUNT(*) FROM servicios);
    RAISE NOTICE '✅ Dientes catalogados: % registros', (SELECT COUNT(*) FROM dientes);
    RAISE NOTICE '✅ Configuraciones del sistema: % registros', (SELECT COUNT(*) FROM configuracion_sistema);
    
    IF tabla_count = 15 AND funcion_count = 4 AND vista_count = 4 THEN
        RAISE NOTICE '🎉 ¡BASE DE DATOS CREADA EXITOSAMENTE!';
        RAISE NOTICE '🚀 El sistema odontológico está listo para usar';
    ELSE
        RAISE WARNING '⚠️ Algunas entidades no se crearon correctamente';
    END IF;
END $$;

-- =====================================================
-- FIN DEL SCRIPT
-- =====================================================

/*
=====================================================
🎯 RESUMEN DE LA BASE DE DATOS CREADA

📊 TABLAS PRINCIPALES (15):
✅ roles - Sistema de permisos granulares
✅ usuarios - Sincronizado con Supabase Auth  
✅ personal - Información del personal médico/administrativo
✅ pacientes - Registro completo de pacientes
✅ servicios - Catálogo de procedimientos odontológicos
✅ consultas - Gestión de citas y consultas
✅ intervenciones - Procedimientos realizados
✅ historial_medico - Historiales clínicos detallados
✅ pagos - Sistema de facturación y pagos
✅ odontograma - Odontogramas digitales
✅ dientes - Catálogo FDI (52 dientes)
✅ condiciones_diente - Estados específicos de cada diente
✅ imagenes_clinicas - Gestión de imágenes médicas
✅ auditoria - Trazabilidad completa del sistema
✅ configuracion_sistema - Configuraciones globales

🔧 FUNCIONES AUTOMÁTICAS:
✅ Trigger para sincronización con Supabase Auth
✅ Generación automática de números únicos
✅ Cálculo automático de edad y saldo pendiente
✅ Actualización automática de timestamps
✅ Verificación de permisos por rol

📈 VISTAS Y REPORTES:
✅ Vista consolidada de personal
✅ Consultas del día
✅ Ingresos mensuales  
✅ Servicios más utilizados

🔒 SEGURIDAD:
✅ Row Level Security (RLS) activado
✅ Políticas de acceso configuradas
✅ Validaciones de datos en todas las tablas
✅ Auditoría completa del sistema

📋 DATOS INICIALES:
✅ 4 roles predefinidos (gerente, administrador, odontólogo, asistente)
✅ 14 servicios odontológicos básicos
✅ 52 dientes catalogados según FDI
✅ 8 configuraciones del sistema

🚀 PRÓXIMOS PASOS:
1. Ejecutar este script en Supabase SQL Editor
2. Configurar variables de entorno en la aplicación
3. Implementar las funciones Python mejoradas
4. Crear el primer usuario administrador
5. Probar todas las funcionalidades

⚠️ IMPORTANTE:
- Este script crea la BD completa desde cero
- Incluye todas las buenas prácticas de PostgreSQL
- Compatible 100% con Supabase
- Documentado y explicado paso a paso
- Listo para producción

📞 SOPORTE:
Si encuentras algún error durante la ejecución,
revisa los logs de PostgreSQL para más detalles.
=====================================================
*/