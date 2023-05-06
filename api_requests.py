import requests
import json
import random
from decouple import config


def get_question(discord_id):
    headers = {'Authorization': f'Token {config("auth")}'}
    response = requests.get(f'http://127.0.0.1:8000/api/question/?discord_id={discord_id}', headers=headers)
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
        average = json_data[random_int]['get_average_review']['average']
        author = json_data[random_int]['author']['name']

        return (qs, answer, points, question_id, average, author)
    else:
        return (qs, answer, points, question_id, average, author)


def question_details(question_id) -> str:
    headers = {'Authorization': f'Token {config("auth")}'}
    link = f'http://127.0.0.1:8000/api/question/get_question/?id={question_id}'
    response = requests.get(link, headers=headers)
    json_data = json.loads(response.text)
    text = f'Question id: {json_data["id"]}\n' \
           f'Title: {json_data["title"]}\n' \
           f'Points: {json_data["points"]}\n' \
           f'Author: {json_data["author"]["name"]}\n' \
           f'Created on: {json_data["created"]}\n' \
           f'Average review: {("No reviews for this question" if json_data["get_average_review"]["average"] == None else json_data["get_average_review"]["average"])}'

    return text


def my_questions(user_id) -> str:
    headers = {'Authorization': f'Token {config("auth")}'}
    link = f'http://127.0.0.1:8000/api/question/?user_id={user_id}'
    response = requests.get(link, headers=headers)
    json_data = json.loads(response.text)

    text = ''
    if len(json_data) > 0:
        for i in range(0, len(json_data)):
            text += 'id: ' + str(json_data[i]['id']) + ' - Question: ' + json_data[i]['title'] + ' - Created on: ' + json_data[i]['created'] + '\n'
    else:
        text = None

    return text


def update_points(name, points, id, question_id) -> None:
    headers = {'Authorization': f'Token {config("auth")}'}
    url = 'http://127.0.0.1:8000/api/users/'

    data = {
        'name': name,
        'score': points,
        'discord_id': id,
        'question_id': question_id,
    }
    request = requests.post(url, data, headers=headers)
    '''json_data = json.loads(request.text)
    print('update points json data', json_data)'''
    return


def get_ranking(message, author_id) -> str:
    msg = message.split(' ')
    leaderboard = ''

    if len(msg) > 1:
        if msg[1].isdigit():
            if int(msg[1]) < 1:
                return 'Number must be greater than zero'
            link = f'http://127.0.0.1:8000/api/users/?id={author_id}&param={msg[1]}'
        else:
            return 'Wrong format! $rank - Displaying my current ranking | $rank (number) - Displaying top players from 1 to number '
    else:
        link = f'http://127.0.0.1:8000/api/users/?id={author_id}'

    headers = {'Authorization': f'Token {config("auth")}'}
    response = requests.get(link, headers=headers)
    json_data = json.loads(response.text)
    position = 1

    if len(json_data) >= 1:
        for user in json_data:
            leaderboard += str(position) + '. ' + user['name'] + ' points: ' + str(user['score']) + '\n'
            position += 1
    else:
        return 'There is no users in ranking!'

    return leaderboard


def create_question(message, author_id, name) -> str or dict:
    content = message.content.replace('$create', '')
    msg = content.split('.')

    if int(msg[1]) not in list(range(1, 6)):
        return 'Points number must be in range from 1 to 5'
    if len(msg) < 6 or len(msg) > 9:
        return 'WRONG! You need at least 3 answers to your question (max 5 answers)!\nCorrect question template: [ EXAMPLE: $create how old are you?.2.14.16.21.3 (question: how old are you? - points: 2 - answers: 14, 16, 21 - correct answer: 3)\n($create [title].[points].[answers (multiple)].[correct answer]) ]'
    if not msg[1].isdigit():
        return 'ERROR! Question points must be a number (integer)!\nCorrect question template: [ EXAMPLE: $create how old are you?.2.14.16.21.3 (question: how old are you? - points: 2 - answers: 14, 16, 21 - numner of correct answer: 3(answer 21))\n($create [title].[points].[answers (multiple)].[correct answer]) ]'
    if not msg[-1].isdigit():
        return 'ERROR! Correct answer must be an number (integer)!\nCorrect question template: [ EXAMPLE: $create how old are you?.2.14.16.21.3 (question: how old are you? - points: 2 - answers: 14, 16, 21 - numner of correct answer: 3(answer 21))\n($create [title].[points].[answers (multiple)].[correct answer]) ]'
    if int(msg[-1]) > len(msg[2:-1]):
        return 'ERROR! Correct answer number cant be greater than the number of all answers!\nCorrect question template: [ EXAMPLE: $create how old are you?.2.14.16.21.3 (question: how old are you? - points: 2 - answers: 14, 16, 21 - numner of correct answer: 3(answer 21))\n($create [title].[points].[answers (multiple)].[correct answer]) ]'

    data = {
        'name': name,
        'author_id': author_id,
        'title': msg[0],
        'points': msg[1],
        'answers': msg[2:-1],
        'correct': msg[-1]
    }

    headers = {'Authorization': f'Token {config("auth")}'}
    link = 'http://127.0.0.1:8000/api/question/'
    response = requests.post(link, data=data, headers=headers)
    json_data = json.loads(response.text)

    return json_data


def delete_question(user_id, question_id) -> dict:
    link = f'http://127.0.0.1:8000/api/question/{question_id}/?user_id={user_id}'
    headers = {'Authorization': f'Token {config("auth")}'}
    response = requests.delete(link, headers=headers)
    json_data = json.loads(response.text)

    return json_data


def rate_question(question_id, rating, user_id, username) -> dict or str:
    if not str(question_id).isdigit() or not str(rating).isdigit():
        return '$rate (question_id) (rating from 1 to 5) - Rate question with given id'

    url = f'http://127.0.0.1:8000/api/question/{question_id}/'
    data = {
        'rating': rating,
        'user_id': user_id,
        'username': username
    }
    headers = {'Authorization': f'Token {config("auth")}'}
    response = requests.put(url, data=data, headers=headers)
    json_data = json.loads(response.text)

    if json_data['detail'] == 'Not found.':
        return 'Make sure you are using correct question id'

    return json_data


def my_reviews(user_id) -> str:
    url = f'http://127.0.0.1:8000/api/review/?id={user_id}'
    headers = {'Authorization': f'Token {config("auth")}'}
    response = requests.get(url, headers=headers)
    json_data = json.loads(response.text)
    print('my reviews json data', json_data)
    text = ''

    if json_data:
        for i in range(0, len(json_data)):
            text += 'REVIEW ID: ' + str(json_data[i]['id']) + ' --- RATING: ' + str(json_data[i]['stars']) + ' --- Question id: ' + str(json_data[i]['question']['id']) + ' --- Question title [' + json_data[i]['question']['title'] + ']\n'
    else:
        text = 'You have no reviews!'
    return text


def delete_review(user_id, question_id) -> dict:
    link = f'http://127.0.0.1:8000/api/review/{question_id}/?user_id={user_id}'
    headers = {'Authorization': f'Token {config("auth")}'}
    response = requests.delete(link, headers=headers)
    json_data = json.loads(response.text)

    return json_data


def profile(user_id) -> str:
    url = f'http://127.0.0.1:8000/api/users/profile_details/?id={user_id}'
    headers = {'Authorization': f'Token {config("auth")}'}
    response = requests.get(url, headers=headers)
    json_data = json.loads(response.text)

    if isinstance(json_data, dict):
        text = f"Name: {json_data['name']}\nScore: {json_data['score']}\nCreated questions: {json_data['questions_number']}\nCreated reviews: {json_data['reviews_number']}\nTotal attempts: {json_data['total_attempts']}\nSuccessful attempts: {json_data['successful_attempts']}\nEfficiency: {json_data['correct_rate']}%"
    else:
        text = json_data
    return text


def increase_attempts(user_id, username) -> None:
    url = f'http://127.0.0.1:8000/api/users/increase_attempts/?id={user_id}&name={username}'
    headers = {'Authorization': f'Token {config("auth")}'}
    response = requests.put(url, data={}, headers=headers)
    json_data = json.loads(response.text)
    return


def increase_successful_attempts(user_id) -> None:
    url = f'http://127.0.0.1:8000/api/users/increase_successful_attempts/?id={user_id}'
    headers = {'Authorization': f'Token {config("auth")}'}
    response = requests.put(url, data={}, headers=headers)
    json_data = json.loads(response.text)
    return
