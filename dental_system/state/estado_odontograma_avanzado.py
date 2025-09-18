"""
🦷 ESTADO DEL ODONTOGRAMA FDI AVANZADO
=====================================

Estado especializado para el odontograma FDI interactivo avanzado.
Separado del componente para evitar imports circulares.
"""

import reflex as rx
from typing import Dict, List, Optional, Any
import asyncio

from dental_system.services.odontograma_service import odontograma_service
from dental_system.models.odontologia_models import DienteModel

# ==========================================
# 🎯 ESTADO DEL ODONTOGRAMA AVANZADO
# ==========================================

class EstadoOdontogramaAvanzado(rx.State,mixin=True):
    """🎯 Estado completo del odontograma FDI avanzado"""
    
    # Variables básicas del odontograma FDI
    diente_seleccionado: Optional[int] = None
    catalogo_cargado: bool = False
    is_loading: bool = False
    error_message: str = ""
    
    # Datos del catálogo FDI
    dientes_catalogo: List[Dict[str, Any]] = []
    condiciones_disponibles: List[Dict[str, Any]] = []
    
    # Estados de los dientes (Dict[numero_fdi, estado])
    dientes_estados: Dict[int, Dict[str, Any]] = {}
    
    # Estadísticas
    total_sanos: int = 32
    total_con_patologia: int = 0
    total_tratados: int = 0
    
    @rx.event
    async def cargar_catalogo_fdi(self):
        """🦷 Cargar catálogo FDI desde base de datos"""
        if self.catalogo_cargado:
            return
            
        self.is_loading = True
        self.error_message = ""
        
        try:
            # Cargar dientes FDI
            dientes = await odontograma_service.cargar_catalogo_fdi()
            
            if dientes:
                self.dientes_catalogo = [
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
                
                # Inicializar estados (todos sanos por defecto)
                for diente in self.dientes_catalogo:
                    self.dientes_estados[diente["numero_fdi"]] = {
                        "condicion": "sano",
                        "codigo": "SAO", 
                        "color": "#16a34a",
                        "superficie": "completa",
                        "observaciones": ""
                    }
                
                # Cargar condiciones disponibles
                condiciones = await odontograma_service.cargar_condiciones_disponibles()
                self.condiciones_disponibles = condiciones
                
                self.catalogo_cargado = True
                self.calcular_estadisticas()
                
            else:
                self.error_message = "❌ No se pudo cargar el catálogo FDI"
                
        except Exception as e:
            self.error_message = f"❌ Error: {str(e)}"
        
        finally:
            self.is_loading = False
    
    @rx.event
    def seleccionar_diente(self, numero_fdi: int):
        """🔍 Seleccionar diente para editar en odontograma
        
        Args:
            numero_fdi: Número FDI del diente (11-48)
            
        El método realiza:
        1. Validación del número FDI
        2. Permite deseleccionar un diente si se selecciona el mismo
        3. Verifica que el diente exista en el catálogo
        """
        # Validar rango FDI válido (11-48)
        if not (11 <= numero_fdi <= 48):
            self.error_message = "❌ Número FDI inválido"
            return
            
        # Deseleccionar si se hace clic en el mismo diente
        if self.diente_seleccionado == numero_fdi:
            self.diente_seleccionado = None
            return
            
        # Verificar que el diente existe en el catálogo
        diente_existe = any(d["numero_fdi"] == numero_fdi for d in self.dientes_catalogo)
        if not diente_existe:
            self.error_message = "❌ El diente no existe en el catálogo"
            return
            
        # Actualizar selección
        self.error_message = ""
        self.diente_seleccionado = numero_fdi
    
    @rx.event
    def aplicar_condicion_diente(self, numero_fdi: int, codigo_condicion: str):
        """🎨 Aplicar condición a un diente"""
        # Mapeo de colores por defecto para cada código
        colores_default = {
            "SAO": "#16a34a",    # Verde - Sano
            "CAR": "#dc2626",    # Rojo - Caries
            "OBT": "#2563eb",    # Azul - Obturado
            "COR": "#d97706",    # Naranja - Corona
            "EXT": "#7c2d12",    # Marrón - Extracción
            "ENDO": "#be185d",   # Rosa - Endodoncia
            "FRAC": "#059669",   # Verde oscuro - Fracturado
            "AUS": "#374151"     # Gris - Ausente
        }
        
        # Buscar información de la condición
        condicion_info = next(
            (c for c in self.condiciones_disponibles if c.get("codigo") == codigo_condicion),
            {
                "nombre": codigo_condicion, 
                "color_hex": colores_default.get(codigo_condicion, "#16a34a"), 
                "codigo": codigo_condicion
            }
        )
        
        # Actualizar estado del diente
        self.dientes_estados[numero_fdi] = {
            "condicion": condicion_info.get("nombre", codigo_condicion),
            "codigo": codigo_condicion,
            "color": condicion_info.get("color_hex", colores_default.get(codigo_condicion, "#16a34a")),
            "superficie": "completa",
            "observaciones": ""
        }
        
        self.calcular_estadisticas()
    
    def calcular_estadisticas(self):
        """📊 Calcular estadísticas del odontograma"""
        sanos = 0
        patologia = 0
        tratados = 0
        
        for estado in self.dientes_estados.values():
            codigo = estado.get("codigo", "SAO")
            if codigo == "SAO":
                sanos += 1
            elif codigo in ["CAR", "FRAC"]:
                patologia += 1
            elif codigo in ["OBT", "COR", "ENDO"]:
                tratados += 1
            elif codigo in ["EXT", "AUS"]:
                # Los dientes extraídos o ausentes no se cuentan en ninguna categoría activa
                pass
                
        self.total_sanos = sanos
        self.total_con_patologia = patologia
        self.total_tratados = tratados