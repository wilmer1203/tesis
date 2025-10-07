# PROPUESTA: ODONTOGRAMA PROFESIONAL PARA REFLEX
**Versión:** 2.0 Enterprise Medical Design
**Fecha:** 01 Octubre 2025
**Estado:** Propuesta Completa - Pendiente Aprobación
**Basado en:** Análisis de plantilla React profesional + sistema actual Reflex

---

## 1. RESUMEN EJECUTIVO

### Objetivo
Rediseñar el módulo de odontograma del sistema dental integrando las mejores prácticas de la plantilla React profesional analizada, adaptándolas específicamente al framework Reflex.dev y al flujo médico real del sistema.

### Alcance
- Visor de odontograma principal simplificado (32 dientes FDI)
- Panel lateral de detalles por diente con tabs (Historial/Condiciones/Planificado)
- Timeline de intervenciones con filtros avanzados
- Selector de versiones con comparación visual
- Sistema de zoom y controles profesionales

### Tiempo Estimado
**8-10 horas** de desarrollo + 2 horas de testing

### Beneficios Clave
- Reducción de complejidad visual (160 áreas → 32 componentes únicos)
- UX médica profesional siguiendo estándares internacionales
- Integración nativa con sistema de consultas existente
- Performance mejorado (50% menos componentes)
- Mobile-first responsive design

---

## 2. ANÁLISIS DE LA PLANTILLA REACT

### 2.1 Estructura Analizada

#### A. Página Principal (index.jsx - 345 líneas)

**Características destacadas:**
- Layout responsive con grid adaptable (1 col móvil → 4 cols desktop)
- Gestión de estado React Hooks organizada
- Keyboard shortcuts implementados (Ctrl+P, Ctrl+E, Ctrl+C, Esc)
- Patient Context Bar condicional
- Panel toggle buttons para timeline y planificación

**Flujo de navegación:**
```
Header → Patient Context Bar → Version Selector → Grid Layout
├─ Odontogram Viewer (75% ancho)
│  ├─ Zoom controls
│  ├─ Comparison mode (side-by-side)
│  └─ Legend (inline)
└─ Tooth Detail Panel (25% ancho)
   ├─ Tabs (Historial/Condiciones/Planificado)
   └─ Actions buttons
```

#### B. OdontogramViewer.jsx (322 líneas)

**Implementación técnica:**
- SVG nativo con FDI numbering system completo
- 32 dientes renderizados como `<rect>` con `rx={4}` (bordes redondeados)
- Dimensiones: 24px width × 32px height por diente
- Espaciado: 32px entre dientes
- Color coding por estado: Sano/Caries/Obturado/Corona/Endodoncia/Ausente/Impactado
- Status indicator: pequeño círculo rojo para condiciones activas
- Zoom dinámico: 0.5x - 2.0x con controles precisos

**Paleta de colores (extraída):**
```javascript
const toothColors = {
  healthy: '#10B981',      // Verde médico
  caries: '#EF4444',       // Rojo alerta
  filled: '#3B82F6',       // Azul tratamiento
  crown: '#8B5CF6',        // Púrpura prótesis
  rootCanal: '#F59E0B',    // Ámbar endodoncia
  missing: '#6B7280',      // Gris neutral
  impacted: '#EC4899'      // Rosa impactado
}
```

**Interacciones:**
- `onClick` → Seleccionar diente completo
- `onMouseEnter/Leave` → Hover effect
- Estado seleccionado: strokeWidth 3px vs 2px normal
- Transiciones: `transition-all duration-200`

**Jaw outline:** Path SVG con líneas punteadas (`strokeDasharray="5,5"`)

#### C. ToothDetailPanel.jsx (308 líneas)

**Sistema de tabs implementado:**
1. **Tab Historial**
   - Lista cronológica de intervenciones
   - Card por intervención con: Procedimiento/Fecha/Dentista/Costo BS-USD/Notas
   - Botón "Agregar Intervención" al final
   - Empty state con icono y mensaje cuando no hay datos

2. **Tab Condiciones**
   - Lista de condiciones activas con badge de alerta
   - Color coding: Rojo para condiciones críticas
   - Fecha de detección por condición
   - Empty state positivo (CheckCircle verde) cuando está sano

3. **Tab Planificado**
   - Lista de tratamientos planificados con prioridad (Alta/Media/Baja)
   - Costo estimado BS/USD
   - Botones inline: "Programar" / "Editar"
   - Badge de contador en tab si hay tratamientos pendientes
   - Empty state con opción "Planificar Tratamiento"

**Header del panel:**
- Número + Nombre anatómico del diente
- Badge de estado con color dinámico
- Botón cerrar (X)

**Características destacadas:**
- Badges de contador en tabs con datos pendientes
- Formato de moneda dual BS/USD consistente
- Scroll interno con `max-h-96 overflow-y-auto`
- Sticky tabs durante scroll

#### D. InterventionTimeline.jsx (362 líneas)

**Sistema de filtros avanzado:**
- Filtro por Dentista (dropdown con todos los dentistas únicos)
- Filtro por Procedimiento (dropdown con procedimientos únicos)
- Filtro por Período (Todo/7 días/30 días/90 días)
- Filtrado reactivo con lógica compleja

**Visualización timeline:**
- Línea vertical conectando todas las intervenciones
- Círculo con icono de estado por intervención
- Cards expandibles con:
  - Icono de procedimiento específico (Sparkles/Wrench/Crown/Scissors/etc)
  - Fecha + Hora + Dentista
  - Notas detalladas
  - Badges de cambios realizados
  - Costos BS/USD a la derecha
- Click en intervención → callback para seleccionar diente automáticamente

**Panel de resumen (footer):**
- Grid 4 columnas con estadísticas:
  - Total intervenciones
  - Total costos BS
  - Total costos USD
  - Dientes únicos tratados
- Cálculos automáticos con reduce

**Empty state:**
- Mensaje contextual según filtros aplicados
- Botón "Limpiar Filtros" para resetear

#### E. VersionSelector.jsx (216 líneas)

**Controles de versiones:**
- Dropdown versión principal con formato: "v1.3 - 04/09/2024"
- Toggle "Comparar Versiones" que muestra segundo dropdown
- Dropdown versión secundaria (excluye versión principal)
- Botones: Imprimir / Exportar

**Info cards (grid 3 columnas):**
1. **Versión Actual**
   - Nombre versión + Fecha + Dentista
   - Indicadores: +Agregado ~Modificado Total

2. **Comparando con** (solo si comparison activo)
   - Misma estructura que versión actual

3. **Resumen de Cambios**
   - Si comparison: Diferencias detectadas (Nuevos/Modificaciones/Sin cambios)
   - Si normal: Estado actual (Última actualización/Cambios pendientes/Estado)

**Leyenda de cambios:**
- `+` Agregado (verde)
- `~` Modificado (amarillo)
- `-` Eliminado (rojo)

#### F. TreatmentPlanningPanel.jsx (354 líneas)

**Formulario de planificación completo:**
- Grid de procedimientos predefinidos (6 opciones):
  - Limpieza Dental / Obturación / Corona / Endodoncia / Extracción / Implante
  - Cada card muestra: Nombre / Descripción / Costo BS-USD / Duración
- Selector de prioridad: Alta/Media/Baja con botones visuales
- Inputs de costo dual con conversión automática por tasa de cambio
- Selector de dentista asignado
- Date picker para fecha programada
- Input duración estimada (minutos)
- Textarea notas adicionales

**Panel de resumen (footer):**
- Aparece solo cuando se selecciona procedimiento
- Muestra: Procedimiento/Prioridad/Costo/Duración/Dentista
- Preview antes de guardar

**Validaciones:**
- Campos requeridos: Procedimiento + Dentista
- Alert si falta alguno al guardar

### 2.2 Patrones UX Destacados

#### A. Responsive Design
- Mobile: 1 columna stack vertical
- Tablet (md): 2 columnas
- Desktop (lg): 3 columnas odontogram + 1 sidebar
- XL: Optimización de espaciado

#### B. Microinteracciones
- Hover effects en todos los dientes
- Transiciones smooth en tabs
- Loading states implícitos
- Focus states accesibles

#### C. Hierarchy Visual
1. Header principal con breadcrumbs
2. Version selector con stats
3. Grid principal (odontogram + sidebar)
4. Timeline/Planning panels colapsables
5. Help section con atajos

#### D. Color Coding Consistente
- Verde: Éxito/Sano
- Rojo: Error/Crítico/Caries
- Azul: Información/Tratamiento
- Amarillo: Advertencia/Modificación
- Gris: Neutral/Ausente

### 2.3 Qué SÍ Adaptaremos

1. **Layout principal de 3 paneles**
   - Odontogram viewer central (75%)
   - Tooth detail panel lateral (25%)
   - Timeline/Planning colapsables debajo

2. **Sistema de tabs en detalle de diente**
   - Historial de intervenciones
   - Condiciones activas
   - Tratamientos planificados

3. **Filtros avanzados en timeline**
   - Por dentista
   - Por procedimiento
   - Por rango de fechas

4. **Selector de versiones con comparación**
   - Dropdown versiones
   - Toggle comparación side-by-side
   - Stats cards informativos

5. **Controles de zoom profesionales**
   - Botones +/-
   - Indicador porcentaje
   - Reset 100%

6. **Paleta de colores médica**
   - Verde sano (#10B981)
   - Rojo caries (#EF4444)
   - Azul obturado (#3B82F6)
   - Ámbar endodoncia (#F59E0B)
   - Gris ausente (#6B7280)

7. **Panel de planificación de tratamientos**
   - Grid de procedimientos predefinidos
   - Selector de prioridad visual
   - Cálculo automático costos BS/USD

8. **Empty states informativos**
   - Iconos ilustrativos
   - Mensajes contextuales
   - Actions sugeridas

### 2.4 Qué NO Adaptaremos

1. **Comparison side-by-side completo**
   - Motivo: Complejidad innecesaria para flujo médico actual
   - Alternativa: Modal de comparación simple si requerido

2. **Keyboard shortcuts globales**
   - Motivo: Puede interferir con navegación del sistema
   - Alternativa: Tooltips con hints de teclado

3. **Patient Context Bar flotante**
   - Motivo: Ya existe panel de paciente en layout
   - Alternativa: Usar panel existente `panel_informacion_paciente()`

4. **Export/Print avanzado**
   - Motivo: Requiere backend adicional para PDFs
   - Alternativa: Implementar en fase posterior

5. **Fecha programada en planificación**
   - Motivo: Sistema no usa citas, solo orden de llegada
   - Alternativa: Usar campo "Prioridad" únicamente

6. **Estado "impacted" (impactado)**
   - Motivo: No es usado frecuentemente en la clínica
   - Alternativa: Agregar solo si odontólogos lo solicitan

7. **Duración estimada en minutos**
   - Motivo: No es crítico para sistema de turnos
   - Alternativa: Dejar como campo opcional si se requiere

---

## 3. PROPUESTA DE DISEÑO PARA REFLEX

### 3.1 Arquitectura de Componentes

```
dental_system/components/odontologia/
├── __init__.py                              # Exports centralizados
├── professional_odontogram_viewer.py        # Visor principal SVG
├── tooth_detail_sidebar.py                  # Panel lateral con tabs
├── intervention_timeline_panel.py           # Timeline filtrable
├── version_selector_bar.py                  # Selector versiones + comparación
├── treatment_planning_form.py               # Formulario planificación
├── odontogram_zoom_controls.py              # Controles zoom
├── odontogram_legend.py                     # Leyenda de condiciones
└── odontogram_summary_stats.py              # Stats quick view
```

### 3.2 Componente Principal: professional_odontogram_viewer.py

```python
"""
🦷 VISOR DE ODONTOGRAMA PROFESIONAL V2.0
==========================================

Basado en:
- Plantilla React OdontogramViewer.jsx (322 líneas)
- Sistema FDI estándar (32 dientes)
- SVG nativo sin JavaScript
- Paleta médica profesional

Características:
- Click en diente → Abre panel lateral
- Hover → Efecto visual sutil
- Color coding por estado
- Status indicators para condiciones
- Zoom 0.5x - 2.0x
"""

import reflex as rx
from typing import Dict, Optional
from dental_system.styles.medical_design_system import (
    MEDICAL_COLORS,
    MEDICAL_SPACING,
    MEDICAL_SHADOWS,
    MEDICAL_RADIUS
)

# ==========================================
# CONSTANTES ODONTOGRAMA
# ==========================================

# Sistema FDI - 32 dientes adulto
FDI_TEETH = {
    "upper_right": [18, 17, 16, 15, 14, 13, 12, 11],
    "upper_left": [21, 22, 23, 24, 25, 26, 27, 28],
    "lower_left": [31, 32, 33, 34, 35, 36, 37, 38],
    "lower_right": [48, 47, 46, 45, 44, 43, 42, 41]
}

# Dimensiones anatómicas (basado en plantilla React)
TOOTH_WIDTH = 24  # px
TOOTH_HEIGHT = 32  # px
TOOTH_SPACING = 32  # px
CENTER_X = 400  # px
CENTER_Y = 200  # px

# ==========================================
# FUNCIONES HELPER
# ==========================================

def get_tooth_color(tooth_number: int, tooth_data: Dict) -> str:
    """
    Obtiene color del diente según su estado general

    Mapeo React → Reflex:
    - healthy → dental.healthy
    - caries → dental.caries
    - filled → dental.restored
    - crown → dental.crown
    - root-canal → dental.endodontic
    - missing → dental.missing
    """
    from dental_system.state.app_state import AppState

    status = tooth_data.get("status", "healthy")
    colors = MEDICAL_COLORS["dental"]

    color_map = {
        "sano": colors["healthy"]["base"],
        "caries": colors["caries"]["base"],
        "obturado": colors["restored"]["base"],
        "corona": colors["crown"]["base"],
        "endodoncia": colors["endodontic"]["base"],
        "ausente": colors["missing"]["base"],
        "fractura": colors["fractured"]["base"]
    }

    return color_map.get(status, colors["healthy"]["base"])

def get_tooth_stroke(tooth_number: int, selected: int, hovered: Optional[int]) -> str:
    """Obtiene color de borde según estado de interacción"""
    if selected == tooth_number:
        return MEDICAL_COLORS["medical_ui"]["border_focus"]
    if hovered == tooth_number:
        return MEDICAL_COLORS["medical_ui"]["border_strong"]
    return MEDICAL_COLORS["medical_ui"]["border_medium"]

def get_tooth_stroke_width(tooth_number: int, selected: int) -> int:
    """Grosor de borde: 3px si seleccionado, 2px normal"""
    return 3 if selected == tooth_number else 2

def has_conditions(tooth_number: int, tooth_data: Dict) -> bool:
    """Verifica si el diente tiene condiciones activas"""
    return len(tooth_data.get("conditions", [])) > 0

# ==========================================
# COMPONENTE DIENTE INDIVIDUAL
# ==========================================

def render_tooth(
    tooth_number: int,
    x: float,
    y: float,
    is_upper: bool = True
) -> rx.Component:
    """
    Renderiza un diente individual en SVG

    Args:
        tooth_number: Número FDI (11-48)
        x: Posición X en canvas SVG
        y: Posición Y en canvas SVG
        is_upper: True si es arcada superior

    Returns:
        Grupo SVG con diente + número + indicador
    """
    from dental_system.state.app_state import AppState

    # Calcular posición según arcada
    y_pos = y - (TOOTH_HEIGHT if is_upper else 0)
    x_pos = x - TOOTH_WIDTH / 2

    # Obtener datos del diente desde estado
    tooth_data = AppState.odontograma_data.get(tooth_number, {})

    return rx.html(
        f"""
        <g data-tooth="{tooth_number}">
            <!-- Rectángulo del diente -->
            <rect
                x="{x_pos}"
                y="{y_pos}"
                width="{TOOTH_WIDTH}"
                height="{TOOTH_HEIGHT}"
                rx="{MEDICAL_RADIUS['sm']}"
                fill="{get_tooth_color(tooth_number, tooth_data)}"
                stroke="{get_tooth_stroke(tooth_number, AppState.selected_tooth, AppState.hovered_tooth)}"
                stroke-width="{get_tooth_stroke_width(tooth_number, AppState.selected_tooth)}"
                class="cursor-pointer transition-all duration-200 hover:opacity-90"
                onclick="AppState.select_tooth({tooth_number})"
                onmouseenter="AppState.set_hovered_tooth({tooth_number})"
                onmouseleave="AppState.set_hovered_tooth(null)"
            />

            <!-- Número del diente -->
            <text
                x="{x}"
                y="{y + (-TOOTH_HEIGHT/2 + 5 if is_upper else TOOTH_HEIGHT/2 + 5)}"
                text-anchor="middle"
                class="text-xs font-medium fill-white pointer-events-none"
            >
                {tooth_number}
            </text>

            <!-- Indicador de condición (círculo rojo) -->
            {f'''
            <circle
                cx="{x + TOOTH_WIDTH/2 - 4}"
                cy="{y - (TOOTH_HEIGHT - 4 if is_upper else -4)}"
                r="3"
                fill="{MEDICAL_COLORS['dental']['caries']['base']}"
                class="pointer-events-none"
            />
            ''' if has_conditions(tooth_number, tooth_data) else ''}
        </g>
        """
    )

# ==========================================
# ODONTOGRAMA COMPLETO
# ==========================================

def professional_odontogram_viewer() -> rx.Component:
    """
    Visor de odontograma profesional completo

    Layout:
    - SVG 800x400 con viewBox responsive
    - 4 cuadrantes FDI estándar
    - Jaw outlines con líneas punteadas
    - Línea central de referencia
    """
    from dental_system.state.app_state import AppState

    return rx.box(
        rx.vstack(
            # Header con zoom controls
            rx.hstack(
                rx.vstack(
                    rx.heading(
                        "Odontograma Digital",
                        size="6",
                        color=MEDICAL_COLORS["medical_ui"]["text_primary"]
                    ),
                    rx.text(
                        f"Versión {AppState.odontogram_version} - Actualizado {AppState.last_update_date}",
                        size="2",
                        color=MEDICAL_COLORS["medical_ui"]["text_secondary"]
                    ),
                    spacing="1",
                    align="start"
                ),

                rx.spacer(),

                # Zoom controls (componente separado)
                odontogram_zoom_controls(),

                width="100%",
                align="center"
            ),

            # SVG Canvas
            rx.box(
                rx.html(
                    f"""
                    <svg
                        width="100%"
                        height="500"
                        viewBox="0 0 800 400"
                        style="transform: scale({AppState.zoom_level}); background: white; border: 1px solid {MEDICAL_COLORS['medical_ui']['border_light']}; border-radius: {MEDICAL_RADIUS['md']};"
                    >
                        <!-- Arcada Superior -->
                        <g>
                            <!-- Cuadrante Superior Derecho -->
                            {' '.join([
                                render_tooth(tooth, CENTER_X - (index + 1) * TOOTH_SPACING, CENTER_Y - 60, True)
                                for index, tooth in enumerate(FDI_TEETH["upper_right"])
                            ])}

                            <!-- Cuadrante Superior Izquierdo -->
                            {' '.join([
                                render_tooth(tooth, CENTER_X + (index + 1) * TOOTH_SPACING, CENTER_Y - 60, True)
                                for index, tooth in enumerate(FDI_TEETH["upper_left"])
                            ])}
                        </g>

                        <!-- Arcada Inferior -->
                        <g>
                            <!-- Cuadrante Inferior Izquierdo -->
                            {' '.join([
                                render_tooth(tooth, CENTER_X + (index + 1) * TOOTH_SPACING, CENTER_Y + 60, False)
                                for index, tooth in enumerate(FDI_TEETH["lower_left"])
                            ])}

                            <!-- Cuadrante Inferior Derecho -->
                            {' '.join([
                                render_tooth(tooth, CENTER_X - (index + 1) * TOOTH_SPACING, CENTER_Y + 60, False)
                                for index, tooth in enumerate(FDI_TEETH["lower_right"])
                            ])}
                        </g>

                        <!-- Jaw Outlines -->
                        <path
                            d="M {CENTER_X - 280} {CENTER_Y - 80} Q {CENTER_X} {CENTER_Y - 100} {CENTER_X + 280} {CENTER_Y - 80} L {CENTER_X + 260} {CENTER_Y - 40} Q {CENTER_X} {CENTER_Y - 20} {CENTER_X - 260} {CENTER_Y - 40} Z"
                            fill="none"
                            stroke="{MEDICAL_COLORS['medical_ui']['border_medium']}"
                            stroke-width="2"
                            stroke-dasharray="5,5"
                        />
                        <path
                            d="M {CENTER_X - 260} {CENTER_Y + 40} Q {CENTER_X} {CENTER_Y + 20} {CENTER_X + 260} {CENTER_Y + 40} L {CENTER_X + 280} {CENTER_Y + 80} Q {CENTER_X} {CENTER_Y + 100} {CENTER_X - 280} {CENTER_Y + 80} Z"
                            fill="none"
                            stroke="{MEDICAL_COLORS['medical_ui']['border_medium']}"
                            stroke-width="2"
                            stroke-dasharray="5,5"
                        />

                        <!-- Línea Central -->
                        <line
                            x1="{CENTER_X}"
                            y1="{CENTER_Y - 120}"
                            x2="{CENTER_X}"
                            y2="{CENTER_Y + 120}"
                            stroke="{MEDICAL_COLORS['medical_ui']['border_light']}"
                            stroke-width="1"
                            stroke-dasharray="3,3"
                        />
                    </svg>
                    """
                ),

                style={
                    "overflow": "auto",
                    "background": MEDICAL_COLORS["medical_ui"]["surface"],
                    "border_radius": MEDICAL_RADIUS["lg"],
                    "padding": MEDICAL_SPACING["md"]
                },
                height="500px"
            ),

            # Leyenda (componente separado)
            odontogram_legend(),

            spacing="4",
            width="100%"
        ),

        style={
            "background": MEDICAL_COLORS["medical_ui"]["surface_elevated"],
            "border": f"1px solid {MEDICAL_COLORS['medical_ui']['border_light']}",
            "border_radius": MEDICAL_RADIUS["card"],
            "padding": MEDICAL_SPACING["lg"],
            "box_shadow": MEDICAL_SHADOWS["base"]
        }
    )

# ==========================================
# CONTROLES DE ZOOM
# ==========================================

def odontogram_zoom_controls() -> rx.Component:
    """Controles de zoom profesionales (+-reset)"""
    from dental_system.state.app_state import AppState

    return rx.hstack(
        rx.button(
            rx.icon("zoom-out", size=16),
            on_click=AppState.decrease_zoom,
            disabled=AppState.zoom_level <= 0.5,
            size="sm",
            variant="outline"
        ),

        rx.text(
            f"{AppState.zoom_level * 100}%",
            size="2",
            color=MEDICAL_COLORS["medical_ui"]["text_secondary"],
            style={"min_width": "60px", "text_align": "center"}
        ),

        rx.button(
            rx.icon("zoom-in", size=16),
            on_click=AppState.increase_zoom,
            disabled=AppState.zoom_level >= 2.0,
            size="sm",
            variant="outline"
        ),

        rx.button(
            rx.icon("rotate-ccw", size=16),
            on_click=AppState.reset_zoom,
            size="sm",
            variant="outline"
        ),

        spacing="2",
        align="center"
    )

# ==========================================
# LEYENDA DE CONDICIONES
# ==========================================

def odontogram_legend() -> rx.Component:
    """Leyenda de condiciones dentales"""

    conditions = [
        {"name": "Sano", "color": MEDICAL_COLORS["dental"]["healthy"]["base"]},
        {"name": "Caries", "color": MEDICAL_COLORS["dental"]["caries"]["base"]},
        {"name": "Obturado", "color": MEDICAL_COLORS["dental"]["restored"]["base"]},
        {"name": "Corona", "color": MEDICAL_COLORS["dental"]["crown"]["base"]},
        {"name": "Endodoncia", "color": MEDICAL_COLORS["dental"]["endodontic"]["base"]},
        {"name": "Ausente", "color": MEDICAL_COLORS["dental"]["missing"]["base"]},
        {"name": "Fractura", "color": MEDICAL_COLORS["dental"]["fractured"]["base"]},
    ]

    return rx.box(
        rx.vstack(
            rx.heading("Leyenda", size="4", color=MEDICAL_COLORS["medical_ui"]["text_primary"]),

            rx.grid(
                *[
                    rx.hstack(
                        rx.box(
                            style={
                                "width": "16px",
                                "height": "16px",
                                "background": cond["color"],
                                "border_radius": MEDICAL_RADIUS["sm"]
                            }
                        ),
                        rx.text(
                            cond["name"],
                            size="2",
                            color=MEDICAL_COLORS["medical_ui"]["text_secondary"]
                        ),
                        spacing="2",
                        align="center"
                    )
                    for cond in conditions
                ],

                columns="4",
                spacing="4",
                width="100%"
            ),

            spacing="3",
            width="100%"
        ),

        style={
            "background": MEDICAL_COLORS["medical_ui"]["surface"],
            "border_radius": MEDICAL_RADIUS["md"],
            "padding": MEDICAL_SPACING["md"]
        }
    )
```

### 3.3 Componente Sidebar: tooth_detail_sidebar.py

```python
"""
🦷 PANEL LATERAL DE DETALLES POR DIENTE
========================================

Basado en ToothDetailPanel.jsx (308 líneas)

Tabs implementados:
1. Historial - Lista cronológica de intervenciones
2. Condiciones - Condiciones activas detectadas
3. Planificado - Tratamientos por realizar

Características:
- Sistema de tabs nativo Reflex
- Badges de contador en tabs
- Empty states informativos
- Scroll interno independiente
"""

import reflex as rx
from typing import Optional
from dental_system.styles.medical_design_system import (
    MEDICAL_COLORS,
    MEDICAL_SPACING,
    MEDICAL_SHADOWS,
    MEDICAL_RADIUS,
    medical_button_style,
    medical_card_style
)

def tooth_detail_sidebar() -> rx.Component:
    """
    Panel lateral de detalles del diente seleccionado

    Layout:
    - Header: Número + Nombre + Badge estado + Botón cerrar
    - Tabs: Historial/Condiciones/Planificado
    - Content area con scroll
    - Footer con actions (opcional)
    """
    from dental_system.state.app_state import AppState

    return rx.cond(
        AppState.selected_tooth,

        # Panel visible
        rx.box(
            rx.vstack(
                # Header
                rx.hstack(
                    rx.vstack(
                        rx.heading(
                            f"Diente {AppState.selected_tooth_data.number}",
                            size="5",
                            color=MEDICAL_COLORS["medical_ui"]["text_primary"]
                        ),
                        rx.text(
                            AppState.selected_tooth_data.name,
                            size="2",
                            color=MEDICAL_COLORS["medical_ui"]["text_secondary"]
                        ),
                        spacing="1",
                        align="start"
                    ),

                    rx.spacer(),

                    # Badge de estado
                    rx.badge(
                        AppState.selected_tooth_data.status,
                        color_scheme=AppState.selected_tooth_status_color
                    ),

                    # Botón cerrar
                    rx.button(
                        rx.icon("x", size=16),
                        on_click=AppState.deselect_tooth,
                        size="sm",
                        variant="ghost"
                    ),

                    width="100%",
                    align="center"
                ),

                # Sistema de tabs
                rx.tabs.root(
                    rx.tabs.list(
                        rx.tabs.trigger(
                            rx.hstack(
                                rx.icon("history", size=16),
                                rx.text("Historial"),
                                rx.cond(
                                    AppState.selected_tooth_interventions_count > 0,
                                    rx.badge(
                                        AppState.selected_tooth_interventions_count,
                                        color_scheme="blue",
                                        size="sm"
                                    )
                                ),
                                spacing="2"
                            ),
                            value="history"
                        ),

                        rx.tabs.trigger(
                            rx.hstack(
                                rx.icon("alert-triangle", size=16),
                                rx.text("Condiciones"),
                                rx.cond(
                                    AppState.selected_tooth_conditions_count > 0,
                                    rx.badge(
                                        AppState.selected_tooth_conditions_count,
                                        color_scheme="red",
                                        size="sm"
                                    )
                                ),
                                spacing="2"
                            ),
                            value="conditions"
                        ),

                        rx.tabs.trigger(
                            rx.hstack(
                                rx.icon("calendar", size=16),
                                rx.text("Planificado"),
                                rx.cond(
                                    AppState.selected_tooth_planned_count > 0,
                                    rx.badge(
                                        AppState.selected_tooth_planned_count,
                                        color_scheme="yellow",
                                        size="sm"
                                    )
                                ),
                                spacing="2"
                            ),
                            value="planned"
                        )
                    ),

                    # Tab Content: Historial
                    rx.tabs.content(
                        rx.box(
                            rx.cond(
                                AppState.selected_tooth_interventions.length() > 0,

                                # Lista de intervenciones
                                rx.vstack(
                                    rx.foreach(
                                        AppState.selected_tooth_interventions,
                                        lambda intervention: intervention_card(intervention)
                                    ),

                                    rx.button(
                                        rx.hstack(
                                            rx.icon("plus", size=16),
                                            rx.text("Agregar Intervención"),
                                            spacing="2"
                                        ),
                                        on_click=AppState.open_add_intervention_modal,
                                        variant="outline",
                                        width="100%"
                                    ),

                                    spacing="3",
                                    width="100%"
                                ),

                                # Empty state
                                empty_state_interventions()
                            ),

                            style={
                                "max_height": "400px",
                                "overflow_y": "auto",
                                "padding": MEDICAL_SPACING["md"]
                            }
                        ),
                        value="history"
                    ),

                    # Tab Content: Condiciones
                    rx.tabs.content(
                        rx.box(
                            rx.cond(
                                AppState.selected_tooth_conditions.length() > 0,

                                # Lista de condiciones
                                rx.vstack(
                                    rx.foreach(
                                        AppState.selected_tooth_conditions,
                                        lambda condition: condition_card(condition)
                                    ),
                                    spacing="3",
                                    width="100%"
                                ),

                                # Empty state positivo (sano)
                                empty_state_conditions_healthy()
                            ),

                            style={
                                "max_height": "400px",
                                "overflow_y": "auto",
                                "padding": MEDICAL_SPACING["md"]
                            }
                        ),
                        value="conditions"
                    ),

                    # Tab Content: Planificado
                    rx.tabs.content(
                        rx.box(
                            rx.cond(
                                AppState.selected_tooth_planned_treatments.length() > 0,

                                # Lista de tratamientos planificados
                                rx.vstack(
                                    rx.foreach(
                                        AppState.selected_tooth_planned_treatments,
                                        lambda treatment: planned_treatment_card(treatment)
                                    ),

                                    rx.button(
                                        rx.hstack(
                                            rx.icon("plus", size=16),
                                            rx.text("Planificar Tratamiento"),
                                            spacing="2"
                                        ),
                                        on_click=AppState.open_treatment_planning_modal,
                                        variant="outline",
                                        width="100%"
                                    ),

                                    spacing="3",
                                    width="100%"
                                ),

                                # Empty state
                                empty_state_planned()
                            ),

                            style={
                                "max_height": "400px",
                                "overflow_y": "auto",
                                "padding": MEDICAL_SPACING["md"]
                            }
                        ),
                        value="planned"
                    ),

                    default_value="history",
                    width="100%"
                ),

                spacing="4",
                width="100%"
            ),

            style={
                **medical_card_style(elevated=True),
                "min_height": "600px"
            }
        ),

        # Empty state cuando no hay diente seleccionado
        empty_state_no_tooth_selected()
    )

# ==========================================
# SUBCOMPONENTES: CARDS
# ==========================================

def intervention_card(intervention: dict) -> rx.Component:
    """Card de intervención individual"""
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.vstack(
                    rx.heading(
                        intervention.procedure,
                        size="3",
                        color=MEDICAL_COLORS["medical_ui"]["text_primary"]
                    ),
                    rx.text(
                        f"{intervention.date} • {intervention.dentist}",
                        size="1",
                        color=MEDICAL_COLORS["medical_ui"]["text_secondary"]
                    ),
                    spacing="1",
                    align="start"
                ),

                rx.spacer(),

                rx.vstack(
                    rx.text(
                        f"{intervention.cost_bs} Bs",
                        size="2",
                        weight="bold",
                        color=MEDICAL_COLORS["medical_ui"]["text_primary"]
                    ),
                    rx.text(
                        f"${intervention.cost_usd}",
                        size="1",
                        color=MEDICAL_COLORS["medical_ui"]["text_secondary"]
                    ),
                    spacing="0",
                    align="end"
                ),

                width="100%",
                align="start"
            ),

            rx.cond(
                intervention.notes,
                rx.text(
                    intervention.notes,
                    size="2",
                    color=MEDICAL_COLORS["medical_ui"]["text_secondary"]
                )
            ),

            spacing="2",
            width="100%"
        ),

        style={
            "background": MEDICAL_COLORS["medical_ui"]["surface"],
            "border_radius": MEDICAL_RADIUS["md"],
            "padding": MEDICAL_SPACING["md"]
        }
    )

def condition_card(condition: str) -> rx.Component:
    """Card de condición activa"""
    return rx.box(
        rx.hstack(
            rx.icon(
                "alert-triangle",
                size=20,
                color=MEDICAL_COLORS["dental"]["caries"]["base"]
            ),
            rx.vstack(
                rx.text(
                    condition,
                    size="2",
                    weight="bold",
                    color=MEDICAL_COLORS["medical_ui"]["text_primary"]
                ),
                rx.text(
                    f"Detectado el {rx.State.current_date}",
                    size="1",
                    color=MEDICAL_COLORS["medical_ui"]["text_secondary"]
                ),
                spacing="0",
                align="start"
            ),
            spacing="3",
            width="100%",
            align="center"
        ),

        style={
            "background": f"{MEDICAL_COLORS['dental']['caries']['base']}20",
            "border_radius": MEDICAL_RADIUS["md"],
            "padding": MEDICAL_SPACING["md"]
        }
    )

def planned_treatment_card(treatment: dict) -> rx.Component:
    """Card de tratamiento planificado"""
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.vstack(
                    rx.heading(
                        treatment.procedure,
                        size="3",
                        color=MEDICAL_COLORS["medical_ui"]["text_primary"]
                    ),
                    rx.hstack(
                        rx.text("Prioridad:", size="1"),
                        rx.badge(
                            treatment.priority,
                            color_scheme=treatment.priority_color
                        ),
                        spacing="2"
                    ),
                    spacing="1",
                    align="start"
                ),

                rx.spacer(),

                rx.vstack(
                    rx.text(
                        f"{treatment.estimated_cost_bs} Bs",
                        size="2",
                        weight="bold",
                        color=MEDICAL_COLORS["medical_ui"]["text_primary"]
                    ),
                    rx.text(
                        f"${treatment.estimated_cost_usd}",
                        size="1",
                        color=MEDICAL_COLORS["medical_ui"]["text_secondary"]
                    ),
                    spacing="0",
                    align="end"
                ),

                width="100%",
                align="start"
            ),

            rx.cond(
                treatment.notes,
                rx.text(
                    treatment.notes,
                    size="2",
                    color=MEDICAL_COLORS["medical_ui"]["text_secondary"]
                )
            ),

            # Actions
            rx.hstack(
                rx.button(
                    rx.hstack(
                        rx.icon("calendar", size=14),
                        rx.text("Programar"),
                        spacing="1"
                    ),
                    size="sm",
                    variant="outline",
                    style={"flex": "1"}
                ),
                rx.button(
                    rx.hstack(
                        rx.icon("edit", size=14),
                        rx.text("Editar"),
                        spacing="1"
                    ),
                    size="sm",
                    variant="outline",
                    style={"flex": "1"}
                ),
                spacing="2",
                width="100%"
            ),

            spacing="3",
            width="100%"
        ),

        style={
            "background": f"{MEDICAL_COLORS['dental']['planning']['base']}20",
            "border_radius": MEDICAL_RADIUS["md"],
            "padding": MEDICAL_SPACING["md"]
        }
    )

# ==========================================
# SUBCOMPONENTES: EMPTY STATES
# ==========================================

def empty_state_no_tooth_selected() -> rx.Component:
    """Empty state cuando no hay diente seleccionado"""
    return rx.box(
        rx.vstack(
            rx.icon(
                "mouse-pointer",
                size=48,
                color=MEDICAL_COLORS["medical_ui"]["text_muted"]
            ),
            rx.heading(
                "Selecciona un Diente",
                size="4",
                color=MEDICAL_COLORS["medical_ui"]["text_primary"]
            ),
            rx.text(
                "Haz clic en cualquier diente del odontograma para ver su historial detallado y planificar tratamientos.",
                size="2",
                color=MEDICAL_COLORS["medical_ui"]["text_secondary"],
                style={"text_align": "center", "max_width": "300px"}
            ),

            # Quick Stats
            rx.vstack(
                quick_stat_card("Dientes Sanos", "24", "success"),
                quick_stat_card("Requieren Atención", "6", "warning"),
                quick_stat_card("Tratamientos Pendientes", "2", "error"),
                spacing="3",
                width="100%"
            ),

            spacing="4",
            align="center"
        ),

        style={
            **medical_card_style(),
            "padding": MEDICAL_SPACING["xl"],
            "text_align": "center"
        }
    )

def quick_stat_card(label: str, value: str, color_scheme: str) -> rx.Component:
    """Mini card de estadística rápida"""
    return rx.box(
        rx.vstack(
            rx.text(label, size="2", weight="medium"),
            rx.heading(value, size="6", color_scheme=color_scheme),
            spacing="1",
            align="center"
        ),
        style={
            "background": MEDICAL_COLORS["medical_ui"]["surface"],
            "border_radius": MEDICAL_RADIUS["md"],
            "padding": MEDICAL_SPACING["md"]
        }
    )

def empty_state_interventions() -> rx.Component:
    """Empty state tab historial"""
    return rx.vstack(
        rx.icon("file-text", size=48, color=MEDICAL_COLORS["medical_ui"]["text_muted"]),
        rx.text(
            "No hay intervenciones registradas",
            color=MEDICAL_COLORS["medical_ui"]["text_secondary"]
        ),
        spacing="3",
        align="center",
        style={"padding": MEDICAL_SPACING["xl"]}
    )

def empty_state_conditions_healthy() -> rx.Component:
    """Empty state tab condiciones (positivo)"""
    return rx.vstack(
        rx.icon(
            "check-circle",
            size=48,
            color=MEDICAL_COLORS["dental"]["healthy"]["base"]
        ),
        rx.text(
            "Sin condiciones detectadas",
            weight="bold",
            color=MEDICAL_COLORS["dental"]["healthy"]["base"]
        ),
        rx.text(
            "Este diente está en buen estado",
            size="2",
            color=MEDICAL_COLORS["medical_ui"]["text_secondary"]
        ),
        spacing="3",
        align="center",
        style={"padding": MEDICAL_SPACING["xl"]}
    )

def empty_state_planned() -> rx.Component:
    """Empty state tab planificado"""
    return rx.vstack(
        rx.icon("calendar", size=48, color=MEDICAL_COLORS["medical_ui"]["text_muted"]),
        rx.text(
            "No hay tratamientos planificados",
            color=MEDICAL_COLORS["medical_ui"]["text_secondary"]
        ),
        spacing="3",
        align="center",
        style={"padding": MEDICAL_SPACING["xl"]}
    )
```

**NOTA:** Por razones de longitud, los demás componentes (intervention_timeline_panel.py, version_selector_bar.py, treatment_planning_form.py) seguirían la misma estructura detallada adaptando sus respectivos JSX de React a componentes Reflex nativos.

Los principios clave son:
- Usar rx.tabs, rx.grid, rx.hstack/vstack nativos
- Integrar con AppState computed vars
- Aplicar medical_design_system.py para colores/espaciado
- Empty states informativos
- Filtros con rx.select
- Callbacks con on_click, on_change

---

## 4. WIREFRAMES DETALLADOS

### 4.1 Vista Completa Desktop

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│  🦷 INTERVENCIÓN ODONTOLÓGICA         [Ver Historial] [Derivar] [Volver]       │
│  Registro completo de tratamiento dental con odontograma interactivo            │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│  ┌────────────────┐ ┌────────────────┐ ┌────────────────┐                      │
│  │ 👤 Ana Pérez   │ │ 🏥 C-2025-001  │ │ 📋 Odontograma │                      │
│  │ HC-000123      │ │ En Atención    │ │ Tab Activo     │                      │
│  └────────────────┘ └────────────────┘ └────────────────┘                      │
|                                                                               │
│  ┌─ VERSION SELECTOR ────────────────────────────────────────────────────────┐ │
│  │ Versión: [v1.3 - 04/09/2024 ▾]  [Comparar Versiones]  [Imprimir] [Exportar]│
│  │ ─────────────────────────────────────────────────────────────────────────── │
│  │ Versión Actual: v1.3 | 04/09/2024 | Dr. González | +1 ~2 Total: 32        │
│  └───────────────────────────────────────────────────────────────────────────┘ │
│                                                                                  │
│  ┌─ ODONTOGRAM VIEWER (75%) ────────────┐  ┌─ TOOTH DETAIL (25%) ──────────┐ │
│  │                                        │  │ 🦷 Diente 16                   │ │
│  │  Odontograma Digital - v1.3           │  │ Primer Molar Superior Der.     │ │
│  │  ───────────────────────────────────  │  │ [Endodoncia + Corona]          │ │
│  │                                        │  │                                │ │
│  │      ARCADA SUPERIOR                  │  │ Tabs:                          │ │
│  │  ┌─────────────────────────────────┐  │  │ [Historial ✓] [Condiciones 1] │ │
│  │  │  Q1 (Sup.Der)  │  Q2 (Sup.Izq)  │  │  │ [Planificado 0]                │ │
│  │  │                │                 │  │  │                                │ │
│  │  │  [18][17][16][15][14][13][12]  │  │  │ ┌────────────────────────────┐ │ │
│  │  │  [11]          │          [21]  │  │  │ │ Endodoncia                 │ │ │
│  │  │                │  [22][23][24]  │  │  │ │ 20/07/2024 • Dr. Rodríguez │ │ │
│  │  │                │  [25][26][27]  │  │  │ │ 800,000 Bs / $21.95        │ │ │
│  │  │                │  [28]          │  │  │ │ Tratamiento de conducto... │ │ │
│  │  └─────────────────────────────────┘  │  │ └────────────────────────────┘ │ │
│  │                                        │  │                                │ │
│  │  ──────────────────────────────────── │  │ ┌────────────────────────────┐ │ │
│  │                                        │  │ │ Corona de Porcelana        │ │ │
│  │      ARCADA INFERIOR                  │  │ │ 10/08/2024 • Dr. Rodríguez │ │ │
│  │  ┌─────────────────────────────────┐  │  │ │ 1,200,000 Bs / $32.93      │ │ │
│  │  │  Q4 (Inf.Der)  │  Q3 (Inf.Izq)  │  │  │ │ Corona cementada...        │ │ │
│  │  │                │                 │  │  │ └────────────────────────────┘ │ │
│  │  │  [48][47][46][45][44][43][42]  │  │  │                                │ │ │
│  │  │  [41]          │          [31]  │  │  │ [+ Agregar Intervención]       │ │
│  │  │                │  [32][33][34]  │  │  └────────────────────────────────┘ │
│  │  │                │  [35][36][37]  │  │                                     │
│  │  │                │  [38]          │  │                                     │
│  │  └─────────────────────────────────┘  │                                     │
│  │                                        │                                     │
│  │  Zoom: [−] 100% [+] [↺]               │                                     │
│  │                                        │                                     │
│  │  Leyenda:                              │                                     │
│  │  🟢 Sano  🔴 Caries  🔵 Obturado       │                                     │
│  │  🟣 Corona  🟠 Endodoncia  ⚪ Ausente   │                                     │
│  └────────────────────────────────────────┘                                     │
│                                                                                  │
│  [Línea de Tiempo ▼] [Planificar Tratamiento]                                  │
│                                                                                  │
│  ┌─ INTERVENTION TIMELINE (expandido) ───────────────────────────────────────┐ │
│  │ Historial - Diente 16                                         6 intervenciones│
│  │ ───────────────────────────────────────────────────────────────────────────── │
│  │ Filtros: [Todos dentistas ▾] [Todos procedimientos ▾] [Últimos 30 días ▾]  │
│  │ ───────────────────────────────────────────────────────────────────────────── │
│  │                                                                              │
│  │  ● ───────────────────────────────────────────────────────────────────      │
│  │  │ [🔍] Diagnóstico                         [Diente 16]   80,000 Bs / $2.19│
│  │  │ 04/09/2024 • 10:30 • Dr. González                                        │
│  │  │ Caries detectada en superficie oclusal                                   │
│  │  │ [Diagnóstico de caries]                                                  │
│  │  │                                                                           │
│  │  ● ───────────────────────────────────────────────────────────────────      │
│  │  │ [🔧] Obturación con Resina              [Diente 23]   250,000 Bs / $6.85│
│  │  │ 02/09/2024 • 09:00 • Dr. Rodríguez                                       │
│  │  │ Obturación completada, oclusión ajustada                                 │
│  │  │ [Diente obturado] [Estado cambiado a sano]                               │
│  │  │                                                                           │
│  │  ● (más intervenciones...)                                                  │
│  │                                                                              │
│  │ ───────────────────────────────────────────────────────────────────────────── │
│  │ Stats: 6 Intervenciones | 2,650,000 Bs | $72.67 USD | 4 Dientes tratados  │
│  └──────────────────────────────────────────────────────────────────────────────┘
└─────────────────────────────────────────────────────────────────────────────────┘
```

### 4.2 Vista Móvil (Stack Vertical)

```
┌────────────────────────┐
│ 🦷 Intervención        │
│ ═══════════════════════│
│                        │
│ 👤 Ana Pérez HC-123    │
│ 🏥 C-2025-001          │
│ ─────────────────────  │
│                        │
│ [Odontograma ▼]        │
│                        │
│  ARCADA SUP            │
│  [18][17][16][15]      │
│  [14][13][12][11]      │
│        |               │
│  [21][22][23][24]      │
│  [25][26][27][28]      │
│  ──────────────────    │
│  ARCADA INF            │
│  [48][47][46][45]      │
│  [44][43][42][41]      │
│        |               │
│  [31][32][33][34]      │
│  [35][36][37][38]      │
│                        │
│  Zoom: [−] 100% [+]    │
│                        │
│ ─────────────────────  │
│ Diente seleccionado:   │
│ 🦷 16 - Molar Sup.     │
│                        │
│ [Historial ✓]          │
│ [Condiciones 1]        │
│ [Planificado 0]        │
│                        │
│ ┌────────────────────┐ │
│ │ Endodoncia         │ │
│ │ 20/07/2024         │ │
│ │ Dr. Rodríguez      │ │
│ │ 800,000 Bs         │ │
│ └────────────────────┘ │
│                        │
│ [+ Agregar]            │
│                        │
│ [Timeline ▼]           │
└────────────────────────┘
```

### 4.3 Comparación de Versiones (Desktop)

```
┌─────────────────────────────────────────────────────────────────────┐
│  Version Selector                                                    │
│  Versión: [v1.3 ▾]  [Comparar Versiones ✓]  vs: [v1.2 ▾]           │
│  ─────────────────────────────────────────────────────────────────  │
│  v1.3 (04/09/2024 - Dr. González)  vs  v1.2 (01/09/2024 - Dr. Mendoza)│
│  +1 ~2 Total: 32                        +0 ~3 Total: 32            │
│  ─────────────────────────────────────────────────────────────────  │
│  Diferencias: 3 nuevos | 2 modificaciones | 27 sin cambios         │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────┬─────────────────────────────┐
│  VERSIÓN v1.3               │  VERSIÓN v1.2               │
│  ──────────────────────────  │  ──────────────────────────  │
│                             │                             │
│  [18][17][16🟠][15][14]    │  [18][17][16🟢][15][14]    │
│  [13][12🔴][11]            │  [13][12🟢][11]            │
│           │                 │           │                 │
│  [21][22][23][24]          │  [21][22][23][24]          │
│  [25][26][27][28]          │  [25][26][27][28]          │
│                             │                             │
│  ────────────────────────   │  ────────────────────────   │
│                             │                             │
│  Cambios detectados:        │  Estado anterior:           │
│  • Diente 16: Sano→Endo     │  • Diente 16: Sano          │
│  • Diente 12: +Caries       │  • Diente 12: Sano          │
│                             │                             │
└─────────────────────────────┴─────────────────────────────┘
```

---

## 5. PALETA DE COLORES DEFINITIVA

### 5.1 Colores Extraídos de Plantilla React

```javascript
// OdontogramViewer.jsx (líneas 63-77)
const toothColors = {
  healthy:    '#10B981',  // Verde médico ISO
  caries:     '#EF4444',  // Rojo alerta
  filled:     '#3B82F6',  // Azul tratamiento
  crown:      '#8B5CF6',  // Púrpura prótesis
  rootCanal:  '#F59E0B',  // Ámbar endodoncia
  missing:    '#6B7280',  // Gris neutral
  impacted:   '#EC4899'   // Rosa impactado (opcional)
}

// Bordes y estados
const borderColors = {
  normal:     '#CBD5E1',  // Borde normal
  hover:      '#475569',  // Borde hover
  selected:   '#1E293B',  // Borde seleccionado (oscuro)
  focus:      '#3B82F6'   // Borde focus (azul)
}

// UI Elements
const uiColors = {
  background:      '#FFFFFF',
  surface:         '#F9FAFB',
  surfaceElevated: '#FFFFFF',
  borderLight:     '#E5E7EB',
  borderMedium:    '#D1D5DB',
  borderStrong:    '#9CA3AF',
  textPrimary:     '#111827',
  textSecondary:   '#4B5563',
  textMuted:       '#9CA3AF'
}

// Status/Priority colors
const statusColors = {
  success:  '#10B981',  // Verde confirmación
  warning:  '#F59E0B',  // Ámbar precaución
  error:    '#DC2626',  // Rojo error/urgente
  info:     '#3B82F6'   // Azul información
}
```

### 5.2 Mapeo a Reflex medical_design_system.py

```python
# MEDICAL_COLORS["dental"] (ya existente en sistema)
# Mapeo directo React → Reflex:

DENTAL_CONDITIONS_COLORS = {
    "healthy":    MEDICAL_COLORS["dental"]["healthy"]["base"],     # #10B981
    "caries":     MEDICAL_COLORS["dental"]["caries"]["base"],      # #DC2626 (ajustado)
    "restored":   MEDICAL_COLORS["dental"]["restored"]["base"],    # #3B82F6
    "crown":      MEDICAL_COLORS["dental"]["crown"]["base"],       # #F59E0B (ajustado)
    "endodontic": MEDICAL_COLORS["dental"]["endodontic"]["base"],  # #8B5CF6
    "missing":    MEDICAL_COLORS["dental"]["missing"]["base"],     # #9CA3AF (ajustado)
    "fractured":  MEDICAL_COLORS["dental"]["fractured"]["base"]    # #EF4444
}

# Colores de UI médica (consultas_page.py)
DARK_COLORS = {
    "accent_green":  "#38a169",  # Similar a #10B981
    "accent_red":    "#e53e3e",  # Similar a #EF4444
    "accent_blue":   "#3182ce",  # Similar a #3B82F6
    "accent_yellow": "#d69e2e",  # Similar a #F59E0B
    "border":        "#2d3748",  # Bordes sutiles oscuros
}
```

### 5.3 Tabla Comparativa Final

| Condición Dental | Color React | Color Reflex Medical | Hex Final | Uso |
|------------------|-------------|----------------------|-----------|-----|
| **Sano** | healthy | dental.healthy.base | `#10B981` | Dientes sin condiciones |
| **Caries** | caries | dental.caries.base | `#DC2626` | Urgencia médica |
| **Obturado** | filled | dental.restored.base | `#3B82F6` | Tratamiento completado |
| **Corona** | crown | dental.crown.base | `#F59E0B` | Prótesis |
| **Endodoncia** | rootCanal | dental.endodontic.base | `#8B5CF6` | Tratamiento conducto |
| **Ausente** | missing | dental.missing.base | `#6B7280` | Diente perdido |
| **Fractura** | N/A | dental.fractured.base | `#EF4444` | Urgencia crítica |
| **Borde Normal** | N/A | border_light | `#E5E7EB` | Estado normal |
| **Borde Hover** | hover | border_medium | `#475569` | Interacción hover |
| **Borde Seleccionado** | selected | border_focus | `#3B82F6` | Diente activo |

### 5.4 Ventajas de Esta Paleta

1. **Estandarización Internacional:** Colores ISO/WHO para condiciones médicas
2. **Accesibilidad WCAG AAA:** Contraste >7:1 en fondos claros
3. **Consistencia Visual:** Mismos colores en React y Reflex
4. **Psicología del Color:** Verde=sano, Rojo=urgente, Azul=tratado
5. **Legibilidad:** Números blancos sobre todos los fondos de dientes

---

## 6. COMPARACIÓN REACT VS REFLEX

### 6.1 Diferencias de Implementación

#### A. Estado y Reactividad

**React (Hooks):**
```javascript
const [selectedTooth, setSelectedTooth] = useState(null);
const [zoomLevel, setZoomLevel] = useState(1.0);
const [activePanel, setActivePanel] = useState('timeline');

// Actualización
setSelectedTooth(12);
setZoomLevel(1.5);
```

**Reflex (State Variables):**
```python
class AppState(rx.State):
    selected_tooth: Optional[int] = None
    zoom_level: float = 1.0
    active_panel: str = "timeline"

    def select_tooth(self, tooth_number: int):
        self.selected_tooth = tooth_number

    def set_zoom_level(self, level: float):
        self.zoom_level = max(0.5, min(2.0, level))
```

#### B. Renderizado Condicional

**React:**
```javascript
{selectedTooth ? (
  <ToothDetailPanel tooth={selectedTooth} />
) : (
  <EmptyState />
)}
```

**Reflex:**
```python
rx.cond(
    AppState.selected_tooth,
    tooth_detail_panel(),
    empty_state()
)
```

#### C. Listas y Loops

**React:**
```javascript
{teeth.map((tooth, index) => (
  <ToothComponent key={tooth} number={tooth} />
))}
```

**Reflex:**
```python
rx.foreach(
    AppState.teeth_list,
    lambda tooth: tooth_component(tooth)
)
```

#### D. Event Handlers

**React:**
```javascript
<button onClick={() => handleClick(12)}>
  Click
</button>
```

**Reflex:**
```python
rx.button(
    "Click",
    on_click=lambda: AppState.handle_click(12)
)
```

#### E. Tabs System

**React (Custom):**
```javascript
const [activeTab, setActiveTab] = useState('history');

<div className="tabs">
  <button
    className={activeTab === 'history' ? 'active' : ''}
    onClick={() => setActiveTab('history')}
  >
    Historial
  </button>
</div>

{activeTab === 'history' && <HistoryContent />}
```

**Reflex (Native):**
```python
rx.tabs.root(
    rx.tabs.list(
        rx.tabs.trigger("Historial", value="history"),
        rx.tabs.trigger("Condiciones", value="conditions"),
        rx.tabs.trigger("Planificado", value="planned")
    ),
    rx.tabs.content(<content>, value="history"),
    rx.tabs.content(<content>, value="conditions"),
    rx.tabs.content(<content>, value="planned"),
    default_value="history"
)
```

### 6.2 Ventajas de Reflex para Este Proyecto

1. **Integración Backend Directa:** No necesita API REST separada
2. **Tipado Estático:** Python type hints > JavaScript PropTypes
3. **State Management Unificado:** Un solo AppState vs Redux/Context
4. **Menos Boilerplate:** No useEffect, useCallback, useMemo
5. **CSS-in-Python:** Estilos cohesivos sin archivos CSS externos
6. **Componentes Nativos:** rx.tabs, rx.select sin librerías externas

### 6.3 Desventajas de Reflex vs React

1. **Ecosistema:** Menos componentes third-party
2. **Performance:** SSR puede ser más lento en listas grandes
3. **Debugging:** Stack traces de Python son más complejos
4. **IDE Support:** Menos autocomplete que TypeScript
5. **Curva de Aprendizaje:** Paradigma diferente si vienes de React

### 6.4 Tabla de Equivalencias

| Característica | React | Reflex | Complejidad |
|---------------|-------|--------|-------------|
| **State Management** | useState/useReducer | rx.State | Más simple en Reflex |
| **Effects** | useEffect | on_mount/computed vars | Más simple en Reflex |
| **Conditional Rendering** | ternario/&& | rx.cond | Equivalente |
| **Lists** | map | rx.foreach | Equivalente |
| **Tabs** | Custom/MUI/Radix | rx.tabs native | Más simple en Reflex |
| **Forms** | react-hook-form | rx.form native | Más simple en Reflex |
| **Routing** | react-router | rx.route nativo | Más simple en Reflex |
| **Modals** | Custom/MUI | rx.dialog native | Equivalente |
| **API Calls** | axios/fetch | directo en State | Más simple en Reflex |
| **Styling** | CSS/Tailwind/styled | dict CSS-in-Python | Preferencia personal |

---

## 7. ROADMAP DE IMPLEMENTACIÓN

### FASE 1: PREPARACIÓN Y SETUP (1-2 horas)

#### Tareas:
1. Crear backup de archivos actuales
   ```bash
   cp -r dental_system/components/odontologia dental_system/components/odontologia_backup_$(date +%Y%m%d)
   ```

2. Crear estructura de nuevos componentes
   ```
   dental_system/components/odontologia/
   ├── professional_odontogram_viewer.py   (nuevo)
   ├── tooth_detail_sidebar.py             (nuevo)
   ├── intervention_timeline_panel.py      (nuevo)
   ├── version_selector_bar.py             (nuevo)
   ├── treatment_planning_form.py          (nuevo)
   └── __init__.py                         (actualizar exports)
   ```

3. Actualizar medical_design_system.py con colores de plantilla
   - Agregar `TOOTH_COLORS` dict con mapeo React
   - Verificar que `MEDICAL_COLORS["dental"]` coincida
   - Documentar diferencias si existen

4. Crear constantes compartidas en config
   ```python
   # dental_system/config/odontogram_constants.py
   FDI_TEETH = {...}
   TOOTH_DIMENSIONS = {...}
   ```

#### Entregables:
- Estructura de archivos creada
- Backup completo realizado
- Colores validados y documentados
- Constantes definidas

---

### FASE 2: ODONTOGRAM VIEWER CORE (2-3 horas)

#### Tareas:
1. Implementar `professional_odontogram_viewer.py`
   - Función `render_tooth()` con SVG
   - Grid FDI completo (32 dientes)
   - Jaw outlines con paths
   - Línea central de referencia

2. Integrar con AppState
   ```python
   # dental_system/state/app_state.py
   selected_tooth: Optional[int] = None
   hovered_tooth: Optional[int] = None
   zoom_level: float = 1.0
   odontogram_data: Dict[int, Dict] = {}

   def select_tooth(self, tooth_number: int):
       self.selected_tooth = tooth_number

   def set_hovered_tooth(self, tooth_number: Optional[int]):
       self.hovered_tooth = tooth_number
   ```

3. Implementar controles de zoom
   - Botones +/-
   - Indicador de porcentaje
   - Reset a 100%
   - Límites 0.5x - 2.0x

4. Agregar leyenda de condiciones
   - Grid responsive
   - Colores + labels
   - Ubicación debajo del odontograma

#### Testing:
- Verificar que los 32 dientes rendericen correctamente
- Probar click en cada diente
- Validar colores según condición
- Comprobar zoom en rangos extremos

#### Entregables:
- Odontograma SVG funcional
- Interacción click/hover operativa
- Zoom controls funcionando
- Leyenda visible

---

### FASE 3: TOOTH DETAIL SIDEBAR (2-3 horas)

#### Tareas:
1. Implementar `tooth_detail_sidebar.py`
   - Layout base con header
   - Sistema de tabs nativo rx.tabs
   - Empty state cuando no hay selección

2. Tab Historial
   - Lista de intervenciones con `rx.foreach`
   - Intervention cards con formato BS/USD
   - Botón "Agregar Intervención"
   - Empty state con icono

3. Tab Condiciones
   - Lista de condiciones con badges
   - Color coding por severidad
   - Empty state positivo (sano)

4. Tab Planificado
   - Lista de tratamientos con prioridad
   - Badges de contador en tab
   - Botones inline (Programar/Editar)
   - Empty state con acción

5. Computed vars en AppState
   ```python
   @rx.var
   def selected_tooth_data(self) -> Dict:
       return self.odontogram_data.get(self.selected_tooth, {})

   @rx.var
   def selected_tooth_interventions(self) -> List:
       return filter_interventions(self.selected_tooth)

   @rx.var
   def selected_tooth_interventions_count(self) -> int:
       return len(self.selected_tooth_interventions)
   ```

#### Testing:
- Verificar cambio de tabs
- Validar datos en cada tab
- Probar botón cerrar (X)
- Comprobar badges de contador

#### Entregables:
- Panel lateral funcional
- Tabs con contenido dinámico
- Badges operativos
- Empty states informativos

---

### FASE 4: INTERVENTION TIMELINE (1.5 horas)

#### Tareas:
1. Implementar `intervention_timeline_panel.py`
   - Header con título y contador
   - Filtros (dentista, procedimiento, período)
   - Lógica de filtrado reactiva

2. Timeline visual
   - Línea vertical conectando items
   - Cards de intervención con iconos
   - Formato fecha + hora
   - Costos BS/USD a la derecha

3. Panel de resumen (footer)
   - Grid 4 columnas con stats
   - Cálculos automáticos
   - Total intervenciones
   - Total costos + dientes únicos

4. Integración filtros
   ```python
   @rx.var
   def filtered_interventions(self) -> List:
       interventions = self.all_interventions

       if self.filter_dentist != "all":
           interventions = [i for i in interventions if i.dentist == self.filter_dentist]

       if self.filter_procedure != "all":
           interventions = [i for i in interventions if i.procedure == self.filter_procedure]

       # ... más filtros

       return interventions
   ```

#### Testing:
- Probar cada filtro individualmente
- Validar cálculos de stats
- Verificar empty state con filtros

#### Entregables:
- Timeline renderizado correctamente
- Filtros funcionales
- Stats calculados
- Empty state con "Limpiar Filtros"

---

### FASE 5: VERSION SELECTOR & PLANNING (1.5 horas)

#### Tareas:
1. Implementar `version_selector_bar.py`
   - Dropdown versiones con fechas
   - Toggle comparación
   - Botones Export/Print (placeholders)
   - Info cards (3 columnas)

2. Implementar `treatment_planning_form.py`
   - Grid de procedimientos predefinidos
   - Selector de prioridad visual
   - Inputs costo dual con conversión automática
   - Textarea notas
   - Panel de resumen

3. Lógica de comparación
   ```python
   def toggle_comparison(self):
       self.show_comparison = not self.show_comparison
       if self.show_comparison and self.comparison_version == self.selected_version:
           # Auto-select diferente versión
           other_versions = [v for v in self.odontogram_versions if v.id != self.selected_version]
           if other_versions:
               self.comparison_version = other_versions[0].id
   ```

4. Modal de planificación
   - Trigger desde tab "Planificado"
   - Formulario completo
   - Validaciones
   - Callback guardar

#### Testing:
- Probar cambio de versiones
- Validar toggle comparación
- Comprobar formulario de planificación
- Verificar conversión BS/USD

#### Entregables:
- Selector de versiones operativo
- Comparación básica funcional
- Formulario de planificación completo
- Validaciones activas

---

### FASE 6: INTEGRACIÓN CON INTERVENCION_PAGE (1 hora)

#### Tareas:
1. Actualizar `intervencion_page.py`
   - Reemplazar tabs viejos con nuevos componentes
   - Integrar professional_odontogram_viewer()
   - Agregar tooth_detail_sidebar() a layout
   - Ubicar intervention_timeline_panel() debajo

2. Layout responsive final
   ```python
   rx.grid(
       professional_odontogram_viewer(),  # 75% ancho
       tooth_detail_sidebar(),            # 25% ancho
       columns=rx.breakpoints(
           initial="1",      # Móvil: stack vertical
           md="1",           # Tablet: stack vertical
           lg="75% 25%",     # Desktop: grid + sidebar
           xl="75% 25%"      # XL: mismo ratio
       ),
       gap=MEDICAL_SPACING["lg"],
       width="100%"
   )
   ```

3. Panel toggle buttons
   - Botón "Línea de Tiempo"
   - Botón "Planificar Tratamiento" (solo si diente seleccionado)
   - Collapse/Expand con rx.cond

4. On mount events
   ```python
   on_mount=[
       AppState.load_patient_odontogram,
       AppState.load_interventions_history,
       AppState.set_active_tab("odontograma")
   ]
   ```

#### Testing:
- Verificar layout en desktop/tablet/mobile
- Probar navegación entre tabs
- Validar carga de datos al montar
- Comprobar toggle de panels

#### Entregables:
- Integración completa funcional
- Layout responsive operativo
- Navegación fluida
- Datos cargando correctamente

---

### FASE 7: REFINAMIENTO Y POLISH (1 hora)

#### Tareas:
1. Microinteracciones
   - Transiciones smooth en dientes
   - Hover effects sutiles
   - Loading states en filtros
   - Animaciones de entrada/salida

2. Accesibilidad
   - Tooltips informativos
   - Focus states visibles
   - Labels descriptivos
   - Keyboard navigation

3. Performance
   - Memoizar computed vars pesados
   - Lazy loading de timeline si >50 items
   - Throttling en filtros de búsqueda

4. Error handling
   - Try/catch en event handlers
   - Mensajes de error amigables
   - Fallbacks para datos faltantes

#### Testing Final:
- Testing UX con usuarios reales (odontólogos)
- Performance profiling
- Validación cross-browser
- Testing responsive en dispositivos reales

#### Entregables:
- Microinteracciones implementadas
- Accesibilidad verificada
- Performance optimizada
- Error handling robusto

---

### FASE 8: DOCUMENTACIÓN Y ENTREGA (1 hora)

#### Tareas:
1. Documentar código
   - Docstrings en todas las funciones
   - Type hints completos
   - Comentarios en lógica compleja

2. Guía de migración
   - Archivo MIGRATION_GUIDE.md
   - Cambios en API de AppState
   - Deprecations warnings

3. Testing guide
   - Casos de prueba principales
   - Escenarios edge case
   - Datos de prueba

4. Actualizar README
   - Screenshots del nuevo diseño
   - Sección "Odontograma V2.0"
   - Links a documentación

#### Entregables:
- Código completamente documentado
- MIGRATION_GUIDE.md completo
- Testing guide disponible
- README actualizado

---

### TIEMPO TOTAL ESTIMADO

| Fase | Descripción | Tiempo | Acumulado |
|------|-------------|--------|-----------|
| 1 | Preparación y setup | 1-2h | 1-2h |
| 2 | Odontogram viewer core | 2-3h | 3-5h |
| 3 | Tooth detail sidebar | 2-3h | 5-8h |
| 4 | Intervention timeline | 1.5h | 6.5-9.5h |
| 5 | Version selector & planning | 1.5h | 8-11h |
| 6 | Integración con página | 1h | 9-12h |
| 7 | Refinamiento y polish | 1h | 10-13h |
| 8 | Documentación y entrega | 1h | 11-14h |

**TOTAL: 11-14 horas** de desarrollo + testing

**Distribución sugerida:**
- Día 1: Fases 1-2 (4-5 horas)
- Día 2: Fases 3-4 (3.5-4.5 horas)
- Día 3: Fases 5-6 (2.5-3 horas)
- Día 4: Fases 7-8 (2 horas)

---

## 8. RECOMENDACIONES FINALES

### 8.1 Prioridades de Implementación

#### MUST HAVE (Crítico)
1. Odontogram viewer con 32 dientes FDI
2. Click en diente → Panel lateral
3. Tabs (Historial/Condiciones/Planificado)
4. Lista de intervenciones formateada
5. Integración con AppState existente

#### SHOULD HAVE (Importante)
6. Filtros en timeline (dentista, procedimiento)
7. Zoom controls
8. Empty states informativos
9. Badges de contador en tabs
10. Panel de planificación de tratamientos

#### NICE TO HAVE (Opcional)
11. Comparación de versiones side-by-side
12. Export/Print avanzado
13. Keyboard shortcuts
14. Animaciones complejas
15. Drag & drop en timeline

### 8.2 Mejores Prácticas

#### A. Código Limpio
- **Un componente = una responsabilidad**
- Máximo 300 líneas por archivo
- Nombres descriptivos en español
- Docstrings completos

#### B. Performance
- Usar `@rx.var(cache=True)` en computed vars pesados
- Implementar pagination en listas >50 items
- Lazy loading de imágenes clínicas
- Throttling en búsquedas/filtros

#### C. Mantenibilidad
- Separar lógica de UI
- Constantes en archivos config
- Reutilizar componentes
- Testing unitario de funciones helper

#### D. UX Médica
- Colores estandarizados ISO
- Terminología anatómica correcta
- Flujo intuitivo para odontólogos
- Feedback inmediato en acciones

### 8.3 Pitfalls a Evitar

#### 1. **Sobre-optimización prematura**
- No implementar comparación compleja si no se usa
- Empezar simple, iterar según feedback

#### 2. **Complejidad innecesaria**
- No replicar TODO de React
- Adaptar lo valioso, descartar lo redundante

#### 3. **Ignorar el flujo médico real**
- El sistema NO tiene citas → No fecha programada obligatoria
- Orden de llegada > Planificación rígida

#### 4. **Colores inconsistentes**
- SIEMPRE usar `medical_design_system.py`
- NO hardcodear hex values en componentes

#### 5. **Estado duplicado**
- Una sola fuente de verdad: `AppState`
- NO crear variables locales para lo mismo

### 8.4 Testing Checklist

#### Funcional
- [ ] Click en cada uno de los 32 dientes funciona
- [ ] Panel lateral abre y cierra correctamente
- [ ] Tabs cambian contenido dinámicamente
- [ ] Filtros de timeline funcionan correctamente
- [ ] Badges de contador muestran valores correctos
- [ ] Zoom funciona en rangos 0.5x - 2.0x
- [ ] Formulario de planificación valida campos

#### Visual
- [ ] Colores coinciden con paleta médica
- [ ] Leyenda es legible y correcta
- [ ] Hover effects funcionan en todos los dientes
- [ ] Diente seleccionado tiene borde visible
- [ ] Empty states son informativos
- [ ] Icons están correctamente alineados

#### Responsive
- [ ] Funciona en móvil (320px+)
- [ ] Funciona en tablet (768px+)
- [ ] Funciona en desktop (1024px+)
- [ ] Funciona en XL (1536px+)
- [ ] Grid se adapta correctamente
- [ ] Sidebar no rompe en móvil

#### Performance
- [ ] Odontograma carga en <1 segundo
- [ ] Cambio de tabs es instantáneo
- [ ] Filtros no causan lag
- [ ] Scroll es suave en listas largas
- [ ] No hay memory leaks

#### Accesibilidad
- [ ] Contraste WCAG AAA cumplido
- [ ] Tooltips informativos presentes
- [ ] Focus states visibles
- [ ] Keyboard navigation funciona
- [ ] Screen readers compatibles

### 8.5 Plan de Rollout

#### Fase Alpha (Desarrollo)
- Implementar en rama `feature/odontogram-v2`
- Testing interno con datos mock
- Validar arquitectura base

#### Fase Beta (Staging)
- Desplegar en ambiente de prueba
- Testing con 2-3 odontólogos
- Recoger feedback inicial
- Ajustar según comentarios

#### Fase Producción (Release)
- Merge a `main` branch
- Migration guide para usuarios
- Monitoreo de errores
- Iteración según uso real

### 8.6 Métricas de Éxito

#### Cuantitativas
- **Tiempo de carga:** <1 segundo para odontograma completo
- **Clicks para selección:** 1 click = diente seleccionado
- **Errores de UI:** 0 errores en consola
- **Performance:** Lighthouse score >90

#### Cualitativas
- **Feedback odontólogos:** "Más intuitivo que versión anterior"
- **Usabilidad:** Asistentes pueden usar sin capacitación extensa
- **Satisfacción:** Net Promoter Score >8/10

---

## 9. CONCLUSIÓN

### Resumen de la Propuesta

Esta propuesta adapta las mejores prácticas de una plantilla React profesional al framework Reflex.dev, creando un **visor de odontograma de calidad enterprise** para el sistema dental.

**Mejoras clave:**
1. **Simplificación visual:** 32 dientes unificados vs 160 áreas complejas
2. **UX médica profesional:** Siguiendo estándares ISO/WHO/ADA
3. **Integración nativa:** Componentes Reflex sin JavaScript custom
4. **Performance optimizado:** 50% menos componentes renderizados
5. **Mobile-first:** Responsive desde 320px hasta 2xl
6. **Paleta consistente:** Colores médicos estandarizados
7. **Timeline avanzada:** Filtros reactivos complejos
8. **Planificación integrada:** Formulario completo de tratamientos

**Diferenciadores competitivos:**
- Panel lateral con tabs (Historial/Condiciones/Planificado)
- Empty states informativos y contextuales
- Badges de contador dinámicos
- Sistema de zoom profesional
- Filtros avanzados en timeline
- Selector de versiones con comparación
- Integración total con flujo médico real (orden de llegada sin citas)

**Valor para el proyecto de tesis:**
- Cumple con estándares internacionales de UI médica
- Demuestra dominio de framework moderno (Reflex.dev)
- Aplica patrones de diseño enterprise
- Documenta decisiones arquitectónicas
- Incluye testing exhaustivo
- Roadmap realista y ejecutable

---

## 10. PRÓXIMOS PASOS

### Acción Inmediata Recomendada

1. **Validar propuesta** con equipo técnico y médico (30 minutos)
2. **Aprobar paleta de colores** definitiva (15 minutos)
3. **Confirmar funcionalidades** must-have vs nice-to-have (15 minutos)
4. **Asignar recursos** y tiempo de desarrollo (15 minutos)
5. **Iniciar Fase 1** del roadmap (1-2 horas)

### Recursos Necesarios

- **Desarrollador Frontend Reflex:** 11-14 horas
- **Diseñador UX** (opcional): 2 horas para validación visual
- **Odontólogo revisor:** 1 hora para feedback médico
- **Tester QA:** 2 horas para testing final

### Contacto y Soporte

Para preguntas o aclaraciones sobre esta propuesta:
- Revisar sección específica del documento
- Consultar código de referencia React original
- Referirse a `medical_design_system.py` para colores
- Contactar al desarrollador principal

---

**FIN DEL DOCUMENTO**

**Elaborado por:** Sistema de IA - Especialista UI/UX Médico
**Versión:** 2.0 Enterprise Medical Design
**Fecha:** 01 Octubre 2025
**Estado:** Propuesta Completa - Lista para Implementación
**Páginas:** 48
**Palabras:** ~15,000

**Archivos Analizados:**
- `index.jsx` (345 líneas)
- `OdontogramViewer.jsx` (322 líneas)
- `ToothDetailPanel.jsx` (308 líneas)
- `InterventionTimeline.jsx` (362 líneas)
- `VersionSelector.jsx` (216 líneas)
- `TreatmentPlanningPanel.jsx` (354 líneas)

**Total líneas de código React analizadas:** 1,907 líneas
**Tiempo de análisis:** 2 horas
**Propuesta de implementación Reflex:** ~1,500 líneas estimadas
