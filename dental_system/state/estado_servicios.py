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
from typing import Dict, Any, List, Optional
import logging

# Servicios y modelos
from dental_system.services.servicios_service import servicios_service
from dental_system.models import (
    ServicioModel,
    ServicioStatsModel,
    EstadisticaCategoriaModel,
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

    # ==========================================
    # 🪟 CONTROL DE MODALES (COMO PERSONAL)
    # ==========================================
    modal_crear_servicio_abierto: bool = False
    modal_editar_servicio_abierto: bool = False


    # ==========================================
    # 📋 DATOS PRINCIPALES
    # ==========================================
    lista_servicios: List[ServicioModel] = []
    total_servicios: int = 0

    # ==========================================
    # 🎯 SERVICIO SELECCIONADO (COMO EMPLEADO_SELECCIONADO)
    # ==========================================
    servicio_seleccionado: Optional[ServicioModel] = None
    id_servicio_seleccionado: str = ""

    # ==========================================
    # 📝 FORMULARIO TIPADO (COMO PERSONAL)
    # ==========================================
    formulario_servicio: ServicioFormModel = ServicioFormModel()
    errores_validacion_servicio: Dict[str, str] = {}

    # Variables auxiliares para operaciones
    mostrar_solo_activos_servicios: bool = True

    # ==========================================
    # 🔄 VARIABLES TEMPORALES PARA ACCIONES (COMO PERSONAL)
    # ==========================================
    servicio_to_modify: Optional[ServicioModel] = None  # Servicio a activar/desactivar
    accion_servicio: bool = False  # True = activar, False = desactivar
    
    
    # ==========================================
    # 🏥 CATEGORÍAS Y CLASIFICACIÓN
    # ==========================================
    
    # Categorías disponibles (basadas en BD real)
    categorias_servicios: List[str] = [
        "Preventiva",
        "Restaurativa",
        "Endodoncia",
        "Cirugía",
        "Prótesis",
        "Estética",
        "Implantología",
        "Diagnóstico",
        "Consulta"
    ]

    # ==========================================
    # 🦷 CATÁLOGO DE CONDICIONES V3.0
    # ==========================================

    # Filtros por categoría
    filtro_categoria: str = "todas"
    filtro_estado_servicio: str = "activos"  # todos, activos, inactivos
    filtro_rango_precio_servicios: Dict[str, float] = {"min": 0.0, "max": 999999.0}
    
    # ==========================================
    # 🏥 BÚSQUEDAS Y FILTROS OPTIMIZADOS
    # ==========================================
    
    # Búsqueda principal con throttling
    termino_busqueda_servicios: str = ""
    
    # ==========================================
    # 🪟 ESTADOS DE MODAL
    # ==========================================
    modal_servicio_abierto: bool = False
    modo_modal_servicio: str = "crear"  # crear, editar
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
    def opciones_categoria_completas(self) -> List[str]:
        """🏷️ Lista completa de opciones para select de categorías"""
        return ["todas"] + self.categorias_servicios

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
            if precio_min <= s.precio_base_usd<= precio_max
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
        
            # Aplicar ordenamiento
            if self.campo_ordenamiento_servicios == "nombre":
                resultado = sorted(resultado, key=lambda x: x.nombre)
            elif self.campo_ordenamiento_servicios == "categoria":
                resultado = sorted(resultado, key=lambda x: x.categoria or "")
            
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
    def estadisticas_por_categoria(self) -> Dict[str, EstadisticaCategoriaModel]:
        """Estadísticas detalladas por categoría usando modelos tipados"""
        try:
            stats = {}
            for categoria, servicios in self.servicios_por_categoria.items():
                if servicios:
                    stats[categoria] = EstadisticaCategoriaModel.from_servicios_list(servicios)
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
    # 📝 COMPUTED VARS PARA FORMULARIO
    # ==========================================

    @rx.var
    def formulario_precio_usd_value(self) -> str:
        """📝 Precio USD del formulario de servicio"""
        if not self.formulario_servicio:
            return ""
        valor = str(self.formulario_servicio.precio_base_usd) if self.formulario_servicio.precio_base_usd else ""
        return valor

    # ==========================================
    # 🔄 MÉTODOS DE CARGA DE DATOS
    # ==========================================
    
    async def cargar_lista_servicios(self):
        """
        Carga la lista de servicios desde el servicio
        Disponible para todos los roles (lectura), solo Gerente puede editar
        """
        # Verificar autenticación usando propiedades del mixin
        if not self.esta_autenticado:
            logger.warning("Usuario no autenticado intentando cargar servicios")
            return
        
        self.cargando_lista_servicios = True
        
        try:
            # Establecer contexto de usuario en el servicio usando propiedades correctas del mixin
            servicios_service.set_user_context(self.id_usuario, self.perfil_usuario)
            
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
    
    async def filtrar_por_precio(self, rango: Dict[str, float]):
        """Filtrar servicios por rango de precio"""
        self.filtro_rango_precio_servicios = rango
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
        
    
    # ==========================================
    # ➕ MÉTODOS CRUD DE SERVICIOS
    # ==========================================
    
    async def crear_servicio(self):
        """
        Crear nuevo servicio con validaciones
        Solo accesible por Gerente
        """
        # Verificar permisos usando la propiedad del mixin
        if not self.rol_usuario == "gerente":
            self.mostrar_toast("Solo el gerente puede crear servicios", "error")
            return

        # Validar formulario usando modelo tipado - PATRÓN PERSONAL
        errores = self.formulario_servicio.validate_form()
        if errores:
            self.errores_validacion_servicio = {field: errores[field] for field in errores.keys()}
            return

        self.cargando_operacion_servicio = True

        try:
            # Configurar contexto del usuario antes de usar servicio
            servicios_service.set_user_context(self.id_usuario, self.perfil_usuario)

            # Crear servicio usando modelo tipado
            nuevo_servicio = await servicios_service.create_service(
                servicio_form=self.formulario_servicio,
                user_id=self.id_usuario,
            )

            if nuevo_servicio:
                # Agregar a la lista
                self.lista_servicios.append(nuevo_servicio)
                self.total_servicios += 1

                # Limpiar formulario
                self.limpiar_formulario_servicio()

                # Limpiar y cerrar modal
                self.limpiar_y_cerrar_modal_crear()

                self.mostrar_toast(f"Servicio '{nuevo_servicio.nombre}' creado exitosamente", "success")
                logger.info(f"✅ Servicio creado: {nuevo_servicio.nombre}")
            else:
                self.mostrar_toast("Error al crear servicio", "error")

        except Exception as e:
            logger.error(f"❌ Error creando servicio: {e}")
            self.mostrar_toast("Error al crear servicio", "error")

        finally:
            self.cargando_operacion_servicio = False
    
    async def actualizar_servicio(self):
        """
        Actualizar servicio existente con validaciones y manejo de errores
        """
        # Verificar que hay un servicio seleccionado
        if not self.id_servicio_seleccionado:
            self.mostrar_toast("No hay servicio seleccionado para editar", "error")
            return

        # Verificar permisos usando la propiedad del mixin
        if not self.rol_usuario == "gerente":
            self.mostrar_toast("Solo el gerente puede editar servicios", "error")
            return

        # Validar formulario
        errores = self.formulario_servicio.validate_form()
        if errores:
            self.errores_validacion_servicio = {field: errores[field] for field in errores.keys()}
            return
            
        self.cargando_operacion_servicio = True
        
        try:
            # Configurar contexto del usuario antes de usar servicio
            servicios_service.set_user_context(self.id_usuario, self.perfil_usuario)

            # Actualizar usando el servicio
            servicio_actualizado = await servicios_service.update_service(
                service_id=self.id_servicio_seleccionado,
                servicio_form=self.formulario_servicio,
            )
            
            if servicio_actualizado:
                # Actualizar en la lista local
                self.lista_servicios = [
                    servicio_actualizado if s.id == self.id_servicio_seleccionado 
                    else s for s in self.lista_servicios
                ]
                
                # Actualizar seleccionado
                self.servicio_seleccionado = servicio_actualizado
                
                # Limpiar y cerrar
                self.limpiar_y_cerrar_modal_editar()
                self.mostrar_toast(f"Servicio {servicio_actualizado.nombre} actualizado exitosamente", "success")
                
                logger.info(f"✅ Servicio actualizado: {servicio_actualizado.nombre}")
            else:
                raise ValueError("No se pudo actualizar el servicio")
                
        except Exception as e:
            logger.error(f"❌ Error actualizando servicio: {e}")
            self.mostrar_toast(f"Error al actualizar servicio: {str(e)}", "error")
            
        finally:
            self.cargando_operacion_servicio = False
    
    async def activar_desactivar_servicio(self, servicio_id: str, activar: bool):
        """
        🔄 Preparar activación o desactivación de servicio (PATRÓN PERSONAL)

        Args:
            servicio_id: ID del servicio a modificar
            activar: True para activar, False para desactivar
        """
        try:
            # Buscar el servicio en la lista
            servicio_encontrado = None
            for servicio in self.lista_servicios:
                if servicio.id == servicio_id:
                    servicio_encontrado = servicio
                    print(f"servicio encontrado {servicio_encontrado}")
                    break

            if servicio_encontrado:
                # Establecer el servicio a modificar y la acción
                self.servicio_to_modify = servicio_encontrado
                self.accion_servicio = activar

                nombre_completo = servicio_encontrado.nombre

                # Mostrar modal apropiado según la acción
                if activar:
                    # Modal de reactivación (NO es async, quitar await)
                    self.abrir_modal_confirmacion(
                        "Confirmar Reactivación",
                        f"¿Estás seguro de que deseas reactivar el servicio '{nombre_completo}'? El servicio estará disponible nuevamente en el catálogo.",
                        "activar_servicio"
                    )
                else:
                    # Modal de desactivación (NO es async, quitar await)
                    self.abrir_modal_confirmacion(
                        "Confirmar Desactivación",
                        f"¿Estás seguro de que deseas desactivar el servicio '{nombre_completo}'? El servicio no estará disponible para nuevas intervenciones.",
                        "desactivar_servicio"
                    )
                logger.info(f"❓ Confirmación {'activar' if activar else 'desactivar'} servicio: {servicio_id}")
            else:
                logger.warning(f"⚠️ Servicio {servicio_id} no encontrado")

        except Exception as e:
            logger.error(f"❌ Error preparando acción de servicio: {e}")
            self.mostrar_toast("Error al preparar la acción", "error")

    
    # ==========================================
    # 📝 GESTIÓN DE FORMULARIOS
    # ==========================================
    
    def cargar_servicio_en_formulario(self, servicio: ServicioModel):
        """Cargar datos de servicio en el formulario para edición - PATRÓN PERSONAL"""
        self.servicio_seleccionado = servicio
        self.id_servicio_seleccionado = servicio.id

        # Cargar en modelo tipado (IGUAL QUE PERSONAL)
        self.formulario_servicio = ServicioFormModel.from_servicio_model(servicio)

        # Limpiar errores
        self.errores_validacion_servicio = {}
    
    def limpiar_formulario_servicio(self):
        """Limpiar todos los datos del formulario - PATRÓN PERSONAL"""
        self.formulario_servicio = ServicioFormModel()
        self.errores_validacion_servicio = {}
        self.servicio_seleccionado = None
        self.id_servicio_seleccionado = ""
    
    def actualizar_campo_formulario_servicio(self, campo: str, valor: str):
        """Actualizar campo específico del formulario - PATRÓN PERSONAL"""
        if not self.formulario_servicio:
            self.formulario_servicio = ServicioFormModel()

        # Actualizar modelo tipado directamente
        if hasattr(self.formulario_servicio, campo):
            setattr(self.formulario_servicio, campo, valor)

        # Limpiar error específico del campo
        if campo in self.errores_validacion_servicio:
            del self.errores_validacion_servicio[campo]
    
    
    # ==========================================
    # 🪟 CONTROL DE MODALES
    # ==========================================


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
    # 🪟 MÉTODOS DE MODAL Y UI
    # ==========================================

    def limpiar_y_cerrar_modal_crear(self):
        """Limpiar y cerrar modal de crear servicio"""
        self.modal_crear_servicio_abierto = False
        self.limpiar_formulario_servicio()
        logger.info("Modal crear servicio cerrado y limpiado")

    def limpiar_y_cerrar_modal_editar(self):
        """Limpiar y cerrar modal de editar servicio"""
        self.modal_editar_servicio_abierto = False
        self.limpiar_formulario_servicio()
        self.servicio_seleccionado = ServicioModel()
        self.id_servicio_seleccionado = ""
        logger.info("Modal editar servicio cerrado y limpiado")

    @rx.event
    def limpiar_y_cerrar_modal_crear_servicio(self):
        """Limpiar y cerrar modal de crear servicio"""
        self.modal_crear_servicio_abierto = False
        self.modal_editar_servicio_abierto = False
        self.limpiar_formulario_servicio()
        self.servicio_seleccionado = ServicioModel()
        self.id_servicio_seleccionado = ""
        logger.info("Modal crear servicio cerrado y limpiado")

    @rx.event
    async def abrir_modal_crear_servicio(self):
        """🆕 Abrir modal para crear nuevo servicio"""
        # Verificar permisos
        # Limpiar formulario
        self.limpiar_formulario_servicio()
        self.servicio_seleccionado = ServicioModel()
        self.id_servicio_seleccionado = ""

        # Abrir modal directamente
        self.modal_crear_servicio_abierto = True
        logger.info("🆕 Modal crear servicio abierto")


    @rx.event
    async def seleccionar_y_abrir_modal_servicio(self, servicio_id: str = ""):
        """
        📱 Seleccionar servicio y abrir modal - Crear o Editar según ID - PATRÓN PERSONAL

        Args:
            servicio_id: Si está vacío → Crear, Si tiene valor → Editar
        """
        try:
            if servicio_id:
                # Modo editar: buscar el servicio en la lista
                servicio = next(
                    (s for s in self.lista_servicios if s.id == servicio_id),
                    None
                )

                if not servicio:
                    return

                # Guardar selección
                self.id_servicio_seleccionado = servicio_id
                self.servicio_seleccionado = servicio

                # Cargar datos en formulario (IGUAL QUE PERSONAL)
                self.cargar_servicio_en_formulario(servicio)

                # Limpiar errores previos
                self.errores_validacion_servicio = {}

                # Abrir modal editar (IGUAL QUE PERSONAL)
                self.abrir_modal_servicio("editar")
                logger.info(f"📝 Modal editar servicio abierto: {servicio_id}")
            else:
                # Modo crear: limpiar selección y abrir modal
                self.servicio_seleccionado = ServicioModel()
                self.id_servicio_seleccionado = ""
                self.limpiar_formulario_servicio()
                # Abrir modal crear
                self.abrir_modal_servicio("crear")
                logger.info("✅ Modal crear servicio abierto")

        except Exception as e:
            logger.error(f"Error abriendo modal servicio: {e}")



    @rx.event
    async def set_mostrar_solo_activos_servicios(self, mostrar_activos: bool):
        """👁️ Cambiar filtro de mostrar solo activos"""
        self.mostrar_solo_activos_servicios = mostrar_activos
        if mostrar_activos:
            self.filtro_estado_servicio = "activos"
        else:
            self.filtro_estado_servicio = "todos"
        logger.info(f"👁️ Filtro solo activos: {mostrar_activos}")


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
    
    # ==========================================
    # 🏥 MÉTODOS AUXILIARES PARA APPSTATE
    # ==========================================
    
    @rx.event
    async def cargar_servicios_basico(self):
        """📋 CARGAR LISTA BÁSICA DE SERVICIOS PARA APPSTATE"""
        try:
            self.cargando_lista_servicios = True
            
            # Establecer contexto básico si está disponible
            if hasattr(self, 'id_usuario') and self.id_usuario:
                servicios_service.set_user_context(self.id_usuario, self.perfil_usuario)
            
            # Cargar todos los servicios sin filtros complejos
            self.lista_servicios = await servicios_service.get_all_services()
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
    
    async def ejecutar_accion_servicio(self):
        """
        ✅ EJECUTAR ACCIÓN DE ACTIVAR/DESACTIVAR SERVICIO (PATRÓN PERSONAL)

        Ejecuta la acción almacenada en self.accion_servicio
        sobre el servicio en self.servicio_to_modify
        """
        if self.servicio_to_modify and self.servicio_to_modify.id:
            nombre_servicio = self.servicio_to_modify.nombre
            servicio_id = self.servicio_to_modify.id
            activar = self.accion_servicio

            try:
                # Establecer contexto de usuario en el servicio
                servicios_service.set_user_context(
                    user_id=self.id_usuario,
                    user_profile=self.perfil_usuario
                )

                # Ejecutar la acción apropiada
                if activar:
                    success = await servicios_service.reactivate_service(servicio_id)
                    accion_texto = "reactivado"
                else:
                    success = await servicios_service.deactivate_service(servicio_id)
                    accion_texto = "desactivado"

                if success:
                    # Recargar lista para reflejar cambios
                    await self.cargar_lista_servicios()

                    # Mostrar éxito
                    self.mostrar_toast(f"Servicio '{nombre_servicio}' {accion_texto} exitosamente", "success")

                    logger.info(f"✅ Servicio '{nombre_servicio}' {accion_texto} exitosamente")

                # Limpiar variables temporales
                self.servicio_to_modify = None
                self.accion_servicio = False

            except Exception as e:
                logger.error(f"❌ Error ejecutando acción de servicio: {e}")
                self.mostrar_toast(f"Error al modificar el servicio '{nombre_servicio}'", "error")
        else:
            logger.warning("❌ No hay servicio seleccionado para modificar")

    def limpiar_datos(self):
        """🧹 LIMPIAR TODOS LOS DATOS - USADO EN LOGOUT"""
        self.lista_servicios = []
        self.total_servicios = 0
        self.servicio_seleccionado = ServicioModel()
        self.id_servicio_seleccionado = ""
        self.formulario_servicio = ServicioFormModel()
        self.errores_validacion_servicio = {}
        self.mostrar_solo_activos_servicios = True

        # Limpiar variables temporales de acciones
        self.servicio_to_modify = None
        self.accion_servicio = False

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


