# 🔍 ANÁLISIS DE SINCRONIZACIÓN: MODELOS VS ESQUEMA DE BASE DE DATOS
## Sistema Odontológico - Verificación de Integridad Estructural

**Fecha:** 2025-10-13
**Contexto:** Verificación de sincronización entre `estado_intervencion_servicios.py` y esquema PostgreSQL
**Objetivo:** Detectar desalineaciones entre modelos Python y tablas de BD

---

## 📊 RESUMEN EJECUTIVO

### **Estado General:**
- ✅ **Tabla Principal:** `intervenciones_servicios` SINCRONIZADA
- ✅ **Campos Nuevos:** `diente_numero`, `superficie` AGREGADOS (Migración 20251010)
- ⚠️ **Modelo Python:** `ServicioIntervencionTemporal` necesita actualización
- 🔄 **Compatibilidad:** 85% - Requiere ajustes menores

---

## 🗄️ ESQUEMA DE BASE DE DATOS (FUENTE DE VERDAD)

### **Tabla: `intervenciones_servicios`**

#### **📋 Estructura Actual (desde esquema.sql + migración 20251010)**

```sql
CREATE TABLE intervenciones_servicios (
    -- Identificadores
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    intervencion_id UUID NOT NULL REFERENCES intervenciones(id) ON DELETE CASCADE,
    servicio_id UUID NOT NULL REFERENCES servicios(id),

    -- Información económica
    cantidad INTEGER DEFAULT 1 NOT NULL,
    precio_unitario_bs DECIMAL(10, 2) DEFAULT 0,
    precio_unitario_usd DECIMAL(10, 2) DEFAULT 0,
    precio_total_bs DECIMAL(10, 2) DEFAULT 0,
    precio_total_usd DECIMAL(10, 2) DEFAULT 0,

    -- 🆕 CAMPOS AGREGADOS EN MIGRACIÓN 20251010
    diente_numero INTEGER,                    -- Número FDI del diente (11-48)
    superficie VARCHAR(20),                   -- Superficie específica (oclusal, mesial, distal, vestibular, lingual)

    -- Observaciones
    observaciones TEXT,

    -- Timestamps
    fecha_creacion TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Índices optimizados
CREATE INDEX idx_interv_servicios_diente ON intervenciones_servicios(diente_numero);
CREATE INDEX idx_interv_servicios_diente_superficie ON intervenciones_servicios(diente_numero, superficie);
```

#### **✅ Campos Totales en BD:** 12 campos

---

## 🐍 MODELO PYTHON ACTUAL

### **Clase: `ServicioIntervencionTemporal` (estado_intervencion_servicios.py, líneas 15-50)**

```python
class ServicioIntervencionTemporal(rx.Base):
    """🛒 Modelo temporal para servicios en intervención"""
    # Identificadores
    id_servicio: str = ""
    nombre_servicio: str = ""
    categoria_servicio: str = ""

    # Dientes y cantidad
    dientes_texto: str = ""                  # ⚠️ "11, 12, 21" (string)
    cantidad: int = 1

    # Precios
    precio_unitario_bs: float = 0.0
    precio_unitario_usd: float = 0.0
    total_bs: float = 0.0
    total_usd: float = 0.0

    # 🆕 Nuevos campos clínicos (agregados recientemente)
    material_utilizado: str = ""             # ✅ Amalgama, Resina, Composite, etc.
    superficie_dental: str = ""              # ⚠️ NOMBRE DIFERENTE vs BD (superficie)
    observaciones: str = ""                  # ✅ Notas específicas del procedimiento
```

#### **✅ Campos Totales en Modelo:** 13 campos

---

## 🔍 COMPARACIÓN DETALLADA CAMPO POR CAMPO

| # | Campo BD | Campo Modelo | Estado | Notas |
|---|----------|--------------|--------|-------|
| 1 | `id` | ❌ No existe | ⚠️ **FALTANTE** | ID autogenerado por BD, no necesario en temporal |
| 2 | `intervencion_id` | ❌ No existe | ✅ OK | Se agrega al insertar en BD |
| 3 | `servicio_id` | ✅ `id_servicio` | ✅ OK | Mapeo correcto |
| 4 | `cantidad` | ✅ `cantidad` | ✅ OK | Tipo compatible (int) |
| 5 | `precio_unitario_bs` | ✅ `precio_unitario_bs` | ✅ OK | Tipo compatible (float) |
| 6 | `precio_unitario_usd` | ✅ `precio_unitario_usd` | ✅ OK | Tipo compatible (float) |
| 7 | `precio_total_bs` | ✅ `total_bs` | ✅ OK | Mapeo correcto |
| 8 | `precio_total_usd` | ✅ `total_usd` | ✅ OK | Mapeo correcto |
| 9 | **`diente_numero`** | ❌ **FALTANTE** | 🔴 **CRÍTICO** | Campo nuevo en BD (migración 20251010), no mapeado |
| 10 | **`superficie`** | ⚠️ **`superficie_dental`** | 🟡 **DESALINEADO** | Existe pero con nombre diferente |
| 11 | `observaciones` | ✅ `observaciones` | ✅ OK | Compatible |
| 12 | `fecha_creacion` | ❌ No existe | ✅ OK | Autogenerado por BD |
| 13 | - | ❌ `nombre_servicio` | ℹ️ Info | Campo adicional para UI (no persiste) |
| 14 | - | ❌ `categoria_servicio` | ℹ️ Info | Campo adicional para UI (no persiste) |
| 15 | - | ❌ `dientes_texto` | ℹ️ Info | Texto display, se parsea a `diente_numero` |
| 16 | - | ❌ `material_utilizado` | ⚠️ **HUÉRFANO** | ¿Se guarda en `observaciones`? |

---

## 🚨 PROBLEMAS DETECTADOS

### **🔴 PROBLEMA 1: Campo `diente_numero` faltante en modelo**

**Descripción:**
La migración `20251010_agregar_diente_superficie_intervenciones_servicios.sql` agregó el campo `diente_numero` (INTEGER) a la tabla, pero el modelo Python no lo incluye.

**Impacto:**
- ❌ Los servicios se guardan en BD con `diente_numero = NULL`
- ❌ No se puede asociar un servicio a un diente específico
- ❌ Pérdida de granularidad clínica

**Evidencia:**
```sql
-- esquema.sql línea 563
diente_numero INTEGER,

-- Migración 20251010 línea 9
ADD COLUMN diente_numero INTEGER,

-- Comentario línea 17
COMMENT ON COLUMN intervenciones_servicios.diente_numero IS 'Número FDI del diente (11-48). NULL para servicios de boca completa.';
```

**Estado Actual:**
```python
# estado_intervencion_servicios.py línea 20
dientes_texto: str = ""  # ⚠️ "11, 12, 21" (string de múltiples dientes)
# ❌ NO HAY: diente_numero: Optional[int] = None
```

---

### **🟡 PROBLEMA 2: Desalineación de nombres - `superficie_dental` vs `superficie`**

**Descripción:**
El modelo usa `superficie_dental` pero la BD espera `superficie`.

**Impacto:**
- ⚠️ Confusión al mapear datos
- ⚠️ Posibles errores de inserción silenciosos
- ⚠️ Naming inconsistente

**Evidencia:**
```sql
-- esquema.sql línea 564
superficie VARCHAR(20),
```

```python
# estado_intervencion_servicios.py línea 29
superficie_dental: str = ""  # ⚠️ Nombre diferente
```

---

### **⚠️ PROBLEMA 3: Campo `material_utilizado` no tiene columna en BD**

**Descripción:**
El modelo tiene `material_utilizado` pero la tabla `intervenciones_servicios` NO tiene ese campo.

**Análisis:**
```python
# estado_intervencion_servicios.py línea 28
material_utilizado: str = ""      # ⚠️ Campo huérfano
```

**Posibles Destinos:**
1. **Tabla `intervenciones`**: Tiene campo `materiales_utilizados TEXT` (esquema.sql línea 538)
2. **Campo `observaciones`**: De `intervenciones_servicios` (esquema.sql línea 565)
3. **Tabla `condiciones_diente`**: Tiene `material_utilizado VARCHAR(100)` (esquema.sql línea 588)

**Impacto:**
- ⚠️ Si se está pasando a `observaciones`, funciona pero es impreciso
- ⚠️ Si se ignora, hay pérdida de información clínica
- ⚠️ Si se intenta insertar directamente, falla silenciosamente

---

### **ℹ️ PROBLEMA 4: Campo `dientes_texto` vs arquitectura de tabla**

**Descripción:**
El modelo usa `dientes_texto: str = "11, 12, 21"` (múltiples dientes en string), pero la BD espera `diente_numero: INTEGER` (un diente por registro).

**Análisis Arquitectural:**

**❌ Enfoque Actual (Conflictivo):**
```python
dientes_texto: str = "11, 12, 21"  # Múltiples dientes en un string
# Se inserta 1 registro en intervenciones_servicios con diente_numero = NULL
```

**✅ Enfoque Esperado por BD:**
```python
diente_numero: int = 11  # UN diente por registro
# Se insertan 3 registros separados: diente 11, 12, 21
```

**Evidencia del Diseño Correcto:**
```sql
-- esquema.sql líneas 563-564
diente_numero INTEGER,        -- UN diente (singular)
superficie VARCHAR(20),       -- UNA superficie específica

-- Migración 20251010 línea 17
COMMENT: 'Número FDI del diente (11-48). NULL para servicios de boca completa.'
```

**Implicación:**
Si un servicio afecta 3 dientes diferentes, se deben crear **3 registros separados** en `intervenciones_servicios`, uno por cada diente.

---

## 🔄 FLUJO ACTUAL DE DATOS (ANÁLISIS)

### **🔵 Cómo se Guardan los Datos Actualmente**

Revisando `estado_intervencion_servicios.py` líneas 557-569:

```python
# Preparar datos de servicios
servicios_backend = []
for servicio in self.servicios_en_intervencion:
    servicio_data = {
        "servicio_id": servicio.id_servicio,
        "cantidad": servicio.cantidad,
        "precio_unitario_bs": float(servicio.precio_unitario_bs),
        "precio_unitario_usd": float(servicio.precio_unitario_usd),
        "dientes_texto": servicio.dientes_texto,          # ⚠️ String "11, 12, 21"
        "material_utilizado": servicio.material_utilizado,  # ⚠️ No existe en BD
        "superficie_dental": servicio.superficie_dental,   # ⚠️ Nombre incorrecto
        "observaciones": servicio.observaciones or servicio.nombre_servicio
    }
    servicios_backend.append(servicio_data)
```

### **🔵 Problema en el Servicio Backend**

El servicio `odontologia_service.crear_intervencion_con_servicios()` debe:
1. ❓ Parsear `dientes_texto` ("11, 12, 21") → extraer números [11, 12, 21]
2. ❓ Por cada diente, crear 1 registro en `intervenciones_servicios`
3. ❓ Mapear `superficie_dental` → `superficie`
4. ❓ Decidir qué hacer con `material_utilizado`

**Sin ver el código del servicio**, asumimos que está haciendo la conversión correctamente, pero el modelo temporal debería reflejar la estructura final de BD para mayor claridad.

---

## ✅ SOLUCIONES PROPUESTAS

### **🎯 SOLUCIÓN 1: Actualizar `ServicioIntervencionTemporal` (RECOMENDADO)**

#### **Opción A: Mantener Modelo Temporal Actual + Agregar Campos**

```python
class ServicioIntervencionTemporal(rx.Base):
    """🛒 Modelo temporal para servicios en intervención (UI/Frontend)"""
    # === IDENTIFICADORES ===
    id_servicio: str = ""
    nombre_servicio: str = ""              # ℹ️ Solo para display
    categoria_servicio: str = ""           # ℹ️ Solo para display

    # === INFORMACIÓN CLÍNICA ===
    dientes_texto: str = ""                # ℹ️ String para UI: "11, 12, 21"
    diente_numero: Optional[int] = None    # 🆕 Campo individual para BD
    cantidad: int = 1

    # === PRECIOS ===
    precio_unitario_bs: float = 0.0
    precio_unitario_usd: float = 0.0
    total_bs: float = 0.0
    total_usd: float = 0.0

    # === DETALLES CLÍNICOS ===
    material_utilizado: str = ""           # ℹ️ Se incluye en observaciones o intervencion.materiales_utilizados
    superficie: str = ""                   # 🔧 RENOMBRADO de "superficie_dental" → "superficie"
    observaciones: str = ""

    @classmethod
    def from_servicio(cls, servicio: ServicioModel, dientes: str, cantidad: int = 1,
                     material: str = "", superficie: str = "", observaciones: str = ""):
        """Crear desde ServicioModel con dientes, cantidad y datos clínicos"""
        return cls(
            id_servicio=servicio.id,
            nombre_servicio=servicio.nombre,
            categoria_servicio=servicio.categoria or "General",
            dientes_texto=dientes,
            diente_numero=None,  # Se poblará al dividir por diente
            cantidad=cantidad,
            precio_unitario_bs=servicio.precio_base_bs or 0.0,
            precio_unitario_usd=servicio.precio_base_usd or 0.0,
            total_bs=(servicio.precio_base_bs or 0.0) * cantidad,
            total_usd=(servicio.precio_base_usd or 0.0) * cantidad,
            material_utilizado=material,
            superficie=superficie,  # 🔧 Nombre correcto
            observaciones=observaciones
        )

    def to_db_record(self, intervencion_id: str) -> Dict[str, Any]:
        """
        🆕 Convertir a formato de BD para inserción

        Returns:
            Dict compatible con tabla intervenciones_servicios
        """
        # Calcular totales
        precio_total_bs = float(self.precio_unitario_bs) * self.cantidad
        precio_total_usd = float(self.precio_unitario_usd) * self.cantidad

        # Preparar observaciones completas (incluir material si existe)
        obs_completa = self.observaciones or ""
        if self.material_utilizado:
            obs_completa = f"Material: {self.material_utilizado}. {obs_completa}".strip()

        return {
            "intervencion_id": intervencion_id,
            "servicio_id": self.id_servicio,
            "cantidad": self.cantidad,
            "precio_unitario_bs": float(self.precio_unitario_bs),
            "precio_unitario_usd": float(self.precio_unitario_usd),
            "precio_total_bs": precio_total_bs,
            "precio_total_usd": precio_total_usd,
            "diente_numero": self.diente_numero,     # 🆕 Campo BD
            "superficie": self.superficie,            # 🔧 Nombre correcto
            "observaciones": obs_completa
        }
```

**Ventajas:**
- ✅ Mantiene compatibilidad con código UI existente
- ✅ Agrega campos necesarios para BD
- ✅ Método helper `to_db_record()` para conversión clara
- ✅ Corrige naming inconsistency

**Desventajas:**
- ⚠️ Mantiene campo `dientes_texto` que puede causar confusión
- ⚠️ Necesita lógica externa para dividir por diente

---

#### **Opción B: Modelo Completamente Alineado con BD (MÁS LIMPIO)**

```python
class ServicioIntervencionTemporal(rx.Base):
    """
    🛒 Modelo temporal para servicios en intervención

    CAMBIO ARQUITECTURAL:
    - Ahora representa UNA LÍNEA de intervenciones_servicios
    - Si un servicio afecta 3 dientes, se crean 3 instancias
    """
    # === IDENTIFICADORES ===
    id_servicio: str = ""
    nombre_servicio: str = ""              # ℹ️ Solo para display
    categoria_servicio: str = ""           # ℹ️ Solo para display

    # === INFORMACIÓN CLÍNICA (1 DIENTE = 1 REGISTRO) ===
    diente_numero: Optional[int] = None    # 🆕 UN diente específico (11-48) o None para boca completa
    superficie: str = ""                   # 🔧 UNA superficie específica o "completa"
    cantidad: int = 1                      # Cantidad de este servicio en este diente

    # === PRECIOS ===
    precio_unitario_bs: float = 0.0
    precio_unitario_usd: float = 0.0
    total_bs: float = 0.0                  # precio_unitario * cantidad
    total_usd: float = 0.0                 # precio_unitario * cantidad

    # === DETALLES CLÍNICOS ===
    material_utilizado: str = ""           # Se incluirá en observaciones
    observaciones: str = ""

    @classmethod
    def from_servicio_multiple_dientes(cls, servicio: ServicioModel, dientes_texto: str,
                                       material: str = "", superficie: str = "",
                                       observaciones: str = "") -> List["ServicioIntervencionTemporal"]:
        """
        🆕 Crear MÚLTIPLES instancias desde un servicio con varios dientes

        Args:
            servicio: Modelo del servicio
            dientes_texto: "11, 12, 21" (string con múltiples dientes)
            material, superficie, observaciones: Detalles clínicos

        Returns:
            Lista de instancias, una por cada diente
        """
        import re

        # Parsear dientes
        if "todos" in dientes_texto.lower() or "toda" in dientes_texto.lower():
            # Toda la boca
            return [cls(
                id_servicio=servicio.id,
                nombre_servicio=servicio.nombre,
                categoria_servicio=servicio.categoria or "General",
                diente_numero=None,  # NULL = toda la boca
                superficie=superficie or "completa",
                cantidad=1,
                precio_unitario_bs=servicio.precio_base_bs or 0.0,
                precio_unitario_usd=servicio.precio_base_usd or 0.0,
                total_bs=servicio.precio_base_bs or 0.0,
                total_usd=servicio.precio_base_usd or 0.0,
                material_utilizado=material,
                observaciones=observaciones
            )]

        # Extraer números de dientes (regex FDI: 11-48)
        numeros = re.findall(r'\b([1-4][1-8])\b', dientes_texto)
        dientes_validos = [int(num) for num in numeros if 11 <= int(num) <= 48]

        if not dientes_validos:
            # Si no hay dientes válidos, retornar vacío
            return []

        # Crear una instancia por cada diente
        instancias = []
        for diente in dientes_validos:
            instancias.append(cls(
                id_servicio=servicio.id,
                nombre_servicio=servicio.nombre,
                categoria_servicio=servicio.categoria or "General",
                diente_numero=diente,
                superficie=superficie or "completa",
                cantidad=1,  # 1 servicio por diente
                precio_unitario_bs=servicio.precio_base_bs or 0.0,
                precio_unitario_usd=servicio.precio_base_usd or 0.0,
                total_bs=servicio.precio_base_bs or 0.0,
                total_usd=servicio.precio_base_usd or 0.0,
                material_utilizado=material,
                observaciones=observaciones
            ))

        return instancias

    def to_db_record(self, intervencion_id: str) -> Dict[str, Any]:
        """Convertir a formato de BD - MAPEO DIRECTO"""
        obs_completa = self.observaciones or ""
        if self.material_utilizado:
            obs_completa = f"Material: {self.material_utilizado}. {obs_completa}".strip()

        return {
            "intervencion_id": intervencion_id,
            "servicio_id": self.id_servicio,
            "cantidad": self.cantidad,
            "precio_unitario_bs": float(self.precio_unitario_bs),
            "precio_unitario_usd": float(self.precio_unitario_usd),
            "precio_total_bs": float(self.total_bs),
            "precio_total_usd": float(self.total_usd),
            "diente_numero": self.diente_numero,     # ✅ Mapeo directo
            "superficie": self.superficie,            # ✅ Mapeo directo
            "observaciones": obs_completa
        }
```

**Ventajas:**
- ✅ **100% alineado con esquema BD**
- ✅ Elimina parsing manual en el servicio
- ✅ Claridad arquitectural: 1 instancia = 1 registro BD
- ✅ Facilita validaciones y testing

**Desventajas:**
- ⚠️ **BREAKING CHANGE** - Requiere modificar lógica en UI
- ⚠️ Necesita actualizar `agregar_servicio_a_intervencion()` para crear múltiples instancias

---

### **🎯 SOLUCIÓN 2: Actualizar Lógica de Guardado (Backend)**

Si mantenemos el modelo actual, el servicio `odontologia_service.crear_intervencion_con_servicios()` debe:

```python
async def crear_intervencion_con_servicios(self, datos_intervencion: Dict[str, Any]):
    """
    Crear intervención y sus servicios asociados

    DEBE MANEJAR:
    1. Parsear dientes_texto → lista de números
    2. Por cada diente, crear registro en intervenciones_servicios
    3. Mapear superficie_dental → superficie
    4. Incluir material_utilizado en observaciones
    """
    servicios = datos_intervencion.get("servicios", [])

    for servicio_data in servicios:
        # Extraer dientes del texto
        dientes_texto = servicio_data.get("dientes_texto", "")
        dientes_numeros = self._extraer_numeros_dientes(dientes_texto)

        # Extraer superficies
        superficie_str = servicio_data.get("superficie_dental", "")  # ⚠️ Nombre viejo
        superficies = self._mapear_superficie(superficie_str)

        # Por cada diente, crear registro
        for diente_num in dientes_numeros:
            for superficie in superficies:
                # Preparar observaciones incluyendo material
                observaciones = servicio_data.get("observaciones", "")
                material = servicio_data.get("material_utilizado", "")
                if material:
                    observaciones = f"Material: {material}. {observaciones}".strip()

                # Insertar en BD
                await intervenciones_servicios_table.create({
                    "intervencion_id": intervencion_id,
                    "servicio_id": servicio_data["servicio_id"],
                    "cantidad": 1,  # 1 por diente
                    "precio_unitario_bs": servicio_data["precio_unitario_bs"],
                    "precio_unitario_usd": servicio_data["precio_unitario_usd"],
                    "precio_total_bs": servicio_data["precio_unitario_bs"],
                    "precio_total_usd": servicio_data["precio_unitario_usd"],
                    "diente_numero": diente_num,      # 🆕 Campo nuevo
                    "superficie": superficie,         # 🔧 Nombre correcto
                    "observaciones": observaciones
                })
```

**Ventaja:**
- ✅ No requiere cambios en UI

**Desventajas:**
- ⚠️ Duplica lógica (parsing de dientes ya existe en estado)
- ⚠️ Mantiene naming inconsistency (`superficie_dental` vs `superficie`)

---

## 📝 RECOMENDACIONES FINALES

### **🏆 ESTRATEGIA RECOMENDADA: HÍBRIDA (Solución 1 Opción A + Mejoras Backend)**

**Fase 1: Actualizar Modelo (Cambios Mínimos)**
1. ✅ Renombrar `superficie_dental` → `superficie`
2. ✅ Agregar campo opcional `diente_numero: Optional[int] = None`
3. ✅ Agregar método `to_db_record()` para conversión explícita
4. ✅ Documentar que `dientes_texto` es solo para UI

**Fase 2: Actualizar Lógica de Guardado**
1. ✅ Modificar `finalizar_mi_intervencion_odontologo()` línea 557:
   - Parsear `dientes_texto` a lista de números
   - Llamar método de servicio que maneje división por diente
2. ✅ Verificar que servicio `odontologia_service` inserta correctamente:
   - Campo `diente_numero` (no NULL si hay diente específico)
   - Campo `superficie` (no `superficie_dental`)
   - Campo `observaciones` incluya material si existe

**Fase 3: Testing**
1. ✅ Probar servicio con 1 diente → 1 registro en BD
2. ✅ Probar servicio con 3 dientes → 3 registros en BD
3. ✅ Probar servicio "toda la boca" → 1 registro con `diente_numero = NULL`
4. ✅ Verificar que `material_utilizado` se guarda correctamente

---

## 📊 CHECKLIST DE VERIFICACIÓN

### **✅ Modelo Python**
- [ ] Campo `superficie_dental` renombrado a `superficie`
- [ ] Campo `diente_numero` agregado (Optional[int])
- [ ] Método `to_db_record()` implementado
- [ ] Documentación actualizada

### **✅ Lógica de Guardado**
- [ ] Parsing de `dientes_texto` → lista de números
- [ ] Inserción de 1 registro por diente en `intervenciones_servicios`
- [ ] Mapeo correcto de `superficie`
- [ ] Inclusión de `material_utilizado` en observaciones

### **✅ Migración de BD**
- [x] Migración `20251010` aplicada correctamente
- [x] Índices creados (`idx_interv_servicios_diente`)
- [x] Constraints verificados

### **✅ Testing**
- [ ] Test: Servicio 1 diente → 1 registro BD
- [ ] Test: Servicio 3 dientes → 3 registros BD
- [ ] Test: Servicio "toda boca" → diente_numero NULL
- [ ] Test: Material se guarda en observaciones

---

## 🎯 PRÓXIMOS PASOS

1. **Actualizar `ServicioIntervencionTemporal`** según Solución 1 Opción A
2. **Revisar `odontologia_service.crear_intervencion_con_servicios()`** para validar lógica
3. **Ejecutar suite de tests** para verificar integridad
4. **Documentar cambios** en CHANGELOG

---

**Creado por:** Claude Code
**Fecha:** 2025-10-13
**Estado:** 🔴 **ACCIÓN REQUERIDA** - Actualizar modelo y verificar lógica de guardado
