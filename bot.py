import discord
from decouple import config
from api_requests import get_question, my_questions, update_points, get_ranking
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

client.run(token)
