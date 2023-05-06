#!/usr/bin/python
# -*- coding: <encoding name> -*-


import telebot
import nltk
import nltk.sentiment.vader as vader
from time import sleep
from translate import Translator

# API TOKEN -- Cuidado para não vazar. --
API_TOKEN = "<API Token do seu bot>"

# Objetos Básicos
sid = vader.SentimentIntensityAnalyzer()
trad = Translator(from_lang="pt", to_lang="en")
bot = telebot.TeleBot(API_TOKEN)
greylist = open("greylist.txt", "rt").read().split(' ')
blacklist = open("blacklist.txt", "rt").read().split(' ')


# Funções Básicas
# Multiple Replace
def mreplace(texto):
    lista = ['"', '.', '!', '@', '#', '$', '%', '¨', '&', '*', '(', ')', '¹', '²', '³', '£', '¢', '¬', '_',
             '-', '+', '=', '§', '´', '`', '~', '^', '[', '{', ']', '}', 'º', 'ª', ';', ':', '.', '>', ',',
             '<', '/', '?', '°', '|']
    result = texto.lower()
    for char in result:
        if char in lista:
            result = result.replace(char, '')
    return str(result)


# Verificar se há palavras das listas no texto
def verificar(message):
    texto = mreplace(message)
    text1 = nltk.word_tokenize(texto, "portuguese")
    for item in text1:
        if item in blacklist or item in greylist:
            return True


# Identificar de qual lista é a palavra encontrada no texto
def analisartxt(texto):
    textr = nltk.word_tokenize(mreplace(texto), language="portuguese")
    if set(textr).intersection(blacklist):
        return 'b'
    elif set(textr).intersection(greylist):
        return 'g'


# Traduzir e Analisar sentimento do texto
def analisarsent(texto):
    tx = nltk.sent_tokenize(texto, "portuguese")
    for item in tx:
        if sid.polarity_scores(trad.translate(item))['compound'] < 0:
            return True
        else:
            return False


# Programa principal

try:
    @bot.message_handler(func=lambda x: True)
    def outputing(message):
        out = dict()
        out['user'] = str(message.from_user)
        out['date'] = str(message.date)
        out['text'] = str(message.text)
        out['message_id'] = str(message.message_id)
        out['chat_id'] = str(message.chat.id)
        output = open("output.txt", "at+", encoding='utf-8')
        output.write(str(f'{out}\n'))
        output.close()
        sleep(1)
        if verificar(message.text) is True:
            texto = message.text.lower()
            bg = analisartxt(texto)
            match bg:
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


except:
    pass

bot.polling()
# bot.send_message(chat_id=-1001885652312, text="coisas")
