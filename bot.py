import telebot
import random
import csv
import difflib

# إنشاء البوت باستخدام التوكن الخاص بك
bot = telebot.TeleBot("6288789065:AAGE3Xgmhj2dG4C1bduaW-Pg8qTpxeOUTsc")

# قراءة الأسئلة من ملف CSV
def load_questions_from_csv():
    questions = []
    with open('questions.csv', 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            questions.append({"question": row['question'], "answer": row['answer']})
    return questions

questions = load_questions_from_csv()

# إرسال سؤالين يوميًا
def send_daily_questions(chat_id):
    selected_questions = random.sample(questions, 2)  # اختيار سؤالين عشوائيًا
    for q in selected_questions:
        bot.send_message(chat_id, q["question"])
        bot.register_next_step_handler_by_chat_id(chat_id, check_answer, q["answer"])

# التحقق من الإجابة باستخدام difflib
def check_answer(message, correct_answer):
    user_answer = message.text.strip().lower()
    similarity = difflib.SequenceMatcher(None, user_answer, correct_answer.lower()).ratio()
    if similarity > 0.8:  # نسبة التطابق 80%
        bot.send_message(message.chat.id, "إجابة صحيحة! حصلت على نقاط.")
    else:
        bot.send_message(message.chat.id, "إجابة خاطئة! حاول مرة أخرى.")

# بدء التفاعل
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "مرحبًا بك! ستتلقى سؤالين يوميًا.")
    send_daily_questions(message.chat.id)

bot.polling()