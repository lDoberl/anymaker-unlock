# Anymaker Unlock

> 🇷🇺 [Русский](#русский) · 🇬🇧 [English](#english)

Небольшое десктоп‑приложение (GUI) для разблокировки предметов и компонентов в
одиночной игре **Anymaker (Demo)**. Редактирует только ваш локальный файл сохранения
`unlocks.txt`, делает резервную копию и умеет откатывать изменения.

A small desktop GUI to unlock items and vehicle components in the single‑player game
**Anymaker (Demo)**. It edits only your local `unlocks.txt`, keeps a backup, and can
roll back.

---

## Русский

### Что это

`unlocks.txt` в Anymaker — это список разблокированных объектов, зашифрованный так:

```
unlocks.txt = base32_lsb( utf8(JSON) XOR SteamID64 )
```

то есть обычный JSON `{"unlocked_items": [...]}`, поксоренный циклически вашим
**SteamID64** (17 цифр), а затем закодированный в **Base32** (алфавит
`abcdefghijklmnopqrstuvwxyz234567`, упаковка бит **LSB‑first**). Приложение умеет
читать, генерировать и записывать этот формат.

### Возможности

- **Пропатчить (безопасно)** — открывает весь контент, легальный для демо
  (`tech_tier ≤ 2`): предметы, компоненты редактора техники, все цвета покраски.
  Не вызывает встроенную «пасхалку» разработчиков.
- **Полный анлок (для изучения)** — галочка, открывающая вообще всё, включая контент
  полной игры (`tech_tier 3/4/5`: военное снаряжение, топовое оружие, спец‑компоненты).
- **Откатить к оригиналу** — восстанавливает ваш исходный `unlocks.txt` из бэкапа.
- Папка сейвов и **SteamID64** определяются автоматически.

### ⚠️ Про «рыбу» (анти‑тампер демо)

Разработчики добавили защиту: если в `unlocks.txt` появляется контент, недоступный в
демоверсии (`tech_tier 3+`), игра запускает троллинг‑эффект — **рыбу, кружащую вокруг
головы** (нарастает со временем), и **блокирует сохранение мира**. Поэтому режим
«Полный анлок» помечен как «для изучения»: он специально показывает этот эффект.
Безопасный режим его не вызывает. Если включили полный и хотите вернуть нормальную
игру — нажмите **«Откатить к оригиналу»**.

### Установка и запуск

Нужен **Python 3** (на python.org; `tkinter` входит в стандартную поставку для Windows).

Запуск из исходника:

```bash
python anymaker_unlock_gui.py
```

Должно открыться окно с кнопками.

### Сборка в .exe (Windows)

```bash
pip install pyinstaller
python -m PyInstaller --onefile --windowed --name "Anymaker Unlock" anymaker_unlock_gui.py
```

Готовый файл появится в `dist\Anymaker Unlock.exe`. Или просто запустите `build.bat`.

> SmartScreen/антивирус может предупредить о неизвестном издателе — это типично для
> неподписанных self‑built exe.

### Как пользоваться

1. Закройте игру (и по возможности Steam, чтобы облако не перезаписало файл).
2. Запустите приложение, при необходимости проверьте папку и SteamID64.
3. Нажмите **«Пропатчить»** (или поставьте галочку «Полный анлок» для изучения).
4. Запустите игру.
5. Чтобы вернуть всё назад — **«Откатить к оригиналу»**.

### Дисклеймер

Проект сделан для **личного использования в одиночной игре** и в образовательных целях
(разбор формата сохранения). Он меняет только ваш локальный файл и всегда создаёт
резервную копию. Не связан с разработчиками Anymaker. Используйте на свой страх и риск.
Полноценный контент честно открывается в полной версии игры.

---

## English

### What it is

In Anymaker, `unlocks.txt` is the list of unlocked objects, encrypted like this:

```
unlocks.txt = base32_lsb( utf8(JSON) XOR SteamID64 )
```

i.e. a plain JSON `{"unlocked_items": [...]}`, XOR‑ed cyclically with your **SteamID64**
(17 digits), then encoded as **Base32** (alphabet `abcdefghijklmnopqrstuvwxyz234567`,
**LSB‑first** bit packing). The app reads, generates and writes this format.

### Features

- **Patch (safe)** — unlocks everything that is legitimate for the demo
  (`tech_tier ≤ 2`): items, vehicle‑editor components, all paint colors.
  Does **not** trigger the developers' easter egg.
- **Full unlock (for study)** — a checkbox that unlocks everything, including full‑game
  content (`tech_tier 3/4/5`: military gear, top weapons, special components).
- **Roll back** — restores your original `unlocks.txt` from the backup.
- Save folder and **SteamID64** are detected automatically.

### ⚠️ About the "fish" (demo anti‑tamper)

The developers added a protection: if `unlocks.txt` contains content unavailable in the
demo (`tech_tier 3+`), the game triggers a troll effect — **fish circling your head**
(growing over time) — and **disables world saving**. That is why the "Full unlock" mode
is labeled "for study": it deliberately reproduces this effect. The safe mode never
triggers it. Press **Roll back** to return to normal.

### Install & run

Requires **Python 3** (from python.org; `tkinter` ships with Python on Windows).

Run from source:

```bash
python anymaker_unlock_gui.py
```

A window with buttons should open.

### Build a .exe (Windows)

```bash
pip install pyinstaller
python -m PyInstaller --onefile --windowed --name "Anymaker Unlock" anymaker_unlock_gui.py
```

The result appears in `dist\Anymaker Unlock.exe`. Or just run `build.bat`.

> SmartScreen/antivirus may warn about an unknown publisher — that is normal for
> unsigned, self‑built executables.

### Usage

1. Close the game (and Steam, so the cloud doesn't overwrite the file).
2. Launch the app; check the folder and SteamID64 if needed.
3. Click **Patch** (or tick **Full unlock** to study).
4. Launch the game.
5. To revert, click **Roll back**.

### Disclaimer

This project is for **personal, single‑player use** and for educational purposes
(reverse‑engineering the save format). It only edits your local file and always makes a
backup. Not affiliated with the Anymaker developers. Use at your own risk. Full content
is properly unlocked in the full version of the game.

---

## License

[MIT](LICENSE) © 2026 Dober
