import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from dotenv import load_dotenv

# API kalitlarini yuklash
load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not TOKEN:
    raise ValueError("Bot tokeni topilmadi! Iltimos, .env faylda TOKENni tekshiring.")

# Bot va dispatcher
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Muammo turlari uchun tugmalar
muammo_tugmalar = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="♻ Noqonuniy chiqindilar", callback_data="chiqindilar")],
    [InlineKeyboardButton(text="💧 Suvning ifloslanishi", callback_data="suv_iflos")],
    [InlineKeyboardButton(text="🚱 Suv tanqisligi", callback_data="suv_tanqis")],
    [InlineKeyboardButton(text="🌳 Daraxtlarning kesilishi", callback_data="daraxt_kesish")],
    [InlineKeyboardButton(text="🦉 Hayvonlarga zarar yetkazish", callback_data="hayvonlar")],
    [InlineKeyboardButton(text="🌍 Boshqa muammo", callback_data="boshqa")]
])

# /start komandasi
@dp.message(Command("start"))
async def start_xabar(message: types.Message):
    await message.answer(
        "🌱 *Salom! Bu EcoLegal bot!* 🌍\n\n"
        "Siz ekologik muammolar bo‘yicha murojaat qilishingiz mumkin:\n"
        "✅ *Rasm yoki video yuborish*\n"
        "✅ *Joylashuvingizni ulashish*\n"
        "✅ *Ekologik qonunlar bo‘yicha ma’lumot olish*\n\n"
        "Savollaringiz bo‘lsa, yozib yuboring!", parse_mode="Markdown"
    )

# Rasm yoki video qabul qilish
@dp.message(lambda message: message.photo or message.video)
async def media_qabul_qilish(message: types.Message):
    await message.answer("📌 *Bu qanday muammo?* Iltimos, tanlang:", reply_markup=muammo_tugmalar, parse_mode="Markdown")

# Joylashuv qabul qilish
@dp.message(lambda message: message.location)
async def lokatsiya_qabul_qilish(message: types.Message):
    latitude = message.location.latitude
    longitude = message.location.longitude
    await message.answer(f"📍 *Joylashuv qabul qilindi!*\n\nKenglik: {latitude}\nUzunlik: {longitude}", parse_mode="Markdown")

# Tugmalar bosilganda javob berish
@dp.callback_query()
async def tugma_bosildi(callback_query: types.CallbackQuery):
    muammo_nomi = {
        "chiqindilar": "♻ Noqonuniy chiqindilar",
        "suv_iflos": "💧 Suvning ifloslanishi",
        "suv_tanqis": "🚱 Suv tanqisligi",
        "daraxt_kesish": "🌳 Daraxtlarning kesilishi",
        "hayvonlar": "🦉 Hayvonlarga zarar yetkazish",
        "boshqa": "🌍 Boshqa muammo"
    }
    tanlangan_muammo = muammo_nomi.get(callback_query.data, "Noma'lum muammo")
    await callback_query.message.answer(f"✅ *Rahmat! Siz '{tanlangan_muammo}' muammosi haqida ma’lumot berdingiz.*\nUni tekshirib chiqamiz.", parse_mode="Markdown")
    await bot.answer_callback_query(callback_query.id)

# Eng ko‘p beriladigan 20 ta ekologik huquqiy savollar va javoblar
savol_javoblar = {
    "daraxt kesish": "🌳 MJtK 79-modda: Ruxsatsiz daraxt kesish 5 mln so‘mgacha jarima yoki 15 sutkagacha qamoq.",
    "chiqindilar": "🚯 MJtK 87-modda: Chiqindilarni noqonuniy tashlash 10 mln so‘mgacha jarima.",
    "suv ifloslanishi": "💧 MJtK 90-modda: Suv ifloslantirilsa, 10 mln so‘mgacha jarima yoki faoliyat to‘xtatilishi mumkin.",
    "hayvonlarni o‘ldirish": "🦉 Jinoyat kodeksi 202-modda: Noqonuniy ov qilish 50 mln so‘mgacha jarima yoki 3 yil qamoq.",
    "havo ifloslanishi": "🌫 MJtK 91-modda: Havoni ifloslantirgan shaxslarga 30 mln so‘mgacha jarima.",
    "yerning ifloslanishi": "🌎 MJtK 94-modda: Qishloq xo‘jaligi yerlarini ifloslantirish 15 mln so‘mgacha jarima.",
    "plastik chiqindilar": "♻ Plastik chiqindilarni noqonuniy tashlash 5 mln so‘mgacha jarima yoki 10 sutkagacha qamoq.",
    "suv tanqisligi": "🚱 Suvni noqonuniy ishlatish 10 mln so‘mgacha jarima yoki suv ta’minotidan uzish mumkin.",
    "yovvoyi hayvonlar": "🐾 Ruxsatsiz yovvoyi hayvonlarni ovlash 30 mln so‘mgacha jarima yoki 3 yil qamoq.",
    "elektron chiqindilar": "⚡ Elektron chiqindilarni noqonuniy yo‘q qilish 10 mln so‘mgacha jarima.",
}
# Har xil savollarga mos javob berish
@dp.message()
async def ekologik_javob(message: types.Message):
    savol = message.text.lower()
    for kalit_soz, javob in savol_javoblar.items():
        if kalit_soz in savol:
            await message.answer(javob)
            return
    await message.answer("❌ *Kechirasiz, bu haqda aniq ma’lumot topa olmadim.*\nIltimos, rasmiy manbalarni tekshiring.", parse_mode="Markdown")

# Botni ishga tushirish
async def main():
    print("🤖 Bot ishga tushdi!")
    await dp.start_polling(bot)

asyncio.run(main())
from keep_alive import keep_alive
import telebot
import os

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

keep_alive()  # Flask serverni ishga tushiramiz

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Bot ishlayapti!")

bot.polling()