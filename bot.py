from telegram import ReplyKeyboardMarkup
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, ConversationHandler, MessageHandler, Filters
from covid19 import Covid19

buttons = ReplyKeyboardMarkup([['Statistika'],['Dunyo']],resize_keyboard = True)
covid = Covid19()

def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        'Salom {}'.format(update.effective_user.first_name),reply_markup = buttons )
    return  1



def stats(update, context):
    data = covid.getByCountryCode('Uzbekistan')
    update.message.reply_html(
        "<b>🇺🇿 "
        "Umumiy statistika</b>\n\n\n<b>Yuqtirganlar: </b> {}\n <b>Sogayganlar: </b> {}\n <b>Vafot etganlar: </b> {}\n <b>Davolanayotganlar: </b>{}\n <b>Og'ir axvoldagilar: {}</b>"
        "\n\n <b>Bugungi statistika: </b> \n\n <b>Bugungi yuqtirganlar: {}</b>\n Bugungi o'limlar soni: {}" .
            format(data['confirmed'],data['recovered'],data['deaths'],data['active'],data['critical'],
                   data['confirmedToday'],data['deathsToday']), reply_markup=buttons)




def world(update, context):
    data = covid.getLatest()
    update.message.reply_html(
        "<b>🌏 Umumiy statistika</b>\n\n<b>Yuqtirganlar: </b> {}\n <b>Sogayganlar: </b> {}\n "
        "<b>Vafot etganlar: </b> {}\n <b>Davolanayotganlar: </b>{}\n ".
        format(
            "{:,}".format(data['confirmed']),
            "{:,}".format(data['recovered']),
            "{:,}".format(data['deaths']),
            "{:,}".format(data['active'])), reply_markup=buttons)


updater = Updater('1360745993:AAH_nXZ9LSYZb_S3o5y9VFvd_f-WoUJaApc',use_context=True)
conv_handler = ConversationHandler(
    entry_points = [CommandHandler('start',start)],
    states = {
        1:[
            MessageHandler(Filters.regex('^(Statistika)$'),stats),
            MessageHandler(Filters.regex('^(Dunyo)$'), world),
        ]
    },
    fallbacks = [MessageHandler(Filters.text,start)]
)



updater.dispatcher.add_handler(conv_handler)


updater.start_polling()
updater.idle()