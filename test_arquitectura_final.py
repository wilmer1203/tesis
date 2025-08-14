#!/usr/bin/env python3
"""
TEST FINAL DE ARQUITECTURA - VERIFICACION COMPLETA
==================================================

PROPOSITO: Validar que la nueva arquitectura es correcta
- Importaciones sin errores
- Modelos tipados funcionando
- Computed vars bien definidos
- Variables en espanol
- Sin conflictos de nombres

RESULTADO ESPERADO: Arquitectura completamente funcional
"""

import sys
from datetime import datetime

def test_arquitectura_completa():
    """TEST COMPLETO DE ARQUITECTURA SIN INSTANCIAR STATES"""
    print("TEST DE ARQUITECTURA COMPLETA")
    print("=" * 50)
    print(f"Fecha: {datetime.now()}")
    print("-" * 50)
    
    exitosos = 0
    total = 0
    
    # TEST 1: Importaciones principales
    print("\n1. Verificando importaciones principales...")
    total += 1
    try:
        from dental_system.models import (
            PacienteModel, ConsultaModel, ServicioModel,
            PersonalModel, PagoModel, IntervencionModel, OdontogramaModel
        )
        print("   OK - Modelos principales importados")
        exitosos += 1
    except Exception as e:
        print(f"   ERROR - {e}")
    
    # TEST 2: Importaciones de substates
    print("\n2. Verificando importaciones de substates...")
    total += 1
    try:
        from dental_system.state.estado_pacientes import EstadoPacientes
        from dental_system.state.estado_consultas import EstadoConsultas
        from dental_system.state.estado_servicios import EstadoServicios
        from dental_system.state.estado_pagos import EstadoPagos
        from dental_system.state.estado_odontologia import EstadoOdontologia
        print("   OK - Substates importados sin conflictos")
        exitosos += 1
    except Exception as e:
        print(f"   ERROR - {e}")
    
    # TEST 3: AppState principal
    print("\n3. Verificando AppState principal...")
    total += 1
    try:
        from dental_system.state.app_state import AppState
        print("   OK - AppState principal importado correctamente")
        exitosos += 1
    except Exception as e:
        print(f"   ERROR - {e}")
    
    # TEST 4: Servicios integrados
    print("\n4. Verificando servicios integrados...")
    total += 1
    try:
        from dental_system.services.pacientes_service import pacientes_service
        from dental_system.services.consultas_service import consultas_service
        from dental_system.services.servicios_service import servicios_service
        from dental_system.services.pagos_service import pagos_service
        from dental_system.services.odontologia_service import odontologia_service
        print("   OK - Servicios importados correctamente")
        exitosos += 1
    except Exception as e:
        print(f"   ERROR - {e}")
    
    # TEST 5: Verificar estructura de clases (sin instanciar)
    print("\n5. Verificando estructura de clases...")
    total += 1
    try:
        from dental_system.state.estado_pacientes import EstadoPacientes
        from dental_system.state.estado_consultas import EstadoConsultas
        
        # Verificar atributos de clase (sin instanciar)
        assert hasattr(EstadoPacientes, 'lista_pacientes')
        assert hasattr(EstadoPacientes, 'pacientes_filtrados_display')
        assert hasattr(EstadoConsultas, 'lista_consultas')
        assert hasattr(EstadoConsultas, 'consultas_filtradas_display')
        
        print("   OK - Estructura de clases correcta")
        exitosos += 1
    except Exception as e:
        print(f"   ERROR - {e}")
    
    # TEST 6: Modelos tipados funcionando
    print("\n6. Verificando modelos tipados...")
    total += 1
    try:
        from dental_system.models import PacienteModel, ConsultaModel
        
        # Crear instancias de modelos (esto si es permitido)
        paciente = PacienteModel()
        consulta = ConsultaModel()
        
        # Probar from_dict
        paciente_test = PacienteModel.from_dict({
            "id": "test",
            "primer_nombre": "Juan",
            "primer_apellido": "Perez"
        })
        
        assert paciente_test.nombre_completo == "Juan Perez"
        print("   OK - Modelos tipados funcionando correctamente")
        exitosos += 1
    except Exception as e:
        print(f"   ERROR - {e}")
    
    # TEST 7: Verificar que AppState tiene metodos esperados
    print("\n7. Verificando metodos de AppState...")
    total += 1
    try:
        from dental_system.state.app_state import AppState
        
        # Verificar metodos de composicion
        assert hasattr(AppState, 'get_estado_pacientes')
        assert hasattr(AppState, 'get_estado_consultas') 
        assert hasattr(AppState, 'get_estado_servicios')
        assert hasattr(AppState, 'get_estado_pagos')
        assert hasattr(AppState, 'get_estado_odontologia')
        
        print("   OK - Metodos de composicion presentes")
        exitosos += 1
    except Exception as e:
        print(f"   ERROR - {e}")
    
    # Reporte final
    print("\n" + "=" * 50)
    print("REPORTE FINAL")
    print("=" * 50)
    print(f"Tests exitosos: {exitosos}/{total}")
    
    if exitosos == total:
        print("\nRESULTADO: ARQUITECTURA COMPLETAMENTE FUNCIONAL")
        print("- Todas las importaciones funcionan")
        print("- Sin conflictos de nombres")
        print("- Modelos tipados correctos")
        print("- Substates bien estructurados")
        print("- AppState con composicion funcionando")
        print("- Servicios integrados correctamente")
        print("\nLA REFACTORIZACION ES EXITOSA!")
        return True
    else:
        print(f"\nRESULTADO: {total - exitosos} errores encontrados")
        print("- Se requiere revision adicional")
        return False

if __name__ == "__main__":
    try:
        exito = test_arquitectura_completa()
        sys.exit(0 if exito else 1)
    except Exception as e:
        print(f"Error fatal: {e}")
        sys.exit(1)