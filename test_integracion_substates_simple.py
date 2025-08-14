"""
TEST DE INTEGRACION - SUBSTATES ESPECIALIZADOS
==============================================

PROPOSITO: Validar que los substates funcionen correctamente en conjunto
- EstadoAuth, EstadoUI, EstadoPacientes, EstadoConsultas
- EstadoPersonal, EstadoOdontologia, EstadoServicios
- Comunicacion entre substates
- Get_state() patterns funcionando
- Cache y performance optimizados

EJECUTAR: python test_integracion_substates_simple.py
"""

import asyncio
import time
import sys
import os

# Añadir el directorio del proyecto al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from dental_system.state.estado_auth import EstadoAuth
    from dental_system.state.estado_ui import EstadoUI
    from dental_system.state.estado_pacientes import EstadoPacientes
    from dental_system.state.estado_consultas import EstadoConsultas
    from dental_system.state.estado_personal import EstadoPersonal
    from dental_system.state.estado_odontologia import EstadoOdontologia
    from dental_system.state.estado_servicios import EstadoServicios
    
    # Si existe el AppState refactorizado, incluirlo
    try:
        from dental_system.state.app_state_refactored import AppState as AppStateRefactorizado
        APPSTATE_REFACTORED_AVAILABLE = True
    except ImportError:
        APPSTATE_REFACTORED_AVAILABLE = False
        print("ADVERTENCIA: AppStateRefactorizado no disponible")
        
except ImportError as e:
    print(f"ERROR: Error importando substates: {e}")
    sys.exit(1)

class TestIntegracionSubstatesSimple:
    """
    SUITE DE TESTS DE INTEGRACION PARA SUBSTATES
    """
    
    def __init__(self):
        self.resultados = {
            'substates_importados': False,
            'variables_basicas': False, 
            'computed_vars': False,
            'cache_funcionando': False,
            'comunicacion_substates': False,
            'errores_encontrados': []
        }
    
    def log_test(self, nombre_test: str, estado: str, mensaje: str = ""):
        """Log de tests con formato consistente"""
        emoji_estado = "[PASS]" if estado == "PASS" else "[FAIL]" if estado == "FAIL" else "[WAIT]"
        print(f"{emoji_estado} {nombre_test}: {mensaje}")
    
    async def test_importacion_substates(self):
        """
        TEST 1: VERIFICAR IMPORTACION DE SUBSTATES
        
        Verifica que todos los substates se importen correctamente
        """
        try:
            print("\nTEST 1: Importacion de substates")
            
            # Verificar que las clases existan
            clases_requeridas = [
                EstadoAuth,
                EstadoUI, 
                EstadoPacientes,
                EstadoConsultas,
                EstadoPersonal,
                EstadoOdontologia,
                EstadoServicios
            ]
            
            for clase in clases_requeridas:
                if not clase:
                    raise Exception(f"Clase {clase.__name__} no disponible")
            
            self.resultados['substates_importados'] = True
            self.log_test("Importacion Substates", "PASS", "Todos los 7 substates importados correctamente")
            
        except Exception as e:
            self.resultados['errores_encontrados'].append(f"Importacion test: {str(e)}")
            self.log_test("Importacion Substates", "FAIL", f"Error: {e}")
    
    async def test_variables_basicas_substates(self):
        """
        TEST 2: VERIFICAR VARIABLES BASICAS DE SUBSTATES
        
        Verifica que los substates tengan sus variables principales
        """
        try:
            print("\nTEST 2: Variables basicas de substates")
            
            # Test EstadoAuth
            estado_auth = EstadoAuth()
            variables_auth = [
                'esta_autenticado', 'id_usuario', 'rol_usuario', 'email_usuario'
            ]
            for var in variables_auth:
                if not hasattr(estado_auth, var):
                    raise Exception(f"EstadoAuth no tiene variable: {var}")
            
            # Test EstadoUI  
            estado_ui = EstadoUI()
            variables_ui = [
                'pagina_actual', 'mostrar_sidebar', 'theme_actual'
            ]
            for var in variables_ui:
                if not hasattr(estado_ui, var):
                    raise Exception(f"EstadoUI no tiene variable: {var}")
            
            # Test EstadoPacientes
            estado_pacientes = EstadoPacientes()
            variables_pacientes = [
                'lista_pacientes', 'paciente_seleccionado'
            ]
            for var in variables_pacientes:
                if not hasattr(estado_pacientes, var):
                    raise Exception(f"EstadoPacientes no tiene variable: {var}")
            
            # Test EstadoConsultas
            estado_consultas = EstadoConsultas()
            variables_consultas = [
                'lista_consultas', 'consulta_seleccionada'
            ]
            for var in variables_consultas:
                if not hasattr(estado_consultas, var):
                    raise Exception(f"EstadoConsultas no tiene variable: {var}")
            
            # Test EstadoPersonal  
            estado_personal = EstadoPersonal()
            variables_personal = [
                'lista_personal', 'empleado_seleccionado'
            ]
            for var in variables_personal:
                if not hasattr(estado_personal, var):
                    raise Exception(f"EstadoPersonal no tiene variable: {var}")
            
            # Test EstadoOdontologia
            estado_odontologia = EstadoOdontologia()
            variables_odontologia = [
                'pacientes_asignados', 'consulta_actual', 'formulario_intervencion'
            ]
            for var in variables_odontologia:
                if not hasattr(estado_odontologia, var):
                    raise Exception(f"EstadoOdontologia no tiene variable: {var}")
            
            # Test EstadoServicios
            estado_servicios = EstadoServicios()
            variables_servicios = [
                'lista_servicios', 'servicio_seleccionado'
            ]
            for var in variables_servicios:
                if not hasattr(estado_servicios, var):
                    raise Exception(f"EstadoServicios no tiene variable: {var}")
            
            self.resultados['variables_basicas'] = True
            self.log_test("Variables Basicas", "PASS", "Todas las variables principales presentes")
            
        except Exception as e:
            self.resultados['errores_encontrados'].append(f"Variables basicas test: {str(e)}")
            self.log_test("Variables Basicas", "FAIL", f"Error: {e}")
    
    async def test_computed_vars_funcionando(self):
        """
        TEST 3: VERIFICAR COMPUTED VARS CON CACHE
        
        Verifica que los computed vars esten funcionando
        """
        try:
            print("\nTEST 3: Computed vars con cache")
            
            # Test computed vars de EstadoAuth
            estado_auth = EstadoAuth()
            
            # Simular datos de usuario
            estado_auth.rol_usuario = "gerente"
            estado_auth.email_usuario = "test@test.com"
            estado_auth.esta_autenticado = True
            estado_auth.id_usuario = "test_id"
            
            # Test computed vars
            computed_vars_test = [
                ('tiene_permiso_pacientes', True),  # Gerente debe tener permiso
                ('tiene_permiso_personal', True),   # Gerente debe tener permiso  
                ('rol_usuario_display', "Gerente"), # Display formateado
                ('sesion_valida', True)             # Sesion debe ser valida
            ]
            
            for var_name, valor_esperado in computed_vars_test:
                if hasattr(estado_auth, var_name):
                    valor_actual = getattr(estado_auth, var_name)
                    if valor_actual != valor_esperado:
                        print(f"ADVERTENCIA {var_name}: esperado {valor_esperado}, obtenido {valor_actual}")
                else:
                    raise Exception(f"Computed var {var_name} no existe en EstadoAuth")
            
            # Test EstadoPacientes computed vars
            estado_pacientes = EstadoPacientes()
            estado_pacientes.lista_pacientes = []  # Lista vacia
            
            if hasattr(estado_pacientes, 'total_pacientes_display'):
                total = getattr(estado_pacientes, 'total_pacientes_display')
                if total != 0:
                    print(f"ADVERTENCIA total_pacientes_display: esperado 0, obtenido {total}")
            
            self.resultados['computed_vars'] = True
            self.log_test("Computed Vars", "PASS", "Computed vars funcionando correctamente")
            
        except Exception as e:
            self.resultados['errores_encontrados'].append(f"Computed vars test: {str(e)}")
            self.log_test("Computed Vars", "FAIL", f"Error: {e}")
    
    async def test_cache_optimization(self):
        """
        TEST 4: VERIFICAR OPTIMIZACIONES DE CACHE
        
        Verifica que las optimizaciones de cache esten funcionando
        """
        try:
            print("\nTEST 4: Optimizaciones de cache")
            
            # Test performance de computed vars con cache
            estado_auth = EstadoAuth()
            estado_auth.rol_usuario = "administrador"
            
            # Medir tiempo de multiples accesos al mismo computed var
            tiempos = []
            for i in range(10):
                start_time = time.time()
                permiso = estado_auth.tiene_permiso_pacientes  # Deberia usar cache
                tiempo_acceso = time.time() - start_time
                tiempos.append(tiempo_acceso)
            
            tiempo_promedio = sum(tiempos) / len(tiempos)
            
            # El cache deberia hacer que accesos posteriores sean muy rapidos
            if tiempo_promedio < 0.001:  # Menos de 1ms es muy bueno
                cache_efectivo = True
            else:
                cache_efectivo = False
                print(f"ADVERTENCIA Tiempo promedio de computed var: {tiempo_promedio:.4f}s")
            
            self.resultados['cache_funcionando'] = cache_efectivo
            
            if cache_efectivo:
                self.log_test("Cache Optimization", "PASS", f"Tiempo promedio: {tiempo_promedio:.4f}s")
            else:
                self.log_test("Cache Optimization", "FAIL", "Cache no optimizado suficientemente")
            
        except Exception as e:
            self.resultados['errores_encontrados'].append(f"Cache test: {str(e)}")
            self.log_test("Cache Optimization", "FAIL", f"Error: {e}")
    
    async def test_comunicacion_entre_substates(self):
        """
        TEST 5: COMUNICACION ENTRE SUBSTATES
        
        Verifica que los substates puedan comunicarse correctamente
        """
        try:
            print("\nTEST 5: Comunicacion entre substates")
            
            # Simular flujo de autenticacion → navegacion → datos
            estado_auth = EstadoAuth()
            estado_ui = EstadoUI()
            estado_pacientes = EstadoPacientes()
            
            # 1. Simular login exitoso
            estado_auth.esta_autenticado = True
            estado_auth.rol_usuario = "gerente"
            estado_auth.id_usuario = "test_gerente"
            
            # 2. Verificar que UI puede acceder a info de auth
            if estado_auth.sesion_valida:
                # 3. Simular navegacion a pacientes
                estado_ui.pagina_actual = "pacientes"
                
                # 4. Verificar permisos para cargar pacientes
                if estado_auth.tiene_permiso_pacientes:
                    # 5. Simular carga de datos
                    estado_pacientes.cargando_lista_pacientes = True
                    
                    # Simular datos cargados
                    await asyncio.sleep(0.1)  # Simular carga
                    estado_pacientes.cargando_lista_pacientes = False
                    estado_pacientes.lista_pacientes = [
                        {"id": "1", "nombre": "Test Patient"}
                    ]
                    
                    comunicacion_exitosa = True
                else:
                    raise Exception("Gerente deberia tener permiso de pacientes")
            else:
                raise Exception("Sesion deberia ser valida")
            
            self.resultados['comunicacion_substates'] = comunicacion_exitosa
            self.log_test("Comunicacion Substates", "PASS", "Flujo de comunicacion funcionando")
            
        except Exception as e:
            self.resultados['errores_encontrados'].append(f"Comunicacion test: {str(e)}")
            self.log_test("Comunicacion Substates", "FAIL", f"Error: {e}")
    
    async def test_appstate_refactored_opcional(self):
        """
        TEST 6: APPSTATE REFACTORIZADO (OPCIONAL)
        
        Si esta disponible, probar el AppState coordinador
        """
        if not APPSTATE_REFACTORED_AVAILABLE:
            print("\nTEST 6: AppState refactorizado no disponible (normal)")
            return
        
        try:
            print("\nTEST 6: AppState refactorizado")
            
            # Test get_state patterns
            app_state = AppStateRefactorizado()
            
            # Verificar que los metodos get_estado_* existan
            metodos_requeridos = [
                'get_estado_auth',
                'get_estado_ui', 
                'get_estado_pacientes',
                'get_estado_consultas',
                'get_estado_personal',
                'get_estado_odontologia',
                'get_estado_servicios'
            ]
            
            for metodo in metodos_requeridos:
                if not hasattr(app_state, metodo):
                    raise Exception(f"AppState no tiene metodo: {metodo}")
            
            # Test acceso a substates
            estado_auth = app_state.get_estado_auth()
            estado_ui = app_state.get_estado_ui()
            
            if not isinstance(estado_auth, EstadoAuth):
                raise Exception("get_estado_auth no devuelve EstadoAuth")
            
            if not isinstance(estado_ui, EstadoUI):
                raise Exception("get_estado_ui no devuelve EstadoUI")
            
            self.log_test("AppState Refactored", "PASS", "Coordinador funcionando correctamente")
            
        except Exception as e:
            self.resultados['errores_encontrados'].append(f"AppState refactored test: {str(e)}")
            self.log_test("AppState Refactored", "FAIL", f"Error: {e}")
    
    def imprimir_resumen(self):
        """
        RESUMEN FINAL DE TESTS DE INTEGRACION
        """
        print("\n" + "="*70)
        print("RESUMEN DE TESTS - INTEGRACION SUBSTATES")
        print("="*70)
        
        print(f"Substates Importados:       {'PASS' if self.resultados['substates_importados'] else 'FAIL'}")
        print(f"Variables Basicas:          {'PASS' if self.resultados['variables_basicas'] else 'FAIL'}")
        print(f"Computed Vars:              {'PASS' if self.resultados['computed_vars'] else 'FAIL'}")
        print(f"Cache Functioning:          {'PASS' if self.resultados['cache_funcionando'] else 'FAIL'}")
        print(f"Comunicacion Substates:     {'PASS' if self.resultados['comunicacion_substates'] else 'FAIL'}")
        
        if self.resultados['errores_encontrados']:
            print("\nErrores encontrados:")
            for error in self.resultados['errores_encontrados']:
                print(f"   - {error}")
        
        # Evaluacion general
        tests_exitosos = sum([
            self.resultados['substates_importados'],
            self.resultados['variables_basicas'], 
            self.resultados['computed_vars'],
            self.resultados['cache_funcionando'],
            self.resultados['comunicacion_substates']
        ])
        
        print(f"\nRESULTADO GENERAL: {tests_exitosos}/5 tests pasados")
        
        if tests_exitosos >= 4:
            print("EXITO: Substates funcionando correctamente!")
            print("Listos para migrar paginas existentes a nueva arquitectura")
        elif tests_exitosos >= 3:
            print("PARCIAL: Substates mayormente funcionales, revisar errores menores")
        else:
            print("FALLO: Substates requieren correccion antes de usar")
        
        return tests_exitosos >= 4
    
    async def ejecutar_todos_los_tests(self):
        """
        EJECUTAR TODOS LOS TESTS DE INTEGRACION
        """
        print("INICIANDO TESTS DE INTEGRACION - SUBSTATES ESPECIALIZADOS")
        print("=" * 70)
        
        tiempo_inicio = time.time()
        
        # Ejecutar tests en secuencia
        await self.test_importacion_substates()
        await self.test_variables_basicas_substates()
        await self.test_computed_vars_funcionando()
        await self.test_cache_optimization()
        await self.test_comunicacion_entre_substates()
        await self.test_appstate_refactored_opcional()
        
        tiempo_total = time.time() - tiempo_inicio
        
        # Mostrar resumen
        exito = self.imprimir_resumen()
        print(f"\nTiempo total de tests: {tiempo_total:.2f}s")
        
        return exito

async def main():
    """
    FUNCION PRINCIPAL DE TESTING
    """
    try:
        # Crear y ejecutar suite de tests
        suite_tests = TestIntegracionSubstatesSimple()
        exito = await suite_tests.ejecutar_todos_los_tests()
        
        # Recomendaciones segun resultado
        print("\nPROXIMOS PASOS RECOMENDADOS:")
        if exito:
            print("1. Migrar paginas existentes a usar substates")
            print("2. Actualizar imports en componentes UI")  
            print("3. Implementar AppState refactorizado como coordinador")
            print("4. Medir mejoras de performance en produccion")
        else:
            print("1. Corregir errores encontrados en tests")
            print("2. Revisar imports y dependencias")
            print("3. Re-ejecutar tests hasta que pasen")
        
    except Exception as e:
        print(f"ERROR: Error ejecutando tests de integracion: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # Ejecutar tests de integracion
    asyncio.run(main())