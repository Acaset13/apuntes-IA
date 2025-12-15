import pygame
import heapq

pygame.init()

# ---------------- Configuración principal (ajusta aquí filas y columnas) ----------------
ANCHO_VENTANA = 700
MARGEN_SUPERIOR = 80  # espacio para botones
# Cambia estas variables para una cuadrícula dinámica
FILAS = 10   # número de filas (ejemplo 3)
COLS = 10  # número de columnas (ejemplo 5)
# --------------------------------------------------------------------------------------

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
GRIS = (200, 200, 200)
VERDE = (0, 200, 0)
ROJO = (200, 0, 0)
NARANJA = (255, 165, 0)
PURPURA = (128, 0, 128)
DORADO = (255, 200, 0)
AZUL = (0, 120, 255)
AZUL_OSCURO = (0, 90, 200)

# Ventana calculada en función de ancho y proporciones (cuadrícula ocupa ancho)
VENTANA = pygame.display.set_mode((ANCHO_VENTANA, ANCHO_VENTANA + MARGEN_SUPERIOR))
pygame.display.set_caption("Visualización algoritmo A* (Paso a paso / Automático)")

FUENTE = pygame.font.SysFont(None, 18)
FUENTE_BOTON = pygame.font.SysFont(None, 24)

# Costes
COSTE_RECTA = 10
COSTE_DIAG = 14

# ---------------- Clase Nodo ----------------
class Nodo:
    def __init__(self, fila, col, ancho, filas, cols):
        self.fila = fila
        self.col = col
        self.ancho = ancho
        self.x = col * ancho
        self.y = fila * ancho + MARGEN_SUPERIOR
        self.color = BLANCO
        self.vecinos = []
        self.filas = filas
        self.cols = cols

        # valores de A*
        self.g = float("inf")
        self.h = float("inf")
        self.f = float("inf")

    def get_pos(self):
        return (self.fila, self.col)

    def es_pared(self):
        return self.color == NEGRO

    def es_inicio(self):
        return self.color == NARANJA

    def es_fin(self):
        return self.color == PURPURA

    def restablecer(self):
        self.color = BLANCO
        self.g = float("inf")
        self.h = float("inf")
        self.f = float("inf")

    def hacer_inicio(self):
        self.color = NARANJA

    def hacer_pared(self):
        self.color = NEGRO

    def hacer_fin(self):
        self.color = PURPURA

    def hacer_abierto(self):
        if not self.es_inicio() and not self.es_fin():
            self.color = VERDE

    def hacer_cerrado(self):
        if not self.es_inicio() and not self.es_fin():
            self.color = ROJO

    def hacer_camino(self):
        if not self.es_inicio() and not self.es_fin():
            self.color = DORADO

    def dibujar(self, ventana):
        pygame.draw.rect(ventana, self.color, (self.x, self.y, self.ancho, self.ancho))
        pygame.draw.rect(ventana, GRIS, (self.x, self.y, self.ancho, self.ancho), 1)

        # Mostrar G,H,F dentro de la casilla si están definidos (evitar inf)
        if self.g != float("inf"):
            texto_g = FUENTE.render(str(int(self.g)), True, NEGRO)
            ventana.blit(texto_g, (self.x + 3, self.y + 2))
        if self.h != float("inf"):
            texto_h = FUENTE.render(str(int(self.h)), True, NEGRO)
            ventana.blit(texto_h, (self.x + 3, self.y + self.ancho - 16))
        if self.f != float("inf"):
            texto_f = FUENTE.render(str(int(self.f)), True, AZUL_OSCURO)
            # centrar F en esquina derecha superior
            ventana.blit(texto_f, (self.x + self.ancho - 3 - texto_f.get_width(), self.y + 2))

    # Actualizar vecinos (incluye 8 direcciones; diagonales permitidas incluso si hay muros)
    def actualizar_vecinos(self, grid):
        self.vecinos = []
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                nf = self.fila + dr
                nc = self.col + dc
                if 0 <= nf < self.filas and 0 <= nc < self.cols:
                    vecino = grid[nf][nc]
                    if not vecino.es_pared():
                        self.vecinos.append(vecino)

    # Comparaciones para uso en sets/dicts/heap (útiles como claves)
    def __lt__(self, otro):
        return (self.f, self.g) < (otro.f, otro.g)

    def __hash__(self):
        return hash((self.fila, self.col))

    def __eq__(self, otro):
        if not isinstance(otro, Nodo):
            return False
        return (self.fila, self.col) == (otro.fila, otro.col)

# ---------------- Heurística Manhattan multiplicada por 10 ----------------
def heuristica(a, b):
    (x1, y1) = a
    (x2, y2) = b
    return (abs(x1 - x2) + abs(y1 - y2)) * COSTE_RECTA

# ---------------- Reconstruir camino ----------------
def reconstruir_camino(came_from, actual, dibujar):
    while actual in came_from:
        actual = came_from[actual]
        actual.hacer_camino()
        dibujar()

# ---------------- A* con paso a paso ----------------
class AStar:
    def __init__(self, grid, inicio, fin):
        # grid: matriz de nodos
        # inicio/fin: nodos
        self.grid = grid
        self.inicio = inicio
        self.fin = fin
        self.came_from = {}
        self.counter = 0  # para desempate por orden de descubrimiento
        self.open_heap = []  # heap de (f, contador, nodo)
        self.open_hash = set()
        self.closed_set = set()
        self.running = False
        self.finished = False
        self.found = False

        # Inicializar scores
        for fila in grid:
            for n in fila:
                n.g = float("inf")
                n.h = float("inf")
                n.f = float("inf")
        self.inicio.g = 0
        self.inicio.h = heuristica(self.inicio.get_pos(), self.fin.get_pos())
        self.inicio.f = self.inicio.h
        heapq.heappush(self.open_heap, (self.inicio.f, self.counter, self.inicio))
        self.open_hash.add(self.inicio)
        self.counter += 1
        self.running = True

    # Realiza UN paso de A* y devuelve estado: 'running', 'found', 'no_path'
    def step(self):
        if not self.running or self.finished:
            return 'finished'

        if not self.open_heap:
            self.finished = True
            self.running = False
            return 'no_path'

        # Pop nodo con f más bajo (heap)
        _, _, actual = heapq.heappop(self.open_heap)
        if actual in self.open_hash:
            self.open_hash.remove(actual)

        # Marcar como cerrado
        if actual != self.inicio and actual != self.fin:
            actual.hacer_cerrado()
        self.closed_set.add(actual)

        # Si llegamos al fin
        if actual == self.fin:
            reconstruir_camino(self.came_from, self.fin, lambda: None)  # dibujado hecho fuera
            self.fin.hacer_fin()
            self.inicio.hacer_inicio()
            self.finished = True
            self.running = False
            self.found = True
            return 'found'

        # Procesar vecinos
        for vecino in actual.vecinos:
            if vecino in self.closed_set:
                continue

            # calcular coste de movimiento desde actual a vecino
            dr = abs(vecino.fila - actual.fila)
            dc = abs(vecino.col - actual.col)
            coste_mov = COSTE_DIAG if (dr == 1 and dc == 1) else COSTE_RECTA

            temp_g = actual.g + coste_mov

            if temp_g < vecino.g:
                self.came_from[vecino] = actual
                vecino.g = temp_g
                vecino.h = heuristica(vecino.get_pos(), self.fin.get_pos())
                vecino.f = vecino.g + vecino.h

                # añadir a abierto si no está
                if vecino not in self.open_hash:
                    heapq.heappush(self.open_heap, (vecino.f, self.counter, vecino))
                    self.open_hash.add(vecino)
                    self.counter += 1
                    vecino.hacer_abierto()
                else:
                    # si ya está en open, actualizamos heap añadiendo otra entrada (lazy-deletion)
                    heapq.heappush(self.open_heap, (vecino.f, self.counter, vecino))
                    self.counter += 1
                    vecino.hacer_abierto()

        return 'running'

# ---------------- Crear cuadrícula dinámica filas x cols ----------------
def crear_grid(filas, cols, ancho_total):
    grid = []
    ancho_nodo = ancho_total // cols
    # Afinar alto total para que cuadricula se ajuste al ancho
    for i in range(filas):
        fila = []
        for j in range(cols):
            nodo = Nodo(i, j, ancho_nodo, filas, cols)
            fila.append(nodo)
        grid.append(fila)
    return grid

# ---------------- Dibujado de la interfaz (botones + cuadrícula) ----------------
def dibujar_boton(ventana, rect, texto, color_fondo=AZUL):
    pygame.draw.rect(ventana, color_fondo, rect, border_radius=8)
    txt = FUENTE_BOTON.render(texto, True, BLANCO)
    ventana.blit(txt, (rect.x + (rect.width - txt.get_width()) // 2, rect.y + (rect.height - txt.get_height()) // 2))

def dibujar(ventana, grid, filas, cols):
    ventana.fill(BLANCO)
    # Botones
    boton_iniciar = pygame.Rect(10, 10, 130, 40)
    boton_paso = pygame.Rect(150, 10, 100, 40)
    boton_reset = pygame.Rect(270, 10, 100, 40)
    boton_ejemplo = pygame.Rect(390, 10, 120, 40)

    dibujar_boton(ventana, boton_iniciar, "Iniciar A*")
    dibujar_boton(ventana, boton_paso, "Paso")
    dibujar_boton(ventana, boton_reset, "Reset")
    dibujar_boton(ventana, boton_ejemplo, "Cargar Ejemplo")

    # Dibujar nodos
    for fila in grid:
        for nodo in fila:
            nodo.dibujar(ventana)

    pygame.display.update()
    return boton_iniciar, boton_paso, boton_reset, boton_ejemplo

# ---------------- Obtener posición del click en la cuadrícula ----------------
def obtener_click_pos(pos, filas, cols, ancho_total):
    x, y = pos
    if y < MARGEN_SUPERIOR:
        return None
    ancho_nodo = ancho_total // cols
    fila = (y - MARGEN_SUPERIOR) // ancho_nodo
    col = x // ancho_nodo
    if 0 <= fila < filas and 0 <= col < cols:
        return fila, col
    return None

# ---------------- Función para cargar tu ejemplo 3x5 ----------------
def cargar_ejemplo(grid, filas, cols):
    # limpiar todo
    for f in grid:
        for n in f:
            n.restablecer()

    # Ajustar inicio y fin según tu ejemplo (1-1 -> indices 0,0 ; fin 3-5 -> 2,4)
    inicio = grid[0][0]
    fin = grid[2][4]
    inicio.hacer_inicio()
    fin.hacer_fin()

    # muros en (1-2),(2-4),(3-3) según tu formato 1-indexed
    muros = [(0,1),(1,3),(2,2)]
    for (r,c) in muros:
        if 0 <= r < filas and 0 <= c < cols:
            grid[r][c].hacer_pared()

    return inicio, fin

# ---------------- Reset general ----------------
def reset_grid(grid, filas, cols):
    for f in grid:
        for n in f:
            n.restablecer()

# ---------------- Programa principal ----------------
def main():
    clock = pygame.time.Clock()
    ancho_total = ANCHO_VENTANA
    grid = crear_grid(FILAS, COLS, ancho_total)

    # Precalcular vecinos (se recalculará antes de iniciar A*)
    for fila in grid:
        for n in fila:
            n.actualizar_vecinos(grid)

    inicio = None
    fin = None
    astar = None
    auto_run = False

    corriendo = True
    while corriendo:
        clock.tick(30)  # FPS
        boton_iniciar, boton_paso, boton_reset, boton_ejemplo = dibujar(VENTANA, grid, FILAS, COLS)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False
                break

            if evento.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                # Botones
                if boton_iniciar.collidepoint(pos):
                    # preparar A*
                    if inicio and fin:
                        # actualizar vecinos antes de iniciar
                        for fila in grid:
                            for n in fila:
                                n.actualizar_vecinos(grid)
                        astar = AStar(grid, inicio, fin)
                        auto_run = True
                    continue

                if boton_paso.collidepoint(pos):
                    # ejecutar solo un paso
                    if inicio and fin:
                        # si no hay astar inicializado, inicializar
                        if astar is None or astar.finished:
                            for fila in grid:
                                for n in fila:
                                    n.actualizar_vecinos(grid)
                            astar = AStar(grid, inicio, fin)
                        auto_run = False
                        estado = astar.step()
                        # si found o no_path, marcar auto_run False
                        if estado in ('found','no_path'):
                            auto_run = False
                        # actualizar dibujo inmediato
                    continue

                if boton_reset.collidepoint(pos):
                    reset_grid(grid, FILAS, COLS)
                    inicio = None
                    fin = None
                    astar = None
                    auto_run = False
                    continue

                if boton_ejemplo.collidepoint(pos):
                    # cargar el ejemplo 3x5 (si dimensiones son compatibles)
                    if FILAS >= 3 and COLS >= 5:
                        inicio, fin = cargar_ejemplo(grid, FILAS, COLS)
                        astar = None
                        # recalcular vecinos
                        for fila in grid:
                            for n in fila:
                                n.actualizar_vecinos(grid)
                        auto_run = False
                    continue

                # Click en la cuadrícula: colocación inicio/fin/muro o borrado con botón derecho
                if evento.button == 1:  # izquierdo: establecer
                    click = obtener_click_pos(pos, FILAS, COLS, ancho_total)
                    if click:
                        f, c = click
                        nodo = grid[f][c]
                        if not inicio and nodo != fin:
                            inicio = nodo
                            inicio.hacer_inicio()
                        elif not fin and nodo != inicio:
                            fin = nodo
                            fin.hacer_fin()
                        elif nodo != inicio and nodo != fin:
                            nodo.hacer_pared()
                elif evento.button == 3:  # derecho: restablecer
                    click = obtener_click_pos(pos, FILAS, COLS, ancho_total)
                    if click:
                        f, c = click
                        nodo = grid[f][c]
                        # si borra inicio/fin limpiar referencia
                        if nodo == inicio:
                            inicio = None
                        if nodo == fin:
                            fin = None
                        nodo.restablecer()

        # Auto run: si está activo, ejecutar pasos hasta terminar con un pequeño ritmo (por frame 2 pasos)
        if auto_run and (astar is not None) and not astar.finished:
            # Ejecutar algunos pasos por frame para velocidad (puedes ajustar)
            pasos_por_frame = 2
            for _ in range(pasos_por_frame):
                estado = astar.step()
                if estado in ('found','no_path'):
                    auto_run = False
                    break

        # Si finalizó y se encontró ruta, reconstruir camino con llamada visual (para pintar bien)
        if astar and astar.finished and astar.found:
            # reconstruir visiblemente (usar came_from)
            reconstruir_camino(astar.came_from, astar.fin, lambda: None)
            astar.found = False  # evitar reconstrucción repetida

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
