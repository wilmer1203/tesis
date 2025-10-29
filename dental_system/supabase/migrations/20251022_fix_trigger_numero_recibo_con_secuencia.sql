-- ✅ SOLUCIÓN AL RACE CONDITION DEL TRIGGER DE NUMERO_RECIBO
-- Problema: MAX() + 1 tiene race condition cuando se ejecuta simultáneamente
-- Solución: Usar tabla de secuencias atómicas por mes

-- =====================================================
-- PASO 1: CREAR TABLA DE SECUENCIAS POR MES
-- =====================================================
CREATE TABLE IF NOT EXISTS pagos_secuencias (
    año_mes VARCHAR(6) PRIMARY KEY,  -- "202510"
    ultimo_numero INTEGER DEFAULT 0 NOT NULL
);

COMMENT ON TABLE pagos_secuencias IS 'Secuencias atómicas para numero_recibo por mes';

-- =====================================================
-- PASO 2: FUNCIÓN PARA OBTENER SIGUIENTE NÚMERO (ATÓMICA)
-- =====================================================
CREATE OR REPLACE FUNCTION obtener_siguiente_numero_recibo(fecha DATE)
RETURNS INTEGER AS $$
DECLARE
    año_mes_key VARCHAR(6);
    siguiente_num INTEGER;
BEGIN
    -- Formato: YYYYMM
    año_mes_key := TO_CHAR(fecha, 'YYYYMM');

    -- 🔒 UPSERT ATÓMICO: Incrementar o crear registro
    INSERT INTO pagos_secuencias (año_mes, ultimo_numero)
    VALUES (año_mes_key, 1)
    ON CONFLICT (año_mes)
    DO UPDATE SET ultimo_numero = pagos_secuencias.ultimo_numero + 1
    RETURNING ultimo_numero INTO siguiente_num;

    RETURN siguiente_num;
END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION obtener_siguiente_numero_recibo IS 'Genera siguiente número de recibo atómicamente (sin race condition)';

-- =====================================================
-- PASO 3: TRIGGER CORREGIDO (USANDO SECUENCIA ATÓMICA)
-- =====================================================
CREATE OR REPLACE FUNCTION generar_numero_recibo()
RETURNS TRIGGER AS $$
DECLARE
    siguiente_numero INTEGER;
    nuevo_numero VARCHAR(20);
    fecha_actual DATE;
BEGIN
    IF NEW.numero_recibo IS NULL OR NEW.numero_recibo = '' THEN
        fecha_actual := COALESCE(NEW.fecha_pago::DATE, CURRENT_DATE);

        -- ✅ OBTENER SIGUIENTE NÚMERO DE FORMA ATÓMICA (sin race condition)
        siguiente_numero := obtener_siguiente_numero_recibo(fecha_actual);

        -- Generar número: REC + YYYYMM + 0001
        nuevo_numero := 'REC' || TO_CHAR(fecha_actual, 'YYYYMM') || LPAD(siguiente_numero::TEXT, 4, '0');

        NEW.numero_recibo := nuevo_numero;

        RAISE NOTICE 'Generado numero_recibo: %', nuevo_numero;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- =====================================================
-- PASO 4: RECREAR TRIGGER (por si ya existe)
-- =====================================================
DROP TRIGGER IF EXISTS trigger_generar_numero_recibo ON pagos;

CREATE TRIGGER trigger_generar_numero_recibo
    BEFORE INSERT ON pagos
    FOR EACH ROW
    EXECUTE FUNCTION generar_numero_recibo();

-- =====================================================
-- PASO 5: INICIALIZAR SECUENCIA CON DATOS EXISTENTES
-- =====================================================
-- Si ya tienes pagos en la BD, inicializar la secuencia con el último número usado
DO $$
DECLARE
    registro RECORD;
BEGIN
    FOR registro IN
        SELECT
            TO_CHAR(fecha_pago, 'YYYYMM') as año_mes,
            MAX(CAST(SUBSTRING(numero_recibo FROM 8) AS INTEGER)) as max_num
        FROM pagos
        WHERE numero_recibo IS NOT NULL
          AND numero_recibo ~ '^REC[0-9]{6}[0-9]+$'
        GROUP BY TO_CHAR(fecha_pago, 'YYYYMM')
    LOOP
        INSERT INTO pagos_secuencias (año_mes, ultimo_numero)
        VALUES (registro.año_mes, registro.max_num)
        ON CONFLICT (año_mes) DO NOTHING;
    END LOOP;

    RAISE NOTICE 'Secuencias inicializadas desde datos existentes';
END $$;

-- =====================================================
-- TESTING: VERIFICAR FUNCIONAMIENTO
-- =====================================================
-- Mostrar secuencias actuales
SELECT * FROM pagos_secuencias ORDER BY año_mes DESC;

-- Probar generación (simulación)
SELECT 'REC' || TO_CHAR(CURRENT_DATE, 'YYYYMM') || LPAD(obtener_siguiente_numero_recibo(CURRENT_DATE)::TEXT, 4, '0') as siguiente_recibo;
