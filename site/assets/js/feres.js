/* =========================================================================
   FERES — общий скрипт сайта.
   Ничего не ломает без JS: все эффекты — надстройка над рабочей вёрсткой.
   ========================================================================= */
(function () {
  'use strict';

  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  var heroVideo = document.querySelector('.hero__bg video');
  if (heroVideo) {
    heroVideo.muted = true;
    heroVideo.playsInline = true;
    heroVideo.autoplay = true;
    heroVideo.play().catch(function () {});
  }

  /* --- Шапка: состояние при скролле ------------------------------------ */
  var header = document.querySelector('.header');
  if (header) {
    var onScroll = function () {
      header.classList.toggle('is-stuck', window.scrollY > 12);
    };
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  /* --- Мобильное меню --------------------------------------------------- */
  var menu = document.querySelector('[data-menu]');
  var openMenu = function (open) {
    if (!menu) return;
    menu.classList.toggle('is-open', open);
    document.body.style.overflow = open ? 'hidden' : '';
    var btn = document.querySelector('[data-menu-open]');
    if (btn) btn.setAttribute('aria-expanded', open ? 'true' : 'false');
  };
  document.addEventListener('click', function (e) {
    if (e.target.closest('[data-menu-open]')) { openMenu(true); }
    if (e.target.closest('[data-menu-close]')) { openMenu(false); }
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') { openMenu(false); closeSuggest(); closeSearchModal(); }
  });

  /* --- Попап поиска в шапке ------------------------------------------- */
  var searchModal = document.querySelector('[data-search-modal]');
  var modalInput = searchModal ? searchModal.querySelector('input[type="search"]') : null;
  var modalForm = document.querySelector('[data-search-modal-form]');
  var modalResults = searchModal ? searchModal.querySelector('[data-search-modal-results]') : null;
  var modalProducts = [];

  function normalizeText(value) {
    return String(value || '').toLowerCase().replace(/[^a-zа-я0-9]/g, ' ')
      .replace(/\s+/g, ' ').trim();
  }

  function renderModalResults(query) {
    if (!modalResults) return;
    var q = normalizeText(query);
    if (!q) {
      modalResults.innerHTML = '<div class="search-modal__empty">Введите марку автомобиля, артикул или название товара.</div>';
      return;
    }

    var matches = modalProducts.filter(function (product) {
      var haystack = [
        product.name,
        product.sku,
        product.group,
        (product.applicability || []).join(' ')
      ].join(' ');
      return normalizeText(haystack).indexOf(q) !== -1;
    }).slice(0, 8);

    if (!matches.length) {
      modalResults.innerHTML = '<div class="search-modal__empty">Ничего не найдено. Попробуйте марку, OEM-номер или название детали.</div>';
      return;
    }

    modalResults.innerHTML = matches.map(function (product) {
      return '<a class="search-modal__item" href="product.html?sku=' + encodeURIComponent(product.sku) + '">' +
        '<img src="' + product.image + '" alt="" loading="lazy" width="48" height="48">' +
        '<span class="search-modal__meta"><strong>' + product.name + '</strong><span>' + product.sku + ' · ' + product.group + '</span></span>' +
        '</a>';
    }).join('');
  }

  function openSearchModal() {
    if (!searchModal || !modalInput) return;
    searchModal.classList.add('is-open');
    searchModal.setAttribute('aria-hidden', 'false');
    document.body.style.overflow = 'hidden';
    setTimeout(function () { modalInput.focus(); }, 30);
    if (!modalProducts.length) {
      fetch('data/products.json')
        .then(function (response) { return response.ok ? response.json() : { products: [] }; })
        .then(function (data) {
          modalProducts = data.products || [];
          renderModalResults(modalInput.value);
        })
        .catch(function () {
          modalProducts = [];
          renderModalResults(modalInput.value);
        });
    }
  }
  function closeSearchModal() {
    if (!searchModal) return;
    searchModal.classList.remove('is-open');
    searchModal.setAttribute('aria-hidden', 'true');
    document.body.style.overflow = '';
  }
  document.addEventListener('click', function (e) {
    if (e.target.closest('[data-search-open]')) { e.stopPropagation(); openSearchModal(); }
    if (e.target.closest('[data-search-close]')) { e.stopPropagation(); closeSearchModal(); }
  });
  if (searchModal) {
    searchModal.addEventListener('click', function (e) {
      if (e.target === searchModal || e.target.closest('[data-search-close]')) {
        closeSearchModal();
      }
    });
  }

  if (modalForm && modalInput) {
    modalInput.addEventListener('input', function () {
      renderModalResults(modalInput.value);
    });

    modalForm.addEventListener('submit', function (e) {
      e.preventDefault();
      renderModalResults(modalInput.value);
    });
  }

  /* --- «Лак»: блик следует за курсором --------------------------------- */
  if (!reduced && window.matchMedia('(hover: hover)').matches) {
    var pending = null;
    document.addEventListener('pointermove', function (e) {
      if (pending) return;
      pending = requestAnimationFrame(function () {
        pending = null;
        var el = e.target.closest ? e.target.closest('.lac') : null;
        if (!el) return;
        var r = el.getBoundingClientRect();
        el.style.setProperty('--mx', ((e.clientX - r.left) / r.width * 100).toFixed(1) + '%');
        el.style.setProperty('--my', ((e.clientY - r.top) / r.height * 100).toFixed(1) + '%');
      });
    }, { passive: true });
  }

  /* --- Появление секций при скролле ------------------------------------ */
  var revealables = document.querySelectorAll('.reveal');
  if (revealables.length) {
    if (reduced || !('IntersectionObserver' in window)) {
      revealables.forEach(function (el) { el.classList.add('is-in'); });
    } else {
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) return;
          entry.target.classList.add('is-in');
          io.unobserve(entry.target);
        });
      }, { rootMargin: '0px 0px -8% 0px', threshold: 0.06 });
      revealables.forEach(function (el, i) {
        var group = el.closest('[data-stagger]');
        if (group) {
          var idx = Array.prototype.indexOf.call(group.querySelectorAll('.reveal'), el);
          el.style.setProperty('--d', Math.min(idx, 6) * 0.07 + 's');
        }
        io.observe(el);
      });
    }
  }

  /* --- Счётчики цифр-фактов -------------------------------------------- */
  var counters = document.querySelectorAll('[data-count]');
  if (counters.length) {
    var run = function (el) {
      var target = parseFloat(el.dataset.count);
      var suffix = el.dataset.suffix || '';
      if (!isFinite(target)) return;          /* не число — не наш элемент, не трогаем */
      var dur = 1100;
      if (reduced) { el.textContent = format(target) + suffix; return; }
      var t0 = performance.now();
      var step = function (now) {
        var p = Math.min(1, (now - t0) / dur);
        var eased = 1 - Math.pow(1 - p, 3);
        el.textContent = format(Math.round(target * eased)) + suffix;
        if (p < 1) requestAnimationFrame(step);
      };
      requestAnimationFrame(step);
    };
    var format = function (n) { return String(n).replace(/\B(?=(\d{3})+(?!\d))/g, ' '); };
    if ('IntersectionObserver' in window) {
      var cio = new IntersectionObserver(function (entries) {
        entries.forEach(function (en) {
          if (!en.isIntersecting) return;
          run(en.target); cio.unobserve(en.target);
        });
      }, { threshold: 0.5 });
      counters.forEach(function (el) { cio.observe(el); });
    } else {
      counters.forEach(run);
    }
  }

  /* --- Умный поиск: определение типа запроса + подсказки ---------------- */
  /* Типы: артикул FERES / OEM-номер / название. На проде подсказки отдаёт
     сервер (Битрикс), здесь — демонстрация на данных data/products.json.  */
  var products = [];
  var searchRoots = document.querySelectorAll('[data-search]');

  function detectType(q) {
    var s = q.trim();
    if (s.length < 2) return null;
    if (/^[A-Za-zА-Яа-я\s\-]+$/.test(s) && /[А-Яа-я]{3}/.test(s)) return 'Название';
    if (/^FR[\dA-Za-z\-]+$/i.test(s)) return 'Артикул FERES';
    if (/^\d{4,}[\.\-]?[\d\-\.]*$/.test(s)) return 'OEM / артикул';
    if (/[\d]/.test(s) && /[A-Za-z]/.test(s)) return 'OEM / кросс';
    return 'Название';
  }

  function normalize(s) { return String(s).toLowerCase().replace(/[\s\-\.]/g, ''); }

  function closeSuggest() {
    document.querySelectorAll('.suggest').forEach(function (s) { s.classList.remove('is-open'); });
  }
  document.addEventListener('click', function (e) {
    if (!e.target.closest('[data-search]')) closeSuggest();
  });

  function renderSuggest(box, q) {
    var nq = normalize(q);
    var hits = products.filter(function (p) {
      return normalize(p.sku).indexOf(nq) > -1 ||
             normalize(p.name).indexOf(nq) > -1 ||
             normalize(p.group).indexOf(nq) > -1 ||
             (p.applicability || []).some(function (a) { return normalize(a).indexOf(nq) > -1; });
    }).slice(0, 5);

    if (!hits.length) {
      box.innerHTML = '<p class="suggest__empty">Ничего не найдено. Проверьте номер или напишите нам — подберём деталь: ' +
        '<a class="txt-sand" href="contacts.html">sales@feres.ru</a></p>';
    } else {
      box.innerHTML = hits.map(function (p) {
        return '<a class="suggest__item" href="product.html?sku=' + encodeURIComponent(p.sku) + '">' +
          '<img src="' + p.image + '" alt="" loading="lazy" width="46" height="46">' +
          '<span class="stack"><span class="small">' + p.name + '</span>' +
          '<span class="art">' + p.sku + ' · ' + p.group + '</span></span></a>';
      }).join('');
    }
    box.classList.add('is-open');
  }

  if (searchRoots.length) {
    fetch('data/products.json')
      .then(function (r) { return r.ok ? r.json() : { products: [] }; })
      .then(function (d) { products = d.products || []; })
      .catch(function () { products = []; });

    searchRoots.forEach(function (root) {
      var input = root.querySelector('.search__input');
      var type = root.querySelector('.search__type');
      var box = root.querySelector('.suggest');
      if (!input) return;

      input.addEventListener('input', function () {
        var q = input.value;
        var t = detectType(q);
        if (type) {
          type.textContent = t || '';
          type.classList.toggle('is-on', !!t);
        }
        if (box) {
          if (q.trim().length >= 2 && products.length) renderSuggest(box, q);
          else box.classList.remove('is-open');
        }
      });
      input.addEventListener('focus', function () {
        if (box && input.value.trim().length >= 2) renderSuggest(box, input.value);
      });
      root.addEventListener('submit', function (e) {
        e.preventDefault();
        var q = input.value.trim();
        if (q) window.location.href = 'catalog.html?q=' + encodeURIComponent(q);
      });
    });

    document.querySelectorAll('[data-chip]').forEach(function (chip) {
      chip.addEventListener('click', function () {
        var root = document.querySelector('[data-search]');
        var input = root && root.querySelector('.search__input');
        if (!input) return;
        input.value = chip.dataset.chip;
        input.focus();
        input.dispatchEvent(new Event('input'));
      });
    });
  }

  /* --- Cookie-баннер (152-ФЗ: до согласия необязательные счётчики не включаем) */
  var cookie = document.querySelector('[data-cookie]');
  if (cookie) {
    var KEY = 'feres_cookie_consent';
    var saved = null;
    try { saved = localStorage.getItem(KEY); } catch (e) { saved = null; }
    if (!saved) {
      setTimeout(function () { cookie.classList.add('is-open'); }, 900);
    }
    cookie.addEventListener('click', function (e) {
      if (!e.target.closest('[data-cookie-accept]')) return;
      try { localStorage.setItem(KEY, JSON.stringify({ accepted: true, at: new Date().toISOString() })); } catch (err) {}
      cookie.classList.remove('is-open');
      document.dispatchEvent(new CustomEvent('feres:analytics-allowed'));
    });
  }

  /* --- Магнитные кнопки: элемент тянется к курсору ---------------------- */
  /* Сдвиг пишем в CSS-переменные — анимацией занимается сам браузер.       */
  if (!reduced && window.matchMedia('(hover: hover)').matches) {
    document.querySelectorAll('.magnet').forEach(function (el) {
      var frame = null;
      el.addEventListener('pointermove', function (e) {
        if (frame) return;
        frame = requestAnimationFrame(function () {
          frame = null;
          var r = el.getBoundingClientRect();
          var dx = e.clientX - r.left - r.width / 2;
          var dy = e.clientY - r.top - r.height / 2;
          el.classList.add('is-pulling');
          el.style.setProperty('--mgx', (dx * 0.26).toFixed(1) + 'px');
          el.style.setProperty('--mgy', (dy * 0.32).toFixed(1) + 'px');
          el.style.setProperty('--mgs', '1.04');
        });
      });
      el.addEventListener('pointerleave', function () {
        el.classList.remove('is-pulling');
        el.style.setProperty('--mgx', '0px');
        el.style.setProperty('--mgy', '0px');
        el.style.setProperty('--mgs', '1');
      });
    });
  }

  /* --- «Занавес»: подвал закреплён под страницей ------------------------ */
  /* Без JS, на узких экранах и при prefers-reduced-motion — обычный подвал. */
  var finale = document.querySelector('[data-finale]');
  if (finale) {
    var inner = finale.querySelector('.finale__inner');
    var supported = window.CSS && CSS.supports && CSS.supports('clip-path', 'inset(0)');
    var lastHeight = -1;

    var syncCurtain = function () {
      var roomy = window.innerWidth >= 1040 && window.innerHeight >= 620;
      var on = !!(roomy && supported && !reduced);
      document.documentElement.classList.toggle('has-curtain', on);
      var h = on ? inner.offsetHeight : 0;
      if (h !== lastHeight) {
        lastHeight = h;
        finale.style.height = on ? h + 'px' : '';
      }
    };

    syncCurtain();
    window.addEventListener('resize', syncCurtain, { passive: true });
    if ('ResizeObserver' in window) new ResizeObserver(syncCurtain).observe(inner);
    window.addEventListener('load', syncCurtain);
  }

  document.addEventListener('click', function (e) {
    if (!e.target.closest('[data-to-top]')) return;
    window.scrollTo({ top: 0, behavior: reduced ? 'auto' : 'smooth' });
  });

  /* --- Формы: согласие на обработку ПДн обязательно --------------------- */
  document.querySelectorAll('form[data-consent-form]').forEach(function (form) {
    var submit = form.querySelector('[type="submit"]');
    var required = form.querySelector('[data-consent]');
    if (!submit || !required) return;
    var sync = function () { submit.disabled = !required.checked; };
    sync();
    required.addEventListener('change', sync);
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!required.checked) return;
      /* На проде: POST на сервер + запись факта согласия (дата, IP, форма, версия документа) */
      form.querySelector('[data-form-ok]')?.removeAttribute('hidden');
      form.reset();
      sync();
    });
  });
})();
