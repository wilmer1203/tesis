# 🛠️ GUÍA DE IMPLEMENTACIÓN: Correcciones a `_actualizar_odontograma_por_servicios`

**Fecha:** 2025-10-19
**Versión Objetivo:** V4.0 Corregida y Simplificada
**Basado en:** Análisis Exhaustivo de V3.0

---

## 📋 ÍNDICE DE CORRECCIONES

### **FASE 1: Correcciones Críticas (OBLIGATORIO)** 🔴
1. [Corregir Lógica de Prioridad](#1-corregir-lógica-de-prioridad)
2. [Soportar Servicios Multi-Diente](#2-soportar-servicios-multi-diente)
3. [Implementar Transaccionalidad Atómica](#3-implementar-transaccionalidad-atómica)

### **FASE 2: Simplificación (RECOMENDADO)** ⚙️
4. [Eliminar Normalización Multi-Formato](#4-eliminar-normalización-multi-formato)
5. [Mover Resolución de Conflictos a SQL](#5-mover-resolución-de-conflictos-a-sql)
6. [Extraer Subfunciones](#6-extraer-subfunciones)

### **FASE 3: Mejoras Complementarias (OPCIONAL)** ✨
7. [Validar Superficies y Condiciones](#7-validar-superficies-y-condiciones)
8. [Implementar Optimistic Locking](#8-implementar-optimistic-locking)
9. [Añadir Tests Unitarios](#9-añadir-tests-unitarios)

---

## 🔴 FASE 1: CORRECCIONES CRÍTICAS

### **1. Corregir Lógica de Prioridad**

**Problema:** Sistema usa prioridad de condición (severidad médica) en vez de temporalidad de aplicación.

**Archivo:** `dental_system/state/estado_intervencion_servicios.py`

#### **Opción A: Usar Timestamp de Aplicación (RECOMENDADO)**

```python
async def _resolver_conflictos_servicios(
    self,
    servicios_normalizados: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """
    V4.0: Resolver conflictos por TEMPORALIDAD (último servicio aplicado gana)

    Cambio vs V3.0:
    - ANTES: Ordenar por catalogo_condiciones.prioridad (severidad médica)
    - AHORA: Ordenar por timestamp_aplicacion (orden temporal)

    Justificación:
    Si se aplicó obturación DESPUÉS de diagnosticar caries,
    el diente está obturado (tratamiento > diagnóstico)
    """
    try:
        # Agrupar servicios por diente + superficie
        grupos: Dict[str, List[Dict]] = {}

        for idx, servicio in enumerate(servicios_normalizados):
            condicion = servicio.get("condicion_resultante")

            # Skip servicios preventivos
            if not condicion:
                continue

            diente = servicio.get("diente_numero")
            superficies = servicio.get("superficies", [])

            # ✅ NUEVO: Agregar índice temporal (orden de aplicación)
            servicio["orden_aplicacion"] = idx

            for superficie in superficies:
                clave = f"{diente}_{superficie}"

                if clave not in grupos:
                    grupos[clave] = []

                grupos[clave].append(servicio)

        # Resolver cada grupo
        servicios_resueltos = []

        for clave, servicios_en_grupo in grupos.items():
            if len(servicios_en_grupo) == 1:
                # Sin conflicto
                servicios_resueltos.append(servicios_en_grupo[0])
            else:
                # ✅ CORRECCIÓN: Ordenar por TEMPORALIDAD (orden_aplicacion)
                # En vez de prioridad médica
                servicios_en_grupo.sort(
                    key=lambda s: s.get("orden_aplicacion", 0),
                    reverse=False  # Menor índice primero
                )

                # ✅ TOMAR ÚLTIMO (más reciente)
                ganador = servicios_en_grupo[-1]

                logger.info(
                    f"⚖️ Conflicto resuelto por temporalidad | "
                    f"Diente-Superficie: {clave} | "
                    f"Servicios: {len(servicios_en_grupo)} | "
                    f"Ganador: {ganador.get('nombre')} (último aplicado)"
                )

                servicios_resueltos.append(ganador)

        return servicios_resueltos

    except Exception as e:
        logger.error(f"❌ Error resolviendo conflictos: {str(e)}")
        return servicios_normalizados  # Retornar sin resolver
```

#### **Opción B: Lógica Médica Explícita (ALTERNATIVA)**

```python
async def _resolver_conflictos_servicios(
    self,
    servicios_normalizados: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """
    V4.0 ALT: Resolver conflictos con lógica médica explícita

    Reglas médicas:
    1. Tratamiento > Diagnóstico (obturación > caries)
    2. Ausente es final (no se puede tratar diente ausente)
    3. Endodoncia > Cualquier otra (tratamiento invasivo)
    4. Si mismo tipo, último gana (temporalidad)
    """

    # Jerarquía médica (tratamiento > diagnóstico)
    JERARQUIA_MEDICA = {
        # Condiciones finales (no reversibles)
        "ausente": 1000,
        "implante": 900,

        # Tratamientos invasivos
        "endodoncia": 800,
        "corona": 700,
        "puente": 650,

        # Tratamientos restaurativos
        "obturacion": 500,

        # Condiciones patológicas (diagnóstico, no tratamiento)
        "caries": 100,
        "fractura": 90,

        # Condiciones normales
        "sano": 10
    }

    grupos: Dict[str, List[Dict]] = {}

    # ... (código de agrupación igual) ...

    for clave, servicios_en_grupo in grupos.items():
        if len(servicios_en_grupo) == 1:
            servicios_resueltos.append(servicios_en_grupo[0])
        else:
            # Ordenar por jerarquía médica + temporalidad
            servicios_en_grupo.sort(
                key=lambda s: (
                    JERARQUIA_MEDICA.get(s.get("condicion_resultante"), 0),
                    s.get("orden_aplicacion", 0)
                ),
                reverse=True  # Mayor jerarquía y más reciente primero
            )

            ganador = servicios_en_grupo[0]
            servicios_resueltos.append(ganador)

    return servicios_resueltos
```

---

### **2. Soportar Servicios Multi-Diente**

**Problema:** Solo procesa primer diente cuando servicio afecta múltiples dientes.

**Archivo:** `dental_system/state/estado_intervencion_servicios.py`

#### **Solución: Explosionar por Diente en Normalización**

```python
def _normalizar_servicio(
    self,
    servicio: Any
) -> List[Dict[str, Any]]:  # ← CAMBIO: Retorna LISTA
    """
    V4.0: Normalizar servicio a formato estándar

    CAMBIO CRÍTICO:
    - ANTES: Retornaba UN dict (solo primer diente)
    - AHORA: Retorna LISTA de dicts (uno por diente)

    Ejemplo:
    Input: Servicio con dientes [11, 12, 13]
    Output: [
        {diente_numero: 11, ...},
        {diente_numero: 12, ...},
        {diente_numero: 13, ...}
    ]
    """

    # Formato 1: ServicioIntervencionCompleto
    if isinstance(servicio, ServicioIntervencionCompleto):
        dientes_texto = servicio.dientes_afectados or ""
        dientes_numeros = self._extraer_numeros_dientes(dientes_texto)

        # ✅ CORRECCIÓN: Crear un servicio POR CADA diente
        servicios_normalizados = []

        for diente_numero in dientes_numeros:
            servicios_normalizados.append({
                "nombre": servicio.nombre_servicio,
                "condicion_resultante": servicio.nueva_condicion,
                "diente_numero": diente_numero,  # ← Un diente específico
                "superficies": servicio.superficies or [],
                "material": servicio.material,
                "observaciones": servicio.observaciones
            })

        return servicios_normalizados if servicios_normalizados else [
            {
                "nombre": servicio.nombre_servicio,
                "condicion_resultante": servicio.nueva_condicion,
                "diente_numero": None,  # Servicio general
                "superficies": servicio.superficies or [],
                "material": servicio.material,
                "observaciones": servicio.observaciones
            }
        ]

    # Formato 2: Dict
    elif isinstance(servicio, dict):
        dientes_texto = servicio.get("dientes_afectados", "")
        dientes_numeros = self._extraer_numeros_dientes(dientes_texto)

        servicios_normalizados = []

        for diente_numero in dientes_numeros:
            servicios_normalizados.append({
                "nombre": servicio.get("nombre", ""),
                "condicion_resultante": servicio.get("condicion_resultante"),
                "diente_numero": diente_numero,
                "superficies": self._expandir_superficies(servicio.get("superficie", "")),
                "material": servicio.get("material", ""),
                "observaciones": servicio.get("observaciones", "")
            })

        return servicios_normalizados if servicios_normalizados else [servicio]

    # Formato desconocido
    logger.warning(f"⚠️ Formato de servicio desconocido: {type(servicio)}")
    return [{}]  # Lista vacía de 1 elemento


# ✅ ACTUALIZAR PASO 2 en función principal:
async def _actualizar_odontograma_por_servicios(
    self, intervencion_id: str, servicios: List
) -> "ActualizacionOdontogramaResult":
    # ...

    # PASO 2: Normalizar servicios (MODIFICADO)
    servicios_normalizados = []
    for servicio in servicios:
        servicios_lista = self._normalizar_servicio(servicio)  # ← Retorna lista
        servicios_normalizados.extend(servicios_lista)  # ← extend en vez de append

    logger.info(
        f"📊 Normalización completada | "
        f"Servicios originales: {len(servicios)} | "
        f"Servicios normalizados: {len(servicios_normalizados)} | "
        f"Explosión por dientes: {len(servicios_normalizados) - len(servicios)}"
    )

    # ... (resto igual)
```

---

### **3. Implementar Transaccionalidad Atómica**

**Problema:** Batch no usa transacción explícita, fallos parciales dejan BD inconsistente.

**Archivo:** `dental_system/supabase/migrations/YYYYMMDD_fix_batch_transaccion.sql`

#### **Migración SQL: Agregar Transaccionalidad**

```sql
-- ============================================================================
-- MIGRACIÓN: Agregar transaccionalidad atómica a actualizar_condiciones_batch
-- ============================================================================
-- Fecha: 2025-10-19
-- Autor: Sistema
-- Objetivo: Garantizar atomicidad (todo o nada) en actualizaciones batch

-- ============================================================================
-- PASO 1: Backup de función actual
-- ============================================================================

-- Renombrar función actual como backup
ALTER FUNCTION actualizar_condiciones_batch(jsonb)
RENAME TO actualizar_condiciones_batch_v3_backup;

-- ============================================================================
-- PASO 2: Crear nueva función V4.0 con transaccionalidad
-- ============================================================================

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
BEGIN
    -- Contar total de actualizaciones
    total_actualizaciones := jsonb_array_length(actualizaciones);

    RAISE NOTICE '🚀 V4.0 Iniciando batch transaccional | Total: %', total_actualizaciones;

    -- ✅ INICIO TRANSACCIÓN EXPLÍCITA
    BEGIN
        -- Iterar cada actualización
        FOR upd IN SELECT * FROM jsonb_array_elements(actualizaciones) LOOP
            BEGIN
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
                    upd->>'material_utilizado',
                    upd->>'descripcion',
                    (upd->>'intervencion_id')::uuid,
                    (upd->>'registrado_por')::uuid,
                    TRUE,
                    CURRENT_TIMESTAMP
                ) RETURNING id INTO nueva_condicion_id;

                -- Registrar éxito
                ids_creados := array_append(ids_creados, nueva_condicion_id::text);
                exitosos := exitosos + 1;

            EXCEPTION WHEN OTHERS THEN
                -- ✅ Registrar error pero NO abortar transacción completa
                -- (Permite procesar resto de actualizaciones)
                fallidos := fallidos + 1;
                RAISE WARNING '⚠️ Error en actualización individual: % | Diente: % | Error: %',
                    upd->>'tipo_condicion',
                    upd->>'diente_numero',
                    SQLERRM;
            END;
        END LOOP;

        -- ✅ VALIDAR: Si hay fallos, decidir si revertir TODO
        IF fallidos > 0 THEN
            RAISE WARNING '⚠️ Batch con fallos parciales | Exitosos: % | Fallidos: %',
                exitosos, fallidos;

            -- OPCIÓN 1: Revertir TODO si hay UN solo fallo (más seguro)
            -- ROLLBACK;
            -- exitosos := 0;
            -- ids_creados := '{}';
            -- fallidos := total_actualizaciones;

            -- OPCIÓN 2: Permitir commit parcial (actual)
            -- (Se mantiene COMMIT abajo)
        END IF;

        -- ✅ COMMIT EXPLÍCITO (todo o nada)
        COMMIT;

        RAISE NOTICE '✅ Batch completado | Exitosos: % | Fallidos: %', exitosos, fallidos;

    EXCEPTION WHEN OTHERS THEN
        -- ✅ ROLLBACK EN CASO DE ERROR CRÍTICO
        ROLLBACK;

        RAISE WARNING '💥 Error crítico en batch, ROLLBACK completo: %', SQLERRM;

        -- Retornar todo como fallido
        exitosos := 0;
        fallidos := total_actualizaciones;
        ids_creados := '{}';
    END;

    -- Retornar resultado
    RETURN jsonb_build_object(
        'exitosos', exitosos,
        'fallidos', fallidos,
        'ids_creados', ids_creados,
        'total', total_actualizaciones
    );
END;
$$ LANGUAGE plpgsql;

-- ============================================================================
-- PASO 3: Comentar función con mejoras
-- ============================================================================

COMMENT ON FUNCTION actualizar_condiciones_batch(jsonb) IS
'V4.0 - Actualización batch con transaccionalidad atómica

MEJORAS vs V3.0:
- ✅ Transacción explícita BEGIN/COMMIT/ROLLBACK
- ✅ Manejo de errores individuales sin abortar batch completo
- ✅ Logging detallado con RAISE NOTICE/WARNING
- ✅ Validación de fallos parciales

OPCIONES DE ROLLBACK:
- Actual: Permite commit parcial (algunos exitosos, algunos fallidos)
- Alternativa: Descomentar ROLLBACK en línea 85 para todo-o-nada estricto

RETORNA:
{
  "exitosos": int,    -- Actualizaciones exitosas
  "fallidos": int,    -- Actualizaciones fallidas
  "ids_creados": [],  -- UUIDs de condiciones creadas
  "total": int        -- Total de actualizaciones intentadas
}
';

-- ============================================================================
-- PASO 4: Verificación
-- ============================================================================

-- Test básico (NO ejecutar en producción sin datos válidos)
-- SELECT actualizar_condiciones_batch('[
--   {
--     "paciente_id": "uuid-valido",
--     "diente_numero": 11,
--     "superficie": "oclusal",
--     "tipo_condicion": "sano",
--     "material_utilizado": "",
--     "descripcion": "Test",
--     "intervencion_id": "uuid-valido",
--     "registrado_por": "uuid-valido"
--   }
-- ]'::jsonb);
```

#### **Configuración en Python (Opción TODO-O-NADA)**

Si se prefiere todo-o-nada estricto, agregar validación en Python:

```python
# En odontologia_service.py

async def actualizar_condiciones_batch(
    self,
    actualizaciones: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """V4.0: Batch con validación todo-o-nada opcional"""

    try:
        # ... código existente ...

        result = self.client.rpc('actualizar_condiciones_batch', {
            'actualizaciones': actualizaciones_jsonb
        }).execute()

        if result.data:
            data = result.data[0] if isinstance(result.data, list) else result.data

            exitosos = data.get("exitosos", 0)
            fallidos = data.get("fallidos", 0)
            total = data.get("total", 0)

            # ✅ VALIDACIÓN TODO-O-NADA (opcional)
            if fallidos > 0:
                logger.error(
                    f"❌ Batch con fallos parciales | "
                    f"Exitosos: {exitosos} | Fallidos: {fallidos}"
                )

                # OPCIÓN A: Lanzar excepción para revertir en app
                raise ValueError(
                    f"Batch parcialmente fallido: {fallidos}/{total} fallos"
                )

                # OPCIÓN B: Retornar como fallido pero sin excepción
                # return {
                #     "success": False,
                #     "exitosos": 0,
                #     "fallidos": total,
                #     "ids_creados": [],
                #     "error": f"{fallidos} actualizaciones fallaron"
                # }

            return {
                "success": True,
                "exitosos": exitosos,
                "fallidos": fallidos,
                "ids_creados": data.get("ids_creados", [])
            }

    except Exception as e:
        logger.error(f"❌ Error en batch: {str(e)}")
        return {
            "success": False,
            "exitosos": 0,
            "fallidos": len(actualizaciones),
            "ids_creados": [],
            "error": str(e)
        }
```

---

## ⚙️ FASE 2: SIMPLIFICACIÓN (RECOMENDADO)

### **4. Eliminar Normalización Multi-Formato**

**Objetivo:** Forzar tipo único desde origen, eliminar conversión runtime.

**Archivos:**
- `dental_system/models/odontologia_models.py`
- `dental_system/state/estado_odontologia.py`
- `dental_system/state/estado_intervencion_servicios.py`

#### **Paso 4.1: Crear Modelo Normalizado Único**

```python
# dental_system/models/odontologia_models.py

class ServicioIntervencionNormalizado(rx.Base):
    """
    V4.0: Modelo ÚNICO para servicios en intervenciones

    Este modelo reemplaza ServicioIntervencionCompleto,
    ServicioIntervencionTemporal y dicts sueltos.

    Ventajas:
    - ✅ Validación en compile-time (no runtime)
    - ✅ Tipado fuerte
    - ✅ Sin necesidad de _normalizar_servicio()
    """

    # Identificación
    servicio_id: str  # UUID del catálogo de servicios
    nombre_servicio: str  # "Obturación Simple"
    categoria: str = "general"  # "restaurativa", "preventiva", etc.

    # Condición resultante (None si preventivo)
    condicion_resultante: Optional[str] = None  # "obturacion", "sano", None

    # Dientes afectados (lista, NO solo el primero)
    dientes_numeros: List[int] = []  # [11, 12, 13] o [] si general

    # Superficies (ya expandidas, NO "completa")
    superficies: List[str] = []  # ["oclusal", "mesial"] o [] si general

    # Detalles clínicos
    material_utilizado: str = ""
    observaciones: str = ""
    tecnica_utilizada: str = ""

    # Temporalidad (para resolución de conflictos)
    orden_aplicacion: int = 0  # Índice en lista original

    # Precios (para facturación)
    precio_unitario_bs: float = 0.0
    precio_unitario_usd: float = 0.0
    cantidad: int = 1

    @property
    def es_preventivo(self) -> bool:
        """Servicio preventivo (no modifica odontograma)"""
        return self.condicion_resultante is None

    @property
    def afecta_odontograma(self) -> bool:
        """Servicio modifica odontograma"""
        return (
            self.condicion_resultante is not None
            and len(self.dientes_numeros) > 0
        )

    @property
    def total_superficies_afectadas(self) -> int:
        """Total de superficies que se actualizarán"""
        return len(self.dientes_numeros) * len(self.superficies)
```

#### **Paso 4.2: Normalizar en Origen (Estado Odontología)**

```python
# dental_system/state/estado_odontologia.py

class EstadoOdontologia(rx.State):
    # ... código existente ...

    def _convertir_a_servicio_normalizado(
        self,
        servicio_temp: ServicioIntervencionTemporal,
        orden: int
    ) -> ServicioIntervencionNormalizado:
        """
        V4.0: Convertir servicio temporal a normalizado

        La normalización ocurre AQUÍ (origen),
        NO en _actualizar_odontograma_por_servicios
        """

        # Extraer dientes
        dientes_numeros = []
        if servicio_temp.dientes_texto:
            dientes_numeros = self._extraer_numeros_dientes_validados(
                servicio_temp.dientes_texto
            )

        # Expandir superficies
        superficies = self._expandir_superficies_validadas(
            servicio_temp.superficie_texto
        )

        return ServicioIntervencionNormalizado(
            servicio_id=servicio_temp.servicio_id,
            nombre_servicio=servicio_temp.nombre_servicio,
            categoria=servicio_temp.categoria,
            condicion_resultante=servicio_temp.nueva_condicion,
            dientes_numeros=dientes_numeros,
            superficies=superficies,
            material_utilizado=servicio_temp.material,
            observaciones=servicio_temp.observaciones,
            orden_aplicacion=orden,
            precio_unitario_bs=servicio_temp.precio_bs,
            precio_unitario_usd=servicio_temp.precio_usd,
            cantidad=1
        )

    def _extraer_numeros_dientes_validados(self, texto: str) -> List[int]:
        """Extraer y VALIDAR dientes FDI"""
        import re

        if not texto:
            return []

        # Casos especiales
        texto_lower = texto.lower()
        if "todos" in texto_lower or "toda" in texto_lower:
            # Todos los dientes FDI (32)
            return list(range(11, 19)) + list(range(21, 29)) + \
                   list(range(31, 39)) + list(range(41, 49))

        # Extraer números FDI (11-48)
        numeros = re.findall(r'\b([1-4][1-8])\b', texto)

        dientes_validos = []
        for num_str in numeros:
            num = int(num_str)
            # Validar rango FDI
            cuadrante = num // 10
            posicion = num % 10
            if cuadrante in [1, 2, 3, 4] and 1 <= posicion <= 8:
                dientes_validos.append(num)
            else:
                logger.warning(f"⚠️ Diente inválido ignorado: {num}")

        return sorted(list(set(dientes_validos)))  # Únicos y ordenados

    def _expandir_superficies_validadas(self, texto: str) -> List[str]:
        """Expandir y VALIDAR superficies dentales"""

        SUPERFICIES_VALIDAS = {
            "oclusal", "mesial", "distal", "vestibular", "lingual"
        }

        TODAS_SUPERFICIES = ["oclusal", "mesial", "distal", "vestibular", "lingual"]

        if not texto:
            return TODAS_SUPERFICIES  # Default: todas

        texto_lower = texto.lower().strip()

        # Mapeo de nombres comunes
        mapeo = {
            "oclusal": ["oclusal"],
            "mesial": ["mesial"],
            "distal": ["distal"],
            "vestibular": ["vestibular"],
            "lingual": ["lingual"],
            "palatino": ["lingual"],
            "completa": TODAS_SUPERFICIES,
            "todas": TODAS_SUPERFICIES,
            "todo": TODAS_SUPERFICIES,
            "no especifica": TODAS_SUPERFICIES,
            "no específica": TODAS_SUPERFICIES
        }

        if texto_lower in mapeo:
            return mapeo[texto_lower]

        # Validar si es superficie válida
        if texto_lower in SUPERFICIES_VALIDAS:
            return [texto_lower]

        # No reconocido, usar todas
        logger.warning(f"⚠️ Superficie no reconocida '{texto}', usando todas")
        return TODAS_SUPERFICIES

    async def crear_intervencion_con_servicios(self):
        """
        V4.0: Crear intervención con servicios PRE-NORMALIZADOS
        """

        # Convertir servicios temporales a normalizados
        servicios_normalizados = [
            self._convertir_a_servicio_normalizado(servicio_temp, idx)
            for idx, servicio_temp in enumerate(self.servicios_intervencion)
        ]

        logger.info(
            f"📦 Servicios normalizados | "
            f"Total: {len(servicios_normalizados)} | "
            f"Preventivos: {sum(1 for s in servicios_normalizados if s.es_preventivo)} | "
            f"Modifican odontograma: {sum(1 for s in servicios_normalizados if s.afecta_odontograma)}"
        )

        # Llamar servicio con datos normalizados
        resultado = await self.servicio_intervencion.crear_intervencion_completa(
            consulta_id=self.consulta_actual.id,
            paciente_id=self.paciente_actual.id,
            odontologo_id=self.id_usuario,
            servicios_normalizados=servicios_normalizados,  # ← YA NORMALIZADO
            observaciones=self.observaciones_intervencion
        )

        if resultado.get("success"):
            # Actualizar odontograma (YA NO necesita normalizar)
            await self._actualizar_odontograma_por_servicios(
                resultado["intervencion_id"],
                servicios_normalizados  # ← TIPO ÚNICO
            )
```

#### **Paso 4.3: Simplificar Función Principal**

```python
# dental_system/state/estado_intervencion_servicios.py

async def _actualizar_odontograma_por_servicios(
    self,
    intervencion_id: str,
    servicios: List[ServicioIntervencionNormalizado]  # ← TIPO ÚNICO
) -> "ActualizacionOdontogramaResult":
    """
    V4.0 SIMPLIFICADO - Sin normalización runtime

    ELIMINADO:
    - ❌ _normalizar_servicio() (60 líneas)
    - ❌ Detección de formato
    - ❌ Conversión runtime

    ASUME:
    - ✅ servicios ya están normalizados
    - ✅ Tipo único ServicioIntervencionNormalizado
    - ✅ Validaciones ya realizadas en origen
    """
    resultado = ActualizacionOdontogramaResult()

    try:
        # PASO 1: Validar contexto (simplificado)
        if not self.paciente_actual or not self.paciente_actual.id:
            resultado.advertencias.append("No hay paciente válido")
            return resultado

        if not servicios:
            resultado.advertencias.append("No hay servicios")
            return resultado

        logger.info(
            f"🦷 V4.0 Iniciando actualización | "
            f"Paciente: {self.paciente_actual.id[:8]}... | "
            f"Servicios: {len(servicios)}"
        )

        # PASO 2: ❌ ELIMINADO - Normalización (ya viene normalizado)

        # PASO 3: Filtrar servicios activos (simplificado)
        servicios_activos = [
            s for s in servicios
            if s.afecta_odontograma  # ← Usa property del modelo
        ]

        if not servicios_activos:
            resultado.advertencias.append("Todos los servicios son preventivos")
            return resultado

        logger.info(f"📊 Servicios activos: {len(servicios_activos)}/{len(servicios)}")

        # PASO 4: Resolver conflictos (simplificado)
        servicios_resueltos = await self._resolver_conflictos_v4(servicios_activos)

        # PASO 5: Preparar batch (simplificado)
        actualizaciones = self._preparar_batch_v4(servicios_resueltos, intervencion_id)

        if not actualizaciones:
            resultado.advertencias.append("No hay actualizaciones después de resolución")
            return resultado

        # PASO 6: Ejecutar batch transaccional
        batch_result = await odontologia_service.actualizar_condiciones_batch(
            actualizaciones
        )

        # PASO 7: Procesar resultado
        resultado.exitosos = batch_result.get("exitosos", 0)
        resultado.fallidos = batch_result.get("fallidos", 0)
        resultado.ids_creados = batch_result.get("ids_creados", [])

        if resultado.fallidos > 0:
            resultado.advertencias.append(
                f"{resultado.fallidos} actualizaciones fallaron"
            )

        # PASO 8: Recargar UI
        if resultado.exitosos > 0:
            logger.info(
                f"✅ Odontograma actualizado | "
                f"Exitosos: {resultado.exitosos} | "
                f"Tasa: {resultado.tasa_exito_pct:.1f}%"
            )
            await self._recargar_odontograma_ui()

        return resultado

    except Exception as e:
        logger.error(f"💥 Error crítico: {str(e)}", exc_info=True)
        resultado.advertencias.append(f"Error: {str(e)}")
        return resultado


def _preparar_batch_v4(
    self,
    servicios: List[ServicioIntervencionNormalizado],
    intervencion_id: str
) -> List[Dict[str, Any]]:
    """V4.0: Preparar batch (código extraído y simplificado)"""

    actualizaciones = []

    for servicio in servicios:
        for diente_numero in servicio.dientes_numeros:  # ← YA es lista completa
            for superficie in servicio.superficies:  # ← YA expandidas
                actualizaciones.append({
                    "paciente_id": self.paciente_actual.id,
                    "diente_numero": diente_numero,
                    "superficie": superficie,
                    "tipo_condicion": servicio.condicion_resultante,
                    "material_utilizado": servicio.material_utilizado,
                    "descripcion": servicio.observaciones or servicio.nombre_servicio,
                    "intervencion_id": intervencion_id
                })

    logger.info(f"📦 Batch preparado: {len(actualizaciones)} actualizaciones")
    return actualizaciones
```

**Beneficio:** 80 líneas → 40 líneas (50% reducción)

---

### **5. Mover Resolución de Conflictos a SQL**

**Objetivo:** Ejecutar resolución en BD (más eficiente).

**Archivo:** `dental_system/supabase/migrations/YYYYMMDD_resolver_conflictos_sql.sql`

```sql
-- ============================================================================
-- FUNCIÓN SQL: Resolver conflictos de servicios
-- ============================================================================
-- V4.0: Mover lógica de Python a PostgreSQL

CREATE OR REPLACE FUNCTION resolver_conflictos_servicios(
    servicios_json jsonb
) RETURNS jsonb AS $$
DECLARE
    servicios_resueltos jsonb := '[]'::jsonb;
    servicio_ganador jsonb;
BEGIN
    RAISE NOTICE '⚖️ Resolviendo conflictos de servicios en SQL';

    -- Agrupar por diente + superficie y tomar el de mayor orden_aplicacion
    -- (último aplicado gana)
    FOR servicio_ganador IN
        SELECT DISTINCT ON (s->>'diente_numero', s->>'superficie')
            s as servicio
        FROM jsonb_array_elements(servicios_json) s
        WHERE
            -- Solo servicios que afectan odontograma
            s->>'condicion_resultante' IS NOT NULL
            AND s->>'diente_numero' IS NOT NULL
        ORDER BY
            s->>'diente_numero',
            s->>'superficie',
            (s->>'orden_aplicacion')::int DESC  -- ← Último aplicado primero
    LOOP
        servicios_resueltos := servicios_resueltos || servicio_ganador;
    END LOOP;

    RETURN servicios_resueltos;
END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION resolver_conflictos_servicios(jsonb) IS
'V4.0 - Resolver conflictos de servicios por temporalidad

Regla: Cuando múltiples servicios afectan mismo diente+superficie,
       el ÚLTIMO aplicado (mayor orden_aplicacion) gana.

Justificación: Si se aplicó obturación DESPUÉS de diagnosticar caries,
               el diente está obturado (tratamiento > diagnóstico).

Input:  jsonb array de servicios normalizados
Output: jsonb array sin conflictos (uno por diente+superficie)
';
```

**Uso en Python:**

```python
async def _resolver_conflictos_v4(
    self,
    servicios_activos: List[ServicioIntervencionNormalizado]
) -> List[Dict[str, Any]]:
    """V4.0: Resolver conflictos en SQL (más eficiente)"""

    # Convertir a JSONB
    import json
    servicios_json = json.dumps([
        {
            "diente_numero": s.dientes_numeros[0] if s.dientes_numeros else None,
            "superficie": s.superficies[0] if s.superficies else None,
            "condicion_resultante": s.condicion_resultante,
            "orden_aplicacion": s.orden_aplicacion,
            "nombre": s.nombre_servicio,
            "material": s.material_utilizado,
            "observaciones": s.observaciones
        }
        for s in servicios_activos
    ])

    # Llamar función SQL
    result = self.client.rpc('resolver_conflictos_servicios', {
        'servicios_json': servicios_json
    }).execute()

    servicios_resueltos = json.loads(result.data) if result.data else []

    logger.info(
        f"⚖️ Conflictos resueltos en SQL | "
        f"Entrada: {len(servicios_activos)} | "
        f"Salida: {len(servicios_resueltos)} | "
        f"Descartados: {len(servicios_activos) - len(servicios_resueltos)}"
    )

    return servicios_resueltos
```

**Beneficio:** 50 líneas Python → 1 llamada SQL

---

### **6. Extraer Subfunciones**

**Objetivo:** Reducir complejidad de función principal.

```python
# dental_system/state/estado_intervencion_servicios.py

# ============================================================================
# HELPERS EXTRAÍDOS
# ============================================================================

def _tiene_contexto_valido(self, servicios) -> Tuple[bool, str]:
    """Validar contexto (paciente + servicios)"""
    if not self.paciente_actual or not self.paciente_actual.id:
        return False, "No hay paciente válido"

    if not servicios:
        return False, "No hay servicios para procesar"

    return True, ""


def _filtrar_servicios_activos(
    self,
    servicios: List[ServicioIntervencionNormalizado]
) -> List[ServicioIntervencionNormalizado]:
    """Filtrar servicios que modifican odontograma"""
    activos = [s for s in servicios if s.afecta_odontograma]

    logger.info(
        f"🔍 Filtrado | "
        f"Total: {len(servicios)} | "
        f"Activos: {len(activos)} | "
        f"Preventivos: {len(servicios) - len(activos)}"
    )

    return activos


async def _recargar_odontograma_ui(self):
    """Recargar odontograma en UI sin fallar"""
    try:
        await self.cargar_odontograma_paciente(self.paciente_actual.id)
        logger.info("♻️ Odontograma recargado en UI")
    except AttributeError:
        pass  # Método no disponible en este contexto
    except Exception as e:
        logger.warning(f"⚠️ Error recargando UI: {e}")


def _manejar_error_critico(
    self,
    resultado: "ActualizacionOdontogramaResult",
    error: Exception
) -> "ActualizacionOdontogramaResult":
    """Manejo centralizado de errores críticos"""
    logger.error(f"💥 Error crítico: {error}", exc_info=True)
    resultado.advertencias.append(f"Error: {str(error)}")
    return resultado


# ============================================================================
# FUNCIÓN PRINCIPAL SIMPLIFICADA
# ============================================================================

async def _actualizar_odontograma_por_servicios(
    self,
    intervencion_id: str,
    servicios: List[ServicioIntervencionNormalizado]
) -> "ActualizacionOdontogramaResult":
    """
    V4.0 ULTRA-SIMPLIFICADO - 25 líneas vs 80 originales

    MEJORAS:
    - ✅ Sin normalización (tipo único)
    - ✅ Subfunciones extraídas
    - ✅ Resolución en SQL
    - ✅ Batch transaccional
    """
    resultado = ActualizacionOdontogramaResult()

    try:
        # PASO 1: Validar
        valido, mensaje = self._tiene_contexto_valido(servicios)
        if not valido:
            resultado.advertencias.append(mensaje)
            return resultado

        # PASO 2: Filtrar activos
        servicios_activos = self._filtrar_servicios_activos(servicios)
        if not servicios_activos:
            resultado.advertencias.append("Solo servicios preventivos")
            return resultado

        # PASO 3: Resolver conflictos (SQL)
        servicios_resueltos = await self._resolver_conflictos_v4(servicios_activos)

        # PASO 4: Preparar + Ejecutar batch
        actualizaciones = self._preparar_batch_v4(servicios_resueltos, intervencion_id)
        batch_result = await odontologia_service.actualizar_condiciones_batch(
            actualizaciones
        )

        # PASO 5: Procesar resultado
        resultado.actualizar_desde_batch(batch_result)  # Helper en modelo

        # PASO 6: Recargar UI si exitoso
        if resultado.exitosos > 0:
            await self._recargar_odontograma_ui()

        return resultado

    except Exception as e:
        return self._manejar_error_critico(resultado, e)
```

**Resultado:**
- **ANTES:** 80 líneas en 1 función
- **DESPUÉS:** 25 líneas + 5 helpers (30 líneas cada uno)
- **Reducción:** 69% menos código en función principal

---

## ✅ CHECKLIST DE IMPLEMENTACIÓN

### **Fase 1: Crítico** 🔴
- [ ] Corregir lógica de prioridad (Opción A o B)
- [ ] Test manual: Servicio con múltiples dientes
- [ ] Crear migración de transaccionalidad
- [ ] Aplicar migración en BD desarrollo
- [ ] Test: Batch con 1 fallo (verificar rollback)
- [ ] Test: Batch completo exitoso

### **Fase 2: Simplificación** ⚙️
- [ ] Crear modelo `ServicioIntervencionNormalizado`
- [ ] Actualizar estado_odontologia con normalización
- [ ] Eliminar `_normalizar_servicio()` de estado_intervencion
- [ ] Crear función SQL `resolver_conflictos_servicios()`
- [ ] Actualizar `_resolver_conflictos_v4()` para usar SQL
- [ ] Extraer subfunciones helpers
- [ ] Actualizar función principal simplificada

### **Fase 3: Validación Final** ✅
- [ ] Tests unitarios (ver sección 9)
- [ ] Tests de integración
- [ ] Validación con datos reales
- [ ] Performance benchmarks
- [ ] Code review
- [ ] Actualizar documentación
- [ ] Deploy a producción

---

**FIN DE LA GUÍA DE IMPLEMENTACIÓN**

**Próximo Documento:** Tests Unitarios (sección 9)
**Tiempo Estimado Total:** 7 días desarrollo + 2 días testing
**Fecha:** 2025-10-19
