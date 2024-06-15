import re
import time
 
#Solución 1: Utilizando Listas y Ordenamiento Personalizado
#En la primera solución, utilizaremos listas para almacenar
#jugadores, equipos y sedes, y aplicaremos técnicas de ordenamiento 
#utilizando comparaciones directas y algoritmos de ordenamiento 
#como el Merge Sort implementado manualmente. 
#Este enfoque es adecuado para entender cómo se pueden manipular
#y ordenar datos de manera directa.

class Jugador:
    
    def __init__(self, id, nombre, edad, rendimiento):
        self.id = id
        self.nombre = nombre
        self.edad = edad
        self.rendimiento = rendimiento

    def __repr__(self):
        return f"{self.nombre} ({self.id}), Edad: {self.edad}, Rendimiento: {self.rendimiento}"


class Equipo:
    def __init__(self, id, deporte):
        self.id = id
        self.deporte = deporte
        self.jugadores = []

    def agregar_jugador(self, jugador):
        self.jugadores.append(jugador)

    def rendimiento_promedio(self):
        if not self.jugadores:
            return 0
        total_rendimiento = sum(jugador.rendimiento for jugador in self.jugadores)
        return total_rendimiento / len(self.jugadores)

    def ordenar_jugadores(self):
        self.jugadores = merge_sort(self.jugadores, key=lambda j: (j.rendimiento, -j.edad))

    def __repr__(self):
        return f"{self.deporte}: {self.jugadores}"


class Sede:
    def __init__(self, id, nombre):
        self.id = id
        self.nombre = nombre
        self.equipos = []

    def agregar_equipo(self, equipo):
        self.equipos.append(equipo)

    def rendimiento_promedio(self):
        if not self.equipos:
            return 0
        total_rendimiento = sum(equipo.rendimiento_promedio() for equipo in self.equipos)
        return total_rendimiento / len(self.equipos)

    def ordenar_equipos(self):
        self.equipos = merge_sort(self.equipos, key=lambda e: (e.rendimiento_promedio(), -len(e.jugadores)))

    def __repr__(self):
        return f"{self.nombre}: {self.equipos}"


class Asociacion:
    def __init__(self):
        self.sedes = []

    def agregar_sede(self, sede):
        self.sedes.append(sede)

    def ordenar_sedes(self):
        self.sedes = merge_sort(self.sedes, key=lambda s: (s.rendimiento_promedio(), -sum(len(e.jugadores) for e in s.equipos)))

    def ranking_jugadores(self):
        todos_jugadores = [jugador for sede in self.sedes for equipo in sede.equipos for jugador in equipo.jugadores]
        return merge_sort(todos_jugadores, key=lambda j: j.rendimiento)

    def calcular_estadisticas(self):
        todos_equipos = [equipo for sede in self.sedes for equipo in sede.equipos]
        todos_jugadores = [jugador for sede in self.sedes for equipo in sede.equipos for jugador in equipo.jugadores]


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

    def __repr__(self):
        self.ordenar_sedes()
        ranking = self.ranking_jugadores()
        estadisticas = self.calcular_estadisticas()
        sedes_str = '\n\n'.join(str(sede) for sede in self.sedes)
        ranking_str = ', '.join(str(jugador.id) for jugador in ranking)

        return f"{sedes_str}\n\nRanking Jugadores:\n{ranking_str}\n\nEstadísticas:\n{estadisticas}"


def merge_sort(arr, key=lambda x: x):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid], key=key)
    right = merge_sort(arr[mid:], key=key)
    return merge(left, right, key)


def merge(left, right, key):
    sorted_list = []
    while left and right:
        if key(left[0]) < key(right[0]):
            sorted_list.append(left.pop(0))
        else:
            sorted_list.append(right.pop(0))
    sorted_list.extend(left if left else right)
    return sorted_list

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

# Función para medir el tiempo de ejecución de la solución 1
def medir_tiempo_solucion_1(filepath):
    inicio = time.time()
    
    jugadores, equipos, sedes = leer_datos(filepath)
    asociacion = Asociacion()
    for sede in sedes.values():
        asociacion.agregar_sede(sede)

    resultado = str(asociacion)
    
    fin = time.time()
    tiempo_total = fin - inicio
    print("La función de la solución 1 se ejecutó en", tiempo_total, "segundos")
    return resultado

# Ejemplo de uso
filepath = "input1.txt"
resultado = medir_tiempo_solucion_1(filepath)

# Cargar datos del archivo
jugadores, equipos, sedes = leer_datos("input1.txt")

# Crear la asociación
asociacion = Asociacion()
for sede in sedes.values():
    asociacion.agregar_sede(sede)

# Imprimir los resultados
print(asociacion)
