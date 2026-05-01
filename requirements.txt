import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = os.getenv("TELEGRAM_TOKEN")

# ---- בדיקת TOKEN ----
if not TOKEN:
    raise Exception("Missing TELEGRAM_TOKEN in Railway Variables")

# ---- תרגום ----
def translate(text):
    url = "https://api.mymemory.translated.net/get"
    params = {"q": text, "langpair": "he|en"}
    res = requests.get(url, params=params).json()
    return res["responseData"]["translatedText"]

# ---- מניה ----
def stock_price(symbol):
    url = f"https://query1.finance.yahoo.com/v7/finance/quote?symbols={symbol}"
    res = requests.get(url).json()
    try:
        return res["quoteResponse"]["result"][0]["regularMarketPrice"]
    except:
        return None

# ---- /start ----
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 הבוט עובד!\n\n"
        "כתוב טקסט לתרגום 🌍\n"
        "או: stock AAPL 📈"
    )

# ---- הודעות ----
async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    # מניה
    if text.lower().startswith("stock"):
        try:
            symbol = text.split(" ")[1].upper()
            price = stock_price(symbol)

            if price:
                await update.message.reply_text(f"📈 {symbol}: ${price}")
            else:
                await update.message.reply_text("❌ לא נמצא סמל מניה")
        except:
            await update.message.reply_text("❌ שימוש: stock AAPL")
        return

    # תרגום
    result = translate(text)
    await update.message.reply_text(f"🌍 {result}")

# ---- הפעלה ----
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

    app.run_polling()

if __name__ == "__main__":
    main()
