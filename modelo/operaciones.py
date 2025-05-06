from modelo.automata import Automata, Estado, Transicion

def union(a1: Automata, a2: Automata) -> Automata:
    nuevos_estados = []
    transiciones = []

    offset = len(a1.estados)
    for estado in a1.estados:
        nuevos_estados.append(estado)
    for estado in a2.estados:
        nuevos = Estado(
            nombre=estado.nombre + "_2",
            inicial=False,
            final=estado.final
        )
        nuevos_estados.append(nuevos)

    inicial = Estado("nuevo_inicial", inicial=True, final=False)
    nuevos_estados.append(inicial)

    for estado in nuevos_estados:
        if estado.inicial and estado.nombre != "nuevo_inicial":
            estado.inicial = False

    transiciones = list(a1.transiciones)
    transiciones += [
        Transicion("nuevo_inicial", e.nombre, "λ")
        for e in a1.estados if e.inicial
    ]
    transiciones += [
        Transicion("nuevo_inicial", e.nombre + "_2", "λ")
        for e in a2.estados if e.inicial
    ]
    for t in a2.transiciones:
        transiciones.append(
            Transicion(t.origen + "_2", t.destino + "_2", t.simbolo)
        )

    return Automata(nuevos_estados, transiciones)

def interseccion(a1: Automata, a2: Automata) -> Automata:
    nuevos_estados = []
    transiciones = []

    for e1 in a1.estados:
        for e2 in a2.estados:
            nombre = f"{e1.nombre}_{e2.nombre}"
            inicial = e1.inicial and e2.inicial
            final = e1.final and e2.final
            nuevos_estados.append(Estado(nombre, inicial=inicial, final=final))

    for t1 in a1.transiciones:
        for t2 in a2.transiciones:
            if t1.simbolo == t2.simbolo:
                origen = f"{t1.origen}_{t2.origen}"
                destino = f"{t1.destino}_{t2.destino}"
                transiciones.append(Transicion(origen, destino, t1.simbolo))

    return Automata(nuevos_estados, transiciones)

def concatenacion(a1: Automata, a2: Automata) -> Automata:
    nuevos_estados = []
    transiciones = []

    for e in a1.estados:
        nuevos_estados.append(Estado(e.nombre, inicial=e.inicial, final=False))

    for e in a2.estados:
        nombre = e.nombre + "_2"
        nuevos_estados.append(Estado(nombre, inicial=False, final=e.final))

    transiciones += a1.transiciones
    for t in a2.transiciones:
        transiciones.append(Transicion(t.origen + "_2", t.destino + "_2", t.simbolo))

    for e1 in a1.estados:
        if e1.final:
            for e2 in a2.estados:
                if e2.inicial:
                    transiciones.append(
                        Transicion(e1.nombre, e2.nombre + "_2", "λ")
                    )

    return Automata(nuevos_estados, transiciones)

def complemento(a: Automata) -> Automata:
    # Completamos el autómata y luego invertimos los estados finales
    a_completo = completar(a)
    nuevos_estados = []

    for e in a_completo.estados:
        nuevos_estados.append(
            Estado(
                e.nombre,
                inicial=e.inicial,
                final=not e.final
            )
        )

    return Automata(nuevos_estados, a_completo.transiciones)

def completar(a: Automata) -> Automata:
    simbolos = set(t.simbolo for t in a.transiciones if t.simbolo != "λ")
    estado_sumidero = Estado("sumidero", inicial=False, final=False)

    nuevos_estados = {e.nombre: Estado(e.nombre, e.inicial, e.final) for e in a.estados}
    nuevos_estados["sumidero"] = estado_sumidero
    nuevas_transiciones = list(a.transiciones)

    for estado in a.estados:
        transiciones_estado = [t.simbolo for t in a.transiciones if t.origen == estado.nombre]
        faltantes = simbolos - set(transiciones_estado)
        for simbolo in faltantes:
            nuevas_transiciones.append(Transicion(estado.nombre, "sumidero", simbolo))

    for simbolo in simbolos:
        nuevas_transiciones.append(Transicion("sumidero", "sumidero", simbolo))

    return Automata(list(nuevos_estados.values()), nuevas_transiciones)

def inverso(a: Automata) -> Automata:
    nuevos_estados = []
    nuevas_transiciones = []

    for e in a.estados:
        nuevos_estados.append(Estado(e.nombre, inicial=False, final=False))

    for t in a.transiciones:
        nuevas_transiciones.append(Transicion(t.destino, t.origen, t.simbolo))

    nuevos_iniciales = [e.nombre for e in a.estados if e.final]
    nuevos_finales = [e.nombre for e in a.estados if e.inicial]

    for estado in nuevos_estados:
        if estado.nombre in nuevos_iniciales:
            estado.inicial = True
        if estado.nombre in nuevos_finales:
            estado.final = True

    return Automata(nuevos_estados, nuevas_transiciones)
