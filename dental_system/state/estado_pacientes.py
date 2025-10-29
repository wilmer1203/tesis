"""
👥 ESTADO DE PACIENTES - SUBSTATE SEPARADO
==========================================

PROPÓSITO: Manejo centralizado y especializado de gestión de pacientes
- CRUD completo de pacientes con validaciones
- Búsquedas y filtros optimizados
- Cache inteligente para performance
- Integración con servicio de pacientes
- Estadísticas y métricas de pacientes

USADO POR: AppState como coordinador principal  
PATRÓN: Substate con get_estado_pacientes() en AppState
"""

import reflex as rx
from datetime import date, datetime
from typing import Dict, Any, List, Optional, Union
import logging

# Servicios y modelos
from dental_system.services.pacientes_service import pacientes_service
from dental_system.models import (
    PacienteModel, 
    PacientesStatsModel, 
    ContactoEmergenciaModel,
    PacienteFormModel
)

logger = logging.getLogger(__name__)

class EstadoPacientes(rx.State,mixin=True):
    """
    👥 ESTADO ESPECIALIZADO EN GESTIÓN DE PACIENTES
    
    RESPONSABILIDADES:
    - CRUD completo de pacientes con validaciones de negocio
    - Sistema de búsquedas y filtros optimizados
    - Cache inteligente para mejorar performance
    - Estadísticas y métricas de pacientes
    - Gestión de contactos de emergencia
    - Validaciones de unicidad (cédula, email, etc.)
    """
    
    # ==========================================
    # 👥 VARIABLES PRINCIPALES DE PACIENTES
    # ==========================================
    
    # Lista principal de pacientes (modelos tipados)
    lista_pacientes: List[PacienteModel] = []
    total_pacientes: int = 0
    
    # Paciente seleccionado para operaciones
    paciente_seleccionado: PacienteModel = PacienteModel()
    id_paciente_seleccionado: str = ""
    
    # Formulario de paciente (tipado v4.1)
    formulario_paciente: PacienteFormModel = PacienteFormModel()
    errores_validacion_paciente: Dict[str, str] = {}
    
    # Variables auxiliares para operaciones
    paciente_para_eliminar: Optional[PacienteModel] = None
    mostrar_solo_activos_pacientes: bool = True
    
    # ==========================================
    # 👥 FILTROS Y BÚSQUEDAS OPTIMIZADAS
    # ==========================================
    
    # Búsqueda principal
    termino_busqueda_pacientes: str = ""
    busqueda_activa: bool = False
    
    # Filtros avanzados
    filtro_genero: str = "todos"  # todos, masculino, femenino
    filtro_estado: str = "activos"  # todos, activos, inactivos
    # UNUSED - [2025-01-04] - Filtros no implementados en UI
    # filtro_edad_min: int = 0
    # filtro_edad_max: int = 120
    # filtro_ciudad: str = ""
    
    # Ordenamiento
    campo_ordenamiento: str = "nombre"  # nombre, fecha_registro, edad
    direccion_ordenamiento: str = "asc"  # asc, desc
    
    # Paginación
    pagina_actual_pacientes: int = 1
    pacientes_por_pagina: int = 20
    total_paginas_pacientes: int = 1
    
    # ==========================================
    # 👥 ESTADÍSTICAS Y MÉTRICAS CACHE
    # ==========================================
    
    # Estadísticas principales
    estadisticas_pacientes: PacientesStatsModel = PacientesStatsModel()
    ultima_actualizacion_stats: str = ""
    
    # UNUSED - [2025-01-04] - Variables de cache no utilizadas
    # cache_pacientes_activos: List[PacienteModel] = []
    # cache_timestamp_activos: str = ""
    # cache_validez_minutos: int = 15
    
    # Estados de carga
    cargando_lista_pacientes: bool = False
    cargando_estadisticas: bool = False
    cargando_operacion: bool = False
    
   
    # ==========================================
    # 👥 MÉTODOS PRINCIPALES DE CRUD
    # ==========================================
    
    @rx.event
    async def cargar_lista_pacientes(self):
        """
        📋 CARGAR LISTA COMPLETA DE PACIENTES CON CACHE
        
        Args:
            forzar_refresco: Forzar recarga desde BD ignorando cache
        """
        print("👥 Cargando lista de pacientes...")
        
        self.cargando_lista_pacientes = True
        
        try:
            # Configurar contexto del usuario antes de usar servicio
            pacientes_service.set_user_context(self.id_usuario, self.perfil_usuario)
            
            # Obtener datos desde el servicio
            pacientes_data = await pacientes_service.get_filtered_patients(
                search=self.termino_busqueda_pacientes if self.termino_busqueda_pacientes.strip() else None,
                genero=self.filtro_genero if self.filtro_genero != "todos" else None,
                activos_only=self.filtro_estado == "activos" if self.filtro_estado != "todos" else None
            )
            
            # Convertir a modelos tipados y actualizar estado
            self.lista_pacientes = pacientes_data
            self.total_pacientes = len(pacientes_data)
            # Calcular paginación
            self._actualizar_paginacion()
            
            print(f"✅ {self.total_pacientes} pacientes cargados correctamente")
            
        except Exception as e:
            error_msg = f"Error cargando pacientes: {str(e)}"
            logger.error(error_msg)
            print(f"❌ {error_msg}")

        finally:
            self.cargando_lista_pacientes = False
    
    @rx.event
    async def crear_paciente(self, datos_formulario: Dict[str, Any]):
        """
        ➕ CREAR NUEVO PACIENTE CON VALIDACIONES COMPLETAS
        
        Args:
            datos_formulario: Diccionario con datos del formulario
        """
        print("➕ Creando nuevo paciente...")
        
        self.cargando_operacion = True
        self.errores_validacion_paciente = {}
        
        try:
            # Verificar autenticación (ya disponible por mixin)
            if not self.esta_autenticado:
                raise ValueError("Usuario no autenticado para crear paciente")
            
            # Configurar contexto del usuario antes de usar servicio
            pacientes_service.set_user_context(self.id_usuario, self.perfil_usuario)
            
            # Crear paciente usando el servicio
            paciente_nuevo = await pacientes_service.create_patient(
                datos_formulario, 
                self.id_usuario  # Disponible directamente por mixin
            )
            
            # Actualizar lista local
            await self.cargar_lista_pacientes()
            
            print(f"✅ Paciente creado: {paciente_nuevo.numero_historia}")
            return paciente_nuevo
            
        except ValueError as e:
            error_msg = str(e)
            self.errores_validacion_paciente["general"] = error_msg
            logger.warning(f"Validación fallida al crear paciente: {error_msg}")
            print(f"⚠️ Error de validación: {error_msg}")
            
        except Exception as e:
            error_msg = f"Error inesperado creando paciente: {str(e)}"
            self.errores_validacion_paciente["general"] = error_msg
            logger.error(error_msg)
            print(f"❌ {error_msg}")
            
        finally:
            self.cargando_operacion = False
    
    @rx.event
    async def guardar_paciente_formulario(self):
        """
        ➕ CREAR PACIENTE USANDO DATOS DEL FORMULARIO INTERNO
        
        Método wrapper que usa self.formulario_paciente
        """
        try:
            if not self.formulario_paciente:
                self.errores_validacion_paciente["general"] = "No hay datos de formulario para guardar"
                return
            
            resultado = await self.crear_paciente(self.formulario_paciente)
            
            # Solo proceder si la creación fue exitosa
            if resultado and not self.errores_validacion_paciente:
                # Cerrar el modal
                self.cerrar_todos_los_modales()
                
                # Limpiar el formulario
                self.formulario_paciente = PacienteFormModel()    
                print("✅ Paciente guardado exitosamente, modal cerrado y lista actualizada")
            
        except Exception as e:
            logger.error(f"❌ Error guardando paciente desde formulario: {e}")
            self.errores_validacion_paciente["general"] = f"Error guardando paciente: {str(e)}"
    
    @rx.event
    def actualizar_campo_paciente(self, campo: str, valor: str):
        """
        📝 ACTUALIZAR CAMPO ESPECÍFICO DEL FORMULARIO DE PACIENTE
        
        Args:
            campo: Nombre del campo a actualizar
            valor: Nuevo valor del campo
        """
        try:
            # Inicializar modelo tipado si no existe
            if not self.formulario_paciente:
                self.formulario_paciente = PacienteFormModel()
            
            # Usar setattr para actualizar campo en modelo tipado
            if hasattr(self.formulario_paciente, campo):
                setattr(self.formulario_paciente, campo, valor)
            else:
                logger.warning(f"⚠️ Campo {campo} no existe en PacienteFormModel")
            
            # Limpiar error específico del campo si existe
            if campo in self.errores_validacion_paciente:
                del self.errores_validacion_paciente[campo]
                
            print(f"📝 Campo actualizado: {campo} = {valor}")
            
        except Exception as e:
            logger.error(f"❌ Error actualizando campo {campo}: {e}")
    
    @rx.event
    async def actualizar_paciente(self, id_paciente: str, datos_formulario: Dict[str, Any]):
        """
        ✏️ ACTUALIZAR PACIENTE EXISTENTE
        
        Args:
            id_paciente: ID del paciente a actualizar
            datos_formulario: Nuevos datos del formulario
        """
        print(f"✏️ Actualizando paciente {id_paciente}...")
        
        self.cargando_operacion = True
        self.errores_validacion_paciente = {}
        
        try:
            # Configurar contexto del usuario antes de usar servicio
            pacientes_service.set_user_context(self.id_usuario, self.perfil_usuario)
            
            # Actualizar usando el servicio
            paciente_actualizado = await pacientes_service.update_patient(
                id_paciente, 
                datos_formulario
            )
            
            # Actualizar en lista local
            for i, paciente in enumerate(self.lista_pacientes):
                if paciente.id == id_paciente:
                    self.lista_pacientes[i] = paciente_actualizado
                    break
            
            # Actualizar paciente seleccionado si corresponde
            if self.id_paciente_seleccionado == id_paciente:
                self.paciente_seleccionado = paciente_actualizado
            
            # REMOVED - [2025-01-04] - Referencias a cache comentadas
            # self._invalidar_cache_pacientes()
            
            print(f"✅ Paciente {id_paciente} actualizado correctamente")
            return paciente_actualizado
            
        except Exception as e:
            error_msg = f"Error actualizando paciente: {str(e)}"
            self.errores_validacion_paciente["general"] = error_msg
            logger.error(error_msg)
            print(f"❌ {error_msg}")
            
        finally:
            self.cargando_operacion = False
    
    @rx.event
    async def eliminar_paciente(self, id_paciente: str):
        """
        🗑️ ELIMINAR PACIENTE (SOFT DELETE)
        
        Args:
            id_paciente: ID del paciente a eliminar
        """
        print(f"🗑️ Eliminando paciente {id_paciente}...")
        
        self.cargando_operacion = True
        
        try:
            # Configurar contexto del usuario antes de usar servicio
            pacientes_service.set_user_context(self.id_usuario, self.perfil_usuario)
            
            # Eliminar usando el servicio (soft delete)
            resultado = await pacientes_service.delete_patient(id_paciente)
            
            if resultado:
                # Remover de lista local
                self.lista_pacientes = [p for p in self.lista_pacientes if p.id != id_paciente]
                self.total_pacientes -= 1
                
                # Limpiar selección si era el paciente eliminado
                if self.id_paciente_seleccionado == id_paciente:
                    self.paciente_seleccionado = PacienteModel()
                    self.id_paciente_seleccionado = ""
                
                # Invalidar cache
                self._invalidar_cache_pacientes()
                
                print(f"✅ Paciente {id_paciente} eliminado correctamente")
                return True
            else:
                print(f"⚠️ No se pudo eliminar el paciente {id_paciente}")
                return False
                
        except Exception as e:
            error_msg = f"Error eliminando paciente: {str(e)}"
            logger.error(error_msg)
            print(f"❌ {error_msg}")
            return False
            
        finally:
            self.cargando_operacion = False
    
    @rx.event
    async def ejecutar_eliminar_paciente(self):
        """
        🗑️ EJECUTAR ELIMINACIÓN DEL PACIENTE SELECCIONADO
        
        Utiliza self.paciente_para_eliminar para eliminar el paciente
        """
        if self.paciente_para_eliminar and self.paciente_para_eliminar.id:
            await self.eliminar_paciente(self.paciente_para_eliminar.id)
            # Limpiar variable después de eliminar
            self.paciente_para_eliminar = None
        else:
            print("❌ No hay paciente seleccionado para eliminar")
    
    @rx.event
    async def seleccionar_paciente(self, id_paciente: str):
        """
        🎯 SELECCIONAR PACIENTE PARA OPERACIONES
        
        Args:
            id_paciente: ID del paciente a seleccionar
        """
        try:
            # Buscar en lista local primero
            paciente_encontrado = None
            for paciente in self.lista_pacientes:
                if paciente.id == id_paciente:
                    paciente_encontrado = paciente
                    break
            
            if paciente_encontrado:
                self.paciente_seleccionado = paciente_encontrado
                self.id_paciente_seleccionado = id_paciente
                print(f"🎯 Paciente seleccionado: {paciente_encontrado.primer_nombre} {paciente_encontrado.primer_apellido}")
            else:
                # Si no está en lista local, cargar desde servicio
                # Configurar contexto del usuario antes de usar servicio
                pacientes_service.set_user_context(self.id_usuario, self.perfil_usuario)
                paciente_data = await pacientes_service.get_patient_by_id(id_paciente)
                if paciente_data:
                    self.paciente_seleccionado = paciente_data
                    self.id_paciente_seleccionado = id_paciente
                    print(f"🎯 Paciente cargado y seleccionado: {paciente_data.primer_nombre}")
                else:
                    print(f"⚠️ Paciente {id_paciente} no encontrado")
                    
        except Exception as e:
            error_msg = f"Error seleccionando paciente: {str(e)}"
            logger.error(error_msg)
            print(f"❌ {error_msg}")
    
    # ==========================================
    # 👥 BÚSQUEDAS Y FILTROS OPTIMIZADOS
    # ==========================================
    
    @rx.event
    async def buscar_pacientes(self, termino: str):
        """
        🔍 BÚSQUEDA PRINCIPAL DE PACIENTES (CON THROTTLING)
        
        Args:
            termino: Término de búsqueda
        """
        self.termino_busqueda_pacientes = termino.strip()
        self.busqueda_activa = bool(self.termino_busqueda_pacientes)
        
        print(f"🔍 Búsqueda de pacientes: '{self.termino_busqueda_pacientes}'")
        
        # Recargar lista con filtros aplicados
        await self.cargar_lista_pacientes(forzar_refresco=True)
    
    @rx.event
    async def aplicar_filtros(self, filtros: Dict[str, Any]):
        """
        🎛️ APLICAR FILTROS AVANZADOS
        
        Args:
            filtros: Diccionario con filtros a aplicar
        """
        # Actualizar filtros
        self.filtro_genero = filtros.get("genero", "todos")
        self.filtro_estado = filtros.get("estado", "activos")
        # REMOVED - [2025-01-04] - Referencias a variables comentadas eliminadas
        # self.filtro_edad_min = filtros.get("edad_min", 0)
        # self.filtro_edad_max = filtros.get("edad_max", 120)
        # self.filtro_ciudad = filtros.get("ciudad", "")
        
        print(f"🎛️ Filtros aplicados: {filtros}")
        
        # Recargar con nuevos filtros
        await self.cargar_lista_pacientes(forzar_refresco=True)
    
    @rx.event
    def limpiar_filtros(self):
        """🧹 LIMPIAR TODOS LOS FILTROS"""
        self.termino_busqueda_pacientes = ""
        self.filtro_genero = "todos"
        self.filtro_estado = "activos"
        # REMOVED - [2025-01-04] - Referencias a variables comentadas eliminadas
        # self.filtro_edad_min = 0
        # self.filtro_edad_max = 120
        # self.filtro_ciudad = ""
        self.busqueda_activa = False
        
        print("🧹 Filtros limpiados")
    
    @rx.event
    def cambiar_ordenamiento(self, campo: str):
        """📊 CAMBIAR ORDENAMIENTO DE LISTA
        
        Args:
            campo: Campo por el cual ordenar
        """
        if self.campo_ordenamiento == campo:
            # Cambiar dirección si es el mismo campo
            self.direccion_ordenamiento = "desc" if self.direccion_ordenamiento == "asc" else "asc"
        else:
            # Nuevo campo, ordenamiento ascendente
            self.campo_ordenamiento = campo
            self.direccion_ordenamiento = "asc"
        
        # Aplicar ordenamiento local
        self._ordenar_lista_local()
        
        print(f"📊 Ordenamiento: {campo} {self.direccion_ordenamiento}")
    
    # ==========================================
    # 👥 ESTADÍSTICAS Y MÉTRICAS
    # ==========================================
    
    @rx.event
    async def cargar_estadisticas_pacientes(self, forzar_refresco: bool = False):
        """
        📊 CARGAR ESTADÍSTICAS DE PACIENTES CON CACHE
        
        Args:
            forzar_refresco: Forzar recálculo de estadísticas
        """
        # REMOVED - [2025-01-04] - Referencias a cache comentadas
        # if not forzar_refresco and self._cache_estadisticas_valido():
        #     print("✅ Usando cache de estadísticas válido")
        #     return
        
        self.cargando_estadisticas = True
        
        try:
            # Configurar contexto del usuario antes de usar servicio
            pacientes_service.set_user_context(self.id_usuario, self.perfil_usuario)
            
            # Obtener estadísticas desde el servicio
            stats = await pacientes_service.get_patients_stats()
            
            self.estadisticas_pacientes = stats
            self.ultima_actualizacion_stats = datetime.now().isoformat()
            
            print("✅ Estadísticas de pacientes actualizadas")
            
        except Exception as e:
            error_msg = f"Error cargando estadísticas: {str(e)}"
            logger.error(error_msg)
            print(f"❌ {error_msg}")
            
        finally:
            self.cargando_estadisticas = False
    
    # ==========================================
    # 👥 COMPUTED VARS CON CACHE
    # ==========================================
    
    @rx.var(cache=True)
    def pacientes_filtrados_display(self) -> List[PacienteModel]:
        """📋 Lista de pacientes para mostrar (con paginación)"""
        inicio = (self.pagina_actual_pacientes - 1) * self.pacientes_por_pagina
        fin = inicio + self.pacientes_por_pagina
        return self.lista_pacientes[inicio:fin]
    
    @rx.var(cache=True)
    def total_pacientes_activos(self) -> int:
        """👥 Total de pacientes activos"""
        return len([p for p in self.lista_pacientes if p.activo])
    
    @rx.var(cache=True)
    def total_pacientes_inactivos(self) -> int:
        """👤 Total de pacientes inactivos"""
        return len([p for p in self.lista_pacientes if not p.activo])
    
    @rx.var(cache=True)
    def distribucion_por_genero(self) -> Dict[str, int]:
        """👨‍👩‍👧‍👦 Distribución de pacientes por género"""
        distribucion = {"masculino": 0, "femenino": 0, "otro": 0}
        
        for paciente in self.lista_pacientes:
            genero = paciente.genero.lower() if paciente.genero else "otro"
            if genero in distribucion:
                distribucion[genero] += 1
            else:
                distribucion["otro"] += 1
        
        return distribucion
    
    @rx.var(cache=True)
    def pacientes_registrados_hoy(self) -> int:
        """📅 Pacientes registrados hoy"""
        hoy = date.today().isoformat()
        return len([
            p for p in self.lista_pacientes 
            if p.fecha_registro and p.fecha_registro.startswith(hoy)
        ])
    
    @rx.var(cache=True)
    def tiene_filtros_activos(self) -> bool:
        """🎛️ Verificar si hay filtros activos"""
        return (
            self.busqueda_activa or
            self.filtro_genero != "todos" or
            self.filtro_estado != "activos"
            # REMOVED - [2025-01-04] - Referencias a variables comentadas eliminadas
            # self.filtro_edad_min > 0 or
            # self.filtro_edad_max < 120 or
            # bool(self.filtro_ciudad.strip())
        )
    
    @rx.var(cache=True)
    def informacion_paginacion(self) -> str:
        """📄 Información de paginación para mostrar"""
        inicio = (self.pagina_actual_pacientes - 1) * self.pacientes_por_pagina + 1
        fin = min(self.pagina_actual_pacientes * self.pacientes_por_pagina, self.total_pacientes)
        return f"Mostrando {inicio}-{fin} de {self.total_pacientes} pacientes"
    
    @rx.var(cache=True)
    def paciente_seleccionado_valido(self) -> bool:
        """✅ Verificar si hay un paciente seleccionado válido"""
        return bool(self.id_paciente_seleccionado) and bool(self.paciente_seleccionado.id)
    
    # ==========================================
    # 👥 MÉTODOS DE UTILIDAD Y CACHE
    # ==========================================
    
    def _cache_pacientes_valido(self) -> bool:
        """⏰ Verificar si el cache de pacientes es válido"""
        if not self.cache_timestamp_activos or not self.cache_pacientes_activos:
            return False
        
        try:
            timestamp_cache = datetime.fromisoformat(self.cache_timestamp_activos)
            tiempo_transcurrido = datetime.now() - timestamp_cache
            return tiempo_transcurrido.total_seconds() < (self.cache_validez_minutos * 60)
        except:
            return False
    
    def _cache_estadisticas_valido(self) -> bool:
        """📊 Verificar si el cache de estadísticas es válido"""
        if not self.ultima_actualizacion_stats:
            return False
        
        try:
            timestamp_stats = datetime.fromisoformat(self.ultima_actualizacion_stats)
            tiempo_transcurrido = datetime.now() - timestamp_stats
            return tiempo_transcurrido.total_seconds() < (self.cache_validez_minutos * 60)
        except:
            return False
    
    def _invalidar_cache_pacientes(self):
        """🗑️ Invalidar cache de pacientes"""
        self.cache_timestamp_activos = ""
        self.ultima_actualizacion_stats = ""
        print("🗑️ Cache de pacientes invalidado")
    
    def _actualizar_paginacion(self):
        """📄 Actualizar cálculos de paginación"""
        if self.pacientes_por_pagina > 0:
            self.total_paginas_pacientes = max(1, (self.total_pacientes + self.pacientes_por_pagina - 1) // self.pacientes_por_pagina)
            
            # Ajustar página actual si es necesario
            if self.pagina_actual_pacientes > self.total_paginas_pacientes:
                self.pagina_actual_pacientes = self.total_paginas_pacientes
        else:
            self.total_paginas_pacientes = 1
    
    def _ordenar_lista_local(self):
        """📊 Ordenar lista de pacientes localmente"""
        if not self.lista_pacientes:
            return
        
        reverse = self.direccion_ordenamiento == "desc"
        
        if self.campo_ordenamiento == "nombre":
            self.lista_pacientes.sort(
                key=lambda p: f"{p.primer_nombre} {p.primer_apellido}".lower(),
                reverse=reverse
            )
        elif self.campo_ordenamiento == "fecha_registro":
            self.lista_pacientes.sort(
                key=lambda p: p.fecha_registro or "",
                reverse=reverse
            )
        elif self.campo_ordenamiento == "edad":
            self.lista_pacientes.sort(
                key=lambda p: self._calcular_edad(p.fecha_nacimiento),
                reverse=reverse
            )
    
    def _calcular_edad(self, fecha_nacimiento: Optional[str]) -> int:
        """🎂 Calcular edad a partir de fecha de nacimiento"""
        if not fecha_nacimiento:
            return 0
        
        try:
            fecha_nac = datetime.strptime(fecha_nacimiento, "%Y-%m-%d").date()
            hoy = date.today()
            edad = hoy.year - fecha_nac.year
            
            # Ajustar si no ha cumplido años este año
            if hoy.month < fecha_nac.month or (hoy.month == fecha_nac.month and hoy.day < fecha_nac.day):
                edad -= 1
            
            return max(0, edad)
        except:
            return 0
    
    # ==========================================
    # 👥 MÉTODOS DE PAGINACIÓN
    # ==========================================
    
    @rx.event
    def ir_a_pagina(self, numero_pagina: int):
        """📄 Ir a página específica"""
        if 1 <= numero_pagina <= self.total_paginas_pacientes:
            self.pagina_actual_pacientes = numero_pagina
            print(f"📄 Página actual: {numero_pagina}/{self.total_paginas_pacientes}")
    
    @rx.event
    def pagina_anterior(self):
        """⬅️ Ir a página anterior"""
        if self.pagina_actual_pacientes > 1:
            self.pagina_actual_pacientes -= 1
            print(f"⬅️ Página anterior: {self.pagina_actual_pacientes}")
    
    @rx.event
    def pagina_siguiente(self):
        """➡️ Ir a página siguiente"""
        if self.pagina_actual_pacientes < self.total_paginas_pacientes:
            self.pagina_actual_pacientes += 1
            print(f"➡️ Página siguiente: {self.pagina_actual_pacientes}")
    
    @rx.event
    def cambiar_pacientes_por_pagina(self, cantidad: int):
        """📊 Cambiar cantidad de pacientes por página"""
        self.pacientes_por_pagina = max(10, min(100, cantidad))
        self.pagina_actual_pacientes = 1  # Resetear a primera página
        self._actualizar_paginacion()
        print(f"📊 Pacientes por página: {self.pacientes_por_pagina}")
    
    # ==========================================
    # 👥 VALIDACIONES Y UTILIDADES
    # ==========================================
    
    def validar_formulario_paciente(self, datos: Dict[str, Any]) -> Dict[str, str]:
        """✅ Validar datos del formulario de paciente"""
        errores = {}
        
        # Validaciones básicas
        if not datos.get("primer_nombre", "").strip():
            errores["primer_nombre"] = "Primer nombre es requerido"
        
        if not datos.get("primer_apellido", "").strip():
            errores["primer_apellido"] = "Primer apellido es requerido"
        
        if not datos.get("numero_documento", "").strip():
            errores["numero_documento"] = "Número de documento es requerido"
        
        # Validación de email si se proporciona
        email = datos.get("email", "").strip()
        if email and "@" not in email:
            errores["email"] = "Email debe ser válido"
        
        # Validación de fecha de nacimiento
        fecha_nac = datos.get("fecha_nacimiento")
        if fecha_nac:
            try:
                fecha_nac_obj = datetime.strptime(fecha_nac, "%Y-%m-%d").date()
                if fecha_nac_obj > date.today():
                    errores["fecha_nacimiento"] = "Fecha de nacimiento no puede ser futura"
            except:
                errores["fecha_nacimiento"] = "Fecha de nacimiento inválida"
        
        return errores
    
    def obtener_paciente_por_documento(self, numero_documento: str) -> Optional[PacienteModel]:
        """🔍 Buscar paciente por número de documento"""
        for paciente in self.lista_pacientes:
            if paciente.numero_documento == numero_documento:
                return paciente
        return None
    
    def obtener_contexto_paciente_seleccionado(self) -> Dict[str, Any]:
        """📋 Obtener contexto completo del paciente seleccionado"""
        if not self.paciente_seleccionado_valido:
            return {}
        
        return {
            "paciente": self.paciente_seleccionado,
            "edad": self._calcular_edad(self.paciente_seleccionado.fecha_nacimiento),
            "tiene_contacto_emergencia": bool(self.paciente_seleccionado.contacto_emergencia.get("nombre", "")),
            "total_consultas": 0,  # Se calculará en otro substate
            "ultima_consulta": None,  # Se calculará en otro substate
        }
    
    # ==========================================
    # 👥 MÉTODOS AUXILIARES PARA APPSTATE
    # ==========================================
    
    @rx.event
    async def aplicar_filtros_pacientes(self, filtros: Dict[str, Any]):
        """🔍 APLICAR FILTROS DE PACIENTES - COORDINACIÓN CON APPSTATE"""
        try:
            # Aplicar filtros individuales
            if "genero" in filtros:
                self.filtro_genero = filtros["genero"]
            
            if "estado" in filtros:
                self.filtro_estado = filtros["estado"]
            
            if "mostrar_solo_activos" in filtros:
                self.mostrar_solo_activos_pacientes = filtros["mostrar_solo_activos"]
            
            # REMOVED - [2025-01-04] - Referencias a variables comentadas eliminadas
            # if "edad_min" in filtros:
            #     self.filtro_edad_min = filtros["edad_min"]
            #     
            # if "edad_max" in filtros:
            #     self.filtro_edad_max = filtros["edad_max"]
            
            logger.info(f"✅ Filtros aplicados: {filtros}")
            
        except Exception as e:
            logger.error(f"❌ Error aplicando filtros: {str(e)}")
    
    @rx.event  
    async def actualizar_ultimo_acceso(self, patient_id: str):
        """🕒 ACTUALIZAR ÚLTIMO ACCESO DEL PACIENTE"""
        try:
            # Actualizar en la lista local si existe
            for i, paciente in enumerate(self.lista_pacientes):
                if paciente.id == patient_id:
                    # Crear copia con último acceso actualizado
                    paciente_actualizado = PacienteModel.from_dict({
                        **paciente.__dict__,
                        "ultimo_acceso": datetime.now().isoformat()
                    })
                    self.lista_pacientes[i] = paciente_actualizado
                    break
            
            logger.info(f"✅ Último acceso actualizado para paciente: {patient_id}")
            
        except Exception as e:
            logger.error(f"❌ Error actualizando último acceso: {str(e)}")
    
    def limpiar_datos(self):
        """🧹 LIMPIAR TODOS LOS DATOS - USADO EN LOGOUT"""
        self.lista_pacientes = []
        self.total_pacientes = 0
        self.paciente_seleccionado = PacienteModel()
        self.id_paciente_seleccionado = ""
        self.formulario_paciente = PacienteFormModel()
        self.errores_validacion_paciente = {}
        self.paciente_para_eliminar = None
        self.termino_busqueda_pacientes = ""
        self.busqueda_activa = False
        self.filtro_genero = "todos"
        self.filtro_estado = "activos"
        self.mostrar_solo_activos_pacientes = True
        self.cargando_lista_pacientes = False
        self.cargando_estadisticas = False
        self.cargando_operacion = False
        
        # REMOVED - [2025-01-04] - Referencias a variables comentadas eliminadas
        # self.cache_pacientes_activos = []
        # self.cache_timestamp_activos = ""
        
        logger.info("🧹 Datos de pacientes limpiados")
    
    @rx.event
    async def seleccionar_y_abrir_modal_paciente(self, paciente_id: str = ""):
        """
        📱 Seleccionar paciente y abrir modal - Crear o Editar según ID
        
        Args:
            paciente_id: Si está vacío → Crear, Si tiene valor → Editar
        """
        try:
            if paciente_id:
                # Modo editar: seleccionar el paciente primero
                await self.seleccionar_paciente(paciente_id)
                # Cargar datos en el formulario
                if self.paciente_seleccionado:
                    self.cargar_paciente_en_formulario(self.paciente_seleccionado)
                # Abrir modal editar
                self.abrir_modal_paciente("editar")
                logger.info(f"📝 Modal editar paciente abierto: {paciente_id}")
            else:
                # Modo crear: limpiar selección
                self.paciente_seleccionado = PacienteModel()
                self.id_paciente_seleccionado = ""
                self.formulario_paciente = PacienteFormModel()
                self.errores_validacion_paciente = {}
                # Abrir modal crear
                self.abrir_modal_paciente("crear")
                logger.info("➕ Modal crear paciente abierto")
                
        except Exception as e:
            logger.error(f"❌ Error abriendo modal paciente: {e}")
    
    def cargar_paciente_en_formulario(self, paciente: PacienteModel):
        """Cargar datos de paciente en el formulario para edición"""
        self.paciente_seleccionado = paciente
        self.id_paciente_seleccionado = paciente.id
        
        # Mapear modelo a formulario tipado directamente (v4.1)
        self.formulario_paciente = PacienteFormModel(
            # Nombres completos
            primer_nombre=paciente.primer_nombre or "",
            segundo_nombre=paciente.segundo_nombre or "",
            primer_apellido=paciente.primer_apellido or "",
            segundo_apellido=paciente.segundo_apellido or "",
            
            # Identificación (usando esquema v4.1)
            tipo_documento=paciente.tipo_documento or "CI",
            numero_documento=paciente.numero_documento or "",
            numero_historia=paciente.numero_historia or "",
            
            # Información demográfica
            genero=paciente.genero or "",
            fecha_nacimiento=paciente.fecha_nacimiento or "",
            edad=str(paciente.edad) if paciente.edad else "",
            estado_civil=paciente.estado_civil or "",
            ocupacion=paciente.ocupacion or "",
            
            # Contacto y ubicación (usando celular v4.1)
            celular_1=getattr(paciente, 'celular_1', '') or getattr(paciente, 'telefono_1', '') or "",
            celular_2=getattr(paciente, 'celular_2', '') or getattr(paciente, 'telefono_2', '') or "",
            email=paciente.email or "",
            direccion=paciente.direccion or "",
            ciudad=paciente.ciudad or "",
            departamento=paciente.departamento or "",
            
            # Información médica
            alergias=", ".join(paciente.alergias) if isinstance(paciente.alergias, list) else str(paciente.alergias or ""),
            medicamentos_actuales=", ".join(paciente.medicamentos_actuales) if isinstance(paciente.medicamentos_actuales, list) else str(paciente.medicamentos_actuales or ""),
            condiciones_medicas=", ".join(paciente.condiciones_medicas) if isinstance(paciente.condiciones_medicas, list) else str(paciente.condiciones_medicas or ""),
            antecedentes_familiares=", ".join(paciente.antecedentes_familiares) if isinstance(paciente.antecedentes_familiares, list) else str(paciente.antecedentes_familiares or ""),
            observaciones_medicas=paciente.observaciones or "",
            
            # Contacto emergencia desde JSONB v4.1
            contacto_emergencia_nombre=paciente.contacto_emergencia.get("nombre", "") if isinstance(paciente.contacto_emergencia, dict) else "",
            contacto_emergencia_telefono=paciente.contacto_emergencia.get("telefono", "") if isinstance(paciente.contacto_emergencia, dict) else "",
            contacto_emergencia_relacion=paciente.contacto_emergencia.get("relacion", "") if isinstance(paciente.contacto_emergencia, dict) else "",
            contacto_emergencia_direccion=paciente.contacto_emergencia.get("direccion", "") if isinstance(paciente.contacto_emergencia, dict) else ""
        )
        
        # Limpiar errores
        self.errores_validacion_paciente = {}