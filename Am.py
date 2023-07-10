import telebot
import random
import requests

TOKEN = '5566197914:AAHIoqN-wclAi8BU6vAnR_b5HQP07yPNKMw'
bot = telebot.TeleBot(TOKEN)

elements = {
    "المونيوم": {"symbol": "Al", "state": "S", "melting_point": 660, "boiling_point": 2470, "density": 2.7},
    "النحاس": {"symbol": "Cu", "state": "S", "melting_point": 1083, "boiling_point": 2562, "density": 8.96},
    "الذهب": {"symbol": "Au", "state": "S", "melting_point": 1063, "boiling_point": 2856, "density": 19.3},
    "الحديد": {"symbol": "Fe", "state": "S", "melting_point": 1535, "boiling_point": 2862, "density": 7.87},
    "الرصاص": {"symbol": "Pb", "state": "S", "melting_point": 327, "boiling_point": 1749, "density": 11.34},
    'الماغنسيوم': {'symbol': 'Mg', 'state': 'S', 'melting_point': 650, 'boiling_point': 1090, 'density': 1.738},
    'الزئبق': {'symbol': 'Hg', 'state': 'I', 'melting_point': -39, 'boiling_point': 357, 'density': 13.5336},
    'النيكل': {'symbol': 'Ni', 'state': 'S', 'melting_point': 1453, 'boiling_point': 2913, 'density': 8.908},
    'الفضة': {'symbol': 'Ag', 'state': 'S', 'melting_point': 961, 'boiling_point': 2162, 'density': 10.49},
    'القصدير': {'symbol': 'Sn', 'state': 'S', 'melting_point': 232, 'boiling_point': 2602, 'density': 7.287},
    'الخارصين': {'symbol': 'Zn', 'state': 'S', 'melting_point': 420, 'boiling_point': 907, 'density':7.14}
}

element_names = list(elements.keys())
random.shuffle(element_names)

user_options = {}
user_data = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_data[message.chat.id] = {'correct_answers': 0, 'wrong_answers': [],'current_element_index' :0}
    msg = bot.send_message(message.chat.id, f"مرحباً {message.from_user.first_name}! هل أنت مستعد للاختبار؟")
    bot.register_next_step_handler(msg, ask_name_or_symbol)

def ask_name_or_symbol(message):
    msg = bot.send_message(message.chat.id, f"اختر: هل تريد الأسماء مكان الرموز (1) أو الرموز مكان الأسماء (2)؟")
    bot.register_next_step_handler(msg, process_name_or_symbol)

def process_name_or_symbol(message):
    user_options['name_or_symbol'] = int(message.text)
    msg = bot.send_message(message.chat.id, f"هل تريد درجة الغليان ضمن الأسئلة؟ (Y/N)")
    bot.register_next_step_handler(msg, process_include_boiling)

def process_include_boiling(message):
    user_options['include_boiling'] = message.text.upper() == "Y"
    msg = bot.send_message(message.chat.id, f"هل تريد حالة العنصر ضمن الأسئلة؟ (Y/N)")
    bot.register_next_step_handler(msg, process_include_state)

def process_include_state(message):
    user_options['include_state'] = message.text.upper() == "Y"
    msg = bot.send_message(message.chat.id, f"هل تريد درجة الانصهار ضمن الأسئلة؟ (Y/N)")
    bot.register_next_step_handler(msg, process_include_melting)

def process_include_melting(message):
    user_options['include_melting'] = message.text.upper() == "Y"
    msg = bot.send_message(message.chat.id, f"هل تريد الكثافة ضمن الأسئلة؟ (Y/N)")
    bot.register_next_step_handler(msg, process_include_density)

def process_include_density(message):
    user_options['include_density'] = message.text.upper() == "Y"
    ask_element_questions(message,0)

def ask_element_questions(message,index):
    if index >= len(element_names):
        show_results(message)
        return
    element = element_names[index]
    user_data[message.chat.id]['current_element_index'] = index
    if user_options['name_or_symbol'] == 1:
        msg = bot.send_message(message.chat.id, f"ما هو اسم {elements[element]['symbol']}؟")
        bot.register_next_step_handler(msg, lambda msg: process_element_name(msg, element))
    else:
        msg = bot.send_message(message.chat.id, f"ما هو رمز {element}؟")
        bot.register_next_step_handler(msg, lambda msg: process_element_symbol(msg, element))

def process_element_name(message, element):
    if message.text == element:
        bot.send_message(message.chat.id, "صحيح!")
        user_data[message.chat.id]['correct_answers'] += 1
    else:
        bot.send_message(message.chat.id, f"غلط! الإجابة الصحيحة هي {element}")
        user_data[message.chat.id]['wrong_answers'].append(element)
    if user_options['include_state']:
        msg = bot.send_message(message.chat.id, f"ما هو حالة {element}؟")
        bot.register_next_step_handler(msg, lambda msg: process_element_state(msg, element))
    else:
        ask_element_questions(message,user_data[message.chat.id]['current_element_index']+1)

def process_element_symbol(message, element):
    if message.text == elements[element]['symbol']:
        bot.send_message(message.chat.id, "صحيح!")
        user_data[message.chat.id]['correct_answers'] += 1
    else:
        bot.send_message(message.chat.id, f"غلط! الإجابة الصحيحة هي {elements[element]['symbol']}")
        user_data[message.chat.id]['wrong_answers'].append(element)
    if user_options['include_state']:
        msg = bot.send_message(message.chat.id, f"ما هو حالة {element}؟")
        bot.register_next_step_handler(msg, lambda msg: process_element_state(msg, element))
    else:
        ask_element_questions(message,user_data[message.chat.id]['current_element_index']+1)

def process_element_state(message, element):
    if message.text == elements[element]['state']:
        bot.send_message(message.chat.id, "صحيح!")
        user_data[message.chat.id]['correct_answers'] += 1
    else:
        bot.send_message(message.chat.id, f"غلط! الإجابة الصحيحة هي {elements[element]['state']}")
        user_data[message.chat.id]['wrong_answers'].append(element)
    if user_options['include_melting']:
        msg = bot.send_message(message.chat.id, f"ما هو درجة انصهار {element}؟")
        bot.register_next_step_handler(msg, lambda msg: process_element_melting(msg, element))
    else:
        ask_element_questions(message,user_data[message.chat.id]['current_element_index']+1)

def process_element_melting(message, element):
    if int(message.text) == elements[element]['melting_point']:
        bot.send_message(message.chat.id, "صحيح!")
        user_data[message.chat.id]['correct_answers'] += 1
    else:
        bot.send_message(message.chat.id, f"غلط! الإجابة الصحيحة هي {elements[element]['melting_point']}")
        user_data[message.chat.id]['wrong_answers'].append(element)
    if user_options['include_boiling']:
        msg = bot.send_message(message.chat.id, f"ما هو درجة غليان {element}؟")
        bot.send_message(message.chat.id, f"ما هو درجة غليان {element}؟")
        bot.register_next_step_handler(msg, lambda msg: process_element_boiling(msg, element))




def show_results(message):
    total_questions = len(element_names)
    correct_answers = user_data[message.chat.id]['correct_answers']
    wrong_answers = len(user_data[message.chat.id]['wrong_answers'])
    percentage = round((correct_answers / total_questions) * 100, 2)
    bot.send_message(message.chat.id, f"لقد أجبت على {correct_answers} من أصل {total_questions} بشكل صحيح. عدد الإجابات الخاطئة هو {wrong_answers}. نسبة الإجابات الصحيحة هي {percentage}%")
    if wrong_answers > 0:
        bot.send_message(message.chat.id, f"العناصر التي أجبت عنها بشكل خاطئ: {', '.join(user_data[message.chat.id]['wrong_answers'])}")
    msg = bot.send_message(message.chat.id, "هل ترغب في إعادة الاختبار؟ (Y/N)")
    bot.register_next_step_handler(msg, restart_test)

def restart_test(message):
    if message.text.upper() == "Y":
        random.shuffle(element_names)
        user_data[message.chat.id] = {'correct_answers': 0, 'wrong_answers': [],'current_element_index' :0}
        ask_name_or_symbol(message)
print("bot")
bot.polling()
