import os
import subprocess
import json
import instaloader
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

TOKEN = "8694667171:AAGLVa1-aB4WOy4kxUr_isgjXSfHuIf-Vic"
FILE_PATH = "/home/ubuntu/insta.json"

L = instaloader.Instaloader()

def get_id(username):
    try:
        profile = instaloader.Profile.from_username(L.context, username)
        return str(profile.userid)
    except:
        return None

def search_db(term):
    try:
        output = subprocess.check_output(['grep', '-i', term, FILE_PATH], stderr=subprocess.STDOUT)
        lines = output.decode('utf-8').strip().split('\n')
        return [line for line in lines if line]
    except:
        return []

def format_data(json_str):
    try:
        if json_str.endswith(','):
            json_str = json_str[:-1]
        
        data = json.loads(json_str)
        
        username = data.get("username", "N/A")
        user_id = data.get("id", "N/A")
        email = data.get("email") or "Not Available"
        phone = data.get("phone") or "Not Available"
        name = data.get("name") or "Not Available"

        formatted_text = (
            f"👤 *Name:* `{name}`\n"
            f"🔗 *Username:* `@{username}`\n"
            f"🆔 *ID:* `{user_id}`\n"
            f"📧 *Email:* `{email}`\n"
            f"📞 *Phone:* `{phone}`\n"
            f"━━━━━━━━━━━━━━━━━━━━━━"
        )
        return formatted_text, username
    except:
        return None, None

def start_command(update, context):
    update.message.reply_text(
        "👋 *Welcome to the Database Scanner*\n\n"
        "Send me any Instagram username to scan the database.",
        parse_mode=ParseMode.MARKDOWN
    )

def handle_message(update, context):
    username = update.message.text.strip().replace('@', '')
    status_msg = update.message.reply_text(f"🔍 *Scanning database for* `@{username}`...", parse_mode=ParseMode.MARKDOWN)

    user_id = get_id(username)
    
    raw_results = []
    
    if user_id:
        raw_results.extend(search_db(f'"id": "{user_id}"'))
        if not raw_results:
            raw_results.extend(search_db(f'"id":"{user_id}"'))
            
    if not raw_results:
        raw_results.extend(search_db(f'"username": "{username}"'))
        if not raw_results:
            raw_results.extend(search_db(f'"username":"{username}"'))

    raw_results = list(set(raw_results))
    
    if not raw_results:
        status_msg.edit_text(f"❌ *No records found for* `@{username}` *in the current database.*", parse_mode=ParseMode.MARKDOWN)
        return

    final_text = "✅ *Record Successfully Retrieved:*\n\n"
    profile_username = username
    
    for res in raw_results:
        formatted, extracted_username = format_data(res)
        if formatted:
            final_text += formatted + "\n"
            if extracted_username and extracted_username != "N/A":
                profile_username = extracted_username

    keyboard = [
        [InlineKeyboardButton("View Instagram Profile", url=f"https://instagram.com/{profile_username}")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if len(final_text) > 4000:
        with open("result.txt", "w", encoding="utf-8") as f:
            f.write(final_text.replace('*', '').replace('`', ''))
        update.message.reply_document(document=open("result.txt", "rb"))
        status_msg.delete()
    else:
        status_msg.edit_text(final_text, parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup)

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    
    dp.add_handler(CommandHandler("start", start_command))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

