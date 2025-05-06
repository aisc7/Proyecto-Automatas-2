from modelo.automata import Automata, Estado, Transicion

def union(a1: Automata, a2: Automata) -> Automata:
    nuevos_estados = []
    transiciones = []
    estado_dict = {}  # Diccionario para mapear nombres a objetos Estado

    # Copiar estados de a1
    for estado in a1.estados:
        nuevo_estado = Estado(estado.nombre, es_inicial=estado.es_inicial, es_final=estado.es_final)
        nuevos_estados.append(nuevo_estado)
        estado_dict[estado.nombre] = nuevo_estado

    # Copiar estados de a2, renombrando
    for estado in a2.estados:
        nuevo_nombre = estado.nombre + "_2"
        nuevo_estado = Estado(nuevo_nombre, es_inicial=estado.es_inicial, es_final=estado.es_final)
        nuevos_estados.append(nuevo_estado)
        estado_dict[nuevo_nombre] = nuevo_estado

    # Crear nuevo estado inicial
    inicial = Estado("nuevo_inicial", es_inicial=True, es_final=False)
    nuevos_estados.append(inicial)
    estado_dict["nuevo_inicial"] = inicial

    # Desactivar otros iniciales
    for estado in nuevos_estados:
        if estado.es_inicial and estado.nombre != "nuevo_inicial":
            estado.es_inicial = False

    # Copiar transiciones de a1
    for t in a1.transiciones:
        origen = estado_dict[t.origen.nombre if isinstance(t.origen, Estado) else t.origen]
        destino = estado_dict[t.destino.nombre if isinstance(t.destino, Estado) else t.destino]
        transiciones.append(Transicion(origen, destino, t.simbolo))

    # Agregar transiciones lambda desde el nuevo estado inicial
    for e in a1.estados:
        if e.es_inicial:
            transiciones.append(
                Transicion(estado_dict["nuevo_inicial"], estado_dict[e.nombre], "λ")
            )
    
    for e in a2.estados:
        if e.es_inicial:
            transiciones.append(
                Transicion(estado_dict["nuevo_inicial"], estado_dict[e.nombre + "_2"], "λ")
            )

    # Copiar transiciones de a2 con nombres modificados
    for t in a2.transiciones:
        origen_nombre = t.origen.nombre if isinstance(t.origen, Estado) else t.origen
        destino_nombre = t.destino.nombre if isinstance(t.destino, Estado) else t.destino
        
        origen = estado_dict[origen_nombre + "_2"]
        destino = estado_dict[destino_nombre + "_2"]
        
        transiciones.append(Transicion(origen, destino, t.simbolo))

    return Automata(nuevos_estados, transiciones)

def interseccion(a1: Automata, a2: Automata) -> Automata:
    nuevos_estados = []
    transiciones = []
    estado_dict = {}  # Diccionario para mapear nombres a objetos Estado

    # Crear estados para el producto cartesiano
    for e1 in a1.estados:
        for e2 in a2.estados:
            nombre = f"{e1.nombre}_{e2.nombre}"
            es_inicial = e1.es_inicial and e2.es_inicial
            es_final = e1.es_final and e2.es_final
            nuevo_estado = Estado(nombre, es_inicial=es_inicial, es_final=es_final)
            nuevos_estados.append(nuevo_estado)
            estado_dict[nombre] = nuevo_estado

    # Crear transiciones
    for t1 in a1.transiciones:
        for t2 in a2.transiciones:
            if t1.simbolo == t2.simbolo:
                origen_nombre1 = t1.origen.nombre if isinstance(t1.origen, Estado) else t1.origen
                destino_nombre1 = t1.destino.nombre if isinstance(t1.destino, Estado) else t1.destino
                origen_nombre2 = t2.origen.nombre if isinstance(t2.origen, Estado) else t2.origen
                destino_nombre2 = t2.destino.nombre if isinstance(t2.destino, Estado) else t2.destino
                
                origen = estado_dict.get(f"{origen_nombre1}_{origen_nombre2}")
                destino = estado_dict.get(f"{destino_nombre1}_{destino_nombre2}")
                
                if origen and destino:
                    transiciones.append(Transicion(origen, destino, t1.simbolo))

    return Automata(nuevos_estados, transiciones)

def concatenacion(a1: Automata, a2: Automata) -> Automata:
    nuevos_estados = []
    transiciones = []
    estado_dict = {}  # Diccionario para mapear nombres a objetos Estado

    # Copiar estados de a1 (finales se vuelven no finales)
    for e in a1.estados:
        nuevo_estado = Estado(e.nombre, es_inicial=e.es_inicial, es_final=False)
        nuevos_estados.append(nuevo_estado)
        estado_dict[e.nombre] = nuevo_estado

    # Copiar estados de a2 (iniciales se vuelven no iniciales)
    for e in a2.estados:
        nombre = e.nombre + "_2"
        nuevo_estado = Estado(nombre, es_inicial=False, es_final=e.es_final)
        nuevos_estados.append(nuevo_estado)
        estado_dict[nombre] = nuevo_estado

    # Copiar transiciones de a1
    for t in a1.transiciones:
        origen_nombre = t.origen.nombre if isinstance(t.origen, Estado) else t.origen
        destino_nombre = t.destino.nombre if isinstance(t.destino, Estado) else t.destino
        
        origen = estado_dict.get(origen_nombre)
        destino = estado_dict.get(destino_nombre)
        
        if origen and destino:
            transiciones.append(Transicion(origen, destino, t.simbolo))

    # Copiar transiciones de a2
    for t in a2.transiciones:
        origen_nombre = t.origen.nombre if isinstance(t.origen, Estado) else t.origen
        destino_nombre = t.destino.nombre if isinstance(t.destino, Estado) else t.destino
        
        origen = estado_dict.get(origen_nombre + "_2")
        destino = estado_dict.get(destino_nombre + "_2")
        
        if origen and destino:
            transiciones.append(Transicion(origen, destino, t.simbolo))

    # Agregar transiciones lambda desde estados finales de a1 a estados iniciales de a2
    for e1 in a1.estados:
        if e1.es_final:
            for e2 in a2.estados:
                if e2.es_inicial:
                    transiciones.append(
                        Transicion(estado_dict[e1.nombre], estado_dict[e2.nombre + "_2"], "λ")
                    )

    return Automata(nuevos_estados, transiciones)

def complemento(a: Automata) -> Automata:
    a_completo = completar(a)
    nuevos_estados = []
    estado_dict = {}  # Diccionario para mapear nombres a objetos Estado

    # Invertir estados finales/no finales
    for e in a_completo.estados:
        nuevo_estado = Estado(
            e.nombre,
            es_inicial=e.es_inicial,
            es_final=not e.es_final
        )
        nuevos_estados.append(nuevo_estado)
        estado_dict[e.nombre] = nuevo_estado

    # Copiar transiciones con los nuevos objetos Estado
    nuevas_transiciones = []
    for t in a_completo.transiciones:
        origen_nombre = t.origen.nombre if isinstance(t.origen, Estado) else t.origen
        destino_nombre = t.destino.nombre if isinstance(t.destino, Estado) else t.destino
        
        origen = estado_dict.get(origen_nombre)
        destino = estado_dict.get(destino_nombre)
        
        if origen and destino:
            nuevas_transiciones.append(Transicion(origen, destino, t.simbolo))

    return Automata(nuevos_estados, nuevas_transiciones)

def completar(a: Automata) -> Automata:
    # Obtener alfabeto
    simbolos = set(t.simbolo for t in a.transiciones if t.simbolo != "λ")
    
    # Crear estados
    nuevos_estados = []
    estado_dict = {}  # Diccionario para mapear nombres a objetos Estado
    
    for e in a.estados:
        nuevo_estado = Estado(e.nombre, es_inicial=e.es_inicial, es_final=e.es_final)
        nuevos_estados.append(nuevo_estado)
        estado_dict[e.nombre] = nuevo_estado
    
    # Crear estado sumidero
    estado_sumidero = Estado("sumidero", es_inicial=False, es_final=False)
    nuevos_estados.append(estado_sumidero)
    estado_dict["sumidero"] = estado_sumidero
    
    # Copiar transiciones existentes
    nuevas_transiciones = []
    for t in a.transiciones:
        origen_nombre = t.origen.nombre if isinstance(t.origen, Estado) else t.origen
        destino_nombre = t.destino.nombre if isinstance(t.destino, Estado) else t.destino
        
        origen = estado_dict.get(origen_nombre)
        destino = estado_dict.get(destino_nombre)
        
        if origen and destino:
            nuevas_transiciones.append(Transicion(origen, destino, t.simbolo))
    
    # Agregar transiciones faltantes hacia el estado sumidero
    for estado in a.estados:
        estado_nombre = estado.nombre
        # Encontrar símbolos que ya tienen transiciones desde este estado
        transiciones_estado = [t.simbolo for t in a.transiciones 
                              if (t.origen == estado or t.origen == estado_nombre)]
        # Agregar transiciones para símbolos faltantes
        faltantes = simbolos - set(transiciones_estado)
        for simbolo in faltantes:
            nuevas_transiciones.append(
                Transicion(estado_dict[estado_nombre], estado_dict["sumidero"], simbolo)
            )
    
    # Agregar transiciones del sumidero a sí mismo para todos los símbolos
    for simbolo in simbolos:
        nuevas_transiciones.append(
            Transicion(estado_dict["sumidero"], estado_dict["sumidero"], simbolo)
        )

    return Automata(nuevos_estados, nuevas_transiciones)

def inverso(a: Automata) -> Automata:
    nuevos_estados = []
    estado_dict = {}  # Diccionario para mapear nombres a objetos Estado
    
    # Crear nuevos estados (sin iniciales/finales por ahora)
    for e in a.estados:
        nuevo_estado = Estado(e.nombre, es_inicial=False, es_final=False)
        nuevos_estados.append(nuevo_estado)
        estado_dict[e.nombre] = nuevo_estado
    
    # Invertir iniciales y finales
    nuevos_iniciales = [e.nombre for e in a.estados if e.es_final]
    nuevos_finales = [e.nombre for e in a.estados if e.es_inicial]
    
    for estado in nuevos_estados:
        if estado.nombre in nuevos_iniciales:
            estado.es_inicial = True
        if estado.nombre in nuevos_finales:
            estado.es_final = True
    
    # Invertir transiciones
    nuevas_transiciones = []
    for t in a.transiciones:
        origen_nombre = t.origen.nombre if isinstance(t.origen, Estado) else t.origen
        destino_nombre = t.destino.nombre if isinstance(t.destino, Estado) else t.destino
        
        # Invertir: el destino se convierte en origen y viceversa
        origen = estado_dict.get(destino_nombre)
        destino = estado_dict.get(origen_nombre)
        
        if origen and destino:
            nuevas_transiciones.append(Transicion(origen, destino, t.simbolo))

    return Automata(nuevos_estados, nuevas_transiciones)