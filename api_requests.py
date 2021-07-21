import requests
import json
import random


def get_question(discord_id):
    response = requests.get(f'http://127.0.0.1:8000/api/question/?discord_id={discord_id}')
    json_data = json.loads(response.text)
    id = 1
    qs = ''
    answer = None
    points = None
    question_id = None
    average = None
    author = None

    if len(json_data) > 0:
        random_int = random.randint(0, len(json_data)-1)
        qs += json_data[random_int]['title'] + '\n'
        qs += '[You have 10 seconds to type the corrent answer]\n'
        for item in json_data[random_int]['answer']:
            qs += str(id) + '. ' + item['content'] + '\n'

            if item['correct']:
                answer = id
            id += 1

        points = json_data[random_int]['points']
        question_id = json_data[random_int]['id']
        return (qs, answer, points, question_id, average, author)
    else:
        return (qs, answer, points, question_id, average, author)


def my_questions(user_id):
    link = f'http://127.0.0.1:8000/api/question/?user_id={user_id}'
    response = requests.get(link)
    json_data = json.loads(response.text)

    text = ''
    if len(json_data) > 0:
        for i in range(0, len(json_data)):
            text += 'id: ' + str(json_data[i]['id']) + ' - Question: ' + json_data[i]['title'] + ' rating: ' + str(json_data[i]['get_average_review']['average']) + '\n'
    else:
        text = None
    return text
