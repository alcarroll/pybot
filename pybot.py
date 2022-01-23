# bot.py
from discord.ext import commands
import os, random, asyncio, discord, pymysql, asyncio

from discord.ext import commands, tasks, commands
from dotenv import load_dotenv
#from discord.ext.commands import clean_content

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
PB_DBH = os.getenv('PYBOT_DB_HOST')
PB_DBU = os.getenv('PYBOT_DB_USER')
PB_DBP = os.getenv('PYBOT_DB_PASS')
PB_DBN = os.getenv('PYBOT_DB_NAME')

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


@bot.command(name='letterkenny', help='Responds with a random quote from Letterkenny.')
async def letterkenny(ctx):
    letterkenny_quotes = [
        'It\'s almost not worth thinkin about.',
        'Wish you weren\'t so awkward, bud',
        'Do what you love and you\'ll never work a day in your life.',
        'Pitter patter, let\'s get at\'er',
        'And I suggest you let that one marinate!',
        'You\’re made of spare parts, aren\’t ya, bud?',
	'There\'s a special place in heaven for animal lovers, that\'s what I always say',
        'I just don\'t think you have to pluralize those words',
        'FUCKING. EMBARASSING!',
        'FUCK YOU SHORESY',
        'Oh, I got so much time for sushi.',
        'Not my pig, not my farm.',
        'Not my forte.',
        'If I was a Dr. Seuss book, I’d be The Fat in the Hat.',
        'I see the muscle shirt came today. Muscles coming tomorrow?',
        'This eau de toilette is enchantingly refreshing on summer days like this.',
        'Yeah. Oh, hey, look at you, ground',
        'You wanna come to a super soft birthday party?',
        'Vomit on your mom\’s spaghetti, or whatever that talking singer says.',
        
    ]

    response = random.choice(letterkenny_quotes)
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
        # Only made a couple of insignificant tweaks so leaving original author in
    emb.set_author(name='Magic 8 ball', icon_url='https://www.horoscope.com/images-US/games/game-magic-8-ball-no-text.png')
    await ctx.send(embed=emb)

@bot.command(name='gamble', help='Try your luck!')
async def gamble(ctx):
    # Get username
    gambleuser = (ctx.message.author.name)
    # DB connection, gather user's current worth
    db = pymysql.connect( host=PB_DBH , user=PB_DBU , password=PB_DBP , database=PB_DBN )
    cursor = db.cursor()
    cursor.execute("SELECT MAX(worth) FROM users WHERE name LIKE %s", "%" + (str(gambleuser, )) + "%")
    row = cursor.fetchone()
    worth = row[0]
    # Determine win/lose and value
    gambleresult = random.choice(["(Win)", "(Lose)"])
    gamblevalue = random.randint(1, 1000)

    # Make sure they have money to spend
    if ( worth <= 0 ):
        emb = (discord.Embed(title="Sorry, you don't have any money.", description="You'll have to !work in order to gamble", colour=0xE80303))
    # Calculate win/loss and set emb    
    elif gambleresult == "(Win)":
        worth = (worth + gamblevalue)
        emb = (discord.Embed(title=str(gambleuser) + " gambles and wins: $" + str(gamblevalue),
                         description="They now have: $" + str(worth), colour=0xE80303))
    else:
        worth = (worth - gamblevalue)
        emb = (discord.Embed(title=str(gambleuser) + " gambles and loses : $" + str(gamblevalue),
                         description="They now have: $" + str(worth), colour=0xE80303))
    # Update DB and output    
    cursor.execute("UPDATE users SET worth='%s' WHERE name='%s' " % (worth, gambleuser))
    db.commit()
    await ctx.send(embed=emb)

@bot.command(name='work',  help='make some gambling cash')
async def work(ctx):
    # Get username
    workuser = (ctx.message.author.name)
    # Determine Overtime
    if random.randint(1, 100) < 30:
        overtime = (random.randint(20, 100))
    else:
        overtime = None
    # DB connection, get job list, select job    
    db = pymysql.connect( host=PB_DBH , user=PB_DBU , password=PB_DBP , database=PB_DBN )
    cursor = db.cursor()
    cursor.execute("SELECT MAX(worth) FROM users WHERE name LIKE %s", "%" + (str(workuser, )) + "%")
    row = cursor.fetchone()
    worth = row[0]
    cursor.execute("SELECT * FROM work")
    cursor.fetchall()
    max = cursor.rowcount
    jobnum = random.randint(1, max)
    cursor.execute("SELECT task FROM work where ID like'" + str(jobnum) + "';")
    jobtask = cursor.fetchone()
    job = jobtask[0]
    # Determine payout and set emb
    payout = random.randint(1, 500)
    if overtime == None:
        payout = payout
        worth = (worth + payout)
        emb = (discord.Embed(title=str(workuser) + " " + str(job) + " and made $" + str(payout), 
            description="They now have: $ " + str(worth), colour=0xE80303))
    else:
        payout = payout + overtime
        worth = (worth + payout)
        emb = (discord.Embed(title=str(workuser) + " " + str(job) + " and made $" + str(payout), 
            description="Including $" + str(overtime) + " from overtime!\nThey now have: $" + str(worth), colour=0xE80303))
    # Update DB and output    
    cursor.execute("UPDATE users SET worth='%s' WHERE name='%s' " % (worth, workuser))
    db.commit()
    await ctx.send(embed=emb)

# Better now but still could use improvement
@bot.command(name='networth', help='See how much cash everyone has')
async def networth(ctx):
    db = pymysql.connect( host=PB_DBH , user=PB_DBU , password=PB_DBP , database=PB_DBN )
    cursor = db.cursor()
    cursor.execute("SELECT name,worth FROM users")
    userlist = cursor.fetchall()
    for row in userlist:
        emb = discord.Embed(title=(row[0]), description=(row[1]), colour=0xE80303)
        await ctx.send(embed=emb)
        await ctx.send(str(row[0]) + " has $" + str(row[1])) 

@bot.command(name='thief', help='Hire the bot thief')
async def thief(ctx):
    thiefcaller = (ctx.message.author.name)
    #emb = (discord.Embed(title="OH NO! " + str(thiefcaller) + " envoked the bot thief!", colour=0xE80303))
    await ctx.send("**OH NO! " + str(thiefcaller) + " hired the bot thief!**")
    callergains = 0
    db = pymysql.connect( host=PB_DBH , user=PB_DBU , password=PB_DBP , database=PB_DBN )
    cursor = db.cursor()
    cursor.execute("SELECT name,worth FROM users")
    playerlist = cursor.fetchall()
    for row in playerlist:
        stolen = random.randint(1, 200)
        lossworth = (row[1]) - stolen
        gainworth = (row[1]) + stolen
        target = (row[0])
        if (target != thiefcaller):
            cursor.execute("UPDATE users SET worth='%s' WHERE name='%s' " % (lossworth, target))
            #cursor.execute("UPDATE users SET worth='%s' WHERE name='%s' " % (gainworth, thiefcaller))
            db.commit()
            await ctx.send("The bot theif stole $" + str(stolen) + " from " + str(target) + "!!")
            callergains = callergains + stolen

    thiefpay = random.randint(1, callergains)
    callernet  = callergains - thiefpay
    await ctx.send("**The bot thief stole $" + str(callergains) + " and charged " + str(thiefcaller) + " $" + str(thiefpay) + " for its work. " + str(thiefcaller) + " is now $" + str(callernet) + " richer!**")
    cursor.execute("SELECT MAX(worth) FROM users WHERE name LIKE %s", "%" + (str(thiefcaller, )) + "%")
    row = cursor.fetchone()
    callerworth = row[0]
    cursor.execute("UPDATE users SET worth='%s' WHERE name='%s' " % (callernet + callerworth, thiefcaller))
    db.commit()

@bot.command(name='fartroulette', help='Play Russian roulette, but with farts instead of bullets.')
async def fart_roulette(ctx):
    fart_roulette_results = [
        'Click. Whew, you dodged that one.',
        'Click. Your nose can live another day.',
        'Click. Safe this time!',
        'Click.',
        (   
            'PPPRRRRRRTTTTTFFFF!! OH THE HUMANITY!! '
            'FARRRRRRRRRRRRRT!! COUGH COUGH COUGH GAG!'
            'THHHHHHPPPPPPT! BOOOOOM! AAAAAAAAAAGH MAKE IT STOP!'
        ),
        'Click. Sniff Sniff. Oh, thank goodness.'
    ]
    
    response = random.choice(fart_roulette_results)
    await ctx.send(response)

bot.run(TOKEN)
