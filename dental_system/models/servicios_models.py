"""
Modelos de datos para el módulo de SERVICIOS
Centraliza todos los modelos relacionados con servicios odontológicos

Validaciones según estructura de BD:
- id: uuid NOT NULL DEFAULT uuid_generate_v4()
- codigo: varchar(20) NOT NULL + UNIQUE + CHECK (codigo ~ '^[A-Z0-9]+$')
- nombre: varchar(100) NOT NULL
- categoria: varchar(50) NOT NULL
- precios: numeric(10,2) NOT NULL + CHECK (precio > 0)
"""

import reflex as rx
from typing import Optional, Dict, Any, List
from datetime import datetime
from decimal import Decimal
from dental_system.utils.servicios_validators import (
    validar_codigo_servicio,
    validar_nombre_servicio,
    validar_precio,
    validar_categoria,
    validar_alcance_servicio,
    validar_condicion_resultante
)

class ServicioModel(rx.Base):
    """Modelo para datos de servicios odontológicos"""
    # Campos obligatorios
    id: Optional[str] = ""  # uuid autogenerado
    codigo: str = ""        # varchar(20) + regex ^[A-Z0-9]+$
    nombre: str = ""        # varchar(100)
    categoria: str = ""     # varchar(50)
    precio_base_usd: Decimal = Decimal('0.00')  # numeric(10,2) > 0

    # 🆕 Alcance del servicio
    alcance_servicio: str = "superficie_especifica"  # superficie_especifica | diente_completo | boca_completa

    # ✨ V3.0: Condición resultante (FK a catalogo_condiciones)
    condicion_resultante: Optional[str] = None  # NULL = servicio preventivo (no modifica odontograma)

    # Campos opcionales
    descripcion: Optional[str] = None      # text
    activo: bool = True
    fecha_creacion: str = ""
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ServicioModel":
        """Crear instancia desde diccionario de Supabase"""
        if not data or not isinstance(data, dict):
            return cls()

        # Procesar precio desde BD
        precio_usd_bd = data.get("precio_base_usd", 0)

        return cls(
            id=str(data.get("id", "")),
            codigo=str(data.get("codigo", "")),
            nombre=str(data.get("nombre", "")),
            descripcion=str(data.get("descripcion", "") if data.get("descripcion") else ""),
            categoria=str(data.get("categoria", "")),
            precio_base_usd=float(precio_usd_bd),
            alcance_servicio=str(data.get("alcance_servicio", "superficie_especifica")),
            condicion_resultante=data.get("condicion_resultante"),  # NULL si es preventivo
            activo=bool(data.get("activo", True)),
            fecha_creacion=str(data.get("fecha_creacion", ""))
        )
    # ✨ V3.0: Métodos para condición resultante

    @property
    def es_preventivo(self) -> bool:
        """Indica si es un servicio preventivo (no modifica odontograma)"""
        return self.condicion_resultante is None

    @property
    def condicion_display(self) -> str:
        """Condición resultante formateada para UI"""
        if not self.condicion_resultante:
            return "No modifica odontograma"

        # Mapeo de condiciones a etiquetas legibles
        condiciones_map = {
            "sano": "✅ Sano",
            "caries": "🦠 Caries",
            "obturacion": "🔧 Obturación",
            "endodoncia": "🦷 Endodoncia",
            "corona": "👑 Corona",
            "puente": "🌉 Puente",
            "implante": "🔩 Implante",
            "protesis": "🦾 Prótesis",
            "ausente": "❌ Ausente",
            "fractura": "💥 Fractura",
            "extraccion_indicada": "⚠️ Extracción Indicada"
        }

        return condiciones_map.get(
            self.condicion_resultante,
            self.condicion_resultante.replace("_", " ").title()
        )



class ServicioFormModel(rx.Base):
    """
    Modelo tipado para formulario de servicios con validaciones
    Implementa todas las restricciones de la tabla servicios
    """
    # Campos obligatorios
    codigo: str = ""
    nombre: str = ""
    categoria: str = ""
    precio_base_usd: str = "0.00"  # Cambio: Decimal → str para compatibilidad con formularios
    alcance_servicio: str = "superficie_especifica"  # superficie_especifica | diente_completo | boca_completa

    # Campos opcionales
    descripcion: Optional[str] = ""
    condicion_resultante: Optional[str] = None  # NULL = servicio preventivo (no modifica odontograma)
    
    def validate_form(self) -> Dict[str, str]:
        """
        Validación completa del formulario según restricciones de BD
        
        Returns:
            Dict con mensajes de error por campo
        """
        errors: Dict[str, str] = {}

        # Validar campos obligatorios
        if error := validar_codigo_servicio(self.codigo):
            errors["codigo"] = error

        if error := validar_nombre_servicio(self.nombre):
            errors["nombre"] = error

        if error := validar_categoria(self.categoria):
            errors["categoria"] = error

        if error := validar_precio(self.precio_base_usd, "dólares"):
            errors["precio_base_usd"] = error

        if error := validar_alcance_servicio(self.alcance_servicio):
            errors["alcance_servicio"] = error

        # Validar campo opcional condicion_resultante
        if error := validar_condicion_resultante(self.condicion_resultante):
            errors["condicion_resultante"] = error

        return errors
    
    def to_dict(self) -> Dict:
        """
        Convierte el modelo a diccionario para la BD
        Asegura que los tipos coincidan con la tabla
        """
        return {
            "codigo": self.codigo.strip().upper(),
            "nombre": self.nombre.strip(),
            "categoria": self.categoria.lower(),
            "precio_base_usd": float(self.precio_base_usd),
            "alcance_servicio": self.alcance_servicio,
            "descripcion": self.descripcion.strip() if self.descripcion else None,
            "condicion_resultante": self.condicion_resultante if self.condicion_resultante else None
        }

    @classmethod
    def from_servicio_model(cls, servicio: "ServicioModel") -> "ServicioFormModel":
        """Crear instancia de formulario desde ServicioModel para edición"""
        form_precio_usd = str(float(servicio.precio_base_usd or 0.00))

        return cls(
            codigo=servicio.codigo or "",
            nombre=servicio.nombre or "",
            categoria=servicio.categoria or "Preventiva",
            descripcion=servicio.descripcion or "",
            precio_base_usd=form_precio_usd,
            alcance_servicio=servicio.alcance_servicio or "superficie_especifica",
            condicion_resultante=servicio.condicion_resultante
        )


class ServicioStatsModel(rx.Base):
    """Modelo para estadísticas de servicios"""
    total_servicios: int = 0
    activos: int = 0
    por_categoria: Dict[str, int] = {}
    mas_solicitados: List[Dict[str, Any]] = []
    mayor_ingreso: List[Dict[str, Any]] = []
    
    # Promedios
    precio_promedio: float = 0.0
    duracion_promedio: float = 0.0  # En minutos


class EstadisticaCategoriaModel(rx.Base):
    """Modelo para estadísticas específicas de una categoría de servicio"""
    total: int = 0
    precio_promedio: float = 0.0
    precio_min: float = 0.0
    precio_max: float = 0.0
    mas_popular: str = ""
    
    @classmethod
    def from_servicios_list(cls, servicios: List["ServicioModel"]) -> "EstadisticaCategoriaModel":
        """Crear estadísticas desde lista de servicios de una categoría"""
        if not servicios:
            return cls()

        # Encontrar el más popular
        mas_popular = ""
        if servicios:
            servicio_popular = max(servicios, key=lambda x: getattr(x, 'veces_usado', 0) or 0)
            mas_popular = servicio_popular.nombre
        
        return cls(
            total=len(servicios),
            precio_promedio=sum(precios) / len(precios) if precios else 0.0,
            precio_min=min(precios) if precios else 0.0,
            precio_max=max(precios) if precios else 0.0,
            mas_popular=mas_popular
        )
    
    @property
    def precio_promedio_display(self) -> str:
        """Precio promedio formateado"""
        return f"${self.precio_promedio:,.2f}"
    
    @property
    def rango_precios_display(self) -> str:
        """Rango de precios formateado"""
        if self.precio_min == self.precio_max:
            return f"${self.precio_min:,.2f}"
        return f"${self.precio_min:,.2f} - ${self.precio_max:,.2f}"


class IntervencionModel(rx.Base):
    """Modelo para intervenciones/tratamientos realizados - Esquema BD simplificado"""
    # Campos principales coincidentes con la BD
    id: Optional[str] = ""
    consulta_id: str = ""
    odontologo_id: str = ""

    # Control temporal
    hora_inicio: str = ""

    # Detalles clínicos
    procedimiento_realizado: str = ""

    # Información económica en múltiples monedas
    total_bs: float = 0.0
    total_usd: float = 0.0

    # Estado del procedimiento
    estado: str = "completada"  # en_progreso, completada, suspendida

    # Timestamps
    fecha_registro: str = ""
    
    # Campos adicionales para compatibilidad con componentes existentes
    precio_final: float = 0.0  # Calculado como total_bs + total_usd
    observaciones: Optional[str] = ""  # Para componentes que lo necesiten
    
    # Información relacionada
    servicio_nombre: str = ""
    servicio_categoria: str = ""
    odontologo_nombre: str = ""
    odontologo_especialidad: str = ""  # Especialidad del odontólogo
    paciente_nombre: str = ""

    # Campos adicionales para display
    servicios_resumen: str = ""  # Resumen de servicios realizados
    costo_total_bs: float = 0.0  # Alias para total_bs (compatibilidad componentes)
    costo_total_usd: float = 0.0  # Alias para total_usd (compatibilidad componentes)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "IntervencionModel":
        """Crear instancia desde diccionario de Supabase"""
        if not data or not isinstance(data, dict):
            return cls()
        
        # Procesar datos relacionados
        servicio_data = data.get("servicio", {}) or data.get("servicios", {})
        odontologo_data = data.get("odontologo", {}) or data.get("personal", {})
        
        return cls(
            id=str(data.get("id", "")),
            consulta_id=str(data.get("consulta_id", "")),
            odontologo_id=str(data.get("odontologo_id", "")),
            hora_inicio=str(data.get("hora_inicio", "")),
            procedimiento_realizado=str(data.get("procedimiento_realizado", "")),

            # Campos económicos según BD
            total_bs=float(data.get("total_bs", 0)),
            total_usd=float(data.get("total_usd", 0)),

            # Estado
            estado=str(data.get("estado", "completada")),
            fecha_registro=str(data.get("fecha_registro", "")),
            
            # Compatibilidad hacia atrás
            precio_final=float(data.get("precio_final", 0)) or (float(data.get("total_bs", 0)) + float(data.get("total_usd", 0))),
            observaciones=str(data.get("observaciones", "") if data.get("observaciones") else ""),
            
            # Información relacionada
            servicio_nombre=str(servicio_data.get("nombre", "") if servicio_data else ""),
            servicio_categoria=str(servicio_data.get("categoria", "") if servicio_data else ""),
            odontologo_nombre=str(odontologo_data.get("nombre_completo", "") if odontologo_data else ""),
            odontologo_especialidad=str(odontologo_data.get("especialidad", "") if odontologo_data else ""),
            paciente_nombre=str(data.get("paciente_nombre", "")),

            # Campos adicionales para display
            servicios_resumen=str(data.get("servicios_resumen", "") or data.get("procedimiento_realizado", "")),
            costo_total_bs=float(data.get("total_bs", 0)),  # Alias
            costo_total_usd=float(data.get("total_usd", 0))  # Alias
        )
    
    @property
    def precio_final_display(self) -> str:
        """Precio final formateado"""
        return f"${self.precio_final:,.2f}"


class MaterialModel(rx.Base):
    """Modelo para materiales odontológicos"""
    id: str = ""
    nombre: str = ""
    marca: str = ""
    tipo: str = ""  # composite, amalgama, cemento, etc.
    unidad_medida: str = ""  # gramos, ml, unidades
    stock_actual: int = 0
    stock_minimo: int = 0
    precio_unitario: float = 0.0
    fecha_vencimiento: Optional[str] = ""
    proveedor: str = ""
    activo: bool = True
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MaterialModel":
        """Crear instancia desde diccionario"""
        if not data or not isinstance(data, dict):
            return cls()
        
        return cls(
            id=str(data.get("id", "")),
            nombre=str(data.get("nombre", "")),
            marca=str(data.get("marca", "")),
            tipo=str(data.get("tipo", "")),
            unidad_medida=str(data.get("unidad_medida", "")),
            stock_actual=int(data.get("stock_actual", 0)),
            stock_minimo=int(data.get("stock_minimo", 0)),
            precio_unitario=float(data.get("precio_unitario", 0)),
            fecha_vencimiento=str(data.get("fecha_vencimiento", "") if data.get("fecha_vencimiento") else ""),
            proveedor=str(data.get("proveedor", "")),
            activo=bool(data.get("activo", True))
        )
    
    @property
    def stock_bajo(self) -> bool:
        """Indica si el stock está bajo"""
        return self.stock_actual <= self.stock_minimo
    
    @property
    def estado_stock(self) -> str:
        """Estado del stock con colores"""
        if self.stock_actual == 0:
            return "🔴 Agotado"
        elif self.stock_bajo:
            return "🟡 Stock Bajo"
        else:
            return "🟢 Disponible"

