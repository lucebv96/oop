import heapq
from colorama import init, Fore, Back

init(autoreset=True)  # Inicializar colorama para que los colores ANSI se reseteen automáticamente

class Nodo:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.g = float('inf')  # Costo desde el nodo inicial hasta el nodo actual
        self.h = float('inf')  # Estimación heurística desde el nodo actual hasta el nodo final
        self.f = float('inf')  # Costo total: g + h
        self.padre = None  # Nodo padre en el camino

    def __lt__(self, otro):
        return self.f < otro.f

class Mapa:
    def __init__(self, filas, columnas, inicio, fin):
        self.filas = filas
        self.columnas = columnas
        self.tablero = [[0] * columnas for _ in range(filas)]
        self.inicio = inicio
        self.fin = fin
        self.tablero[inicio[0]][inicio[1]] = 'i'
        self.tablero[fin[0]][fin[1]] = 'f'

    def agregar_obstaculo(self, x, y):
        self.tablero[x][y] = 1

    def quitar_obstaculo(self, x, y):
        self.tablero[x][y] = 0

    def es_accesible(self, x, y):
        if 0 <= x < self.filas and 0 <= y < self.columnas:
            return self.tablero[x][y] != 1
        return False

class CalculadoraRutas:
    def __init__(self, mapa):
        self.mapa = mapa
        self.conjunto_abierto = []
        self.conjunto_cerrado = set()

        # Inicializar nodo inicial
        inicio = mapa.inicio
        fin = mapa.fin
        self.nodo_inicial = Nodo(inicio[0], inicio[1])
        self.nodo_inicial.g = 0
        self.nodo_inicial.h = self.heuristica(self.nodo_inicial)
        self.nodo_inicial.f = self.nodo_inicial.g + self.nodo_inicial.h
        heapq.heappush(self.conjunto_abierto, self.nodo_inicial)

    def heuristica(self, nodo):
        return abs(nodo.x - self.mapa.fin[0]) + abs(nodo.y - self.mapa.fin[1])

    def obtener_vecinos(self, nodo):
        vecinos = []
        direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for dx, dy in direcciones:
            nx, ny = nodo.x + dx, nodo.y + dy
            if self.mapa.es_accesible(nx, ny) and (nx, ny) not in self.conjunto_cerrado:
                vecinos.append(Nodo(nx, ny))
        return vecinos

    def reconstruir_camino(self, nodo_actual):
        camino = []
        while nodo_actual is not None:
            camino.append((nodo_actual.x, nodo_actual.y))
            nodo_actual = nodo_actual.padre
        return camino[::-1]

    def encontrar_camino(self):
        while self.conjunto_abierto:
            nodo_actual = heapq.heappop(self.conjunto_abierto)

            if (nodo_actual.x, nodo_actual.y) == self.mapa.fin:
                return self.reconstruir_camino(nodo_actual)

            self.conjunto_cerrado.add((nodo_actual.x, nodo_actual.y))

            for vecino in self.obtener_vecinos(nodo_actual):
                g_tentativo = nodo_actual.g + 1

                if g_tentativo < vecino.g:
                    vecino.padre = nodo_actual
                    vecino.g = g_tentativo
                    vecino.h = self.heuristica(vecino)
                    vecino.f = vecino.g + vecino.h

                    if (vecino.x, vecino.y) not in self.conjunto_cerrado:
                        heapq.heappush(self.conjunto_abierto, vecino)

        return None

def imprimir_tablero(tablero):
    for fila in tablero:
        for celda in fila:
            if celda == 0:
                print(Back.WHITE + '  ', end='')
            elif celda == 'i':
                print(Back.CYAN + '  ', end='')
            elif celda == 'f':
                print(Back.BLUE + '  ', end='')
            elif celda == 1:
                print(Fore.RED + '██', end='')
            elif celda == 'camino':
                print(Fore.YELLOW + '██', end='')
            else:
                print(Back.WHITE + '  ', end='')

        print()

def main():
    # Pedir al usuario los puntos de inicio y fin
    inicio_x = int(input("Ingrese la fila para el punto de inicio (0-5): "))
    inicio_y = int(input("Ingrese la columna para el punto de inicio (0-8): "))
    fin_x = int(input("Ingrese la fila para el punto final (0-5): "))
    fin_y = int(input("Ingrese la columna para el punto final (0-8): "))

    # Crear el mapa
    mapa = Mapa(6, 9, (inicio_x, inicio_y), (fin_x, fin_y))

    # Pedir al usuario los obstáculos (paredes)
    while True:
        print("\nOpciones:")
        print("1. Agregar obstáculo")
        print("2. Quitar obstáculo")
        print("0. Terminar")
        opcion = int(input("Seleccione una opción: "))

        if opcion == 0:
            break
        elif opcion == 1:
            obstaculo_x = int(input("Ingrese la fila para agregar un obstáculo (0-5): "))
            obstaculo_y = int(input("Ingrese la columna para agregar un obstáculo (0-8): "))
            mapa.agregar_obstaculo(obstaculo_x, obstaculo_y)
        elif opcion == 2:
            obstaculo_x = int(input("Ingrese la fila para quitar un obstáculo (0-5): "))
            obstaculo_y = int(input("Ingrese la columna para quitar un obstáculo (0-8): "))
            mapa.quitar_obstaculo(obstaculo_x, obstaculo_y)
        else:
            print("Opción no válida. Intente nuevamente.")

        # Imprimir el tablero actualizado con los bloques de color para i y f
        imprimir_tablero(mapa.tablero)

    # Ejecutar algoritmo A*
    calculadora_rutas = CalculadoraRutas(mapa)
    camino = calculadora_rutas.encontrar_camino()

    if camino:
        print("\nCamino encontrado:")
        for paso in camino:
            x, y = paso
            if mapa.tablero[x][y] != 'i' and mapa.tablero[x][y] != 'f':
                mapa.tablero[x][y] = 'camino'
        imprimir_tablero(mapa.tablero)
    else:
        print("\nNo se encontró un camino válido.")

if __name__ == "__main__":
    main()
