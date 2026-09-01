# Генераторы страниц FERES

Каждая внутренняя страница сайта (кроме `index.html` и `ui-kit.html`, они написаны вручную)
собирается своим Python-скриптом. Скрипт один раз читает шапку и подвал из `site/index.html`
и данные из `site/data/*.json`, поэтому шапка, подвал, карточки товаров и точки продаж везде
идентичны — правятся в одном месте и перегенерируются везде разом.

## Как перегенерировать страницу

```bash
cd tools
python build_catalog.py      # -> ../site/catalog.html
python build_product.py      # -> ../site/product.html
python build_where.py        # -> ../site/where-to-buy.html
python build_partners.py     # -> ../site/partners.html
python build_company.py      # -> ../site/company.html
python build_knowledge.py    # -> ../site/knowledge.html
python build_contacts.py     # -> ../site/contacts.html
python build_account.py      # -> ../site/account.html
python build_legal.py        # -> ../site/privacy-policy.html и ../site/personal-data-consent.html
```

Требуется Python 3 (без внешних зависимостей — только стандартная библиотека).

## Файлы

- **`common.py`** — общие утилиты: извлечение шапки/подвала, иконки, обёртка страницы,
  хлебные крошки, блок согласия 152-ФЗ. Импортируется всеми остальными скриптами.
- **`build_map.py`** — отдельная утилита: строит `site/data/map-russia.json` (контур России +
  координаты городов) из geojson-источника Natural Earth. Запускается редко — только если
  меняется список точек продаж в `locations.json` или нужно перестроить карту.

## Если меняете данные

- Товары каталога → правьте `site/data/products.json`, затем перезапустите `build_catalog.py`
  и `build_product.py`.
- Точки продаж → правьте `site/data/locations.json`, затем `build_where.py` (и `build_map.py`,
  если поменялись города).
- Шапка/подвал → правьте их в `site/index.html` (единственная страница с оригинальной
  разметкой шапки/подвала), затем перезапустите ВСЕ скрипты — они читают шапку/подвал заново
  при каждом запуске.

## Важно

Скрипт **`build_stubs.py` намеренно удалён** из этой папки — на раннем этапе он генерировал
страницы-заглушки с описанием будущего наполнения. Все эти страницы теперь собраны по-настоящему
(`build_catalog.py`, `build_partners.py` и т. д.). Если такой скрипт где-то попадётся — не
запускайте его, он затрёт реальные страницы placeholder-текстом.
