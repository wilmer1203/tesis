"""
🧪 COMPONENTE DE PRUEBA - CATÁLOGO FDI AVANZADO
==================================================

Componente temporal para probar que el servicio avanzado
funciona correctamente con los datos reales de la BD.
"""

import reflex as rx
from typing import List, Dict, Any
import asyncio

from dental_system.services.odontograma_service import odontograma_service
from dental_system.styles.themes import COLORS, DARK_THEME

# ==========================================
# 🧪 ESTADO DE PRUEBA FDI
# ==========================================

class TestFDIState(rx.State):
    """Estado para probar el catálogo FDI"""
    
    # Datos cargados
    dientes_fdi: List[Dict[str, Any]] = []
    condiciones_disponibles: List[Dict[str, Any]] = []
    
    # Estado de carga
    is_loading: bool = False
    error_message: str = ""
    success_message: str = ""
    
    # Estadísticas
    total_dientes: int = 0
    dientes_por_cuadrante: Dict[int, int] = {}
    
    async def cargar_catalogo_fdi(self):
        """🦷 Cargar y probar catálogo FDI desde BD"""
        self.is_loading = True
        self.error_message = ""
        self.success_message = ""
        
        try:
            # Cargar catálogo FDI
            dientes = await odontograma_service.cargar_catalogo_fdi()
            
            if dientes:
                # Convertir a dict para el estado
                self.dientes_fdi = [
                    {
                        "numero_fdi": diente.numero_fdi,
                        "nombre_diente": diente.nombre_diente,
                        "cuadrante": diente.cuadrante,
                        "tipo_diente": diente.tipo_diente,
                        "coordenadas_svg": diente.coordenadas_svg,
                        "superficies_disponibles": diente.superficies_disponibles
                    }
                    for diente in dientes
                ]
                
                # Calcular estadísticas
                self.total_dientes = len(self.dientes_fdi)
                self.dientes_por_cuadrante = {}
                
                for diente in self.dientes_fdi:
                    cuadrante = diente["cuadrante"]
                    self.dientes_por_cuadrante[cuadrante] = self.dientes_por_cuadrante.get(cuadrante, 0) + 1
                
                self.success_message = f"✅ Catálogo FDI cargado: {self.total_dientes} dientes"
            else:
                self.error_message = "❌ No se encontraron dientes en la BD"
                
        except Exception as e:
            self.error_message = f"❌ Error cargando catálogo: {str(e)}"
        
        finally:
            self.is_loading = False
    
    async def cargar_condiciones(self):
        """🎨 Cargar condiciones disponibles"""
        try:
            condiciones = await odontograma_service.cargar_condiciones_disponibles()
            self.condiciones_disponibles = condiciones
            
            if condiciones:
                self.success_message += f" | {len(condiciones)} condiciones"
            
        except Exception as e:
            self.error_message += f" | Error condiciones: {str(e)}"
    
    async def test_diente_especifico(self, numero_fdi: int):
        """🔍 Probar búsqueda de diente específico"""
        try:
            diente = await odontograma_service.obtener_diente_por_fdi(numero_fdi)
            
            if diente:
                self.success_message = f"✅ Diente {numero_fdi}: {diente.nombre_diente}"
            else:
                self.error_message = f"❌ Diente {numero_fdi} no encontrado"
                
        except Exception as e:
            self.error_message = f"❌ Error buscando diente {numero_fdi}: {str(e)}"

# ==========================================
# 🧪 COMPONENTES DE PRUEBA
# ==========================================

def test_fdi_header() -> rx.Component:
    """🏷️ Header del componente de prueba"""
    return rx.vstack(
        rx.heading(
            "🧪 PRUEBA CATÁLOGO FDI AVANZADO",
            size="6",
            color=COLORS["primary"]
        ),
        rx.text(
            "Verificación del servicio avanzado con datos reales de la base de datos",
            color=DARK_THEME["colors"]["text_secondary"],
            font_size="sm"
        ),
        spacing="2",
        align="center",
        width="100%"
    )

def test_controls() -> rx.Component:
    """🎮 Controles de prueba"""
    return rx.hstack(
        rx.button(
            rx.cond(
                TestFDIState.is_loading,
                rx.hstack(
                    rx.spinner(size="1"),
                    rx.text("Cargando..."),
                    spacing="2"
                ),
                rx.hstack(
                    rx.icon("database"),
                    rx.text("Cargar Catálogo FDI"),
                    spacing="2"
                )
            ),
            on_click=TestFDIState.cargar_catalogo_fdi,
            disabled=TestFDIState.is_loading,
            variant="solid",
            color_scheme="blue"
        ),
        rx.button(
            rx.hstack(
                rx.icon("palette"),
                rx.text("Cargar Condiciones"),
                spacing="2"
            ),
            on_click=TestFDIState.cargar_condiciones,
            variant="outline",
            color_scheme="cyan"
        ),
        spacing="3",
        justify="center",
        width="100%"
    )

def test_messages() -> rx.Component:
    """📢 Mensajes de estado"""
    return rx.vstack(
        rx.cond(
            TestFDIState.success_message != "",
            rx.callout(
                TestFDIState.success_message,
                icon="check_circle",
                color_scheme="green",
                size="1"
            )
        ),
        rx.cond(
            TestFDIState.error_message != "",
            rx.callout(
                TestFDIState.error_message,
                icon="alert_circle",
                color_scheme="red",
                size="1"
            )
        ),
        spacing="2",
        width="100%"
    )

def test_stats() -> rx.Component:
    """📊 Estadísticas del catálogo"""
    return rx.cond(
        TestFDIState.total_dientes > 0,
        rx.vstack(
            rx.heading("📊 Estadísticas del Catálogo", size="4", color=COLORS["primary"]),
            
            # Total de dientes
            rx.card(
                rx.hstack(
                    rx.badge(
                        TestFDIState.total_dientes,
                        color_scheme="blue",
                        size="3"
                    ),
                    rx.text("Total de dientes cargados", font_weight="medium"),
                    spacing="3",
                    align="center",
                    justify="between",
                    width="100%"
                ),
                width="100%"
            ),
            
            # Dientes por cuadrante
            rx.card(
                rx.vstack(
                    rx.text("🦷 Dientes por Cuadrante", font_weight="bold", size="3"),
                    rx.vstack(
                        rx.foreach(
                            TestFDIState.dientes_por_cuadrante,
                            lambda cuadrante_info: rx.hstack(
                                rx.badge(f"Q{cuadrante_info[0]}", color_scheme="gray"),
                                rx.text(f"{cuadrante_info[1]} dientes"),
                                spacing="2",
                                align="center"
                            )
                        ),
                        spacing="1",
                        align="start"
                    ),
                    spacing="3",
                    align="start"
                ),
                width="100%"
            ),
            
            spacing="4",
            width="100%"
        )
    )

def test_dientes_grid() -> rx.Component:
    """🦷 Grid de dientes para verificación visual"""
    return rx.cond(
        TestFDIState.dientes_fdi.length() > 0,
        rx.vstack(
            rx.heading("🦷 Catálogo Visual FDI", size="4", color=COLORS["primary"]),
            
            rx.box(
                rx.grid(
                    rx.foreach(
                        TestFDIState.dientes_fdi,
                        lambda diente: rx.card(
                            rx.vstack(
                                rx.heading(
                                    diente["numero_fdi"],
                                    size="4",
                                    color=COLORS["primary"]
                                ),
                                rx.text(
                                    diente["tipo_diente"].capitalize(),
                                    font_size="xs",
                                    color=DARK_THEME["colors"]["text_secondary"]
                                ),
                                rx.text(
                                    diente["nombre_diente"],
                                    font_size="xs",
                                    text_align="center",
                                    color=COLORS["text"]
                                ),
                                spacing="1",
                                align="center"
                            ),
                            padding="2",
                            min_height="80px",
                            cursor="pointer",
                            on_click=TestFDIState.test_diente_especifico(diente["numero_fdi"]),
                            _hover={
                                "background": COLORS["bg_hover"],
                                "transform": "scale(1.05)",
                                "transition": "all 0.2s"
                            }
                        )
                    ),
                    columns="8",
                    spacing="2",
                    width="100%"
                ),
                width="100%",
                max_height="400px",
                overflow_y="auto"
            ),
            
            spacing="4",
            width="100%"
        )
    )

def test_condiciones_list() -> rx.Component:
    """🎨 Lista de condiciones disponibles"""
    return rx.cond(
        TestFDIState.condiciones_disponibles.length() > 0,
        rx.vstack(
            rx.heading("🎨 Condiciones Disponibles", size="4", color=COLORS["primary"]),
            
            rx.box(
                rx.vstack(
                    rx.foreach(
                        TestFDIState.condiciones_disponibles,
                        lambda condicion: rx.card(
                            rx.hstack(
                                rx.box(
                                    width="16px",
                                    height="16px",
                                    background=condicion.get("color_hex", "#16a34a"),
                                    border_radius="50%"
                                ),
                                rx.vstack(
                                    rx.text(
                                        condicion["nombre"].capitalize(),
                                        font_weight="medium",
                                        font_size="sm"
                                    ),
                                    rx.text(
                                        condicion.get("descripcion", ""),
                                        font_size="xs",
                                        color=DARK_THEME["colors"]["text_secondary"]
                                    ),
                                    spacing="0",
                                    align="start"
                                ),
                                rx.badge(
                                    condicion.get("codigo", ""),
                                    color_scheme="gray",
                                    size="1"
                                ),
                                rx.cond(
                                    condicion.get("es_urgente", False),
                                    rx.badge(
                                        "URGENTE",
                                        color_scheme="red",
                                        size="1"
                                    )
                                ),
                                spacing="3",
                                align="center",
                                justify="between",
                                width="100%"
                            ),
                            padding="3"
                        )
                    ),
                    spacing="2",
                    width="100%"
                ),
                max_height="300px",
                overflow_y="auto",
                width="100%"
            ),
            
            spacing="4",
            width="100%"
        )
    )

# ==========================================
# 🧪 COMPONENTE PRINCIPAL DE PRUEBA
# ==========================================

def test_fdi_component() -> rx.Component:
    """🧪 Componente principal de prueba del catálogo FDI"""
    return rx.container(
        rx.vstack(
            test_fdi_header(),
            
            rx.divider(),
            
            test_controls(),
            
            test_messages(),
            
            rx.divider(),
            
            test_stats(),
            
            test_dientes_grid(),
            
            test_condiciones_list(),
            
            spacing="6",
            width="100%",
            max_width="1200px"
        ),
        padding="6",
        width="100%"
    )