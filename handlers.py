from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from states import DetectiveStates
from keyboards import (
    get_start_keyboard, get_anxiety_keyboard, get_distortion_keyboard,
    get_threat_keyboard, get_emotion_keyboard, get_body_keyboard,
    get_breathing_keyboard, get_micro_action_keyboard, get_finish_keyboard
)

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    text = (
        "Привет.\n\n"
        "Это 5-минутная интервенция против накрутки.\n"
        "Мы не будем \"успокаиваться\".\n"
        "Мы будем расследовать мысль.\n\n"
        "Если тревога выше 7/10 — делаем короткую версию.\n\n"
        "Готов начать?"
    )
    await message.answer(text, reply_markup=get_start_keyboard())


@router.callback_query(F.data == "start_investigation")
async def start_investigation(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    text = (
        "🔍 ШАГ 1. Место преступления\n\n"
        "Какая мысль запустила тревогу?\n"
        "Напиши её дословно.\n\n"
        "Пример: «Если я ошибусь — все поймут, что я ноль»."
    )
    await callback.message.edit_text(text)
    await state.set_state(DetectiveStates.waiting_thought)


@router.message(DetectiveStates.waiting_thought)
async def process_thought(message: Message, state: FSMContext):
    await state.update_data(thought=message.text)
    text = (
        "Принято.\n\n"
        "Оцени тревогу сейчас от 1 до 10.\n\n"
        "1 — почти спокойно.\n"
        "10 — максимум, трясёт."
    )
    await message.answer(text, reply_markup=get_anxiety_keyboard())
    await state.set_state(DetectiveStates.waiting_anxiety_before)


@router.callback_query(F.data.startswith("anxiety_"), DetectiveStates.waiting_anxiety_before)
async def process_anxiety_before(callback: CallbackQuery, state: FSMContext):
    anxiety = int(callback.data.split("_")[1])
    await state.update_data(anxiety_before=anxiety)

        if anxiety > 7:
        text = (
            "Тревога высокая.\n"
            "Пойдём по ускоренному протоколу.\n\n"
            "🔍 ШАГ 2. Допрос мысли\n\n"
            "Сейчас выберем, КАК именно мозг накручивает.\n\n"
            "Катастрофизация — «Если чуть ошибусь — будет КАТАСТРОФА».\n"
            "Чтение мыслей — «Они точно думают, что я ноль».\n"
            "Персонализация — «Если что-то случилось — это из‑за меня».\n"
            "Всё или ничего — «Либо идеально, либо провал».\n"
            "Предсказание будущего — «Я заранее знаю, что всё пойдёт плохо».\n"
            "Обесценивание позитива — «Хорошее — случайность, плохое — правда».\n"
            "Долженствование — «Я должен всегда быть идеальным / удобным».\n"
            "Эмоциональное доказательство — «Мне страшно → значит, это правда».\n\n"
            "Выбери вариант, который больше всего похож на твою мысль."
        )
        await state.update_data(short_mode=True)
    else:
        text = (
            "🔍 ШАГ 2. Допрос мысли\n\n"
            "Сейчас выберем, КАК именно мозг накручивает.\n\n"
            "Катастрофизация — «Если чуть ошибусь — будет КАТАСТРОФА».\n"
            "Чтение мыслей — «Они точно думают, что я ноль».\n"
            "Персонализация — «Если что-то случилось — это из‑за меня».\n"
            "Всё или ничего — «Либо идеально, либо провал».\n"
            "Предсказание будущего — «Я заранее знаю, что всё пойдёт плохо».\n"
            "Обесценивание позитива — «Хорошее — случайность, плохое — правда».\n"
            "Долженствование — «Я должен всегда быть идеальным / удобным».\n"
            "Эмоциональное доказательство — «Мне страшно → значит, это правда».\n\n"
            "Выбери вариант, который больше всего похож на твою мысль."
        )
        await state.update_data(short_mode=False)


    await callback.message.edit_text(text, reply_markup=get_distortion_keyboard())
    await state.set_state(DetectiveStates.waiting_distortion)
    await callback.answer()


@router.callback_query(F.data.startswith("dist_"), DetectiveStates.waiting_distortion)
async def process_distortion(callback: CallbackQuery, state: FSMContext):
    distortion_map = {
        "dist_catastrophizing": "Катастрофа",
        "dist_mindreading": "Чтение мыслей",
        "dist_blackwhite": "Всё или ничего",
        "dist_fortune": "Предсказание будущего",
        "dist_discount": "Обесценивание хорошего",
        "dist_should": "Долженствование",
    }

    distortion = distortion_map.get(callback.data, "Неизвестно")
    await state.update_data(distortion=distortion)

    text = (
        "Это реальная угроза СЕЙЧАС?\n\n"
        "УГРОЗА: «У меня горит квартира».\n"
        "НЕОПРЕДЕЛЁННОСТЬ: «А вдруг завтра будет пожар?».\n\n"
        "Твоя мысль ближе к чему?"
    )
    await callback.message.edit_text(text, reply_markup=get_threat_keyboard())
    await state.set_state(DetectiveStates.waiting_threat_type)
    await callback.answer()


@router.callback_query(F.data.startswith("threat_"), DetectiveStates.waiting_threat_type)
async def process_threat_type(callback: CallbackQuery, state: FSMContext):
    threat_type = callback.data.split("_")[1]
    await state.update_data(threat_type=threat_type)

    if threat_type == "uncertainty":
        text = (
            "Что здесь неизвестно?\n\n"
            "Пример: мысль «Я провалю экзамен».\n"
            "Неизвестно: «Какой будет результат».\n\n"
            "Напиши коротко: что именно не знаешь?"
        )
        await callback.message.edit_text(text)
        await state.set_state(DetectiveStates.waiting_unknown)
    else:
        data = await state.get_data()
        short_mode = data.get('short_mode', False)

        if short_mode:
            text = (
                "🔍 ШАГ 3. Факт ПРОТИВ мысли\n\n"
                "Факты ПРОТИВ — это реальные события,\n"
                "которые показывают, что всё не так страшно.\n\n"
                "Примеры:\n"
                "• «У меня 5 клиентов на этой неделе»\n"
                "• «Я ответил на все сообщения»\n"
                "• «Клиент сказал спасибо»\n\n"
                "Напиши 1 факт ПРОТИВ твоей мысли."
            )
            await callback.message.edit_text(text)
            await state.set_state(DetectiveStates.waiting_evidence_against)
        else:
            text = (
                "🔍 ШАГ 3. Факт ЗА мысль\n\n"
                "Факты ЗА — это реальные события,\n"
                "которые поддерживают твою тревожную мысль.\n\n"
                "Примеры:\n"
                "• «2 дня не было новых клиентов»\n"
                "• «Я забыл ответить на сообщение»\n"
                "• «Клиент был недоволен»\n\n"
                "Напиши 1 факт ЗА твою мысль."
            )
            await callback.message.edit_text(text)
            await state.set_state(DetectiveStates.waiting_evidence_for)

    await callback.answer()


@router.message(DetectiveStates.waiting_unknown)
async def process_unknown(message: Message, state: FSMContext):
    await state.update_data(unknown=message.text)
    data = await state.get_data()
    short_mode = data.get('short_mode', False)

    if short_mode:
        text = (
            "🔍 ШАГ 3. Факт ПРОТИВ мысли\n\n"
            "Факты ПРОТИВ — это реальные события,\n"
            "которые показывают, что всё не так страшно.\n\n"
            "Примеры:\n"
            "• «У меня 5 клиентов на этой неделе»\n"
            "• «Я ответил на все сообщения»\n"
            "• «Клиент сказал спасибо»\n\n"
            "Напиши 1 факт ПРОТИВ."
        )
        await message.answer(text)
        await state.set_state(DetectiveStates.waiting_evidence_against)
    else:
        text = (
            "🔍 ШАГ 3. Факт ЗА мысль\n\n"
            "Факты ЗА — это реальные события,\n"
            "которые поддерживают твою тревожную мысль.\n\n"
            "Примеры:\n"
            "• «2 дня не было новых клиентов»\n"
            "• «Я забыл ответить на сообщение»\n"
            "• «Клиент был недоволен»\n\n"
            "Напиши 1 факт ЗА твою мысль."
        )
        await message.answer(text)
        await state.set_state(DetectiveStates.waiting_evidence_for)


@router.message(DetectiveStates.waiting_evidence_for)
async def process_evidence_for(message: Message, state: FSMContext):
    await state.update_data(evidence_for=message.text)
    text = (
        "🔍 Теперь факт ПРОТИВ мысли\n\n"
        "Примеры фактов ПРОТИВ:\n"
        "• «У меня 5 клиентов на этой неделе»\n"
        "• «Я ответил на все сообщения»\n"
        "• «Клиент сказал спасибо»\n\n"
        "Напиши 1 факт ПРОТИВ."
    )
    await message.answer(text)
    await state.set_state(DetectiveStates.waiting_evidence_against)


@router.message(DetectiveStates.waiting_evidence_against)
async def process_evidence_against(message: Message, state: FSMContext):
    await state.update_data(evidence_against=message.text)
    data = await state.get_data()
    short_mode = data.get('short_mode', False)

    if short_mode:
        text = (
            "🔍 ШАГ 4. Новая мысль\n\n"
            "Пример:\n"
            "Было: «Я полный неудачник».\n"
            "Стало: «У меня есть ошибки, но я стараюсь и учусь».\n\n"
            "Напиши свою более честную и спокойную мысль.\n"
            "Не «всё супер», а реалистично."
        )
        await message.answer(text)
        await state.set_state(DetectiveStates.waiting_reframed)
    else:
        text = (
            "Насколько это вероятно? (0–100%)\n\n"
            "Пример: «Меня точно уволят завтра».\n"
            "Если до этого тебя никогда не увольняли,\n"
            "может быть это не 100%, а, например, 20–30%.\n\n"
            "Напиши число от 0 до 100."
        )
        await message.answer(text)
        await state.set_state(DetectiveStates.waiting_probability)


@router.message(DetectiveStates.waiting_probability)
async def process_probability(message: Message, state: FSMContext):
    try:
        probability = int(message.text)
        if 0 <= probability <= 100:
            await state.update_data(probability=probability)
            text = (
                "Если это всё-таки случится — насколько это плохо? (0–10)\n\n"
                "Пример: «Уволят».\n"
                "Это неприятно, но не конец жизни.\n"
                "Можно оценить как 7/10, а не 10/10.\n\n"
                "Напиши число от 0 до 10."
            )
            await message.answer(text)
            await state.set_state(DetectiveStates.waiting_impact)
        else:
            await message.answer("Пожалуйста, введи число от 0 до 100.")
    except ValueError:
        await message.answer("Пожалуйста, введи число от 0 до 100.")


@router.message(DetectiveStates.waiting_impact)
async def process_impact(message: Message, state: FSMContext):
    try:
        impact = int(message.text)
        if 0 <= impact <= 10:
            await state.update_data(impact=impact)
            text = (
                "Теперь как детектив.\n"
                "Посмотрев на все улики:\n\n"
                "Какой вердикт ты бы вынес?\n\n"
                "Примеры:\n"
                "• «Недостаточно улик, чтобы считать это катастрофой»\n"
                "• «Мысль преувеличена, но риск есть»\n"
                "• «Это неприятно, но не конец»\n\n"
                "Напиши свой вердикт."
            )
            await message.answer(text)
            await state.set_state(DetectiveStates.waiting_verdict)
        else:
            await message.answer("Пожалуйста, введи число от 0 до 10.")
    except ValueError:
        await message.answer("Пожалуйста, введи число от 0 до 10.")


@router.message(DetectiveStates.waiting_verdict)
async def process_verdict(message: Message, state: FSMContext):
    await state.update_data(verdict=message.text)
    text = (
        "🔍 ШАГ 4. Новая мысль\n\n"
        "Пример:\n"
        "Было: «Я точно провалюсь».\n"
        "Стало: «Мне тревожно, но я готовлюсь и могу справиться».\n\n"
        "Теперь сформулируй свою более реалистичную мысль."
    )
    await message.answer(text)
    await state.set_state(DetectiveStates.waiting_reframed)


@router.message(DetectiveStates.waiting_reframed)
async def process_reframed(message: Message, state: FSMContext):
    await state.update_data(reframed=message.text)
    text = (
        "Насколько ты веришь в новую мысль? (0–100%)\n\n"
        "0 — совсем не верю.\n"
        "100 — верю полностью.\n\n"
        "Напиши число."
    )
    await message.answer(text)
    await state.set_state(DetectiveStates.waiting_belief)


@router.message(DetectiveStates.waiting_belief)
async def process_belief(message: Message, state: FSMContext):
    try:
        belief = int(message.text)
        if 0 <= belief <= 100:
            await state.update_data(belief=belief)
            text = (
                "Кроме тревоги, что ты ещё чувствуешь?\n\n"
                "Например: раздражение, грусть, усталость, стыд…"
            )
            await message.answer(text, reply_markup=get_emotion_keyboard())
            await state.set_state(DetectiveStates.waiting_other_emotion)
        else:
            await message.answer("Пожалуйста, введи число от 0 до 100.")
    except ValueError:
        await message.answer("Пожалуйста, введи число от 0 до 100.")


@router.callback_query(F.data.startswith("emotion_"), DetectiveStates.waiting_other_emotion)
async def process_other_emotion(callback: CallbackQuery, state: FSMContext):
    emotion_map = {
        "emotion_irritation": "Раздражение",
        "emotion_sadness": "Грусть",
        "emotion_fatigue": "Усталость",
        "emotion_shame": "Стыд",
        "emotion_other": "Другое"
    }

    emotion = emotion_map.get(callback.data, "Неизвестно")
    await state.update_data(other_emotion=emotion)

    text = (
        "🔍 ШАГ 5. Возврат контроля\n\n"
        "Что ты реально контролируешь прямо сейчас?\n\n"
        "Примеры:\n"
        "• «Могу доделать одну задачу»\n"
        "• «Могу написать человеку»\n"
        "• «Могу лечь спать вовремя»\n\n"
        "Напиши коротко."
    )
    await callback.message.edit_text(text)
    await state.set_state(DetectiveStates.waiting_control)
    await callback.answer()


@router.message(DetectiveStates.waiting_control)
async def process_control(message: Message, state: FSMContext):
    await state.update_data(control_direct=message.text)
    text = (
        "Где в теле тревога сильнее всего?\n\n"
        "Выбери область."
    )
    await message.answer(text, reply_markup=get_body_keyboard())
    await state.set_state(DetectiveStates.waiting_body_location)


@router.callback_query(F.data.startswith("body_"), DetectiveStates.waiting_body_location)
async def process_body_location(callback: CallbackQuery, state: FSMContext):
    body_map = {
        "body_chest": "Грудь",
        "body_stomach": "Живот",
        "body_throat": "Горло",
        "body_other": "Другое"
    }

    body = body_map.get(callback.data, "Неизвестно")
    await state.update_data(body_location=body)

    text = (
        "Сделай 3 медленных выдоха.\n"
        "На каждый выдох — расслабь тело там, где больше всего зажато.\n\n"
        "Нажми «Сделал», когда будешь готов."
    )
    await callback.message.edit_text(text, reply_markup=get_breathing_keyboard())
    await state.set_state(DetectiveStates.waiting_breathing)
    await callback.answer()


@router.callback_query(F.data == "breathing_done", DetectiveStates.waiting_breathing)
async def process_breathing(callback: CallbackQuery, state: FSMContext):
    text = (
        "Выбери микро-действие на 5–10 минут.\n\n"
        "Важно: небольшое и выполнимое прямо сегодня."
    )
    await callback.message.edit_text(text, reply_markup=get_micro_action_keyboard())
    await state.set_state(DetectiveStates.waiting_micro_action)
    await callback.answer()


@router.callback_query(F.data.startswith("action_"), DetectiveStates.waiting_micro_action)
async def process_micro_action(callback: CallbackQuery, state: FSMContext):
    action_map = {
        "action_write": "Написать поддерживающему человеку",
        "action_task": "Сделать одну маленькую задачу",
        "action_walk": "Выйти на прогулку",
        "action_work": "Поработать 15 минут",
        "action_control": "Записать 3 вещи под контролем"
    }

    if callback.data == "action_custom":
        text = "Напиши своё действие на 5–10 минут."
        await callback.message.edit_text(text)
        await state.set_state(DetectiveStates.waiting_custom_action)
    else:
        action = action_map.get(callback.data, "Неизвестно")
        await state.update_data(micro_action=action)
        text = (
            "Из-за тревоги ты сегодня НЕ будешь делать что?\n\n"
            "Пример: «Не буду час гуглить симптомы»\n"
            "или «Не буду проверять мессенджер каждые 2 минуты»."
        )
        await callback.message.edit_text(text)
        await state.set_state(DetectiveStates.waiting_no_compulsion)

    await callback.answer()


@router.message(DetectiveStates.waiting_custom_action)
async def process_custom_action(message: Message, state: FSMContext):
    await state.update_data(micro_action=message.text)
    text = (
        "Из-за тревоги ты сегодня НЕ будешь делать что?\n\n"
        "Пример: «Не буду час гуглить симптомы»\n"
        "или «Не буду проверять мессенджер каждые 2 минуты»."
    )
    await message.answer(text)
    await state.set_state(DetectiveStates.waiting_no_compulsion)


@router.message(DetectiveStates.waiting_no_compulsion)
async def process_no_compulsion(message: Message, state: FSMContext):
    await state.update_data(no_compulsion=message.text)
    text = (
        "Ещё раз оцени тревогу сейчас (1–10).\n\n"
        "1 — почти спокойно.\n"
        "10 — максимум."
    )
    await message.answer(text, reply_markup=get_anxiety_keyboard())
    await state.set_state(DetectiveStates.waiting_anxiety_after)


@router.callback_query(F.data.startswith("anxiety_"), DetectiveStates.waiting_anxiety_after)
async def process_anxiety_after(callback: CallbackQuery, state: FSMContext):
    anxiety_after = int(callback.data.split("_")[1])
    await state.update_data(anxiety_after=anxiety_after)

    data = await state.get_data()
    anxiety_before = data.get('anxiety_before', 0)

    text = (
        f"Было: {anxiety_before}/10\n"
        f"Стало: {anxiety_after}/10\n\n"
        "Ты не убежал от мысли.\n"
        "Ты её проверил как детектив.\n\n"
        "Если бы этой мысли сейчас не было —\n"
        "что бы ты делал?"
    )
    await callback.message.edit_text(text)
    await state.set_state(DetectiveStates.waiting_bridge_action)
    await callback.answer()


@router.message(DetectiveStates.waiting_bridge_action)
async def process_bridge_action(message: Message, state: FSMContext):
    await state.update_data(bridge_action=message.text)

    text = (
        "✅ Сессия завершена.\n\n"
        "Ты сделал важную работу.\n"
        "Это навык, он усиливается с практикой.\n\n"
        "Когда захочешь ещё одну сессию — нажми /start."
    )
    await message.answer(text, reply_markup=get_finish_keyboard())
    await state.clear()


@router.callback_query(F.data == "finish")
async def finish_session(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await cmd_start(callback.message, state)
    await callback.answer()


def register_handlers(dp):
    dp.include_router(router)

