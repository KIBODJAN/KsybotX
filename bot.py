import os
import asyncio
import random
from aiogram import Bot, Dispatcher, Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.client.default import DefaultBotProperties

# 🔐 Твои данные
API_TOKEN = "7535965441:AAHLs_QtIgv8TYB7z7LGQTFiCSMx1kBaD8o"
TON_WALLET = "UQAV3W64G7Db8C2jzPtNFAFleUiwS4JGy4-PC36qlpZ_ziSh"
INVITE_LINK = "https://t.me/+Dl9vygrxopYwMGFi"

# Создание нужной папки
os.makedirs("data/romantic", exist_ok=True)

router = Router()

# 📦 Пакеты
PACKS = {
    "start_pack": ("Стартовый", "1 TON"),
    "yummy_pack": ("Вкусный", "3 TON"),
    "juicy_pack": ("Сочный + VIP", "5 TON")
}

# 🧁 Старт
@router.message(CommandStart())
async def cmd_start(message: Message):
    builder = InlineKeyboardBuilder()
    builder.button(text="🥉 Стартовый", callback_data="start_pack")
    builder.button(text="🥈 Вкусный", callback_data="yummy_pack")
    builder.button(text="🥇 Сочный + VIP", callback_data="juicy_pack")
    builder.button(text="⭐ Купить звёзды", callback_data="buy_stars")
    builder.button(text="🎲 Рандомный приз", callback_data="random_prize")
    builder.button(text="🎁 Участвовать в конкурсе", callback_data="contest")
    builder.adjust(1)

    text = (
        "<b>💎 Добро пожаловать в Элит-клуб наслаждения 💎</b>\n\n"
        "╔════════════════════╗\n"
        "  <b>🍓 Только ты и я…</b>\n"
        "╚════════════════════╝\n\n"
        "👠 Здесь исполняются желания — тихо, дерзко и интимно...\n"
        "📸 Приватные фото, видео, голосовые фантазии\n"
        "💋 Всё, что запрещено — ты получишь здесь\n\n"
        "<b>🎁 Готов сорваться? Выбирай пакет:</b>\n\n"
        "🥉 <b>Стартовый</b> — разогрей фантазию 💭\n"
        "🥈 <b>Вкусный</b> — загляни чуть глубже 😈\n"
        "🥇 <b>Сочный + VIP</b> — без тормозов… без границ 💦\n\n"
        "💸 <b>Оплата: только сеть TON</b>\n"
        f"📥 Кошелёк: <code>{TON_WALLET}</code>\n\n"
        "🌟 <b>Звёзды</b> откроют больше:\n"
        "• 🌃 Ночной чат\n"
        "• 📷 Фото по запросу\n"
        "• 🔞 Доступ к самой интимной части\n\n"
        "🎲 Хочешь азарт? Попробуй <b>рандомный приз</b> за 2 TON\n"
        "🎁 Или участвуй в конкурсе — я выберу лучших 😘"
    )

    await message.answer(text, reply_markup=builder.as_markup(), parse_mode=ParseMode.HTML)

# 💳 Покупка пакета
@router.callback_query(F.data.in_(PACKS.keys()))
async def show_pack(callback: CallbackQuery):
    name, price = PACKS[callback.data]
    builder = InlineKeyboardBuilder()
    builder.button(text="✅ Я оплатил", callback_data=f"paid_{callback.data}")
    builder.adjust(1)

    text = (
        f"╔════════════════════╗\n"
        f"  <b>🔥 Пакет: {name}</b>\n"
        f"╚════════════════════╝\n\n"
        f"💰 Стоимость: <b>{price}</b>\n"
        f"📥 Кошелёк: <code>{TON_WALLET}</code>\n\n"
        f"Ты на пути к удовольствию, которое запомнится надолго…\n"
        f"📸 Там будут фото, которые не попадают в соцсети\n"
        f"🎥 Видео, которые никто не видел\n"
        f"💬 И доступ к моим сокровенным желаниям\n\n"
        f"🔐 Переведи TON и нажми «Я оплатил» — я уже разогрелась 😘\n"
        f"⚠️ Только сеть TON!"
    )
    await callback.message.answer(text, reply_markup=builder.as_markup(), parse_mode=ParseMode.HTML)

# ✅ Я оплатил
@router.callback_query(F.data.startswith("paid_"))
async def after_payment(callback: CallbackQuery):
    await callback.message.answer(
        f"🕐 <b>Проверяю перевод...</b>\n\n"
        f"Ты уже на пороге самого сладкого… 💋\n"
        f"Ещё немного — и я откроюсь тебе полностью\n\n"
        f"🔗 <b>Твоя личная ссылка в приват:</b>\n"
        f"<a href=\"{INVITE_LINK}\">{INVITE_LINK}</a>\n\n"
        f"👮‍♀️ Ожидай подтверждения от администратора\n"
        f"✨ А пока представь, что тебя ждёт внутри...",
        parse_mode=ParseMode.HTML
    )

# ⭐ Купить звезды
@router.callback_query(F.data == "buy_stars")
async def buy_stars(callback: CallbackQuery):
    await callback.message.answer(
        f"⭐ <b>Звёзды — валюта желаний</b>\n\n"
        f"🔓 Они открывают:\n"
        f"• 🌃 Ночной чат (5⭐)\n"
        f"• 📷 Фото по твоему вкусу (7⭐)\n"
        f"• 🎥 Личное видео (10⭐)\n"
        f"• 📢 Реклама твоего канала (15⭐)\n"
        f"• 🔒 Секретная VIP-папка (20⭐)\n\n"
        f"📊 <b>Курс:</b>\n"
        f"10⭐ = 1 TON\n"
        f"25⭐ = 2.2 TON\n"
        f"50⭐ = 4 TON\n"
        f"100⭐ = 7 TON\n\n"
        f"💸 Перевод: <code>{TON_WALLET}</code>\n"
        f"После оплаты — нажми «Я оплатил» или напиши лично 💌",
        parse_mode=ParseMode.HTML
    )

# 🎲 Рандомный приз
@router.callback_query(F.data == "random_prize")
async def random_prize(callback: CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.button(text="✅ Я сыграл", callback_data="played_luck")
    await callback.message.answer(
        f"🎲 <b>Испытай удачу</b> — только для смелых 😏\n\n"
        f"💰 Стоимость участия: <b>2 TON</b>\n"
        f"📥 Кошелёк: <code>{TON_WALLET}</code>\n\n"
        f"✨ Возможные призы:\n"
        f"• 15 звёзд\n"
        f"• 📷 Эксклюзивное фото\n"
        f"• 💎 VIP-доступ на 24 часа\n"
        f"• 😢 Ничего… кроме томного разочарования\n\n"
        f"После оплаты нажми «Я сыграл» — и я раскрою твой приз 🎁",
        reply_markup=builder.as_markup(),
        parse_mode=ParseMode.HTML
    )

@router.callback_query(F.data == "played_luck")
async def played_luck(callback: CallbackQuery):
    prizes = [
        "🎉 Ты выиграл 15 звёзд!",
        "📷 Я пришлю тебе эксклюзивное фото 😘",
        "💎 Ты получаешь VIP на 24 часа!",
        "😢 Увы… сегодня не твой день. Но ты всё равно красавчик!"
    ]
    await callback.message.answer(random.choice(prizes))

# 🎁 Участие в конкурсе
@router.callback_query(F.data == "contest")
async def contest(callback: CallbackQuery):
    await callback.message.answer(
        "🎁 <b>Прими участие в конкурсе</b>\n\n"
        "🔓 Победители получают:\n"
        "• VIP-доступ\n"
        "• Звёзды\n"
        "• Фото и даже личное внимание 😘\n\n"
        "📌 Условия — в описании канала и сторис\n"
        "💗 Не упусти шанс оказаться ближе ко мне...",
        parse_mode=ParseMode.HTML
    )

# 🚀 Запуск бота
async def main():
    bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

# ▶️ Старт
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот остановлен.")
