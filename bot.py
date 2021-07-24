import discord
from decouple import config
from api_requests import (get_question, my_questions, update_points,
                          get_ranking, delete_question, create_question,
                          my_reviews, rate_question)
import asyncio

client = discord.Client()
token = config('token')


@client.event
async def on_message(message):

    if message.author == client.user:
        return

    if message.content.startswith('$random'):
        a, answer, points, question_id, average, author = get_question(message.author.id)

        if answer is not None:
            msg = f'Question id: {question_id}, created by: {author}\n--- Average stars: {average} \n\n {a}'
            await message.channel.send(msg)

            def check(m):
                return m.author == message.author and m.content.isdigit()

            try:
                guess = await client.wait_for('message', check=check, timeout=5.0)
            except asyncio.TimeoutError:
                return await message.channel.send('Time is up, you failed')

            if int(guess.content) == answer:
                user = guess.author
                msg = str(guess.author.name) + ' you got it +' + str(points) + 'points'
                await message.channel.send(msg)
                update_points(user, points, user.id, question_id)
            else:
                await message.channel.send('Wrong answer!')
        else:
            await message.channel.send('Theres no more questions to be solved')

    if message.content.startswith('$myquestions'):
        content = my_questions(message.author.id)
        print('my questions cointent', content)
        if content is not None:
            await message.channel.send(content)
        else:
            await message.channel.send('You dont have any questions')

    if message.content.startswith('$rank'):
        leaderboard = get_ranking(message.content, message.author.id)
        await message.channel.send(leaderboard)

    if message.content.startswith('$create'):
        name = message.author.name + message.author.discriminator
        msg = create_question(message, message.author.id, name)
        await message.channel.send(msg)

    if message.content.startswith('$delete'):
        msg = message.content.split(' ')
        print('delete question: message', msg)

        if len(msg) > 2 or len(msg) == 1:
            await message.channel.send("( $delete question_id ) is correct format for deleting questions")
        else:
            content = delete_question(message.author.id, int(msg[1]))
            print('delete content', content)
            await message.channel.send(content)

    if message.content.startswith('$myreviews'):
        content = my_reviews(message.author.id)
        await message.channel.send(content)

    if message.content.startswith('$rate'):
        msg = message.content.split(' ')
        if len(msg) == 3:
            content = rate_question(msg[1], msg[2], message.author.id, message.author.name)
            await message.channel.send(content)
        else:
            await message.channel.send("( $rate (question id) (0-5 rating) ) is correct format for deleting questions")

client.run(token)
