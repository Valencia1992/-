# FERES Website — Проектная документация

## Команда разработки

**Заказчик:** ООО «Федерал Резерв» (FERES)
**Разработчик:** Claude Code
**Тип проекта:** Рабочий прототип HTML/CSS/JS (итеративная разработка)
**Итоговый формат:** Статический сайт на GitHub Pages

---

## 🎨 Типографическая система

### Главное правило

**НИКОГДА не используй `style="font-size: ..."`** в HTML. Только классы из типографии.

### Шрифты

- **Семейство:** FERES (PF Din Text Cond Pro)
- **Веса:** 300 (light), 400 (regular), 500 (medium), 700 (bold)
- **Файлы:** `/assets/fonts/feres-*.woff2`

### CSS переменные типографики

```css
/* Размеры */
--fs-h1, --fs-h2, --fs-h3, --fs-h4, --fs-h5
--fs-body, --fs-body-sm, --fs-small, --fs-xs, --fs-micro, --fs-eyebrow

/* Веса */
--font-light, --font-regular, --font-medium, --font-bold

/* Высота строк */
--lh-tight, --lh-normal, --lh-relaxed, --lh-loose

/* Интерлеттинг */
--ls-tight, --ls-normal, --ls-loose, --ls-ultra-loose
```

Все переменные определены в `/assets/css/typography.css`

### Классы для использования в HTML

**Заголовки:** `.h1`, `.h2`, `.h3`, `.h4`, `.h5`
**Текст:** `.body`, `.body-sm`, `.small`, `.xs`, `.micro`, `.lead`, `.eyebrow`, `.label`
**Утилиты:** `.font-bold`, `.font-medium`, `.uppercase`, `.lh-relaxed`, и т.д.

**Специфические компоненты:**
- `.quality-title` — заголовок блока качества (24px, bold, margin-bottom: 24px)
- `.quality-subtitle` — подзаголовок в качестве (19px, bold)
- `.quality-desc` — описание под подзаголовком (14px)
- `.cat-subtitle` — теги-тексты в каталоге (13px, uppercase, ls-loose)
- `.cat-category-title` — название категории каталога (16px, bold)

**Полный гайд:** `/assets/css/TYPOGRAPHY-GUIDE.md`

### ✅ Примеры правильного использования

```html
<!-- Заголовок -->
<h2 class="h2">Основной заголовок</h2>

<!-- Если нужен размер h1, но семантика h2 -->
<h2 class="h1">Выглядит как h1</h2>

<!-- Основной текст -->
<p class="body">Обычный абзац текста</p>

<!-- Мелкий текст -->
<p class="small">Мелкий текст</p>

<!-- Вспомогательный текст -->
<p class="eyebrow">Раздел · название</p>

<!-- Текст-тег -->
<span class="label">КАТЕГОРИЯ</span>

<!-- Комбинирование классов -->
<h3 class="h4 font-medium">Полусредний заголовок</h3>
```

### ❌ Запрещено

```html
<!-- ПЛОХО! Inline стили нарушают систему -->
<p style="font-size: 16px; line-height: 1.5;">Текст</p>

<!-- ПЛОХО! Hardcoded значения -->
<h2 style="font-size: 28px;">Заголовок</h2>

<!-- ПЛОХО! Смешивание подходов -->
<p class="body" style="font-size: 18px;">Текст</p>
```

---

## 🏗️ Структура проекта

```
site/
├── index.html                    # Главная страница
├── catalog.html                  # Каталог продукции
├── where-to-buy.html            # Где купить
├── knowledge.html               # База знаний
├── assets/
│   ├── css/
│   │   ├── feres.css            # Основной CSS (подключает typography.css)
│   │   ├── typography.css       # Типографическая система (v8+)
│   │   └── TYPOGRAPHY-GUIDE.md  # Полный гайд типографики
│   ├── fonts/
│   │   ├── feres-300.woff2
│   │   ├── feres-400.woff2
│   │   ├── feres-400i.woff2
│   │   ├── feres-500.woff2
│   │   └── feres-700.woff2
│   ├── js/
│   │   └── feres.js             # Three.js 3D модель шатуна
│   ├── img/                     # Изображения
│   ├── models/
│   │   └── model.glb            # 3D модель шатуна (14MB)
│   └── video/
│       └── feres-production-web.mp4
└── .gitignore
```

---

## 🚀 Развёртывание и кэш

### Управление кэшем браузера

**Версия CSS/JS в URL:**
```html
<link rel="stylesheet" href="assets/css/feres.css?v=8">
<script src="assets/js/feres.js?v=8"></script>
```

**Как обновить кэш:**
1. Измени всё `?v=X` на `?v=X+1` во ВСЕХ HTML файлах
2. Закоммитьте и запушьте
3. Пользователь обновит страницу (Ctrl+Shift+R)

### Актуальная версия

**Текущая версия кэша:** v=8

---

## 📱 Отзывчивый дизайн

### Breakpoints (используются в CSS)

- **Мобильный:** 0px — 719px
- **Планшет:** 720px — 899px
- **Десктоп:** 900px+

### Сетка (grid)

Основной контейнер `.wrap` использует max-width и центрирование.

---

## 🎯 3D модель (Three.js)

### Конфигурация

- **Three.js версия:** 0.152.0
- **CDN:** unpkg.com
- **Модель:** Connecting Rod (шатун) от Meshy AI
- **Размер:** 14MB GLB (оптимизировано)
- **Загрузчик:** GLTFLoader с DRACO поддержкой

### Что работает

✅ Модель загружается 100%
✅ Анимация воспроизводится
✅ Правильное освещение
✅ Auto-фокус камеры (Box3)
✅ Поддержка DRACO compression

### Ссылка на модель

```html
<img src="assets/models/model.glb" />
```

---

## 🔄 Git workflow

### Последние коммиты

```
v8   - Add comprehensive typography system
v7   - Add product photos from Федерал_фото directory  
v6   - Replace 6 product groups with 17 catalog categories
v5   - Add cache buster version to CSS and JS
```

### Как коммитить

```bash
git add site/
git commit -m "Описание изменений

- Пункт 1
- Пункт 2

Co-Authored-By: Claude Haiku 4.5 <noreply@anthropic.com>"
git push
```

---

## 📋 Правила разработки

1. **Типографика:** Используй только классы из TYPOGRAPHY-GUIDE.md
2. **CSS:** Добавляй стили в `feres.css` или `typography.css`, не в HTML
3. **HTML:** Пиши семантичный HTML5 (h1, h2, p, section, article)
4. **3D модель:** Не менял конфиги Three.js без обсуждения
5. **Git:** Коммитьте часто, с понятными сообщениями
6. **Кэш:** После правок обновляй версию в HTML (?v=N)

---

## ⚠️ Известные проблемы

- GitHub Pages может кэшировать контент (обновляется за 1-2 минуты)
- Некоторые браузеры кэшируют HTML агрессивнее чем CSS/JS
- Для разработки используй localhost вместо GitHub Pages

---

## 📞 Контакты заказчика

**Компания:** ООО «Федерал Резерв»
**Сайт:** https://feres.ru/
**Email:** valya060992@gmail.com
**Репозиторий:** https://github.com/Valencia1992/-

---

## 📅 История версий

| Версия | Дата | Изменения |
|--------|------|-----------|
| v8 | 2026-09-08 | Добавлена полная типографическая система |
| v7 | 2026-09-08 | Добавлены фото из Федерал_фото |
| v6 | 2026-09-08 | Каталог переделан на 17 категорий |
| v5 | 2026-09-07 | Кэш-бастер версия |
| v4 | 2026-09-07 | 3D модель шатуна работает |

---

**Последнее обновление:** 2026-09-08 (Claude Code)
