# 📋 ANÁLISIS Y PLAN DE REFACTORIZACIÓN - MÓDULO ODONTOLOGÍA
**Fecha:** 2025-01-13
**Objetivo:** Simplificar y limpiar código redundante manteniendo funcionalidad

---

## 🔍 PROBLEMAS IDENTIFICADOS

### 1. **PACIENTES DISPONIBLES NO FUNCIONA** ❌
**Ubicación:** `odontologia_page.py` línea 281, `estado_odontologia.py` línea 479-505

**Problema:**
```python
# odontologia_page.py línea 281
on_mount=[
    AppState.cargar_pacientes_asignados,
    AppState.cargar_consultas_disponibles_otros,  # ← Este método
]

# estado_odontologia.py línea 498
pacientes_disponibles = await odontologia_service.get_pacientes_disponibles(self.id_personal)
self.pacientes_disponibles_otros = pacientes_disponibles
```

**Causa raíz:**
- El método `get_pacientes_disponibles()` probablemente no está filtrando correctamente consultas con estado `"entre_odontologos"`
- La lista se carga pero queda vacía

**Solución:**
```python
# Verificar query SQL en odontologia_service.py línea 1034
# Debe filtrar:
WHERE consultas.estado = 'entre_odontologos'
  AND consultas.odontologo_id != %s  -- No mostrar propios
  AND consultas.fecha_creacion >= CURRENT_DATE  -- Solo hoy
```

---

### 2. **ESTADÍSTICAS NO CUENTAN CONSULTAS COMPLETADAS DEL DÍA** ❌
**Ubicación:** `estado_odontologia.py` líneas 433-477

**Problema:**
```python
# Línea 455-458: Solo carga consultas NO completadas
self.consultas_asignadas = [
    c for c in consultas_asignadas
    if c.estado in ["en_espera", "programada", "en_progreso", "en_atencion"]  # ← Excluye "completada"
]

# Línea 669: Computed var cuenta de consultas_asignadas (sin completadas)
"consultas_completadas": len([c for c in consultas_del_odontologo if c.estado == "completada"])
```

**Causa raíz:**
- `cargar_pacientes_asignados()` filtra y excluye consultas completadas
- Las estadísticas usan `self.consultas_asignadas` que no tiene completadas
- Resultado: Siempre muestra 0 completadas

**Solución SIMPLE:**
```python
# estado_odontologia.py
# ANTES (línea 455-458)
self.consultas_asignadas = [
    c for c in consultas_asignadas
    if c.estado in ["en_espera", "programada", "en_progreso", "en_atencion"]
]

# DESPUÉS: Cargar TODAS las del día
self.consultas_asignadas = consultas_asignadas  # Sin filtro

# Y usar computed var para separar:
@rx.var(cache=True)
def consultas_activas(self) -> List[ConsultaModel]:
    """Consultas que NO están completadas"""
    return [
        c for c in self.consultas_asignadas
        if c.estado in ["en_espera", "programada", "en_progreso", "en_atencion"]
    ]
```

---

### 3. **MODELO `ServicioIntervencionCompleto` INNECESARIO** 🔧
**Ubicación:** `estado_intervencion_servicios.py` líneas 30-116

**Problema:**
- Tenemos `ServicioModel` en `models/servicios_models.py`
- Creamos OTRO modelo `ServicioIntervencionCompleto` que es casi igual
- Método `from_servicio_model()` convierte uno en otro ← REDUNDANTE

**Causa raíz:**
- Duplicación de estructura
- Más código que mantener
- Confusión sobre cuál modelo usar

**Solución SIMPLE:**
```python
# ELIMINAR estado_intervencion_servicios.py líneas 30-116
# USAR SOLO ServicioModel con campos opcionales ya existentes

# En vez de:
servicio = ServicioIntervencionCompleto.from_servicio_model(...)

# Hacer:
servicio_temp = ServicioModel(
    id=servicio.id,
    nombre=servicio.nombre,
    # Agregar campos temporales de intervención
    diente_numero=diente_numero,
    superficies=superficies,
    nueva_condicion=condicion
)
```

---

### 4. **VARIABLES DEPRECATED ACTIVAS** 🧹
**Ubicación:** `estado_intervencion_servicios.py` líneas 137-142

**Problema:**
```python
# ⚠️ DEPRECATED - MANTENER POR COMPATIBILIDAD TEMPORAL
servicio_temporal: ServicioModel = ServicioModel()
dientes_seleccionados_texto: str = ""
superficie_temporal: str = ""
observaciones_temporal: str = ""
```

**Causa raíz:**
- Marcadas como deprecated hace meses
- TODAVÍA se usan en `agregar_servicio_a_intervencion()` línea 172

**Solución SIMPLE:**
```python
# ELIMINAR estas 4 variables
# USAR SOLO las nuevas del estado_odontologia:
# - selected_service_name
# - selected_tooth
# - superficie_oclusal_selected, superficie_mesial_selected, etc.
# - intervention_observations
```

---

### 5. **DUPLICACIÓN ENTRE ESTADOS** 🔄
**Problema:** Dos estados manejan servicios:

| Responsabilidad | estado_odontologia | estado_intervencion_servicios |
|----------------|-------------------|-------------------------------|
| Agregar servicio | ✅ `save_intervention_to_consultation()` | ✅ `agregar_servicio_a_intervencion()` |
| Lista temporal | ✅ `servicios_en_intervencion` | ✅ `servicios_en_intervencion` |
| Calcular totales | ❌ | ✅ `_recalcular_totales()` |
| Finalizar | ❌ Delega | ✅ `finalizar_mi_intervencion_odontologo()` |

**Solución SIMPLE:**
- **estado_odontologia**: Solo UI (formularios, modales, diente seleccionado)
- **estado_intervencion_servicios**: Solo lógica (agregar, calcular, guardar)

---

## 🎯 PLAN DE REFACTORIZACIÓN SIMPLE

### FASE 1: ARREGLAR BUGS CRÍTICOS (30 min)

#### 1.1. Arreglar estadísticas ✅
```python
# dental_system/state/estado_odontologia.py línea 455

# CAMBIO MÍNIMO:
self.consultas_asignadas = consultas_asignadas  # Sin filtro

# Agregar computed var nuevo:
@rx.var(cache=True)
def consultas_activas(self) -> List[ConsultaModel]:
    """Solo consultas que NO están completadas"""
    return [c for c in self.consultas_asignadas
            if c.estado not in ["completada", "cancelada"]]
```

#### 1.2. Arreglar pacientes disponibles ✅
```python
# dental_system/services/odontologia_service.py línea 1034

# Verificar query incluye:
SELECT DISTINCT
    p.*,
    c.id as consulta_id
FROM pacientes p
JOIN consultas c ON c.paciente_id = p.id
JOIN usuarios u ON u.id = c.odontologo_id
JOIN personal odontologo ON odontologo.usuario_id = u.id
WHERE c.estado = 'entre_odontologos'
  AND odontologo.id != %s  -- No mostrar propios
  AND c.fecha_creacion::date = CURRENT_DATE
ORDER BY c.updated_at DESC
```

---

### FASE 2: LIMPIAR CÓDIGO (1 hora)

#### 2.1. Eliminar variables deprecated
```python
# estado_intervencion_servicios.py líneas 137-142
# ELIMINAR:
# - servicio_temporal
# - dientes_seleccionados_texto
# - superficie_temporal
# - observaciones_temporal

# ACTUALIZAR método agregar_servicio_a_intervencion() línea 148
# Para usar variables de estado_odontologia directamente
```

#### 2.2. Consolidar manejo de servicios
```python
# REGLA CLARA:
# - estado_odontologia: SOLO UI (selected_tooth, modales, formularios)
# - estado_intervencion_servicios: SOLO lógica (agregar, totales, guardar)

# Mover estos métodos de estado_odontologia → estado_intervencion_servicios:
# - save_intervention_to_consultation() → agregar_servicio_directo()
# - delete_consultation_service() → remover_servicio_de_intervencion()
```

#### 2.3. Simplificar modelo ServicioIntervencionCompleto
```python
# OPCIÓN A (más simple): ELIMINAR clase completa
# Usar dict temporal: {"servicio_id": "...", "diente_numero": 16, ...}

# OPCIÓN B (mantener tipado): Simplificar a dataclass
from dataclasses import dataclass

@dataclass
class ServicioIntervencionTemp:
    servicio_id: str
    diente_numero: int | None
    superficies: list[str]
    nueva_condicion: str | None
    costo_usd: float

    # SIN métodos from_servicio_model() complejos
```

---

### FASE 3: MEJORAR PÁGINA ODONTOLOGÍA (30 min)

#### 3.1. ¿Qué más agregar a odontologia_page.py?

**OPCIONES SIMPLES:**

1. **Botón refrescar manual** ✅
```python
rx.button(
    rx.icon("refresh-cw", size=16),
    "Actualizar",
    on_click=[
        AppState.cargar_pacientes_asignados,
        AppState.cargar_consultas_disponibles_otros
    ],
    variant="ghost"
)
```

2. **Filtro por estado** (opcional)
```python
rx.select(
    ["Todos", "En Espera", "En Atención", "Entre Odontólogos"],
    value=AppState.filtro_estado_consulta,
    on_change=AppState.set_filtro_estado_consulta
)
```

3. **Búsqueda por paciente** (opcional)
```python
rx.input(
    placeholder="Buscar paciente...",
    value=AppState.termino_busqueda_pacientes,
    on_change=AppState.set_termino_busqueda_pacientes
)
```

**MI RECOMENDACIÓN:** Solo agregar botón refrescar. Mantener simple.

---

### FASE 4: ACTUALIZAR TEMA INTERVENCION_PAGE (15 min)

**Problema mencionado:** "no está usando el tema del proyecto"

**Verificación:**
```python
# intervencion_page.py líneas 22-25
from dental_system.styles.themes import (
    COLORS, RADIUS, SPACING, SHADOWS, DARK_THEME, GRADIENTS,  # ✅ SÍ usa tema
    dark_crystal_card, dark_header_style, glassmorphism_card
)
```

**¿Qué actualizar?**
```python
# Línea 17: Cambiar import
# ANTES:
from dental_system.styles.medical_design_system import MEDICAL_COLORS

# DESPUÉS:
from dental_system.styles.themes import DARK_THEME

# Reemplazar MEDICAL_COLORS → DARK_THEME en:
# - current_consultation_services_table.py línea 17
```

---

## 📊 RESUMEN DE CAMBIOS

### ARCHIVOS A MODIFICAR:

| Archivo | Líneas | Cambio | Prioridad |
|---------|--------|--------|-----------|
| `estado_odontologia.py` | 455-458 | Eliminar filtro de completadas | 🔴 CRÍTICO |
| `odontologia_service.py` | 1034-1080 | Arreglar query SQL | 🔴 CRÍTICO |
| `estado_intervencion_servicios.py` | 137-142 | Eliminar variables deprecated | 🟡 MEDIO |
| `estado_intervencion_servicios.py` | 30-116 | Simplificar/eliminar modelo | 🟡 MEDIO |
| `current_consultation_services_table.py` | 17 | Actualizar import tema | 🟢 BAJO |
| `odontologia_page.py` | 170-175 | Agregar botón refrescar | 🟢 OPCIONAL |

### LÍNEAS DE CÓDIGO:
- **Eliminar:** ~200 líneas (modelo complejo + variables deprecated)
- **Modificar:** ~50 líneas (bugs + imports)
- **Agregar:** ~20 líneas (computed var + botón)
- **NETO:** -130 líneas (6.5% del módulo)

---

## ✅ CHECKLIST DE EJECUCIÓN

### PASO 1: Arreglar bugs críticos
- [ ] Modificar `estado_odontologia.py` línea 455 (quitar filtro)
- [ ] Agregar computed var `consultas_activas`
- [ ] Verificar query SQL en `odontologia_service.py`
- [ ] Probar en UI: estadísticas ahora muestran completadas
- [ ] Probar en UI: pacientes disponibles aparecen

### PASO 2: Limpiar código
- [ ] Eliminar variables deprecated (líneas 137-142)
- [ ] Actualizar `agregar_servicio_a_intervencion()`
- [ ] Decidir: ¿Eliminar o simplificar `ServicioIntervencionCompleto`?
- [ ] Consolidar métodos entre estados

### PASO 3: Mejoras UI
- [ ] Agregar botón refrescar (opcional)
- [ ] Actualizar tema en tabla servicios
- [ ] Probar todo el flujo end-to-end

---

## 🎯 RECOMENDACIÓN FINAL

**ENFOQUE SUGERIDO: Incremental y probado**

1. **HOY:** Solo PASO 1 (arreglar bugs críticos) - 30 min
2. **MAÑANA:** PASO 2 (limpiar código) - 1 hora
3. **DESPUÉS:** PASO 3 (mejoras UI) - 30 min

**Total:** ~2 horas de trabajo limpio y probado.

**¿Empezamos con PASO 1 (bugs críticos)?** Son cambios pequeños con gran impacto.
