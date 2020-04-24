# bot.py
import os, random, asyncio, discord

from discord.ext import commands
from dotenv import load_dotenv
from discord.ext.commands import clean_content

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORT_GUILD')

client = discord.Client()

bot = commands.Bot(command_prefix='!')

@bot.command(name='99', help='Responds with a random quote from Brooklyn 99.')
async def nine_nine(ctx):
    brooklyn_99_quotes = [
        'I\'m the human form of the 100 emoji.',
        'Bingpot!',
        'Noice!',
        (
            'Cool. Cool cool cool cool cool cool, '
            'no doubt no doubt no doubt no doubt'
        ),
        'Ok, no hard feelings, but I hate you. Not jokeing. Bye.',
        'Sarge, with all due respect, I am gonna completely ignore everything you just said.',
        'Great, I\'d lke to see your 8-est dollar bottle of wine\, please.'
    ]
    
    response = random.choice(brooklyn_99_quotes)
    await ctx.send(response)

    
@bot.command(name='roll_dice', help='Simulates rolling dice.')
async def roll(ctx, number_of_dice: int, number_of_sides: int):
    dice = [
        str(random.choice(range(1, number_of_sides + 1)))
        for _ in range(number_of_dice)
    
    ]
    await ctx.send(', '.join(dice))


@bot.command(name='8ball', help='Ask the magic 8ball a question.')
async def eightball(ctx, *, ballInput):
    choiceType = random.choice(["(Affirmative)", "(Non-committal)", "(Negative)"])
    if choiceType == "(Affirmative)":
        prediction = random.choice(["It is certain ",
                                    "It is decidedly so ",
                                    "Without a doubt ",
                                    "Yes, defintiely ",
                                    "You may rely on it ",
                                    "As I see it, yes ",
                                    "Most likely ",
                                    "Outlook good ",
                                    "Yes ",
                                    "Signs point to yes "]) + ":8ball:"

        emb = (discord.Embed(title="Question: {}".format(ballInput), colour=0x3be801, description=prediction))
    elif choiceType == "(Non-committal)":
        prediction = random.choice(["Reply hazy try again ",
                                    "Ask again later ",
                                    "Better not tell you now ",
                                    "Cannot predict now ",
                                    "Concentrate and ask again "]) + ":8ball:"
        emb = (discord.Embed(title="Question: {}".format(ballInput), colour=0xff6600, description=prediction))
    elif choiceType == "(Negative)":
        prediction = random.choice(["Don't count on it ",
                                    "My reply is no ",
                                    "My sources say no ",
                                    "Outlook not so good ",
                                    "Very doubtful "]) + ":8ball:"
        emb = (discord.Embed(title="Question: {}".format(ballInput), colour=0xE80303, description=prediction))
    emb.set_author(name='Magic 8 ball', icon_url='https://www.horoscope.com/images-US/games/game-magic-8-ball-no-text.png')
    await ctx.send(embed=emb)

bot.run(TOKEN)
