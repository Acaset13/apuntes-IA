import pygame
import heapq

pygame.init()

# ---------------- Configuración principal (ajusta aquí filas y columnas) ----------------
ANCHO_VENTANA = 400
MARGEN_SUPERIOR = 80    # espacio para botones arriba
ALTURA_FOOTER = 80      # espacio abajo para mostrar listas abierta/cerrada (texto plano)
FILAS = 10               # número de filas (cambia aquí)
COLS = 10                # número de columnas (cambia aquí)
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

# Ventana: alto = cuadrícula (ancho) + margen superior + footer
VENTANA = pygame.display.set_mode((ANCHO_VENTANA, ANCHO_VENTANA + MARGEN_SUPERIOR + ALTURA_FOOTER))
pygame.display.set_caption("A* (diagonales coherentes) - Paso/Auto")

FUENTE = pygame.font.SysFont(None, 18)
FUENTE_BOTON = pygame.font.SysFont(None, 24)
FUENTE_FOOTER = pygame.font.SysFont(None, 18)

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
        # y toma en cuenta el margen superior
        self.y = fila * ancho + MARGEN_SUPERIOR
        self.color = BLANCO
        self.vecinos = []
        self.filas = filas
        self.cols = cols
        # A* scores
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

        # Mostrar G, H, F con letras (si están definidos)
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
        """
        Permitir 8 direcciones, pero aplicar la regla especial:
        - Si movimiento es diagonal, se PROHÍBE solo si AMBOS ortogonales adyacentes son muros.
          (Esto implementa la regla que pediste: ejemplo (2,3)->(3,4) bloqueada
           solo si (2,4) y (3,3) son muros).
        """
        self.vecinos = []
        # 8 direcciones
        direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1),
                       (-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dr, dc in direcciones:
            nf = self.fila + dr
            nc = self.col + dc
            if 0 <= nf < self.filas and 0 <= nc < self.cols:
                vecino = grid[nf][nc]
                if vecino.es_pared():
                    continue

                # Si es diagonal -> comprobar los dos ortogonales adyacentes
                if abs(dr) == 1 and abs(dc) == 1:
                    orto1 = grid[self.fila][nc]   # mismo fila, col del vecino
                    orto2 = grid[nf][self.col]   # fila del vecino, misma col
                    # Solo bloquear si ambos ortogonales son muros
                    if orto1.es_pared() and orto2.es_pared():
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

# ---------------- A* con paso a paso y tracking de listas (abierta/ cerrada) ----------------
class AStar:
    def __init__(self, grid, inicio, fin, open_order_list, closed_order_list):
        self.grid = grid
        self.inicio = inicio
        self.fin = fin
        self.came_from = {}
        self.counter = 0            # para desempate por orden de descubrimiento
        self.open_heap = []        # heap de (f, contador, nodo)
        self.open_hash = set()     # nodos actualmente en "open"
        self.closed_set = set()
        self.running = True
        self.finished = False
        self.found = False

        # listas con orden de descubrimiento / procesamiento (para mostrar en footer)
        # estas listas son referencias externas (se actualizan para dibujarlas en la UI)
        self.open_order_list = open_order_list
        self.closed_order_list = closed_order_list

        # Inicializar G/H/F
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
        # registrar inicio en lista abierta como descubierto primero
        self.open_order_list.append(self.inicio)
        self.counter += 1

    def step(self):
        # Si ya no hay abiertos
        while self.open_heap and True:
            _, _, actual = heapq.heappop(self.open_heap)
            # ignorar entradas antiguas del heap (lazy deletion)
            if actual not in self.open_hash:
                continue
            # Procesamos el nodo actual
            break
        else:
            # no quedó ninguno en heap
            self.finished = True
            self.running = False
            return 'no_path'

        # remover de open_hash y open_order_list (pasa a cerrada)
        if actual in self.open_hash:
            self.open_hash.remove(actual)
        # quitar de open_order_list si está (mantener descubrimiento en orden original, pero borrarlo al procesar)
        if actual in self.open_order_list:
            try:
                self.open_order_list.remove(actual)
            except ValueError:
                pass

        # marcar como cerrado (visual)
        if actual != self.inicio and actual != self.fin:
            actual.hacer_cerrado()
        self.closed_set.add(actual)
        # agregar al final de la lista cerrada (orden de procesamiento)
        self.closed_order_list.append(actual)

        # si actual es fin -> reconstruir camino
        if actual == self.fin:
            reconstruir_camino(self.came_from, self.fin, lambda: None)
            self.fin.hacer_fin()
            self.inicio.hacer_inicio()
            self.finished = True
            self.found = True
            return 'found'

        # explorar vecinos
        for vecino in actual.vecinos:
            if vecino in self.closed_set:
                continue

            # coste movimiento
            dr = abs(vecino.fila - actual.fila)
            dc = abs(vecino.col - actual.col)
            coste_mov = COSTE_DIAG if (dr == 1 and dc == 1) else COSTE_RECTA
            temp_g = actual.g + coste_mov

            if temp_g < vecino.g:
                self.came_from[vecino] = actual
                vecino.g = temp_g
                vecino.h = heuristica(vecino.get_pos(), self.fin.get_pos())
                vecino.f = vecino.g + vecino.h

                # si no estaba en open -> añadir y registrar orden de descubrimiento
                if vecino not in self.open_hash:
                    heapq.heappush(self.open_heap, (vecino.f, self.counter, vecino))
                    self.open_hash.add(vecino)
                    self.open_order_list.append(vecino)   # registro para mostrar Abierta en orden descubierto
                    self.counter += 1
                    vecino.hacer_abierto()
                else:
                    # si ya estaba en open, reinsertamos nueva entrada (lazy update)
                    heapq.heappush(self.open_heap, (vecino.f, self.counter, vecino))
                    self.counter += 1
                    vecino.hacer_abierto()

        return 'running'

# ---------------- Crear cuadrícula dinámica filas x cols ----------------
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

# ---------------- Dibujado UI ----------------
def dibujar_boton(ventana, rect, texto, color_fondo=AZUL):
    pygame.draw.rect(ventana, color_fondo, rect, border_radius=8)
    txt = FUENTE_BOTON.render(texto, True, BLANCO)
    ventana.blit(txt, (rect.x + (rect.width - txt.get_width()) // 2, rect.y + (rect.height - txt.get_height()) // 2))

def dibujar(ventana, grid, open_list, closed_list):
    ventana.fill(BLANCO)
    # botones superiores
    boton_iniciar = pygame.Rect(10, 10, 130, 40)
    boton_paso = pygame.Rect(150, 10, 100, 40)
    boton_reset = pygame.Rect(270, 10, 100, 40)
    boton_ejemplo = pygame.Rect(390, 10, 120, 40)

    dibujar_boton(ventana, boton_iniciar, "Iniciar A*")
    dibujar_boton(ventana, boton_paso, "Paso")
    dibujar_boton(ventana, boton_reset, "Reset")
    dibujar_boton(ventana, boton_ejemplo, "Cargar Ejemplo")

    # dibujar nodos
    for fila in grid:
        for nodo in fila:
            nodo.dibujar(ventana)

    # footer: dibujar listas Abierta y Cerrada como texto plano
    footer_y = ANCHO_VENTANA + MARGEN_SUPERIOR + 6
    # Preparar strings (usar 1-indexado para lectura humana)
    abierta_str = "Abierta: "
    if not open_list:
        abierta_str += "(vacía)"
    else:
        abierta_str += " ".join(f"({n.fila+1},{n.col+1})" for n in open_list)

    cerrada_str = "Cerrada: "
    if not closed_list:
        cerrada_str += "(vacía)"
    else:
        cerrada_str += " ".join(f"({n.fila+1},{n.col+1})" for n in closed_list)

    txt_abierta = FUENTE_FOOTER.render(abierta_str, True, NEGRO)
    txt_cerrada = FUENTE_FOOTER.render(cerrada_str, True, NEGRO)

    ventana.blit(txt_abierta, (10, footer_y))
    ventana.blit(txt_cerrada, (10, footer_y + 22))

    pygame.display.update()
    return boton_iniciar, boton_paso, boton_reset, boton_ejemplo

# ---------------- Obtener posición del click en la cuadrícula ----------------
def obtener_click_pos(pos, filas, cols, ancho_total):
    x, y = pos
    if y < MARGEN_SUPERIOR:
        return None
    if y > MARGEN_SUPERIOR + (ancho_total // cols) * filas:
        return None
    ancho_nodo = ancho_total // cols
    fila = (y - MARGEN_SUPERIOR) // ancho_nodo
    col = x // ancho_nodo
    if 0 <= fila < filas and 0 <= col < cols:
        return fila, col
    return None

# ---------------- Ejemplo (tu 3x5 con muros especificados) ----------------
def cargar_ejemplo(grid):
    for f in grid:
        for n in f:
            n.restablecer()
    inicio = grid[0][0]     # 1-1
    fin = grid[2][4]        # 3-5
    inicio.hacer_inicio()
    fin.hacer_fin()
    # muros en 1-2, 2-4, 3-3 (1-indexed -> convertimos a 0-index)
    muros = [(0,1),(1,3),(2,2)]
    for r, c in muros:
        if 0 <= r < FILAS and 0 <= c < COLS:
            grid[r][c].hacer_pared()
    return inicio, fin

def reset_grid(grid):
    for f in grid:
        for n in f:
            n.restablecer()

# ---------------- Programa principal ----------------
def main():
    clock = pygame.time.Clock()
    ancho_total = ANCHO_VENTANA
    grid = crear_grid(FILAS, COLS, ancho_total)

    # Precalcular vecinos
    for fila in grid:
        for n in fila:
            n.actualizar_vecinos(grid)

    inicio = None
    fin = None
    astar = None
    auto_run = False

    # listas para mostrar (referencias que AStar actualizará)
    open_order_list = []
    closed_order_list = []

    corriendo = True
    while corriendo:
        clock.tick(30)
        botones = dibujar(VENTANA, grid, open_order_list, closed_order_list)
        boton_iniciar, boton_paso, boton_reset, boton_ejemplo = botones

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False
                break

            if evento.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                # botones
                if boton_iniciar.collidepoint(pos):
                    if inicio and fin:
                        # recalcular vecinos (por si cambiaron muros)
                        for fila in grid:
                            for n in fila:
                                n.actualizar_vecinos(grid)
                        # resetear listas de tracking
                        open_order_list.clear()
                        closed_order_list.clear()
                        astar = AStar(grid, inicio, fin, open_order_list, closed_order_list)
                        auto_run = True
                    continue

                if boton_paso.collidepoint(pos):
                    if inicio and fin:
                        if astar is None or astar.finished:
                            for fila in grid:
                                for n in fila:
                                    n.actualizar_vecinos(grid)
                            open_order_list.clear()
                            closed_order_list.clear()
                            astar = AStar(grid, inicio, fin, open_order_list, closed_order_list)
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
                    open_order_list.clear()
                    closed_order_list.clear()
                    continue

                if boton_ejemplo.collidepoint(pos):
                    # cargar ejemplo (asegúrate de que FILAS>=3 && COLS>=5 en configuración)
                    if FILAS >= 3 and COLS >= 5:
                        inicio, fin = cargar_ejemplo(grid)
                        # recalcular vecinos
                        for fila in grid:
                            for n in fila:
                                n.actualizar_vecinos(grid)
                        astar = None
                        auto_run = False
                        open_order_list.clear()
                        closed_order_list.clear()
                    continue

                # clicks en la cuadrícula
                click = obtener_click_pos(pos, FILAS, COLS, ancho_total)
                if click:
                    f, c = click
                    nodo = grid[f][c]
                    if evento.button == 1:  # izquierdo
                        if not inicio and nodo != fin:
                            inicio = nodo
                            inicio.hacer_inicio()
                        elif not fin and nodo != inicio:
                            fin = nodo
                            fin.hacer_fin()
                        elif nodo != inicio and nodo != fin:
                            nodo.hacer_pared()
                    elif evento.button == 3:  # derecho -> restablecer
                        if nodo == inicio:
                            inicio = None
                        if nodo == fin:
                            fin = None
                        nodo.restablecer()
                        # si se borraron muros, recalcular vecinos (no inmediato necesario)
                        # pero la próxima inicialización recalculará
        # Auto-run: avanzar varios pasos por frame
        if auto_run and astar and not astar.finished:
            pasos_por_frame = 2
            for _ in range(pasos_por_frame):
                estado = astar.step()
                if estado in ('found', 'no_path'):
                    auto_run = False
                    break

        # Si A* terminó y encontró camino, reconstruir visualmente (una vez)
        if astar and astar.finished and astar.found:
            reconstruir_camino(astar.came_from, astar.fin, lambda: None)
            astar.found = False  # evitar repetir reconstrucción

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
