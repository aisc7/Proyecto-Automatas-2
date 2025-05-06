from graphviz import Digraph

def graficar_automata(automata, nombre_salida="automata"):
    dot = Digraph()

    # Nodo inicial ficticio
    if automata.estado_inicial:
        dot.node("ini", shape="point")
        dot.edge("ini", automata.estado_inicial.nombre)

    for estado in automata.estados:
        shape = "doublecircle" if estado.es_final else "circle"
        color = "lightblue" if estado.es_inicial else "black"
        dot.node(estado.nombre, shape=shape, color=color)

    for trans in automata.transiciones:
        dot.edge(trans.origen.nombre, trans.destino.nombre, label=trans.simbolo)

    dot.render(nombre_salida, format="png", cleanup=True)
    dot.view()
