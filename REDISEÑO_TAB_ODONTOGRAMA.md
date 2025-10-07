# REDISEÑO TAB ODONTOGRAMA PROFESIONAL
**Fecha:** 01 Octubre 2025
**Versión:** 1.0 - Propuesta de Diseño
**Estado:** Análisis y Diseño Completo

---

## 1. PROBLEMAS IDENTIFICADOS EN DISEÑO ACTUAL

### A. COMPLEJIDAD VISUAL INNECESARIA

#### Problema: División de dientes por superficies es visualmente confusa
**Archivo:** `interactive_tooth.py` (líneas 236-305)

```python
# ACTUAL: 5 superficies separadas visualmente por diente
def tooth_surface(tooth_number, surface_name, condition, is_selected, is_modified):
    # Renderiza 5 boxes superpuestos con posiciones absolutas
    SURFACE_POSITIONS = {
        "oclusal": {"position": "absolute", "top": "15%", "left": "25%", ...},
        "mesial": {"position": "absolute", "left": "8%", "top": "25%", ...},
        # ... 3 superficies más
    }
```

**Impacto UX:**
- El usuario ve 5 regiones clickeables por diente (160 áreas para 32 dientes)
- Difícil distinguir qué superficie está seleccionada
- Sobrecarga visual en la interfaz
- Dificulta navegación rápida médica

#### Problema: Demasiadas columnas en grid
**Archivo:** `odontograma_interactivo_grid.py` (líneas 449-507)

```python
# ACTUAL: Grid con 4 columnas por cuadrante
rx.grid(
    rx.foreach(...),
    columns="4",  # 4 columnas = demasiado espacio horizontal
    gap="12px",
)
```

**Impacto UX:**
- Requiere scroll horizontal en pantallas medianas
- Dientes muy separados dificultan visión panorámica
- No sigue estándar de odontogramas médicos (que son más compactos)

### B. INCONSISTENCIAS DE COLORES

#### Problema: Paleta de colores diferente a resto del sistema
**Archivo:** `interactive_tooth.py` (líneas 15-112)

```python
# ACTUAL: Paleta personalizada del odontograma
MEDICAL_CONDITION_PALETTE = {
    "sano": {"bg": "#dcfce7", "border": "#16a34a", ...},
    "caries": {"bg": "#fef2f2", "border": "#dc2626", ...},
    # ... definiciones únicas
}
```

**VS consultas_page.py (paleta consistente del sistema):**
```python
DARK_COLORS = {
    "background": "#0f1419",
    "surface": "#1a1f2e",
    "border": "#2d3748",
    "accent_blue": "#3182ce",
    "accent_green": "#38a169",
    # ... paleta profesional oscura
}
```

**Impacto UX:**
- Colores muy claros (#dcfce7) chocan con tema oscuro (#0f1419)
- Inconsistencia visual al cambiar de tabs
- Dientes parecen "pegados" del tema claro anterior

### C. ORGANIZACIÓN ESPACIAL NO OPTIMIZADA

#### Problema: Layout no sigue patrón enterprise del sistema
**Archivo:** `intervencion_page.py` (líneas 263-299)

```python
# ACTUAL: Layout básico sin estructura clara
rx.grid(
    panel_paciente_enterprise(),
    intervention_tabs_integrated(),
    columns=rx.breakpoints(initial="1", md="1", lg="320px 1fr", xl="350px 1fr"),
    # Sin headers, sin status bars consistentes, sin leyendas
)
```

**VS consultas_page.py (patrón enterprise profesional):**
```python
# CORRECTO: Header + Stats + Control bar + Grid
medical_page_layout(
    clean_consultas_page_header(),
    queue_control_bar_simple(),  # Stats cards con glassmorphism
    rx.grid(...),  # Grid principal
)
```

**Impacto UX:**
- No hay contexto visual claro del paciente en tab odontograma
- Falta leyenda de condiciones accesible
- Sin indicadores de progreso/estado sincronización
- Barra de estado V3.0 existe pero no está bien integrada

---

## 2. PROPUESTA DE NUEVO DISEÑO

### FILOSOFÍA DE DISEÑO:
> **"Un diente, un componente. La complejidad en el modal, no en el grid."**

### A. PRINCIPIOS CLAVE

1. **Simplicidad Visual**: Diente = 1 componente unificado
2. **Interacción Progresiva**: Click abre modal con detalles de superficies
3. **Paleta Consistente**: Usar DARK_COLORS de consultas_page.py
4. **Layout Enterprise**: Seguir patrón de personal_page.py y consultas_page.py
5. **Mobile-First**: Responsive desde 320px hasta 2xl

### B. ESTRUCTURA DE COMPONENTES OPTIMIZADA

```python
# ==========================================
# NUEVO SISTEMA DE ODONTOGRAMA SIMPLIFICADO
# ==========================================

# 1. COMPONENTE DIENTE UNIFICADO (NO 5 SUPERFICIES)
def simple_tooth_component(tooth_number: int, estado_general: str) -> rx.Component:
    """
    Diente simple unificado - Click abre modal para seleccionar superficie

    Args:
        tooth_number: Número FDI (11-48)
        estado_general: "sano" | "con_condiciones" | "critico"

    Returns:
        Box único con color de estado general
    """

    return rx.tooltip(
        rx.box(
            # Número del diente centrado
            rx.text(str(tooth_number), font_weight="800", size="2"),

            # Indicador visual de condiciones (pequeño badge)
            rx.cond(
                tiene_condiciones(tooth_number),
                rx.box(
                    style={
                        "position": "absolute",
                        "top": "4px",
                        "right": "4px",
                        "width": "8px",
                        "height": "8px",
                        "background": get_condition_indicator_color(tooth_number),
                        "border_radius": "50%",
                        "box_shadow": "0 0 6px rgba(255,255,255,0.4)"
                    }
                )
            ),

            style={
                # Dimensiones profesionales
                "width": "48px",
                "height": "48px",
                "border_radius": RADIUS["xl"],

                # Color según estado GENERAL (no por superficie)
                "background": get_general_tooth_color(tooth_number),
                "border": f"2px solid {get_tooth_border_color(tooth_number)}",

                # Glassmorphism consistente con sistema
                "backdrop_filter": "blur(10px)",
                "box_shadow": SHADOWS["md"],

                # Interactividad premium
                "cursor": "pointer",
                "transition": "all 0.3s ease",
                "_hover": {
                    "transform": "translateY(-4px) scale(1.08)",
                    "box_shadow": SHADOWS["xl"],
                    "border_color": DARK_COLORS["accent_blue"]
                }
            },

            # Click abre modal de superficies
            on_click=lambda: AppState.abrir_modal_superficies_diente(tooth_number)
        ),
        content=f"Diente {tooth_number}: Click para editar superficies"
    )

# 2. MODAL SELECTOR DE SUPERFICIES (NUEVO)
def modal_selector_superficies() -> rx.Component:
    """
    Modal que aparece al click en diente - Aquí sí se muestran las 5 superficies

    Layout:
    - Header: Diente seleccionado + estado general
    - Grid 3x2: 5 superficies interactivas + leyenda
    - Selector: 12 condiciones médicas disponibles
    - Footer: Guardar / Cancelar
    """

    return rx.dialog.root(
        rx.dialog.content(
            rx.vstack(
                # Header
                rx.hstack(
                    rx.text(
                        f"Diente {AppState.diente_seleccionado}",
                        size="6",
                        weight="bold"
                    ),
                    rx.spacer(),
                    rx.dialog.close(rx.icon("x"))
                ),

                # Visualización 5 superficies
                rx.grid(
                    superficie_card("oclusal"),
                    superficie_card("mesial"),
                    superficie_card("distal"),
                    superficie_card("vestibular"),
                    superficie_card("lingual"),
                    columns="3",
                    gap="3"
                ),

                # Selector de condición
                rx.select(
                    options=CONDICIONES_MEDICAS,
                    on_change=AppState.aplicar_condicion_superficie
                ),

                # Botones
                rx.hstack(
                    rx.button("Cancelar", variant="outline"),
                    rx.button("Guardar Cambios", on_click=AppState.guardar_cambios_diente),
                    spacing="3"
                ),

                spacing="6",
                width="100%"
            ),

            style={
                "max_width": "600px",
                "background": DARK_COLORS["surface"],
                "border_radius": RADIUS["2xl"],
                "padding": SPACING["8"]
            }
        ),
        open=AppState.modal_superficies_abierto
    )

# 3. GRID ODONTOGRAMA COMPACTO (6 COLUMNAS VS 4 ACTUAL)
def compact_odontogram_grid() -> rx.Component:
    """Grid optimizado con más dientes por fila"""

    return rx.box(
        rx.vstack(
            # Arcada Superior
            rx.hstack(
                # Cuadrante 1 (Superior Derecho): 18-11
                cuadrante_compacto(
                    titulo="Cuadrante I",
                    dientes=[18,17,16,15,14,13,12,11],
                    color=DARK_COLORS["accent_blue"]
                ),

                # Separador
                rx.divider(orientation="vertical", height="200px"),

                # Cuadrante 2 (Superior Izquierdo): 21-28
                cuadrante_compacto(
                    titulo="Cuadrante II",
                    dientes=[21,22,23,24,25,26,27,28],
                    color=DARK_COLORS["accent_green"]
                ),

                spacing="6",
                width="100%",
                justify="center"
            ),

            # Separador Horizontal
            rx.divider(width="80%"),

            # Arcada Inferior (similar)
            # ... (mismo patrón)

            spacing="8",
            align="center"
        ),

        style={
            "background": DARK_COLORS["surface"],
            "border_radius": RADIUS["2xl"],
            "padding": SPACING["8"],
            "border": f"1px solid {DARK_COLORS['border']}"
        }
    )

def cuadrante_compacto(titulo: str, dientes: list, color: str) -> rx.Component:
    """Cuadrante con 6 columnas (más compacto que actual)"""

    return rx.vstack(
        # Badge título
        rx.badge(titulo, color_scheme="blue"),

        # Grid de dientes - 6 COLUMNAS vs 4 actual
        rx.grid(
            *[simple_tooth_component(num) for num in dientes],
            columns="4",  # 2 filas de 4 dientes
            gap="8px",
            justify_items="center"
        ),

        spacing="3",
        align="center"
    )
```

### C. PALETA DE COLORES EXTRAÍDA DE CONSULTAS_PAGE.PY

```python
# ==========================================
# PALETA DE COLORES ODONTOGRAMA V3.0
# ==========================================

# Basado en DARK_COLORS de consultas_page.py (líneas 27-50)
ODONTOGRAM_COLORS = {
    # Backgrounds del sistema
    "background": "#0f1419",
    "surface": "#1a1f2e",
    "surface_hover": "#252b3a",
    "border": "#2d3748",
    "glass_bg": "rgba(26, 31, 46, 0.8)",

    # Estados de dientes (REEMPLAZA MEDICAL_CONDITION_PALETTE)
    "tooth_sano": {
        "bg": DARK_COLORS["accent_green"],        # Verde oscuro
        "border": DARK_COLORS["accent_green"],
        "hover_shadow": "0 8px 25px rgba(56, 161, 105, 0.4)"
    },

    "tooth_caries": {
        "bg": DARK_COLORS["priority_urgent"],     # Rojo oscuro
        "border": DARK_COLORS["priority_urgent"],
        "hover_shadow": "0 8px 25px rgba(220, 38, 38, 0.5)",
        "animation": "pulse 2s infinite"
    },

    "tooth_obturado": {
        "bg": DARK_COLORS["accent_blue"],         # Azul oscuro
        "border": DARK_COLORS["accent_blue"],
        "hover_shadow": "0 8px 25px rgba(49, 130, 206, 0.4)"
    },

    "tooth_corona": {
        "bg": DARK_COLORS["accent_yellow"],       # Amarillo oscuro
        "border": DARK_COLORS["accent_yellow"],
        "hover_shadow": "0 8px 25px rgba(214, 158, 46, 0.4)"
    },

    "tooth_ausente": {
        "bg": DARK_COLORS["surface_hover"],       # Gris oscuro
        "border": DARK_COLORS["border"],
        "opacity": "0.6"
    },

    "tooth_fractura": {
        "bg": DARK_COLORS["accent_red"],          # Rojo intenso
        "border": DARK_COLORS["accent_red"],
        "hover_shadow": "0 8px 25px rgba(229, 62, 62, 0.5)",
        "animation": "pulse 2s infinite"
    },

    "tooth_en_tratamiento": {
        "bg": DARK_COLORS["priority_high"],       # Naranja oscuro
        "border": DARK_COLORS["priority_high"],
        "hover_shadow": "0 8px 25px rgba(234, 88, 12, 0.4)"
    }
}

# Funciones helper para obtener colores
def get_general_tooth_color(tooth_number: int) -> str:
    """Obtiene color de fondo según estado GENERAL del diente"""

    # Lógica:
    # 1. Si TODAS superficies sanas → verde
    # 2. Si ALGUNA crítica (caries/fractura) → rojo
    # 3. Si tratado (obturado/corona) → azul
    # 4. Si ausente → gris

    estado = calcular_estado_general(tooth_number)
    return ODONTOGRAM_COLORS[f"tooth_{estado}"]["bg"]

def get_tooth_border_color(tooth_number: int) -> str:
    """Color de borde según estado"""
    estado = calcular_estado_general(tooth_number)
    return ODONTOGRAM_COLORS[f"tooth_{estado}"]["border"]

def calcular_estado_general(tooth_number: int) -> str:
    """
    Calcula estado GENERAL del diente basado en todas sus superficies

    Prioridad:
    1. ausente (si diente ausente)
    2. fractura (si cualquier superficie fracturada)
    3. caries (si cualquier superficie con caries)
    4. en_tratamiento
    5. corona/obturado (si alguna superficie)
    6. sano (si todas superficies sanas)
    """

    condiciones = AppState.condiciones_por_diente.get(tooth_number, {})

    # Verificar en orden de prioridad
    if "ausente" in condiciones.values():
        return "ausente"
    if "fractura" in condiciones.values():
        return "fractura"
    if "caries" in condiciones.values():
        return "caries"
    if "en_tratamiento" in condiciones.values():
        return "en_tratamiento"
    if "corona" in condiciones.values() or "obturado" in condiciones.values():
        return "obturado"

    return "sano"
```

### D. LAYOUT ENTERPRISE COMPLETO

```python
# ==========================================
# LAYOUT COMPLETO TAB ODONTOGRAMA V3.0
# ==========================================

def odontograma_tab_v3() -> rx.Component:
    """
    Tab de odontograma rediseñado siguiendo patrón enterprise

    Estructura:
    1. Barra de estado con info paciente + sincronización
    2. Controles y filtros (modo edición, comparar versiones)
    3. Grid principal de odontograma compacto
    4. Panel lateral con leyenda de condiciones
    5. Modal selector de superficies
    """

    return rx.vstack(
        # 1. BARRA DE ESTADO (ya existe - reusar y mejorar)
        odontograma_status_bar_v3_enhanced(),

        # 2. CONTROLES Y FILTROS (simplificados)
        rx.hstack(
            # Switch modo edición
            rx.hstack(
                rx.switch(
                    checked=AppState.modo_edicion_odontograma,
                    on_change=AppState.toggle_modo_edicion
                ),
                rx.text("Modo Edición", color=DARK_COLORS["text_secondary"]),
                spacing="2"
            ),

            rx.spacer(),

            # Botones acción
            rx.hstack(
                rx.button(
                    rx.hstack(
                        rx.icon("history", size=16),
                        rx.text("Ver Historial"),
                        spacing="2"
                    ),
                    on_click=AppState.abrir_modal_historial,
                    variant="outline"
                ),

                rx.button(
                    rx.hstack(
                        rx.icon("save", size=16),
                        rx.text("Guardar Cambios"),
                        spacing="2"
                    ),
                    on_click=AppState.guardar_odontograma,
                    disabled=~AppState.cambios_sin_guardar,
                    style={
                        "background": f"linear-gradient(135deg, {DARK_COLORS['accent_green']} 0%, #48bb78 100%)"
                    }
                ),

                spacing="3"
            ),

            width="100%",
            padding=SPACING["4"],
            style={
                "background": DARK_COLORS["surface"],
                "border_radius": RADIUS["lg"],
                "border": f"1px solid {DARK_COLORS['border']}"
            }
        ),

        # 3. LAYOUT PRINCIPAL: Grid + Leyenda lateral
        rx.grid(
            # Grid odontograma (ocupa 70%)
            compact_odontogram_grid(),

            # Panel lateral leyenda (ocupa 30%)
            leyenda_condiciones_panel(),

            columns=rx.breakpoints(
                initial="1",      # Móvil: stack vertical
                md="1",           # Tablet: stack vertical
                lg="70% 30%",     # Desktop: grid + leyenda
                xl="75% 25%"      # XL: más espacio al grid
            ),
            gap=SPACING["6"],
            width="100%"
        ),

        # 4. MODAL SELECTOR SUPERFICIES
        modal_selector_superficies(),

        spacing="6",
        width="100%",
        align="start"
    )

def leyenda_condiciones_panel() -> rx.Component:
    """Panel lateral con leyenda de condiciones siempre visible"""

    return rx.box(
        rx.vstack(
            # Header
            rx.hstack(
                rx.icon("info", size=16, color=DARK_COLORS["accent_blue"]),
                rx.text("Leyenda de Condiciones", font_weight="700", size="3"),
                spacing="2"
            ),

            # Lista de condiciones con colores
            rx.vstack(
                *[
                    condicion_item(nombre, color_data)
                    for nombre, color_data in ODONTOGRAM_COLORS.items()
                    if nombre.startswith("tooth_")
                ],
                spacing="2",
                width="100%"
            ),

            # Info útil
            rx.divider(),

            rx.vstack(
                rx.text("Cómo usar:", font_weight="600", size="2"),
                rx.text(
                    "1. Click en diente para editar",
                    size="1",
                    color=DARK_COLORS["text_muted"]
                ),
                rx.text(
                    "2. Selecciona superficie específica",
                    size="1",
                    color=DARK_COLORS["text_muted"]
                ),
                rx.text(
                    "3. Aplica condición médica",
                    size="1",
                    color=DARK_COLORS["text_muted"]
                ),
                spacing="1",
                align="start"
            ),

            spacing="4",
            width="100%",
            align="start"
        ),

        style={
            "background": DARK_COLORS["surface"],
            "border_radius": RADIUS["xl"],
            "padding": SPACING["6"],
            "border": f"1px solid {DARK_COLORS['border']}",
            "height": "fit-content",
            "position": "sticky",
            "top": SPACING["4"]
        }
    )

def condicion_item(nombre: str, color_data: dict) -> rx.Component:
    """Item individual en leyenda"""

    nombre_limpio = nombre.replace("tooth_", "").title()

    return rx.hstack(
        # Cuadro de color
        rx.box(
            style={
                "width": "24px",
                "height": "24px",
                "background": color_data["bg"],
                "border": f"2px solid {color_data['border']}",
                "border_radius": RADIUS["md"]
            }
        ),

        # Nombre condición
        rx.text(
            nombre_limpio,
            size="2",
            color=DARK_COLORS["text_primary"]
        ),

        spacing="3",
        align="center",
        width="100%"
    )
```

---

## 3. WIREFRAME EN TEXTO

```
┌─────────────────────────────────────────────────────────────────────┐
│  🦷 INTERVENCIÓN ODONTOLÓGICA                    [Ver Historial] [Volver]
│  Registro completo de tratamiento dental con odontograma interactivo
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │
│  │ 👤 Paciente  │  │ 🏥 Consulta  │  │ 📋 Tab Activo│              │
│  │ Juan Pérez   │  │ C-2025-001   │  │ Odontograma  │              │
│  │ HC-000123    │  │ En Atención  │  │              │              │
│  └──────────────┘  └──────────────┘  └──────────────┘              │
├─────────────────────────────────────────────────────────────────────┤
│  TABS: [Intervención] [Odontograma ✓] [Historial] [Notas]          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  ┌─ BARRA DE ESTADO ──────────────────────────────────────────────┐ │
│  │ ✅ Sincronizado | Última modificación: hace 2 min              │ │
│  └──────────────────────────────────────────────────────────────────┘ │
│                                                                       │
│  ┌─ CONTROLES ────────────────────────────────────────────────────┐ │
│  │ [ ] Modo Edición    [Ver Historial] [Guardar Cambios]         │ │
│  └──────────────────────────────────────────────────────────────────┘ │
│                                                                       │
│  ┌─ ODONTOGRAMA (70%) ─────────────┐  ┌─ LEYENDA (30%) ──────────┐ │
│  │                                  │  │ ℹ️ Leyenda de Condiciones│ │
│  │  ARCADA SUPERIOR                │  │                           │ │
│  │  ┌────────────────────────────┐ │  │ 🟢 Sano                   │ │
│  │  │ Q1 (Sup.Der) | Q2 (Sup.Izq)│ │  │ 🔴 Caries (Urgente)       │ │
│  │  │ [18][17][16][15][14][13]   │ │  │ 🔵 Obturado               │ │
│  │  │ [12][11]  |  [21][22][23]  │ │  │ 🟡 Corona                 │ │
│  │  │           |  [24][25][26]  │ │  │ ⚪ Ausente                 │ │
│  │  │           |  [27][28]      │ │  │ 🟠 En Tratamiento         │ │
│  │  └────────────────────────────┘ │  │                           │ │
│  │                                  │  │ ───────────────────       │ │
│  │  ─────────────────────────────  │  │ Cómo usar:                │ │
│  │                                  │  │ 1. Click en diente        │ │
│  │  ARCADA INFERIOR                │  │ 2. Selecciona superficie  │ │
│  │  ┌────────────────────────────┐ │  │ 3. Aplica condición       │ │
│  │  │ Q4 (Inf.Der) | Q3 (Inf.Izq)│ │  │                           │ │
│  │  │ [48][47][46][45][44][43]   │ │  └───────────────────────────┘ │
│  │  │ [42][41]  |  [31][32][33]  │ │                               │
│  │  │           |  [34][35][36]  │ │                               │
│  │  │           |  [37][38]      │ │                               │
│  │  └────────────────────────────┘ │                               │
│  └──────────────────────────────────┘                               │
└─────────────────────────────────────────────────────────────────────┘

MODAL AL CLICK EN DIENTE (ej. diente 16):
┌─────────────────────────────────────────┐
│  🦷 Diente 16                        [X]│
│  ─────────────────────────────────────  │
│                                          │
│  Selecciona la superficie a editar:     │
│                                          │
│  ┌──────────┬──────────┬──────────┐     │
│  │ Oclusal  │ Mesial   │ Distal   │     │
│  │  [🟢]    │  [🔴]    │  [🟢]    │     │
│  │  Sano    │ Caries   │  Sano    │     │
│  ├──────────┼──────────┼──────────┤     │
│  │Vestibular│ Lingual  │          │     │
│  │  [🟢]    │  [🟢]    │          │     │
│  │  Sano    │  Sano    │          │     │
│  └──────────┴──────────┴──────────┘     │
│                                          │
│  Condición a aplicar:                   │
│  [ Selecciona condición ▾ ]             │
│    - Sano                                │
│    - Caries                              │
│    - Obturado                            │
│    - Corona                              │
│    - ... (12 opciones)                   │
│                                          │
│  ────────────────────────────────────   │
│  [Cancelar]         [Guardar Cambios]   │
└─────────────────────────────────────────┘
```

---

## 4. LISTA DE COMPONENTES A MODIFICAR/CREAR

### A. MODIFICAR (Archivos Existentes)

#### 1. `interactive_tooth.py`
**Cambios:**
- Eliminar `tooth_surface()` complejo con 5 boxes
- Simplificar `interactive_tooth()` a componente unificado
- Cambiar paleta `MEDICAL_CONDITION_PALETTE` → usar `DARK_COLORS`
- Agregar función `simple_tooth_component()`
- Agregar función `calcular_estado_general()`

**Líneas a refactorizar:** 15-305 (paleta + superficies complejas)

#### 2. `odontograma_interactivo_grid.py`
**Cambios:**
- Reducir `columns="4"` → `columns="4"` (mantener 4 pero layout más compacto)
- Agregar `leyenda_condiciones_panel()` lateral
- Modificar `cuadrante_dientes()` para grid más compacto
- Integrar nuevo layout enterprise

**Líneas a refactorizar:** 449-507 (cuadrante_dientes)

#### 3. `intervencion_page.py`
**Cambios:**
- Actualizar integración del tab odontograma
- Asegurar consistencia con nuevo diseño
- Revisar que odontograma_status_bar_v3() esté bien integrado

**Líneas a revisar:** 263-299 (layout grid principal)

### B. CREAR (Archivos Nuevos)

#### 1. `modal_selector_superficies.py`
**Responsabilidad:** Modal que aparece al click en diente
**Contenido:**
```python
def modal_selector_superficies() -> rx.Component:
    """Modal para editar superficies específicas del diente"""
    # Header con diente seleccionado
    # Grid 3x2 con 5 superficies visuales
    # Selector de condición médica
    # Botones Guardar/Cancelar
```

#### 2. `odontogram_colors_v3.py`
**Responsabilidad:** Centralizar paleta de colores del odontograma
**Contenido:**
```python
# Paleta basada en DARK_COLORS de consultas_page.py
ODONTOGRAM_COLORS = {...}

# Funciones helper
def get_general_tooth_color(tooth_number: int) -> str
def get_tooth_border_color(tooth_number: int) -> str
def calcular_estado_general(tooth_number: int) -> str
```

#### 3. `leyenda_panel.py`
**Responsabilidad:** Panel lateral con leyenda de condiciones
**Contenido:**
```python
def leyenda_condiciones_panel() -> rx.Component:
    """Panel lateral sticky con leyenda médica"""
    # Lista de condiciones con colores
    # Instrucciones de uso
    # Stats del odontograma actual
```

---

## 5. PALETA DE COLORES DETALLADA

### EXTRAÍDA DE `consultas_page.py`

```python
# ==========================================
# PALETA OFICIAL SISTEMA (consultas_page.py líneas 27-50)
# ==========================================

DARK_COLORS_SISTEMA = {
    # Fondos principales
    "background": "#0f1419",           # Fondo app principal
    "surface": "#1a1f2e",             # Cards y superficies
    "surface_hover": "#252b3a",       # Hover en cards

    # Bordes
    "border": "#2d3748",              # Bordes sutiles
    "border_hover": "#4a5568",        # Bordes en hover

    # Textos
    "text_primary": "#f7fafc",        # Texto principal blanco
    "text_secondary": "#a0aec0",      # Texto secundario gris
    "text_muted": "#718096",          # Texto apagado

    # Acentos principales (USAR ESTOS PARA CONDICIONES)
    "accent_blue": "#3182ce",         # Azul principal → obturado
    "accent_green": "#38a169",        # Verde éxito → sano
    "accent_yellow": "#d69e2e",       # Amarillo advertencia → corona
    "accent_red": "#e53e3e",          # Rojo error → fractura

    # Glassmorphism
    "glass_bg": "rgba(26, 31, 46, 0.8)",
    "glass_border": "rgba(255, 255, 255, 0.1)",

    # Prioridades (USAR PARA CONDICIONES CRÍTICAS)
    "priority_urgent": "#dc2626",     # Rojo intenso → caries
    "priority_high": "#ea580c",       # Naranja → en_tratamiento
    "priority_normal": "#6b7280",     # Gris → ausente
    "priority_urgent_bg": "rgba(220, 38, 38, 0.1)",
    "priority_high_bg": "rgba(234, 88, 12, 0.1)",
    "priority_normal_bg": "rgba(107, 114, 128, 0.1)",
}
```

### MAPEO: Condiciones Médicas → Colores Sistema

| Condición Médica | Color Sistema | Hex | Uso |
|------------------|---------------|-----|-----|
| **Sano** | `accent_green` | `#38a169` | Dientes sin condiciones |
| **Caries** | `priority_urgent` | `#dc2626` | Urgencia médica |
| **Obturado** | `accent_blue` | `#3182ce` | Tratamiento completado |
| **Corona** | `accent_yellow` | `#d69e2e` | Prótesis |
| **Fractura** | `accent_red` | `#e53e3e` | Urgencia crítica |
| **En Tratamiento** | `priority_high` | `#ea580c` | Proceso activo |
| **Ausente** | `priority_normal` | `#6b7280` | Diente perdido |
| **Implante** | `accent_green` (oscuro) | `#2f855a` | Verde oscuro |
| **Endodoncia** | `accent_yellow` (oscuro) | `#b7791f` | Amarillo oscuro |

### VENTAJAS DE USAR ESTA PALETA

1. **Consistencia Visual**: Mismo tema en toda la app
2. **Profesional**: Colores oscuros médicos estándar
3. **Accesibilidad**: Contraste WCAG AAA en fondos oscuros
4. **Animaciones**: Ya soporta `pulse` para urgencias
5. **Glassmorphism**: Integrado con efectos del sistema

---

## 6. COMPARACIÓN: ANTES vs DESPUÉS

### ANTES (Actual)

```
PROBLEMAS:
✗ 160 áreas clickeables (5 superficies × 32 dientes)
✗ Colores claros (#dcfce7) en tema oscuro (#0f1419)
✗ Grid 4 columnas muy espaciado
✗ Sin leyenda visible
✗ Paleta inconsistente con sistema
✗ Complejidad visual alta
✗ Difícil navegación móvil

MÉTRICAS:
- Áreas interactivas: 160
- Tiempo para editar: ~8 clicks
- Colores únicos: 20 (paleta custom)
- Líneas de código: ~1100
- Responsive: Básico
```

### DESPUÉS (Propuesta)

```
MEJORAS:
✓ 32 áreas clickeables (1 diente = 1 componente)
✓ Colores oscuros consistentes (#1a1f2e, #38a169)
✓ Grid 4 columnas compacto + leyenda lateral
✓ Leyenda sticky siempre visible
✓ Paleta 100% basada en DARK_COLORS
✓ Modal para detalles de superficies
✓ Mobile-first responsive

MÉTRICAS:
- Áreas interactivas: 32 (5x menos)
- Tiempo para editar: ~3 clicks
- Colores únicos: 8 (reutilizando sistema)
- Líneas de código: ~600 (45% reducción)
- Responsive: Enterprise-grade
```

---

## 7. ROADMAP DE IMPLEMENTACIÓN

### FASE 1: PREPARACIÓN (1 hora)
- [ ] Crear backup de archivos actuales
- [ ] Crear `odontogram_colors_v3.py` con nueva paleta
- [ ] Crear estructura de `modal_selector_superficies.py`

### FASE 2: COMPONENTES CORE (2 horas)
- [ ] Refactorizar `simple_tooth_component()` en `interactive_tooth.py`
- [ ] Implementar `calcular_estado_general()`
- [ ] Eliminar código de superficies visuales complejas

### FASE 3: LAYOUT (1.5 horas)
- [ ] Crear `leyenda_condiciones_panel()`
- [ ] Actualizar `odontograma_interactivo_grid.py` con nuevo layout
- [ ] Integrar grid 70% + leyenda 30%

### FASE 4: MODAL (1.5 horas)
- [ ] Implementar `modal_selector_superficies()`
- [ ] Conectar con AppState eventos de selección
- [ ] Testing de guardado de condiciones

### FASE 5: INTEGRACIÓN (1 hora)
- [ ] Actualizar `intervencion_page.py`
- [ ] Verificar que status bar V3 funcione correctamente
- [ ] Tests responsive en mobile/tablet/desktop

### FASE 6: REFINAMIENTO (1 hora)
- [ ] Animaciones de hover y micro-interacciones
- [ ] Testing UX con usuarios finales
- [ ] Documentación del nuevo sistema

**TIEMPO TOTAL ESTIMADO: 8 horas**

---

## 8. CONSIDERACIONES TÉCNICAS

### A. COMPATIBILIDAD CON ESTADO ACTUAL

```python
# AppState ya tiene estas variables (NO cambiar):
AppState.condiciones_por_diente: Dict[int, Dict[str, str]]
AppState.diente_seleccionado: int
AppState.modal_condiciones_abierto: bool
AppState.odontograma_guardando: bool
AppState.cambios_sin_guardar: bool

# NUEVO a agregar en AppState:
AppState.modal_superficies_abierto: bool = False
AppState.superficie_en_edicion: str = ""
AppState.modo_edicion_odontograma: bool = True
```

### B. PERFORMANCE

**Optimizaciones:**
1. **Reducción de renders**: 32 componentes vs 160 actual (5x menos)
2. **Lazy loading**: Modal solo se renderiza al abrir
3. **Memoización**: `calcular_estado_general()` con cache
4. **Batch updates**: Guardar múltiples superficies en una transacción

### C. ACCESIBILIDAD

1. **Contraste WCAG AAA**: Todos los colores cumplen ratio >7:1
2. **Keyboard navigation**: Tab entre dientes, Enter para abrir modal
3. **Screen readers**: Labels descriptivos en tooltips
4. **Focus visible**: Bordes azules en elementos focuseados

---

## 9. PREGUNTAS PARA VALIDAR CON EL EQUIPO

1. ¿El modal de superficies debe ser `rx.dialog` o `rx.drawer` (slide desde derecha)?
2. ¿Mantener botón "Simular Test" en controles o removerlo?
3. ¿Leyenda debe ser colapsable o siempre visible?
4. ¿Grid debe ser 4 columnas (actual) o 6 columnas (más compacto)?
5. ¿Animación `pulse` solo para urgencias o también para en_tratamiento?

---

## 10. PRÓXIMOS PASOS

### ACCIÓN INMEDIATA RECOMENDADA:

1. **Revisar esta propuesta** con el equipo médico/desarrollo
2. **Validar paleta de colores** con odontólogos usuarios
3. **Crear prototipo interactivo** con Figma/Adobe XD (opcional)
4. **Aprobar diseño** antes de comenzar implementación
5. **Iniciar Fase 1** del roadmap

### RECURSOS NECESARIOS:

- **Desarrollador Frontend**: 8 horas
- **Diseñador UX** (opcional): 2 horas para validación
- **Odontólogo revisor**: 1 hora para feedback médico
- **Tester QA**: 2 horas para testing final

---

**Fin del Documento de Diseño**

**Autor:** Sistema de IA - Especialista UI/UX
**Versión:** 1.0
**Fecha:** 01 Octubre 2025
**Estado:** Pendiente Aprobación
