"""
🏥 ESTADO DE SERVICIOS - SUBSTATE SEPARADO
===========================================

PROPÓSITO: Manejo centralizado y especializado de servicios odontológicos
- Catálogo completo de servicios con CRUD (solo Gerente)
- Categorización y precios dinámicos
- Filtros y búsquedas optimizadas
- Estadísticas de servicios más solicitados
- Cache inteligente para performance

USADO POR: AppState como coordinador principal  
PATRÓN: Substate con get_estado_servicios() en AppState
"""

import reflex as rx
from datetime import date, datetime
from typing import Dict, Any, List, Optional, Union
import logging

# Servicios y modelos
from dental_system.services.servicios_service import servicios_service
from dental_system.models import (
    ServicioModel,
    ServicioStatsModel,
    CategoriaServicioModel,
    ServicioFormModel
)

logger = logging.getLogger(__name__)

class EstadoServicios(rx.State,mixin=True):
    """
    🏥 ESTADO ESPECIALIZADO EN GESTIÓN DE SERVICIOS ODONTOLÓGICOS
    
    RESPONSABILIDADES:
    - CRUD completo de servicios (solo Gerente)
    - Categorización y organización de servicios
    - Gestión de precios dinámicos (base, mínimo, máximo)
    - Filtros y búsquedas optimizadas
    - Estadísticas de servicios más solicitados
    - Cache inteligente para mejorar performance
    """
    
    # ==========================================
    # 🏥 VARIABLES PRINCIPALES DE SERVICIOS
    # ==========================================
    
    # Lista principal de servicios (modelos tipados)
    lista_servicios: List[ServicioModel] = []
    total_servicios: int = 0
    
    # Servicio seleccionado para operaciones
    servicio_seleccionado: ServicioModel = ServicioModel()
    id_servicio_seleccionado: str = ""
    
    # Formulario de servicio (datos temporales)
    formulario_servicio: Dict[str, Any] = {}
    formulario_servicio_data: ServicioFormModel = ServicioFormModel()
    errores_validacion_servicio: Dict[str, str] = {}
    
    # Variables auxiliares para operaciones
    servicio_para_eliminar: Optional[ServicioModel] = None
    mostrar_solo_activos_servicios: bool = True
    
    # Lista de categorías tipadas
    lista_categorias_servicios: List[CategoriaServicioModel] = []
    
    # ==========================================
    # 🏥 CATEGORÍAS Y CLASIFICACIÓN
    # ==========================================
    
    # Categorías disponibles
    categorias_servicios: List[str] = [
        "Preventiva",
        "Restaurativa", 
        "Endodoncia",
        "Periodoncia",
        "Cirugía Oral",
        "Ortodincia",
        "Prótesis",
        "Estética Dental",
        "Implantología",
        "Odontopediatría",
        "Urgencias",
        "General"
    ]
    
    # Filtros por categoría
    filtro_categoria: str = "todas"
    filtro_estado_servicio: str = "activos"  # todos, activos, inactivos
    filtro_rango_precio_servicios: Dict[str, float] = {"min": 0.0, "max": 999999.0}
    
    # ==========================================
    # 🏥 BÚSQUEDAS Y FILTROS OPTIMIZADOS
    # ==========================================
    
    # Búsqueda principal con throttling
    termino_busqueda_servicios: str = ""
    busqueda_activa_servicios: bool = False
    
    # Ordenamiento
    campo_ordenamiento_servicios: str = "nombre"  # nombre, precio, categoria, popularidad
    direccion_ordenamiento_servicios: str = "asc"  # asc, desc
    
    # Paginación
    pagina_actual_servicios: int = 1
    servicios_por_pagina: int = 18
    total_paginas_servicios: int = 1
    
    # ==========================================
    # 🏥 ESTADÍSTICAS Y MÉTRICAS CACHE
    # ==========================================
    
    # Estadísticas principales
    estadisticas_servicios: ServicioStatsModel = ServicioStatsModel()
    ultima_actualizacion_stats_servicios: str = ""
    
    # Cache de operaciones pesadas
    cache_servicios_populares: List[ServicioModel] = []
    cache_servicios_por_categoria: Dict[str, List[ServicioModel]] = {}
    cache_timestamp_servicios: str = ""
    cache_validez_minutos_servicios: int = 30
    
    # Estados de carga
    cargando_lista_servicios: bool = False
    cargando_estadisticas_servicios: bool = False
    cargando_operacion_servicio: bool = False
    
    # ==========================================
    # 🏥 COMPUTED VARS PARA UI (SIN ASYNC)
    # ==========================================
    
    @rx.var(cache=True)
    def servicios_filtrados_display(self) -> List[ServicioModel]:
        """🔍 Servicios filtrados según criterios actuales"""
        servicios = self.lista_servicios
        
        # Filtrar por búsqueda
        if self.termino_busqueda_servicios:
            servicios = [
                s for s in servicios 
                if (self.termino_busqueda_servicios.lower() in s.nombre.lower() or
                    self.termino_busqueda_servicios.lower() in s.descripcion.lower())
            ]
        
        # Filtrar por categoría
        if self.filtro_categoria != "todas":
            servicios = [s for s in servicios if s.categoria == self.filtro_categoria]
        
        # Filtrar por estado activo
        if self.mostrar_solo_activos_servicios:
            servicios = [s for s in servicios if s.activo]
        
        # Filtrar por rango de precio
        precio_min = self.filtro_rango_precio_servicios.get("min", 0.0)
        precio_max = self.filtro_rango_precio_servicios.get("max", 999999.0)
        servicios = [
            s for s in servicios 
            if precio_min <= s.precio_base <= precio_max
        ]
        
        return servicios
    
    @rx.var(cache=True)
    def servicios_activos(self) -> List[ServicioModel]:
        """✅ Servicios activos"""
        return [s for s in self.lista_servicios if s.activo]
    
    @rx.var(cache=True)
    def servicios_mas_populares(self) -> List[ServicioModel]:
        """⭐ Servicios más populares (cache)"""
        return self.cache_servicios_populares
    
    @rx.var(cache=True)
    def servicio_seleccionado_valido(self) -> bool:
        """✅ Validar si hay servicio seleccionado"""
        return (
            hasattr(self.servicio_seleccionado, 'id') and 
            bool(self.servicio_seleccionado.id)
        )
    
    # ==========================================
    # 🏥 GESTIÓN DE PRECIOS
    # ==========================================
    
    # Configuración de precios
    precio_minimo_global: float = 0.0
    precio_maximo_global: float = 1000000.0
    incremento_precio_sugerido: float = 0.1  # 10%
    
    # Filtros de precio
    precio_min_filtro: float = 0.0
    precio_max_filtro: float = 1000000.0
    
    # ==========================================
    # 💡 COMPUTED VARS OPTIMIZADAS CON CACHE
    # ==========================================
    
    @rx.var(cache=True)
    def servicios_filtrados(self) -> List[ServicioModel]:
        """
        Lista de servicios filtrada y optimizada con cache
        Aplica búsquedas, filtros y ordenamiento
        """
        if not self.lista_servicios:
            return []
        
        try:
            resultado = self.lista_servicios.copy()
            
            # Aplicar búsqueda si hay término (mínimo 2 caracteres)
            if self.termino_busqueda_servicios and len(self.termino_busqueda_servicios) >= 2:
                termino_lower = self.termino_busqueda_servicios.lower()
                resultado = [
                    serv for serv in resultado
                    if (termino_lower in serv.nombre.lower() or
                        termino_lower in serv.codigo.lower() or
                        (serv.descripcion and termino_lower in serv.descripcion.lower()) or
                        (serv.categoria and termino_lower in serv.categoria.lower()))
                ]
            
            # Filtro por categoría
            if self.filtro_categoria != "todas":
                resultado = [serv for serv in resultado if serv.categoria == self.filtro_categoria]
            
            # Filtro por estado
            if self.filtro_estado_servicio == "activos":
                resultado = [serv for serv in resultado if serv.activo]
            elif self.filtro_estado_servicio == "inactivos":
                resultado = [serv for serv in resultado if not serv.activo]
            
            # Filtro por rango de precio
            if self.filtro_rango_precio != "todos":
                resultado = self._aplicar_filtro_precio(resultado, self.filtro_rango_precio)
            
            # Aplicar ordenamiento
            if self.campo_ordenamiento_servicios == "nombre":
                resultado = sorted(resultado, key=lambda x: x.nombre)
            elif self.campo_ordenamiento_servicios == "precio":
                resultado = sorted(resultado, key=lambda x: x.precio_base or 0)
            elif self.campo_ordenamiento_servicios == "categoria":
                resultado = sorted(resultado, key=lambda x: x.categoria or "")
            elif self.campo_ordenamiento_servicios == "popularidad":
                # Ordenar por servicios más usados (requiere estadísticas)
                resultado = sorted(resultado, key=lambda x: x.veces_usado or 0, reverse=True)
            
            # Aplicar dirección de ordenamiento
            if self.direccion_ordenamiento_servicios == "desc":
                resultado.reverse()
            
            return resultado
            
        except Exception as e:
            logger.error(f"Error en servicios_filtrados: {e}")
            return []
    
    @rx.var(cache=True)
    def servicios_paginados(self) -> List[ServicioModel]:
        """Lista paginada de servicios filtrados"""
        try:
            inicio = (self.pagina_actual_servicios - 1) * self.servicios_por_pagina
            fin = inicio + self.servicios_por_pagina
            return self.servicios_filtrados[inicio:fin]
        except Exception:
            return []
    
    @rx.var(cache=True)
    def info_paginacion_servicios(self) -> Dict[str, int]:
        """Información de paginación de servicios"""
        try:
            total_filtrado = len(self.servicios_filtrados)
            total_paginas = max(1, (total_filtrado + self.servicios_por_pagina - 1) // self.servicios_por_pagina)
            
            return {
                "pagina_actual": self.pagina_actual_servicios,
                "total_paginas": total_paginas,
                "total_items": total_filtrado,
                "items_por_pagina": self.servicios_por_pagina,
                "item_inicio": ((self.pagina_actual_servicios - 1) * self.servicios_por_pagina) + 1,
                "item_fin": min(self.pagina_actual_servicios * self.servicios_por_pagina, total_filtrado)
            }
        except Exception:
            return {
                "pagina_actual": 1,
                "total_paginas": 1,
                "total_items": 0,
                "items_por_pagina": self.servicios_por_pagina,
                "item_inicio": 0,
                "item_fin": 0
            }
    
    @rx.var(cache=True)
    def servicios_por_categoria(self) -> Dict[str, List[ServicioModel]]:
        """Servicios agrupados por categoría"""
        try:
            agrupados = {}
            for servicio in self.lista_servicios:
                if servicio.activo:  # Solo servicios activos
                    categoria = servicio.categoria or "General"
                    if categoria not in agrupados:
                        agrupados[categoria] = []
                    agrupados[categoria].append(servicio)
            return agrupados
        except Exception:
            return {}
    
    @rx.var(cache=True)
    def servicios_populares(self) -> List[ServicioModel]:
        """Top 10 servicios más populares"""
        try:
            servicios_activos = [s for s in self.lista_servicios if s.activo]
            # Ordenar por veces usado (descendente) y tomar los primeros 10
            populares = sorted(
                servicios_activos, 
                key=lambda x: x.veces_usado or 0, 
                reverse=True
            )[:10]
            return populares
        except Exception:
            return []
    
    @rx.var(cache=True)
    def estadisticas_por_categoria(self) -> Dict[str, Dict[str, Any]]:
        """Estadísticas detalladas por categoría"""
        try:
            stats = {}
            for categoria, servicios in self.servicios_por_categoria.items():
                if servicios:
                    precios = [s.precio_base for s in servicios if s.precio_base]
                    stats[categoria] = {
                        "total": len(servicios),
                        "precio_promedio": sum(precios) / len(precios) if precios else 0,
                        "precio_min": min(precios) if precios else 0,
                        "precio_max": max(precios) if precios else 0,
                        "mas_popular": max(servicios, key=lambda x: x.veces_usado or 0).nombre if servicios else ""
                    }
            return stats
        except Exception:
            return {}
    
    @rx.var(cache=True)
    def servicios_activos_count(self) -> int:
        """Cantidad de servicios activos"""
        try:
            return len([s for s in self.lista_servicios if s.activo])
        except Exception:
            return 0
    
    @rx.var(cache=True)
    def precio_promedio_servicios(self) -> float:
        """Precio promedio de todos los servicios activos"""
        try:
            servicios_activos = [s for s in self.lista_servicios if s.activo and s.precio_base]
            if not servicios_activos:
                return 0.0
            return sum(s.precio_base for s in servicios_activos) / len(servicios_activos)
        except Exception:
            return 0.0
    
    # ==========================================
    # 🔄 MÉTODOS DE CARGA DE DATOS
    # ==========================================
    
    async def cargar_lista_servicios(self):
        """
        Carga la lista de servicios desde el servicio
        Disponible para todos los roles (lectura), solo Gerente puede editar
        """
        from dental_system.state.estado_auth import EstadoAuth
        
        auth_state = self.get_state(EstadoAuth)
        
        if not auth_state.is_authenticated:
            logger.warning("Usuario no autenticado intentando cargar servicios")
            return
        
        self.cargando_lista_servicios = True
        
        try:
            # Establecer contexto de usuario en el servicio
            servicios_service.set_user_context(
                user_id=auth_state.user_profile.get("id"),
                role=auth_state.user_role
            )
            
            # Obtener servicios con filtros actuales
            servicios_data = await servicios_service.get_filtered_services(
                search=self.termino_busqueda_servicios if len(self.termino_busqueda_servicios) >= 2 else None,
                categoria=self.filtro_categoria if self.filtro_categoria != "todas" else None,
                activos_only=self.filtro_estado_servicio == "activos"
            )
            
            # Convertir a modelos tipados
            self.lista_servicios = servicios_data
            self.total_servicios = len(servicios_data)
            
            # Actualizar paginación
            self._calcular_paginacion_servicios()
            
            # Log exitoso
            logger.info(f"✅ Lista servicios cargada: {len(servicios_data)} servicios")
            
        except Exception as e:
            logger.error(f"❌ Error cargando lista servicios: {e}")
            self.handle_error("Error al cargar lista de servicios", e)
            
        finally:
            self.cargando_lista_servicios = False
    
    async def cargar_estadisticas_servicios(self):
        """Carga estadísticas de servicios con cache"""
        self.cargando_estadisticas_servicios = True
        
        try:
            stats_data = await servicios_service.get_servicios_stats()
            self.estadisticas_servicios = stats_data
            self.ultima_actualizacion_stats_servicios = datetime.now().strftime("%H:%M:%S")
            
            logger.info("✅ Estadísticas de servicios actualizadas")
            
        except Exception as e:
            logger.error(f"❌ Error cargando estadísticas servicios: {e}")
        finally:
            self.cargando_estadisticas_servicios = False
    
    # ==========================================
    # 🔍 MÉTODOS DE BÚSQUEDA Y FILTROS
    # ==========================================
    
    @rx.event
    async def buscar_servicios(self, termino: str):
        """
        Búsqueda de servicios con throttling automático
        Solo busca si hay al menos 2 caracteres
        """
        self.termino_busqueda_servicios = termino.strip()
        self.busqueda_activa_servicios = True
        self.pagina_actual_servicios = 1  # Reset a primera página
        
        # Solo recargar si hay término válido o si se está limpiando
        if len(termino.strip()) >= 2 or termino.strip() == "":
            await self.cargar_lista_servicios()
        
        self.busqueda_activa_servicios = False
    
    async def filtrar_por_categoria(self, categoria: str):
        """Filtrar servicios por categoría"""
        self.filtro_categoria = categoria
        self.pagina_actual_servicios = 1
        await self.cargar_lista_servicios()
    
    async def filtrar_por_estado_servicio(self, estado: str):
        """Filtrar servicios por estado (activo/inactivo)"""
        self.filtro_estado_servicio = estado
        self.pagina_actual_servicios = 1
        await self.cargar_lista_servicios()
    
    async def filtrar_por_precio(self, rango: str):
        """Filtrar servicios por rango de precio"""
        self.filtro_rango_precio = rango
        self.pagina_actual_servicios = 1
        await self.cargar_lista_servicios()
    
    async def ordenar_servicios(self, campo: str):
        """Cambiar ordenamiento de la lista"""
        if self.campo_ordenamiento_servicios == campo:
            # Toggle dirección si es el mismo campo
            self.direccion_ordenamiento_servicios = "desc" if self.direccion_ordenamiento_servicios == "asc" else "asc"
        else:
            # Nuevo campo, empezar en ascendente
            self.campo_ordenamiento_servicios = campo
            self.direccion_ordenamiento_servicios = "asc"
        
        # Las computed vars se actualizarán automáticamente
    
    def _aplicar_filtro_precio(self, servicios: List[ServicioModel], rango: str) -> List[ServicioModel]:
        """Aplicar filtro de rango de precio"""
        try:
            if not servicios:
                return []
            
            # Calcular rangos dinámicos basados en precios existentes
            precios = [s.precio_base for s in servicios if s.precio_base and s.precio_base > 0]
            if not precios:
                return servicios
            
            precio_min = min(precios)
            precio_max = max(precios)
            
            # Dividir en 3 rangos
            rango_size = (precio_max - precio_min) / 3
            
            if rango == "bajo":
                limite = precio_min + rango_size
                return [s for s in servicios if s.precio_base and s.precio_base <= limite]
            elif rango == "medio":
                limite_min = precio_min + rango_size
                limite_max = precio_min + (2 * rango_size)
                return [s for s in servicios if s.precio_base and limite_min < s.precio_base <= limite_max]
            elif rango == "alto":
                limite = precio_min + (2 * rango_size)
                return [s for s in servicios if s.precio_base and s.precio_base > limite]
            
            return servicios
            
        except Exception as e:
            logger.error(f"Error aplicando filtro precio: {e}")
            return servicios
    
    # ==========================================
    # ➕ MÉTODOS CRUD DE SERVICIOS
    # ==========================================
    
    async def crear_servicio(self):
        """
        Crear nuevo servicio con validaciones
        Solo accesible por Gerente
        """
        from dental_system.state.estado_auth import EstadoAuth
        from dental_system.state.estado_ui import EstadoUI
        
        auth_state = self.get_state(EstadoAuth)
        ui_state = self.get_state(EstadoUI)
        
        # Verificar permisos
        if not auth_state.user_role == "gerente":
            ui_state.mostrar_toast_error("Solo el gerente puede crear servicios")
            return
        
        # Validar formulario
        if not self.validar_formulario_servicio():
            return
        
        self.cargando_operacion_servicio = True
        
        try:
            # Crear servicio
            nuevo_servicio = await servicios_service.create_service(
                form_data=self.formulario_servicio,
                user_id=auth_state.user_profile.get("id")
            )
            
            # Agregar a la lista
            self.lista_servicios.append(nuevo_servicio)
            self.total_servicios += 1
            
            # Limpiar formulario
            self.limpiar_formulario_servicio()
            
            # Cerrar modal y mostrar éxito
            ui_state.cerrar_modal("modal_servicio")
            ui_state.mostrar_toast_exito(f"Servicio {nuevo_servicio.nombre} creado exitosamente")
            
            logger.info(f"✅ Servicio creado: {nuevo_servicio.nombre}")
            
        except Exception as e:
            logger.error(f"❌ Error creando servicio: {e}")
            ui_state.mostrar_toast_error("Error al crear servicio")
            
        finally:
            self.cargando_operacion_servicio = False
    
    async def actualizar_servicio(self):
        """Actualizar servicio existente"""
        if not self.servicio_seleccionado or not self.servicio_seleccionado.id:
            return
        
        if not self.validar_formulario_servicio():
            return
        
        from dental_system.state.estado_auth import EstadoAuth
        from dental_system.state.estado_ui import EstadoUI
        
        auth_state = self.get_state(EstadoAuth)
        ui_state = self.get_state(EstadoUI)
        
        self.cargando_operacion_servicio = True
        
        try:
            # Actualizar servicio
            servicio_actualizado = await servicios_service.update_service(
                service_id=self.servicio_seleccionado.id,
                form_data=self.formulario_servicio,
                user_id=auth_state.user_profile.get("id")
            )
            
            # Actualizar en la lista
            for i, serv in enumerate(self.lista_servicios):
                if serv.id == servicio_actualizado.id:
                    self.lista_servicios[i] = servicio_actualizado
                    break
            
            # Actualizar seleccionado
            self.servicio_seleccionado = servicio_actualizado
            
            # Limpiar y cerrar
            self.limpiar_formulario_servicio()
            ui_state.cerrar_modal("modal_servicio")
            ui_state.mostrar_toast_exito("Servicio actualizado exitosamente")
            
            logger.info(f"✅ Servicio actualizado: {servicio_actualizado.nombre}")
            
        except Exception as e:
            logger.error(f"❌ Error actualizando servicio: {e}")
            ui_state.mostrar_toast_error("Error al actualizar servicio")
            
        finally:
            self.cargando_operacion_servicio = False
    
    async def activar_desactivar_servicio(self, servicio_id: str, activar: bool):
        """Activar o desactivar servicio (soft delete)"""
        from dental_system.state.estado_auth import EstadoAuth
        from dental_system.state.estado_ui import EstadoUI
        
        auth_state = self.get_state(EstadoAuth)
        ui_state = self.get_state(EstadoUI)
        
        # Verificar permisos
        if not auth_state.user_role == "gerente":
            ui_state.mostrar_toast_error("Solo el gerente puede cambiar el estado de servicios")
            return
        
        try:
            success = await servicios_service.toggle_service_status(
                service_id=servicio_id,
                activo=activar,
                user_id=auth_state.user_profile.get("id")
            )
            
            if success:
                # Actualizar en la lista
                for i, serv in enumerate(self.lista_servicios):
                    if serv.id == servicio_id:
                        self.lista_servicios[i].activo = activar
                        break
                
                accion = "activado" if activar else "desactivado"
                ui_state.mostrar_toast_exito(f"Servicio {accion} exitosamente")
                
        except Exception as e:
            logger.error(f"❌ Error cambiando estado servicio: {e}")
            ui_state.mostrar_toast_error("Error al cambiar estado del servicio")
    
    # ==========================================
    # 📝 GESTIÓN DE FORMULARIOS
    # ==========================================
    
    def cargar_servicio_en_formulario(self, servicio: ServicioModel):
        """Cargar datos de servicio en el formulario para edición"""
        self.servicio_seleccionado = servicio
        self.id_servicio_seleccionado = servicio.id
        
        # Mapear modelo a formulario
        self.formulario_servicio = {
            "codigo": servicio.codigo,
            "nombre": servicio.nombre,
            "descripcion": servicio.descripcion or "",
            "categoria": servicio.categoria or "",
            "precio_base": str(servicio.precio_base) if servicio.precio_base else "",
            "precio_minimo": str(servicio.precio_minimo) if servicio.precio_minimo else "",
            "precio_maximo": str(servicio.precio_maximo) if servicio.precio_maximo else "",
            "duracion_estimada": str(servicio.duracion_estimada) if servicio.duracion_estimada else "",
            "requiere_consulta_previa": str(servicio.requiere_consulta_previa),
            "requiere_autorizacion": str(servicio.requiere_autorizacion),
            "material_incluido": servicio.material_incluido or "",
            "instrucciones_pre": servicio.instrucciones_pre or "",
            "instrucciones_post": servicio.instrucciones_post or "",
            "observaciones": servicio.observaciones or ""
        }
        
        # Limpiar errores
        self.errores_validacion_servicio = {}
    
    def limpiar_formulario_servicio(self):
        """Limpiar todos los datos del formulario"""
        self.formulario_servicio = {}
        self.errores_validacion_servicio = {}
        self.servicio_seleccionado = ServicioModel()
        self.id_servicio_seleccionado = ""
    
    def actualizar_campo_formulario_servicio(self, campo: str, valor: str):
        """Actualizar campo específico del formulario"""
        if not self.formulario_servicio:
            self.formulario_servicio = {}
        
        self.formulario_servicio[campo] = valor
        
        # Limpiar error específico del campo
        if campo in self.errores_validacion_servicio:
            del self.errores_validacion_servicio[campo]
    
    def validar_formulario_servicio(self) -> bool:
        """
        Validar datos del formulario de servicio
        Returns True si es válido, False caso contrario
        """
        self.errores_validacion_servicio = {}
        
        # Campos requeridos
        campos_requeridos = [
            "nombre", "categoria", "precio_base"
        ]
        
        for campo in campos_requeridos:
            valor = self.formulario_servicio.get(campo, "").strip()
            if not valor:
                self.errores_validacion_servicio[campo] = "Este campo es requerido"
        
        # Validaciones específicas
        
        # Precio base válido
        precio_base = self.formulario_servicio.get("precio_base", "").strip()
        if precio_base:
            try:
                precio = float(precio_base)
                if precio <= 0:
                    self.errores_validacion_servicio["precio_base"] = "El precio debe ser mayor a 0"
            except ValueError:
                self.errores_validacion_servicio["precio_base"] = "Precio inválido"
        
        # Validar rango de precios
        precio_min = self.formulario_servicio.get("precio_minimo", "").strip()
        precio_max = self.formulario_servicio.get("precio_maximo", "").strip()
        
        if precio_min and precio_max and precio_base:
            try:
                p_min = float(precio_min)
                p_max = float(precio_max)
                p_base = float(precio_base)
                
                if p_min > p_base:
                    self.errores_validacion_servicio["precio_minimo"] = "Precio mínimo no puede ser mayor al precio base"
                if p_max < p_base:
                    self.errores_validacion_servicio["precio_maximo"] = "Precio máximo no puede ser menor al precio base"
                if p_min > p_max:
                    self.errores_validacion_servicio["precio_maximo"] = "Precio máximo debe ser mayor al mínimo"
                    
            except ValueError:
                pass  # Ya se validó en precio_base
        
        # Duración válida
        duracion = self.formulario_servicio.get("duracion_estimada", "").strip()
        if duracion:
            try:
                dur = int(duracion)
                if dur <= 0:
                    self.errores_validacion_servicio["duracion_estimada"] = "La duración debe ser mayor a 0"
            except ValueError:
                self.errores_validacion_servicio["duracion_estimada"] = "Duración debe ser un número entero"
        
        return len(self.errores_validacion_servicio) == 0
    
    # ==========================================
    # 📄 MÉTODOS DE PAGINACIÓN
    # ==========================================
    
    def siguiente_pagina_servicios(self):
        """Ir a la siguiente página"""
        info = self.info_paginacion_servicios
        if self.pagina_actual_servicios < info["total_paginas"]:
            self.pagina_actual_servicios += 1
    
    def pagina_anterior_servicios(self):
        """Ir a la página anterior"""
        if self.pagina_actual_servicios > 1:
            self.pagina_actual_servicios -= 1
    
    def ir_a_pagina_servicios(self, numero_pagina: int):
        """Ir a una página específica"""
        info = self.info_paginacion_servicios
        if 1 <= numero_pagina <= info["total_paginas"]:
            self.pagina_actual_servicios = numero_pagina
    
    def cambiar_servicios_por_pagina(self, cantidad: int):
        """Cambiar cantidad de servicios por página"""
        self.servicios_por_pagina = cantidad
        self.pagina_actual_servicios = 1  # Reset a primera página
        self._calcular_paginacion_servicios()
    
    def _calcular_paginacion_servicios(self):
        """Recalcular paginación basado en filtros actuales"""
        total_filtrado = len(self.servicios_filtrados)
        self.total_paginas_servicios = max(1, (total_filtrado + self.servicios_por_pagina - 1) // self.servicios_por_pagina)
        
        # Asegurar que la página actual sea válida
        if self.pagina_actual_servicios > self.total_paginas_servicios:
            self.pagina_actual_servicios = max(1, self.total_paginas_servicios)
    
    # ==========================================
    # 🔧 MÉTODOS DE UTILIDAD Y CACHE
    # ==========================================
    
    def handle_error(self, contexto: str, error: Exception):
        """Manejar errores de manera centralizada"""
        logger.error(f"{contexto}: {str(error)}")
        
        # Obtener estado UI para mostrar notificaciones
        try:
            from dental_system.state.estado_ui import EstadoUI
            ui_state = self.get_state(EstadoUI)
            ui_state.mostrar_toast_error(f"Error: {contexto}")
        except Exception:
            # Si no se puede acceder al estado UI, solo log
            pass
    
    def limpiar_cache_servicios(self):
        """Limpiar cache de servicios para forzar recarga"""
        self.cache_servicios_populares = []
        self.cache_servicios_por_categoria = {}
        self.cache_timestamp_servicios = ""
        logger.info("🧹 Cache de servicios limpiado")
    
    async def refrescar_datos_servicios(self):
        """Refrescar todos los datos de servicios"""
        self.limpiar_cache_servicios()
        await self.cargar_lista_servicios()
        await self.cargar_estadisticas_servicios()
        logger.info("🔄 Datos de servicios refrescados")
    
    # ==========================================
    # 📊 MÉTODOS DE ANÁLISIS Y REPORTES
    # ==========================================
    
    def obtener_servicio_por_id(self, servicio_id: str) -> Optional[ServicioModel]:
        """Obtener servicio específico por ID"""
        try:
            return next(
                (s for s in self.lista_servicios if s.id == servicio_id),
                None
            )
        except Exception:
            return None
    
    def calcular_precio_con_descuento(self, servicio_id: str, descuento_pct: float) -> float:
        """Calcular precio final con descuento aplicado"""
        try:
            servicio = self.obtener_servicio_por_id(servicio_id)
            if not servicio or not servicio.precio_base:
                return 0.0
            
            descuento = (descuento_pct / 100) * servicio.precio_base
            precio_final = servicio.precio_base - descuento
            
            # Asegurar que no baje del precio mínimo
            if servicio.precio_minimo and precio_final < servicio.precio_minimo:
                return servicio.precio_minimo
            
            return precio_final
            
        except Exception:
            return 0.0
    
    # ==========================================
    # 🏥 MÉTODOS AUXILIARES PARA APPSTATE
    # ==========================================
    
    @rx.event
    async def cargar_lista_servicios(self):
        """📋 CARGAR LISTA COMPLETA DE SERVICIOS - COORDINACIÓN CON APPSTATE"""
        try:
            self.cargando_lista_servicios = True
            
            # Cargar desde el servicio
            servicios_data = await servicios_service.get_all_services()
            
            # Convertir a modelos tipados
            self.lista_servicios = [
                ServicioModel.from_dict(servicio) 
                for servicio in servicios_data
            ]
            self.total_servicios = len(self.lista_servicios)
            
            logger.info(f"✅ {len(self.lista_servicios)} servicios cargados")
            
        except Exception as e:
            logger.error(f"❌ Error cargando servicios: {str(e)}")
        finally:
            self.cargando_lista_servicios = False
    
    @rx.event
    async def aplicar_filtros_servicios(self, filtros: Dict[str, Any]):
        """🔍 APLICAR FILTROS DE SERVICIOS - COORDINACIÓN CON APPSTATE"""
        try:
            # Aplicar filtros individuales
            if "categoria" in filtros:
                self.filtro_categoria = filtros["categoria"]
            
            if "estado" in filtros:
                self.filtro_estado_servicio = filtros["estado"]
            
            if "mostrar_solo_activos" in filtros:
                self.mostrar_solo_activos_servicios = filtros["mostrar_solo_activos"]
            
            if "rango_precio" in filtros:
                self.filtro_rango_precio_servicios = filtros["rango_precio"]
            
            logger.info(f"✅ Filtros de servicios aplicados: {filtros}")
            
        except Exception as e:
            logger.error(f"❌ Error aplicando filtros servicios: {str(e)}")
    
    def limpiar_datos(self):
        """🧹 LIMPIAR TODOS LOS DATOS - USADO EN LOGOUT"""
        self.lista_servicios = []
        self.total_servicios = 0
        self.servicio_seleccionado = ServicioModel()
        self.id_servicio_seleccionado = ""
        self.formulario_servicio = {}
        self.formulario_servicio_data = ServicioFormModel()
        self.errores_validacion_servicio = {}
        self.servicio_para_eliminar = None
        self.mostrar_solo_activos_servicios = True
        self.lista_categorias_servicios = []
        
        # Limpiar filtros
        self.filtro_categoria = "todas"
        self.filtro_estado_servicio = "activos"
        self.filtro_rango_precio_servicios = {"min": 0.0, "max": 999999.0}
        self.termino_busqueda_servicios = ""
        self.busqueda_activa_servicios = False
        
        # Limpiar cache
        self.cache_servicios_populares = []
        self.cache_servicios_por_categoria = {}
        self.cache_timestamp_servicios = ""
        
        # Estados de carga
        self.cargando_lista_servicios = False
        self.cargando_estadisticas_servicios = False
        self.cargando_operacion_servicio = False
        
        logger.info("🧹 Datos de servicios limpiados")

