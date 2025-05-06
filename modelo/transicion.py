class Transicion:
    def __init__(self, origen, destino, simbolo):
        self.origen = origen
        self.destino = destino
        self.simbolo = simbolo
        
    def __str__(self):
        origen_nombre = self.origen.nombre if hasattr(self.origen, 'nombre') else str(self.origen)
        destino_nombre = self.destino.nombre if hasattr(self.destino, 'nombre') else str(self.destino)
        return f"Transicion({origen_nombre} --{self.simbolo}--> {destino_nombre})"
        
    def to_dict(self):
        """Convierte la transición a un formato diccionario para serialización JSON"""
        origen_nombre = None
        # Verifica que self.origen exista y tenga el atributo 'nombre'
        if self.origen and hasattr(self.origen, 'nombre'):
            origen_nombre = self.origen.nombre

        destino_nombre = None
        # Verifica que self.destino exista y tenga el atributo 'nombre'
        if self.destino and hasattr(self.destino, 'nombre'):
            destino_nombre = self.destino.nombre
            
        return {
            "origen": origen_nombre,
            "destino": destino_nombre,
            "simbolo": self.simbolo
        }