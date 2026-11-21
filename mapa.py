# -*- coding: utf-8 -*-
"""Mapa de destinos en puntos, generado una vez desde Natural Earth (dominio publico, via world-atlas).

Convierte la tierra en una rejilla de puntos (un <path> compacto) y calcula los arcos desde Valencia.
Lo usa build.py. Sin dependencias.
"""
import json, os

RAIZ = os.path.dirname(os.path.abspath(__file__))

# Recorte: de Seattle a Egipto, con margen
LON0, LON1, LAT0, LAT1 = -132.0, 48.0, 8.0, 66.0
PASO = 1.6            # grados entre puntos
ESCALA = 6.0          # px de SVG por grado
W = round((LON1 - LON0) * ESCALA)
H = round((LAT1 - LAT0) * ESCALA)

BASE = ("Valencia", -0.38, 39.47)
# Ciudades: posicion real. Paises: punto aproximado dentro del pais (no un puerto concreto).
DESTINOS = [
    ("Seattle", -122.33, 47.61, "c"), ("Nueva York", -74.0, 40.71, "c"), ("Miami", -80.19, 25.76, "c"),
    ("St. Thomas", -64.93, 18.34, "c"),
    ("Francia", 2.4, 46.6, "p"), ("Italia", 12.6, 42.8, "p"), ("Croacia", 15.6, 45.0, "p"), ("Grecia", 22.0, 39.3, "p"),
    ("Alemania", 10.2, 51.0, "p"), ("Holanda", 5.4, 52.2, "p"), ("Bélgica", 4.6, 50.6, "p"),
    ("Turquía", 33.0, 39.2, "p"), ("Egipto", 30.2, 26.8, "p"),
    ("Islas Canarias", -15.6, 28.2, "c"),
]
NOMBRES_EN = {"Nueva York": "New York", "Francia": "France", "Italia": "Italy", "Croacia": "Croatia", "Grecia": "Greece",
              "Alemania": "Germany", "Holanda": "Netherlands", "Bélgica": "Belgium", "Turquía": "Turkey", "Egipto": "Egypt", "Islas Canarias": "Canary Islands"}
# Etiquetas visibles en el mapa (Europa va agrupada para que no se pisen)
ETIQUETAS = {"Seattle": (0, -12, "middle"), "Nueva York": (8, -8, "start"), "Miami": (-8, 4, "end"),
             "St. Thomas": (8, 12, "start"), "Turquía": (10, -6, "start"), "Egipto": (10, 6, "start"),
             "Islas Canarias": (-10, 6, "end")}


def xy(lon, lat):
    return (lon - LON0) * ESCALA, (LAT1 - lat) * ESCALA


def _poligonos():
    topo = json.load(open(os.path.join(RAIZ, "src/mapa/land-110m.json")))
    sx, sy = topo["transform"]["scale"]; tx, ty = topo["transform"]["translate"]
    arcs = []
    for arc in topo["arcs"]:
        x = y = 0; pts = []
        for dx, dy in arc:
            x += dx; y += dy
            pts.append((x * sx + tx, y * sy + ty))
        arcs.append(pts)

    def anillo(idx):
        pts = []
        for i in idx:
            a = arcs[i] if i >= 0 else arcs[~i][::-1]
            pts.extend(a if not pts else a[1:])
        return pts

    polis = []
    for g in topo["objects"]["land"]["geometries"]:
        coords = g["arcs"] if g["type"] == "MultiPolygon" else [g["arcs"]]
        for poly in coords:
            polis.append([anillo(r) for r in poly])
    return polis


def _dentro(lon, lat, anillo):
    c = False; n = len(anillo); j = n - 1
    for i in range(n):
        xi, yi = anillo[i]; xj, yj = anillo[j]
        if (yi > lat) != (yj > lat) and lon < (xj - xi) * (lat - yi) / (yj - yi + 1e-12) + xi:
            c = not c
        j = i
    return c


def puntos():
    polis = _poligonos()
    # cajas para descartar rapido
    cajas = []
    for p in polis:
        xs = [q[0] for q in p[0]]; ys = [q[1] for q in p[0]]
        cajas.append((min(xs), max(xs), min(ys), max(ys)))
    trozos = []
    lat = LAT1 - PASO / 2
    fila = 0
    while lat > LAT0:
        lon = LON0 + PASO / 2 + (PASO / 2 if fila % 2 else 0)
        while lon < LON1:
            for p, (x0, x1, y0, y1) in zip(polis, cajas):
                if x0 <= lon <= x1 and y0 <= lat <= y1 and _dentro(lon, lat, p[0]) and not any(_dentro(lon, lat, h) for h in p[1:]):
                    x, y = xy(lon, lat)
                    trozos.append(f"M{x:.0f} {y:.0f}h0")
                    break
            lon += PASO
        lat -= PASO; fila += 1
    return "".join(trozos)


def svg(lang, aria):
    bx, by = xy(BASE[1], BASE[2])
    arcos, pines, etiquetas = [], [], []
    for i, (n, lon, lat, tipo) in enumerate(DESTINOS):
        x, y = xy(lon, lat)
        d = ((x - bx) ** 2 + (y - by) ** 2) ** .5
        cx, cy = (bx + x) / 2, (by + y) / 2 - d * .2
        arcos.append(f'<path class="arco" style="--i:{i}" pathLength="1" d="M{bx:.0f} {by:.0f}Q{cx:.0f} {cy:.0f} {x:.0f} {y:.0f}"/>')
        pines.append(f'<circle class="pin" style="--i:{i}" cx="{x:.0f}" cy="{y:.0f}" r="4"/>')
        if n in ETIQUETAS:
            dx, dy, anc = ETIQUETAS[n]
            txt = NOMBRES_EN.get(n, n) if lang == "en" else n
            etiquetas.append(f'<text class="et" style="--i:{i}" x="{x + dx:.0f}" y="{y + dy:.0f}" text-anchor="{anc}">{txt}</text>')
    europa = "Europa" if lang == "es" else "Europe"
    ex, ey = xy(8.5, 55.5)
    etiquetas.append(f'<text class="et" style="--i:9" x="{ex:.0f}" y="{ey:.0f}" text-anchor="middle">{europa}</text>')
    return (f'<svg class="mapa-svg" viewBox="0 0 {W} {H}" role="img" aria-label="{aria}">'
            f'<path class="tierra" d="{puntos()}"/>'
            f'<g class="arcos">{"".join(arcos)}</g><g class="pines">{"".join(pines)}</g>'
            f'<circle class="base-halo" cx="{bx:.0f}" cy="{by:.0f}" r="12"/><circle class="base-pin" cx="{bx:.0f}" cy="{by:.0f}" r="5.5"/>'
            f'<text class="et et-base" x="{bx - 10:.0f}" y="{by + 18:.0f}" text-anchor="end">Valencia</text>'
            f'<g class="etiquetas">{"".join(etiquetas)}</g></svg>')


if __name__ == "__main__":
    s = svg("es", "Mapa")
    print(W, H, len(s), s.count("h0"))
