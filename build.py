# -*- coding: utf-8 -*-
"""Genera la web de Villanueva Nautical Services en dos idiomas desde una sola plantilla.

    python prep_fotos.py   # cuando cambian fotos (necesita Pillow)
    python build.py        # escribe index.html, es/index.html y en/index.html

Antes / proceso / despues: crea src/antes-despues/<trabajo>/ con antes.jpg, proceso.jpg,
despues.jpg y un info.json {"titulo_es","titulo_en","texto_es","texto_en"}. Pasa prep_fotos.py
y build.py y la seccion aparece sola. Sin esa carpeta, la seccion no existe.
"""
import json, os, html, glob

RAIZ = os.path.dirname(os.path.abspath(__file__))
BASE = "https://nuriars2404-ops.github.io/villanueva-nautical/"
VERSION = "2"
WA = "34669239433"
TEL = "+34669239433"
TEL_VER = "+34 669 239 433"
EMAIL = "villanueva.nautical.services@gmail.com"
IG = "https://www.instagram.com/villanuevanauticalservices/"
GOOGLE = "https://www.google.com/maps/search/?api=1&query=Villanueva+Nautical+Services+Valencia"

FOTOS = json.load(open(os.path.join(RAIZ, "img/fotos.json")))

# Destinos: lista dada por el propio negocio (21/11/2026)
DESTINOS = {
    "es": [("América y Caribe", ["Miami", "Nueva York", "Seattle", "St. Thomas"]),
           ("Europa", ["España", "Francia", "Italia", "Croacia", "Grecia", "Alemania", "Holanda", "Bélgica"]),
           ("Mediterráneo oriental", ["Turquía", "Egipto"])],
    "en": [("Americas & Caribbean", ["Miami", "New York", "Seattle", "St. Thomas"]),
           ("Europe", ["Spain", "France", "Italy", "Croatia", "Greece", "Germany", "Netherlands", "Belgium"]),
           ("Eastern Mediterranean", ["Turkey", "Egypt"])],
}

# Resenas de Google copiadas tal cual (21/11/2026). Solo las que tienen texto.
RESENAS = [
    ("Elihu M.", "Muy profesional , atento al detalle !!! Recomendable 100%",
     "Very professional, great attention to detail!!! 100% recommended"),
    ("Anthony F.", "Calidad y servicio 10/10", "Quality and service 10/10"),
    ("Cesar C.", "He trabajado con ellos y son el top en carpintería náutica.\nMuy profesionales y comprometidos con la calidad.",
     "I have worked with them and they are the best in marine carpentry.\nVery professional and committed to quality."),
]

T = {
 "es": {
  "lang": "es", "locale": "es_ES", "otro": "en", "otro_nombre": "English", "otro_corto": "EN",
  "title": "Villanueva Nautical Services · Cubiertas de teca y carpintería naval",
  "desc": "Renovación de cubiertas de teca, cambio de Sikaflex y carpintería naval a medida. Con base en Valencia, trabajamos donde esté tu barco.",
  "nav": [("servicios", "Servicios"), ("trabajos", "Trabajos"), ("destinos", "Destinos"), ("contacto", "Contacto")],
  "wa_corto": "WhatsApp", "wa_largo": "Escríbenos por WhatsApp", "llamar": "Llamar",
  "wa_msg": "Hola, os escribo desde la web de Villanueva Nautical Services. Quería información sobre ",
  "eyebrow": "Carpintería naval · Valencia · Desde 2009",
  "h1": "Teca hecha para durar lo que dura el barco",
  "hero_p": "Renovamos cubiertas de teca, cambiamos el Sikaflex y hacemos carpintería a medida para yates y veleros. Con base en Valencia, trabajamos donde esté tu barco: de Miami a Croacia.",
  "cinta": ["Teca", "Sikaflex", "Carpintería", "Mantenimiento", "Calafateado", "Cubiertas"],
  "serv_kicker": "Servicios", "serv_h2": "Cuatro oficios, una sola cubierta",
  "serv_p": "Trabajamos la madera de teca de principio a fin: desde quitar la cubierta gastada hasta el último remate del interior.",
  "servicios": [
    ("cubierta-curva", "Renovación de cubierta en teca", "Retiramos la cubierta gastada y montamos teca nueva a medida, tabla a tabla, con sus curvas, juntas y remates."),
    ("cubierta-angulo", "Cambio de Sikaflex", "Sacamos las juntas viejas, limpiamos y volvemos a calafatear para que la cubierta quede estanca y con la línea negra impecable."),
    ("cofre-interior", "Carpintería interior y exterior", "Camarotes, cocinas, cofres, tapas y remates a medida, dentro y fuera del barco, en madera que aguanta el mar."),
    ("tapa-cubierta", "Mantenimiento de cubierta", "Lijado, limpieza y repaso de juntas con un plan pensado para que la cubierta acompañe al barco hasta sus 100 años."),
  ],
  "ofi_kicker": "Oficio", "ofi_h2": "Más de quince años con las manos en la teca",
  "ofi_p": "Somos carpinteros navales. Medimos, cortamos y ajustamos cada pieza en el propio barco, con la paciencia que pide una madera que tiene que vivir al sol y al salitre durante décadas.",
  "stat1_n": "+15", "stat1_t": "años de experiencia", "stat2_n": "14", "stat2_t": "destinos donde hemos trabajado",
  "ofi_alt": "Cunas de madera hechas a medida para un velero de regatas en varadero, al atardecer",
  "proc_kicker": "Proceso", "proc_h2": "Cómo trabajamos",
  "pasos": [("Inspección", "Vemos el barco o nos mandas fotos. Medimos, revisamos el grosor de la teca y el estado de las juntas."),
            ("Preparación", "Retiramos lo que hay que cambiar y dejamos la base limpia, seca y lista para trabajar."),
            ("Montaje y calafateado", "Ajustamos cada tabla en su sitio y sellamos las juntas con Sikaflex."),
            ("Lijado y acabado", "Lijamos, repasamos remates y entregamos la cubierta lista para navegar.")],
  "trab_kicker": "Trabajos", "trab_h2": "Hecho a mano, tabla a tabla",
  "trab_p": "Algunos de nuestros trabajos. Toca una foto para verla en grande.",
  "alts": {"proa-teca": "Pasillo lateral de un yate con cubierta de teca nueva y el puerto al fondo",
           "cubierta-curva": "Cubierta de teca curvada con juntas negras junto a la superestructura de un yate",
           "tapa-cubierta": "Tapa de registro en cubierta de teca con marco curvo y bisagras de acero",
           "cubierta-angulo": "Encuentro en ángulo de dos paños de cubierta de teca",
           "cunas-varada": "Cunas de madera para un velero de regatas en varadero",
           "cofre-interior": "Cofre interior de teca con tapa abierta y puerta de rejilla"},
  "ad_kicker": "Antes y después", "ad_h2": "Del desgaste a la teca nueva", "ad_rango": "Desliza para comparar antes y después", "ad_antes": "Antes", "ad_proceso": "Proceso", "ad_despues": "Después",
  "dest_kicker": "Destinos", "dest_h2": "Donde esté tu barco",
  "dest_p": "Nuestra base está en Valencia, pero vamos al barco. Estos son los sitios donde ya hemos trabajado:",
  "res_kicker": "Reseñas", "res_h2": "Lo que dicen en Google", "res_link": "Ver las reseñas en Google",
  "faq_kicker": "Preguntas", "faq_h2": "Lo que nos preguntan siempre",
  "faq": [("¿Os desplazáis fuera de España?", "Sí. Hemos trabajado en Miami, Nueva York, Seattle y St. Thomas, y en Francia, Italia, Croacia, Grecia, Alemania, Holanda, Bélgica, Turquía y Egipto. Dinos dónde está el barco y lo organizamos."),
          ("¿Puedo pedir presupuesto enviando fotos?", "Sí. Mándanos por WhatsApp fotos de la cubierta o de la zona que quieres arreglar, la eslora y el puerto, y te damos una primera valoración. El presupuesto definitivo se cierra al ver el barco."),
          ("¿Cuánto se tarda en renovar una cubierta?", "Depende de los metros de teca, de su estado y de si se cambia todo o solo las juntas. Te damos el plazo concreto junto con el presupuesto."),
          ("¿Hay que cambiar toda la teca o basta con el Sikaflex?", "Si la madera conserva grosor suficiente, muchas veces basta con renovar las juntas y lijar. Lo comprobamos en la inspección y te decimos qué compensa.")],
  "con_kicker": "Contacto", "con_h2": "Cuéntanos tu barco",
  "con_p": "Rellena lo que sepas y te abrimos WhatsApp con el mensaje ya escrito. Solo tienes que enviarlo.",
  "f_nombre": "Tu nombre", "f_barco": "Tipo de barco", "f_barcos": ["Velero", "Yate a motor", "Barco clásico", "Otro"],
  "f_eslora": "Eslora (metros)", "f_trabajo": "¿Qué necesitas?", "f_trabajos": ["Renovación de cubierta en teca", "Cambio de Sikaflex", "Carpintería interior o exterior", "Mantenimiento de cubierta", "Otra cosa"],
  "f_donde": "¿Dónde está el barco?", "f_donde_ph": "Puerto, ciudad o país", "f_detalles": "Algo más que debamos saber",
  "f_enviar": "Enviar por WhatsApp", "f_nota": "Se abre WhatsApp con tu mensaje. No guardamos nada en esta web.",
  "f_noscript": "Escribe tu mensaje y pulsa enviar: se abrirá WhatsApp.",
  "m_hola": "Hola, os escribo desde la web de Villanueva Nautical Services.", "m_nombre": "Nombre", "m_barco": "Barco", "m_trabajo": "Trabajo", "m_donde": "Dónde está", "m_detalles": "Detalles", "m_eslora": "m",
  "directo": "O directamente", "ig": "Instagram", "email": "Email",
  "pie": "Carpintería naval y cubiertas de teca. Base en Valencia, trabajos en todo el mundo.",
  "cerrar": "Cerrar", "elige": "Elige…", "ver_foto": "Ver foto en grande",
 },
 "en": {
  "lang": "en", "locale": "en_GB", "otro": "es", "otro_nombre": "Español", "otro_corto": "ES",
  "title": "Villanueva Nautical Services · Teak decks and marine carpentry",
  "desc": "Teak deck renewal, re-caulking and bespoke marine joinery. Based in Valencia, Spain, working wherever your yacht is.",
  "nav": [("servicios", "Services"), ("trabajos", "Work"), ("destinos", "Locations"), ("contacto", "Contact")],
  "wa_corto": "WhatsApp", "wa_largo": "Message us on WhatsApp", "llamar": "Call",
  "wa_msg": "Hello, I'm writing from the Villanueva Nautical Services website. I'd like some information about ",
  "eyebrow": "Marine carpentry · Valencia, Spain · Since 2009",
  "h1": "Teak built to last as long as the yacht",
  "hero_p": "We renew teak decks, replace deck caulking and build bespoke joinery for yachts and sailing boats. Based in Valencia, we work wherever your boat is: from Miami to Croatia.",
  "cinta": ["Teak", "Caulking", "Joinery", "Maintenance", "Sikaflex", "Decks"],
  "serv_kicker": "Services", "serv_h2": "Four crafts, one deck",
  "serv_p": "We handle teak from start to finish: from lifting a worn deck to the last trim piece below deck.",
  "servicios": [
    ("cubierta-curva", "Teak deck renewal", "We lift the worn deck and lay new made-to-measure teak, plank by plank, with every curve, seam and finishing piece."),
    ("cubierta-angulo", "Sikaflex re-caulking", "We remove the old seams, clean them out and re-caulk so the deck is watertight again, with crisp black lines."),
    ("cofre-interior", "Interior and exterior joinery", "Cabins, galleys, lockers, hatches and trim made to measure, inside and outside the boat, in wood that stands up to the sea."),
    ("tapa-cubierta", "Deck maintenance", "Sanding, cleaning and seam repairs on a plan designed so the deck stays with the boat all the way to its 100th year."),
  ],
  "ofi_kicker": "Craft", "ofi_h2": "Over fifteen years with our hands on teak",
  "ofi_p": "We are marine carpenters. We measure, cut and fit every piece on the boat itself, with the patience a wood needs when it has to live in sun and salt for decades.",
  "stat1_n": "+15", "stat1_t": "years of experience", "stat2_n": "14", "stat2_t": "locations we have worked in",
  "ofi_alt": "Made-to-measure wooden cradles for a racing yacht in a boatyard at sunset",
  "proc_kicker": "Process", "proc_h2": "How we work",
  "pasos": [("Survey", "We see the boat or you send us photos. We measure, check the teak thickness and the condition of the seams."),
            ("Preparation", "We remove what needs replacing and leave a clean, dry base ready to work on."),
            ("Fitting and caulking", "Each plank is fitted in place and the seams are sealed with Sikaflex."),
            ("Sanding and finish", "We sand, go over the trim and hand back a deck ready to sail.")],
  "trab_kicker": "Work", "trab_h2": "Handmade, plank by plank",
  "trab_p": "A selection of our work. Tap a photo to see it larger.",
  "alts": {"proa-teca": "Side deck of a yacht with new teak decking and the harbour behind",
           "cubierta-curva": "Curved teak deck with black seams next to a yacht superstructure",
           "tapa-cubierta": "Hatch in a teak deck with a curved frame and steel hinges",
           "cubierta-angulo": "Angled joint between two sections of teak deck",
           "cunas-varada": "Wooden cradles for a racing yacht in a boatyard",
           "cofre-interior": "Interior teak locker with open lid and slatted door"},
  "ad_kicker": "Before and after", "ad_h2": "From worn deck to new teak", "ad_rango": "Slide to compare before and after", "ad_antes": "Before", "ad_proceso": "In progress", "ad_despues": "After",
  "dest_kicker": "Locations", "dest_h2": "Wherever your boat is",
  "dest_p": "We are based in Valencia, but we come to the boat. These are the places where we have already worked:",
  "res_kicker": "Reviews", "res_h2": "What people say on Google", "res_link": "See the reviews on Google",
  "res_trad": "Original review in Spanish. Our translation:",
  "faq_kicker": "Questions", "faq_h2": "What clients always ask",
  "faq": [("Do you travel outside Spain?", "Yes. We have worked in Miami, New York, Seattle and St. Thomas, and in France, Italy, Croatia, Greece, Germany, the Netherlands, Belgium, Turkey and Egypt. Tell us where the boat is and we will organise it."),
          ("Can I get a quote by sending photos?", "Yes. Send us photos of the deck or the area you want fixed on WhatsApp, along with the boat's length and port, and we will give you a first assessment. The final quote is confirmed once we see the boat."),
          ("How long does a deck renewal take?", "It depends on the square metres of teak, its condition and whether the whole deck or only the seams are replaced. We give you a firm timeline together with the quote."),
          ("Do I need a whole new deck or just new caulking?", "If the teak still has enough thickness, renewing the seams and sanding is often enough. We check it during the survey and tell you what is worth doing.")],
  "con_kicker": "Contact", "con_h2": "Tell us about your boat",
  "con_p": "Fill in what you know and we will open WhatsApp with the message ready. You just press send.",
  "f_nombre": "Your name", "f_barco": "Type of boat", "f_barcos": ["Sailing yacht", "Motor yacht", "Classic boat", "Other"],
  "f_eslora": "Length (metres)", "f_trabajo": "What do you need?", "f_trabajos": ["Teak deck renewal", "Sikaflex re-caulking", "Interior or exterior joinery", "Deck maintenance", "Something else"],
  "f_donde": "Where is the boat?", "f_donde_ph": "Port, city or country", "f_detalles": "Anything else we should know",
  "f_enviar": "Send via WhatsApp", "f_nota": "WhatsApp opens with your message. Nothing is stored on this website.",
  "f_noscript": "Write your message and press send: WhatsApp will open.",
  "m_hola": "Hello, I'm writing from the Villanueva Nautical Services website.", "m_nombre": "Name", "m_barco": "Boat", "m_trabajo": "Job", "m_donde": "Location", "m_detalles": "Details", "m_eslora": "m",
  "directo": "Or reach us directly", "ig": "Instagram", "email": "Email",
  "pie": "Marine carpentry and teak decks. Based in Valencia, working worldwide.",
  "cerrar": "Close", "elige": "Choose…", "ver_foto": "View larger photo",
 },
}

e = html.escape
ICO = {
 "wa": '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2Zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8-.2-.1-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.2-.4.7-1.4.1-.2 0-.3 0-.5l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.7 11.8 11.8 0 0 0 4.5 4c1.7.7 2.3.8 3.2.6.5-.1 1.5-.6 1.7-1.2.2-.6.2-1.1.2-1.2-.1-.1-.3-.2-.5-.3Z"/></svg>',
 "tel": '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round" d="M5 3h4l2 5-2.5 1.5a11 11 0 0 0 6 6L16 13l5 2v4a2 2 0 0 1-2 2A17 17 0 0 1 3 5a2 2 0 0 1 2-2Z"/></svg>',
 "mail": '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path fill="none" stroke="currentColor" stroke-width="1.8" d="M3 5h18v14H3z M3 6l9 7 9-7"/></svg>',
 "ig": '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5" fill="none" stroke="currentColor" stroke-width="1.8"/><circle cx="12" cy="12" r="4" fill="none" stroke="currentColor" stroke-width="1.8"/><circle cx="17.5" cy="6.5" r="1.2" fill="currentColor"/></svg>',
 "flecha": '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path fill="none" stroke="currentColor" stroke-width="1.8" d="M5 12h14M13 6l6 6-6 6"/></svg>',
}

def timon(cls="timon"):
    radios = "".join(f'<line x1="32" y1="32" x2="{32+29*c:.1f}" y2="{32+29*s:.1f}"/>' for c, s in
                     [(1,0),(0,1),(-1,0),(0,-1),(.707,.707),(-.707,.707),(.707,-.707),(-.707,-.707)])
    return (f'<svg class="{cls}" viewBox="0 0 64 64" aria-hidden="true"><g fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round">'
            f'<circle cx="32" cy="32" r="18"/><circle cx="32" cy="32" r="14.5" stroke-width="1.2"/>{radios}'
            f'<circle cx="32" cy="32" r="5"/></g></svg>')

def marca():
    return (f'<span class="marca">{timon()}<span class="marca-txt"><span class="m1">Villanueva</span>'
            f'<span class="m2">Nautical Services</span></span></span>')

def foto(base, alt, sizes, prioritaria=False, cls=""):
    v = FOTOS[base]
    carga = 'loading="eager" fetchpriority="high"' if prioritaria else 'loading="lazy" decoding="async"'
    w, h = v[-1]
    pre = "../img/"
    ss = lambda ext: ", ".join(f"{pre}{base}-{a}.{ext} {a}w" for a, _ in v)
    c = f' class="{cls}"' if cls else ""
    return (f'<picture{c}><source type="image/webp" srcset="{ss("webp")}" sizes="{sizes}">'
            f'<img src="{pre}{base}-{w}.jpg" srcset="{ss("jpg")}" sizes="{sizes}" width="{w}" height="{h}" alt="{e(alt)}" {carga}></picture>')

def wa_link(t, extra=""):
    from urllib.parse import quote
    return f"https://wa.me/{WA}?text={quote(t['wa_msg'] + extra)}"

def head(t, url, alterna_es, alterna_en):
    ld = {
        "@context": "https://schema.org", "@type": "LocalBusiness",
        "name": "Villanueva Nautical Services", "description": t["desc"], "url": url,
        "image": BASE + "img/compartir.jpg", "logo": BASE + "img/logo.png",
        "telephone": TEL, "email": EMAIL, "foundingDate": "2009",
        "address": {"@type": "PostalAddress", "addressLocality": "Valencia", "addressCountry": "ES"},
        "areaServed": [d for _, ds in DESTINOS["en"] for d in ds],
        "sameAs": [IG],
    }
    return f'''<!doctype html>
<html lang="{t["lang"]}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(t["title"])}</title>
<meta name="description" content="{e(t["desc"])}">
<meta name="theme-color" content="#12100c">
<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="es" href="{alterna_es}">
<link rel="alternate" hreflang="en" href="{alterna_en}">
<link rel="alternate" hreflang="x-default" href="{BASE}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Villanueva Nautical Services">
<meta property="og:title" content="{e(t["title"])}">
<meta property="og:description" content="{e(t["desc"])}">
<meta property="og:url" content="{url}">
<meta property="og:locale" content="{t["locale"]}">
<meta property="og:image" content="{BASE}img/compartir.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{e(t["ofi_alt"])}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="../assets/favicon.svg" type="image/svg+xml">
<link rel="preload" href="../assets/fonts/Cormorant.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="../assets/fonts.css?v={VERSION}">
<link rel="stylesheet" href="../assets/movimiento.css?v={VERSION}">
<link rel="stylesheet" href="../assets/site.css?v={VERSION}">
<script>document.documentElement.classList.add('js')</script>
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False, separators=(",", ":"))}</script>
</head>'''

def juntas_svg():
    # Lineas de calafateo en perspectiva, como las juntas de una cubierta vistas desde popa
    lineas = []
    for i in range(-7, 8):
        x0 = 300 + i * 95
        lineas.append(f'<path style="--k:{abs(i)}" d="M{x0} 820 C {300 + i*60} 520, {300 + i*22} 260, {300 + i*6} -40"/>')
    return f'<svg class="juntas" viewBox="0 0 600 800" preserveAspectRatio="xMidYMax slice" aria-hidden="true"><g>{"".join(lineas)}</g></svg>'

def antes_despues(t):
    """Una pareja por sufijo: antes.jpg/despues.jpg, antes-1/despues-1, antes-2/despues-2...
    Fotos de proceso opcionales: proceso.jpg, proceso-1.jpg... Solo sale si info.json dice "publicar": true."""
    import re
    trabajos = []
    for d in sorted(glob.glob(os.path.join(RAIZ, "src/antes-despues/*/"))):
        nombre = os.path.basename(d.rstrip("/"))
        info = {}
        if os.path.exists(os.path.join(d, "info.json")):
            info = json.load(open(os.path.join(d, "info.json")))
        if not info.get("publicar"):
            continue
        claves = [k[len(nombre) + 1:] for k in FOTOS if k.startswith(nombre + "-")]
        pares = sorted((m.group(1) or "") for k in claves for m in [re.fullmatch(r"antes(-\d+)?", k)] if m and ("despues" + (m.group(1) or "")) in claves)
        procesos = sorted(k for k in claves if re.fullmatch(r"proceso(-\d+)?", k))
        solo_antes = sorted(k for k in claves if re.fullmatch(r"antes(-\d+)?", k))
        if pares or solo_antes:
            trabajos.append((nombre, info, pares, procesos, [] if pares else solo_antes))
    if not trabajos:
        return ""
    l = t["lang"]
    bloques = []
    for nombre, info, pares, procesos, solo_antes in trabajos:
        tit = info.get(f"titulo_{l}", ""); txt = info.get(f"texto_{l}", "")
        comps = "".join(f'''
    <div class="comparar" style="--x:50%">
      {foto(f"{nombre}-antes{sx}", t["ad_antes"] + ": " + tit, "(min-width: 900px) 60vw, 100vw", cls="c-antes")}
      {foto(f"{nombre}-despues{sx}", t["ad_despues"] + ": " + tit, "(min-width: 900px) 60vw, 100vw", cls="c-despues")}
      <span class="c-et c-et-a">{t["ad_antes"]}</span><span class="c-et c-et-d">{t["ad_despues"]}</span>
      <span class="c-tirador" aria-hidden="true"></span>
      <input type="range" min="0" max="100" value="50" aria-label="{e(t["ad_rango"])}">
    </div>''' for sx in pares)
        # mientras no hay "despues": las fotos del antes solas, con su etiqueta
        comps += "".join(f'<figure class="ad-proceso" data-entra>{foto(f"{nombre}-{k}", t["ad_antes"] + ": " + tit, "(min-width: 900px) 45vw, 100vw")}<figcaption>{t["ad_antes"]}</figcaption></figure>'
                         for k in solo_antes)
        proc ="".join(f'<figure class="ad-proceso" data-entra>{foto(f"{nombre}-{k}", t["ad_proceso"] + ": " + tit, "(min-width: 900px) 30vw, 100vw")}<figcaption>{t["ad_proceso"]}</figcaption></figure>'
                       for k in procesos)
        bloques.append(f'''<div class="ad-trabajo">
  <div class="ad-texto">{f"<h3>{e(tit)}</h3>" if tit else ""}{f"<p>{e(txt)}</p>" if txt else ""}</div>
  <div class="ad-comparadores">{comps}
  </div>
  {f'<div class="ad-procesos">{proc}</div>' if proc else ""}
</div>''')
    return f'''
<section id="antes-despues" class="seccion">
  <div class="envoltura">
    <p class="kicker">{t["ad_kicker"]}</p>
    <h2>{t["ad_h2"]}</h2>
    {"".join(bloques)}
  </div>
</section>'''

def pagina(l):
    t = T[l]
    url = BASE + l + "/"
    otro = f"../{t['otro']}/"
    wa = wa_link(t)
    nav = "".join(f'<a href="#{a}">{n}</a>' for a, n in t["nav"])
    cinta_items = "".join(f'<span{" class=hueco" if i % 2 else ""}>{p}</span><i></i>' for i, p in enumerate(t["cinta"]))
    servicios = "".join(f'''
      <article class="card servicio" style="--k:{i}">
        {foto(b, t["alts"][b], "(min-width: 900px) 24vw, (min-width: 600px) 45vw, 100vw")}
        <div class="servicio-txt"><span class="num">0{i+1}</span><h3>{h}</h3><p>{p}</p></div>
      </article>''' for i, (b, h, p) in enumerate(t["servicios"]))
    pasos = "".join(f'<li class="step"><span class="paso-n">0{i+1}</span><div><h3>{h}</h3><p>{p}</p></div></li>'
                    for i, (h, p) in enumerate(t["pasos"]))
    cols = [["proa-teca", "tapa-cubierta"], ["cofre-interior", "cubierta-angulo"], ["cubierta-curva", "cunas-varada"]]
    galeria = "".join(
        f'<div class="col" style="--f:{f}">' + "".join(
            f'<button class="g-item" type="button" data-full="../img/{b}-{FOTOS[b][-1][0]}.jpg" data-alt="{e(t["alts"][b])}" aria-label="{e(t["ver_foto"])}: {e(t["alts"][b])}">'
            f'{foto(b, t["alts"][b], "(min-width: 900px) 30vw, 50vw")}</button>' for b in col) + '</div>'
        for col, f in zip(cols, ["-.06", ".05", "-.11"]))
    destinos = "".join(f'<div class="region"><h3>{r}</h3><ul>' + "".join(f'<li data-entra>{d}</li>' for d in ds) + '</ul></div>'
                       for r, ds in DESTINOS[l])
    resenas = "".join(
        f'<figure class="resena card"><blockquote lang="es"><p>{e(es).replace(chr(10), "<br>")}</p></blockquote>'
        + (f'<p class="trad"><span>{t["res_trad"]}</span> {e(en).replace(chr(10), " ")}</p>' if l == "en" else "")
        + f'<figcaption>{n} · Google</figcaption></figure>' for n, es, en in RESENAS)
    faq = "".join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in t["faq"])
    opts = lambda xs: "".join(f'<option>{x}</option>' for x in xs)
    msg_js = {k: t[k] for k in ("m_hola", "m_nombre", "m_barco", "m_trabajo", "m_donde", "m_detalles", "m_eslora")}

    return head(t, url, BASE + "es/", BASE + "en/") + f'''
<body>
<a class="saltar" href="#servicios">{t["nav"][0][1]}</a>
<header class="barra">
  <a href="#inicio" class="barra-marca" aria-label="Villanueva Nautical Services">{marca()}</a>
  <nav class="barra-nav" aria-label="Menu">{nav}</nav>
  <div class="barra-acc">
    <a class="idioma" href="{otro}" hreflang="{t["otro"]}" lang="{t["otro"]}" aria-label="{t["otro_nombre"]}">{t["otro_corto"]}</a>
    <a class="btn btn-principal btn-barra" href="{wa}" target="_blank" rel="noopener">{ICO["wa"]}<span>{t["wa_corto"]}</span></a>
  </div>
</header>

<main>
<section class="hero" id="inicio">
  <div class="hero-foto">{foto("proa-teca", t["alts"]["proa-teca"], "(min-width: 900px) 44vw, 100vw", prioritaria=True)}</div>
  {juntas_svg()}
  <div class="hero-txt">
    <p class="eyebrow">{t["eyebrow"]}</p>
    <h1 class="titulo-hero">{t["h1"]}</h1>
    <p class="hero-p">{t["hero_p"]}</p>
    <div class="botones">
      <a class="btn btn-principal" href="{wa}" target="_blank" rel="noopener">{ICO["wa"]}<span>{t["wa_largo"]}</span></a>
      <a class="btn btn-sec" href="tel:{TEL}">{ICO["tel"]}<span>{t["llamar"]} {TEL_VER}</span></a>
    </div>
  </div>
</section>

<div class="cinta" aria-hidden="true"><div class="pista">{cinta_items}{cinta_items}</div></div>

<section id="servicios" class="seccion">
  <div class="envoltura">
    <p class="kicker">{t["serv_kicker"]}</p>
    <h2>{t["serv_h2"]}</h2>
    <p class="intro">{t["serv_p"]}</p>
    <div class="servicios">{servicios}
    </div>
  </div>
</section>

<section id="oficio" class="seccion oscuro">
  <div class="envoltura oficio">
    <figure class="destapa" data-prog>{foto("cunas-varada", t["ofi_alt"], "(min-width: 900px) 55vw, 100vw")}</figure>
    <div class="oficio-txt">
      <p class="kicker">{t["ofi_kicker"]}</p>
      <h2>{t["ofi_h2"]}</h2>
      <p>{t["ofi_p"]}</p>
      <div class="stats">
        <div class="stat"><span class="n">{t["stat1_n"]}</span><span class="t">{t["stat1_t"]}</span></div>
        <div class="stat"><span class="n">{t["stat2_n"]}</span><span class="t">{t["stat2_t"]}</span></div>
      </div>
    </div>
  </div>
</section>

<section id="proceso" class="seccion">
  <div class="envoltura proceso">
    <div class="proceso-cab">
      <p class="kicker">{t["proc_kicker"]}</p>
      <h2>{t["proc_h2"]}</h2>
    </div>
    <ol class="pasos"><span class="linea" data-prog aria-hidden="true"></span>{pasos}</ol>
  </div>
</section>

<section id="trabajos" class="seccion">
  <div class="envoltura">
    <p class="kicker">{t["trab_kicker"]}</p>
    <h2>{t["trab_h2"]}</h2>
    <p class="intro">{t["trab_p"]}</p>
    <div class="galeria">{galeria}</div>
  </div>
</section>
{antes_despues(t)}
<section id="destinos" class="seccion oscuro">
  <div class="envoltura">
    <p class="kicker">{t["dest_kicker"]}</p>
    <h2><span class="shiny">{t["dest_h2"]}</span></h2>
    <p class="intro">{t["dest_p"]}</p>
    <div class="regiones">{destinos}</div>
    <p class="base">{timon("timon-peq")} Valencia</p>
  </div>
</section>

<section id="resenas" class="seccion">
  <div class="envoltura">
    <p class="kicker">{t["res_kicker"]}</p>
    <h2>{t["res_h2"]}</h2>
    <div class="resenas">{resenas}</div>
    <a class="enlace" href="{GOOGLE}" target="_blank" rel="noopener">{t["res_link"]} {ICO["flecha"]}</a>
  </div>
</section>

<section id="preguntas" class="seccion">
  <div class="envoltura estrecha">
    <p class="kicker">{t["faq_kicker"]}</p>
    <h2>{t["faq_h2"]}</h2>
    <div class="faq">{faq}</div>
  </div>
</section>

<section id="contacto" class="seccion oscuro">
  <div class="envoltura contacto">
    <div class="contacto-cab">
      <p class="kicker">{t["con_kicker"]}</p>
      <h2>{t["con_h2"]}</h2>
      <p>{t["con_p"]}</p>
      <p class="directo-t">{t["directo"]}</p>
      <ul class="directo">
        <li><a href="tel:{TEL}">{ICO["tel"]}<span>{TEL_VER}</span></a></li>
        <li><a href="mailto:{EMAIL}">{ICO["mail"]}<span>{EMAIL}</span></a></li>
        <li><a href="{IG}" target="_blank" rel="noopener">{ICO["ig"]}<span>@villanuevanauticalservices</span></a></li>
      </ul>
    </div>
    <form class="form-barco" action="https://wa.me/{WA}" method="get" target="_blank" data-msg='{e(json.dumps(msg_js, ensure_ascii=False))}' data-wa="{WA}">
      <div class="campo"><label for="f-nombre">{t["f_nombre"]}</label><input id="f-nombre" autocomplete="name"></div>
      <div class="fila">
        <div class="campo"><label for="f-barco">{t["f_barco"]}</label><select id="f-barco"><option value="">{t["elige"]}</option>{opts(t["f_barcos"])}</select></div>
        <div class="campo"><label for="f-eslora">{t["f_eslora"]}</label><input id="f-eslora" type="number" inputmode="decimal" min="3" max="120" step="0.1"></div>
      </div>
      <div class="campo"><label for="f-trabajo">{t["f_trabajo"]}</label><select id="f-trabajo"><option value="">{t["elige"]}</option>{opts(t["f_trabajos"])}</select></div>
      <div class="campo"><label for="f-donde">{t["f_donde"]}</label><input id="f-donde" placeholder="{t["f_donde_ph"]}"></div>
      <div class="campo"><label for="f-detalles">{t["f_detalles"]}</label><textarea id="f-detalles" name="text" rows="3"></textarea></div>
      <noscript><p class="nota">{t["f_noscript"]}</p></noscript>
      <button class="btn btn-principal btn-ancho" type="submit">{ICO["wa"]}<span>{t["f_enviar"]}</span></button>
      <p class="nota">{t["f_nota"]}</p>
    </form>
  </div>
</section>
</main>

<footer class="pie">
  <div class="envoltura pie-in">
    {marca()}
    <p>{t["pie"]}</p>
    <p class="pie-links"><a href="tel:{TEL}">{TEL_VER}</a><a href="mailto:{EMAIL}">{EMAIL}</a><a href="{otro}" lang="{t["otro"]}">{t["otro_nombre"]}</a></p>
    <p class="pie-c">© 2026 Villanueva Nautical Services</p>
  </div>
</footer>

<div class="barra-movil">
  <a class="btn btn-principal" href="{wa}" target="_blank" rel="noopener">{ICO["wa"]}<span>{t["wa_corto"]}</span></a>
  <a class="btn btn-sec" href="tel:{TEL}">{ICO["tel"]}<span>{t["llamar"]}</span></a>
</div>

<dialog class="visor" id="visor"><button type="button" class="visor-cerrar" aria-label="{t["cerrar"]}">×</button></dialog>

<script src="../assets/movimiento.js?v={VERSION}"></script>
<script src="../assets/site.js?v={VERSION}"></script>
</body>
</html>
'''

def raiz():
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Villanueva Nautical Services · Teak decks and marine carpentry</title>
<meta name="description" content="{e(T["en"]["desc"])}">
<link rel="canonical" href="{BASE}">
<link rel="alternate" hreflang="es" href="{BASE}es/">
<link rel="alternate" hreflang="en" href="{BASE}en/">
<link rel="alternate" hreflang="x-default" href="{BASE}">
<meta property="og:type" content="website">
<meta property="og:title" content="Villanueva Nautical Services">
<meta property="og:description" content="{e(T["en"]["desc"])}">
<meta property="og:url" content="{BASE}">
<meta property="og:image" content="{BASE}img/compartir.jpg">
<meta name="theme-color" content="#12100c">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
<script>
(function(){{var p=(navigator.languages&&navigator.languages[0])||navigator.language||'en';
location.replace(/^es\\b/i.test(p)?'es/':'en/');}})();
</script>
<style>
body{{margin:0;min-height:100vh;display:grid;place-items:center;background:#12100c;color:#efe6d8;font:16px/1.5 system-ui,sans-serif;text-align:center}}
a{{color:#d6a15e;display:inline-block;padding:12px 20px;margin:6px;border:1px solid #d6a15e;border-radius:999px;text-decoration:none}}
</style>
</head>
<body>
<main><p>Villanueva Nautical Services</p><p><a href="en/" hreflang="en">English</a><a href="es/" hreflang="es" lang="es">Español</a></p></main>
</body>
</html>
'''

if __name__ == "__main__":
    for l in ("es", "en"):
        os.makedirs(os.path.join(RAIZ, l), exist_ok=True)
        open(os.path.join(RAIZ, l, "index.html"), "w").write(pagina(l))
    open(os.path.join(RAIZ, "index.html"), "w").write(raiz())
    print("ok")
