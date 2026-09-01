# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from common import *

header, footer = load_shell()
header = header.replace('<a href="company.html">Компания</a>', '<a href="company.html" aria-current="page">Компания</a>', 1)

head = page_head_block(
    "Компания", "FERES — производитель автокомпонентов",
    "Бренд ООО «Федерал Резерв»: производственная экспертиза, унаследованная от Federal-Mogul, и фокус на рынок России и СНГ с 2022 года.",
    crumbs(("Компания", None)),
    anchors=[("history", "История"), ("production", "Производство"), ("quality", "Контроль качества"),
             ("news", "Новости"), ("career", "Карьера")])

TIMELINE = [
    ("1899", "Начало экспертизы", "Федерал Резерв опирается на инженерные наработки, восходящие к компании Federal-Mogul — одному из старейших производителей автокомпонентов в мире."),
    ("2022", "Запуск бренда FERES", "FERES выходит на рынок России и СНГ как самостоятельный бренд для профессионального ремонта."),
    ("Сегодня", "833 позиции в каталоге", "Ассортимент расширяется каждый квартал: от цилиндропоршневой группы до тормозной системы и фильтров."),
]
tline_html = "".join(
    """<div class="tline__row"><span class="tline__year">%s</span>
        <div><h3 class="h4">%s</h3><p class="small mt-8">%s</p></div></div>"""
    % (y, t, d) for y, t, d in TIMELINE)

history_section = """<section class="section section--tight" id="history">
  <div class="wrap">
    %s
    <div class="tline">%s</div>
  </div>
</section>""" % (sec_head("01 · История", "Экспертиза, которой можно доверять"), tline_html)

production_section = """<section class="section section--ink1 section--line" id="production">
  <div class="wrap">
    %s
    <p class="lead" style="max-width:74ch">Мы понимаем, что происходит внутри двигателя: детали проектируются под реальные условия ремонта, а не под минимальную себестоимость. Каждая партия проходит контроль на входе и выходе производства.</p>
    <div class="gallery-band mt-24">
      <img src="assets/img/atmo/crop-pistons.jpg" alt="Производство поршней FERES" loading="lazy" width="560" height="560">
      <img src="assets/img/atmo/crop-liners.jpg" alt="Гильзы цилиндров FERES" loading="lazy" width="560" height="560">
      <img src="assets/img/atmo/crop-valves.jpg" alt="Клапаны и кольца FERES" loading="lazy" width="560" height="560">
      <img src="assets/img/atmo/crop-package.jpg" alt="Упаковка продукции FERES" loading="lazy" width="560" height="560">
    </div>
    <div class="demo-note mt-24">%s
      <p>Фотографии производственной площадки ожидаем от заказчика — здесь временно показаны предметные съёмки продукции.</p>
    </div>
  </div>
</section>""" % (sec_head("02 · Производство", "Полный цикл — от материала до упаковки"), ICON["info"])

QUALITY = [
    ("Инженерная экспертиза", "Геометрия и допуски проверяются под конкретный узел, а не усредняются под «универсальный» ремонт."),
    ("Контроль на входе и выходе", "Каждая партия проверяется перед отгрузкой — это снижает долю возвратов у партнёров."),
    ("Честная гарантия", "Мы остаёмся рядом после покупки: гарантийные случаи решаются по существу."),
]
quality_html = "\n      ".join(
    """<div class="card lac tile reveal"><span class="tile__icon">%s</span>
        <h3 class="h4">%s</h3><p class="small">%s</p></div>""" % (ICON["check"], t, d) for t, d in QUALITY)

quality_section = """<section class="section" id="quality">
  <div class="wrap">
    %s
    <div class="grid cols-3" data-stagger>%s</div>
  </div>
</section>""" % (sec_head("03 · Контроль качества", "Ответственность перед владельцем автомобиля"), quality_html)

certs_section = """<section class="section section--ink1 section--line" id="certificates">
  <div class="wrap">
    %s
    <div class="demo-note">%s
      <p>Сканы сертификатов соответствия ожидаем от заказчика — после загрузки они появятся здесь и в карточках товаров (кнопка «Скачать сертификат»).</p>
    </div>
  </div>
</section>""" % (sec_head("04 · Сертификаты", "Документы качества и соответствия"), ICON["info"])

NEWS = [
    ("12 августа 2026", "Ассортимент тормозной группы расширен: диски и колодки для семейства LADA"),
    ("29 июля 2026", "Новые точки продаж в Санкт-Петербурге и Перми"),
    ("15 июля 2026", "Открыт набор в программу обучения механиков FERES"),
]
news_html = "\n      ".join(
    """<a class="news__item reveal" href="#news"><span class="news__date">%s</span><span class="h4">%s</span></a>""" % (d, t)
    for d, t in NEWS)

news_section = """<section class="section" id="news">
  <div class="wrap">
    %s
    <div class="grid cols-3" data-stagger>%s</div>
  </div>
</section>""" % (sec_head("05 · Новости", "Что нового у FERES"), news_html)

career_section = """<section class="section section--ink1 section--line" id="career">
  <div class="wrap">
    %s
    <div class="card lac form-card">
      <p class="body" style="max-width:66ch">Открытых вакансий сейчас нет, но мы всегда рады резюме инженеров, технологов и специалистов по продажам автокомпонентов.</p>
      <a class="btn btn--primary mt-24 sheen" href="mailto:sales@feres.ru?subject=Резюме">Отправить резюме %s</a>
    </div>
  </div>
</section>""" % (sec_head("06 · Карьера", "Работа в FERES"), ICON["arrow"])

suppliers_section = """<section class="section" id="suppliers">
  <div class="wrap">
    %s
    <p class="body" style="max-width:70ch">Рассматриваем предложения от производителей сырья, комплектующих и упаковки. Опишите профиль вашей компании — ответим с условиями сотрудничества.</p>
    <a class="link-arrow mt-16" href="mailto:sales@feres.ru?subject=Предложение поставщика" style="display:inline-flex">sales@feres.ru %s</a>
  </div>
</section>""" % (sec_head("07 · Поставщикам", "Сотрудничество"), ICON["arrow"])

contacts_section = """<section class="section section--ink1 section--line">
  <div class="wrap">
    <div class="card lac form-card row" style="justify-content:space-between">
      <div><p class="eyebrow">Контакты и реквизиты</p>
        <p class="h3 mt-8">ООО «ФЕДЕРАЛ РЕЗЕРВ» · г. Тольятти</p></div>
      <a class="btn btn--ghost" href="contacts.html#requisites">Открыть контакты %s</a>
    </div>
  </div>
</section>""" % ICON["arrow"]

content = (head + "\n" + history_section + "\n" + production_section + "\n" + quality_section + "\n"
           + certs_section + "\n" + news_section + "\n" + career_section + "\n" + suppliers_section + "\n" + contacts_section)

extra_ld = """<script type="application/ld+json">
{ "@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
  { "@type": "ListItem", "position": 1, "name": "Главная", "item": "https://feres.ru/" },
  { "@type": "ListItem", "position": 2, "name": "Компания", "item": "https://feres.ru/company/" }
]}
</script>"""

write_page("company.html",
           "О компании FERES — производитель автокомпонентов ООО «Федерал Резерв»",
           "История, производство и контроль качества FERES: экспертиза от Federal-Mogul, бренд для рынка России и СНГ с 2022 года.",
           content, header, footer, extra_ld)
