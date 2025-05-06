from typing import List
from modelo.automata import Automata
from modelo import operaciones
from util.graficador import graficar_automata
import json

class Controlador:
    def __init__(self):
        self.automatas_cargados: List[Automata] = []
        self.automata_actual: Automata = None

    def cargar_desde_archivo(self, ruta: str) -> Automata:
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
        if 0 <= index < len(self.automatas_cargados):
            self.automata_actual = self.automatas_cargados[index]
            return True
        return False

    def realizar_operacion(self, operacion: str, index_automata2: int = None) -> bool:
        if not self.automata_actual:
            return False

        if operacion in ['union', 'interseccion', 'concatenacion']:
            if index_automata2 is None or index_automata2 >= len(self.automatas_cargados):
                return False
            otro = self.automatas_cargados[index_automata2]

        if operacion == 'union':
            self.automata_actual = operaciones.union(self.automata_actual, otro)
        elif operacion == 'interseccion':
            self.automata_actual = operaciones.interseccion(self.automata_actual, otro)
        elif operacion == 'concatenacion':
            self.automata_actual = operaciones.concatenacion(self.automata_actual, otro)
        elif operacion == 'complemento':
            self.automata_actual = operaciones.complemento(self.automata_actual)
        elif operacion == 'inverso':
            self.automata_actual = operaciones.inverso(self.automata_actual)
        elif operacion == 'completar':
            self.automata_actual = operaciones.completar(self.automata_actual)
        else:
            return False
        return True

    def guardar_automata(self, ruta: str):
        if not self.automata_actual:
            raise ValueError("No hay autómata actual para guardar.")
        with open(ruta, 'w', encoding='utf-8') as f:
            json.dump(self.automata_actual.a_json(), f, indent=4, ensure_ascii=False)

    def graficar(self, ruta_imagen: str):
        if not self.automata_actual:
            raise ValueError("No hay autómata actual para graficar.")
        graficar_automata(self.automata_actual, ruta_imagen)
