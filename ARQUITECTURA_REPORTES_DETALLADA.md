# 📊 ARQUITECTURA DETALLADA - SISTEMA DE REPORTES
## Diseño Visual y Técnico Completo

**Fecha:** 2025-11-07
**Versión:** 1.0
**Estado:** Planificación detallada

---

## 🎯 ÍNDICE

1. [Diagrama de Arquitectura General](#arquitectura-general)
2. [Reporte Gerente - Layout Completo](#reporte-gerente)
3. [Reporte Odontólogo - Layout Completo](#reporte-odontologo)
4. [Reporte Administrador - Layout Completo](#reporte-administrador)
5. [Arquitectura de Servicios](#arquitectura-servicios)
6. [Flujo de Datos](#flujo-datos)
7. [Componentes Nuevos a Crear](#componentes-nuevos)

---

## 🏗️ ARQUITECTURA GENERAL {#arquitectura-general}

```
┌─────────────────────────────────────────────────────────────┐
│                    REPORTES PAGE                             │
│                  (reportes_page.py)                          │
└─────────────────────────────────────────────────────────────┘
                           │
                           │ AppState.rol_usuario
                           │
        ┌──────────────────┴──────────────────┐
        │                  │                   │
        ▼                  ▼                   ▼
┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│   GERENTE    │   │  ODONTÓLOGO  │   │    ADMIN     │
│   REPORTES   │   │   REPORTES   │   │   REPORTES   │
└──────┬───────┘   └──────┬───────┘   └──────┬───────┘
       │                  │                   │
       │                  │                   │
       ▼                  ▼                   ▼
┌──────────────────────────────────────────────────────┐
│          REPORTES SERVICE                             │
│        (reportes_service.py)                          │
│                                                       │
│  ├── get_distribucion_pagos_usd_bs()                 │
│  ├── get_ranking_servicios()                         │
│  ├── get_ranking_odontologos()                       │
│  ├── get_ingresos_odontologo_usd_bs()                │
│  ├── get_intervenciones_odontologo()                 │
│  ├── get_consultas_por_estado()                      │
│  └── get_pagos_pendientes()                          │
└───────────────────┬──────────────────────────────────┘
                    │
                    │ Supabase Client
                    │
                    ▼
┌──────────────────────────────────────────────────────┐
│              BASE DE DATOS SUPABASE                   │
│                                                       │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐          │
│  │  pago    │  │historia_ │  │interven- │          │
│  │          │  │ medica   │  │  cion    │          │
│  └──────────┘  └──────────┘  └──────────┘          │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐          │
│  │ consulta │  │ servicio │  │ personal │          │
│  └──────────┘  └──────────┘  └──────────┘          │
│  ┌──────────┐  ┌──────────┐                        │
│  │ paciente │  │  diente  │                        │
│  └──────────┘  └──────────┘                        │
└──────────────────────────────────────────────────────┘
```

---

## 👔 REPORTE GERENTE - LAYOUT COMPLETO {#reporte-gerente}

### **📐 Wireframe Visual:**

```
╔════════════════════════════════════════════════════════════════════╗
║  📊 REPORTES Y ANÁLISIS                                            ║
║  Estadísticas y métricas del sistema                              ║
║                                                                    ║
║  [Filtros: 📅 Este Mes ▼] [🔄 Actualizar] [📥 Exportar PDF]      ║
╚════════════════════════════════════════════════════════════════════╝

┌────────────────────────────────────────────────────────────────────┐
│ SECCIÓN 1: CARDS DE ESTADÍSTICAS PRINCIPALES                       │
└────────────────────────────────────────────────────────────────────┘

┌────────────┐  ┌────────────┐  ┌────────────┐  ┌────────────┐
│ 💰 INGRESOS│  │ 📊 PROMEDIO│  │ 🦷 SERVICIOS│ │ ✅ TASA    │
│  DEL MES   │  │ POR CONSULT│  │  APLICADOS │  │ CONVERSIÓN │
│            │  │            │  │            │  │            │
│ $12,450 USD│  │  $85.50    │  │    287     │  │    94%     │
│ ↑ +15%     │  │  ↑ +8%     │  │  ↑ +12%    │  │  ↑ +3%     │
└────────────┘  └────────────┘  └────────────┘  └────────────┘

┌────────────────────────────────────────────────────────────────────┐
│ SECCIÓN 2: DISTRIBUCIÓN DE PAGOS USD vs BS                         │
└────────────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────┐
│ 💵 Distribución de Ingresos por Moneda                         │
│ ─────────────────────────────────────────────────────────────  │
│                                                                │
│         [Filtro: 📅 Últimos 30 días ▼]                        │
│                                                                │
│              ╭─────────────╮                                   │
│              │     35%     │                                   │
│          ╭───│    USD      │───╮                               │
│          │   │  $4,357.75  │   │                               │
│          │   ╰─────────────╯   │    ┌─────────────────┐       │
│          │                     │    │  USD:  $4,357.75│       │
│      ╭───┴───╮             ╭───┴──╮ │  BS:   $8,092.25│       │
│      │  65%  │             │      │ │  TOTAL:$12,450  │       │
│      │  BS   │             │      │ └─────────────────┘       │
│      ╰───────╯             ╰──────╯                            │
│                                                                │
└───────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────┐
│ SECCIÓN 3: GRID CON 2 COLUMNAS                                     │
└────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────┐  ┌──────────────────────────────┐
│ 🏆 RANKING DE SERVICIOS      │  │ 👨‍⚕️ RANKING DE ODONTÓLOGOS   │
│ ──────────────────────────── │  │ ──────────────────────────── │
│                              │  │                              │
│ [Top 10] [Ver todos]         │  │ [Por Consultas▼] [Ingresos] │
│                              │  │                              │
│ 1. 🦷 Limpieza Dental        │  │ 1. 👤 Dr. Juan Pérez        │
│    📊 ████████████ 156 veces │  │    📈 ████ 89 intervenciones │
│    💰 $4,680 generados       │  │    💰 $8,920 generados      │
│                              │  │                                │
│ 2. 🔧 Obturación Simple      │  │                              │
│    📊 ████████ 124 veces     │  │ 2. 👤 Dra. María González   │
│    💰 $3,720 generados       │  │    📈 ███ 76 intervenciones  │
│                              │  │    💰 $7,450 generados      │
│ 3. 🌟 Blanqueamiento         │  │                                 │
│    📊 ██████ 98 veces        │  │                              │
│    💰 $9,800 generados       │  │ 3. 👤 Dr. Carlos Rodríguez  │
│                              │  │    📈 ██ 65 intervenciones   │
│ 4. 👑 Corona Porcelana       │  │    💰 $6,780 generados      │
│    📊 █████ 78 veces         │  │                             │
│    💰 $15,600 generados      │  │                              │
│                              │  │ [Ver más odontólogos...]    │
│ [Ver más servicios...]       │  │                              │
└──────────────────────────────┘  └──────────────────────────────┘

┌────────────────────────────────────────────────────────────────────┐
│ SECCIÓN 4: EVOLUCIÓN TEMPORAL (GRÁFICO DE ÁREA/BARRAS)             │
└────────────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────┐
│ 📈 Métricas de los Últimos 30 Días                             │
│ ─────────────────────────────────────────────────────────────  │
│                                                                │
│ [📊 Área] [📊 Barras]                                          │
│                                                                │
│ ┌─────────┬──────────┬──────────┐                             │
│ │Pacientes│ Ingresos │ Consultas│  ← Tabs con toggle          │
│ └─────────┴──────────┴──────────┘                             │
│                                                                │
│  15 │                        ╱╲                                │
│     │                    ╱╲ ╱  ╲        ╱╲                     │
│  10 │         ╱╲     ╱╲╱  ╲╱    ╲    ╱╲╱  ╲                    │
│     │     ╱╲ ╱  ╲ ╱╲╱              ╲ ╱        ╲                 │
│   5 │ ╱╲╱  ╲╱    ╲╱                  ╱          ╲               │
│     │╱                                          ╲╱             │
│   0 └────────────────────────────────────────────────────     │
│     01  05  10  15  20  25  30  (Días)                        │
│                                                                │
│  💡 Promedio: 8.5 pacientes/día  | 📈 Tendencia: +12%         │
└───────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────┐
│ SECCIÓN 5: ESTADÍSTICAS DE PACIENTES                               │
└────────────────────────────────────────────────────────────────────┘

┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│ 👥 TOTAL     │  │ 🆕 NUEVOS    │  │ 📊 GÉNERO    │
│  PACIENTES   │  │  ESTE MES    │  │  DISTRIBUCIÓN│
│              │  │              │  │              │
│    1,247     │  │     87       │  │  ♂ 48%       │
│  ↑ +5.2%     │  │  ↑ +12%      │  │  ♀ 52%       │
└──────────────┘  └──────────────┘  └──────────────┘

┌────────────────────────────────────────────────────────────────────┐
│ SECCIÓN 6: MÉTODOS DE PAGO MÁS USADOS                              │
└────────────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────┐
│ 💳 Métodos de Pago Más Utilizados                              │
│ ─────────────────────────────────────────────────────────────  │
│                                                                │
│ Efectivo           ████████████████ 45% (234 pagos)           │
│                                                                │
│ Transferencia      ████████████ 32% (167 pagos)               │
│                                                                │
│ Tarjeta Débito     ████████ 18% (94 pagos)                    │
│                                                                │
│ Tarjeta Crédito    ███ 5% (26 pagos)                          │
│                                                                │
└───────────────────────────────────────────────────────────────┘
```

### **🔧 Componentes Usados (Gerente):**

```python
# Sección 1: Cards
- stat_card(title="Ingresos del Mes", value="$12,450", icon="dollar-sign", ...)
- stat_card(title="Promedio por Consulta", value="$85.50", icon="trending-up", ...)
- stat_card(title="Servicios Aplicados", value="287", icon="activity", ...)
- stat_card(title="Tasa de Conversión", value="94%", icon="check-circle", ...)

# Sección 2: Gráfico de Torta
- pie_chart_card(  # NUEVO
    title="Distribución de Ingresos por Moneda",
    data=[{"name": "USD", "value": 4357.75}, {"name": "BS", "value": 8092.25}],
    colors=["#10b981", "#3b82f6"]
  )

# Sección 3: Rankings
- ranking_table(  # NUEVO
    title="Ranking de Servicios",
    columns=["Servicio", "Veces Aplicado", "Ingresos"],
    data=[...],
    show_progress_bar=True
  )
- ranking_table(  # NUEVO
    title="Ranking de Odontólogos",
    columns=["Odontólogo", "Consultas", "Ingresos", "Satisfacción"],
    data=[...],
    avatar_column=0
  )

# Sección 4: Gráfico temporal
- graficas_resume()  # REUTILIZADO de charts.py

# Sección 5: Estadísticas pacientes
- stat_card() x3

# Sección 6: Métodos de pago
- horizontal_bar_chart()  # NUEVO (simple rx.recharts.bar_chart)
```

---

## 🦷 REPORTE ODONTÓLOGO - LAYOUT COMPLETO {#reporte-odontologo}

### **📐 Wireframe Visual:**

```
╔════════════════════════════════════════════════════════════════════╗
║  📊 MIS REPORTES CLÍNICOS                                          ║
║  Dr. Juan Pérez - Estadísticas y análisis de mi trabajo           ║
║                                                                    ║
║  [Filtros: 📅 Este Mes ▼] [🔄 Actualizar] [📥 Exportar PDF]      ║
╚════════════════════════════════════════════════════════════════════╝

┌────────────────────────────────────────────────────────────────────┐
│ SECCIÓN 1: CARDS DE ESTADÍSTICAS PERSONALES                        │
└────────────────────────────────────────────────────────────────────┘

┌────────────┐  ┌────────────┐  ┌────────────┐  ┌────────────┐
│ 💰 INGRESOS│  │ 💵 INGRESOS│  │ 🦷 CONSULTAS│ │ 📊 SERVICIOS│
│  DEL MES   │  │    HOY     │  │    HOY     │  │  APLICADOS │
│            │  │            │  │            │  │            │
│ $8,920 USD │  │  $450 USD  │  │     12     │  │     45     │
│ ↑ +18%     │  │  ↑ +5%     │  │  ↑ +3      │  │  ↑ +8      │
└────────────┘  └────────────┘  └────────────┘  └────────────┘

┌────────────────────────────────────────────────────────────────────┐
│ SECCIÓN 2: DISTRIBUCIÓN DE MIS INGRESOS USD vs BS                  │
└────────────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────┐
│ 💵 Mis Ingresos por Moneda (Este Mes)                          │
│ ─────────────────────────────────────────────────────────────  │
│                                                                │
│              ╭─────────────╮                                   │
│              │     40%     │                                   │
│          ╭───│    USD      │───╮                               │
│          │   │  $3,568.00  │   │                               │
│          │   ╰─────────────╯   │    ┌─────────────────┐       │
│          │                     │    │  USD:  $3,568.00│       │
│      ╭───┴───╮             ╭───┴──╮ │  BS:   $5,352.00│       │
│      │  60%  │             │      │ │  TOTAL:$8,920.00│       │
│      │  BS   │             │      │ └─────────────────┘       │
│      ╰───────╯             ╰──────╯                            │
│                                                                │
└───────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────┐
│ SECCIÓN 3: RANKING DE MIS SERVICIOS MÁS APLICADOS                  │
└────────────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────┐
│ 🏆 Mis Servicios Más Realizados                                │
│ ─────────────────────────────────────────────────────────────  │
│                                                                │
│ [Top 10] [Ver todos]                                           │
│                                                                │
│ 1. 🦷 Limpieza Dental                                          │
│    📊 ████████████████ 67 veces (28%)                          │
│    💰 $2,010 generados | 💵 Promedio: $30/servicio            │
│    📈 Tendencia: +15% vs mes anterior                          │
│                                                                │
│ 2. 🔧 Obturación Simple                                        │
│    📊 ████████████ 52 veces (22%)                              │
│    💰 $1,560 generados | 💵 Promedio: $30/servicio            │
│    📈 Tendencia: +8% vs mes anterior                           │
│                                                                │
│ 3. 👑 Corona Porcelana                                         │
│    📊 ████████ 34 veces (14%)                                  │
│    💰 $6,800 generados | 💵 Promedio: $200/servicio           │
│    📈 Tendencia: +22% vs mes anterior                          │
│                                                                │
│ 4. 🌟 Blanqueamiento Dental                                    │
│    📊 ██████ 28 veces (12%)                                    │
│    💰 $2,800 generados | 💵 Promedio: $100/servicio           │
│    📉 Tendencia: -3% vs mes anterior                           │
│                                                                │
│ 5. 🦴 Endodoncia                                               │
│    📊 █████ 21 veces (9%)                                      │
│    💰 $3,150 generados | 💵 Promedio: $150/servicio           │
│    📈 Tendencia: +12% vs mes anterior                          │
│                                                                │
│ [Ver más servicios...]                                         │
└───────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────┐
│ SECCIÓN 4: EVOLUCIÓN DE MIS INTERVENCIONES EN EL TIEMPO            │
└────────────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────┐
│ 📈 Mis Intervenciones - Últimos 30 Días                        │
│ ─────────────────────────────────────────────────────────────  │
│                                                                │
│ [📊 Área] [📊 Barras]                                          │
│                                                                │
│ ┌──────────┬──────────┐                                        │
│ │ Consultas│ Ingresos │  ← Tabs con toggle                    │
│ └──────────┴──────────┘                                        │
│                                                                │
│  15 │                        ╱╲                                │
│     │                    ╱╲ ╱  ╲        ╱╲                     │
│  10 │         ╱╲     ╱╲╱  ╲╱    ╲    ╱╲╱  ╲                    │
│     │     ╱╲ ╱  ╲ ╱╲╱              ╲ ╱        ╲                 │
│   5 │ ╱╲╱  ╲╱    ╲╱                  ╱          ╲               │
│     │╱                                          ╲╱             │
│   0 └────────────────────────────────────────────────────     │
│     01  05  10  15  20  25  30  (Días)                        │
│                                                                │
│  💡 Promedio: 4.2 consultas/día  | 📈 Tendencia: +18%         │
└───────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────┐
│ SECCIÓN 5: ESTADÍSTICAS DEL ODONTOGRAMA                            │
└────────────────────────────────────────────────────────────────────┘

┌────────────────────┐  ┌────────────────────┐  ┌─────────────────┐
│ 🦷 CONDICIONES     │  │ 📍 DIENTES MÁS     │  │ 📐 SUPERFICIES  │
│    MÁS TRATADAS    │  │   INTERVENIDOS     │  │   MÁS TRATADAS  │
│ ────────────────── │  │ ────────────────── │  │ ─────────────── │
│                    │  │                    │  │                 │
│ Obturación █████   │  │ Diente 16 ████     │  │ Oclusal  █████  │
│        67 (34%)    │  │       18 veces     │  │      45 (38%)   │
│                    │  │                    │  │                 │
│ Caries    ████     │  │ Diente 26 ███      │  │ Mesial   ████   │
│        52 (26%)    │  │       15 veces     │  │      32 (27%)   │
│                    │  │                    │  │                 │
│ Corona    ███      │  │ Diente 36 ███      │  │ Distal   ███    │
│        34 (17%)    │  │       14 veces     │  │      28 (23%)   │
│                    │  │                    │  │                 │
│ Endodoncia █       │  │ Diente 46 ██       │  │ Vestibular ██   │
│        21 (11%)    │  │       12 veces     │  │      18 (15%)   │
└────────────────────┘  └────────────────────┘  └─────────────────┘

┌────────────────────────────────────────────────────────────────────┐
│ SECCIÓN 6: TABLA COMPLETA DE MIS INTERVENCIONES                    │
└────────────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────┐
│ 🔍 Historial Completo de Intervenciones                        │
│ ─────────────────────────────────────────────────────────────  │
│                                                                │
│ [🔍 Buscar paciente/consulta...] [📅 Últimos 30 días ▼]      │
│                                                                │
│ ┌─────────────────────────────────────────────────────────┐   │
│ │Fecha      │Consulta│Paciente    │Procedimiento  │Total │   │
│ ├─────────────────────────────────────────────────────────┤   │
│ │2025-11-07 │C-123   │Juan Pérez  │Limpieza +     │$150 │   │
│ │10:30 AM   │        │            │Obturación     │USD  │ ▼ │
│ ├─────────────────────────────────────────────────────────┤   │
│ │2025-11-07 │C-124   │Ana García  │Corona         │$200 │   │
│ │11:45 AM   │        │            │Porcelana      │USD  │ ▼ │
│ ├─────────────────────────────────────────────────────────┤   │
│ │2025-11-06 │C-118   │Carlos Ruiz │Endodoncia +   │$180 │   │
│ │03:15 PM   │        │            │Obturación     │USD  │ ▼ │
│ ├─────────────────────────────────────────────────────────┤   │
│ │2025-11-06 │C-115   │María López │Limpieza       │$30  │   │
│ │09:00 AM   │        │            │Dental         │USD  │ ▼ │
│ └─────────────────────────────────────────────────────────┘   │
│                                                                │
│ [← Anterior] Página 1 de 12 [Siguiente →]                     │
│                                                                │
│ 💡 Click en ▼ para ver servicios detallados de cada consulta  │
└───────────────────────────────────────────────────────────────┘
```

### **🔧 Componentes Usados (Odontólogo):**

```python
# Sección 1: Cards personales
- stat_card() x4

# Sección 2: Distribución ingresos propios
- pie_chart_card()  # NUEVO

# Sección 3: Ranking servicios propios
- ranking_table_enhanced(  # NUEVO CON MÁS DETALLES
    title="Mis Servicios Más Realizados",
    columns=["Servicio", "Veces", "Ingresos", "Promedio", "Tendencia"],
    data=[...],
    show_progress_bar=True,
    show_trend_arrows=True
  )

# Sección 4: Evolución temporal
- graficas_resume()  # REUTILIZADO

# Sección 5: Stats odontograma
- mini_stat_card() x3  # NUEVO (versión compacta de stat_card)

# Sección 6: Tabla de intervenciones
- intervenciones_table(  # NUEVO
    data=[...],
    expandable=True,  # Para ver detalles de servicios
    searchable=True,
    filterable=True,
    pagination=True
  )
```

---

## 👨‍💼 REPORTE ADMINISTRADOR - LAYOUT COMPLETO {#reporte-administrador}

### **📐 Wireframe Visual:**

```
╔════════════════════════════════════════════════════════════════════╗
║  📊 REPORTES OPERATIVOS                                            ║
║  Control y supervisión de operaciones diarias                     ║
║                                                                    ║
║  [Filtros: 📅 Hoy ▼] [🔄 Actualizar] [📥 Exportar PDF]           ║
╚════════════════════════════════════════════════════════════════════╝

┌────────────────────────────────────────────────────────────────────┐
│ SECCIÓN 1: CARDS DE MÉTRICAS OPERATIVAS                            │
└────────────────────────────────────────────────────────────────────┘

┌────────────┐  ┌────────────┐  ┌────────────┐  ┌────────────┐
│ 📋 CONSULTAS│ │ ⏳ PENDIENTES│ │ 💰 PAGOS   │  │ 👥 PACIENTES│
│    HOY     │  │            │  │ PENDIENTES │  │   NUEVOS   │
│            │  │            │  │            │  │            │
│     24     │  │      8     │  │  $2,340    │  │     12     │
│  ↑ +6      │  │  → igual   │  │  ↑ +$450   │  │  ↑ +3      │
└────────────┘  └────────────┘  └────────────┘  └────────────┘

┌────────────────────────────────────────────────────────────────────┐
│ SECCIÓN 2: CONSULTAS POR ESTADO (HOY)                              │
└────────────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────┐
│ 📊 Estado de Consultas del Día                                 │
│ ─────────────────────────────────────────────────────────────  │
│                                                                │
│  Consultas                                                     │
│      │                                                         │
│   14 │                 ████                                    │
│      │                 ████                                    │
│   12 │                 ████                                    │
│      │                 ████                                    │
│   10 │                 ████                                    │
│      │                 ████                                    │
│    8 │     ████        ████        ████                        │
│      │     ████        ████        ████                        │
│    6 │     ████        ████        ████                        │
│      │     ████        ████        ████        ████            │
│    4 │     ████        ████        ████        ████            │
│      │     ████        ████        ████        ████            │
│    2 │     ████        ████        ████        ████            │
│      │     ████        ████        ████        ████            │
│    0 └─────────────────────────────────────────────────────    │
│        En Espera  En Atención  Completada   Cancelada          │
│           8            6            14           2             │
│                                                                │
│  💡 14 consultas completadas hoy (58% del total)               │
└───────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────┐
│ SECCIÓN 3: TABLA DE CONSULTAS (HOY/SEMANA/MES)                     │
└────────────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────┐
│ 📋 Registro de Consultas                                       │
│ ─────────────────────────────────────────────────────────────  │
│                                                                │
│ [🔍 Buscar...] [📅 Hoy▼] [👨‍⚕️ Todos▼] [🏷️ Estado: Todos▼]  │
│                                                                │
│ ┌─────────────────────────────────────────────────────────┐   │
│ │N° Consulta│Llegada │Paciente    │Odontólogo │Estado   │   │
│ ├─────────────────────────────────────────────────────────┤   │
│ │C-0124     │10:30 AM│Juan Pérez  │Dr. García │🟢 Compl.│   │
│ │           │        │HC: 0012    │           │         │   │
│ ├─────────────────────────────────────────────────────────┤   │
│ │C-0125     │11:45 AM│Ana Martínez│Dra.López  │🔵 En At.│   │
│ │           │        │HC: 0045    │           │         │   │
│ ├─────────────────────────────────────────────────────────┤   │
│ │C-0126     │02:15 PM│Carlos Ruiz │Dr. García │🟡 Espera│   │
│ │           │        │HC: 0089    │           │         │   │
│ ├─────────────────────────────────────────────────────────┤   │
│ │C-0127     │03:30 PM│María Silva │Dra.López  │🟡 Espera│   │
│ │           │        │HC: 0156    │           │         │   │
│ └─────────────────────────────────────────────────────────┘   │
│                                                                │
│ [← Anterior] Página 1 de 3 [Siguiente →]                      │
└───────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────┐
│ SECCIÓN 4: PAGOS PENDIENTES (TABLA CON ALERTAS)                    │
└────────────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────┐
│ 💰 Cuentas por Cobrar                                          │
│ ─────────────────────────────────────────────────────────────  │
│                                                                │
│ [🔍 Buscar paciente...] [⚠️ Por antigüedad ▼]                 │
│                                                                │
│ ┌─────────────────────────────────────────────────────────┐   │
│ │Recibo │Paciente    │Saldo    │Fecha Pago│Días │Alerta │   │
│ ├─────────────────────────────────────────────────────────┤   │
│ │REC-001│Ana García  │$450 USD │2025-10-05│ 33  │🔴 Urgente│ │
│ │       │HC: 0023    │         │          │     │         │   │
│ ├─────────────────────────────────────────────────────────┤   │
│ │REC-012│Luis Torres │$280 USD │2025-10-18│ 20  │🟡 Pronto│  │
│ │       │HC: 0067    │         │          │     │         │   │
│ ├─────────────────────────────────────────────────────────┤   │
│ │REC-023│María López │$150 USD │2025-10-28│ 10  │🟢 Normal│  │
│ │       │HC: 0145    │         │          │     │         │   │
│ └─────────────────────────────────────────────────────────┘   │
│                                                                │
│ 💡 Total por cobrar: $2,340 USD | 15 cuentas pendientes      │
│ ⚠️ 3 pagos con más de 30 días de antigüedad                   │
└───────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────┐
│ SECCIÓN 5: GRID CON 2 COLUMNAS                                     │
└────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────┐  ┌──────────────────────────────┐
│ 📈 PACIENTES NUEVOS (30 DÍAS)│  │ 📊 CONSULTAS POR ODONTÓLOGO │
│ ──────────────────────────── │  │ ──────────────────────────── │
│                              │  │                              │
│  15 │        ╱╲              │  │ Dr. García    ████████ 42   │
│     │    ╱╲ ╱  ╲        ╱╲   │  │                              │
│  10 │ ╱╲╱  ╲╱    ╲    ╱╲╱  ╲ │  │ Dra. López    ██████ 35     │
│     │╱              ╲ ╱        │  │                              │
│   5 │                ╱          │  │ Dr. Rodríguez ████ 28       │
│     │                           │  │                              │
│   0 └──────────────────────    │  │ Dr. Martínez  ██ 18         │
│     05  10  15  20  25  30     │  │                              │
│                                │  │ [Este mes: Octubre 2025]    │
│ 💡 +87 pacientes nuevos        │  │                              │
│ 📈 Tendencia: +12%             │  │ 💡 Total: 123 consultas     │
└──────────────────────────────┘  └──────────────────────────────┘

┌────────────────────────────────────────────────────────────────────┐
│ SECCIÓN 6: TIPOS DE CONSULTA (PIE CHART)                           │
└────────────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────┐
│ 🏷️ Distribución de Tipos de Consulta (Este Mes)               │
│ ─────────────────────────────────────────────────────────────  │
│                                                                │
│              ╭─────────────╮                                   │
│              │     65%     │                                   │
│          ╭───│   GENERAL   │───╮                               │
│          │   │  80 consultas│  │    ┌──────────────────┐      │
│          │   ╰─────────────╯   │    │ General:    80   │      │
│      ╭───┴───╮             ╭───┴──╮ │ Control:    25   │      │
│      │  20%  │             │  10% │ │ Urgencia:   12   │      │
│      │CONTROL│             │ URG. │ │ Emergencia:  6   │      │
│      ╰───────╯             ╰──────╯ │                  │      │
│                          ╭────╮     │ Total: 123       │      │
│                          │ 5% │     └──────────────────┘      │
│                          │EMER│                               │
│                          ╰────╯                               │
│                                                                │
└───────────────────────────────────────────────────────────────┘
```

### **🔧 Componentes Usados (Administrador):**

```python
# Sección 1: Cards operativos
- stat_card() x4

# Sección 2: Consultas por estado
- rx.recharts.bar_chart(
    data=[
        {"estado": "En Espera", "cantidad": 8, "fill": "#f59e0b"},
        {"estado": "En Atención", "cantidad": 6, "fill": "#3b82f6"},
        {"estado": "Completada", "cantidad": 14, "fill": "#10b981"},
        {"estado": "Cancelada", "cantidad": 2, "fill": "#ef4444"}
    ]
  )

# Sección 3: Tabla de consultas
- consultas_table(  # NUEVO
    data=[...],
    searchable=True,
    filterable=True,
    status_badges=True
  )

# Sección 4: Pagos pendientes
- pagos_pendientes_table(  # NUEVO
    data=[...],
    alert_column=True,  # Muestra alertas por antigüedad
    sortable=True
  )

# Sección 5: Gráficos en grid
- render_chart()  # Pacientes nuevos (área)
- horizontal_bar_chart()  # Consultas por odontólogo

# Sección 6: Tipos de consulta
- pie_chart_card()  # REUTILIZADO
```

---

## ⚙️ ARQUITECTURA DE SERVICIOS {#arquitectura-servicios}

### **📁 Archivo: `reportes_service.py`**

```python
"""
🎯 SERVICIO CENTRALIZADO DE REPORTES
Maneja todas las consultas y procesamiento de datos para reportes
"""

from typing import Dict, Any, List, Optional
from datetime import date, datetime, timedelta
from .base_service import BaseService
import logging

logger = logging.getLogger(__name__)

class ReportesService(BaseService):
    """
    Servicio que maneja todas las estadísticas y reportes por rol
    """

    def __init__(self):
        super().__init__()

    # ====================================================================
    # 👔 MÉTODOS PARA GERENTE
    # ====================================================================

    async def get_distribucion_pagos_usd_bs(
        self,
        fecha_inicio: str,
        fecha_fin: str
    ) -> Dict[str, float]:
        """
        💵 Distribución de pagos USD vs BS

        Returns:
            {
                "total_usd": 4357.75,
                "total_bs": 8092.25,
                "porcentaje_usd": 35,
                "porcentaje_bs": 65
            }
        """
        pass

    async def get_ranking_servicios(
        self,
        fecha_inicio: str,
        fecha_fin: str,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        🏆 Ranking de servicios más aplicados

        Returns:
            [
                {
                    "servicio_nombre": "Limpieza Dental",
                    "categoria": "Preventiva",
                    "veces_aplicado": 156,
                    "ingresos_generados": 4680.00,
                    "porcentaje": 28
                },
                ...
            ]
        """
        pass

    async def get_ranking_odontologos(
        self,
        fecha_inicio: str,
        fecha_fin: str,
        ordenar_por: str = 'consultas'  # 'consultas' o 'ingresos'
    ) -> List[Dict[str, Any]]:
        """
        👨‍⚕️ Ranking de odontólogos

        Returns:
            [
                {
                    "nombre": "Dr. Juan Pérez",
                    "especialidad": "Endodoncia",
                    "total_consultas": 89,
                    "total_intervenciones": 145,
                    "ingresos_totales": 8920.00,
                    "satisfaccion": 98  # placeholder para v2.0
                },
                ...
            ]
        """
        pass

    async def get_estadisticas_pacientes(self) -> Dict[str, Any]:
        """
        👥 Estadísticas generales de pacientes

        Returns:
            {
                "total_pacientes": 1247,
                "nuevos_mes": 87,
                "hombres": 598,
                "mujeres": 649,
                "edad_promedio": 35.5
            }
        """
        pass

    async def get_metodos_pago_populares(
        self,
        fecha_inicio: str,
        fecha_fin: str
    ) -> List[Dict[str, Any]]:
        """
        💳 Métodos de pago más usados

        Returns:
            [
                {
                    "metodo": "Efectivo",
                    "veces_usado": 234,
                    "monto_total": 12450.00,
                    "porcentaje": 45
                },
                ...
            ]
        """
        pass

    # ====================================================================
    # 🦷 MÉTODOS PARA ODONTÓLOGO
    # ====================================================================

    async def get_ingresos_odontologo_usd_bs(
        self,
        odontologo_id: str,
        fecha_inicio: str,
        fecha_fin: str
    ) -> Dict[str, float]:
        """
        💵 Distribución de ingresos USD vs BS del odontólogo
        """
        pass

    async def get_ranking_servicios_odontologo(
        self,
        odontologo_id: str,
        fecha_inicio: str,
        fecha_fin: str,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        🏆 Ranking de servicios más aplicados por el odontólogo

        Returns: Similar a get_ranking_servicios pero con datos del odontólogo
        """
        pass

    async def get_intervenciones_odontologo(
        self,
        odontologo_id: str,
        filtros: Dict[str, Any],
        limit: int = 50,
        offset: int = 0
    ) -> Dict[str, Any]:
        """
        📋 Tabla completa de intervenciones del odontólogo

        Args:
            filtros: {
                "fecha_inicio": "2025-10-01",
                "fecha_fin": "2025-10-31",
                "busqueda": "texto",  # nombre paciente o número consulta
                "estado": "completada"
            }

        Returns:
            {
                "intervenciones": [...],
                "total": 145,
                "pagina_actual": 1,
                "total_paginas": 3
            }
        """
        pass

    async def get_estadisticas_odontograma_odontologo(
        self,
        odontologo_id: str,
        fecha_inicio: str,
        fecha_fin: str
    ) -> Dict[str, Any]:
        """
        🦷 Estadísticas del odontograma del odontólogo

        Returns:
            {
                "condiciones_mas_tratadas": [
                    {"tipo": "obturacion", "cantidad": 67, "porcentaje": 34},
                    ...
                ],
                "dientes_mas_intervenidos": [
                    {"diente_numero": 16, "intervenciones": 18},
                    ...
                ],
                "superficies_mas_tratadas": [
                    {"superficie": "oclusal", "cantidad": 45, "porcentaje": 38},
                    ...
                ]
            }
        """
        pass

    # ====================================================================
    # 👨‍💼 MÉTODOS PARA ADMINISTRADOR
    # ====================================================================

    async def get_consultas_por_estado(
        self,
        fecha: str  # "hoy", "semana", "mes", o fecha específica
    ) -> List[Dict[str, Any]]:
        """
        📊 Distribución de consultas por estado

        Returns:
            [
                {"estado": "en_espera", "cantidad": 8},
                {"estado": "en_atencion", "cantidad": 6},
                {"estado": "completada", "cantidad": 14},
                {"estado": "cancelada", "cantidad": 2}
            ]
        """
        pass

    async def get_consultas_tabla(
        self,
        filtros: Dict[str, Any],
        limit: int = 50,
        offset: int = 0
    ) -> Dict[str, Any]:
        """
        📋 Tabla de consultas con filtros

        Args:
            filtros: {
                "fecha": "hoy" | "semana" | "mes",
                "odontologo_id": "uuid",
                "estado": "en_espera",
                "busqueda": "texto"
            }

        Returns:
            {
                "consultas": [...],
                "total": 24,
                "pagina_actual": 1,
                "total_paginas": 1
            }
        """
        pass

    async def get_pagos_pendientes(self) -> List[Dict[str, Any]]:
        """
        💰 Lista de pagos pendientes con alertas

        Returns:
            [
                {
                    "recibo": "REC-001",
                    "paciente_nombre": "Ana García",
                    "paciente_hc": "0023",
                    "saldo_total": 450.00,
                    "fecha_pago": "2025-10-05",
                    "dias_pendientes": 33,
                    "alerta": "urgente"  # urgente, pronto, normal
                },
                ...
            ]
        """
        pass

    async def get_pacientes_nuevos_tiempo(
        self,
        fecha_inicio: str,
        fecha_fin: str
    ) -> List[Dict[str, Any]]:
        """
        📈 Pacientes nuevos por día

        Returns:
            [
                {"fecha": "2025-11-01", "nuevos": 3},
                {"fecha": "2025-11-02", "nuevos": 5},
                ...
            ]
        """
        pass

    async def get_distribucion_consultas_odontologo(
        self,
        fecha_inicio: str,
        fecha_fin: str
    ) -> List[Dict[str, Any]]:
        """
        📊 Distribución de consultas por odontólogo

        Returns:
            [
                {
                    "odontologo": "Dr. García",
                    "total_consultas": 42,
                    "completadas": 38,
                    "pendientes": 4
                },
                ...
            ]
        """
        pass

    async def get_tipos_consulta_distribucion(
        self,
        fecha_inicio: str,
        fecha_fin: str
    ) -> List[Dict[str, Any]]:
        """
        🏷️ Distribución de tipos de consulta

        Returns:
            [
                {"tipo": "general", "cantidad": 80, "porcentaje": 65},
                {"tipo": "control", "cantidad": 25, "porcentaje": 20},
                {"tipo": "urgencia", "cantidad": 12, "porcentaje": 10},
                {"tipo": "emergencia", "cantidad": 6, "porcentaje": 5}
            ]
        """
        pass

# Instancia única para importar
reportes_service = ReportesService()
```

---

## 🔄 FLUJO DE DATOS {#flujo-datos}

### **📊 Ejemplo: Ranking de Servicios (Gerente)**

```
┌─────────────────┐
│  PÁGINA REPORTES│
│  (Frontend)     │
└────────┬────────┘
         │
         │ 1. Usuario selecciona "Este Mes"
         │    AppState.filtro_fecha = "este_mes"
         │
         ▼
┌─────────────────┐
│   APP STATE     │
│ (estado_reportes│
│      .py)       │
└────────┬────────┘
         │
         │ 2. Llama a servicio
         │    await reportes_service.get_ranking_servicios(
         │        fecha_inicio="2025-11-01",
         │        fecha_fin="2025-11-30",
         │        limit=10
         │    )
         │
         ▼
┌─────────────────┐
│ REPORTES SERVICE│
│ (reportes_      │
│  service.py)    │
└────────┬────────┘
         │
         │ 3. Ejecuta query SQL
         │    SELECT s.nombre, s.categoria,
         │           COUNT(*) as veces,
         │           SUM(hm.precio_total) as ingresos
         │    FROM historia_medica hm
         │    JOIN servicio s ON hm.servicio_id = s.id
         │    WHERE hm.fecha_registro BETWEEN ? AND ?
         │    GROUP BY s.id
         │    ORDER BY veces DESC
         │    LIMIT 10
         │
         ▼
┌─────────────────┐
│   SUPABASE      │
│   PostgreSQL    │
└────────┬────────┘
         │
         │ 4. Retorna datos
         │    [
         │      {"servicio": "Limpieza", "veces": 156, "ingresos": 4680},
         │      {"servicio": "Obturación", "veces": 124, "ingresos": 3720},
         │      ...
         │    ]
         │
         ▼
┌─────────────────┐
│ REPORTES SERVICE│
│ (Procesamiento) │
└────────┬────────┘
         │
         │ 5. Calcula porcentajes y formatea
         │    total_servicios = sum(veces)
         │    for item in data:
         │        item["porcentaje"] = (veces / total) * 100
         │
         ▼
┌─────────────────┐
│   APP STATE     │
│ (Actualización) │
└────────┬────────┘
         │
         │ 6. Actualiza estado reactivo
         │    self.ranking_servicios = processed_data
         │
         ▼
┌─────────────────┐
│  COMPONENTE UI  │
│ ranking_table() │
└─────────────────┘
         │
         │ 7. Renderiza tabla con:
         │    - Nombre del servicio
         │    - Barra de progreso visual
         │    - Número de veces aplicado
         │    - Ingresos generados
         │
         ▼
    👤 USUARIO
```

---

## 🆕 COMPONENTES NUEVOS A CREAR {#componentes-nuevos}

### **1. `pie_chart_card()`**
```python
def pie_chart_card(
    title: str,
    data: List[Dict[str, Any]],  # [{"name": "USD", "value": 4357.75}, ...]
    colors: List[str],
    subtitle: Optional[str] = None
) -> rx.Component:
    """
    📊 Card con gráfico de torta

    Ubicación: dental_system/components/charts.py
    """
    return rx.box(
        rx.vstack(
            # Header
            rx.text(title, style=dark_header_style()),

            # Pie Chart
            rx.recharts.pie_chart(
                rx.recharts.pie(
                    data=data,
                    data_key="value",
                    name_key="name",
                    cx="50%",
                    cy="50%",
                    label=True
                ),
                rx.recharts.legend(),
                width="100%",
                height=300
            ),

            # Stats summary
            rx.hstack(
                *[
                    rx.hstack(
                        rx.box(
                            width="12px",
                            height="12px",
                            background=colors[i],
                            border_radius="2px"
                        ),
                        rx.text(f"{item['name']}: ${item['value']:,.2f}"),
                        spacing="2"
                    )
                    for i, item in enumerate(data)
                ],
                spacing="4"
            ),

            spacing="4",
            width="100%"
        ),
        **dark_crystal_card(color=COLORS["primary"]["500"])
    )
```

### **2. `ranking_table()`**
```python
def ranking_table(
    title: str,
    columns: List[str],
    data: List[Dict[str, Any]],
    show_progress_bar: bool = False,
    show_trend: bool = False,
    avatar_column: Optional[int] = None
) -> rx.Component:
    """
    🏆 Tabla de ranking con barras de progreso opcionales

    Ubicación: dental_system/components/common.py
    """
    return rx.box(
        rx.vstack(
            # Header
            page_header(title, actions=[
                rx.button("Ver todos", variant="ghost")
            ]),

            # Table
            rx.table.root(
                rx.table.header(
                    rx.table.row(
                        *[rx.table.column_header_cell(col) for col in columns]
                    )
                ),
                rx.table.body(
                    rx.foreach(
                        data,
                        lambda row: rx.table.row(
                            # Renderiza cada celda con lógica especial
                            # Si show_progress_bar y columna numérica → barra
                            # Si avatar_column → muestra avatar + nombre
                            # Si show_trend → muestra flecha ↑/↓
                        )
                    )
                ),
                width="100%"
            ),

            spacing="4",
            width="100%"
        ),
        **dark_crystal_card(color=COLORS["primary"]["500"])
    )
```

### **3. `filtro_fecha_rango()`**
```python
def filtro_fecha_rango() -> rx.Component:
    """
    📅 Selector de rango de fechas con presets

    Ubicación: dental_system/components/common.py
    """
    return rx.select.root(
        rx.select.trigger("📅 Este Mes"),
        rx.select.content(
            rx.select.item("Hoy", value="hoy"),
            rx.select.item("Esta Semana", value="semana"),
            rx.select.item("Este Mes", value="mes"),
            rx.select.item("Últimos 30 días", value="30_dias"),
            rx.select.item("Últimos 3 meses", value="3_meses"),
            rx.select.item("Este Año", value="año"),
            rx.select.separator(),
            rx.select.item("Rango personalizado...", value="custom")
        ),
        on_change=AppState.set_filtro_fecha
    )
```

### **4. `intervenciones_table()`**
```python
def intervenciones_table(
    data: List[Dict[str, Any]],
    expandable: bool = True,
    searchable: bool = True,
    pagination: bool = True
) -> rx.Component:
    """
    📋 Tabla de intervenciones con detalles expandibles

    Ubicación: dental_system/components/odontologia/
    """
    return rx.box(
        # Buscador
        rx.cond(
            searchable,
            rx.input(
                placeholder="🔍 Buscar por paciente o consulta...",
                on_change=AppState.buscar_intervenciones
            )
        ),

        # Tabla con filas expandibles
        rx.table.root(
            rx.table.header(...),
            rx.table.body(
                rx.foreach(
                    data,
                    lambda interv: rx.fragment(
                        # Fila principal
                        rx.table.row(...),

                        # Fila expandida (servicios detallados)
                        rx.cond(
                            interv.expanded,
                            rx.table.row(
                                rx.table.cell(
                                    rx.vstack(
                                        # Lista de servicios aplicados
                                        ...
                                    ),
                                    colspan=len(columns)
                                )
                            )
                        )
                    )
                )
            )
        ),

        # Paginación
        rx.cond(
            pagination,
            rx.hstack(
                rx.button("← Anterior", ...),
                rx.text("Página 1 de 12"),
                rx.button("Siguiente →", ...)
            )
        )
    )
```

---

## 📦 RESUMEN DE IMPLEMENTACIÓN

### **Archivos a Crear:**
```
✅ dental_system/services/reportes_service.py       (550 líneas aprox)
✅ dental_system/state/estado_reportes.py           (200 líneas aprox)
✅ dental_system/pages/reportes_page.py             (400 líneas aprox)
```

### **Archivos a Modificar:**
```
✅ dental_system/components/charts.py               (+150 líneas)
   └── Agregar: pie_chart_card(), horizontal_bar_chart()

✅ dental_system/components/common.py               (+200 líneas)
   └── Agregar: ranking_table(), filtro_fecha_rango(), mini_stat_card()

✅ dental_system/dental_system.py                   (+5 líneas)
   └── Agregar ruta: app.add_page(reportes_page, route="/reportes")
```

### **Total de Código Nuevo:**
- **Líneas nuevas:** ~1,500 líneas
- **Queries SQL:** ~20 consultas optimizadas
- **Componentes nuevos:** 6
- **Tiempo estimado:** 6-8 horas

---

## ✅ CHECKLIST DE DESARROLLO

### **Fase 1: Servicios (2-3 horas)**
- [ ] Crear `reportes_service.py`
- [ ] Implementar métodos para Gerente (6 métodos)
- [ ] Implementar métodos para Odontólogo (4 métodos)
- [ ] Implementar métodos para Administrador (6 métodos)
- [ ] Testing de queries SQL

### **Fase 2: Estado (1 hora)**
- [ ] Crear `estado_reportes.py`
- [ ] Definir variables de estado por rol
- [ ] Implementar métodos de carga de datos
- [ ] Implementar filtros y paginación

### **Fase 3: Componentes (2 horas)**
- [ ] `pie_chart_card()`
- [ ] `ranking_table()`
- [ ] `filtro_fecha_rango()`
- [ ] `intervenciones_table()`

### **Fase 4: Páginas (2 horas)**
- [ ] Layout gerente
- [ ] Layout odontólogo
- [ ] Layout administrador
- [ ] Integración con navegación

### **Fase 5: Testing y Ajustes (1 hora)**
- [ ] Pruebas por rol
- [ ] Optimización de queries
- [ ] Ajustes de UI/UX
- [ ] Documentación final

---

**📝 ÚLTIMA ACTUALIZACIÓN:** 2025-11-07
**🎯 ESTADO:** Planificación Completa - Listo para Implementación
**👨‍💻 PREPARADO POR:** Claude Code
