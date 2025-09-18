-- ==========================================
-- 🦷 FUNCIÓN DE INICIALIZACIÓN DE ECOSISTEMA DE PACIENTE
-- ==========================================
-- Archivo: initialize_patient_ecosystem.sql
-- Propósito: Crear automáticamente odontograma + historial médico + auditoría
--           cuando se crea un nuevo paciente
-- Versión: 1.0
-- Fecha: 2025-01-17

-- ==========================================
-- 🔧 FUNCIÓN PRINCIPAL: initialize_patient_ecosystem
-- ==========================================

CREATE OR REPLACE FUNCTION initialize_patient_ecosystem(
    new_patient_id UUID,
    numero_historia_param VARCHAR,
    creator_id UUID
) RETURNS VOID AS $$
DECLARE
    nuevo_odontograma_id UUID;
    numero_fdi INTEGER;
    dientes_fdi INTEGER[] := ARRAY[
        -- Cuadrante 1: Superior derecho (11-18)
        11, 12, 13, 14, 15, 16, 17, 18,
        -- Cuadrante 2: Superior izquierdo (21-28)
        21, 22, 23, 24, 25, 26, 27, 28,
        -- Cuadrante 3: Inferior izquierdo (31-38)
        31, 32, 33, 34, 35, 36, 37, 38,
        -- Cuadrante 4: Inferior derecho (41-48)
        41, 42, 43, 44, 45, 46, 47, 48
    ];
BEGIN
    -- Log de inicio
    RAISE NOTICE '🦷 Iniciando ecosistema para paciente: %', numero_historia_param;

    -- ==========================================
    -- 📋 1. CREAR ODONTOGRAMA INICIAL
    -- ==========================================

    INSERT INTO odontogramas (
        numero_historia,
        version,
        id_version_anterior,
        id_intervencion_origen,
        es_version_actual,
        motivo_nueva_version,
        fecha_creacion,
        odontologo_id,
        tipo_odontograma,
        notas_generales,
        observaciones_clinicas,
        template_usado,
        dientes_estados
    ) VALUES (
        numero_historia_param,
        1, -- Primera versión
        NULL, -- No hay versión anterior
        NULL, -- No hay intervención origen
        TRUE, -- Es la versión actual
        'Odontograma inicial automático',
        CURRENT_TIMESTAMP,
        creator_id,
        'adulto',
        'Odontograma inicial creado automáticamente',
        'Todos los dientes inicializados como sanos',
        'universal',
        '{}'::JSONB -- Se poblará después
    ) RETURNING id INTO nuevo_odontograma_id;

    RAISE NOTICE '✅ Odontograma creado con ID: %', nuevo_odontograma_id;

    -- ==========================================
    -- 🦷 2. CREAR CONDICIONES INICIALES PARA 32 DIENTES FDI
    -- ==========================================

    -- Iterar sobre cada diente FDI y crear condición "sano"
    FOREACH numero_fdi IN ARRAY dientes_fdi
    LOOP
        INSERT INTO condiciones_diente_historial (
            odontograma_id,
            numero_fdi,
            codigo_condicion,
            nombre_condicion,
            superficie_afectada,
            categoria,
            es_urgente,
            color_hex,
            descripcion,
            observaciones,
            fecha_registro,
            intervencion_origen_id,
            estado
        ) VALUES (
            nuevo_odontograma_id,
            numero_fdi,
            'SAO',
            'sano',
            'completa',
            'normal',
            FALSE,
            '#16a34a',
            'Diente sano sin patologías',
            'Estado inicial automático',
            CURRENT_TIMESTAMP,
            NULL,
            'actual'
        );
    END LOOP;

    RAISE NOTICE '✅ % condiciones de dientes creadas', array_length(dientes_fdi, 1);

    -- ==========================================
    -- 📋 3. CREAR HISTORIAL MÉDICO INICIAL
    -- ==========================================

    INSERT INTO historial_medico (
        paciente_id,
        consulta_id,
        intervencion_id,
        odontologo_id,
        tipo_registro,
        sintomas_principales,
        examen_clinico,
        diagnostico_principal,
        diagnosticos_secundarios,
        plan_tratamiento,
        pronostico,
        medicamentos_recetados,
        recomendaciones,
        contraindicaciones,
        presion_arterial,
        frecuencia_cardiaca,
        temperatura,
        imagenes_url,
        documentos_url,
        proxima_consulta,
        observaciones,
        confidencial,
        fecha_registro,
        registrado_por
    ) VALUES (
        new_patient_id,
        NULL, -- No hay consulta aún
        NULL, -- No hay intervención aún
        creator_id,
        'inicial',
        'Paciente nuevo registrado en el sistema',
        'Pendiente de evaluación inicial',
        'Sin diagnóstico - Paciente nuevo',
        '{}', -- Array vacío
        'Evaluación inicial pendiente',
        'A determinar en primera consulta',
        '[]'::JSONB, -- Array vacío de medicamentos
        'Agendar consulta de evaluación inicial',
        'Ninguna conocida',
        NULL, -- Presión arterial pendiente
        NULL, -- Frecuencia cardíaca pendiente
        NULL, -- Temperatura pendiente
        '{}', -- Array vacío de imágenes
        '{}', -- Array vacío de documentos
        NULL, -- Próxima consulta a programar
        'Historial médico inicial creado automáticamente al registrar paciente',
        FALSE, -- No confidencial
        CURRENT_TIMESTAMP,
        creator_id
    );

    RAISE NOTICE '✅ Historial médico inicial creado';

    -- ==========================================
    -- 📝 4. REGISTRAR AUDITORÍA DE INICIALIZACIÓN
    -- ==========================================

    INSERT INTO auditoria (
        tabla_afectada,
        registro_id,
        accion,
        usuario_id,
        datos_anteriores,
        datos_nuevos,
        modulo,
        ip_address,
        descripcion,
        fecha_accion
    ) VALUES (
        'pacientes',
        new_patient_id,
        'ECOSYSTEM_INIT',
        creator_id,
        NULL, -- No hay datos anteriores
        jsonb_build_object(
            'numero_historia', numero_historia_param,
            'accion', 'Inicialización completa de ecosistema',
            'componentes', ARRAY['paciente', 'odontograma', 'historial_medico'],
            'odontograma_id', nuevo_odontograma_id,
            'dientes_inicializados', array_length(dientes_fdi, 1)
        ),
        'pacientes',
        '127.0.0.1', -- Placeholder IP
        'Ecosistema completo inicializado automáticamente para paciente ' || numero_historia_param,
        CURRENT_TIMESTAMP
    );

    RAISE NOTICE '✅ Auditoría de inicialización registrada';

    -- Log final
    RAISE NOTICE '🎉 Ecosistema completo para paciente % inicializado exitosamente', numero_historia_param;

EXCEPTION
    WHEN OTHERS THEN
        -- Manejo de errores
        RAISE EXCEPTION '❌ Error inicializando ecosistema para %: % (SQLSTATE: %)',
            numero_historia_param, SQLERRM, SQLSTATE;
END;
$$ LANGUAGE plpgsql;

-- ==========================================
-- 🔧 COMENTARIOS DE LA FUNCIÓN
-- ==========================================

COMMENT ON FUNCTION initialize_patient_ecosystem(UUID, VARCHAR, UUID) IS
'🦷 Inicializa automáticamente el ecosistema completo de un paciente nuevo:
- Crea odontograma inicial con 32 dientes como "sanos"
- Crea historial médico inicial
- Registra auditoría de inicialización
Usado por: PacientesService._inicializar_ecosistema_paciente_completo()';

-- ==========================================
-- 🔥 TRIGGER AUTOMÁTICO (OPCIONAL)
-- ==========================================
-- Descomentar las siguientes líneas si quieres que se ejecute automáticamente
-- cada vez que se inserta un nuevo paciente en la tabla pacientes

/*
CREATE OR REPLACE FUNCTION trigger_initialize_patient_ecosystem()
RETURNS TRIGGER AS $$
BEGIN
    -- Solo ejecutar para pacientes activos
    IF NEW.activo = TRUE THEN
        -- Ejecutar función de inicialización (async en background)
        PERFORM initialize_patient_ecosystem(
            NEW.id,
            NEW.numero_historia,
            NEW.registrado_por::UUID
        );
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Crear trigger que se ejecute DESPUÉS del INSERT
DROP TRIGGER IF EXISTS after_insert_patient_ecosystem ON pacientes;
CREATE TRIGGER after_insert_patient_ecosystem
    AFTER INSERT ON pacientes
    FOR EACH ROW
    EXECUTE FUNCTION trigger_initialize_patient_ecosystem();

COMMENT ON TRIGGER after_insert_patient_ecosystem ON pacientes IS
'🔥 Trigger automático que inicializa el ecosistema completo cada vez que se crea un paciente nuevo';
*/

-- ==========================================
-- 📋 INSTRUCCIONES DE USO
-- ==========================================

/*
PARA USAR MANUALMENTE:
SELECT initialize_patient_ecosystem(
    'paciente-uuid-aqui'::UUID,
    'HC000001',
    'creator-user-uuid-aqui'::UUID
);

PARA ACTIVAR TRIGGER AUTOMÁTICO:
Descomenta las líneas del trigger arriba (líneas 140-165)

PARA VERIFICAR EJECUCIÓN:
- Revisa tabla odontogramas: SELECT * FROM odontogramas WHERE numero_historia = 'HC000001';
- Revisa condiciones: SELECT COUNT(*) FROM condiciones_diente_historial WHERE odontograma_id = 'odontograma-id';
- Revisa historial: SELECT * FROM historial_medico WHERE paciente_id = 'paciente-id';
- Revisa auditoría: SELECT * FROM auditoria WHERE accion = 'ECOSYSTEM_INIT';
*/

-- ==========================================
-- ✅ FINALIZADO
-- ==========================================