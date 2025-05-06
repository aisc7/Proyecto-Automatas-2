class Estado:
    def __init__(self, nombre, es_inicial=False, es_final=False):
        self.nombre = nombre
        self.es_inicial = es_inicial
        self.es_final = es_final
        self.transiciones = []  # Lista de nombres de estados destino
        
    def __str__(self):
        return f"Estado({self.nombre})"
        
    def to_dict(self):
        """Convierte el estado a un formato diccionario para serialización JSON"""
        return {
            "nombre": self.nombre,
            "es_inicial": self.es_inicial,
            "es_final": self.es_final,
            "transiciones": self.transiciones
        }