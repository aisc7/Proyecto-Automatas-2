class Estado:
    def __init__(self, nombre, es_inicial=False, es_final=False):
        self.nombre = nombre
        self.es_inicial = es_inicial
        self.es_final = es_final
        self.transiciones = []  
        
    def __str__(self):
        return f"Estado({self.nombre}, inicial={self.es_inicial}, final={self.es_final})"