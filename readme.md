# Proyecto: Operaciones y Visualización de Autómatas Finitos

## Descripción General

Este proyecto es una aplicación de escritorio desarrollada en Python con la librería PySide6 para la interfaz gráfica. Permite a los usuarios cargar, visualizar y realizar diversas operaciones fundamentales sobre autómatas finitos (AF). Los autómatas se definen y manipulan a través de archivos en formato JSON.

El objetivo principal es proporcionar una herramienta interactiva para experimentar con conceptos de la teoría de autómatas, como la unión, intersección, concatenación, complemento, inverso y la completitud de un autómata. Los resultados de estas operaciones, así como los autómatas cargados, pueden ser visualizados gráficamente.

## Características Principales

*   **Carga de Autómatas**: Importa definiciones de autómatas desde archivos JSON.
*   **Operaciones con Autómatas**:
    *   Unión de dos autómatas.
    *   Intersección de dos autómatas.
    *   Concatenación de dos autómatas.
    *   Complemento de un autómata.
    *   Inverso (o reverso) de un autómata.
    *   Completar un autómata (añadir estado sumidero y transiciones faltantes).
*   **Visualización Gráfica**: Muestra una representación visual del autómata actual o del resultado de una operación. La graficación se realiza utilizando la librería `graphviz`.
*   **Guardado de Resultados**: Los autómatas resultantes de las operaciones pueden ser guardados en formato JSON.
*   **Interfaz Intuitiva**: Organizada en pestañas para facilitar la navegación entre la carga de archivos, la selección de operaciones y la visualización.

## Estructura del Proyecto y Descripción Detallada de Archivos

El proyecto sigue una arquitectura que separa la interfaz de usuario (Vista), la lógica de la aplicación (Controlador) y la representación de los datos y operaciones (Modelo).

### 1. Archivo Principal de Ejecución

*   **`main.py`**:
    *   **Propósito**: Es el script que inicia la aplicación.
    *   **Detalles**:
        *   Importa las clases necesarias, incluyendo `QApplication` de PySide6 y `VentanaPrincipal` de la vista.
        *   En el bloque `if __name__ == "__main__":`, crea una instancia de `QApplication` (necesaria para cualquier aplicación Qt/PySide).
        *   Crea una instancia de `VentanaPrincipal`, que es la ventana principal de la GUI.
        *   Muestra la ventana (`ventana.show()`).
        *   Inicia el bucle de eventos de la aplicación (`app.exec()`), que espera interacciones del usuario hasta que la aplicación se cierra.

### 2. Vista (Interfaz de Usuario - Directorio: `vista/`)

*   **`vista/ventana_principal.py`**:
    *   **Propósito**: Define la clase `VentanaPrincipal`, que construye y gestiona todos los elementos de la interfaz gráfica.
    *   **Detalles**:
        *   Importa varios widgets de `PySide6.QtWidgets` (como `QWidget`, `QLabel`, `QPushButton`, `QTabWidget`, etc.) y `QPixmap` para manejar imágenes.
        *   Crea una instancia del `Controlador` para interactuar con la lógica de la aplicación.
        *   **Estructura de la GUI**:
            *   Utiliza un `QTabWidget` para dividir la interfaz en tres pestañas principales:
                1.  **Pestaña "Cargar Autómatas"**: Permite al usuario seleccionar archivos JSON de autómatas. Muestra los autómatas cargados en `QComboBox` para su selección.
                2.  **Pestaña "Operaciones"**: Permite al usuario seleccionar una operación (unión, intersección, etc.) y los autómatas operandos (de los cargados previamente). Un botón "Realizar Operación" ejecuta la acción.
                3.  **Pestaña "Visualizar Autómata"**: Muestra una imagen del autómata actualmente seleccionado o del resultado de la última operación. También puede mostrar mensajes de estado.
        *   **Manejo de Eventos**: Conecta las acciones del usuario (ej. clic en un botón) a métodos específicos (slots). Por ejemplo, el clic en "Cargar Archivo" abre un `QFileDialog`.
        *   **Comunicación con el Controlador**: Llama a métodos del `Controlador` para:
            *   Cargar un autómata (`controlador.cargar_desde_archivo`).
            *   Realizar una operación (`controlador.realizar_operacion` o métodos específicos como `controlador.realizar_union`).
            *   Obtener la imagen del autómata (`controlador.graficar`).
        *   **Actualización de la Vista**: Actualiza los `QComboBox` con los autómatas cargados y muestra la imagen del autómata en un `QLabel` (`self.visor_automata`).
        *   Utiliza una ruta temporal (`self.temp_img_path`) para guardar la imagen generada por `graphviz` antes de cargarla en el `QLabel`.

### 3. Controlador (Lógica de la Aplicación - Directorio: `controlador/`)

*   **`controlador/controlador.py`**:
    *   **Propósito**: Define la clase `Controlador`. Actúa como un puente entre la interfaz gráfica (Vista) y la lógica de negocio/datos (Modelo).
    *   **Detalles**:
        *   Mantiene una lista (`self.automatas_cargados`) de todos los objetos `Automata` que han sido cargados por el usuario.
        *   Mantiene una referencia al `self.automata_actual` que está siendo visualizado o utilizado en operaciones.
        *   **`cargar_desde_archivo(ruta)`**:
            *   Abre y lee el archivo JSON especificado por `ruta`.
            *   Llama a `Automata.desde_json(data)` para convertir los datos JSON en un objeto `Automata`.
            *   Añade el nuevo autómata a `self.automatas_cargados` y lo establece como `self.automata_actual`.
        *   **Métodos de Operaciones (ej. `realizar_union(a1, a2)`)**:
            *   Recibe los autómatas operandos.
            *   Llama a la función correspondiente en el módulo `modelo.operaciones` (ej. `operaciones.union(a1, a2)`).
            *   Devuelve el autómata resultante.
        *   **`realizar_operacion(tipo_operacion, a1, a2=None)`**: Un método unificado opcional que puede llamar a la operación correcta basándose en un string `tipo_operacion`.
        *   **`graficar(ruta_imagen)`**:
            *   Llama a la función `graficar_automata` del módulo `util.graficador`, pasándole el `self.automata_actual` y la `ruta_imagen` donde se guardará la imagen.

### 4. Modelo (Representación de Datos y Lógica del Dominio - Directorio: `modelo/`)

*   **`modelo/automata.py`**:
    *   **Propósito**: Define la clase `Automata`, la representación central de un autómata finito.
    *   **Atributos**:
        *   `estados`: Lista de objetos `Estado`.
        *   `alfabeto`: Lista de símbolos (strings) que componen el alfabeto del autómata.
        *   `transiciones`: Lista de objetos `Transicion`.
        *   `estado_inicial`: Objeto `Estado` que es el estado inicial.
        *   `estados_finales`: Lista de objetos `Estado` que son estados finales.
        *   `nombre`: Un string para identificar el autómata.
    *   **Métodos Clave**:
        *   `__init__(...)`: Constructor para inicializar un autómata con sus componentes.
        *   `a_json()`: Convierte el objeto `Automata` a un diccionario Python que puede ser fácilmente serializado a JSON. Es crucial para guardar autómatas.
        *   `desde_json(cls, data)`: Un método de clase (`@classmethod`) que toma un diccionario (deserializado de JSON) y construye un nuevo objeto `Automata` a partir de él. Es crucial para cargar autómatas.
        *   Los métodos `modeloA`, `asterisco`, `mas`, `concatenar`, `disyuncion` parecen ser parte de una implementación del algoritmo de Thompson para convertir expresiones regulares a AFN. Su integración con el sistema principal de operaciones (que opera sobre autómatas ya definidos) podría necesitar clarificación o refactorización si se pretende que sean usados por el usuario final directamente.

*   **`modelo/estado.py`**:
    *   **Propósito**: Define la clase `Estado`.
    *   **Atributos**:
        *   `nombre`: String identificador del estado (ej. "q0", "A").
        *   `es_inicial`: Booleano, `True` si es el estado inicial.
        *   `es_final`: Booleano, `True` si es un estado final.
    *   **Nota**: El atributo `transiciones` que originalmente podría haber contenido nombres de estados destino parece no ser la forma principal en que se manejan las transiciones para las operaciones y la serialización; esto se hace a través de la lista de objetos `Transicion` en la clase `Automata`.

*   **`modelo/transicion.py`**:
    *   **Propósito**: Define la clase `Transicion`.
    *   **Atributos**:
        *   `origen`: Objeto `Estado` desde el cual parte la transición.
        *   `destino`: Objeto `Estado` hacia el cual va la transición.
        *   `simbolo`: String que representa el símbolo que dispara esta transición.
    *   **Métodos Clave**:
        *   `to_dict()`: Convierte la transición a un diccionario (ej. `{"origen": "q0", "destino": "q1", "simbolo": "a"}`) para la serialización JSON.

*   **`modelo/operaciones.py`**:
    *   **Propósito**: Contiene la lógica algorítmica para cada una de las operaciones que se pueden realizar sobre los autómatas (unión, intersección, etc.).
    *   **Detalles**:
        *   Cada función (ej. `union(a1, a2)`) toma uno o dos objetos `Automata` como entrada.
        *   Construye un *nuevo* objeto `Automata` que representa el resultado de la operación. Esto implica:
            *   Crear nuevos estados (o copiar y adaptar los existentes).
            *   Definir las nuevas transiciones.
            *   Determinar el nuevo estado inicial.
            *   Determinar el nuevo conjunto de estados finales.
            *   Calcular el alfabeto del nuevo autómata.
            *   Asignar un nombre descriptivo al autómata resultante.
        *   Devuelve el nuevo objeto `Automata` completamente formado.
        *   Incluye una función auxiliar `_calcular_alfabeto_desde_transiciones` para derivar el alfabeto a partir de una lista de transiciones.

### 5. Utilidades (Funciones Auxiliares - Directorio: `util/`)

*   **`util/graficador.py`**:
    *   **Propósito**: Encapsula la lógica para generar una imagen de un autómata.
    *   **Detalles**:
        *   La función `graficar_automata(automata, nombre_salida)`:
            *   Toma un objeto `Automata`.
            *   Utiliza la librería `graphviz` (Python) para construir un objeto `Digraph`.
            *   Añade nodos al grafo para cada estado (círculos para estados normales, dobles círculos para finales, un punto de entrada para el inicial).
            *   Añade arcos (edges) al grafo para cada transición, etiquetados con el símbolo de la transición.
            *   Renderiza el grafo como un archivo de imagen (ej. PNG) en la ruta especificada por `nombre_salida`.
            *   **Importante**: Se ha modificado para *no* llamar a `dot.view()`, de modo que la imagen solo se guarda y no se abre automáticamente en un visor externo, permitiendo que la GUI la cargue internamente.

### 6. Recursos (Archivos de Ejemplo - Directorio: `recursos/`)

*   **`recursos/1automata.json`**:
    *   **Propósito**: Un archivo de ejemplo en formato JSON que define un autómata.
    *   **Uso**: Puede ser cargado en la aplicación para probar su funcionalidad.
    *   **Estructura JSON Esperada**:
        ```json
        {
          "nombre": "NombreOpcionalDelAutomata", // Opcional
          "alfabeto": ["0", "1"], // Opcional, puede ser derivado
          "estados": [
            {
              "nombre": "q0",
              "inicial": true,
              "final": false,
              "transiciones": [
                {"simbolo": "0", "destino": "q1"},
                {"simbolo": "1", "destino": "q0"}
              ]
            },
            {
              "nombre": "q1",
              "inicial": false,
              "final": true,
              "transiciones": [
                {"simbolo": "0", "destino": "q0"},
                {"simbolo": "1", "destino": "q1"}
              ]
            }
          ]
          // "estado_inicial": "q0", // Opcional si se usa "inicial": true en un estado
          // "estados_finales": ["q1"] // Opcional si se usa "final": true en estados
        }
        ```
        (Nota: La estructura exacta que tu `Automata.desde_json` espera debe ser consistente con esto).

*   **`recursos/2automata.json`**:
    *   **Propósito**: Otro archivo JSON de ejemplo, similar a `1automata.json`, para definir un autómata diferente.
    *   **Uso**: Para pruebas y demostración.

## Requisitos para la Ejecución

Para ejecutar este proyecto, necesitarás:

1.  **Python 3**: Preferiblemente una versión reciente (ej. 3.8+).
2.  **Librerías de Python**:
    *   **`PySide6`**: Para la interfaz gráfica de usuario. Puedes instalarla con pip:
        ```bash
        pip install PySide6
        ```
    *   **`graphviz`**: La librería de Python para interactuar con Graphviz. Puedes instalarla con pip:
        ```bash
        pip install graphviz
        ```
3.  **Software Graphviz**: La librería `graphviz` de Python es un *wrapper* alrededor del software Graphviz. Debes tener Graphviz instalado en tu sistema operativo y el ejecutable `dot` (parte de Graphviz) debe estar en el PATH de tu sistema.
    *   **Linux (Debian/Ubuntu)**: `sudo apt-get install graphviz`
    *   **macOS (usando Homebrew)**: `brew install graphviz`
    *   **Windows**: Descarga el instalador desde el [sitio oficial de Graphviz](https://graphviz.org/download/) y asegúrate de añadir el directorio `bin` de Graphviz a tu variable de entorno PATH.

## Cómo Ejecutar la Aplicación

1.  **Clona o descarga el proyecto** en tu máquina local.
2.  **Abre una terminal o línea de comandos**.
3.  **Navega al directorio raíz del proyecto** (donde se encuentra `main.py`).
4.  **Asegúrate de que todos los requisitos están instalados** (Python, PySide6, librería graphviz, software Graphviz).
5.  **Ejecuta el script principal**:
    ```bash
    python main.py
    ```
    o si tienes múltiples versiones de Python:
    ```bash
    python3 main.py
    ```

Esto debería lanzar la ventana principal de la aplicación, desde donde podrás cargar autómatas, realizar operaciones y visualizarlos.

## Flujo de Trabajo Típico del Usuario

1.  El usuario inicia la aplicación.
2.  Va a la pestaña "Cargar Autómatas".
3.  Hace clic en "Cargar Archivo" y selecciona un archivo `.json` que define un autómata (ej. `recursos/1automata.json`).
4.  Repite el paso 3 si desea cargar un segundo autómata para operaciones binarias.
5.  Los autómatas cargados aparecen en los `QComboBox` "Autómata 1" y "Autómata 2".
6.  El usuario va a la pestaña "Operaciones".
7.  Selecciona una operación del `QComboBox` de operaciones (ej. "Unión").
8.  Selecciona los autómatas operandos de los `QComboBox` correspondientes.
9.  Hace clic en "Realizar Operación".
10. El controlador llama a la función de operación apropiada en el modelo.
11. El autómata resultante se convierte en el "autómata actual".
12. La pestaña "Visualizar Autómata" se actualiza automáticamente (o el usuario navega a ella) para mostrar la imagen del autómata resultante.
13. El usuario puede optar por guardar el autómata resultante en un nuevo archivo JSON.