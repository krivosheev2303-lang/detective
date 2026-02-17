from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

def get_start_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Начать расследование", callback_data="start_investigation")]
    ])

def get_anxiety_keyboard():
    buttons = []
    row = []
    for i in range(1, 11):
        row.append(InlineKeyboardButton(text=str(i), callback_data=f"anxiety_{i}"))
        if i % 5 == 0:
            buttons.append(row)
            row = []
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_distortion_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Катастрофизация", callback_data="dist_catastrophizing")],
        [InlineKeyboardButton(text="Чтение мыслей", callback_data="dist_mindreading")],
        [InlineKeyboardButton(text="Персонализация", callback_data="dist_personalization")],
        [InlineKeyboardButton(text="Всё или ничего", callback_data="dist_blackwhite")],
        [InlineKeyboardButton(text="Предсказание будущего", callback_data="dist_fortune")],
        [InlineKeyboardButton(text="Обесценивание позитива", callback_data="dist_discount")],
        [InlineKeyboardButton(text="Долженствование", callback_data="dist_should")],
        [InlineKeyboardButton(text="Эмоциональное доказательство", callback_data="dist_emotional")]
    ])

def get_threat_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Реальная угроза", callback_data="threat_real")],
        [InlineKeyboardButton(text="Неопределённость", callback_data="threat_uncertainty")]
    ])

def get_emotion_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Раздражение", callback_data="emotion_irritation")],
        [InlineKeyboardButton(text="Грусть", callback_data="emotion_sadness")],
        [InlineKeyboardButton(text="Усталость", callback_data="emotion_fatigue")],
        [InlineKeyboardButton(text="Стыд", callback_data="emotion_shame")],
        [InlineKeyboardButton(text="Другое", callback_data="emotion_other")]
    ])

def get_body_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Грудь", callback_data="body_chest")],
        [InlineKeyboardButton(text="Живот", callback_data="body_stomach")],
        [InlineKeyboardButton(text="Горло", callback_data="body_throat")],
        [InlineKeyboardButton(text="Другое", callback_data="body_other")]
    ])

def get_breathing_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Сделал", callback_data="breathing_done")]
    ])

def get_micro_action_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Написать поддерживающему человеку", callback_data="action_write")],
        [InlineKeyboardButton(text="Сделать одну маленькую задачу", callback_data="action_task")],
        [InlineKeyboardButton(text="Выйти на прогулку", callback_data="action_walk")],
        [InlineKeyboardButton(text="Поработать 15 минут", callback_data="action_work")],
        [InlineKeyboardButton(text="Записать 3 вещи под контролем", callback_data="action_control")],
        [InlineKeyboardButton(text="Своё действие", callback_data="action_custom")]
    ])

def get_finish_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Завершить", callback_data="finish")]
    ])