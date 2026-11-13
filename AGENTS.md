# shavkero.com: инструкция для ИИ-ассистентов

Личный портфолио-сайт режиссёра Антона Шавкеро. Этот репозиторий и есть сайт.

- Статика на **GitHub Pages**, ветка `main`, домен из `CNAME`.
- Любой пуш в `main` появляется на https://shavkero.com примерно через минуту.
- Сборки нет, правится прямо HTML и JSON.

С Антоном общайся по-русски.

## Структура

| Путь | Что это |
|---|---|
| `index.html` | главная, сразу редиректит на `/works` |
| `works/index.html` | **/works**: короткая подборка из 15 главных работ, список `<li class="wo-it">` |
| `works/full/index.html` | **/works/full**: полный каталог, все работы с Vimeo, фильтры по категориям |
| `works/full/tags.json` | категории работ: `{ "<vimeo id>": ["FILMING","CAST",...] }` |
| `works/full/order.json` | порядок работ на /works/full: массив Vimeo ID |
| `works/full/intl.json` | какие работы показывать на /works/international: массив Vimeo ID |
| `works/international/index.html` | загрузчик: подгружает /works/full и фильтрует по `intl.json`. **Не править.** |
| `info/index.html` | **/info**: текст о себе и бренды с видео при наведении |
| `bio/` | /bio и /bio/deal-memo на EN, RU и ZH, плюс PDF |
| `admin/index.html` | админка работ (вкладки Категории, Порядок, International), см. ниже |
| `family/` | редирект на family.shavkero.com |
| `wp-content/` | статика от старой темы WordPress (CSS, JS, шрифты). **Не трогать.** |

## Частые задачи

**Категории, порядок, International.**
- Проще всего через админку https://shavkero.com/admin/. Пароль знает Антон.
- Или напрямую правкой `works/full/tags.json`, `order.json`, `intl.json`.

**Добавить работу в /works/full.**
1. Вставь в `works/full/index.html`, внутри `<ul id="wo-li">`, плитку по образцу соседних:
   ```html
   <li class="wo-it" data-src="https://player.vimeo.com/video/<ID>?h=<HASH>" data-fo="16/9" data-cats="ai"><div class="wo-ti y_"><div class="y"><div class="h">TITLE</div><div class="i">TITLE</div></div></div><div class="wo-vi y_"><div class="y"><img src="<постер vimeocdn …-d_1280x720?&amp;region=us>" alt></div></div></li>
   ```
   - `ID?h=HASH` берётся из `player_embed_url` видео на Vimeo.
   - `data-fo` — пропорции: `16/9`, `9/16`, `1/1`, `4/5`.
2. Добавь ID в `order.json` в нужное место. Работы, которых нет в `order.json`, встают в начало.
3. Добавь категории в `tags.json`.
4. Если работа нужна на /works/international, добавь её ID в `intl.json`.

**Новая категория.**
- В `works/full/index.html`, в `#wf-filter`, добавь кнопку `<button type="button" data-f="newcat">NEW CAT</button>`.
- `data-f` — это подпись в нижнем регистре без пробелов.
- Админка подхватит новую категорию сама.

**Переименовать работу на сайте.** Поменяй текст в обоих `<div class="h">` и `<div class="i">` этой плитки.

**Убрать работу.** Удали `<li>` и её ID из `order.json`, `tags.json` и `intl.json`.

**/works (главная подборка).** Список `<li class="wo-it">` в `works/index.html`, порядок как в файле.

**/info.** Текст лежит в `info/index.html` дважды, оба места надо менять вместе:
- `<p id="in-pa">` — мобильная версия, бренды в `<i>`;
- `<div id="in-hi">` — десктоп, бренды в `<i class="in-vi" data-src=... >` с видео-превью.

## Правила

- **Перед своими коммитами делай `git pull`.** Админка коммитит сама от имени «shavkero admin», в любой момент.
- JSON должен оставаться валидным.
- Никаких паролей, токенов и ключей в репозитории: он публичный.
- Не трогай `CNAME`, `wp-content/`, `works/international/index.html` и файлы подтверждения поисковиков `google5dfbe7d1e4f7953c.html`, `yandex_d698e60da82ef82c.html` (сайт подключён к Google Search Console и Яндекс Вебмастеру).
- SEO: `robots.txt` + `sitemap.xml` (новые публичные страницы добавляй туда); `/bio` и `/admin` закрыты от индексации (`noindex`) — bio отправляется клиентам по ссылке, в поиске её быть не должно. В заголовках /works, /info имя дублируется кириллицей «Антон Шавкеро» — для русских запросов, не убирать.
- Не трогай скрипты внутри `works/full/index.html`: порядок, фильтр International и живые теги. Правь только данные.
- После пуша проверь страницу на https://shavkero.com через 1–2 минуты. Кеш браузера: ⌘⇧R.

## Как устроена админка

- Страница `admin/index.html` лежит здесь.
- API работает на сервере Антона в Германии: `stats.clan.team/shavkero/api.php`.
- Сохранение: API кладёт pending-файл, systemd на сервере коммитит его в этот репозиторий через deploy key, дальше публикует GitHub Pages.
- Код API и скрипта синхронизации не в этом репо. Подробности в базе знаний Антона: Obsidian, `04-projects/shavkero-com-site.md`.
