/* =========================================================================
   FERES — фильтр статей базы знаний по рубрике.
   ========================================================================= */
(function () {
  'use strict';
  var grid = document.querySelector('[data-kb-grid]');
  if (!grid) return;
  var chips = document.querySelectorAll('[data-kb-filter]');
  var items = grid.querySelectorAll('[data-kb-item]');

  chips.forEach(function (chip) {
    chip.addEventListener('click', function () {
      var rubric = chip.dataset.kbFilter;
      items.forEach(function (el) {
        el.style.display = (rubric === 'all' || el.dataset.kbRubric === rubric) ? '' : 'none';
      });
      chips.forEach(function (c) { c.setAttribute('aria-pressed', c === chip ? 'true' : 'false'); });
    });
  });
})();
