import heapq
import re
import time

#Solución 2: Utilizando Diccionarios y Módulo heapq para Priorización
#La segunda solución utilizará diccionarios para almacenar la información 
#de manera estructurada, y utilizaremos el módulo heapq para eficientar 
#la operación de ordenamiento basada en la prioridad. 
#Este enfoque es más avanzado y eficiente para manejar grandes conjuntos
#de datos donde el acceso rápido y la priorización son cruciales.


class Jugador:
    def __init__(self, id, nombre, edad, rendimiento):
        self.id = id
        self.nombre = nombre
        self.edad = edad
        self.rendimiento = rendimiento

    def __repr__(self):
        return f"Jugador(id={self.id}, nombre='{self.nombre}', edad={self.edad}, rendimiento={self.rendimiento})"


class Equipo:
    def __init__(self, id, deporte):
        self.id = id
        self.deporte = deporte
        self.jugadores = {}

    def agregar_jugador(self, jugador):
        self.jugadores[jugador.id] = jugador

    def rendimiento_promedio(self):
        if not self.jugadores:
            return 0
        return sum(j.rendimiento for j in self.jugadores.values()) / len(self.jugadores)

    def ordenar_jugadores(self):
        return heapq.nlargest(len(self.jugadores), self.jugadores.values(), key=lambda j: (j.rendimiento, -j.edad))

    def __repr__(self):
        return f"Equipo(deporte='{self.deporte}', jugadores={self.ordenar_jugadores()})"


class Sede:
    def __init__(self, id, nombre):
        self.id = id
        self.nombre = nombre
        self.equipos = {}

    def agregar_equipo(self, equipo):
        self.equipos[equipo.id] = equipo

    def rendimiento_promedio(self):
        if not self.equipos:
            return 0
        return sum(e.rendimiento_promedio() for e in self.equipos.values())

    def ordenar_equipos(self):
        return heapq.nlargest(len(self.equipos), self.equipos.values(), key=lambda e: (e.rendimiento_promedio(), -len(e.jugadores)))

    def __repr__(self):
        return f"Sede(nombre='{self.nombre}', equipos={self.ordenar_equipos()})"


class Asociacion:
    def __init__(self):
        self.sedes = {}

    def agregar_sede(self, sede):
        self.sedes[sede.id] = sede

    def ordenar_sedes(self):
        return heapq.nlargest(len(self.sedes), self.sedes.values(), key=lambda s: (s.rendimiento_promedio(), -sum(len(e.jugadores) for e in s.equipos.values())))

    def ranking_jugadores(self):
        todos_jugadores = [jugador for sede in self.sedes.values() for equipo in sede.equipos.values() for jugador in equipo.jugadores.values()]
        return heapq.nsmallest(len(todos_jugadores), todos_jugadores, key=lambda j: j.rendimiento)

    def calcular_estadisticas(self):
        todos_equipos = [equipo for sede in self.sedes.values() for equipo in sede.equipos.values()]
        todos_jugadores = [jugador for equipo in todos_equipos for jugador in equipo.jugadores.values()]

        equipo_mayor_rendimiento = max(todos_equipos, key=lambda e: e.rendimiento_promedio(), default=None)
        equipo_menor_rendimiento = min(todos_equipos, key=lambda e: e.rendimiento_promedio(), default=None)
        jugador_mayor_rendimiento = max(todos_jugadores, key=lambda j: j.rendimiento, default=None)
        jugador_menor_rendimiento = min(todos_jugadores, key=lambda j: j.rendimiento, default=None)
        jugador_mas_joven = min(todos_jugadores, key=lambda j: j.edad, default=None)
        jugador_mas_veterano = max(todos_jugadores, key=lambda j: j.edad, default=None)
        promedio_edad = sum(jugador.edad for jugador in todos_jugadores) / len(todos_jugadores)
        promedio_rendimiento = sum(jugador.rendimiento for jugador in todos_jugadores) / len(todos_jugadores)

        return {
            "equipo_mayor_rendimiento": equipo_mayor_rendimiento,
            "equipo_menor_rendimiento": equipo_menor_rendimiento,
            "jugador_mayor_rendimiento": jugador_mayor_rendimiento,
            "jugador_menor_rendimiento": jugador_menor_rendimiento,
            "jugador_mas_joven": jugador_mas_joven,
            "jugador_mas_veterano": jugador_mas_veterano,
            "promedio_edad": promedio_edad,
            "promedio_rendimiento": promedio_rendimiento
        }

    def generar_salida_sedes(self):
        resultados = []
        for sede in self.sedes.values():
            resultados.append(f"{sede.nombre}, Rendimiento: {sede.rendimiento_promedio()}")
            equipos_ordenados = sede.ordenar_equipos()
            for equipo in equipos_ordenados:
                resultados.append(f"{equipo.deporte}, Rendimiento: {equipo.rendimiento_promedio()}")
                jugadores_ordenados = sorted(equipo.jugadores.values(), key=lambda j: j.rendimiento, reverse=True)
                jugadores_info = ", ".join([f"{{{j.id}, {j.nombre}, {j.rendimiento}}}" for j in jugadores_ordenados])
                resultados.append(f"{{{jugadores_info}}}")
        return resultados

    def generar_salida_ranking_jugadores(self):
        ranking = self.ranking_jugadores()
        ranking_info = ", ".join([str(jugador.id) for jugador in ranking])
        return f"Ranking Jugadores:\n{{{ranking_info}}}"

    def generar_salida_estadisticas(self):
        estadisticas = self.calcular_estadisticas()
        jugador_mayor_rendimiento = estadisticas["jugador_mayor_rendimiento"]
        jugador_menor_rendimiento = estadisticas["jugador_menor_rendimiento"]
        jugador_mas_joven = estadisticas["jugador_mas_joven"]
        jugador_mas_veterano = estadisticas["jugador_mas_veterano"]
        promedio_edad = estadisticas["promedio_edad"]
        promedio_rendimiento = estadisticas["promedio_rendimiento"]

        return (
            f"Equipo con mayor rendimiento: {{{estadisticas['equipo_mayor_rendimiento'].deporte} {estadisticas['equipo_mayor_rendimiento'].id} {estadisticas['equipo_mayor_rendimiento'].rendimiento_promedio()}}}\n"
            f"Equipo con menor rendimiento: {{{estadisticas['equipo_menor_rendimiento'].deporte} {estadisticas['equipo_menor_rendimiento'].id} {estadisticas['equipo_menor_rendimiento'].rendimiento_promedio()}}}\n"
            f"Jugador con mayor rendimiento: {{{jugador_mayor_rendimiento.id}, {jugador_mayor_rendimiento.nombre}, {jugador_mayor_rendimiento.rendimiento}}}\n"
            f"Jugador con menor rendimiento: {{{jugador_menor_rendimiento.id}, {jugador_menor_rendimiento.nombre}, {jugador_menor_rendimiento.rendimiento}}}\n"
            f"Jugador más joven: {{{jugador_mas_joven.id}, {jugador_mas_joven.nombre}, {jugador_mas_joven.edad}}}\n"
            f"Jugador más veterano: {{{jugador_mas_veterano.id}, {jugador_mas_veterano.nombre}, {jugador_mas_veterano.edad}}}\n"
            f"Promedio de edad de los jugadores: {promedio_edad}\n"
            f"Promedio de rendimiento de los jugadores: {promedio_rendimiento}"
        )

    def generar_salida_completa(self):
        sedes_info = '\n\n'.join(self.generar_salida_sedes())
        ranking_info = self.generar_salida_ranking_jugadores()
        estadisticas_info = self.generar_salida_estadisticas()

        return f"{sedes_info}\n\n{ranking_info}\n\n{estadisticas_info}"

# Función para leer los datos desde el archivo
def leer_datos(filepath):
    jugadores = {}
    equipos = {}
    sedes = {}
    
    with open(filepath, 'r') as file:
        lines = file.readlines()

    jugador_regex = r'j(\d+) = Jugador.Jugador\("([^"]+)", (\d+), (\d+)\)'
    equipo_regex = r'e(\d+) = Equipo.Equipo\("([^"]+)", \[(.*?)\]\)'
    sede_regex = r's(\d+) = Sede.Sede\("([^"]+)", \[(.*?)\]\)'

    for line in lines:
        line = line.strip()
        if line.startswith('j'):
            match = re.match(jugador_regex, line)
            if match:
                id = int(match.group(1))
                nombre = match.group(2)
                edad = int(match.group(3))
                rendimiento = int(match.group(4))
                jugadores[id] = Jugador(id, nombre, edad, rendimiento)

        elif line.startswith('e'):
            match = re.match(equipo_regex, line)
            if match:
                id = int(match.group(1))
                deporte = match.group(2)
                jugadores_ids = match.group(3).split(', ')
                equipo = Equipo(id, deporte)
                for j_id in jugadores_ids:
                    j_id = int(j_id[1:])  # Eliminar la 'j' y convertir a entero
                    equipo.agregar_jugador(jugadores[j_id])
                equipos[id] = equipo

        elif line.startswith('s'):
            match = re.match(sede_regex, line)
            if match:
                id = int(match.group(1))
                nombre = match.group(2)
                equipos_ids = match.group(3).split(', ')
                sede = Sede(id, nombre)
                for e_id in equipos_ids:
                    e_id = int(e_id[1:])  # Eliminar la 'e' y convertir a entero
                    sede.agregar_equipo(equipos[e_id])
                sedes[id] = sede

    return jugadores, equipos, sedes

def medir_tiempo_ejecucion(filepath):
    inicio = time.time()

    # Cargar datos del archivo
    jugadores, equipos, sedes = leer_datos(filepath)

    # Crear la asociación
    asociacion = Asociacion()
    for sede in sedes.values():
        asociacion.agregar_sede(sede)

    # Imprimir los resultados
    resultado = asociacion.generar_salida_completa()

    fin = time.time()
    tiempo_total = fin - inicio
    print("La función se ejecutó en", tiempo_total, "segundos")
    print(resultado)
    return resultado

# Ejemplo de uso
medir_tiempo_ejecucion("input1.txt")
