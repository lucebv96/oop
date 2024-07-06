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
        self.padre = None

    def __lt__(self, otro):
        return self.f < otro.f

class AEstrella:
    def __init__(self, tablero, inicio, fin):
        self.tablero = tablero
        self.inicio = inicio
        self.fin = fin
        self.conjunto_abierto = [] #por explorar
        self.conjunto_cerrado = set() #explorados 

        # Inicializar nodo inicial
        self.nodo_inicial = Nodo(inicio[0], inicio[1])
        self.nodo_inicial.g = 0
        self.nodo_inicial.h = self.heuristica(self.nodo_inicial)
        self.nodo_inicial.f = self.nodo_inicial.g + self.nodo_inicial.h

        heapq.heappush(self.conjunto_abierto, self.nodo_inicial)

    def heuristica(self, nodo):
        # Heurística de distancia de Manhattan
        return abs(nodo.x - self.fin[0]) + abs(nodo.y - self.fin[1])

    def obtener_vecinos(self, nodo):
        vecinos = []
        direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Arriba, Abajo, Izquierda, Derecha

        for dx, dy in direcciones:
            nx, ny = nodo.x + dx, nodo.y + dy
            if 0 <= nx < len(self.tablero) and 0 <= ny < len(self.tablero[0]):
                if self.tablero[nx][ny] != 1 and (nx, ny) not in self.conjunto_cerrado:
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

            if (nodo_actual.x, nodo_actual.y) == self.fin:
                return self.reconstruir_camino(nodo_actual)

            self.conjunto_cerrado.add((nodo_actual.x, nodo_actual.y))

            for vecino in self.obtener_vecinos(nodo_actual):
                g_tentativo = nodo_actual.g + 1  # Asumiendo que cada paso cuesta 1

                if g_tentativo < vecino.g:
                    vecino.padre = nodo_actual
                    vecino.g = g_tentativo
                    vecino.h = self.heuristica(vecino)
                    vecino.f = vecino.g + vecino.h

                    if (vecino.x, vecino.y) not in self.conjunto_cerrado:
                        heapq.heappush(self.conjunto_abierto, vecino)

        return None  # No se encontró un camino

def imprimir_tablero(tablero):
    for fila in tablero:
        for celda in fila:
            if celda == 0:
                print(Back.WHITE + '  ', end='')  # Espacio blanco para mantener la alineación
            elif celda == 'i':
                print(Back.CYAN + '  ', end='')  # Cambio a cyan para el punto inicial
            elif celda == 'f':
                print(Back.BLUE + '  ', end='')  # Bloque azul para el punto final
            elif celda == 1:
                print(Fore.RED + '██', end='')  # Cambio a rojo para los obstáculos
            elif celda == 'camino':
                print(Fore.YELLOW + '██', end='')  # Cambio a amarillo para el camino encontrado
            else:
                print(Back.WHITE + '  ', end='')  # Espacios en blanco para cualquier otro caso

        print()  # Nueva línea al final de cada fila

def main():
    # Inicializar un tablero de 6x9 con todos ceros
    tablero = [[0] * 9 for _ in range(6)]

    # Pedir al usuario los puntos de inicio y fin
    inicio_x = int(input("Ingrese la fila para el punto de inicio (0-5): "))
    inicio_y = int(input("Ingrese la columna para el punto de inicio (0-8): "))
    fin_x = int(input("Ingrese la fila para el punto final (0-5): "))
    fin_y = int(input("Ingrese la columna para el punto final (0-8): "))

    # Marcar puntos de inicio y fin en el tablero
    tablero[inicio_x][inicio_y] = 'i'
    tablero[fin_x][fin_y] = 'f'

    # Pedir al usuario los obstáculos (paredes)
    while True:
        obstaculo_x = int(input("Ingrese la fila para un obstáculo (0-5), o -1 para terminar: "))
        if obstaculo_x == -1:
            break
        obstaculo_y = int(input("Ingrese la columna para un obstáculo (0-8): "))
        tablero[obstaculo_x][obstaculo_y] = 1

    # Imprimir el tablero inicial con los bloques de color para i y f
    imprimir_tablero(tablero)

    # Ejecutar algoritmo A*
    a_estrella = AEstrella(tablero, (inicio_x, inicio_y), (fin_x, fin_y))
    camino = a_estrella.encontrar_camino()

    if camino:
        print("\nCamino encontrado:")
        for paso in camino:
            x, y = paso
            if tablero[x][y] != 'i' and tablero[x][y] != 'f':  # No cambiar color si es punto inicial o final
                tablero[x][y] = 'camino'  # Marcar el camino como 'camino' en lugar de '*'
        imprimir_tablero(tablero)
    else:
        print("\nNo se encontró un camino válido.")

if __name__ == "__main__":
    main()
