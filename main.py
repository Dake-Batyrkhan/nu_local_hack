import telebot
import nltk 
from nltk.corpus import wordnet

TOKEN  = "1012384959:AAHaqGdOMFEGfkZ4zBW1QEW7N3u1WAmyAZs" 

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def help_start(message):
  bot.send_message(message.chat.id,"Welcome!")

@bot.message_handler(commands=['paraphrase'])
def help_start(message):
  bot.send_message(message.chat.id,"Send your text")

@bot.message_handler(func=lambda m: True)
def send_welcome(message):
  try:
    try:
      x = int(message.text)
    except Exception as e:
      raise e
  except:
    try:
      x = float(message.text)
    except:
      x = message.text
  low = x.split(' ')
  res_str = ''
  for word in low:
    synonym = get(word)
    if '_' in synonym:
      string = ''
      two_sent = synonym.split('_')
      for sent in two_sent:
        string += sent
        string += ' '
      synonym = string
    res_str += synonym
    res_str += ' '

  bot.send_message(message.chat.id, res_str)
  print(res_str)


def get(word):
  if len(word) < 3:
    return word

  synonyms = []
  for syn in wordnet.synsets(word):
    for l in syn.lemmas():
      synonyms.append(l.name())
  if len(synonyms) == 0:
    return word

  max_similar = 0
  index = 0
  sim_list = ['n', 'a', 'v', 's', 'r']
  for t in sim_list:
    try:
      w1 = wordnet.synset('{}.{}.01'.format(word, t))
    except:
      continue
    for i in range(len(synonyms)):
      try:
        w2 = wordnet.synset('{}.{}.01'.format(synonyms[i], t))
        current = w1.wup_similarity(w2)

        if current > 0.5 and synonyms[i].lower() != word.lower():
          if current > max_similar:
            max_similar = current
            index = i
      except:
        continue


  return synonyms[index]

bot.polling()


