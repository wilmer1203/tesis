-- ============================================================================
-- ESQUEMA DE BASE DE DATOS - SISTEMA DE GESTIÓN ODONTOLÓGICA V2.0
-- Universidad de Oriente - Trabajo de Grado - Ingeniería de Sistemas
-- Estudiante: Wilmer Aguirre
-- Última actualización: 2025-10-07
-- ============================================================================

-- ============================================================================
-- SECCIÓN 1: FUNCIONES DE NEGOCIO
-- ============================================================================

-- ----------------------------------------------------------------------------
-- 1.1 FUNCIONES DE AUTO-NUMERACIÓN
-- ----------------------------------------------------------------------------

-- Generar número de historia clínica (HC000001, HC000002, ...)
CREATE OR REPLACE FUNCTION generar_numero_historia()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
DECLARE
    ultimo_numero INTEGER;
    nuevo_numero VARCHAR(20);
BEGIN
    IF NEW.numero_historia IS NULL OR NEW.numero_historia = '' THEN
        SELECT COALESCE(
            MAX(CAST(SUBSTRING(numero_historia FROM 3) AS INTEGER)), 0
        ) + 1
        INTO ultimo_numero
        FROM pacientes
        WHERE numero_historia ~ '^HC[0-9]+$';

        nuevo_numero := 'HC' || LPAD(ultimo_numero::TEXT, 6, '0');
        NEW.numero_historia := nuevo_numero;
    END IF;
    RETURN NEW;
END;
$$;

-- Generar número de consulta (YYYYMMDD001, YYYYMMDD002, ...)
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

        SELECT COALESCE(
            MAX(CAST(SUBSTRING(numero_consulta FROM 10) AS INTEGER)), 0
        ) + 1
        INTO ultimo_numero
        FROM consultas
        WHERE numero_consulta ~ ('^' || TO_CHAR(fecha_actual, 'YYYYMMDD') || '[0-9]+$');

        nuevo_numero := TO_CHAR(fecha_actual, 'YYYYMMDD') || LPAD(ultimo_numero::TEXT, 3, '0');
        NEW.numero_consulta := nuevo_numero;
    END IF;
    RETURN NEW;
END;
$$;

-- Generar número de recibo (RECYYYYMM0001, RECYYYYMM0002, ...)
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

        SELECT COALESCE(
            MAX(CAST(SUBSTRING(numero_recibo FROM 8) AS INTEGER)), 0
        ) + 1
        INTO ultimo_numero
        FROM pagos
        WHERE numero_recibo ~ ('^REC' || TO_CHAR(fecha_actual, 'YYYYMM') || '[0-9]+$');

        nuevo_numero := 'REC' || TO_CHAR(fecha_actual, 'YYYYMM') || LPAD(ultimo_numero::TEXT, 4, '0');
        NEW.numero_recibo := nuevo_numero;
    END IF;
    RETURN NEW;
END;
$$;

-- ----------------------------------------------------------------------------
-- 1.2 FUNCIONES DE CÁLCULO AUTOMÁTICO
-- ----------------------------------------------------------------------------

-- Calcular edad del paciente automáticamente
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

-- Actualizar fecha de modificación
CREATE OR REPLACE FUNCTION actualizar_fecha_modificacion()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    NEW.fecha_actualizacion = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$;

-- Calcular totales de intervención
CREATE OR REPLACE FUNCTION calcular_totales_intervencion()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
DECLARE
    total_bs_calc DECIMAL(10, 2) := 0;
    total_usd_calc DECIMAL(10, 2) := 0;
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

-- Actualizar costos de consulta
CREATE OR REPLACE FUNCTION actualizar_costos_consulta()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
DECLARE
    costo_bs_calc DECIMAL(10, 2) := 0;
    costo_usd_calc DECIMAL(10, 2) := 0;
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

-- Calcular saldos de pago
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

-- ----------------------------------------------------------------------------
-- 1.3 FUNCIONES DE SISTEMA DE COLAS
-- ----------------------------------------------------------------------------

-- Asignar orden de llegada automático
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

-- Cambiar odontólogo de una consulta (con justificación)
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
            'Cambiado de odontólogo: ' || COALESCE(motivo, 'Sin motivo especificado') ||
            ' - ' || CURRENT_TIMESTAMP
    WHERE id = consulta_id_param;

    RETURN FOUND;
END;
$$;

-- Obtener próximo paciente en cola
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
        TRIM(CONCAT(
            p.primer_nombre, ' ',
            COALESCE(p.segundo_nombre, ''), ' ',
            p.primer_apellido, ' ',
            COALESCE(p.segundo_apellido, '')
        )),
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

-- ----------------------------------------------------------------------------
-- 1.4 FUNCIONES DE ODONTOGRAMA V2.0
-- ----------------------------------------------------------------------------

-- Crear odontograma inicial automáticamente (160 condiciones "sano")
CREATE OR REPLACE FUNCTION crear_odontograma_inicial()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
DECLARE
    diente INTEGER;
    superficie TEXT;
    total_creadas INTEGER := 0;
BEGIN
    RAISE NOTICE 'Creando odontograma inicial para paciente %', NEW.numero_historia;

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
        FOR superficie IN
            SELECT unnest(ARRAY['oclusal', 'mesial', 'distal', 'vestibular', 'lingual'])
        LOOP
            INSERT INTO condiciones_diente (
                paciente_id, diente_numero, superficie,
                tipo_condicion, severidad, descripcion,
                color_hex, activo
            ) VALUES (
                NEW.id, diente, superficie,
                'sano', 'leve', 'Condición inicial',
                '#90EE90', TRUE
            );
            total_creadas := total_creadas + 1;
        END LOOP;
    END LOOP;

    RAISE NOTICE 'Odontograma inicial creado: % condiciones', total_creadas;
    RETURN NEW;
END;
$$;


-- ============================================================================
-- SECCIÓN 2: TABLAS PRINCIPALES
-- ============================================================================

-- ----------------------------------------------------------------------------
-- 2.1 AUTENTICACIÓN Y ROLES
-- ----------------------------------------------------------------------------

CREATE TABLE roles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nombre VARCHAR(50) UNIQUE NOT NULL,
    descripcion TEXT,
    permisos JSONB DEFAULT '{}'::JSONB,
    fecha_creacion TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL,
    activo BOOLEAN DEFAULT TRUE NOT NULL
);

CREATE TABLE usuarios (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    auth_user_id UUID UNIQUE,
    email VARCHAR(100) UNIQUE NOT NULL,
    nombre_completo VARCHAR(200) NOT NULL,
    rol_id UUID REFERENCES roles(id),
    activo BOOLEAN DEFAULT TRUE NOT NULL,
    ultimo_acceso TIMESTAMPTZ,
    fecha_creacion TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL,
    fecha_actualizacion TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- ----------------------------------------------------------------------------
-- 2.2 PERSONAL MÉDICO
-- ----------------------------------------------------------------------------

CREATE TABLE personal (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    usuario_id UUID UNIQUE REFERENCES usuarios(id),
    tipo_personal VARCHAR(50) NOT NULL,
    numero_documento VARCHAR(20) UNIQUE NOT NULL,
    primer_nombre VARCHAR(100) NOT NULL,
    segundo_nombre VARCHAR(100),
    primer_apellido VARCHAR(100) NOT NULL,
    segundo_apellido VARCHAR(100),
    especialidad VARCHAR(100),
    registro_profesional VARCHAR(50),
    fecha_ingreso DATE NOT NULL,
    fecha_egreso DATE,
    salario_base DECIMAL(10, 2),
    porcentaje_comision DECIMAL(5, 2) DEFAULT 0,
    telefono VARCHAR(20),
    email_personal VARCHAR(100),
    direccion TEXT,
    contacto_emergencia VARCHAR(200),
    telefono_emergencia VARCHAR(20),
    estado_laboral VARCHAR(20) DEFAULT 'activo',
    observaciones TEXT,
    fecha_creacion TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL,
    fecha_actualizacion TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL,

    CONSTRAINT personal_tipo_check CHECK (
        tipo_personal IN ('odontologo', 'asistente', 'administrativo', 'gerente')
    ),
    CONSTRAINT personal_estado_check CHECK (
        estado_laboral IN ('activo', 'inactivo', 'vacaciones', 'suspendido')
    )
);

-- ----------------------------------------------------------------------------
-- 2.3 PACIENTES
-- ----------------------------------------------------------------------------

CREATE TABLE pacientes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    numero_historia VARCHAR(20) UNIQUE NOT NULL,
    tipo_documento VARCHAR(10) DEFAULT 'cedula' NOT NULL,
    numero_documento VARCHAR(20) UNIQUE NOT NULL,
    primer_nombre VARCHAR(100) NOT NULL,
    segundo_nombre VARCHAR(100),
    primer_apellido VARCHAR(100) NOT NULL,
    segundo_apellido VARCHAR(100),
    fecha_nacimiento DATE NOT NULL,
    edad INTEGER,
    genero VARCHAR(10) NOT NULL,
    grupo_sanguineo VARCHAR(5),
    telefono_principal VARCHAR(20) NOT NULL,
    telefono_secundario VARCHAR(20),
    email VARCHAR(100),
    direccion TEXT NOT NULL,
    ciudad VARCHAR(100) DEFAULT 'Cumaná',
    estado VARCHAR(100) DEFAULT 'Sucre',
    pais VARCHAR(100) DEFAULT 'Venezuela',
    ocupacion VARCHAR(100),
    estado_civil VARCHAR(20),
    contacto_emergencia VARCHAR(200) NOT NULL,
    telefono_emergencia VARCHAR(20) NOT NULL,
    relacion_emergencia VARCHAR(50),
    alergias TEXT,
    enfermedades_cronicas TEXT,
    medicamentos_actuales TEXT,
    observaciones_medicas TEXT,
    activo BOOLEAN DEFAULT TRUE NOT NULL,
    registrado_por UUID REFERENCES usuarios(id),
    fecha_registro TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL,
    fecha_actualizacion TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL,

    CONSTRAINT pacientes_tipo_documento_check CHECK (
        tipo_documento IN ('cedula', 'pasaporte', 'rif')
    ),
    CONSTRAINT pacientes_genero_check CHECK (
        genero IN ('masculino', 'femenino', 'otro')
    ),
    CONSTRAINT pacientes_estado_civil_check CHECK (
        estado_civil IN ('soltero', 'casado', 'divorciado', 'viudo', 'union_estable')
    )
);

-- ----------------------------------------------------------------------------
-- 2.4 SERVICIOS ODONTOLÓGICOS
-- ----------------------------------------------------------------------------

CREATE TABLE servicios (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    codigo VARCHAR(20) UNIQUE NOT NULL,
    nombre VARCHAR(200) NOT NULL,
    descripcion TEXT,
    categoria VARCHAR(100) NOT NULL,
    precio_base_bs DECIMAL(10, 2) DEFAULT 0,
    precio_base_usd DECIMAL(10, 2) DEFAULT 0,
    precio_minimo_bs DECIMAL(10, 2),
    precio_minimo_usd DECIMAL(10, 2),
    precio_maximo_bs DECIMAL(10, 2),
    precio_maximo_usd DECIMAL(10, 2),
    duracion_estimada INTEGER,
    requiere_autorizacion BOOLEAN DEFAULT FALSE,
    activo BOOLEAN DEFAULT TRUE NOT NULL,
    instrucciones_preparacion TEXT,
    instrucciones_postcuidado TEXT,
    creado_por UUID REFERENCES usuarios(id),
    fecha_creacion TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL,
    fecha_actualizacion TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- ----------------------------------------------------------------------------
-- 2.5 CONSULTAS Y SISTEMA DE COLAS
-- ----------------------------------------------------------------------------

CREATE TABLE consultas (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    numero_consulta VARCHAR(20) UNIQUE NOT NULL,
    paciente_id UUID NOT NULL REFERENCES pacientes(id) ON DELETE RESTRICT,
    primer_odontologo_id UUID REFERENCES usuarios(id),
    odontologo_preferido_id UUID REFERENCES usuarios(id),
    tipo_consulta VARCHAR(50) DEFAULT 'primera_vez' NOT NULL,
    estado VARCHAR(20) DEFAULT 'en_espera' NOT NULL,
    fecha_llegada TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL,
    fecha_atencion TIMESTAMPTZ,
    fecha_finalizacion TIMESTAMPTZ,
    orden_llegada_general INTEGER NOT NULL,
    orden_cola_odontologo INTEGER NOT NULL,
    motivo_consulta TEXT NOT NULL,
    diagnostico_inicial TEXT,
    plan_tratamiento TEXT,
    costo_total_bs DECIMAL(10, 2) DEFAULT 0,
    costo_total_usd DECIMAL(10, 2) DEFAULT 0,
    observaciones TEXT,
    requiere_seguimiento BOOLEAN DEFAULT FALSE,
    fecha_proximo_control DATE,
    creada_por UUID REFERENCES usuarios(id),
    fecha_creacion TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL,
    fecha_actualizacion TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL,

    CONSTRAINT consultas_tipo_check CHECK (
        tipo_consulta IN ('primera_vez', 'control', 'emergencia', 'seguimiento')
    ),
    CONSTRAINT consultas_estado_check CHECK (
        estado IN ('en_espera', 'en_atencion', 'completada', 'cancelada', 'derivada')
    )
);

-- ----------------------------------------------------------------------------
-- 2.6 INTERVENCIONES MÉDICAS
-- ----------------------------------------------------------------------------

CREATE TABLE intervenciones (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    consulta_id UUID NOT NULL REFERENCES consultas(id) ON DELETE CASCADE,
    odontologo_id UUID NOT NULL REFERENCES usuarios(id),
    asistente_id UUID REFERENCES usuarios(id),
    fecha_inicio TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL,
    fecha_fin TIMESTAMPTZ,
    duracion_minutos INTEGER,
    diagnostico TEXT,
    tratamiento_realizado TEXT NOT NULL,
    materiales_utilizados TEXT,
    tecnicas_aplicadas TEXT,
    dientes_tratados INTEGER[],
    complicaciones TEXT,
    indicaciones_paciente TEXT,
    receta_medica TEXT,
    total_bs DECIMAL(10, 2) DEFAULT 0,
    total_usd DECIMAL(10, 2) DEFAULT 0,
    descuento_bs DECIMAL(10, 2) DEFAULT 0,
    descuento_usd DECIMAL(10, 2) DEFAULT 0,
    motivo_descuento TEXT,
    observaciones TEXT,
    requiere_cita_control BOOLEAN DEFAULT FALSE,
    fecha_creacion TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE TABLE intervenciones_servicios (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    intervencion_id UUID NOT NULL REFERENCES intervenciones(id) ON DELETE CASCADE,
    servicio_id UUID NOT NULL REFERENCES servicios(id),
    cantidad INTEGER DEFAULT 1 NOT NULL,
    precio_unitario_bs DECIMAL(10, 2) DEFAULT 0,
    precio_unitario_usd DECIMAL(10, 2) DEFAULT 0,
    precio_total_bs DECIMAL(10, 2) DEFAULT 0,
    precio_total_usd DECIMAL(10, 2) DEFAULT 0,
    diente_numero INTEGER,
    superficie VARCHAR(20),
    observaciones TEXT,
    fecha_creacion TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- ----------------------------------------------------------------------------
-- 2.7 ODONTOGRAMA V2.0 SIMPLIFICADO
-- ----------------------------------------------------------------------------

CREATE TABLE condiciones_diente (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    -- Relación directa (sin tabla intermedia)
    paciente_id UUID NOT NULL REFERENCES pacientes(id) ON DELETE CASCADE,
    diente_numero INTEGER NOT NULL,
    superficie VARCHAR(20) NOT NULL,

    -- Condición actual
    tipo_condicion VARCHAR(50) NOT NULL,
    severidad VARCHAR(20) DEFAULT 'leve',

    -- Detalles
    descripcion TEXT,
    observaciones TEXT,
    material_utilizado VARCHAR(100),
    tecnica_utilizada VARCHAR(100),
    color_material VARCHAR(50),
    fecha_tratamiento DATE,

    -- Trazabilidad
    intervencion_id UUID REFERENCES intervenciones(id) ON DELETE SET NULL,
    registrado_por UUID REFERENCES usuarios(id),
    fecha_registro TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL,

    -- Historial simple (en vez de sistema de versiones)
    activo BOOLEAN DEFAULT TRUE NOT NULL,

    -- Renderizado
    color_hex VARCHAR(7) DEFAULT '#90EE90',

    -- Constraint: Solo UNA condición activa por diente-superficie
    CONSTRAINT unique_active_condition UNIQUE (paciente_id, diente_numero, superficie, activo)
        WHERE (activo = TRUE),

    CONSTRAINT condiciones_diente_numero_check CHECK (
        diente_numero IN (
            18,17,16,15,14,13,12,11,  -- Cuadrante 1
            21,22,23,24,25,26,27,28,  -- Cuadrante 2
            31,32,33,34,35,36,37,38,  -- Cuadrante 3
            41,42,43,44,45,46,47,48   -- Cuadrante 4
        )
    ),
    CONSTRAINT condiciones_superficie_check CHECK (
        superficie IN ('oclusal', 'mesial', 'distal', 'vestibular', 'lingual')
    ),
    CONSTRAINT condiciones_tipo_check CHECK (
        tipo_condicion IN (
            'sano', 'caries', 'obturacion', 'corona', 'puente',
            'implante', 'extraccion', 'fractura', 'endodoncia',
            'ausente', 'protesis', 'sellante'
        )
    ),
    CONSTRAINT condiciones_severidad_check CHECK (
        severidad IN ('leve', 'moderada', 'severa')
    )
);

-- Índices optimizados
CREATE INDEX idx_condiciones_paciente_activo ON condiciones_diente(paciente_id, activo);
CREATE INDEX idx_condiciones_intervencion ON condiciones_diente(intervencion_id);
CREATE INDEX idx_condiciones_diente_numero ON condiciones_diente(diente_numero);
CREATE INDEX idx_condiciones_fecha ON condiciones_diente(fecha_registro DESC);

-- ----------------------------------------------------------------------------
-- 2.8 PAGOS Y FACTURACIÓN
-- ----------------------------------------------------------------------------

CREATE TABLE pagos (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    numero_recibo VARCHAR(20) UNIQUE NOT NULL,
    consulta_id UUID NOT NULL REFERENCES consultas(id),
    paciente_id UUID NOT NULL REFERENCES pacientes(id),
    fecha_pago TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL,

    -- Montos totales
    monto_total_bs DECIMAL(10, 2) DEFAULT 0 NOT NULL,
    monto_total_usd DECIMAL(10, 2) DEFAULT 0 NOT NULL,

    -- Montos pagados
    monto_pagado_bs DECIMAL(10, 2) DEFAULT 0 NOT NULL,
    monto_pagado_usd DECIMAL(10, 2) DEFAULT 0 NOT NULL,

    -- Saldos
    saldo_pendiente_bs DECIMAL(10, 2) DEFAULT 0 NOT NULL,
    saldo_pendiente_usd DECIMAL(10, 2) DEFAULT 0 NOT NULL,

    -- Métodos de pago
    metodo_pago VARCHAR(50) NOT NULL,
    referencia_pago VARCHAR(100),
    banco VARCHAR(100),

    -- Tasa de cambio
    tasa_cambio_bs_usd DECIMAL(10, 4),

    -- Descuentos e impuestos
    descuento_bs DECIMAL(10, 2) DEFAULT 0,
    descuento_usd DECIMAL(10, 2) DEFAULT 0,
    motivo_descuento TEXT,
    impuesto_bs DECIMAL(10, 2) DEFAULT 0,
    impuesto_usd DECIMAL(10, 2) DEFAULT 0,

    -- Estado y control
    estado_pago VARCHAR(20) DEFAULT 'pendiente' NOT NULL,
    observaciones TEXT,
    procesado_por UUID REFERENCES usuarios(id),
    autorizado_por UUID REFERENCES usuarios(id),
    fecha_creacion TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL,

    CONSTRAINT pagos_metodo_check CHECK (
        metodo_pago IN (
            'efectivo_bs', 'efectivo_usd', 'transferencia_bs',
            'transferencia_usd', 'punto_venta', 'pago_movil',
            'zelle', 'mixto'
        )
    ),
    CONSTRAINT pagos_estado_check CHECK (
        estado_pago IN ('pendiente', 'parcial', 'completado', 'cancelado', 'reembolsado')
    )
);

-- ----------------------------------------------------------------------------
-- 2.9 HISTORIAL MÉDICO
-- ----------------------------------------------------------------------------

CREATE TABLE historial_medico (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    paciente_id UUID NOT NULL REFERENCES pacientes(id) ON DELETE CASCADE,
    consulta_id UUID REFERENCES consultas(id),
    intervencion_id UUID REFERENCES intervenciones(id),
    odontologo_id UUID REFERENCES usuarios(id),
    fecha_registro TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL,

    tipo_registro VARCHAR(50) NOT NULL,
    titulo VARCHAR(200) NOT NULL,
    descripcion TEXT NOT NULL,
    hallazgos TEXT,
    recomendaciones TEXT,

    dientes_afectados INTEGER[],
    imagenes_urls TEXT[],
    documentos_adjuntos JSONB,

    es_critico BOOLEAN DEFAULT FALSE,
    requiere_atencion BOOLEAN DEFAULT FALSE,

    CONSTRAINT historial_tipo_check CHECK (
        tipo_registro IN (
            'diagnostico', 'tratamiento', 'control',
            'observacion', 'alerta', 'laboratorio'
        )
    )
);

-- ----------------------------------------------------------------------------
-- 2.10 IMÁGENES CLÍNICAS
-- ----------------------------------------------------------------------------

CREATE TABLE imagenes_clinicas (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    paciente_id UUID NOT NULL REFERENCES pacientes(id) ON DELETE CASCADE,
    consulta_id UUID REFERENCES consultas(id),
    intervencion_id UUID REFERENCES intervenciones(id),

    tipo_imagen VARCHAR(50) NOT NULL,
    url_imagen TEXT NOT NULL,
    url_thumbnail TEXT,
    nombre_archivo VARCHAR(255) NOT NULL,
    tamano_bytes BIGINT,
    formato VARCHAR(10),

    diente_numero INTEGER,
    descripcion TEXT,
    observaciones TEXT,

    capturada_por UUID REFERENCES usuarios(id),
    fecha_captura TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL,

    CONSTRAINT imagenes_tipo_check CHECK (
        tipo_imagen IN (
            'radiografia', 'foto_intraoral', 'foto_extraoral',
            'panoramica', 'periapical', 'oclusal', 'otro'
        )
    )
);

-- ----------------------------------------------------------------------------
-- 2.11 COLA DE ATENCIÓN
-- ----------------------------------------------------------------------------

CREATE TABLE cola_atencion (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    consulta_id UUID NOT NULL REFERENCES consultas(id),
    odontologo_id UUID NOT NULL REFERENCES usuarios(id),
    posicion_cola INTEGER NOT NULL,
    fecha_ingreso_cola TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    fecha_salida_cola TIMESTAMPTZ,
    estado_cola VARCHAR(20) DEFAULT 'esperando',
    observaciones TEXT,

    CONSTRAINT cola_estado_check CHECK (
        estado_cola IN ('esperando', 'siendo_atendido', 'atendido', 'derivado', 'cancelado')
    ),
    CONSTRAINT uq_consulta_odontologo_activo UNIQUE (consulta_id, odontologo_id)
);

-- ----------------------------------------------------------------------------
-- 2.12 CONFIGURACIÓN DEL SISTEMA
-- ----------------------------------------------------------------------------

CREATE TABLE configuracion_sistema (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    clave VARCHAR(100) UNIQUE NOT NULL,
    valor TEXT NOT NULL,
    tipo_dato VARCHAR(20) NOT NULL,
    descripcion TEXT,
    categoria VARCHAR(50),
    es_editable BOOLEAN DEFAULT TRUE,
    modificado_por UUID REFERENCES usuarios(id),
    fecha_modificacion TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT config_tipo_check CHECK (
        tipo_dato IN ('string', 'number', 'boolean', 'json', 'date')
    )
);

-- ----------------------------------------------------------------------------
-- 2.13 NOTIFICACIONES
-- ----------------------------------------------------------------------------

CREATE TABLE notificaciones_sistema (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    usuario_id UUID REFERENCES usuarios(id),
    tipo_notificacion VARCHAR(50) NOT NULL,
    titulo VARCHAR(200) NOT NULL,
    mensaje TEXT NOT NULL,
    prioridad VARCHAR(20) DEFAULT 'normal',
    leida BOOLEAN DEFAULT FALSE,
    fecha_lectura TIMESTAMPTZ,
    url_accion VARCHAR(255),
    consulta_id UUID REFERENCES consultas(id),
    intervencion_id UUID REFERENCES intervenciones(id),
    metadata JSONB,
    fecha_creacion TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL,
    fecha_expiracion TIMESTAMPTZ,

    CONSTRAINT notif_tipo_check CHECK (
        tipo_notificacion IN (
            'nueva_consulta', 'proximo_turno', 'consulta_completada',
            'pago_recibido', 'recordatorio', 'alerta_medica', 'sistema'
        )
    ),
    CONSTRAINT notif_prioridad_check CHECK (
        prioridad IN ('baja', 'normal', 'alta', 'urgente')
    )
);

-- ----------------------------------------------------------------------------
-- 2.14 AUDITORÍA
-- ----------------------------------------------------------------------------

CREATE TABLE auditoria (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tabla_afectada VARCHAR(50) NOT NULL,
    registro_id UUID NOT NULL,
    accion VARCHAR(20) NOT NULL,
    usuario_id UUID REFERENCES usuarios(id),
    fecha_accion TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    ip_address INET,
    user_agent TEXT,
    datos_anteriores JSONB,
    datos_nuevos JSONB,
    campos_modificados TEXT[],
    motivo TEXT,
    modulo VARCHAR(50),
    accion_contexto VARCHAR(100),

    CONSTRAINT auditoria_accion_check CHECK (
        accion IN ('INSERT', 'UPDATE', 'DELETE')
    )
);


-- ============================================================================
-- SECCIÓN 3: VISTAS ÚTILES
-- ============================================================================

-- Vista de odontograma actual de cada paciente
CREATE OR REPLACE VIEW vista_odontograma_actual AS
SELECT
    c.paciente_id,
    p.numero_historia,
    CONCAT(p.primer_nombre, ' ', p.primer_apellido) as paciente_nombre,
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

-- Vista de cola de odontólogos en tiempo real
CREATE OR REPLACE VIEW vista_cola_odontologos AS
SELECT
    u.id as odontologo_id,
    u.nombre_completo as odontologo_nombre,
    COUNT(c.id) as pacientes_en_espera,
    MIN(c.orden_cola_odontologo) as proximo_turno,
    AVG(EXTRACT(EPOCH FROM (CURRENT_TIMESTAMP - c.fecha_llegada))/60)::INTEGER as tiempo_espera_promedio_min
FROM usuarios u
LEFT JOIN consultas c ON u.id = c.primer_odontologo_id
    AND c.estado = 'en_espera'
    AND DATE(c.fecha_llegada) = CURRENT_DATE
WHERE u.rol_id IN (SELECT id FROM roles WHERE nombre = 'odontologo')
    AND u.activo = TRUE
GROUP BY u.id, u.nombre_completo
ORDER BY pacientes_en_espera DESC;

-- Vista de personal completo con información del usuario
CREATE OR REPLACE VIEW vista_personal_completo AS
SELECT
    p.id,
    p.tipo_personal,
    p.numero_documento,
    CONCAT(p.primer_nombre, ' ', p.primer_apellido) as nombre_completo,
    p.especialidad,
    p.registro_profesional,
    p.estado_laboral,
    p.salario_base,
    p.porcentaje_comision,
    u.email,
    u.activo as usuario_activo,
    r.nombre as rol_nombre
FROM personal p
LEFT JOIN usuarios u ON p.usuario_id = u.id
LEFT JOIN roles r ON u.rol_id = r.id
ORDER BY p.tipo_personal, p.primer_apellido;

-- Vista de consultas del día
CREATE OR REPLACE VIEW vista_consultas_dia AS
SELECT
    c.id,
    c.numero_consulta,
    c.estado,
    c.orden_llegada_general,
    c.orden_cola_odontologo,
    p.numero_historia,
    CONCAT(p.primer_nombre, ' ', p.primer_apellido) as paciente_nombre,
    u.nombre_completo as odontologo_nombre,
    c.fecha_llegada,
    c.motivo_consulta,
    EXTRACT(EPOCH FROM (CURRENT_TIMESTAMP - c.fecha_llegada))/60 as minutos_esperando
FROM consultas c
JOIN pacientes p ON c.paciente_id = p.id
LEFT JOIN usuarios u ON c.primer_odontologo_id = u.id
WHERE DATE(c.fecha_llegada) = CURRENT_DATE
ORDER BY c.orden_llegada_general;


-- ============================================================================
-- SECCIÓN 4: TRIGGERS
-- ============================================================================

-- Triggers de auto-numeración
CREATE TRIGGER trigger_generar_numero_historia
    BEFORE INSERT ON pacientes
    FOR EACH ROW EXECUTE FUNCTION generar_numero_historia();

CREATE TRIGGER trigger_generar_numero_consulta
    BEFORE INSERT ON consultas
    FOR EACH ROW EXECUTE FUNCTION generar_numero_consulta();

CREATE TRIGGER trigger_generar_numero_recibo
    BEFORE INSERT ON pagos
    FOR EACH ROW EXECUTE FUNCTION generar_numero_recibo();

-- Triggers de cálculo automático
CREATE TRIGGER trigger_calcular_edad_paciente
    BEFORE INSERT OR UPDATE ON pacientes
    FOR EACH ROW EXECUTE FUNCTION calcular_edad_paciente();

CREATE TRIGGER trigger_calcular_saldos_pago
    BEFORE INSERT OR UPDATE ON pagos
    FOR EACH ROW EXECUTE FUNCTION calcular_saldos_pago();

CREATE TRIGGER trigger_calcular_totales_intervencion
    AFTER INSERT OR UPDATE OR DELETE ON intervenciones_servicios
    FOR EACH ROW EXECUTE FUNCTION calcular_totales_intervencion();

CREATE TRIGGER trigger_actualizar_costos_consulta
    AFTER INSERT OR UPDATE OR DELETE ON intervenciones
    FOR EACH ROW EXECUTE FUNCTION actualizar_costos_consulta();

-- Triggers de fecha de actualización
CREATE TRIGGER trigger_pacientes_fecha_actualizacion
    BEFORE UPDATE ON pacientes
    FOR EACH ROW EXECUTE FUNCTION actualizar_fecha_modificacion();

CREATE TRIGGER trigger_usuarios_fecha_actualizacion
    BEFORE UPDATE ON usuarios
    FOR EACH ROW EXECUTE FUNCTION actualizar_fecha_modificacion();

CREATE TRIGGER trigger_personal_fecha_actualizacion
    BEFORE UPDATE ON personal
    FOR EACH ROW EXECUTE FUNCTION actualizar_fecha_modificacion();

CREATE TRIGGER trigger_consultas_fecha_actualizacion
    BEFORE UPDATE ON consultas
    FOR EACH ROW EXECUTE FUNCTION actualizar_fecha_modificacion();

-- Trigger de sistema de colas
CREATE TRIGGER trigger_asignar_orden_llegada
    BEFORE INSERT ON consultas
    FOR EACH ROW EXECUTE FUNCTION asignar_orden_llegada();

-- Trigger de odontograma automático
CREATE TRIGGER trigger_crear_odontograma_inicial
    AFTER INSERT ON pacientes
    FOR EACH ROW EXECUTE FUNCTION crear_odontograma_inicial();


-- ============================================================================
-- SECCIÓN 5: ÍNDICES ADICIONALES
-- ============================================================================

-- Índices para pacientes
CREATE INDEX idx_pacientes_numero_documento ON pacientes(numero_documento);
CREATE INDEX idx_pacientes_nombre ON pacientes(primer_nombre, primer_apellido);
CREATE INDEX idx_pacientes_activo ON pacientes(activo);

-- Índices para consultas
CREATE INDEX idx_consultas_paciente ON consultas(paciente_id);
CREATE INDEX idx_consultas_odontologo ON consultas(primer_odontologo_id);
CREATE INDEX idx_consultas_fecha ON consultas(fecha_llegada DESC);
CREATE INDEX idx_consultas_estado ON consultas(estado);
CREATE INDEX idx_consultas_cola ON consultas(primer_odontologo_id, estado, orden_cola_odontologo);

-- Índices para intervenciones
CREATE INDEX idx_intervenciones_consulta ON intervenciones(consulta_id);
CREATE INDEX idx_intervenciones_odontologo ON intervenciones(odontologo_id);
CREATE INDEX idx_intervenciones_fecha ON intervenciones(fecha_inicio DESC);

-- Índices para pagos
CREATE INDEX idx_pagos_consulta ON pagos(consulta_id);
CREATE INDEX idx_pagos_paciente ON pagos(paciente_id);
CREATE INDEX idx_pagos_fecha ON pagos(fecha_pago DESC);
CREATE INDEX idx_pagos_estado ON pagos(estado_pago);

-- Índices para usuarios y personal
CREATE INDEX idx_usuarios_email ON usuarios(email);
CREATE INDEX idx_usuarios_rol ON usuarios(rol_id);
CREATE INDEX idx_personal_tipo ON personal(tipo_personal);
CREATE INDEX idx_personal_estado ON personal(estado_laboral);


-- ============================================================================
-- COMENTARIOS Y DOCUMENTACIÓN
-- ============================================================================

COMMENT ON TABLE pacientes IS 'Tabla principal de pacientes con historia clínica';
COMMENT ON TABLE consultas IS 'Sistema de consultas sin citas, por orden de llegada';
COMMENT ON TABLE condiciones_diente IS 'Odontograma V2.0 simplificado con historial por campo activo';
COMMENT ON TABLE intervenciones IS 'Intervenciones médicas realizadas por odontólogos';
COMMENT ON TABLE pagos IS 'Sistema de pagos mixtos BS/USD con distribución automática';

COMMENT ON FUNCTION crear_odontograma_inicial() IS 'Auto-crea 160 condiciones "sano" al crear paciente nuevo';
COMMENT ON FUNCTION asignar_orden_llegada() IS 'Asigna orden automático en cola general y por odontólogo';
COMMENT ON FUNCTION obtener_proximo_paciente(UUID) IS 'Obtiene el próximo paciente en la cola del odontólogo';

-- ============================================================================
-- FIN DEL ESQUEMA
-- ============================================================================
