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
    PacienteFormModel,
    HistorialCompletoPaciente
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
    historial_completo: HistorialCompletoPaciente
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
        
        print(f"🎛️ Filtros aplicados: {filtros}")
        
        # Recargar con nuevos filtros
        await self.cargar_lista_pacientes(forzar_refresco=True)
    
    @rx.event
    def limpiar_filtros(self):
        """🧹 LIMPIAR TODOS LOS FILTROS"""
        self.termino_busqueda_pacientes = ""
        self.filtro_genero = "todos"
        self.filtro_estado = "activos"
        self.busqueda_activa = False
        
        print("🧹 Filtros limpiados")
    
 
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
    

    def _actualizar_paginacion(self):
        """📄 Actualizar cálculos de paginación"""
        if self.pacientes_por_pagina > 0:
            self.total_paginas_pacientes = max(1, (self.total_pacientes + self.pacientes_por_pagina - 1) // self.pacientes_por_pagina)
            
            # Ajustar página actual si es necesario
            if self.pagina_actual_pacientes > self.total_paginas_pacientes:
                self.pagina_actual_pacientes = self.total_paginas_pacientes
        else:
            self.total_paginas_pacientes = 1
    
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
    # 👥 MÉTODOS AUXILIARES PARA APPSTATE
    # ==========================================

    
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
            
        
    @rx.event
    async def navegar_a_historial_paciente(self, id_paciente: str):
        """
        📋 NAVEGAR A PÁGINA DE HISTORIAL DEL PACIENTE

        Args:
            id_paciente: ID del paciente a mostrar historial
        """
        try:
            # 1. Seleccionar el paciente
            await self.seleccionar_paciente(id_paciente)

            # 2. Cargar historial completo del paciente desde el servicio
            from dental_system.services.pacientes_service import pacientes_service
            pacientes_service.set_user_context(self.id_usuario, self.perfil_usuario)
            self.historial_completo = await pacientes_service.get_historial_completo_paciente(id_paciente)

            # 4. Cargar odontograma del paciente
            try:
                await self.cargar_odontograma_paciente_actual()
            except Exception as odonto_error:
                logger.warning(f"⚠️ No se pudo cargar odontograma: {odonto_error}")
                # Continuar aunque falle el odontograma

            # 5. Navegar a la página
            self.navigate_to(
                "historial-paciente",
                f"Historial de {self.paciente_seleccionado.nombre_completo}",
                f"HC: {self.paciente_seleccionado.numero_historia}"
            )

            print(f"✅ Navegando a historial de paciente {id_paciente} - {self.historial_completo.total_consultas} consultas cargadas")

        except Exception as e:
            error_msg = f"Error navegando a historial: {str(e)}"
            logger.error(error_msg)
            self.mostrar_toast(f"Error al cargar historial: {str(e)}", "error")
            
    @rx.var(cache=True)
    def consultas_del_paciente_seleccionado(self) -> List:
        """📅 Consultas del paciente seleccionado (para historial)"""
        if not self.id_paciente_seleccionado:
            return []
        return [
            c for c in self.lista_consultas
            if c.paciente_id == self.id_paciente_seleccionado
        ]