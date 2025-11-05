# 📊 DIAGRAMA ER - BASE DE DATOS SIMPLIFICADA
## Sistema de Gestión Odontológica - Versión Optimizada

**Fecha:** 2025-11-04
**Tablas:** 10 (de 14 originales)
**Reducción:** 99 columnas eliminadas (~45%)

---

## 🗂️ DIAGRAMA MERMAID

```mermaid
erDiagram
    roles ||--o{ usuarios : "define"
    usuarios ||--o{ personal : "vincula"
    usuarios ||--o{ pagos : "procesa"

    personal ||--o{ consultas : "atiende"
    personal ||--o{ intervenciones : "realiza"

    pacientes ||--o{ consultas : "tiene"
    pacientes ||--o{ pagos : "realiza"
    pacientes ||--o{ condiciones_diente : "posee"

    consultas ||--o{ intervenciones : "contiene"
    consultas ||--o{ pagos : "genera"

    intervenciones ||--o{ intervenciones_servicios : "incluye"
    intervenciones ||--o{ condiciones_diente : "modifica"

    servicios ||--o{ intervenciones_servicios : "usado_en"

    roles {
        uuid id PK
        varchar nombre UK
        text descripcion
        boolean activo
        timestamptz fecha_creacion
        timestamptz fecha_actualizacion
    }

    usuarios {
        uuid id PK
        varchar email UK
        uuid rol_id FK
        boolean activo
        timestamptz fecha_creacion
        timestamptz fecha_actualizacion
        uuid auth_user_id UK
    }

    personal {
        uuid id PK
        uuid usuario_id FK_UK
        varchar primer_nombre
        varchar segundo_nombre
        varchar primer_apellido
        varchar segundo_apellido
        varchar tipo_documento
        varchar numero_documento UK
        date fecha_nacimiento
        varchar direccion
        varchar celular
        varchar tipo_personal
        varchar especialidad
        varchar numero_licencia
        date fecha_contratacion
        varchar estado_laboral
        timestamptz fecha_creacion
        timestamptz fecha_actualizacion
    }

    servicios {
        uuid id PK
        varchar codigo UK
        varchar nombre
        text descripcion
        varchar categoria
        numeric precio_base_usd
        boolean activo
        timestamptz fecha_creacion
        varchar alcance_servicio
        varchar condicion_resultante
    }

    pacientes {
        uuid id PK
        varchar numero_historia UK
        varchar primer_nombre
        varchar segundo_nombre
        varchar primer_apellido
        varchar segundo_apellido
        varchar tipo_documento
        varchar numero_documento UK
        date fecha_nacimiento
        varchar genero
        varchar celular_1
        varchar celular_2
        varchar email
        varchar direccion
        varchar ciudad
        jsonb contacto_emergencia
        array alergias
        array medicamentos_actuales
        array condiciones_medicas
        timestamptz fecha_registro
        timestamptz fecha_actualizacion
        boolean activo
    }

    consultas {
        uuid id PK
        varchar numero_consulta UK
        uuid paciente_id FK
        uuid primer_odontologo_id FK
        timestamptz fecha_llegada
        integer orden_cola_odontologo
        varchar estado
        varchar tipo_consulta
        text motivo_consulta
        text observaciones
        timestamptz fecha_creacion
        timestamptz fecha_actualizacion
    }

    intervenciones {
        uuid id PK
        uuid consulta_id FK
        uuid odontologo_id FK
        timestamptz hora_inicio
        text procedimiento_realizado
        numeric total_bs
        numeric total_usd
        varchar estado
        timestamptz fecha_registro
    }

    intervenciones_servicios {
        uuid id PK
        uuid intervencion_id FK
        uuid servicio_id FK
        numeric precio_unitario_bs
        numeric precio_unitario_usd
        numeric precio_total_bs
        numeric precio_total_usd
        integer diente_numero
        varchar superficie
        timestamptz fecha_registro
    }

    condiciones_diente {
        uuid id PK
        uuid paciente_id FK
        integer diente_numero
        varchar superficie
        varchar tipo_condicion
        uuid intervencion_id FK
        timestamptz fecha_registro
        boolean activo
        varchar color_hex
    }

    pagos {
        uuid id PK
        varchar numero_recibo UK
        uuid consulta_id FK
        uuid paciente_id FK
        timestamptz fecha_pago
        numeric monto_total_bs
        numeric monto_total_usd
        numeric monto_pagado_bs
        numeric monto_pagado_usd
        numeric saldo_pendiente_bs
        numeric saldo_pendiente_usd
        numeric tasa_cambio_bs_usd
        jsonb metodos_pago
        text concepto
        numeric descuento_usd
        text motivo_descuento
        varchar estado_pago
        uuid procesado_por FK
    }
```

---

## 📋 RELACIONES PRINCIPALES

### **1. AUTENTICACIÓN Y ROLES**
```
roles (1) ──→ (N) usuarios
usuarios (1) ──→ (1) personal
```

### **2. PACIENTES Y CONSULTAS**
```
pacientes (1) ──→ (N) consultas
personal (1) ──→ (N) consultas (como odontólogo)
```

### **3. CONSULTAS E INTERVENCIONES**
```
consultas (1) ──→ (N) intervenciones
personal (1) ──→ (N) intervenciones (como odontólogo)
```

### **4. INTERVENCIONES Y SERVICIOS**
```
intervenciones (1) ──→ (N) intervenciones_servicios
servicios (1) ──→ (N) intervenciones_servicios
```

### **5. ODONTOGRAMA**
```
pacientes (1) ──→ (N) condiciones_diente
intervenciones (1) ──→ (N) condiciones_diente
```

### **6. PAGOS**
```
pacientes (1) ──→ (N) pagos
consultas (1) ──→ (N) pagos
usuarios (1) ──→ (N) pagos (como procesado_por)
```

---

## 🎯 DIAGRAMA ASCII SIMPLIFICADO

```
┌─────────────┐
│   roles     │
│  (6 cols)   │
└──────┬──────┘
       │ 1:N
       ▼
┌─────────────┐         ┌──────────────┐
│  usuarios   │  1:1    │   personal   │
│  (7 cols)   │◄────────┤  (18 cols)   │
└──────┬──────┘         └──────┬───────┘
       │                       │
       │ 1:N                   │ 1:N (odontologo)
       │                       │
       │                ┌──────▼──────┐      ┌──────────────┐
       │                │  consultas  │ 1:N  │ pacientes    │
       │                │  (12 cols)  │◄─────┤  (22 cols)   │
       │                └──────┬──────┘      └──────┬───────┘
       │                       │                    │
       │                       │ 1:N                │ 1:N
       │                       │                    │
       │                ┌──────▼─────────┐          │
       │                │ intervenciones │          │
       │                │   (9 cols)     │          │
       │                └──────┬─────────┘          │
       │                       │                    │
       │                       │ 1:N                │ 1:N
       │              ┌────────┼────────┐           │
       │              │                 │           │
       │    ┌─────────▼────────┐  ┌────▼────────────▼──┐
       │    │ intervenciones_  │  │ condiciones_diente │
       │    │    servicios     │  │     (9 cols)       │
       │    │   (10 cols)      │  └────────────────────┘
       │    └─────────┬────────┘
       │              │
       │              │ N:1
       │              │
       │    ┌─────────▼────────┐
       │    │   servicios      │
       │    │   (10 cols)      │
       │    └──────────────────┘
       │
       │ 1:N (procesado_por)
       │
       ▼
┌──────────────┐
│    pagos     │◄───── consultas (1:N)
│  (18 cols)   │
└──────┬───────┘
       ▲
       │ N:1
       │
   pacientes
```

---

## 📊 RESUMEN DE CARDINALIDADES

| Relación | Cardinalidad | Descripción |
|----------|-------------|-------------|
| roles → usuarios | 1:N | Un rol puede tener muchos usuarios |
| usuarios → personal | 1:1 | Un usuario puede ser un empleado |
| usuarios → pagos | 1:N | Un usuario procesa muchos pagos |
| personal → consultas | 1:N | Un odontólogo atiende muchas consultas |
| personal → intervenciones | 1:N | Un odontólogo realiza muchas intervenciones |
| pacientes → consultas | 1:N | Un paciente tiene muchas consultas |
| pacientes → pagos | 1:N | Un paciente realiza muchos pagos |
| pacientes → condiciones_diente | 1:N | Un paciente tiene muchas condiciones dentales |
| consultas → intervenciones | 1:N | Una consulta tiene muchas intervenciones |
| consultas → pagos | 1:N | Una consulta genera muchos pagos |
| intervenciones → intervenciones_servicios | 1:N | Una intervención incluye muchos servicios |
| intervenciones → condiciones_diente | 1:N | Una intervención modifica muchas condiciones |
| servicios → intervenciones_servicios | 1:N | Un servicio se usa en muchas intervenciones |

---

## 🔑 CLAVES Y CONSTRAINTS

### **Primary Keys (PK):**
- Todas las tablas usan `uuid` como PK
- Generación automática con `uuid_generate_v4()` o `gen_random_uuid()`

### **Unique Keys (UK):**
- `usuarios.email`
- `usuarios.auth_user_id`
- `personal.numero_documento`
- `personal.usuario_id`
- `servicios.codigo`
- `pacientes.numero_historia`
- `pacientes.numero_documento`
- `consultas.numero_consulta`
- `pagos.numero_recibo`

### **Foreign Keys (FK):**
- **13 relaciones totales**
- Todas con validación de integridad referencial
- Algunas con `ON DELETE CASCADE`

### **Check Constraints:**
- Validación de emails, documentos, teléfonos
- Estados controlados (enum-like)
- Montos siempre positivos

---

## 🎨 LEYENDA

- **PK** = Primary Key (Clave Primaria)
- **FK** = Foreign Key (Clave Foránea)
- **UK** = Unique Key (Clave Única)
- **1:1** = Relación uno a uno
- **1:N** = Relación uno a muchos
- **N:1** = Relación muchos a uno

---

## 📈 ESTADÍSTICAS FINALES

| Métrica | Valor |
|---------|-------|
| **Total de tablas** | 10 |
| **Total de columnas** | 121 |
| **Total de relaciones (FK)** | 13 |
| **Total de índices** | ~50+ |
| **Total de triggers** | 19 |
| **Total de funciones** | 46 |

---

## ✅ VALIDACIÓN POST-MIGRACIÓN

- ✅ Todas las relaciones mantienen integridad referencial
- ✅ No hay FK huérfanas
- ✅ Todas las tablas tienen PK
- ✅ Nomenclatura consistente en español
- ✅ Timestamps automáticos funcionando
- ✅ Auto-numeración funcionando (HC, consultas, recibos)
- ✅ Triggers operativos

---

**Última actualización:** 2025-11-04
**Versión:** Post-Simplificación V2.0
**Estado:** ✅ Base de datos optimizada y funcional
