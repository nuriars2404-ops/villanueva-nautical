/* Capa de movimiento ligada al scroll. Se enchufa a cualquier web estatica sin build.
   Todo ligado al scroll: avanza y retrocede. Sin JS la pagina es la de siempre.
   - section h2 sin spans: titulo palabra a palabra (--tp, --i, --n)
   - .card, .step, .panel, .stat, .lvl, .price-box, [data-entra]: entran girando (--sp)
   - .stat .n con numero: cuenta desde 0 (formato es-ES con puntos)
   - .cinta .pista: banda de palabras con la velocidad del scroll
   - [data-prog]: recibe --p (0..1) segun su recorrido en pantalla (para barras y progresos)
   - red de seguridad: lo que ya se paso de largo queda en estado final */
(function () {
  'use strict';
  if (matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  var root = document.documentElement;
  root.classList.add('mov');
  var vh = innerHeight;

  function trocea(el) {
    var t = el.textContent.trim(), pal = t.split(/\s+/);
    el.setAttribute('aria-label', t);
    el.innerHTML = pal.map(function (p, i) { return '<span class="pal" aria-hidden="true" style="--i:' + i + '">' + p + '</span>'; }).join(' ');
    el.style.setProperty('--n', pal.length);
  }
  var items = [];
  function reg(el, tipo, x) { items.push({ el: el, tipo: tipo, x: x || {} }); }

  Array.prototype.forEach.call(document.querySelectorAll('section h2, .cap h2'), function (el) {
    if (el.querySelector('span') || el.closest('.hero')) return;
    trocea(el); reg(el, 'tit');
  });
  Array.prototype.forEach.call(document.querySelectorAll('.card,.step,.panel,.stat,.lvl,.price-box,[data-entra]'), function (el) { reg(el, 'card'); });
  Array.prototype.forEach.call(document.querySelectorAll('.card'), function (el) {
    var s = document.createElement('span'); s.className = 'brillo'; s.setAttribute('aria-hidden', 'true'); el.appendChild(s);
  });
  Array.prototype.forEach.call(document.querySelectorAll('.stat .n, [data-cuenta]'), function (el) {
    var m = el.textContent.match(/(\D*?)([\d.]+)(.*)$/);
    if (!m) return;
    var n = parseInt(m[2].replace(/\./g, ''), 10);
    if (!n) return;
    reg(el, 'num', { pre: m[1], post: m[3], n: n, fin: el.textContent });
  });
  Array.prototype.forEach.call(document.querySelectorAll('.cinta .pista'), function (el, i) { reg(el, 'cinta', { dir: i % 2 ? 1 : -1 }); });
  Array.prototype.forEach.call(document.querySelectorAll('[data-prog]'), function (el) { reg(el, 'prog'); });

  function lim(v) { return v < 0 ? 0 : v > 1 ? 1 : v; }
  function fmt(n) { return String(n).replace(/\B(?=(\d{3})+(?!\d))/g, '.'); }
  var ultimoY = scrollY, vel = 0, corriendo = false;

  function cuadro() {
    var y = scrollY;
    vel += ((y - ultimoY) - vel) * .18; ultimoY = y;
    for (var k = 0; k < items.length; k++) {
      var it = items[k], el = it.el, r = el.getBoundingClientRect();
      if (r.top > vh + 300) continue;
      if (r.bottom < -300) {
        if (!it.fin) {
          it.fin = true;
          if (it.tipo === 'tit') el.style.setProperty('--tp', '1');
          else if (it.tipo === 'card') el.style.setProperty('--sp', '1');
          else if (it.tipo === 'num') el.textContent = it.x.fin;
          else if (it.tipo === 'prog') el.style.setProperty('--p', '1');
        }
        continue;
      }
      it.fin = false;
      if (it.tipo === 'card') el.style.setProperty('--sp', lim((vh - r.top) / (vh * .42)).toFixed(3));
      else if (it.tipo === 'tit') el.style.setProperty('--tp', lim((vh - r.top) / (vh * .3)).toFixed(3));
      else if (it.tipo === 'num') {
        var p = lim((vh - r.top) / (vh * .45));
        p = 1 - Math.pow(1 - p, 3);
        el.textContent = p >= 1 ? it.x.fin : it.x.pre + fmt(Math.round(it.x.n * p)) + it.x.post;
      } else if (it.tipo === 'prog') {
        // 0 cuando el elemento entra por abajo, 1 cuando su parte baja llega al 35% de la pantalla
        var pp = lim((vh - r.top) / (r.height + vh * .65));
        el.style.setProperty('--p', pp.toFixed(3));
      } else if (it.tipo === 'cinta') {
        var mitad = el.scrollWidth / 2, off = (y * .45) % mitad;
        var sk = Math.max(-9, Math.min(9, vel * -.35));
        el.style.transform = 'translate3d(' + (it.x.dir < 0 ? -off : off - mitad).toFixed(1) + 'px,0,0) skewX(' + sk.toFixed(2) + 'deg)';
      }
    }
    if (Math.abs(vel) > .05) requestAnimationFrame(cuadro); else corriendo = false;
  }
  function pide() { if (!corriendo) { corriendo = true; requestAnimationFrame(cuadro); } }
  addEventListener('scroll', pide, { passive: true });
  addEventListener('resize', function () { vh = innerHeight; pide(); });
  corriendo = true; requestAnimationFrame(cuadro);

  if (matchMedia('(pointer: fine)').matches) {
    Array.prototype.forEach.call(document.querySelectorAll('.card'), function (el) {
      el.addEventListener('pointermove', function (e) {
        var r = el.getBoundingClientRect(), fx = (e.clientX - r.left) / r.width, fy = (e.clientY - r.top) / r.height;
        el.style.setProperty('--ty', ((fx - .5) * 8).toFixed(2) + 'deg');
        el.style.setProperty('--tx', ((.5 - fy) * 8).toFixed(2) + 'deg');
        el.style.setProperty('--gx', (fx * 100).toFixed(1) + '%'); el.style.setProperty('--gy', (fy * 100).toFixed(1) + '%');
      });
      el.addEventListener('pointerleave', function () { el.style.setProperty('--tx', '0deg'); el.style.setProperty('--ty', '0deg'); });
    });
  }
})();
