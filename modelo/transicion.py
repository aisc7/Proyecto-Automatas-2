class Transicion:
    def __init__(self, origen, destino, simbolo):
        self.origen = origen
        self.destino = destino
        self.simbolo = simbolo
        
    def __str__(self):
        origen_nombre = self.origen.nombre if hasattr(self.origen, 'nombre') else str(self.origen)
        destino_nombre = self.destino.nombre if hasattr(self.destino, 'nombre') else str(self.destino)
        return f"Transicion({origen_nombre} --{self.simbolo}--> {destino_nombre})"