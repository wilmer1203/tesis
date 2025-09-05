"""
Modelos de datos para DASHBOARD Y ESTADÍSTICAS
Centraliza todos los modelos relacionados con métricas y estadísticas del sistema
"""

import reflex as rx
from typing import Optional, Dict, Any, List


class DashboardStatsModel(rx.Base):
    """Modelo base para estadísticas del dashboard"""
    total_pacientes: int = 0
    consultas_hoy: int = 0
    ingresos_mes: float = 0.0
    personal_activo: int = 0
    servicios_activos: int = 0
    pagos_pendientes: int = 0


class AdminStatsModel(rx.Base):
    """Modelo para estadísticas específicas del administrador"""
    total_pacientes: int = 0
    nuevos_pacientes_mes: int = 0
    consultas_hoy: int = 0
    pagos_pendientes: int = 0
    
    # Estadísticas adicionales de pacientes
    pacientes_activos: int = 0
    pacientes_hombres: int = 0
    pacientes_mujeres: int = 0
    
    # Estadísticas de actividad
    pacientes_registrados_semana: int = 0
    consultas_semana: int = 0
    ingresos_mes: float = 0.0


class GerenteStatsModel(rx.Base):
    """Modelo para estadísticas específicas del gerente (acceso total)"""
    # Estadísticas generales
    total_pacientes: int = 0
    consultas_hoy: int = 0
    ingresos_mes: float = 0.0
    personal_activo: int = 0
    servicios_activos: int = 0
    pagos_pendientes: int = 0
    
    # Estadísticas financieras detalladas
    ingresos_dia: float = 0.0
    ingresos_semana: float = 0.0
    meta_mensual: float = 0.0
    porcentaje_meta: float = 0.0
    
    # Estadísticas de personal
    odontologos_activos: int = 0
    administradores_activos: int = 0
    asistentes_activos: int = 0
    
    # Servicios más rentables
    servicios_populares: List[Dict[str, Any]] = []
    
    # KPIs importantes
    promedio_consultas_dia: float = 0.0
    tiempo_promedio_atencion: float = 0.0  # En minutos
    satisfaccion_pacientes: float = 0.0    # Porcentaje


class OdontologoStatsModel(rx.Base):
    """Modelo para estadísticas específicas del odontólogo"""
    # Consultas
    consultas_hoy: int = 0
    consultas_semana: int = 0
    consultas_mes: int = 0
    
    # Pacientes
    pacientes_asignados: int = 0
    pacientes_nuevos_mes: int = 0
    
    # Tratamientos
    intervenciones_mes: int = 0
    tratamientos_completados: int = 0
    tratamientos_pendientes: int = 0
    
    # Productividad
    ingresos_generados_mes: float = 0.0
    promedio_tiempo_consulta: float = 0.0  # En minutos
    
    # Próximas actividades
    consultas_pendientes_hoy: int = 0
    controles_programados: int = 0
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "OdontologoStatsModel":
        """Crear instancia desde diccionario"""
        if not data or not isinstance(data, dict):
            return cls()
        
        return cls(
            consultas_hoy=int(data.get("consultas_hoy", 0)),
            consultas_semana=int(data.get("consultas_semana", 0)),
            consultas_mes=int(data.get("consultas_mes", 0)),
            pacientes_asignados=int(data.get("pacientes_asignados", 0)),
            pacientes_nuevos_mes=int(data.get("pacientes_nuevos_mes", 0)),
            intervenciones_mes=int(data.get("intervenciones_mes", 0)),
            tratamientos_completados=int(data.get("tratamientos_completados", 0)),
            tratamientos_pendientes=int(data.get("tratamientos_pendientes", 0)),
            ingresos_generados_mes=float(data.get("ingresos_generados_mes", 0.0)),
            promedio_tiempo_consulta=float(data.get("promedio_tiempo_consulta", 0.0)),
            consultas_pendientes_hoy=int(data.get("consultas_pendientes_hoy", 0)),
            controles_programados=int(data.get("controles_programados", 0))
        )


class AsistenteStatsModel(rx.Base):
    """Modelo para estadísticas específicas del asistente"""
    # Actividades del día
    consultas_hoy: int = 0
    pacientes_en_espera: int = 0
    
    # Apoyo en tratamientos
    intervenciones_asistidas: int = 0
    
    # Tareas administrativas
    registros_actualizados: int = 0


class MetricaTemporalModel(rx.Base):
    """Modelo para métricas organizadas por tiempo"""
    periodo: str = ""           # dia, semana, mes, año
    fecha: str = ""
    valor: float = 0.0
    descripcion: str = ""
    categoria: str = ""         # ingresos, consultas, pacientes, etc.
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MetricaTemporalModel":
        """Crear instancia desde diccionario"""
        if not data or not isinstance(data, dict):
            return cls()
        
        return cls(
            periodo=str(data.get("periodo", "")),
            fecha=str(data.get("fecha", "")),
            valor=float(data.get("valor", 0)),
            descripcion=str(data.get("descripcion", "")),
            categoria=str(data.get("categoria", ""))
        )


class ComparativaModel(rx.Base):
    """Modelo para comparativas entre períodos"""
    metrica: str = ""
    periodo_actual: float = 0.0
    periodo_anterior: float = 0.0
    diferencia: float = 0.0
    porcentaje_cambio: float = 0.0
    tendencia: str = "estable"  # crecimiento, decrecimiento, estable
    
    @property
    def tendencia_display(self) -> str:
        """Tendencia con emoji"""
        tendencias_map = {
            "crecimiento": "📈 Crecimiento",
            "decrecimiento": "📉 Decrecimiento", 
            "estable": "➡️ Estable"
        }
        return tendencias_map.get(self.tendencia, self.tendencia.title())
    
    @property
    def color_tendencia(self) -> str:
        """Color según la tendencia"""
        colores = {
            "crecimiento": "#28a745",    # Verde
            "decrecimiento": "#dc3545",  # Rojo
            "estable": "#6c757d"         # Gris
        }
        return colores.get(self.tendencia, "#007bff")


class AlertaModel(rx.Base):
    """Modelo para alertas y notificaciones del sistema"""
    id: str = ""
    tipo: str = ""              # info, warning, error, success
    titulo: str = ""
    mensaje: str = ""
    fecha_creacion: str = ""
    fecha_expiracion: Optional[str] = ""
    activa: bool = True
    dirigida_a_rol: Optional[str] = ""  # gerente, administrador, odontologo, asistente
    accionable: bool = False
    accion_url: Optional[str] = ""
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AlertaModel":
        """Crear instancia desde diccionario"""
        if not data or not isinstance(data, dict):
            return cls()
        
        return cls(
            id=str(data.get("id", "")),
            tipo=str(data.get("tipo", "info")),
            titulo=str(data.get("titulo", "")),
            mensaje=str(data.get("mensaje", "")),
            fecha_creacion=str(data.get("fecha_creacion", "")),
            fecha_expiracion=str(data.get("fecha_expiracion", "") if data.get("fecha_expiracion") else ""),
            activa=bool(data.get("activa", True)),
            dirigida_a_rol=str(data.get("dirigida_a_rol", "") if data.get("dirigida_a_rol") else ""),
            accionable=bool(data.get("accionable", False)),
            accion_url=str(data.get("accion_url", "") if data.get("accion_url") else "")
        )
    
    @property
    def tipo_display(self) -> str:
        """Tipo de alerta con emoji"""
        tipos_map = {
            "info": "ℹ️ Información",
            "warning": "⚠️ Advertencia",
            "error": "❌ Error",
            "success": "✅ Éxito"
        }
        return tipos_map.get(self.tipo, self.tipo.title())
    
    @property
    def color_tipo(self) -> str:
        """Color según el tipo de alerta"""
        colores = {
            "info": "#17a2b8",      # Azul info
            "warning": "#ffc107",   # Amarillo
            "error": "#dc3545",     # Rojo
            "success": "#28a745"    # Verde
        }
        return colores.get(self.tipo, "#17a2b8")


class ReporteModel(rx.Base):
    """Modelo para reportes generados"""
    id: str = ""
    nombre: str = ""
    tipo_reporte: str = ""      # pacientes, consultas, ingresos, servicios, etc.
    parametros: Dict[str, Any] = {}
    fecha_generacion: str = ""
    generado_por: str = ""
    formato: str = "html"       # html, pdf, excel, csv
    url_descarga: Optional[str] = ""
    estado: str = "generado"    # pendiente, generando, generado, error
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ReporteModel":
        """Crear instancia desde diccionario"""
        if not data or not isinstance(data, dict):
            return cls()
        
        return cls(
            id=str(data.get("id", "")),
            nombre=str(data.get("nombre", "")),
            tipo_reporte=str(data.get("tipo_reporte", "")),
            parametros=data.get("parametros", {}),
            fecha_generacion=str(data.get("fecha_generacion", "")),
            generado_por=str(data.get("generado_por", "")),
            formato=str(data.get("formato", "html")),
            url_descarga=str(data.get("url_descarga", "") if data.get("url_descarga") else ""),
            estado=str(data.get("estado", "generado"))
        )


class KPIModel(rx.Base):
    """Modelo para indicadores clave de rendimiento (KPIs)"""
    nombre: str = ""
    valor_actual: float = 0.0
    valor_objetivo: float = 0.0
    unidad: str = ""            # %, pesos, cantidad, etc.
    porcentaje_cumplimiento: float = 0.0
    tendencia: str = "estable"
    periodo: str = "mes"        # dia, semana, mes, año
    categoria: str = ""         # financiero, operativo, satisfaccion
    
    @property
    def cumplimiento_display(self) -> str:
        """Porcentaje de cumplimiento formateado"""
        return f"{self.porcentaje_cumplimiento:.1f}%"
    
    @property
    def valor_display(self) -> str:
        """Valor actual formateado con unidad"""
        if self.unidad == "%":
            return f"{self.valor_actual:.1f}%"
        elif self.unidad == "pesos":
            return f"${self.valor_actual:,.0f}"
        else:
            return f"{self.valor_actual:.0f} {self.unidad}"
    
    @property
    def color_cumplimiento(self) -> str:
        """Color según el porcentaje de cumplimiento"""
        if self.porcentaje_cumplimiento >= 100:
            return "#28a745"    # Verde - Objetivo cumplido
        elif self.porcentaje_cumplimiento >= 80:
            return "#ffc107"    # Amarillo - Cerca del objetivo
        else:
            return "#dc3545"    # Rojo - Lejos del objetivo