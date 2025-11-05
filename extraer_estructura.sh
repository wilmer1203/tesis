#!/bin/bash

OUTPUT="estructura_bd_completa.md"

echo "# ESTRUCTURA COMPLETA BASE DE DATOS - SISTEMA DENTAL" > $OUTPUT
echo "**Fecha:** $(date '+%Y-%m-%d %H:%M:%S')" >> $OUTPUT
echo "" >> $OUTPUT

TABLAS=("usuarios" "roles" "personal" "servicios" "pacientes" "historial_medico" "imagenes_clinicas" "consultas" "intervenciones" "intervenciones_servicios" "condiciones_diente" "dientes" "pagos" "pagos_secuencias")

for tabla in "${TABLAS[@]}"; do
    echo "---" >> $OUTPUT
    echo "" >> $OUTPUT
    echo "## TABLA: \`$tabla\`" >> $OUTPUT
    echo "" >> $OUTPUT
    echo '```' >> $OUTPUT
    docker exec supabase_db_tesis-main psql -U postgres -d postgres -c "\d+ $tabla" >> $OUTPUT 2>&1
    echo '```' >> $OUTPUT
    echo "" >> $OUTPUT
done

echo "---" >> $OUTPUT
echo "" >> $OUTPUT
echo "## VISTAS" >> $OUTPUT
echo "" >> $OUTPUT

VISTAS=("verificacion_limpieza" "vista_cola_odontologos" "vista_personal_completo")

for vista in "${VISTAS[@]}"; do
    echo "### VISTA: \`$vista\`" >> $OUTPUT
    echo "" >> $OUTPUT
    echo '```' >> $OUTPUT
    docker exec supabase_db_tesis-main psql -U postgres -d postgres -c "\d+ $vista" >> $OUTPUT 2>&1
    echo '```' >> $OUTPUT
    echo "" >> $OUTPUT
done

echo "---" >> $OUTPUT
echo "" >> $OUTPUT
echo "## TRIGGERS" >> $OUTPUT
echo "" >> $OUTPUT
echo '```' >> $OUTPUT
docker exec supabase_db_tesis-main psql -U postgres -d postgres -c "SELECT trigger_name, event_object_table, action_timing, event_manipulation, action_statement FROM information_schema.triggers WHERE trigger_schema = 'public' ORDER BY event_object_table, trigger_name;" >> $OUTPUT 2>&1
echo '```' >> $OUTPUT
echo "" >> $OUTPUT

echo "---" >> $OUTPUT
echo "" >> $OUTPUT
echo "## FUNCIONES" >> $OUTPUT
echo "" >> $OUTPUT
echo '```' >> $OUTPUT
docker exec supabase_db_tesis-main psql -U postgres -d postgres -c "SELECT proname, pg_get_functiondef(oid) FROM pg_proc WHERE pronamespace = 'public'::regnamespace ORDER BY proname;" >> $OUTPUT 2>&1
echo '```' >> $OUTPUT

echo "Archivo generado: $OUTPUT"
