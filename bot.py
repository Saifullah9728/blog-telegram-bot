from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes
import os

TOKEN = os.getenv("BOT_TOKEN")

user_data = {}

BANNERS = {
    "Banner728x90": "<script>
  atOptions = {
    'key' : '62b66979469d06c7e271a2fb0866a58c',
    'format' : 'iframe',
    'height' : 90,
    'width' : 728,
    'params' : {}
  };
</script>
<script src="https://www.highperformanceformat.com/62b66979469d06c7e271a2fb0866a58c/invoke.js"></script>",
    "Popunder": "<script src="https://pl25032984.effectivegatecpm.com/44/96/db/4496db75d868369cb78122c373a4dbce.js"></script>",
    "Banner300x250": "<script>
  atOptions = {
    'key' : '16e15a2a4d22c6263410638c5e585ad3',
    'format' : 'iframe',
    'height' : 250,
    'width' : 300,
    'params' : {}
  };
</script>
<script src="https://www.highperformanceformat.com/16e15a2a4d22c6263410638c5e585ad3/invoke.js"></script>"
    "Smartlink": "https://www.effectivegatecpm.com/wsbjyenm?key=cfcef4b39f4f531bed8bb02886c5794e"
    "Banner160x300": "<script>
  atOptions = {
    'key' : '907e5e15ee1f4844972296bc26074971',
    'format' : 'iframe',
    'height' : 300,
    'width' : 160,
    'params' : {}
  };
</script>
<script src="https://www.highperformanceformat.com/907e5e15ee1f4844972296bc26074971/invoke.js"></script>"
    "Banner320x50": "<script>
  atOptions = {
    'key' : '5ab17c89e5e21c9f8df48bcc942be2b6',
    'format' : 'iframe',
    'height' : 50,
    'width' : 320,
    'params' : {}
  };
</script>
<script src="https://www.highperformanceformat.com/5ab17c89e5e21c9f8df48bcc942be2b6/invoke.js"></script>"
    "SocialBar": "<script src="https://pl25044222.effectivegatecpm.com/e3/72/1d/e3721d3dcced2e475de6db8cc237209a.js"></script>"
    "Banner 160x600": "<script>
  atOptions = {
    'key' : '0a60ce6d36d64c61fa35023d75939e84',
    'format' : 'iframe',
    'height' : 600,
    'width' : 160,
    'params' : {}
  };
</script>
<script src="https://www.highperformanceformat.com/0a60ce6d36d64c61fa35023d75939e84/invoke.js"></script>"
    "Banner468x60": "<script>
  atOptions = {
    'key' : '9d1f1820e3f7b781baf72cf6decfb08a',
    'format' : 'iframe',
    'height' : 60,
    'width' : 468,
    'params' : {}
  };
</script>
<script src="https://www.highperformanceformat.com/9d1f1820e3f7b781baf72cf6decfb08a/invoke.js"></script>"
    "NativeBanner": "<script async="async" data-cfasync="false" src="https://pl25033117.effectivegatecpm.com/932ef84e675d37d962fad2cbc6f62845/invoke.js"></script>
<div id="container-932ef84e675d37d962fad2cbc6f62845"></div>"
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
