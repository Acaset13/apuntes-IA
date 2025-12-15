import pygame
import heapq

pygame.init()

# ---------------- Configuración principal ----------------
ANCHO_VENTANA = 700
MARGEN_SUPERIOR = 200
FILAS = 3
COLS = 5

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

VENTANA = pygame.display.set_mode((ANCHO_VENTANA, ANCHO_VENTANA + MARGEN_SUPERIOR))
pygame.display.set_caption("Algoritmo A* (Paso a paso / Automático)")

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

        # Mostrar G,H,F con letras si están definidos
        if self.g != float("inf"):
            texto_g = FUENTE.render(f"G:{int(self.g)}", True, NEGRO)
            ventana.blit(texto_g, (self.x + 2, self.y + 2))
        if self.h != float("inf"):
            texto_h = FUENTE.render(f"H:{int(self.h)}", True, NEGRO)
            ventana.blit(texto_h, (self.x + 2, self.y + self.ancho // 2 - 8))
        if self.f != float("inf"):
            texto_f = FUENTE.render(f"F:{int(self.f)}", True, AZUL_OSCURO)
            ventana.blit(texto_f, (self.x + 2, self.y + self.ancho - 18))

    def actualizar_vecinos(self, grid):
        self.vecinos = []
        # Direcciones (8)
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1),
                       (-1, -1), (-1, 1), (1, -1), (1, 1)]:
            nf = self.fila + dr
            nc = self.col + dc
            if 0 <= nf < self.filas and 0 <= nc < self.cols:
                vecino = grid[nf][nc]
                if vecino.es_pared():
                    continue

                # Si es diagonal, verificar que no se corten esquinas
                if abs(dr) == 1 and abs(dc) == 1:
                    if grid[self.fila][nc].es_pared() or grid[nf][self.col].es_pared():
                        continue

                self.vecinos.append(vecino)

    def __lt__(self, otro):
        return (self.f, self.g) < (otro.f, otro.g)

    def __hash__(self):
        return hash((self.fila, self.col))

    def __eq__(self, otro):
        return (self.fila, self.col) == (otro.fila, otro.col)


# ---------------- Heurística Manhattan * 10 ----------------
def heuristica(a, b):
    (x1, y1) = a
    (x2, y2) = b
    return (abs(x1 - x2) + abs(y1 - y2)) * COSTE_RECTA


# ---------------- Reconstrucción del camino ----------------
def reconstruir_camino(came_from, actual, dibujar):
    while actual in came_from:
        actual = came_from[actual]
        actual.hacer_camino()
        dibujar()


# ---------------- Algoritmo A* paso a paso ----------------
class AStar:
    def __init__(self, grid, inicio, fin):
        self.grid = grid
        self.inicio = inicio
        self.fin = fin
        self.came_from = {}
        self.counter = 0
        self.open_heap = []
        self.open_hash = set()
        self.closed_set = set()
        self.running = True
        self.finished = False
        self.found = False

        # Inicializar
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

    def step(self):
        if not self.open_heap:
            self.finished = True
            self.running = False
            return 'no_path'

        _, _, actual = heapq.heappop(self.open_heap)
        if actual not in self.open_hash:
            return 'running'
        self.open_hash.remove(actual)

        if actual != self.inicio and actual != self.fin:
            actual.hacer_cerrado()
        self.closed_set.add(actual)

        if actual == self.fin:
            reconstruir_camino(self.came_from, self.fin, lambda: None)
            self.fin.hacer_fin()
            self.inicio.hacer_inicio()
            self.finished = True
            self.found = True
            return 'found'

        for vecino in actual.vecinos:
            if vecino in self.closed_set:
                continue

            dr = abs(vecino.fila - actual.fila)
            dc = abs(vecino.col - actual.col)
            coste_mov = COSTE_DIAG if (dr == 1 and dc == 1) else COSTE_RECTA

            temp_g = actual.g + coste_mov

            if temp_g < vecino.g:
                self.came_from[vecino] = actual
                vecino.g = temp_g
                vecino.h = heuristica(vecino.get_pos(), self.fin.get_pos())
                vecino.f = vecino.g + vecino.h

                if vecino not in self.open_hash:
                    heapq.heappush(self.open_heap, (vecino.f, self.counter, vecino))
                    self.open_hash.add(vecino)
                    self.counter += 1
                    vecino.hacer_abierto()

        return 'running'


# ---------------- Crear cuadrícula ----------------
def crear_grid(filas, cols, ancho_total):
    grid = []
    ancho_nodo = ancho_total // cols
    for i in range(filas):
        fila = []
        for j in range(cols):
            nodo = Nodo(i, j, ancho_nodo, filas, cols)
            fila.append(nodo)
        grid.append(fila)
    return grid


# ---------------- Botones y dibujo ----------------
def dibujar_boton(ventana, rect, texto, color_fondo=AZUL):
    pygame.draw.rect(ventana, color_fondo, rect, border_radius=8)
    txt = FUENTE_BOTON.render(texto, True, BLANCO)
    ventana.blit(txt, (rect.x + (rect.width - txt.get_width()) // 2,
                       rect.y + (rect.height - txt.get_height()) // 2))


def dibujar(ventana, grid):
    ventana.fill(BLANCO)
    boton_iniciar = pygame.Rect(10, 10, 130, 40)
    boton_paso = pygame.Rect(150, 10, 100, 40)
    boton_reset = pygame.Rect(270, 10, 100, 40)
    boton_ejemplo = pygame.Rect(390, 10, 120, 40)

    dibujar_boton(ventana, boton_iniciar, "Iniciar A*")
    dibujar_boton(ventana, boton_paso, "Paso")
    dibujar_boton(ventana, boton_reset, "Reset")
    dibujar_boton(ventana, boton_ejemplo, "Cargar Ejemplo")

    for fila in grid:
        for nodo in fila:
            nodo.dibujar(ventana)

    pygame.display.update()
    return boton_iniciar, boton_paso, boton_reset, boton_ejemplo


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


def cargar_ejemplo(grid):
    for f in grid:
        for n in f:
            n.restablecer()
    inicio = grid[0][0]
    fin = grid[2][4]
    inicio.hacer_inicio()
    fin.hacer_fin()
    muros = [(0, 1), (1, 3), (2, 2)]
    for (r, c) in muros:
        grid[r][c].hacer_pared()
    return inicio, fin


def reset_grid(grid):
    for f in grid:
        for n in f:
            n.restablecer()


def main():
    clock = pygame.time.Clock()
    grid = crear_grid(FILAS, COLS, ANCHO_VENTANA)

    for fila in grid:
        for n in fila:
            n.actualizar_vecinos(grid)

    inicio = None
    fin = None
    astar = None
    auto_run = False
    corriendo = True

    while corriendo:
        clock.tick(30)
        botones = dibujar(VENTANA, grid)
        boton_iniciar, boton_paso, boton_reset, boton_ejemplo = botones

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False

            if evento.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if boton_iniciar.collidepoint(pos):
                    if inicio and fin:
                        for fila in grid:
                            for n in fila:
                                n.actualizar_vecinos(grid)
                        astar = AStar(grid, inicio, fin)
                        auto_run = True
                    continue
                if boton_paso.collidepoint(pos):
                    if inicio and fin:
                        if astar is None or astar.finished:
                            for fila in grid:
                                for n in fila:
                                    n.actualizar_vecinos(grid)
                            astar = AStar(grid, inicio, fin)
                        auto_run = False
                        estado = astar.step()
                        if estado in ('found', 'no_path'):
                            auto_run = False
                    continue
                if boton_reset.collidepoint(pos):
                    reset_grid(grid)
                    inicio = None
                    fin = None
                    astar = None
                    auto_run = False
                    continue
                if boton_ejemplo.collidepoint(pos):
                    inicio, fin = cargar_ejemplo(grid)
                    astar = None
                    auto_run = False
                    continue

                click = obtener_click_pos(pos, FILAS, COLS, ANCHO_VENTANA)
                if click:
                    f, c = click
                    nodo = grid[f][c]
                    if evento.button == 1:
                        if not inicio and nodo != fin:
                            inicio = nodo
                            inicio.hacer_inicio()
                        elif not fin and nodo != inicio:
                            fin = nodo
                            fin.hacer_fin()
                        elif nodo != inicio and nodo != fin:
                            nodo.hacer_pared()
                    elif evento.button == 3:
                        nodo.restablecer()
                        if nodo == inicio:
                            inicio = None
                        if nodo == fin:
                            fin = None

        if auto_run and astar and not astar.finished:
            pasos = 2
            for _ in range(pasos):
                estado = astar.step()
                if estado in ('found', 'no_path'):
                    auto_run = False
                    break

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
