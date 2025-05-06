from typing import List, Optional
from modelo.automata import Automata
from modelo import operaciones
from util.graficador import graficar_automata
import json

class Controlador:
    def __init__(self):
        """Inicializa el controlador con listas vacías de autómatas"""
        self.automatas_cargados: List[Automata] = []
        self.automata_actual: Optional[Automata] = None

    def cargar_desde_archivo(self, ruta: str) -> Optional[Automata]:
        """Carga un autómata desde un archivo JSON"""
        try:
            with open(ruta, 'r', encoding='utf-8') as f:
                data = json.load(f)
            automata = Automata.desde_json(data)
            self.automatas_cargados.append(automata)
            self.automata_actual = automata
            return automata
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error al cargar el archivo: {e}")
            return None

    def seleccionar_automata(self, index: int) -> bool:
        """Selecciona un autómata de la lista cargada por su índice"""
        if 0 <= index < len(self.automatas_cargados):
            self.automata_actual = self.automatas_cargados[index]
            return True
        return False

    # Métodos específicos que la vista espera
    def realizar_union(self, automata1: Automata, automata2: Automata) -> Automata:
        """Realiza la unión de dos autómatas"""
        return operaciones.union(automata1, automata2)

    def realizar_interseccion(self, automata1: Automata, automata2: Automata) -> Automata:
        """Realiza la intersección de dos autómatas"""
        return operaciones.interseccion(automata1, automata2)

    def realizar_concatenacion(self, automata1: Automata, automata2: Automata) -> Automata:
        """Realiza la concatenación de dos autómatas"""
        return operaciones.concatenacion(automata1, automata2)

    def realizar_complemento(self, automata: Automata) -> Automata:
        """Calcula el complemento de un autómata"""
        return operaciones.complemento(automata)

    def realizar_inverso(self, automata: Automata) -> Automata:
        """Invierte las transiciones de un autómata"""
        return operaciones.inverso(automata)

    def completar_automata(self, automata: Automata) -> Automata:
        """Completa un autómata añadiendo estado sumidero si es necesario"""
        return operaciones.completar(automata)

    def graficar(self, ruta_imagen: str) -> None:
        """Genera una imagen del autómata actual"""
        if not self.automata_actual:
            raise ValueError("No hay autómata actual para graficar.")
        
        # Generar la imagen del autómata
        graficar_automata(self.automata_actual, ruta_imagen)

    # Método alternativo para operaciones (opcional)
    def realizar_operacion(self, tipo_operacion: str, automata1: Automata, automata2: Optional[Automata] = None) -> Automata:
        """
        Método unificado para realizar operaciones.
        Puede usarse como alternativa a los métodos específicos.
        """
        operaciones_disponibles = {
            'union': operaciones.union,
            'interseccion': operaciones.interseccion,
            'concatenacion': operaciones.concatenacion,
            'complemento': operaciones.complemento,
            'inverso': operaciones.inverso,
            'completar': operaciones.completar
        }

        if tipo_operacion not in operaciones_disponibles:
            raise ValueError(f"Operación no soportada: {tipo_operacion}")

        if tipo_operacion in ['union', 'interseccion', 'concatenacion']:
            if automata2 is None:
                raise ValueError("Esta operación requiere dos autómatas")
            return operaciones_disponibles[tipo_operacion](automata1, automata2)
        else:
            return operaciones_disponibles[tipo_operacion](automata1)
