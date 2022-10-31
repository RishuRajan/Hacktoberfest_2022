import telegram
bot = telegram.bot(token='TOKEN') #Replace TOKEN with your token string 

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
updater = Updater(token='TOKEN', use_context=True) #Replace TOKEN with your token string
dispatcher = updater.dispatcher

def hello(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Hello, World')

 
hello_handler = CommandHandler('hello', hello)
dispatcher.add_handler(hello_handler)


updater.start_polling()


import json
def summary(update, context):
    response = requests.get('https://api.covid19api.com/summary')
    if(response.status_code==200): #Everything went okay, we have the data
        data = response.json()
        print(data['Global'])
        context.bot.send_message(chat_id=update.effective_chat.id, text=data['Global'])
    else: #something went wrong
        context.bot.send_message(chat_id=update.effective_chat.id, text="Error, something went wrong.")
​
corona_summary_handler = CommandHandler('summary', summary)
dispatcher.add_handler(corona_summary_handler)

