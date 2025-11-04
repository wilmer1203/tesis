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
    material_incluido: Optional[List[str]] = None  # text[]
    activo: bool = True
    fecha_creacion: str = ""
    creado_por: Optional[str] = ""
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ServicioModel":
        """Crear instancia desde diccionario de Supabase"""
        if not data or not isinstance(data, dict):
            return cls()
        
        # Procesar material_incluido desde BD
        material_data = data.get("material_incluido", [])

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
            material_incluido=material_data,
            activo=bool(data.get("activo", True)),
            fecha_creacion=str(data.get("fecha_creacion", "")),
            creado_por=str(data.get("creado_por", "") if data.get("creado_por") else "")
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
    material_incluido: Optional[str] = ""
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

        # Validar material incluido (es string, no lista en formulario)
        if self.material_incluido and len(self.material_incluido) > 500:
            errors["material_incluido"] = "El material incluido no puede exceder 500 caracteres"

        return errors
    
    def to_dict(self) -> Dict:
        """
        Convierte el modelo a diccionario para la BD
        Asegura que los tipos coincidan con la tabla
        """
        # Procesar material_incluido como lista
        material_incluido_list = None
        if self.material_incluido and self.material_incluido.strip():
            # Convertir string separado por comas a lista
            material_incluido_list = [item.strip() for item in self.material_incluido.split(',') if item.strip()]

        return {
            "codigo": self.codigo.strip().upper(),
            "nombre": self.nombre.strip(),
            "categoria": self.categoria.lower(),
            "precio_base_usd": float(self.precio_base_usd),
            "alcance_servicio": self.alcance_servicio,
            "descripcion": self.descripcion.strip() if self.descripcion else None,
            "material_incluido": material_incluido_list,
            "condicion_resultante": self.condicion_resultante if self.condicion_resultante else None
        }

    @classmethod
    def from_servicio_model(cls, servicio: "ServicioModel") -> "ServicioFormModel":
        """Crear instancia de formulario desde ServicioModel para edición"""

        # Conversión de datos desde ServicioModel a formulario
        # Conversión de material_incluido: Array → String separado por comas
        material_str = ""
        if servicio.material_incluido is not None:
            try:
                if isinstance(servicio.material_incluido, list):
                    # Filtrar elementos vacíos y unir con coma y espacio
                    materiales_filtrados = [mat.strip() for mat in servicio.material_incluido if mat and mat.strip()]
                    material_str = ", ".join(materiales_filtrados)
                elif isinstance(servicio.material_incluido, str):
                    # Si ya es string, limpiar y usar directamente
                    material_str = servicio.material_incluido.strip()
                else:
                    # Cualquier otro tipo, convertir a string
                    material_str = str(servicio.material_incluido).strip()
            except Exception as e:
                material_str = ""
        form_precio_usd = str(float(servicio.precio_base_usd or 0.00))

        # Datos convertidos correctamente para formulario

        return cls(
            codigo=servicio.codigo or "",
            nombre=servicio.nombre or "",
            categoria=servicio.categoria or "Preventiva",
            descripcion=servicio.descripcion or "",
            precio_base_usd=form_precio_usd, # str: "67.89"
            alcance_servicio=servicio.alcance_servicio or "superficie_especifica",
            material_incluido=material_str,
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
    """Modelo para intervenciones/tratamientos realizados - Esquema BD v4.1"""
    # Campos principales coincidentes con la BD
    id: Optional[str] = ""
    consulta_id: str = ""
    odontologo_id: str = ""
    asistente_id: Optional[str] = ""
    
    # Control temporal
    hora_inicio: str = ""
    hora_fin: Optional[str] = ""
    duracion_real: Optional[str] = ""
    
    # Detalles clínicos
    dientes_afectados: List[int] = []  # INTEGER[] en BD
    diagnostico_inicial: Optional[str] = ""
    procedimiento_realizado: str = ""
    materiales_utilizados: List[str] = []
    anestesia_utilizada: Optional[str] = ""
    complicaciones: Optional[str] = ""
    
    # Información económica en múltiples monedas (COMO EN BD)
    total_bs: float = 0.0
    total_usd: float = 0.0
    descuento_bs: float = 0.0
    descuento_usd: float = 0.0
    
    # Estado del procedimiento
    estado: str = "completada"  # en_progreso, completada, suspendida
    
    # Seguimiento
    requiere_control: bool = False
    fecha_control_sugerida: Optional[str] = ""
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
            asistente_id=str(data.get("asistente_id", "") if data.get("asistente_id") else ""),
            hora_inicio=str(data.get("hora_inicio", "")),
            hora_fin=str(data.get("hora_fin", "") if data.get("hora_fin") else ""),
            duracion_real=str(data.get("duracion_real", "") if data.get("duracion_real") else ""),
            dientes_afectados=data.get("dientes_afectados", []),
            diagnostico_inicial=str(data.get("diagnostico_inicial", "") if data.get("diagnostico_inicial") else ""),
            procedimiento_realizado=str(data.get("procedimiento_realizado", "")),
            materiales_utilizados=data.get("materiales_utilizados", []),
            anestesia_utilizada=str(data.get("anestesia_utilizada", "") if data.get("anestesia_utilizada") else ""),
            complicaciones=str(data.get("complicaciones", "") if data.get("complicaciones") else ""),
            
            # Nuevos campos económicos según BD
            total_bs=float(data.get("total_bs", 0)),
            total_usd=float(data.get("total_usd", 0)),
            descuento_bs=float(data.get("descuento_bs", 0)),
            descuento_usd=float(data.get("descuento_usd", 0)),
            
            # Estado y seguimiento
            estado=str(data.get("estado", "completada")),
            requiere_control=bool(data.get("requiere_control", False)),
            fecha_control_sugerida=str(data.get("fecha_control_sugerida", "") if data.get("fecha_control_sugerida") else ""),
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
    
    @property
    def dientes_display(self) -> str:
        """Dientes afectados formateados"""
        if self.dientes_afectados:
            return ", ".join(map(str, self.dientes_afectados))
        return "No especificado"
    
    @property
    def materiales_display(self) -> str:
        """Materiales utilizados formateados"""
        if self.materiales_utilizados:
            return ", ".join(self.materiales_utilizados)
        return "No especificado"
    

    @property
    def duracion_display(self) -> str:
        """Duración real formateada"""
        if self.duracion_real:
            try:
                # Parsear duración en formato PostgreSQL interval
                # Ej: "01:30:00" o "30 minutes"
                if ":" in self.duracion_real:
                    partes = self.duracion_real.split(":")
                    horas = int(partes[0])
                    minutos = int(partes[1])
                    if horas > 0:
                        return f"{horas}h {minutos}m"
                    else:
                        return f"{minutos}m"
                else:
                    return self.duracion_real
            except:
                return self.duracion_real
        return "No registrada"


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

