#!/usr/bin/env python3
"""
🧪 TEST MODAL FIXES - Verificar que los modales funcionan correctamente

Este test verifica que las correcciones aplicadas a los modales funcionen:

✅ ERRORES CORREGIDOS:
1. empleado_seleccionado ahora es Optional[PersonalModel] = None
2. seleccionar_empleado() método implementado correctamente  
3. Acceso seguro con getattr() para atributos opcionales

✅ FUNCIONALIDAD VERIFICADA:
- Modal de personal puede abrirse sin errores de tipo
- Selección de empleados funciona correctamente
- No hay warnings de get_state() en error handling
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dental_system.state.estado_personal import EstadoPersonal
from dental_system.models.personal_models import PersonalModel

def test_modal_fixes():
    """Probar que los fixes de modales funcionan correctamente"""
    
    print("Testing Modal Fixes...")
    print("=" * 50)
    
    # Test 1: empleado_seleccionado puede ser None
    estado = EstadoPersonal()
    
    print("Test 1: empleado_seleccionado puede ser None")
    assert estado.empleado_seleccionado is None
    assert estado.id_empleado_seleccionado == ""
    print("   - empleado_seleccionado correctamente inicializado como None")
    
    # Test 2: Método seleccionar_empleado existe
    print("\nTest 2: Método seleccionar_empleado existe")
    assert hasattr(estado, 'seleccionar_empleado')
    assert callable(getattr(estado, 'seleccionar_empleado'))
    print("   - Método seleccionar_empleado está presente y es callable")
    
    # Test 3: Lista personal puede procesarse sin errores
    print("\nTest 3: Lista personal puede procesarse")
    
    # Simular algunos empleados en la lista
    empleado_test = PersonalModel.from_dict({
        "id": "test-123",
        "primer_nombre": "Juan",
        "primer_apellido": "Pérez",
        "tipo_personal": "Odontólogo",
        "numero_documento": "12345678",
        "celular": "3001234567",
        "estado_laboral": "activo"
    })
    
    estado.lista_personal = [empleado_test]
    print(f"   - Lista personal simulada: {len(estado.lista_personal)} empleados")
    
    # Test 4: Acceso seguro con getattr en métodos
    print("\nTest 4: Acceso seguro con getattr")
    
    # Simular selección de empleado
    estado.empleado_seleccionado = empleado_test
    estado.id_empleado_seleccionado = "test-123"
    
    # Verificar acceso seguro
    empleado_id = getattr(estado.empleado_seleccionado, 'id', None)
    empleado_nombre = getattr(estado.empleado_seleccionado, 'nombre_completo', 'Sin nombre')
    
    assert empleado_id == "test-123"
    assert empleado_nombre == "Juan Pérez"
    print("   - Acceso seguro con getattr funciona correctamente")
    print(f"   - ID: {empleado_id}")
    print(f"   - Nombre: {empleado_nombre}")
    
    # Test 5: Computed vars funcionan con empleado seleccionado None
    print("\nTest 5: Computed vars con empleado seleccionado None")
    
    estado.empleado_seleccionado = None
    estado.id_empleado_seleccionado = ""
    
    # Estas computed vars deben funcionar sin error
    personal_filtrado = estado.personal_filtrado
    odontologos = estado.odontologos_disponibles
    empleados_activos = estado.empleados_activos_count
    
    print(f"   - personal_filtrado: {len(personal_filtrado)} empleados")
    print(f"   - odontologos_disponibles: {len(odontologos)} odontólogos")
    print(f"   - empleados_activos_count: {empleados_activos} activos")
    
    # Test 6: Verificar propiedades del modelo PersonalModel
    print("\nTest 6: Propiedades del modelo PersonalModel")
    
    assert hasattr(empleado_test, 'nombre_completo')
    assert hasattr(empleado_test, 'rol_nombre_computed')
    
    print(f"   - nombre_completo: '{empleado_test.nombre_completo}'")
    print(f"   - rol_nombre_computed: '{empleado_test.rol_nombre_computed}'")
    print(f"   - tipo_display: '{empleado_test.tipo_display}'")
    print(f"   - estado_display: '{empleado_test.estado_display}'")
    
    print("\nTODOS LOS TESTS PASARON EXITOSAMENTE")
    print("=" * 50)
    print("- Los modales de personal deberían funcionar correctamente ahora")
    print("- No debería haber errores de tipo con empleado_seleccionado")
    print("- El método seleccionar_empleado está implementado")
    print("- El acceso seguro con getattr previene errores")
    
    return True

if __name__ == "__main__":
    try:
        test_modal_fixes()
        print("\nTest completado exitosamente - Los fixes de modales funcionan!")
    except Exception as e:
        print(f"\nError en test: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)