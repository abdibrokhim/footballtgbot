# without Django

from telegram import (
    Update,
    KeyboardButton,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    InlineKeyboardMarkup,
    InlineKeyboardButton,

)

from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    filters,
    MessageHandler,

)

import logging
import scraper

from warnings import filterwarnings
from telegram.warnings import PTBUserWarning

filterwarnings(action="ignore", message=r".*CallbackQueryHandler", category=PTBUserWarning)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)

TELEGRAM_BOT_TOKEN = '5499476254:AAH2kCbL3ZZ8o70ra0D-yCJxMiDtVc8XGbA'
CHANNEL_LINK = 'https://t.me/prmngr'
CHANNEL_USERNAME = '@prmngr'

_bots = """
🤖 Bizning Botlar:
    🤖 @thesaver_bot
    🤖 @insta_downder_bot
    🤖 @usellbuybot
    🤖 @musicfindmebot (yengi versiya)
    🤖 @anonyiobot
    🤖 @tiktoknowater_bot (yengi versiya)
    🤖 @music_recognizerBot
    🤖 @tiktokwatermark_removerBot
    🤖 @RealTimeFootballTable_bot
    
📞 Contact: @abdibrokhim
📞 Contact: @contactdevsbot

📢 Channel: @prmngr

👻 Developer: @abdibrokhim
"""

_ads = """
🗣 Biz bilan bog\'lanish uchun:
    🤖 @contactdevsbot
    👻 @abdibrokhim
    
🗣 Bizning kanal: @prmngr

🗣 Reklama: @prmngr
🗣 Yangiliklar: @prmngr

🗣 Xullas hamma narsa shetda, krurasila 💩: @prmngr
"""

_about = """
🌝 Bu Bot orqali siz Football o'yinlari haqida ma\'lumot olishingiz mumkin /football!

🗣 "Command"lar xaqida to\'liq ma\'lumot olish uchun /cmd buyrug\'ini yuboring

🗣 Taklif, murojat, reklama va xokazo, /ads buyrug\'ini yuboring

🗣 Barcha Botlarimiz haqida to\'liq ma\'lumot olish uchun, /bots buyrug\'ini yuboring

🗣 Kanalimizga a'zo bo'ling: @prmngr
"""

_commands = """
🤖 /start - Botni ishga tushirishh️ 

🤖 /menu - Bosh Menu

🤖 /football - O'yinlar haqida ma'lumot olish 

🤖 /doc - Bot haqida ma\'lumot

🤖 /ads - Reklama va Takliflar

🤖 /bots - Bizning botlarimiz

🤖 /cmd - Barcha buyruqlar

🤖 /end - Botni to\'xtatish
"""

(MAIN) = range(1)


async def doc_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(text=_about)


async def cmd_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(text=_commands)


async def ads_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(text=_ads)


async def bots_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(text=_bots)


async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton('↗️ Kanalga go', url=CHANNEL_LINK)]])

    await update.message.reply_text("Assalomu alaykum, {}!".format(user.first_name))
    await update.message.reply_text(
        "Botga xush kelibsiz\n\nBotdan foydalanish uchun /menu bosing\n\n⬇️ Kanalimizga obuna bo'ling! ⬇️",
        reply_markup=reply_markup)


async def menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buttons = [
        [
            KeyboardButton(text="⚽️ Football o'yinlari", ),
        ],
    ]
    reply_markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True)

    await update.message.reply_text(
        "Quyidagi ko'rsatilgan menyudan o'zingizga kerakli bo'limni tanlang\n\nTo\'liq ma\'lumot olish uchun /doc bosing\n\nReklama /ads, Botlar /bots",
        reply_markup=reply_markup)

    return MAIN


async def football_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    txt = ""

    scrapeable = scraper.scrape_data()

    if scrapeable:
        for i in scrapeable:
            txt += "\n⎯  ⎯\n"
            txt += f"\n⚽️ {i[0]['name']}\n\n"

            for k in range(0, len(i[0]['matches'])):
                txt += f"    ⏰ {i[0]['matches'][k]['time']}\n    🎮 {i[0]['matches'][k]['team']}\n\n"

        await update.message.reply_text(text=txt)

        return MAIN
    else:
        await update.message.reply_text("💩 Ma'lumotlar topilmadi")

        return MAIN


async def cancel_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤧 Bekor qilindi")
    await update.message.reply_text("Qaytadan boshlash uchun\n/menu ni bosing", reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error {context.error}")


if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).read_timeout(100).get_updates_read_timeout(100).build()
    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler('start', start_handler),
            CommandHandler('menu', menu_handler),
            CommandHandler('doc', doc_handler),
        ],
        states={
            MAIN: [
                MessageHandler(filters.Regex(".*Football o'yinlari$"), football_handler),
            ],
        },
        fallbacks=[
            CommandHandler('cancel', cancel_handler),
            CommandHandler('start', start_handler),
            CommandHandler('menu', menu_handler),
            CommandHandler('football', football_handler),
            CommandHandler('doc', doc_handler),
            CommandHandler('ads', ads_handler),
            CommandHandler('cmd', cmd_handler),
            CommandHandler('bots', bots_handler),
        ],
    )

    app.add_handler(conv_handler)

    app.add_error_handler(error_handler)

    print("updated...")
    app.run_polling()
