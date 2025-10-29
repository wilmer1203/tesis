# 🔍 ANÁLISIS COMPLETO: FLUJO "FINALIZAR INTERVENCIÓN"
## Sistema Odontológico - Dental System

**Fecha:** 2025-10-10
**Propósito:** Documentar todos los caminos, funciones y variables involucradas al hacer clic en "Finalizar Intervención"

---

## 📊 FLUJO PRINCIPAL COMPLETO

```
USUARIO HACE CLIC EN "FINALIZAR INTERVENCIÓN"
         ↓
guardar_intervencion_completa()
         ↓
[VALIDACIONES PREVIAS]
         ↓
[PASO 1] Crear intervención en BD
         ↓
[PASO 2] Guardar servicios detallados
         ↓
[PASO 3] Actualizar odontograma (si hay cambios)
         ↓
[PASO 4] Cambiar estado consulta
         ↓
[PASO 5] Limpiar estado local
         ↓
[PASO 6] Navegar a lista pacientes
```

---

## 🎯 FUNCIÓN PRINCIPAL

### **`guardar_intervencion_completa()`**
**Archivo:** `dental_system/state/estado_odontologia.py`
**Línea:** 3138
**Trigger:** Click en botón "Finalizar Intervención" (componente UI)

---

## ✅ VALIDACIONES PREVIAS (Líneas 3149-3158)

### **Validación 1: Servicios no vacíos**
```python
if not self.servicios_consulta_actual:
    self.mostrar_toast("⚠️ No hay servicios para guardar", "warning")
    return
```
**Variables usadas:**
- `self.servicios_consulta_actual` (List[Dict]) - Lista de servicios agregados

**¿Cuándo se llena?**
- Método: `agregar_servicio_a_intervencion()` (línea 3920)
- Cada vez que el odontólogo agrega un servicio desde el modal

### **Validación 2: Consulta activa válida**
```python
if not self.consulta_actual or not self.consulta_actual.id:
    self.mostrar_toast("❌ No hay consulta activa", "error")
    return
```
**Variables usadas:**
- `self.consulta_actual` (ConsultaModel) - Consulta siendo atendida

**¿Cuándo se llena?**
- Método: `navegar_a_intervencion()` cuando odontólogo selecciona paciente de su cola

---

## 📝 PASO 1: CREAR INTERVENCIÓN (Líneas 3172-3198)

### **1.1 Preparar datos de intervención**
```python
# Calcular totales
total_bs = sum(float(s.get("costo_bs", 0)) for s in self.servicios_consulta_actual)
total_usd = sum(float(s.get("costo_usd", 0)) for s in self.servicios_consulta_actual)

# Extraer dientes únicos tratados
dientes_afectados = list(set([s.get("diente") for s in self.servicios_consulta_actual if s.get("diente")]))

# Preparar descripción del tratamiento
tratamiento_desc = "\n".join([
    f"- Diente {s.get('diente')}: {s.get('servicio')} en {', '.join(s.get('superficies', []))} - Obs: {s.get('observaciones', 'N/A')}"
    for s in self.servicios_consulta_actual
])
```

**Variables calculadas:**
- `total_bs` (float) - Suma de todos los servicios en bolívares
- `total_usd` (float) - Suma de todos los servicios en dólares
- `dientes_afectados` (List[int]) - Lista de números FDI únicos
- `tratamiento_desc` (str) - Descripción textual del tratamiento

### **1.2 Crear registro en tabla `intervenciones`**
```python
nueva_intervencion = interventions_table.create({
    "consulta_id": self.consulta_actual.id,
    "odontologo_id": personal_id,
    "hora_inicio": datetime.now().isoformat(),
    "hora_fin": datetime.now().isoformat(),
    "procedimiento_realizado": tratamiento_desc,
    "dientes_afectados": dientes_afectados,
    "total_bs": float(total_bs),
    "total_usd": float(total_usd),
    "estado": "completada"
})

intervencion_id = nueva_intervencion.get("id")
```

**Tabla BD:** `intervenciones`
**Columnas usadas:**
- `consulta_id` (UUID) - FK a consultas
- `odontologo_id` (UUID) - FK a personal (ID del odontólogo)
- `hora_inicio` (TIMESTAMPTZ) - Momento de inicio (actual)
- `hora_fin` (TIMESTAMPTZ) - Momento de fin (actual)
- `procedimiento_realizado` (TEXT) - Descripción textual
- `dientes_afectados` (INTEGER[]) - Array de números FDI
- `total_bs` (NUMERIC) - Total en bolívares
- `total_usd` (NUMERIC) - Total en dólares
- `estado` (VARCHAR) - Siempre "completada"

**Variables generadas:**
- `intervencion_id` (UUID) - ID de la intervención creada

---

## 🦷 PASO 2: GUARDAR SERVICIOS DETALLADOS (Líneas 3200-3241)

### **2.1 Iterar sobre servicios agregados**
```python
for servicio_data in self.servicios_consulta_actual:
    diente_num = servicio_data.get("diente") if servicio_data.get("diente") else None
    superficies = servicio_data.get("superficies", [])
```

**Estructura de `servicio_data` (Dict):**
```python
{
    "id": "uuid-temp",
    "servicio": "Limpieza Dental",
    "servicio_id": "4e736b8e-...",  # ✅ ID real del servicio
    "costo_bs": 1825.0,
    "costo_usd": 50.0,
    "observaciones": "zzzzz",
    "alcance": "boca_completa",  # o "superficie_especifica" o "diente_completo"
    "diente": None,  # o número FDI (11-48)
    "superficies": []  # o ["Oclusal", "Mesial", ...]
}
```

### **2.2 Guardar en tabla `intervenciones_servicios`**

**CASO A: Servicio con superficies específicas (líneas 3211-3225)**
```python
if superficies and len(superficies) > 0:
    # Crear UN REGISTRO por cada superficie
    for superficie in superficies:
        intervenciones_servicios_table.create({
            "intervencion_id": intervencion_id,
            "servicio_id": servicio_data.get("servicio_id"),
            "cantidad": 1,
            "precio_unitario_bs": float(servicio_data.get("costo_bs", 0)),
            "precio_unitario_usd": float(servicio_data.get("costo_usd", 0)),
            "precio_total_bs": float(servicio_data.get("costo_bs", 0)),
            "precio_total_usd": float(servicio_data.get("costo_usd", 0)),
            "diente_numero": diente_num,
            "superficie": superficie.lower(),  # "oclusal", "mesial", etc.
            "observaciones_servicio": servicio_data.get("observaciones", "")
        })
```

**Ejemplo:** Obturación en diente 18, superficies Oclusal y Mesial → 2 registros

**CASO B: Servicio de boca completa (líneas 3226-3239)**
```python
else:
    # Crear UN SOLO REGISTRO sin diente ni superficie
    intervenciones_servicios_table.create({
        "intervencion_id": intervencion_id,
        "servicio_id": servicio_data.get("servicio_id"),
        "cantidad": 1,
        "precio_unitario_bs": float(servicio_data.get("costo_bs", 0)),
        "precio_unitario_usd": float(servicio_data.get("costo_usd", 0)),
        "precio_total_bs": float(servicio_data.get("costo_bs", 0)),
        "precio_total_usd": float(servicio_data.get("costo_usd", 0)),
        "diente_numero": None,  # ✅ NULL para boca completa
        "superficie": None,     # ✅ NULL para boca completa
        "observaciones_servicio": servicio_data.get("observaciones", "Servicio aplicado a boca completa")
    })
```

**Ejemplo:** Limpieza Dental (boca completa) → 1 registro con diente y superficie NULL

**Tabla BD:** `intervenciones_servicios`
**Columnas usadas:**
- `intervencion_id` (UUID) - FK a intervenciones
- `servicio_id` (UUID) - FK a servicios
- `cantidad` (INTEGER) - Siempre 1 por ahora
- `precio_unitario_bs` (NUMERIC) - Precio por unidad en BS
- `precio_unitario_usd` (NUMERIC) - Precio por unidad en USD
- `precio_total_bs` (NUMERIC) - Total en BS (cantidad × unitario)
- `precio_total_usd` (NUMERIC) - Total en USD (cantidad × unitario)
- `diente_numero` (INTEGER) - Número FDI o NULL
- `superficie` (VARCHAR) - Nombre superficie o NULL
- `observaciones_servicio` (TEXT) - Observaciones

---

## 🦷 PASO 3: ACTUALIZAR ODONTOGRAMA (Líneas 3243-3284)

### **3.1 Verificar si hay cambios pendientes**
```python
if self.cambios_pendientes_odontograma and len(self.cambios_pendientes_odontograma) > 0:
    # Hay cambios → actualizar
else:
    logger.info("ℹ️ No hay cambios en el odontograma para actualizar")
    # Saltar actualización
```

**Variable clave:** `self.cambios_pendientes_odontograma`

**Estructura:**
```python
{
    18: {  # Número FDI del diente
        "oclusal": "caries",      # Superficie: nueva condición
        "mesial": "obturacion"
    },
    25: {
        "distal": "sano"
    }
}
```

**¿Cuándo se llena?**
- Método: `agregar_servicio_a_intervencion()` (líneas 3924-3941)
- SOLO cuando odontólogo marca checkbox "Cambiar condición automáticamente"
- Y el alcance NO es "boca_completa"

**IMPORTANTE:**
- `self.condiciones_por_diente` → Odontograma COMPLETO actual (32 dientes × 5 superficies = 160)
- `self.cambios_pendientes_odontograma` → SOLO dientes/superficies modificados

### **3.2 Actualizar cada condición cambiada**
```python
for diente_num, condiciones in self.cambios_pendientes_odontograma.items():
    for superficie, condicion in condiciones.items():
        # PASO 3.2.1: Desactivar condición anterior
        response_anteriores = odontologia_service.client.table("condiciones_diente").select("id")
            .eq("paciente_id", self.paciente_actual.id)
            .eq("diente_numero", int(diente_num))
            .eq("superficie", superficie.lower())
            .eq("activo", True).execute()

        for cond_anterior in response_anteriores.data:
            condiciones_table.update(cond_anterior['id'], {"activo": False})

        # PASO 3.2.2: Crear nueva condición activa
        condiciones_table.create({
            "paciente_id": self.paciente_actual.id,
            "diente_numero": int(diente_num),
            "superficie": superficie.lower(),
            "tipo_condicion": condicion,
            "intervencion_id": intervencion_id,
            "registrado_por": self.id_usuario,  # ✅ ID de tabla usuarios
            "descripcion": "Condición actualizada por intervención",
            "activo": True
        })
```

**Tabla BD:** `condiciones_diente`
**Columnas usadas:**
- `paciente_id` (UUID) - FK a pacientes
- `diente_numero` (INTEGER) - Número FDI (11-48)
- `superficie` (VARCHAR) - "oclusal", "mesial", "distal", "vestibular", "lingual"
- `tipo_condicion` (VARCHAR) - "sano", "caries", "obturacion", "corona", etc.
- `intervencion_id` (UUID) - FK a intervenciones
- `registrado_por` (UUID) - FK a **usuarios** (NO personal)
- `descripcion` (TEXT) - Descripción del cambio
- `activo` (BOOLEAN) - TRUE para actual, FALSE para histórico

**Patrón de historial:**
1. Buscar condición actual (activo = TRUE)
2. Desactivarla (activo = FALSE)
3. Crear nueva condición (activo = TRUE)

### **3.3 Limpiar cambios pendientes**
```python
self.cambios_pendientes_odontograma = {}
```

---

## 🔄 PASO 4: CAMBIAR ESTADO CONSULTA (Líneas 3310-3335)

### **4.1 Verificar si puede cambiar estado**
```python
estado_actual = self.consulta_actual.estado

if estado_actual and estado_actual not in ["completada", "cancelada"]:
    # Cambiar a "entre_odontologos"
else:
    # Saltar cambio (ya está en estado final)
```

**Estados posibles de consulta:**
- `programada` - En espera por orden de llegada
- `en_curso` - Siendo atendida por odontólogo
- `entre_odontologos` - Atendida por un odontólogo, disponible para otro
- `completada` - Finalizada completamente
- `cancelada` - Cancelada

### **4.2 Cambiar estado a "entre_odontologos"**
```python
await consultas_service.change_consultation_status(
    consultation_id=self.consulta_actual.id,
    nuevo_estado="entre_odontologos",
    notas=f"Intervención completada por odontólogo con {len(self.servicios_consulta_actual)} servicios"
)
```

**¿Por qué "entre_odontologos"?**
- Permite que OTRO odontólogo pueda atender al mismo paciente si es necesario
- Si no hay más odontólogos, administrador debe cambiar manualmente a "completada"

---

## 🧹 PASO 5: LIMPIAR ESTADO LOCAL (Líneas 3341-3346)

```python
self.servicios_consulta_actual = []
self.condiciones_por_diente = {}  # ⚠️ NOTA: Esto limpia la visualización
self.selected_tooth = None
self.show_add_intervention_modal = False
self.tiene_servicios_seleccionados = False
```

**Variables limpiadas:**
- `servicios_consulta_actual` - Lista de servicios agregados
- `condiciones_por_diente` - Odontograma completo cargado
- `selected_tooth` - Diente seleccionado en UI
- `show_add_intervention_modal` - Estado del modal
- `tiene_servicios_seleccionados` - Flag para habilitar botón "Finalizar"

---

## 🧭 PASO 6: NAVEGAR A LISTA (Líneas 3348-3355)

```python
self.mostrar_toast("✅ Intervención completada exitosamente", "success")

import asyncio
await asyncio.sleep(2)  # Esperar 2 segundos

self.navigate_to("odontologia", "Lista de Pacientes", "")
```

**Resultado:** Odontólogo vuelve a ver su cola de pacientes

---

## 🔍 ANÁLISIS DE VARIABLES CLAVE

### **Variable 1: `servicios_consulta_actual`**
**Tipo:** `List[Dict[str, Any]]`
**Cuándo se llena:** `agregar_servicio_a_intervencion()` (línea 3920)
**Cuándo se vacía:** Después de guardar intervención (línea 3342)
**Uso:** Acumulador temporal de servicios antes de guardar

### **Variable 2: `cambios_pendientes_odontograma`**
**Tipo:** `Dict[int, Dict[str, str]]`
**Cuándo se llena:** `agregar_servicio_a_intervencion()` (líneas 3924-3941) SI checkbox activo
**Cuándo se vacía:** Después de actualizar odontograma (línea 3282)
**Uso:** Rastrear SOLO dientes/superficies modificados

### **Variable 3: `condiciones_por_diente`**
**Tipo:** `Dict[int, Dict[str, str]]`
**Cuándo se llena:** `cargar_odontograma_paciente_actual()` (línea 2631)
**Cuándo se vacía:** Al limpiar estado (línea 3343)
**Uso:** Odontograma COMPLETO para visualización

### **Variable 4: `consulta_actual`**
**Tipo:** `ConsultaModel`
**Cuándo se llena:** `navegar_a_intervencion()` al seleccionar paciente
**Uso:** Contexto de la consulta siendo atendida

### **Variable 5: `paciente_actual`**
**Tipo:** `PacienteModel`
**Cuándo se llena:** `navegar_a_intervencion()` al seleccionar paciente
**Uso:** Datos del paciente siendo atendido

---

## ⚠️ ERRORES COMUNES Y SOLUCIONES

### **Error 1: Foreign key constraint en `condiciones_diente`**
**Causa:** Usar `personal_id` en campo `registrado_por`
**Solución:** Usar `self.id_usuario` (tabla usuarios)
**Línea:** 3271

### **Error 2: Intentar actualizar 160 registros en boca completa**
**Causa:** Usar `condiciones_por_diente` en vez de `cambios_pendientes_odontograma`
**Solución:** Verificar `cambios_pendientes_odontograma` (línea 3244)
**Línea corregida:** 3244, 3250

### **Error 3: Servicios sin `servicio_id`**
**Causa:** No obtener ID real del servicio al agregar
**Solución:** Usar `self.selected_service_id` (línea 3870)
**Línea:** 3870

### **Error 4: Superficie "boca completa" como string**
**Causa:** Pasar `["Boca completa"]` en vez de array vacío
**Solución:** `servicio["superficies"] = []` para boca completa
**Línea:** 3916

---

## 📊 TABLA RESUMEN: FUNCIONES Y SU PROPÓSITO

| Función | Propósito | ¿Cuándo se llama? |
|---------|-----------|-------------------|
| `guardar_intervencion_completa()` | Finalizar intervención completa | Click en botón "Finalizar" |
| `agregar_servicio_a_intervencion()` | Agregar servicio a lista temporal | Click en "Agregar servicio" en modal |
| `cargar_odontograma_paciente_actual()` | Cargar odontograma completo | Al iniciar atención de paciente |
| `guardar_cambios_odontograma()` | Guardar cambios manuales (NO usado en finalizar) | Click manual en "Guardar odontograma" |
| `navegar_a_intervencion()` | Iniciar atención de paciente | Click en paciente de la cola |
| `change_consultation_status()` | Cambiar estado de consulta | Al finalizar intervención |

---

## 🎯 CAMINOS POSIBLES AL FINALIZAR

### **CAMINO 1: Servicio de boca completa (sin cambios odontograma)**
```
1. ✅ Crear intervención
2. ✅ Guardar 1 servicio (diente=NULL, superficie=NULL)
3. ℹ️ Saltar actualización odontograma (cambios_pendientes_odontograma vacío)
4. ✅ Cambiar consulta a "entre_odontologos"
5. ✅ Limpiar estado
6. ✅ Navegar a lista
```

### **CAMINO 2: Servicio superficie específica CON cambio automático**
```
1. ✅ Crear intervención
2. ✅ Guardar N servicios (1 por superficie)
3. ✅ Actualizar M condiciones en odontograma (solo las modificadas)
4. ✅ Cambiar consulta a "entre_odontologos"
5. ✅ Limpiar estado
6. ✅ Navegar a lista
```

### **CAMINO 3: Servicio diente completo SIN cambio automático**
```
1. ✅ Crear intervención
2. ✅ Guardar 5 servicios (1 por superficie: oclusal, mesial, distal, vestibular, lingual)
3. ℹ️ Saltar actualización odontograma (checkbox desactivado)
4. ✅ Cambiar consulta a "entre_odontologos"
5. ✅ Limpiar estado
6. ✅ Navegar a lista
```

---

## 🔧 FUNCIONES QUE FALTAN / TODO

### **TODO 1: Crear pago pendiente automáticamente**
**Línea:** 3337
**Estado:** Comentado
**Descripción:** Sistema debe crear pago pendiente automáticamente al finalizar intervención

### **TODO 2: Registrar hora_inicio y hora_fin reales**
**Líneas:** 3188-3189
**Estado:** Usando `datetime.now()` para ambos
**Mejora:** Registrar hora real de inicio cuando inicia atención

### **TODO 3: Manejo de múltiples odontólogos en misma consulta**
**Estado:** Implementado parcialmente
**Descripción:** Falta UI para mostrar intervenciones de otros odontólogos en misma consulta

---

## ✅ VERIFICACIONES FINALES

**Antes de finalizar intervención, el sistema debe tener:**
1. ✅ Al menos 1 servicio en `servicios_consulta_actual`
2. ✅ `consulta_actual` con ID válido
3. ✅ `paciente_actual` con ID válido
4. ✅ `id_usuario` válido (para registrado_por)
5. ✅ `id_personal` válido (para odontologo_id)

**Después de finalizar intervención, el sistema debe:**
1. ✅ Crear 1 registro en `intervenciones`
2. ✅ Crear N registros en `intervenciones_servicios` (según servicios)
3. ✅ Crear M registros en `condiciones_diente` (solo si hay cambios)
4. ✅ Actualizar estado de `consultas` a "entre_odontologos"
5. ✅ Limpiar estado local
6. ✅ Mostrar toast de éxito
7. ✅ Navegar a lista de pacientes

---

**Documento creado:** 2025-10-10
**Última actualización:** 2025-10-10
**Estado:** ✅ Completo
**Propósito:** Referencia técnica para debugging y desarrollo
