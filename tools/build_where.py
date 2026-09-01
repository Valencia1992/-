# -*- coding: utf-8 -*-
"""Собирает страницу «Где купить» из data/locations.json и data/map-russia.json.
   Точки выводятся в HTML статически (для индексации), фильтрация — на JS."""
import json, os, html

SITE = r"C:\Users\user\Desktop\Сайт FERES\site"
index = open(os.path.join(SITE, "index.html"), encoding="utf-8").read()
header = index[index.index("<!-- ================= ШАПКА ================="):index.index('<main id="main">')].strip()
footer = index[index.index("<!-- ================= ПОДВАЛ ================="):index.index('<script type="application/ld+json">')].strip()

loc = json.load(open(os.path.join(SITE, "data", "locations.json"), encoding="utf-8"))
points = [p for p in loc["locations"] if p["status"] == "active"]
mp = json.load(open(os.path.join(SITE, "data", "map-russia.json"), encoding="utf-8"))

TYPE_LABEL = {"opt": "Оптовик", "roz": "Розница", "sto": "СТО", "srv": "Сервис", "int": "Интернет"}
counts = {t: sum(1 for p in points if p["type"] == t) for t in TYPE_LABEL}
cities = sorted({p["city"] for p in points})

def e(s):
    return html.escape(str(s), quote=True)

def plural(n):
    d10, d100 = n % 10, n % 100
    if d10 == 1 and d100 != 11:
        return "%d точка продаж" % n
    if 2 <= d10 <= 4 and not (10 <= d100 < 20):
        return "%d точки продаж" % n
    return "%d точек продаж" % n

def phone_href(p):
    digits = "".join(ch for ch in p if ch.isdigit())
    if len(digits) == 11 and digits[0] == "8":
        digits = "7" + digits[1:]
    return "+" + digits if digits else "#"

ICON = {
 "pin": '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M20 10.5c0 5.4-8 12-8 12s-8-6.6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10.3" r="2.8"/></svg>',
 "phone": '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M21 16.9v2.5a2 2 0 0 1-2.2 2 19.6 19.6 0 0 1-8.5-3 19.3 19.3 0 0 1-6-6 19.6 19.6 0 0 1-3-8.6A2 2 0 0 1 3.3 1.6h2.5a2 2 0 0 1 2 1.7c.1 1 .4 2 .7 2.9a2 2 0 0 1-.5 2.1L7 9.4a16 16 0 0 0 6 6l1.1-1.1a2 2 0 0 1 2.1-.5c.9.3 1.9.6 2.9.7a2 2 0 0 1 1.7 2Z"/></svg>',
 "clock": '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M12 7.2V12l3.2 2"/></svg>',
 "mail": '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3.5 6.5 8.5 6 8.5-6"/></svg>',
 "arrow": '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
 "ext": '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 4h6v6M20 4l-9 9"/><path d="M18 14v4a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4"/></svg>',
}

# --- карточки точек ---------------------------------------------------------
cards = []
for p in points:
    phones = "".join(
        '<a class="point__row" href="tel:%s">%s<span>%s</span></a>' % (phone_href(ph), ICON["phone"], e(ph))
        for ph in p["phones"])
    mail = ('<a class="point__row" href="mailto:%s">%s<span>%s</span></a>' % (e(p["email"]), ICON["mail"], e(p["email"]))
            if p["email"] else "")
    badge_mod = " badge-type--opt" if p["type"] == "opt" else (" badge-type--sto" if p["type"] == "sto" else "")
    cards.append("""      <article class="point" id="point-%(id)d" data-point data-type="%(type)s" data-city="%(city)s"
        data-search="%(search)s">
        <div class="point__top">
          <div>
            <p class="point__city">%(city)s%(region)s</p>
            <h3 class="point__name">%(name)s</h3>
          </div>
          <span class="badge-type%(badge)s">%(type_label)s</span>
        </div>
        <p class="point__row">%(pin)s<span>%(address)s</span></p>
        %(phones)s
        <p class="point__row">%(clock)s<span>%(hours)s</span></p>
        %(mail)s
        <div class="point__acts">
          <button class="link-arrow" type="button" data-show-city="%(city)s">Показать на карте</button>
        </div>
      </article>""" % {
        "id": p["id"], "type": p["type"], "city": e(p["city"]),
        "region": (" · " + e(p["region"])) if p["region"] else "",
        "search": e((p["name"] + " " + p["city"] + " " + p["address"]).lower()),
        "name": e(p["name"]), "badge": badge_mod, "type_label": TYPE_LABEL[p["type"]],
        "address": e(p["address"]), "phones": phones, "hours": e(p["hours"]), "mail": mail,
        "pin": ICON["pin"], "clock": ICON["clock"]})

# --- карта -------------------------------------------------------------------
paths = "".join('<path class="map__land" d="%s"/>' % d for d in mp["paths"])
pins = []
for pt in mp["points"]:
    ids = [i for i in pt["ids"] if any(p["id"] == i for p in points)]
    if not ids:
        continue
    types = sorted({p["type"] for p in points if p["id"] in ids})
    pins.append('<button class="map__pin" type="button" style="left:%s%%;top:%s%%" data-pin="%s" '
                'data-types="%s" data-size="%s" aria-label="%s: %s"></button>'
                % (pt["x"], pt["y"], e(pt["city"]), " ".join(types),
                   "multi" if len(ids) > 1 else "one", e(pt["city"]), plural(len(ids))))
pins_html = "\n        ".join(pins)

city_options = "".join('<option value="%s">%s</option>' % (e(c), e(c)) for c in cities)

MARKETPLACES = [
    ("OZON", "https://ozon.ru/s/federal-reserve", "Официальный магазин FERES на Ozon: доставка по всей России, отзывы покупателей."),
    ("Wildberries", "https://www.wildberries.ru/seller/250097192", "Магазин бренда на Wildberries: пункты выдачи в каждом городе присутствия."),
    ("Яндекс Маркет", "https://market.yandex.ru/cc/Aa8ijG", "Витрина FERES на Яндекс Маркете: быстрая доставка и удобный подбор по авто."),
]
mp_cards = "\n      ".join(
    """<a class="card lac mp sheen reveal" href="%s" target="_blank" rel="noopener nofollow">
        <div>
          <p class="eyebrow eyebrow--bare">Маркетплейс</p>
          <p class="mp__name mt-8">%s</p>
        </div>
        <p class="mp__desc">%s</p>
        <span class="mp__go">Перейти в магазин %s</span>
      </a>""" % (url, name, desc, ICON["ext"]) for name, url, desc in MARKETPLACES)

CHANNELS = [
    ("opt", "Оптовые центры", "Закупка партиями, работа с магазинами и сетями. Оптовику — условия дилерства, отсрочка и поддержка продаж."),
    ("roz", "Розничные магазины", "Купить деталь поштучно, посмотреть упаковку и получить консультацию по подбору."),
    ("sto", "СТО и сервисы", "Ремонт с деталями FERES: механик подберёт позицию по автомобилю и сразу выполнит замену."),
]
channel_cards = "\n      ".join(
    """<div class="card lac tile reveal">
        <p class="stat__val" style="font-size:clamp(30px,3vw,42px)">%d</p>
        <h3 class="h4">%s</h3>
        <p class="small">%s</p>
        <p class="mt-8"><button class="link-arrow" type="button" data-show-type="%s">Показать на карте %s</button></p>
      </div>""" % (counts[code], title, desc, code, ICON["arrow"]) for code, title, desc in CHANNELS)

PAGE = """<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Где купить FERES — точки продаж, магазины и маркетплейсы</title>
<meta name="description" content="Где купить автокомпоненты FERES: %(n)d точек продаж в %(cities)d городах России — оптовые центры, магазины и СТО, а также официальные магазины бренда на Ozon, Wildberries и Яндекс Маркете.">
<link rel="canonical" href="https://feres.ru/where-to-buy/">
<meta property="og:type" content="website">
<meta property="og:title" content="Где купить FERES">
<meta property="og:description" content="%(n)d точек продаж в %(cities)d городах России и официальные магазины бренда на маркетплейсах.">
<link rel="icon" href="assets/img/brand/favicon.ico" sizes="any">
<link rel="preload" href="assets/fonts/feres-700.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="assets/css/feres.css">
</head>
<body>
<a class="skip" href="#main">Перейти к содержимому</a>

%(header)s

<main id="main">

<section class="page-head">
  <div class="wrap">
    <nav class="crumbs" aria-label="Хлебные крошки">
      <a href="index.html">Главная</a><span>/</span><span class="txt-dim">Где купить</span>
    </nav>
    <p class="eyebrow">Точки продаж</p>
    <h1 class="h1 mt-16">Где купить FERES</h1>
    <p class="lead mt-16" style="max-width:64ch">%(n_word)s в %(cities)d городах России: оптовые центры, розничные магазины и СТО. Плюс официальные магазины бренда на маркетплейсах — с доставкой в любой регион.</p>
    <nav class="anchors" aria-label="Разделы страницы">
      <a href="#map">Карта</a>
      <a href="#channels">Оптовики, розница, СТО</a>
      <a href="#online">Интернет-магазины</a>
      <a href="#marketplaces">Маркетплейсы</a>
      <a href="#add">Добавить точку</a>
    </nav>
  </div>
</section>

<!-- ================= КАРТА И ПОИСК ТОЧЕК ================= -->
<section class="section section--tight" id="map">
  <div class="wrap">
    <div class="sec-head">
      <p class="eyebrow">01 · Карта</p>
      <div class="scale" aria-hidden="true"></div>
      <div class="sec-head__top"><h2 class="h2">Найдите ближайшую точку</h2></div>
      <p class="body">Выберите город на карте или отфильтруйте список по типу точки. Показаны только действующие адреса.</p>
    </div>

    <div class="finder" data-finder>
      <div class="map">
        <div class="map__frame">
          <svg viewBox="%(viewbox)s" role="img" aria-label="Карта России с точками продаж FERES">
            %(paths)s
          </svg>
          %(pins)s
          <span class="map__label" data-map-label aria-hidden="true"></span>
        </div>
        <div class="map__legend">
          <span class="tick"><svg width="11" height="11" viewBox="0 0 24 24" fill="currentColor"><circle cx="12" cy="12" r="9"/></svg>Город с одной точкой</span>
          <span class="tick"><svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor"><circle cx="12" cy="12" r="9"/></svg>Несколько точек в городе</span>
          <span class="map__note">Координаты уточняются: сейчас точки показаны по центрам городов.</span>
        </div>
      </div>

      <div>
        <div class="filters">
          <button class="chip" type="button" data-filter-type="all" aria-pressed="true">Все точки</button>
          <button class="chip" type="button" data-filter-type="opt" aria-pressed="false">Оптовики · %(opt)d</button>
          <button class="chip" type="button" data-filter-type="roz" aria-pressed="false">Розница · %(roz)d</button>
          <button class="chip" type="button" data-filter-type="sto" aria-pressed="false">СТО · %(sto)d</button>
          <span class="filters__count" data-count-label>%(n)d точек</span>
        </div>

        <label class="vh" for="city">Город</label>
        <select class="field" id="city" data-filter-city style="margin-bottom:12px">
          <option value="">Все города</option>
          %(city_options)s
        </select>

        <div class="points" data-points>
%(cards)s
          <p class="empty" data-empty hidden>В этом городе точек продаж пока нет. Закажите на маркетплейсе или напишите нам — подскажем ближайшего партнёра.</p>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- ================= КАНАЛЫ ================= -->
<section class="section section--ink1 section--line" id="channels">
  <div class="wrap">
    <div class="sec-head">
      <p class="eyebrow">02 · Каналы продаж</p>
      <div class="scale" aria-hidden="true"></div>
      <div class="sec-head__top"><h2 class="h2">Опт, розница и сервис</h2></div>
      <p class="body">Три канала решают разные задачи. Магазину и сервису выгоднее работать напрямую с оптовым центром, автовладельцу — купить в рознице или сразу отремонтировать машину на СТО.</p>
    </div>
    <div class="grid cols-3" data-stagger>
      %(channels)s
    </div>
  </div>
</section>

<!-- ================= ИНТЕРНЕТ-МАГАЗИНЫ ================= -->
<section class="section" id="online">
  <div class="wrap">
    <div class="sec-head">
      <p class="eyebrow">03 · Интернет-магазины</p>
      <div class="scale" aria-hidden="true"></div>
      <div class="sec-head__top"><h2 class="h2">Онлайн-партнёры</h2></div>
    </div>
    <div class="card lac form-card">
      <p class="body">Список интернет-магазинов, которые продают продукцию FERES, формируется. Если вы продаёте наши детали онлайн — добавьте площадку, мы разместим ссылку в этом разделе.</p>
      <div class="row mt-24">
        <a class="btn btn--primary sheen" href="#add">Добавить интернет-магазин</a>
        <a class="link-arrow" href="#marketplaces">Пока смотрите маркетплейсы %(arrow)s</a>
      </div>
    </div>
  </div>
</section>

<!-- ================= МАРКЕТПЛЕЙСЫ ================= -->
<section class="section section--ink1 section--line" id="marketplaces">
  <div class="wrap">
    <div class="sec-head">
      <p class="eyebrow">04 · Маркетплейсы</p>
      <div class="scale" aria-hidden="true"></div>
      <div class="sec-head__top"><h2 class="h2">Официальные магазины бренда</h2></div>
      <p class="body">Это магазины самого производителя: ассортимент, упаковка и гарантия — те же, что у дилеров. Доставка работает по всей России, включая города без наших точек продаж.</p>
    </div>
    <div class="grid cols-3" data-stagger>
      %(marketplaces)s
    </div>
  </div>
</section>

<!-- ================= ФОРМЫ ================= -->
<section class="section" id="add">
  <div class="wrap">
    <div class="sec-head">
      <p class="eyebrow">05 · Стать точкой продаж</p>
      <div class="scale" aria-hidden="true"></div>
      <div class="sec-head__top"><h2 class="h2">Добавить магазин, СТО или стать дилером</h2></div>
      <p class="body">Заполните заявку — менеджер свяжется в течение рабочего дня, расскажет об условиях и пришлёт прайс.</p>
    </div>

    <div class="card lac form-card">
      <form data-consent-form>
        <div class="form-grid">
          <div class="form-grid__full">
            <label class="label" for="kind">Тип обращения</label>
            <select class="field" id="kind" name="kind" data-form-kind>
              <option value="shop">Добавить магазин</option>
              <option value="sto">Добавить СТО</option>
              <option value="dealer">Стать дилером</option>
            </select>
          </div>
          <div>
            <label class="label" for="company">Компания</label>
            <input class="field" id="company" name="company" placeholder="ООО «Автодеталь»" required>
          </div>
          <div>
            <label class="label" for="fcity">Город</label>
            <input class="field" id="fcity" name="city" placeholder="Тольятти" required>
          </div>
          <div>
            <label class="label" for="fname">Контактное лицо</label>
            <input class="field" id="fname" name="name" placeholder="Имя и фамилия" required>
          </div>
          <div>
            <label class="label" for="fphone">Телефон</label>
            <input class="field" id="fphone" name="phone" type="tel" placeholder="+7 (___) ___-__-__" required>
          </div>
          <div class="form-grid__full">
            <label class="label" for="fcomment">Комментарий</label>
            <textarea class="field" id="fcomment" name="comment" rows="3" placeholder="Адрес точки, ассортимент, который интересует"></textarea>
          </div>
        </div>

        <label class="consent mt-24">
          <input type="checkbox" data-consent>
          <span>Даю согласие на обработку персональных данных в соответствии с <a href="privacy-policy.html">политикой конфиденциальности</a> и <a href="personal-data-consent.html">согласием на обработку ПДн</a>.</span>
        </label>
        <label class="consent mt-16">
          <input type="checkbox">
          <span>Согласен получать новости и информацию об акциях (необязательно).</span>
        </label>

        <div class="row mt-24">
          <button class="btn btn--primary sheen" type="submit">Отправить заявку</button>
          <span class="micro">Отправляя заявку, вы соглашаетесь с условиями обработки данных. Факт согласия фиксируется.</span>
        </div>
        <p class="form-ok mt-24" data-form-ok hidden>Заявка отправлена. Менеджер свяжется с вами в течение рабочего дня.</p>
      </form>
    </div>
  </div>
</section>

</main>

%(footer)s

<div class="cookie" data-cookie role="dialog" aria-label="Использование cookies">
  <p>Сайт использует cookies и Яндекс.Метрику, чтобы работать корректно и понимать, какие разделы полезны. Подробности — в <a class="txt-sand" href="privacy-policy.html">политике конфиденциальности</a>.</p>
  <button class="btn btn--primary btn--sm" type="button" data-cookie-accept>Принять</button>
</div>

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    { "@type": "ListItem", "position": 1, "name": "Главная", "item": "https://feres.ru/" },
    { "@type": "ListItem", "position": 2, "name": "Где купить", "item": "https://feres.ru/where-to-buy/" }
  ]
}
</script>

<script src="assets/js/feres.js" defer></script>
<script src="assets/js/where-to-buy.js" defer></script>
</body>
</html>
"""

out = PAGE % {
    "header": header, "footer": footer,
    "n": len(points), "n_word": plural(len(points)).capitalize(), "cities": len(cities),
    "opt": counts["opt"], "roz": counts["roz"], "sto": counts["sto"],
    "viewbox": mp["meta"]["viewBox"], "paths": paths, "pins": pins_html,
    "city_options": city_options, "cards": "\n".join(cards),
    "channels": channel_cards, "marketplaces": mp_cards, "arrow": ICON["arrow"],
}
open(os.path.join(SITE, "where-to-buy.html"), "w", encoding="utf-8").write(out)
print("where-to-buy.html:", len(out), "байт ·", len(points), "точек ·", len(cities), "городов ·", len(pins), "маркеров")
