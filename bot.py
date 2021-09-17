import discord
import asyncio
from decouple import config
from api_requests import *


client = discord.Client()
token = config('token')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$commands'):
        content = '**$random** - Picks a random question from the database\n\n' \
                  '**$question (question_id)** - Show question details\n\n' \
                  '**$rank** - Display my current ranking | **$rank (number)** - Display top players from 1 to number\n\n' \
                  '**($create [title].[points for correct answer (from 1 to 5)].[answers (minimum 3 - maximum 5)].[correct answer (1 - number of answers)])** - ' \
                  'Create question that will be added to the database,\nEXAMPLE: $create What is the earth diameter?.2.6000km.5200km.6400km.6900km.3 (2 points for correct answer and third question is correct)\n\n' \
                  '**$myquestions** - Display list of all questions I added\n\n' \
                  '**$delete (question_id)** - Delete question with given id (if you are the author)\n\n' \
                  '**$rate (question_id) (rating from 1 to 5)** - Rate question with given id\n\n' \
                  '**$myreviews** - Display list of my reviews\n\n' \
                  '**$reviewdelete (review_id)** - Delete review with given id (if you are the author)\n\n' \
                  '**$profile** - Display my profile stats\n\n'
        await message.channel.send(content)

    if message.content.startswith('$random'):
        a, answer, points, question_id, average, author = get_question(message.author.id)

        if answer is not None:
            msg = f'**Question id: {question_id}, created by: {author}\n--- Average stars for this question: {("No reviews for this question yet" if average == None else average)} \n\n {a}**'
            await message.channel.send(msg)

            def check(m):
                return m.author == message.author and m.content.isdigit()

            try:
                guess = await client.wait_for('message', check=check, timeout=10.0)
            except asyncio.TimeoutError:
                increase_attempts(message.author.id, message.author)
                return await message.channel.send('**Time is up, you failed**')

            if int(guess.content) == answer:
                user = guess.author
                msg = '`' + str(guess.author.name) + ' you got it +' + str(points) + ' points`'
                await message.channel.send(msg)
                update_points(user, points, user.id, question_id)
                increase_successful_attempts(message.author.id)
            else:
                await message.channel.send('**Wrong answer!**')
            increase_attempts(message.author.id, message.author)
        else:
            await message.channel.send('**Theres no questions to be solved**')

    if message.content.startswith('$question'):
        msg = message.content.split(' ')

        if len(msg) > 2 or len(msg) == 1:
            await message.channel.send("( $question question_id ) is correct format for displaying question details")
        else:
            content = question_details(msg[1])
            await message.channel.send(content)

    if message.content.startswith('$myquestions'):
        content = my_questions(message.author.id)
        text = f'```{content}```'

        if content is not None:
            await message.channel.send(text)
        else:
            await message.channel.send('```You dont have any questions```')

    if message.content.startswith('$rank'):
        leaderboard = get_ranking(message.content, message.author.id)
        text = f'```{leaderboard}```'
        await message.channel.send(text)

    if message.content.startswith('$create'):
        name = message.author
        msg = create_question(message, message.author.id, name)
        text = f'```{msg}```'
        await message.channel.send(text)

    if message.content.startswith('$delete'):
        msg = message.content.split(' ')

        if len(msg) > 2 or len(msg) == 1:
            await message.channel.send("( $delete question_id ) is correct format for deleting questions")
        else:
            if not str(msg[1]).isdigit():
                await message.channel.send('$rate (question_id) (rating from 1 to 5) - Rate question with given id')
            else:
                content = delete_question(message.author.id, int(msg[1]))
                text = f'`{content}`'
                await message.channel.send(text)

    if message.content.startswith('$myreviews'):
        content = my_reviews(message.author.id)
        text = f'```{content}```'
        await message.channel.send(text)

    if message.content.startswith('$rate'):
        msg = message.content.split(' ')

        if len(msg) == 3:
            content = rate_question(msg[1], msg[2], message.author.id, message.author.name)
            text = f'`{content}`'
            await message.channel.send(text)
        else:
            await message.channel.send("**$rate (question_id) (rating from 1 to 5) - Rate question with given id**")

    if message.content.startswith('$reviewdelete'):
        msg = message.content.split(' ')

        if len(msg) > 2 or len(msg) == 1:
            await message.channel.send("( $deletereview review_id ) is correct format for deleting reviews")
        else:
            content = delete_review(message.author.id, int(msg[1]))
            await message.channel.send(content)

    if message.content.startswith('$profile'):
        content = profile(message.author.id)
        text = f'```{content}```'
        await message.channel.send(text)

client.run(token)
