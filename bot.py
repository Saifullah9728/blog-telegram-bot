from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os

TOKEN = os.getenv("BOT_TOKEN")

# User data store (per user)
user_data = {}  # {user_id: {'title': str, 'parts': [str], 'banners': [str]} }

# Banner codes (wrapped in centered div for better Blogger look)
BANNERS = {
    "728": '<div style="text-align:center; margin:20px 0;"><script>atOptions = { \'key\' : \'62b66979469d06c7e271a2fb0866a58c\', \'format\' : \'iframe\', \'height\' : 90, \'width\' : 728, \'params\' : {} }; </script><script src="https://www.highperformanceformat.com/62b66979469d06c7e271a2fb0866a58c/invoke.js"></script></div>',
    
    "300": '<div style="text-align:center; margin:20px 0;"><script>atOptions = { \'key\' : \'16e15a2a4d22c6263410638c5e585ad3\', \'format\' : \'iframe\', \'height\' : 250, \'width\' : 300, \'params\' : {} }; </script><script src="https://www.highperformanceformat.com/16e15a2a4d22c6263410638c5e585ad3/invoke.js"></script></div>',
    
    "160": '<div style="text-align:center; margin:20px 0;"><script>atOptions = { \'key\' : \'0a60ce6d36d64c61fa35023d75939e84\', \'format\' : \'iframe\', \'height\' : 600, \'width\' : 160, \'params\' : {} }; </script><script src="https://www.highperformanceformat.com/0a60ce6d36d64c61fa35023d75939e84/invoke.js"></script></div>',
    
    "468": '<div style="text-align:center; margin:20px 0;"><script>atOptions = { \'key\' : \'9d1f1820e3f7b781baf72cf6decfb08a\', \'format\' : \'iframe\', \'height\' : 60, \'width\' : 468, \'params\' : {} }; </script><script src="https://www.highperformanceformat.com/9d1f1820e3f7b781baf72cf6decfb08a/invoke.js"></script></div>',
    
    "320": '<div style="text-align:center; margin:20px 0;"><script>atOptions = { \'key\' : \'5ab17c89e5e21c9f8df48bcc942be2b6\', \'format\' : \'iframe\', \'height\' : 50, \'width\' : 320, \'params\' : {} }; </script><script src="https://www.highperformanceformat.com/5ab17c89e5e21c9f8df48bcc942be2b6/invoke.js"></script></div>',
    
    "smart": '<div style="text-align:center; margin:20px 0; font-size:18px;"><a href="https://www.effectivegatecpm.com/wsbjyenm?key=cfcef4b39f4f531bed8bb02886c5794e" target="_blank" style="color:#ff0000; font-weight:bold;">এখানে ক্লিক করে আজ থেকেই আয় শুরু করুন →</a></div>',
    
    "native": '<div style="text-align:center; margin:20px 0;"><script async="async" data-cfasync="false" src="https://pl25033117.effectivegatecpm.com/932ef84e675d37d962fad2cbc6f62845/invoke.js"></script><div id="container-932ef84e675d37d962fad2cbc6f62845"></div></div>',
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "স্বাগতম! এই বট দিয়ে Blogger post-এর HTML তৈরি করতে পারবে।\n\n"
        "কমান্ডস:\n"
        "/title <পোস্টের টাইটেল>\n"
        "/part <একটা অংশ/প্যারাগ্রাফ>\n"
        "/banner <কোড>   (যেমন: 728, 300, 160, smart, native)\n"
        "/done           → পুরো HTML পাবে\n"
        "/clear          → সব রিসেট করো\n"
        "/help           → এই মেসেজ আবার দেখো"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await start(update, context)

async def title(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text.replace("/title", "").strip()
    if not text:
        await update.message.reply_text("উদাহরণ: /title How to Earn Money Online 2026")
        return
    user_data.setdefault(user_id, {'title': '', 'parts': []})
    user_data[user_id]['title'] = text
    await update.message.reply_text(f"টাইটেল সেট হয়েছে: {text}")

async def part(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text.replace("/part", "").strip()
    if not text:
        await update.message.reply_text("উদাহরণ: /part এখানে তোমার প্যারাগ্রাফ লিখো")
        return
    user_data.setdefault(user_id, {'title': '', 'parts': []})
    user_data[user_id]['parts'].append(text)
    await update.message.reply_text("অংশ যোগ হয়েছে ✅")

async def banner(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    args = context.args
    if not args:
        await update.message.reply_text("উদাহরণ: /banner 728 বা /banner 300 বা /banner smart")
        return
    
    code = args[0].lower()
    banner_key = None
    for key in BANNERS:
        if code in key.lower() or code == key.lower():
            banner_key = key
            break
    
    if not banner_key:
        await update.message.reply_text("Available banners: 728, 300, 160, 468, 320, smart, native")
        return
    
    user_data.setdefault(user_id, {'title': '', 'parts': []})
    user_data[user_id]['parts'].append(BANNERS[banner_key])
    await update.message.reply_text(f"{banner_key} banner যোগ হয়েছে ✅")

async def done(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in user_data or not user_data[user_id].get('parts'):
        await update.message.reply_text("কোনো কনটেন্ট যোগ করা হয়নি। /part দিয়ে শুরু করো।")
        return
    
    data = user_data[user_id]
    title = data.get('title', 'Untitled Post')
    
    final_html = f"<h1>{title}</h1>\n\n<div class='post-content'>\n"
    for item in data['parts']:
        final_html += f"{item}\n\n"
    final_html += "</div>"
    
    # Telegram message limit ~4096 chars, তাই চেক করে পাঠানো
    if len(final_html) > 4000:
        await update.message.reply_text(final_html[:4000] + "\n\n... (বাকিটা দেখতে /done আবার দাও অথবা copy করো)")
    else:
        await update.message.reply_text(final_html, parse_mode=None)  # HTML হিসেবে না পাঠিয়ে raw text
    
    # Clear after done (optional - comment out if you want to keep)
    # del user_data[user_id]

async def clear(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id in user_data:
        del user_data[user_id]
    await update.message.reply_text("সব ক্লিয়ার হয়েছে। নতুন করে শুরু করো!")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("title", title))
    app.add_handler(CommandHandler("part", part))
    app.add_handler(CommandHandler("banner", banner))
    app.add_handler(CommandHandler("done", done))
    app.add_handler(CommandHandler("clear", clear))
    
    print("Bot is running...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
