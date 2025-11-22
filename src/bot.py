import telebot
from telebot import types
import os
from datetime import datetime
import psycopg2  # <-- вместо sqlite3

# -----------------------------
# 1. НАСТРОЙКИ
# -----------------------------
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")  # теперь токен берётся из ENV
ADMIN_CHAT_ID = int(os.getenv("ADMIN_CHAT_ID", "1311098591"))
ADMIN_USER_ID = int(os.getenv("ADMIN_USER_ID", "5054557414"))

if not TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN не найден! Установи переменную окружения.")

bot = telebot.TeleBot(TOKEN)

# используем DATABASE_URL для PostgreSQL
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL не найден! Добавь его в переменные окружения.")


def get_conn():
    return psycopg2.connect(DATABASE_URL)


# -----------------------------
# 2. МИССИИ
# -----------------------------
MISSIONS = {
    1: {
        "title": "🎬 Разобраться, как работает TikTok",
        "task": "Найди на YouTube 2–3 видео про то, как развивать канал или делать короткие ролики. "
                "Выпиши 3 совета, которые реально тебе пригодятся, и сними короткое видео “Что я понял про TikTok”.",
        "bonus": 250
    },
    2: {
        "title": "✍️ Разбор блогеров по Standoff 2",
        "task": "Найди 1–2 блогеров, которые тебе реально нравятся. Выпиши, что у них крутого (монтаж, музыка, стиль) "
                "и что можно взять себе.",
        "bonus": 200
    },
    3: {
        "title": "🔎 Как попасть в рекомендации",
        "task": "Посмотри видео “как работает алгоритм TikTok”. Сделай короткий конспект: 5 пунктов, "
                "что помогает ролику попасть в рекомендации.",
        "bonus": 200
    },
    4: {
        "title": "🧠 Что делает видео интересным",
        "task": "Подумай и запиши короткий ролик “Что делает видео интересным” — объясни своими словами.",
        "bonus": 300
    },
    5: {
        "title": "✍️ 5 идей коротких видео",
        "task": "Придумай 5 идей для роликов (мувики, советы, реакции, нарезки).",
        "bonus": 200
    },
    6: {
        "title": "💡 Придумай “правило канала”",
        "task": "Сформулируй свою идею: что тебя отличает от других (например, “играю красиво, не токсично”). "
                "Вставь это в описание профиля.",
        "bonus": 150
    },
    7: {
        "title": "🎨 Найди свой визуальный стиль",
        "task": "Найди 2–3 канала с крутым оформлением, отметь, что нравится (цвета, фон, логотип), "
                "придумай свой вариант оформления и обсуди идею.",
        "bonus": 350
    },
    8: {
        "title": "🎨 Обложка или логотип",
        "task": "Сделай обложку профиля или логотип канала (в Canva, Leonardo.ai и т.п.).",
        "bonus": 350
    },
    9: {
        "title": "🔊 Музыкальная фишка",
        "task": "Подбери музыкальную тему, которая будет “твоей фишкой” (например, использовать один бит "
                "в начале видео).",
        "bonus": 100
    },
    10: {
        "title": "💬 Приветствие для видео",
        "task": "Придумай короткую фразу, с которой ты начинаешь видео.",
        "bonus": 100
    },
    11: {
        "title": "🎧 Музыка под настроение",
        "task": "Сделай новое видео, где подбираешь музыку под эмоцию боя (и объясни, почему именно она).",
        "bonus": 300
    },
    12: {
        "title": "⚙️ Эффекты и переходы",
        "task": "Найди видео “как сделать плавные переходы / эффекты в CapCut”. Применяй 1–2 приёма в новом ролике.",
        "bonus": 300
    },
    13: {
        "title": "✂️ Разбор чужого видео",
        "task": "Возьми видео другого блогера, разбери по кадрам — где добавлены эффекты, переходы, музыка.",
        "bonus": 150
    },
    14: {
        "title": "💻 3 эффекта в клипе",
        "task": "Смонтируй свой клип с тремя эффектами (в CapCut, DaVinci, VN и т.п.).",
        "bonus": 350
    },
    15: {
        "title": "🧩 Туториал по монтажу",
        "task": "Найди туториал “монтаж геймплея Standoff 2” и повтори один приём.",
        "bonus": 200
    },
    16: {
        "title": "🔥 Что я узнал про монтаж",
        "task": "Сделай короткий ролик “Что я узнал, пока учился монтажу” — расскажи или покажи примеры.",
        "bonus": 250
    },
    17: {
        "title": "🧩 Придумай 3 идеи видео",
        "task": "Придумай три идеи: одну смешную, одну эпичную, одну с историей.",
        "bonus": 200
    },
    18: {
        "title": "📜 Сценарий одного видео",
        "task": "Напиши короткий план сценария (вступление, идея, концовка). Можно брать любую тему и идею, "
                "которая у тебя есть.",
        "bonus": 250
    },
    19: {
        "title": "🗒️ Сценарий с деталями",
        "task": "Напиши более подробный сценарий (400–500 слов печатного текста): что происходит, где, под какую "
                "музыку, что должен почувствовать зритель. Обсуди и внеси правки после обсуждения.",
        "bonus": 350
    },
    20: {
        "title": "🎥 Тестовое видео",
        "task": "Сними по своему сценарию короткий ролик и отметь, что можно улучшить.",
        "bonus": 250
    },
    21: {
        "title": "🧠 Историческое видео",
        "task": "Сделай ролик о себе — “Как я учился играть / монтировать”.",
        "bonus": 300
    },
    22: {
        "title": "🕹️ Новая тема: прокачка навыка",
        "task": "Выбери тему (анимация, AI, эффекты). Посмотри 2 ролика и попробуй применить хотя бы один приём.",
        "bonus": 300
    },
    23: {
        "title": "💬 Как я стал лучше",
        "task": "Сделай видео “Что я прокачал за последнее время” — покажи 2–3 фишки, которые освоил "
                "(в игре, монтаже или контенте). Можно в формате “до / после”.",
        "bonus": 250
    },
    24: {
        "title": "📊 Мои фейлы и апгрейды",
        "task": "Запиши ролик “Топ 3 ошибок, которые я делал, и чему они меня научили”. "
                "Добавь короткие примеры из своих видео или игры.",
        "bonus": 300
    },
    25: {
        "title": "🔍 Изучение форматов",
        "task": "Найди и проанализируй 5 разных форматов (реакция, гайд, челлендж, обзор). "
                "Определи, какие подходят тебе, и сделай короткое видео с выводами "
                "(можно просто форматом разговорного видео без монтажа).",
        "bonus": 300
    },
    26: {
        "title": "🤖 Эксперимент с ИИ",
        "task": "Используй ChatGPT (или аналог): напиши запрос для сценария видео → получи ответ → доработай под себя. "
                "Напиши мини-отчёт “промпт → ответ → доработка”.",
        "bonus": 350
    },
    27: {
        "title": "🤖 Идеи через ChatGPT",
        "task": "С помощью ChatGPT придумай идеи для серии видео и выбери лучшую. "
                "Напиши мини-отчёт — какие промпты ты использовал и что выдал ИИ.",
        "bonus": 150
    },
    28: {
        "title": "🧠 Анимация с ИИ — разведка",
        "task": "Разбери тему: как создавать анимацию с помощью искусственного интеллекта. Найди 2–3 бесплатных "
                "инструмента (например, Kaiber, Pika Labs, Runway ML и т.п.), узнай, что они умеют, и какой из них можно "
                "использовать для твоего контента. Составь мини-список с краткими описаниями (название — что делает — плюс/минус).",
        "bonus": 300
    },
    29: {
        "title": "🎞️ Сделай тест-анимацию",
        "task": "Используй один из инструментов, что нашёл (Kaiber, Pika, Runway). Сделай короткую тест-анимацию — "
                "можно превратить фрагмент геймплея в “синематику”.",
        "bonus": 400
    },
    30: {
        "title": "📣 Взаимодействие с подписчиками",
        "task": "Посмотри видео “как выстраивать аудиторию на TikTok/YouTube”. Сделай конспект 3–5 пунктов, "
                "придумай один мини-опыт (опрос, челлендж, Q&A) и реализуй.",
        "bonus": 350
    },
    31: {
        "title": "🎯 Тест форматов",
        "task": "Финальный тест контента: выбери 3 формата (гайд, челлендж, летсплей и т.д.). Сними по одному видео "
                "каждого, проанализируй, что зашло лучше. Сделай мини-отчёт “что выстрелило и почему”.",
        "bonus": 500
    },
}

# -----------------------------
# 3. БАЗА ДАННЫХ
# -----------------------------


def init_db():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS mission_reports (
            id SERIAL PRIMARY KEY,
            user_id BIGINT,
            username TEXT,
            chat_id BIGINT,
            mission_num INTEGER,
            standard_bonus INTEGER,
            extra_bonus INTEGER DEFAULT 0,
            status TEXT DEFAULT 'pending', -- pending / accepted / redo / discuss
            admin_comment TEXT,
            created_at TIMESTAMP
        )
        """
    )
    conn.commit()
    conn.close()


def create_or_update_report(user_id, username, chat_id, mission_num, standard_bonus):
    conn = get_conn()
    cur = conn.cursor()

    # Проверяем, есть ли уже отчет по этой миссии от этого юзера
    cur.execute(
        "SELECT id FROM mission_reports WHERE user_id = %s AND mission_num = %s",
        (user_id, mission_num)
    )
    row = cur.fetchone()
    now = datetime.now()

    if row:
        # Отчет уже есть — обновляем
        report_id = row[0]
        cur.execute(
            """
            UPDATE mission_reports
            SET username = %s, chat_id = %s, standard_bonus = %s,
                extra_bonus = 0,
                status = 'pending',
                admin_comment = NULL,
                created_at = %s
            WHERE id = %s
            """,
            (username, chat_id, standard_bonus, now, report_id)
        )
    else:
        # Отчета нет — создаем
        cur.execute(
            """
            INSERT INTO mission_reports (user_id, username, chat_id, mission_num, standard_bonus, created_at)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id
            """,
            (user_id, username, chat_id, mission_num, standard_bonus, now)
        )
        report_id = cur.fetchone()[0]

    conn.commit()
    conn.close()
    return report_id


def update_status(report_id, status):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("UPDATE mission_reports SET status = %s WHERE id = %s", (status, report_id))
    conn.commit()
    conn.close()


def set_total_bonus(report_id, amount):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "UPDATE mission_reports SET standard_bonus = %s, extra_bonus = 0 WHERE id = %s",
        (amount, report_id)
    )
    conn.commit()
    conn.close()


def add_extra_bonus(report_id, amount):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("UPDATE mission_reports SET extra_bonus = extra_bonus + %s WHERE id = %s", (amount, report_id))
    conn.commit()
    conn.close()


def set_admin_comment(report_id, comment):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("UPDATE mission_reports SET admin_comment = %s WHERE id = %s", (comment, report_id))
    conn.commit()
    conn.close()


def get_report(report_id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, user_id, username, chat_id, mission_num, standard_bonus, extra_bonus, status, admin_comment "
        "FROM mission_reports WHERE id = %s",
        (report_id,)
    )
    row = cur.fetchone()
    conn.close()
    if not row:
        return None
    return {
        "id": row[0],
        "user_id": row[1],
        "username": row[2],
        "chat_id": row[3],
        "mission_num": row[4],
        "standard_bonus": row[5],
        "extra_bonus": row[6],
        "status": row[7],
        "admin_comment": row[8],
    }


def get_user_balance(user_id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "SELECT COALESCE(SUM(standard_bonus + extra_bonus), 0) FROM mission_reports WHERE user_id = %s AND status = 'accepted'",
        (user_id,)
    )
    row = cur.fetchone()
    conn.close()
    return row[0] or 0


def set_total_bonus(report_id, amount):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "UPDATE mission_reports SET standard_bonus = %s, extra_bonus = 0 WHERE id = %s",
        (amount, report_id)
    )
    conn.commit()
    conn.close()


# -----------------------------
# 4. СОСТОЯНИЕ ПОЛЬЗОВАТЕЛЕЙ
# -----------------------------

user_states = {}            # кто сейчас пишет отчёт
admin_review_state = {}     # {ADMIN_CHAT_ID: report_id} — ждём текст ревью
admin_finish_state = {}     # {ADMIN_CHAT_ID: report_id} — ждём итоговый бонус

# -----------------------------
# 5. ХЕЛПЕРЫ ДЛЯ КНОПОК
# -----------------------------

def make_admin_keyboard(report_id):
    kb = types.InlineKeyboardMarkup()
    row1 = [
        types.InlineKeyboardButton("🧐 Начать ревью", callback_data=f"report:{report_id}:review"),
        types.InlineKeyboardButton("✅ Миссия завершена", callback_data=f"report:{report_id}:finish"),
    ]
    kb.row(*row1)
    return kb


def format_report_for_admin(report):
    mission = MISSIONS.get(report["mission_num"], {})
    title = mission.get("title", f"Миссия {report['mission_num']}")
    total = report["standard_bonus"] + report["extra_bonus"]
    text = (
        f"📩 *ОТЧЁТ ПО МИССИИ {report['mission_num']}* — {title}\n"
        f"От @{report['username'] or 'без_ника'} (id: {report['user_id']})\n\n"
        f"Комментарий от босса 😎: \n"
        f"Стандартный бонус: {report['standard_bonus']}₽\n"
        f"Доп. бонус: {report['extra_bonus']}₽\n"
        f"Итого: {total}₽\n"
        f"Статус: {report['status']}\n"
    )
    if report["admin_comment"]:
        text += f"\nКомментарий: {report['admin_comment']}"
    return text


def format_status_for_user(report, status_label):
    mission = MISSIONS.get(report["mission_num"], {})
    title = mission.get("title", f"Миссия {report['mission_num']}")
    total = report["standard_bonus"] + report["extra_bonus"]
    text = (
        f"✅ *{status_label} по миссии {report['mission_num']}* — {title}\n\n"
        f"Бонус: {total}₽ (стандартный {report['standard_bonus']}₽"
        f"{' + доп. ' + str(report['extra_bonus']) + '₽' if report['extra_bonus'] else ''})\n"
    )
    if report["admin_comment"]:
        text += f"\nКомментарий: {report['admin_comment']}"
    return text


# -----------------------------
# 6. /start
# -----------------------------
@bot.message_handler(commands=['start'])
def start(message):
    text = (
        "Йоу! Я бот для твоих миссий по блоггингу 🎮\n\n"
        "*Команды:*\n"
        "• `/missions` — список миссий\n"
        "• `миссия <номер>` — открыть миссию\n"
        "• `/report_format` — шаблон отчёта\n"
        "• `/ideas` — записать идею\n"
        "• `/help` — как работает система\n"
        "• `/balance` — сколько бонусов уже принято\n\n"
        "Когда выполняешь миссию — присылай отчёт прямо сюда.\n"
        "В конце напиши: *Готово* или нажми кнопку ✅ Готово."
    )

    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # верхний ряд
    btn_missions = types.KeyboardButton("📋 Миссии")
    btn_report = types.KeyboardButton("🧾 Шаблон отчёта")
    kb.row(btn_missions, btn_report)

    # второй ряд
    btn_ideas = types.KeyboardButton("💡 Идея")
    btn_help = types.KeyboardButton("ℹ️ Помощь")
    kb.row(btn_ideas, btn_help)

    # третий ряд — управление отчётом
    btn_start_report = types.KeyboardButton("📝 Начать отчёт")
    btn_done = types.KeyboardButton("✅ Готово")
    kb.row(btn_start_report, btn_done)

    # четвёртый ряд — баланс
    btn_balance = types.KeyboardButton("💰 Баланс")
    kb.row(btn_balance)

    bot.send_message(message.chat.id, text, reply_markup=kb)

# -----------------------------
# 7. /help
# -----------------------------
@bot.message_handler(commands=['help'])
def help_message(message):
    text = (
        "📘 *Как работает система миссий*\n\n"
        "1️⃣ Выбираешь миссию (`/missions` или `миссия <номер>`).\n"
        "2️⃣ Выполняешь задание.\n"
        "3️⃣ Оформляешь отчёт по шаблону (`/report_format`).\n"
        "4️⃣ Отправляешь материалы и в конце пишешь: *Готово*.\n\n"
        "💸 Бонусы копятся до 6к или двумя выплатами по 3к.\n\n"
        "Пиши своими словами, не формально — важны твои мысли!"
    )
    bot.send_message(message.chat.id, text)


# -----------------------------
# 8. /report_format — шаблон отчёта
# -----------------------------
@bot.message_handler(commands=['report_format'])
def report_format(message):
    text = (
        "🧾 *ШАБЛОН ОТЧЁТА О МИССИИ*\n\n"
        "Это миссия №: ___\n"
        "Название: ___\n"
        "Дата начала: ___\n"
        "Дата завершения: ___\n\n"
        "*Что нужно было сделать:*\n(коротко из задания)\n\n"
        "*Что я сделал(а):*\n(шаги, что пробовал, инструменты)\n\n"
        "*Что получилось:*\n(ссылка, скрин, описание результата)\n\n"
        "*Что было сложно / чему научился(ась):*\n(2–5 предложений)\n\n"
        "*Что хочу сделать дальше:*\n(что улучшить / попробовать)\n\n" 
        "Скопируй этот шаблон в сообщение и заполни. Если еще не нажал *начать миссию*, то не забудь нажать, а потом начинай отчет. После отправки отчета напиши следующим сообщением 'Готово' и отчет отправится (бот напишет, что передал отчет)."
    )
    bot.send_message(message.chat.id, text)


# -----------------------------
# 9. /ideas — идеи
# -----------------------------
@bot.message_handler(commands=['ideas'])
def ideas_info(message):
    bot.reply_to(
        message,
        "💡 Напиши идею форматом:\n\n*идея: твой текст*\n\nЯ сохраню её 😎"
    )


# -----------------------------
# 10. /missions — список миссий
# -----------------------------
@bot.message_handler(commands=['missions'])
def missions_cmd(message):
    text = "📘 *Список доступных миссий:*\n\n"
    for num, m in MISSIONS.items():
        text += f"{num}. {m['title']} — {m['bonus']}₽\n"
    text += "\nНапиши: `миссия <номер>`"
    bot.reply_to(message, text)


# -----------------------------
# 11. /balance — баланс одобренных бонусов
# -----------------------------
@bot.message_handler(commands=['balance'])
def balance_cmd(message):
    total = get_user_balance(message.from_user.id)
    bot.reply_to(message, f"💰 Принято бонусов: *{total}₽*")

# кнопки

@bot.message_handler(func=lambda m: m.text == "📋 Миссии")
def missions_button(message):
    missions_cmd(message)


@bot.message_handler(func=lambda m: m.text == "🧾 Шаблон отчёта")
def report_button(message):
    report_format(message)


@bot.message_handler(func=lambda m: m.text == "💡 Идея")
def idea_button(message):
    ideas_info(message)


@bot.message_handler(func=lambda m: m.text == "ℹ️ Помощь")
def help_button(message):
    help_message(message)


@bot.message_handler(func=lambda m: m.text == "💰 Баланс")
def balance_button(message):
    balance_cmd(message)


@bot.message_handler(func=lambda m: m.text == "📝 Начать отчёт")
def start_report_button(message):
    user_id = message.from_user.id
    state = user_states.get(user_id)

    if not state or "mission" not in state:
        bot.reply_to(message, "Сначала выбери миссию: `миссия <номер>`")
        return

    # начинаем сбор отчёта, очищаем старый буфер
    state["collecting"] = True
    state["buffer"] = []
    bot.reply_to(
        message,
        f"Окей, начинаем отчёт по миссии {state['mission']}.\n"
        "Кидай сюда текст, скрины, видео. В конце нажми *✅ Готово* или напиши 'Готово'."
    )


# Альтернативная текстовая команда
@bot.message_handler(func=lambda m: m.text and m.text.lower().strip() == "начать отчет")
def start_report_text(message):
    start_report_button(message)


@bot.message_handler(func=lambda m: m.text == "✅ Готово")
def done_button(message):
    fake_message = message
    fake_message.text = "Готово"
    collect_report(fake_message)


# -----------------------------
# 12. Выбор миссии "миссия N"
# -----------------------------
@bot.message_handler(func=lambda m: m.text and m.text.lower().startswith("миссия"))
def choose_mission(message):
    parts = message.text.split()
    if len(parts) < 2 or not parts[1].isdigit():
        bot.reply_to(message, "Пиши так: `миссия 3`")
        return

    num = int(parts[1])
    mission = MISSIONS.get(num)

    if not mission:
        bot.reply_to(message, "Такой миссии нет 👀")
        return

    # только выбираем миссию, но не начинаем сбор отчёта
    user_states[message.from_user.id] = {
        "mission": num,
        "collecting": False,
        "buffer": []
    }

    text = (
        f"🔥 *Миссия {num}:* {mission['title']}\n\n"
        f"*Что нужно сделать:*\n{mission['task']}\n\n"
        f"*Бонус:* {mission['bonus']}₽\n\n"
        "Когда будешь готов(а) делать отчёт:\n"
        "• нажми кнопку *📝 Начать отчёт* или напиши 'Начать' — и присылай материалы\n"
        "• можешь пользоваться шаблоном: /report_format\n"
        "• после того, как нажал *Начать отчёт* ты можешь возвращаться и редактировать отчет по этой миссии пока не нажмешь *Готово*.\n"
        "• чтобы отправить отчёт на проверку — нажми *✅ Готово* или напиши 'Готово'"
    )
    bot.reply_to(message, text)


# -----------------------------
# 13. Обработка текстов админа (ревью и финальный бонус)
# -----------------------------
@bot.message_handler(func=lambda m: m.chat.id == ADMIN_CHAT_ID and (
    ADMIN_CHAT_ID in admin_review_state or ADMIN_CHAT_ID in admin_finish_state
))
def handle_admin_text(message):
    chat_id = message.chat.id
    text = message.text.strip()

    # 1) Ревью по миссии
    if chat_id in admin_review_state:
        report_id = admin_review_state.pop(chat_id)

        # сохраняем новое ревью в БД
        set_admin_comment(report_id, text)

        # загружаем свежее состояние отчёта
        report = get_report(report_id)
        if not report:
            bot.send_message(ADMIN_CHAT_ID, "Не нашёл отчёт 🤔")
            return

        mission_num = report["mission_num"]

        # формируем ревью для пользователя
        updated_review = (
            f"🔁 *Босс обновил ревью по миссии {mission_num}*\n\n"
            f"{report['admin_comment']}"
        )

        # отправляем пользователю
        bot.send_message(report["chat_id"], updated_review)

        # сообщение админу
        bot.send_message(ADMIN_CHAT_ID, "Обновлённое ревью отправлено пользователю ✅")
        return

    # 2) Завершение миссии (итоговый бонус)
    if chat_id in admin_finish_state:
        report_id = admin_finish_state.pop(chat_id)
        try:
            bonus = int(text)
        except ValueError:
            bot.send_message(ADMIN_CHAT_ID, "Нужно ввести число, например: 350")
            admin_finish_state[chat_id] = report_id
            return

        set_total_bonus(report_id, bonus)
        update_status(report_id, "accepted")
        report = get_report(report_id)
        if not report:
            bot.send_message(ADMIN_CHAT_ID, "Не нашёл отчёт 🤔")
            return

        mission_num = report["mission_num"]

        user_msg = (
            f"✅ Босс завершил миссию {report['mission_num']}!\n"
            f"Ты получаешь бонус *{bonus}₽* 🎉"
        )
        bot.send_message(report["chat_id"], user_msg)

        bot.send_message(ADMIN_CHAT_ID, f"Миссия #{mission_num} закрыта. Итоговый бонус: {bonus}₽ ✅")


# -----------------------------
# 14. Обработка отчётов от пользователя
# -----------------------------
@bot.message_handler(content_types=['text', 'photo', 'video', 'voice', 'document'])
def collect_report(message):
    user_id = message.from_user.id

    # --- отдельная обработка идей, чтобы они не путались с отчётами ---
    if message.content_type == 'text' and message.text:
        text_lower = message.text.lower().strip()
        if text_lower.startswith("идея:"):
            idea_text = message.text[5:].strip()
            bot.send_message(
                ADMIN_CHAT_ID,
                f"💡 *ИДЕЯ от @{message.from_user.username or message.from_user.first_name}:*\n\n{idea_text}"
            )
            bot.reply_to(message, "Принято! Идея сохранена 💡🔥")
            return

    # --- если это текст "готово" вне отчёта ---
    if message.content_type == 'text' and message.text.lower() == "готово":
        if user_id not in user_states:
            bot.reply_to(message, "❗ Сначала выбери миссию: напиши `миссия <номер>` 🙂")
            return

        if len(user_states[user_id]["buffer"]) == 0:
            bot.reply_to(message, "⚠️ Ты ещё не написал ничего в отчёт! Сначала добавь текст или файл.")
            return

        if not user_states[user_id]["collecting"]:
            bot.reply_to(message, "❗ Чтобы завершить миссию, нажми кнопочку *📝 Начать отчёт*.")
            return

    if user_id not in user_states or not user_states[user_id]["collecting"]:
        return

    if message.content_type == 'text' and message.text.lower() == "готово":
        mission_num = user_states[user_id]["mission"]
        mission = MISSIONS.get(mission_num)
        standard_bonus = mission["bonus"] if mission else 0
        username = message.from_user.username or message.from_user.first_name

        report_id = create_or_update_report(user_id, username, message.chat.id, mission_num, standard_bonus)
        report = get_report(report_id)

        text_parts = []
        for msg in user_states[user_id]["buffer"]:
            if msg.content_type == 'text':
                text_parts.append(msg.text.strip())
        report_body = "\n\n".join(text_parts).strip()

        if not report_body:
            report_body = "_(в отчёте нет текстовой части, только медиа)_"

        mission_title = mission["title"] if mission else f"Миссия {mission_num}"
        total = report["standard_bonus"] + report["extra_bonus"]

        admin_text = (
            f"📩 *ОТЧЁТ ПО МИССИИ {mission_num}* — {mission_title}\n"
            f"От @{username or 'без_ника'} (id: {user_id})\n\n"
            f"{report_body}\n\n"
            f"Комментарий от босса 😎: \n"
            f"Стандартный бонус: {report['standard_bonus']}₽\n"
            f"Доп. бонус: {report['extra_bonus']}₽\n"
            f"Итого: {total}₽\n"
            f"Статус: {report['status']}"
        )

        kb = make_admin_keyboard(report_id)

        bot.send_message(
            ADMIN_CHAT_ID,
            admin_text,
            reply_markup=kb
        )

        bot.reply_to(message, "Готово! Я передал отчёт боссу 👌🔥")
        user_states.pop(user_id)
        return

    user_states[user_id]["buffer"].append(message)


# -----------------------------
# X. Команда /set_status МИССИЯ СТАТУС
# -----------------------------
@bot.message_handler(commands=['set_status'])
def admin_set_status(message):
    if message.from_user.id != ADMIN_CHAT_ID:
        return

    try:
        _, mission_str, status = message.text.split()
        mission_num = int(mission_str)
    except:
        bot.reply_to(message, "Формат: /set_status <миссия> <status>")
        return

    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, chat_id FROM mission_reports WHERE mission_num = %s", (mission_num,))
    rows = cur.fetchall()
    conn.close()

    if not rows:
        bot.reply_to(message, f"Нет отчётов по миссии {mission_num}")
        return

    for report_id, chat_id in rows:
        update_status(report_id, status)
        bot.send_message(chat_id, f"⚠️ Статус миссии {mission_num} изменён боссом: *{status}*")

    bot.reply_to(message, f"Статус обновлён у {len(rows)} отчётов.")


# -----------------------------
# X. Команда /set_bonus МИССИЯ АММУНТ
# -----------------------------
@bot.message_handler(commands=['set_bonus'])
def admin_set_bonus(message):
    if message.from_user.id != ADMIN_CHAT_ID:
        return

    try:
        _, mission_str, bonus_str = message.text.split()
        mission_num = int(mission_str)
        amount = int(bonus_str)
    except:
        bot.reply_to(message, "Формат: /set_bonus <миссия> <рубли>")
        return

    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, chat_id FROM mission_reports WHERE mission_num = %s", (mission_num,))
    rows = cur.fetchall()
    conn.close()

    if not rows:
        bot.reply_to(message, f"Нет отчётов по миссии {mission_num}")
        return

    for report_id, chat_id in rows:
        set_total_bonus(report_id, amount)
        bot.send_message(chat_id, f"💰 Босс изменил бонус по миссии {mission_num}: *{amount}₽*")

    bot.reply_to(message, f"Бонус обновлён у {len(rows)} отчётов.")


# -----------------------------
# X. Обработка лишних сообщений от пользователя
# -----------------------------
@bot.message_handler(func=lambda m: True, content_types=['text'])
def fallback_handler(message):
    user_id = message.from_user.id

    text = message.text.strip().lower()

    if text.startswith("/") or text in ["📋 миссии", "🧾 шаблон отчёта", "💡 идея", "ℹ️ помощь", "💰 баланс"]:
        return

    if text in ["📝 начать отчёт", "✅ готово"]:
        return

    if text.startswith("идея:"):
        return

    if user_id in user_states and user_states[user_id]["collecting"]:
        return

    bot.reply_to(
        message,
        "Я не понял 🤔\n\n"
        "Используй меню внизу или напиши:\n"
        "• `миссия <номер>` чтобы выбрать задание\n"
        "• `идея: текст` чтобы сохранить идею\n"
        "• `/missions`, `/help`, `/report_format`\n\n"
        "Если хочешь отправить отчёт — сначала нажми *📝 Начать отчёт*."
    )


# -----------------------------
# 15. Обработка нажатий кнопок админа
# -----------------------------
@bot.callback_query_handler(func=lambda call: call.data.startswith("report:"))
def handle_report_callback(call):
    if call.from_user.id != ADMIN_CHAT_ID:
        bot.answer_callback_query(call.id, "Эта панель только для босса 😼")
        return

    try:
        _, report_id_str, action = call.data.split(":")
        report_id = int(report_id_str)
    except ValueError:
        bot.answer_callback_query(call.id, "Ошибка данных кнопки")
        return

    report = get_report(report_id)
    if not report:
        bot.answer_callback_query(call.id, "Отчёт не найден")
        return

    mission_num = report["mission_num"]

    if action == "review":
        admin_review_state[ADMIN_CHAT_ID] = report_id
        bot.answer_callback_query(call.id, "Напиши ревью следующим сообщением")
        bot.send_message(
            ADMIN_CHAT_ID,
            f"✍️ Напиши ревью для *миссии #{mission_num}*"
        )

    elif action == "finish":
        admin_finish_state[ADMIN_CHAT_ID] = report_id
        bot.answer_callback_query(call.id, "Введи итоговый бонус числом")
        bot.send_message(
            ADMIN_CHAT_ID,
            f"💰 Введи итоговый бонус за *миссию #{mission_num}* (только число)"
        )

    else:
        bot.answer_callback_query(call.id, "Неизвестное действие")


# -----------------------------
# 16. Запуск
# -----------------------------
if __name__ == "__main__":
    init_db()
    print("Бот запущен...")
    bot.infinity_polling()
