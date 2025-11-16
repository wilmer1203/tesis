# 📋 DOCUMENTACIÓN DE ESTADOS - SISTEMA ODONTOLÓGICO
## Referencia Rápida para Claude Code

---

## 🎯 PROPÓSITO DE ESTE ARCHIVO

**Este archivo documenta todos los métodos y computed vars disponibles en cada substate**, para que Claude pueda:
- ✅ Entender rápidamente qué funcionalidad está disponible
- ✅ Saber cómo usar cada método sin leer todo el código
- ✅ Identificar el estado correcto para cada operación
- ✅ Mantener coherencia en el desarrollo

---

## 🏗️ ARQUITECTURA DE ESTADOS

El sistema usa **AppState como coordinador principal** con **substates especializados**:

```python
# AppState (dental_system/state/app_state.py)
class AppState(
    EstadoAuth,      # 🔐 Autenticación y permisos
    EstadoUI,        # 🎨 Interfaz y modales
    EstadoPacientes, # 👥 Gestión de pacientes
    EstadoPersonal,  # 👨‍⚕️ Gestión de empleados
    EstadoConsultas, # 📅 Sistema de consultas
    EstadoOdontologia, # 🦷 Módulo odontológico
    EstadoServicios, # 🏥 Catálogo de servicios
    EstadoPagos,     # 💳 Sistema de facturación
    rx.State
):
```

**Acceso:** `AppState.metodo()` o `self.metodo()` dentro de cualquier substate

---

## 🔐 ESTADO_AUTH.PY - Autenticación y Permisos

### **Variables Principales:**
```python
# Estado de autenticación
esta_autenticado: bool           # Si el usuario está logueado
id_usuario: str                  # ID en tabla usuarios
id_personal: str                 # ID en tabla personal (odontólogos)
email_usuario: str               # Email del usuario actual
rol_usuario: str                 # gerente, administrador, odontologo, asistente
perfil_usuario: Dict[str, Any]   # Datos completos del usuario
error_login: str                 # Mensaje de error de login
esta_cargando_auth: bool         # Loading state para login
```

### **Métodos Principales:**
```python
# 🔑 AUTENTICACIÓN
async def iniciar_sesion(datos_formulario: Dict[str, str])
# Uso: AppState.iniciar_sesion({"email": "...", "password": "..."})
# Función: Login completo + redirección automática según rol

async def cerrar_sesion()
# Uso: AppState.cerrar_sesion()
# Función: Logout completo + limpieza de datos + redirect a /login

def obtener_ruta_dashboard() -> str
# Uso: ruta = AppState.obtener_ruta_dashboard()
# Función: Devuelve ruta según rol (gerente→/boss, admin→/admin, etc.)
```

### **Computed Vars (Variables Calculadas):**
```python
@rx.var def nombre_usuario_display(self) -> str
# Uso: AppState.nombre_usuario_display
# Función: Nombre formateado para mostrar en UI

@rx.var def rol_usuario_display(self) -> str
# Uso: AppState.rol_usuario_display  
# Función: Rol formateado (gerente → "Gerente")

@rx.var def sesion_valida(self) -> bool
# Uso: AppState.sesion_valida
# Función: True si hay sesión válida completa
```

### **Métodos de Utilidad:**
```python
def obtener_contexto_usuario() -> Dict[str, Any]
# Uso: contexto = AppState.obtener_contexto_usuario()
# Función: Datos completos del usuario para servicios

def validar_permiso_para_operacion(modulo: str, operacion: str) -> bool
# Uso: puede = AppState.validar_permiso_para_operacion("pacientes", "crear")
# Función: Validación granular de permisos

def requiere_autenticacion() -> bool
def requiere_rol(roles_permitidos: Union[str, List[str]]) -> bool
def verificar_acceso_a_modulo(modulo: str) -> bool
# Uso: Validaciones de seguridad antes de operaciones
```

---

## 👨‍⚕️ ESTADO_PERSONAL.PY - Gestión de Personal

### **Variables Principales:**
```python
# Lista y selección  
lista_personal: List[PersonalModel] = []
total_empleados: int = 0
empleado_seleccionado: Optional[PersonalModel] = None

# Formulario tipado
formulario_empleado: PersonalFormModel = PersonalFormModel()
errores_validacion_empleado: Dict[str, str] = {}

# Filtros especializados
filtro_rol: str = "todos"
filtro_especialidad: str = "todas"
filtro_estado_empleado: str = "activos"

# Búsqueda
termino_busqueda_personal: str = ""
```

### **Métodos Principales:**
```python
# 👨‍⚕️ CRUD DE PERSONAL (solo Gerente)
async def cargar_lista_personal()
# Uso: await AppState.cargar_lista_personal()
# Función: Carga empleados (valida permisos automáticamente)

async def crear_empleado()
# Uso: await AppState.crear_empleado()
# Función: Crea empleado + usuario vinculado

async def actualizar_empleado()
# Uso: await AppState.actualizar_empleado()
# Función: Actualiza empleado seleccionado

async def guardar_personal_formulario()
# Uso: await AppState.guardar_personal_formulario()
# Función: Create/Update automático según si hay empleado_seleccionado

# 🔍 BÚSQUEDA Y FILTROS
async def buscar_personal(termino: str)
# Uso: await AppState.buscar_personal("Dr. García")
# Función: Búsqueda por nombre, documento, celular, especialidad

async def filtrar_por_rol(rol: str)
async def filtrar_por_especialidad(especialidad: str)
async def filtrar_por_estado(estado: str)
# Uso: await AppState.filtrar_por_rol("odontologo")
# Función: Filtros especializados para personal

# 📋 FORMULARIOS
def cargar_empleado_en_formulario(empleado: PersonalModel)
def limpiar_formulario_empleado()
def validar_formulario_empleado() -> bool
# Uso: Gestión del formulario de empleados

# 🎯 SELECCIÓN Y MODALES  
async def seleccionar_empleado(personal_id: str)
async def seleccionar_y_abrir_modal_personal(personal_id: str = "")
# Uso: Modal create/edit automático
```

### **Computed Vars:**
```python
@rx.var def personal_filtrado(self) -> List[PersonalModel]
@rx.var def personal_paginado(self) -> List[PersonalModel] 
@rx.var def odontologos_disponibles(self) -> List[PersonalModel]
@rx.var def personal_por_rol(self) -> Dict[str, int]
# Función: Datos procesados para UI
```

---

## 👥 ESTADO_PACIENTES.PY - Gestión de Pacientes

### **Variables Principales:**
```python
# Lista y selección
lista_pacientes: List[PacienteModel] = []
total_pacientes: int = 0
paciente_seleccionado: PacienteModel = PacienteModel()

# Formulario tipado
formulario_paciente: PacienteFormModel = PacienteFormModel()
errores_validacion_paciente: Dict[str, str] = {}

# Búsqueda y filtros
termino_busqueda_pacientes: str = ""
filtro_genero: str = "todos"
filtro_estado: str = "activos"

# Estados de carga
cargando_lista_pacientes: bool = False
cargando_operacion: bool = False
```

### **Métodos Principales:**
```python
# 📋 CRUD DE PACIENTES
async def cargar_lista_pacientes(forzar_refresco: bool = False)
async def crear_paciente(datos_formulario: Dict[str, Any])
async def guardar_paciente_formulario()
async def actualizar_paciente(id_paciente: str, datos_formulario: Dict[str, Any])
async def eliminar_paciente(id_paciente: str)

# 🔍 BÚSQUEDA Y FILTROS
async def buscar_pacientes(termino: str)
async def aplicar_filtros(filtros: Dict[str, Any])
def limpiar_filtros()

# 🎯 SELECCIÓN Y MODALES
async def seleccionar_paciente(id_paciente: str)
async def seleccionar_y_abrir_modal_paciente(id_paciente: str = "")
```

### **Computed Vars:**
```python
@rx.var def pacientes_filtrados_display(self) -> List[PacienteModel]
@rx.var def total_pacientes_activos(self) -> int
@rx.var def total_pacientes_inactivos(self) -> int
@rx.var def distribucion_por_genero(self) -> Dict[str, int]
@rx.var def tiene_filtros_activos(self) -> bool
```

---

## 📅 ESTADO_CONSULTAS.PY - Sistema de Consultas

### **Variables Principales:**
```python
# Listas principales
lista_consultas: List[ConsultaModel] = []
consultas_hoy: List[ConsultaModel] = []
total_consultas: int = 0

# Consulta seleccionada
consulta_seleccionada: Optional[ConsultaModel] = None

# Formulario de nueva consulta
formulario_consulta_data: ConsultaFormModel = ConsultaFormModel()
consulta_form_odontologo_id: str = ""
consulta_form_paciente_seleccionado: PacienteModel = PacienteModel()
consulta_form_tipo_consulta: str = "general"
consulta_form_prioridad: str = "normal"
consulta_form_motivo: str = ""

# Sistema de turnos
turnos_por_odontologo: Dict[str, List[TurnoModel]] = {}
consulta_en_curso: Optional[ConsultaModel] = None

# Filtros
filtro_fecha_consultas: str = date.today().isoformat()
filtro_estado_consultas: str = "todas"
filtro_odontologo_consultas: str = ""
termino_busqueda_consultas: str = ""
```

### **Métodos Principales:**
```python
# 📅 CRUD DE CONSULTAS
async def cargar_consultas(fecha: str = None, odontologo_id: str = None)
async def crear_consulta_completa()
async def actualizar_estado_consulta(consulta_id: str, nuevo_estado: str)

# 🔍 BÚSQUEDA Y FILTROS  
async def buscar_consultas(termino: str)
def aplicar_filtro_consultas(filtro: str, valor: str)
def limpiar_filtros_consultas()

# 🎯 GESTIÓN DE MODALES
async def abrir_modal_nueva_consulta()
def limpiar_formulario_consulta()
```

### **Computed Vars:**
```python
@rx.var def consultas_filtradas(self) -> List[ConsultaModel]
@rx.var def consultas_pendientes(self) -> List[ConsultaModel]
@rx.var def consultas_en_progreso(self) -> List[ConsultaModel]
@rx.var def consultas_completadas_hoy(self) -> List[ConsultaModel]
```

---

## 🎨 ESTADO_UI.PY - Gestión de Interfaz y Modales

### **Variables Principales:**
```python
# Navegación y páginas
current_page: str = "dashboard"
previous_page: str = ""
titulo_pagina: str = "Dashboard"
subtitulo_pagina: str = ""
ruta_navegacion: List[Dict[str, str]] = []

# Layout y responsive
sidebar_abierto: bool = True
sidebar_colapsado: bool = False
modo_mobile: bool = False
ancho_pantalla: str = "desktop"

# Modales del sistema
modal_crear_paciente_abierto: bool = False
modal_editar_paciente_abierto: bool = False
modal_crear_consulta_abierto: bool = False
modal_crear_personal_abierto: bool = False
modal_confirmacion_abierto: bool = False
modal_alerta_abierto: bool = False

# Formularios multi-paso
paso_formulario_paciente: int = 0
paso_formulario_personal: int = 0
paso_formulario_consulta: int = 0
total_pasos_paciente: int = 3
datos_temporales_paciente: Dict[str, Any] = {}

# Sistema de notificaciones
notificaciones_activas: List[Dict[str, Any]] = []
toast_visible: bool = False
toast_mensaje: str = ""
toast_tipo: str = "info"

# Loading states
cargando_global: bool = False
cargando_pacientes: bool = False
cargando_consultas: bool = False
```

### **Métodos Principales:**
```python
# 🧭 NAVEGACIÓN
@rx.event
def navigate_to(pagina: str, titulo: str = "", subtitulo: str = "")
# Uso: AppState.navigate_to("pacientes", "Gestión de Pacientes")
# Función: Navegación principal entre páginas con breadcrumbs

@rx.event
def retroceder_pagina()
# Uso: AppState.retroceder_pagina()
# Función: Volver a la página anterior

# 🪟 GESTIÓN DE MODALES
@rx.event 
def abrir_modal_paciente(tipo: str, datos: Dict[str, Any] = None)
@rx.event
def abrir_modal_consulta(tipo: str, datos: Dict[str, Any] = None)
@rx.event
def abrir_modal_personal(tipo: str, datos: Dict[str, Any] = None)
# Uso: AppState.abrir_modal_paciente("crear") / AppState.abrir_modal_paciente("editar", datos)
# Función: Abrir modales específicos con modo crear/editar/ver

@rx.event
def abrir_modal_confirmacion(titulo: str, mensaje: str, accion: str)
# Uso: AppState.abrir_modal_confirmacion("Eliminar", "¿Confirmar?", "eliminar_paciente")
# Función: Modal de confirmación para acciones críticas

@rx.event
def cerrar_todos_los_modales()
# Uso: AppState.cerrar_todos_los_modales()
# Función: Cerrar todos los modales + limpiar datos temporales

# 📋 FORMULARIOS MULTI-PASO
@rx.event
def avanzar_paso_paciente() / avanzar_paso_personal() / avanzar_paso_consulta()
@rx.event  
def retroceder_paso_paciente() / retroceder_paso_personal() / retroceder_paso_consulta()
@rx.event
def resetear_formulario_paciente() / resetear_formulario_personal() / resetear_formulario_consulta()
# Uso: Control de formularios con múltiples pasos

# 🔔 SISTEMA DE NOTIFICACIONES
@rx.event
def mostrar_toast(mensaje: str, tipo: str = "info", duracion: int = 3000)
# Uso: AppState.mostrar_toast("Guardado exitoso", "success")
# Función: Mostrar mensajes temporales

@rx.event
def agregar_notificacion(titulo: str, mensaje: str, tipo: str = "info")
# Uso: AppState.agregar_notificacion("Nueva consulta", "Paciente asignado")
# Función: Agregar notificación persistente

# ⏳ LOADING STATES
@rx.event
def iniciar_carga_global(mensaje: str = "Cargando...")
@rx.event
def finalizar_carga_global()
@rx.event
def set_cargando_modulo(modulo: str, cargando: bool)
# Uso: AppState.set_cargando_modulo("pacientes", True)
# Función: Controlar estados de carga por módulo
```

### **Computed Vars:**
```python
@rx.var def hay_modales_abiertos(self) -> bool
# Uso: AppState.hay_modales_abiertos
# Función: True si hay algún modal abierto

@rx.var def progreso_formulario_paciente(self) -> float
@rx.var def progreso_formulario_personal(self) -> float  
@rx.var def progreso_formulario_consulta(self) -> float
# Uso: AppState.progreso_formulario_paciente
# Función: Progreso del formulario (0-100)

@rx.var def hay_notificaciones_pendientes(self) -> bool
@rx.var def hay_carga_activa(self) -> bool
@rx.var def clase_css_sidebar(self) -> str
# Función: Estados reactivos para UI
```

---

## 🦷 ESTADO_ODONTOLOGIA.PY - Módulo Odontológico

### **Variables Principales:**
```python
# Pacientes y consultas asignadas
pacientes_asignados: List[PacienteModel] = []
consultas_asignadas: List[ConsultaModel] = []
total_pacientes_asignados: int = 0

# Paciente y consulta actual
consulta_actual: ConsultaModel = ConsultaModel()
paciente_actual: PacienteModel = PacienteModel()
intervencion_actual: IntervencionModel = IntervencionModel()

# Pacientes disponibles de otros odontólogos
pacientes_disponibles_otros: List[PacienteModel] = []
consultas_disponibles_otros: List[ConsultaModel] = []

# Estadísticas del odontólogo
estadisticas_dia: OdontologoStatsModel = OdontologoStatsModel()

# Servicios odontológicos
servicios_disponibles: List[ServicioModel] = []
servicio_seleccionado: ServicioModel = ServicioModel()

# Formulario de intervención
formulario_intervencion: IntervencionFormModel = IntervencionFormModel()
errores_validacion_intervencion: Dict[str, str] = {}

# Odontograma FDI (32 dientes)
dientes_fdi: List[DienteModel] = []
odontograma_actual: OdontogramaModel = OdontogramaModel()
diente_seleccionado: Optional[int] = None
superficie_seleccionada: str = "oclusal"
condiciones_odontograma: Dict[int, Dict[str, str]] = {}
cambios_pendientes_odontograma: Dict[int, Dict[str, str]] = {}
modo_odontograma: str = "visualizacion"

# Cuadrantes FDI
cuadrante_1: List[int] = [11, 12, 13, 14, 15, 16, 17, 18]  # Superior derecho
cuadrante_2: List[int] = [21, 22, 23, 24, 25, 26, 27, 28]  # Superior izquierdo
cuadrante_3: List[int] = [31, 32, 33, 34, 35, 36, 37, 38]  # Inferior izquierdo
cuadrante_4: List[int] = [41, 42, 43, 44, 45, 46, 47, 48]  # Inferior derecho

# Estados de navegación
en_formulario_intervencion: bool = False
modo_formulario: str = "crear"
```

### **Métodos Principales:**
```python
# 🔄 CARGA DE DATOS
async def cargar_pacientes_asignados()
# Uso: await AppState.cargar_pacientes_asignados()
# Función: Cargar consultas del día por orden de llegada

async def cargar_servicios_disponibles()
# Uso: await AppState.cargar_servicios_disponibles()
# Función: Cargar catálogo de servicios odontológicos

async def cargar_odontograma_paciente(paciente_id: str)
# Uso: await AppState.cargar_odontograma_paciente("pac_id")
# Función: Cargar odontograma del paciente actual

async def cargar_estadisticas_dia()
# Uso: await AppState.cargar_estadisticas_dia()
# Función: Cargar métricas del odontólogo para dashboard

# 🦷 GESTIÓN DE CONSULTAS E INTERVENCIONES
async def iniciar_consulta(consulta_id: str)
async def completar_consulta(consulta_id: str)
# Uso: await AppState.iniciar_consulta("consulta_id")
# Función: Cambiar estado consulta (programada → en_progreso → completada)

def navegar_a_intervencion(paciente: PacienteModel, consulta: ConsultaModel)
# Uso: AppState.navegar_a_intervencion(paciente, consulta)
# Función: Ir al formulario de intervención con paciente seleccionado

async def crear_intervencion()
# Uso: await AppState.crear_intervencion()
# Función: Crear nueva intervención odontológica

# 🔄 DERIVACIONES
async def tomar_paciente_disponible(paciente: PacienteModel, consulta_id: str)
# Uso: await AppState.tomar_paciente_disponible(paciente, "consulta_id")
# Función: Tomar paciente derivado de otro odontólogo

# 📝 GESTIÓN DEL FORMULARIO
def seleccionar_servicio(servicio_id: str)
def actualizar_campo_intervencion(campo: str, valor: Any)
def agregar_diente_afectado(numero_diente: int)
def quitar_diente_afectado(numero_diente: int)
def limpiar_formulario_intervencion()
def validar_formulario_intervencion() -> bool

# 🦷 ODONTOGRAMA
def seleccionar_diente(numero_diente: int)
async def seleccionar_diente_superficie(numero_diente: int, nombre_superficie: str)
def alternar_modo_odontograma()
def obtener_color_diente(numero_diente: int) -> str
async def establecer_condicion_diente(numero_diente: int, superficie: str, condicion: str)
```

### **Computed Vars:**
```python
@rx.var def pacientes_filtrados(self) -> List[PacienteModel]
@rx.var def consultas_por_estado(self) -> Dict[str, List[ConsultaModel]]
@rx.var def servicios_por_categoria_computed(self) -> Dict[str, List[ServicioModel]]
@rx.var def precio_servicio_seleccionado(self) -> str
@rx.var def turno_actual_paciente(self) -> str
@rx.var def estadisticas_del_dia_computed(self) -> OdontologoStatsModel
@rx.var def dientes_afectados_texto(self) -> str
@rx.var def puede_crear_intervencion(self) -> bool
@rx.var def formulario_intervencion_valido(self) -> bool
@rx.var def texto_estado_consulta_actual(self) -> str
@rx.var def resumen_dientes_seleccionados(self) -> str
```

---

## 🏥 ESTADO_SERVICIOS.PY - Catálogo de Servicios

### **Variables Principales:**
```python
# Lista principal de servicios
lista_servicios: List[ServicioModel] = []
total_servicios: int = 0
servicio_seleccionado: ServicioModel = ServicioModel()

# Formulario de servicio
formulario_servicio: Dict[str, Any] = {}
formulario_servicio_data: ServicioFormModel = ServicioFormModel()
errores_validacion_servicio: Dict[str, str] = {}

# Categorías disponibles
categorias_servicios: List[str] = [
    "Preventiva", "Restaurativa", "Endodoncia", "Periodoncia",
    "Cirugía Oral", "Ortodancia", "Prótesis", "Estética Dental",
    "Implantología", "Odontopediatría", "Urgencias", "General"
]

# Filtros especializados
filtro_categoria: str = "todas"
filtro_estado_servicio: str = "activos"
filtro_rango_precio_servicios: Dict[str, float] = {"min": 0.0, "max": 999999.0}
termino_busqueda_servicios: str = ""
mostrar_solo_activos_servicios: bool = True

# Ordenamiento y paginación
campo_ordenamiento_servicios: str = "nombre"
direccion_ordenamiento_servicios: str = "asc"
pagina_actual_servicios: int = 1
servicios_por_pagina: int = 18

# Estadísticas y cache
estadisticas_servicios: ServicioStatsModel = ServicioStatsModel()
cache_servicios_populares: List[ServicioModel] = []
cache_servicios_por_categoria: Dict[str, List[ServicioModel]] = {}
```

### **Métodos Principales:**
```python
# 📋 CRUD DE SERVICIOS (solo Gerente)
async def cargar_lista_servicios()
# Uso: await AppState.cargar_lista_servicios()
# Función: Cargar catálogo completo con filtros

async def crear_servicio()
# Uso: await AppState.crear_servicio()
# Función: Crear nuevo servicio (solo Gerente)

async def actualizar_servicio()
# Uso: await AppState.actualizar_servicio()
# Función: Actualizar servicio seleccionado

async def activar_desactivar_servicio(servicio_id: str, activar: bool)
# Uso: await AppState.activar_desactivar_servicio("serv_id", True)
# Función: Activar/desactivar servicio (soft delete)

# 🔍 BÚSQUEDA Y FILTROS
@rx.event
async def buscar_servicios(termino: str)
# Uso: await AppState.buscar_servicios("limpieza")
# Función: Búsqueda por nombre, descripción, código

async def filtrar_por_categoria(categoria: str)
async def filtrar_por_estado_servicio(estado: str)
async def ordenar_servicios(campo: str)
# Uso: await AppState.filtrar_por_categoria("Preventiva")
# Función: Filtros especializados para servicios

# 📝 GESTIÓN DE FORMULARIOS
def cargar_servicio_en_formulario(servicio: ServicioModel)
def limpiar_formulario_servicio()
def actualizar_campo_formulario_servicio(campo: str, valor: str)

# 📄 PAGINACIÓN
def siguiente_pagina_servicios()
def pagina_anterior_servicios()
def ir_a_pagina_servicios(numero_pagina: int)
def cambiar_servicios_por_pagina(cantidad: int)

# 🔧 UTILIDADES
async def refrescar_datos_servicios()
def limpiar_cache_servicios()
def obtener_servicio_por_id(servicio_id: str) -> Optional[ServicioModel]
def calcular_precio_con_descuento(servicio_id: str, descuento_pct: float) -> float
```

### **Computed Vars:**
```python
@rx.var def servicios_filtrados(self) -> List[ServicioModel]
@rx.var def servicios_paginados(self) -> List[ServicioModel]  
@rx.var def servicios_activos(self) -> List[ServicioModel]
@rx.var def servicios_por_categoria(self) -> Dict[str, List[ServicioModel]]
@rx.var def servicios_populares(self) -> List[ServicioModel]
@rx.var def info_paginacion_servicios(self) -> Dict[str, int]
@rx.var def estadisticas_por_categoria(self) -> Dict[str, EstadisticaCategoriaModel]
@rx.var def servicios_activos_count(self) -> int
@rx.var def precio_promedio_servicios(self) -> float
@rx.var def servicio_seleccionado_valido(self) -> bool
```

---

## 💳 ESTADO_PAGOS.PY - Sistema de Facturación

### **Variables Principales:**
```python
# Lista principal de pagos
lista_pagos: List[PagoModel] = []
total_pagos: int = 0
pago_seleccionado: PagoModel = PagoModel()

# Formularios de pagos
formulario_pago: Dict[str, Any] = {}
formulario_pago_data: PagoFormModel = PagoFormModel()
formulario_pago_parcial_data: PagoParcialFormModel = PagoParcialFormModel()
errores_validacion_pago: Dict[str, str] = {}

# Métodos de pago disponibles
metodos_pago_disponibles: List[str] = [
    "efectivo", "tarjeta_credito", "tarjeta_debito",
    "transferencia_bancaria", "cheque", "pago_movil", "otros"
]

# Estados de pago
estados_pago_disponibles: List[str] = [
    "pendiente", "completado", "anulado", "reembolsado"
]

# Filtros especializados
termino_busqueda_pagos: str = ""
buscar_por_paciente: str = ""
buscar_por_numero_recibo: str = ""
filtro_metodo_pago: str = "todos"
filtro_estado_pago: str = "todos"
filtro_rango_monto: Dict[str, float] = {"min": 0.0, "max": 999999.0}
mostrar_solo_pendientes: bool = False

# Cache financiero
cache_pagos_recientes: List[PagoModel] = []
cache_cuentas_por_cobrar: List[CuentaPorCobrarModel] = []
cache_validez_minutos: int = 10  # Cache más corto para datos financieros
```

### **Métodos Principales:**
```python
# 💳 CRUD DE PAGOS
@rx.event
async def cargar_lista_pagos(force_refresh: bool = False)
# Uso: await AppState.cargar_lista_pagos()
# Función: Cargar lista completa de pagos y facturas

@rx.event  
async def crear_pago(form_data: Dict[str, Any])
# Uso: await AppState.crear_pago(datos_pago)
# Función: Crear nuevo pago con validaciones

@rx.event
async def procesar_pago_parcial(pago_id: str, monto_pago: float)
# Uso: await AppState.procesar_pago_parcial("pago_id", 150.0)
# Función: Procesar abono parcial a deuda

@rx.event
async def anular_pago(pago_id: str, motivo: str)
# Uso: await AppState.anular_pago("pago_id", "Error en proceso")
# Función: Anular pago con justificación

# 🔍 BÚSQUEDA Y SELECCIÓN
@rx.event
async def buscar_pagos(query: str)
# Uso: await AppState.buscar_pagos("REC202412")
# Función: Búsqueda por número recibo, concepto, paciente

@rx.event
async def seleccionar_pago(pago_id: str)
# Uso: await AppState.seleccionar_pago("pago_id")
# Función: Seleccionar pago para operaciones

@rx.event
async def aplicar_filtros_pagos(filtros: Dict[str, Any])
# Uso: await AppState.aplicar_filtros_pagos({"metodo_pago": "efectivo"})
# Función: Aplicar filtros múltiples de pagos
```

### **Computed Vars:**
```python
@rx.var def pagos_filtrados_display(self) -> List[PagoModel]
@rx.var def pagos_pendientes(self) -> List[PagoModel]
@rx.var def pagos_completados_hoy(self) -> List[PagoModel]
@rx.var def pagos_con_saldo_pendiente(self) -> List[PagoModel]
@rx.var def total_pagos_pendientes(self) -> int
@rx.var def total_saldo_pendiente(self) -> float
@rx.var def recaudacion_del_dia(self) -> float
@rx.var def pago_seleccionado_valido(self) -> bool
@rx.var def proximo_numero_recibo(self) -> str
# Función: Auto-genera número de recibo (REC2024120001)
```

---

## 📝 VARIABLES/MÉTODOS COMENTADOS (NO USAR)

### **EstadoAuth:**
```python
# COMENTADO - No usar
# paso_formulario_paciente, errores_formulario_paciente
# avanzar_paso_formulario_paciente(), resetear_formulario_paciente()
# tiene_permiso_pacientes(), tiene_permiso_consultas(), tipo_dashboard()
```

### **EstadoPersonal:**
```python
# COMENTADO - No usar
# cache_personal_activo, cache_timestamp_personal
# ordenar_personal(), cambiar_empleados_por_pagina()
# empleados_activos_count(), especialidades_en_uso()
```

### **EstadoPacientes:**
```python
# COMENTADO - No usar
# filtro_edad_min, filtro_edad_max, filtro_ciudad
# cache_pacientes_activos, cache_timestamp_activos
# Métodos de cache: _cache_pacientes_valido(), _invalidar_cache_pacientes()
```

### **EstadoConsultas:**
```python
# COMENTADO - No usar
# consulta_form_legacy, tiempo_total_atencion_hoy
# Referencias a last_update (no funciona)
```

---

## 📖 CÓMO USAR ESTA DOCUMENTACIÓN

### **Para Claude:**
1. **SIEMPRE** leer este archivo antes de trabajar con estados
2. Usar los nombres exactos de métodos documentados
3. **NO USAR** variables/métodos marcados como COMENTADOS
4. Verificar permisos antes de operaciones sensibles
5. Seguir los patrones de uso mostrados

### **Para el Desarrollador:**
1. Mantener este archivo actualizado al agregar métodos
2. Marcar métodos comentados/deprecados
3. Incluir ejemplos de uso reales
4. Documentar computed vars nuevos

---

## 🎯 PATRONES COMUNES

### **Patrón de CRUD:**
```python
# 1. Cargar datos
await AppState.cargar_lista_[modulo]()

# 2. Seleccionar para editar  
await AppState.seleccionar_[modulo](id)

# 3. Abrir modal (crear/editar)
await AppState.seleccionar_y_abrir_modal_[modulo](id="")  # Crear
await AppState.seleccionar_y_abrir_modal_[modulo](id)     # Editar

# 4. Guardar
await AppState.guardar_[modulo]_formulario()
```

### **Patrón de Filtros:**
```python
# Aplicar filtro
await AppState.filtrar_por_[campo](valor)

# Buscar
await AppState.buscar_[modulo](termino)

# Limpiar
AppState.limpiar_filtros()
```

---

**Última actualización:** 2025-01-04  
**Estado:** Parcial - 4 de 8 substates documentados  
**Próximo:** Completar documentación de estados restantes