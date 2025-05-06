from PySide6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton,
    QFileDialog, QMessageBox, QComboBox, QTabWidget, QGroupBox, QTextEdit
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
from controlador.controlador import Controlador
from modelo.automata import Automata, Transicion
import json
import os
import tempfile

class VentanaPrincipal(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Operaciones con Autómatas")
        self.setMinimumSize(800, 600)
        self.controlador = Controlador()
        
        # Configuración de archivos temporales
        self.temp_dir = tempfile.mkdtemp()
        self.temp_img_path = os.path.join(self.temp_dir, "temp_automata.png")
        
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.tabs = QTabWidget()

        tab_carga = self.crear_tab_carga()
        tab_operaciones = self.crear_tab_operaciones()
        tab_visualizacion = self.crear_tab_visualizacion()

        self.tabs.addTab(tab_carga, "Carga")
        self.tabs.addTab(tab_operaciones, "Operaciones")
        self.tabs.addTab(tab_visualizacion, "Visualización")

        layout.addWidget(self.tabs)
        self.setLayout(layout)

    def crear_tab_carga(self):
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

    def crear_tab_operaciones(self):
        tab = QWidget()
        layout = QVBoxLayout()

        # Grupo de selección
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

        # Operaciones binarias
        grupo_binarias = QGroupBox("Operaciones Binarias")
        layout_binarias = QHBoxLayout()

        for texto, operacion in [
            ("Unión (A ∪ B)", 'union'),
            ("Intersección (A ∩ B)", 'interseccion'),
            ("Concatenación (A.B)", 'concatenacion')
        ]:
            btn = QPushButton(texto)
            btn.clicked.connect(lambda _, op=operacion: self.realizar_operacion(op))
            layout_binarias.addWidget(btn)

        grupo_binarias.setLayout(layout_binarias)
        layout.addWidget(grupo_binarias)

        # Operaciones unarias
        grupo_unarias = QGroupBox("Operaciones Unarias")
        layout_unarias = QHBoxLayout()

        for texto, operacion in [
            ("Complemento (A')", 'complemento'),
            ("Inverso (A⁻¹)", 'inverso'),
            ("Completar Autómata", 'completar')
        ]:
            btn = QPushButton(texto)
            btn.clicked.connect(lambda _, op=operacion: self.realizar_operacion(op))
            layout_unarias.addWidget(btn)

        grupo_unarias.setLayout(layout_unarias)
        layout.addWidget(grupo_unarias)

        # Resultado
        self.resultado_operacion = QTextEdit()
        self.resultado_operacion.setReadOnly(True)
        layout.addWidget(QLabel("Resultado:"))
        layout.addWidget(self.resultado_operacion)

        tab.setLayout(layout)
        return tab

    def crear_tab_visualizacion(self):
        tab = QWidget()
        layout = QVBoxLayout()

        self.visor_automata = QLabel()
        self.visor_automata.setAlignment(Qt.AlignCenter)
        self.visor_automata.setText("Visualización del autómata aparecerá aquí")
        
        self.estado_visualizacion = QLabel()
        self.estado_visualizacion.setAlignment(Qt.AlignCenter)

        btn_actualizar = QPushButton("Actualizar Visualización")
        btn_actualizar.clicked.connect(self.actualizar_visualizacion)

        layout.addWidget(self.visor_automata)
        layout.addWidget(self.estado_visualizacion)
        layout.addWidget(btn_actualizar)

        tab.setLayout(layout)
        return tab

    def actualizar_listas(self):
        self.combo_automatas.clear()
        self.combo_automata1.clear()
        self.combo_automata2.clear()

        for i, automata in enumerate(self.controlador.automatas_cargados):
            nombre = f"Autómata {i+1}: {automata.nombre or 'Sin nombre'}"
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

            automata = Automata.desde_json(datos)
            
            if automata:
                self.controlador.automatas_cargados.append(automata)
                self.controlador.automata_actual = automata
                self.actualizar_listas()
                self.combo_automatas.setCurrentIndex(len(self.controlador.automatas_cargados) - 1)
                QMessageBox.information(self, "Éxito", "Autómata cargado correctamente")
                self.actualizar_visualizacion()
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo cargar el archivo:\n{str(e)}")

    def seleccionar_automata(self, index):
        if index >= 0 and self.controlador.seleccionar_automata(index):
            self.actualizar_visualizacion()

    def realizar_operacion(self, operacion):
        try:
            if operacion in ['union', 'interseccion', 'concatenacion']:
                self.realizar_operacion_binaria(operacion)
            else:
                self.realizar_operacion_unaria(operacion)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al realizar operación:\n{str(e)}")

    def realizar_operacion_binaria(self, operacion):
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
        else:
            return

        self.procesar_resultado(operacion, resultado)

    def realizar_operacion_unaria(self, operacion):
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
        else:
            return

        self.procesar_resultado(operacion, resultado)

# ...existing code...
    def procesar_resultado(self, operacion, resultado):
        if not resultado:
            return

        self.controlador.automatas_cargados.append(resultado)
        self.controlador.automata_actual = resultado
        
        self.actualizar_listas()
        self.combo_automatas.setCurrentIndex(len(self.controlador.automatas_cargados) - 1)
        self.resultado_operacion.setPlainText(f"Operación {operacion} completada con éxito")
        
        nombre_archivo = f"{operacion}_resultado.json"
        try:
            print(f"\n--- Inspeccionando autómata ANTES de a_json() para operación: {operacion} ---")
            print(f"Nombre del autómata resultado: {resultado.nombre}")
            print(f"Alfabeto: {resultado.alfabeto}, Tipo: {type(resultado.alfabeto)}")
            print(f"Estado inicial: {resultado.estado_inicial.nombre if resultado.estado_inicial else 'None'}")
            print(f"Número de estados: {len(resultado.estados)}")
            print("Detalle de Estados:")
            for i_est, est in enumerate(resultado.estados):
                print(f"  Estado [{i_est}]: Nombre='{est.nombre}', Inicial={est.es_inicial}, Final={est.es_final}, Tipo={type(est)}")
            
            print(f"Número de transiciones globales en autómata resultado: {len(resultado.transiciones)}")
            print("Detalle de Transiciones Globales del Autómata (self.transiciones):")
            if resultado.transiciones:
                for i_trans, trans_obj in enumerate(resultado.transiciones):
                    print(f"  Transición Global [{i_trans}]:")
                    print(f"    Tipo de trans_obj: {type(trans_obj)}")
                    if isinstance(trans_obj, Transicion): 
                        origen_info = "Origen NULO o sin nombre"
                        if trans_obj.origen and hasattr(trans_obj.origen, 'nombre'):
                            origen_info = f"'{trans_obj.origen.nombre}' (Tipo: {type(trans_obj.origen)})"
                        elif trans_obj.origen:
                             origen_info = f"Origen SIN NOMBRE (Tipo: {type(trans_obj.origen)})"
                        print(f"    Origen: {origen_info}")

                        destino_info = "Destino NULO o sin nombre"
                        if trans_obj.destino and hasattr(trans_obj.destino, 'nombre'):
                            destino_info = f"'{trans_obj.destino.nombre}' (Tipo: {type(trans_obj.destino)})"
                        elif trans_obj.destino:
                            destino_info = f"Destino SIN NOMBRE (Tipo: {type(trans_obj.destino)})"
                        print(f"    Destino: {destino_info}")
                        print(f"    Símbolo: '{trans_obj.simbolo}'")
                        if hasattr(trans_obj, 'to_dict') and callable(getattr(trans_obj, 'to_dict')):
                            try:
                                print(f"    to_dict() output: {trans_obj.to_dict()}")
                            except Exception as e_todict:
                                print(f"    ERROR al llamar a to_dict(): {e_todict}")
                        else:
                            print(f"    ADVERTENCIA: trans_obj NO tiene un método to_dict() callable.")
                    else:
                        print(f"    ADVERTENCIA: trans_obj NO es instancia de Transicion. Es {type(trans_obj)}")
            else:
                print("  No hay transiciones globales en el autómata resultado.")
            print("--- Fin inspección ANTES de a_json() ---\n")
        except Exception as e:
            print(f"Error durante la inspección del autómata: {e}")

            datos_json = resultado.a_json() 
            
            print(f"\n--- Inspeccionando datos_json DESPUÉS de a_json() para operación: {operacion} ---")
            if isinstance(datos_json, dict):
                print("datos_json es un diccionario.")
                if "estados" in datos_json and isinstance(datos_json["estados"], list):
                    print(f"Número de estados en datos_json: {len(datos_json['estados'])}")
                    for i_est_json, estado_json_dict in enumerate(datos_json["estados"]):
                        print(f"  Estado JSON [{i_est_json}]:")
                        if isinstance(estado_json_dict, dict) and "transiciones" in estado_json_dict and isinstance(estado_json_dict["transiciones"], list):
                            print(f"    Número de transiciones en JSON para este estado: {len(estado_json_dict['transiciones'])}")
                            for i_trans_json, trans_json_item in enumerate(estado_json_dict["transiciones"]):
                                print(f"      Transición JSON [{i_trans_json}]: Tipo={type(trans_json_item)}, Contenido={trans_json_item}")
                                if not isinstance(trans_json_item, dict):
                                    print(f"        ¡¡¡ADVERTENCIA!!! Esta transición en datos_json NO es un diccionario.")
                        else:
                            print(f"    ADVERTENCIA: estado_json_dict['transiciones'] no es una lista o estado_json_dict no es un dict.")
                else:
                    print("    ADVERTENCIA: datos_json['estados'] no es una lista o no existe.")
            else:
                print(f"ADVERTENCIA: datos_json NO es un diccionario. Es {type(datos_json)}")
            print("--- Fin inspección DESPUÉS de a_json() ---\n")

            with open(nombre_archivo, 'w', encoding='utf-8') as f:
                json.dump(datos_json, f, ensure_ascii=False, indent=4) 

    
    def actualizar_visualizacion(self):
        if not self.controlador.automata_actual:
            self.visor_automata.setText("No hay autómata seleccionado")
            self.estado_visualizacion.clear()
            return

        try:
            # Generar la imagen usando el método graficar() del controlador
            self.controlador.graficar(self.temp_img_path)
            
            if os.path.exists(self.temp_img_path):
                pixmap = QPixmap(self.temp_img_path)
                
                # Escalar si es necesario
                if (pixmap.width() > self.visor_automata.width() or 
                    pixmap.height() > self.visor_automata.height()):
                    pixmap = pixmap.scaled(
                        self.visor_automata.width(),
                        self.visor_automata.height(),
                        Qt.KeepAspectRatio,
                        Qt.SmoothTransformation
                    )
                
                self.visor_automata.setPixmap(pixmap)
                nombre = self.controlador.automata_actual.nombre or "Autómata actual"
                self.estado_visualizacion.setText(f"Visualizando: {nombre}")
                
        except Exception as e:
            self.visor_automata.setText("Error al visualizar el autómata")
            self.estado_visualizacion.setText(f"Error: {str(e)}")
            QMessageBox.warning(self, "Error", f"No se pudo generar la visualización: {str(e)}")

    def closeEvent(self, event):
        """Limpiar archivos temporales al cerrar la aplicación"""
        try:
            if os.path.exists(self.temp_img_path):
                os.remove(self.temp_img_path)
            if os.path.exists(self.temp_dir):
                os.rmdir(self.temp_dir)
        except Exception:
            pass
        
        super().closeEvent(event)