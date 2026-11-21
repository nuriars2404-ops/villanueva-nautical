"""Prepara las fotos de src/fotos en img/: dos anchos (movil y original), WebP + JPEG.
Uso: python prep_fotos.py   (necesita Pillow). Escribe img/fotos.json con medidas para build.py.
Las de src/antes-despues/<trabajo>/{antes,proceso,despues}.jpg tambien se procesan si existen."""
import json, os, glob
from PIL import Image

RAIZ = os.path.dirname(os.path.abspath(__file__))
SAL = os.path.join(RAIZ, "img")
RECORTES = {"cubierta-angulo": (0, 0, 1, .86)}   # quita la franja oscura que dejo Wix abajo
ANCHO_MOVIL = 560

def variantes(im, base):
    w0, h0 = im.size
    anchos = sorted({min(ANCHO_MOVIL, w0), w0})
    fuera = []
    for a in anchos:
        h = round(a * h0 / w0)
        c = im if a == w0 else im.resize((a, h), Image.LANCZOS)
        c.save(os.path.join(SAL, f"{base}-{a}.webp"), "WEBP", quality=80, method=6)
        c.save(os.path.join(SAL, f"{base}-{a}.jpg"), "JPEG", quality=82, optimize=True, progressive=True)
        fuera.append([a, h])
    return fuera

def abre(ruta, base):
    im = Image.open(ruta).convert("RGB")
    if base in RECORTES:
        x0, y0, x1, y1 = RECORTES[base]; w, h = im.size
        im = im.crop((round(x0*w), round(y0*h), round(x1*w), round(y1*h)))
    return im

os.makedirs(SAL, exist_ok=True)
datos = {}
for ruta in sorted(glob.glob(os.path.join(RAIZ, "src/fotos/*"))):
    if not ruta.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
        continue
    base = os.path.splitext(os.path.basename(ruta))[0]
    if base == "logo":
        continue
    datos[base] = variantes(abre(ruta, base), base)
for ruta in sorted(glob.glob(os.path.join(RAIZ, "src/antes-despues/*/*.*"))):
    if not ruta.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
        continue
    trabajo = os.path.basename(os.path.dirname(ruta))
    base = f"{trabajo}-{os.path.splitext(os.path.basename(ruta))[0]}"
    datos[base] = variantes(abre(ruta, base), base)

# Imagen para compartir (WhatsApp): 1200x630, archivo suelto
im = Image.open(os.path.join(RAIZ, "src/fotos/cunas-varada.jpg")).convert("RGB")
w, h = im.size; th = round(w * 630 / 1200); y = (h - th) // 2
im.crop((0, y, w, y + th)).resize((1200, 630), Image.LANCZOS).save(os.path.join(SAL, "compartir.jpg"), "JPEG", quality=85, optimize=True)

json.dump(datos, open(os.path.join(SAL, "fotos.json"), "w"), indent=1)
print(json.dumps(datos))
