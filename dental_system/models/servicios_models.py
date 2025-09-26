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
    validar_duracion,
    validar_categoria
)

class ServicioModel(rx.Base):
    """Modelo para datos de servicios odontológicos"""
    # Campos obligatorios
    id: Optional[str] = ""  # uuid autogenerado
    codigo: str = ""        # varchar(20) + regex ^[A-Z0-9]+$
    nombre: str = ""        # varchar(100)
    categoria: str = ""     # varchar(50)
    duracion_estimada: str = "00:30:00"  # interval default 30min
    precio_base_bs: Decimal = Decimal('0.00')   # numeric(10,2) > 0
    precio_base_usd: Decimal = Decimal('0.00')  # numeric(10,2) > 0
    
    # Campos opcionales
    descripcion: Optional[str] = None      # text
    subcategoria: Optional[str] = None     # varchar(50)
    material_incluido: Optional[List[str]] = None  # text[]
    instrucciones_pre: Optional[str] = None   # text
    instrucciones_post: Optional[str] = None  # text
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

        # Procesar precios y duración llegando desde BD
        duracion_bd = data.get("duracion_estimada", "30 minutes")
        precio_bs_bd = data.get("precio_base_bs", 0)
        precio_usd_bd = data.get("precio_base_usd", 0)

        return cls(
            id=str(data.get("id", "")),
            codigo=str(data.get("codigo", "")),
            nombre=str(data.get("nombre", "")),
            descripcion=str(data.get("descripcion", "") if data.get("descripcion") else ""),
            categoria=str(data.get("categoria", "")),
            subcategoria=str(data.get("subcategoria", "") if data.get("subcategoria") else ""),
            duracion_estimada=str(duracion_bd),

            # Precios dual currency - mapeo directo desde BD
            precio_base_bs=float(precio_bs_bd),
            precio_base_usd=float(precio_usd_bd),
            material_incluido=material_data,
            instrucciones_pre=str(data.get("instrucciones_pre", "") if data.get("instrucciones_pre") else ""),
            instrucciones_post=str(data.get("instrucciones_post", "") if data.get("instrucciones_post") else ""),
            activo=bool(data.get("activo", True)),
            fecha_creacion=str(data.get("fecha_creacion", "")),
            creado_por=str(data.get("creado_por", "") if data.get("creado_por") else "")
        )
    
    @property
    def precio_base_display(self) -> str:
        """Precio base formateado para mostrar (USD)"""
        return f"${self.precio_base_usd:,.2f}"

    @property
    def precio_bs_display(self) -> str:
        """Precio en bolívares formateado"""
        return f"Bs {self.precio_base_bs:,.2f}"

    @property
    def precio_dual_display(self) -> str:
        """Precios dual currency formateados"""
        return f"${self.precio_base_usd:,.2f} | Bs {self.precio_base_bs:,.2f}"
    
    @property
    def categoria_display(self) -> str:
        """Categoría formateada con emoji"""
        categorias_map = {
            "preventiva": "🛡️ Preventiva",
            "restaurativa": "🔧 Restaurativa",
            "estetica": "✨ Estética",
            "cirugia": "⚔️ Cirugía",
            "endodoncia": "🦷 Endodoncia",
            "protesis": "🦾 Prótesis",
            "ortodoncia": "📐 Ortodoncia",
            "implantes": "🔩 Implantes",
            "pediatrica": "👶 Pediátrica",
            "diagnostico": "🔬 Diagnóstico",
            "emergencia": "🚨 Emergencia",
            "otro": "📋 Otro"
        }
        return categorias_map.get(self.categoria.lower(), f"📋 {self.categoria.title()}")
    
    @property
    def duracion_display(self) -> str:
        """Duración formateada"""
        try:
            # Si viene como "30 minutes", "1 hour", etc.
            if "minute" in self.duracion_estimada:
                minutos = int(self.duracion_estimada.split()[0])
                if minutos < 60:
                    return f"{minutos} min"
                else:
                    horas = minutos // 60
                    mins = minutos % 60
                    if mins > 0:
                        return f"{horas}h {mins}m"
                    else:
                        return f"{horas}h"
            elif "hour" in self.duracion_estimada:
                horas = int(self.duracion_estimada.split()[0])
                return f"{horas}h"
            else:
                return self.duracion_estimada
        except:
            return self.duracion_estimada
    
    @property
    def material_incluido_display(self) -> str:
        """Material incluido formateado"""
        if self.material_incluido:
            return ", ".join(self.material_incluido)
        return "No especificado"
    
    @property
    def requisitos_display(self) -> List[str]:
        """Lista de requisitos del servicio"""
        requisitos = []
        if self.requiere_cita_previa:
            requisitos.append("📅 Requiere cita previa")
        if self.requiere_autorizacion:
            requisitos.append("✋ Requiere autorización")
        return requisitos
    
    @property
    def color_categoria(self) -> str:
        """Color según la categoría para UI"""
        colores_categoria = {
            "preventiva": "#28a745",     # Verde
            "restaurativa": "#007bff",   # Azul
            "estetica": "#e83e8c",       # Rosa
            "cirugia": "#dc3545",        # Rojo
            "endodoncia": "#fd7e14",     # Naranja
            "protesis": "#6c757d",       # Gris
            "ortodoncia": "#20c997",     # Turquesa
            "implantes": "#343a40",      # Negro
            "pediatrica": "#ffc107",     # Amarillo
            "diagnostico": "#17a2b8",    # Cian
            "emergencia": "#dc3545",     # Rojo
            "otro": "#6f42c1"            # Púrpura
        }
        return colores_categoria.get(self.categoria.lower(), "#007bff")


class CategoriaServicioModel(rx.Base):
    """Modelo para categorías de servicios"""
    id: str = ""
    nombre: str = ""
    descripcion: str = ""
    icono: str = ""
    color: str = "#007bff"
    orden: int = 0
    activa: bool = True
    
    # Estadísticas
    cantidad_servicios: int = 0
    ingresos_mes_actual: float = 0.0
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CategoriaServicioModel":
        """Crear instancia desde diccionario"""
        if not data or not isinstance(data, dict):
            return cls()
        
        return cls(
            id=str(data.get("id", "")),
            nombre=str(data.get("nombre", "")),
            descripcion=str(data.get("descripcion", "")),
            icono=str(data.get("icono", "📋")),
            color=str(data.get("color", "#007bff")),
            orden=int(data.get("orden", 0)),
            activa=bool(data.get("activa", True)),
            cantidad_servicios=int(data.get("cantidad_servicios", 0)),
            ingresos_mes_actual=float(data.get("ingresos_mes_actual", 0))
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
    duracion_estimada: str = "00:30:00"
    precio_base_bs: str = "0.00"  # Cambio: Decimal → str para compatibilidad con formularios
    precio_base_usd: str = "0.00"  # Cambio: Decimal → str para compatibilidad con formularios
    
    # Campos opcionales
    descripcion: Optional[str] = ""
    subcategoria: Optional[str] = ""
    material_incluido: Optional[str] = ""
    instrucciones_pre: Optional[str] = ""
    instrucciones_post: Optional[str] = ""
    
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
            
        if error := validar_duracion(self.duracion_estimada):
            errors["duracion_estimada"] = error
            
        if error := validar_precio(self.precio_base_bs, "bolívares"):
            errors["precio_base_bs"] = error
            
        if error := validar_precio(self.precio_base_usd, "dólares"):
            errors["precio_base_usd"] = error
            
        # Validar campos opcionales si tienen valor
        if self.subcategoria and len(self.subcategoria) > 50:
            errors["subcategoria"] = "La subcategoría no puede exceder 50 caracteres"
            
        # Validar material incluido
        if self.material_incluido:
            for item in self.material_incluido:
                if len(item) > 100:
                    errors["material_incluido"] = "Los items de material no pueden exceder 100 caracteres"
                    break
                    
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
            "duracion_estimada": self.duracion_estimada,
            "precio_base_bs": float(self.precio_base_bs),
            "precio_base_usd": float(self.precio_base_usd),
            "descripcion": self.descripcion.strip() if self.descripcion else None,
            "subcategoria": self.subcategoria.strip() if self.subcategoria else None,
            "material_incluido": material_incluido_list,
            "instrucciones_pre": self.instrucciones_pre.strip() if self.instrucciones_pre else None,
            "instrucciones_post": self.instrucciones_post.strip() if self.instrucciones_post else None
        }

    @classmethod
    def from_servicio_model(cls, servicio: "ServicioModel") -> "ServicioFormModel":
        """Crear instancia de formulario desde ServicioModel para edición"""

        # Conversión de datos desde ServicioModel a formulario

        # Conversión de duracion_estimada: "00:30:00" → "30" (minutos)
        duracion_str = "30"  # Default
        if servicio.duracion_estimada:
            try:
                if ":" in servicio.duracion_estimada:
                    # Formato HH:MM:SS → convertir a minutos
                    parts = servicio.duracion_estimada.split(":")
                    horas = int(parts[0])
                    minutos = int(parts[1])
                    segundos = int(parts[2]) if len(parts) > 2 else 0

                    # Convertir todo a minutos (redondear segundos)
                    total_minutos = (horas * 60) + minutos
                    if segundos >= 30:  # Redondear hacia arriba si >= 30 segundos
                        total_minutos += 1

                    # Mínimo 1 minuto si hay algún tiempo registrado
                    if total_minutos == 0 and (horas > 0 or minutos > 0 or segundos > 0):
                        total_minutos = 1

                    duracion_str = str(total_minutos)
                    # Conversión exitosa de duración

                elif "minutes" in servicio.duracion_estimada:
                    # Formato "30 minutes" → "30"
                    duracion_str = servicio.duracion_estimada.replace(" minutes", "").strip()
                else:
                    # Asumir que es solo el número de minutos
                    duracion_str = str(servicio.duracion_estimada).strip()
            except Exception:
                duracion_str = "30"

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

        # Conversión de precios: Decimal → str (para compatibilidad con formularios HTML)
        form_precio_bs = str(float(servicio.precio_base_bs or 0.00))
        form_precio_usd = str(float(servicio.precio_base_usd or 0.00))

        # Datos convertidos correctamente para formulario

        return cls(
            codigo=servicio.codigo or "",
            nombre=servicio.nombre or "",
            categoria=servicio.categoria or "Preventiva",
            descripcion=servicio.descripcion or "",
            subcategoria=servicio.subcategoria or "",
            duracion_estimada=duracion_str,  # String de minutos para el formulario
            precio_base_bs=form_precio_bs,   # str: "123.45"
            precio_base_usd=form_precio_usd, # str: "67.89"
            material_incluido=material_str,
            instrucciones_pre=servicio.instrucciones_pre or "",
            instrucciones_post=servicio.instrucciones_post or ""
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
        
        precios = [s.precio_base for s in servicios if s.precio_base and s.precio_base > 0]
        
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
    paciente_nombre: str = ""
    
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
            paciente_nombre=str(data.get("paciente_nombre", ""))
        )
    
    @property
    def precio_final_display(self) -> str:
        """Precio final formateado"""
        return f"${self.precio_final:,.2f}"
    
    @property
    def descuento_display(self) -> str:
        """Descuento formateado"""
        if self.descuento > 0:
            return f"-${self.descuento:,.2f}"
        return "Sin descuento"
    
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
    def estado_display(self) -> str:
        """Estado formateado para mostrar"""
        estados_map = {
            "pendiente": "⏳ Pendiente",
            "en_progreso": "🔄 En Progreso",
            "completada": "✅ Completada",
            "suspendida": "⏸️ Suspendida"
        }
        return estados_map.get(self.estado, self.estado.capitalize())
    
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


# ==========================================
# 📝 FORMULARIOS DE SERVICIOS
# ==========================================

# class ServicioFormModel(rx.Base):
#     """
#     📝 FORMULARIO DE CREACIÓN/EDICIÓN DE SERVICIOS
    
#     Reemplaza: form_data: Dict[str, str] en servicios_service
#     """
    
#     # Información básica
#     codigo: str = ""  # Código del servicio (ej: SER001)
#     nombre: str = ""
#     descripcion: str = ""
#     categoria: str = "preventiva"  # preventiva, restaurativa, estetica, cirugia, etc.
    
#     # Precios dual currency
#     precio_base_bs: str = "0"
#     precio_base_usd: str = "0"

#     # Detalles del servicio
#     duracion_estimada: str = "30"  # minutos

#     # Materiales e instrucciones
#     material_incluido: str = ""
#     instrucciones_pre: str = ""
#     instrucciones_post: str = ""
    
#     # Estado
#     activo: bool = True
    
#     @classmethod
#     def from_servicio_model(cls, servicio: "ServicioModel") -> "ServicioFormModel":
#         """Crear instancia de formulario desde ServicioModel para edición"""
#         return cls(
#             nombre=servicio.nombre,
#             descripcion=servicio.descripcion or "",
#             categoria=servicio.categoria or "preventiva",
#             precio_base_bs=str(servicio.precio_base_bs) if servicio.precio_base_bs else "0",
#             precio_base_usd=str(servicio.precio_base_usd) if servicio.precio_base_usd else "0",
#             duracion_estimada=str(servicio.duracion_estimada).replace(" minutes", "") if servicio.duracion_estimada else "30",
#             material_incluido=", ".join(servicio.material_incluido) if servicio.material_incluido else "",
#             instrucciones_pre=servicio.instrucciones_pre or "",
#             instrucciones_post=servicio.instrucciones_post or "",
#             activo=servicio.activo
#         )
    
#     def validate_servicio(self) -> Dict[str, List[str]]:
#         """Validar campos específicos de servicios (alias para validate_form)"""
#         return self.validate_form()
    
#     def validate_form(self) -> Dict[str, List[str]]:
#         """Validar campos requeridos y formato"""
#         errors = {}
        
#         if not self.nombre.strip():
#             errors.setdefault("nombre", []).append("Nombre del servicio es requerido")
        
#         if not self.categoria.strip():
#             errors.setdefault("categoria", []).append("Categoría es requerida")
        
#         # Validar precios dual currency
#         try:
#             precio_bs = float(self.precio_base_bs)
#             if precio_bs <= 0:
#                 errors.setdefault("precio_base_bs", []).append("Precio en BS debe ser mayor a 0")
#         except (ValueError, TypeError):
#             errors.setdefault("precio_base_bs", []).append("Precio en BS debe ser un número válido")

#         try:
#             precio_usd = float(self.precio_base_usd)
#             if precio_usd <= 0:
#                 errors.setdefault("precio_base_usd", []).append("Precio en USD debe ser mayor a 0")
#         except (ValueError, TypeError):
#             errors.setdefault("precio_base_usd", []).append("Precio en USD debe ser un número válido")
        
#         # Validar duración
#         try:
#             if self.duracion_estimada and self.duracion_estimada.strip():
#                 duracion = int(self.duracion_estimada)
#                 if duracion <= 0:
#                     errors.setdefault("duracion_estimada", []).append("Duración debe ser mayor a 0 minutos")
#         except (ValueError, TypeError):
#             errors.setdefault("duracion_estimada", []).append("Duración debe ser un número entero de minutos")
        
#         return errors
    
#     def to_dict(self) -> Dict[str, str]:
#         """Convertir a dict para compatibilidad"""
#         return {
#             "nombre": self.nombre,
#             "descripcion": self.descripcion,
#             "categoria": self.categoria,
#             "precio_base_bs": self.precio_base_bs,
#             "precio_base_usd": self.precio_base_usd,
#             "duracion_estimada": self.duracion_estimada,
#             "material_incluido": self.material_incluido,
#             "instrucciones_pre": self.instrucciones_pre,
#             "instrucciones_post": self.instrucciones_post,
#             "activo": str(self.activo),
#         }