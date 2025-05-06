from modelo.automata import Automata, Estado, Transicion
from typing import List, Set, Optional

def _calcular_alfabeto_desde_transiciones(transiciones: List[Transicion]) -> List[str]:
    """Calcula el alfabeto (lista ordenada de símbolos) a partir de una lista de transiciones."""
    alfabeto_set: Set[str] = set()
    for t in transiciones:
        if t.simbolo != "λ":  # Asumiendo "λ" como epsilon y no parte del alfabeto formal
            alfabeto_set.add(t.simbolo)
    return sorted(list(alfabeto_set))

def union(a1: Automata, a2: Automata) -> Automata:
    nuevos_estados: List[Estado] = []
    transiciones_union: List[Transicion] = []
    estado_dict = {} # Mapea nombres originales a nuevos objetos Estado

    # Copiar estados de a1 (marcando como no iniciales/finales temporalmente)
    for estado_orig in a1.estados:
        nuevo_estado = Estado(estado_orig.nombre, es_inicial=False, es_final=estado_orig.es_final)
        nuevos_estados.append(nuevo_estado)
        estado_dict[estado_orig.nombre] = nuevo_estado

    # Copiar estados de a2, renombrando (marcando como no iniciales/finales temporalmente)
    for estado_orig in a2.estados:
        nombre_nuevo_a2 = estado_orig.nombre + "_union_a2"
        nuevo_estado = Estado(nombre_nuevo_a2, es_inicial=False, es_final=estado_orig.es_final)
        nuevos_estados.append(nuevo_estado)
        estado_dict[nombre_nuevo_a2] = nuevo_estado # Usar el nuevo nombre como clave

    # Crear nuevo estado inicial para la unión
    estado_inicial_union = Estado("S_union_inicial", es_inicial=True, es_final=False)
    nuevos_estados.append(estado_inicial_union)

    # Copiar transiciones de a1, usando los nuevos objetos Estado
    for t_orig in a1.transiciones:
        origen_obj = estado_dict.get(t_orig.origen.nombre)
        destino_obj = estado_dict.get(t_orig.destino.nombre)
        if origen_obj and destino_obj:
            transiciones_union.append(Transicion(origen_obj, destino_obj, t_orig.simbolo))

    # Copiar transiciones de a2, usando los nuevos objetos Estado (con nombres renombrados)
    for t_orig in a2.transiciones:
        origen_obj = estado_dict.get(t_orig.origen.nombre + "_union_a2")
        destino_obj = estado_dict.get(t_orig.destino.nombre + "_union_a2")
        if origen_obj and destino_obj:
            transiciones_union.append(Transicion(origen_obj, destino_obj, t_orig.simbolo))

    # Conectar el nuevo estado inicial de la unión a los antiguos estados iniciales de a1 y a2
    if a1.estado_inicial:
        antiguo_inicial_a1_obj = estado_dict.get(a1.estado_inicial.nombre)
        if antiguo_inicial_a1_obj:
            transiciones_union.append(Transicion(estado_inicial_union, antiguo_inicial_a1_obj, "λ"))
    
    if a2.estado_inicial:
        antiguo_inicial_a2_obj = estado_dict.get(a2.estado_inicial.nombre + "_union_a2")
        if antiguo_inicial_a2_obj:
            transiciones_union.append(Transicion(estado_inicial_union, antiguo_inicial_a2_obj, "λ"))
    
    alfabeto_calculado = _calcular_alfabeto_desde_transiciones(transiciones_union)
    
    # Los estados finales son aquellos que eran finales en a1 o a2 (ya copiados con su es_final)
    estados_finales_union = [e for e in nuevos_estados if e.es_final and e != estado_inicial_union]

    nombre_union = f"Union({a1.nombre or 'A1'}, {a2.nombre or 'A2'})"

    return Automata(
        estados=nuevos_estados,
        alfabeto=alfabeto_calculado,
        transiciones=transiciones_union,
        estado_inicial=estado_inicial_union,
        estados_finales=estados_finales_union,
        nombre=nombre_union
    )

def interseccion(a1: Automata, a2: Automata) -> Automata:
    nuevos_estados: List[Estado] = []
    transiciones_interseccion: List[Transicion] = []
    estado_dict_prod = {} # Mapea tupla de nombres originales (n1, n2) a nuevo objeto Estado producto
    
    estado_inicial_interseccion: Optional[Estado] = None
    estados_finales_interseccion: List[Estado] = []

    # Crear estados producto (e1, e2)
    for e1 in a1.estados:
        for e2 in a2.estados:
            nombre_prod = f"({e1.nombre},{e2.nombre})"
            es_inicial_prod = e1.es_inicial and e2.es_inicial
            es_final_prod = e1.es_final and e2.es_final
            
            nuevo_estado_prod = Estado(nombre_prod, es_inicial=es_inicial_prod, es_final=es_final_prod)
            nuevos_estados.append(nuevo_estado_prod)
            estado_dict_prod[(e1.nombre, e2.nombre)] = nuevo_estado_prod
            
            if es_inicial_prod:
                estado_inicial_interseccion = nuevo_estado_prod
            if es_final_prod:
                estados_finales_interseccion.append(nuevo_estado_prod)

    # Crear transiciones para el producto
    for e1_origen in a1.estados:
        for e2_origen in a2.estados:
            estado_origen_prod_obj = estado_dict_prod.get((e1_origen.nombre, e2_origen.nombre))
            if not estado_origen_prod_obj:
                continue

            for t1 in a1.transiciones:
                if t1.origen == e1_origen: # Transición desde e1_origen
                    for t2 in a2.transiciones:
                        if t2.origen == e2_origen and t1.simbolo == t2.simbolo: # Transición desde e2_origen con mismo símbolo
                            e1_destino = t1.destino
                            e2_destino = t2.destino
                            estado_destino_prod_obj = estado_dict_prod.get((e1_destino.nombre, e2_destino.nombre))
                            if estado_destino_prod_obj:
                                transiciones_interseccion.append(
                                    Transicion(estado_origen_prod_obj, estado_destino_prod_obj, t1.simbolo)
                                )
    
    alfabeto_calculado = _calcular_alfabeto_desde_transiciones(transiciones_interseccion)
    nombre_interseccion = f"Interseccion({a1.nombre or 'A1'}, {a2.nombre or 'A2'})"

    return Automata(
        estados=nuevos_estados,
        alfabeto=alfabeto_calculado,
        transiciones=transiciones_interseccion,
        estado_inicial=estado_inicial_interseccion,
        estados_finales=estados_finales_interseccion,
        nombre=nombre_interseccion
    )

def concatenacion(a1: Automata, a2: Automata) -> Automata:
    nuevos_estados: List[Estado] = []
    transiciones_concat: List[Transicion] = []
    estado_dict = {} # Mapea nombres originales a nuevos objetos Estado

    estado_inicial_concat: Optional[Estado] = None
    estados_finales_concat: List[Estado] = []

    # Copiar estados de a1
    for e_orig in a1.estados:
        # El estado inicial de a1 es el inicial de la concatenación.
        # Los finales de a1 dejan de serlo (se conectarán a los iniciales de a2).
        es_inicial_nuevo = e_orig.es_inicial 
        nuevo_estado = Estado(e_orig.nombre, es_inicial=es_inicial_nuevo, es_final=False)
        nuevos_estados.append(nuevo_estado)
        estado_dict[e_orig.nombre] = nuevo_estado
        if es_inicial_nuevo:
            estado_inicial_concat = nuevo_estado
    
    # Copiar estados de a2, renombrando
    for e_orig in a2.estados:
        nombre_nuevo_a2 = e_orig.nombre + "_concat_a2"
        # Los iniciales de a2 dejan de serlo (se conectan desde los finales de a1).
        # Los finales de a2 son los finales de la concatenación.
        es_final_nuevo = e_orig.es_final
        nuevo_estado = Estado(nombre_nuevo_a2, es_inicial=False, es_final=es_final_nuevo)
        nuevos_estados.append(nuevo_estado)
        estado_dict[nombre_nuevo_a2] = nuevo_estado
        if es_final_nuevo:
            estados_finales_concat.append(nuevo_estado)

    # Copiar transiciones de a1
    for t_orig in a1.transiciones:
        origen_obj = estado_dict.get(t_orig.origen.nombre)
        destino_obj = estado_dict.get(t_orig.destino.nombre)
        if origen_obj and destino_obj:
            transiciones_concat.append(Transicion(origen_obj, destino_obj, t_orig.simbolo))

    # Copiar transiciones de a2
    for t_orig in a2.transiciones:
        origen_obj = estado_dict.get(t_orig.origen.nombre + "_concat_a2")
        destino_obj = estado_dict.get(t_orig.destino.nombre + "_concat_a2")
        if origen_obj and destino_obj:
            transiciones_concat.append(Transicion(origen_obj, destino_obj, t_orig.simbolo))

    # Conectar los que eran finales en a1 con los que eran iniciales en a2
    for e1_orig in a1.estados:
        if e1_orig.es_final: # Si el estado original en a1 era final
            estado_final_a1_copiado = estado_dict.get(e1_orig.nombre)
            if estado_final_a1_copiado:
                for e2_orig in a2.estados:
                    if e2_orig.es_inicial: # Si el estado original en a2 era inicial
                        estado_inicial_a2_copiado = estado_dict.get(e2_orig.nombre + "_concat_a2")
                        if estado_inicial_a2_copiado:
                            transiciones_concat.append(
                                Transicion(estado_final_a1_copiado, estado_inicial_a2_copiado, "λ")
                            )
    
    alfabeto_calculado = _calcular_alfabeto_desde_transiciones(transiciones_concat)
    nombre_concat = f"Concatenacion({a1.nombre or 'A1'}, {a2.nombre or 'A2'})"

    return Automata(
        estados=nuevos_estados,
        alfabeto=alfabeto_calculado,
        transiciones=transiciones_concat,
        estado_inicial=estado_inicial_concat,
        estados_finales=estados_finales_concat,
        nombre=nombre_concat
    )

def completar(a: Automata) -> Automata:
    nuevos_estados: List[Estado] = []
    transiciones_completas: List[Transicion] = []
    estado_dict = {}

    # Usar el alfabeto del autómata original si está definido y es una lista/set, sino calcularlo
    alfabeto_original_simbolos: Set[str] = set()
    if isinstance(a.alfabeto, (list, set)):
        for sym in a.alfabeto:
            if isinstance(sym, str):
                alfabeto_original_simbolos.add(sym)
    if not alfabeto_original_simbolos: # Si a.alfabeto no era útil, calcular de transiciones
         for t in a.transiciones:
            if t.simbolo != "λ":
                alfabeto_original_simbolos.add(t.simbolo)


    # Copiar estados originales
    for e_orig in a.estados:
        nuevo_estado = Estado(e_orig.nombre, es_inicial=e_orig.es_inicial, es_final=e_orig.es_final)
        nuevos_estados.append(nuevo_estado)
        estado_dict[e_orig.nombre] = nuevo_estado
    
    # Crear estado sumidero si es necesario (si hay transiciones faltantes)
    estado_sumidero_necesario = False
    for e_obj_nuevo in nuevos_estados: # Iterar sobre los nuevos objetos estado
        # Para cada estado, verificar si tiene transiciones para todos los símbolos del alfabeto
        transiciones_salientes_simbolos: Set[str] = set()
        for t_orig in a.transiciones: # Buscar en las transiciones originales
            if t_orig.origen.nombre == e_obj_nuevo.nombre: # Si la transición original salía de este estado
                 transiciones_salientes_simbolos.add(t_orig.simbolo)
        
        if not alfabeto_original_simbolos.issubset(transiciones_salientes_simbolos):
            estado_sumidero_necesario = True
            break
    
    estado_sumidero: Optional[Estado] = None
    if estado_sumidero_necesario:
        estado_sumidero = Estado("S_sumidero", es_inicial=False, es_final=False)
        nuevos_estados.append(estado_sumidero)
        estado_dict[estado_sumidero.nombre] = estado_sumidero

    # Copiar transiciones existentes
    for t_orig in a.transiciones:
        origen_obj = estado_dict.get(t_orig.origen.nombre)
        destino_obj = estado_dict.get(t_orig.destino.nombre)
        if origen_obj and destino_obj:
            transiciones_completas.append(Transicion(origen_obj, destino_obj, t_orig.simbolo))

    # Agregar transiciones faltantes al estado sumidero (si existe)
    if estado_sumidero:
        for e_obj_nuevo in nuevos_estados:
            if e_obj_nuevo == estado_sumidero: continue # No agregar transiciones desde el sumidero aquí

            transiciones_salientes_simbolos = set()
            for t_completas in transiciones_completas:
                if t_completas.origen == e_obj_nuevo:
                    transiciones_salientes_simbolos.add(t_completas.simbolo)
            
            for simbolo in alfabeto_original_simbolos:
                if simbolo not in transiciones_salientes_simbolos:
                    transiciones_completas.append(Transicion(e_obj_nuevo, estado_sumidero, simbolo))
        
        # Transiciones del sumidero a sí mismo
        for simbolo in alfabeto_original_simbolos:
            transiciones_completas.append(Transicion(estado_sumidero, estado_sumidero, simbolo))

    estado_inicial_completo = estado_dict.get(a.estado_inicial.nombre) if a.estado_inicial else None
    estados_finales_completos = [estado_dict.get(ef.nombre) for ef in a.estados_finales if estado_dict.get(ef.nombre)]
    
    nombre_completo = f"Completo({a.nombre or 'A'})"

    return Automata(
        estados=nuevos_estados,
        alfabeto=sorted(list(alfabeto_original_simbolos)),
        transiciones=transiciones_completas,
        estado_inicial=estado_inicial_completo,
        estados_finales=estados_finales_completos,
        nombre=nombre_completo
    )

def complemento(a: Automata) -> Automata:
    # Primero, asegurar que el autómata esté completo
    a_completo = completar(a)
    
    nuevos_estados_comp: List[Estado] = []
    estado_dict_comp = {}
    
    estado_inicial_comp: Optional[Estado] = None
    estados_finales_comp: List[Estado] = []

    # Copiar estados de a_completo, invirtiendo la finalidad
    for e_orig_completo in a_completo.estados:
        es_final_invertido = not e_orig_completo.es_final
        nuevo_estado = Estado(e_orig_completo.nombre, 
                              es_inicial=e_orig_completo.es_inicial, 
                              es_final=es_final_invertido)
        nuevos_estados_comp.append(nuevo_estado)
        estado_dict_comp[e_orig_completo.nombre] = nuevo_estado
        
        if nuevo_estado.es_inicial:
            estado_inicial_comp = nuevo_estado
        if nuevo_estado.es_final:
            estados_finales_comp.append(nuevo_estado)

    # Copiar transiciones de a_completo
    transiciones_comp: List[Transicion] = []
    for t_orig_completo in a_completo.transiciones:
        origen_obj = estado_dict_comp.get(t_orig_completo.origen.nombre)
        destino_obj = estado_dict_comp.get(t_orig_completo.destino.nombre)
        if origen_obj and destino_obj:
            transiciones_comp.append(Transicion(origen_obj, destino_obj, t_orig_completo.simbolo))
            
    nombre_complemento = f"Complemento({a.nombre or 'A'})"

    return Automata(
        estados=nuevos_estados_comp,
        alfabeto=list(a_completo.alfabeto), # El alfabeto no cambia respecto al completo
        transiciones=transiciones_comp,
        estado_inicial=estado_inicial_comp,
        estados_finales=estados_finales_comp,
        nombre=nombre_complemento
    )

def inverso(a: Automata) -> Automata:
    nuevos_estados_inv: List[Estado] = []
    transiciones_inv: List[Transicion] = []
    estado_dict_inv = {}

    estado_inicial_inv: Optional[Estado] = None
    estados_finales_inv: List[Estado] = []

    # Copiar estados
    for e_orig in a.estados:
        # La finalidad y la inicialidad se determinarán después
        nuevo_estado = Estado(e_orig.nombre, es_inicial=False, es_final=False)
        nuevos_estados_inv.append(nuevo_estado)
        estado_dict_inv[e_orig.nombre] = nuevo_estado

    # Determinar nuevo estado inicial y nuevos estados finales
    # Si hay múltiples estados finales en 'a', creamos un nuevo estado inicial único para el inverso
    originales_finales_nombres = [ef.nombre for ef in a.estados_finales]
    
    if len(originales_finales_nombres) > 1:
        estado_inicial_inv = Estado("S_inverso_inicial_unico", es_inicial=True, es_final=False)
        nuevos_estados_inv.append(estado_inicial_inv) # Añadirlo a la lista de estados
        for nombre_final_orig in originales_finales_nombres:
            estado_final_orig_copiado = estado_dict_inv.get(nombre_final_orig)
            if estado_final_orig_copiado:
                 # Este estado copiado ya no es final por sí mismo, se conecta desde el nuevo inicial
                transiciones_inv.append(Transicion(estado_inicial_inv, estado_final_orig_copiado, "λ"))
    elif len(originales_finales_nombres) == 1:
        estado_inicial_inv = estado_dict_inv.get(originales_finales_nombres[0])
        if estado_inicial_inv:
            estado_inicial_inv.es_inicial = True
    # Si no hay estados finales en 'a', el inverso no tendrá estado inicial (o uno inalcanzable)

    # El estado inicial original de 'a' se convierte en estado final del inverso
    if a.estado_inicial:
        estado_final_nuevo = estado_dict_inv.get(a.estado_inicial.nombre)
        if estado_final_nuevo:
            estado_final_nuevo.es_final = True
            estados_finales_inv.append(estado_final_nuevo)

    # Invertir transiciones
    for t_orig in a.transiciones:
        # El origen de la nueva transición es el destino de la original
        # El destino de la nueva transición es el origen de la original
        nuevo_origen_obj = estado_dict_inv.get(t_orig.destino.nombre)
        nuevo_destino_obj = estado_dict_inv.get(t_orig.origen.nombre)
        if nuevo_origen_obj and nuevo_destino_obj:
            transiciones_inv.append(Transicion(nuevo_origen_obj, nuevo_destino_obj, t_orig.simbolo))
            
    alfabeto_calculado = list(a.alfabeto) # El alfabeto no cambia
    nombre_inverso = f"Inverso({a.nombre or 'A'})"
    
    return Automata(
        estados=nuevos_estados_inv,
        alfabeto=alfabeto_calculado,
        transiciones=transiciones_inv,
        estado_inicial=estado_inicial_inv,
        estados_finales=estados_finales_inv,
        nombre=nombre_inverso
    )