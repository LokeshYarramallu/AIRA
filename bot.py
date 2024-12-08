from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, MessageReactionHandler
from lindata import scrap_profile
from cloud import FBDB
from resume import get_latex, tex_to_pdf
import re
from chatbot import aira_assist
import time, asyncio

user_data = FBDB()
TOKEN: Final = "7515472060:"+"AAGPjaQ6w1vyMYlNDboBvyQetVw10FywUjk"  # Replace with your actual bot token
BOT_USERNAME: Final = '@aira_telegram_bot'

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! This is AIRA, your AI powered Resume assistant")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    output = ("/resume - Get your resume\n"
              "/update - Update your LinkedIn profile")
    await update.message.reply_text(output)

async def resume_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Checking Data...")
    user_id = update.message.chat_id
    json_file = user_data.get(user_id)
    if not json_file:
        await update.message.reply_text("No profile data found. Please update your profile using /update.")
        return
    tex_file = get_latex(json_file)
    tex_filename = "resume.tex"

    # Write LaTeX file asynchronously to avoid blocking the event loop
    with open(tex_filename, "w") as f:
        f.write(tex_file)

    await asyncio.sleep(4)  # Replace time.sleep() with async sleep
    tex_to_pdf(input_tex_file=tex_filename)  # Assuming this function handles PDF generation synchronously
    await update.message.reply_text("Here's your resume:")
    await update.message.reply_document('resume.pdf')

async def update_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.chat_id
    await update.message.reply_text("Enter your LinkedIn Profile URL:")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.chat_id
    message_type = update.message.chat.type
    text = update.message.text
    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

    text = text.lower()

    # Updated LinkedIn URL regex to match a broader set of URLs
    if re.match(r"^https:\/\/(www\.)?linkedin\.com\/in\/[\w\-]+\/?$", text):
        await update.message.reply_text("Checking your url...")
        profile_data = scrap_profile(text)

        if profile_data is None:
            await update.message.reply_text("Please verify the URL you provided!")
        else:
            await update.message.reply_text("Verified!")
            updated = user_data.update(user_id, profile_data)
            if updated:
                await update.message.reply_text("Details Updated!")
    else:
        user_info = user_data.get(user_id)
        if user_info is None:
            await update.message.reply_text("I think you are new here. Please use /help for commands.")
        else:
            response = aira_assist(str(user_info), text)
            await update.message.reply_text(response)

if __name__ == '__main__':
    if not TOKEN:
        print("Error: Bot token is missing. Please set the TELEGRAM_BOT_TOKEN environment variable.")
    else:
        print('Starting bot...')
        app = Application.builder().token(TOKEN).build()

        app.add_handler(CommandHandler('start', start_command))
        app.add_handler(CommandHandler('help', help_command))
        app.add_handler(CommandHandler('resume', resume_command))
        app.add_handler(CommandHandler('update', update_command))

        app.add_handler(MessageHandler(filters.TEXT, handle_message))
        print('Polling...')
        app.run_polling(poll_interval=3)