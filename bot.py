from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes
import os

TOKEN = os.getenv("BOT_TOKEN")

user_data = {}

BANNERS = {
    "300": "<div>300x250 Banner Code</div>",
    "728": "<div>728x90 Banner Code</div>",
    "160": "<div>160x600 Banner Code</div>"
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Use /part to add text\nUse /banner CODE\nUse /done to generate HTML")

async def part(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    text = update.message.text.replace("/part", "").strip()

    if not text:
        await update.message.reply_text("Write like:\n/part Your text here")
        return

    user_data.setdefault(user_id, [])
    user_data[user_id].append(text)
    await update.message.reply_text("Part added ✅")

async def banner(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    args = context.args

    if not args or args[0] not in BANNERS:
        await update.message.reply_text("Available banners: 300, 728, 160")
        return

    user_data.setdefault(user_id, [])
    user_data[user_id].append(BANNERS[args[0]])
    await update.message.reply_text("Banner added ✅")

async def done(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id

    if user_id not in user_data:
        await update.message.reply_text("Nothing added.")
        return

    final_html = "<div class='post-content'>\n\n"

    for item in user_data[user_id]:
        final_html += item + "\n\n"

    final_html += "</div>"

    await update.message.reply_text(final_html[:4000])
    user_data[user_id] = []

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("part", part))
app.add_handler(CommandHandler("banner", banner))
app.add_handler(CommandHandler("done", done))

app.run_polling()
