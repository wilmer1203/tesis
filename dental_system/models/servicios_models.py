"""
Modelos de datos para el módulo de SERVICIOS
Centraliza todos los modelos relacionados con servicios odontológicos
"""

import reflex as rx
from typing import Optional, Dict, Any, List
from datetime import datetime


class ServicioModel(rx.Base):
    """Modelo para datos de servicios odontológicos"""
    id: Optional[str] = ""
    codigo: str = ""
    nombre: str = ""
    descripcion: Optional[str] = ""
    categoria: str = ""
    subcategoria: Optional[str] = ""
    duracion_estimada: str = "30 minutes"
    precio_base: float = 0.0
    precio_minimo: Optional[float] = None
    precio_maximo: Optional[float] = None
    
    # Campos adicionales para dual currency (BS/USD)
    precio_bs: float = 0.0      # Precio en Bolívares
    precio_usd: float = 0.0     # Precio en Dólares
    requiere_cita_previa: bool = True
    requiere_autorizacion: bool = False
    material_incluido: Optional[List[str]] = None
    instrucciones_pre: Optional[str] = ""
    instrucciones_post: Optional[str] = ""
    activo: bool = True
    fecha_creacion: str = ""
    creado_por: Optional[str] = ""
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ServicioModel":
        """Crear instancia desde diccionario de Supabase"""
        if not data or not isinstance(data, dict):
            return cls()
        
        return cls(
            id=str(data.get("id", "")),
            codigo=str(data.get("codigo", "")),
            nombre=str(data.get("nombre", "")),
            descripcion=str(data.get("descripcion", "") if data.get("descripcion") else ""),
            categoria=str(data.get("categoria", "")),
            subcategoria=str(data.get("subcategoria", "") if data.get("subcategoria") else ""),
            duracion_estimada=str(data.get("duracion_estimada", "30 minutes")),
            precio_base=float(data.get("precio_base_bs", data.get("precio_base", 0))),
            precio_minimo=float(data.get("precio_minimo", 0)) if data.get("precio_minimo") else None,
            precio_maximo=float(data.get("precio_maximo", 0)) if data.get("precio_maximo") else None,
            
            # Precios dual currency - mapear desde la BD
            precio_bs=float(data.get("precio_base_bs", data.get("precio_bs", 0))),
            precio_usd=float(data.get("precio_base_usd", data.get("precio_usd", 0))),
            requiere_cita_previa=bool(data.get("requiere_cita_previa", True)),
            requiere_autorizacion=bool(data.get("requiere_autorizacion", False)),
            material_incluido=data.get("material_incluido", []),
            instrucciones_pre=str(data.get("instrucciones_pre", "") if data.get("instrucciones_pre") else ""),
            instrucciones_post=str(data.get("instrucciones_post", "") if data.get("instrucciones_post") else ""),
            activo=bool(data.get("activo", True)),
            fecha_creacion=str(data.get("fecha_creacion", "")),
            creado_por=str(data.get("creado_por", "") if data.get("creado_por") else "")
        )
    
    @property
    def precio_base_display(self) -> str:
        """Precio base formateado para mostrar"""
        return f"${self.precio_base:,.2f}"
    
    @property
    def rango_precio_display(self) -> str:
        """Rango de precios formateado"""
        if self.precio_minimo and self.precio_maximo:
            return f"${self.precio_minimo:,.2f} - ${self.precio_maximo:,.2f}"
        elif self.precio_minimo:
            return f"Desde ${self.precio_minimo:,.2f}"
        elif self.precio_maximo:
            return f"Hasta ${self.precio_maximo:,.2f}"
        else:
            return self.precio_base_display
    
    @property
    def precios_dual_display(self) -> str:
        """Precios BS/USD formateados para mostrar"""
        if self.precio_usd > 0 and self.precio_bs > 0:
            return f"${self.precio_usd:.0f} / {self.precio_bs:,.0f} Bs"
        elif self.precio_usd > 0:
            return f"${self.precio_usd:.0f}"
        elif self.precio_bs > 0:
            return f"{self.precio_bs:,.0f} Bs"
        else:
            return "Precio no definido"
    
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

class ServicioFormModel(rx.Base):
    """
    📝 FORMULARIO DE CREACIÓN/EDICIÓN DE SERVICIOS
    
    Reemplaza: form_data: Dict[str, str] en servicios_service
    """
    
    # Información básica
    nombre: str = ""
    descripcion: str = ""
    categoria: str = "preventiva"  # preventiva, restaurativa, estetica, cirugia, etc.
    
    # Precios
    precio_base: str = "0"
    precio_minimo: str = "0"
    precio_maximo: str = "0"
    
    # Detalles del servicio
    duracion_estimada: str = "30"  # minutos
    requiere_consulta_previa: bool = False
    requiere_autorizacion: bool = False
    
    # Materiales e instrucciones
    material_incluido: str = ""
    instrucciones_pre: str = ""
    instrucciones_post: str = ""
    
    # Estado
    activo: bool = True
    
    @classmethod
    def from_servicio_model(cls, servicio: "ServicioModel") -> "ServicioFormModel":
        """Crear instancia de formulario desde ServicioModel para edición"""
        return cls(
            nombre=servicio.nombre,
            descripcion=servicio.descripcion or "",
            categoria=servicio.categoria or "preventiva",
            precio_base=str(servicio.precio_base) if servicio.precio_base else "0",
            precio_minimo=str(servicio.precio_minimo) if servicio.precio_minimo else "0",
            precio_maximo=str(servicio.precio_maximo) if servicio.precio_maximo else "0",
            duracion_estimada=str(servicio.duracion_estimada).replace(" minutes", "") if servicio.duracion_estimada else "30",
            requiere_consulta_previa=getattr(servicio, 'requiere_cita_previa', False),
            requiere_autorizacion=servicio.requiere_autorizacion,
            material_incluido=servicio.material_incluido_display if hasattr(servicio, 'material_incluido_display') else "",
            instrucciones_pre=servicio.instrucciones_pre or "",
            instrucciones_post=servicio.instrucciones_post or "",
            activo=servicio.activo
        )
    
    def validate_servicio(self) -> Dict[str, List[str]]:
        """Validar campos específicos de servicios (alias para validate_form)"""
        return self.validate_form()
    
    def validate_form(self) -> Dict[str, List[str]]:
        """Validar campos requeridos y formato"""
        errors = {}
        
        if not self.nombre.strip():
            errors.setdefault("nombre", []).append("Nombre del servicio es requerido")
        
        if not self.categoria.strip():
            errors.setdefault("categoria", []).append("Categoría es requerida")
        
        # Validar precio base
        try:
            precio_base = float(self.precio_base)
            if precio_base <= 0:
                errors.setdefault("precio_base", []).append("Precio base debe ser mayor a 0")
        except (ValueError, TypeError):
            errors.setdefault("precio_base", []).append("Precio base debe ser un número válido")
        
        # Validar precios mínimo y máximo si están presentes
        try:
            if self.precio_minimo and self.precio_minimo.strip():
                precio_min = float(self.precio_minimo)
                precio_base = float(self.precio_base)
                if precio_min > precio_base:
                    errors.setdefault("precio_minimo", []).append("Precio mínimo no puede ser mayor al precio base")
        except (ValueError, TypeError):
            errors.setdefault("precio_minimo", []).append("Precio mínimo debe ser un número válido")
        
        try:
            if self.precio_maximo and self.precio_maximo.strip():
                precio_max = float(self.precio_maximo)
                precio_base = float(self.precio_base)
                if precio_max < precio_base:
                    errors.setdefault("precio_maximo", []).append("Precio máximo no puede ser menor al precio base")
        except (ValueError, TypeError):
            errors.setdefault("precio_maximo", []).append("Precio máximo debe ser un número válido")
        
        # Validar duración
        try:
            if self.duracion_estimada and self.duracion_estimada.strip():
                duracion = int(self.duracion_estimada)
                if duracion <= 0:
                    errors.setdefault("duracion_estimada", []).append("Duración debe ser mayor a 0 minutos")
        except (ValueError, TypeError):
            errors.setdefault("duracion_estimada", []).append("Duración debe ser un número entero de minutos")
        
        return errors
    
    def to_dict(self) -> Dict[str, str]:
        """Convertir a dict para compatibilidad"""
        return {
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "categoria": self.categoria,
            "precio_base": self.precio_base,
            "precio_minimo": self.precio_minimo,
            "precio_maximo": self.precio_maximo,
            "duracion_estimada": self.duracion_estimada,
            "requiere_consulta_previa": str(self.requiere_consulta_previa),
            "requiere_autorizacion": str(self.requiere_autorizacion),
            "material_incluido": self.material_incluido,
            "instrucciones_pre": self.instrucciones_pre,
            "instrucciones_post": self.instrucciones_post,
            "activo": str(self.activo),
        }