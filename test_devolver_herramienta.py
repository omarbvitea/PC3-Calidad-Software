import unittest
from sistema_alquiler import SistemaAlquiler, Pedido, EstadoPedido

class TestDevolverHerramienta(unittest.TestCase):
    """
    Feature: Devolver herramienta
    
    Scenario: Registrar devolución de herramienta
        Given que he finalizado el uso de la herramienta alquilada
        When accedo a la sección de mis pedidos y selecciono la opción "Devolver herramienta"
        Then debería registrarse la devolución y mostrarse una confirmación
    """
    
    def setUp(self):
        """Configuración inicial para cada test"""
        self.sistema = SistemaAlquiler()
    
    def test_registrar_devolucion_de_herramienta(self):
        """
        Scenario: Registrar devolución de herramienta
        
        Given que he finalizado el uso de la herramienta alquilada
        When accedo a la sección de mis pedidos y selecciono la opción "Devolver herramienta"
        Then debería registrarse la devolución y mostrarse una confirmación
        """
        pedido = Pedido(
            id_pedido="PED001",
            id_usuario="USR001",
            herramienta="Taladro Eléctrico",
            estado=EstadoPedido.EN_USO
        )
        self.sistema.agregar_pedido(pedido)
        
        resultado = self.sistema.registrar_devolucion(pedido.id_pedido)
        
        self.assertTrue(resultado['exito'], "La devolución no se registró correctamente")
        self.assertEqual(resultado['mensaje'], "Devolución registrada exitosamente")
        
        pedido_actualizado = self.sistema.obtener_pedido(pedido.id_pedido)
        self.assertEqual(pedido_actualizado.estado, EstadoPedido.DEVUELTO, 
                        "El estado no cambió a DEVUELTO")
        self.assertIsNotNone(pedido_actualizado.fecha_devolucion, 
                            "No se registró la fecha de devolución")
    
    def test_finalizar_alquiler_y_cerrar_transaccion(self):
        """
        Scenario: Finalizar el alquiler y cerrar la transacción
        
        Given que la devolución ha sido registrada
        When confirmo el cierre del alquiler
        Then debería generarse el resumen final del alquiler y enviarse notificación al proveedor
        """
        pedido = Pedido(
            id_pedido="PED002",
            id_usuario="USR002",
            herramienta="Cortadora de Césped",
            estado=EstadoPedido.DEVUELTO,
            id_proveedor="PROV001"
        )
        self.sistema.agregar_pedido(pedido)
        
        resultado = self.sistema.cerrar_alquiler(pedido.id_pedido)
        
        self.assertTrue(resultado['exito'], "El cierre del alquiler falló")
        self.assertIn('resumen', resultado, "No se generó el resumen")
        self.assertEqual(resultado['resumen']['id_pedido'], pedido.id_pedido)
        self.assertEqual(resultado['resumen']['herramienta'], "Cortadora de Césped")
        self.assertTrue(resultado['notificacion_enviada'], 
                       "No se envió notificación al proveedor")
        
        pedido_actualizado = self.sistema.obtener_pedido(pedido.id_pedido)
        self.assertEqual(pedido_actualizado.estado, EstadoPedido.CERRADO, 
                        "El estado no cambió a CERRADO")
        self.assertIsNotNone(pedido_actualizado.fecha_cierre, 
                            "No se registró la fecha de cierre")
    
    def test_no_se_puede_devolver_pedido_no_en_uso(self):
        """Test: No se puede devolver un pedido que no está en uso"""
        pedido = Pedido(
            id_pedido="PED003",
            id_usuario="USR003",
            herramienta="Sierra Eléctrica",
            estado=EstadoPedido.PENDIENTE
        )
        self.sistema.agregar_pedido(pedido)
        
        resultado = self.sistema.registrar_devolucion(pedido.id_pedido)
        
        self.assertFalse(resultado['exito'])
        self.assertEqual(resultado['mensaje'], 'El pedido no está en estado EN_USO')
    
    def test_no_se_puede_cerrar_pedido_no_devuelto(self):
        """Test: No se puede cerrar un pedido que no ha sido devuelto"""
        pedido = Pedido(
            id_pedido="PED004",
            id_usuario="USR004",
            herramienta="Lijadora",
            estado=EstadoPedido.EN_USO
        )
        self.sistema.agregar_pedido(pedido)
        
        resultado = self.sistema.cerrar_alquiler(pedido.id_pedido)
        
        self.assertFalse(resultado['exito'])
        self.assertEqual(resultado['mensaje'], 
                        'El pedido debe estar en estado DEVUELTO para cerrarse')
    
    def test_devolucion_pedido_inexistente(self):
        """Test: No se puede devolver un pedido que no existe"""
        resultado = self.sistema.registrar_devolucion("PED_INEXISTENTE")
        
        self.assertFalse(resultado['exito'])
        self.assertEqual(resultado['mensaje'], 'Pedido no encontrado')
    
    def test_cerrar_pedido_inexistente(self):
        """Test: No se puede cerrar un pedido que no existe"""
        resultado = self.sistema.cerrar_alquiler("PED_INEXISTENTE")
        
        self.assertFalse(resultado['exito'])
        self.assertEqual(resultado['mensaje'], 'Pedido no encontrado')


if __name__ == '__main__':
    unittest.main()
