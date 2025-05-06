from graphviz import Digraph

def graficar_automata(automata, nombre_salida="automata"):
    dot = Digraph()

    # Crear nodos para los estados
    for estado in automata.estados:
        # Usamos el nombre del estado, no el objeto estado
        shape = "doublecircle" if estado in automata.estados_finales else "circle"
        dot.node(estado.nombre, shape=shape)  # Aquí usamos estado.nombre

    # Nodo inicial (punto ficticio)
    if automata.estado_inicial:
        dot.node("ini", shape="point")
        dot.edge("ini", automata.estado_inicial.nombre)  # Aquí usamos estado_inicial.nombre

    # Agregar transiciones
    for trans in automata.transiciones:
        origen = trans.origen.nombre  # Aquí usamos trans.origen.nombre
        destino = trans.destino.nombre  # Aquí usamos trans.destino.nombre
        simbolo = trans.simbolo
        dot.edge(origen, destino, label=simbolo)

    # Renderiza el gráfico y lo guarda como archivo PNG
    dot.render(nombre_salida, format="png", cleanup=True)
