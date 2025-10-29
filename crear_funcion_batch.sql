-- ==================================================================
-- FUNCIÓN: actualizar_condiciones_batch (V4.0 Transaccional)
-- ==================================================================
-- Actualiza múltiples condiciones dentales en una sola transacción
-- ==================================================================

CREATE OR REPLACE FUNCTION actualizar_condiciones_batch(
    actualizaciones jsonb
) RETURNS jsonb AS $$
DECLARE
    upd jsonb;
    exitosos int := 0;
    fallidos int := 0;
    ids_creados text[] := '{}';
    nueva_condicion_id uuid;
    total_actualizaciones int;
    error_msg text;
BEGIN
    -- Contar total de actualizaciones
    total_actualizaciones := jsonb_array_length(actualizaciones);

    RAISE NOTICE 'V4.0 Iniciando batch transaccional | Total: %', total_actualizaciones;

    BEGIN
        -- Iterar cada actualización
        FOR upd IN SELECT * FROM jsonb_array_elements(actualizaciones) LOOP
            BEGIN
                -- Validar campos requeridos
                IF (upd->>'paciente_id') IS NULL OR
                   (upd->>'diente_numero') IS NULL OR
                   (upd->>'superficie') IS NULL OR
                   (upd->>'tipo_condicion') IS NULL THEN
                    RAISE WARNING 'Actualización inválida (campos NULL): %', upd;
                    fallidos := fallidos + 1;
                    CONTINUE;
                END IF;

                -- PASO A: Desactivar condición anterior (historial)
                UPDATE condiciones_diente
                SET
                    activo = FALSE,
                    updated_at = CURRENT_TIMESTAMP
                WHERE paciente_id = (upd->>'paciente_id')::uuid
                  AND diente_numero = (upd->>'diente_numero')::int
                  AND superficie = upd->>'superficie'
                  AND activo = TRUE;

                -- PASO B: Insertar nueva condición (activa)
                INSERT INTO condiciones_diente (
                    paciente_id,
                    diente_numero,
                    superficie,
                    tipo_condicion,
                    material_utilizado,
                    descripcion,
                    intervencion_id,
                    registrado_por,
                    activo,
                    fecha_registro
                ) VALUES (
                    (upd->>'paciente_id')::uuid,
                    (upd->>'diente_numero')::int,
                    upd->>'superficie',
                    upd->>'tipo_condicion',
                    NULLIF(upd->>'material_utilizado', ''),
                    NULLIF(upd->>'descripcion', ''),
                    (upd->>'intervencion_id')::uuid,
                    NULLIF((upd->>'registrado_por'), '')::uuid,
                    TRUE,
                    CURRENT_TIMESTAMP
                ) RETURNING id INTO nueva_condicion_id;

                -- Registrar éxito
                ids_creados := array_append(ids_creados, nueva_condicion_id::text);
                exitosos := exitosos + 1;

            EXCEPTION WHEN OTHERS THEN
                -- Capturar error individual sin abortar batch completo
                GET STACKED DIAGNOSTICS error_msg = MESSAGE_TEXT;
                fallidos := fallidos + 1;

                RAISE WARNING 'Error en actualización individual | Diente: % | Superficie: % | Error: %',
                    upd->>'diente_numero',
                    upd->>'superficie',
                    error_msg;
            END;
        END LOOP;

        -- Validar resultado
        IF fallidos > 0 THEN
            RAISE WARNING 'Batch con fallos parciales | Exitosos: % | Fallidos: % | Total: %',
                exitosos, fallidos, total_actualizaciones;
        END IF;

        RAISE NOTICE 'Batch completado | Exitosos: % | Fallidos: %',
            exitosos, fallidos;

    EXCEPTION WHEN OTHERS THEN
        -- ROLLBACK automático en caso de error crítico
        GET STACKED DIAGNOSTICS error_msg = MESSAGE_TEXT;
        RAISE WARNING 'Error crítico en batch, ROLLBACK automático: %', error_msg;

        -- Retornar todo como fallido
        exitosos := 0;
        fallidos := total_actualizaciones;
        ids_creados := '{}';

        -- Re-lanzar para que llamador sepa que falló
        RAISE;
    END;

    -- Retornar resultado
    RETURN jsonb_build_object(
        'exitosos', exitosos,
        'fallidos', fallidos,
        'ids_creados', ids_creados,
        'total', total_actualizaciones,
        'tasa_exito_pct', ROUND((exitosos::decimal / NULLIF(total_actualizaciones, 0) * 100), 1)
    );
END;
$$ LANGUAGE plpgsql;

-- Comentario de documentación
COMMENT ON FUNCTION actualizar_condiciones_batch(jsonb) IS
'V4.0 - Actualización batch con transaccionalidad atómica
Actualiza múltiples condiciones dentales manteniendo historial automático.
Retorna: {exitosos, fallidos, ids_creados, total, tasa_exito_pct}';
