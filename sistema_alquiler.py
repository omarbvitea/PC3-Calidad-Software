from enum import Enum
from datetime import datetime
from typing import Dict, Optional

class EstadoPedido(Enum):
    """Estados posibles de un pedido de alquiler"""
    PENDIENTE = "pendiente"
    EN_USO = "en_uso"
    DEVUELTO = "devuelto"
    CERRADO = "cerrado"

class Pedido:
    """Representa un pedido de alquiler de herramienta"""
    
    def __init__(self, id_pedido: str, id_usuario: str, herramienta: str, 
                 estado: EstadoPedido, id_proveedor: str = None):
        self.id_pedido = id_pedido
        self.id_usuario = id_usuario
        self.herramienta = herramienta
        self.estado = estado
        self.id_proveedor = id_proveedor
        self.fecha_devolucion = None
        self.fecha_cierre = None

class SistemaAlquiler:
    """Sistema de gestión de alquiler de herramientas"""
    
    def __init__(self):
        self.pedidos: Dict[str, Pedido] = {}
        self.notificaciones_enviadas = []
    
    def agregar_pedido(self, pedido: Pedido) -> None:
        """Agrega un pedido al sistema"""
        self.pedidos[pedido.id_pedido] = pedido
    
    def obtener_pedido(self, id_pedido: str) -> Optional[Pedido]:
        """Obtiene un pedido por su ID"""
        return self.pedidos.get(id_pedido)
    
    def registrar_devolucion(self, id_pedido: str) -> Dict:
        """
        Registra la devolución de una herramienta
        
        Args:
            id_pedido: ID del pedido a devolver
            
        Returns:
            Dict con el resultado de la operación
        """
        pedido = self.obtener_pedido(id_pedido)
        
        if not pedido:
            return {
                'exito': False,
                'mensaje': 'Pedido no encontrado'
            }
        
        if pedido.estado != EstadoPedido.EN_USO:
            return {
                'exito': False,
                'mensaje': 'El pedido no está en estado EN_USO'
            }
        
        pedido.estado = EstadoPedido.DEVUELTO
        pedido.fecha_devolucion = datetime.now()
        
        return {
            'exito': True,
            'mensaje': 'Devolución registrada exitosamente',
            'fecha_devolucion': pedido.fecha_devolucion
        }
    
    def cerrar_alquiler(self, id_pedido: str) -> Dict:
        """
        Cierra un alquiler y genera el resumen final
        
        Args:
            id_pedido: ID del pedido a cerrar
            
        Returns:
            Dict con el resultado de la operación y el resumen
        """
        pedido = self.obtener_pedido(id_pedido)
        
        if not pedido:
            return {
                'exito': False,
                'mensaje': 'Pedido no encontrado'
            }
        
        if pedido.estado != EstadoPedido.DEVUELTO:
            return {
                'exito': False,
                'mensaje': 'El pedido debe estar en estado DEVUELTO para cerrarse'
            }
        
        pedido.estado = EstadoPedido.CERRADO
        pedido.fecha_cierre = datetime.now()
        
        resumen = {
            'id_pedido': pedido.id_pedido,
            'id_usuario': pedido.id_usuario,
            'herramienta': pedido.herramienta,
            'fecha_devolucion': pedido.fecha_devolucion,
            'fecha_cierre': pedido.fecha_cierre
        }
        
        notificacion_enviada = self._enviar_notificacion_proveedor(pedido)
        
        return {
            'exito': True,
            'mensaje': 'Alquiler cerrado exitosamente',
            'resumen': resumen,
            'notificacion_enviada': notificacion_enviada
        }
    
    def _enviar_notificacion_proveedor(self, pedido: Pedido) -> bool:
        """
        Envía notificación al proveedor sobre el cierre del alquiler
        
        Args:
            pedido: Pedido cerrado
            
        Returns:
            True si la notificación se envió exitosamente
        """
        if pedido.id_proveedor:
            notificacion = {
                'id_proveedor': pedido.id_proveedor,
                'id_pedido': pedido.id_pedido,
                'mensaje': f'El alquiler {pedido.id_pedido} ha sido cerrado',
                'fecha': datetime.now()
            }
            self.notificaciones_enviadas.append(notificacion)
            return True
        return False
