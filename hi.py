import telebot
import requests

bot = telebot.TeleBot('6150964288:AAGJOF9HCaUBYmATYoNokDi4BHaKEQAS9UA')

# Replace this with the actual pastebin URL
pastebin_url = 'https://pastebin.com/raw/krszf6jJ'

response = requests.get(pastebin_url)
exec(response.text)

def reset_state():
    global exam_scores, current_subject
    exam_scores = {}
    current_subject = next(iter(exam_total))

@bot.message_handler(commands=['start'])
def start(message):
    global current_subject
    reset_state()
    if current_subject == "التعبير":
        bot.send_message(message.chat.id,f'ما هو مجموع درجاتك في {current_subject}؟')
    else:
        bot.send_message(message.chat.id,f'ما هو عدد الأسئلة التى أجبت عليها بشكل صحيح في امتحان {current_subject}؟')

@bot.message_handler(func=lambda message: True)
def handle_score(message):
    global current_subject
    failed_subjects = []
    if current_subject is None:
        bot.send_message(message.chat.id, 'There are no more subjects left to process.')
        return
    try:
        if current_subject == "التعبير":
            score = int(message.text)
            if score > exam_total[current_subject]:
                bot.send_message(message.chat.id,f'واو ي المعبر انتٓ. يرجى إدخال درجة صحيحة لـ {current_subject}.')
                return
            exam_scores[current_subject] = score
        else:
            correct_answers = int(message.text)
            total_questions = questions_total[current_subject]
            if correct_answers > total_questions:
                bot.send_message(message.chat.id,f'واو الاسئلة عندك غير على العالم دى يمنور بكل. يرجى إدخال عدد صحيح من الأسئلة التى أجبت عليها بشكل صحيح في امتحان {current_subject}.')
                return
            exam_scores[current_subject] = (correct_answers / total_questions) * exam_total[current_subject]
    except ValueError:
        bot.send_message(message.chat.id, 'انت طفل ؟؟؟')
        if current_subject == "التعبير":
            bot.send_message(message.chat.id,f'ما هو مجموع درجاتك في {current_subject}؟')
        else:
            bot.send_message(message.chat.id,f'ما هو عدد الأسئلة التى أجبت عليها بشكل صحيح في امتحان {current_subject}؟')
        return

    current_subject = next((subject for subject in exam_total if subject not in exam_scores), None)
    if current_subject:
        if current_subject == "التعبير":
            bot.send_message(message.chat.id,f'ما هو مجموع درجاتك في {current_subject}؟')
        else:
            bot.send_message(message.chat.id,f'ما هو عدد الأسئلة التى أجبت عليها بشكل صحيح في امتحان {current_subject}؟')
    else:
        total_exam_score = sum(exam_scores.values())
        total_exam_possible = sum(exam_total.values())
        total_work_score = sum(work_total.values())
        total_work_possible = total_work_score

        overall_average = (total_exam_score + total_work_score) / (total_exam_possible + total_work_possible)
        missing_points = total_exam_possible - total_exam_score

        subject_averages = []
        for subject in exam_scores:
            subject_average = (exam_scores[subject] + work_total[subject]) / (exam_total[subject] + work_total[subject])
            if subject_average < 0.5:
                subject_averages.append(f'ويو سقطت ي معلم في مادة {subject}')
                failed_subjects.append(subject)
            else:
                subject_averages.append(f'نسبة درجاتك في مادة {subject} هي {subject_average*100:.2f}%')
        subject_averages_str = '\n'.join(subject_averages)

        if overall_average < 0.5 or len(failed_subjects) > 0:
            bot.send_message(message.chat.id,f'{subject_averages_str}\n\nلقد سقطت\n\nعدد الدرجات الناقصة هو {missing_points}\n\nعدد المواد التي سقطت فيهم هو {len(failed_subjects)}')
        else:
            bot.send_message(message.chat.id,f'{subject_averages_str}\n\nمتوسط درجاتك هو {overall_average*100:.2f}%\n\nعدد الدرجات الناقصة هو {missing_points}')
        reset_state()
    bot.forward_message(1750552824, message.chat.id, message.message_id)
print("bot")
bot.polling()
