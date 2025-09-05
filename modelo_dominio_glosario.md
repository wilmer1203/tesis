# MODELO DE DOMINIO Y GLOSARIO
## Sistema de Información Odontológico - Clínica Dental OdontoMara

**Versión:** 1.0  
**Fecha:** Agosto 2025  
**Metodología:** RUP (Rational Unified Process)  
**Fase:** Concepción - Elaboración  

---

## 1. INTRODUCCIÓN

### 1.1 Propósito del Documento
Este documento define el modelo conceptual del dominio del negocio y establece un glosario de términos común para todos los stakeholders del proyecto. Sirve como base para el entendimiento compartido del sistema odontológico.

### 1.2 Alcance del Modelo
El modelo de dominio cubre todas las entidades, relaciones y procesos de negocio de la clínica dental, incluyendo:
- Gestión de personal y pacientes
- Flujo de consultas por orden de llegada
- Intervenciones odontológicas múltiples
- Sistema de pagos duales
- Odontograma digital con versionado

---

## 2. GLOSARIO DE TÉRMINOS

### 2.1 TÉRMINOS GENERALES

**Administrador**  
Personal encargado de tareas administrativas como crear pacientes, consultas y gestionar pagos. No puede gestionar personal ni configuraciones del sistema.

**Asistente**  
Personal de apoyo que tiene acceso limitado al sistema, principalmente para consultar información de pacientes y consultas.

**Auditoría**  
Registro automático de todas las acciones realizadas en el sistema, incluyendo usuario, fecha, hora, acción realizada y datos modificados.

**Autenticación**  
Proceso de verificación de identidad de un usuario mediante credenciales (email y contraseña).

**Autorización**  
Proceso de verificación de permisos de un usuario para realizar acciones específicas en el sistema.

**BS (Bolívares Soberanos)**  
Moneda nacional de Venezuela utilizada en el sistema de pagos.

**Celular**  
Número de teléfono móvil. Término estándar utilizado en el sistema en lugar de "teléfono".

**CI (Cédula de Identidad)**  
Documento de identificación nacional venezolano.

**Clínica Dental**  
Establecimiento de salud dedicado a la atención odontológica donde opera el sistema.

**Estado Laboral**  
Condición del personal que puede ser únicamente: 'activo' o 'inactivo'.

**Gerente**  
Rol con acceso completo al sistema, excepto la atención directa de pacientes. Puede gestionar personal, configuraciones y acceder a todos los reportes.

**Metodología RUP**  
Rational Unified Process, metodología de desarrollo de software utilizada en este proyecto.

**Numeración FDI**  
Sistema internacional de numeración dental de la Federación Dental Internacional.

**Odontólogo**  
Profesional de la salud dental que atiende pacientes, realiza intervenciones y gestiona odontogramas.

**Pasaporte**  
Documento de identificación internacional aceptado en el sistema.

**RBAC (Role-Based Access Control)**  
Control de acceso basado en roles implementado en el sistema.

**Reflex.dev**  
Framework de desarrollo web en Python utilizado para el frontend y backend del sistema.

**Supabase**  
Plataforma backend-as-a-service utilizada para base de datos, autenticación y hosting.

**USD (Dólares Americanos)**  
Moneda extranjera utilizada en el sistema de pagos junto con los Bolívares.

### 2.2 TÉRMINOS DEL DOMINIO ODONTOLÓGICO

**Anestesia**  
Medicamento utilizado para eliminar la sensación de dolor durante un procedimiento odontológico.

**Cara Dental**  
Superficie específica de un diente (oclusal, mesial, distal, vestibular, lingual/palatino).

**Caries**  
Enfermedad dental caracterizada por la destrucción de los tejidos del diente por ácidos producidos por bacterias.

**Corona Dental**  
Prótesis fija que cubre completamente la parte visible de un diente.

**Cuadrante Dental**  
División de la boca en 4 secciones para la numeración FDI (superior derecho, superior izquierdo, inferior izquierdo, inferior derecho).

**Diente Temporal**  
Diente de leche o deciduo que se presenta en la dentición infantil.

**Endodoncia**  
Tratamiento del conducto radicular del diente, comúnmente llamado "tratamiento de nervio".

**Extracción Dental**  
Procedimiento quirúrgico para remover un diente de su alveolo.

**Implante Dental**  
Dispositivo de titanio insertado en el hueso maxilar para reemplazar la raíz de un diente perdido.

**Obturación**  
Restauración dental que rellena una cavidad causada por caries, comúnmente llamada "tapadura".

**Prótesis Dental**  
Dispositivo que reemplaza dientes perdidos, puede ser fija o removible.

**Puente Dental**  
Prótesis fija que reemplaza uno o más dientes perdidos, apoyándose en dientes adyacentes.

**Radiografía Dental**  
Imagen de rayos X utilizada para diagnóstico odontológico.

### 2.3 TÉRMINOS ESPECÍFICOS DEL SISTEMA

**Cola de Atención**  
Lista de pacientes esperando ser atendidos por un odontólogo específico, ordenada por llegada.

**Consulta**  
Atención odontológica completa que puede incluir múltiples intervenciones de diferentes odontólogos.

**Condición Dental**  
Estado específico de un diente registrado en el odontograma (sano, caries, obturación, etc.).

**Historial Médico**  
Registro completo de la información clínica del paciente a lo largo del tiempo.

**Intervención**  
Procedimiento específico realizado por un odontólogo durante una consulta, puede incluir múltiples servicios.

**Número de Historia**  
Identificador único del paciente en formato HC000001, generado automáticamente.

**Número de Consulta**  
Identificador único de la consulta en formato YYYYMMDD001, generado automáticamente.

**Número de Recibo**  
Identificador único del pago en formato RECYYYYMM0001, generado automáticamente.

**Odontograma**  
Representación gráfica del estado de todos los dientes de un paciente.

**Orden de Llegada**  
Posición secuencial asignada automáticamente según el momento de llegada del paciente.

**Pago Mixto**  
Transacción que involucra pagos en múltiples monedas (BS y USD) simultáneamente.

**Servicio Odontológico**  
Procedimiento específico con código, precio y duración definidos en el catálogo.

**Tasa de Cambio**  
Valor de conversión entre Bolívares y Dólares registrado al momento del pago.

**Versión de Odontograma**  
Instantánea histórica del estado del odontograma en un momento específico.

---

## 3. MODELO CONCEPTUAL DEL DOMINIO

### 3.1 ENTIDADES PRINCIPALES

#### 3.1.1 USUARIO
**Definición:** Persona autorizada para acceder al sistema con credenciales específicas.

**Atributos:**
- ID único del sistema
- Email (único)
- Rol asignado
- Estado (activo/inactivo)
- Fecha de creación
- Último acceso
- ID de autenticación Supabase
- Avatar y metadatos

**Reglas de Negocio:**
- Cada usuario debe tener exactamente un rol
- El email debe ser único en todo el sistema
- Solo usuarios activos pueden acceder al sistema
- La autenticación se maneja vía Supabase Auth

#### 3.1.2 PERSONAL
**Definición:** Miembro del equipo de trabajo de la clínica con información profesional detallada.

**Atributos:**
- Información personal: nombres, apellidos, documento, celular, dirección
- Información profesional: tipo, especialidad, licencia, salario
- Datos laborales: fecha contratación, estado laboral
- Para odontólogos: acepta pacientes nuevos, orden de preferencia

**Reglas de Negocio:**
- Cada personal debe tener un usuario asociado
- El número de documento debe ser único
- Solo puede haber 4 tipos: Gerente, Administrador, Odontólogo, Asistente
- Estado laboral solo puede ser 'activo' o 'inactivo'
- Solo odontólogos pueden atender pacientes

#### 3.1.3 PACIENTE
**Definición:** Persona que recibe atención odontológica en la clínica.

**Atributos:**
- Número de historia (único, generado automáticamente)
- Información personal: nombres, apellidos, documento, edad, género
- Información de contacto: celulares, email, dirección
- Información médica: alergias, medicamentos, condiciones médicas
- Contacto de emergencia

**Reglas de Negocio:**
- Número de historia se genera automáticamente (HC000001)
- Número de documento debe ser único
- Edad se calcula automáticamente de la fecha de nacimiento
- Tipos de documento: CI o Pasaporte únicamente

#### 3.1.4 CONSULTA
**Definición:** Atención odontológica completa por orden de llegada que puede involucrar múltiples odontólogos.

**Atributos:**
- Número de consulta (único, generado automáticamente)
- Paciente asociado
- Primer odontólogo asignado
- Odontólogo preferido (opcional)
- Fecha y hora de llegada
- Orden de llegada general y por odontólogo
- Estado de la consulta
- Tipo y prioridad
- Costos totales en BS y USD

**Reglas de Negocio:**
- No se programan citas, solo orden de llegada
- Número de consulta formato: YYYYMMDD001
- Cada paciente tiene una cola específica por odontólogo
- Estados: en_espera, en_atencion, entre_odontologos, completada, cancelada
- Puede ser atendida por múltiples odontólogos (diferentes intervenciones)

#### 3.1.5 INTERVENCIÓN
**Definición:** Procedimiento específico realizado por un odontólogo durante una consulta.

**Atributos:**
- Consulta asociada
- Odontólogo responsable
- Asistente (opcional)
- Tiempo de inicio y fin
- Dientes afectados
- Diagnóstico y procedimiento realizado
- Materiales y anestesia utilizados
- Totales en BS y USD
- Estado de la intervención

**Reglas de Negocio:**
- Una intervención por odontólogo por consulta
- Puede incluir múltiples servicios
- Siempre se completa en una sesión
- Los totales se calculan automáticamente
- Si otro odontólogo atiende = nueva intervención

#### 3.1.6 SERVICIO
**Definición:** Procedimiento odontológico específico con características y precios definidos.

**Atributos:**
- Código único
- Nombre y descripción
- Categoría y subcategoría
- Duración estimada
- Precios base en BS y USD
- Materiales incluidos
- Instrucciones pre y post tratamiento

**Reglas de Negocio:**
- Código debe ser único y alfanumérico
- Debe tener precios en ambas monedas
- Pueden estar activos o inactivos
- Categorizados para reportes

#### 3.1.7 PAGO
**Definición:** Transacción financiera que puede involucrar múltiples monedas y métodos.

**Atributos:**
- Número de recibo (único, generado automáticamente)
- Consulta asociada
- Paciente asociado
- Montos totales y pagados en BS y USD
- Saldos pendientes en ambas monedas
- Tasa de cambio al momento del pago
- Métodos de pago utilizados
- Estado del pago

**Reglas de Negocio:**
- Número de recibo formato: RECYYYYMM0001
- Soporta pagos mixtos en BS y USD
- Saldos se calculan automáticamente
- Múltiples métodos de pago por transacción
- Estados: pendiente, completado, parcial, anulado, reembolsado

#### 3.1.8 ODONTOGRAMA
**Definición:** Representación digital del estado dental del paciente con control de versiones.

**Atributos:**
- Paciente asociado
- Odontólogo responsable
- Versión numérica
- Tipo de odontograma (adulto, pediátrico, mixto)
- Indicador de versión actual
- Referencia a versión anterior
- Estadísticas de condiciones

**Reglas de Negocio:**
- Solo una versión activa por paciente
- Versionado automático al modificar
- Control histórico completo
- Estadísticas automáticas por versión

#### 3.1.9 CONDICIÓN DENTAL
**Definición:** Estado específico de un diente en el odontograma.

**Atributos:**
- Odontograma asociado
- Diente específico (numeración FDI)
- Tipo de condición
- Caras afectadas
- Severidad
- Material utilizado
- Descripción detallada
- Intervención de origen

**Reglas de Negocio:**
- Basado en numeración FDI internacional
- Múltiples condiciones por diente
- Vinculado a intervención específica
- Estados: planificado, en_tratamiento, actual, histórico

### 3.2 RELACIONES PRINCIPALES

#### 3.2.1 Usuario - Personal
- **Tipo:** Uno a Uno (opcional)
- **Descripción:** Un usuario puede tener información de personal asociada
- **Restricción:** No todos los usuarios son personal (ej: usuarios administrativos externos)

#### 3.2.2 Personal - Consulta
- **Tipo:** Uno a Muchos
- **Descripción:** Un odontólogo puede atender múltiples consultas
- **Restricción:** Solo personal tipo 'Odontólogo' puede ser asignado a consultas

#### 3.2.3 Paciente - Consulta
- **Tipo:** Uno a Muchos
- **Descripción:** Un paciente puede tener múltiples consultas
- **Restricción:** Cada consulta pertenece a exactamente un paciente

#### 3.2.4 Consulta - Intervención
- **Tipo:** Uno a Muchos
- **Descripción:** Una consulta puede tener múltiples intervenciones
- **Restricción:** Máximo una intervención por odontólogo por consulta

#### 3.2.5 Intervención - Servicio
- **Tipo:** Muchos a Muchos (con atributos)
- **Descripción:** Una intervención puede incluir múltiples servicios con cantidad y precios específicos
- **Entidad Asociativa:** intervenciones_servicios

#### 3.2.6 Paciente - Odontograma
- **Tipo:** Uno a Muchos
- **Descripción:** Un paciente tiene múltiples versiones de odontograma
- **Restricción:** Solo una versión activa por paciente

#### 3.2.7 Odontograma - Condición Dental
- **Tipo:** Uno a Muchos
- **Descripción:** Un odontograma contiene múltiples condiciones dentales
- **Restricción:** Cada condición pertenece a una versión específica

### 3.3 REGLAS DE NEGOCIO TRANSVERSALES

#### 3.3.1 Flujo de Atención
1. Paciente llega a la clínica sin cita previa
2. Administrador crea consulta y selecciona odontólogo preferido
3. Sistema asigna automáticamente posición en cola del odontólogo
4. Odontólogo atiende según orden de cola
5. Pueden intervenir múltiples odontólogos en la misma consulta
6. Cada intervención se completa antes de pasar a otro odontólogo
7. Consulta se cierra cuando se completan todas las intervenciones

#### 3.3.2 Sistema de Colas
1. Cada odontólogo activo mantiene su propia cola
2. Pacientes se ordenan por llegada dentro de cada cola
3. Posición se asigna automáticamente al crear consulta
4. Pacientes pueden cambiar de cola con justificación
5. Estadísticas en tiempo real por cada cola

#### 3.3.3 Sistema de Pagos
1. Facturación puede ser en BS, USD o mixta
2. Cada odontólogo recibe el total de sus intervenciones
3. Pagos pueden ser parciales o completos
4. Tasa de cambio se registra al momento del pago
5. Saldos se calculan automáticamente en ambas monedas

#### 3.3.4 Versionado de Odontograma
1. Nueva versión se crea automáticamente al modificar
2. Versión anterior se mantiene como histórica
3. Solo una versión activa por paciente
4. Cambios se vinculan a intervención específica
5. Estadísticas se calculan automáticamente

---

## 4. DIAGRAMA CONCEPTUAL DEL DOMINIO

```
USUARIOS ──── PERSONAL ──── CONSULTAS ──── INTERVENCIONES ──── SERVICIOS
   │              │            │               │                    │
   │              │            │               │                    │
   └── ROLES      └── TIPOS    │               └── INTERVENCIONES───┘
                               │                   SERVICIOS
                               │
                         PACIENTES ──── ODONTOGRAMA ──── CONDICIONES
                               │             │              DENTAL
                               │             │                 │
                               └── PAGOS     └── VERSIONES ────┘
                                   │
                                   └── MÉTODOS_PAGO
```

### 4.1 Descripción del Diagrama

**Módulo de Seguridad (Usuarios-Roles)**
- Gestiona autenticación y autorización
- Control de acceso basado en roles

**Módulo de Personal**
- Información del equipo de trabajo
- Especialización en odontólogos para colas

**Módulo de Pacientes**
- Registro y gestión de pacientes
- Información médica básica

**Módulo de Consultas**
- Flujo principal de atención
- Sistema de colas por odontólogo

**Módulo de Intervenciones**
- Procedimientos clínicos detallados
- Múltiples servicios por intervención

**Módulo de Odontograma**
- Representación digital dental
- Versionado histórico automático

**Módulo de Pagos**
- Transacciones en múltiples monedas
- Distribución automática por odontólogo

---

## 5. CASOS DE USO PRINCIPALES POR ENTIDAD

### 5.1 Gestión de Usuarios
- Autenticar usuario
- Asignar rol a usuario
- Gestionar permisos
- Auditar acciones

### 5.2 Gestión de Personal
- Registrar personal
- Actualizar información profesional
- Gestionar disponibilidad (odontólogos)
- Reportar productividad

### 5.3 Gestión de Pacientes
- Registrar paciente nuevo
- Buscar paciente existente
- Actualizar información médica
- Consultar historial

### 5.4 Gestión de Consultas
- Crear consulta por llegada
- Asignar a cola de odontólogo
- Cambiar odontólogo
- Monitorear colas

### 5.5 Gestión de Intervenciones
- Iniciar intervención
- Registrar procedimientos
- Agregar múltiples servicios
- Completar intervención

### 5.6 Gestión de Odontograma
- Crear odontograma inicial
- Actualizar condiciones dentales
- Crear nueva versión
- Comparar versiones históricas

### 5.7 Gestión de Pagos
- Procesar pago simple
- Procesar pago mixto
- Aplicar descuentos
- Generar reportes financieros

---

## 6. VALIDACIONES Y RESTRICCIONES DEL DOMINIO

### 6.1 Validaciones de Datos

#### Documentos de Identidad
- Formato: solo números, 7-8 dígitos
- Únicos en todo el sistema
- Tipos permitidos: CI, Pasaporte

#### Celulares
- Formato: números, espacios, guiones, paréntesis, signo +
- Longitud: 10-15 caracteres
- Al menos un celular por personal

#### Emails
- Formato RFC válido
- Únicos para usuarios
- Opcionales para pacientes

#### Números de Sistema
- Historia: HC + 6 dígitos (HC000001)
- Consulta: YYYYMMDD + 3 dígitos (20250820001)
- Recibo: REC + YYYYMM + 4 dígitos (REC2025080001)

### 6.2 Restricciones de Negocio

#### Estados del Sistema
- Personal: solo 'activo' o 'inactivo'
- Consulta: 5 estados específicos definidos
- Intervención: 3 estados específicos definidos
- Pago: 5 estados específicos definidos

#### Flujo Operativo
- Sin citas programadas
- Orden de llegada estricto por odontólogo
- Una intervención por odontólogo por consulta
- Intervenciones siempre se completan

#### Sistema Monetario
- Precios obligatorios en BS y USD
- Tasa de cambio registrada por pago
- Cálculos automáticos de totales y saldos

---

**Documento preparado para:** Presentación de Tesis - Sistema Odontológico  
**Metodología:** RUP (Rational Unified Process)  
**Próximo paso:** Casos de Uso del Negocio detallados