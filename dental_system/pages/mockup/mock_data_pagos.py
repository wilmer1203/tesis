"""
💾 DATOS MOCK PARA MÓDULO DE PAGOS
====================================

Datos estáticos variados y realistas para desarrollo de UI
Usa estructura compatible con modelos reales para migración fácil

CASOS DE USO CUBIERTOS:
- Consultas simples (1 servicio)
- Consultas complejas (múltiples servicios)
- Diferentes odontólogos
- Diferentes días de antigüedad
- Diferentes rangos de precios
- Prioridades variadas
- Estados de pago variados (completado, pendiente, mixto)
"""

from datetime import datetime, timedelta

# ==========================================
# 🏥 CONSULTAS PENDIENTES DE FACTURACIÓN
# ==========================================

CONSULTAS_PENDIENTES_MOCK = [
    # CASO 1: Consulta del día - 3 servicios - Precio medio
    {
        "consulta_id": "uuid-001",
        "numero_consulta": "CONS-20251020001",
        "paciente_id": "pac-001",
        "paciente_nombre": "Juan Carlos Pérez García",
        "paciente_documento": "V-12345678",
        "odontologo_id": "doc-001",
        "odontologo_nombre": "Dr. Carlos Mendoza",
        "fecha_consulta": "2025-10-20T10:30:00",
        "servicios_realizados": [
            {"nombre": "Limpieza Dental Profunda", "precio_usd": 45.00, "precio_bs": 1642.50},
            {"nombre": "Extracción Simple", "precio_usd": 60.00, "precio_bs": 2190.00},
            {"nombre": "Radiografía Periapical", "precio_usd": 15.00, "precio_bs": 547.50}
        ],
        "servicios_count": 3,
        "total_usd": 120.00,
        "total_bs": 4380.00,
        "concepto": "Consulta CONS-20251020001 - 3 servicios",
        "estado_consulta": "completada",
        "dias_pendiente": 0,
        "prioridad": "baja"
    },

    # CASO 2: Consulta 1 día atrás - 2 servicios - Precio bajo
    {
        "consulta_id": "uuid-002",
        "numero_consulta": "CONS-20251019005",
        "paciente_id": "pac-002",
        "paciente_nombre": "María Elena López Rodríguez",
        "paciente_documento": "V-23456789",
        "odontologo_id": "doc-002",
        "odontologo_nombre": "Dra. Ana Patricia Rodríguez",
        "fecha_consulta": "2025-10-19T14:00:00",
        "servicios_realizados": [
            {"nombre": "Obturación Composite", "precio_usd": 75.00, "precio_bs": 2737.50},
            {"nombre": "Consulta General", "precio_usd": 25.00, "precio_bs": 912.50}
        ],
        "servicios_count": 2,
        "total_usd": 100.00,
        "total_bs": 3650.00,
        "concepto": "Consulta CONS-20251019005 - 2 servicios",
        "estado_consulta": "completada",
        "dias_pendiente": 1,
        "prioridad": "normal"
    },

    # CASO 3: Consulta 5 días atrás - 2 servicios - Precio ALTO - PRIORIDAD ALTA
    {
        "consulta_id": "uuid-003",
        "numero_consulta": "CONS-20251015002",
        "paciente_id": "pac-003",
        "paciente_nombre": "Pedro Antonio Gómez Fernández",
        "paciente_documento": "V-34567890",
        "odontologo_id": "doc-003",
        "odontologo_nombre": "Dr. Luis Alberto Fernández",
        "fecha_consulta": "2025-10-15T09:00:00",
        "servicios_realizados": [
            {"nombre": "Endodoncia", "precio_usd": 180.00, "precio_bs": 6570.00},
            {"nombre": "Corona Dental de Porcelana", "precio_usd": 220.00, "precio_bs": 8030.00}
        ],
        "servicios_count": 2,
        "total_usd": 400.00,
        "total_bs": 14600.00,
        "concepto": "Consulta CONS-20251015002 - Tratamiento de conducto",
        "estado_consulta": "completada",
        "dias_pendiente": 5,
        "prioridad": "alta"  # Más de 3 días pendiente
    },

    # CASO 4: Consulta del día - 1 servicio - Precio alto - Estético
    {
        "consulta_id": "uuid-004",
        "numero_consulta": "CONS-20251020003",
        "paciente_id": "pac-004",
        "paciente_nombre": "Carolina Isabel Martínez Silva",
        "paciente_documento": "V-45678901",
        "odontologo_id": "doc-004",
        "odontologo_nombre": "Dra. Patricia Alejandra Silva",
        "fecha_consulta": "2025-10-20T16:30:00",
        "servicios_realizados": [
            {"nombre": "Blanqueamiento Dental Láser", "precio_usd": 150.00, "precio_bs": 5475.00}
        ],
        "servicios_count": 1,
        "total_usd": 150.00,
        "total_bs": 5475.00,
        "concepto": "Consulta CONS-20251020003 - Blanqueamiento",
        "estado_consulta": "completada",
        "dias_pendiente": 0,
        "prioridad": "normal"
    },

    # CASO 5: Consulta 2 días atrás - 3 servicios - Preventivo
    {
        "consulta_id": "uuid-005",
        "numero_consulta": "CONS-20251018010",
        "paciente_id": "pac-005",
        "paciente_nombre": "Roberto José Ramírez Torres",
        "paciente_documento": "V-56789012",
        "odontologo_id": "doc-005",
        "odontologo_nombre": "Dr. Miguel Ángel Torres",
        "fecha_consulta": "2025-10-18T11:15:00",
        "servicios_realizados": [
            {"nombre": "Limpieza Profunda con Ultrasonido", "precio_usd": 65.00, "precio_bs": 2372.50},
            {"nombre": "Aplicación de Flúor", "precio_usd": 20.00, "precio_bs": 730.00},
            {"nombre": "Sellantes de Fosas y Fisuras", "precio_usd": 35.00, "precio_bs": 1277.50}
        ],
        "servicios_count": 3,
        "total_usd": 120.00,
        "total_bs": 4380.00,
        "concepto": "Consulta CONS-20251018010 - Tratamiento preventivo",
        "estado_consulta": "completada",
        "dias_pendiente": 2,
        "prioridad": "normal"
    },

    # CASO 6: Consulta del día - 4 servicios - Ortodoncia - Precio medio-alto
    {
        "consulta_id": "uuid-006",
        "numero_consulta": "CONS-20251020006",
        "paciente_id": "pac-006",
        "paciente_nombre": "Sofía Gabriela Herrera Castro",
        "paciente_documento": "V-67890123",
        "odontologo_id": "doc-006",
        "odontologo_nombre": "Dr. Gabriel Enrique Herrera",
        "fecha_consulta": "2025-10-20T13:45:00",
        "servicios_realizados": [
            {"nombre": "Consulta de Ortodoncia", "precio_usd": 30.00, "precio_bs": 1095.00},
            {"nombre": "Radiografía Panorámica", "precio_usd": 25.00, "precio_bs": 912.50},
            {"nombre": "Modelos de Estudio", "precio_usd": 40.00, "precio_bs": 1460.00},
            {"nombre": "Plan de Tratamiento Ortodóntico", "precio_usd": 50.00, "precio_bs": 1825.00}
        ],
        "servicios_count": 4,
        "total_usd": 145.00,
        "total_bs": 5292.50,
        "concepto": "Consulta CONS-20251020006 - Evaluación ortodóntica",
        "estado_consulta": "completada",
        "dias_pendiente": 0,
        "prioridad": "normal"
    },

    # CASO 7: Consulta 1 día atrás - 1 servicio - Emergencia - Bajo costo
    {
        "consulta_id": "uuid-007",
        "numero_consulta": "CONS-20251019012",
        "paciente_id": "pac-007",
        "paciente_nombre": "Daniel Alejandro Moreno Díaz",
        "paciente_documento": "V-78901234",
        "odontologo_id": "doc-001",
        "odontologo_nombre": "Dr. Carlos Mendoza",
        "fecha_consulta": "2025-10-19T18:30:00",
        "servicios_realizados": [
            {"nombre": "Consulta de Emergencia", "precio_usd": 35.00, "precio_bs": 1277.50}
        ],
        "servicios_count": 1,
        "total_usd": 35.00,
        "total_bs": 1277.50,
        "concepto": "Consulta CONS-20251019012 - Emergencia dental",
        "estado_consulta": "completada",
        "dias_pendiente": 1,
        "prioridad": "normal"
    },

    # CASO 8: Consulta 3 días atrás - 5 servicios - Rehabilitación compleja
    {
        "consulta_id": "uuid-008",
        "numero_consulta": "CONS-20251017004",
        "paciente_id": "pac-008",
        "paciente_nombre": "Valentina Sofía Reyes Morales",
        "paciente_documento": "V-89012345",
        "odontologo_id": "doc-002",
        "odontologo_nombre": "Dra. Ana Patricia Rodríguez",
        "fecha_consulta": "2025-10-17T10:00:00",
        "servicios_realizados": [
            {"nombre": "Extracción Compleja", "precio_usd": 95.00, "precio_bs": 3467.50},
            {"nombre": "Curetaje Periodontal", "precio_usd": 80.00, "precio_bs": 2920.00},
            {"nombre": "Radiografía Bite-Wing", "precio_usd": 18.00, "precio_bs": 657.00},
            {"nombre": "Limpieza Post-Quirúrgica", "precio_usd": 45.00, "precio_bs": 1642.50},
            {"nombre": "Medicación y Antibióticos", "precio_usd": 30.00, "precio_bs": 1095.00}
        ],
        "servicios_count": 5,
        "total_usd": 268.00,
        "total_bs": 9782.00,
        "concepto": "Consulta CONS-20251017004 - Cirugía periodontal",
        "estado_consulta": "completada",
        "dias_pendiente": 3,
        "prioridad": "normal"
    }
]

# ==========================================
# 📋 HISTORIAL DE PAGOS PROCESADOS
# ==========================================

PAGOS_HISTORIAL_MOCK = [
    # PAGO 1: Completado - Solo USD - Efectivo
    {
        "id": "pago-001",
        "numero_recibo": "REC2025100001",
        "paciente_nombre": "Laura Patricia Díaz Moreno",
        "paciente_documento": "V-11223344",
        "concepto": "Consulta CONS-20251019002 - Obturación",
        "monto_pagado_usd": 95.00,
        "monto_pagado_bs": 0.00,
        "monto_total_usd": 95.00,
        "monto_total_bs": 3467.50,
        "saldo_pendiente_usd": 0.00,
        "saldo_pendiente_bs": 0.00,
        "estado_pago": "completado",
        "fecha_pago": "2025-10-19T15:30:00",
        "metodo_pago": "efectivo_usd",
        "procesado_por": "admin@clinica.com",
        "tasa_cambio": 36.50
    },

    # PAGO 2: Completado - Solo BS - Transferencia
    {
        "id": "pago-002",
        "numero_recibo": "REC2025100002",
        "paciente_nombre": "Andrés Felipe Castro Ruiz",
        "paciente_documento": "V-22334455",
        "concepto": "Consulta CONS-20251018008 - Limpieza",
        "monto_pagado_usd": 0.00,
        "monto_pagado_bs": 2920.00,
        "monto_total_usd": 80.00,
        "monto_total_bs": 2920.00,
        "saldo_pendiente_usd": 0.00,
        "saldo_pendiente_bs": 0.00,
        "estado_pago": "completado",
        "fecha_pago": "2025-10-18T17:00:00",
        "metodo_pago": "transferencia_bs",
        "procesado_por": "admin@clinica.com",
        "tasa_cambio": 36.50
    },

    # PAGO 3: Pendiente - Pago parcial - Mixto
    {
        "id": "pago-003",
        "numero_recibo": "REC2025100003",
        "paciente_nombre": "Carmen Rosa Jiménez Vega",
        "paciente_documento": "V-33445566",
        "concepto": "Consulta CONS-20251017004 - Pago parcial (50%)",
        "monto_pagado_usd": 50.00,
        "monto_pagado_bs": 1825.00,
        "monto_total_usd": 150.00,
        "monto_total_bs": 5475.00,
        "saldo_pendiente_usd": 50.00,
        "saldo_pendiente_bs": 1825.00,
        "estado_pago": "pendiente",
        "fecha_pago": "2025-10-17T10:00:00",
        "metodo_pago": "mixto",
        "procesado_por": "admin@clinica.com",
        "tasa_cambio": 36.50
    },

    # PAGO 4: Completado - Mixto USD+BS
    {
        "id": "pago-004",
        "numero_recibo": "REC2025100004",
        "paciente_nombre": "Diego Fernando Sánchez Luna",
        "paciente_documento": "V-44556677",
        "concepto": "Consulta CONS-20251020004 - Corona dental",
        "monto_pagado_usd": 80.00,
        "monto_pagado_bs": 1460.00,
        "monto_total_usd": 120.00,
        "monto_total_bs": 4380.00,
        "saldo_pendiente_usd": 0.00,
        "saldo_pendiente_bs": 0.00,
        "estado_pago": "completado",
        "fecha_pago": "2025-10-20T11:45:00",
        "metodo_pago": "mixto",
        "procesado_por": "gerente@clinica.com",
        "tasa_cambio": 36.50
    },

    # PAGO 5: Completado - Solo USD - Tarjeta
    {
        "id": "pago-005",
        "numero_recibo": "REC2025100005",
        "paciente_nombre": "Isabella Camila Vargas Ortiz",
        "paciente_documento": "V-55667788",
        "concepto": "Consulta CONS-20251019007 - Blanqueamiento",
        "monto_pagado_usd": 150.00,
        "monto_pagado_bs": 0.00,
        "monto_total_usd": 150.00,
        "monto_total_bs": 5475.00,
        "saldo_pendiente_usd": 0.00,
        "saldo_pendiente_bs": 0.00,
        "estado_pago": "completado",
        "fecha_pago": "2025-10-19T16:20:00",
        "metodo_pago": "tarjeta_credito",
        "procesado_por": "admin@clinica.com",
        "tasa_cambio": 36.50
    },

    # PAGO 6: Completado - Solo BS - Pago móvil
    {
        "id": "pago-006",
        "numero_recibo": "REC2025100006",
        "paciente_nombre": "Sebastián Andrés Medina Cruz",
        "paciente_documento": "V-66778899",
        "concepto": "Consulta CONS-20251018011 - Extracción",
        "monto_pagado_usd": 0.00,
        "monto_pagado_bs": 2190.00,
        "monto_total_usd": 60.00,
        "monto_total_bs": 2190.00,
        "saldo_pendiente_usd": 0.00,
        "saldo_pendiente_bs": 0.00,
        "estado_pago": "completado",
        "fecha_pago": "2025-10-18T14:10:00",
        "metodo_pago": "pago_movil",
        "procesado_por": "admin@clinica.com",
        "tasa_cambio": 36.50
    },

    # PAGO 7: Pendiente - Pago inicial - Solo USD
    {
        "id": "pago-007",
        "numero_recibo": "REC2025100007",
        "paciente_nombre": "Mariana Valentina Rojas Peña",
        "paciente_documento": "V-77889900",
        "concepto": "Consulta CONS-20251016003 - Endodoncia (Inicial)",
        "monto_pagado_usd": 100.00,
        "monto_pagado_bs": 0.00,
        "monto_total_usd": 250.00,
        "monto_total_bs": 9125.00,
        "saldo_pendiente_usd": 150.00,
        "saldo_pendiente_bs": 5475.00,
        "estado_pago": "pendiente",
        "fecha_pago": "2025-10-16T09:30:00",
        "metodo_pago": "efectivo_usd",
        "procesado_por": "gerente@clinica.com",
        "tasa_cambio": 36.50
    },

    # PAGO 8: Completado - Alto valor - Solo USD - Transferencia
    {
        "id": "pago-008",
        "numero_recibo": "REC2025100008",
        "paciente_nombre": "Alejandro José Ramírez Gutiérrez",
        "paciente_documento": "V-88990011",
        "concepto": "Consulta CONS-20251015005 - Implante dental",
        "monto_pagado_usd": 450.00,
        "monto_pagado_bs": 0.00,
        "monto_total_usd": 450.00,
        "monto_total_bs": 16425.00,
        "saldo_pendiente_usd": 0.00,
        "saldo_pendiente_bs": 0.00,
        "estado_pago": "completado",
        "fecha_pago": "2025-10-15T13:00:00",
        "metodo_pago": "transferencia_usd",
        "procesado_por": "gerente@clinica.com",
        "tasa_cambio": 36.50
    },

    # PAGO 9: Completado - Bajo valor - Solo BS - Efectivo
    {
        "id": "pago-009",
        "numero_recibo": "REC2025100009",
        "paciente_nombre": "Camila Andrea Torres Delgado",
        "paciente_documento": "V-99001122",
        "concepto": "Consulta CONS-20251020008 - Consulta general",
        "monto_pagado_usd": 0.00,
        "monto_pagado_bs": 912.50,
        "monto_total_usd": 25.00,
        "monto_total_bs": 912.50,
        "saldo_pendiente_usd": 0.00,
        "saldo_pendiente_bs": 0.00,
        "estado_pago": "completado",
        "fecha_pago": "2025-10-20T09:15:00",
        "metodo_pago": "efectivo_bs",
        "procesado_por": "admin@clinica.com",
        "tasa_cambio": 36.50
    },

    # PAGO 10: Completado - Mixto - Descuento aplicado
    {
        "id": "pago-010",
        "numero_recibo": "REC2025100010",
        "paciente_nombre": "Nicolás Eduardo Figueroa Suárez",
        "paciente_documento": "V-00112233",
        "concepto": "Consulta CONS-20251019014 - Ortodoncia (desc. 10%)",
        "monto_pagado_usd": 90.00,
        "monto_pagado_bs": 1825.00,
        "monto_total_usd": 140.00,
        "monto_total_bs": 5110.00,
        "saldo_pendiente_usd": 0.00,
        "saldo_pendiente_bs": 0.00,
        "estado_pago": "completado",
        "fecha_pago": "2025-10-19T12:00:00",
        "metodo_pago": "mixto",
        "procesado_por": "gerente@clinica.com",
        "tasa_cambio": 36.50,
        "descuento_aplicado": 14.00,
        "motivo_descuento": "Descuento por pronto pago"
    }
]

# ==========================================
# 📊 ESTADÍSTICAS DEL DÍA
# ==========================================

ESTADISTICAS_DIA_MOCK = {
    # Consultas pendientes de facturación
    "consultas_pendientes_pago": len(CONSULTAS_PENDIENTES_MOCK),

    # Recaudación del día (suma de pagos completados hoy)
    "recaudacion_usd_hoy": 225.00,  # Pagos 4, 9
    "recaudacion_bs_hoy": 2372.50,  # Pagos 4, 9

    # Tasa de cambio actual
    "tasa_del_dia": 36.50,

    # Contadores
    "pagos_completados_hoy": 2,
    "pagos_pendientes_hoy": 0,
    "total_pagos_procesados": len([p for p in PAGOS_HISTORIAL_MOCK if p["estado_pago"] == "completado"]),

    # Totales pendientes (todas las consultas sin facturar)
    "total_pendiente_usd": sum(c["total_usd"] for c in CONSULTAS_PENDIENTES_MOCK),
    "total_pendiente_bs": sum(c["total_bs"] for c in CONSULTAS_PENDIENTES_MOCK),

    # Saldos por cobrar (pagos parciales)
    "saldos_por_cobrar_usd": sum(p["saldo_pendiente_usd"] for p in PAGOS_HISTORIAL_MOCK if p["estado_pago"] == "pendiente"),
    "saldos_por_cobrar_bs": sum(p["saldo_pendiente_bs"] for p in PAGOS_HISTORIAL_MOCK if p["estado_pago"] == "pendiente"),

    # Distribución de pagos
    "pagos_solo_usd": len([p for p in PAGOS_HISTORIAL_MOCK if p["monto_pagado_usd"] > 0 and p["monto_pagado_bs"] == 0]),
    "pagos_solo_bs": len([p for p in PAGOS_HISTORIAL_MOCK if p["monto_pagado_bs"] > 0 and p["monto_pagado_usd"] == 0]),
    "pagos_mixtos": len([p for p in PAGOS_HISTORIAL_MOCK if p["monto_pagado_usd"] > 0 and p["monto_pagado_bs"] > 0]),

    # Recaudación total del mes
    "recaudacion_mes_usd": sum(p["monto_pagado_usd"] for p in PAGOS_HISTORIAL_MOCK if p["estado_pago"] == "completado"),
    "recaudacion_mes_bs": sum(p["monto_pagado_bs"] for p in PAGOS_HISTORIAL_MOCK if p["estado_pago"] == "completado"),
}

# ==========================================
# 🎨 DATOS PARA FORMULARIO DE PAGO
# ==========================================

FORMULARIO_PAGO_MOCK = {
    "consulta_seleccionada": None,  # Se llena al seleccionar una consulta
    "paciente_id": "",
    "paciente_nombre": "",
    "monto_total_usd": 0.00,
    "monto_total_bs": 0.00,
    "pago_usd": "0.00",
    "pago_bs": "0.00",
    "metodo_pago_usd": "efectivo",
    "metodo_pago_bs": "efectivo",
    "referencia_usd": "",
    "referencia_bs": "",
    "concepto": "",
    "observaciones": "",
    "tasa_cambio": 36.50
}

# ==========================================
# 🔧 MÉTODOS DE PAGO DISPONIBLES
# ==========================================

METODOS_PAGO_DISPONIBLES = ["efectivo", "transferencia", "pago_movil", "tarjeta_credito", "tarjeta_debito", "cheque"]
