import telebot
import google.generativeai as genai
import os
from config import *

TELEGRAM_BOT_TOKEN = TOKEN
GEMINI_API_KEY = GOOGLE_API_KEY


bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)


genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-pro")


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Hello there! I'm Gemini, your AI assistant. How can I help you today? 🤖\nCommands:\n   `/version` Gives GenAI version info. \n   `/essay [Word Count] [Title]` Generates you a beautiful essay. \n   `/answer [Message]` Gives you some options for answering a message", parse_mode="Markdown")

@bot.message_handler(commands=['version'])
def ver(message):
    versionnumber = model.model_name.strip('models/')
    bot.send_message(message.chat.id, f"This model is running on {versionnumber}")

@bot.message_handler(commands=['essay'])
def essay(message):
    promp = message.text.split()
    title = ' '.join(message.text.split()[2:])

    bot.send_chat_action(message.chat.id, "typing")
    bot.send_message(message.chat.id, f"Generating a {promp[1]}-word essay about *{title}*..", parse_mode="Markdown")
    
    try:
        print(f'Generating a {promp[1]}-word essay on {title}. Keeping it formal and informative.')
        response = model.generate_content(f'Generate a {promp[1]}-word essay on {title}. Keep it formal and informative.') 
        bot.send_message(message.chat.id, response.text, parse_mode="Markdown") 
    except Exception as error:
        bot.send_message(message.chat.id, "⚠️ Error processing your request.")
        print("Error:", error)
    
@bot.message_handler(commands=['answer'])
def answer(message):
    
    msg = ' '.join(message.text.split()[1:])

    bot.send_chat_action(message.chat.id, "typing")
    bot.send_message(message.chat.id, f"Writing you an answer for `{msg}`", parse_mode="Markdown")
    
    try:
        print(f'Generating an answer for {msg}.')
        response = model.generate_content(f'How would you answer to {msg}? Give me 3 variants. Do not use " in the answers. Add enter between the answers. Add an introduction to your message.') 
        bot.send_message(message.chat.id, response.text, parse_mode="Markdown") 
    except Exception as error:
        bot.send_message(message.chat.id, "⚠️ Error processing your request.")
        print("Error:", error)


@bot.message_handler(commands=['essay'])
def essay(message):
    promp = message.text.split()
    title = ' '.join(message.text.split()[2:])

    bot.send_chat_action(message.chat.id, "typing")
    bot.send_message(message.chat.id, f"Generating a {promp[1]}-word essay about *{title}*..", parse_mode="Markdown")
    
    try:
        print(f'Generating a {promp[1]}-word essay on {title}. Keeping it formal and informative.')
        response = model.generate_content(f'Generate a {promp[1]}-word essay on {title}. Keep it formal and informative.') 
        bot.send_message(message.chat.id, response.text, parse_mode="Markdown") 
    except Exception as error:
        bot.send_message(message.chat.id, "⚠️ Error processing your request.")
        print("Error:", error)
    
@bot.message_handler(commands=['email'])
def email(message):
    
    title = ' '.join(message.text.split()[1:])

    bot.send_chat_action(message.chat.id, "typing")
    bot.send_message(message.chat.id, f"Writing you an E-Mail for `{title}`", parse_mode="Markdown")
    
    try:
        print(f'Generating an email: {title}.')
        response = model.generate_content(f'Generate an email with the subject: {title}.') 
        bot.send_message(message.chat.id, response.text, parse_mode="Markdown") 
    except Exception as error:
        bot.send_message(message.chat.id, "⚠️ Error processing your request.")
        print("Error:", error)

 
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    bot.send_chat_action(message.chat.id, "typing")
    
    try:
        response = model.generate_content(message.text) 
        bot.send_message(message.chat.id, response.text, parse_mode="Markdown") 
    except Exception as error:
        bot.send_message(message.chat.id, "⚠️ Error processing your request.")
        print("Error:", error)


print("Bot is running")
bot.infinity_polling()