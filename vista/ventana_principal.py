from PySide6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton,
    QFileDialog, QMessageBox, QComboBox, QTabWidget, QGroupBox, QTextEdit
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
from controlador.controlador import Controlador
from modelo.transicion import Transicion
from modelo.automata import Automata
from modelo.estado import Estado
import json
import os


class VentanaPrincipal(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Operaciones con Autómatas")
        self.setMinimumSize(800, 600)
        self.controlador = Controlador()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        tabs = QTabWidget()

        tab_carga = self.crear_tab_carga()
        tab_operaciones = self.crear_tab_operaciones()
        tab_visualizacion = self.crear_tab_visualizacion()

        tabs.addTab(tab_carga, "Carga")
        tabs.addTab(tab_operaciones, "Operaciones")
        tabs.addTab(tab_visualizacion, "Visualización")

        layout.addWidget(tabs)
        self.setLayout(layout)

    def crear_tab_carga(self) -> QWidget:
        tab = QWidget()
        layout = QHBoxLayout()

        panel_archivos = QGroupBox("Carga de Archivos")
        panel_layout = QVBoxLayout()

        btn_cargar = QPushButton("Cargar Autómata")
        btn_cargar.clicked.connect(self.cargar_json)
        panel_layout.addWidget(btn_cargar)

        self.combo_automatas = QComboBox()
        self.combo_automatas.currentIndexChanged.connect(self.seleccionar_automata)
        panel_layout.addWidget(QLabel("Autómatas cargados:"))
        panel_layout.addWidget(self.combo_automatas)

        panel_archivos.setLayout(panel_layout)
        layout.addWidget(panel_archivos)
        tab.setLayout(layout)

        return tab

    def crear_tab_operaciones(self) -> QWidget:
        tab = QWidget()
        layout = QVBoxLayout()

        grupo_seleccion = QGroupBox("Selección de Autómatas")
        layout_seleccion = QHBoxLayout()

        self.combo_automata1 = QComboBox()
        self.combo_automata2 = QComboBox()

        layout_seleccion.addWidget(QLabel("Autómata 1:"))
        layout_seleccion.addWidget(self.combo_automata1)
        layout_seleccion.addWidget(QLabel("Autómata 2:"))
        layout_seleccion.addWidget(self.combo_automata2)

        grupo_seleccion.setLayout(layout_seleccion)
        layout.addWidget(grupo_seleccion)

        grupo_binarias = QGroupBox("Operaciones Binarias")
        layout_binarias = QHBoxLayout()
        operaciones_binarias = [
            ("Unión (A ∪ B)", 'union'),
            ("Intersección (A ∩ B)", 'interseccion'),
            ("Concatenación (A.B)", 'concatenacion')
        ]
        for texto, operacion in operaciones_binarias:
            btn = QPushButton(texto)
            btn.clicked.connect(lambda _, op=operacion: self.realizar_operacion(op))
            layout_binarias.addWidget(btn)
        grupo_binarias.setLayout(layout_binarias)
        layout.addWidget(grupo_binarias)

        grupo_unarias = QGroupBox("Operaciones Unarias")
        layout_unarias = QHBoxLayout()
        operaciones_unarias = [
            ("Complemento (A')", 'complemento'),
            ("Inverso (A⁻¹)", 'inverso'),
            ("Completar Autómata", 'completar')
        ]
        for texto, operacion in operaciones_unarias:
            btn = QPushButton(texto)
            btn.clicked.connect(lambda _, op=operacion: self.realizar_operacion(op))
            layout_unarias.addWidget(btn)
        grupo_unarias.setLayout(layout_unarias)
        layout.addWidget(grupo_unarias)

        self.resultado_operacion = QTextEdit()
        self.resultado_operacion.setReadOnly(True)
        layout.addWidget(QLabel("Resultado:"))
        layout.addWidget(self.resultado_operacion)

        tab.setLayout(layout)
        return tab

    def crear_tab_visualizacion(self) -> QWidget:
        tab = QWidget()
        layout = QVBoxLayout()

        self.visor_automata = QLabel()
        self.visor_automata.setAlignment(Qt.AlignCenter)
        self.visor_automata.setText("Visualización del autómata aparecerá aquí")

        btn_actualizar = QPushButton("Actualizar Visualización")
        btn_actualizar.clicked.connect(self.actualizar_visualizacion)

        layout.addWidget(self.visor_automata)
        layout.addWidget(btn_actualizar)
        tab.setLayout(layout)

        return tab

    def actualizar_listas(self):
        self.combo_automatas.clear()
        self.combo_automata1.clear()
        self.combo_automata2.clear()

        for i, _ in enumerate(self.controlador.automatas_cargados):
            nombre = f"Autómata {i+1}"
            self.combo_automatas.addItem(nombre, i)
            self.combo_automata1.addItem(nombre, i)
            self.combo_automata2.addItem(nombre, i)

    def cargar_json(self):
        ruta, _ = QFileDialog.getOpenFileName(
            self, "Cargar Autómata", "", "Archivos JSON (*.json)"
        )
        if not ruta:
            return

        try:
            with open(ruta, 'r', encoding='utf-8') as archivo:
                datos = json.load(archivo)

            automata = self.convertir_formato_json(datos)

            if automata:
                self.controlador.automatas_cargados.append(automata)
                self.controlador.automata_actual = automata
                self.actualizar_listas()
                self.combo_automatas.setCurrentIndex(len(self.controlador.automatas_cargados) - 1)
                QMessageBox.information(self, "Éxito", "Autómata cargado correctamente")
                self.actualizar_visualizacion()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo cargar el archivo:\n{str(e)}")

   
    def convertir_formato_json(self, data: dict) -> Automata:
        """Convierte un JSON con la estructura esperada a un objeto Automata"""
        estados_obj = []  # Lista de objetos Estado
        estado_inicial = None
        estados_finales = []
        transiciones = []
        
        # Primero creamos todos los estados
        estado_dict = {}  # Diccionario para mapear nombres a objetos Estado
        for estado_data in data["estados"]:
            nombre = estado_data["nombre"]
            es_inicial = estado_data.get("inicial", False)
            es_final = estado_data.get("final", False)
            
            estado = Estado(nombre=nombre, es_inicial=es_inicial, es_final=es_final)
            estados_obj.append(estado)
            estado_dict[nombre] = estado
            
            if es_inicial:
                estado_inicial = estado
            if es_final:
                estados_finales.append(estado)
        
        # Luego procesamos las transiciones
        for estado_data in data["estados"]:
            origen_nombre = estado_data["nombre"]
            origen = estado_dict[origen_nombre]
            
            for trans in estado_data.get("transiciones", []):
                destino_nombre = trans.get("destino") or trans.get("a")
                simbolo = trans.get("simbolo")
                
                if destino_nombre is not None and simbolo is not None:
                    destino = estado_dict.get(destino_nombre)
                    if destino:
                        transicion = Transicion(origen, destino, simbolo)
                        transiciones.append(transicion)
                        origen.transiciones.append(destino.nombre)  # Guardamos el nombre en las transiciones del estado
        
        # Creamos el autómata
        automata = Automata(
            estados=estados_obj,
            transiciones=transiciones,
            estado_inicial=estado_inicial,
            estados_finales=estados_finales
        )
        
        # Extraemos el alfabeto de las transiciones si no está definido
        if not automata.alfabeto:
            simbolos = {t.simbolo for t in transiciones if t.simbolo != 'e'}
            automata.alfabeto = ''.join(sorted(simbolos))
        
        return automata

    def seleccionar_automata(self, index: int):
        if index >= 0 and self.controlador.seleccionar_automata(index):
            self.mostrar_automata_actual()

    def mostrar_automata_actual(self):
        self.actualizar_visualizacion()

    def realizar_operacion(self, operacion: str):
        try:
            if operacion in ['union', 'interseccion', 'concatenacion']:
                self.realizar_operacion_binaria(operacion)
            elif operacion in ['complemento', 'inverso', 'completar']:
                self.realizar_operacion_unaria(operacion)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al realizar operación:\n{str(e)}")

    def realizar_operacion_binaria(self, operacion: str):
        index1 = self.combo_automata1.currentIndex()
        index2 = self.combo_automata2.currentIndex()

        if index1 == -1 or index2 == -1:
            QMessageBox.warning(self, "Error", "Debe seleccionar dos autómatas")
            return

        automata1 = self.controlador.automatas_cargados[index1]
        automata2 = self.controlador.automatas_cargados[index2]

        operaciones = {
            'union': self.controlador.realizar_union,
            'interseccion': self.controlador.realizar_interseccion,
            'concatenacion': self.controlador.realizar_concatenacion
        }

        resultado = operaciones[operacion](automata1, automata2)
        self.procesar_resultado(operacion, resultado)

    def realizar_operacion_unaria(self, operacion: str):
        index = self.combo_automata1.currentIndex()

        if index == -1:
            QMessageBox.warning(self, "Error", "Debe seleccionar un autómata")
            return

        automata = self.controlador.automatas_cargados[index]

        operaciones = {
            'complemento': self.controlador.realizar_complemento,
            'inverso': self.controlador.realizar_inverso,
            'completar': self.controlador.completar_automata
        }

        resultado = operaciones[operacion](automata)
        self.procesar_resultado(operacion, resultado)

    def procesar_resultado(self, operacion: str, resultado: Automata):
        if resultado:
            self.controlador.automatas_cargados.append(resultado)
            self.controlador.automata_actual = resultado
            self.actualizar_listas()
            self.combo_automatas.setCurrentIndex(len(self.controlador.automatas_cargados) - 1)
            self.resultado_operacion.setPlainText(f"Operación {operacion} completada con éxito")
            self.actualizar_visualizacion()

    def actualizar_visualizacion(self):
        if not self.controlador.automata_actual:
            return

        img_path = "temp_automata.png"

        try:
            self.controlador.graficar(img_path)
            if os.path.exists(img_path):
                pixmap = QPixmap(img_path)
                if (pixmap.width() > self.visor_automata.width() or
                        pixmap.height() > self.visor_automata.height()):
                    pixmap = pixmap.scaled(
                        self.visor_automata.width(),
                        self.visor_automata.height(),
                        Qt.KeepAspectRatio,
                        Qt.SmoothTransformation
                    )
                self.visor_automata.setPixmap(pixmap)
                os.remove(img_path)
        except Exception as e:
            # Mostrar un mensaje más específico con la cadena del error
            QMessageBox.warning(self, "Error", f"No se pudo generar la visualización: {str(e)}")
