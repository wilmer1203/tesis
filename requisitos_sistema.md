# REQUISITOS DEL SISTEMA
## Sistema de Información Odontológico - Clínica Dental OdontoMara

**Versión:** 1.0  
**Fecha:** Agosto 2025  
**Metodología:** RUP (Rational Unified Process)  
**Fase:** Concepción - Elaboración  

---

## 1. INFORMACIÓN GENERAL DEL PROYECTO

### 1.1 Propósito del Sistema
Desarrollar un sistema de información integral para la gestión de una clínica dental, optimizado para el flujo específico de consultas por orden de llegada (sin citas programadas), con capacidad de manejo de múltiples odontólogos por consulta, pagos en múltiples monedas, y odontograma digital interactivo.

### 1.2 Alcance del Sistema
El sistema cubrirá todos los procesos operativos de la clínica dental:
- Gestión de pacientes y personal
- Control de consultas por orden de llegada
- Intervenciones odontológicas múltiples
- Odontograma digital con versionado
- Sistema de pagos mixtos (BS/USD)
- Reportes administrativos y clínicos
- Control de acceso por roles

### 1.3 Características del Negocio
- **Modalidad:** Consultas por orden de llegada (NO citas programadas)
- **Flujo:** Paciente llega → Se asigna a odontólogo → Cola específica por odontólogo
- **Atención:** Múltiples odontólogos pueden atender la misma consulta
- **Pagos:** Sistema dual Bolívares/Dólares
- **Personal:** 4 roles definidos (Gerente, Administrador, Odontólogo, Asistente)

---

## 2. REQUISITOS FUNCIONALES

### 2.1 GESTIÓN DE USUARIOS Y PERSONAL

#### RF-001: Gestión de Roles de Usuario
**Prioridad:** Alta  
**Descripción:** El sistema debe permitir la gestión de cuatro roles específicos de usuario.

**Criterios de Aceptación:**
- El sistema debe soportar exactamente 4 roles: Gerente, Administrador, Odontólogo, Asistente
- Cada rol debe tener permisos específicos y granulares
- Los permisos deben ser configurables por módulo y acción
- El Gerente debe tener acceso completo al sistema excepto atención directa de pacientes
- Solo usuarios autorizados pueden crear y modificar roles

**Entrada:** Información del rol (nombre, descripción, permisos)  
**Salida:** Confirmación de creación/modificación del rol  
**Flujo Principal:**
1. Usuario autorizado accede al módulo de roles
2. Especifica nombre, descripción y permisos granulares
3. Sistema valida la información
4. Sistema crea/actualiza el rol
5. Sistema confirma la operación

#### RF-002: Registro y Gestión de Personal
**Prioridad:** Alta  
**Descripción:** El sistema debe permitir el registro completo del personal médico y administrativo.

**Criterios de Aceptación:**
- Cada miembro del personal debe tener un usuario asociado
- Los datos personales deben incluir: nombres, apellidos, documento, celular, dirección
- Los datos profesionales deben incluir: tipo de personal, especialidad, número de licencia
- El estado laboral debe ser: 'activo' o 'inactivo' únicamente
- Para odontólogos: configurar disponibilidad y orden de preferencia

**Entrada:** Datos personales y profesionales del personal  
**Salida:** Confirmación de registro y credenciales de acceso  

#### RF-003: Autenticación y Autorización
**Prioridad:** Alta  
**Descripción:** El sistema debe implementar autenticación segura integrada con Supabase Auth.

**Criterios de Aceptación:**
- Autenticación mediante email y contraseña
- Integración completa con Supabase Auth
- Control de acceso basado en roles (RBAC)
- Sesiones seguras con tiempo de expiración
- Registro de último acceso de cada usuario

### 2.2 GESTIÓN DE PACIENTES

#### RF-004: Registro de Pacientes
**Prioridad:** Alta  
**Descripción:** El sistema debe permitir el registro completo de pacientes con generación automática de número de historia.

**Criterios de Aceptación:**
- Generación automática de número de historia (formato: HC000001)
- Validación de documento de identidad único
- Campos obligatorios: nombres, apellidos, documento
- Campos opcionales: celulares, email, dirección, información médica básica
- Tipos de documento: CI (Cédula de Identidad) o Pasaporte
- Cálculo automático de edad basado en fecha de nacimiento

**Entrada:** Información personal y médica del paciente  
**Salida:** Número de historia asignado y confirmación de registro  

#### RF-005: Búsqueda y Consulta de Pacientes
**Prioridad:** Alta  
**Descripción:** El sistema debe proporcionar múltiples opciones de búsqueda de pacientes.

**Criterios de Aceptación:**
- Búsqueda por número de historia clínica
- Búsqueda por número de documento
- Búsqueda por nombres y apellidos (parcial)
- Búsqueda por celular
- Resultados ordenados por relevancia
- Filtros por estado (activo/inactivo)

### 2.3 GESTIÓN DE CONSULTAS Y COLAS

#### RF-006: Creación de Consulta por Orden de Llegada
**Prioridad:** Alta  
**Descripción:** El sistema debe permitir crear consultas basadas en orden de llegada sin citas programadas.

**Criterios de Aceptación:**
- Generación automática de número de consulta (formato: YYYYMMDD001)
- Asignación automática de orden de llegada general del día
- Selección de odontólogo preferido por el paciente
- Asignación automática a cola específica del odontólogo
- Estados: en_espera, en_atencion, entre_odontologos, completada, cancelada
- Registro automático de fecha y hora de llegada

**Entrada:** Paciente, odontólogo preferido, motivo de consulta  
**Salida:** Número de consulta y posición en cola  

#### RF-007: Gestión de Colas por Odontólogo
**Prioridad:** Alta  
**Descripción:** El sistema debe manejar colas independientes por cada odontólogo activo.

**Criterios de Aceptación:**
- Cola específica e independiente para cada odontólogo
- Visualización de posición actual en cada cola
- Cambio de paciente entre colas de odontólogos
- Estadísticas en tiempo real: pacientes esperando, atendiendo, atendidos
- Próximo paciente en cola claramente identificado
- Tiempo de espera calculado automáticamente

#### RF-008: Cambio de Odontólogo en Consulta
**Prioridad:** Media  
**Descripción:** El sistema debe permitir reasignar pacientes entre odontólogos.

**Criterios de Aceptación:**
- Cambio de odontólogo con motivo obligatorio
- Reasignación automática de posición en nueva cola
- Registro histórico de todos los cambios
- Notificación automática del cambio
- Actualización de estadísticas de ambas colas

### 2.4 GESTIÓN DE INTERVENCIONES Y SERVICIOS

#### RF-009: Registro de Intervenciones Odontológicas
**Prioridad:** Alta  
**Descripción:** El sistema debe permitir el registro detallado de intervenciones por cada odontólogo.

**Criterios de Aceptación:**
- Una intervención por odontólogo por consulta
- Múltiples servicios dentro de una intervención
- Registro de dientes afectados (numeración FDI)
- Registro de materiales utilizados y anestesia
- Control de tiempo: hora inicio, hora fin, duración real
- Estado de intervención: en_progreso, completada, suspendida
- Cálculo automático de costos en BS y USD

#### RF-010: Catálogo de Servicios Odontológicos
**Prioridad:** Alta  
**Descripción:** El sistema debe mantener un catálogo completo de servicios con precios duales.

**Criterios de Aceptación:**
- Servicios categorizados (Consulta, Preventiva, Restaurativa, etc.)
- Precios en Bolívares y Dólares
- Duración estimada por servicio
- Códigos únicos alfanuméricos
- Instrucciones pre y post tratamiento
- Gestión de estado activo/inactivo

#### RF-011: Múltiples Servicios por Intervención
**Prioridad:** Alta  
**Descripción:** El sistema debe permitir que un odontólogo realice múltiples servicios en una sola intervención.

**Criterios de Aceptación:**
- Selección múltiple de servicios por intervención
- Cantidad específica de cada servicio
- Precios individuales y totales calculados automáticamente
- Dientes específicos afectados por cada servicio
- Observaciones particulares por servicio

### 2.5 ODONTOGRAMA DIGITAL

#### RF-012: Odontograma Interactivo
**Prioridad:** Alta  
**Descripción:** El sistema debe proporcionar un odontograma digital interactivo y detallado.

**Criterios de Aceptación:**
- Numeración FDI estándar internacional
- Interfaz visual interactiva para selección de dientes
- Tipos de condición: sano, caries, obturación, corona, puente, implante, ausente, etc.
- Selección específica de caras afectadas por diente
- Colores y símbolos diferenciados por condición
- Anotaciones detalladas por diente y cara
- Compatible con dientes temporales y permanentes

#### RF-013: Versionado Histórico del Odontograma
**Prioridad:** Alta  
**Descripción:** El sistema debe mantener un historial completo de versiones del odontograma.

**Criterios de Aceptación:**
- Creación automática de nueva versión al modificar
- Solo una versión activa por paciente
- Referencia a versión anterior para trazabilidad
- Motivo de creación de nueva versión
- Visualización comparativa entre versiones
- Estadísticas automáticas de condiciones por versión
- Restricción de eliminación de versiones históricas

#### RF-014: Registro de Cambios por Intervención
**Prioridad:** Media  
**Descripción:** El sistema debe registrar qué cambios específicos se hicieron en cada intervención.

**Criterios de Aceptación:**
- Vinculación de condiciones con intervención de origen
- Registro de antes y después por intervención
- Odontólogo responsable de cada cambio
- Fecha y hora específica de cada modificación

### 2.6 SISTEMA DE PAGOS

#### RF-015: Pagos en Múltiples Monedas
**Prioridad:** Alta  
**Descripción:** El sistema debe manejar pagos en Bolívares Soberanos (BS) y Dólares Americanos (USD).

**Criterios de Aceptación:**
- Facturación en ambas monedas simultáneamente
- Pagos mixtos: parte en BS, parte en USD
- Tasa de cambio registrada al momento del pago
- Cálculo automático de saldos pendientes en cada moneda
- Múltiples métodos de pago por transacción
- Generación automática de número de recibo (formato: RECYYYYMM0001)

#### RF-016: Gestión de Saldos y Pagos Parciales
**Prioridad:** Alta  
**Descripción:** El sistema debe permitir pagos parciales y gestión de saldos pendientes.

**Criterios de Aceptación:**
- Pagos parciales en cualquier moneda
- Cálculo automático de saldos pendientes
- Estados: pendiente, completado, parcial, anulado, reembolsado
- Historial completo de pagos por consulta
- Aplicación de descuentos con justificación

#### RF-017: Distribución de Ingresos por Odontólogo
**Prioridad:** Media  
**Descripción:** El sistema debe calcular automáticamente los ingresos por odontólogo.

**Criterios de Aceptación:**
- Cada odontólogo recibe el total de sus intervenciones
- Cálculo en la moneda en que se pagó cada intervención
- Reportes de ingresos por período
- Estadísticas de productividad por odontólogo

### 2.7 HISTORIAL MÉDICO

#### RF-018: Registro de Historial Clínico
**Prioridad:** Alta  
**Descripción:** El sistema debe mantener un historial médico completo por paciente.

**Criterios de Aceptación:**
- Vinculación con consultas específicas e intervenciones
- Registro de síntomas, examen clínico, diagnóstico
- Plan de tratamiento y pronóstico
- Medicamentos recetados en formato estructurado
- Recomendaciones e instrucciones al paciente
- Signos vitales cuando aplique
- Adjuntos: imágenes y documentos

#### RF-019: Control de Confidencialidad
**Prioridad:** Alta  
**Descripción:** El sistema debe permitir marcar información como confidencial.

**Criterios de Aceptación:**
- Clasificación de confidencialidad por registro
- Acceso restringido según rol de usuario
- Registro de auditoría para información confidencial

### 2.8 REPORTES Y ESTADÍSTICAS

#### RF-020: Reportes Administrativos
**Prioridad:** Media  
**Descripción:** El sistema debe generar reportes para la gestión administrativa.

**Criterios de Aceptación:**
- Consultas atendidas por día/mes/año
- Ingresos por período en ambas monedas
- Productividad por odontólogo
- Servicios más realizados
- Estadísticas de tiempos de espera
- Reportes de pacientes nuevos vs. recurrentes

#### RF-021: Reportes Clínicos
**Prioridad:** Media  
**Descripción:** El sistema debe generar reportes para análisis clínico.

**Criterios de Aceptación:**
- Evolución de tratamientos por paciente
- Estadísticas de condiciones odontológicas
- Comparativas de odontogramas en el tiempo
- Seguimiento de casos específicos

---

## 3. REQUISITOS NO FUNCIONALES

### 3.1 RENDIMIENTO

#### RNF-001: Tiempo de Respuesta
**Prioridad:** Alta  
**Descripción:** El sistema debe mantener tiempos de respuesta aceptables.

**Criterios de Aceptación:**
- Consultas simples: máximo 2 segundos
- Carga de odontograma: máximo 3 segundos
- Reportes complejos: máximo 10 segundos
- Búsquedas de pacientes: máximo 1 segundo

#### RNF-002: Capacidad de Usuarios Concurrentes
**Prioridad:** Media  
**Descripción:** El sistema debe soportar múltiples usuarios simultáneos.

**Criterios de Aceptación:**
- Mínimo 10 usuarios concurrentes sin degradación
- Escalabilidad horizontal mediante Supabase
- Gestión eficiente de conexiones a base de datos

### 3.2 SEGURIDAD

#### RNF-003: Autenticación y Autorización
**Prioridad:** Alta  
**Descripción:** El sistema debe implementar medidas de seguridad robustas.

**Criterios de Aceptación:**
- Autenticación de doble factor opcional
- Encriptación de datos sensibles en tránsito y reposo
- Políticas de contraseñas seguras
- Sesiones con tiempo de expiración
- Control de acceso basado en roles (RBAC)

#### RNF-004: Auditoría y Trazabilidad
**Prioridad:** Alta  
**Descripción:** El sistema debe registrar todas las acciones críticas.

**Criterios de Aceptación:**
- Registro de todas las operaciones CRUD en datos sensibles
- Identificación del usuario, fecha, hora, IP
- Datos antes y después de cada modificación
- Registros inmutables de auditoría
- Retención mínima de logs: 5 años

#### RNF-005: Protección de Datos Médicos
**Prioridad:** Alta  
**Descripción:** El sistema debe cumplir con estándares de protección de datos médicos.

**Criterios de Aceptación:**
- Cumplimiento con regulaciones locales de datos médicos
- Clasificación de información por nivel de sensibilidad
- Acceso restringido a información confidencial
- Respaldo seguro de información médica

### 3.3 USABILIDAD

#### RNF-006: Interfaz de Usuario Intuitiva
**Prioridad:** Alta  
**Descripción:** El sistema debe ser fácil de usar para personal con conocimientos básicos de informática.

**Criterios de Aceptación:**
- Interfaz web responsive para diferentes dispositivos
- Navegación clara y consistente
- Formularios con validación en tiempo real
- Mensajes de error claros y orientativos
- Ayuda contextual en funciones complejas

#### RNF-007: Accesibilidad
**Prioridad:** Media  
**Descripción:** El sistema debe ser accesible para usuarios con diferentes capacidades.

**Criterios de Aceptación:**
- Contraste de colores adecuado
- Navegación por teclado
- Texto alternativo en imágenes importantes
- Tamaños de fuente ajustables

### 3.4 DISPONIBILIDAD

#### RNF-008: Disponibilidad del Sistema
**Prioridad:** Alta  
**Descripción:** El sistema debe estar disponible durante horas de operación.

**Criterios de Aceptación:**
- Disponibilidad mínima: 99% durante horario laboral
- Tiempo máximo de inactividad planificada: 2 horas/mes
- Recuperación ante fallos: máximo 30 minutos
- Respaldos automáticos diarios

#### RNF-009: Recuperación ante Desastres
**Prioridad:** Media  
**Descripción:** El sistema debe tener capacidad de recuperación ante fallos.

**Criterios de Aceptación:**
- Respaldos automáticos en múltiples ubicaciones
- Procedimientos documentados de recuperación
- Pruebas periódicas de recuperación
- RTO (Recovery Time Objective): 4 horas
- RPO (Recovery Point Objective): 1 hora

### 3.5 ESCALABILIDAD

#### RNF-010: Crecimiento de Datos
**Prioridad:** Media  
**Descripción:** El sistema debe manejar el crecimiento proyectado de datos.

**Criterios de Aceptación:**
- Capacidad para 10,000+ pacientes
- 100+ consultas diarias
- Crecimiento anual del 30% sin degradación
- Archivado automático de datos históricos

#### RNF-011: Escalabilidad Técnica
**Prioridad:** Media  
**Descripción:** El sistema debe ser escalable técnicamente.

**Criterios de Aceptación:**
- Arquitectura basada en microservicios con Reflex.dev
- Base de datos escalable con Supabase
- CDN para recursos estáticos
- Optimización de consultas automática

### 3.6 COMPATIBILIDAD

#### RNF-012: Compatibilidad de Navegadores
**Prioridad:** Alta  
**Descripción:** El sistema debe funcionar en navegadores modernos.

**Criterios de Aceptación:**
- Chrome 90+, Firefox 88+, Safari 14+, Edge 90+
- Funcionalidad completa sin plugins adicionales
- Responsive design para tablets y móviles

#### RNF-013: Integración con Sistemas Externos
**Prioridad:** Baja  
**Descripción:** El sistema debe tener capacidad de integración futura.

**Criterios de Aceptación:**
- API REST para integraciones externas
- Exportación de datos en formatos estándar
- Webhooks para notificaciones externas

### 3.7 MANTENIBILIDAD

#### RNF-014: Código Mantenible
**Prioridad:** Media  
**Descripción:** El código debe ser fácil de mantener y actualizar.

**Criterios de Aceptación:**
- Documentación técnica completa
- Código comentado y estructurado
- Patrones de diseño consistentes
- Pruebas unitarias con cobertura >80%

#### RNF-015: Configurabilidad
**Prioridad:** Media  
**Descripción:** El sistema debe permitir configuración sin cambios de código.

**Criterios de Aceptación:**
- Configuración de parámetros del sistema vía interfaz
- Configuración de precios y servicios
- Personalización de campos opcionales
- Configuración de roles y permisos

---

## 4. RESTRICCIONES Y LIMITACIONES

### 4.1 Restricciones Técnicas

#### RT-001: Tecnologías Obligatorias
- **Frontend:** Reflex.dev (Python)
- **Backend:** Reflex.dev con Supabase
- **Base de datos:** PostgreSQL (vía Supabase)
- **Autenticación:** Supabase Auth
- **Hosting:** Supabase + servicio compatible con Reflex

#### RT-002: Restricciones de Despliegue
- Sistema debe funcionar completamente en la nube
- Sin dependencias de software local específico
- Acceso exclusivo vía navegador web

### 4.2 Restricciones del Negocio

#### RN-001: Flujo Operativo
- NO se implementarán citas programadas
- Solo consultas por orden de llegada
- Máximo 4 roles de usuario predefinidos

#### RN-002: Restricciones Regulatorias
- Cumplimiento con ley de protección de datos personales
- Retención mínima de historiales médicos: 5 años
- Trazabilidad completa de cambios en información médica

### 4.3 Limitaciones del Proyecto

#### LP-001: Recursos
- Desarrollo por equipo de 1 persona
- Presupuesto limitado para servicios externos
- Tiempo de desarrollo: 6 meses máximo

#### LP-002: Funcionalidades Excluidas en v1.0
- Integración con equipos médicos
- Telemedicina
- App móvil nativa
- Integración contable avanzada
- Múltiples sucursales

---

## 5. CRITERIOS DE ACEPTACIÓN GENERALES

### 5.1 Funcionalidad
- Todas las funciones especificadas deben operar correctamente
- Validación completa de datos de entrada
- Manejo adecuado de errores y excepciones
- Interfaz coherente en todo el sistema

### 5.2 Calidad
- Pruebas unitarias con cobertura mínima del 80%
- Pruebas de integración para flujos críticos
- Pruebas de usabilidad con usuarios finales
- Documentación técnica y de usuario completa

### 5.3 Rendimiento
- Cumplimiento de todos los requisitos no funcionales
- Pruebas de carga con usuarios concurrentes
- Optimización de consultas de base de datos
- Monitoreo de rendimiento en producción

---

## 6. MATRIZ DE TRAZABILIDAD

| ID Requisito | Prioridad | Módulo Afectado | Casos de Uso | Estado |
|--------------|-----------|-----------------|--------------|--------|
| RF-001 | Alta | Usuarios | CU-001, CU-002 | Definido |
| RF-002 | Alta | Personal | CU-003, CU-004 | Definido |
| RF-006 | Alta | Consultas | CU-010, CU-011 | Definido |
| RF-012 | Alta | Odontograma | CU-020, CU-021 | Definido |
| RF-015 | Alta | Pagos | CU-025, CU-026 | Definido |

---

**Documento preparado para:** Presentación de Tesis - Sistema Odontológico  
**Metodología:** RUP (Rational Unified Process)  
**Próximo paso:** Casos de Uso del Negocio y Modelo de Dominio