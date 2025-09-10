# CASOS DE USO DEL NEGOCIO
## Sistema de Información Odontológico - Clínica Dental OdontoMara

**Versión:** 1.0  
**Fecha:** Agosto 2025  
**Metodología:** RUP (Rational Unified Process)  
**Fase:** Concepción - Elaboración  

---

## 1. INTRODUCCIÓN

### 1.1 Propósito del Documento
Este documento describe los casos de uso del negocio del sistema odontológico, definiendo los procesos principales que realiza la clínica y cómo interactúan los diferentes actores del sistema.

### 1.2 Alcance
Los casos de uso cubren todos los procesos operativos de la clínica dental:
- Gestión de personal y usuarios
- Atención de pacientes por orden de llegada
- Realización de intervenciones odontológicas
- Gestión de pagos en múltiples monedas
- Mantenimiento de odontogramas digitales

---

## 2. ACTORES DEL SISTEMA

### 2.1 ACTORES PRINCIPALES

#### Actor: Gerente
**Descripción:** Personal administrativo con acceso completo al sistema  
**Responsabilidades:**
- Gestionar personal y usuarios del sistema
- Configurar servicios y precios
- Acceder a todos los reportes administrativos
- Gestionar pagos y facturación
- NO atiende pacientes directamente

**Casos de Uso Principales:**
- Gestionar Personal
- Configurar Sistema
- Generar Reportes Administrativos
- Gestionar Servicios Odontológicos

#### Actor: Administrador
**Descripción:** Personal encargado de tareas administrativas operativas  
**Responsabilidades:**
- Registrar y gestionar pacientes
- Crear consultas por orden de llegada
- Gestionar colas de odontólogos
- Procesar pagos

**Casos de Uso Principales:**
- Registrar Paciente
- Crear Consulta por Llegada
- Gestionar Cola de Atención
- Procesar Pago

#### Actor: Odontólogo
**Descripción:** Profesional de la salud dental que atiende pacientes  
**Responsabilidades:**
- Atender pacientes según cola asignada
- Realizar intervenciones odontológicas
- Gestionar odontogramas
- Registrar historial médico

**Casos de Uso Principales:**
- Atender Paciente
- Realizar Intervención
- Actualizar Odontograma
- Registrar Historial Médico

#### Actor: Asistente
**Descripción:** Personal de apoyo con acceso limitado  
**Responsabilidades:**
- Consultar información de pacientes
- Consultar cola de atención
- Apoyo en consultas

**Casos de Uso Principales:**
- Consultar Información Paciente
- Consultar Cola de Atención

### 2.2 ACTORES SECUNDARIOS

#### Actor: Sistema de Auditoría
**Descripción:** Sistema automatizado que registra todas las acciones  
**Responsabilidades:**
- Registrar automáticamente todas las operaciones
- Mantener trazabilidad de cambios
- Generar logs de seguridad

#### Actor: Sistema de Supabase
**Descripción:** Plataforma externa que proporciona servicios de backend  
**Responsabilidades:**
- Autenticación de usuarios
- Almacenamiento de datos
- Respaldos automáticos

---

## 3. CASOS DE USO PRINCIPALES

### 3.1 MÓDULO DE GESTIÓN DE PERSONAL

#### CU-001: Gestionar Personal
**Actor Principal:** Gerente  
**Precondiciones:** Usuario autenticado como Gerente  
**Objetivo:** Registrar, actualizar o inactivar personal de la clínica  

**Flujo Principal:**
1. Gerente accede al módulo de gestión de personal
2. Sistema muestra lista de personal existente
3. Gerente selecciona opción (crear nuevo, editar, inactivar)
4. **Si es crear nuevo:**
   4.1. Sistema muestra formulario de registro
   4.2. Gerente ingresa datos personales y profesionales
   4.3. Sistema valida información
   4.4. Sistema crea usuario asociado
   4.5. Sistema envía credenciales de acceso
5. **Si es editar:**
   5.1. Sistema muestra formulario con datos actuales
   5.2. Gerente modifica información necesaria
   5.3. Sistema valida cambios
   5.4. Sistema actualiza información
6. **Si es inactivar:**
   6.1. Sistema solicita confirmación
   6.2. Gerente confirma acción
   6.3. Sistema cambia estado a inactivo
7. Sistema confirma operación realizada
8. Sistema registra auditoría de la acción

**Flujos Alternativos:**
- **A1:** Datos inválidos - Sistema muestra errores específicos
- **A2:** Personal con consultas activas - Sistema no permite inactivar
- **A3:** Email duplicado - Sistema rechaza creación

**Postcondiciones:**
- Personal registrado/actualizado en el sistema
- Usuario creado con rol correspondiente
- Auditoría registrada

#### CU-002: Autenticar Usuario
**Actor Principal:** Cualquier usuario del sistema  
**Precondiciones:** Usuario registrado en el sistema  
**Objetivo:** Verificar identidad y otorgar acceso al sistema  

**Flujo Principal:**
1. Usuario accede a la página de login
2. Sistema muestra formulario de autenticación
3. Usuario ingresa email y contraseña
4. Sistema valida credenciales con Supabase Auth
5. **Si credenciales son válidas:**
   5.1. Sistema obtiene información del usuario
   5.2. Sistema verifica estado activo
   5.3. Sistema carga permisos según rol
   5.4. Sistema redirige a dashboard principal
   5.5. Sistema registra último acceso
6. Sistema muestra interfaz según rol del usuario

**Flujos Alternativos:**
- **A1:** Credenciales inválidas - Sistema muestra error
- **A2:** Usuario inactivo - Sistema deniega acceso
- **A3:** Error de comunicación - Sistema muestra mensaje técnico

**Postcondiciones:**
- Usuario autenticado en el sistema
- Permisos cargados según rol
- Último acceso actualizado

### 3.2 MÓDULO DE GESTIÓN DE PACIENTES

#### CU-003: Registrar Paciente
**Actor Principal:** Administrador  
**Precondiciones:** Usuario autenticado como Administrador  
**Objetivo:** Registrar nuevo paciente en el sistema  

**Flujo Principal:**
1. Administrador accede al módulo de pacientes
2. Sistema muestra opción de crear nuevo paciente
3. Administrador selecciona "Nuevo Paciente"
4. Sistema muestra formulario de registro
5. Administrador ingresa información obligatoria:
   - Primer nombre y primer apellido
   - Tipo y número de documento
   - Fecha de nacimiento (opcional)
6. Administrador ingresa información opcional:
   - Segundo nombre y segundo apellido
   - Celulares de contacto
   - Email, dirección, ocupación
   - Información médica básica
7. Sistema valida datos ingresados
8. Sistema genera número de historia automáticamente
9. Sistema calcula edad si hay fecha de nacimiento
10. Sistema guarda información del paciente
11. Sistema muestra confirmación con número de historia
12. Sistema registra auditoría de creación

**Flujos Alternativos:**
- **A1:** Documento duplicado - Sistema muestra error específico
- **A2:** Datos obligatorios faltantes - Sistema resalta campos
- **A3:** Formato de documento inválido - Sistema muestra formato requerido

**Postcondiciones:**
- Paciente registrado con número de historia único
- Edad calculada automáticamente
- Auditoría de creación registrada

#### CU-004: Buscar Paciente
**Actor Principal:** Administrador, Odontólogo  
**Precondiciones:** Usuario autenticado con permisos de lectura de pacientes  
**Objetivo:** Encontrar paciente existente en el sistema  

**Flujo Principal:**
1. Usuario accede a la función de búsqueda
2. Sistema muestra opciones de búsqueda:
   - Por número de historia
   - Por número de documento
   - Por nombres y apellidos
   - Por celular
3. Usuario selecciona criterio e ingresa información
4. Sistema ejecuta búsqueda
5. Sistema muestra resultados ordenados por relevancia
6. Usuario selecciona paciente de la lista
7. Sistema muestra información detallada del paciente

**Flujos Alternativos:**
- **A1:** Sin resultados - Sistema muestra opción de crear nuevo
- **A2:** Múltiples resultados - Sistema permite refinar búsqueda
- **A3:** Búsqueda muy amplia - Sistema limita resultados

**Postcondiciones:**
- Paciente encontrado y mostrado
- Acceso registrado en auditoría

### 3.3 MÓDULO DE GESTIÓN DE CONSULTAS

#### CU-005: Crear Consulta por Llegada
**Actor Principal:** Administrador  
**Precondiciones:** 
- Usuario autenticado como Administrador
- Paciente registrado en el sistema
- Al menos un odontólogo activo disponible

**Objetivo:** Registrar llegada de paciente y asignarlo a cola de odontólogo  

**Flujo Principal:**
1. Administrador accede al módulo de consultas
2. Sistema muestra opción "Nueva Consulta"
3. Administrador selecciona o busca paciente
4. Sistema muestra información del paciente
5. Administrador ingresa motivo de consulta
6. Administrador selecciona odontólogo preferido o permite asignación automática
7. Sistema verifica disponibilidad del odontólogo
8. Sistema genera número de consulta automáticamente
9. Sistema asigna orden de llegada general del día
10. Sistema asigna posición en cola específica del odontólogo
11. Sistema registra fecha y hora de llegada
12. Sistema cambia estado a "en_espera"
13. Sistema muestra confirmación con:
    - Número de consulta
    - Posición en cola del odontólogo
    - Tiempo estimado de espera
14. Sistema actualiza estadísticas de cola en tiempo real

**Flujos Alternativos:**
- **A1:** Odontólogo no disponible - Sistema sugiere alternativas
- **A2:** Paciente con consulta activa - Sistema muestra advertencia
- **A3:** Cola muy larga - Sistema sugiere otro odontólogo

**Postcondiciones:**
- Consulta creada con número único
- Paciente en cola específica del odontólogo
- Estadísticas de cola actualizadas
- Auditoría registrada

#### CU-006: Gestionar Cola de Atención
**Actor Principal:** Administrador  
**Precondiciones:** 
- Usuario autenticado como Administrador
- Existen consultas en estado "en_espera"

**Objetivo:** Monitorear y gestionar las colas de atención por odontólogo  

**Flujo Principal:**
1. Administrador accede al dashboard de colas
2. Sistema muestra estado actual de todas las colas:
   - Lista de odontólogos activos
   - Pacientes esperando por cada odontólogo
   - Pacientes actualmente en atención
   - Tiempos de espera estimados
3. Administrador puede realizar acciones:
   - Ver próximo paciente en cada cola
   - Cambiar paciente de cola
   - Ver estadísticas detalladas
4. **Si cambia paciente de cola:**
   4.1. Administrador selecciona paciente
   4.2. Administrador selecciona nuevo odontólogo
   4.3. Administrador ingresa motivo del cambio
   4.4. Sistema reasigna posición en nueva cola
   4.5. Sistema actualiza estadísticas
5. Sistema actualiza información en tiempo real

**Flujos Alternativos:**
- **A1:** Cola vacía - Sistema muestra mensaje informativo
- **A2:** Odontólogo no disponible - Sistema actualiza estado
- **A3:** Error de reasignación - Sistema revierte cambios

**Postcondiciones:**
- Colas actualizadas según cambios realizados
- Estadísticas en tiempo real mantenidas
- Auditoría de cambios registrada

#### CU-007: Cambiar Odontólogo de Consulta
**Actor Principal:** Administrador  
**Precondiciones:** 
- Consulta en estado "en_espera" o "entre_odontologos"
- Odontólogo destino disponible

**Objetivo:** Reasignar paciente a cola de otro odontólogo  

**Flujo Principal:**
1. Administrador selecciona consulta a reasignar
2. Sistema muestra información actual de la consulta
3. Administrador selecciona nuevo odontólogo
4. Sistema muestra estado de la cola del nuevo odontólogo
5. Administrador ingresa motivo del cambio (obligatorio)
6. Sistema calcula nueva posición en cola
7. Administrador confirma el cambio
8. Sistema actualiza consulta:
   - Cambia odontólogo asignado
   - Asigna nueva posición en cola
   - Registra motivo en observaciones
9. Sistema actualiza estadísticas de ambas colas
10. Sistema confirma cambio realizado

**Flujos Alternativos:**
- **A1:** Motivo no especificado - Sistema solicita motivo obligatorio
- **A2:** Odontólogo no disponible - Sistema muestra error
- **A3:** Consulta ya en atención - Sistema impide cambio

**Postcondiciones:**
- Consulta reasignada a nuevo odontólogo
- Posición en nueva cola asignada
- Historial de cambios actualizado

### 3.4 MÓDULO DE INTERVENCIONES ODONTOLÓGICAS

#### CU-008: Atender Paciente
**Actor Principal:** Odontólogo  
**Precondiciones:** 
- Usuario autenticado como Odontólogo
- Existe paciente en cola asignada

**Objetivo:** Iniciar atención del siguiente paciente en cola  

**Flujo Principal:**
1. Odontólogo accede a su cola de pacientes
2. Sistema muestra próximo paciente en orden
3. Sistema muestra información del paciente:
   - Datos personales básicos
   - Motivo de consulta
   - Historial médico relevante
   - Última versión de odontograma
4. Odontólogo selecciona "Iniciar Atención"
5. Sistema cambia estado de consulta a "en_atencion"
6. Sistema registra hora de inicio de atención
7. Sistema actualiza estadísticas de cola
8. Sistema muestra panel de atención con opciones:
   - Realizar intervención
   - Consultar historial completo
   - Ver/actualizar odontograma
   - Derivar a otro odontólogo

**Flujos Alternativos:**
- **A1:** Cola vacía - Sistema muestra mensaje y estadísticas
- **A2:** Paciente no se presenta - Sistema permite marcar como "no asistió"
- **A3:** Emergencia - Sistema permite atender fuera de orden

**Postcondiciones:**
- Consulta en estado "en_atencion"
- Hora de inicio registrada
- Cola actualizada

#### CU-009: Realizar Intervención
**Actor Principal:** Odontólogo  
**Precondiciones:** 
- Consulta en estado "en_atencion"
- Odontólogo atendiendo al paciente

**Objetivo:** Registrar procedimientos odontológicos realizados  

**Flujo Principal:**
1. Odontólogo inicia nueva intervención
2. Sistema registra hora de inicio automáticamente
3. Odontólogo ingresa información clínica:
   - Diagnóstico inicial
   - Dientes afectados (selección visual/FDI)
   - Procedimiento realizado
4. Odontólogo selecciona servicios a realizar:
   4.1. Busca servicios en catálogo
   4.2. Selecciona múltiples servicios si aplica
   4.3. Especifica cantidad de cada servicio
   4.4. Asigna dientes específicos por servicio
5. Sistema calcula precios automáticamente:
   - Precios unitarios en BS y USD
   - Totales por servicio
   - Total general de la intervención
6. Odontólogo ingresa información adicional:
   - Materiales utilizados
   - Anestesia aplicada
   - Complicaciones (si las hay)
   - Instrucciones al paciente
7. Odontólogo registra cambios en odontograma (si aplica)
8. Odontólogo finaliza intervención
9. Sistema registra hora de fin y calcula duración
10. Sistema actualiza totales de la consulta
11. Sistema registra auditoría completa

**Flujos Alternativos:**
- **A1:** Sin servicios seleccionados - Sistema solicita al menos uno
- **A2:** Cambios en odontograma - Sistema crea nueva versión
- **A3:** Intervención suspendida - Sistema permite guardar parcialmente

**Postcondiciones:**
- Intervención registrada completamente
- Totales calculados automáticamente
- Odontograma actualizado si aplica
- Auditoría completa registrada

#### CU-010: Derivar a Otro Odontólogo
**Actor Principal:** Odontólogo  
**Precondiciones:** 
- Consulta actualmente en atención
- Existe otro odontólogo disponible

**Objetivo:** Transferir paciente a otro odontólogo para atención especializada  

**Flujo Principal:**
1. Odontólogo actual selecciona "Derivar Paciente"
2. Sistema muestra lista de odontólogos disponibles
3. Odontólogo selecciona especialista destino
4. Odontólogo ingresa motivo de derivación (obligatorio)
5. Odontólogo ingresa notas para el especialista
6. Sistema calcula posición en cola del especialista
7. Odontólogo confirma derivación
8. Sistema actualiza estado de consulta a "entre_odontologos"
9. Sistema asigna paciente a nueva cola
10. Sistema registra derivación en historial
11. Sistema notifica al odontólogo destino
12. Sistema actualiza estadísticas de ambas colas

**Flujos Alternativos:**
- **A1:** Especialista no disponible - Sistema sugiere alternativas
- **A2:** Motivo no especificado - Sistema requiere motivo obligatorio
- **A3:** Cola destino llena - Sistema advierte tiempo de espera

**Postcondiciones:**
- Paciente derivado exitosamente
- Historial de derivación registrado
- Colas actualizadas

### 3.5 MÓDULO DE ODONTOGRAMA DIGITAL

#### CU-011: Actualizar Odontograma
**Actor Principal:** Odontólogo  
**Precondiciones:** 
- Usuario autenticado como Odontólogo
- Paciente en atención
- Existe odontograma previo o se crea uno nuevo

**Objetivo:** Registrar condiciones dentales actuales del paciente  

**Flujo Principal:**
1. Odontólogo accede al odontograma del paciente
2. Sistema muestra versión actual del odontograma
3. Sistema muestra interfaz interactiva con:
   - Representación visual de todos los dientes
   - Numeración FDI estándar
   - Paleta de condiciones disponibles
   - Herramientas de selección por cara dental
4. Odontólogo selecciona diente a modificar
5. Sistema muestra opciones de condición:
   - Sano, caries, obturación, corona, etc.
   - Severidad (leve, moderada, severa)
   - Caras afectadas específicas
6. Odontólogo especifica detalles:
   - Tipo de condición
   - Caras afectadas
   - Material utilizado (si aplica)
   - Observaciones específicas
7. Sistema aplica cambios visualmente
8. Odontólogo repite proceso para otros dientes
9. Odontólogo agrega notas generales del odontograma
10. Sistema verifica si hay cambios significativos
11. **Si hay cambios:**
    11.1. Sistema crea nueva versión automáticamente
    11.2. Sistema vincula cambios con intervención actual
    11.3. Sistema calcula estadísticas actualizadas
12. Odontólogo guarda odontograma
13. Sistema confirma actualización exitosa

**Flujos Alternativos:**
- **A1:** Sin cambios - Sistema mantiene versión actual
- **A2:** Error en numeración FDI - Sistema valida selección
- **A3:** Odontograma corrupto - Sistema crea nuevo desde cero

**Postcondiciones:**
- Odontograma actualizado con nueva versión
- Cambios vinculados a intervención específica
- Auditoría de modificaciones registrada

#### CU-012: Consultar Historial de Odontograma
**Actor Principal:** Odontólogo  
**Precondiciones:** 
- Paciente con historial de odontogramas
- Usuario con permisos de lectura

**Objetivo:** Revisar evolución del estado dental del paciente  

**Flujo Principal:**
1. Odontólogo accede al historial del paciente
2. Sistema muestra lista de versiones de odontograma ordenadas por fecha
3. Odontólogo selecciona versiones a comparar
4. Sistema muestra comparación visual:
   - Versión anterior y actual lado a lado
   - Cambios resaltados con colores
   - Fechas y odontólogos responsables
5. Sistema muestra estadísticas de evolución:
   - Nuevas condiciones agregadas
   - Condiciones resueltas
   - Tendencias de salud dental
6. Odontólogo puede exportar comparación para reportes

**Flujos Alternativos:**
- **A1:** Solo una versión disponible - Sistema muestra mensaje informativo
- **A2:** Versiones corruptas - Sistema omite versiones dañadas

**Postcondiciones:**
- Historial consultado exitosamente
- Comparación visual generada

#### CU-012.1: Usar Odontograma Nativo Interactivo
**Actor Principal:** Odontólogo  
**Precondiciones:** 
- Usuario autenticado como Odontólogo
- Paciente en atención
- Página de intervención abierta

**Objetivo:** Seleccionar dientes usando odontograma nativo sin JavaScript  

**Flujo Principal:** ✅ IMPLEMENTADO
1. Odontólogo accede al tab "Odontograma" en panel central
2. Sistema muestra odontograma nativo con 32 dientes FDI
3. Sistema organiza dientes en 4 cuadrantes:
   - Superior Derecho: 18-11 (Cuadrante 1)
   - Superior Izquierdo: 21-28 (Cuadrante 2)
   - Inferior Izquierdo: 31-38 (Cuadrante 3)
   - Inferior Derecho: 48-41 (Cuadrante 4)
4. Odontólogo hace clic en dientes específicos
5. Sistema cambia color visual del diente seleccionado
6. Sistema actualiza contador de dientes seleccionados
7. Sistema muestra panel lateral con leyenda de condiciones
8. Sistema actualiza resumen de dientes seleccionados en tiempo real
9. Odontólogo puede usar botón "Limpiar" para resetear selección

**Flujos Alternativos:**
- **A1:** Odontólogo deselecciona diente - Sistema remueve de selección
- **A2:** Selección múltiple - Sistema acumula dientes seleccionados
- **A3:** Responsive en tablet - Sistema ajusta tamaño botones

**Postcondiciones:**
- Dientes seleccionados guardados en AppState
- Interfaz visual actualizada
- Contador actualizado en toolbar

#### CU-012.2: Usar Panel de Detalles de Diente
**Actor Principal:** Odontólogo  
**Precondiciones:** 
- Usuario autenticado como Odontólogo
- Diente específico seleccionado en odontograma
- Panel derecho de detalles activo

**Objetivo:** Revisar y gestionar información específica de un diente  

**Flujo Principal:** ✅ IMPLEMENTADO
1. Odontólogo selecciona diente específico en odontograma
2. Sistema muestra panel de detalles con 4 tabs especializados:
   - **Tab Estado:** Condición actual y cambios recientes
   - **Tab Historial:** Timeline completo de modificaciones
   - **Tab Procedimientos:** Servicios realizados en el diente
   - **Tab Notas:** Observaciones clínicas específicas
3. Odontólogo navega entre tabs según necesidad
4. Sistema muestra información contextual por tab
5. **En Tab Estado:**
   - Muestra condición actual visual
   - Lista cambios recientes con fechas
   - Indica estado de riesgo si aplica
6. **En Tab Historial:**
   - Timeline visual con intervenciones pasadas
   - Odontólogos responsables de cada cambio
   - Comparación de estados antes/después
7. **En Tab Procedimientos:**
   - Lista servicios realizados en el diente
   - Fechas y odontólogos responsables
   - Costos asociados por procedimiento
8. **En Tab Notas:**
   - Campo de texto para observaciones
   - Historial de notas anteriores
   - Marcadores de importancia

**Flujos Alternativos:**
- **A1:** Sin historial - Sistema muestra mensaje informativo
- **A2:** Toggle panel derecho - Sistema puede cambiar a historial general

**Postcondiciones:**
- Información específica de diente consultada
- Contexto clínico completo disponible

#### CU-012.3: Sistema de Versionado Automático
**Actor Principal:** Sistema (automático), Odontólogo (consulta)  
**Precondiciones:** 
- Cambios significativos detectados en odontograma
- Intervención activa en progreso

**Objetivo:** Crear automáticamente nueva versión del odontograma  

**Flujo Principal:** ✅ IMPLEMENTADO
1. Sistema detecta cambios significativos en odontograma
2. Sistema evalúa criterios de nueva versión:
   - Cambio de condición de sano a patológico
   - Nuevas restauraciones o tratamientos
   - Extracciones o implantes
3. **Si aplica nueva versión:**
   3.1. Sistema crea nueva versión automáticamente
   3.2. Sistema vincula versión con intervención actual
   3.3. Sistema asigna odontólogo responsable
   3.4. Sistema establece versión anterior como referencia
4. Odontólogo puede consultar sistema de versionado en tab "Versiones"
5. Sistema muestra timeline de versiones:
   - Lista cronológica de todas las versiones
   - Fechas de creación
   - Odontólogos responsables
   - Motivos de nueva versión
6. Odontólogo puede comparar versiones lado a lado
7. Sistema genera estadísticas de evolución dental

**Flujos Alternativos:**
- **A1:** Cambios menores - Sistema no crea nueva versión
- **A2:** Versión corrupta - Sistema crea nueva desde cero

**Postcondiciones:**
- Nueva versión creada automáticamente
- Trazabilidad histórica mantenida
- Vinculación con intervención establecida

#### CU-012.4: Sistema de Notificaciones en Tiempo Real
**Actor Principal:** Sistema (automático)  
**Precondiciones:** 
- Cambios críticos detectados en intervención
- Sistema de notificaciones activo

**Objetivo:** Notificar automáticamente cambios críticos durante intervenciones  

**Flujo Principal:** ✅ IMPLEMENTADO
1. Sistema monitorea cambios en tiempo real durante intervención
2. Sistema evalúa severidad de cambios:
   - **Info:** Cambios rutinarios (restauraciones simples)
   - **Advertencia:** Cambios moderados (endodoncias)
   - **Crítico:** Cambios severos (extracciones, implantes)
3. Sistema genera notificación automática según criterios
4. Sistema muestra badge con conteo en header de intervención
5. Odontólogo puede hacer clic en ícono de notificaciones
6. Sistema despliega panel con historial de notificaciones:
   - Clasificación por color según severidad
   - Timestamps de cada notificación
   - Descripción del cambio detectado
   - Acción sugerida si aplica
7. Sistema permite configurar tipos de notificaciones
8. Sistema mantiene historial de notificaciones por sesión

**Flujos Alternativos:**
- **A1:** Notificaciones deshabilitadas - Sistema no genera alertas
- **A2:** Configuración personalizada - Sistema respeta preferencias

**Postcondiciones:**
- Notificaciones críticas alertadas en tiempo real
- Historial de cambios mantenido
- Configuración personalizable aplicada

### 3.6 MÓDULO DE GESTIÓN DE PAGOS

#### CU-013: Procesar Pago Simple
**Actor Principal:** Administrador  
**Precondiciones:** 
- Consulta completada con intervenciones
- Totales calculados automáticamente

**Objetivo:** Registrar pago de consulta en una sola moneda  

**Flujo Principal:**
1. Administrador accede al módulo de pagos
2. Administrador busca y selecciona consulta a pagar
3. Sistema muestra detalle de la consulta:
   - Servicios realizados por intervención
   - Totales en BS y USD
   - Saldos pendientes
4. Administrador selecciona moneda de pago (BS o USD)
5. Administrador ingresa monto a pagar
6. Sistema valida que no exceda el saldo pendiente
7. Administrador selecciona método de pago:
   - Efectivo, tarjeta crédito, tarjeta débito, transferencia
8. Administrador ingresa referencia de pago (si aplica)
9. Sistema calcula nuevo saldo pendiente
10. Administrador confirma transacción
11. Sistema genera número de recibo automáticamente
12. Sistema registra tasa de cambio actual
13. Sistema actualiza estado de pago
14. Sistema distribuye ingresos por odontólogo automáticamente
15. Sistema genera recibo para impresión

**Flujos Alternativos:**
- **A1:** Monto excede saldo - Sistema ajusta automáticamente
- **A2:** Descuento aplicado - Administrador especifica motivo
- **A3:** Error en método de pago - Sistema permite corrección

**Postcondiciones:**
- Pago registrado correctamente
- Saldo pendiente actualizado
- Recibo generado
- Ingresos distribuidos por odontólogo

#### CU-014: Procesar Pago Mixto
**Actor Principal:** Administrador  
**Precondiciones:** 
- Consulta con saldo pendiente en ambas monedas
- Cliente desea pagar en múltiples monedas

**Objetivo:** Registrar pago utilizando BS y USD simultáneamente  

**Flujo Principal:**
1. Administrador accede al módulo de pagos
2. Administrador selecciona consulta a pagar
3. Sistema muestra saldos pendientes en ambas monedas
4. Administrador selecciona "Pago Mixto"
5. Sistema muestra interface de pago dual:
   - Campo para monto en BS
   - Campo para monto en USD
   - Calculadora de equivalencias
6. Administrador ingresa montos en cada moneda
7. Sistema valida que no excedan saldos pendientes
8. Administrador especifica métodos de pago por moneda:
   - Método para pago en BS
   - Método para pago en USD
   - Referencias respectivas
9. Sistema calcula tasa de cambio actual
10. Sistema muestra resumen del pago mixto
11. Administrador confirma transacción
12. Sistema registra ambos pagos vinculados
13. Sistema actualiza saldos en ambas monedas
14. Sistema genera recibo consolidado
15. Sistema distribuye ingresos por odontólogo en monedas correspondientes

**Flujos Alternativos:**
- **A1:** Tasa de cambio no actualizada - Sistema solicita actualización
- **A2:** Métodos de pago diferentes - Sistema valida compatibilidad
- **A3:** Error en cálculos - Sistema recalcula automáticamente

**Postcondiciones:**
- Pago mixto registrado correctamente
- Saldos en ambas monedas actualizados
- Recibo consolidado generado
- Distribución por odontólogo en monedas respectivas

### 3.7 MÓDULO DE REPORTES Y ESTADÍSTICAS

#### CU-015: Generar Reporte de Productividad
**Actor Principal:** Gerente  
**Precondiciones:** 
- Usuario autenticado como Gerente
- Existen datos de intervenciones en el período

**Objetivo:** Obtener estadísticas de productividad por odontólogo  

**Flujo Principal:**
1. Gerente accede al módulo de reportes
2. Gerente selecciona "Reporte de Productividad"
3. Sistema muestra opciones de filtros:
   - Rango de fechas
   - Odontólogo específico o todos
   - Tipo de servicios
4. Gerente configura filtros deseados
5. Sistema procesa información y genera reporte con:
   - Intervenciones realizadas por odontólogo
   - Servicios más frecuentes
   - Ingresos generados en BS y USD
   - Tiempo promedio por intervención
   - Pacientes únicos atendidos
   - Comparativas entre odontólogos
6. Sistema presenta reporte en formato visual e interactivo
7. Gerente puede exportar reporte en PDF o Excel

**Flujos Alternativos:**
- **A1:** Sin datos en período - Sistema muestra mensaje informativo
- **A2:** Error en exportación - Sistema ofrece formato alternativo

**Postcondiciones:**
- Reporte generado exitosamente
- Datos exportados si se solicita

#### CU-016: Generar Reporte Financiero
**Actor Principal:** Gerente  
**Precondiciones:** 
- Usuario autenticado como Gerente
- Existen transacciones de pago

**Objetivo:** Obtener resumen financiero de la clínica  

**Flujo Principal:**
1. Gerente accede a reportes financieros
2. Sistema muestra opciones de reporte:
   - Ingresos por período
   - Ingresos por odontólogo
   - Análisis de pagos pendientes
   - Comparativa de monedas
3. Gerente selecciona tipo de reporte y período
4. Sistema genera reporte financiero con:
   - Total de ingresos en BS y USD
   - Distribución por método de pago
   - Evolución temporal de ingresos
   - Análisis de saldos pendientes
   - Proyecciones basadas en tendencias
5. Sistema presenta gráficos y tablas interactivas
6. Gerente puede desglosar información por categorías
7. Sistema permite exportación en múltiples formatos

**Flujos Alternativos:**
- **A1:** Datos incompletos - Sistema indica períodos con información faltante
- **A2:** Error en cálculos - Sistema recalcula y valida datos

**Postcondiciones:**
- Reporte financiero generado
- Análisis y proyecciones disponibles

---

## 4. MATRIZ DE CASOS DE USO vs ACTORES

| Caso de Uso | Gerente | Administrador | Odontólogo | Asistente |
|-------------|---------|---------------|------------|-----------|
| CU-001: Gestionar Personal | ● | | | |
| CU-002: Autenticar Usuario | ● | ● | ● | ● |
| CU-003: Registrar Paciente | ● | ● | | |
| CU-004: Buscar Paciente | ● | ● | ● | ● |
| CU-005: Crear Consulta por Llegada | ● | ● | | |
| CU-006: Gestionar Cola de Atención | ● | ● | | ◐ |
| CU-007: Cambiar Odontólogo | ● | ● | | |
| CU-008: Atender Paciente | | | ● | |
| CU-009: Realizar Intervención | | | ● | |
| CU-010: Derivar a Otro Odontólogo | | | ● | |
| CU-011: Actualizar Odontograma | | | ● | |
| CU-012: Consultar Historial Odontograma | ● | ● | ● | ◐ |
| CU-013: Procesar Pago Simple | ● | ● | | |
| CU-014: Procesar Pago Mixto | ● | ● | | |
| CU-015: Generar Reporte Productividad | ● | | | |
| CU-016: Generar Reporte Financiero | ● | | | |

**Leyenda:**
- ● = Actor principal (acceso completo)
- ◐ = Actor secundario (acceso limitado/consulta)

---

## 5. FLUJO PRINCIPAL DE TRABAJO

### 5.1 Proceso Completo de Atención

```
LLEGADA DEL PACIENTE
         ↓
[CU-003] Registrar Paciente (si es nuevo)
         ↓
[CU-005] Crear Consulta por Llegada
         ↓
[CU-006] Asignar a Cola de Odontólogo
         ↓
[CU-008] Odontólogo Atiende Paciente
         ↓
[CU-009] Realizar Intervención
         ↓
[CU-011] Actualizar Odontograma (si aplica)
         ↓
¿Requiere otro odontólogo?
    ↙ Sí              ↘ No
[CU-010] Derivar         [CU-013/014] Procesar Pago
    ↓                        ↓
Volver a CU-008         FIN DE CONSULTA
```

### 5.2 Procesos Administrativos Paralelos

```
GESTIÓN DE PERSONAL
[CU-001] Registrar Personal → [CU-002] Crear Usuario

GESTIÓN DE COLAS
[CU-006] Monitorear Colas → [CU-007] Reasignar si necesario

REPORTES GERENCIALES
[CU-015] Productividad → [CU-016] Finanzas
```

---

## 6. DEPENDENCIAS ENTRE CASOS DE USO

### 6.1 Dependencias Obligatorias
- **CU-001 → CU-002:** Personal debe tener usuario para acceder
- **CU-003 → CU-005:** Paciente debe existir para crear consulta
- **CU-005 → CU-008:** Consulta debe existir para ser atendida
- **CU-008 → CU-009:** Paciente debe estar en atención para intervenir
- **CU-009 → CU-013/014:** Intervención debe existir para generar pago

### 6.2 Dependencias Opcionales
- **CU-009 ↔ CU-011:** Intervención puede requerir actualización de odontograma
- **CU-008 → CU-010:** Atención puede requerir derivación
- **CU-007 ← CU-006:** Gestión de colas puede requerir reasignaciones

---

## 7. VALIDACIONES TRANSVERSALES

### 7.1 Validaciones de Seguridad
- Todos los casos de uso requieren autenticación previa
- Permisos validados según rol antes de cada operación
- Auditoría automática de todas las acciones sensibles
- Protección de datos médicos según confidencialidad

### 7.2 Validaciones de Negocio
- Un paciente no puede tener múltiples consultas activas simultáneamente
- Un odontólogo no puede atender múltiples pacientes simultáneamente
- Los pagos no pueden exceder el saldo pendiente
- Las intervenciones deben estar vinculadas a consultas activas

### 7.3 Validaciones de Integridad
- Números únicos (historia, consulta, recibo) se generan automáticamente
- Estados de consulta siguen flujo lógico definido
- Totales monetarios se calculan automáticamente y son consistentes
- Versiones de odontograma mantienen trazabilidad histórica

---

**Documento preparado para:** Presentación de Tesis - Sistema Odontológico  
**Metodología:** RUP (Rational Unified Process)  
**Próximo paso:** Diagramas de Casos de Uso (FASE RUP 2)