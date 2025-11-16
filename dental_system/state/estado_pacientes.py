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
from typing import Dict, Any, List
import logging
from dental_system.services.pacientes_service import pacientes_service
from dental_system.models import PacienteModel, PacienteFormModel,HistorialCompletoPaciente


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
    paciente_seleccionado: PacienteModel = PacienteModel()
    historial_completo = HistorialCompletoPaciente = HistorialCompletoPaciente()

    # Formulario de paciente (tipado v4.1)
    formulario_paciente: PacienteFormModel = PacienteFormModel()
    errores_validacion_paciente: Dict[str, str] = {}

    # ==========================================
    # 👥 FILTROS Y BÚSQUEDAS
    # ==========================================

    termino_busqueda_pacientes: str = ""
    filtro_genero: str = "todos"  # todos, masculino, femenino
    filtro_estado: str = "todos"  # todos, activos, inactivos
    filtro_rango_edad: str = "todos"  # todos, 0-17, 18-35, 36-50, 51-65, 66+

    # ==========================================
    # 👥 ESTADOS DE CARGA
    # ==========================================
    cargando_operacion_paciente: bool = False
    modal_crear_paciente_abierto: bool = False
    modal_editar_paciente_abierto: bool = False
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
        self.cargando_operacion_paciente = True
        
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

            print(f"✅ {len(pacientes_data)} pacientes cargados correctamente")
            
        except Exception as e:
            error_msg = f"Error cargando pacientes: {str(e)}"
            logger.error(error_msg)
            print(f"❌ {error_msg}")

        finally:
            self.cargando_operacion_paciente = False
    
    @rx.event
    async def crear_paciente(self):
        """
        ➕ CREAR NUEVO PACIENTE CON VALIDACIONES COMPLETAS
        """
        print("➕ Creando nuevo paciente...")
        
        self.cargando_operacion_paciente = True
        self.errores_validacion_paciente = {}
        
        try:
            # Verificar autenticación (ya disponible por mixin)
            if not self.esta_autenticado:
                raise ValueError("Usuario no autenticado para crear paciente")
            
            # Configurar contexto del usuario antes de usar servicio
            pacientes_service.set_user_context(self.id_usuario, self.perfil_usuario)

            paciente_nuevo = await pacientes_service.create_patient(self.formulario_paciente,self.id_usuario)
            
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
            self.cargando_operacion_paciente = False
    
    @rx.event
    async def guardar_paciente_formulario(self):
        """
        💾 GUARDAR PACIENTE - CREAR O ACTUALIZAR AUTOMÁTICAMENTE
        Decide automáticamente si crear nuevo paciente o actualizar existentebasándose en si hay un paciente seleccionado
        """
        try:
            if not self.formulario_paciente:
                self.errores_validacion_paciente["general"] = "No hay datos de formulario para guardar"
                return

            # ✅ DECISIÓN AUTOMÁTICA: Crear o Actualizar
            if self.paciente_seleccionado.id and self.modal_editar_paciente_abierto:
                # MODO EDITAR: Actualizar paciente existente
                print(f"✏️ Modo EDITAR - Actualizando paciente {self.paciente_seleccionado.id}")
                await self.actualizar_paciente()
            else:
                # MODO CREAR: Crear nuevo paciente
                print("➕ Modo CREAR - Creando nuevo paciente")
                resultado = await self.crear_paciente()

                if not resultado:
                    return  # Si hay errores, no continuar

            # Solo proceder si la operación fue exitosa
            if not self.errores_validacion_paciente:
                
                await self.cargar_lista_pacientes()
                # Cerrar el modal
                self.cerrar_todos_los_modales()
                # Limpiar el formulario
                self.formulario_paciente = PacienteFormModel()
                self.paciente_seleccionado = PacienteModel()
                self.paso_formulario_paciente = 0
                print("✅ Paciente guardado exitosamente, modal cerrado y lista actualizada")

        except Exception as e:
            logger.error(f"❌ Error guardando paciente desde formulario: {e}")
            self.errores_validacion_paciente["general"] = f"Error guardando paciente: {str(e)}"
    
    @rx.event
    def actualizar_campo_paciente(self, campo: str, valor: str):
        """
        📝 ACTUALIZAR CAMPO ESPECÍFICO DEL FORMULARIO DE PACIENTE
        """
        try:
            # Inicializar modelo tipado si no existe
            if not self.formulario_paciente:
                self.formulario_paciente = PacienteFormModel()
            
            # Usar setattr para actualizar campo en modelo tipado
            if hasattr(self.formulario_paciente, campo):
                setattr(self.formulario_paciente, campo, valor)
            else:
                print(f"⚠️ Campo {campo} no existe en PacienteFormModel")
            
            # Limpiar error específico del campo si existe
            if campo in self.errores_validacion_paciente:
                del self.errores_validacion_paciente[campo]
        except Exception as e:
            logger.error(f"❌ Error actualizando campo {campo}: {e}")
    
    @rx.event
    async def actualizar_paciente(self):
        """
        ✏️ ACTUALIZAR PACIENTE EXISTENTE
        """
        print(f"✏️ Actualizando paciente {self.paciente_seleccionado.id}...")
        
        self.cargando_operacion_paciente = True
        self.errores_validacion_paciente = {}
        
        try:
            # Configurar contexto del usuario antes de usar servicio
            pacientes_service.set_user_context(self.id_usuario, self.perfil_usuario)
            
            # Actualizar usando el servicio
            paciente_actualizado = await pacientes_service.update_patient(self.paciente_seleccionado.id, self.formulario_paciente)
            print(f"✅ Paciente actualizado: {paciente_actualizado.primer_nombre} {paciente_actualizado.primer_apellido}")

        except Exception as e:
            error_msg = f"Error actualizando paciente: {str(e)}"
            self.errores_validacion_paciente["general"] = error_msg
            logger.error(error_msg)
            print(f"❌ {error_msg}")
            
        finally:
            self.cargando_operacion_paciente = False
    
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
                print(f"🎯 Paciente seleccionado: {paciente_encontrado.primer_nombre} {paciente_encontrado.primer_apellido}")
            else:
                pacientes_service.set_user_context(self.id_usuario, self.perfil_usuario)
                paciente_data = await pacientes_service.get_patient_by_id(id_paciente)
                if paciente_data:
                    self.paciente_seleccionado = paciente_data
                    print(f"🎯 Paciente cargado y seleccionado: {paciente_data.primer_nombre}")
                else:
                    print(f"⚠️ Paciente {id_paciente} no encontrado")
                    
        except Exception as e:
            error_msg = f"Error seleccionando paciente: {str(e)}"
            logger.error(error_msg)
            print(f"❌ {error_msg}")

  

    # ==========================================
    # 👥 BÚSQUEDA
    # ==========================================

    @rx.event
    async def buscar_pacientes(self, termino: str):
        self.termino_busqueda_pacientes = termino.strip()
        print(f"🔍 Búsqueda de pacientes: '{self.termino_busqueda_pacientes}'")
        await self.cargar_lista_pacientes()

    @rx.event
    async def set_filtro_genero(self, genero: str):
        """Establecer filtro por género"""
        self.filtro_genero = genero
        print(f"🔍 Filtro de género: '{self.filtro_genero}'")
        await self.cargar_lista_pacientes()

    # ==========================================
    # 👥 COMPUTED VARS CON CACHE
    # ==========================================

    @rx.var(cache=True)
    def pacientes_filtrados_display(self) -> List[PacienteModel]:
        """📋 Lista de pacientes para mostrar con filtrado por edad y género"""
        pacientes = self.lista_pacientes

        # Filtrar por rango de edad
        if self.filtro_rango_edad and self.filtro_rango_edad != "todos":
            if self.filtro_rango_edad == "0-17":
                pacientes = [p for p in pacientes if 0 <= p.edad <= 17]
            elif self.filtro_rango_edad == "18-35":
                pacientes = [p for p in pacientes if 18 <= p.edad <= 35]
            elif self.filtro_rango_edad == "36-50":
                pacientes = [p for p in pacientes if 36 <= p.edad <= 50]
            elif self.filtro_rango_edad == "51-65":
                pacientes = [p for p in pacientes if 51 <= p.edad <= 65]
            elif self.filtro_rango_edad == "66+":
                pacientes = [p for p in pacientes if p.edad >= 66]

        # Filtrar por género
        if self.filtro_genero and self.filtro_genero != "todos":
            pacientes = [p for p in pacientes if p.genero == self.filtro_genero]

        return pacientes

    @rx.var(cache=True)
    def total_pacientes_activos(self) -> int:
        """👥 Total de pacientes activos"""
        return len([p for p in self.lista_pacientes if p.activo])
    
    @rx.var
    def total_pacientes_masculinos(self) -> int:
        """👨 Total de pacientes masculinos"""
        return len([p for p in self.lista_pacientes if p.genero == "masculino"])
    
    @rx.var
    def total_pacientes_femeninos(self) -> int:
        """👨 Total de pacientes masculinos"""
        return len([p for p in self.lista_pacientes if p.genero == "femenino"])

    # ==========================================
    # 🎂 FUNCIÓN HELPER PARA CALCULAR EDAD
    # ==========================================

    def calcular_edad_desde_fecha(self, fecha_nacimiento: str) -> int:
        """
        🎂 Calcular edad desde fecha de nacimiento (función helper para componentes)

        Args:
            fecha_nacimiento: String en formato YYYY-MM-DD

        Returns:
            Edad en años (0 si no hay fecha válida)
        """
        if not fecha_nacimiento:
            return 0

        try:
            from datetime import date, datetime
            # Convertir string fecha a objeto date
            if isinstance(fecha_nacimiento, str) and fecha_nacimiento:
                fecha_nac = datetime.strptime(fecha_nacimiento, "%Y-%m-%d").date()
            else:
                return 0

            hoy = date.today()
            edad = hoy.year - fecha_nac.year

            # Ajustar si aún no ha cumplido años este año
            if (hoy.month, hoy.day) < (fecha_nac.month, fecha_nac.day):
                edad -= 1

            return max(0, edad)
        except Exception as e:
            print(f"Error calculando edad: {e}")
            return 0

    # ==========================================
    # 👥 MÉTODOS AUXILIARES
    # ==========================================
    
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

                if self.paciente_seleccionado:
                    self.cargar_paciente_en_formulario(self.paciente_seleccionado)
                # Abrir modal editar
                self.modal_editar_paciente_abierto = True

            else:
                # Modo crear: limpiar selección
                self.paciente_seleccionado = PacienteModel()
                self.formulario_paciente = PacienteFormModel()
                self.errores_validacion_paciente = {}
                # Abrir modal crear
                self.modal_crear_paciente_abierto = True

                
        except Exception as e:
            logger.error(f"❌ Error abriendo modal paciente: {e}")
    
    def cargar_paciente_en_formulario(self, paciente: PacienteModel):
        """Cargar datos de paciente en el formulario para edición"""
        self.paciente_seleccionado = paciente

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

            
            # Contacto y ubicación (usando celular v4.1)
            celular_1=getattr(paciente, 'celular_1', '') or getattr(paciente, 'telefono_1', '') or "",
            celular_2=getattr(paciente, 'celular_2', '') or getattr(paciente, 'telefono_2', '') or "",
            email=paciente.email or "",
            direccion=paciente.direccion or "",
            ciudad=paciente.ciudad or "",
            # Información médica
            alergias=", ".join(paciente.alergias) if isinstance(paciente.alergias, list) else str(paciente.alergias or ""),
            medicamentos_actuales=", ".join(paciente.medicamentos_actuales) if isinstance(paciente.medicamentos_actuales, list) else str(paciente.medicamentos_actuales or ""),
            condiciones_medicas=", ".join(paciente.condiciones_medicas) if isinstance(paciente.condiciones_medicas, list) else str(paciente.condiciones_medicas or ""),

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
            
            pacientes_service.set_user_context(self.id_usuario, self.perfil_usuario)
            self.historial_completo = await pacientes_service.get_historial_completo_paciente(id_paciente)
            
            self.paciente_actual = self.paciente_seleccionado
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
        if not self.paciente_seleccionado.id:
            return []
        return [
            c for c in self.lista_consultas
            if c.paciente_id == self.paciente_seleccionado.id
        ]

    # ==========================================
    # COMPUTED VARS PARA HISTORIAL DEL PACIENTE
    # ==========================================

    @rx.var(cache=True)
    def contacto_emergencia_nombre(self) -> str:
        """Nombre del contacto de emergencia"""
        if not self.paciente_seleccionado or not self.paciente_seleccionado.contacto_emergencia:
            return "No registrado"
        return self.paciente_seleccionado.contacto_emergencia.get("nombre", "No registrado")

    @rx.var(cache=True)
    def contacto_emergencia_relacion(self) -> str:
        """Relación del contacto de emergencia"""
        if not self.paciente_seleccionado or not self.paciente_seleccionado.contacto_emergencia:
            return "No registrado"
        return self.paciente_seleccionado.contacto_emergencia.get("relacion", "No registrado")

    @rx.var(cache=True)
    def contacto_emergencia_telefono(self) -> str:
        """Teléfono del contacto de emergencia"""
        if not self.paciente_seleccionado or not self.paciente_seleccionado.contacto_emergencia:
            return "No registrado"
        return self.paciente_seleccionado.contacto_emergencia.get("telefono", "No registrado")