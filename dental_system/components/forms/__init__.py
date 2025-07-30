"""
Formularios reutilizables del sistema dental.

Este módulo contiene formularios específicos para las diferentes
entidades del sistema: pacientes, consultas y pagos.
"""

from .patient_form import patient_form, patient_form_fields
from .appointment_form import appointment_form, appointment_form_fields  
from .payment_form import payment_form, payment_form_fields

__all__ = [
    "patient_form",
    "patient_form_fields", 
    "appointment_form",
    "appointment_form_fields",
    "payment_form", 
    "payment_form_fields"
]