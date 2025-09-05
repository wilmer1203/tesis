-- =====================================================
-- SISTEMA ODONTOLÓGICO CLÍNICA DENTAL - ESQUEMA FINAL CORREGIDO
-- Versión: 4.1 - CORREGIDAS INCONSISTENCIAS
-- Fecha: Agosto 2025
-- Metodología: RUP (Rational Unified Process)
-- 
-- FLUJO ESPECÍFICO DE LA CLÍNICA:
-- 1. Paciente llega sin cita (solo consultas por orden de llegada)
-- 2. Administrador crea consulta y asigna primer odontólogo preferido
-- 3. Sistema maneja cola por odontólogo específico
-- 4. Cada odontólogo puede hacer múltiples servicios en UNA intervención
-- 5. Múltiples odontólogos pueden atender la misma consulta (diferentes intervenciones)
-- 6. Pagos mixtos en BS y USD
-- 7. Odontólogos cobran completo lo de sus intervenciones
-- 8. Odontograma detallado con versionado histórico
-- =====================================================

-- =====================================================
-- EXTENSIONES Y CONFIGURACIÓN INICIAL
-- =====================================================
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";
SET timezone = 'America/Caracas';

-- =====================================================
-- TABLA 1: ROLES CON PERMISOS GRANULARES
-- =====================================================
CREATE TABLE roles (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    nombre VARCHAR(50) UNIQUE NOT NULL,
    descripcion TEXT,
    permisos JSONB DEFAULT '{}',
    activo BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT chk_roles_nombre_valido CHECK (nombre ~ '^[a-z_]+$'),
    CONSTRAINT chk_roles_permisos_json CHECK (jsonb_typeof(permisos) = 'object')
);

-- =====================================================
-- TABLA 2: USUARIOS DEL SISTEMA (SIMPLIFICADA)
-- =====================================================
CREATE TABLE usuarios (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(100) UNIQUE NOT NULL,
    rol_id UUID REFERENCES roles(id) NOT NULL,
    activo BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    ultimo_acceso TIMESTAMP WITH TIME ZONE,
    configuraciones JSONB DEFAULT '{}',
    
    -- Integración con Supabase Auth
    auth_user_id UUID UNIQUE,
    avatar_url TEXT,
    metadata JSONB DEFAULT '{}',
    
    CONSTRAINT chk_usuarios_email_valido CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$')
);

-- =====================================================
-- TABLA 3: PERSONAL MÉDICO Y ADMINISTRATIVO
-- =====================================================
CREATE TABLE personal (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    usuario_id UUID UNIQUE REFERENCES usuarios(id) ON DELETE CASCADE,
    
    -- Información personal
    primer_nombre VARCHAR(50) NOT NULL,
    segundo_nombre VARCHAR(50),
    primer_apellido VARCHAR(50) NOT NULL, 
    segundo_apellido VARCHAR(50),
    tipo_documento VARCHAR(20) DEFAULT 'CI' CHECK (tipo_documento IN ('CI', 'Pasaporte')),
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
    estado_laboral VARCHAR(20) DEFAULT 'activo' CHECK (estado_laboral IN ('activo', 'inactivo')),
    observaciones TEXT,
    
    -- ESPECÍFICO PARA ODONTÓLOGOS: Cola y disponibilidad
    acepta_pacientes_nuevos BOOLEAN DEFAULT TRUE,
    orden_preferencia INTEGER DEFAULT 1,
    
    fecha_creacion TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT chk_personal_documento CHECK (numero_documento ~ '^\d{6,20}$'),
    CONSTRAINT chk_personal_celular CHECK (celular ~ '^[\+]?[\d\s\-\(\)]{7,20}$'),
    CONSTRAINT chk_personal_salario CHECK (salario IS NULL OR salario >= 0)
);

-- =====================================================
-- TABLA 4: PACIENTES
-- =====================================================
CREATE TABLE pacientes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    numero_historia VARCHAR(20) UNIQUE NOT NULL,
    
    -- Información personal
    primer_nombre VARCHAR(50) NOT NULL,
    segundo_nombre VARCHAR(50),
    primer_apellido VARCHAR(50) NOT NULL, 
    segundo_apellido VARCHAR(50),
    tipo_documento VARCHAR(20) DEFAULT 'CI' CHECK (tipo_documento IN ('CI', 'Pasaporte')),
    numero_documento VARCHAR(20) UNIQUE NOT NULL,
    fecha_nacimiento DATE,
    edad INTEGER,
    genero VARCHAR(10) CHECK (genero IN ('masculino', 'femenino', 'otro')),
    celular_1 VARCHAR(20),
    celular_2 VARCHAR(20),
    email VARCHAR(100),
    direccion TEXT,
    ciudad VARCHAR(100),
    departamento VARCHAR(100),
    ocupacion VARCHAR(100),
    estado_civil VARCHAR(20),
    contacto_emergencia JSONB DEFAULT '{}',
    
    -- Información médica básica
    alergias TEXT[],
    medicamentos_actuales TEXT[],
    condiciones_medicas TEXT[],
    antecedentes_familiares TEXT[],
    
    -- Control del sistema
    fecha_registro TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    registrado_por UUID REFERENCES usuarios(id),
    activo BOOLEAN DEFAULT TRUE,
    observaciones TEXT,
    
    CONSTRAINT chk_pacientes_documento CHECK (numero_documento ~ '^\d{6,20}$'),
    CONSTRAINT chk_pacientes_edad CHECK (edad IS NULL OR (edad >= 0 AND edad <= 150)),
    CONSTRAINT chk_pacientes_email CHECK (email IS NULL OR email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'),
    CONSTRAINT chk_pacientes_celular1 CHECK (celular_1 IS NULL OR celular_1 ~ '^[\+]?[\d\s\-\(\)]{7,20}$'),
    CONSTRAINT chk_pacientes_celular2 CHECK (celular_2 IS NULL OR celular_2 ~ '^[\+]?[\d\s\-\(\)]{7,20}$')
);

-- =====================================================
-- TABLA 5: SERVICIOS ODONTOLÓGICOS
-- =====================================================
CREATE TABLE servicios (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    codigo VARCHAR(20) UNIQUE NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    categoria VARCHAR(50) NOT NULL,
    subcategoria VARCHAR(50),
    duracion_estimada INTERVAL NOT NULL DEFAULT '30 minutes',
    precio_base_bs DECIMAL(10,2) NOT NULL,
    precio_base_usd DECIMAL(10,2) NOT NULL,
    material_incluido TEXT[],
    instrucciones_pre TEXT,
    instrucciones_post TEXT,
    activo BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    creado_por UUID REFERENCES usuarios(id),
    
    CONSTRAINT chk_servicios_codigo CHECK (codigo ~ '^[A-Z0-9]+$'),
    CONSTRAINT chk_servicios_precio_bs CHECK (precio_base_bs > 0),
    CONSTRAINT chk_servicios_precio_usd CHECK (precio_base_usd > 0)
);

-- =====================================================
-- TABLA 6: CONSULTAS (OPTIMIZADA PARA FLUJO SIN CITAS)
-- =====================================================
CREATE TABLE consultas (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    numero_consulta VARCHAR(20) UNIQUE NOT NULL,
    paciente_id UUID REFERENCES pacientes(id) NOT NULL,
    
    -- FLUJO ESPECÍFICO: Múltiples odontólogos por consulta
    primer_odontologo_id UUID REFERENCES personal(id) NOT NULL,
    odontologo_preferido_id UUID REFERENCES personal(id),
    
    -- SISTEMA DE COLAS POR ODONTÓLOGO
    fecha_llegada TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    orden_llegada_general INTEGER,
    orden_cola_odontologo INTEGER,
    
    -- Estados de la consulta adaptados al flujo
    estado VARCHAR(20) DEFAULT 'en_espera' CHECK (estado IN (
        'en_espera',        -- Paciente esperando a ser atendido
        'en_atencion',      -- Siendo atendido por algún odontólogo
        'entre_odontologos', -- Esperando atención de otro odontólogo
        'completada',       -- Consulta finalizada
        'cancelada'         -- Cancelada por algún motivo
    )),
    
    tipo_consulta VARCHAR(30) DEFAULT 'general' CHECK (tipo_consulta IN ('general', 'control', 'urgencia', 'emergencia')),
    prioridad VARCHAR(20) DEFAULT 'normal' CHECK (prioridad IN ('baja', 'normal', 'alta', 'urgente')),
    
    -- Información adicional
    motivo_consulta TEXT,
    observaciones TEXT,
    notas_internas TEXT,
    
    -- COSTOS EN MÚLTIPLES MONEDAS
    costo_total_bs DECIMAL(10,2) DEFAULT 0,
    costo_total_usd DECIMAL(10,2) DEFAULT 0,
    
    -- Control administrativo
    creada_por UUID REFERENCES usuarios(id),
    fecha_creacion TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    fecha_inicio_atencion TIMESTAMP WITH TIME ZONE,
    fecha_fin_atencion TIMESTAMP WITH TIME ZONE,
    
    CONSTRAINT chk_consultas_fecha_logica CHECK (
        fecha_inicio_atencion IS NULL OR fecha_fin_atencion IS NULL OR fecha_inicio_atencion <= fecha_fin_atencion
    ),
    CONSTRAINT chk_consultas_costos CHECK (costo_total_bs >= 0 AND costo_total_usd >= 0)
);

-- =====================================================
-- TABLA 7: INTERVENCIONES (OPTIMIZADA PARA MÚLTIPLES SERVICIOS)
-- =====================================================
CREATE TABLE intervenciones (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    consulta_id UUID REFERENCES consultas(id) NOT NULL,
    odontologo_id UUID REFERENCES personal(id) NOT NULL,
    asistente_id UUID REFERENCES personal(id),
    
    -- Control temporal
    hora_inicio TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    hora_fin TIMESTAMP WITH TIME ZONE,
    duracion_real INTERVAL,
    
    -- Detalles clínicos
    dientes_afectados INTEGER[],
    diagnostico_inicial TEXT,
    procedimiento_realizado TEXT NOT NULL,
    materiales_utilizados TEXT[],
    anestesia_utilizada TEXT,
    complicaciones TEXT,
    
    -- INFORMACIÓN ECONÓMICA EN MÚLTIPLES MONEDAS
    total_bs DECIMAL(10,2) DEFAULT 0,
    total_usd DECIMAL(10,2) DEFAULT 0,
    descuento_bs DECIMAL(10,2) DEFAULT 0,
    descuento_usd DECIMAL(10,2) DEFAULT 0,
    
    -- Estado del procedimiento
    estado VARCHAR(20) DEFAULT 'completada' CHECK (estado IN ('en_progreso', 'completada', 'suspendida')),
    
    -- Seguimiento
    requiere_control BOOLEAN DEFAULT FALSE,
    fecha_control_sugerida DATE,
    instrucciones_paciente TEXT,
    
    -- CAMBIOS AL ODONTOGRAMA EN ESTA INTERVENCIÓN
    cambios_odontograma JSONB DEFAULT '[]',
    
    fecha_registro TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT chk_intervenciones_totales CHECK (total_bs >= 0 AND total_usd >= 0),
    CONSTRAINT chk_intervenciones_descuentos CHECK (descuento_bs >= 0 AND descuento_usd >= 0)
);

-- =====================================================
-- TABLA 8: SERVICIOS POR INTERVENCIÓN
-- =====================================================
CREATE TABLE intervenciones_servicios (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    intervencion_id UUID REFERENCES intervenciones(id) ON DELETE CASCADE NOT NULL,
    servicio_id UUID REFERENCES servicios(id) NOT NULL,
    cantidad INTEGER DEFAULT 1 CHECK (cantidad > 0),
    
    -- Precios específicos de este servicio en esta intervención
    precio_unitario_bs DECIMAL(10,2) NOT NULL,
    precio_unitario_usd DECIMAL(10,2) NOT NULL,
    precio_total_bs DECIMAL(10,2) NOT NULL,
    precio_total_usd DECIMAL(10,2) NOT NULL,
    
    -- Detalles específicos del servicio
    dientes_especificos INTEGER[],
    observaciones_servicio TEXT,
    
    fecha_registro TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT chk_interv_serv_precios CHECK (
        precio_unitario_bs > 0 AND precio_unitario_usd > 0 AND
        precio_total_bs = (cantidad * precio_unitario_bs) AND
        precio_total_usd = (cantidad * precio_unitario_usd)
    )
);

-- =====================================================
-- TABLA 9: HISTORIAL MÉDICO
-- =====================================================
CREATE TABLE historial_medico (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    paciente_id UUID REFERENCES pacientes(id) NOT NULL,
    consulta_id UUID REFERENCES consultas(id),
    intervencion_id UUID REFERENCES intervenciones(id),
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
    medicamentos_recetados JSONB DEFAULT '[]',
    recomendaciones TEXT,
    contraindicaciones TEXT,
    
    -- Signos vitales
    presion_arterial VARCHAR(20),
    frecuencia_cardiaca INTEGER,
    temperatura DECIMAL(4,2),
    
    -- Archivos adjuntos
    imagenes_url TEXT[],
    documentos_url TEXT[],
    
    -- Seguimiento
    proxima_consulta DATE,
    observaciones TEXT,
    confidencial BOOLEAN DEFAULT FALSE,
    
    CONSTRAINT chk_historial_temperatura CHECK (temperatura IS NULL OR (temperatura >= 30 AND temperatura <= 45)),
    CONSTRAINT chk_historial_frecuencia CHECK (frecuencia_cardiaca IS NULL OR (frecuencia_cardiaca >= 40 AND frecuencia_cardiaca <= 200))
);

-- =====================================================
-- TABLA 10: SISTEMA DE PAGOS MIXTOS
-- =====================================================
CREATE TABLE pagos (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    numero_recibo VARCHAR(20) UNIQUE NOT NULL,
    consulta_id UUID REFERENCES consultas(id),
    paciente_id UUID REFERENCES pacientes(id) NOT NULL,
    
    -- INFORMACIÓN DEL PAGO MIXTO
    fecha_pago TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    monto_total_bs DECIMAL(10,2) DEFAULT 0,
    monto_total_usd DECIMAL(10,2) DEFAULT 0,
    monto_pagado_bs DECIMAL(10,2) DEFAULT 0,
    monto_pagado_usd DECIMAL(10,2) DEFAULT 0,
    saldo_pendiente_bs DECIMAL(10,2) DEFAULT 0,
    saldo_pendiente_usd DECIMAL(10,2) DEFAULT 0,
    
    -- TASA DE CAMBIO AL MOMENTO DEL PAGO
    tasa_cambio_bs_usd DECIMAL(10,4),
    
    -- Métodos de pago múltiples
    metodos_pago JSONB DEFAULT '[]',
    
    -- Detalles adicionales
    concepto TEXT NOT NULL,
    descuento_bs DECIMAL(10,2) DEFAULT 0,
    descuento_usd DECIMAL(10,2) DEFAULT 0,
    motivo_descuento TEXT,
    impuestos_bs DECIMAL(10,2) DEFAULT 0,
    impuestos_usd DECIMAL(10,2) DEFAULT 0,
    
    -- Control administrativo
    estado_pago VARCHAR(20) DEFAULT 'completado' CHECK (estado_pago IN ('pendiente', 'completado', 'parcial', 'anulado', 'reembolsado')),
    procesado_por UUID REFERENCES usuarios(id) NOT NULL,
    autorizado_por UUID REFERENCES usuarios(id),
    
    -- Facturación
    numero_factura VARCHAR(50),
    fecha_facturacion DATE,
    observaciones TEXT,
    
    CONSTRAINT chk_pagos_montos CHECK (
        monto_total_bs >= 0 AND monto_total_usd >= 0 AND
        monto_pagado_bs >= 0 AND monto_pagado_usd >= 0 AND
        saldo_pendiente_bs >= 0 AND saldo_pendiente_usd >= 0
    ),
    CONSTRAINT chk_pagos_descuentos CHECK (descuento_bs >= 0 AND descuento_usd >= 0)
);

-- =====================================================
-- TABLA 11: ODONTOGRAMA CON VERSIONADO
-- =====================================================
CREATE TABLE odontograma (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    paciente_id UUID REFERENCES pacientes(id) NOT NULL,
    fecha_creacion TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    odontologo_id UUID REFERENCES personal(id) NOT NULL,
    
    -- SISTEMA DE VERSIONES
    version INTEGER DEFAULT 1,
    es_version_actual BOOLEAN DEFAULT TRUE,
    version_anterior_id UUID REFERENCES odontograma(id),
    motivo_nueva_version TEXT,
    
    tipo_odontograma VARCHAR(20) DEFAULT 'adulto' CHECK (tipo_odontograma IN ('adulto', 'pediatrico', 'mixto')),
    
    notas_generales TEXT,
    observaciones_clinicas TEXT,
    
    -- Metadatos para renderizado
    template_usado VARCHAR(50) DEFAULT 'universal',
    configuracion JSONB DEFAULT '{}',
    
    -- METADATOS PARA PRESENTACIÓN DE TESIS
    estadisticas_condiciones JSONB DEFAULT '{}',
    
    CONSTRAINT chk_odontograma_version CHECK (version > 0)
);

-- =====================================================
-- TABLA 12: CATÁLOGO DE DIENTES (FDI)
-- =====================================================
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
    
    -- METADATOS PARA RENDERIZADO DETALLADO
    coordenadas_svg JSONB DEFAULT '{}',
    forma_base VARCHAR(20) DEFAULT 'rectangular',
    
    activo BOOLEAN DEFAULT TRUE
);

-- =====================================================
-- TABLA 13: CONDICIONES DE DIENTES (DETALLADA PARA TESIS)
-- =====================================================
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
    
    -- DESCRIPCIÓN DETALLADA PARA TESIS
    descripcion TEXT,
    observaciones TEXT,
    hallazgos_clinicos TEXT,
    
    -- Material y tratamiento
    material_utilizado VARCHAR(100),
    color_material VARCHAR(50),
    fecha_tratamiento DATE,
    
    -- INFORMACIÓN DETALLADA DEL TRATAMIENTO
    tecnica_utilizada VARCHAR(100),
    tiempo_tratamiento INTERVAL,
    
    -- Estado y seguimiento
    estado VARCHAR(20) DEFAULT 'actual' CHECK (estado IN ('planificado', 'en_tratamiento', 'actual', 'historico')),
    requiere_seguimiento BOOLEAN DEFAULT FALSE,
    fecha_proximo_control DATE,
    
    -- Control de versiones
    fecha_registro TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    registrado_por UUID REFERENCES usuarios(id),
    intervencion_origen_id UUID REFERENCES intervenciones(id),
    
    -- METADATOS PARA RENDERIZADO DETALLADO
    posicion_x DECIMAL(5,2),
    posicion_y DECIMAL(5,2),
    color_hex VARCHAR(7) DEFAULT '#FFFFFF',
    forma_renderizado VARCHAR(20) DEFAULT 'default',
    
    -- ANOTACIONES DETALLADAS PARA TESIS
    anotaciones_detalladas JSONB DEFAULT '{}',
    imagenes_referencia TEXT[],
    documentos_adjuntos TEXT[]
);

-- =====================================================
-- TABLA 14: IMÁGENES CLÍNICAS
-- =====================================================
CREATE TABLE imagenes_clinicas (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    paciente_id UUID REFERENCES pacientes(id) NOT NULL,
    consulta_id UUID REFERENCES consultas(id),
    intervencion_id UUID REFERENCES intervenciones(id),
    odontograma_id UUID REFERENCES odontograma(id),
    
    -- Información de la imagen
    titulo VARCHAR(200) NOT NULL,
    descripcion TEXT,
    tipo_imagen VARCHAR(50) NOT NULL CHECK (tipo_imagen IN (
        'radiografia_panoramica', 'radiografia_periapical', 'radiografia_bite_wing',
        'fotografia_intraoral', 'fotografia_extraoral', 'fotografia_oclusal',
        'tomografia', 'escaner_3d', 'antes_tratamiento', 'despues_tratamiento', 'otro'
    )),
    
    -- Almacenamiento
    url_imagen TEXT NOT NULL,
    url_thumbnail TEXT,
    tamaño_archivo BIGINT,
    formato_archivo VARCHAR(10),
    
    -- Metadatos
    fecha_captura TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    capturada_por UUID REFERENCES usuarios(id),
    equipo_utilizado VARCHAR(100),
    configuracion_equipo JSONB DEFAULT '{}',
    
    -- ANOTACIONES EN LA IMAGEN PARA TESIS
    anotaciones_imagen JSONB DEFAULT '[]',
    dientes_visibles INTEGER[],
    
    -- Clasificación y búsqueda
    es_confidencial BOOLEAN DEFAULT FALSE,
    tags TEXT[],
    activo BOOLEAN DEFAULT TRUE
);

-- =====================================================
-- TABLA 15: AUDITORÍA DEL SISTEMA
-- =====================================================
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

-- =====================================================
-- TABLA 16: CONFIGURACIÓN DEL SISTEMA
-- =====================================================
CREATE TABLE configuracion_sistema (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    clave VARCHAR(100) UNIQUE NOT NULL,
    valor JSONB NOT NULL,
    descripcion TEXT,
    categoria VARCHAR(50) NOT NULL,
    tipo_dato VARCHAR(20) NOT NULL CHECK (tipo_dato IN ('string', 'number', 'boolean', 'json', 'array')),
    es_publica BOOLEAN DEFAULT FALSE,
    modificado_por UUID REFERENCES usuarios(id),
    fecha_modificacion TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- TABLA 17: COLA DE ATENCIÓN POR ODONTÓLOGO
-- =====================================================
CREATE TABLE cola_atencion (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    consulta_id UUID REFERENCES consultas(id) NOT NULL,
    odontologo_id UUID REFERENCES personal(id) NOT NULL,
    posicion_cola INTEGER NOT NULL,
    fecha_ingreso_cola TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    fecha_salida_cola TIMESTAMP WITH TIME ZONE,
    estado_cola VARCHAR(20) DEFAULT 'esperando' CHECK (estado_cola IN (
        'esperando',
        'siendo_atendido',
        'atendido',
        'derivado',
        'cancelado'
    )),
    observaciones TEXT,
    
    CONSTRAINT uq_consulta_odontologo_activo UNIQUE (consulta_id, odontologo_id)
);

-- =====================================================
-- ÍNDICES PARA OPTIMIZACIÓN
-- =====================================================

-- Usuarios y autenticación
CREATE INDEX idx_usuarios_email ON usuarios(email);
CREATE INDEX idx_usuarios_auth_user_id ON usuarios(auth_user_id);
CREATE INDEX idx_usuarios_activo ON usuarios(activo);

-- Personal
CREATE INDEX idx_personal_usuario_id ON personal(usuario_id);
CREATE INDEX idx_personal_tipo_estado ON personal(tipo_personal, estado_laboral);
CREATE INDEX idx_personal_documento ON personal(numero_documento);
CREATE INDEX idx_personal_odontologos_disponibles ON personal(tipo_personal, acepta_pacientes_nuevos, estado_laboral);

-- Pacientes
CREATE INDEX idx_pacientes_numero_documento ON pacientes(numero_documento);
CREATE INDEX idx_pacientes_activo ON pacientes(activo);
CREATE INDEX idx_pacientes_fecha_registro ON pacientes(fecha_registro);
CREATE INDEX idx_pacientes_nombres_completo ON pacientes(primer_nombre, primer_apellido);
CREATE INDEX idx_pacientes_celular1 ON pacientes(celular_1);

-- Consultas - OPTIMIZADO PARA FLUJO
CREATE INDEX idx_consultas_paciente_fecha ON consultas(paciente_id, fecha_llegada);
CREATE INDEX idx_consultas_primer_odontologo ON consultas(primer_odontologo_id, fecha_llegada);
CREATE INDEX idx_consultas_estado_fecha ON consultas(estado, fecha_llegada);
CREATE INDEX idx_consultas_orden_general ON consultas(orden_llegada_general);
CREATE INDEX idx_consultas_cola_odontologo ON consultas(primer_odontologo_id, orden_cola_odontologo);

-- Intervenciones
CREATE INDEX idx_intervenciones_consulta ON intervenciones(consulta_id);
CREATE INDEX idx_intervenciones_odontologo_fecha ON intervenciones(odontologo_id, hora_inicio);
CREATE INDEX idx_intervenciones_estado ON intervenciones(estado);

-- Servicios por intervención
CREATE INDEX idx_interv_servicios_intervencion ON intervenciones_servicios(intervencion_id);
CREATE INDEX idx_interv_servicios_servicio ON intervenciones_servicios(servicio_id);

-- Pagos
CREATE INDEX idx_pagos_paciente_fecha ON pagos(paciente_id, fecha_pago);
CREATE INDEX idx_pagos_estado_fecha ON pagos(estado_pago, fecha_pago);
CREATE INDEX idx_pagos_numero_recibo ON pagos(numero_recibo);

-- Odontograma con versionado
CREATE INDEX idx_odontograma_paciente_version ON odontograma(paciente_id, version);
CREATE INDEX idx_odontograma_actual ON odontograma(paciente_id, es_version_actual);
CREATE INDEX idx_condiciones_odontograma ON condiciones_diente(odontograma_id);
CREATE INDEX idx_condiciones_diente ON condiciones_diente(diente_id);

-- Cola de atención
CREATE INDEX idx_cola_odontologo_posicion ON cola_atencion(odontologo_id, posicion_cola, estado_cola);
CREATE INDEX idx_cola_consulta ON cola_atencion(consulta_id);

-- =====================================================
-- FUNCIONES Y TRIGGERS AUTOMÁTICOS
-- =====================================================

-- Función para actualizar fecha_actualizacion
CREATE OR REPLACE FUNCTION actualizar_fecha_modificacion()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    NEW.fecha_actualizacion = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$;

-- Triggers para actualización automática
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

-- Función para calcular totales de intervención automáticamente
CREATE OR REPLACE FUNCTION calcular_totales_intervencion()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
DECLARE
    total_bs_calc DECIMAL(10,2) := 0;
    total_usd_calc DECIMAL(10,2) := 0;
BEGIN
    -- Calcular totales de servicios para esta intervención
    SELECT 
        COALESCE(SUM(precio_total_bs), 0),
        COALESCE(SUM(precio_total_usd), 0)
    INTO total_bs_calc, total_usd_calc
    FROM intervenciones_servicios 
    WHERE intervencion_id = COALESCE(NEW.intervencion_id, OLD.intervencion_id);
    
    -- Actualizar totales en la intervención
    UPDATE intervenciones 
    SET 
        total_bs = total_bs_calc - COALESCE(descuento_bs, 0),
        total_usd = total_usd_calc - COALESCE(descuento_usd, 0)
    WHERE id = COALESCE(NEW.intervencion_id, OLD.intervencion_id);
    
    RETURN COALESCE(NEW, OLD);
END;
$$;

CREATE TRIGGER trigger_calcular_totales_intervencion
    AFTER INSERT OR UPDATE OR DELETE ON intervenciones_servicios
    FOR EACH ROW EXECUTE FUNCTION calcular_totales_intervencion();

-- Función para actualizar costos de consulta automáticamente
CREATE OR REPLACE FUNCTION actualizar_costos_consulta()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
DECLARE
    costo_bs_calc DECIMAL(10,2) := 0;
    costo_usd_calc DECIMAL(10,2) := 0;
BEGIN
    -- Calcular costos totales de todas las intervenciones de esta consulta
    SELECT 
        COALESCE(SUM(total_bs), 0),
        COALESCE(SUM(total_usd), 0)
    INTO costo_bs_calc, costo_usd_calc
    FROM intervenciones 
    WHERE consulta_id = COALESCE(NEW.consulta_id, OLD.consulta_id);
    
    -- Actualizar costos en la consulta
    UPDATE consultas 
    SET 
        costo_total_bs = costo_bs_calc,
        costo_total_usd = costo_usd_calc
    WHERE id = COALESCE(NEW.consulta_id, OLD.consulta_id);
    
    RETURN COALESCE(NEW, OLD);
END;
$$;

CREATE TRIGGER trigger_actualizar_costos_consulta
    AFTER INSERT OR UPDATE OR DELETE ON intervenciones
    FOR EACH ROW EXECUTE FUNCTION actualizar_costos_consulta();

-- Función para calcular saldo pendiente en pagos
CREATE OR REPLACE FUNCTION calcular_saldos_pago()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    NEW.saldo_pendiente_bs = NEW.monto_total_bs - NEW.monto_pagado_bs;
    NEW.saldo_pendiente_usd = NEW.monto_total_usd - NEW.monto_pagado_usd;
    RETURN NEW;
END;
$$;

CREATE TRIGGER trigger_calcular_saldos_pago
    BEFORE INSERT OR UPDATE ON pagos
    FOR EACH ROW EXECUTE FUNCTION calcular_saldos_pago();

-- Función para calcular edad del paciente
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

-- Función para manejar versionado de odontograma
CREATE OR REPLACE FUNCTION manejar_version_odontograma()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    -- Si se está creando una nueva versión actual
    IF NEW.es_version_actual = TRUE THEN
        -- Marcar todas las otras versiones como no actuales
        UPDATE odontograma 
        SET es_version_actual = FALSE 
        WHERE paciente_id = NEW.paciente_id 
        AND id != NEW.id;
        
        -- Si no es la primera versión, calcular estadísticas
        IF NEW.version > 1 THEN
            NEW.estadisticas_condiciones = (
                SELECT jsonb_build_object(
                    'total_condiciones', COUNT(*),
                    'condiciones_por_tipo', jsonb_object_agg(tipo_condicion, cantidad)
                )
                FROM (
                    SELECT tipo_condicion, COUNT(*) as cantidad
                    FROM condiciones_diente 
                    WHERE odontograma_id = NEW.id
                    GROUP BY tipo_condicion
                ) stats
            );
        END IF;
    END IF;
    
    RETURN NEW;
END;
$$;

CREATE TRIGGER trigger_manejar_version_odontograma
    BEFORE INSERT OR UPDATE ON odontograma
    FOR EACH ROW EXECUTE FUNCTION manejar_version_odontograma();

-- =====================================================
-- FUNCIONES PARA GENERAR NÚMEROS ÚNICOS
-- =====================================================

-- Función para generar número de historia clínica
CREATE OR REPLACE FUNCTION generar_numero_historia()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
DECLARE
    ultimo_numero INTEGER;
    nuevo_numero VARCHAR(20);
BEGIN
    IF NEW.numero_historia IS NULL OR NEW.numero_historia = '' THEN
        SELECT COALESCE(MAX(CAST(SUBSTRING(numero_historia FROM 3) AS INTEGER)), 0) + 1
        INTO ultimo_numero
        FROM pacientes
        WHERE numero_historia ~ '^HC[0-9]+$';
        
        nuevo_numero := 'HC' || LPAD(ultimo_numero::TEXT, 6, '0');
        NEW.numero_historia := nuevo_numero;
    END IF;
    
    RETURN NEW;
END;
$$;

CREATE TRIGGER trigger_generar_numero_historia
    BEFORE INSERT ON pacientes
    FOR EACH ROW EXECUTE FUNCTION generar_numero_historia();

-- Función para generar número de consulta
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
        
        SELECT COALESCE(MAX(CAST(SUBSTRING(numero_consulta FROM 10) AS INTEGER)), 0) + 1
        INTO ultimo_numero
        FROM consultas
        WHERE numero_consulta ~ ('^' || TO_CHAR(fecha_actual, 'YYYYMMDD') || '[0-9]+$');
        
        nuevo_numero := TO_CHAR(fecha_actual, 'YYYYMMDD') || LPAD(ultimo_numero::TEXT, 3, '0');
        NEW.numero_consulta := nuevo_numero;
    END IF;
    
    RETURN NEW;
END;
$$;

CREATE TRIGGER trigger_generar_numero_consulta
    BEFORE INSERT ON consultas
    FOR EACH ROW EXECUTE FUNCTION generar_numero_consulta();

-- Función para manejar orden de llegada automáticamente
CREATE OR REPLACE FUNCTION asignar_orden_llegada()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
DECLARE
    ultimo_orden_general INTEGER;
    ultimo_orden_odontologo INTEGER;
BEGIN
    -- Asignar orden general del día
    SELECT COALESCE(MAX(orden_llegada_general), 0) + 1
    INTO ultimo_orden_general
    FROM consultas
    WHERE DATE(fecha_llegada) = DATE(NEW.fecha_llegada);
    
    NEW.orden_llegada_general := ultimo_orden_general;
    
    -- Asignar orden en cola del odontólogo
    SELECT COALESCE(MAX(orden_cola_odontologo), 0) + 1
    INTO ultimo_orden_odontologo
    FROM consultas
    WHERE primer_odontologo_id = NEW.primer_odontologo_id
    AND DATE(fecha_llegada) = DATE(NEW.fecha_llegada)
    AND estado IN ('en_espera', 'en_atencion');
    
    NEW.orden_cola_odontologo := ultimo_orden_odontologo;
    
    RETURN NEW;
END;
$$;

CREATE TRIGGER trigger_asignar_orden_llegada
    BEFORE INSERT ON consultas
    FOR EACH ROW EXECUTE FUNCTION asignar_orden_llegada();

-- Función para generar número de recibo
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
        
        SELECT COALESCE(MAX(CAST(SUBSTRING(numero_recibo FROM 8) AS INTEGER)), 0) + 1
        INTO ultimo_numero
        FROM pagos
        WHERE numero_recibo ~ ('^REC' || TO_CHAR(fecha_actual, 'YYYYMM') || '[0-9]+$');
        
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
-- VISTAS OPTIMIZADAS PARA EL FLUJO ESPECÍFICO
-- =====================================================

-- Vista de consultas del día con cola por odontólogo
CREATE OR REPLACE VIEW vista_consultas_dia AS
SELECT 
    c.id,
    c.numero_consulta,
    c.fecha_llegada,
    c.estado,
    c.tipo_consulta,
    c.motivo_consulta,
    c.orden_llegada_general,
    c.orden_cola_odontologo,
    c.costo_total_bs,
    c.costo_total_usd,
    
    -- Información del paciente
    p.numero_historia,
    TRIM(CONCAT(p.primer_nombre, ' ', COALESCE(p.segundo_nombre, ''), ' ', p.primer_apellido, ' ', COALESCE(p.segundo_apellido, ''))) as paciente_nombre,
    p.celular_1 as paciente_celular,
    p.numero_documento as paciente_documento,
    
    -- Información del primer odontólogo
    pers_primer.id as primer_odontologo_id,
    TRIM(CONCAT(pers_primer.primer_nombre, ' ', COALESCE(pers_primer.segundo_nombre, ''), ' ', pers_primer.primer_apellido, ' ', COALESCE(pers_primer.segundo_apellido, ''))) as primer_odontologo_nombre,
    pers_primer.especialidad as primer_odontologo_especialidad,
    
    -- Información del odontólogo preferido (si es diferente)
    CASE 
        WHEN c.odontologo_preferido_id IS NOT NULL AND c.odontologo_preferido_id != c.primer_odontologo_id THEN
            TRIM(CONCAT(pers_pref.primer_nombre, ' ', COALESCE(pers_pref.segundo_nombre, ''), ' ', pers_pref.primer_apellido, ' ', COALESCE(pers_pref.segundo_apellido, '')))
        ELSE NULL
    END as odontologo_preferido_nombre,
    
    -- Estadísticas de la consulta
    (SELECT COUNT(*) FROM intervenciones WHERE consulta_id = c.id) as total_intervenciones,
    (SELECT COUNT(DISTINCT odontologo_id) FROM intervenciones WHERE consulta_id = c.id) as total_odontologos_atendieron

FROM consultas c
JOIN pacientes p ON c.paciente_id = p.id
JOIN personal pers_primer ON c.primer_odontologo_id = pers_primer.id
LEFT JOIN personal pers_pref ON c.odontologo_preferido_id = pers_pref.id
WHERE DATE(c.fecha_llegada) = CURRENT_DATE
ORDER BY c.orden_llegada_general;

-- Vista de cola por odontólogo
CREATE OR REPLACE VIEW vista_cola_odontologos AS
SELECT 
    pers.id as odontologo_id,
    TRIM(CONCAT(pers.primer_nombre, ' ', COALESCE(pers.segundo_nombre, ''), ' ', pers.primer_apellido, ' ', COALESCE(pers.segundo_apellido, ''))) as odontologo_nombre,
    pers.especialidad,
    pers.acepta_pacientes_nuevos,
    
    -- Estadísticas de cola
    COUNT(CASE WHEN c.estado = 'en_espera' THEN 1 END) as pacientes_esperando,
    COUNT(CASE WHEN c.estado = 'en_atencion' AND c.primer_odontologo_id = pers.id THEN 1 END) as pacientes_atendiendo,
    COUNT(CASE WHEN c.estado = 'completada' AND DATE(c.fecha_llegada) = CURRENT_DATE THEN 1 END) as pacientes_atendidos_hoy,
    
    -- Próximo paciente en cola
    MIN(CASE WHEN c.estado = 'en_espera' THEN c.orden_cola_odontologo END) as proximo_en_cola

FROM personal pers
LEFT JOIN consultas c ON pers.id = c.primer_odontologo_id AND DATE(c.fecha_llegada) = CURRENT_DATE
WHERE pers.tipo_personal = 'Odontólogo' 
AND pers.estado_laboral = 'activo'
GROUP BY pers.id, pers.primer_nombre, pers.segundo_nombre, pers.primer_apellido, pers.segundo_apellido, pers.especialidad, pers.acepta_pacientes_nuevos
ORDER BY pacientes_esperando ASC, pers.orden_preferencia;

-- =====================================================
-- FUNCIONES ESPECÍFICAS PARA EL FLUJO DE TRABAJO
-- =====================================================

-- Función para obtener próximo paciente en cola
CREATE OR REPLACE FUNCTION obtener_proximo_paciente(odontologo_id_param UUID)
RETURNS TABLE(
    consulta_id UUID,
    paciente_nombre TEXT,
    numero_historia VARCHAR,
    orden_cola INTEGER,
    tiempo_espera INTERVAL
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT 
        c.id,
        TRIM(CONCAT(p.primer_nombre, ' ', COALESCE(p.segundo_nombre, ''), ' ', p.primer_apellido, ' ', COALESCE(p.segundo_apellido, ''))),
        p.numero_historia,
        c.orden_cola_odontologo,
        AGE(CURRENT_TIMESTAMP, c.fecha_llegada)
    FROM consultas c
    JOIN pacientes p ON c.paciente_id = p.id
    WHERE c.primer_odontologo_id = odontologo_id_param
    AND c.estado = 'en_espera'
    AND DATE(c.fecha_llegada) = CURRENT_DATE
    ORDER BY c.orden_cola_odontologo
    LIMIT 1;
END;
$$;

-- Función para cambiar paciente de odontólogo
CREATE OR REPLACE FUNCTION cambiar_odontologo_consulta(
    consulta_id_param UUID,
    nuevo_odontologo_id UUID,
    motivo TEXT DEFAULT NULL
)
RETURNS BOOLEAN
LANGUAGE plpgsql
AS $$
DECLARE
    ultimo_orden INTEGER;
BEGIN
    -- Obtener último orden en cola del nuevo odontólogo
    SELECT COALESCE(MAX(orden_cola_odontologo), 0) + 1
    INTO ultimo_orden
    FROM consultas
    WHERE primer_odontologo_id = nuevo_odontologo_id
    AND DATE(fecha_llegada) = CURRENT_DATE
    AND estado IN ('en_espera', 'en_atencion');
    
    -- Actualizar la consulta
    UPDATE consultas
    SET 
        primer_odontologo_id = nuevo_odontologo_id,
        orden_cola_odontologo = ultimo_orden,
        observaciones = COALESCE(observaciones, '') || 
            CASE WHEN observaciones IS NOT NULL THEN E'\n' ELSE '' END ||
            'Cambiado de odontólogo: ' || COALESCE(motivo, 'Sin motivo especificado') || ' - ' || CURRENT_TIMESTAMP
    WHERE id = consulta_id_param;
    
    RETURN FOUND;
END;
$$;

-- =====================================================
-- ROW LEVEL SECURITY (RLS)
-- =====================================================
ALTER TABLE usuarios ENABLE ROW LEVEL SECURITY;
ALTER TABLE personal ENABLE ROW LEVEL SECURITY;
ALTER TABLE pacientes ENABLE ROW LEVEL SECURITY;
ALTER TABLE consultas ENABLE ROW LEVEL SECURITY;
ALTER TABLE intervenciones ENABLE ROW LEVEL SECURITY;
ALTER TABLE historial_medico ENABLE ROW LEVEL SECURITY;
ALTER TABLE pagos ENABLE ROW LEVEL SECURITY;
ALTER TABLE odontograma ENABLE ROW LEVEL SECURITY;

-- Políticas básicas
CREATE POLICY "usuarios_policy" ON usuarios FOR ALL USING (true);
CREATE POLICY "personal_policy" ON personal FOR ALL USING (true);
CREATE POLICY "pacientes_policy" ON pacientes FOR ALL USING (true);
CREATE POLICY "consultas_policy" ON consultas FOR ALL USING (true);
CREATE POLICY "intervenciones_policy" ON intervenciones FOR ALL USING (true);
CREATE POLICY "historial_medico_policy" ON historial_medico FOR ALL USING (true);
CREATE POLICY "pagos_policy" ON pagos FOR ALL USING (true);
CREATE POLICY "odontograma_policy" ON odontograma FOR ALL USING (true);

-- =====================================================
-- DATOS INICIALES DEL SISTEMA
-- =====================================================

-- Roles del sistema
INSERT INTO roles (nombre, descripcion, permisos) VALUES 
('gerente', 'Acceso completo al sistema', '{
    "usuarios": ["crear", "leer", "actualizar", "eliminar"],
    "pacientes": ["crear", "leer", "actualizar", "eliminar"],
    "consultas": ["crear", "leer", "actualizar", "eliminar"],
    "servicios": ["crear", "leer", "actualizar", "eliminar"],
    "personal": ["crear", "leer", "actualizar", "eliminar"],
    "pagos": ["crear", "leer", "actualizar", "eliminar"],
    "reportes": ["leer", "generar"],
    "configuracion": ["leer", "actualizar"],
    "odontograma": ["crear", "leer", "actualizar"],
    "cola_atencion": ["leer", "actualizar"]
}'),
('administrador', 'Gestión de pacientes, consultas y pagos', '{
    "pacientes": ["crear", "leer", "actualizar"],
    "consultas": ["crear", "leer", "actualizar", "eliminar"],
    "pagos": ["crear", "leer", "actualizar"],
    "servicios": ["leer"],
    "reportes": ["leer"],
    "cola_atencion": ["leer", "actualizar"]
}'),
('odontologo', 'Atención de pacientes y gestión clínica', '{
    "pacientes": ["leer", "actualizar"],
    "consultas": ["leer", "actualizar"],
    "intervenciones": ["crear", "leer", "actualizar"],
    "odontograma": ["crear", "leer", "actualizar"],
    "historial_medico": ["crear", "leer", "actualizar"],
    "servicios": ["leer"],
    "cola_atencion": ["leer"]
}'),
('asistente', 'Apoyo en consultas y tareas básicas', '{
    "pacientes": ["leer"],
    "consultas": ["leer"],
    "servicios": ["leer"],
    "cola_atencion": ["leer"]
}');

-- Configuraciones del sistema
INSERT INTO configuracion_sistema (clave, valor, descripcion, categoria, tipo_dato, es_publica) VALUES
('consultorio_nombre', '"Clínica Dental OdontoMara"', 'Nombre del consultorio', 'general', 'string', true),
('consultorio_direccion', '"Puerto La Cruz, Estado Anzoátegui"', 'Dirección del consultorio', 'general', 'string', true),
('consultorio_celular', '"+58 281-123-4567"', 'Celular del consultorio', 'general', 'string', true),
('duracion_consulta_default', '30', 'Duración por defecto de consultas en minutos', 'operacion', 'number', false),
('moneda_principal', '"VES"', 'Moneda principal del sistema', 'financiero', 'string', true),
('moneda_secundaria', '"USD"', 'Moneda secundaria del sistema', 'financiero', 'string', true),
('tasa_cambio_actual', '36.50', 'Tasa de cambio actual VES/USD', 'financiero', 'number', false),
('version_odontograma_auto', 'true', 'Crear nueva versión automáticamente al modificar', 'clinico', 'boolean', false);

-- Servicios básicos con precios en ambas monedas
INSERT INTO servicios (codigo, nombre, descripcion, categoria, precio_base_bs, precio_base_usd) VALUES
('CONS001', 'Consulta General', 'Consulta odontológica general', 'Consulta', 1825.00, 50.00),
('LIMP001', 'Profilaxis Dental', 'Limpieza dental profesional', 'Preventiva', 2920.00, 80.00),
('OBTU001', 'Obturación Simple', 'Restauración dental con resina', 'Restaurativa', 4380.00, 120.00),
('ENDO001', 'Endodoncia', 'Tratamiento de conducto radicular', 'Endodoncia', 12775.00, 350.00),
('EXTR001', 'Extracción Simple', 'Extracción dental simple', 'Cirugía', 2920.00, 80.00),
('EXTR002', 'Extracción Compleja', 'Extracción dental compleja', 'Cirugía', 5475.00, 150.00),
('CORO001', 'Corona Dental', 'Corona en porcelana o metal-porcelana', 'Prótesis', 29200.00, 800.00),
('IMPL001', 'Implante Dental', 'Implante titanio + corona', 'Implantología', 73000.00, 2000.00),
('BLAN001', 'Blanqueamiento', 'Blanqueamiento dental en consultorio', 'Estética', 10950.00, 300.00),
('RADI001', 'Radiografía Panorámica', 'Radiografía panorámica digital', 'Diagnóstico', 2190.00, 60.00);

-- Catálogo completo de dientes según numeración FDI (solo algunos ejemplos por brevedad)
INSERT INTO dientes (numero_diente, nombre, tipo_diente, ubicacion, cuadrante, posicion_en_cuadrante, es_temporal, caras) VALUES
-- Dientes permanentes - Cuadrante 1 (Superior Derecho)
(11, 'Incisivo Central Superior Derecho', 'incisivo', 'superior_derecha', 1, 1, false, ARRAY['incisal', 'mesial', 'distal', 'vestibular', 'palatino']),
(12, 'Incisivo Lateral Superior Derecho', 'incisivo', 'superior_derecha', 1, 2, false, ARRAY['incisal', 'mesial', 'distal', 'vestibular', 'palatino']),
(13, 'Canino Superior Derecho', 'canino', 'superior_derecha', 1, 3, false, ARRAY['incisal', 'mesial', 'distal', 'vestibular', 'palatino']),
(14, 'Primer Premolar Superior Derecho', 'premolar', 'superior_derecha', 1, 4, false, ARRAY['oclusal', 'mesial', 'distal', 'vestibular', 'palatino']),
(15, 'Segundo Premolar Superior Derecho', 'premolar', 'superior_derecha', 1, 5, false, ARRAY['oclusal', 'mesial', 'distal', 'vestibular', 'palatino']),
(16, 'Primer Molar Superior Derecho', 'molar', 'superior_derecha', 1, 6, false, ARRAY['oclusal', 'mesial', 'distal', 'vestibular', 'palatino']),
(17, 'Segundo Molar Superior Derecho', 'molar', 'superior_derecha', 1, 7, false, ARRAY['oclusal', 'mesial', 'distal', 'vestibular', 'palatino']),
(18, 'Tercer Molar Superior Derecho', 'molar', 'superior_derecha', 1, 8, false, ARRAY['oclusal', 'mesial', 'distal', 'vestibular', 'palatino']);
-- [Continuar con el resto de dientes...]

-- =====================================================
-- PERMISOS FINALES
-- =====================================================
GRANT SELECT ON ALL TABLES IN SCHEMA public TO authenticated;
GRANT INSERT, UPDATE ON usuarios, personal, pacientes, consultas, intervenciones, historial_medico, pagos, odontograma, condiciones_diente, intervenciones_servicios, cola_atencion TO authenticated;
GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA public TO authenticated;
GRANT SELECT ON ALL SEQUENCES IN SCHEMA public TO authenticated;

-- =====================================================
-- ESQUEMA FINAL CORREGIDO COMPLETADO
-- =====================================================

COMMENT ON SCHEMA public IS 'Esquema corregido para Sistema Odontológico - Clínica Dental OdontoMara - Versión 4.1';