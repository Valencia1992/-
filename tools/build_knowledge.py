# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from common import *

header, footer = load_shell()
header = header.replace('<a href="knowledge.html">База знаний</a>', '<a href="knowledge.html" aria-current="page">База знаний</a>', 1)

head = page_head_block(
    "База знаний", "Разбираем ремонт по деталям",
    "Подбор деталей, устройство узлов, причины поломок и советы механиков — материалы, которые помогают выбрать правильное решение и понять, почему сломалась деталь.",
    crumbs(("База знаний", None)))

RUBRICS = ["Все статьи", "Подбор деталей", "Устройство деталей", "Причины поломок", "Советы механиков", "Инструкции", "FAQ"]
chips = "".join(
    '<button class="chip" type="button" data-kb-filter="%s" aria-pressed="%s">%s</button>'
    % (("all" if i == 0 else r), ("true" if i == 0 else "false"), r) for i, r in enumerate(RUBRICS))

ARTICLES = [
    ("Подбор деталей", "crop-pistons.jpg", "Как подобрать поршневую группу по ремонтному размеру",
     "Номинал и ремонтные размеры, маркировка на поршне, что смотреть в блоке перед заказом комплекта."),
    ("Причины поломок", "crop-valves.jpg", "Стучат гидрокомпенсаторы: что проверить до замены",
     "Давление масла, зазоры, качество масла и износ постели распредвала — разбираем, почему стук возвращается."),
    ("Советы механиков", "crop-liners.jpg", "Замена опоры передней стойки: ошибки, из-за которых стук возвращается",
     "Момент затяжки, положение подшипника, состояние отбойника — короткий чек-лист для СТО."),
    ("Советы механиков", "crop-rings.jpg", "Зачем менять кольца вместе с поршнями, а не отдельно",
     "Износ канавок и цилиндра растёт нелинейно — почему частичная замена не даёт ожидаемого результата."),
    ("Причины поломок", "crop-wide.jpg", "Задиры на гильзе: как отличить брак от неправильной обкатки",
     "Разбираем типичные причины задиров и на что смотреть при рекламации."),
    ("Устройство деталей", "crop-package.jpg", "Из чего состоит комплект сцепления и зачем менять все элементы разом",
     "Корзина, диск, выжимной подшипник — почему экономия на одном элементе сокращает ресурс остальных."),
]
def article_card(rubric, img, title, desc):
    return """<article class="card lac post reveal" data-kb-item data-kb-rubric="%s">
        <div class="post__media"><img class="post__img" src="assets/img/atmo/%s" alt="" loading="lazy" width="560" height="560"></div>
        <div class="post__body"><p class="post__cat">%s</p>
          <h3 class="h4">%s</h3><p class="small">%s</p>
          <p class="mt-8"><a class="link-arrow" href="#">Читать %s</a></p></div>
      </article>""" % (rubric, img, rubric, title, desc, ICON["arrow"])

articles_html = "\n      ".join(article_card(*a) for a in ARTICLES)

kb_section = """<section class="section section--tight">
  <div class="wrap">
    %s
    <div class="chips mt-24" style="margin-bottom:26px" role="group" aria-label="Рубрики">%s</div>
    <div class="grid cols-3" data-stagger data-kb-grid>%s</div>
  </div>
</section>""" % (sec_head("01 · Материалы", "Статьи и инструкции"), chips, articles_html)

FAQ = [
    ("Как убедиться, что деталь оригинальная FERES?", "На упаковке — QR-код, который ведёт на страницу товара с реальным артикулом. Приобретайте у партнёров из раздела «Где купить»."),
    ("Где посмотреть OEM-номер и применяемость детали?", "В карточке товара — блоки «Применяемость» и «OEM-номера». Если детали ещё нет в каталоге — уточните у ближайшего партнёра."),
    ("Даёте ли вы гарантию на продукцию?", "Да, гарантия предоставляется на всю продукцию FERES. Условия и сроки уточняйте у партнёра, у которого приобретали деталь."),
    ("Как стать дилером FERES?", "Заполните форму на странице «Партнёрам» — менеджер свяжется в течение рабочего дня."),
]
faq_html = "".join(
    """<details class="faq__item"><summary>%s %s</summary><p>%s</p></details>"""
    % (q, ICON["plus"], a) for q, a in FAQ)

faq_section = """<section class="section section--ink1 section--line">
  <div class="wrap">
    %s
    <div class="faq">%s</div>
  </div>
</section>""" % (sec_head("02 · Частые вопросы", "FAQ"), faq_html)

content = head + "\n" + kb_section + "\n" + faq_section

extra_ld = """<script type="application/ld+json">
{ "@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [""" + ",".join(
    '{"@type":"Question","name":"%s","acceptedAnswer":{"@type":"Answer","text":"%s"}}' % (e(q), e(a))
    for q, a in FAQ) + """] }
</script>
<script type="application/ld+json">
{ "@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
  { "@type": "ListItem", "position": 1, "name": "Главная", "item": "https://feres.ru/" },
  { "@type": "ListItem", "position": 2, "name": "База знаний", "item": "https://feres.ru/knowledge/" }
]}
</script>"""

extra_scripts = '<script src="assets/js/knowledge.js" defer></script>'

write_page("knowledge.html",
           "База знаний FERES — подбор деталей, причины поломок, советы механиков",
           "Статьи и инструкции FERES: как подобрать деталь, устройство узлов, причины поломок, советы механиков и ответы на частые вопросы.",
           content, header, footer, extra_ld, extra_scripts)
