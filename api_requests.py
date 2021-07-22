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
    print('my questions json data', json_data)
    if len(json_data) > 0:
        for i in range(0, len(json_data)):
            text += 'id: ' + str(json_data[i]['id']) + ' - Question: ' + json_data[i]['title'] + ' - Created on: ' + json_data[i]['created'] + '\n'
    else:
        text = None
    return text


def update_points(name, points, id, question_id):
    url = 'http://127.0.0.1:8000/api/users/'
    data = {'name': name, 'score': points, 'discord_id': id, 'question_id': question_id}
    request = requests.post(url, data)
    return


def get_ranking(message, author_id):
    msg = message.split(' ')
    print(msg)
    leaderboard = ''
    link = None

    if len(msg) > 1:
        link = f'http://127.0.0.1:8000/api/users/?id={author_id}&param={msg[1]}'
    else:
        link = f'http://127.0.0.1:8000/api/users/?id={author_id}'

    response = requests.get(link)
    json_data = json.loads(response.text)
    if json_data is not None:
        position = 1
        if len(json_data) > 1:
            for user in json_data:
                leaderboard += str(position) + '. ' + user['name'] + ' points: ' + str(user['score']) + '\n'
                position += 1
        else:
            leaderboard += str(position) + '. ' + json_data[0]['name'] + ' points: ' + str(json_data[0]['score']) + '\n'
        return leaderboard
    else:
        return 'Number must be greater than 0!'


