import os
import logging
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import FSInputFile
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiohttp import ClientSession
from pathlib import Path

# === НАСТРОЙКИ ===
TOKEN = "7535965441:AAHLs_QtIgv8TYB7z7LGQTFiCSMx1kBaD8o"
TON_WALLET = "UQAV3W64G7Db8C2jzPtNFAFleUiwS4JGy4-PC36qlpZ_ziSh"
TON_API_KEY = "AFQZX3V5SD7FNIIAAAABYTAHKIUWZYRRNILLRGA5HPUYMX2QWGBLOKYQS72KKE6XPINAIHY"

PRICES = {
    "start": 1,
    "tasty": 3,
    "juicy": 5,
}

CONTENT_DIR = Path("data/romantic")
os.makedirs(CONTENT_DIR, exist_ok=True)

# === НАСТРОЙКА БОТА ===
logging.basicConfig(level=logging.INFO)
bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

# === КОМАНДА /start ===
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    kb = [
        [types.KeyboardButton(text="🥉 Стартовый — 1 TON")],
        [types.KeyboardButton(text="🥈 Вкусный — 3 TON")],
        [types.KeyboardButton(text="🥇 Сочный — 5 TON")],
    ]
    await message.answer(
        "Привет 😘 Я — Ксюша18+.\nВыбери один из пакетов, чтобы получить 🔥 контент.\nОплата только через TON (сеть TON):",
        reply_markup=types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True),
    )

# === ХЭНДЛЕРЫ ДЛЯ ПАКЕТОВ ===
@dp.message(F.text.contains("Стартовый"))
async def start_pack(msg: types.Message):
    await send_preview_and_pay(msg, "start")

@dp.message(F.text.contains("Вкусный"))
async def tasty_pack(msg: types.Message):
    await send_preview_and_pay(msg, "tasty")

@dp.message(F.text.contains("Сочный"))
async def juicy_pack(msg: types.Message):
    await send_preview_and_pay(msg, "juicy")

# === ПОКАЗ ПРЕВЬЮ + ИНСТРУКЦИИ ===
async def send_preview_and_pay(msg: types.Message, pack):
    preview_files = sorted(CONTENT_DIR.glob("*.jpg"))
    if not preview_files:
        await msg.answer("Пока нет фото в папке 🥺")
        return

    preview = FSInputFile(preview_files[0])
    await msg.answer_photo(preview, caption=f"Это превью 🔥 пакета '{pack}'")

    await msg.answer(
        f"💳 Стоимость: <b>{PRICES[pack]} TON</b>\n"
        f"Отправь <b>ровно {PRICES[pack]} TON</b> на мой TON-кошелек:\n"
        f"<code>{TON_WALLET}</code>\n\n"
        f"После перевода — нажми кнопку 'Я оплатил ✅'",
        reply_markup=types.ReplyKeyboardMarkup(
            keyboard=[[types.KeyboardButton(text=f"Я оплатил ✅ {pack}")]],
            resize_keyboard=True,
        ),
    )

# === ПРОВЕРКА ОПЛАТЫ ===
@dp.message(F.text.startswith("Я оплатил ✅"))
async def check_payment(msg: types.Message):
    pack = msg.text.split("✅")[-1].strip()
    ton_amount = PRICES.get(pack)
    user_id = msg.from_user.id

    await msg.answer("🔄 Проверяю оплату через TON, подожди...")

    async with ClientSession() as session:
        url = f"https://tonapi.io/v2/blockchain/accounts/{TON_WALLET}/transactions"
        headers = {"Authorization": f"Bearer {TON_API_KEY}"}
        async with session.get(url, headers=headers) as resp:
            data = await resp.json()

    for tx in data.get("transactions", []):
        if tx["in_msg"].get("source") and float(tx["in_msg"].get("value", 0)) / 10**9 >= ton_amount:
            await msg.answer("✅ Оплата найдена! Получай свои фотки 😈")
            await send_package_content(msg)
            return

    await msg.answer("❌ Оплата не найдена. Убедись, что ты отправил правильную сумму и попробуй позже.")

# === ВЫДАЧА КОНТЕНТА ===
async def send_package_content(msg: types.Message):
    files = sorted(CONTENT_DIR.glob("*"))
    if not files:
        await msg.answer("⚠️ Контент пока не загружен.")
        return
    for file in files:
        if file.suffix in [".jpg", ".jpeg", ".png"]:
            await msg.answer_photo(FSInputFile(file))
        elif file.suffix in [".mp4", ".mov"]:
            await msg.answer_video(FSInputFile(file))

# === ЗАПУСК ===
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
