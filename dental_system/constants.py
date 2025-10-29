"""
Constantes del Sistema Odontológico
====================================
Valores constantes compartidos entre módulos del sistema.
"""

# ==========================================
# 💳 CONSTANTES DE PAGOS
# ==========================================

METODOS_PAGO = [
    "efectivo",
    "tarjeta_credito",
    "tarjeta_debito",
    "transferencia_bancaria",
    "cheque",
    "pago_movil",
    "zelle",
    "otros"
]

ESTADOS_PAGO = [
    "pendiente",
    "completado",
    "anulado",
    "reembolsado"
]

# ==========================================
# 🦷 CONSTANTES DE ODONTOLOGÍA (V2.0)
# ==========================================

# Condiciones dentales válidas (catálogo completo)
CONDICIONES_VALIDAS = {
    'sano', 'caries', 'obturacion', 'corona', 'puente', 'implante',
    'ausente', 'extraccion_indicada', 'endodoncia', 'protesis',
    'fractura', 'mancha', 'desgaste', 'sensibilidad', 'movilidad',
    'impactado', 'en_erupcion', 'retenido', 'supernumerario', 'otro'
}

# Mapeo de condiciones a etiquetas legibles
CONDICIONES_DISPLAY = {
    "sano": "✅ Sano",
    "caries": "🦠 Caries",
    "obturacion": "🔧 Obturación",
    "endodoncia": "🦷 Endodoncia",
    "corona": "👑 Corona",
    "puente": "🌉 Puente",
    "implante": "🔩 Implante",
    "protesis": "🦾 Prótesis",
    "ausente": "❌ Ausente",
    "fractura": "💥 Fractura",
    "extraccion_indicada": "⚠️ Extracción Indicada",
    "mancha": "🟤 Mancha",
    "desgaste": "📉 Desgaste",
    "sensibilidad": "⚡ Sensibilidad",
    "movilidad": "↔️ Movilidad",
    "impactado": "🔒 Impactado",
    "en_erupcion": "🌱 En Erupción",
    "retenido": "🔗 Retenido",
    "supernumerario": "➕ Supernumerario",
    "otro": "📋 Otro"
}

# Alcances de servicios
ALCANCES_SERVICIO = {
    'superficie_especifica',
    'diente_completo',
    'boca_completa'
}

# Superficies dentales válidas
SUPERFICIES_VALIDAS = {
    'oclusal', 'mesial', 'distal', 'vestibular', 'lingual', 'incisal'
}

# Todas las superficies para diente completo
TODAS_LAS_SUPERFICIES = ['oclusal', 'mesial', 'distal', 'vestibular', 'lingual']

# Dientes permanentes por cuadrante (FDI)
CUADRANTE_1 = list(range(11, 19))  # Superior derecho
CUADRANTE_2 = list(range(21, 29))  # Superior izquierdo
CUADRANTE_3 = list(range(31, 39))  # Inferior izquierdo
CUADRANTE_4 = list(range(41, 49))  # Inferior derecho

# Todos los dientes permanentes FDI
DIENTES_FDI_PERMANENTES = CUADRANTE_1 + CUADRANTE_2 + CUADRANTE_3 + CUADRANTE_4

# Colores por condición (UI)
COLORES_CONDICION = {
    'sano': '#90EE90',           # Verde claro
    'caries': '#FF6B6B',         # Rojo
    'obturacion': '#4ECDC4',     # Azul turquesa
    'endodoncia': '#FFB347',     # Naranja
    'corona': '#FFD700',         # Dorado
    'puente': '#DDA0DD',         # Púrpura claro
    'implante': '#A9A9A9',       # Gris
    'protesis': '#F0E68C',       # Amarillo claro
    'ausente': '#000000',        # Negro
    'fractura': '#8B0000',       # Rojo oscuro
    'extraccion_indicada': '#FF4500',  # Naranja rojizo
    'otro': '#C0C0C0'            # Plata
}

# ==========================================
# 🛡️ FUNCIONES DE VALIDACIÓN (V2.0)
# ==========================================

def validar_condicion(condicion: str) -> bool:
    """
    Valida si una condición es válida según el catálogo

    Args:
        condicion: Condición a validar

    Returns:
        True si es válida, False si no
    """
    if not condicion:
        return True  # NULL es válido (servicios preventivos)
    return condicion.lower() in CONDICIONES_VALIDAS


def validar_diente_fdi(numero_diente: int) -> bool:
    """
    Valida si un número de diente es válido según FDI

    Args:
        numero_diente: Número FDI del diente

    Returns:
        True si es válido, False si no
    """
    return numero_diente in DIENTES_FDI_PERMANENTES


def validar_superficie(superficie: str) -> bool:
    """
    Valida si una superficie es válida

    Args:
        superficie: Nombre de la superficie

    Returns:
        True si es válida, False si no
    """
    return superficie.lower() in SUPERFICIES_VALIDAS


def validar_alcance(alcance: str) -> bool:
    """
    Valida si un alcance es válido

    Args:
        alcance: Alcance del servicio

    Returns:
        True si es válido, False si no
    """
    return alcance in ALCANCES_SERVICIO


def obtener_error_validacion_condicion(condicion: str) -> str:
    """
    Obtiene mensaje de error para condición inválida

    Args:
        condicion: Condición a validar

    Returns:
        Mensaje de error o string vacío si es válida
    """
    if not condicion:
        return ""  # NULL es válido

    if condicion.lower() not in CONDICIONES_VALIDAS:
        condiciones_disponibles = ', '.join(sorted(CONDICIONES_VALIDAS))
        return (
            f"Condición '{condicion}' no es válida. "
            f"Condiciones disponibles: {condiciones_disponibles}"
        )

    return ""
