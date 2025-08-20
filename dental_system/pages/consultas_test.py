"""
🧪 PÁGINA DE PRUEBA PARA CONSULTAS FASE 1
========================================

Página temporal para probar el nuevo diseño doctor-céntrico
sin afectar la página principal de consultas
"""

import reflex as rx
from dental_system.pages.consultas_fase2 import consultas_fase2_page
from dental_system.components.modal_nueva_consulta_simple import modal_nueva_consulta_simple

def consultas_test_page() -> rx.Component:
    """🧪 Página de prueba para el nuevo diseño"""
    return rx.box(
        # Modal de nueva consulta simplificado
        modal_nueva_consulta_simple(),
        
        # Contenido principal Fase 2
        consultas_fase2_page(),
        
        width="100%"
    )