# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from common import *

header, footer = load_shell()
header = header.replace('<a href="contacts.html">Контакты</a>', '<a href="contacts.html" aria-current="page">Контакты</a>', 1)

head = page_head_block(
    "Контакты", "Контакты",
    "Свяжитесь с нами напрямую или отправьте сообщение через форму — ответим в течение рабочего дня.",
    crumbs(("Контакты", None)))

cards_section = """<section class="section section--tight">
  <div class="wrap">
    %s
    <div class="grid cols-3" data-stagger>
      <div class="card lac tile reveal">
        <span class="tile__icon">%s</span>
        <h3 class="h4">Адрес</h3>
        <p class="small">445007, г. Тольятти,<br>ул. Ленина, 42, стр. 3</p>
        <p class="mt-8"><a class="link-arrow" href="https://yandex.ru/maps/?text=%s" target="_blank" rel="noopener">Открыть на карте %s</a></p>
      </div>
      <div class="card lac tile reveal">
        <span class="tile__icon">%s</span>
        <h3 class="h4">Телефоны</h3>
        <p class="small"><a href="tel:+78482639090">+7 (8482) 63-90-90</a><br>
          <a href="tel:+78482298008">+7 (8482) 29-80-08</a><br>
          <a href="tel:+78482639999">+7 (8482) 63-99-99</a></p>
      </div>
      <div class="card lac tile reveal">
        <span class="tile__icon">%s</span>
        <h3 class="h4">Почта</h3>
        <p class="small"><a href="mailto:sales@feres.ru">sales@feres.ru</a></p>
        <p class="micro mt-8">Отдел продаж и общие вопросы</p>
      </div>
    </div>
  </div>
</section>""" % (sec_head("01 · Прямые контакты", "Как с нами связаться"),
                  ICON["pin"], "Тольятти, ул. Ленина, 42", ICON["arrow"], ICON["phone"], ICON["mail"])

form_section = """<section class="section section--ink1 section--line">
  <div class="wrap">
    %s
    <div class="card lac form-card" style="max-width:640px">
      <form data-consent-form>
        <div class="form-grid">
          <div><label class="label" for="cname">Имя</label>
            <input class="field" id="cname" name="name" placeholder="Как к вам обращаться" required></div>
          <div><label class="label" for="cphone">Телефон или email</label>
            <input class="field" id="cphone" name="contact" placeholder="Для ответа" required></div>
          <div class="form-grid__full"><label class="label" for="cmsg">Сообщение</label>
            <textarea class="field" id="cmsg" name="message" rows="4" placeholder="Опишите вопрос" required></textarea></div>
        </div>
        %s
        <button class="btn btn--primary mt-24 sheen" type="submit">Отправить сообщение</button>
        <p class="form-ok mt-24" data-form-ok hidden>Сообщение отправлено. Ответим в течение рабочего дня.</p>
      </form>
    </div>
  </div>
</section>""" % (sec_head("02 · Обратная связь", "Написать нам"), CONSENT_BLOCK)

req_section = """<section class="section" id="requisites">
  <div class="wrap">
    %s
    <div class="card lac form-card">
      <div class="grid cols-2">
        <div>
          <p class="label">Полное наименование</p>
          <p class="body mt-8">Общество с ограниченной ответственностью «ФЕДЕРАЛ РЕЗЕРВ»</p>
          <p class="label mt-24">Юридический адрес</p>
          <p class="body mt-8">445007, Самарская область, г. Тольятти, ул. Ленина, 42, стр. 3</p>
        </div>
        <div>
          <p class="label">ИНН / ОГРН</p>
          <p class="body mt-8">Уточняется — реквизиты будут добавлены после получения от заказчика.</p>
          <p class="label mt-24">Банковские реквизиты</p>
          <p class="body mt-8">Предоставляются по запросу для заключения договора.</p>
        </div>
      </div>
    </div>
  </div>
</section>""" % sec_head("03 · Реквизиты", "ООО «Федерал Резерв»")

content = head + "\n" + cards_section + "\n" + form_section + "\n" + req_section

extra_ld = """<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "FERES",
  "legalName": "ООО «ФЕДЕРАЛ РЕЗЕРВ»",
  "address": { "@type": "PostalAddress", "streetAddress": "ул. Ленина, 42, стр. 3", "addressLocality": "Тольятти", "postalCode": "445007", "addressCountry": "RU" },
  "telephone": "+7-8482-63-90-90",
  "email": "sales@feres.ru",
  "url": "https://feres.ru/contacts/"
}
</script>"""

write_page("contacts.html",
           "Контакты FERES — адрес, телефоны, реквизиты",
           "Контакты ООО «Федерал Резерв»: адрес в Тольятти, телефоны отдела продаж, email, реквизиты компании и форма обратной связи.",
           content, header, footer, extra_ld)
