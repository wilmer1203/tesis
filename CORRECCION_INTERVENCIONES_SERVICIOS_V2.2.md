# CORRECCIÓN V2.2: CREACIÓN DE INTERVENCIONES POR SERVICIO

**Fecha:** 2025-10-20
**Versión:** 2.2
**Estado:** ✅ IMPLEMENTADO

---

## 🔴 PROBLEMA IDENTIFICADO

### Comportamiento Incorrecto (ANTES):

La función `crear_intervencion_con_servicios` estaba creando múltiples registros innecesarios en `intervenciones_servicios`:

1. **Blanqueamiento (boca completa):** Creaba **160 registros** (32 dientes × 5 superficies)
2. **Obturación (diente completo):** Creaba **5 registros** (5 superficies del diente)
3. **Campo `dientes_afectados`:** Mostraba todos los 32 dientes incorrectamente

### Causa Raíz:

1. El campo `alcance` no se transmitía del frontend al backend
2. Función `_mapear_superficie()` expandía "completa" → TODAS las superficies
3. Lógica de inserción iteraba todas las superficies sin validar el alcance
4. Cálculo de `dientes_afectados` incluía 32 dientes para "toda la boca"

---

## ✅ SOLUCIÓN IMPLEMENTADA

### Cambios Realizados:

#### 1. **Frontend: Transmitir campo `alcance`**

**Archivo:** `dental_system/state/estado_intervencion_servicios.py` (líneas 360-443)

**Cambios:**
- Agregado campo `alcance` en conversión de servicios
- Ajustada conversión de `dientes_texto` y `superficie_str` según alcance:
  - `boca_completa`: `dientes_texto=""`, `superficie_str=None`
  - `diente_completo`: `dientes_texto="diente"`, `superficie_str=None`
  - `superficie_especifica`: `dientes_texto="diente"`, `superficie_str="oclusal"`

```python
# ANTES (incorrecto)
superficie_str = ", ".join(servicio.superficies) if servicio.superficies else "completa"

# DESPUÉS (correcto)
if servicio.alcance == "boca_completa":
    dientes_texto = ""
    superficie_str = None
elif servicio.alcance == "diente_completo":
    dientes_texto = str(servicio.diente_numero)
    superficie_str = None
else:  # superficie_especifica
    dientes_texto = str(servicio.diente_numero)
    superficie_str = ", ".join(servicio.superficies) if servicio.superficies else None
```

---

#### 2. **Backend: Nuevo método `_mapear_superficie_especifica`**

**Archivo:** `dental_system/services/odontologia_service.py` (líneas 777-815)

**Diferencia con `_mapear_superficie` antiguo:**
- NO expande "completa" a todas las superficies
- Retorna lista vacía `[]` para valores nulos (en vez de `SUPERFICIES`)
- Pensado para usar con campo `alcance` explícito

```python
def _mapear_superficie_especifica(self, superficie_str: str) -> List[str]:
    """
    Mapear SOLO superficies específicas (sin expansión automática)
    """
    if not superficie_str:
        return []  # Vacío en vez de SUPERFICIES

    # Mapeo ESTRICTO (sin "completa")
    mapeo_simple = {
        "oclusal": ["oclusal"],
        "mesial": ["mesial"],
        # ...
    }

    # Si es combinación "oclusal, mesial"
    if "," in superficie_str:
        return [s.strip() for s in superficie_str.split(",")]

    return mapeo_simple.get(superficie_lower, [])
```

---

#### 3. **Backend: Lógica con 3 branches por alcance**

**Archivo:** `dental_system/services/odontologia_service.py` (líneas 618-746)

**Estructura reescrita:**

```python
for servicio in servicios:
    alcance = servicio.get("alcance", "superficie_especifica")

    # ESCENARIO 1: BOCA COMPLETA
    if alcance == "boca_completa":
        # UN SOLO REGISTRO con diente_numero=NULL, superficie=NULL
        registro = {
            "diente_numero": None,
            "superficie": None,
            # ...
        }
        insert(registro)

    # ESCENARIO 2: DIENTE COMPLETO
    elif alcance == "diente_completo":
        # UN REGISTRO por diente con superficie=NULL
        for diente_num in dientes_servicio:
            registro = {
                "diente_numero": diente_num,
                "superficie": None,
                # ...
            }
            insert(registro)

    # ESCENARIO 3: SUPERFICIE ESPECÍFICA
    else:  # superficie_especifica
        # UN REGISTRO por combinación diente+superficie
        superficies = self._mapear_superficie_especifica(superficie_str)
        for diente_num in dientes_servicio:
            for superficie in superficies:
                registro = {
                    "diente_numero": diente_num,
                    "superficie": superficie,
                    # ...
                }
                insert(registro)
```

---

#### 4. **Backend: Cálculo correcto de `dientes_afectados`**

**Archivo:** `dental_system/services/odontologia_service.py` (líneas 577-605)

**Lógica corregida:**

```python
dientes_todos = []
tiene_boca_completa = False

for servicio in servicios:
    alcance = servicio.get("alcance", "superficie_especifica")

    # Detectar boca completa
    if alcance == "boca_completa":
        tiene_boca_completa = True
        continue  # No agregar dientes individuales

    # Agregar dientes específicos
    dientes_todos.extend(dientes_servicio)

# Determinar valor final
if tiene_boca_completa:
    dientes_unicos = None  # NULL = boca completa
else:
    dientes_unicos = sorted(list(set(dientes_todos)))
```

---

## 📊 IMPACTO DE LA CORRECCIÓN

### Comportamiento ANTES vs DESPUÉS:

| Servicio | Alcance | Registros ANTES | Registros DESPUÉS | `dientes_afectados` ANTES | `dientes_afectados` DESPUÉS |
|----------|---------|-----------------|-------------------|---------------------------|------------------------------|
| Blanqueamiento | boca_completa | **160** | **1** (NULL, NULL) | [11,12,...,48] (32) | **NULL** |
| Obturación diente 11 | diente_completo | **5** | **1** (11, NULL) | [11] | [11] |
| Caries 21-oclusal | superficie_especifica | 1 | 1 (21, oclusal) | [21] | [21] |

### Mejoras:

✅ **Reducción masiva de registros** innecesarios (160 → 1 para blanqueamiento)
✅ **Integridad semántica** correcta en base de datos
✅ **Campo `dientes_afectados`** refleja la realidad del tratamiento
✅ **Queries más rápidas** (menos registros a procesar)
✅ **Reportes correctos** por tipo de servicio

---

## 🧪 VALIDACIÓN DE LA CORRECCIÓN

### Test 1: BOCA COMPLETA (Blanqueamiento)

**Datos de entrada:**
```python
{
    "servicio_id": "SER014",
    "alcance": "boca_completa",
    "dientes_texto": "",
    "superficie": None
}
```

**Resultado esperado:**
```sql
-- 1 registro en intervenciones_servicios
SELECT * FROM intervenciones_servicios WHERE intervencion_id = '...';
-- diente_numero: NULL
-- superficie: NULL

-- dientes_afectados en intervención
SELECT dientes_afectados FROM intervenciones WHERE id = '...';
-- dientes_afectados: NULL
```

---

### Test 2: DIENTE COMPLETO (Obturación diente 11)

**Datos de entrada:**
```python
{
    "servicio_id": "SER003",
    "alcance": "diente_completo",
    "dientes_texto": "11",
    "superficie": None
}
```

**Resultado esperado:**
```sql
-- 1 registro en intervenciones_servicios
SELECT * FROM intervenciones_servicios WHERE intervencion_id = '...';
-- diente_numero: 11
-- superficie: NULL

-- dientes_afectados en intervención
SELECT dientes_afectados FROM intervenciones WHERE id = '...';
-- dientes_afectados: [11]
```

---

### Test 3: SUPERFICIE ESPECÍFICA (Caries 21-oclusal)

**Datos de entrada:**
```python
{
    "servicio_id": "SER002",
    "alcance": "superficie_especifica",
    "dientes_texto": "21",
    "superficie": "oclusal"
}
```

**Resultado esperado:**
```sql
-- 1 registro en intervenciones_servicios
SELECT * FROM intervenciones_servicios WHERE intervencion_id = '...';
-- diente_numero: 21
-- superficie: 'oclusal'

-- dientes_afectados en intervención
SELECT dientes_afectados FROM intervenciones WHERE id = '...';
-- dientes_afectados: [21]
```

---

### Test 4: MIXTO (Limpieza + Obturación)

**Datos de entrada:**
```python
[
    {
        "servicio_id": "SER001",
        "alcance": "boca_completa",  # Limpieza
        "dientes_texto": "",
        "superficie": None
    },
    {
        "servicio_id": "SER003",
        "alcance": "diente_completo",  # Obturación diente 11
        "dientes_texto": "11",
        "superficie": None
    }
]
```

**Resultado esperado:**
```sql
-- 2 registros en intervenciones_servicios
SELECT * FROM intervenciones_servicios WHERE intervencion_id = '...';
-- Registro 1: NULL, NULL (limpieza)
-- Registro 2: 11, NULL (obturación)

-- dientes_afectados en intervención (NULL porque tiene boca_completa)
SELECT dientes_afectados FROM intervenciones WHERE id = '...';
-- dientes_afectados: NULL
```

---

## 📋 ARCHIVOS MODIFICADOS

1. **`dental_system/state/estado_intervencion_servicios.py`**
   - Líneas 360-443: Conversión con campo `alcance`

2. **`dental_system/services/odontologia_service.py`**
   - Líneas 777-815: Nuevo método `_mapear_superficie_especifica()`
   - Líneas 618-746: Lógica con 3 branches por alcance
   - Líneas 577-605: Cálculo correcto de `dientes_afectados`

---

## ✅ CHECKLIST DE VALIDACIÓN EN PRODUCCIÓN

Para validar la corrección en el sistema real:

- [ ] Crear intervención con servicio de **boca completa** (ej: Blanqueamiento)
  - [ ] Verificar 1 solo registro en `intervenciones_servicios`
  - [ ] Verificar `diente_numero` = NULL
  - [ ] Verificar `superficie` = NULL
  - [ ] Verificar `dientes_afectados` en `intervenciones` = NULL

- [ ] Crear intervención con servicio de **diente completo** (ej: Obturación diente 11)
  - [ ] Verificar 1 registro por diente
  - [ ] Verificar `diente_numero` = 11
  - [ ] Verificar `superficie` = NULL
  - [ ] Verificar `dientes_afectados` = [11]

- [ ] Crear intervención con servicio de **superficie específica** (ej: Caries 21-oclusal)
  - [ ] Verificar 1 registro
  - [ ] Verificar `diente_numero` = 21
  - [ ] Verificar `superficie` = 'oclusal'
  - [ ] Verificar `dientes_afectados` = [21]

- [ ] Crear intervención **mixta** (limpieza + obturación)
  - [ ] Verificar registros correctos por cada servicio
  - [ ] Verificar `dientes_afectados` = NULL (por la limpieza de boca completa)

---

## 🎯 CONCLUSIÓN

✅ **Corrección implementada exitosamente**

La lógica ahora diferencia correctamente los 3 tipos de alcance:
1. **Boca completa** → 1 registro con ambos campos NULL
2. **Diente completo** → 1 registro por diente con superficie NULL
3. **Superficie específica** → N registros con ambos campos llenos

El sistema ahora crea la cantidad correcta de registros en `intervenciones_servicios` y calcula correctamente el campo `dientes_afectados` en la tabla `intervenciones`.

**Impacto:** Reducción de hasta 99.4% en registros innecesarios (160 → 1) y datos correctos para reportes.

---

**Implementado por:** Claude Code
**Fecha:** 2025-10-20
**Versión:** V2.2
