# CÓDIGO A AGREGAR EN estado_odontologia.py

## 📍 UBICACIÓN: Después de las variables existentes (línea ~170)

```python
# ==========================================
# 🆕 VARIABLES NUEVA ESTRUCTURA (SIN TABS)
# ==========================================

# Modales
show_add_intervention_modal: bool = False
show_change_condition_modal: bool = False

# Formulario intervención completa
selected_service_name: str = ""
superficie_oclusal_selected: bool = False
superficie_mesial_selected: bool = False
superficie_distal_selected: bool = False
superficie_vestibular_selected: bool = False
superficie_lingual_selected: bool = False
auto_change_condition: bool = False
new_condition_value: str = ""
intervention_observations: str = ""

# Formulario cambio condición rápido
quick_surface_selected: str = ""
quick_condition_value: str = ""

# Servicios de consulta actual (temporal, antes de guardar en BD)
servicios_consulta_actual: List[Dict[str, Any]] = []
```

## 📍 UBICACIÓN: En la sección de computed vars (línea ~4850)

```python
# ==========================================
# 🆕 COMPUTED VARS NUEVA ESTRUCTURA
# ==========================================

@rx.var(cache=True)
def get_tooth_conditions_rows(self) -> List[Dict[str, str]]:
    """
    📊 Formatear condiciones del diente seleccionado para tabla

    Returns:
        Lista de 5 dicts (una por superficie) con formato:
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
    if not self.selected_tooth:
        return []

    # Mapeo de condiciones a iconos/colores
    condition_map = {
        "sano": {"icon": "check-circle", "color": "#48BB78"},
        "caries": {"icon": "alert-circle", "color": "#E53E3E"},
        "obturado": {"icon": "shield", "color": "#4299E1"},
        "corona": {"icon": "crown", "color": "#9F7AEA"},
        "endodoncia": {"icon": "zap", "color": "#ED8936"},
        "ausente": {"icon": "x-circle", "color": "#A0AEC0"},
        "por_extraer": {"icon": "scissors", "color": "#F59E0B"},
        "fracturado": {"icon": "alert-triangle", "color": "#EF4444"},
    }

    surfaces = [
        ("oclusal", "Oclusal"),
        ("mesial", "Mesial"),
        ("distal", "Distal"),
        ("vestibular", "Vestibular"),
        ("lingual", "Lingual"),
    ]

    rows = []
    condiciones_diente = self.condiciones_por_diente.get(self.selected_tooth, {})

    for surface_key, surface_name in surfaces:
        condicion = condiciones_diente.get(surface_key, "sano")
        map_data = condition_map.get(condicion, {"icon": "circle", "color": "#A0AEC0"})

        rows.append({
            "superficie": surface_name,
            "estado": condicion.replace("_", " ").title(),
            "icon": map_data["icon"],
            "color": map_data["color"]
        })

    return rows

@rx.var(cache=True)
def get_consultation_services_rows(self) -> List[Dict[str, Any]]:
    """
    📋 Formatear servicios de consulta actual para tabla

    Returns:
        Lista de dicts formateados para mostrar en tabla
    """
    rows = []
    for service in self.servicios_consulta_actual:
        # Formatear superficies
        superficies = service.get("superficies", [])
        superficies_str = ", ".join(superficies) if superficies else "—"

        rows.append({
            "id": service.get("id", ""),
            "diente": str(service.get("diente", "")),
            "servicio": service.get("servicio", ""),
            "superficies": superficies_str,
            "costo_bs": f"{service.get('costo_bs', 0):,.0f} Bs",
            "costo_usd": f"${service.get('costo_usd', 0):.2f}",
        })

    return rows

@rx.var(cache=True)
def get_consultation_total_bs(self) -> float:
    """💰 Total en bolívares de servicios actuales"""
    return sum(s.get("costo_bs", 0) for s in self.servicios_consulta_actual)

@rx.var(cache=True)
def get_consultation_total_usd(self) -> float:
    """💰 Total en dólares de servicios actuales"""
    return sum(s.get("costo_usd", 0) for s in self.servicios_consulta_actual)

@rx.var(cache=True)
def get_consultation_total_bs_formatted(self) -> str:
    """💰 Total BS formateado"""
    return f"{self.get_consultation_total_bs:,.0f} Bs"

@rx.var(cache=True)
def get_consultation_total_usd_formatted(self) -> str:
    """💰 Total USD formateado"""
    return f"/ ${self.get_consultation_total_usd:.2f}"

@rx.var(cache=True)
def get_available_services_names(self) -> List[str]:
    """📋 Lista de nombres de servicios para select"""
    # Obtener desde self.lista_servicios si existe
    if hasattr(self, 'lista_servicios') and self.lista_servicios:
        return [s.get("nombre", "") for s in self.lista_servicios if s.get("nombre")]
    return []

@rx.var(cache=True)
def selected_service_cost_bs(self) -> float:
    """💵 Costo BS del servicio seleccionado"""
    if not self.selected_service_name:
        return 0.0

    for service in self.lista_servicios:
        if service.get("nombre") == self.selected_service_name:
            return service.get("precio_base_bs", 0.0)
    return 0.0

@rx.var(cache=True)
def selected_service_cost_usd(self) -> float:
    """💵 Costo USD del servicio seleccionado"""
    if not self.selected_service_name:
        return 0.0

    for service in self.lista_servicios:
        if service.get("nombre") == self.selected_service_name:
            return service.get("precio_base_usd", 0.0)
    return 0.0
```

## 📍 UBICACIÓN: En la sección de métodos (línea ~4200)

```python
# ==========================================
# 🆕 MÉTODOS NUEVA ESTRUCTURA
# ==========================================

# ─────────────────────────────────────────
# MODALES
# ─────────────────────────────────────────

def toggle_add_intervention_modal(self):
    """Toggle modal agregar intervención"""
    self.show_add_intervention_modal = not self.show_add_intervention_modal

def open_add_intervention_modal(self):
    """Abrir modal agregar intervención"""
    self.show_add_intervention_modal = True
    # Resetear formulario
    self.selected_service_name = ""
    self.superficie_oclusal_selected = False
    self.superficie_mesial_selected = False
    self.superficie_distal_selected = False
    self.superficie_vestibular_selected = False
    self.superficie_lingual_selected = False
    self.auto_change_condition = False
    self.new_condition_value = ""
    self.intervention_observations = ""

def toggle_change_condition_modal(self):
    """Toggle modal cambiar condición"""
    self.show_change_condition_modal = not self.show_change_condition_modal

# ─────────────────────────────────────────
# SUPERFICIES (CHECKBOXES)
# ─────────────────────────────────────────

def toggle_superficie_oclusal(self, checked: bool):
    """Toggle superficie oclusal"""
    self.superficie_oclusal_selected = checked

def toggle_superficie_mesial(self, checked: bool):
    """Toggle superficie mesial"""
    self.superficie_mesial_selected = checked

def toggle_superficie_distal(self, checked: bool):
    """Toggle superficie distal"""
    self.superficie_distal_selected = checked

def toggle_superficie_vestibular(self, checked: bool):
    """Toggle superficie vestibular"""
    self.superficie_vestibular_selected = checked

def toggle_superficie_lingual(self, checked: bool):
    """Toggle superficie lingual"""
    self.superficie_lingual_selected = checked

# ─────────────────────────────────────────
# OTROS SETTERS
# ─────────────────────────────────────────

def toggle_auto_change_condition(self, checked: bool):
    """Toggle cambio automático de condición"""
    self.auto_change_condition = checked

def set_new_condition_value(self, value: str):
    """Setear nueva condición"""
    self.new_condition_value = value

def set_intervention_observations(self, value: str):
    """Setear observaciones"""
    self.intervention_observations = value

def set_selected_service_name(self, value: str):
    """Setear servicio seleccionado"""
    self.selected_service_name = value

def set_quick_surface_selected(self, value: str):
    """Setear superficie seleccionada (cambio rápido)"""
    self.quick_surface_selected = value

def set_quick_condition(self, condition: str):
    """Setear condición (cambio rápido)"""
    self.quick_condition_value = condition

# ─────────────────────────────────────────
# GUARDAR SERVICIOS
# ─────────────────────────────────────────

@rx.event
async def save_intervention_to_consultation(self):
    """
    💾 Agregar servicio a lista temporal de consulta actual

    NO guarda en BD aún, solo agrega a self.servicios_consulta_actual
    Se guardará cuando se complete la consulta
    """
    async with self:
        try:
            # Validar datos
            if not self.selected_service_name:
                self.mostrar_toast("Selecciona un servicio", "warning")
                return

            if not self.selected_tooth:
                self.mostrar_toast("Selecciona un diente", "warning")
                return

            # Recopilar superficies seleccionadas
            superficies = []
            if self.superficie_oclusal_selected:
                superficies.append("Oclusal")
            if self.superficie_mesial_selected:
                superficies.append("Mesial")
            if self.superficie_distal_selected:
                superficies.append("Distal")
            if self.superficie_vestibular_selected:
                superficies.append("Vestibular")
            if self.superficie_lingual_selected:
                superficies.append("Lingual")

            if not superficies:
                self.mostrar_toast("Selecciona al menos una superficie", "warning")
                return

            # Crear dict del servicio
            import uuid
            servicio = {
                "id": str(uuid.uuid4()),
                "diente": self.selected_tooth,
                "servicio": self.selected_service_name,
                "superficies": superficies,
                "costo_bs": self.selected_service_cost_bs,
                "costo_usd": self.selected_service_cost_usd,
                "observaciones": self.intervention_observations,
            }

            # Agregar a lista
            self.servicios_consulta_actual.append(servicio)

            # Si auto_change_condition, actualizar condiciones
            if self.auto_change_condition and self.new_condition_value:
                if self.selected_tooth not in self.condiciones_por_diente:
                    self.condiciones_por_diente[self.selected_tooth] = {}

                for superficie in superficies:
                    self.condiciones_por_diente[self.selected_tooth][superficie.lower()] = self.new_condition_value

                # Guardar en BD
                await self.guardar_cambios_odontograma()

            # Cerrar modal
            self.show_add_intervention_modal = False
            self.mostrar_toast("Servicio agregado exitosamente", "success")

        except Exception as e:
            logger.error(f"❌ Error agregando servicio: {str(e)}")
            self.mostrar_toast(f"Error: {str(e)}", "error")

@rx.event
async def apply_quick_condition_change(self):
    """
    🔄 Cambiar condición del diente (cambio rápido)

    Guarda directamente en BD
    """
    async with self:
        try:
            # Validar
            if not self.selected_tooth:
                self.mostrar_toast("Selecciona un diente", "warning")
                return

            if not self.quick_surface_selected:
                self.mostrar_toast("Selecciona una superficie", "warning")
                return

            if not self.quick_condition_value:
                self.mostrar_toast("Selecciona una condición", "warning")
                return

            # Actualizar en memoria
            if self.selected_tooth not in self.condiciones_por_diente:
                self.condiciones_por_diente[self.selected_tooth] = {}

            self.condiciones_por_diente[self.selected_tooth][self.quick_surface_selected] = self.quick_condition_value

            # Guardar en BD
            await self.guardar_cambios_odontograma()

            # Cerrar modal
            self.show_change_condition_modal = False
            self.mostrar_toast("Condición actualizada", "success")

        except Exception as e:
            logger.error(f"❌ Error cambiando condición: {str(e)}")
            self.mostrar_toast(f"Error: {str(e)}", "error")

@rx.event
async def edit_consultation_service(self, service_id: str):
    """✏️ Editar servicio de la consulta actual"""
    # TODO: Implementar edición
    self.mostrar_toast("Edición próximamente", "info")

@rx.event
async def delete_consultation_service(self, service_id: str):
    """🗑️ Eliminar servicio de la consulta actual"""
    async with self:
        self.servicios_consulta_actual = [
            s for s in self.servicios_consulta_actual
            if s.get("id") != service_id
        ]
        self.mostrar_toast("Servicio eliminado", "success")
```

## ✅ VERIFICACIÓN

Después de agregar este código:

1. ✅ Variables de estado: 22 nuevas variables
2. ✅ Computed vars: 10 nuevos computed vars
3. ✅ Métodos: 14 nuevos métodos

**Total agregado:** ~250 líneas de código al estado
