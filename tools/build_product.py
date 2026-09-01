# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from common import *

header, footer = load_shell()
data = products()
items = {p["sku"]: p for p in data["products"]}
groups = {g["slug"]: g for g in data["meta"]["groups"]}

SKU = "21127.100401587.01"          # демонстрационный товар — комплект поршневой, полный набор данных
p = items[SKU]
group = groups[p["group_slug"]]
other = [x for x in data["products"] if x["sku"] != SKU][:3]

crumbs_html = crumbs((group["name"], "catalog.html?group=%s" % p["group_slug"]), (p["name"], None))

gallery_imgs = [p["image"]] + p.get("gallery", [])
thumbs = "\n          ".join(
    '<button class="gallery__thumb%s" type="button" data-thumb="%s" aria-label="Фото %d">'
    '<img src="%s" alt="" loading="lazy"></button>'
    % (" is-active" if i == 0 else "", img, i + 1, img)
    for i, img in enumerate(gallery_imgs)) if len(gallery_imgs) > 1 else ""

badge = '<span class="product__badge" style="position:static;display:inline-block;margin-bottom:4px">Новинка</span><br>' if p.get("is_new") else ""

applist = "".join('<li>%s</li>' % e(a) for a in p["applicability"])

hero = """<section class="page-head section--tight">
  <div class="wrap">
    %s
  </div>
</section>

<section class="section section--tight">
  <div class="wrap pgrid">
    <div>
      <div class="gallery__main" id="gmain" data-gallery>
        <img src="%s" alt="%s" width="1000" height="600" fetchpriority="high">
      </div>
      <div class="gallery__thumbs">%s</div>
    </div>

    <div class="pinfo">
      <div>
        %s
        <h1 class="h1" style="font-size:clamp(30px,4vw,48px)">%s</h1>
        <p class="pinfo__art art mt-8">Артикул FERES: <b class="txt-sand">%s</b> · Группа: <a class="txt-sand" href="catalog.html?group=%s">%s</a></p>
      </div>

      <div class="pinfo__acts">
        <a class="btn btn--primary btn--lg sheen" href="where-to-buy.html">%s Где купить</a>
        <span class="btn btn--quiet btn--disabled">%s Скачать PDF</span>
        <span class="btn btn--quiet btn--disabled">%s Скачать сертификат</span>
      </div>
      <p class="pinfo__price">%s Цена не публикуется в открытом доступе. Для дилеров — <a href="account.html">РРЦ и ваша цена в личном кабинете</a>.</p>

      <div>
        <p class="label">Преимущества</p>
        <ul class="advlist mt-8">
          <li>%s Инженерное качество: геометрия и допуски проверены под конкретный двигатель, а не усреднены под «универсальный» ремонт.</li>
          <li>%s Контроль на входе и выходе производства — каждая партия проходит проверку перед отгрузкой.</li>
          <li>%s Упаковка и маркировка защищают от подделки: QR-код на коробке ведёт на страницу товара.</li>
        </ul>
      </div>

      <div>
        <p class="label">Применяемость</p>
        <ul class="applist mt-8">%s</ul>
      </div>
    </div>
  </div>
</section>""" % (crumbs_html, gallery_imgs[0], e(p["name"]), thumbs, badge, e(p["name"]), e(p["sku"]),
                  p["group_slug"], e(group["name"]), ICON["cart"], ICON["pdf"], ICON["cert"], ICON["lock"],
                  ICON["check"], ICON["check"], ICON["check"], applist)

# --- «С этим товаром покупают» — реальные другие товары, не выдумка -------
also_html = "\n      ".join(
    """<article class="card lac product reveal">
        <div class="product__media"><img src="%s" alt="%s" loading="lazy" width="1000" height="600"></div>
        <div class="product__body">
          <h3 class="product__name"><a href="product.html?sku=%s">%s</a></h3>
          <p class="art">%s</p>
        </div>
        <div class="product__foot">
          <a class="link-arrow" href="where-to-buy.html">Где купить</a>
          <a class="micro" href="product.html?sku=%s">Подробнее</a>
        </div>
      </article>""" % (x["image"], e(x["name"]), e(x["sku"]), e(x["name"]), e(x["sku"]), e(x["sku"]))
    for x in other)

also_section = """<section class="pblock section--ink1">
  <div class="wrap">
    <div class="pblock__head"><h2 class="h3">С этим товаром покупают</h2></div>
    <div class="grid cols-3" data-stagger>
      %s
    </div>
  </div>
</section>""" % also_html

# --- Статьи по теме (переиспользуем демо-материалы базы знаний) ------------
articles_section = """<section class="pblock">
  <div class="wrap">
    <div class="pblock__head"><h2 class="h3">Статьи по теме</h2>
      <a class="sec-link" href="knowledge.html">Вся база знаний %s</a></div>
    <div class="grid cols-3" data-stagger>
      <article class="card lac post reveal">
        <div class="post__media"><img class="post__img" src="assets/img/atmo/crop-pistons.jpg" alt="" loading="lazy" width="560" height="560"></div>
        <div class="post__body"><p class="post__cat">Подбор деталей</p>
          <h3 class="h4">Как подобрать поршневую группу по ремонтному размеру</h3>
          <p class="mt-8"><a class="link-arrow" href="knowledge.html">Читать</a></p></div>
      </article>
      <article class="card lac post reveal">
        <div class="post__media"><img class="post__img" src="assets/img/atmo/crop-rings.jpg" alt="" loading="lazy" width="480" height="320"></div>
        <div class="post__body"><p class="post__cat">Советы механиков</p>
          <h3 class="h4">Зачем менять кольца вместе с поршнями, а не отдельно</h3>
          <p class="mt-8"><a class="link-arrow" href="knowledge.html">Читать</a></p></div>
      </article>
      <article class="card lac post reveal">
        <div class="post__media"><img class="post__img" src="assets/img/atmo/crop-liners.jpg" alt="" loading="lazy" width="560" height="560"></div>
        <div class="post__body"><p class="post__cat">Причины поломок</p>
          <h3 class="h4">Задиры на гильзе: как отличить брак от неправильной обкатки</h3>
          <p class="mt-8"><a class="link-arrow" href="knowledge.html">Читать</a></p></div>
      </article>
    </div>
  </div>
</section>""" % ICON["arrow"]

# Наличие в СТО/автомагазинах — Фаза 3, место в структуре заложено, но скрыто
phase3_slot = "\n<!-- Блок «Наличие в СТО/автомагазинах» — Фаза 3 (интеграция остатков субдилеров). Место в структуре заложено, сейчас скрыт. -->\n"

content = hero + also_section + articles_section + phase3_slot

ld = """<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "%s",
  "sku": "%s",
  "mpn": "%s",
  "brand": { "@type": "Brand", "name": "FERES" },
  "image": ["https://feres.ru/%s"],
  "category": "%s"
}
</script>
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    { "@type": "ListItem", "position": 1, "name": "Главная", "item": "https://feres.ru/" },
    { "@type": "ListItem", "position": 2, "name": "Каталог", "item": "https://feres.ru/catalog/" },
    { "@type": "ListItem", "position": 3, "name": "%s", "item": "https://feres.ru/catalog/%s/" },
    { "@type": "ListItem", "position": 4, "name": "%s", "item": "https://feres.ru/product/%s/" }
  ]
}
</script>""" % (e(p["name"]), e(p["sku"]), e(p["sku"]), p["image"], e(group["name"]),
                e(group["name"]), p["group_slug"], e(p["name"]), p["sku"])

extra_scripts = '<script src="assets/js/product.js" defer></script>'

app_txt = ", ".join(p["applicability"])
write_page("product.html",
           "%s %s — купить %s FERES для %s" % (p["name"], p["sku"], group["name"].lower(), app_txt),
           "%s (%s): применяемость, преимущества, где купить. Артикул FERES, группа «%s»." % (p["name"], p["sku"], group["name"]),
           content, header, footer, ld, extra_scripts)
