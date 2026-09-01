# -*- coding: utf-8 -*-
"""Строит SVG-контур России (проекция Альберса) и проецирует города точек продаж.
   Результат: site/data/map-russia.json — путь контура, viewBox и координаты городов."""
import json, math, os

SRC_GEO = "russia10.geojson"   # Natural Earth 10m, российская точка зрения (с Крымом)
LOC = r"C:\Users\user\Desktop\Сайт FERES\site\data\locations.json"
OUT = r"C:\Users\user\Desktop\Сайт FERES\site\data\map-russia.json"

# --- Проекция Альберса (равновеликая коническая), стандартная для карт России
LON0, LAT0, LAT1, LAT2 = 100.0, 56.0, 50.0, 70.0
r = math.radians
n = 0.5 * (math.sin(r(LAT1)) + math.sin(r(LAT2)))
C = math.cos(r(LAT1)) ** 2 + 2 * n * math.sin(r(LAT1))
RHO0 = math.sqrt(C - 2 * n * math.sin(r(LAT0))) / n

def albers(lon, lat):
    if lon < 0:                      # Чукотка за 180-м меридианом
        lon += 360
    theta = n * r(lon - LON0)
    rho = math.sqrt(max(C - 2 * n * math.sin(r(lat)), 1e-9)) / n
    return rho * math.sin(theta), RHO0 - rho * math.cos(theta)

def dp(points, tol):
    """Упрощение Дугласа — Пекера."""
    if len(points) < 3:
        return points
    def dist(p, a, b):
        (x, y), (x1, y1), (x2, y2) = p, a, b
        dx, dy = x2 - x1, y2 - y1
        if dx == 0 and dy == 0:
            return math.hypot(x - x1, y - y1)
        t = max(0, min(1, ((x - x1) * dx + (y - y1) * dy) / (dx * dx + dy * dy)))
        return math.hypot(x - (x1 + t * dx), y - (y1 + t * dy))
    dmax, idx = 0, 0
    for i in range(1, len(points) - 1):
        d = dist(points[i], points[0], points[-1])
        if d > dmax:
            dmax, idx = d, i
    if dmax > tol:
        return dp(points[:idx + 1], tol)[:-1] + dp(points[idx:], tol)
    return [points[0], points[-1]]

def ring_area(pts):
    s = 0
    for i in range(len(pts)):
        x1, y1 = pts[i]
        x2, y2 = pts[(i + 1) % len(pts)]
        s += x1 * y2 - x2 * y1
    return abs(s) / 2

geo = json.load(open(SRC_GEO, encoding="utf-8"))
polys = geo["geometry"]["coordinates"]

import sys
sys.setrecursionlimit(20000)
rings = []
for poly in polys:
    outer = poly[0]
    if len(outer) > 4000:                    # предварительное прореживание крупных колец
        step = len(outer) // 4000 + 1
        outer = outer[::step] + [outer[-1]]
    pts = [albers(lon, lat) for lon, lat in outer]
    if ring_area(pts) > 0.00015:             # выбрасываем острова мельче ~6000 км²
        rings.append(pts)

xs = [p[0] for ring in rings for p in ring]
ys = [p[1] for ring in rings for p in ring]
minx, maxx, miny, maxy = min(xs), max(xs), min(ys), max(ys)
W = 1200.0
scale = W / (maxx - minx)
H = (maxy - miny) * scale

def to_svg(p):
    return ((p[0] - minx) * scale, H - (p[1] - miny) * scale)

tol = 0.0011
paths = []
for ring in rings:
    simp = dp(ring, tol)
    pts = [to_svg(p) for p in simp]
    d = "M" + " ".join("%.1f %.1f" % pt for pt in pts) + "Z"
    paths.append(d)

locations = json.load(open(LOC, encoding="utf-8"))["locations"]
cities = {}
for loc in locations:
    if loc["lat"] is None:
        continue
    cities.setdefault(loc["city"], {"city": loc["city"], "lat": loc["lat"], "lon": loc["lon"], "ids": []})
    cities[loc["city"]]["ids"].append(loc["id"])
points = []
for c in cities.values():
    x, y = to_svg(albers(c["lon"], c["lat"]))
    points.append({"city": c["city"], "ids": c["ids"],
                   "x": round(x / W * 100, 3), "y": round(y / H * 100, 3)})   # в процентах

out = {
    "meta": {"projection": "Albers Equal Area (lon0=100, lat1=50, lat2=70)",
             "note": "Контур — Natural Earth 110m, упрощён. Точки позиционируются в процентах от габарита карты.",
             "viewBox": "0 0 %d %d" % (round(W), round(H))},
    "paths": paths,
    "points": sorted(points, key=lambda p: p["x"])
}
json.dump(out, open(OUT, "w", encoding="utf-8"), ensure_ascii=False)
print("контуров:", len(paths), "точек городов:", len(points),
      "размер файла:", round(os.path.getsize(OUT) / 1024, 1), "КБ", "viewBox", out["meta"]["viewBox"])
