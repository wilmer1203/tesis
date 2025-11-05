# 📚 DOCUMENTACIÓN COMPLETA - BASE DE DATOS
## Sistema de Gestión Odontológica

**Fecha:** 2025-11-04
**Versión:** Post-Simplificación V2.0
**Total de Tablas:** 10
**Total de Columnas:** 121

---

## 📋 ÍNDICE DE TABLAS

1. [roles](#1-tabla-roles) - Roles y permisos del sistema
2. [usuarios](#2-tabla-usuarios) - Usuarios del sistema
3. [personal](#3-tabla-personal) - Personal de la clínica
4. [servicios](#4-tabla-servicios) - Catálogo de servicios odontológicos
5. [pacientes](#5-tabla-pacientes) - Pacientes de la clínica
6. [consultas](#6-tabla-consultas) - Consultas por orden de llegada
7. [intervenciones](#7-tabla-intervenciones) - Tratamientos odontológicos
8. [intervenciones_servicios](#8-tabla-intervenciones_servicios) - Servicios aplicados en intervenciones
9. [condiciones_diente](#9-tabla-condiciones_diente) - Odontograma del paciente
10. [pagos](#10-tabla-pagos) - Pagos y facturación

---

# TABLAS DETALLADAS

## 1. TABLA: `roles`

**Descripción:**
Almacena los diferentes roles del sistema que determinan los permisos y nivel de acceso de los usuarios. El sistema cuenta con 4 roles principales: gerente (acceso total), administrador (gestión operativa), odontólogo (atención clínica) y asistente (apoyo básico). Los permisos específicos están hardcodeados en el código de la aplicación, no en la base de datos.

### Columnas:

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | uuid | Identificador único del rol (Primary Key). Generado automáticamente. |
| `nombre` | varchar(50) | Nombre del rol en minúsculas (ej: gerente, administrador, odontologo, asistente). Único en el sistema. |
| `descripcion` | text | Descripción detallada del rol y sus responsabilidades. |
| `activo` | boolean | Indica si el rol está activo en el sistema. Default: true. |
| `fecha_creacion` | timestamptz | Fecha y hora de creación del rol. Default: CURRENT_TIMESTAMP. |
| `fecha_actualizacion` | timestamptz | Fecha y hora de última actualización. Se actualiza automáticamente. |

**Relaciones:**
- Es referenciado por: `usuarios` (1 rol → muchos usuarios)

---

## 2. TABLA: `usuarios`

**Descripción:**
Contiene la información de autenticación y perfil de los usuarios del sistema. Cada usuario tiene asignado un rol que determina sus permisos. Los usuarios están vinculados con Supabase Auth mediante el campo `auth_user_id`, permitiendo autenticación segura con JWT. Un usuario puede estar asociado a un registro en la tabla `personal` si es un empleado de la clínica.

### Columnas:

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | uuid | Identificador único del usuario (Primary Key). Generado automáticamente. |
| `email` | varchar(100) | Correo electrónico del usuario. Único y validado con regex. Requerido. |
| `rol_id` | uuid | Referencia al rol del usuario (Foreign Key → roles.id). Requerido. |
| `activo` | boolean | Indica si el usuario está activo en el sistema. Default: true. |
| `fecha_creacion` | timestamptz | Fecha y hora de creación del usuario. Default: CURRENT_TIMESTAMP. |
| `fecha_actualizacion` | timestamptz | Fecha y hora de última actualización. Se actualiza automáticamente. |
| `auth_user_id` | uuid | ID del usuario en Supabase Auth. Único, permite vinculación con el sistema de autenticación. |

**Relaciones:**
- Depende de: `roles` (muchos usuarios → 1 rol)
- Es referenciado por: `personal` (1 usuario → 1 empleado), `pagos` (1 usuario → muchos pagos procesados)

---

## 3. TABLA: `personal`

**Descripción:**
Almacena la información del personal que trabaja en la clínica odontológica. Incluye odontólogos, administradores, asistentes y gerentes. Cada registro está vinculado a un usuario del sistema mediante `usuario_id`, estableciendo una relación uno a uno. Contiene datos personales, laborales y profesionales (como número de licencia para odontólogos). El campo `tipo_personal` indica el rol laboral de la persona.

### Columnas:

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | uuid | Identificador único del empleado (Primary Key). Generado automáticamente. |
| `usuario_id` | uuid | Referencia al usuario asociado (Foreign Key → usuarios.id). Único, relación 1:1. |
| `primer_nombre` | varchar(50) | Primer nombre del empleado. Requerido. |
| `segundo_nombre` | varchar(50) | Segundo nombre del empleado. Opcional. |
| `primer_apellido` | varchar(50) | Primer apellido del empleado. Requerido. |
| `segundo_apellido` | varchar(50) | Segundo apellido del empleado. Opcional. |
| `tipo_documento` | varchar(20) | Tipo de documento de identidad (CI o Pasaporte). Default: CI. |
| `numero_documento` | varchar(20) | Número del documento de identidad. Único, solo números, 6-20 dígitos. Requerido. |
| `fecha_nacimiento` | date | Fecha de nacimiento del empleado. |
| `direccion` | varchar(200) | Dirección de residencia del empleado. |
| `celular` | varchar(20) | Número de teléfono celular. Validado con regex. Requerido. |
| `tipo_personal` | varchar(20) | Tipo de empleado (Odontólogo, Asistente, Administrador, Gerente). Requerido. |
| `especialidad` | varchar(100) | Especialidad médica (principalmente para odontólogos). |
| `numero_licencia` | varchar(50) | Número de licencia profesional (para odontólogos). |
| `fecha_contratacion` | date | Fecha de ingreso del empleado a la clínica. Default: CURRENT_DATE. Requerido. |
| `estado_laboral` | varchar(20) | Estado actual del empleado (activo o inactivo). Default: activo. |
| `fecha_creacion` | timestamptz | Fecha y hora de creación del registro. Default: CURRENT_TIMESTAMP. |
| `fecha_actualizacion` | timestamptz | Fecha y hora de última actualización. Se actualiza automáticamente. |

**Relaciones:**
- Depende de: `usuarios` (muchos empleados → 1 usuario, aunque en práctica es 1:1)
- Es referenciado por: `consultas` (1 odontólogo → muchas consultas), `intervenciones` (1 odontólogo → muchas intervenciones)

---

## 4. TABLA: `servicios`

**Descripción:**
Catálogo de servicios odontológicos que ofrece la clínica. Cada servicio tiene un código único auto-generado (SER001, SER002...), categoría (Preventiva, Restaurativa, Endodoncia, etc.), y precio base en dólares. El campo `alcance_servicio` indica si el servicio se aplica a una superficie específica del diente, al diente completo, o a toda la boca. El campo `condicion_resultante` se usa para actualizar automáticamente el odontograma después de aplicar el servicio (ej: "obturacion" después de tratar una caries).

### Columnas:

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | uuid | Identificador único del servicio (Primary Key). Generado automáticamente. |
| `codigo` | varchar(20) | Código único del servicio (ej: SER001, SER002). Solo mayúsculas y números. Requerido. |
| `nombre` | varchar(100) | Nombre descriptivo del servicio (ej: Obturación Simple). Requerido. |
| `descripcion` | text | Descripción detallada del servicio y lo que incluye. |
| `categoria` | varchar(50) | Categoría del servicio (Preventiva, Restaurativa, Endodoncia, Cirugía Oral, etc.). Requerido. |
| `precio_base_usd` | numeric(10,2) | Precio base del servicio en dólares USD. Debe ser mayor a 0. Requerido. |
| `activo` | boolean | Indica si el servicio está disponible en el catálogo. Default: true. |
| `fecha_creacion` | timestamptz | Fecha y hora de creación del servicio. Default: CURRENT_TIMESTAMP. |
| `alcance_servicio` | varchar(25) | Alcance de aplicación: superficie_especifica, diente_completo, o boca_completa. Requerido. |
| `condicion_resultante` | varchar(50) | Condición resultante en el odontograma después de aplicar el servicio (ej: obturacion, corona, implante). NULL si no modifica el odontograma. |

**Relaciones:**
- Es referenciado por: `intervenciones_servicios` (1 servicio → muchas aplicaciones en intervenciones)

---

## 5. TABLA: `pacientes`

**Descripción:**
Almacena la información completa de los pacientes de la clínica. Cada paciente recibe un número de historia clínica único auto-generado (HC000001, HC000002...). Incluye datos personales, de contacto, información médica relevante (alergias, medicamentos actuales, condiciones médicas) almacenada en arrays, y datos del contacto de emergencia en formato JSON. Al crear un paciente nuevo, automáticamente se genera su odontograma inicial con 160 condiciones "sano" (32 dientes × 5 superficies) mediante un trigger de base de datos.

### Columnas:

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | uuid | Identificador único del paciente (Primary Key). Generado automáticamente. |
| `numero_historia` | varchar(20) | Número de historia clínica único (ej: HC000001). Auto-generado por trigger. Requerido. |
| `primer_nombre` | varchar(50) | Primer nombre del paciente. Requerido. |
| `segundo_nombre` | varchar(50) | Segundo nombre del paciente. Opcional. |
| `primer_apellido` | varchar(50) | Primer apellido del paciente. Requerido. |
| `segundo_apellido` | varchar(50) | Segundo apellido del paciente. Opcional. |
| `tipo_documento` | varchar(20) | Tipo de documento de identidad (CI o Pasaporte). Default: CI. |
| `numero_documento` | varchar(20) | Número del documento de identidad. Único, solo números, 6-20 dígitos. Requerido. |
| `fecha_nacimiento` | date | Fecha de nacimiento del paciente. Se usa para calcular edad. |
| `genero` | varchar(10) | Género del paciente (masculino, femenino, otro). |
| `celular_1` | varchar(20) | Número de teléfono celular principal. Validado con regex. |
| `celular_2` | varchar(20) | Número de teléfono celular secundario (opcional). Validado con regex. |
| `email` | varchar(100) | Correo electrónico del paciente. Validado con regex. Opcional. |
| `direccion` | text | Dirección de residencia del paciente. |
| `ciudad` | varchar(100) | Ciudad de residencia. Útil para estadísticas geográficas. |
| `contacto_emergencia` | jsonb | Datos del contacto de emergencia en formato JSON (nombre, relación, teléfono, dirección). |
| `alergias` | text[] | Array de alergias conocidas del paciente. Información médica crítica. |
| `medicamentos_actuales` | text[] | Array de medicamentos que el paciente toma actualmente. |
| `condiciones_medicas` | text[] | Array de condiciones médicas pre-existentes del paciente. |
| `fecha_registro` | timestamptz | Fecha y hora de registro del paciente en el sistema. Default: CURRENT_TIMESTAMP. |
| `fecha_actualizacion` | timestamptz | Fecha y hora de última actualización. Se actualiza automáticamente. |
| `activo` | boolean | Indica si el paciente está activo en el sistema. Default: true. |

**Relaciones:**
- Es referenciado por: `consultas` (1 paciente → muchas consultas), `condiciones_diente` (1 paciente → muchas condiciones dentales), `pagos` (1 paciente → muchos pagos)

---

## 6. TABLA: `consultas`

**Descripción:**
Registra las consultas de los pacientes en el sistema. A diferencia de sistemas de citas tradicionales, este funciona por orden de llegada: cuando un paciente llega a la clínica, el administrador crea una consulta y la asigna a la cola de un odontólogo específico mediante `orden_cola_odontologo`. Cada consulta recibe un número único auto-generado por día (YYYYMMDD001, YYYYMMDD002...). Una consulta puede tener múltiples intervenciones realizadas por diferentes odontólogos. El campo `tipo_consulta` se usa para mostrar badges visuales (urgencia, emergencia, etc.).

### Columnas:

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | uuid | Identificador único de la consulta (Primary Key). Generado automáticamente. |
| `numero_consulta` | varchar(20) | Número único de consulta por día (ej: 20251104001). Auto-generado. Requerido. |
| `paciente_id` | uuid | Referencia al paciente (Foreign Key → pacientes.id). Requerido. |
| `primer_odontologo_id` | uuid | Referencia al odontólogo asignado (Foreign Key → personal.id). Requerido. |
| `fecha_llegada` | timestamptz | Fecha y hora de llegada del paciente. Default: CURRENT_TIMESTAMP. Requerido. |
| `orden_cola_odontologo` | integer | Número de orden en la cola del odontólogo específico. Determina prioridad de atención. |
| `estado` | varchar(20) | Estado actual: en_espera, en_atencion, entre_odontologos, completada, cancelada. Default: en_espera. |
| `tipo_consulta` | varchar(30) | Tipo de consulta: general, control, urgencia, emergencia. Se muestra con badge. Default: general. |
| `motivo_consulta` | text | Motivo inicial por el cual el paciente solicita la consulta. Se muestra al odontólogo. |
| `observaciones` | text | Observaciones adicionales sobre la consulta. |
| `fecha_creacion` | timestamptz | Fecha y hora de creación del registro. Default: CURRENT_TIMESTAMP. |
| `fecha_actualizacion` | timestamptz | Fecha y hora de última actualización. Se actualiza automáticamente. |

**Relaciones:**
- Depende de: `pacientes` (muchas consultas → 1 paciente), `personal` (muchas consultas → 1 odontólogo)
- Es referenciado por: `intervenciones` (1 consulta → muchas intervenciones), `pagos` (1 consulta → muchos pagos)

---

## 7. TABLA: `intervenciones`

**Descripción:**
Registra cada tratamiento o procedimiento odontológico realizado dentro de una consulta. Una consulta puede tener múltiples intervenciones, incluso realizadas por diferentes odontólogos (derivaciones). Cada intervención está asociada a uno o más servicios del catálogo (relación con `intervenciones_servicios`). El campo `procedimiento_realizado` describe lo que se hizo, y los totales en bolívares y dólares se calculan automáticamente desde los servicios aplicados. Las intervenciones modifican el odontograma del paciente mediante la tabla `condiciones_diente`.

### Columnas:

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | uuid | Identificador único de la intervención (Primary Key). Generado automáticamente. |
| `consulta_id` | uuid | Referencia a la consulta (Foreign Key → consultas.id). Requerido. |
| `odontologo_id` | uuid | Referencia al odontólogo que realiza la intervención (Foreign Key → personal.id). Requerido. |
| `hora_inicio` | timestamptz | Fecha y hora de inicio de la intervención. Default: CURRENT_TIMESTAMP. Requerido. |
| `procedimiento_realizado` | text | Descripción detallada del procedimiento realizado durante la intervención. Requerido. |
| `total_bs` | numeric(10,2) | Costo total de la intervención en bolívares. Calculado desde servicios. Default: 0. |
| `total_usd` | numeric(10,2) | Costo total de la intervención en dólares. Calculado desde servicios. Default: 0. |
| `estado` | varchar(20) | Estado de la intervención: en_progreso, completada, suspendida. Default: completada. |
| `fecha_registro` | timestamptz | Fecha y hora de registro de la intervención. Default: CURRENT_TIMESTAMP. |

**Relaciones:**
- Depende de: `consultas` (muchas intervenciones → 1 consulta), `personal` (muchas intervenciones → 1 odontólogo)
- Es referenciado por: `intervenciones_servicios` (1 intervención → muchos servicios), `condiciones_diente` (1 intervención → muchas condiciones modificadas)

---

## 8. TABLA: `intervenciones_servicios`

**Descripción:**
Tabla de relación muchos-a-muchos entre intervenciones y servicios. Registra cada servicio aplicado dentro de una intervención específica, con su precio en el momento de la aplicación (en bolívares y dólares), el diente y superficie específica donde se aplicó. Los campos `diente_numero` (numeración FDI: 11-48) y `superficie` (oclusal, mesial, distal, vestibular, lingual) permiten especificar exactamente dónde se realizó el tratamiento. Estos datos se usan para actualizar el odontograma del paciente automáticamente.

### Columnas:

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | uuid | Identificador único del registro (Primary Key). Generado automáticamente. |
| `intervencion_id` | uuid | Referencia a la intervención (Foreign Key → intervenciones.id). Requerido. |
| `servicio_id` | uuid | Referencia al servicio aplicado (Foreign Key → servicios.id). Requerido. |
| `precio_unitario_bs` | numeric(10,2) | Precio unitario del servicio en bolívares al momento de la aplicación. Requerido. |
| `precio_unitario_usd` | numeric(10,2) | Precio unitario del servicio en dólares al momento de la aplicación. Requerido. |
| `precio_total_bs` | numeric(10,2) | Precio total en bolívares (igual al unitario, cantidad siempre es 1). Requerido. |
| `precio_total_usd` | numeric(10,2) | Precio total en dólares (igual al unitario, cantidad siempre es 1). Requerido. |
| `diente_numero` | integer | Número FDI del diente donde se aplicó el servicio (11-48). NULL para servicios de boca completa. |
| `superficie` | varchar(20) | Superficie específica del diente: oclusal, mesial, distal, vestibular, lingual. NULL para servicios de diente completo o boca completa. |
| `fecha_registro` | timestamptz | Fecha y hora de registro. Default: CURRENT_TIMESTAMP. |

**Relaciones:**
- Depende de: `intervenciones` (muchos servicios → 1 intervención), `servicios` (muchas aplicaciones → 1 servicio del catálogo)

---

## 9. TABLA: `condiciones_diente`

**Descripción:**
Almacena el odontograma completo del paciente utilizando la numeración FDI estándar (32 dientes permanentes: 11-48). Cada registro representa la condición de una superficie específica de un diente (oclusal, mesial, distal, vestibular, lingual). El sistema mantiene historial completo mediante el campo `activo`: las condiciones activas (activo=true) representan el estado actual, y las inactivas (activo=false) son el historial de cambios. Al crear un paciente nuevo, un trigger SQL crea automáticamente 160 registros con condición "sano" (32 dientes × 5 superficies). El campo `color_hex` se usa para la visualización gráfica del odontograma en el frontend.

### Columnas:

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | uuid | Identificador único del registro (Primary Key). Generado automáticamente. |
| `paciente_id` | uuid | Referencia al paciente (Foreign Key → pacientes.id). Requerido. |
| `diente_numero` | integer | Número FDI del diente (11-48 para permanentes). Requerido. |
| `superficie` | varchar(20) | Superficie del diente: oclusal, mesial, distal, vestibular, lingual, completo. Requerido. |
| `tipo_condicion` | varchar(50) | Condición actual: sano, caries, obturacion, corona, puente, implante, ausente, endodoncia, protesis, fractura, etc. Requerido. |
| `intervencion_id` | uuid | Referencia a la intervención que generó este cambio (Foreign Key → intervenciones.id). NULL para condiciones iniciales. |
| `fecha_registro` | timestamptz | Fecha y hora del registro de la condición. Default: CURRENT_TIMESTAMP. Requerido. |
| `activo` | boolean | Indica si es la condición actual (true) o histórica (false). Solo una condición activa por diente-superficie. Requerido. |
| `color_hex` | varchar(7) | Color hexadecimal para visualización en el odontograma (#90EE90 = verde = sano). Default: #90EE90. |

**Relaciones:**
- Depende de: `pacientes` (muchas condiciones → 1 paciente), `intervenciones` (muchas condiciones → 1 intervención)

**Constraints especiales:**
- Unique constraint: Solo puede haber una condición activa por combinación (paciente_id, diente_numero, superficie, activo=true)

---

## 10. TABLA: `pagos`

**Descripción:**
Registra todos los pagos realizados por los pacientes. Cada pago recibe un número de recibo único auto-generado por mes (REC202501001, REC202501002...). Soporta pagos mixtos en bolívares y dólares simultáneamente, con registro de la tasa de cambio. Permite pagos parciales automáticos: el sistema calcula el saldo pendiente comparando monto total vs monto pagado. Los métodos de pago se almacenan en formato JSON array permitiendo múltiples métodos en un solo pago (ej: parte efectivo, parte tarjeta). Se pueden aplicar descuentos con justificación obligatoria en `motivo_descuento`. Cada pago está vinculado al usuario que lo procesó para trazabilidad.

### Columnas:

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | uuid | Identificador único del pago (Primary Key). Generado automáticamente. |
| `numero_recibo` | varchar(20) | Número único de recibo (ej: REC202501001). Auto-generado por trigger. Requerido. |
| `consulta_id` | uuid | Referencia a la consulta asociada (Foreign Key → consultas.id). Puede ser NULL para pagos sin consulta. |
| `paciente_id` | uuid | Referencia al paciente (Foreign Key → pacientes.id). Requerido. |
| `fecha_pago` | timestamptz | Fecha y hora del pago. Default: CURRENT_TIMESTAMP. |
| `monto_total_bs` | numeric(10,2) | Monto total a pagar en bolívares. Default: 0. |
| `monto_total_usd` | numeric(10,2) | Monto total a pagar en dólares. Default: 0. |
| `monto_pagado_bs` | numeric(10,2) | Monto efectivamente pagado en bolívares. Default: 0. |
| `monto_pagado_usd` | numeric(10,2) | Monto efectivamente pagado en dólares. Default: 0. |
| `saldo_pendiente_bs` | numeric(10,2) | Saldo que queda por pagar en bolívares. Calculado automáticamente. Default: 0. |
| `saldo_pendiente_usd` | numeric(10,2) | Saldo que queda por pagar en dólares. Calculado automáticamente. Default: 0. |
| `tasa_cambio_bs_usd` | numeric(10,4) | Tasa de cambio aplicada al momento del pago (cuántos bolívares por 1 dólar). |
| `metodos_pago` | jsonb | Array JSON de métodos de pago utilizados (efectivo, tarjeta, transferencia, etc.). Default: []. |
| `concepto` | text | Descripción del concepto del pago. Requerido. |
| `descuento_usd` | numeric(10,2) | Monto del descuento aplicado en dólares. Default: 0. |
| `motivo_descuento` | text | Justificación del descuento aplicado. Requerido si hay descuento. |
| `estado_pago` | varchar(20) | Estado del pago: pendiente, completado, parcial, anulado, reembolsado. Default: completado. |
| `procesado_por` | uuid | Referencia al usuario que procesó el pago (Foreign Key → usuarios.id). Requerido. |

**Relaciones:**
- Depende de: `pacientes` (muchos pagos → 1 paciente), `consultas` (muchos pagos → 1 consulta), `usuarios` (muchos pagos → 1 usuario procesador)

**Triggers:**
- `trigger_calcular_saldos_pago`: Calcula automáticamente saldos pendientes
- `trigger_generar_numero_recibo`: Genera número de recibo único por mes

---


## Diagrama PlantUML
---
erDiagram
    %% === RELACIONES (primero) ===
    ROLES ||--o{ USUARIOS : "tiene"
    USUARIOS }o--o| PERSONAL : "vinculado a"
    USUARIOS }o--o{ PAGOS : "procesa"

    PERSONAL }o--o{ CONSULTAS : "primer odontólogo"
    PERSONAL }o--o{ INTERVENCIONES : "realiza"

    PACIENTES ||--o{ CONSULTAS : "tiene"
    PACIENTES ||--o{ PAGOS : "realiza"
    PACIENTES ||--o{ CONDICIONES_DIENTE : "posee"

    CONSULTAS ||--o{ INTERVENCIONES : "contiene"
    CONSULTAS }o--o| PAGOS : "genera"

    INTERVENCIONES ||--o{ INTERVENCIONES_SERVICIOS : "incluye"
    INTERVENCIONES }o--o| CONDICIONES_DIENTE : "modifica"

    SERVICIOS ||--o{ INTERVENCIONES_SERVICIOS : "usado en"

    %% === ENTIDADES (después) ===
    ROLES {
        uuid id PK
        string nombre UK
        text descripcion
        boolean activo
        date fecha_creacion
        date fecha_actualizacion
    }

    USUARIOS {
        uuid id PK
        string email UK
        uuid rol_id FK
        boolean activo
        date fecha_creacion
        date fecha_actualizacion
        uuid auth_user_id UK
    }

    PERSONAL {
        uuid id PK
        uuid usuario_id FK
        string primer_nombre
        string primer_apellido
        string numero_documento UK
        string tipo_personal
        string celular
        string estado_laboral
        date fecha_contratacion
    }

    SERVICIOS {
        uuid id PK
        string codigo UK
        string nombre
        string categoria
        number precio_base_usd
        boolean activo
        string alcance_servicio
        string condicion_resultante
    }

    PACIENTES {
        uuid id PK
        string numero_historia UK
        string primer_nombre
        string primer_apellido
        string numero_documento UK
        date fecha_nacimiento
        string genero
        string email
        boolean activo
    }

    CONSULTAS {
        uuid id PK
        string numero_consulta UK
        uuid paciente_id FK
        uuid primer_odontologo_id FK
        date fecha_llegada
        string estado
        string tipo_consulta
        text motivo_consulta
    }

    INTERVENCIONES {
        uuid id PK
        uuid consulta_id FK
        uuid odontologo_id FK
        date hora_inicio
        text procedimiento_realizado
        number total_bs
        number total_usd
        string estado
    }

    INTERVENCIONES_SERVICIOS {
        uuid id PK
        uuid intervencion_id FK
        uuid servicio_id FK
        number precio_total_bs
        number precio_total_usd
        int diente_numero
        string superficie
    }

    CONDICIONES_DIENTE {
        uuid id PK
        uuid paciente_id FK
        int diente_numero
        string superficie
        string tipo_condicion
        uuid intervencion_id FK
        boolean activo
        string color_hex
    }

    PAGOS {
        uuid id PK
        string numero_recibo UK
        uuid consulta_id FK
        uuid paciente_id FK
        uuid procesado_por FK
        date fecha_pago
        number monto_total_bs
        number monto_total_usd
        string estado_pago
        number descuento_usd
    }

---

**Generado:** 2025-11-04
**Para:** Equipo de Desarrollo
**Sistema:** Gestión Odontológica - Universidad de Oriente
