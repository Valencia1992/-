# -*- coding: utf-8 -*-
import sys, os, re
sys.path.insert(0, os.path.dirname(__file__))
from common import *

header, footer = load_shell()
header = header.replace('<a href="catalog.html">Каталог</a>', '<a href="catalog.html" aria-current="page">Каталог</a>', 1)
data = products()
groups = data["meta"]["groups"]
items = data["products"]

crumbs_html = crumbs(("Каталог", None))

head = page_head_block(
    "Каталог", "Каталог продукции",
    "833 позиции в шести группах товаров. Четыре способа найти деталь: по группе, по автомобилю, по артикулу FERES и по OEM-номеру или кроссу. Данные и фото — из 1С, обновляются автоматически.",
    crumbs_html,
    anchors=[("ways", "Способы поиска"), ("groups", "Группы товаров"), ("by-car", "Подбор по авто"),
             ("listing", "Каталог")])

WAYS = [
    (ICON["grid"], "По группам товаров", "Полный перечень категорий: от двигателя и ЦПГ до фильтров. Внутри группы — фильтры по применяемости и подгруппе.", "#groups"),
    (ICON["car"], "Подбор по авто", "Марка → модель → поколение → модификация — и сайт покажет все подходящие товары.", "#by-car"),
    (ICON["hash"], "По артикулу FERES", "Знаете номер детали — вводите прямо в строку поиска, подсказки появятся по мере набора.", "#quick-article"),
    (ICON["swap"], "По OEM или кроссу", "Оригинальный номер или артикул конкурента — так чаще всего ищут на СТО.", "#quick-oem"),
]
ways_html = "\n      ".join(
    """<a class="card lac way sheen reveal" href="%s">
        <span class="way__icon">%s</span>
        <h3 class="h4">%s</h3>
        <p class="small">%s</p>
        <span class="way__foot"><span class="link-arrow">Открыть %s</span></span>
      </a>""" % (href, icon, title, desc, ICON["arrow"]) for icon, title, desc, href in WAYS)

ways_section = """<section class="section section--tight" id="ways">
  <div class="wrap">
    %s
    <div class="grid cols-4" data-stagger>
      %s
    </div>
  </div>
</section>""" % (sec_head("01 · Способы поиска", "С чего начать"), ways_html)

group_cards = "\n      ".join(
    """<a class="card lac cat reveal" href="catalog.html?group=%s">
        <img class="cat__img" src="%s" alt="" loading="lazy" width="1000" height="600">
        <h3 class="cat__name">%s</h3>
        <p class="cat__count">%s</p>
      </a>""" % (g["slug"], g["image"], g["name"], g["desc"]) for g in groups)

groups_section = """<section class="section section--ink1 section--line" id="groups">
  <div class="wrap">
    %s
    <div class="grid cols-3" data-stagger>
      %s
    </div>
  </div>
</section>""" % (sec_head("02 · Группы товаров", "Шесть групп продукции",
                            "Полное дерево подгрупп повторяет структуру каталога 1С и приходит вместе с обменом."), group_cards)

marks = ["LADA Granta", "LADA Vesta", "LADA Priora", "LADA Kalina", "LADA XRAY", "ВАЗ 2110–2112", "ВАЗ 2108–2115", "Chevrolet Niva"]
mark_options = "".join('<option>%s</option>' % m for m in marks)

by_car_section = """<section class="section" id="by-car">
  <div class="wrap">
    %s
    <div class="card lac form-card">
      <form class="cascade" onsubmit="return false" aria-label="Подбор по автомобилю">
        <div><label class="label" for="mk">Марка</label>
          <select class="field" id="mk"><option value="">Выберите марку</option>%s</select></div>
        <div><label class="label" for="md">Модель</label>
          <select class="field" id="md" disabled><option value="">Сначала марку</option></select></div>
        <div><label class="label" for="gen">Поколение</label>
          <select class="field" id="gen" disabled><option value="">Сначала модель</option></select></div>
        <div><label class="label" for="mod">Модификация</label>
          <select class="field" id="mod" disabled><option value="">Необязательно</option></select></div>
      </form>
      <div class="row mt-24">
        <a class="btn btn--primary sheen" href="#listing">Показать подходящие товары %s</a>
        <span class="micro">Полное дерево марка → модель → поколение → модификация подключается вместе с данными применяемости из 1С.</span>
      </div>
    </div>
  </div>
</section>""" % (sec_head("03 · Подбор по автомобилю", "Укажите свой автомобиль"), mark_options, ICON["arrow"])

quick_section = """<section class="section section--ink1 section--line">
  <div class="wrap">
    %s
    <div class="grid cols-2" data-stagger>
      <div class="card lac form-card reveal" id="quick-article">
        <p class="eyebrow">По артикулу FERES</p>
        <p class="small mt-16">Например: <b class="txt-sand">2112-1007300-02</b> или <b class="txt-sand">FR6PK1005</b></p>
        <div class="quickfind mt-16">
          <input class="field" type="text" placeholder="Введите артикул" aria-label="Поиск по артикулу FERES">
          <button class="btn btn--primary" type="button">Найти</button>
        </div>
      </div>
      <div class="card lac form-card reveal" id="quick-oem">
        <p class="eyebrow">По OEM или кроссу</p>
        <p class="small mt-16">Оригинальный номер производителя авто или артикул аналога другого бренда.</p>
        <div class="quickfind mt-16">
          <input class="field" type="text" placeholder="Введите OEM-номер" aria-label="Поиск по OEM-номеру">
          <button class="btn btn--primary" type="button">Найти</button>
        </div>
      </div>
    </div>
  </div>
</section>""" % sec_head("04 · Быстрый поиск по номеру", "Знаете номер — вводите сразу")

chips = ['<button class="chip" type="button" data-cat-filter="all" aria-pressed="true">Все группы</button>']
for g in groups:
    chips.append('<button class="chip" type="button" data-cat-filter="%s" aria-pressed="false">%s</button>' % (g["slug"], g["name"]))

def product_card(p):
    badge = '<span class="product__badge">Новинка</span>' if p.get("is_new") else ""
    app = " · ".join(p["applicability"][:2])
    return """<article class="card lac product reveal" data-cat-item data-group="%s">
        <div class="product__media">%s
          <img src="%s" alt="%s" loading="lazy" width="1000" height="600">
        </div>
        <div class="product__body">
          <h3 class="product__name"><a href="product.html?sku=%s">%s</a></h3>
          <p class="art">%s</p>
          <p class="product__meta"><span class="micro">%s</span><span class="micro">%s</span></p>
        </div>
        <div class="product__foot">
          <a class="link-arrow" href="where-to-buy.html">Где купить</a>
          <a class="micro" href="product.html?sku=%s">Подробнее</a>
        </div>
      </article>""" % (p["group_slug"], badge, p["image"], e(p["name"]),
                        e(p["sku"]), e(p["name"]), e(p["sku"]), e(p["group"]), e(app), e(p["sku"]))

listing_html = "\n      ".join(product_card(p) for p in items)

listing_section = """<section class="section" id="listing">
  <div class="wrap">
    %s
    <div class="chips filters--catalog" role="group" aria-label="Фильтр по группе">%s</div>
    <div class="grid cols-4" data-stagger data-cat-grid>
      %s
    </div>
    <div class="demo-note mt-24">%s
      <p>Показаны 10 демонстрационных товаров из 833 — это реальные артикулы и фото FERES, но полный каталог с фильтрами по применяемости появится после интеграции с 1С.</p>
    </div>
  </div>
</section>""" % (sec_head("05 · Каталог", "Все товары"),
                  "".join(chips), listing_html, ICON["info"])

content = head + "\n" + ways_section + "\n" + groups_section + "\n" + by_car_section + "\n" + quick_section + "\n" + listing_section

extra_ld = """<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    { "@type": "ListItem", "position": 1, "name": "Главная", "item": "https://feres.ru/" },
    { "@type": "ListItem", "position": 2, "name": "Каталог", "item": "https://feres.ru/catalog/" }
  ]
}
</script>"""

extra_scripts = '<script src="assets/js/catalog.js" defer></script>'

write_page("catalog.html",
           "Каталог автокомпонентов FERES — 833 позиции, подбор по авто, артикулу и OEM",
           "Каталог FERES: шесть групп автокомпонентов для ВАЗ, LADA, ГАЗ и УАЗ. Подбор по группе, автомобилю, артикулу FERES и OEM-номеру.",
           content, header, footer, extra_ld, extra_scripts)
