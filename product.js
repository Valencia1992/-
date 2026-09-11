/* =========================================================================
   FERES — переключение фото в галерее карточки товара.
   ========================================================================= */
(function () {
  'use strict';
  var main = document.querySelector('[data-gallery] img');
  var thumbs = document.querySelectorAll('[data-thumb]');
  if (!main || !thumbs.length) return;
  thumbs.forEach(function (btn) {
    btn.addEventListener('click', function () {
      main.src = btn.dataset.thumb;
      thumbs.forEach(function (b) { b.classList.remove('is-active'); });
      btn.classList.add('is-active');
    });
  });
})();
