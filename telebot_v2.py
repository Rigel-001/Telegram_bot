import telebot
import nltk
import nltk.sentiment.vader as vader
from time import sleep
from translate import Translator

# API TOKEN -- Cuidado para não vazar. --
API_TOKEN = "CENSURADO"

# Objetos Básicos
sid = vader.SentimentIntensityAnalyzer()
trad = Translator(from_lang="pt", to_lang="en")
bot = telebot.TeleBot(API_TOKEN)
greylist = open("greylist.txt", "rt").read().split(' ')
blacklist = open("blacklist.txt", "rt").read().split(' ')
messagetext = str()


# Funções Básicas
# Verificar se há palavras das listas no texto
def verificar(message):
    text1 = nltk.word_tokenize(str(message.text).lower().replace('.', ''), "portuguese")
    print(text1)
    for item in text1:
        if item in blacklist or item in greylist:
            return True


# Identificar de qual lista é a palavra encontrada no texto
def analisartxt(texto):
    textr = nltk.word_tokenize(texto, language="portuguese")
    if set(textr).intersection(blacklist):
        return 'b'
    elif set(textr).intersection(greylist):
        return 'g'


# Traduzir e Analisar sentimento do texto
def analisarsent(texto):
    tx = nltk.sent_tokenize(texto, "portuguese")
    print(f'tx: {tx}')
    for item in tx:
        print(f'item: {item}')
        print(f'score: {sid.polarity_scores(trad.translate(item))}')
        if sid.polarity_scores(trad.translate(item))['compound'] < 0:
            return True
        else:
            return False


# Pega dado kkkj
@bot.message_handler(func=lambda x: True)
def outputing(message):
    out = dict()
    out['user'] = str(message.from_user)
    out['date'] = str(message.date)
    out['text'] = str(message.text)
    out['entities'] = str(message.entities)
    out['message_id'] = str(message.message_id)
    out['chat_id'] = str(message.chat.id)
    output = open("output.txt", "at+")
    output.write(str(f'{out}\n'))
    out1 = output.readlines()
    output.close()


# Programa Principal
@bot.message_handler(func=verificar)
def flagadm(message):
    texto = str(message.text).lower()
    bgn = analisartxt(texto)
    match bgn:
        case 'b':
            bot.reply_to(message, "cala a boca porra.")
            sleep(5)
            bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        case 'g':
            negativo = analisarsent(texto)
            if negativo is True:
                bot.reply_to(message, "cala a boca porra.")
                sleep(5)
                bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
            else:
                bot.reply_to(message, "cuidado mano.")


bot.polling()
# id do geral: 1885652312_1
