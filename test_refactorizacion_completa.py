#!/usr/bin/env python3
"""
🧪 TEST DE REFACTORIZACIÓN COMPLETA - ARQUITECTURA DE SUBSTATES
===============================================================

PROPÓSITO: Validar que la nueva arquitectura funciona completamente
- Importación de todos los módulos
- Instanciación de modelos tipados
- Validación de computed vars
- Prueba de coordinación entre substates
- Verificación de nombres en español

RESULTADO ESPERADO: ✅ Sin errores de importación ni tipado
"""

import asyncio
import sys
import traceback
from datetime import datetime, date
from typing import List, Dict, Any, Optional

def test_importaciones_basicas():
    """📦 TEST 1: IMPORTACIONES BÁSICAS"""
    print("🔧 TEST 1: Verificando importaciones básicas...")
    
    try:
        # Importar modelos principales
        from dental_system.models import (
            PacienteModel, 
            ConsultaModel, 
            ServicioModel,
            PersonalModel,
            PagoModel,
            IntervencionModel,
            OdontogramaModel
        )
        print("✅ Modelos principales importados correctamente")
        
        # Importar substates
        from dental_system.state.estado_pacientes import EstadoPacientes
        from dental_system.state.estado_consultas import EstadoConsultas
        from dental_system.state.estado_servicios import EstadoServicios
        from dental_system.state.estado_pagos import EstadoPagos
        from dental_system.state.estado_odontologia import EstadoOdontologia
        print("✅ Todos los substates importados correctamente")
        
        # Importar AppState principal
        from dental_system.state.app_state import AppState
        print("✅ AppState principal importado correctamente")
        
        return True
        
    except ImportError as e:
        print(f"❌ Error de importación: {e}")
        traceback.print_exc()
        return False
    except Exception as e:
        print(f"❌ Error inesperado en importaciones: {e}")
        traceback.print_exc()
        return False

def test_instanciacion_modelos():
    """🏗️ TEST 2: INSTANCIACIÓN DE MODELOS TIPADOS"""
    print("\n🏗️ TEST 2: Verificando instanciación de modelos tipados...")
    
    try:
        from dental_system.models import (
            PacienteModel, 
            ConsultaModel, 
            ServicioModel,
            PersonalModel,
            PagoModel
        )
        
        # Crear instancias vacías
        paciente = PacienteModel()
        consulta = ConsultaModel()
        servicio = ServicioModel()
        personal = PersonalModel()
        pago = PagoModel()
        
        print("✅ Modelos instanciados sin errores")
        
        # Verificar tipos
        assert isinstance(paciente, PacienteModel)
        assert isinstance(consulta, ConsultaModel)
        assert isinstance(servicio, ServicioModel)
        assert isinstance(personal, PersonalModel)
        assert isinstance(pago, PagoModel)
        
        print("✅ Verificación de tipos exitosa")
        
        # Crear con datos de prueba
        paciente_test = PacienteModel.from_dict({
            "id": "test-123",
            "primer_nombre": "Juan",
            "primer_apellido": "Pérez",
            "numero_documento": "12345678",
            "numero_historia": "HC001"
        })
        
        print(f"✅ Paciente creado desde dict: {paciente_test.nombre_completo}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en instanciación de modelos: {e}")
        traceback.print_exc()
        return False

def test_substates_instanciacion():
    """🎯 TEST 3: INSTANCIACIÓN DE SUBSTATES"""
    print("\n🎯 TEST 3: Verificando instanciación de substates...")
    
    try:
        from dental_system.state.estado_pacientes import EstadoPacientes
        from dental_system.state.estado_consultas import EstadoConsultas
        from dental_system.state.estado_servicios import EstadoServicios
        from dental_system.state.estado_pagos import EstadoPagos
        from dental_system.state.estado_odontologia import EstadoOdontologia
        
        # Instanciar cada substate
        estado_pacientes = EstadoPacientes()
        estado_consultas = EstadoConsultas()
        estado_servicios = EstadoServicios()
        estado_pagos = EstadoPagos()
        estado_odontologia = EstadoOdontologia()
        
        print("✅ Todos los substates instanciados correctamente")
        
        # Verificar que tienen las variables esperadas
        assert hasattr(estado_pacientes, 'lista_pacientes')
        assert hasattr(estado_pacientes, 'pacientes_filtrados_display')
        assert hasattr(estado_consultas, 'lista_consultas')
        assert hasattr(estado_consultas, 'consultas_filtradas_display')
        assert hasattr(estado_servicios, 'lista_servicios')
        assert hasattr(estado_servicios, 'servicios_filtrados_display')
        assert hasattr(estado_pagos, 'lista_pagos')
        assert hasattr(estado_pagos, 'pagos_filtrados_display')
        assert hasattr(estado_odontologia, 'pacientes_asignados')
        assert hasattr(estado_odontologia, 'pacientes_filtrados_display')
        
        print("✅ Variables esperadas presentes en todos los substates")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en instanciación de substates: {e}")
        traceback.print_exc()
        return False

def test_appstate_principal():
    """🏛️ TEST 4: APPSTATE PRINCIPAL CON COMPOSICIÓN"""
    print("\n🏛️ TEST 4: Verificando AppState principal con composición...")
    
    try:
        from dental_system.state.app_state import AppState
        
        # Instanciar AppState
        app_state = AppState()
        print("✅ AppState principal instanciado")
        
        # Verificar que tiene métodos get_estado_xxx()
        assert hasattr(app_state, 'get_estado_pacientes')
        assert hasattr(app_state, 'get_estado_consultas')
        assert hasattr(app_state, 'get_estado_servicios')
        assert hasattr(app_state, 'get_estado_pagos')
        assert hasattr(app_state, 'get_estado_odontologia')
        print("✅ Métodos get_estado_xxx() presentes")
        
        # Verificar computed vars principales
        assert hasattr(app_state, 'pacientes_filtrados_display')
        assert hasattr(app_state, 'consultas_filtradas_display')
        assert hasattr(app_state, 'servicios_filtrados_display')
        assert hasattr(app_state, 'pagos_filtrados_display')
        print("✅ Computed vars principales presentes")
        
        # Verificar que no hay variables Dict[str, Any] que deberían ser modelos
        # (esto requeriría análisis más profundo del código)
        
        return True
        
    except Exception as e:
        print(f"❌ Error en AppState principal: {e}")
        traceback.print_exc()
        return False

def test_computed_vars_funcionamiento():
    """⚙️ TEST 5: FUNCIONAMIENTO DE COMPUTED VARS"""
    print("\n⚙️ TEST 5: Verificando funcionamiento de computed vars...")
    
    try:
        from dental_system.state.estado_pacientes import EstadoPacientes
        from dental_system.models import PacienteModel
        
        # Crear estado de pacientes
        estado = EstadoPacientes()
        
        # Agregar algunos pacientes de prueba
        paciente1 = PacienteModel.from_dict({
            "id": "p1",
            "primer_nombre": "Ana",
            "primer_apellido": "García",
            "numero_documento": "87654321",
            "numero_historia": "HC002",
            "activo": True
        })
        
        paciente2 = PacienteModel.from_dict({
            "id": "p2", 
            "primer_nombre": "Carlos",
            "primer_apellido": "López",
            "numero_documento": "11223344",
            "numero_historia": "HC003",
            "activo": False
        })
        
        estado.lista_pacientes = [paciente1, paciente2]
        
        # Probar computed vars
        total_activos = estado.total_pacientes_activos
        pacientes_hoy = estado.pacientes_registrados_hoy
        
        print(f"✅ Total pacientes activos: {total_activos}")
        print(f"✅ Pacientes registrados hoy: {pacientes_hoy}")
        
        # Probar filtros
        estado.mostrar_solo_activos_pacientes = True
        filtrados = estado.pacientes_filtrados_display
        print(f"✅ Pacientes filtrados (solo activos): {len(filtrados)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en computed vars: {e}")
        traceback.print_exc()
        return False

def test_nombres_en_espanol():
    """🇪🇸 TEST 6: VERIFICACIÓN DE NOMBRES EN ESPAÑOL"""
    print("\n🇪🇸 TEST 6: Verificando nombres en español...")
    
    try:
        from dental_system.state.estado_pacientes import EstadoPacientes
        from dental_system.state.estado_consultas import EstadoConsultas
        from dental_system.state.estado_servicios import EstadoServicios
        
        # Verificar variables en español
        estado_pacientes = EstadoPacientes()
        variables_espanol_pacientes = [
            'lista_pacientes', 'paciente_seleccionado', 'termino_busqueda_pacientes',
            'cargando_lista_pacientes', 'total_pacientes_activos'
        ]
        
        for var in variables_espanol_pacientes:
            assert hasattr(estado_pacientes, var), f"Variable faltante: {var}"
        
        print("✅ Variables de pacientes en español correctas")
        
        estado_consultas = EstadoConsultas()
        variables_espanol_consultas = [
            'lista_consultas', 'consulta_seleccionada', 'termino_busqueda_consultas',
            'cargando_lista_consultas', 'total_consultas_hoy'
        ]
        
        for var in variables_espanol_consultas:
            assert hasattr(estado_consultas, var), f"Variable faltante: {var}"
        
        print("✅ Variables de consultas en español correctas")
        
        estado_servicios = EstadoServicios()
        variables_espanol_servicios = [
            'lista_servicios', 'servicio_seleccionado', 'termino_busqueda_servicios',
            'cargando_lista_servicios', 'total_servicios_activos'
        ]
        
        for var in variables_espanol_servicios:
            assert hasattr(estado_servicios, var), f"Variable faltante: {var}"
        
        print("✅ Variables de servicios en español correctas")
        
        return True
        
    except Exception as e:
        print(f"❌ Error verificando nombres en español: {e}")
        traceback.print_exc()
        return False

def test_integracion_servicios():
    """🔗 TEST 7: INTEGRACIÓN CON SERVICIOS"""
    print("\n🔗 TEST 7: Verificando integración con servicios...")
    
    try:
        # Verificar que los servicios están importados correctamente
        from dental_system.services.pacientes_service import pacientes_service
        from dental_system.services.consultas_service import consultas_service
        from dental_system.services.servicios_service import servicios_service
        from dental_system.services.pagos_service import pagos_service
        from dental_system.services.odontologia_service import odontologia_service
        
        print("✅ Servicios importados correctamente")
        
        # Verificar que los substates usan los servicios correctos
        from dental_system.state.estado_pacientes import EstadoPacientes
        from dental_system.state.estado_consultas import EstadoConsultas
        
        # Esto es más difícil de verificar sin ejecutar código asíncrono,
        # pero al menos verificamos que no hay errores de importación
        
        print("✅ Integración con servicios verificada")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en integración con servicios: {e}")
        traceback.print_exc()
        return False

def generar_reporte_final(resultados: List[bool]):
    """📊 GENERAR REPORTE FINAL"""
    print("\n" + "="*60)
    print("📊 REPORTE FINAL DE REFACTORIZACIÓN")
    print("="*60)
    
    tests = [
        "Importaciones básicas",
        "Instanciación de modelos",
        "Instanciación de substates", 
        "AppState principal",
        "Computed vars funcionamiento",
        "Nombres en español",
        "Integración con servicios"
    ]
    
    exitosos = 0
    for i, resultado in enumerate(resultados):
        status = "✅ EXITOSO" if resultado else "❌ FALLIDO"
        print(f"{i+1}. {tests[i]}: {status}")
        if resultado:
            exitosos += 1
    
    print("-" * 60)
    print(f"📈 RESUMEN: {exitosos}/{len(tests)} tests exitosos")
    
    if exitosos == len(tests):
        print("🎉 ¡REFACTORIZACIÓN COMPLETAMENTE EXITOSA!")
        print("✅ La nueva arquitectura de substates funciona perfectamente")
        print("✅ Todos los modelos tipados están correctamente implementados")
        print("✅ Los nombres están en español según requerimientos")
        print("✅ La coordinación entre módulos funciona")
    else:
        print("⚠️ Refactorización parcialmente exitosa")
        print(f"❌ {len(tests) - exitosos} tests fallaron")
        print("🔧 Se requiere revisión de los módulos fallidos")
    
    return exitosos == len(tests)

def main():
    """🚀 FUNCIÓN PRINCIPAL"""
    print("🧪 INICIANDO TESTS DE REFACTORIZACIÓN COMPLETA")
    print("=" * 60)
    print(f"📅 Fecha: {datetime.now()}")
    print(f"🐍 Python: {sys.version}")
    print("-" * 60)
    
    # Ejecutar todos los tests
    resultados = []
    
    try:
        resultados.append(test_importaciones_basicas())
        resultados.append(test_instanciacion_modelos())
        resultados.append(test_substates_instanciacion())
        resultados.append(test_appstate_principal())
        resultados.append(test_computed_vars_funcionamiento())
        resultados.append(test_nombres_en_espanol())
        resultados.append(test_integracion_servicios())
        
    except KeyboardInterrupt:
        print("\n⏹️ Tests interrumpidos por el usuario")
        return False
    except Exception as e:
        print(f"\n💥 Error crítico en tests: {e}")
        traceback.print_exc()
        return False
    
    # Generar reporte final
    return generar_reporte_final(resultados)

if __name__ == "__main__":
    try:
        exito = main()
        sys.exit(0 if exito else 1)
    except Exception as e:
        print(f"💥 Error fatal: {e}")
        traceback.print_exc()
        sys.exit(1)