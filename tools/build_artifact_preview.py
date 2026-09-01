# -*- coding: utf-8 -*-
"""Собирает index.html в один самодостаточный HTML-файл для публикации как
   Artifact: инлайнит CSS, JS, шрифты (base64) и все локальные картинки (base64),
   встраивает products.json прямо в скрипт (fetch к относительному пути в
   Artifact не сработает). Не трогает файлы в site/ — пишет отдельный файл."""
import base64, json, os, re, mimetypes

SITE = r"C:\Users\user\Desktop\Сайт FERES\site"
OUT = r"C:\Users\user\Desktop\Сайт FERES\tools\artifact-preview.html"

def data_uri(path):
    mime = mimetypes.guess_type(path)[0] or "application/octet-stream"
    if path.endswith(".woff2"):
        mime = "font/woff2"
    raw = open(path, "rb").read()
    return "data:%s;base64,%s" % (mime, base64.b64encode(raw).decode("ascii"))

html = open(os.path.join(SITE, "index.html"), encoding="utf-8").read()
css = open(os.path.join(SITE, "assets", "css", "feres.css"), encoding="utf-8").read()
js = open(os.path.join(SITE, "assets", "js", "feres.js"), encoding="utf-8").read()
products_json = open(os.path.join(SITE, "data", "products.json"), encoding="utf-8").read()

# --- 1. Шрифты внутри CSS: url('../fonts/xxx.woff2') -> data URI -----------
def font_repl(m):
    rel = m.group(1)
    fpath = os.path.normpath(os.path.join(SITE, "assets", "css", rel))
    return "url('%s')" % data_uri(fpath)
css = re.sub(r"url\('(\.\./fonts/[^']+)'\)", font_repl, css)

# --- 2. Локальные картинки в HTML: src="assets/..." -> data URI ------------
def img_repl(m):
    rel = m.group(1)
    fpath = os.path.join(SITE, rel)
    if not os.path.exists(fpath):
        return m.group(0)
    return 'src="%s"' % data_uri(fpath)
html = re.sub(r'src="(assets/img/[^"]+)"', img_repl, html)

# favicon/preload/canonical/og:image — не нужны и не резолвятся в артефакте
html = re.sub(r'\s*<link rel="canonical"[^>]*>\n', "\n", html)
html = re.sub(r'\s*<meta property="og:[^"]*"[^>]*>\n', "\n", html)
html = re.sub(r'\s*<link rel="icon"[^>]*>\n', "\n", html)
html = re.sub(r'\s*<link rel="apple-touch-icon"[^>]*>\n', "\n", html)
html = re.sub(r'\s*<link rel="preload"[^>]*>\n', "\n", html)

# --- 3. CSS: <link rel="stylesheet"> -> <style> -----------------------------
html = html.replace(
    '<link rel="stylesheet" href="assets/css/feres.css">',
    "<style>\n%s\n</style>" % css)

# --- 4. JS: products.json встраиваем прямо в скрипт, fetch не нужен --------
js_patched = js.replace(
    "fetch('data/products.json')\n      .then(function (r) { return r.ok ? r.json() : { products: [] }; })\n      .then(function (d) { products = d.products || []; })\n      .catch(function () { products = []; });",
    "products = (%s).products || [];" % products_json.strip())
assert js_patched != js, "не нашли место для встраивания products.json — проверь текст fetch в feres.js"

html = html.replace(
    '<script src="assets/js/feres.js" defer></script>',
    "<script>\n%s\n</script>" % js_patched)

# --- 5. Ссылки на другие страницы сайта — заметно, но не ломаем -------------
# (клики по ним в Artifact ни к чему не приведут; это ожидаемо для превью одной страницы)

# --- 6. favicon для Artifact: эмодзи ставится параметром publish, тут не нужен

open(OUT, "w", encoding="utf-8").write(html)
size_kb = os.path.getsize(OUT) / 1024
print("artifact-preview.html: %.0f КБ" % size_kb)
