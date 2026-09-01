# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from common import *

header, footer = load_shell()

head = page_head_block(
    "Личный кабинет", "Вход для партнёров",
    "Единый вход, разные интерфейсы по ролям: дилер, магазин, СТО или частный покупатель. Раздел разворачивается в Фазе 2 — здесь заложена архитектура ролей и авторизации.",
    crumbs(("Личный кабинет", None)))

auth_section = """<section class="section section--tight">
  <div class="wrap">
    <div class="auth">
      <div class="card lac form-card">
        <p class="eyebrow">Вход</p>
        <form class="mt-16" onsubmit="return false" aria-label="Вход в личный кабинет">
          <label class="label" for="email">Email или телефон</label>
          <input class="field" id="email" type="text" autocomplete="username" placeholder="you@company.ru">
          <label class="label mt-16" for="pass">Пароль</label>
          <input class="field" id="pass" type="password" autocomplete="current-password" placeholder="••••••••">
          <div class="row mt-16" style="justify-content:space-between">
            <a class="micro txt-sand" href="#">Забыли пароль?</a>
          </div>
          <button class="btn btn--primary btn--block mt-24 sheen" type="submit">Войти</button>
        </form>
        <p class="micro mt-24">Нет аккаунта? <a class="txt-sand" href="#register">Зарегистрироваться</a> — для дилеров, магазинов и СТО.</p>
        <div class="demo-note mt-24">%s
          <p>Личный кабинет — Фаза 2 проекта: авторизация и персональные цены подключаются после интеграции с 1С и Битрикс. Сейчас показана архитектура ролей.</p>
        </div>
      </div>

      <div id="register">
        <p class="label">Выберите роль при регистрации</p>
        <div class="roles mt-16">
          <div class="card lac role reveal">
            <span class="role__icon">%s</span>
            <h3 class="h4">Дилер</h3>
            <p class="small">РРЦ и персональная цена рядом, заказы и повторные заказы, прогресс до следующего уровня скидки, финансы и документы из 1С, центр загрузок, обучение, персональный менеджер.</p>
          </div>
          <div class="card lac role reveal">
            <span class="role__icon">%s</span>
            <h3 class="h4">Субдилер / магазин</h3>
            <p class="small">Материалы для продаж, обучение, акции, бонусная программа, сертификаты, новости.</p>
          </div>
          <div class="card lac role reveal">
            <span class="role__icon">%s</span>
            <h3 class="h4">СТО</h3>
            <p class="small">Техническая информация, видео по установке, типичные неисправности, поиск ближайшего дилера, статус авторизованного СТО.</p>
          </div>
          <div class="card lac role reveal">
            <span class="role__icon">%s</span>
            <h3 class="h4">Автовладелец</h3>
            <p class="small">Мои автомобили, напоминания о замене, программа лояльности — раздел Фазы 3.</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>""" % (ICON["info"], ICON["cart"], ICON["grid"], ICON["car"], ICON["lock"])

content = head + "\n" + auth_section

write_page("account.html",
           "Личный кабинет FERES — вход для дилеров, магазинов и СТО",
           "Личный кабинет партнёра FERES: персональные цены, заказы, обучение и материалы для продаж. Вход по ролям — дилер, магазин, СТО.",
           content, header, footer)
