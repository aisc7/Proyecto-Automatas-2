from .estado import Estado
from .transicion import Transicion

class Automata:
    def __init__(
        self,
        estados=None,
        alfabeto="",
        transiciones=None,
        estado_inicial=None,
        estados_finales=None
    ):
        self.estados = estados if estados is not None else []  
        self.alfabeto = alfabeto
        self.transiciones = transiciones if transiciones is not None else []  
        self.estado_inicial = estado_inicial
        self.estados_finales = estados_finales if estados_finales is not None else []
        self.contador = 0
        self.visitados = []
        # Added attributes for algorithm
        self.estadoInicial = None  # Reference to Estado object, not just name
        self.estadoFinal = None    # Reference to Estado object, not just name

    def imprimirTransiciones(self):
        for i in range(len(self.transiciones)):
            print("Origen {0} - Destino {1} - Simbolo {2}".format(self.transiciones[i].origen.nombre,self.transiciones[i].destino.nombre,self.transiciones[i].simbolo))

    def setAlfabeto(self, alfabeto):
        self.alfabeto = alfabeto

    def obtenerEstado(self, origen):
        # Fix: Handle both string and Estado object cases
        if isinstance(origen, Estado):
            origen_nombre = origen.nombre
        else:
            origen_nombre = origen
            
        for estado in self.estados:
            # Fix: Make sure estados contains Estado objects, not just strings
            if isinstance(estado, str):
                if estado == origen_nombre:
                    return Estado(estado)
            else:
                if estado.nombre == origen_nombre:
                    return estado
        return None

    def modeloA(self, letra):
        estado1 = Estado(str(self.contador))
        self.contador += 1
        estado2 = Estado(str(self.contador))
        self.contador += 1
        
        # Fix: Append Estado objects, not just names
        self.estados.append(estado1)
        self.estados.append(estado2)
        
        transicion = Transicion(estado1, estado2, letra)
        estado1.transiciones.append(estado2.nombre)
        self.transiciones.append(transicion)
        
        bloque = Automata()
        bloque.estadoInicial = estado1
        bloque.estadoFinal = estado2
        return bloque

    def asterisco(self, bloque):
        nuevoEstadoInicial = Estado(str(self.contador))
        self.contador += 1
        nuevoEstadoFinal = Estado(str(self.contador))
        self.contador += 1
        
        transicion1 = Transicion(nuevoEstadoInicial, bloque.estadoInicial, 'e')
        transicion2 = Transicion(bloque.estadoFinal, nuevoEstadoFinal, 'e')
        transicion3 = Transicion(nuevoEstadoInicial, nuevoEstadoFinal, 'e')
        transicion4 = Transicion(bloque.estadoFinal, bloque.estadoInicial, 'e')
        
        nuevoEstadoInicial.transiciones.append(bloque.estadoInicial.nombre)
        bloque.estadoFinal.transiciones.append(nuevoEstadoFinal.nombre)
        nuevoEstadoInicial.transiciones.append(nuevoEstadoFinal.nombre)
        bloque.estadoFinal.transiciones.append(bloque.estadoInicial.nombre)
        
        # Fix: Append Estado objects, not just names
        self.estados.append(nuevoEstadoInicial)
        self.estados.append(nuevoEstadoFinal)
        
        self.transiciones.append(transicion1)
        self.transiciones.append(transicion2)
        self.transiciones.append(transicion3)
        self.transiciones.append(transicion4)
        
        bloque = Automata()
        bloque.estadoInicial = nuevoEstadoInicial
        bloque.estadoFinal = nuevoEstadoFinal
        return bloque

    def mas(self, bloque):
        nuevoEstadoInicial = Estado(str(self.contador))
        self.contador += 1
        nuevoEstadoFinal = Estado(str(self.contador))
        self.contador += 1
        
        transicion1 = Transicion(nuevoEstadoInicial, bloque.estadoInicial, 'e')
        transicion2 = Transicion(bloque.estadoFinal, nuevoEstadoFinal, 'e')
        transicion4 = Transicion(bloque.estadoFinal, bloque.estadoInicial, 'e')
        
        # Fix: Ensure objects are handled consistently
        nuevoEstadoInicial.transiciones.append(bloque.estadoInicial.nombre)
        bloque.estadoFinal.transiciones.append(nuevoEstadoFinal.nombre)
        bloque.estadoFinal.transiciones.append(bloque.estadoInicial.nombre)
        
        # Fix: Append Estado objects, not just names
        self.estados.append(nuevoEstadoInicial)
        self.estados.append(nuevoEstadoFinal)
        
        self.transiciones.append(transicion1)
        self.transiciones.append(transicion2)
        self.transiciones.append(transicion4)
        
        bloque = Automata()
        bloque.estadoInicial = nuevoEstadoInicial
        bloque.estadoFinal = nuevoEstadoFinal
        return bloque

    def concatenar(self, bloque1, bloque2):
        bloque2.estadoInicial.nombre = bloque1.estadoFinal.nombre
        bloque = Automata()
        bloque.estadoInicial = bloque1.estadoInicial
        bloque.estadoFinal = bloque2.estadoFinal
        return bloque
    
    def disyuncion(self, bloque1, bloque2):
        nuevoEstadoInicial = Estado(str(self.contador))
        self.contador += 1
        nuevoEstadoFinal = Estado(str(self.contador))
        self.contador += 1
        
        self.transiciones.append(Transicion(nuevoEstadoInicial, bloque1.estadoInicial, 'e'))
        self.transiciones.append(Transicion(nuevoEstadoInicial, bloque2.estadoInicial, 'e'))
        self.transiciones.append(Transicion(bloque1.estadoFinal, nuevoEstadoFinal, 'e'))
        self.transiciones.append(Transicion(bloque2.estadoFinal, nuevoEstadoFinal, 'e'))
        
        nuevoEstadoInicial.transiciones.append(bloque1.estadoInicial.nombre)
        nuevoEstadoInicial.transiciones.append(bloque2.estadoInicial.nombre)
        bloque1.estadoFinal.transiciones.append(nuevoEstadoFinal.nombre)
        bloque2.estadoFinal.transiciones.append(nuevoEstadoFinal.nombre)
        
        # Fix: Append Estado objects, not just names
        self.estados.append(nuevoEstadoInicial)
        self.estados.append(nuevoEstadoFinal)
        
        bloque = Automata()
        bloque.estadoInicial = nuevoEstadoInicial
        bloque.estadoFinal = nuevoEstadoFinal
        return bloque

    def RecorridoProfundidad(self, dato):  # dato es en que vertice empieza el recorrido
        if dato in self.visitados:
            return
        else:
            # Fix: Handle both string and Estado object cases
            estado = self.obtenerEstado(dato)
            if estado is not None:
                self.visitados.append(estado.nombre)
                for trans_destino in estado.transiciones:
                    self.RecorridoProfundidad(trans_destino)