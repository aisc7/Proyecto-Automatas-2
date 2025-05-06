from PySide6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton,
    QFileDialog, QMessageBox, QComboBox, QTabWidget, QGroupBox, QTextEdit
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
import json
import os
from modelo.automata import Automata
from controlador.controlador import Controlador

class VentanaPrincipal(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Operaciones con Autómatas")
        self.setMinimumSize(800, 600)
        self.controlador = Controlador()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        
        # Crear pestañas
        tabs = QTabWidget()
        
        # Pestaña 1: Cargar Autómatas
        tab_carga = QWidget()
        self.init_tab_carga(tab_carga)
        
        # Pestaña 2: Operaciones
        tab_operaciones = QWidget()
        self.init_tab_operaciones(tab_operaciones)
        
        # Pestaña 3: Visualización
        tab_visualizacion = QWidget()
        self.init_tab_visualizacion(tab_visualizacion)
        
        tabs.addTab(tab_carga, "Carga")
        tabs.addTab(tab_operaciones, "Operaciones")
        tabs.addTab(tab_visualizacion, "Visualización")
        
        layout.addWidget(tabs)
        self.setLayout(layout)

    def init_tab_carga(self, tab):
        layout = QHBoxLayout()
        
        panel_archivos = QGroupBox("Carga de Archivos")
        panel_archivos_layout = QVBoxLayout()
        
        btn_cargar = QPushButton("Cargar Autómata")
        btn_cargar.clicked.connect(self.cargar_json)
        panel_archivos_layout.addWidget(btn_cargar)
        
        self.combo_automatas = QComboBox()
        self.combo_automatas.currentIndexChanged.connect(self.seleccionar_automata)
        panel_archivos_layout.addWidget(QLabel("Autómatas cargados:"))
        panel_archivos_layout.addWidget(self.combo_automatas)
        
        panel_archivos.setLayout(panel_archivos_layout)
        layout.addWidget(panel_archivos)
        
        tab.setLayout(layout)

    def init_tab_operaciones(self, tab):
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
        
        btn_union = QPushButton("Unión (A ∪ B)")
        btn_union.clicked.connect(lambda: self.realizar_operacion('union'))
        
        btn_interseccion = QPushButton("Intersección (A ∩ B)")
        btn_interseccion.clicked.connect(lambda: self.realizar_operacion('interseccion'))
        
        btn_concatenacion = QPushButton("Concatenación (A.B)")
        btn_concatenacion.clicked.connect(lambda: self.realizar_operacion('concatenacion'))
        
        layout_binarias.addWidget(btn_union)
        layout_binarias.addWidget(btn_interseccion)
        layout_binarias.addWidget(btn_concatenacion)
        
        grupo_binarias.setLayout(layout_binarias)
        layout.addWidget(grupo_binarias)
        
        grupo_unarias = QGroupBox("Operaciones Unarias")
        layout_unarias = QHBoxLayout()
        
        btn_complemento = QPushButton("Complemento (A')")
        btn_complemento.clicked.connect(lambda: self.realizar_operacion('complemento'))
        
        btn_inverso = QPushButton("Inverso (A⁻¹)")
        btn_inverso.clicked.connect(lambda: self.realizar_operacion('inverso'))
        
        btn_completar = QPushButton("Completar Autómata")
        btn_completar.clicked.connect(lambda: self.realizar_operacion('completar'))
        
        layout_unarias.addWidget(btn_complemento)
        layout_unarias.addWidget(btn_inverso)
        layout_unarias.addWidget(btn_completar)
        
        grupo_unarias.setLayout(layout_unarias)
        layout.addWidget(grupo_unarias)
        
        self.resultado_operacion = QTextEdit()
        self.resultado_operacion.setReadOnly(True)
        layout.addWidget(QLabel("Resultado:"))
        layout.addWidget(self.resultado_operacion)
        
        tab.setLayout(layout)

    def init_tab_visualizacion(self, tab):
        layout = QVBoxLayout()
        
        self.visor_automata = QLabel()
        self.visor_automata.setAlignment(Qt.AlignCenter)
        self.visor_automata.setText("Visualización del autómata aparecerá aquí")
        
        btn_actualizar = QPushButton("Actualizar Visualización")
        btn_actualizar.clicked.connect(self.actualizar_visualizacion)
        
        layout.addWidget(self.visor_automata)
        layout.addWidget(btn_actualizar)
        
        tab.setLayout(layout)

    def actualizar_listas(self):
        self.combo_automatas.clear()
        self.combo_automata1.clear()
        self.combo_automata2.clear()
        
        for i, automata in enumerate(self.controlador.automatas_cargados):
            nombre = f"Autómata {i+1}"
            self.combo_automatas.addItem(nombre, i)
            self.combo_automata1.addItem(nombre, i)
            self.combo_automata2.addItem(nombre, i)

    def cargar_json(self):
        archivo, _ = QFileDialog.getOpenFileName(self, "Cargar JSON", "", "JSON (*.json)")
        if archivo:
            try:
                with open(archivo, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                if "estados" in data and isinstance(data["estados"], list) and all(isinstance(e, dict) and "nombre" in e for e in data["estados"]):
                    automata = self.convertir_formato_json(data)
                    self.controlador.automatas_cargados.append(automata)
                    self.controlador.automata_actual = automata
                else:
                    self.controlador.cargar_desde_archivo(archivo)
                
                self.actualizar_listas()
                self.mostrar_automata_actual()
                QMessageBox.information(self, "Éxito", "Autómata cargado correctamente")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo cargar el archivo:\n{str(e)}")

    def seleccionar_automata(self, index):
        if index >= 0:
            self.controlador.seleccionar_automata(index)
            self.mostrar_automata_actual()

    def mostrar_automata_actual(self):
        self.actualizar_visualizacion()

    def realizar_operacion(self, operacion):
        if operacion in ['union', 'interseccion', 'concatenacion']:
            index1 = self.combo_automata1.currentIndex()
            index2 = self.combo_automata2.currentIndex()
            
            if index1 == -1 or index2 == -1:
                QMessageBox.warning(self, "Error", "Debe seleccionar dos autómatas")
                return
                
            automata1 = self.controlador.automatas_cargados[index1]
            automata2 = self.controlador.automatas_cargados[index2]
            
            if operacion == 'union':
                resultado = self.controlador.realizar_union(automata1, automata2)
            elif operacion == 'interseccion':
                resultado = self.controlador.realizar_interseccion(automata1, automata2)
            elif operacion == 'concatenacion':
                resultado = self.controlador.realizar_concatenacion(automata1, automata2)
                
        elif operacion in ['complemento', 'inverso', 'completar']:
            index = self.combo_automata1.currentIndex()
            
            if index == -1:
                QMessageBox.warning(self, "Error", "Debe seleccionar un autómata")
                return
                
            automata = self.controlador.automatas_cargados[index]
            
            if operacion == 'complemento':
                resultado = self.controlador.realizar_complemento(automata)
            elif operacion == 'inverso':
                resultado = self.controlador.realizar_inverso(automata)
            elif operacion == 'completar':
                resultado = self.controlador.completar_automata(automata)
        
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
        self.controlador.graficar(img_path)
        
        if os.path.exists(img_path):
            pixmap = QPixmap(img_path)
            if pixmap.width() > self.visor_automata.width() or pixmap.height() > self.visor_automata.height():
                pixmap = pixmap.scaled(self.visor_automata.width(), self.visor_automata.height(), 
                                       Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.visor_automata.setPixmap(pixmap)
            os.remove(img_path)

    def convertir_formato_json(self, data):
        automata = Automata()
        automata.estados = []
        automata.estados_finales = []
        automata.transiciones = []
        
        for estado_obj in data["estados"]:
            nombre = estado_obj["nombre"]
            automata.estados.append(nombre)
            
            if estado_obj.get("inicial", False):
                automata.estado_inicial = nombre
            
            if estado_obj.get("final", False):
                automata.estados_finales.append(nombre)
            
            for trans in estado_obj.get("transiciones", []):
                automata.transiciones.append({
                    "origen": nombre,
                    "simbolo": trans["simbolo"],
                    "destino": trans["destino"]
                })
        
        return automata
