/* Villanueva Nautical Services · interacciones propias.
   Lo de movimiento va detras de "reducir movimiento"; formulario, visor y comparador funcionan siempre. */
(function () {
  'use strict';
  var quieto = matchMedia('(prefers-reduced-motion: reduce)').matches;
  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };
  var vh = innerHeight;

  /* 1 · Titulo del hero palabra a palabra al cargar */
  var h1 = $('.titulo-hero');
  if (h1 && !quieto) {
    var txt = h1.textContent.trim();
    h1.setAttribute('aria-label', txt);
    h1.innerHTML = txt.split(/\s+/).map(function (p, i) {
      return '<span class="w" aria-hidden="true" style="--i:' + i + '">' + p + '</span>';
    }).join(' ');
  }

  /* 2 · Barra superior solida al bajar */
  var barra = $('.barra');
  function barraEstado() { barra.classList.toggle('solida', scrollY > 40); }

  /* 3 · Bucle ligado al scroll: parallax del hero, columnas de la galeria, tarjetas que se apilan, pasos */
  var hero = $('.hero'), heroFoto = $('.hero-foto'), juntas = $('.juntas');
  var cols = $$('.galeria .col'), galeria = $('.galeria');
  var cards = $$('.servicios .card');
  var pasos = $$('.pasos .step');
  var movil = matchMedia('(max-width: 599px)');
  var escritorio = matchMedia('(min-width: 900px)');
  var pedido = false;

  function cuadro() {
    pedido = false;
    barraEstado();
    if (quieto) return;
    var y = scrollY;
    if (y < vh * 1.2) {
      if (escritorio.matches) heroFoto.style.setProperty('--hy', (y * .18).toFixed(1) + 'px');
      juntas.style.transform = 'translate3d(0,' + (y * -.12).toFixed(1) + 'px,0)';
    }
    if (galeria) {
      var g = galeria.getBoundingClientRect();
      if (g.bottom > -200 && g.top < vh + 200) {
        var d = (g.top + g.height / 2) - vh / 2;
        cols.forEach(function (c) {
          var f = escritorio.matches ? parseFloat(c.style.getPropertyValue('--f')) : parseFloat(c.style.getPropertyValue('--f')) * .5;
          c.style.setProperty('--gy', (d * f).toFixed(1) + 'px');
        });
      }
    }
    if (movil.matches) {
      for (var i = 0; i < cards.length - 1; i++) {
        var a = cards[i].getBoundingClientRect(), b = cards[i + 1].getBoundingClientRect();
        var p = Math.max(0, Math.min(1, (a.bottom - b.top) / a.height));
        cards[i].style.setProperty('--apila', (1 - p * .07).toFixed(3));
      }
    } else if (cards.length && cards[0].style.getPropertyValue('--apila')) {
      cards.forEach(function (c) { c.style.removeProperty('--apila'); });
    }
    pasos.forEach(function (s) {
      s.classList.toggle('activo', s.getBoundingClientRect().top < vh * .62);
    });
  }
  function pide() { if (!pedido) { pedido = true; requestAnimationFrame(cuadro); } }
  addEventListener('scroll', pide, { passive: true });
  addEventListener('resize', function () { vh = innerHeight; pide(); });
  cuadro();
  if (quieto) pasos.forEach(function (s) { s.classList.add('activo'); });

  /* 4 · Un solo boton destacado: el de la barra pasa a secundario si hay otro principal a la vista.
        La barra fija del movil se esconde cuando ya hay botones de contacto en pantalla */
  var btnBarra = $('.btn-barra'), barraMovil = $('.barra-movil');
  var otros = $$('.btn-principal').filter(function (b) { return b !== btnBarra && !b.closest('.barra-movil'); });
  var tapan = [$('.hero .botones'), $('#contacto')].filter(Boolean);
  if ('IntersectionObserver' in window) {
    var visibles = new Set(), tapando = new Set();
    var io = new IntersectionObserver(function (ents) {
      ents.forEach(function (en) { en.isIntersecting ? visibles.add(en.target) : visibles.delete(en.target); });
      if (btnBarra) btnBarra.classList.toggle('sec', visibles.size > 0);
    });
    otros.forEach(function (b) { io.observe(b); });
    var io2 = new IntersectionObserver(function (ents) {
      ents.forEach(function (en) { en.isIntersecting ? tapando.add(en.target) : tapando.delete(en.target); });
      barraMovil.classList.toggle('fuera', tapando.size > 0);
    });
    tapan.forEach(function (el) { io2.observe(el); });
  }

  /* 5 · Visor de fotos con <dialog> nativo */
  var visor = $('#visor');
  if (visor && visor.showModal) {
    var vimg = null;
    $$('.g-item').forEach(function (b) {
      b.addEventListener('click', function () {
        if (!vimg) { vimg = document.createElement('img'); visor.insertBefore(vimg, visor.firstChild); }
        vimg.alt = b.dataset.alt; vimg.src = b.dataset.full;
        visor.showModal();
      });
    });
    $('.visor-cerrar', visor).addEventListener('click', function () { visor.close(); });
    visor.addEventListener('click', function (e) { if (e.target === visor) visor.close(); });
  }

  /* 6 · "Cuentanos tu barco": compone el mensaje y abre WhatsApp */
  var form = $('.form-barco');
  if (form) {
    var M = JSON.parse(form.dataset.msg);
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var v = function (id) { return ($('#' + id).value || '').trim(); };
      var lineas = [M.m_hola, ''];
      if (v('f-nombre')) lineas.push(M.m_nombre + ': ' + v('f-nombre'));
      var barco = [v('f-barco'), v('f-eslora') ? (document.documentElement.lang === 'es' ? v('f-eslora').replace('.', ',') : v('f-eslora')) + ' ' + M.m_eslora : ''].filter(Boolean).join(', ');
      if (barco) lineas.push(M.m_barco + ': ' + barco);
      if (v('f-trabajo')) lineas.push(M.m_trabajo + ': ' + v('f-trabajo'));
      if (v('f-donde')) lineas.push(M.m_donde + ': ' + v('f-donde'));
      if (v('f-detalles')) lineas.push(M.m_detalles + ': ' + v('f-detalles'));
      var url = 'https://wa.me/' + form.dataset.wa + '?text=' + encodeURIComponent(lineas.join('\n'));
      form.dataset.ultimo = url;
      window.open(url, '_blank', 'noopener');
    });
  }

  /* 7 · Comparador antes / despues */
  $$('.comparar').forEach(function (c) {
    var r = $('input', c);
    var pon = function () { c.style.setProperty('--x', r.value + '%'); };
    r.addEventListener('input', pon); pon();
  });

  /* 8 · Chispas al pulsar los botones principales (tambien con el dedo) */
  if (!quieto) {
    var cv = null, ctx = null, chispas = [], corre = false;
    function lienzo() {
      if (cv) return;
      cv = document.createElement('canvas'); cv.className = 'chispas'; cv.setAttribute('aria-hidden', 'true');
      document.body.appendChild(cv); ctx = cv.getContext('2d');
      tam(); addEventListener('resize', tam);
    }
    function tam() { var d = Math.min(devicePixelRatio || 1, 2); cv.width = innerWidth * d; cv.height = innerHeight * d; ctx.setTransform(d, 0, 0, d, 0, 0); }
    function pinta(t) {
      ctx.clearRect(0, 0, innerWidth, innerHeight);
      chispas = chispas.filter(function (s) {
        var k = (t - s.t0) / 420; if (k >= 1) return false;
        var e = 1 - Math.pow(1 - k, 3), dist = e * 26, len = 10 * (1 - e);
        ctx.strokeStyle = 'rgba(232,187,127,' + (1 - k) + ')'; ctx.lineWidth = 2; ctx.beginPath();
        ctx.moveTo(s.x + Math.cos(s.a) * (dist + 6), s.y + Math.sin(s.a) * (dist + 6));
        ctx.lineTo(s.x + Math.cos(s.a) * (dist + 6 + len), s.y + Math.sin(s.a) * (dist + 6 + len));
        ctx.stroke(); return true;
      });
      if (chispas.length) requestAnimationFrame(pinta); else corre = false;
    }
    document.addEventListener('pointerdown', function (e) {
      if (!e.target.closest('.btn-principal')) return;
      lienzo();
      var t0 = performance.now();
      for (var i = 0; i < 8; i++) chispas.push({ x: e.clientX, y: e.clientY, a: i * Math.PI / 4, t0: t0 });
      if (!corre) { corre = true; requestAnimationFrame(pinta); }
    });
  }
})();
