from .estado import Estado
from .transicion import Transicion

class Automata:
    def __init__(
        self,
        estados=None,
        alfabeto="",
        transiciones=None,
        estado_inicial=None,
        estados_finales=None,
        nombre=""
    ):
        self.estados = estados if estados is not None else []  
        self.alfabeto = alfabeto
        self.transiciones = transiciones if transiciones is not None else []  
        self.estado_inicial = estado_inicial
        self.estados_finales = estados_finales if estados_finales is not None else []
        self.nombre = nombre
        self.contador = 0
        self.visitados = []
        self.estadoInicial = None  # Para operaciones de construcción
        self.estadoFinal = None    # Para operaciones de construcción

    def imprimirTransiciones(self):
        for trans in self.transiciones:
            print(f"Origen {trans.origen.nombre} -> Destino {trans.destino.nombre} (Símbolo: {trans.simbolo})")

    def setAlfabeto(self, alfabeto):
        self.alfabeto = alfabeto
        
    def obtenerEstado(self, nombre_estado):
        for estado in self.estados:
            if estado.nombre == nombre_estado:
                return estado
        return None

    def modeloA(self, letra):
        estado1 = Estado(str(self.contador))
        self.contador += 1
        estado2 = Estado(str(self.contador))
        self.contador += 1
        
        self.estados.extend([estado1, estado2])
        
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
        
        transiciones = [
            Transicion(nuevoEstadoInicial, bloque.estadoInicial, 'e'),
            Transicion(bloque.estadoFinal, nuevoEstadoFinal, 'e'),
            Transicion(nuevoEstadoInicial, nuevoEstadoFinal, 'e'),
            Transicion(bloque.estadoFinal, bloque.estadoInicial, 'e')
        ]
        
        nuevoEstadoInicial.transiciones.extend([
            bloque.estadoInicial.nombre,
            nuevoEstadoFinal.nombre
        ])
        bloque.estadoFinal.transiciones.extend([
            nuevoEstadoFinal.nombre,
            bloque.estadoInicial.nombre
        ])
        
        self.estados.extend([nuevoEstadoInicial, nuevoEstadoFinal])
        self.transiciones.extend(transiciones)
        
        bloque_resultado = Automata()
        bloque_resultado.estadoInicial = nuevoEstadoInicial
        bloque_resultado.estadoFinal = nuevoEstadoFinal
        return bloque_resultado

    def mas(self, bloque):
        nuevoEstadoInicial = Estado(str(self.contador))
        self.contador += 1
        nuevoEstadoFinal = Estado(str(self.contador))
        self.contador += 1
        
        transiciones = [
            Transicion(nuevoEstadoInicial, bloque.estadoInicial, 'e'),
            Transicion(bloque.estadoFinal, nuevoEstadoFinal, 'e'),
            Transicion(bloque.estadoFinal, bloque.estadoInicial, 'e')
        ]
        
        nuevoEstadoInicial.transiciones.append(bloque.estadoInicial.nombre)
        bloque.estadoFinal.transiciones.extend([
            nuevoEstadoFinal.nombre,
            bloque.estadoInicial.nombre
        ])
        
        self.estados.extend([nuevoEstadoInicial, nuevoEstadoFinal])
        self.transiciones.extend(transiciones)
        
        bloque_resultado = Automata()
        bloque_resultado.estadoInicial = nuevoEstadoInicial
        bloque_resultado.estadoFinal = nuevoEstadoFinal
        return bloque_resultado

    def concatenar(self, bloque1, bloque2):
        bloque2.estadoInicial = bloque1.estadoFinal
        bloque_resultado = Automata()
        bloque_resultado.estadoInicial = bloque1.estadoInicial
        bloque_resultado.estadoFinal = bloque2.estadoFinal
        return bloque_resultado
    
    def disyuncion(self, bloque1, bloque2):
        nuevoEstadoInicial = Estado(str(self.contador))
        self.contador += 1
        nuevoEstadoFinal = Estado(str(self.contador))
        self.contador += 1
        
        transiciones = [
            Transicion(nuevoEstadoInicial, bloque1.estadoInicial, 'e'),
            Transicion(nuevoEstadoInicial, bloque2.estadoInicial, 'e'),
            Transicion(bloque1.estadoFinal, nuevoEstadoFinal, 'e'),
            Transicion(bloque2.estadoFinal, nuevoEstadoFinal, 'e')
        ]
        
        nuevoEstadoInicial.transiciones.extend([
            bloque1.estadoInicial.nombre,
            bloque2.estadoInicial.nombre
        ])
        bloque1.estadoFinal.transiciones.append(nuevoEstadoFinal.nombre)
        bloque2.estadoFinal.transiciones.append(nuevoEstadoFinal.nombre)
        
        self.estados.extend([nuevoEstadoInicial, nuevoEstadoFinal])
        self.transiciones.extend(transiciones)
        
        bloque_resultado = Automata()
        bloque_resultado.estadoInicial = nuevoEstadoInicial
        bloque_resultado.estadoFinal = nuevoEstadoFinal
        return bloque_resultado

    def RecorridoProfundidad(self, dato):
        if dato in self.visitados:
            return
        
        estado = self.obtenerEstado(dato)
        if estado is not None:
            self.visitados.append(estado.nombre)
            for trans_destino in estado.transiciones:
                self.RecorridoProfundidad(trans_destino)

    def a_json(self):
        """Convierte el autómata a un diccionario compatible con JSON"""
        estados_json = []
        for estado in self.estados:
            transiciones_estado_json = []
            if self.transiciones: # Esta lista está vacía según tu depuración para el autómata 'resultado'
                for trans in self.transiciones:
                    if (hasattr(trans, 'origen') and trans.origen and hasattr(trans.origen, 'nombre') and
                            hasattr(estado, 'nombre') and trans.origen.nombre == estado.nombre):
                        if hasattr(trans, 'to_dict') and callable(getattr(trans, 'to_dict')):
                            transiciones_estado_json.append(trans.to_dict())
                        else:
                            print(f"Advertencia: La transición {trans} para el estado {estado.nombre} no tiene un método to_dict válido.")
            
            estados_json.append({
                "nombre": estado.nombre if hasattr(estado, 'nombre') else None,
                "inicial": estado.es_inicial if hasattr(estado, 'es_inicial') else False,
                "final": estado.es_final if hasattr(estado, 'es_final') else False,
                "transiciones": transiciones_estado_json # Estará vacía si self.transiciones está vacío
            })

        # Sección del alfabeto modificada para ser más defensiva
        alfabeto_procesado = set()
        if isinstance(self.alfabeto, (list, set)):
            for item in self.alfabeto:
                if isinstance(item, str):
                    alfabeto_procesado.add(item)
                elif isinstance(item, Transicion) and hasattr(item, 'simbolo'): # Intenta extraer símbolo si es Transicion
                    if isinstance(item.simbolo, str):
                        alfabeto_procesado.add(item.simbolo)
                # Puedes añadir más lógica aquí si el alfabeto puede tener otros formatos inesperados
        elif isinstance(self.alfabeto, str): # Si el alfabeto es una sola cadena de símbolos
            for char_simbolo in self.alfabeto:
                alfabeto_procesado.add(char_simbolo)
        
        alfabeto_serializable = sorted(list(alfabeto_procesado))

        return {
            "nombre": self.nombre,
            "alfabeto": alfabeto_serializable, # Usar la lista procesada
            "estados": estados_json,
            "estado_inicial": self.estado_inicial.nombre if self.estado_inicial and hasattr(self.estado_inicial, 'nombre') else None,
            "estados_finales": [e.nombre for e in self.estados_finales if hasattr(e, 'nombre')]
        }

    @classmethod
    def desde_json(cls, data):
        """Crea un autómata desde un diccionario JSON"""
        estados = []
        estado_dict = {}
        estado_inicial = None
        estados_finales = []
        
        # Crear todos los estados
        for estado_data in data["estados"]:
            estado = Estado(
                nombre=estado_data["nombre"],
                es_inicial=estado_data.get("inicial", False),
                es_final=estado_data.get("final", False)
            )
            estados.append(estado)
            estado_dict[estado.nombre] = estado
            
            if estado.es_inicial:
                estado_inicial = estado
            if estado.es_final:
                estados_finales.append(estado)
        
        # Crear las transiciones
        transiciones = []
        for estado_data in data["estados"]:
            origen = estado_dict[estado_data["nombre"]]
            for trans_data in estado_data.get("transiciones", []):
                destino = estado_dict.get(trans_data["destino"])
                if destino:
                    transiciones.append(Transicion(origen, destino, trans_data["simbolo"]))
                    origen.transiciones.append(destino.nombre)
        
        return cls(
            estados=estados,
            alfabeto=data.get("alfabeto", ""),
            transiciones=transiciones,
            estado_inicial=estado_inicial,
            estados_finales=estados_finales,
            nombre=data.get("nombre", "")
        )