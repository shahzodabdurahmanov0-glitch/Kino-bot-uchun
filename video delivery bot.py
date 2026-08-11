import json
import logging
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Bu qiymatlarni muhit o'zgaruvchisi sifatida bering, kodga to'g'ridan-to'g'ri yozmang.
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "YOUR_TELEGRAM_BOT_TOKEN")
CHANNEL_ID = int(os.environ.get("CHANNEL_ID", "0"))  # ombor kanal ID'si, masalan: -1001234567890
ADMIN_ID = int(os.environ.get("ADMIN_ID", "0"))  # sizning shaxsiy Telegram user ID'ingiz

# Tizerlar joylanadigan ochiq kanalning havolasi (masalan https://t.me/mening_tizer_kanalim)
TEASER_CHANNEL_LINK = os.environ.get("TEASER_CHANNEL_LINK", "https://t.me/YOUR_TEASER_CHANNEL")

MAP_FILE = "video_map.json"


def load_map() -> dict:
    if os.path.exists(MAP_FILE):
        with open(MAP_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_map(data: dict):
    with open(MAP_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Salom! Menga video kodini yuboring, men sizga o'sha videoni jo'nataman.\n\n"
        f"Kodni bilmasangiz, kanalimizga o'ting — u yerda kodlar bor: {TEASER_CHANNEL_LINK}"
    )


async def list_videos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admin uchun: /list — barcha bog'langan raqamlarni ko'rsatadi."""
    if update.effective_user.id != ADMIN_ID:
        return
    data = load_map()
    if not data:
        await update.message.reply_text("Hozircha hech qanday video bog'lanmagan.")
        return
    text = "\n".join(f"{num} -> xabar ID {mid}" for num, mid in sorted(data.items()))
    await update.message.reply_text(text)


async def handle_admin_forward(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admin kanaldan videoni botga forward qilganda ishga tushadi."""
    msg = update.message
    if update.effective_user.id != ADMIN_ID:
        return
    if not msg.forward_from_chat or msg.forward_from_chat.id != CHANNEL_ID:
        await msg.reply_text("Bu xabar belgilangan kanaldan forward qilinmagan.")
        return

    context.user_data["pending_message_id"] = msg.forward_from_message_id
    await msg.reply_text(
        f"Bu videoga qaysi raqamni bog'laymiz? (kanal xabar ID: {msg.forward_from_message_id})\n"
        "Raqamni oddiy xabar sifatida yuboring."
    )


async def handle_text_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admin uchun raqam biriktirish, foydalanuvchi uchun video so'rash — bittasi ishlaydi."""
    user_id = update.effective_user.id
    text = update.message.text.strip()

    # Admin hozirgina bir videoni forward qilgan va endi unga raqam belgilamoqchi
    if user_id == ADMIN_ID and context.user_data.get("pending_message_id") is not None:
        data = load_map()
        data[text] = context.user_data["pending_message_id"]
        save_map(data)
        context.user_data["pending_message_id"] = None
        await update.message.reply_text(f"✅ {text}-raqam ushbu videoga bog'landi.")
        return

    # Oddiy foydalanuvchi so'rovi
    data = load_map()
    if text not in data:
        await update.message.reply_text(
            "Bunday kodli video topilmadi.\n\n"
            f"To'g'ri kodlarni kanalimizda ko'rishingiz mumkin: {TEASER_CHANNEL_LINK}"
        )
        return

    await context.bot.copy_message(
        chat_id=update.effective_chat.id,
        from_chat_id=CHANNEL_ID,
        message_id=data[text],
    )


def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("list", list_videos))
    app.add_handler(MessageHandler(
        filters.FORWARDED & (filters.VIDEO | filters.Document.ALL),
        handle_admin_forward,
    ))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_message))

    # Render kabi bulutli xosting bu o'zgaruvchini avtomatik beradi — shunga qarab
    # bot qaysi rejimda ishga tushishini o'zi aniqlaydi.
    external_url = os.environ.get("RENDER_EXTERNAL_URL")
    if external_url:
        # Bulutda: webhook rejimi — kompyuter yoqiq turishi shart emas, 24/7 ishlaydi
        port = int(os.environ.get("PORT", 8443))
        app.run_webhook(
            listen="0.0.0.0",
            port=port,
            url_path=BOT_TOKEN,
            webhook_url=f"{external_url}/{BOT_TOKEN}",
        )
    else:
        # Lokal kompyuterda sinab ko'rish uchun: oddiy polling rejimi
        app.run_polling()


if __name__ == "__main__":
    main()
