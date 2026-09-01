# -*- coding: utf-8 -*-
"""Общие утилиты для генераторов страниц FERES: извлечение шапки/подвала
   из index.html, иконки, обёртка страницы."""
import json, os, html

SITE = r"C:\Users\user\Desktop\Сайт FERES\site"

def load_shell():
    index = open(os.path.join(SITE, "index.html"), encoding="utf-8").read()
    header = index[index.index('<!-- ================= ШАПКА ================='):index.index('<main id="main">')].strip()
    footer = index[index.index('<!-- ================= ПОДВАЛ ================='):index.index('<script type="application/ld+json">')].strip()
    return header, footer

def with_current(header, href_exact=None, topnav_text=None):
    """Помечает активный пункт меню aria-current="page" — по точному href в .nav
       или по тексту ссылки в верхней строке .header__topnav."""
    out = header
    if href_exact:
        needle = '<a href="%s">' % href_exact
        out = out.replace(needle, '<a href="%s" aria-current="page">' % href_exact, 1)
    if topnav_text:
        import re
        out = re.sub(r'(<a href="company\.html">)(%s)(</a>)' % re.escape(topnav_text),
                      r'\1\2\3', out)  # верхняя строка без подчёркивания — оставляем как есть
    return out

def e(s):
    return html.escape(str(s), quote=True)

ICON = {
 "pin": '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M20 10.5c0 5.4-8 12-8 12s-8-6.6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10.3" r="2.8"/></svg>',
 "phone": '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M21 16.9v2.5a2 2 0 0 1-2.2 2 19.6 19.6 0 0 1-8.5-3 19.3 19.3 0 0 1-6-6 19.6 19.6 0 0 1-3-8.6A2 2 0 0 1 3.3 1.6h2.5a2 2 0 0 1 2 1.7c.1 1 .4 2 .7 2.9a2 2 0 0 1-.5 2.1L7 9.4a16 16 0 0 0 6 6l1.1-1.1a2 2 0 0 1 2.1-.5c.9.3 1.9.6 2.9.7a2 2 0 0 1 1.7 2Z"/></svg>',
 "clock": '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M12 7.2V12l3.2 2"/></svg>',
 "mail": '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3.5 6.5 8.5 6 8.5-6"/></svg>',
 "arrow": '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
 "check": '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>',
 "ext": '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 4h6v6M20 4l-9 9"/><path d="M18 14v4a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4"/></svg>',
 "plus": '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 5v14M5 12h14"/></svg>',
 "info": '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M12 8h.01M11 12h1v5h1"/></svg>',
 "lock": '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="10.5" width="16" height="10" rx="2"/><path d="M8 10.5V7a4 4 0 0 1 8 0v3.5"/></svg>',
 "pdf": '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8Z"/><path d="M14 2v6h6"/></svg>',
 "cert": '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="8" r="6"/><path d="m9 13.5-1.5 7L12 18l4.5 2.5-1.5-7"/></svg>',
 "cart": '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="9" cy="20" r="1.4"/><circle cx="18" cy="20" r="1.4"/><path d="M2.5 3h2.4l2.7 12.2a2 2 0 0 0 2 1.6h7.7a2 2 0 0 0 2-1.6L21 7.5H6.2"/></svg>',
 "search": '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>',
 "car": '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M5 11h14l-1.4-4.2A2 2 0 0 0 15.7 5.4H8.3a2 2 0 0 0-1.9 1.4Z"/><path d="M5 11v6h14v-6"/><circle cx="8" cy="17.5" r="1.6"/><circle cx="16" cy="17.5" r="1.6"/></svg>',
 "grid": '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/></svg>',
 "hash": '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M5 9h14M5 15h14M10 4 8 20M16 4l-2 16"/></svg>',
 "swap": '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="m4 7 4-4 4 4M8 3v13"/><path d="m20 17-4 4-4-4M16 21V8"/></svg>',
}

PAGE_HEAD = """<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="https://feres.ru/{path}">
<meta property="og:type" content="website">
<meta property="og:title" content="{og_title}">
<meta property="og:description" content="{desc}">
<link rel="icon" href="assets/img/brand/favicon.ico" sizes="any">
<link rel="preload" href="assets/fonts/feres-700.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="assets/css/feres.css">
</head>
<body>
<a class="skip" href="#main">Перейти к содержимому</a>

{header}
<main id="main">
{content}
</main>

{footer}

<div class="cookie" data-cookie role="dialog" aria-label="Использование cookies">
  <p>Сайт использует cookies и Яндекс.Метрику, чтобы работать корректно и понимать, какие разделы полезны. Подробности — в <a class="txt-sand" href="privacy-policy.html">политике конфиденциальности</a>.</p>
  <button class="btn btn--primary btn--sm" type="button" data-cookie-accept>Принять</button>
</div>
{extra_ld}
<script src="assets/js/feres.js" defer></script>
{extra_scripts}
</body>
</html>
"""

def write_page(fname, title, desc, content, header, footer, extra_ld="", extra_scripts=""):
    html_out = PAGE_HEAD.format(
        title=title, desc=desc, path=fname, og_title=title.split(" —")[0],
        header=header, content=content, footer=footer, extra_ld=extra_ld, extra_scripts=extra_scripts)
    out_path = os.path.join(SITE, fname)
    open(out_path, "w", encoding="utf-8").write(html_out)
    print("%-24s %6d байт" % (fname, len(html_out)))

def crumbs(*pairs):
    """pairs: [(label, href_or_None), ...] последний — текущая страница (без ссылки)"""
    parts = ['<a href="index.html">Главная</a>']
    for label, href in pairs:
        parts.append("<span>/</span>")
        if href:
            parts.append('<a href="%s">%s</a>' % (href, e(label)))
        else:
            parts.append('<span class="txt-dim">%s</span>' % e(label))
    return '<nav class="crumbs" aria-label="Хлебные крошки">%s</nav>' % "".join(parts)

def page_head_block(eyebrow, h1, lead, crumbs_html, anchors=None, extra=""):
    a = ""
    if anchors:
        a = '<nav class="anchors" aria-label="Разделы страницы">%s</nav>' % "".join(
            '<a href="#%s">%s</a>' % (aid, e(label)) for aid, label in anchors)
    return """<section class="page-head">
  <div class="wrap">
    %s
    <p class="eyebrow">%s</p>
    <h1 class="h1 mt-16">%s</h1>
    <p class="lead mt-16" style="max-width:66ch">%s</p>
    %s
    %s
  </div>
</section>""" % (crumbs_html, e(eyebrow), h1, lead, a, extra)

def sec_head(eyebrow, h2, lead=None, link=None):
    l = ""
    if link:
        l = '<a class="sec-link" href="%s">%s %s</a>' % (link[1], e(link[0]), ICON["arrow"])
    p = '<p class="body">%s</p>' % lead if lead else ""
    return """<div class="sec-head">
      <p class="eyebrow">%s</p>
      <div class="scale" aria-hidden="true"></div>
      <div class="sec-head__top"><h2 class="h2">%s</h2>%s</div>
      %s
    </div>""" % (e(eyebrow), h2, l, p)

CONSENT_BLOCK = """<label class="consent mt-24">
          <input type="checkbox" data-consent>
          <span>Даю согласие на обработку персональных данных в соответствии с <a href="privacy-policy.html">политикой конфиденциальности</a> и <a href="personal-data-consent.html">согласием на обработку ПДн</a>.</span>
        </label>
        <label class="consent mt-16">
          <input type="checkbox">
          <span>Согласен получать новости и информацию об акциях (необязательно).</span>
        </label>"""

def products():
    return json.load(open(os.path.join(SITE, "data", "products.json"), encoding="utf-8"))
