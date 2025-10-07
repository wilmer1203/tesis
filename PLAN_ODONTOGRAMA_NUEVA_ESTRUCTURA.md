# 🦷 PLAN DE IMPLEMENTACIÓN - NUEVA ESTRUCTURA ODONTOGRAMA
## Fecha: 02 Octubre 2025
## Estado: En Progreso (40% completado)

---

## 📋 RESUMEN EJECUTIVO

### **Objetivo:**
Reestructurar la página de intervención odontológica para eliminar tabs y crear un flujo más intuitivo con:
1. Odontograma + Sidebar con tabla de condiciones
2. Tabla de servicios de consulta actual (editable)
3. Timeline histórico del paciente (solo lectura)

### **Ventajas del nuevo diseño:**
✅ Sin tabs confusos - Una sola página vertical
✅ Separación clara entre "Cambiar Condición" y "Agregar Intervención"
✅ Tabla de servicios actuales editable antes de finalizar consulta
✅ Timeline histórico filtrable al final
✅ Flujo médico más profesional e intuitivo

---

## ✅ PROGRESO ACTUAL (40%)

### **Componentes Creados:**

#### 1. ✅ `tooth_conditions_table.py` (COMPLETADO)
**Ubicación:** `dental_system/components/odontologia/tooth_conditions_table.py`

**Descripción:** Tabla de condiciones actuales del diente seleccionado
- 5 superficies (Oclusal, Mesial, Distal, Vestibular, Lingual)
- Iconos y colores por condición
- 100% declarativo - Usa `AppState.get_tooth_conditions_rows`

**Computed var requerido:**
```python
@rx.var(cache=True)
def get_tooth_conditions_rows(self) -> List[Dict[str, str]]:
    """
    Retorna lista de dicts procesados con:
    [
        {
            "superficie": "Oclusal",
            "estado": "Caries",
            "icon": "alert-circle",
            "color": "#E53E3E"
        },
        ...
    ]
    """
    # TODO: Implementar
    pass
```

#### 2. ❌ `current_consultation_services_table.py` (ELIMINADO - RECREAR)
**Ubicación:** `dental_system/components/odontologia/current_consultation_services_table.py`

**Descripción:** Tabla de servicios agregados en la consulta actual
- Columnas: Diente | Servicio | Superficies | Costo | Acciones
- Editable (editar/eliminar servicios)
- Total acumulado BS/USD
- Botón "Agregar Servicio"

**Estado:** Archivo eliminado por errores de `.get()` con Vars. Necesita recreación 100% declarativa.

**Computed vars requeridos:**
```python
@rx.var(cache=True)
def get_consultation_services_rows(self) -> List[Dict[str, Any]]:
    """
    Retorna lista de servicios de la consulta actual:
    [
        {
            "id": "uuid",
            "diente": 16,
            "servicio": "Obturación",
            "superficies": "Oclusal, Mesial",
            "costo_bs": 250000,
            "costo_usd": 6.85
        },
        ...
    ]
    """
    pass

@rx.var(cache=True)
def get_consultation_total_bs(self) -> float:
    """Total en bolívares de la consulta actual"""
    pass

@rx.var(cache=True)
def get_consultation_total_usd(self) -> float:
    """Total en dólares de la consulta actual"""
    pass
```

#### 3. ⚠️ `modal_add_intervention.py` (NECESITA VALIDACIÓN)
**Ubicación:** `dental_system/components/odontologia/modal_add_intervention.py`

**Descripción:** Modal completo para agregar intervención
- Selector de servicio
- Checkboxes de superficies tratadas
- Checkbox "Cambiar condición automáticamente" + selector
- Observaciones (textarea)
- Costo calculado automáticamente

**Estado:** Creado, pero necesita validar que no use Python puro (if/for/get()).

**Variables de estado requeridas:**
```python
# Modal
show_add_intervention_modal: bool = False

# Formulario
selected_service_name: str = ""
superficie_oclusal_selected: bool = False
superficie_mesial_selected: bool = False
superficie_distal_selected: bool = False
superficie_vestibular_selected: bool = False
superficie_lingual_selected: bool = False
auto_change_condition: bool = False
new_condition_value: str = ""
intervention_observations: str = ""

# Computed vars
@rx.var
def selected_service_cost_bs(self) -> float:
    pass

@rx.var
def selected_service_cost_usd(self) -> float:
    pass

@rx.var
def get_available_services_names(self) -> List[str]:
    pass
```

**Métodos requeridos:**
```python
def toggle_add_intervention_modal(self):
    """Abrir/cerrar modal"""
    pass

def save_intervention_to_consultation(self):
    """Guardar servicio en consulta actual (NO en BD aún)"""
    pass
```

#### 4. ⚠️ `modal_change_condition.py` (NECESITA VALIDACIÓN)
**Ubicación:** `dental_system/components/odontologia/modal_change_condition.py`

**Descripción:** Modal simple para cambiar solo condición visual
- Selector de superficie
- Grid de botones de condiciones (8 opciones)
- Guardado rápido

**Estado:** Creado, necesita validar patrón declarativo.

**Variables de estado requeridas:**
```python
# Modal
show_change_condition_modal: bool = False

# Formulario
quick_surface_selected: str = ""
quick_condition_value: str = ""
```

**Métodos requeridos:**
```python
def toggle_change_condition_modal(self):
    """Abrir/cerrar modal"""
    pass

def set_quick_condition(self, condition: str):
    """Seleccionar condición"""
    self.quick_condition_value = condition

def apply_quick_condition_change(self):
    """Guardar cambio de condición en BD"""
    pass
```

---

## 🔄 TAREAS PENDIENTES (60%)

### **FASE 1: Corregir/Completar Componentes**

#### Tarea 1.1: Recrear `current_consultation_services_table.py`
- [ ] Crear archivo limpio
- [ ] Usar solo `rx.foreach()` y `rx.cond()`
- [ ] Acceder a datos via `AppState.get_consultation_services_rows`
- [ ] NO usar `.get()` con Vars
- [ ] NO usar `if/else` Python

#### Tarea 1.2: Validar `modal_add_intervention.py`
- [ ] Revisar línea por línea
- [ ] Eliminar cualquier `.get()` con Vars
- [ ] Asegurar 100% declarativo
- [ ] Probar compilación

#### Tarea 1.3: Validar `modal_change_condition.py`
- [ ] Revisar línea por línea
- [ ] Eliminar cualquier `.get()` con Vars
- [ ] Asegurar 100% declarativo
- [ ] Probar compilación

### **FASE 2: Agregar al Estado (`estado_odontologia.py`)**

#### Tarea 2.1: Variables de estado para modales
```python
# Modales
show_add_intervention_modal: bool = False
show_change_condition_modal: bool = False

# Formulario intervención
selected_service_name: str = ""
superficie_oclusal_selected: bool = False
superficie_mesial_selected: bool = False
superficie_distal_selected: bool = False
superficie_vestibular_selected: bool = False
superficie_lingual_selected: bool = False
auto_change_condition: bool = False
new_condition_value: str = ""
intervention_observations: str = ""

# Formulario cambio condición
quick_surface_selected: str = ""
quick_condition_value: str = ""

# Servicios de consulta actual
servicios_consulta_actual: List[Dict[str, Any]] = []
```

#### Tarea 2.2: Computed vars
```python
@rx.var(cache=True)
def get_tooth_conditions_rows(self) -> List[Dict[str, str]]:
    """Para tooth_conditions_table"""
    if not self.selected_tooth:
        return []

    # Obtener condiciones del diente desde self.condiciones_por_diente
    # Formatear con iconos y colores
    # Retornar lista de 5 dicts (una por superficie)
    pass

@rx.var(cache=True)
def get_consultation_services_rows(self) -> List[Dict[str, Any]]:
    """Para current_consultation_services_table"""
    return self.servicios_consulta_actual

@rx.var(cache=True)
def get_consultation_total_bs(self) -> float:
    """Total BS de servicios actuales"""
    return sum(s.get("costo_bs", 0) for s in self.servicios_consulta_actual)

@rx.var(cache=True)
def get_consultation_total_usd(self) -> float:
    """Total USD de servicios actuales"""
    return sum(s.get("costo_usd", 0) for s in self.servicios_consulta_actual)

@rx.var(cache=True)
def get_available_services_names(self) -> List[str]:
    """Lista de nombres de servicios para select"""
    # Obtener desde self.lista_servicios
    pass

@rx.var
def selected_service_cost_bs(self) -> float:
    """Costo BS del servicio seleccionado"""
    # Buscar en self.lista_servicios según self.selected_service_name
    pass

@rx.var
def selected_service_cost_usd(self) -> float:
    """Costo USD del servicio seleccionado"""
    pass
```

#### Tarea 2.3: Métodos de eventos
```python
# Modales
def toggle_add_intervention_modal(self):
    self.show_add_intervention_modal = not self.show_add_intervention_modal

def open_add_intervention_modal(self):
    self.show_add_intervention_modal = True

def toggle_change_condition_modal(self):
    self.show_change_condition_modal = not self.show_change_condition_modal

# Superficies (checkboxes)
def toggle_superficie_oclusal(self, checked: bool):
    self.superficie_oclusal_selected = checked

def toggle_superficie_mesial(self, checked: bool):
    self.superficie_mesial_selected = checked

def toggle_superficie_distal(self, checked: bool):
    self.superficie_distal_selected = checked

def toggle_superficie_vestibular(self, checked: bool):
    self.superficie_vestibular_selected = checked

def toggle_superficie_lingual(self, checked: bool):
    self.superficie_lingual_selected = checked

# Otros
def toggle_auto_change_condition(self, checked: bool):
    self.auto_change_condition = checked

def set_new_condition_value(self, value: str):
    self.new_condition_value = value

def set_intervention_observations(self, value: str):
    self.intervention_observations = value

def set_selected_service_name(self, value: str):
    self.selected_service_name = value

def set_quick_surface_selected(self, value: str):
    self.quick_surface_selected = value

def set_quick_condition(self, condition: str):
    self.quick_condition_value = condition

# Guardar
@rx.event
async def save_intervention_to_consultation(self):
    """Agregar servicio a lista temporal (no BD)"""
    # Validar campos
    # Crear dict con datos
    # Agregar a self.servicios_consulta_actual
    # Si auto_change_condition, actualizar condiciones
    # Cerrar modal
    pass

@rx.event
async def apply_quick_condition_change(self):
    """Cambiar condición del diente en BD"""
    # Guardar en tabla condiciones_diente
    # Actualizar self.condiciones_por_diente
    # Cerrar modal
    pass

@rx.event
async def edit_consultation_service(self, service_id: str):
    """Editar servicio de la consulta"""
    pass

@rx.event
async def delete_consultation_service(self, service_id: str):
    """Eliminar servicio de la consulta"""
    # Filtrar self.servicios_consulta_actual
    pass
```

### **FASE 3: Modificar Sidebar y Página**

#### Tarea 3.1: Actualizar `tooth_detail_sidebar.py`
- [ ] Reemplazar tabs por estructura nueva:
  - Tabla de condiciones (usar `tooth_conditions_table()`)
  - Botón "Agregar Intervención" → `on_click=AppState.open_add_intervention_modal`
  - Botón "Cambiar Condición" → `on_click=AppState.toggle_change_condition_modal`

#### Tarea 3.2: Actualizar `intervencion_page.py`
- [ ] Mantener odontograma + sidebar arriba
- [ ] Agregar `current_consultation_services_table()` en medio
- [ ] Mantener `intervention_timeline()` al final
- [ ] Agregar imports de modales:
  ```python
  from dental_system.components.odontologia.modal_add_intervention import modal_add_intervention
  from dental_system.components.odontologia.modal_change_condition import modal_change_condition
  ```
- [ ] Agregar modales al final de la página:
  ```python
  modal_add_intervention(),
  modal_change_condition(),
  ```

### **FASE 4: Pruebas**

#### Tarea 4.1: Compilación
- [ ] Detener todos los procesos Reflex
- [ ] `reflex run`
- [ ] Verificar 0 errores

#### Tarea 4.2: Pruebas funcionales
- [ ] Seleccionar diente → Ver tabla de condiciones
- [ ] Click "Cambiar Condición" → Abrir modal → Seleccionar → Guardar → Verificar BD
- [ ] Click "Agregar Intervención" → Llenar formulario → Guardar → Verificar aparece en tabla
- [ ] Editar servicio de la tabla
- [ ] Eliminar servicio de la tabla
- [ ] Verificar timeline muestra intervenciones históricas

---

## 🎯 PRÓXIMOS PASOS INMEDIATOS

1. **Reiniciar servidor Reflex limpio** (hay 23+ procesos corriendo)
2. **Recrear `current_consultation_services_table.py`** 100% declarativo
3. **Validar ambos modales** línea por línea
4. **Agregar todas las variables y métodos al Estado**
5. **Modificar sidebar y página principal**
6. **Probar compilación y flujo completo**

---

## 📝 NOTAS IMPORTANTES

### **Reglas de Reflex que NO se pueden romper:**
- ❌ NO usar `if/else` en componentes → usar `rx.cond()`
- ❌ NO usar `for` loops → usar `rx.foreach()`
- ❌ NO usar `.get()` con Vars → preparar datos en computed vars
- ❌ NO usar métodos Python en Vars (`.lower()`, `.split()`, etc.)
- ✅ Todos los componentes 100% declarativos
- ✅ Estado procesa datos, componentes solo renderizan

### **Arquitectura de datos:**
```
Estado (estado_odontologia.py)
↓ computed vars procesan datos
↓ retornan List[Dict] o valores primitivos
↓
Componentes (100% declarativos)
↓ rx.foreach() itera
↓ rx.cond() condiciona
↓ lambda functions acceden a campos
```

---

## 📊 DIAGRAMA DE FLUJO FINAL

```
┌─────────────────────────────────────────────────┐
│  🦷 INTERVENCIÓN ODONTOLÓGICA                    │
├─────────────────────────────────────────────────┤
│  [Cards Info] Paciente | Consulta | Estado      │
│                                                  │
│  ┌─ ODONTOGRAMA ──────┐  ┌─ TOOTH DETAIL ─────┐│
│  │ Grid 32 dientes    │  │ 🦷 Diente 16        ││
│  │ Selección por clic │  │                     ││
│  └────────────────────┘  │ 📊 TABLA CONDICIONES││
│                          │ Oclusal  | 🔴 Caries││
│                          │ Mesial   | 🟢 Sano  ││
│                          │ ...                 ││
│                          │                     ││
│                          │ [➕ Agregar         ││
│                          │     Intervención]   ││
│                          │ [🔄 Cambiar         ││
│                          │     Condición]      ││
│                          └─────────────────────┘│
│                                                  │
│  ┌─ SERVICIOS DE ESTA CONSULTA ────────────────┐│
│  │ Diente│Servicio  │Superficies│Costo│Acciones││
│  │ ──────┼──────────┼───────────┼─────┼────────││
│  │   16  │Obturación│Oclusal    │$6.85│ ✏️ 🗑️  ││
│  │   23  │Limpieza  │Todas      │$15  │ ✏️ 🗑️  ││
│  │                   TOTAL: $21.85              ││
│  │                [+ Agregar Servicio]          ││
│  └──────────────────────────────────────────────┘│
│                                                  │
│  ┌─ TIMELINE HISTÓRICO ─────────────────────────┐│
│  │ Filtros: [Diente▾][Dentista▾][Período▾]     ││
│  │                                              ││
│  │ ● Obturación - Diente 16  | 02/09/24        ││
│  │   Dr. Rodríguez • $6.85                     ││
│  │                                              ││
│  │ ● (más intervenciones...)                   ││
│  └──────────────────────────────────────────────┘│
└─────────────────────────────────────────────────┘
```

---

**Fecha creación:** 02 Octubre 2025
**Última actualización:** 02 Octubre 2025
**Estado:** En Progreso - 40% completado
**Próxima sesión:** Continuar desde FASE 1, Tarea 1.1
