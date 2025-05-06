from graphviz import Digraph

def graficar_automata(automata, nombre_salida="automata"):
    dot = Digraph()

    # Crear nodos para los estados
    for estado in automata.estados:
        shape = "doublecircle" if estado in automata.estados_finales else "circle"
        dot.node(estado, shape=shape)

    # Nodo inicial (punto ficticio)
    if automata.estado_inicial:
        dot.node("ini", shape="point")
        dot.edge("ini", automata.estado_inicial)

    # Agregar transiciones
    for trans in automata.transiciones:
        origen = trans["origen"]
        destino = trans["destino"]
        simbolo = trans["simbolo"]
        dot.edge(origen, destino, label=simbolo)

    dot.render(nombre_salida, format="png", cleanup=True)
