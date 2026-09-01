/* =========================================================================
   FERES — фильтр каталога по группе товаров (демо-листинг на products.json).
   ========================================================================= */
(function () {
  'use strict';
  var grid = document.querySelector('[data-cat-grid]');
  if (!grid) return;
  var chips = document.querySelectorAll('[data-cat-filter]');
  var items = grid.querySelectorAll('[data-cat-item]');

  function apply(group) {
    items.forEach(function (el) {
      el.style.display = (group === 'all' || el.dataset.group === group) ? '' : 'none';
    });
    chips.forEach(function (c) {
      c.setAttribute('aria-pressed', c.dataset.catFilter === group ? 'true' : 'false');
    });
  }

  chips.forEach(function (chip) {
    chip.addEventListener('click', function () { apply(chip.dataset.catFilter); });
  });

  var params = new URLSearchParams(location.search);
  var g = params.get('group');
  if (g && document.querySelector('[data-cat-filter="' + g + '"]')) {
    apply(g);
    setTimeout(function () {
      grid.scrollIntoView({ behavior: 'auto', block: 'start' });
    }, 0);
  }
})();
