-- =====================================================
-- Vista consolidada para gestión de personal
-- Adaptada al nuevo esquema (esquema_final_corregido.sql v4.1)
-- =====================================================

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
    p.estado_laboral,
    p.observaciones,
    
    -- ✅ Campos de nombres SEPARADOS (nuevo esquema)
    p.primer_nombre,
    p.segundo_nombre,
    p.primer_apellido,
    p.segundo_apellido,
    
    -- ✅ Campos específicos para odontólogos (nuevo esquema)
    p.acepta_pacientes_nuevos,
    p.orden_preferencia,
    
    -- Información del usuario (aplanada)
    p.usuario_id,
    u.email,
    u.activo as usuario_activo,
    u.ultimo_acceso,
    u.fecha_creacion,
    u.auth_user_id,
    u.avatar_url,
    u.metadata,
    u.configuraciones,
    
    -- Información del rol
    r.id as rol_id,
    r.nombre as rol_nombre,
    r.descripcion as rol_descripcion,
    r.permisos as rol_permisos,
    
    -- ✅ Nombre completo calculado (para compatibilidad)
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
    
    -- ✅ JSON para compatibilidad con código existente (CORREGIDO)
    jsonb_build_object(
        'id', u.id,
        'email', u.email,
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

-- =====================================================
-- Comentarios sobre los cambios realizados:
-- 
-- ELIMINADO del esquema anterior:
-- - u.telefono (no existe en el nuevo esquema)
--
-- AGREGADO del nuevo esquema:
-- - p.acepta_pacientes_nuevos (específico para odontólogos)
-- - p.orden_preferencia (específico para odontólogos)
-- - u.configuraciones (nuevo campo JSONB)
--
-- CORREGIDO:
-- - Sintaxis del JSON en usuario_info (estaba mal formado)
-- - Referencias a campos que no existen
-- =====================================================