/* =========================================================================
   FERES — раздел «Где купить»: фильтры, карта и связь карточек с маркерами.
   Данные уже в разметке: скрипт только фильтрует и подсвечивает.
   ========================================================================= */
(function () {
  'use strict';

  var finder = document.querySelector('[data-finder]');
  if (!finder) return;

  var pins = Array.prototype.slice.call(finder.querySelectorAll('[data-pin]'));
  var cards = Array.prototype.slice.call(finder.querySelectorAll('[data-point]'));
  var typeButtons = Array.prototype.slice.call(finder.querySelectorAll('[data-filter-type]'));
  var citySelect = finder.querySelector('[data-filter-city]');
  var countLabel = finder.querySelector('[data-count-label]');
  var empty = finder.querySelector('[data-empty]');
  var label = finder.querySelector('[data-map-label]');

  var state = { type: 'all', city: '' };

  function plural(n) {
    var d10 = n % 10, d100 = n % 100;
    if (d10 === 1 && d100 !== 11) return n + ' точка';
    if (d10 >= 2 && d10 <= 4 && (d100 < 10 || d100 >= 20)) return n + ' точки';
    return n + ' точек';
  }

  function apply() {
    var visible = 0;
    cards.forEach(function (card) {
      var okType = state.type === 'all' || card.dataset.type === state.type;
      var okCity = !state.city || card.dataset.city === state.city;
      var show = okType && okCity;
      card.classList.toggle('is-hidden', !show);
      card.classList.toggle('is-active', !!state.city && show);
      if (show) visible++;
    });

    pins.forEach(function (pin) {
      var types = pin.dataset.types.split(' ');
      var okType = state.type === 'all' || types.indexOf(state.type) > -1;
      pin.classList.toggle('is-dim', !okType);
      pin.classList.toggle('is-active', !!state.city && pin.dataset.pin === state.city);
    });

    if (countLabel) countLabel.textContent = plural(visible);
    if (empty) empty.hidden = visible !== 0;

    typeButtons.forEach(function (b) {
      b.setAttribute('aria-pressed', b.dataset.filterType === state.type ? 'true' : 'false');
    });
    if (citySelect && citySelect.value !== state.city) citySelect.value = state.city;
  }

  typeButtons.forEach(function (btn) {
    btn.addEventListener('click', function () {
      state.type = btn.dataset.filterType;
      apply();
    });
  });

  if (citySelect) {
    citySelect.addEventListener('change', function () {
      state.city = citySelect.value;
      apply();
      scrollToFirstVisible();
    });
  }

  function scrollToFirstVisible() {
    var first = cards.filter(function (c) { return !c.classList.contains('is-hidden'); })[0];
    var list = finder.querySelector('[data-points]');
    if (first && list) list.scrollTop = Math.max(0, first.offsetTop - list.offsetTop - 6);
  }

  /* Маркеры на карте */
  pins.forEach(function (pin) {
    var city = pin.dataset.pin;
    pin.addEventListener('click', function () {
      state.city = (state.city === city) ? '' : city;
      apply();
      scrollToFirstVisible();
    });
    ['mouseenter', 'focus'].forEach(function (ev) {
      pin.addEventListener(ev, function () {
        if (!label) return;
        var n = cards.filter(function (c) { return c.dataset.city === city; }).length;
        label.textContent = city + ' · ' + plural(n);
        label.style.left = pin.style.left;
        label.style.top = pin.style.top;
        label.classList.add('is-on');
      });
    });
    ['mouseleave', 'blur'].forEach(function (ev) {
      pin.addEventListener(ev, function () { if (label) label.classList.remove('is-on'); });
    });
  });

  /* «Показать на карте» в карточке и кнопки каналов в блоке ниже */
  document.addEventListener('click', function (e) {
    var byCity = e.target.closest('[data-show-city]');
    if (byCity) {
      state.city = byCity.dataset.showCity;
      apply();
      document.getElementById('map').scrollIntoView({ behavior: 'smooth', block: 'start' });
      return;
    }
    var byType = e.target.closest('[data-show-type]');
    if (byType) {
      state.type = byType.dataset.showType;
      state.city = '';
      apply();
      document.getElementById('map').scrollIntoView({ behavior: 'smooth', block: 'start' });
      scrollToFirstVisible();
    }
  });

  /* Тип обращения в форме можно задать ссылкой: #add?kind=sto */
  var kind = document.querySelector('[data-form-kind]');
  if (kind && location.hash.indexOf('kind=') > -1) {
    kind.value = location.hash.split('kind=')[1];
  }

  apply();
})();
