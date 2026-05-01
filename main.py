import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = os.getenv("TELEGRAM_TOKEN")

# -------- תרגום פשוט (חינמי דרך API פתוח) --------
def translate(text):
    url = "https://api.mymemory.translated.net/get"
    params = {
        "q": text,
        "langpair": "he|en"
    }
    res = requests.get(url, params=params).json()
    return res["responseData"]["translatedText"]

# -------- מחיר מניה (ללא מפתח API) --------
def stock_price(symbol):
    url = f"https://query1.finance.yahoo.com/v7/finance/quote?symbols={symbol}"
    res = requests.get(url).json()
    try:
        price = res["quoteResponse"]["result"][0]["regularMarketPrice"]
        return price
    except:
        return None

# -------- פקודת התחלה --------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 ברוך הבא!\n\n"
        "כתוב טקסט → אני אתרגם לאנגלית 🌍\n"
        "או כתוב: stock AAPL 📈"
    )

# -------- הודעות --------
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    # אם זה מניה
    if text.lower().startswith("stock"):
        symbol = text.split(" ")[1].upper()
        price = stock_price(symbol)

        if price:
            await update.message.reply_text(f"📈 מחיר {symbol}: ${price}")
        else:
            await update.message.reply_text("❌ לא נמצא סמל מניה")
        return

    # אחרת – תרגום
    translated = translate(text)
    await update.message.reply_text(f"🌍 תרגום:\n{translated}")

# -------- הפעלה --------
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_polling()

if __name__ == "__main__":
    main()
