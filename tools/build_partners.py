# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from common import *

header, footer = load_shell()
header = header.replace('<a href="partners.html">Партнёрам</a>', '<a href="partners.html" aria-current="page">Партнёрам</a>', 1)

head = page_head_block(
    "Партнёрам", "Помогаем партнёрам развивать продажи и доверие клиентов",
    "Магазину — товар, который можно уверенно рекомендовать. СТО — деталь, снижающая риск повторного обращения. Дилеру — маржа и поддержка на каждом этапе.",
    crumbs(("Партнёрам", None)),
    anchors=[("why", "Почему FERES"), ("terms", "Условия"), ("steps", "Как мы работаем"),
             ("support", "Поддержка"), ("form", "Стать партнёром")])

WHY = [
    ("Маржа и защита территории", "Прозрачная система цен по объёму закупок и закреплённые условия работы в регионе."),
    ("Гарантийное сопровождение", "Разбираем рекламации по существу: если случай гарантийный — решаем вопрос, а не ищем повод отказать."),
    ("Товар, который не стыдно рекомендовать", "Инженерное качество и контроль на каждом этапе производства снижают долю возвратов."),
    ("Готовые материалы для продаж", "Фото, видео, POS и обучающие курсы — не нужно делать контент самим."),
]
why_html = "\n      ".join(
    """<div class="card lac tile reveal"><span class="tile__icon">%s</span>
        <h3 class="h4">%s</h3><p class="small">%s</p></div>""" % (ICON["check"], t, d) for t, d in WHY)

why_section = """<section class="section section--tight" id="why">
  <div class="wrap">
    %s
    <div class="grid cols-4" data-stagger>%s</div>
  </div>
</section>""" % (sec_head("01 · Почему FERES", "С нами меньше риска"), why_html)

STEPS = [
    ("01", "Заявка", "Заполняете форму ниже — компания, город, тип бизнеса."),
    ("02", "Звонок менеджера", "Обсуждаем ассортимент, объём и условия работы в вашем регионе."),
    ("03", "Согласование", "Фиксируем прайс, уровень скидки и порядок поставок."),
    ("04", "Первая поставка", "Отгружаем с ближайшего склада, передаём сопроводительные документы."),
    ("05", "Личный кабинет", "Доступ к ценам, материалам, обучению и персональному менеджеру."),
]
steps_html = "".join(
    """<div class="step"><span class="step__num">%s</span><h3 class="h4">%s</h3><p class="small">%s</p></div>"""
    % (n, t, d) for n, t, d in STEPS)

steps_section = """<section class="section section--ink1 section--line" id="steps">
  <div class="wrap">
    %s
    <div class="steps">%s</div>
  </div>
</section>""" % (sec_head("02 · Как мы работаем", "От заявки до первой поставки", "Пять шагов — без лишней бюрократии."), steps_html)

terms_section = """<section class="section" id="terms">
  <div class="wrap">
    %s
    <div class="terms">
      <div class="card lac terms__card">
        <p class="eyebrow">Опт</p>
        <h3 class="h3">Разовые и объёмные закупки</h3>
        <ul class="terms__list">
          <li>Без привязки к территории и минимальному ассортименту</li>
          <li>Отгрузка с двух складов по России и СНГ</li>
          <li>Подходит магазинам, СТО и маркетплейс-продавцам</li>
        </ul>
      </div>
      <div class="card lac terms__card">
        <p class="eyebrow">Дилерство</p>
        <h3 class="h3">Закреплённая территория</h3>
        <ul class="terms__list">
          <li>Персональные условия по объёму закупок</li>
          <li>Приоритетная маркетинговая поддержка в регионе</li>
          <li>Бонусная программа и обучение команды</li>
        </ul>
      </div>
    </div>
  </div>
</section>""" % sec_head("03 · Условия", "Опт и дилерство")

SUPPORT = [
    ("Маркетинг", "Баннеры, фото, видео, листовки, каталоги, логотипы, POS, презентации — в центре загрузок личного кабинета."),
    ("Обучение", "Курсы и вебинары для продавцов и механиков, тестирование, сертификаты по итогам обучения."),
    ("Бонусная программа", "Дополнительная скидка за объём и участие в акциях — прогресс виден в личном кабинете дилера."),
    ("Материалы для скачивания", "Прайс, сертификаты продукции и презентации — доступны авторизованным партнёрам."),
]
support_html = "\n      ".join(
    """<div class="card lac tile reveal"><h3 class="h4">%s</h3><p class="small">%s</p>
        <p class="mt-8"><a class="link-arrow" href="account.html">Открыть в личном кабинете %s</a></p></div>"""
    % (t, d, ICON["arrow"]) for t, d in SUPPORT)

support_section = """<section class="section section--ink1 section--line" id="support">
  <div class="wrap">
    %s
    <div class="grid cols-4" data-stagger>%s</div>
  </div>
</section>""" % (sec_head("04 · Поддержка партнёров", "Что даём после первой поставки"), support_html)

form_section = """<section class="section" id="form">
  <div class="wrap">
    %s
    <div class="card lac form-card">
      <form data-consent-form>
        <div class="form-grid">
          <div class="form-grid__full">
            <label class="label" for="kind">Тип бизнеса</label>
            <select class="field" id="kind" name="kind">
              <option>Оптовик</option><option>Розничный магазин</option><option>СТО</option>
              <option>Интернет-магазин</option><option>Другое</option>
            </select>
          </div>
          <div><label class="label" for="pcompany">Компания</label>
            <input class="field" id="pcompany" name="company" placeholder="ООО «Автодеталь»" required></div>
          <div><label class="label" for="pcity">Город</label>
            <input class="field" id="pcity" name="city" placeholder="Тольятти" required></div>
          <div><label class="label" for="pname">Контактное лицо</label>
            <input class="field" id="pname" name="name" placeholder="Имя и фамилия" required></div>
          <div><label class="label" for="pphone">Телефон</label>
            <input class="field" id="pphone" name="phone" type="tel" placeholder="+7 (___) ___-__-__" required></div>
          <div class="form-grid__full"><label class="label" for="pcomment">Комментарий</label>
            <textarea class="field" id="pcomment" name="comment" rows="3" placeholder="Какой ассортимент интересует, текущие объёмы закупок"></textarea></div>
        </div>
        %s
        <div class="row mt-24">
          <button class="btn btn--primary sheen" type="submit">Отправить заявку</button>
          <a class="link-arrow" href="account.html">Уже партнёр — войти в личный кабинет %s</a>
        </div>
        <p class="form-ok mt-24" data-form-ok hidden>Заявка отправлена. Менеджер свяжется с вами в течение рабочего дня.</p>
      </form>
    </div>
  </div>
</section>""" % (sec_head("05 · Стать партнёром", "Заполните заявку"), CONSENT_BLOCK, ICON["arrow"])

content = head + "\n" + why_section + "\n" + steps_section + "\n" + terms_section + "\n" + support_section + "\n" + form_section

extra_ld = """<script type="application/ld+json">
{ "@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
  { "@type": "ListItem", "position": 1, "name": "Главная", "item": "https://feres.ru/" },
  { "@type": "ListItem", "position": 2, "name": "Партнёрам", "item": "https://feres.ru/partners/" }
]}
</script>"""

write_page("partners.html",
           "Партнёрам FERES — условия дилерства, опт, маркетинговая поддержка",
           "Условия для магазинов, СТО и дилеров FERES: опт и дилерство, маркетинговая поддержка, обучение, бонусная программа. Заявка на партнёрство.",
           content, header, footer, extra_ld)
