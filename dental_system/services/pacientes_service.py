"""
Servicio centralizado para gestión de pacientes
Elimina duplicación entre boss_state y admin_state
"""

from typing import Dict, List, Optional, Any
from datetime import date, datetime
from .base_service import BaseService
from .cache_invalidation_hooks import invalidate_after_patient_operation, track_cache_invalidation
from dental_system.supabase.tablas import pacientes_table
from dental_system.models import PacienteModel, PacienteFormModel,  HistorialCompletoPaciente,ConsultaHistorial,IntervencionHistorial,ServicioHistorial
import logging

logger = logging.getLogger(__name__)

class PacientesService(BaseService):
    """
    Servicio que maneja toda la lógica de pacientes
    Usado tanto por Boss (vista) como Admin (CRUD completo)
    """
    
    def __init__(self):
        super().__init__()
        self.table = pacientes_table
  
    
    
    async def get_filtered_patients(self, 
                                  search: str = None, 
                                  genero: str = None, 
                                  activos_only: Optional[bool] = None) -> List[PacienteModel]:
        """
        Obtiene pacientes filtrados 
        
        Args:
            search: Término de búsqueda
            genero: Filtro por género (masculino, femenino, todos)
            activos_only: Solo pacientes activos
            
        Returns:
            Lista de pacientes como modelos tipados
        """
        try:
                        
            # Obtener datos usando el table ya existente
            pacientes_data = self.table.get_filtered_patients(
                activos_only=activos_only,
                busqueda=search if search and search.strip() else None,
                genero=genero if genero and genero != "todos" else None
            )
            
            # Convertir a modelos tipados
            pacientes_models = []
            for item in pacientes_data:
                try:
                    model = PacienteModel.from_dict(item)
                    pacientes_models.append(model)
                except Exception as e:
                    logger.warning(f"Error convirtiendo paciente: {e}")
                    continue
            
            print(f"✅ Pacientes obtenidos: {len(pacientes_models)} registros")
            return pacientes_models
            
        except PermissionError:
            logger.warning("Usuario sin permisos para acceder a pacientes")
            raise
        except Exception as e:
            self.handle_error("Error obteniendo pacientes filtrados", e)
            return []
    
    async def create_patient(self, patient_form: PacienteFormModel, user_id: str) -> Optional[PacienteModel]:
        """
        Crea un nuevo paciente con modelo tipado
        
        Args:
            patient_form: Formulario tipado de paciente
            user_id: ID del usuario que crea
            
        Returns:
            PacienteModel creado o None si hay error
        """
        try:
            logger.info("Creando nuevo paciente")
            
            # Verificar permisos
            self.require_permission("pacientes", "crear")
            
            # Validar formulario tipado
            validation_errors = patient_form.validate_form()
            if validation_errors:
                error_msg = f"Errores de validación: {validation_errors}"
                raise ValueError(error_msg)
            
            # Verificar que no exista el documento
            existing = self.table.get_by_documento(patient_form.numero_documento)
            if existing:
                raise ValueError("Ya existe un paciente con este número de documento")
            
            # Procesar campos de fecha
            fecha_nacimiento = None
            if patient_form.fecha_nacimiento:
                try:
                    fecha_nacimiento = datetime.strptime(patient_form.fecha_nacimiento, "%Y-%m-%d").date()
                except ValueError:
                    raise ValueError("Formato de fecha inválido. Use YYYY-MM-DD")
            
            # Procesar arrays (alergias, medicamentos, etc.)
            alergias = self.process_array_field(patient_form.alergias)
            medicamentos = self.process_array_field(patient_form.medicamentos_actuales)
            # Procesar información médica adicional
            condiciones = self.process_array_field(patient_form.observaciones_medicas)
            
            # Procesar información médica adicional
            condiciones_medicas = self.process_array_field(patient_form.condiciones_medicas) if hasattr(patient_form, 'condiciones_medicas') and patient_form.condiciones_medicas else None
            antecedentes_familiares = self.process_array_field(patient_form.antecedentes_familiares) if hasattr(patient_form, 'antecedentes_familiares') and patient_form.antecedentes_familiares else None
            
            # Crear paciente usando el método de la tabla
            result = self.table.create_patient_complete(
                # Nombres separados
                primer_nombre=patient_form.primer_nombre.strip(),
                primer_apellido=patient_form.primer_apellido.strip(),
                segundo_nombre=patient_form.segundo_nombre.strip() or None,
                segundo_apellido=patient_form.segundo_apellido.strip() or None,
                
                # Documentación
                numero_documento=patient_form.numero_documento,
                registrado_por=user_id,
                tipo_documento=patient_form.tipo_documento or "CI",
                fecha_nacimiento=fecha_nacimiento,
                genero=patient_form.genero if patient_form.genero else None,
                
                # Teléfonos separados
                celular_1=patient_form.celular_1 if patient_form.celular_1 else None,
                celular_2=patient_form.celular_2 if patient_form.celular_2 else None,
                
                # Contacto y ubicación
                email=patient_form.email.strip() if patient_form.email and patient_form.email.strip() else None,
                direccion=patient_form.direccion if patient_form.direccion else None,
                ciudad=patient_form.ciudad if patient_form.ciudad else None,
                departamento=patient_form.departamento if patient_form.departamento else None,
                ocupacion=patient_form.ocupacion if patient_form.ocupacion else None,
                estado_civil=patient_form.estado_civil if patient_form.estado_civil else None,
                
                # Información médica
                alergias=alergias if alergias else None,
                medicamentos_actuales=medicamentos if medicamentos else None,
                condiciones_medicas=condiciones_medicas,
                antecedentes_familiares=antecedentes_familiares,
                observaciones=patient_form.observaciones_medicas if patient_form.observaciones_medicas else None,
                
                # Contacto de emergencia como JSONB (esquema v4.1)
                contacto_emergencia={
                    "nombre": patient_form.contacto_emergencia_nombre if patient_form.contacto_emergencia_nombre else "",
                    "telefono": patient_form.contacto_emergencia_telefono if patient_form.contacto_emergencia_telefono else "",
                    "relacion": patient_form.contacto_emergencia_relacion if patient_form.contacto_emergencia_relacion else "",
                    "direccion": patient_form.contacto_emergencia_direccion if patient_form.contacto_emergencia_direccion else ""
                } if any([patient_form.contacto_emergencia_nombre, patient_form.contacto_emergencia_telefono]) else {}
            )
            
            if result:
                # Crear modelo tipado del resultado
                paciente_model = PacienteModel.from_dict(result)    
                return paciente_model
            else:
                raise ValueError("Error creando paciente en la base de datos")
                
        except PermissionError:
            logger.warning("Usuario sin permisos para crear pacientes")
            raise
        except ValueError as e:
            logger.warning(f"Error de validación: {e}")
            raise
        except Exception as e:
            self.handle_error("Error creando paciente", e)
            raise ValueError(f"Error inesperado: {str(e)}")
    
    async def update_patient(self, patient_id: str, patient_form: PacienteFormModel) -> Optional[PacienteModel]:
        """
        Actualiza un paciente existente con modelo tipado
        
        Args:
            patient_id: ID del paciente
            patient_form: Formulario tipado de paciente
            
        Returns:
            PacienteModel actualizado o None si hay error
        """
        try:
            logger.info(f"Actualizando paciente: {patient_id}")
            
            # Verificar permisos
            self.require_permission("pacientes", "actualizar")
            
            # Validar formulario tipado
            validation_errors = patient_form.validate_form()
            if validation_errors:
                error_msg = f"Errores de validación: {validation_errors}"
                raise ValueError(error_msg)
            
            # Verificar documento único (excluyendo el actual)
            existing = self.table.get_by_documento(patient_form.numero_documento)
            if existing and existing.get("id") != patient_id:
                raise ValueError("Ya existe otro paciente con este número de documento")
            
            # Procesar fecha
            fecha_nacimiento = None
            if patient_form.fecha_nacimiento:
                try:
                    fecha_nacimiento = datetime.strptime(patient_form.fecha_nacimiento, "%Y-%m-%d").date()
                except ValueError:
                    raise ValueError("Formato de fecha inválido. Use YYYY-MM-DD")
            
            # Procesar arrays
            alergias = self.process_array_field(patient_form.alergias)
            medicamentos = self.process_array_field(patient_form.medicamentos_actuales)
            
            # Preparar datos para actualización
            data = {
                # Nombres separados
                "primer_nombre": patient_form.primer_nombre.strip(),
                "primer_apellido": patient_form.primer_apellido.strip(),
                "segundo_nombre": patient_form.segundo_nombre.strip() or None,
                "segundo_apellido": patient_form.segundo_apellido.strip() or None,
                
                # Documentación
                "numero_documento": patient_form.numero_documento,
                "tipo_documento": patient_form.tipo_documento or "cedula",
                "genero": patient_form.genero if patient_form.genero else None,
                
                # Teléfonos separados
                "celular_1": patient_form.celular_1 if patient_form.celular_1 else None,
                "celular_2": patient_form.celular_2 if patient_form.celular_2 else None,
                
                # Contacto y ubicación
                "email": patient_form.email if patient_form.email else None,
                "direccion": patient_form.direccion if patient_form.direccion else None,
                "ciudad": patient_form.ciudad if patient_form.ciudad else None,
                "estado_civil": patient_form.estado_civil if patient_form.estado_civil else None,
                
                # Información médica
                "alergias": alergias if alergias else None,
                "medicamentos_actuales": medicamentos if medicamentos else None,
                # "enfermedades_cronicas": patient_form.enfermedades_cronicas if patient_form.enfermedades_cronicas else None,
                "observaciones": patient_form.observaciones_medicas if patient_form.observaciones_medicas else None,
                
                # Contacto de emergencia como JSONB (esquema v4.1)
                "contacto_emergencia": {
                    "nombre": patient_form.contacto_emergencia_nombre if patient_form.contacto_emergencia_nombre else "",
                    "telefono": patient_form.contacto_emergencia_telefono if patient_form.contacto_emergencia_telefono else "",
                    "relacion": patient_form.contacto_emergencia_relacion if patient_form.contacto_emergencia_relacion else "",
                    "direccion": patient_form.contacto_emergencia_direccion if patient_form.contacto_emergencia_direccion else ""
                } if any([patient_form.contacto_emergencia_nombre, patient_form.contacto_emergencia_telefono]) else {}
            }
            
            if fecha_nacimiento:
                data["fecha_nacimiento"] = fecha_nacimiento.isoformat()
            
            # Actualizar
            result = self.table.update(patient_id, data)
            
            if result:
                nombre_display = self.construct_full_name(
                    data["primer_nombre"],
                    data.get("segundo_nombre"),
                    data["primer_apellido"],
                    data.get("segundo_apellido")
                )
                
                # 🗑️ INVALIDAR CACHE después de actualizar paciente
                invalidate_after_patient_operation()
                
                logger.info(f"✅ Paciente actualizado: {nombre_display} (cache invalidado)")
                return result
            else:
                raise ValueError("Error actualizando paciente en la base de datos")
                
        except PermissionError:
            logger.warning("Usuario sin permisos para actualizar pacientes")
            raise
        except ValueError as e:
            logger.warning(f"Error de validación: {e}")
            raise
        except Exception as e:
            self.handle_error("Error actualizando paciente", e)
            raise ValueError(f"Error inesperado: {str(e)}")
    
    async def deactivate_patient(self, patient_id: str, motivo: str = None) -> bool:
        """
        Desactiva un paciente (soft delete)
        
        Args:
            patient_id: ID del paciente
            motivo: Motivo de desactivación
            
        Returns:
            True si se desactivó correctamente
        """
        try:
            logger.info(f"Desactivando paciente: {patient_id}")
            
            # Verificar permisos
            self.require_permission("pacientes", "eliminar")
            
            # TODO: Verificar que no tenga consultas activas
            
            # Desactivar usando el método de la tabla
            user_name = self.get_current_user_name()
            motivo_completo = motivo or f"Desactivado desde dashboard por {user_name}"
            
            result = self.table.deactivate_patient(patient_id, motivo_completo)
            
            if result:
                logger.info(f"✅ Paciente desactivado correctamente")
                return True
            else:
                raise ValueError("Error desactivando paciente")
                
        except PermissionError:
            logger.warning("Usuario sin permisos para desactivar pacientes")
            raise
        except Exception as e:
            self.handle_error("Error desactivando paciente", e)
            raise ValueError(f"Error inesperado: {str(e)}")
    
    async def reactivate_patient(self, patient_id: str) -> bool:
        """
        Reactiva un paciente
        
        Args:
            patient_id: ID del paciente
            
        Returns:
            True si se reactivó correctamente
        """
        try:
            logger.info(f"Reactivando paciente: {patient_id}")
            
            # Verificar permisos
            self.require_permission("pacientes", "crear")  # Reactivar = crear de nuevo
            
            result = self.table.reactivate_patient(patient_id)
            
            if result:
                logger.info(f"✅ Paciente reactivado correctamente")
                return True
            else:
                raise ValueError("Error reactivando paciente")
                
        except PermissionError:
            logger.warning("Usuario sin permisos para reactivar pacientes")
            raise
        except Exception as e:
            self.handle_error("Error reactivando paciente", e)
            raise ValueError(f"Error inesperado: {str(e)}")
    
    async def get_patient_by_id(self, patient_id: str) -> Optional[PacienteModel]:
        """
        Obtiene un paciente por ID
        
        Args:
            patient_id: ID del paciente
            
        Returns:
            Modelo del paciente o None
        """
        try:
            # Verificar permisos
            self.require_permission("pacientes", "leer")
            
            data = self.table.get_by_id(patient_id)
            if data:
                return PacienteModel.from_dict(data)
            return None
            
        except Exception as e:
            self.handle_error("Error obteniendo paciente por ID", e)
            return None

    def get_patient_by_id_sync(self, patient_id: str) -> Optional[PacienteModel]:
        """
        Obtiene un paciente por ID de forma síncrona
        Para casos donde no se puede usar async (como event handlers de Reflex)
        
        Args:
            patient_id: ID del paciente
            
        Returns:
            Modelo del paciente o None
        """
        try:
            # Verificar permisos 
            if not self.check_permission("pacientes", "leer"):
                logger.warning(f"Usuario sin permisos para leer pacientes")
                return None
            
            # Obtener datos directamente de la tabla
            data = self.table.get_by_id(patient_id)
            
            if data:
                return PacienteModel.from_dict(data)
            return None
            
        except Exception as e:
            self.handle_error("Error obteniendo paciente por ID (sync)", e)
            return None

    
    async def get_patient_stats(self) -> Dict[str, Any]:
        """
        Obtiene estadísticas de pacientes
        Usado por dashboard_service pero disponible independientemente
        """
        try:
            stats = self.table.get_patient_stats()
            logger.info(f"Estadísticas de pacientes obtenidas: {stats}")
            return stats
            
        except Exception as e:
            self.handle_error("Error obteniendo estadísticas de pacientes", e)
            return {
                "total": 0,
                "nuevos_mes": 0,
                "activos": 0,
                "hombres": 0,
                "mujeres": 0
            }

    # ==========================================
    # 🦷 MÉTODOS DE INICIALIZACIÓN DE ECOSISTEMA
    # ==========================================

    async def _inicializar_ecosistema_paciente_completo(self, numero_historia: str, paciente_id: str, user_id: str) -> bool:
        """
        🆕 Inicializar ecosistema completo del paciente nuevo

        Args:
            numero_historia: HC del paciente (ej: HC000001)
            paciente_id: UUID del paciente
            user_id: Usuario que crea el paciente

        Returns:
            True si se inicializó correctamente
        """
        try:
            logger.info(f"🦷 Inicializando ecosistema completo para paciente {numero_historia}")

            # # 1. Crear odontograma inicial con 32 dientes como "sanos"
            # odontograma_creado = await self._crear_odontograma_inicial_completo(numero_historia, paciente_id, user_id)

            # 2. Crear historial médico inicial
            historial_creado = await self._crear_historial_medico_inicial(paciente_id, user_id)

            # 3. Registrar auditoría de inicialización
            await self._registrar_auditoria_inicializacion(paciente_id, numero_historia, user_id)

            if odontograma_creado and historial_creado:
                logger.info(f"✅ Ecosistema completo inicializado para {numero_historia}")
                return True
            else:
                logger.warning(f"⚠️ Ecosistema parcialmente inicializado para {numero_historia}")
                return False

        except Exception as e:
            logger.error(f"❌ Error inicializando ecosistema para {numero_historia}: {e}")
            return False


    async def _crear_odontograma_inicial_completo(self, numero_historia: str, paciente_id: str, user_id: str) -> bool:
        """
        🦷 Crear odontograma inicial con 32 dientes como "sanos"

        Args:
            numero_historia: HC del paciente
            paciente_id: UUID del paciente
            user_id: Usuario que crea

        Returns:
            True si se creó correctamente
        """
        try:
            # Importar aquí para evitar circular imports
            from .personal_service import personal_service

            # Obtener personal_id usando la función existente
            personal_id = await personal_service.obtener_personal_id_por_usuario(user_id)

            if not personal_id:
                logger.error(f"❌ No se encontró personal asociado al usuario {user_id}")
                return False

        except Exception as e:
            logger.error(f"❌ Error creando odontograma inicial para {numero_historia}: {e}")
            return False

    async def _crear_historial_medico_inicial(self, paciente_id: str, user_id: str) -> bool:
        """
        📋 Crear entrada inicial en historial médico

        Args:
            paciente_id: UUID del paciente
            user_id: Usuario que crea

        Returns:
            True si se creó correctamente
        """
        try:
            from dental_system.supabase.client import get_client
            from .personal_service import personal_service

            supabase = get_client()

            # Obtener personal_id usando la función existente
            personal_id = await personal_service.obtener_personal_id_por_usuario(user_id)

            if not personal_id:
                logger.error(f"❌ No se encontró personal asociado al usuario {user_id}")
                return False

            # Crear entrada inicial en historial médico
            historial_inicial = {
                "paciente_id": paciente_id,
                "consulta_id": None,  # No hay consulta aún
                "intervencion_id": None,  # No hay intervención aún
                "odontologo_id": personal_id,
                "tipo_registro": "nota",
                "sintomas_principales": "Paciente nuevo registrado en el sistema",
                "examen_clinico": "Pendiente de evaluación inicial",
                "diagnostico_principal": "Sin diagnóstico - Paciente nuevo",
                "plan_tratamiento": "Evaluación inicial pendiente",
                "pronostico": "A determinar en primera consulta",
                "medicamentos_recetados": [],
                "recomendaciones": "Agendar consulta de evaluación inicial",
                "observaciones": "Historial médico inicial creado automáticamente",
                "confidencial": False,
                "fecha_registro": datetime.now().isoformat()
            }

            response = supabase.table("historial_medico").insert(historial_inicial).execute()

            if response.data:
                logger.info(f"✅ Historial médico inicial creado para paciente {paciente_id}")
                return True
            else:
                logger.error(f"❌ No se pudo crear historial médico inicial para paciente {paciente_id}")
                return False

        except Exception as e:
            logger.error(f"❌ Error creando historial médico inicial para paciente {paciente_id}: {e}")
            return False

    async def _registrar_auditoria_inicializacion(self, paciente_id: str, numero_historia: str, user_id: str) -> bool:
        """
        📝 Registrar auditoría de inicialización del ecosistema

        Args:
            paciente_id: UUID del paciente
            numero_historia: HC del paciente
            user_id: Usuario que crea

        Returns:
            True si se registró correctamente
        """
        try:
            from dental_system.supabase.client import get_client

            supabase = get_client()

            # Registrar en auditoría la inicialización completa
            auditoria_entry = {
                "tabla_afectada": "pacientes",
                "registro_id": paciente_id,
                "accion": "INSERT",
                "usuario_id": user_id,
                "datos_nuevos": {
                    "numero_historia": numero_historia,
                    "accion": "Inicialización completa de ecosistema",
                    "componentes": ["paciente", "odontograma", "historial_medico"]
                },
                "modulo": "pacientes",
                "ip_address": "127.0.0.1",  # Placeholder - en producción obtener IP real
                "motivo": f"Ecosistema completo inicializado para paciente {numero_historia}"
            }

            response = supabase.table("auditoria").insert(auditoria_entry).execute()

            if response.data:
                logger.info(f"✅ Auditoría de inicialización registrada para {numero_historia}")
                return True
            else:
                logger.warning(f"⚠️ No se pudo registrar auditoría para {numero_historia}")
                return False

        except Exception as e:
            logger.warning(f"⚠️ Error registrando auditoría para {numero_historia}: {e}")
            return False

    async def get_historial_completo_paciente(self, paciente_id: str) -> HistorialCompletoPaciente:
        """
        📋 Obtener historial completo del paciente con todas las consultas, intervenciones y servicios

        Similar a get_consultas_pendientes_facturacion() de pagos.py pero más completo

        Args:
            paciente_id: ID del paciente

        Returns:
            HistorialCompletoPaciente con todas las consultas y detalles
        """
        try:
            

            logger.info(f"📋 Obteniendo historial completo para paciente {paciente_id}")

            # Query completa con JOINs (similar a pagos.py línea 606)
            query = self.client.table("consultas").select("""
                id,
                numero_consulta,
                fecha_llegada,
                estado,
                motivo_consulta,
                primer_odontologo_id,
                personal!primer_odontologo_id(primer_nombre, primer_apellido),
                intervenciones(
                    id,
                    odontologo_id,
                    procedimiento_realizado,
                    total_usd,
                    total_bs,
                    personal!odontologo_id(primer_nombre, primer_apellido),
                    intervenciones_servicios(
                        cantidad,
                        precio_unitario_usd,
                        precio_unitario_bs,
                        servicios(nombre)
                    )
                ),
                pagos(
                    id,
                    estado_pago,
                    monto_pagado_usd,
                    monto_pagado_bs,
                    saldo_pendiente_usd,
                    saldo_pendiente_bs
                )
            """).eq("paciente_id", paciente_id).order("fecha_llegada", desc=True).execute()

            if not query.data:
                logger.info(f"No se encontraron consultas para paciente {paciente_id}")
                return HistorialCompletoPaciente()

            # Procesar consultas
            consultas_historial = []
            total_consultas = 0
            total_intervenciones = 0
            total_pagado_usd = 0.0
            total_pagado_bs = 0.0
            total_pendiente_usd = 0.0
            total_pendiente_bs = 0.0

            for consulta_data in query.data:
                total_consultas += 1
                # Procesar intervenciones
                intervenciones_list = []
                for interv_data in consulta_data.get("intervenciones", []):
                    total_intervenciones += 1

                    # Procesar servicios de la intervención
                    servicios_list = []
                    for serv_data in interv_data.get("intervenciones_servicios", []):
                        servicio = ServicioHistorial(
                            nombre=serv_data.get("servicios", {}).get("nombre", "Servicio"),
                            cantidad=serv_data.get("cantidad", 1),
                            precio_unitario_usd=float(serv_data.get("precio_unitario_usd", 0)),
                            precio_unitario_bs=float(serv_data.get("precio_unitario_bs", 0)),
                            subtotal_usd=float(serv_data.get("cantidad", 1)) * float(serv_data.get("precio_unitario_usd", 0)),
                            subtotal_bs=float(serv_data.get("cantidad", 1)) * float(serv_data.get("precio_unitario_bs", 0))
                        )
                        servicios_list.append(servicio)

                    # Obtener nombre del odontólogo
                    personal_data = interv_data.get("personal", {})
                    odontologo_nombre = f"{personal_data.get('primer_nombre', '')} {personal_data.get('primer_apellido', '')}".strip() or "Odontólogo"

                    intervencion = IntervencionHistorial(
                        id=interv_data.get("id", ""),
                        odontologo_id=interv_data.get("odontologo_id", ""),
                        odontologo_nombre=odontologo_nombre,
                        procedimiento_realizado=interv_data.get("procedimiento_realizado", ""),
                        total_usd=float(interv_data.get("total_usd", 0)),
                        total_bs=float(interv_data.get("total_bs", 0)),
                        servicios=servicios_list
                    )
                    intervenciones_list.append(intervencion)
                # Procesar pago
                pagos_data = consulta_data.get("pagos", [])
                pago_info = pagos_data[0] if pagos_data else {}

                pago_usd = float(pago_info.get("monto_pagado_usd", 0))
                pago_bs = float(pago_info.get("monto_pagado_bs", 0))
                saldo_usd = float(pago_info.get("saldo_pendiente_usd", 0))
                saldo_bs = float(pago_info.get("saldo_pendiente_bs", 0))

                total_pagado_usd += pago_usd
                total_pagado_bs += pago_bs
                total_pendiente_usd += saldo_usd
                total_pendiente_bs += saldo_bs

                # Determinar estado del pago
                if saldo_usd <= 0 and saldo_bs <= 0:
                    pago_estado = "completado"
                elif pago_usd > 0 or pago_bs > 0:
                    pago_estado = "parcial"
                else:
                    pago_estado = "pendiente"

                # Calcular totales de la consulta
                costo_total_usd = sum(i.total_usd for i in intervenciones_list)
                costo_total_bs = sum(i.total_bs for i in intervenciones_list)

                # Obtener nombre del odontólogo principal
                personal_principal = consulta_data.get("personal", {})
                odontologo_principal = f"{personal_principal.get('primer_nombre', '')} {personal_principal.get('primer_apellido', '')}".strip() or "No asignado"

                consulta = ConsultaHistorial(
                    id=consulta_data.get("id", ""),
                    numero_consulta=consulta_data.get("numero_consulta", ""),
                    fecha_llegada=consulta_data.get("fecha_llegada", ""),
                    estado=consulta_data.get("estado", ""),
                    motivo_consulta=consulta_data.get("motivo_consulta", ""),
                    primer_odontologo_id=consulta_data.get("primer_odontologo_id", ""),
                    primer_odontologo_nombre=odontologo_principal,
                    intervenciones=intervenciones_list,
                    costo_total_usd=costo_total_usd,
                    costo_total_bs=costo_total_bs,
                    pago_id=pago_info.get("id", ""),
                    pago_estado=pago_estado,
                    pago_usd=pago_usd,
                    pago_bs=pago_bs,
                    saldo_pendiente_usd=saldo_usd,
                    saldo_pendiente_bs=saldo_bs
                )
                consultas_historial.append(consulta)
            historial = HistorialCompletoPaciente(
                consultas=consultas_historial,
                total_consultas=total_consultas,
                total_intervenciones=total_intervenciones,
                total_pagado_usd=total_pagado_usd,
                total_pagado_bs=total_pagado_bs,
                total_pendiente_usd=total_pendiente_usd,
                total_pendiente_bs=total_pendiente_bs
            )
            print("="*80)
            print(historial.consultas[1])
            logger.info(f"✅ Historial completo obtenido: {total_consultas} consultas, {total_intervenciones} intervenciones")
            return historial

        except Exception as e:
            logger.error(f"❌ Error obteniendo historial completo: {str(e)}")
            self.handle_error("Error obteniendo historial del paciente", e)
            return HistorialCompletoPaciente()


# Instancia única para importar
pacientes_service = PacientesService()