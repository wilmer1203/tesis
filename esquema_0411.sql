-- WARNING: This schema is for context only and is not meant to be run.
-- Table order and constraints may not be valid for execution.
CREATE TABLE public.consulta (
    id uuid NOT NULL DEFAULT uuid_generate_v4(),
    numero_consulta character varying NOT NULL UNIQUE,
    paciente_id uuid NOT NULL,
    primer_odontologo_id uuid NOT NULL,
    fecha_llegada timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    orden_cola_odontologo integer,
    estado character varying DEFAULT 'en_espera' :: character varying CHECK (
        estado :: text = ANY (
            ARRAY ['en_espera'::character varying, 'en_atencion'::character varying, 'entre_odontologos'::character varying, 'completada'::character varying, 'cancelada'::character varying] :: text []
        )
    ),
    tipo_consulta character varying DEFAULT 'general' :: character varying CHECK (
        tipo_consulta :: text = ANY (
            ARRAY ['general'::character varying, 'control'::character varying, 'urgencia'::character varying, 'emergencia'::character varying] :: text []
        )
    ),
    motivo_consulta text,
    observaciones text,
    fecha_creacion timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT consulta_pkey PRIMARY KEY (id),
    CONSTRAINT consultas_paciente_id_fkey FOREIGN KEY (paciente_id) REFERENCES public.paciente(id),
    CONSTRAINT consultas_primer_odontologo_id_fkey FOREIGN KEY (primer_odontologo_id) REFERENCES public.personal(id)
);
CREATE TABLE public.diente (
    id uuid NOT NULL DEFAULT gen_random_uuid(),
    paciente_id uuid NOT NULL,
    diente_numero integer NOT NULL,
    superficie character varying NOT NULL CHECK (
        superficie :: text = ANY (
            ARRAY ['mesial'::character varying, 'distal'::character varying, 'oclusal'::character varying, 'lingual'::character varying, 'vestibular'::character varying, 'completo'::character varying] :: text []
        )
    ),
    tipo_condicion character varying NOT NULL CHECK (
        tipo_condicion :: text = ANY (
            ARRAY ['sano'::character varying, 'caries'::character varying, 'obturacion'::character varying, 'corona'::character varying, 'puente'::character varying, 'implante'::character varying, 'ausente'::character varying, 'extraccion_indicada'::character varying, 'endodoncia'::character varying, 'protesis'::character varying, 'fractura'::character varying, 'mancha'::character varying, 'desgaste'::character varying, 'sensibilidad'::character varying, 'movilidad'::character varying, 'impactado'::character varying, 'en_erupcion'::character varying, 'retenido'::character varying, 'supernumerario'::character varying, 'otro'::character varying] :: text []
        )
    ),
    intervencion_id uuid,
    fecha_registro timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    activo boolean NOT NULL DEFAULT true,
    color_hex character varying DEFAULT '#90EE90' :: character varying,
    CONSTRAINT diente_pkey PRIMARY KEY (id),
    CONSTRAINT condiciones_diente_paciente_id_fkey FOREIGN KEY (paciente_id) REFERENCES public.paciente(id),
    CONSTRAINT condiciones_diente_intervencion_id_fkey FOREIGN KEY (intervencion_id) REFERENCES public.intervencion(id)
);
CREATE TABLE public.historia_medica (
    id uuid NOT NULL DEFAULT uuid_generate_v4(),
    intervencion_id uuid NOT NULL,
    servicio_id uuid NOT NULL,
    precio_unitario_bs numeric NOT NULL,
    precio_unitario_usd numeric NOT NULL,
    precio_total_bs numeric NOT NULL,
    precio_total_usd numeric NOT NULL,
    fecha_registro timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    diente_numero integer,
    superficie character varying,
    CONSTRAINT historia_medica_pkey PRIMARY KEY (id),
    CONSTRAINT intervenciones_servicios_intervencion_id_fkey FOREIGN KEY (intervencion_id) REFERENCES public.intervencion(id),
    CONSTRAINT intervenciones_servicios_servicio_id_fkey FOREIGN KEY (servicio_id) REFERENCES public.servicio(id)
);
CREATE TABLE public.intervencion (
    id uuid NOT NULL DEFAULT uuid_generate_v4(),
    consulta_id uuid NOT NULL,
    odontologo_id uuid NOT NULL,
    hora_inicio timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    procedimiento_realizado text NOT NULL,
    total_bs numeric DEFAULT 0,
    total_usd numeric DEFAULT 0,
    estado character varying DEFAULT 'completada' :: character varying CHECK (
        estado :: text = ANY (
            ARRAY ['en_progreso'::character varying, 'completada'::character varying, 'suspendida'::character varying] :: text []
        )
    ),
    fecha_registro timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT intervencion_pkey PRIMARY KEY (id),
    CONSTRAINT intervenciones_consulta_id_fkey FOREIGN KEY (consulta_id) REFERENCES public.consulta(id),
    CONSTRAINT intervenciones_odontologo_id_fkey FOREIGN KEY (odontologo_id) REFERENCES public.personal(id)
);
CREATE TABLE public.paciente (
    id uuid NOT NULL DEFAULT uuid_generate_v4(),
    numero_historia character varying NOT NULL UNIQUE,
    primer_nombre character varying NOT NULL,
    segundo_nombre character varying,
    primer_apellido character varying NOT NULL,
    segundo_apellido character varying,
    tipo_documento character varying DEFAULT 'CI' :: character varying CHECK (
        tipo_documento :: text = ANY (
            ARRAY ['CI'::character varying, 'Pasaporte'::character varying] :: text []
        )
    ),
    numero_documento character varying NOT NULL UNIQUE CHECK (numero_documento :: text ~ '^\d{6,20}$' :: text),
    fecha_nacimiento date,
    genero character varying CHECK (
        genero :: text = ANY (
            ARRAY ['masculino'::character varying, 'femenino'::character varying, 'otro'::character varying] :: text []
        )
    ),
    celular_1 character varying CHECK (
        celular_1 IS NULL
        OR celular_1 :: text ~ '^[\+]?[\d\s\-\(\)]{7,20}$' :: text
    ),
    celular_2 character varying CHECK (
        celular_2 IS NULL
        OR celular_2 :: text ~ '^[\+]?[\d\s\-\(\)]{7,20}$' :: text
    ),
    email character varying CHECK (
        email IS NULL
        OR email :: text ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$' :: text
    ),
    direccion text,
    ciudad character varying,
    contacto_emergencia jsonb DEFAULT '{}' :: jsonb,
    alergias ARRAY,
    medicamentos_actuales ARRAY,
    condiciones_medicas ARRAY,
    fecha_registro timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    activo boolean DEFAULT true,
    CONSTRAINT paciente_pkey PRIMARY KEY (id)
);
CREATE TABLE public.pago (
    id uuid NOT NULL DEFAULT uuid_generate_v4(),
    numero_recibo character varying NOT NULL UNIQUE,
    consulta_id uuid,
    paciente_id uuid NOT NULL,
    fecha_pago timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    monto_total_bs numeric DEFAULT 0,
    monto_total_usd numeric DEFAULT 0,
    monto_pagado_bs numeric DEFAULT 0,
    monto_pagado_usd numeric DEFAULT 0,
    saldo_pendiente_bs numeric DEFAULT 0,
    saldo_pendiente_usd numeric DEFAULT 0,
    tasa_cambio_bs_usd numeric,
    metodos_pago jsonb DEFAULT '[]' :: jsonb,
    concepto text NOT NULL,
    descuento_usd numeric DEFAULT 0,
    motivo_descuento text,
    estado_pago character varying DEFAULT 'completado' :: character varying CHECK (
        estado_pago :: text = ANY (
            ARRAY ['pendiente'::character varying, 'completado'::character varying, 'parcial'::character varying, 'anulado'::character varying, 'reembolsado'::character varying] :: text []
        )
    ),
    procesado_por uuid NOT NULL,
    CONSTRAINT pago_pkey PRIMARY KEY (id),
    CONSTRAINT pagos_consulta_id_fkey FOREIGN KEY (consulta_id) REFERENCES public.consulta(id),
    CONSTRAINT pagos_paciente_id_fkey FOREIGN KEY (paciente_id) REFERENCES public.paciente(id),
    CONSTRAINT pagos_procesado_por_fkey FOREIGN KEY (procesado_por) REFERENCES public.usuario(id)
);
CREATE TABLE public.personal (
    id uuid NOT NULL DEFAULT uuid_generate_v4(),
    usuario_id uuid UNIQUE,
    primer_nombre character varying NOT NULL,
    segundo_nombre character varying,
    primer_apellido character varying NOT NULL,
    segundo_apellido character varying,
    tipo_documento character varying DEFAULT 'CI' :: character varying CHECK (
        tipo_documento :: text = ANY (
            ARRAY ['CI'::character varying, 'Pasaporte'::character varying] :: text []
        )
    ),
    numero_documento character varying NOT NULL UNIQUE CHECK (numero_documento :: text ~ '^\d{6,20}$' :: text),
    fecha_nacimiento date,
    direccion character varying,
    celular character varying NOT NULL CHECK (
        celular :: text ~ '^[\+]?[\d\s\-\(\)]{7,20}$' :: text
    ),
    tipo_personal character varying NOT NULL CHECK (
        tipo_personal :: text = ANY (
            ARRAY ['Odontólogo'::character varying, 'Asistente'::character varying, 'Administrador'::character varying, 'Gerente'::character varying] :: text []
        )
    ),
    especialidad character varying,
    numero_licencia character varying,
    fecha_contratacion date NOT NULL DEFAULT CURRENT_DATE,
    estado_laboral character varying DEFAULT 'activo' :: character varying CHECK (
        estado_laboral :: text = ANY (
            ARRAY ['activo'::character varying, 'inactivo'::character varying] :: text []
        )
    ),
    fecha_creacion timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT personal_pkey PRIMARY KEY (id),
    CONSTRAINT personal_usuario_id_fkey FOREIGN KEY (usuario_id) REFERENCES public.usuario(id)
);
CREATE TABLE public.rol (
    id uuid NOT NULL DEFAULT uuid_generate_v4(),
    nombre character varying NOT NULL UNIQUE CHECK (nombre :: text ~ '^[a-z_]+$' :: text),
    descripcion text,
    activo boolean DEFAULT true,
    fecha_creacion timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT rol_pkey PRIMARY KEY (id)
);
CREATE TABLE public.servicio (
    id uuid NOT NULL DEFAULT uuid_generate_v4(),
    codigo character varying NOT NULL UNIQUE CHECK (codigo :: text ~ '^[A-Z0-9]+$' :: text),
    nombre character varying NOT NULL,
    descripcion text,
    categoria character varying NOT NULL,
    precio_base_usd numeric NOT NULL CHECK (precio_base_usd > 0 :: numeric),
    activo boolean DEFAULT true,
    fecha_creacion timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    alcance_servicio character varying NOT NULL DEFAULT 'superficie_especifica' :: character varying CHECK (
        alcance_servicio :: text = ANY (
            ARRAY ['superficie_especifica'::character varying, 'diente_completo'::character varying, 'boca_completa'::character varying] :: text []
        )
    ),
    condicion_resultante character varying CHECK (
        condicion_resultante IS NULL
        OR (
            condicion_resultante :: text = ANY (
                ARRAY ['sano'::character varying, 'caries'::character varying, 'obturacion'::character varying, 'corona'::character varying, 'puente'::character varying, 'implante'::character varying, 'ausente'::character varying, 'extraccion_indicada'::character varying, 'endodoncia'::character varying, 'protesis'::character varying, 'fractura'::character varying, 'mancha'::character varying, 'desgaste'::character varying, 'sensibilidad'::character varying, 'movilidad'::character varying, 'impactado'::character varying, 'en_erupcion'::character varying, 'retenido'::character varying, 'supernumerario'::character varying, 'otro'::character varying] :: text []
            )
        )
    ),
    CONSTRAINT servicio_pkey PRIMARY KEY (id)
);
CREATE TABLE public.usuario (
    id uuid NOT NULL DEFAULT uuid_generate_v4(),
    email character varying NOT NULL UNIQUE CHECK (
        email :: text ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$' :: text
    ),
    rol_id uuid NOT NULL,
    activo boolean DEFAULT true,
    fecha_creacion timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    auth_user_id uuid UNIQUE,
    CONSTRAINT usuario_pkey PRIMARY KEY (id),
    CONSTRAINT usuarios_rol_id_fkey FOREIGN KEY (rol_id) REFERENCES public.rol(id)
);