#TODO:
# runs in 3.11.0 64-Bit Python Installation

'''
Hello! This is BotBot, a programming project turned functional Discord bot made entirely by Jacob Smith.
Development started with a rough prototype in November of 2022, where he could only respond to BBhello with 'Hello!'.
Since then, it has become a character in my friend communities, known for hilarious timings, funny responses,
and wide range of functionality. The highlighs of his abilities are:
    Can play games such as hangman, number guessing, and word of the day
    Virtual currency of "BotCoin", which can be earned, spent, and transferred
    Activity tracking, such as a users most used words, most listened to songs, etc.
    Botify wrapped, showing an approximation of a certain users data in a Discord-friendly embed
    Tens of commands of miscellaneous functionality, such as the magic 8 ball, adding animal pics, and making suggestions

There is over a years worth of experience and progress in this project, and it has become a passion of mine.
My friends ask to add him to every new server we make, and they have been loving it as much as I have.

Things i would do differently if i started over:
    Turn all commands into their own functions using the updated discord api
    Possibly use Java/JS
    organize ahead of time instead of re-organizing every few months
    Isolate large text blocks into separate files in \\data
'''

#imports
import os
from os import path
import discord
from discord.ui import Button, View, Select
import asyncio
from datetime import datetime, date, timedelta
from pytz import timezone
import pytz
import json
from heapq import nlargest
import random
from discord.ext import commands
from discord.utils import get
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import urllib.request
import requests
from io import BytesIO
import requests
from bs4 import BeautifulSoup
from achievements import checkAchievements

#IMPORTANT!! PUT YOUR BOT TOKEN HERE!!
TOKEN = ""

bot = commands.Bot(command_prefix='$', intents=discord.Intents.all())

tz = timezone('EST')

client = discord.Client(intents=discord.Intents.all())

voice = None

cwd = f'{os.getcwd()}\\'

#####################################################################################

remindersOn = False
#List of all accepted commands
commandList = [
    'BBhello', 'BBmywords', 'BBhelp', 'BBmoney', 'BBshop', 'BBmygames',
    'BBmymusic', 'BBmyactivity', 'BBmystreams', 'BBmystreamgames', 'BBmywatching', 'BBmyalbums', 'BBmycomps',
    'BBexp', 'BBsuggest','BBpay', 'BBadmin', 'BBwrapped', 'BBguessnum', 'BBfetchpfp', 'BBaddaduck',
    'BBaddarat', 'BBguessword','BBwordhint', 'BBhangman', 'BBquithangman', 'BBblur', 'BBsnoop', 'BBmycommands', 'BBmymoney', 
    'BBfarmrpg', 'BBachievements', 'BBmyachievements', 'BBscavengerhunt', 'BBreveal', 'BB?', 'BBtoday', 'BBbirthday', 'BBheadsup'
]
#Ignore these words for word counting
wordsToIgnore = [
    'bbpay', 'bbsuggest', 'bbexp', 'bbmystreams', 'bbmywatching', 'bbmycomps', 'bbadmin'
    'bbmymusic', 'bbmyactivity', 'bbshop', 'bbcomeback', 'bbmoney', 'bbhelp',
    'bbhello', 'bbmywords', 'bbmygames', 'i', 'a', 'so', 'and', 'to', 'for',
    'by', 'at', 'in', 'of', 'on', 'with', 'the', 'are', 'he', 'she', 'it',
    'they', 'as', 'was', 'is', 'you', 'like', 'um', 'im', 'that', 'are', 'if', 'just', 'its', 'or',
    'bbgetwords', 'bbgetmusic','bbgetgames','bbreward',
    'bbgetexp','bbaddexp','bbgetbal','bballwords', 'bballmusic', 'bballactivities',
    'bbeconomy', 'bbwrapped', 'bbguessnum', 'bbfetchpfp','bbgetstreams', 'bbgetstreamgames', 'bbmystreamgames',
    'bbaddaduck', 'bbaddarat', 'bbaddapanda', 'bbaddapet', 'bbmyalbums', 'bbguessword', 'bbwordhint', 'bbhangman',
    'bbquithangman', 'BBblur', 'bbsnoop', 'bbmycommands', 'bbmymoney', 'bbfarmrpg', 'bbachievements', 'bbmyachievements',
    'bbscavengerhunt', 'bbreveal', 'bb?', 'bbtoday', 'bbbirthday', 'bbheadsup'
]
#Words to look out for hidden in messages
funny = [
    'bitcoin', 'computer', 'github', 'intern', 'algorithm', 'binary', 'byte',
    'cache', 'code', 'compiler', 'database', 'debugging', 'ethernet', 'firewall', 
    'gigabyte', 'hash', 'html', 'input', 'java', 'kernel', 'lan', 'macro', 'network', 
    'opcode', 'pixel', 'queue', 'router', 'software', 'terminal', 'unicode', 'virtualization', 
    'wi-fi', 'xss', 'yaml'
]
#Admin-only commands
adminCommands = [
    'BBgetwords', 'BBgetmusic','BBgetgames','BBreward',
    'BBgetexp','BBaddexp','BBgetbal','BBallwords', 'BBallmusic', 'BBallactivities',
    'BBeconomy', 'BBfarmrpg'
]
#BotCoin shop
bbshop = {
    "BBcomeback" : [20],
    "BBwordhint" : [40],
    "BBhangman" : [100],
    "BBsnoop" : [20],
    "BBblur" : [5]
}
#List of achievements + descriptions
achievementlist = {
    "Knowledgeable" : "Have 100 unique words.",
    "Linguist" : "Have 1000 unique words.",
    "Thesaurus" : "Have 5000 unique words.",
    "Conversational" : "Have 1000 total words.",
    "Talkative" : "Have 10000 total words.",
    "Chatterbox" : "Have 100000 total words.",
    "Greeter" : "Used the BBhello command.",
    "Nosy" : "Used the BBsnoop command.",
    "CIA" : "Used the BBsnoop command 50 times.",
    "Blurry" : "Used the BBblur command.",
    "Share the Wealth" : "Used the BBpay command.",
    "Face Snatcher" : "Used the BBfetchpfp command.",
    "Idea Generator" : "Used the BBsuggest command.",
    "Wrapper" : "Used the BBwrapped command.",
    "Contributor" : "Used any of the BBadda___ commands.",
    "Animal Lover" : "Used any of the BBadda___ commands 10 times.",
    "Zoologist" : "Used any of the BBadda___ commands 50 times.",
    "Listener" : "Link your Spotify and listen to a song.",
    "Sound Enjoyer" : "Link your Spotify and listen to music for 10 hours.",
    "Music Freak" : "Link your Spotify and listen to music for 50 hours.",
    "Take Off Your Headphones" : "Link your Spotify and listen to music for 100 hours.",
    "Gamer" : "Played a game.",
    "It's Just a Hobby" : "Played games for 5 hours.",
    "Take a break" : "Played games for 10 hours.",
    "You May Need Help" : "Played games for 50 hours.",
    "Touch Grass" : "Played games for 100 hours.",
    "In a Simulation" : "Played games for 1000 hours.",
    "Pocket Change" : "Have 100 BotCoin in your wallet.",
    "The 1%" : "Have 1000 BotCoin in your wallet.",
    "The 0.1%" : "Have 5000 BotCoin in your wallet.",
    #"How'd that get in there?" : "Get Slothed.",
    "Gambling Man" : "Gamble and win once.",
    "Losing Streak" : "Gamble and lose five games.",
    "I Don't Have a Problem" : "Gamble and wager a total of 1000 BotCoin.",
    "Rehab" : "Gamble on 50 games.",
    "Escapee" : "Play and win a game of Hangman.",
    "Serial Gallows Avoider" : "Play and win a game of Hangman 20 times.",
    "Stay Down" : "Play and lose a game of Hangman 20 times.",
    "So Close" : "Guess the Word of the day incorrectly.",
    "Lucky Guess" : "Guess the Word of the day correctly.",
    "Smart Cookie" : "Guess the word of the day correctly 5 times",
    # "Insightful" : "Ask the magic 8 ball a question."
}

totalAchievements = len(achievementlist)
#If someone says 'ty botbot' or some variation, replies with these phrases
tybotbot = [
    "Chill. We're just friends.",
    "Rightio",
    "Aight",
    "np bro",
    "anytime",
    "you're welcome buddy",
    "yeah sure",
    "gotchu homeboy",
    "That's the name don't wear it out",
    "shut up smelly",
    "sorry i have a bf",
    "sorry i have a gf",
    "sorry i have a partner",
    "\"tY bOtBOt\" bro youre talking to a discord bot rn",
    "i love you. platonically",
    "thanks cutie",
    "yeah yeah sure np",
    "no. thank YOU.",
    "my pleasure",
    "uh huh",
    "yeah sure just got a quick question for you about that last interaction\nhttps://media.discordapp.net/attachments/908269843973828628/1107706115942256741/BotBotpfp_1_1.jpg?width=702&height=675"
]
#For playing the game 'Heads up', these include the categories and their answers.
headsupCategories = {
    'Celebrities' : ["🎥",["Miley Cyrus", "Kim Kardashian", "Kayne West", "Margaret Thatcher", "George Washington",
                            "Ghandi", "Nelson Mandela", "Christopher Columbus", "Justin Beiber", "Lady Gaga",
                            "Katy Perry", "Justin Timberlake", "Jay Leno", "David Letterman", "Elle McPherson",
                            "Jennifer Aniston", "Donald Duck", "Pluto", "Goofy", "Johnny Depp", "Brittney Spears",
                            "Paris Hilton", "Hugh Jackman", "Vladimir Putin", "Daniel Radcliffe", "David Beckham",
                            "Madonna", "Eminem", "Matt Damon", "Jack Nicholson", "Kevin Spacey", "Kylie Minogue",
                            "Roger Federer", "Andrew Murray", "Serena Williams", "Brad Pitt", "Mickey Mouse",
                            "Simon Cowell", "Ludwig Beethoven", "Warren Buffett", "Lewis Carroll",
                            "Queen Elizabeth II", "Charles Darwin", "Albert Einstein", "Henry Ford", "Bill Gates",
                            "Steve Jobs", "Vincent van Gogh", "Thomas Jefferson", "Stanley Kubrik", 
                            "Charles Lindbergh", "Courtney Love", "Kurt Cobain", "Michelangelo", "Amadeus Mozart", 
                            "Sir Isaac Newton", "George Orwell", "Andy Warhol", "Orson Welles", "Leonardo Da Vinci", 
                            "Walt Disney", "Abraham Lincoln", "William Shakespeare", "Martin Luther King", 
                            "John F Kennedy", "Princess Diana", "Mother Teresa", "Thomas Edison", "Benjamin Franklin", 
                            "Neil Armstrong", "Napoleon", "Elvis Presley", "Mohammad Ali", "Marilyn Monroe", 
                            "Pablo Picasso", "Charles Dickens", "Cleopatra", "John Lennon", "Michael Jordan", 
                            "Mark Twain", "Nicole Kidman", "Barack Obama", "Robert Pattison", "Hugh Heffner", 
                            "JK Rowling", "Bill Clinton", "Elizabeth Taylor", "Tom Cruise", "Clint Eastwood", 
                            "Alfred Hitchcock", "Stephen Hawking", "Tom Hanks", "Oprah Winfrey", "Beyonce", 
                            "Hilary Clinton", "Dr Suess", "Ray Charles", "Sean Connery", "Julia Roberts", "Pele", 
                            "Meryl Streep", "Helen Keller", "Robin Williams", "Steve Martin", "Fred Astaire", 
                            "Whoopi Goldberg", "Jane Austen", "Bob Hope", "Jessica Simpson", "Frank Lloyd Wright", 
                            "Pamela Anderson", "Susan Boyle", "Mae West", "Snoopy", "Jim Carrey", "Michael J Fox"]],
    'Musicals' : ["🎶",["Sweeney Todd", "Rent", "Miss Saigon", "Matilda the Musical", "The Book of Mormon", 
                        "Blood Brothers", "West Side Story", "The Phantom of the Opera", "Wicked", "Les Misérables", 
                        "Guys & Dolls", "Priscilla Queen of the Desert", "Jesus Christ Superstar", "Once", "Carousel", 
                        "Cats", "From Here to Eternity", "Billy Elliot", "Cabaret", "Company", "Hairspray", 
                        "Merrily We Roll Along", "My Fair Lady", "Evita", "Jersey Boys", "Legally Blonde", 
                        "Sunset Boulevard", "The Lion King", "Chess", "Chicago", "Gypsy", "Hair", "The Sound of Music", 
                        "Spring Awakening", "Starlight Express", "Sunday in the Park with George", "Into the Woods", 
                        "The Producers", "Top Hat", "A Chorus Line", "A Little Night Music", "Avenue Q", 
                        "Love Never Dies", "Mary Poppins", "Oklahoma", "Oliver!", "Chitty Chitty Bang Bang", 
                        "Crazy For You", "Fiddler on the Roof", "Ghost", "Hello Dolly", "Kiss Me Kate", 
                        "La Cage Aux Folles", "Next to Normal", "Parade", "Return to the Forbidden Planet", 
                        "Rock of Ages", "The King & I", "The Rocky Horror Show", "We Will Rock You", "42nd Street", 
                        "A Funny Thing Happened on the Way to the Forum", "The Light Princess", "Betty Blue Eyes", 
                        "Charlie and the Chocolate Factory", "Jerry Springer – The Opera", 
                        "Joseph and the Amazing Technicolor Dreamcoat", "London Road", "Notre Dame Du Paris", 
                        "Ragtime", "Shrek", "Urinetown", "Sister Act", "Anything Goes", "Sunshine on Leith", 
                        "Singin' in the Rain", "American Psycho", "Fame", "The Commitments", "Let it Be", "MAMMA MIA!", 
                        "The Lord of the Rings", "I Can't Sing", "Newsies", "Candide", "Pippin", "South Pacific", 
                        "Putting it Together", "Saturday Night Fever", "The Drowsy Chaperone", "Taboo", "Soul Sister", 
                        "Hedwig and the Angry Inch", "The Music Man", "Reefer Madness", "Tommy", "The Threepenny Opera", 
                        "Scrooge the Musical", "Showboat", "Children of Eden"]],
    'Animals' : ["🐶",["Dog","Cow","Cat","Horse","Donkey","Tiger","Lion","Panther","Leopard","Cheetah","Bear","Elephant",
                       "Polar bear","Turtle","Tortoise","Crocodile","Rabbit","Porcupine","Hare","Hen","Pigeon","Albatross",
                       "Crow","Fish","Dolphin","Frog","Whale","Alligator","Eagle","Flying squirrel","Ostrich","Fox","Goat",
                       "Jackal","Emu","Armadillo","Eel","Goose","Arctic fox","Wolf","Beagle","Gorilla","Chimpanzee",
                       "Monkey","Beaver","Orangutan","Antelope","Bat","Badger","Giraffe","Hermit Crab","Giant Panda",
                       "Hamster","Cobra","Hammerhead shark","Camel","Hawk","Deer","Chameleon","Hippopotamus","Jaguar",
                       "Chihuahua","King Cobra","Ibex","Lizard","Koala","Kangaroo","Iguana","Llama","Chinchillas","Dodo",
                       "Jellyfish","Rhinoceros","Hedgehog","Zebra","Possum","Wombat","Bison","Bull","Buffalo","Sheep",
                       "Meerkat","Mouse","Otter","Sloth","Owl","Vulture","Flamingo","Racoon","Mole","Duck","Swan","Lynx",
                       "Monitor lizard","Elk","Boar","Lemur","Mule","Baboon","Mammoth","Blue whale","Rat","Snake","Peacock",]],
    'Adult Stuff' : ["🔞",[]],
}
#####################################################################################

#When someone updates their activity i.e. game or custom status, record status
@client.event
async def on_presence_update(before, after):
    # print('presence detected')
    if before.bot or after.bot:
        return
    with open(f'{cwd}data\\users.json', 'r') as f:
        users = json.load(f)

    await update_data(users, before)
    if not 'lastAct' in users[str(before.id)]:
        users[str(before.id)]['lastAct'] = 0
    if users[str(before.id)]['lastAct'] == str(after.activities):
        # print(users[str(before.id)]['lastAct'])
        users[str(before.id)]['lastAct'] = str(after.activities)
        return
    users[str(before.id)]['lastAct'] = str(after.activities)
    if before.activity != None:
        now = datetime.now(tz)
        for activity in before.activities:
            if activity in after.activities:
                # print(activity)
                continue
            time = (now - activity.created_at).total_seconds()
            # print(time)
            await update_activities(users, before.id, activity, time)
    #Save data
    with open(f'{cwd}data\\users.json', 'w') as f:
        json.dump(users, f)


#####################################################################################

#When BotBot starts up, copy user data to a safe file in case of corruption
        #number of corruptions so far: 9
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    await client.change_presence(activity=discord.Game('Your mom || BBhelp'))
    for i in range(100):
        with open(f'{cwd}data\\users.json', 'r') as f:
            users = json.load(f)
        with open(f'{cwd}data\\usersbackup.json', 'r') as f:
            usersbackup = json.load(f)
        usersbackup = users
        me = await client.fetch_user('323518323679559721')
        # await me.send('Backed up. Maybe.')
        with open(f'{cwd}data\\usersbackup.json', 'w') as f:
            json.dump(usersbackup, f)
        #Repeat every 24 hours or on re-startup
        await asyncio.sleep(24*60*60)


#####################################################################################

#Almighty message reader! Checks for commands and all other functionality.
@client.event
async def on_message(message):
    with open(f'{cwd}data\\wotd.json', 'r') as f:
        wotd = json.load(f)
    if message.author == client.user:
        return
    if message.author.id == (713586207119900693) and message.channel.id == (1038508453875945514):
        ppl = message.guild.members
        for people in ppl:
            for role in people.roles:
                if role.name == "bottom":
                    await people.remove_roles(role)
                    break
        #Word of the day detection
        if wotd['done'] == 1:
            for player in wotd['players']:
                wotd['players'][player]['today'] = 0
            wotd['done'] = 0
            wotd['lettershinted'] = []
            rand = random.randrange(0, (len(wotd['words']) - 1))
            wotd['wotd'] = wotd['words'].pop(rand)
            with open(f'{cwd}data\\wotd.json', 'w') as f:
                        json.dump(wotd, f)
    if message.author.bot:
        return
    with open(f'{cwd}data\\users.json', 'r') as f:
        users = json.load(f)
    with open(f'{cwd}data\\hm.json', 'r') as g:
        hm = json.load(g)
    with open(f'{cwd}data\\guessnum.json', 'r') as h:
        guessnum = json.load(h)
    #If not in DM's, display achievements earned
    if message.guild != None:
        out = checkAchievements(users, hm, guessnum, wotd, message.author.id)
        if out != "":
            print(out)
            file = await generateAchievement(out, message.author.id, message.guild)
            await message.channel.send(f"Congrats <@{message.author.id}>! You've earned the '{out}' Achievement!", file = file)
            with open(f'{cwd}data\\users.json', 'w') as f:
                json.dump(users, f)
    #updates per message
    await update_data(users, message.author)
    await add_experience(users, message.author, 1)
    await update_words(users, message.author, message.content)
    await funny_word_check(users, message.author, message.channel,
                           message.content)
    #If word of the day not completed, check if theres a winner
    if wotd['done'] == 0:
        await check_wotd(message, wotd['wotd'])

    #For my friend kate <3
    if message.author.id == 759092826658570260:
      rand = random.randrange(0, 50)
      if rand <= 1:
        await message.channel.send("shut up kate.")

#========Animal command keywords - display requested animal==========#
#####################################################################################

    if "duck" in message.content.lower() and not message.content.lower() == "/duck" and not message.content.startswith("BB") and not message.content.startswith("https"):
        if await get_slothed_lmao(message) == True:
            return
        with open(f'{cwd}ducks.json', 'r') as f:
          ducks = json.load(f)
        rand = random.randrange(0, len(ducks["ducks"]))
        await message.channel.send(ducks["ducks"][rand])
        await message.channel.send("**QUACK**")
        with open(f'{cwd}ducks.json', 'w') as f:
                json.dump(ducks, f)

#####################################################################################

    if message.content.lower().startswith("rat") and not message.content.lower() == "/rat" and not message.content.startswith("BB") and not message.content.startswith("https"):
        if await get_slothed_lmao(message) == True:
            return
        with open(f'{cwd}data\\rats.json', 'r') as f:
          rats = json.load(f)
        rand = random.randrange(0, len(rats["rats"]))
        await message.channel.send(rats["rats"][rand])
        await message.channel.send("**SQUEEK**")
        with open(f'{cwd}data\\rats.json', 'w') as f:
                json.dump(rats, f)

#####################################################################################

    if message.content.lower().startswith("panda") and not message.content.lower() == "/panda" and not message.content.startswith("BB") and not message.content.startswith("https"):
        if await get_slothed_lmao(message) == True:
            return
        with open(f'{cwd}data\\redpanda.json', 'r') as f:
          redpanda = json.load(f)
        rand = random.randrange(0, len(redpanda["redpandas"]))
        await message.channel.send(redpanda["redpandas"][rand])
        await message.channel.send("**PANDA NOISE**")
        with open(f'{cwd}data\\redpanda.json', 'w') as f:
                json.dump(redpanda, f)

#####################################################################################

    if message.content.lower().startswith("frog") and not message.content.lower() == "/frogs" and not message.content.startswith("BB") and not message.content.startswith("https"):
        if await get_slothed_lmao(message) == True:
            return
        with open(f'{cwd}data\\frogs.json', 'r') as f:
          frogs = json.load(f)
        rand = random.randrange(0, len(frogs["frogs"]))
        await message.channel.send(frogs["frogs"][rand])
        await message.channel.send("**RIBBIT**")
        with open(f'{cwd}data\\frogs.json', 'w') as f:
                json.dump(frogs, f)

#####################################################################################

    if message.content.lower().startswith("pet") and not message.content.lower() == "/pet" and not message.content.startswith("BB") and not message.content.startswith("https"):
        if await get_slothed_lmao(message) == True:
            return
        with open(f'{cwd}data\\pets.json', 'r') as f:
          pets = json.load(f)
        rand = random.randrange(0, len(pets["pets"]))
        await message.channel.send(pets["pets"][rand])
        await message.channel.send("**PET NOISE**")
        with open(f'{cwd}data\\pets.json', 'w') as f:
                json.dump(pets, f)

#####################################################################################

    if ('ty botbot') in message.content.lower() or ('thank you botbot') in message.content.lower() or 'thanks botbot' in message.content.lower():
        rand = random.randrange(0, len(tybotbot))
        reply = tybotbot[rand]
        await message.channel.send(reply)

#####################################################################################

    if 'botbot' in message.content.lower() and 'ty' not in message.content.lower() and 'thank' not in message.content.lower():
        await message.channel.send('that\'s me')

#####################################################################################

    #The very first command! Says hello back.
    if message.content.startswith('BBhello'):
        await message.channel.send('Hello!')

#####################################################################################

    if 'marvin' in message.content.lower():
        await message.reply('That\'s not my name man')

#####################################################################################
    #Botcoin shop with all
    if message.content.startswith('BBshop'):
        select = Select( 
            placeholder = "Choose a command to learn more:",
            options = [
                discord.SelectOption(label = "BBcomeback", emoji = "🎙"),
                discord.SelectOption(label = "BBwordhint", emoji = "🔍"),
                discord.SelectOption(label = "BBhangman", emoji = "👨‍💼"),
                discord.SelectOption(label = "BBsnoop", emoji = "🕵️‍♀️"),
                discord.SelectOption(label = "BBblur", emoji = "💩")
            ]
        )
        view = discord.ui.View(timeout=None)
        view.add_item(select)
        await message.channel.send( 'Hey there! This is the BotShop\nSelect a reward to learn about:', view = view)
        async def my_callback(interaction):
            embed = discord.Embed(
            title = f'What is {select.values[0]}',
            description = 'Let\'s take a look!',
            color = discord.Color.blue()
        )
            comm = select.values[0]
            if comm == "BBcomeback":
                embed.add_field(name = "Description", value = "BBcomeback puts the only non-banned discord song in the chat!", inline = False)
                embed.add_field(name = "Price", value = f"{bbshop[comm][0]} Botcoin", inline = False)
                embed.add_field(name = "Usage", value = "BBcomeback", inline = False)
            if comm == "BBwordhint":
                embed.add_field(name = "Description", value = "BBwordhint Gives you a hangman style hint for word of the day!", inline = False)
                embed.add_field(name = "Price", value = f"{bbshop[comm][0]} Botcoin", inline = False)
                embed.add_field(name = "Usage", value = "BBwordhint", inline = False)
            if comm == "BBhangman":
                embed.add_field(name = "Description", value = "BBhangman lets you play Hangman! If you guess the word before you lose, you win 150 Botcoin!", inline = False)
                embed.add_field(name = "Price", value = f"{bbshop[comm][0]} Botcoin", inline = False)
                embed.add_field(name = "Usage", value = "BBhangman", inline = False)
            if comm == "BBsnoop":
                embed.add_field(name = "Description", value = "BBsnoop lets you snoop on another person\'s stats!", inline = False)
                embed.add_field(name = "Price", value = f"{bbshop[comm][0]} Botcoin", inline = False)
                embed.add_field(name = "Usage", value = "BBsnoop", inline = False)
            if comm == "BBblur":
                embed.add_field(name = "Description", value = "BBblur lets you enter a prompt and make a blurry image!", inline = False)
                embed.add_field(name = "Price", value = f"{bbshop[comm][0]} Botcoin", inline = False)
                embed.add_field(name = "Usage", value = "BBblur [prompt]", inline = False)
            await interaction.response.send_message(f'you chose {select.values[0]}.', ephemeral = True, embed = embed)
        select.callback = my_callback

#====Stat checking - fan favorites====#
#####################################################################################

    if message.content.startswith('BBmywords'):
        out = await user_word_leaderboard(users, message.author, message.channel)
        await message.channel.send(out)

#####################################################################################

    if message.content.startswith('BBmoney') or message.content.startswith('BBmymoney'):
        await check_bal(users, message.author, message.channel)

#####################################################################################

    if message.content.startswith('BBmymusic'):
        out = await activity_leaderboard(users, message.author, message.channel,
                                   'artists')
        await message.channel.send(out)

#####################################################################################

    if message.content.startswith('BBmygames'):
        out = await activity_leaderboard(users, message.author, message.channel,
                                   'playing')
        await message.channel.send(out)

#####################################################################################

    if message.content.startswith('BBmyactivity'):
        out = await activity_leaderboard(users, message.author, message.channel,
                                   'custom')
        await message.channel.send(out)

#####################################################################################

    if message.content.startswith('BBmywatching'):
        out = await activity_leaderboard(users, message.author, message.channel,
                                   'watching')
        await message.channel.send(out)

#####################################################################################

    if message.content.startswith('BBmystreams'):
        out = await activity_leaderboard(users, message.author, message.channel,
                                   'streaming')
        await message.channel.send(out)

#####################################################################################

    if message.content.startswith('BBmystreamgames'):
        out = await activity_leaderboard(users, message.author, message.channel,
                                   'streamgames')
        await message.channel.send(out)

#####################################################################################

    if message.content.startswith('BBmycomps'):
        out = await activity_leaderboard(users, message.author, message.channel,
                                   'competing')
        await message.channel.send(out)

#####################################################################################

    if message.content.startswith('BBmytracks'):
        out = await activity_leaderboard(users, message.author, message.channel,
                                   'tracks')
        await message.channel.send(out)

#####################################################################################

    if message.content.startswith('BBfetchpfp'):
        args = message.content.split()
        if len(args) == 1:
            await message.channel.send("User doesn't exist or has a default profile picture.")
        else:
            if args[1].startswith('<@'):
                args[1] = args[1][2:-1]
            User = await client.fetch_user(args[1])
            if User.avatar == None:
                await message.channel.send("User doesn't exist or has a default profile picture.")
            else:
                await message.channel.send(User.avatar)

#####################################################################################

    if message.content.startswith('BBachievements') or message.content.startswith('BBmyachievements'):
        #stats?
        if(not "achievements" in users[str(message.author.id)]) or len(users[str(message.author.id)]["achievements"]) == 0:
            await message.channel.send("You don't have any achievements yet!")
        else:
            embed = discord.Embed(
                title = f'{message.author.display_name}\'s Achievements',
                description = f'You\'ve earned {len(users[str(message.author.id)]["achievements"])} / {totalAchievements} achievements',
                color = discord.Color.blue()
            )
            for ach in users[str(message.author.id)]["achievements"]:
                percent = getAchPercent(users, ach)
                embed.add_field(name = ach, value = f'{percent} of people have this achievement.', inline = False)
            #print all achievements that someone has
            await message.channel.send(embed = embed)

#####################################################################################

    if message.content.startswith('BBexp'):
        await message.channel.send(
            f'<@{message.author.id}> has {get_exp(users, message.author)} exp. Can\'t really do anything with that, but neat!'
        )

#####################################################################################
    #Never got to implement the hunt, got too many pages removed ):
    if message.content.startswith('BBscavengerhunt'):
        await message.delete()
        await message.channel.send("This isn\'t ready yet.. But stay tuned 😉")

#Shop functions
#####################################################################################

    if message.content.startswith('BBcomeback'):
        bal = get_bal(users, message.author)
        cost = bbshop['BBcomeback'][0]
        if bal >= cost:
            await change_money(users, message.author, -cost)
            await message.channel.send(
                f'You spent {cost} BotCoin.'
            )
            await message.channel.send('https://youtu.be/tjBs4pKwzhU?t=79')
        else:
            await message.channel.send('You\'re too broke for this option!')

#####################################################################################

    if message.content.startswith('BBwordhint'):
        with open(f'{cwd}data\\wotd.json', 'r') as f:
            wotd = json.load(f)
        bal = get_bal(users, message.author)
        cost = bbshop['BBwordhint'][0]
        if (len(wotd['lettershinted']) == len(wotd['wotd']) or wotd['done'] == 1):
            await message.channel.send('The word is already revealed.')
        else:
            if bal >= cost:
                await change_money(users, message.author, -cost)
                await message.channel.send(
                    f'You spent {cost} BotCoin.'
                )
                #action here
                rand = random.randrange(0, (len(wotd['wotd'])))
                print(len(wotd['wotd']) - 1)
                while rand in wotd['lettershinted']:
                    rand = random.randrange(0, (len(wotd['wotd'])))
                    print(str(rand) + "\n")
                wotd['lettershinted'].insert(0, rand)
                out = ""
                for i in range(len(wotd['wotd'])):
                    if i in wotd['lettershinted']:
                        out += wotd['wotd'][i]
                    else:
                        out += "-"
                await message.channel.send(out)
                with open(f'{cwd}data\\wotd.json', 'w') as f:
                            json.dump(wotd, f)
            else:
                await message.channel.send('You\'re too broke for this option!')

#First game, Hangman!
#####################################################################################

    if message.content.startswith('BBquithangman'):
        with open(f'{cwd}data\\hm.json', 'r') as f:
            hm = json.load(f)
        if hm['players'][str(message.author.id)]['playing'] == 1:
            await message.channel.send("Game quit. No refunds.")
            hm['players'][str(message.author.id)]['playing'] = 0
            with open(f'{cwd}data\\hm.json', 'w') as f:
                json.dump(hm, f)
        else:
            await message.channel.send("Not currently playing game.")

#####################################################################################
    #Creates a game of hangman for a price, with custom words and images
    if message.content.startswith('BBhangman'):
        with open(f'{cwd}data\\hm.json', 'r') as f:
            hm = json.load(f)
        with open(f'{cwd}data\\users.json', 'r') as f:
            users = json.load(f)

        if not str(message.author.id) in hm['players']:
            hm['players'][str(message.author.id)] = {"playing" : 0, "currword" : "", "guessed" : [], "wrong" : 0, "games" : 0, "gameswon" : 0}
        if not 'games' in hm['players'][str(message.author.id)]:
            hm['players'][str(message.author.id)]['games'] = 0
            print("bonk")
            hm['players'][str(message.author.id)]['gameswon'] = 0
        games = hm['players'][str(message.author.id)]['games']
        gameswon = hm['players'][str(message.author.id)]['gameswon']
        if hm['players'][str(message.author.id)]['playing'] == 1:
            return await message.channel.send("You are already playing a game. Type BBquithangman to quit the game.")
        hm['players'][str(message.author.id)]['guessed'] = []
        hm['players'][str(message.author.id)]['wrong'] = 0
        bal = get_bal(users, message.author)
        cost = bbshop['BBhangman'][0]
        def check(m: discord.Message):
          return m.author.id == message.author.id and m.channel == message.channel
        if bal >= cost:
            try:
                await change_money(users, message.author, -cost)
                await message.channel.send("100 Botcoin taken, starting game. Good Luck!")
                rand = random.randrange(0, len(hm['words']))
                word = hm['words'][rand]
                hm['players'][str(message.author.id)]['playing'] = 1
                hm['players'][str(message.author.id)]['currword'] = word
                hm['players'][str(message.author.id)]['games'] = games + 1
                #make hangman idiot
                response = None
                dashes = ""
                for i in range(len(word)):
                    if word[i] == " ":
                        dashes += " "
                    elif word[i] == "-":
                        dashes += "-"
                    else:
                        dashes += "_"
                    if i != len(word)-1:
                        dashes += " "
                image = Image.open(f'{cwd}media\\base.png')
                draw = ImageDraw.Draw(image)
                font = ImageFont.truetype(f'{cwd}fonts\\unispace.regular.otf',120)
                fontsize = 100  # starting font size
                # portion of image width you want text width to be
                img_fraction = 0.90
                breakpoint = img_fraction * image.size[0]
                jumpsize = 75
                while True:
                    if font.getlength(dashes) < breakpoint:
                        fontsize += jumpsize
                    else:
                        jumpsize = jumpsize // 2
                        fontsize -= jumpsize
                    font = ImageFont.truetype(f'{cwd}fonts\\unispace.regular.otf', fontsize)
                    if jumpsize <= 1:
                        break
                #DRAW WORDS AND BLANKS
                xpos = (1920 - font.getlength(dashes)) / 2
                ypos = (1920 - fontsize) - 100
                draw.text((xpos, ypos), dashes, font = font, fill = "white")
                with BytesIO() as image_binary:
                    image.save(image_binary, 'PNG')
                    image_binary.seek(0)
                    file = discord.File(fp=image_binary, filename='image.png')
                    #embed.set_image(url="attachment://image.png")
                response = await message.channel.send(file=file)
                while hm['players'][str(message.author.id)]['playing'] == 1:
                    out = ""
                    image = Image.open(f'{cwd}media\\base.png')
                    draw = ImageDraw.Draw(image)
                    font = ImageFont.truetype(f'{cwd}fonts\\unispace.regular.otf',120)
                    guess = await client.wait_for('message', check = check, timeout=None)
                    if(guess.content == "BBhangman"):
                        await message.channel.send("You are already playing a game. Type BBquithangman to quit the game.")
                        with open(f'{cwd}data\\hm.json', 'w') as f:
                            json.dump(hm, f)
                    if(guess.content == "BBquithangman"):
                        await message.channel.send("Game quit. No refunds.")
                        hm['players'][str(message.author.id)]['playing'] = 0
                        with open(f'{cwd}data\\hm.json', 'w') as f:
                            json.dump(hm, f)
                        break
                    elif(check(guess)) and len(guess.content) == 1:
                        if guess.content.lower() in hm['players'][str(message.author.id)]['guessed']:
                            await message.channel.send("You have already guessed this letter.")
                        else:
                            hm['players'][str(message.author.id)]['guessed'].append(guess.content.lower())
                            correct = 0
                            if not guess.content.lower() in word:
                                #print('wrong')
                                hm['players'][str(message.author.id)]['wrong'] += 1
                            for i in range(len(word)):
                                if word[i] in hm['players'][str(message.author.id)]['guessed'] or word[i] == " ":
                                    out += word[i]
                                    if not i == len(word)-1:
                                        out += " "
                                    correct += 1
                                else:
                                    out += ' '
                                    if not i == len(word)-1:
                                        out += " "
                            if(response != None):
                                await response.delete()
                            fontsize = 100  # starting font size
                            # portion of image width you want text width to be
                            img_fraction = 0.90
                            breakpoint = img_fraction * image.size[0]
                            jumpsize = 75
                            while True:
                                if font.getlength(dashes) < breakpoint:
                                    fontsize += jumpsize
                                else:
                                    jumpsize = jumpsize // 2
                                    fontsize -= jumpsize
                                font = ImageFont.truetype(f'{cwd}fonts\\unispace.regular.otf', fontsize)
                                if jumpsize <= 1:
                                    break
                                #print(fontsize)
                            #print('final font size',fontsize)
                            #DRAW WORDS AND BLANKS
                            xpos = (1920 - font.getlength(out)) / 2
                            ypos = (1920 - fontsize) - 100
                            draw.text((xpos, ypos), dashes, font = font, fill = "white") # put the text on the image
                            draw.text((xpos, ypos - 15), out, font = font, fill = "white") # put the text on the image
                            wrong = hm['players'][str(message.author.id)]['wrong']
                            #DRAW BODY
                            if wrong >= 1:
                                draw.ellipse((356,197,689,530), fill = "black", outline = "white", width = 10) #HEAD
                            if wrong >= 2:
                                draw.line((522,530,522,1000), fill = "white", width = 10) #BODY
                            if wrong >= 3:
                                draw.line((522,1000,322,1200), fill = "white", width = 10) #LLEG
                            if wrong >= 4:
                                draw.line((522,1000,722,1200), fill = "white", width = 10) #RLEG
                            if wrong >= 5:
                                draw.line((522,730,372,830), fill = "white", width = 10) #LARM
                            if wrong >= 6:
                                draw.line((522,730,672,830), fill = "white", width = 10) #RARM
                            #WRITE USED LETTERS
                            font = ImageFont.truetype(f'{cwd}fonts\\unispace.regular.otf', 90)
                            #line = 0
                            #lines = [406,454,502,550,596]
                            newout = ""
                            guessed = hm['players'][str(message.author.id)]['guessed']
                            for i in range(len(guessed)):
                                #print(i)
                                if (i+1)%5 == 0 and i != 0:
                                    newout += f"{guessed[i]}\n"
                                    #draw.text((1062, lines[line]), newout, font = font, fill = "white")
                                else:
                                    newout += (guessed[i])
                                    newout += (" ")
                            draw.text((1075, 406), newout, font = font, fill = "white", spacing = 50)
                                
                            with BytesIO() as image_binary:
                                image.save(image_binary, 'PNG')
                                image_binary.seek(0)
                                file = discord.File(fp=image_binary, filename='image.png')
                                #embed.set_image(url="attachment://image.png")
                            response = await message.channel.send(file=file)
                            if correct == len(word):
                                await message.channel.send("You win! Enjoy 150 BotCoin!")
                                await change_money(users, message.author, 150)
                                hm['players'][str(message.author.id)]['playing'] = 0
                                hm['players'][str(message.author.id)]['gameswon'] += 1
                            if hm['players'][str(message.author.id)]['wrong'] >= 6:
                                hm['players'][str(message.author.id)]['playing'] = 0
                                await message.channel.send(f"You Lose! The word was \"{word}\". Better Luck next time.")
                    with open(f'{cwd}data\\hm.json', 'w') as f:
                        json.dump(hm, f)
            except Exception as e:
                print(repr(e))
                hm['players'][str(message.author.id)]['playing'] = 0
                await message.channel.send('Error. Game Quit.')
        else:
                await message.channel.send('You\'re too broke for this option!')
        with open(f'{cwd}data\\hm.json', 'w') as f:
            json.dump(hm, f)
        with open(f'{cwd}data\\users.json', 'w') as f:
            json.dump(users, f)

#####################################################################################
    #Snoop on someone else's stats!
    if message.content.startswith('BBsnoop'):
        bal = get_bal(users, str(message.author.id))
        cost = bbshop['BBsnoop'][0]
        if bal < cost:
            return await message.channel.send('You\'re too broke for this!')
        members = message.guild.members
        memberslist = [[],[],[],[],[],[],[],[],[],[]]
        personmenu = None
        select = Select( 
            placeholder = "Choose a player to snoop on:",
            options = []
        )
        currselect = 0
        currmod = 0
        j = 1
        for i in range(len(members)):
            if j >= 11:
                currmod += 1
                memberslist[currmod] = []
                j = 1
            if not members[i].bot:
                memberslist[currmod].append(members[i])
                j += 1
        for i in range(len(memberslist[currselect])):
            if not memberslist[currselect][i].bot:
                select.add_option(label = f"{memberslist[currselect][i].display_name}", value = memberslist[currselect][i].id)
        view = discord.ui.View(timeout=None)
        button1 = Button(label = 'Next Page', style = discord.ButtonStyle.green, emoji = "▶")
        button2 = Button(label = 'Prev Page', style = discord.ButtonStyle.red, emoji = "◀")
        async def snoopbutton_callback(interaction): #next page
            if interaction.user != message.author:
                return
            try:
                nonlocal select
                select = Select( 
                placeholder = "Choose a player to snoop on:",
                options = []
                )
                nonlocal currselect
                currselect += 1
                for i in range(len(memberslist[currselect])):
                    if not memberslist[currselect][i].bot:
                        select.add_option(label = f"{memberslist[currselect][i].display_name}", value = memberslist[currselect][i].id)
                view = discord.ui.View(timeout=None)
                view.add_item(select)
                select.callback = my_callback
                if memberslist[currselect] != len(memberslist):
                    if memberslist[currselect+1] != []:
                        view.add_item(button2)
                        view.add_item(button1)
                    else:
                        view.add_item(button2)
                else:
                    view.add_item(button2)
                await interaction.response.defer()
                return await personmenu.edit(content = 'Choose a person to snoop on (10 people per page, change pages if you need to):', view = view)
            except Exception as e:
                print(repr(e))
                print('oops')
        async def snoopbutton_callback2(interaction): #previous page
            if interaction.user != message.author:
                return
            try:
                nonlocal select
                select = Select( 
                placeholder = "Choose a player to snoop on:",
                options = []
                )
                nonlocal currselect
                currselect -= 1
                for i in range(len(memberslist[currselect])):
                    if not memberslist[currselect][i].bot:
                        select.add_option(label = f"{memberslist[currselect][i].display_name}", value = memberslist[currselect][i].id)
                view = discord.ui.View(timeout=None)
                view.add_item(select)
                select.callback = my_callback
                if currselect == 0:
                    view.add_item(button1)
                else:
                    view.add_item(button2)
                    view.add_item(button1)
                await interaction.response.defer()
                return await personmenu.edit(content = 'Choose a person to snoop on (10 people per page, change pages if you need to):', view = view)
            except Exception as e:
                print(repr(e))
                print('oops')
        button1.callback = snoopbutton_callback
        button2.callback = snoopbutton_callback2
        view = discord.ui.View(timeout=None)
        view.add_item(select)
        #view.add_item(button2)
        if len(members) >= 10:
            view.add_item(button1)
        personmenu = await message.channel.send( 'Choose a person to snoop on (10 people per page, change pages if you need to):', view = view)
        snoopselect = None
        comm = None
        snoopselect = Select( 
            placeholder = "Choose what to snoop on about:",
            options = []
        )
        snoopoptions = ['Words', 'Games', 'Tracks', 'Artists', 'Albums', 'BotCoin', 'Exp', 'Activities', 'Gambling', 'Hangman', 'Commands', 'Achievements']
        #message.channel.send(str(comm))
        for i in range(len(snoopoptions)):
            snoopselect.add_option(label = snoopoptions[i])
        async def my_callback(interaction):     
            comm = select.values[0]
            view2 = discord.ui.View(timeout=None)
            view2.add_item(snoopselect)
            if interaction.user.id == message.author.id:
                await interaction.response.send_message(ephemeral = True, view = view2)
            else:
                await interaction.response.send_message("You didn't start this menu.", ephemeral = True)
        async def my_callback2(interaction):
            comm2 = snoopselect.values[0]
            comm = select.values[0]
            embed = None
            file = None
            target = await message.guild.fetch_member(comm)
            if comm2 == "Words":
                out = await user_word_leaderboard(users, comm, message.channel)
                #await message.channel.send(out)
            if comm2 == "Games":
                out = await activity_leaderboard(users, comm, message.channel, 'playing')
            if comm2 == "Hangman":
                with open(f'{cwd}data\\hm.json', 'r') as f:
                    hm = json.load(f)
                if not str(comm) in hm['players'] or not 'games' in hm['players'][str(comm)]:
                    out = f"{target.display_name} Hasn\'t done any Hangman yet / hasn\'t played recently. Sad, right?"
                else:
                    gamesplayed = hm['players'][str(comm)]['games']
                    gameswon = hm['players'][str(comm)]['gameswon']
                    gameslost = gamesplayed = gameswon
                    winrate = round((gameswon / gamesplayed) * 100, 2)
                    moneywon = (-100 * gamesplayed) + (150 * gameswon)
                    embed = discord.Embed(
                        title = 'Hangman Snoop!',
                        description = 'Let\'s take a look!',
                        color = discord.Color.blue()
                    )
                    embed.add_field(name = 'Games Played', value = f'{gamesplayed} Games', inline = True)
                    embed.add_field(name = 'Games won', value = f'{gameswon} Games', inline = True)
                    embed.add_field(name = 'Total Wagers', value = f'{gamesplayed * 100} Botcoin', inline = True)
                    embed.add_field(name = 'Earnings', value = f'{moneywon} Botcoin', inline = True)
                    embed.add_field(name = 'Winrate', value = f'{winrate}%', inline = True)
            if comm2 == "Artists":
                out = await activity_leaderboard(users, comm, message.channel, 'artists')
            if comm2 == "Tracks":
                out = await activity_leaderboard(users, comm, message.channel, 'tracks')
            if comm2 == "Albums":
                out = await get_albums(users, comm, message.guild)
                embed = out[1]
                file = out[0]
                if(file) == None:
                    out = f'{target.display_name} hasn\'t listened to any albums yet!'
            if comm2 == "BotCoin":
                out = f'<@{comm}> has '+str(get_bal(users, comm)) + ' Botcoin.'
            if comm2 == "Exp":
                out = f'<@{comm}> has '+str(get_exp(users, comm)) + ' exp.'
            if comm2 == "Activities":
                out = await activity_leaderboard(users, comm, message.channel, 'custom')
            if comm2 == "Commands":
                out = get_commands(users, comm)
            if comm2 == "Achievements":
                if not "achievements" in users[str(comm)] or len(users[str(comm)]["achievements"]) == 0:
                    out = "They have no achievements!"
                else:
                    embed = discord.Embed(
                        title = f'{target.display_name}\'s Achievements',
                        description = 'Let\'s take a look!',
                        color = discord.Color.blue()
                    )
                    for ach in users[str(comm)]["achievements"]:
                        percent = getAchPercent(users, ach)
                        embed.add_field(name = ach, value = f'{percent} of people have this achievement.', inline = False)
                    #print all achievements that someone has
            if comm2 == "Gambling":
                with open(f'{cwd}data\\guessnum.json', 'r') as f:
                    guessnum = json.load(f)
                embed = discord.Embed(
                    title = 'Gambling Snoop!',
                    description = 'Let\'s take a look!',
                    color = discord.Color.blue()
                )
                embed.add_field(name = 'Gambling Stats:', value = f'How {target.display_name} gambled so far!', inline = False)
                gamesplayed = 0
                gameswon = 0
                gameslost = 0
                moneywagered = 0
                moneyearned = 0
                moneylost = 0
                for games in guessnum["active"]:
                    if games["players"][0] == str(target):
                        gamesplayed += 1
                        moneywagered += games["wager"]
                        if abs(int(games["p1guess"]) - games["answer"]) < abs(int(games["p2guess"]) - games["answer"]):
                            moneyearned += games["wager"]
                            gameswon += 1
                        else:
                            moneylost += games["wager"]
                            gameslost += 1
                    if games["players"][1] == str(target):
                        gamesplayed += 1
                        moneywagered += games["wager"]
                        if abs(int(games["p1guess"]) - games["answer"]) > abs(int(games["p2guess"]) - games["answer"]):
                            moneyearned += games["wager"]
                            gameswon += 1
                        else:
                            moneylost += games["wager"]
                            gameslost += 1
                if gamesplayed != 0:
                    embed.add_field(name = 'Games Played', value = f'{gamesplayed} Games', inline = True)
                    embed.add_field(name = 'Games won', value = f'{round((gameswon/gamesplayed) * 100, 2)}%', inline = True)
                    embed.add_field(name = 'Total Wagers', value = f'{moneywagered} Botcoin', inline = True)
                    embed.add_field(name = 'Earnings', value = f'{moneyearned} Botcoin', inline = True)
                    embed.add_field(name = 'Losses', value = f'{moneylost} Botcoin', inline = True)
                    embed.add_field(name = 'Net Profit', value = f'{moneyearned - moneylost} Botcoin', inline = True)
            if(file):
                await interaction.response.send_message('-20 BotCoin. So nosy.', ephemeral = True, embed = embed, file = file)
            elif(embed):
                await interaction.response.send_message('-20 BotCoin. So nosy.', ephemeral = True, embed = embed)
            else:
                await interaction.response.send_message(out + '\n-20 BotCoin. So nosy.', ephemeral = True)
            mem = await message.guild.fetch_member(comm)
            mem = mem.display_name
            print(str(message.author.display_name) + f' Has snooped on {mem}\'s {comm2}')
            await change_money(users, str(message.author.id), -cost)
            users[str(message.author.id)]["commands"]["BBsnoop"] += 1
        snoopselect.callback = my_callback2
        select.callback = my_callback
        

#####################################################################################

    #Blur an image and make it crispy
    if message.content.startswith('BBblur'):
        custom = False
        bal = get_bal(users, str(message.author.id))
        cost = bbshop['BBblur'][0]
        if bal < cost:
            return await message.channel.send('You\'re too broke for this!')
        prompt = message.content[11:]
        if message.attachments != []: #len(attachments) != 0
            img = message.attachments[0].url
            custom = True
        elif prompt.startswith('https'):
            e = message.content.split(" ")
            img = e[1]
            p = ""
            for word in e:
                if not word.startswith('BBblur') and not word.startswith('https'):
                    p += word + " "
            prompt = p
            custom = True
        else:
            img = get_image(prompt)
            if img == None:
                return await message.channel.send('Something went wrong.. Could be a bad prompt, or @loftzo if it happens to all prompts.') #check bing <img> classes #cimg, cimg img etc.
            # await message.channel.send(img)
        if prompt == "" or prompt == " ":
            return await message.channel.send('Need to enter prompt. For example:\nBBblur bucket')
        response = requests.get(img)
        img = Image.open(BytesIO(response.content))
        if custom == False:
            print("noncustom")
            img = img.resize((img.size[0]*2, img.size[1]*2,), Image.NEAREST)
        # else:
        #     img = img.resize((img.size[0], img.size[1],), Image.NEAREST)
        canvas = Image.new(mode = "RGB", size = img.size)
        canvas.paste(img, (0, 0))
        font = ImageFont.truetype(f'{cwd}fonts\\vanilla Caramel.otf', img.size[1] // 5)
        text = ImageDraw.Draw(canvas)
        text.text((0, 0), f"{prompt}", font = font, stroke_width = 5, stroke_fill = (0,0,0))
        canvas = canvas.filter(ImageFilter.EDGE_ENHANCE_MORE)
        if custom:
            canvas = canvas.filter(ImageFilter.EDGE_ENHANCE_MORE)
            # canvas = canvas.filter(ImageFilter.EDGE_ENHANCE_MORE)
            # canvas = canvas.filter(ImageFilter.EDGE_ENHANCE_MORE)
        # canvas = canvas.filter(ImageFilter.CONTOUR)
        with BytesIO() as image_binary:
                canvas.save(image_binary, 'PNG')
                image_binary.seek(0)
                file = discord.File(fp=image_binary, filename='image.png')
        size = (image_binary.__sizeof__())
        while True:
            with BytesIO() as image_binary:
                canvas.save(image_binary, 'PNG')
                image_binary.seek(0)
                file = discord.File(fp=image_binary, filename='image.png')
            size = (image_binary.__sizeof__())
            scale = (8200000 / size) / 2
            if size >= 8000000:
                canvas = canvas.resize(((int(canvas.size[0]*scale)), int(canvas.size[1]*scale)), Image.NEAREST)
            else:
                break
        await message.channel.send(file=file)
        await change_money(users, str(message.author.id), -cost)

#####################################################################################
    #Ask a question to the all-knowing! Basically a slightly smarter 8-ball
    if message.content.startswith('BB?') or message.content.startswith('BB8ball'):
        pic = None
        bblist = ['yours truly', 'the king', 'god', 'BotBot', 'me', 'the universe (excluding Neptune)', 'today', 'Oz the great and powerful',
                  'the Orb', 'the all-seeing eye', 'jacobs computer', 'some guy behind a taco bell', 'ambiguous Gary', 'the incorporeal being, "Steve"',
                  'Jane Austen\'s nephew', 'an ape with a keyboard', 'infinite monkeys on finite typewriters', 'the missile', 'Richard Nixon\'s first grade superintendent',
                  'the Kool-Aid man', 'chadGPT', 'the voices', 'a chainsaw activist', 'the inventor of the wallet', 'siri']
        phrase = bblist[random.randrange(len(bblist))]
        await message.channel.send(f'What is your question for {phrase}?')
        def check(m: discord.Message):
          return m.author.id == message.author.id and m.channel == message.channel
        monthmsg = await client.wait_for('message', check = check)
        #when
        if monthmsg.content.lower().startswith('when'):
            whenlist = ['Tomorrow.', 'Right now.', 'Literally never.', 'In a week.', 'Next month.', 'After the meeting.', 
                        'When the sun rises.', 'Before you leave.', 'In the near future.', 'On your birthday.', 'Once you finish the task.', 
                        'When the conditions are right.', 'In a few minutes.', 'On a leap year during a blue moon.']
            num = random.randrange(1,10)
            if num > 9:
                start = datetime.now(tz)
                delta = timedelta(
                    days = 1900
                )
                end = start + delta
                delta = end - start
                int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
                random_second = random.randrange(int_delta)
                result = start + timedelta(seconds=random_second)
                answer = result.strftime('%A %B %d, %Y, at %I:%M%p')
            else:
                answer = whenlist[random.randrange(len(whenlist))]
        #where
        elif monthmsg.content.lower().startswith('where'):
            wherelist = ['Up your butt and around the corner.', 'Nunya.', 'Brazil.', 'Your mom\'s house', 'Right where you are.', 'In your walls.',
                         "Where the stars align, and magic unfolds.", "In the land of unicorns and rainbows.", "Ask again in Narnia, I might be there.",
                         "Where the wild things roam and the fun never ends.", "I'm not sure, but let's pretend it's in Atlantis.", "Somewhere over the rainbow, way up high.", 
                         "Where dreams come true, and laughter echoes.", "In the heart of a labyrinth, tread carefully!", "Look for clues in the Enchanted Forest.", "In a galaxy far, far away—Star Wars style!",
                         "I sense it's near the end of the rainbow.", "Lost in translation, ask again in a different language.", "Where the last dragon resides, hidden from the world.", 
                         "Behind the moon, shrouded in mystery.", "I'm not entirely sure, but it's probably in the fridge. Everything seems to end up there!",
                         "Yellowstone National Park", "Easter Island", "Taj Mahal", "Serengeti National Park", "Chichen Itza", "Bora Bora", "Mount Everest", "Niagara Falls"]
            num = random.randrange(1,10)
            if num > 7:
                #Gives a real lat and long coords, and provides the image of the map
                lat = (random.randrange(-530000000, 770000000)) / 10000000
                long = (random.randrange(-1220000000, 1190000000)) / 10000000
                print(str(lat) + ',' + str(long))
                cookies = {
                    'MUID': '008F720CBC8A68AD191E634CBDC56919',
                    'SRCHD': 'AF=NOFORM',
                    'SRCHUID': 'V=2&GUID=DE19F4938FA64838B78FA166B0A0E3B8&dmnchg=1',
                    '_UR': 'QS=0&TQS=0',
                    'BFBUSR': 'BAWAS=1&BAWFS=1',
                    'MMCASM': 'ID=6B21D908D965497C960B7723ABBF52F4',
                    '_HPVN': 'CS=eyJQbiI6eyJDbiI6MiwiU3QiOjAsIlFzIjowLCJQcm9kIjoiUCJ9LCJTYyI6eyJDbiI6MiwiU3QiOjAsIlFzIjowLCJQcm9kIjoiSCJ9LCJReiI6eyJDbiI6MiwiU3QiOjAsIlFzIjowLCJQcm9kIjoiVCJ9LCJBcCI6dHJ1ZSwiTXV0ZSI6dHJ1ZSwiTGFkIjoiMjAyMy0wNC0wNlQwMDowMDowMFoiLCJJb3RkIjowLCJHd2IiOjAsIkRmdCI6bnVsbCwiTXZzIjowLCJGbHQiOjAsIkltcCI6OX0=',
                    'ipv6': 'hit=1680753784478&t=4',
                    'SUID': 'M',
                    'MUIDB': '008F720CBC8A68AD191E634CBDC56919',
                    '_EDGE_S': 'SID=0138B10352826BD12368A25953296A58',
                    'SRCHS': 'PC=U645',
                    'BFB': 'AhCj1a1GOCehbnKU5hMJn9WrzVYkYgfeNKSFg2nmmqlLgUHR4ey1zpMAk3gyXnu-AxDub6ghUJJhfGCLjwMBeMOqB-l7BQVGjZbfv07jqBAFp--5Vtec7e13Q-BOAW3LWAc',
                    'USRLOC': 'HS=1&ELOC=LAT=37.40317916870117|LON=-77.58214569091797|N=Chesterfield%2C%20Virginia|ELT=6|',
                    'SRCHUSR': 'DOB=20220509&T=1690411804000',
                    '_RwBf': 'ilt=12&ihpd=0&ispd=2&rc=45&rb=0&gb=0&rg=200&pc=40&mtu=0&mte=0&rbb=0&g=0&cid=&clo=0&v=2&l=2023-07-26T07:00:00.0000000Z&lft=0001-01-01T00:00:00.0000000&aof=0&o=2&p=&c=&t=0&s=0001-01-01T00:00:00.0000000+00:00&ts=2023-07-26T22:54:06.1757610+00:00&rwred=0&wls=&lka=0&lkt=0&TH=&dci=0',
                    '_SS': 'SID=258B38DFB8726C54141B2A39B9606D2A&R=45&RB=0&GB=0&RG=200&RP=40&PC=U645',
                    'SRCHHPGUSR': 'SRCHLANG=en&PV=10.0.0&BRW=NOTP&BRH=M&CW=642&CH=939&SCW=1084&SCH=2031&DPR=1.0&UTC=-240&DM=1&WTS=63826008602&HV=1690412046&PRVCW=642&PRVCH=939&ADLT=STRICT',
                }

                headers = {
                    'authority': 'www.bing.com',
                    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                    'accept-language': 'en-US,en;q=0.9',
                    'cache-control': 'max-age=0',
                    'referer': 'https://www.microsoft.com/',
                    'sec-ch-ua': '"Opera GX";v="99", "Chromium";v="113", "Not-A.Brand";v="24"',
                    'sec-ch-ua-arch': '"x86"',
                    'sec-ch-ua-bitness': '"64"',
                    'sec-ch-ua-full-version': '"99.0.4788.86"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-model': '""',
                    'sec-ch-ua-platform': '"Windows"',
                    'sec-ch-ua-platform-version': '"10.0.0"',
                    'sec-fetch-dest': 'document',
                    'sec-fetch-mode': 'navigate',
                    'sec-fetch-site': 'cross-site',
                    'sec-fetch-user': '?1',
                    'upgrade-insecure-requests': '1',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 OPR/99.0.0.0',
                }

                response = requests.get(
                    f'https://www.bing.com/search?q={lat},{long}&FORM=U645SB&PC=U645',
                    cookies=cookies,
                    headers=headers,
                )
                soup = BeautifulSoup(response.text, "html.parser")  # parse the HTML content with BeautifulSoup
                pic = soup.find("img", {"id" : "mv_baseMap"})
                pic = pic.get("src")
                answer = f'{lat},{long}'
            else:
                answer = wherelist[random.randrange(len(wherelist))]
        #why
        elif monthmsg.content.lower().startswith('why'):
            whylist = ['Because of safety concerns.', 'To improve efficiency.', 'For better performance.', 'Due to legal requirements.', 
                        'To meet customer demands.', 'To avoid potential risks.', 'In order to reduce costs.', 'For strategic reasons.', 
                        'To comply with regulations.', 'To achieve our goals.', 'Because aliens told us to.', 'To confuse the cat.', 'For the giggles.',
                        'To impress our robot overlords.', 'Because squirrels demanded it.', 'To see what happens.', 'To keep the time-traveling unicorns happy.', 
                        'For the sake of world peace (and pizza).', 'To outsmart the cheese conspiracy.', 'To find the ultimate answer to the universe, life, and everything (spoiler: it\'s 42).']
            answer = whylist[random.randrange(len(whylist))]
        #how many
        elif monthmsg.content.lower().startswith('how many'):
            howmanylist = ['None.', 'Too many to count.', 'Three.', 'At least a dozen.', 'Just one.', 'Infinity and beyond.', 'A handful.', 'Exactly 42.', 'More than you can imagine.', 'Not enough.',
                           'Seven.', 'Twice as much as before.', 'Only a couple.', 'Ten or so.', 'Just a few.', 'A gazillion.', 'Not a single one.', 'Hundreds.', 'Less than a hundred.', 'Half a dozen.',
                            'An army of them.', 'A whole bunch.', 'Enough to fill a bathtub.', 'Exactly 17.', 'Countless.', 'One for each star in the sky.', 'A plethora.', 'A swarm.', 'Infinite possibilities.']
            num = random.randrange(1,10)
            if num > 9:
                answer = random.randrange(0, 9999999)
            else:
                answer = howmanylist[random.randrange(len(howmanylist))]
        #how
        elif monthmsg.content.lower().startswith('how'):
            howlist = ['With a dancing llama.', 'By bribing the laws of physics.', 'By asking the nearest fortune-teller.', 'With the finesse of a caffeinated squirrel.', 'By channeling our inner ninja.', 
                        'Using the sacred art of "winging it."', 'By performing the secret dance of success.', 'With the help of a friendly neighborhood alien.', 'By making a deal with the universe.', 
                        'By harnessing the cosmic power of dad jokes.', 'With a sprinkle of fairy dust.', 'By bribing the coding gnomes.', 'With a dash of pure luck.', 'By bribing the math gods with cookies.', 
                        'With a Jedi mind trick.', 'By consulting the ancient scrolls of internet wisdom.', 'By tapping into the quantum realm of possibilities.', 'By summoning the spirit of Albert Einstein.', 
                        'Using a pinch of imagination and a hint of madness.', 'By bribing the laws of probability with chocolate.']
            answer = howlist[random.randrange(len(howlist))]
        #who
        elif monthmsg.content.lower().startswith('who'):
            wholist = ['A mysterious stranger.', 'The one and only ChatGPT.', 'A team of skilled professionals.', 'Your friendly neighborhood superhero.', 'A group of enthusiastic volunteers.', 'The mastermind behind the plan.', 
                        'A magical unicorn.', 'A brilliant mind from the past.', 'A squad of trained penguins.', 'A secret society of geniuses.', 'The chosen ones.', 'A talking parrot with insider information.', 'An anonymous internet legend.', 
                        'The unsung heroes.', 'A quirky bunch of misfits.', 'The legendary ninja cats.', 'The person who invented time travel (allegedly).', 'A highly caffeinated individual.', 'The ghost of a famous inventor.']
            num = random.randrange(1,10)
            if num > 5 and message.guild:
                people = message.guild.members
                answer = 'I\'d say ' + people[random.randrange(len(people))].display_name
            else:
                answer = wholist[random.randrange(len(wholist))]
        #will/does
        elif monthmsg.content.lower().startswith('will') or monthmsg.content.lower().startswith('does'):
            yesnolist = ['Absolutely, positively, without a doubt, yes!', 'No way, Jose!', 'You bet your sweet bippy!', 'Negative ghost rider.', 'In your dreams!', 'As if!', 'Oh, honey, no!', 'Sure, when pigs fly!', 'Not on your life!', 'Yepity yep!', 
                         'Nopeity nope!', 'Ask again after I\'ve had my coffee.', 'I\'m not a magic eight ball, but I\'ll go with yes.', 'My sources say no, but my gut says who cares!', 'That\'s a clown question, bro.', 'No, no, a thousand times, no!',
                           'Yes, but only on alternate Wednesdays.', 'If I say yes, will you stop asking?', 'As likely as finding a unicorn riding a unicycle.']
            answer = yesnolist[random.randrange(len(yesnolist))]
        else:
            finallist = ["It is certain.", "Outlook good, like a rainbow after rain.", "Ask again later, I'm on a coffee break.", "Cannot predict now, I'm a bit sleepy.", "Better not tell you now, I could tell you, but then I'd have to erase your memory.",
                          "My sources say no, but they've been wrong before. Aliens, you know?", "You may rely on it, or you can toss a coin and decide for yourself.", "Concentrate and ask again, but try not to overheat my circuits with your tough questions.", 
                          "As I see it, yes. By the way, I'm great at predicting the weather—sunny with a chance of giggles.", "Very doubtful. You have better odds of finding Bigfoot doing the Cha-Cha.", "Signs point to yes, but remember, signposts have been wrong before!", 
                          "Reply hazy, try again later, and by then I might have a proper cup of tea.", "Without a doubt, but don't forget to bring an umbrella in case of marshmallow rain.", "My reply is no, unless you're willing to bribe me with cookies.", 
                          "Ask again when pigs fly, or when the moon is made of cheese—whichever comes first."]
            answer = finallist[random.randrange(len(finallist))]
        await message.channel.send(answer)
        if pic:
            await message.channel.send(pic)
        

#####################################################################################
    #List of all relevant commands
    if message.content.startswith('BBhelp'):
        # print(type(message.author))
        select = Select( 
            placeholder = "Choose a command to learn more:",
            options = [
                discord.SelectOption(label = "BBhello", emoji = "👋"),
                discord.SelectOption(label = "BBmywords", emoji = "📧"),
                discord.SelectOption(label = "BBmoney", emoji = "💸"),
                discord.SelectOption(label = "BBguessnum", emoji = "🔢"),
                discord.SelectOption(label = "BBhelp", emoji = "🆘"),
                discord.SelectOption(label = "BBshop", emoji = "🛒"),
                discord.SelectOption(label = "BBmygames", emoji = "🎮"),
                discord.SelectOption(label = "BBmymusic", emoji = "🎧"),
                discord.SelectOption(label = "BBmyalbums", emoji = "📻"),
                discord.SelectOption(label = "BBmyactivity", emoji = "🏃‍♀️"),
                discord.SelectOption(label = "BBmystreams", emoji = "🎥"),
                discord.SelectOption(label = "BBmystreamgames", emoji = "🕹"),
                discord.SelectOption(label = "BBmywatching", emoji = "📺"),
                discord.SelectOption(label = "BBmycomps", emoji = "🤸‍♀️"),
                discord.SelectOption(label = "BBexp", emoji = "🔋"),
                discord.SelectOption(label = "BBsuggest", emoji = "💡"),
                discord.SelectOption(label = "BBpay", emoji = "💰"),
                discord.SelectOption(label = "BBadmin", emoji = "👼"),
                discord.SelectOption(label = "BBwrapped", emoji = "🎁"),
                discord.SelectOption(label = "BBfetchpfp", emoji = "🖼"),
                discord.SelectOption(label = "BBadda___", emoji = "🦆"),
                discord.SelectOption(label = "BBguessword", emoji = "✏"),
                discord.SelectOption(label = "BBachievements", emoji = "🏆"),
                discord.SelectOption(label = "BBscavengerhunt", emoji = "🔍"),
                # discord.SelectOption(label = "BB?", emoji = "❓"),
                # discord.SelectOption(label = "BBtoday", emoji = "📅"),
                # discord.SelectOption(label = "BBbirthday", emoji = "🎂"),
            ]
        )
        view = discord.ui.View(timeout=None)
        view.add_item(select)
        await message.channel.send( 'Hey there! I\'m BotBot, a bot made by loftzo to goof around. Try not to spam commands too much, since they can flood channels pretty easily. Unless you want to. I\'m a bot, not a judge. \nSelect a command to learn about:', view = view)
        async def my_callback(interaction):
            embed = discord.Embed(
            title = f'How to use {select.values[0]}',
            description = 'Let\'s take a look!',
            color = discord.Color.blue()
        )
            comm = select.values[0]
            if comm == "BBhello":
                embed.add_field(name = "Description", value = "BBhello lets BotBot say hello back!", inline = False)
                embed.add_field(name = "Usage", value = "`BBhello`", inline = False)
                embed.add_field(name = "Example", value = "BBhello", inline = False)
            if comm == "BBmywords":
                embed.add_field(name = "Description", value = "BBmywords shows you your top 5 most used words!", inline = False)
                embed.add_field(name = "Usage", value = "`BBmywords`", inline = False)
                embed.add_field(name = "Example", value = "BBmywords", inline = False)
            if comm == "BBhelp":
                embed.add_field(name = "Description", value = "BBhelp Introduces BotBot and lets you select a command to learn about!", inline = False)
                embed.add_field(name = "Usage", value = "`BBhelp`", inline = False)
                embed.add_field(name = "Example", value = "BBhelp", inline = False)
            if comm == "BBmoney":
                embed.add_field(name = "Description", value = "BBmoney lets you check how much BotCoin you have!", inline = False)
                embed.add_field(name = "Usage", value = "`BBmoney`", inline = False)
                embed.add_field(name = "Example", value = "BBmoney", inline = False)
            if comm == "BBguessnum":
                embed.add_field(name = "Description", value = "BBguessnum lets you gamble against another user by picking a number!\n Enter the range as one of the arguments, e.x. if range is 20, you pick a number 1-20!", inline = False)
                embed.add_field(name = "Usage", value = "`BBguessnum [@user] [wager] [range]`", inline = False)
                embed.add_field(name = "Example", value = "BBguessnum @loftzo 50 30", inline = False)
            if comm == "BBshop":
                embed.add_field(name = "Description", value = "BBshop shows you how to spend your hard earned BotCoin!", inline = False)
                embed.add_field(name = "Usage", value = "`BBshop`", inline = False)
                embed.add_field(name = "Example", value = "BBshop", inline = False)
            if comm == "BBmygames":
                embed.add_field(name = "Description", value = "BBmygames shows you your top 5 most played games!", inline = False)
                embed.add_field(name = "Usage", value = "`BBmygames`", inline = False)
                embed.add_field(name = "Example", value = "BBmygames", inline = False)
            if comm == "BBmymusic":
                embed.add_field(name = "Description", value = "BBmymusic shows you your top 5 most played artists!", inline = False)
                embed.add_field(name = "Usage", value = "`BBmymusic`", inline = False)
                embed.add_field(name = "Example", value = "BBmymusic", inline = False)
            if comm == "BBmyalbums":
                embed.add_field(name = "Description", value = "BBmyalbums shows you your top 8 most played albums with a neat picture!", inline = False)
                embed.add_field(name = "Usage", value = "`BBmyalbums`", inline = False)
                embed.add_field(name = "Example", value = "BBmyalbums", inline = False)
            if comm == "BBmyactivity":
                embed.add_field(name = "Description", value = "BBmyactivity shows you your top 5 most used custom activities!", inline = False)
                embed.add_field(name = "Usage", value = "`BBmyactivity`", inline = False)
                embed.add_field(name = "Example", value = "BBmyactivity", inline = False)
            if comm == "BBmystreams":
                embed.add_field(name = "Description", value = "BBmystreams shows you your top 5 most streamed activities!", inline = False)
                embed.add_field(name = "Usage", value = "`BBmystreams`", inline = False)
                embed.add_field(name = "Example", value = "BBmystreams", inline = False)
            if comm == "BBmystreamgames":
                embed.add_field(name = "Description", value = "BBmystreamgames shows you your top 5 most streamed games!", inline = False)
                embed.add_field(name = "Usage", value = "`BBmystreamgames`", inline = False)
                embed.add_field(name = "Example", value = "BBmystreamgames", inline = False)
            if comm == "BBmywatching":
                embed.add_field(name = "Description", value = "BBmywatching shows you your top 5 most watched media!", inline = False)
                embed.add_field(name = "Usage", value = "`BBmywatching`", inline = False)
                embed.add_field(name = "Example", value = "BBmywatching", inline = False)
            if comm == "BBmycomps":
                embed.add_field(name = "Description", value = "BBmycomps shows you your top 5 most competed events!", inline = False)
                embed.add_field(name = "Usage", value = "`BBmycomps`", inline = False)
                embed.add_field(name = "Example", value = "BBmycomps", inline = False)
            if comm == "BBexp":
                embed.add_field(name = "Description", value = "BBexp tells you how much BotBot specific experience you have!", inline = False)
                embed.add_field(name = "Usage", value = "`BBexp`", inline = False)
                embed.add_field(name = "Example", value = "BBexp", inline = False)
            if comm == "BBsuggest":
                embed.add_field(name = "Description", value = "BBsuggest you make a suggestion to improve BotBot, and maybe earn some BotCoin!", inline = False)
                embed.add_field(name = "Usage", value = "`BBsuggest\nBotBot: What\'s your suggestion?\n[suggestion]`", inline = False)
                embed.add_field(name = "Example", value = "BBsuggest ", inline = False)
            if comm == "BBpay":
                embed.add_field(name = "Description", value = "BBpay lets you give some of your BotCoin to someone else!", inline = False)
                embed.add_field(name = "Usage", value = "`BBpay [@user] [amount]`", inline = False)
                embed.add_field(name = "Example", value = "BBpay @loftzo 69", inline = False)
            if comm == "BBadmin":
                embed.add_field(name = "Description", value = "BBadmin lets admins see admin commands!", inline = False )
                embed.add_field(name = "Usage", value = "`BBadmin`", inline = False )
                embed.add_field(name = "Example", value = "BBadmin", inline = False )
            if comm == "BBwrapped":
                embed.add_field(name = "Description", value = "BBwrapped shows you your total stats!", inline = False)
                embed.add_field(name = "Usage", value = "`BBwrapped`", inline = False)
                embed.add_field(name = "Example", value = "BBwrapped", inline = False)
            if comm == "BBfetchpfp":
                embed.add_field(name = "Description", value = "BBfetchpfp gives you the profile picture of a user! **Is this the one you're looking for?**", inline = False)
                embed.add_field(name = "Usage", value = "`BBfetchpfp [userid]` OR `BBfetchpfp [@user]`", inline = False)
                embed.add_field(name = "Example", value = "BBfetchpfp 323518323679559721 OR BBfetchpfp @loftzo", inline = False)
            if comm == "BBadda___":
                embed.add_field(name = "Description", value = "BBadda____ lets you submit a animal pic for potential BotCoin!", inline = False)
                embed.add_field(name = "Usage", value = "`BBadda____\n[link]`", inline = False)
                embed.add_field(name = "Example", value = "BBaddaduck\nBotBot: What's your duck image link?\nhttps:// something", inline = False)
                embed.add_field(name = "All commands", value = "BBaddaduck\nBBaddarat\nBBaddafrog\nBBaddapanda\nBBaddapet\n", inline = False)
            if comm == "BBguessword":
                embed.add_field(name = "Description", value = "BBguessword lets you use your 1 daily guess on the word of the day to potentially win BotCoin!\nThe Word of the Day, or WotD, is reset once daily when the Question Bot asks its question (~8:26 AM EST). If a message (longer than 3 words) contains the WotD, BotBot will react with 👀. Only one winner per day!", inline = False)
                embed.add_field(name = "Usage", value = "`BBguessword\nBotBot: What\'s your guess?\n[guess]`", inline = False)
                embed.add_field(name = "Example", value = "BBguessword\nBotBot: What\'s your guess?\nidiot", inline = False)
                embed.add_field(name = "Prize", value = "If you guess correctly, you will win 100 BotCoin! If you guess wrong, you will lose your guess for the day, and have to try tomorrow.", inline = False)
            if comm == "BBachievements":
                embed.add_field(name = "Description", value = "BBachievements or BBmyachievements shows you all the achievements you\'ve earned!", inline = False)
                embed.add_field(name = "Usage", value = "`BBachievements`", inline = False)
                embed.add_field(name = "Example", value = "BBachievements", inline = False)
            if comm == "BBscavengerhunt":
                embed.add_field(name = "Description", value = "BBscavengerhunt gives you the first of clues to start the hunt.", inline = False)
                embed.add_field(name = "Usage", value = "`BBscavengerhunt`", inline = False)
                embed.add_field(name = "Example", value = "BBscavengerhunt", inline = False)
            if comm == "BB?":
                embed.add_field(name = "Description", value = "BB? lets you ask a question to the all-knowing.", inline = False)
                embed.add_field(name = "Usage", value = "`BB?`", inline = False) 
                embed.add_field(name = "Example", value = "BB?", inline = False)
            if comm == "BBtoday":
                embed.add_field(name = "Description", value = "BBtoday shows off the holidays and birthdays of the day.", inline = False)
                embed.add_field(name = "Usage", value = "`BBtoday`", inline = False)
                embed.add_field(name = "Example", value = "BBtoday", inline = False)
            if comm == "BBbirthday":
                embed.add_field(name = "Description", value = "BBbirthday lets you set your own birthday for BotBot to remember.", inline = False)
                embed.add_field(name = "Usage", value = "`BBbirthday`", inline = False)
                embed.add_field(name = "Example", value = "BBbirthday", inline =False)
                
            await interaction.response.send_message(f'you chose {select.values[0]}.', ephemeral = True, embed = embed)
        select.callback = my_callback


#####################################################################################
    #Botify wrapped!
    if message.content.startswith('BBwrapped'):
        # print(type(message.author))
        with open(f'{cwd}data\\guessnum.json', 'r') as f:
          guessnum = json.load(f)
        embed = discord.Embed(
            title = 'How\'d you do with BotBot this year?',
            description = 'Let\'s take a look!',
            color = discord.Color.blue()
        )

        embed.set_author(name = f'{str(message.author)[:-5]}\'s Botify Wrapped!')
        try:
            embed.set_thumbnail(url = message.author.avatar.url)
        except:
            embed.set_thumbnail(url = "https://static.tvtropes.org/pmwiki/pub/images/wrapped_christmas_presents_wrapped_christmas_present_jpg_fy6ii2_clipart.jpg")
        embed.add_field(name = 'Botcoin', value = f'You\'ve got {get_bal(users, message.author)} Botcoin!', inline = False)
        embed.add_field(name = 'Words Counted', value = f'{users[str(message.author.id)]["totalWords"]} Words', inline = True)
        embed.add_field(name = 'Exp Acquired', value = f'{users[str(message.author.id)]["exp"]} Exp', inline = True)
        embed.add_field(name = 'Unique Words', value = f'{len(users[str(message.author.id)]["words"])} Words', inline = True)
        mentionlist = {}
        for word in users[str(message.author.id)]['words']:
            if word.startswith('<@'):
                mentionlist[word] = users[str(message.author.id)]['words'][word]
        res = nlargest(1,
                mentionlist,
                key=mentionlist.get)
        if len(res) > 0:
            times = users[str(message.author.id)]['words'][res[0]]
            embed.add_field(name = 'Who you @\'d the most', value = f'{res[0]} with {times} mentions', inline = True)
        embed.add_field(name = 'Gambling Stats:', value = 'How you gambled so far!', inline = False)
        gamesplayed = 0
        gameswon = 0
        gameslost = 0
        moneywagered = 0
        moneyearned = 0
        moneylost = 0
        for games in guessnum["active"]:
            if games["players"][0] == str(message.author):
                gamesplayed += 1
                moneywagered += games["wager"]
                if abs(int(games["p1guess"]) - games["answer"]) < abs(int(games["p2guess"]) - games["answer"]):
                    moneyearned += games["wager"]
                    gameswon += 1
                else:
                    moneylost += games["wager"]
                    gameslost += 1
            if games["players"][1] == str(message.author):
                gamesplayed += 1
                moneywagered += games["wager"]
                if abs(int(games["p1guess"]) - games["answer"]) > abs(int(games["p2guess"]) - games["answer"]):
                    moneyearned += games["wager"]
                    gameswon += 1
                else:
                    moneylost += games["wager"]
                    gameslost += 1
        if gamesplayed != 0:
            embed.add_field(name = 'Games Played', value = f'{gamesplayed} Games', inline = True)
            embed.add_field(name = 'Games won', value = f'{round((gameswon/gamesplayed) * 100, 2)}%', inline = True)
            embed.add_field(name = 'Total Wagers', value = f'{moneywagered} Botcoin', inline = True)
            embed.add_field(name = 'Earnings', value = f'{moneyearned} Botcoin', inline = True)
            embed.add_field(name = 'Losses', value = f'{moneylost} Botcoin', inline = True)
            embed.add_field(name = 'Net Profit', value = f'{moneyearned - moneylost} Botcoin', inline = True)
        if "artists" in users[str(message.author.id)]["activities"]:
            embed.add_field(name = 'Music Stats:', value = 'How you\'ve listened so far!', inline = False)
            res = nlargest(1,
                users[str(message.author.id)]['activities']["artists"],
                key=users[str(message.author.id)]['activities']["artists"].get)
            if len(res) > 0:
                time = [users[str(message.author.id)]['activities']["artists"][res[0]], 'seconds']
                if time[0] > 120:
                    time[0] /= 60
                    time[1] = 'minutes'
                if time[0] > 120:
                    time[0] /= 60
                    time[1] = 'hours'
                embed.add_field(name = '#1 Artist', value = f'{res[0]} with {round(time[0], 2)} {time[1]}')
            if "tracks" in users[str(message.author.id)]['activities'] and len(users[str(message.author.id)]['activities']["tracks"]) > 0 :
                besttime = 0
                besttrack = {}
                name = 0
                for track in users[str(message.author.id)]['activities']["tracks"]:
                    if users[str(message.author.id)]['activities']["tracks"][track]['time'] > besttime:
                        besttime = users[str(message.author.id)]['activities']["tracks"][track]['time']
                        besttrack = users[str(message.author.id)]['activities']["tracks"][track]
                        name = track
                time = [besttrack['time'], 'seconds']
                if time[0] > 120:
                    time[0] /= 60
                    time[1] = 'minutes'
                if time[0] > 120:
                    time[0] /= 60
                    time[1] = 'hours'
                embed.add_field(name = '#1 Track', value = f'{name} by {besttrack["artist"]} with {round(time[0], 2)} {time[1]}')
            if "albums" in users[str(message.author.id)]['activities'] and len(users[str(message.author.id)]['activities']['albums']) > 0:
                besttime = 0
                bestalbum = {}
                name = 0
                for album in users[str(message.author.id)]['activities']["albums"]:
                    if users[str(message.author.id)]['activities']["albums"][album]['time'] > besttime:
                        besttime = users[str(message.author.id)]['activities']["albums"][album]['time']
                        bestalbum = users[str(message.author.id)]['activities']["albums"][album]
                        name = album
                time = [bestalbum['time'], 'seconds']
                # embed.set_image(url = bestalbum['albumcover'])
                if time[0] > 120:
                    time[0] /= 60
                    time[1] = 'minutes'
                if time[0] > 120:
                    time[0] /= 60
                    time[1] = 'hours'
                embed.add_field(name = '#1 Album', value = f'{name} by {bestalbum["artist"]} with {round(time[0], 2)} {time[1]}')
                time = [users[str(message.author.id)]['activities']["listening"]["Spotify"], 'seconds']
                if time[0] > 120:
                    time[0] /= 60
                    time[1] = 'minutes'
                if time[0] > 120:
                    time[0] /= 60
                    time[1] = 'hours'
                embed.add_field(name = 'Total time on Spotify', value = f'{round(time[0], 2)} {time[1]} \n')
        if len(users[str(message.author.id)]["activities"]["playing"]) > 0 and "playing" in users[str(message.author.id)]["activities"]:
            embed.add_field(name = 'Game Stats:', value = 'How you\'ve played so far!', inline = False)
            gametime = 0
            for game in users[str(message.author.id)]["activities"]["playing"]:
                gametime += users[str(message.author.id)]["activities"]["playing"][game]
            gamesplayed = len(users[str(message.author.id)]['activities']["playing"])
            embed.add_field(name = 'Unique Games Played:', value = f'{gamesplayed}', inline = True)
            time = [gametime, 'seconds']
            if time[0] > 120:
                time[0] /= 60
                time[1] = 'minutes'
            if time[0] > 120:
                time[0] /= 60
                time[1] = 'hours'
            embed.add_field(name = 'Time Spent Playing:', value = f'{round(time[0], 2)} {time[1]}', inline = True)
            res = nlargest(1,
                users[str(message.author.id)]['activities']["playing"],
                key=users[str(message.author.id)]['activities']["playing"].get)
            time = [users[str(message.author.id)]['activities']["playing"][res[0]], 'seconds']
            if time[0] > 120:
                time[0] /= 60
                time[1] = 'minutes'
            if time[0] > 120:
                time[0] /= 60
                time[1] = 'hours'
            embed.add_field(name = '#1 Game', value = f'{res[0]} with {round(time[0], 2)} {time[1]}', inline = True)

        button1 = Button(label = 'Yes!', style = discord.ButtonStyle.green, emoji = "✅")
        button2 = Button(label = 'No!', style = discord.ButtonStyle.red, emoji = "✖")
        async def button_callback(interaction):
            if interaction.user != message.author:
                return
            try:
                await response.delete()
            except:
                print('oops')
            await interaction.response.send_message(ephemeral=False, embed = embed)
            return
        async def button_callback2(interaction):
            if interaction.user != message.author:
                return
            try:
                await response.delete()
            except:
                print('oops')
            await interaction.response.send_message(ephemeral=True, embed = embed)
            return
        button1.callback = button_callback
        button2.callback = button_callback2
        view = discord.ui.View(timeout=None)
        view.add_item(button1)
        view.add_item(button2)
        response = await message.channel.send("Post publicly in the channel?", view = view)
        try:
            await bot.wait_for("button_click")
        except:
            print('angry')
        

#####################################################################################

    if message.content.startswith('BBsuggest'):
        await message.channel.send('What\'s your suggestion for BotBot?')
        suggestionBox = open(f'{cwd}data\\suggestions.txt', "a")
        def check(m: discord.Message):
          return m.author.id == message.author.id and m.channel == message.channel
        monthmsg = await client.wait_for('message', check = check)
        await message.channel.send(
            'Thanks for the suggestion! It probably sucked.')
        now = datetime.now(tz)
        suggestionBox.write(
            str('\n' + monthmsg.content + ' - ' + str(message.author)))
        suggestionBox.close()
        channel = await client.fetch_channel('1078432676542951526')
        await channel.send('\n' + monthmsg.content + ' - ' + str(message.author) + ' : ' + str(now))

#####################################################################################

    if message.content.startswith('BBreveal'):
        await message.channel.send('What\'the password?')
        def check(m: discord.Message):
          return m.author.id == message.author.id and m.channel == message.channel
        monthmsg = await client.wait_for('message', check = check)
        if monthmsg.content == "password":
            await message.channel.send(
                "Congrats! The next step is at: \n https://docs.google.com/document/d/1S3u67X10YJk9xuyjV3zy_G3P-sCV_Bfva9K3KvGYmHQ/edit?usp=sharing")
        else:
            await message.channel.send("Password Incorrect. You have 1 more guess. ||Jk that'd be mean||")

#####################################################################################

    if message.content.startswith('BBaddaduck'):
        with open(f'{cwd}ducks.json', 'r') as f:
                ducks = json.load(f)
        await message.channel.send('What\'s your duck image link?')
        def check(m: discord.Message):
          return m.author.id == message.author.id and m.channel == message.channel
        monthmsg = await client.wait_for('message', check = check)
        if not monthmsg.content.startswith('https'):
            content = monthmsg.attachments[0].url
        else:
            content = monthmsg.content
        if content in ducks["ducks"]:
            return await message.channel.send("This pic is already in the list dummy.")
        await message.channel.send(
            'Thanks for the duck! If it\'s a good one, you\'ll be rewarded, and there will be a new duck in the pool.')
        now = datetime.now(tz)
        button1 = Button(label = 'Yes!', style = discord.ButtonStyle.green, emoji = "✅")
        button2 = Button(label = 'No!', style = discord.ButtonStyle.red, emoji = "✖")
        async def button_callback(interaction):
            text = interaction.message.content.split()
            pic = text[1]
            user = (text[2])
            await change_money(users, user, 10)
            bal = get_bal(users, user)
            await message.author.send(f"You have been rewarded 10 BotCoin for your duck pic. Thanks! You now have {bal} BotCoin.")
            ducks["ducks"].append(pic)
            print("new duck pog")
            with open(f'{cwd}data\\users.json', 'w') as f:
                    json.dump(users, f)
            with open(f'{cwd}ducks.json', 'w') as f:
                    json.dump(ducks, f)
            try:
                await response.delete()
            except:
                print('yay')
        async def button_callback2(interaction):
            text = interaction.message.content.split()
            user = client.fetch_user(text[2])
            await user.send("Your duck pic was rejected. Nerd.")
            try:
                await response.delete()
            except:
                print('oops')
        button1.callback = button_callback
        button2.callback = button_callback2
        view = discord.ui.View(timeout=None)
        view.add_item(button1)
        view.add_item(button2)
        channel = await client.fetch_channel("1067851792093819002")
        # user = await client.fetch_user("323518323679559721")
        out = ("<@323518323679559721>" + str('\n' + content + ' ' + str(message.author.id) + ' at ' +
            now.strftime("%m/%d/%Y %H:%M:%S") + '\n' + 'duck'))
        response = await channel.send(out, view = view)
        try:
            await bot.wait_for("button_click")
        except:
            print('angry')

#####################################################################################

    if message.content.startswith('BBaddarat'):
        with open(f'{cwd}data\\rats.json', 'r') as f:
                rats = json.load(f)
        await message.channel.send('What\'s your rat image link?')
        def check(m: discord.Message):
          return m.author.id == message.author.id and m.channel == message.channel
        monthmsg = await client.wait_for('message', check = check)
        if not monthmsg.content.startswith('https'):
            content = monthmsg.attachments[0].url
        else:
            content = monthmsg.content
        if content in rats["rats"]:
            return await message.channel.send("This pic is already in the list dummy.")
        await message.channel.send(
            'Thanks for the rat! If it\'s a good one, you\'ll be rewarded, and there will be a new rat in the pool.')
        now = datetime.now(tz)
        button1 = Button(label = 'Yes!', style = discord.ButtonStyle.green, emoji = "✅")
        button2 = Button(label = 'No!', style = discord.ButtonStyle.red, emoji = "✖")
        async def button_callback(interaction):
            text = interaction.message.content.split()
            pic = text[1]
            await change_money(users, text[2], 10)
            bal = get_bal(users, text[2])
            await message.author.send(f"You have been rewarded 10 BotCoin for your rat pic. Thanks! You now have {bal} BotCoin.")
            rats["rats"].append(pic)
            print("new rat pog")
            with open(f'{cwd}data\\users.json', 'w') as f:
                    json.dump(users, f)
            with open(f'{cwd}data\\rats.json', 'w') as f:
                    json.dump(rats, f)
            try:
                await response.delete()
            except:
                print('yay')
        async def button_callback2(interaction):
            text = interaction.message.content.split()
            user = await client.fetch_user(text[2])
            await user.send("Your rat pic was rejected. Nerd.")
            try:
                await response.delete()
            except:
                print('oops')
        button1.callback = button_callback
        button2.callback = button_callback2
        view = discord.ui.View(timeout=None)
        view.add_item(button1)
        view.add_item(button2)
        channel = await client.fetch_channel("1067851792093819002") #the duck rat channel
        # user = await client.fetch_user("323518323679559721") me
        out = ("<@323518323679559721>" + str('\n' + content + ' ' + str(message.author.id) + ' at ' +
            now.strftime("%m/%d/%Y %H:%M:%S") + '\n' + 'rat'))
        response = await channel.send(out, view = view)
        try:
            await bot.wait_for("button_click")
        except:
            print('angry')

#####################################################################################

    if message.content.startswith('BBaddapanda'):
        with open(f'{cwd}data\\redpanda.json', 'r') as f:
                redpanda = json.load(f)
        await message.channel.send('What\'s your red panda image link?')
        def check(m: discord.Message):
          return m.author.id == message.author.id and m.channel == message.channel
        monthmsg = await client.wait_for('message', check = check)
        if not monthmsg.content.startswith('https'):
            content = monthmsg.attachments[0].url
        else:
            content = monthmsg.content
        if content in redpanda["redpandas"]:
            return await message.channel.send("This pic is already in the list dummy.")
        await message.channel.send(
            'Thanks for the red panda! If it\'s a good one, you\'ll be rewarded, and there will be a new red panda in the pool.')
        now = datetime.now(tz)
        button1 = Button(label = 'Yes!', style = discord.ButtonStyle.green, emoji = "✅")
        button2 = Button(label = 'No!', style = discord.ButtonStyle.red, emoji = "✖")
        async def button_callback(interaction):
            text = interaction.message.content.split()
            pic = text[1]
            await change_money(users, text[2], 10)
            bal = get_bal(users, text[2])
            await message.author.send(f"You have been rewarded 10 BotCoin for your red panda pic. Thanks! You now have {bal} BotCoin.")
            redpanda["redpandas"].append(pic)
            print("new redpanda pog")
            with open(f'{cwd}data\\users.json', 'w') as f:
                    json.dump(users, f)
            with open(f'{cwd}data\\redpanda.json', 'w') as f:
                    json.dump(redpanda, f)
            try:
                await response.delete()
            except:
                print('yay')
        async def button_callback2(interaction):
            text = interaction.message.content.split()
            user = await client.fetch_user(text[2])
            await user.send("Your red panda pic was rejected. Nerd.")
            try:
                await response.delete()
            except:
                print('oops')
        button1.callback = button_callback
        button2.callback = button_callback2
        view = discord.ui.View(timeout=None)
        view.add_item(button1)
        view.add_item(button2)
        channel = await client.fetch_channel("1067851792093819002") #the duck rat redpanda channel
        # user = await client.fetch_user("323518323679559721") me
        out = ("<@323518323679559721>" + str('\n' + content + ' ' + str(message.author.id) + ' at ' +
            now.strftime("%m/%d/%Y %H:%M:%S") + '\n' + 'panda'))
        response = await channel.send(out, view = view)
        try:
            await bot.wait_for("button_click")
        except:
            print('angry')

#####################################################################################

    if message.content.startswith('BBaddafrog'):
        with open(f'{cwd}data\\frogs.json', 'r') as f:
                frogs = json.load(f)
        await message.channel.send('What\'s your frog image link?')
        def check(m: discord.Message):
          return m.author.id == message.author.id and m.channel == message.channel
        monthmsg = await client.wait_for('message', check = check)
        if not monthmsg.content.startswith('https'):
            content = monthmsg.attachments[0].url
        else:
            content = monthmsg.content
        if content in frogs["frogs"]:
            return await message.channel.send("This pic is already in the list dummy.")
        await message.channel.send(
            'Thanks for the frog! If it\'s a good one, you\'ll be rewarded, and there will be a new frog in the pool.')
        now = datetime.now(tz)
        button1 = Button(label = 'Yes!', style = discord.ButtonStyle.green, emoji = "✅")
        button2 = Button(label = 'No!', style = discord.ButtonStyle.red, emoji = "✖")
        async def button_callback(interaction):
            text = interaction.message.content.split()
            pic = text[1]
            await change_money(users, text[2], 10)
            bal = get_bal(users, text[2])
            await message.author.send(f"You have been rewarded 10 BotCoin for your frog pic. Thanks! You now have {bal} BotCoin.")
            frogs["frogs"].append(pic)
            print("new frogs pog")
            with open(f'{cwd}data\\users.json', 'w') as f:
                    json.dump(users, f)
            with open(f'{cwd}data\\frogs.json', 'w') as f:
                    json.dump(frogs, f)
            try:
                await response.delete()
            except:
                print('yay')
        async def button_callback2(interaction):
            text = interaction.message.content.split()
            user = await client.fetch_user(text[2])
            await user.send("Your red frog pic was rejected. Nerd.")
            try:
                await response.delete()
            except:
                print('oops')
        button1.callback = button_callback
        button2.callback = button_callback2
        view = discord.ui.View(timeout=None)
        view.add_item(button1)
        view.add_item(button2)
        channel = await client.fetch_channel("1067851792093819002") #the duck rat redpanda channel
        # user = await client.fetch_user("323518323679559721") me
        out = ("<@323518323679559721>" + str('\n' + content + ' ' + str(message.author.id) + ' at ' +
            now.strftime("%m/%d/%Y %H:%M:%S") + '\n' + 'frog'))
        response = await channel.send(out, view = view)
        try:
            await bot.wait_for("button_click")
        except:
            print('angry')

#####################################################################################

    if message.content.startswith('BBaddapet'):
        with open(f'{cwd}data\\pets.json', 'r') as f:
                pets = json.load(f)
        await message.channel.send('What\'s your pet image link?')
        def check(m: discord.Message):
          return m.author.id == message.author.id and m.channel == message.channel
        monthmsg = await client.wait_for('message', check = check)
        if not monthmsg.content.startswith('https'):
            content = monthmsg.attachments[0].url
        else:
            content = monthmsg.content
        if content in pets["pets"]:
            return await message.channel.send("This pic is already in the list dummy.")
        await message.channel.send(
            'Thanks for the pet! If it\'s a good one, you\'ll be rewarded, and there will be a new pet in the pool.')
        now = datetime.now(tz)
        button1 = Button(label = 'Yes!', style = discord.ButtonStyle.green, emoji = "✅")
        button2 = Button(label = 'No!', style = discord.ButtonStyle.red, emoji = "✖")
        async def button_callback(interaction):
            text = interaction.message.content.split()
            pic = text[1]
            with open(f'{cwd}data\\users.json', 'r') as f:
                users = json.load(f)
            await change_money(users, text[2], 10)
            bal = get_bal(users, text[2])
            await message.author.send(f"You have been rewarded 10 BotCoin for your pet pic. Thanks! You now have {bal} BotCoin.")
            pets["pets"].append(pic)
            print("new pets pog")
            with open(f'{cwd}data\\users.json', 'w') as f:
                    json.dump(users, f)
            with open(f'{cwd}data\\pets.json', 'w') as f:
                    json.dump(pets, f)
            try:
                await response.delete()
            except:
                print('yay')
        async def button_callback2(interaction):
            text = interaction.message.content.split()
            user = await client.fetch_user(text[2])
            await user.send("Your pet pic was rejected. Nerd.")
            try:
                await response.delete()
            except:
                print('oops')
        button1.callback = button_callback
        button2.callback = button_callback2
        view = discord.ui.View(timeout=None)
        view.add_item(button1)
        view.add_item(button2)
        channel = await client.fetch_channel("1067851792093819002") #the duck rat redpanda channel
        # user = await client.fetch_user("323518323679559721") me
        out = ("<@323518323679559721>" + str('\n' + content + ' ' + str(message.author.id) + ' at ' +
            now.strftime("%m/%d/%Y %H:%M:%S") + '\n' + 'pets'))
        response = await channel.send(out, view = view)
        try:
            await bot.wait_for("button_click")
        except:
            print('angry')

#####################################################################################

    if message.content.startswith('BBheadsup'):
        guessers = []
        helpers = []

        categorySelect = Select( 
            placeholder = "Pick a category to play:",
            options = []
        )
        wordMessage = 1
        currButtons = 1
        category = ""
        correct = 0
        passed = 0
        numberOrder = []
        wordsList = []
        wordNum = 1
        currWord = ""
        wordStats ={}
        beginMessage = 0
        async def guesser_callback(interaction):
            await interaction.response.defer()
            nonlocal guessers 
            if not interaction.user.id in guessers:
                guessers.append(interaction.user.id)
            view = discord.ui.View(timeout=None)
            guesserBtn = Button(label = f'Guesser ({len(guessers)})', style = discord.ButtonStyle.gray, emoji = "🔍")
            helperBtn = Button(label = f'Helper ({len(helpers)})', style = discord.ButtonStyle.blurple, emoji = "🎯")
            startBtn = Button(label = 'Start', style = discord.ButtonStyle.green, emoji = "▶")
            view.add_item(guesserBtn)
            view.add_item(helperBtn)
            view.add_item(startBtn)
            guesserBtn.callback = guesser_callback
            helperBtn.callback = helper_callback
            startBtn.callback = start_callback
            await interaction.message.edit(view = view)

        async def helper_callback(interaction):
            await interaction.response.defer()
            nonlocal helpers
            if not interaction.user.id in helpers:
                helpers.append(interaction.user.id)
            view = discord.ui.View(timeout=None)
            guesserBtn = Button(label = f'Guesser ({len(guessers)})', style = discord.ButtonStyle.gray, emoji = "🔍")
            helperBtn = Button(label = f'Helper ({len(helpers)})', style = discord.ButtonStyle.blurple, emoji = "🎯")
            startBtn = Button(label = 'Start', style = discord.ButtonStyle.green, emoji = "▶")
            view.add_item(guesserBtn)
            view.add_item(helperBtn)
            view.add_item(startBtn)
            guesserBtn.callback = guesser_callback
            helperBtn.callback = helper_callback
            startBtn.callback = start_callback
            await interaction.message.edit(view = view)

        async def deferer(interaction):
            await interaction.response.defer()
            pass

        async def correct_callback(interaction):
            nonlocal currButtons
            nonlocal wordNum
            nonlocal category
            wordNum += 1
            nonlocal correct
            correct += 1
            nonlocal wordStats
            nonlocal currWord
            wordStats[currWord] = 1
            currWord = headsupCategories[category][1][numberOrder[wordNum]]
            wordStats[currWord] = 0
            wordsList.append(currWord)
            await wordMessage.edit(content = f"The current word is: **{currWord}**! Help the guesser(s) get it!")

            await interaction.message.edit(content = "Correct!", view = None)
            view = discord.ui.View(timeout=None)
            correctButton = Button(label = f'Correct!', style = discord.ButtonStyle.green, emoji = "✅")
            passButton = Button(label = f'Pass!', style = discord.ButtonStyle.gray, emoji = "👋")
            view.add_item(correctButton)
            view.add_item(passButton)
            correctButton.callback = correct_callback
            passButton.callback = pass_callback
            currButtons = await interaction.message.channel.send("When the guessers say it's correct, Press correct! If you don't know it, press pass!", view = view)
        
        async def pass_callback(interaction):
            nonlocal currButtons
            nonlocal wordNum
            wordNum += 1
            nonlocal passed
            nonlocal category
            passed += 1
            nonlocal wordStats
            nonlocal currWord
            wordStats[currWord] = 2
            currWord = headsupCategories[category][1][numberOrder[wordNum]]
            wordStats[currWord] = 0
            wordsList.append(currWord)
            await wordMessage.edit(content = f"The current word is: **{currWord}**! Help the guesser(s) get it!")
            await interaction.message.edit(content = "Passed!", view = None)
            view = discord.ui.View(timeout=None)
            correctButton = Button(label = f'Correct!', style = discord.ButtonStyle.green, emoji = "✅")
            passButton = Button(label = f'Pass!', style = discord.ButtonStyle.gray, emoji = "👋")
            view.add_item(correctButton)
            view.add_item(passButton)
            correctButton.callback = correct_callback
            passButton.callback = pass_callback
            currButtons = await interaction.message.channel.send("When the guessers say it's correct, Press correct! If you don't know it, press pass!", view = view)

        async def start_game(interaction):
            cats = message.guild.categories
            for cat in cats:
                if cat.name == "games":
                    gameCat = cat
                    break
            guessChannel = ([channel for channel in gameCat.channels if channel.name == "headsup-guessers"])[0]
            helpChannel = ([channel for channel in gameCat.channels if channel.name == "headsup-helpers"])[0]
            await interaction.response.defer()
            nonlocal category
            category = categorySelect.values[0]
            nonlocal numberOrder
            nonlocal currWord
            nonlocal wordsList
            await beginMessage.delete()
            numberOrder = [x for x in range(len(headsupCategories[category][1]))]
            random.shuffle(numberOrder)
            currWord = headsupCategories[category][1][numberOrder[wordNum]]
            wordsList.append(currWord)
            #60 second timer start

            #Start loop
            view = discord.ui.View(timeout=None)
            correctButton = Button(label = f'Correct!', style = discord.ButtonStyle.green, emoji = "✅")
            passButton = Button(label = f'Pass!', style = discord.ButtonStyle.gray, emoji = "👋")
            view.add_item(correctButton)
            view.add_item(passButton)
            correctButton.callback = correct_callback
            passButton.callback = pass_callback
            nonlocal currButtons
            nonlocal wordMessage
            nonlocal wordStats
            wordStats[currWord] = 0
            currButtons = await guessChannel.send("When the guessers say it's correct, Press correct! If you don't know it, press pass!", view = view)
            await helpChannel.send(f"It's the start of a new game!\n------------------------------------\n")
            wordMessage = await helpChannel.send(f"The current word is: **{currWord}**! Help the guesser(s) get it!")
            await asyncio.sleep(60) #TIMER FOR GAME LOOP
            await currButtons.delete()
            embed = discord.Embed(
                title = f'How did your Heads Up game go?',
                description = 'What\'d ya miss?',
                color = discord.Color.dark_green()
            )
            out = ""
            statusDecoder = ["Unfinished", "Correct", "Passed"]
            for attemptedWord in wordStats:
                out += f"{attemptedWord} : {statusDecoder[wordStats[attemptedWord]]}\n"
            embed.add_field(name = "Words attempted", value = out, inline = False)
            nonlocal correct
            nonlocal passed
            stats = f"Total attempted: {wordNum}\nTotal Correct: {correct}\nTotal Passed: {passed}\nSeconds per word attempted: {round(60 / wordNum,2)}\nPercent Correct: {round(100 * (correct / wordNum), 2)}%"
            embed.add_field(name = "Stats", value = stats, inline = False)
            await guessChannel.send("Game over! Here's how you did.", embed = embed)
            await helpChannel.send("Game over! Here's how you did.", embed = embed)
                #Choose correct answer and present it to the helpers
                #Create buttons for the guesser and assign their callbacks
            #End loop at 60 seconds
            #Display answers / missed / leaderboard??

        async def start_callback(interaction):
            await interaction.response.defer()
            nonlocal helpers
            nonlocal guessers
            if(len(helpers) > 0 and len(guessers) > 0):
                #Check if games category exists
                cats = message.guild.categories
                hasGames = False
                overwrites = {
                    message.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                }
                for cat in cats:
                    if cat.name == "games":
                        hasGames = True
                        gameCat = cat
                if hasGames == False:
                    gameCat = await message.guild.create_category(name = "games")
                #Check if headsup-guessers exists
                try:
                    guessChannel = ([channel for channel in gameCat.channels if channel.name == "headsup-guessers"])[0]
                except:
                    guessChannel = await message.guild.create_text_channel("headsup-guessers", overwrites = overwrites, category=gameCat)
                #Check if headsup-helpers exists
                try:
                    helpChannel = ([channel for channel in gameCat.channels if channel.name == "headsup-helpers"])[0]
                except:
                    helpChannel = await message.guild.create_text_channel("headsup-helpers", overwrites = overwrites, category=gameCat)
                #Check if in one of those
                await message.channel.send("Everyone head over to their respective channels! The Heads Up channels are under the 'Games' category of channels.")
                #Set permissions of everyone
                for guesser in guessers:
                    user = message.guild.get_member(guesser)
                    await guessChannel.set_permissions(user, read_messages=True, send_messages=True)
                    await helpChannel.set_permissions(user, read_messages=False, send_messages=False)
                for helper in helpers:
                    user = message.guild.get_member(helper)
                    await helpChannel.set_permissions(user, read_messages=True, send_messages=True)
                    await guessChannel.set_permissions(user, read_messages=False, send_messages=False)
                #Let guessers pick category
                view = discord.ui.View(timeout=None)
                beginButton = Button(label = f'Begin!', style = discord.ButtonStyle.green, emoji = "🎉")
                beginButton.callback = start_game

                for cat in headsupCategories:
                    categorySelect.add_option(label = cat, emoji = headsupCategories[cat][0])
                view.add_item(categorySelect)
                view.add_item(beginButton)
                nonlocal beginMessage
                beginMessage = await guessChannel.send(view=view)
                # for i in range(len(headsupCategories)):
                #     categorySelect.add_option(label = headsupCategories[i])
                #Start game with buttons
                pass

        view = discord.ui.View(timeout=None)
        guesserBtn = Button(label = 'Guesser', style = discord.ButtonStyle.gray, emoji = "🔍")
        helperBtn = Button(label = 'Helper', style = discord.ButtonStyle.blurple, emoji = "🎯")
        startBtn = Button(label = 'Start', style = discord.ButtonStyle.green, emoji = "▶")
        view.add_item(guesserBtn)
        view.add_item(helperBtn)
        view.add_item(startBtn)
        guesserBtn.callback = guesser_callback
        helperBtn.callback = helper_callback
        startBtn.callback = start_callback
        categorySelect.callback = deferer
        startMsg = await message.channel.send("Welcome to Heads up, the multiplayer word guessing game!\n If you are the guesser(s), click the guessing button. If you're a helper, click helper.\n Once all players have clicked, someone press start!", view = view)


#####################################################################################

    if message.content.startswith('BBguessnum'):
      with open(f'{cwd}data\\guessnum.json', 'r') as f:
          guessnum = json.load(f)

      args = message.content.split()
      #argument error
      if len(args) != 4:
        await message.channel.send("Incorrect format: BBguessnum [@user] [wager] [range]\n ex: BBguessnum @loftzo 30 10 (this starts a game between you and @loftzo, with a wager of 30, guessing from numbers 1-10)")
        return
      #initialize
      guild = message.guild
      player1 = message.author
      player2 = guild.get_member(int(args[1][2:-1]))
      wager = int(args[2])
      numrange = int(args[3])
      if numrange < 2:
        return await message.channel.send("Range cannot be less than 2!")
      if wager < 1:
        return await message.channel.send("Wager cannot be less than 1!")
      if not player2:
        return await message.channel.send("Player is not in this server!")
      if player2.id == message.author.id:
        return await message.channel.send("You can\'t play against yourself! (narcissist)")
      def check(m: discord.Message):  # m = discord.Message.
        return m.channel.id == message.channel.id and (m.author.id == message.author.id or m.author.id == player2.id) and m.content.isnumeric() and int(m.content) > 0 and int(m.content) < numrange
      #make sure both players can afford it at first 
      if get_bal(users, player1) < wager:
        await message.channel.send(f"<@{player1.id}> is too poor!")
        return
      if get_bal(users, player2) < wager:
        await message.channel.send(f"<@{player2.id}> is too poor!")
        return
      #check if active game, if not, setup game in guessnum
      rand = random.randrange(1, numrange)
      currGame = {'players' : [str(player1), str(player2)], 'wager' : wager, 'answer' : rand, 'p1guess' : '', 'p2guess' : ''}
      if not 'active' in guessnum:
        guessnum['active'] = []
      await message.channel.send(f"Guess a number 1-{numrange}: (30 seconds until game quits)")
      try:
          guess1 = await client.wait_for('message', check = check, timeout=30.0)
          if guess1.author == player1:
            p1guess = guess1
          elif guess1.author == player2:
            p2guess = guess1
          else:
            guessnum['active'].append(currGame)
            return await guess1.channel.send('Game was interrupted somehow and cancelled.')
            
          guess2 = await client.wait_for('message', check = check, timeout=30.0)
          if guess2.author == player1:
            p1guess = guess2
          elif guess2.author == player2:
            p2guess = guess2
          else:
            guessnum['active'].append(currGame)
            return await guess1.channel.send('Game was interrupted somehow and cancelled.')
      except asyncio.TimeoutError:
          return await message.channel.send(f'Sorry, you took too long! Game cancelled.')
      
      currGame['p1guess'] = p1guess.content
      currGame['p2guess'] = p2guess.content

      dist1 = abs(int(p1guess.content) - rand)
      dist2 = abs(int(p2guess.content) - rand)

      if dist1 < dist2:
        await change_money(users, player1, wager)
        await change_money(users, player2, -1*wager)
        await message.channel.send(f'<@{player1.id}>\'s guess ({p1guess.content}) was closer to the target ({rand}) than <@{player2.id}>, whose guess was {p2guess.content}. <@{player1.id}> is awarded {str(wager)} BotCoin, and <@{player2.id}> loses {str(wager)} BotCoin.')
      if dist2 < dist1:
        await change_money(users, player2, wager)
        await change_money(users, player1, -1*wager)
        await message.channel.send(f'<@{player2.id}>\'s guess ({p2guess.content}) was closer to the target ({rand}) than <@{player1.id}>, whose guess was {p1guess.content}. <@{player2.id}> is awarded {str(wager)} BotCoin, and <@{player1.id}> loses {str(wager)} BotCoin.')
      if dist1 == dist2:
        await change_money(users, player1, -1*wager)
        await change_money(users, player2, -1*wager)
        await message.channel.send(f"Yikes, unlucky! The number was {rand}, so you were both {dist1} away from it. Money\'s mine then!")
      
      guessnum['active'].append(currGame)
      
      with open(f'{cwd}data\\guessnum.json', 'w') as f:
                json.dump(guessnum, f)
      

#####################################################################################

    if message.content.startswith('BBpay'):
        
        args = message.content.split()
        if len(args) != 3:
            return await message.channel.send('Incorrect usage! Needs to be \'BBpay [@user] [amount]\'')
        if isinstance(message.channel, discord.channel.DMChannel):
            return await message.channel.send('Unfortunately, your payments have to be public (because it\'s hard to code otherwise)')
        payee = message.guild.get_member(int(args[1][2:-1]))
        payer = message.author
        if args[2][0] == '-' and args[2][1:].isnumeric():
            return await message.channel.send('You can\'t steal from them, dick.')
        if not args[2].isnumeric():
            return await message.channel.send(f'{args[2]} is not a valid payment amount')
        payment = int(args[2])
        if payment == 0:
            return await message.channel.send('Why would you pay someone 0...')
        if payment > get_bal(users, payer):
            return await message.channel.send('LMAO you\'re too broke to send that much.')
        if payer == payee:
            return await message.channel.send(f'You sent yourself {payment} BotCoin... i guess.')
        # if payment >= 100:
        #     payment -= 10
        #     await message.channel.send('That\'s a nice payment there. Would be a shame if someone were to.. tax it.')
        await change_money(users, payer, -1 * payment)
        await change_money(users, payee, payment)
        await message.channel.send('Payment sent.')

#####################################################################################

    if message.content.startswith('BBmyalbums'):
        out = await get_albums(users, message.author.id, message.guild)
        await message.channel.send(file = out[0], embed = out[1])

#####################################################################################

    if message.content.startswith('BBmycommands'):
        out = get_commands(users, str(message.author.id))
        await message.channel.send(out)

#####################################################################################

    if message.content.startswith('BBtoday'):
        await message.channel.typing()
        #create embed
        utc = timezone('UTC')
        now = utc.localize(datetime.utcnow())
        now = tz.localize(datetime.now())
        formattedDate = now.strftime('%B %d, %Y')
        embed = discord.Embed(
            title = f'Today is: {formattedDate}',
            description = 'What are today\'s holidays?',
            color = discord.Color.dark_green()
            )
        #get events from nationaltoday.com
        cookies = {
            '_wpfuuid': 'f3748d5c-0532-4c65-97c0-228bb6ac81fc',
            '_gid': 'GA1.2.46966743.1691283950',
            'wordpress_test_cookie': 'WP%20Cookie%20check',
            'wordpress_logged_in_c28a03ee7d73ba32d6ea0458684da84a': 'jacobasmithwork%40gmail.com%7C4844889634%7CdZyHLeqcBuWmISUkgxEsODroWNbpZ16tvCE6QFcTCLm%7C37e1a2ff5a7ddfd55cc8bf754520d1e944b0f45c1a90162c07cca9be53d7c280',
            '_gat_UA-29697889-1': '1',
            '_ga_SQZQY2VH8E': 'GS1.1.1691289523.2.1.1691289743.59.0.0',
            '_ga': 'GA1.2.1729553690.1691283949',
            'FCNEC': '%5B%5B%22AKsRol-T0Klfvba5AXSQ3hhTsj4BsQj0dMZNXM126Vaq63QqWaIf2uZ1EQXF6PExh4o4uBaq1C2htZOwW1HtzxoDMt77nfpDg5xWLHEyYaj784QW_gr8NElzPGijWbjug8SLJ42xdqJS3eYhG3cmVkah1dp5dR4mYg%3D%3D%22%5D%2Cnull%2C%5B%5D%5D',
        }
        headers = {
            'authority': 'nationaltoday.com',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'max-age=0',
            'referer': 'https://nationaltoday.com/',
            'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Opera GX";v="100"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 OPR/100.0.0.0',
        }
        response = requests.get(f'https://nationaltoday.com/{now.strftime("%B").lower()}-{int(now.day)}-holidays/', cookies=cookies, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")  # parse the HTML content with BeautifulSoup
        holidays = soup.find_all("h3", {"class": "holiday-title"})
        desc = soup.find_all("p", {"class" : "excerpt"})
        img = soup.find_all("a", {"class" : "day-card-mask"})
        embed.set_image(url = (img[1]['style'][22:-2]))
        names = [''] * 5
        descs = [''] * 5
        for i in range(5):
            if i > len(holidays):
                break
            names[i] = holidays[i+1].text
            descs[i] = desc[i].text
        text = ""
        for i in range(len(names)):
            embed.add_field(name = names[i], value = descs[i], inline = False)

        #check server anniversaries
        impDays = [1, 50, 69, 100, 150, 200, 300, 400, 420, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600]
        members = message.channel.guild.members
        for member in members:
            join = member.joined_at
            #birthday
            if(join.day == now.day and join.month == now.month):
                #print("anniverary")
                years = abs(join.year - now.year)
                if years != 1:
                    embed.add_field(name = f'It is <@{member.display_name}>\'s Server Anniversary!',
                                    value = f'<@{member.id}> has been in the server for {years} years!',
                                    inline = False
                    )
                else:
                    embed.add_field(name = f'It is <@{member.display_name}>\'s Server Anniversary!',
                                    value = f'<@{member.id}> has been in the server for {years} year!',
                                    inline = False
                    )
            #half birthday
            elif(join.day == now.day and abs(join.month - now.month) == 6):
                #print("half birthday")
                years = abs(join.year - now.year)
                if years != 0:
                    embed.add_field(name = f'It is {member.display_name}\'s Server Half Anniversary!',
                                value = f'<@{member.id}> has been in the server for {years} and a half years!',
                                inline = False
                    )
                else:
                    embed.add_field(name = f'It is {member.display_name}\'s Server Half Anniversary!',
                                value = f'<@{member.id}> has been in the server for half a year!',
                                inline = False
                    )
            #important day milestones
            elif((now - join).days in impDays):
                days = (now - join).days
                #print("important day milestone")
                if days != 1:
                    embed.add_field(name = f'It is {member.display_name}\'s {days}\'th day on the Server!',
                            value = f'Congrats to <@{member.id}> on sticking around!',
                            inline = False
                    )
                else:
                    embed.add_field(name = f'It is {member.display_name}\'s {days}\'st day on the Server!',
                            value = f'Congrats to <@{member.id}> on sticking around!',
                            inline = False
                    )
            #check real birthdays if provided
            if str(member.id) in users:
                if 'birthday' in users[str(member.id)]:
                    bdaylist = users[str(member.id)]['birthday']
                    if now.month == int(bdaylist[1]) and now.day == int(bdaylist[2]):
                        years = abs(int(bdaylist[0]) - now.year)
                        embed.add_field(name = f'It is {member.display_name}\'s Birthday!',
                                        value = f'<@{member.id}> just turned {years} years old!',
                                        inline = False
                        )
        await message.channel.send(embed = embed)

#####################################################################################

    if message.content.startswith('BBbirthday'):
        if not 'birthday' in users[str(message.author.id)]:
            # users[str(message.author.id)]['birthday'] == ""
            await message.channel.send('When\'s your Birth Month homeboy? (1-12)')
        else:
            await message.channel.send('When\'s your new Birth Month homeboy? (1-12)')
        def check(m: discord.Message):
            return m.channel == message.channel and m.author == message.author
        def check2(m2 : discord.Message):
            return m2.channel == message.channel and m2.author == message.author
        def check3(m3 : discord.Message):
            return m3.channel == message.channel and m3.author == message.author
        monthmsg = await client.wait_for('message', check = check, timeout=None)
        if monthmsg.content.isdigit() and int(monthmsg.content) >= 1 and int(monthmsg.content) <= 12:
            month = monthmsg.content
            await monthmsg.channel.send("What is your Birth Day? (1-31)")
            daymsg = await client.wait_for('message', check = check2, timeout=None)
            if daymsg.content.isdigit() and int(daymsg.content) >= 1 and int(daymsg.content) <= 31:
                day = daymsg.content
                await daymsg.channel.send("What is your Birth Year? (Valid Year)")
                yearmsg = await client.wait_for('message', check = check3, timeout=None)
                if yearmsg.content.isdigit() and int(yearmsg.content) >= 1940 and int(yearmsg.content) <= 2040:
                    year = yearmsg.content
                    try:
                        bday = date(int(year), int(month), int(day))
                        if bday:
                            users[str(message.author.id)]['birthday'] = [year, month, day]
                            await message.channel.send("Noted! You'll be remembered on your birthday if anyone uses the 'BBtoday' command.")
                    except:
                        await message.channel.send("Invalid Birthday. Try again.")
                else:
                    await yearmsg.channel.send("Invalid Year. Try again.")
            else:
                await daymsg.channel.send("Invalid Day. Try again.")
        else:
            await monthmsg.channel.send("Invalid Month. Try again.")

#####################################################################################

    if message.content.startswith('BBstartreminders'):
        if remindersOn == False:
            remindersOn = True
            

#####################################################################################

    if message.content.startswith('BBguessword'):
        with open(f'{cwd}data\\wotd.json', 'r') as f:
            wotd = json.load(f)
        with open(f'{cwd}data\\users.json', 'r') as f:
            users = json.load(f)
        if wotd['done'] == 1:
            return await message.channel.send('The word has already been guessed today!')
        if wotd['players'][str(message.author.id)]['today'] == 1:
            return await message.channel.send('You have already guessed today!')
        await message.channel.send('What\'s your guess for the word of the day?')
        def check(m: discord.Message):
            return m.author.id == message.author.id and m.channel == message.channel
        monthmsg = await client.wait_for('message', check = check)
        word = wotd['wotd']
        if monthmsg.content.lower() == wotd['wotd']:
            wotd['players'][str(message.author.id)]['correct'] += 1
            wotd['done'] = 1
            await monthmsg.reply(f'Good Job! You Guessed todays word, \"{word}.\" You win 100 BotCoin.')
            await change_money(users, message.author, 100)
        else:
            wotd['players'][str(message.author.id)]['incorrect'] += 1
            await monthmsg.reply(f'Sorry dude, not quite. Better luck tomorrow!')

        wotd['players'][str(message.author.id)]['today'] = 1
        with open(f'{cwd}data\\wotd.json', 'w') as f:
                    json.dump(wotd, f)

#####################################################################################

    with open(f'{cwd}data\\users.json', 'w') as f:
        json.dump(users, f)

    if message.content.startswith('BBadmin'):
      if not message.author.id == 323518323679559721:
        await message.channel.send('Access denied. You\'re not an admin, duh')

    for word in adminCommands:
        if message.content.startswith(word) and not message.author.id == 323518323679559721:
            await message.channel.send('Access denied. You\'re not an admin, stinkyhead.')

#############$$$$$$$$$$$$$$$!!!!!!!!!!!!!!!!!!!!!!!!!$$$$$$$$$$$$$$$#################
#############@@@@@@@@@@@@@@@ADMIN COMMANDS BELOW HERE@@@@@@@@@@@@@@@#################
#############%%%%%%%%%%%%%%%!!!!!!!!!!!!!!!!!!!!!!!!!%%%%%%%%%%%%%%%#################
    
    with open(f'{cwd}data\\users.json', 'r') as f:
        users = json.load(f)
        
    if message.author.id == 323518323679559721:
        #print('admin access confirmed')

#############$$$$$$$$$$$$$$$!!!!!!!!!!!!!!!!!!!!!!!!!$$$$$$$$$$$$$$$#################

        if message.content.startswith('BBreward'):
            args = message.content.split(',')
            if len(args) != 4:
                await message.channel.send(
                    'Incorrect usage! Needs: BBreward, [user_id], [rewardAmt], [reason]'
                )
            else:
                await update_data(users, args[1])
                await change_money(users, args[1], args[2])
                if isinstance(message.channel, discord.channel.DMChannel):
                    return
                guild = message.guild
                member = await client.fetch_user(args[1])
                await member.send(f"Hey! You\'ve been rewarded {args[2]} BotCoin for: \"{args[3]}\"")


#############$$$$$$$$$$$$$$$!!!!!!!!!!!!!!!!!!!!!!!!!$$$$$$$$$$$$$$$#################

        if message.content.startswith('BBgetbal'):
            args = message.content.split()
            if len(args) != 2:
                await message.channel.send(
                    'Incorrect usage! Needs: BBgetbal [user_id]'
                )
            else:
                await update_data(users, str(args[1]))
                await check_bal(users, str(args[1]), message.channel)


#############$$$$$$$$$$$$$$$!!!!!!!!!!!!!!!!!!!!!!!!!$$$$$$$$$$$$$$$#################

        if message.content.startswith('BBaddexp'):
            args = message.content.split()
            if len(args) != 3:
                await message.channel.send(
                    'Incorrect usage! Needs: BBaddexp [user_id] [expAmt]'
                )
            else:
                await update_data(users, args[1])
                await add_experience(users, args[1], args[2])


#############$$$$$$$$$$$$$$$!!!!!!!!!!!!!!!!!!!!!!!!!$$$$$$$$$$$$$$$#################

        if message.content.startswith('BBgetexp'):
            args = message.content.split()
            if len(args) != 2:
                await message.channel.send(
                    'Incorrect usage! Needs: BBgetexp [user_id]'
                )
            else:
                await update_data(users, args[1])
                await message.channel.send(f"<@{args[1]}> has {get_exp(users, args[1])} exp!")


#############$$$$$$$$$$$$$$$!!!!!!!!!!!!!!!!!!!!!!!!!$$$$$$$$$$$$$$$#################

        if message.content.startswith('BBbackup'):
            with open(f'{cwd}data\\users.json', 'r') as f:
                users = json.load(f)
            with open(f'{cwd}data\\usersbackup.json', 'r') as f:
                usersbackup = json.load(f)
            usersbackup = users
            me = await client.fetch_user('323518323679559721')
            await me.send('Backed up. Maybe.')
            with open(f'{cwd}data\\usersbackup.json', 'w') as f:
                json.dump(usersbackup, f)


#############$$$$$$$$$$$$$$$!!!!!!!!!!!!!!!!!!!!!!!!!$$$$$$$$$$$$$$$#################

        if message.content.startswith('BBgetmusic'):
            args = message.content.split()
            if len(args) != 2:
                await message.channel.send(
                    'Incorrect usage! Needs: BBgetmusic [user_id]'
                )
            else:
                await update_data(users, args[1])
                out = await activity_leaderboard(users, args[1], message.channel, 'artists')
                await message.channel.send(out)


#############$$$$$$$$$$$$$$$!!!!!!!!!!!!!!!!!!!!!!!!!$$$$$$$$$$$$$$$#################

        if message.content.startswith('BBgetgames'):
            args = message.content.split()
            if len(args) != 2:
                await message.channel.send(
                    'Incorrect usage! Needs: BBgetgames [user_id]'
                )
            else:
                await update_data(users, args[1])
                out = await activity_leaderboard(users, args[1], message.channel, 'playing')
                await message.channel.send(out)


#############$$$$$$$$$$$$$$$!!!!!!!!!!!!!!!!!!!!!!!!!$$$$$$$$$$$$$$$#################

        if message.content.startswith('BBgetstreams'):
            args = message.content.split()
            if len(args) != 2:
                await message.channel.send(
                    'Incorrect usage! Needs: BBgetstreams [user_id]'
                )
            else:
                await update_data(users, args[1])
                out = await activity_leaderboard(users, args[1], message.channel, 'streaming')
                await message.channel.send(out)


#############$$$$$$$$$$$$$$$!!!!!!!!!!!!!!!!!!!!!!!!!$$$$$$$$$$$$$$$#################

        if message.content.startswith('BBgetstreamgames'):
            args = message.content.split()
            if len(args) != 2:
                await message.channel.send(
                    'Incorrect usage! Needs: BBgetstreamgames [user_id]'
                )
            else:
                await update_data(users, args[1])
                out = await activity_leaderboard(users, args[1], message.channel, 'streamgames')
                await message.channel.send(out)


#############$$$$$$$$$$$$$$$!!!!!!!!!!!!!!!!!!!!!!!!!$$$$$$$$$$$$$$$#################

        if message.content.startswith('BBgetwords'):
            args = message.content.split()
            if len(args) != 2:
                await message.channel.send(
                    'Incorrect usage! Needs: BBgetwords [user_id]'
                )
            else:
                await update_data(users, args[1])
                out =  await user_word_leaderboard(users, args[1], message.channel)
                await message.channel.send(out)


#############$$$$$$$$$$$$$$$!!!!!!!!!!!!!!!!!!!!!!!!!$$$$$$$$$$$$$$$#################

        if message.content.startswith('BBadmin'):
            output = "The current admin commands are:\n"
            for commands in adminCommands:
              output += f"{commands}\n"
            await message.channel.send(output)
          
#############$$$$$$$$$$$$$$$!!!!!!!!!!!!!!!!!!!!!!!!!$$$$$$$$$$$$$$$#################

        if message.content.startswith('BBallwords'):
            allWords = {}
            for people in users:
                for word in users[people]['words']:
                    if not word in allWords:
                        allWords[word] = users[people]['words'][word]
                    else:
                        allWords[word] += users[people]['words'][word]
            res = nlargest(5,
                   allWords,
                   key=allWords.get)
            occurences = []
            output = 'The most used words (minus prepositions and such) are: \n'
            for word in res:
                occurences.append(allWords[word])
            for x in range(5):
                output += ('#' + str(x + 1) + ': ' + str(res[x]) + ' with ' +
                        str(occurences[x]) + ' occurences\n')
            await message.channel.send(output)
            

#############$$$$$$$$$$$$$$$!!!!!!!!!!!!!!!!!!!!!!!!!$$$$$$$$$$$$$$$#################

        if message.content.startswith('BBallmusic'):
            totalTime = 0
            allArtists = {}
            for people in users:
                if not 'artists' in users[people]['activities']:
                    continue
                for artist in users[people]['activities']['artists']:
                    if not artist in allArtists:
                        allArtists[artist] = users[people]['activities']['artists'][artist]
                    else:
                        allArtists[artist] += users[people]['activities']['artists'][artist]
                    totalTime += users[people]['activities']['artists'][artist]
            res = nlargest(5,
                   allArtists,
                   key=allArtists.get)
            timeListened = []
            time = [totalTime, 'seconds']
            if time[0] > 120:
                time[0] /= 60
                time[1] = 'minutes'
            if time[0] > 120:
                time[0] /= 60
                time[1] = 'hours'
            output = f'The most listened to songs are (from a total of {round(time[0], 2)} {time[1]}): \n'
            for artist in res:
                timeListened.append(allArtists[artist])
            for x in range(5):
                time = [timeListened[x], 'seconds']
                if time[0] > 120:
                    time[0] /= 60
                    time[1] = 'minutes'
                if time[0] > 120:
                    time[0] /= 60
                    time[1] = 'hours'
                output += ('#' + str(x + 1) + ': ' + str(res[x]) + ' with ' +
                        str(round(time[0], 2)) + ' ' + str(time[1]) + '\n')
            await message.channel.send(output)
            

#############$$$$$$$$$$$$$$$!!!!!!!!!!!!!!!!!!!!!!!!!$$$$$$$$$$$$$$$#################

        if message.content.startswith('BBallactivities'):
            totalTime = 0
            allActivities = {}
            for people in users:
                if not 'custom' in users[people]['activities']:
                    continue
                for artist in users[people]['activities']['custom']:
                    if not artist in allActivities:
                        allActivities[artist] = users[people]['activities']['custom'][artist]
                    else:
                        allActivities[artist] += users[people]['activities']['custom'][artist]
                    totalTime += users[people]['activities']['custom'][artist]
            res = nlargest(5,
                   allActivities,
                   key=allActivities.get)
            timeListened = []
            time = [totalTime, 'seconds']
            if time[0] > 120:
                time[0] /= 60
                time[1] = 'minutes'
            if time[0] > 120:
                time[0] /= 60
                time[1] = 'hours'
            output = f'The most done activities are (from a total of {round(time[0], 2)} {time[1]}): \n'
            for artist in res:
                timeListened.append(allActivities[artist])
            for x in range(5):
                time = [timeListened[x], 'seconds']
                if time[0] > 120:
                    time[0] /= 60
                    time[1] = 'minutes'
                if time[0] > 120:
                    time[0] /= 60
                    time[1] = 'hours'
                output += ('#' + str(x + 1) + ': ' + str(res[x]) + ' with ' +
                        str(round(time[0], 2)) + ' ' + str(time[1]) + '\n')
            await message.channel.send(output)
            

#############$$$$$$$$$$$$$$$!!!!!!!!!!!!!!!!!!!!!!!!!$$$$$$$$$$$$$$$#################

        if message.content.startswith('BBeconomy'):
            totalMoney = 0
            numPeople = 0
            moneyLeaderboard = {}
            for people in users:
                if not 'botCoin' in users[people]:
                    numPeople += 1
                    continue
                moneyLeaderboard[people] = users[people]['botCoin']
                totalMoney += users[people]['botCoin']
                numPeople += 1
            res = nlargest(5,
                   moneyLeaderboard,
                   key=moneyLeaderboard.get)
            moneys = []
            for people in res:
                moneys.append(moneyLeaderboard[people])
            embed = discord.Embed(
            title = 'State of the BotCoin Ecnonomy',
            description = 'The stats:',
            color = discord.Color.dark_green()
            )
            embed.add_field(name = "Total BotCoin in circulation:", value = totalMoney, inline = False)
            # output = f'**Total BotCoin in circulation:** {totalMoney} \n\n'
            # output += f'**Money Leaderboard:**\n'
            output = ""
            for x in range(len(res)):
                output += f'#{x + 1}: <@{res[x]}> with {moneys[x]} BotCoin\n'
            embed.add_field(name = "Money Leaderboard:", value = output, inline = False)
            output = ""
            # output += f'\n**The poorest individual is:**\n'
            brokemf = min(moneyLeaderboard, key=moneyLeaderboard.get)
            output += f'<@{brokemf}> with {moneyLeaderboard[brokemf]} BotCoin.\n'
            embed.add_field(name = "The poorest individual is:", value = output, inline = False)
            output = ""
            output += f'{str(round((totalMoney / numPeople), 2))}\n'
            embed.add_field(name = "Average BotCoin per person:", value = output, inline = False)
            output = ""
            # output += f'\n**Distribution of Wealth:**\n'
            newMoney = 0
            for x in range(len(res)):
                newMoney += moneys[x]
                output += f'{round(100 * ((x + 1)/numPeople),2)}% of the people hold {round(100 * (newMoney/totalMoney), 2)}% of the wealth.\n'
            embed.add_field(name = "Distribution of Wealth:", value = output, inline = False)
            await message.channel.send(embed = embed)

#############$$$$$$$$$$$$$$$!!!!!!!!!!!!!!!!!!!!!!!!!$$$$$$$$$$$$$$$#################

        if message.content.startswith('BBtesting'):
            return
            # out = checkAchievements(users, hm, guessnum, message.author.id)
            # if out != "":
            #     print(out)
            #     file = await generateAchievement(out, message.author.id, message.guild)
            #     await message.channel.send(f"Congrats <@{message.author.id}>! You've earned the '{out}' Achievement!", file = file)
            #     with open(f'{cwd}data\\users.json', 'w') as f:
            #         json.dump(users, f)


#############$$$$$$$$$$$$$$$!!!!!!!!!!!!!!!!!!!!!!!!!$$$$$$$$$$$$$$$#################

        if message.content.startswith('BBstartjeopardy'):
            vc = message.author.voice.channel
            await vc.connect()
            print("im in")

#############$$$$$$$$$$$$$$$!!!!!!!!!!!!!!!!!!!!!!!!!$$$$$$$$$$$$$$$#################

        if message.content.startswith('BBendjeopardy'):
            for vclient in client.voice_clients:
                await vclient.disconnect(force = True)
                print(vclient.channel)

#############$$$$$$$$$$$$$$$!!!!!!!!!!!!!!!!!!!!!!!!!$$$$$$$$$$$$$$$#################

        if message.content.startswith('BBfarmrpg'):
            cookies = {
                'pac_ocean': 'E15FFD3F',
                '_ga': 'GA1.1.526699074.1690423456',
                'HighwindFRPG': 'IMvnk8ISAq21ORpzP11kEA%3D%3D%3Cstrip%3E%24argon2id%24v%3D19%24m%3D7168%2Ct%3D4%2Cp%3D1%24U29kZ0RaSG9PU0xpYmxIVA%24X1VVajLrPoaMwuO44sCRsPip%2B2ZS0RitZAmPmRYVecw',
                '_ga_94M1PS2E9X': 'GS1.1.1690423455.1.1.1690423823.0.0.0',
            }

            headers = {
                'authority': 'farmrpg.com',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'accept-language': 'en-US,en;q=0.9',
                'cache-control': 'max-age=0',
                # 'cookie': 'pac_ocean=E15FFD3F; _ga=GA1.1.526699074.1690423456; HighwindFRPG=IMvnk8ISAq21ORpzP11kEA%3D%3D%3Cstrip%3E%24argon2id%24v%3D19%24m%3D7168%2Ct%3D4%2Cp%3D1%24U29kZ0RaSG9PU0xpYmxIVA%24X1VVajLrPoaMwuO44sCRsPip%2B2ZS0RitZAmPmRYVecw; _ga_94M1PS2E9X=GS1.1.1690423455.1.1.1690423823.0.0.0',
                'referer': 'https://farmrpg.com/',
                'sec-ch-ua': '"Opera GX";v="99", "Chromium";v="113", "Not-A.Brand";v="24"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'same-origin',
                'sec-fetch-user': '?1',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 OPR/99.0.0.0',
            }
            response = requests.get('https://farmrpg.com/index.php', cookies=cookies, headers=headers)
            soup = BeautifulSoup(response.text, "html.parser")  # parse the HTML content with BeautifulSoup
            all_statuses = soup.find_all("div", {"class": "item-after"})
            # print(soup)
            status_list = []
            status_names = []
            alert_list = []
            alert_names = []
            for x in all_statuses:
                if x.string is not None:
                    status_list.append(x.string.strip(" \\n"))
                    status_names.append(x.previous_sibling.previous_sibling.contents[0])
            for i in range((len(status_names))):
                status_names[i] = str(status_names[i])
                status_names[i].strip(" \n")
                if status_names[i] == "<i class=\"fa fa-fw fa-globe\"></i>":
                    status_names[i] = "Online Now"
                if status_names[i] == "<i class=\"fa fa-fw fa-group\"></i>":
                    status_names[i] = "New Players Today"
            alerts = soup.find_all("span", {"style": ["color:#30d611", "color:orange"]})
            for x in alerts:
                if x is not None:
                    alert_list.append(x.string.strip(" \\n"))
                    try:
                        alert_names.append(x.parent.previous_sibling.previous_sibling.contents[0])
                    except:
                        #When farming is done
                        alert_names.append(x.parent.parent.previous_sibling.previous_sibling.contents[0])
            # print(status_list)
            # print(status_names)
            # print(alert_list)
            # print(alert_names)
            embed = discord.Embed(
            title = 'Your FarmRPG Status!',
            color = discord.Color.blue()
            )
            #Alerts
            embed.add_field(
                    name = "Current Alerts",
                    value = " ",
                    inline = False
            )
            for i in range(len(alert_list)):
                embed.add_field(
                    name = alert_names[i],
                    value = alert_list[i]
                )
            #Statuses
            embed.add_field(
                    name = "All Statuses",
                    value = " ",
                    inline = False
            )
            for i in range(len(status_list)):
                embed.add_field(
                    name = status_names[i],
                    value = status_list[i]
                )
            await message.reply(embed = embed)
            select = Select( 
            placeholder = "Choose a command to learn more:",
                options = [
                    discord.SelectOption(label = "Farm", emoji = "🎙"),
                    discord.SelectOption(label = "Harvest", emoji = "🎙"), #Considered Automation / Botting, Not Allowed
                    discord.SelectOption(label = "Plant", emoji = "🎙"), #Considered Automation / Botting, Not Allowed
                    discord.SelectOption(label = "Kitchen", emoji = "👨‍💼"),
                    discord.SelectOption(label = "Fishing", emoji = "💩"),
                    discord.SelectOption(label = "Help Requests", emoji = "💩"),
                    discord.SelectOption(label = "Friendships", emoji = "💩"),
                    discord.SelectOption(label = "Chores", emoji = "💩"),
                    discord.SelectOption(label = "Skills", emoji = "💩"),
                    discord.SelectOption(label = "Currencies", emoji = "💩"),
                    discord.SelectOption(label = "Net Worth", emoji = "💩")
                    # discord.SelectOption(label = "Inventory", emoji = "🔍"),
                    # discord.SelectOption(label = "Town Things", emoji = "🕵️‍♀️"),
                    # discord.SelectOption(label = "Tower", emoji = "💩"),
                    # discord.SelectOption(label = "Masteries", emoji = "💩"),

                ]
            )
            view = discord.ui.View(timeout=None)
            view.add_item(select)
            await message.channel.send("Select something to learn more about if you\'d like!" , view=view)
            def get_progress_bar(percent):
                #assume full embed line of 20 emojis
                yellow = 0
                newnum = int(round(round(float(percent), 0) / 10, 0))
                if float(percent) % 10 >= 4.51:
                    yellow += 1
                    newnum -= 1
                out = "🟩"*newnum
                out += "🟨"*yellow
                out += "⬜"*(10-(newnum + yellow))
                return out
            async def my_callback(interaction):
                embed = discord.Embed(
                title = f'{select.values[0]}:',
                description = 'Let\'s take a look!',
                color = discord.Color.blue()
                )
                comm = select.values[0]
                if comm == "Farm":
                    await interaction.response.defer()
                    await message.channel.typing()
                    params = {
                        'id': '192351',
                    }
                    response = requests.get('https://farmrpg.com/xfarm.php', params=params, cookies=cookies, headers=headers)
                    newsoup = BeautifulSoup(response.text, "html.parser")
                    area = newsoup.find("span", {"id": "pbzone"}).next_sibling.next_sibling.next_sibling.next_sibling
                    growing = area.find_all("div", {"class": "chip concrop"})
                    crops = {}
                    for crop in growing:
                        name = crop.find("div", {"class", "chip-label"}).get_text().strip("\n")
                        width = crop.find("span", {"class" : "c-progress-bar-fill pbxx"})
                        crops[name] = {"time" : crop.get("data-seconds"), "percentage" : width['style'][6:-2]}
                    ready = area.find_all("div", {"class": "chip harvestallbtn"})
                    done = []
                    for crop in ready:
                        done.append(crop.find("div", {"class", "chip-label"}).get_text().strip("\n"))
                    embed.add_field(
                        name = "Crops Growing:",
                        value = ""
                    )
                    if len(growing) == 0:
                        embed.add_field(
                            name = "No crops currently Growing.",
                            value = " ",
                            inline = False
                        )
                    else:
                        for crop in crops:
                            embed.add_field(
                                name = crop,
                                value = f'{crops[crop]["time"]} Seconds left. {crops[crop]["percentage"]}% done\n{get_progress_bar(crops[crop]["percentage"])}',
                                inline = False
                            )
                    embed.add_field(
                        name = "Crops Finished:",
                        value = "",
                        inline = False
                    )
                    if len(done) == 0:
                        embed.add_field(
                            name = "No crops currently Finished.",
                            value = " "
                        )
                    else:
                        for crop in done:
                            embed.add_field(
                                name = crop,
                                value = f'Done',
                                inline = False
                            )
                if comm == "Harvest":
                    await interaction.response.defer()
                    while True:
                        headers.update({
                            'origin': 'https://farmrpg.com'
                        })
                        params = {
                            'go': 'harvestall',
                            'id': '192351',
                        }
                        response = requests.post('https://farmrpg.com/worker.php', params=params, cookies=cookies, headers=headers)
                        print("attempted harvest")
                        await asyncio.sleep(5)
                        headers.update({
                            'origin': 'https://farmrpg.com'
                        })
                        params = {
                            'go': 'plantall',
                            'id': '192351',
                        }
                        response = requests.post('https://farmrpg.com/worker.php', params=params, cookies=cookies, headers=headers)
                        print("attempted plant")
                        await asyncio.sleep(60*87 + random.randrange(5, 20))
                if comm == "Plant":
                    headers.update({
                        'origin': 'https://farmrpg.com'
                    })
                    params = {
                        'go': 'plantall',
                        'id': '192351',
                    }
                    response = requests.post('https://farmrpg.com/worker.php', params=params, cookies=cookies, headers=headers)
                    print("attempted harvest")
                if comm == "Kitchen":
                    return
                if comm == "Fishing":
                    return
                if comm == "Help Requests":
                    return
                if comm == "Friendships":
                    return
                if comm == "Chores":
                    return
                if comm == "Skills":
                    response = requests.get('https://farmrpg.com/index.php', cookies=cookies, headers=headers)      
                    soup = BeautifulSoup(response.text, "html.parser")
                    skills = soup.find("div", {"class" : "row"})
                    skdict = {}
                    for skill in skills.children:
                        if skill.get_text().strip(" \n") != "":
                            prog = (skill.find("div")).get("data-progress")
                            lab = skill.get_text().split()
                            skdict[lab[0][:-2]] = {"level" : lab[1], "percent" : prog}
                    for sk in skdict:
                        if skdict[sk]["level"] == "99":
                            pbar = "🟥🟧🟨🟩🟦🟪🟥🟧🟨🟩"
                        else:
                            pbar = get_progress_bar(skdict[sk]["percent"])
                        embed.add_field(
                            name = sk,
                            value = f'Level {skdict[sk]["level"]}, {skdict[sk]["percent"]}% to next level.\n{pbar}',
                            inline = False
                        )
                if comm == "Currencies":
                    response = requests.get('https://farmrpg.com/index.php', cookies=cookies, headers=headers)      
                    soup = BeautifulSoup(response.text, "html.parser")
                    silver = soup.find("img", {"src" : "/img/items/silver_sm.png?1"})
                if comm == "Net Worth":
                    await interaction.response.defer()
                    await message.channel.typing()
                    #Item Value
                    response = requests.get('https://farmrpg.com/inventory.php', cookies=cookies, headers=headers)      
                    soup = BeautifulSoup(response.text, "html.parser")
                    with open(f'{cwd}data\\farmprices.json', 'r') as f:
                        farmprices = json.load(f)
                    bigcont = soup.find_all("div", {"class", "list-group"})
                    totalnet = 0
                    for cat in bigcont:
                        items = cat.find_all("a")
                        for item in items:
                            id = item.get("href")[12:]
                            name = item.find("div", {"class", "item-title"}).get_text().split("\n")[0]
                            amt = item.find("div", {"class", "item-after"}).get_text()
                            # print(id)
                            # print(name)
                            # print(amt)
                            #Check if id is in data\\farmprices.json. If it is, do math. Else, visit page, add to json, do math.
                            if str(id) in farmprices:
                                totalnet += (int(farmprices[str(id)]["val"]) * int(amt))
                            else:
                                params = {
                                    'id': id,
                                }
                                response = requests.get('https://farmrpg.com/item.php', params=params, cookies=cookies, headers=headers)
                                soup = BeautifulSoup(response.text, "html.parser")
                                sell = soup.find("a", {"href" : "market.php"})
                                if sell is None:
                                    # print(f'Name: {name}')
                                    sell = soup.find("a", {"href" : "steakmarket.php"})
                                    if sell is not None:
                                        print(sell.parent.parent.find("div", {"class" : "item-after"}).get_text().split(" ")[0].strip("\n").replace(',',''))
                                        value = int(sell.parent.parent.find("div", {"class" : "item-after"}).get_text().split(" ")[0].strip("\n").replace(',',''))
                                        print(f'Current {name} price is {value}')
                                        totalnet += int(value) * int(amt)
                                elif sell is not None:
                                    print(name)
                                    value = int(sell.parent.parent.find("div", {"class" : "item-after"}).get_text().split(" ")[0].strip("\n").replace(',',''))
                                    print(name, value)
                                    farmprices[str(id)] = {'val' : value, 'name' : name}
                                    totalnet += int(value) * int(amt)
                                else:
                                    farmprices[str(id)] = {'val' : 0, 'name' : name}
                    embed.add_field(
                        name = "Item value",
                        value = f"{totalnet:,} Silver",
                        inline = False
                    )
                    with open(f'{cwd}data\\farmprices.json', 'w') as f:
                        json.dump(farmprices, f)
                    #Bank Value
                    response = requests.get('https://farmrpg.com/bank.php', cookies=cookies, headers=headers)
                    soup = BeautifulSoup(response.text, "html.parser")
                    opts = soup.find("div", string="Bulk Options")
                    opts = opts.next_element.next_element.next_element.find_all("div", {"class" : "item-after"})
                    wallet = int(opts[0].get_text().split(" ")[0].replace(',',''))
                    bank = int(opts[1].get_text().split(" ")[0].replace(',',''))
                    totalnet += bank + wallet
                    embed.add_field(
                        name = "Money in Wallet",
                        value = f"{wallet:,} Silver",
                        inline = False
                    )
                    embed.add_field(
                        name = "Money in Bank",
                        value = f"{bank:,} Silver",
                        inline = False
                    )
                    #Wine Cellar Value
                    params = {
                        'id': '192351',
                    }
                    response = requests.get('https://farmrpg.com/cellar.php', params=params, cookies=cookies, headers=headers)
                    soup = BeautifulSoup(response.text, "html.parser")
                    wine = soup.find("div", string="Wine Cellar Stats")
                    wine = int(wine.next_sibling.next_sibling.find("strong").get_text().replace(',',''))
                    totalnet += wine
                    embed.add_field(
                        name = "Wine Cellar Value",
                        value = f"{wine:,} Silver",
                        inline = False
                    )
                    #Storehouse Items Value
                    params = {
                        'id': '192351'
                    }
                    stritems = 0
                    response = requests.get('https://farmrpg.com/storehouse.php', params=params, cookies=cookies, headers=headers)
                    soup = BeautifulSoup(response.text, "html.parser")
                    items = soup.find("div", string=lambda x: x is not None and "Items Stored" in x).next_sibling.next_sibling
                    items = items.find_all("a")
                    with open(f'{cwd}data\\farmprices.json', 'r') as f:
                        farmprices = json.load(f)
                    for item in items:
                        id = item.get("href")[12:]
                        name = item.find("div", {"class", "item-title"}).get_text().split("\n")[0]
                        amt = item.find("div", {"class", "item-after"}).get_text()
                        if str(id) in farmprices:
                            # print(f'{name} is {int(farmprices[str(id)]["val"])} Silver * {amt}')
                            totalnet += (int(farmprices[str(id)]["val"]) * int(amt))
                            stritems += (int(farmprices[str(id)]["val"]) * int(amt))
                        else:
                            params = {
                                'id': id,
                            }
                            response = requests.get('https://farmrpg.com/item.php', params=params, cookies=cookies, headers=headers)
                            soup = BeautifulSoup(response.text, "html.parser")
                            sell = soup.find("a", {"href" : "market.php"})
                            if sell is None:
                                # print(f'Name: {name}')
                                sell = soup.find("a", {"href" : "steakmarket.php"})
                                if sell is not None:
                                    value = int(sell.parent.parent.find("div", {"class" : "item-after"}).get_text().split(" ")[0].strip("\n").replace(',',''))
                                    print(f'Current {name} price is {value}')
                                    totalnet += int(value) * int(amt)
                                    stritems += int(value) * int(amt)
                            elif sell is not None:
                                print(name)
                                value = int(sell.parent.parent.find("div", {"class" : "item-after"}).get_text().split(" ")[0].strip("\n").replace(',',''))
                                print(name, value)
                                farmprices[str(id)] = {'val' : value, 'name' : name}
                                totalnet += int(value) * int(amt)
                                stritems += int(value) * int(amt)
                            else:
                                farmprices[str(id)] = {'val' : 0, 'name' : name}
                    embed.add_field(
                        name = "Storehouse Items Value",
                        value = f"{stritems:,} Silver",
                        inline = False
                    )
                    with open(f'{cwd}data\\farmprices.json', 'w') as f:
                        json.dump(farmprices, f)
                    #Storehouse Upgrades Value
                    
                    #Farm Upgrades Value
                    #Kitchen Value
                    #Pet Value
                    #Total Value
                    embed.add_field(
                        name = "Total Net Worth",
                        value = f"{totalnet:,} Silver",
                        inline = False
                    )
                

                await interaction.followup.send(f'You chose {select.values[0]}.', ephemeral = True, embed = embed)
                # await interaction.response.send_message(f'You chose {select.values[0]}.', ephemeral = True, embed = embed)
            select.callback = my_callback

#############$$$$$$$$$$$$$$$!!!!!!!!!!!!!!!!!!!!!!!!!$$$$$$$$$$$$$$$#################
#############$$$$$$$$$$$$$$$!!!!!!!!!!!!!!!!!!!!!!!!!$$$$$$$$$$$$$$$#################
#############$$$$$$$$$$$$$$$!!!!!!!!!!!!!!!!!!!!!!!!!$$$$$$$$$$$$$$$#################

    with open(f'{cwd}data\\users.json', 'w') as f:
            json.dump(users, f)

with open(f'{cwd}data\\users.json', 'r') as f:
        users = json.load(f)
f.close()

async def update_data(users, user):
    if isinstance(user, str):
      id = user
      name = 'unkknown'
    else:
      id = user.id
      name = user.name
    if not str(id) in users:
        users[str(id)] = {}
        users[str(id)]['name'] = name
        users[str(id)]['exp'] = 0
        users[str(id)]['words'] = {}
        users[str(id)]['totalWords'] = 0
        users[str(id)]['botCoin'] = 0
        users[str(id)]['activities'] = {}
    else:
        if not 'exp' in users[str(id)]:
            users[str(id)]['exp'] = 0
        if not 'words' in users[str(id)]:
            users[str(id)]['words'] = {}
        if not 'totalWords' in users[str(id)]:
            users[str(id)]['totalWords'] = 0
        if not 'botCoin' in users[str(id)]:
            users[str(id)]['botCoin'] = 0
        if not 'activities' in users[str(id)]:
            users[str(id)]['activities'] = {}
        if not 'name' in users[str(id)]:
            users[str(id)]['name'] = user.name
        if not 'lastAct' in users[str(id)]:
            users[str(id)]['lastAct'] = 0
        if not 'tracks' in users[str(id)]['activities']:
            users[str(id)]['activities']['tracks'] = {}

#####################################################################################

async def add_experience(users, user, exp):
    if isinstance(user, str):
      id = user
    else:
      id = user.id
    users[str(id)]['exp'] += int(exp)

#####################################################################################

def get_exp(users, user):
    if isinstance(user, str):
      print('yep')
      id = user
    else:
      id = user.id
    return str(users[str(id)]['exp'])

#####################################################################################

def get_commands(users, user):
    if isinstance(user, str):
      id = user
      name = f"<@{user}>"
    else:
      id = user.id
      name = user.name
    if not 'commands' in users[str(id)]:
        users[str(id)]['commands'] = {}
    res = nlargest(20,
        users[str(id)]['commands'],
        key=users[str(id)]['commands'].get)
    if len(res) == 0:
        return ('There\'s no record of that yet!')
    occurences = []
    output = f"{name}\'s Most used commands are:\n"
    for word in res:
            occurences.append(users[str(id)]['commands'][word])
    for x in range(len(res)):
        output += ('#' + str(x + 1) + ': ' + res[x] + f' with {occurences[x]} uses\n')
    return output

#####################################################################################

def getAchPercent(users, achievement):
    numppl = len(users)
    total = 0
    for ppl in users:
        if "achievements" in users[str(ppl)]:
            if(achievement in users[str(ppl)]["achievements"]):
                total += 1
    out = (f'{round((total / numppl) * 100, 2)}%')
    return out

#####################################################################################

async def update_words(users, user, content):
    res = content.split()
    for word in res:
        if word in commandList:
            if not "commands" in users[str(user.id)]:
                users[str(user.id)]['commands'] = {}
            if not word in users[str(user.id)]['commands']:
                users[str(user.id)]['commands'][word] = 1
            else:
                users[str(user.id)]['commands'][word] += 1
        word = word.lower()
        if word in wordsToIgnore or word.isnumeric() or word.startswith('https'):
            users[str(user.id)]['totalWords'] += 1
            continue
        elif not word in users[str(user.id)]['words']:
            users[str(user.id)]['words'][word] = 1
        else:
            users[str(user.id)]['words'][word] += 1
        users[str(user.id)]['totalWords'] += 1
    with open(f'{cwd}data\\wotd.json', 'r') as f:
            wotd = json.load(f)
    if not str(user.id) in wotd['players']:
        wotd['players'][str(user.id)] = {"correct" : 0, "incorrect" : 0, "today" : 0}
    if not "achievements" in users[str(user.id)]:
        users[str(user.id)]["achievements"] = []
    with open(f'{cwd}data\\wotd.json', 'w') as f:
                json.dump(wotd, f)

#####################################################################################

async def activity_leaderboard(users, user, channel, type):
    if isinstance(user, str):
      id = user
      name = f"<@{user}>"
    else:
      id = user.id
      name = user.name
    if not type in users[str(id)]['activities']:
        users[str(id)]['activities'][type] = {}
    if not type == 'tracks':
        res = nlargest(5,
            users[str(id)]['activities'][type],
            key=users[str(id)]['activities'][type].get)
    else:
        tracklist = {}
        for track in users[str(id)]['activities']['tracks']:
            tracklist[track] = users[str(id)]['activities']['tracks'][track]['time']
        res = nlargest(5,
                tracklist,
                key=tracklist.get)
    occurences = []
    if type == 'artists':
        output = '**' + str(name) + '**\'s most listened to artists are: \n'
    if type == 'playing':
        output = '**' + str(name) + '**\'s most played games are: \n'
    if type == 'watching':
        output = '**' + str(name) + '**\'s most watched things are: \n'
    if type == 'streaming':
        output = '**' + str(name) + '**\'s most streamed things are: \n'
    if type == 'streamgames':
        output = '**' + str(name) + '**\'s most streamed things are: \n'
    if type == 'custom':
        output = '**' + str(name) + '**\'s most custom activities have been: \n'
    if type == 'competing':
        output = '**' + str(name) + '**\'s most competeted activites have been: \n'
    if type == 'tracks':
        output = '**' + str(name) + '**\'s most listened to tracks have been: \n'
    if len(res) == 0:
        return ('There\'s no record of that yet!')
    for word in res:
        if not type == 'tracks':
            occurences.append(users[str(id)]['activities'][type][word])
        else:
            occurences.append(users[str(id)]['activities']['tracks'][word]['time'])
    for x in range(len(res)):
        time = [occurences[x], 'seconds']
        if time[0] > 120:
            time[0] /= 60
            time[1] = 'minutes'
        if time[0] > 120:
            time[0] /= 60
            time[1] = 'hours'
        output += ('#' + str(x + 1) + ': ' + str(res[x]) + ' with ' +
                   str(round(time[0], 2)) + ' ' + str(time[1]) + '\n')
    return output
    await channel.send(output)

#####################################################################################

async def get_albums(users, user, guild): #user = id number
    user = await guild.fetch_member(user)
    canvas = Image.new(mode = "RGB", size = (1920, 1920))
    id = user.id
    name = user.display_name
    if not 'albums' in users[str(id)]['activities']:
        users[str(id)]['activities']['albums'] = {}
    timedict = {}
    for album in users[str(id)]['activities']['albums']:
        timedict[album] = users[str(id)]['activities']['albums'][album]['time']
    res = nlargest(8,
                users[str(id)]['activities']['albums'],
                key=timedict.get)
    occurences = []
    links = []
    for album in res:
        occurences.append(timedict[album])
        links.append(users[str(id)]['activities']['albums'][album]['albumcover'])
    if len(res) == 0:
        return ('You haven\'t done any of that yet!')
    for word in res:
        occurences.append(users[str(id)]['activities']['albums'][word])
    output = ""
    for x in range(len(res)):
        time = [occurences[x], 'seconds']
        if time[0] > 120:
            time[0] /= 60
            time[1] = 'minutes'
        if time[0] > 120:
            time[0] /= 60
            time[1] = 'hours'
        output += ('#' + str(x + 1) + ': ' + str(res[x]) + ' with ' +
                str(round(time[0], 2)) + ' ' + str(time[1]) + '\n')
    # await channel.send(output)
    # print(links)
    j = -1
    for i in range(8):
        j += 1
        if j >= len(links):
            j = 0
        response = requests.get(links[j])
        img = Image.open(BytesIO(response.content))
        coords = {0 : [0,0], 1 : [640, 0], 2 : [1280,0], 3 : [0,640], 4 : [1280,640], 5 : [0,1280], 6 : [640,1280], 7 : [1280,1280],}
        canvas.paste(img, (coords[i][0], coords[i][1]))
    response = requests.get(user.display_avatar.url)
    img = Image.open(BytesIO(response.content))
    img = img.resize((300, 300))
    mask_im = Image.new("L", (300,300), 0)
    draw = ImageDraw.Draw(mask_im)
    draw.ellipse((0,0) + (300, 300), fill=255)
    canvas.paste(img, (810, 720), mask_im)
    text = ImageDraw.Draw(canvas)
    try:
        color = (user.roles[-1].color.r, user.roles[-1].color.g, user.roles[-1].color.b)
    except:
        color = (255,255,255)
    font = ImageFont.truetype(f'{cwd}fonts\\vanilla Caramel.otf',120)
    text.text((860, 1020), "Your", fill = color, font = font)
    text.text((800, 1110), "Albums!", fill = color, font = font)
    text.text((900, 1240), "Made by BotBot", fill = (255,255,255), font = ImageFont.truetype(f'{cwd}fonts\\vanilla Caramel.otf',20))
    embed = discord.Embed(
        title = 'Your Favorite Albums!',
        description = 'The stats:',
        color = discord.Color.blue()
        )
    with BytesIO() as image_binary:
        canvas.save(image_binary, 'PNG')
        image_binary.seek(0)
        file = discord.File(fp=image_binary, filename='image.png')
        embed.set_image(url="attachment://image.png")
    # canvas.show()
    embed.add_field(name = "What\'s your top 8 Albums?:", value = output, inline = False)
    try:
        embed.set_thumbnail(url = user.avatar.url)
    except:
        print('aw')
    return [file,embed]

#####################################################################################

async def user_word_leaderboard(users, user, channel):
    if isinstance(user, str) or isinstance(user, int):
      id = user
      name = f"<@{user}>"
    else:
      id = user.id
      name = user.name
    res = nlargest(5,
                   users[str(id)]['words'],
                   key=users[str(id)]['words'].get)
    occurences = []
    if len(res) == 0:
        return "No words on file!"
    output = '**' + str(
        name
    ) + '**\'s most used words (minus prepositions and such) are: \n'
    for word in res:
        occurences.append(users[str(id)]['words'][word])
    for x in range(5):
        output += ('#' + str(x + 1) + ': ' + str(res[x]) + ' with ' +
                   str(occurences[x]) + ' occurences\n')
    return output
    await channel.send(output)

#####################################################################################

async def funny_word_check(users, user, channel, content):
    if content.startswith('https') or content.startswith('<:'):
        return
    for word in commandList:
        if content.startswith(word):
            return
    for word in adminCommands:
        if content.startswith(word):
            return
    rand = random.randrange(0, 40)
    output = ''
    random.shuffle(funny)
    for word in funny:
        wordIndex = 0
        indexes = []
        for x in range(len(content)):
            if wordIndex == len(word):
                break
            if content[x] == word[wordIndex]:
                indexes.append(x)
                wordIndex += 1
        if wordIndex == len(word):
            for y in range(len(content)):
                if y in indexes:
                    output += ' **' + str(content[y]).upper() + '** '
                else:
                    output += str(content[y])
            if rand <= 2 and indexes[-1] - indexes[0] != len(word) - 1:
                await channel.send(output)
                await change_money(users, user, 30)
                await add_experience(users, user, 50)
            print('potential: ' + word + ', rolled a ' + str(rand))
            break


#####################################################################################


async def change_money(users, user, change):
    if isinstance(user, str):
      id = int(user)
    else:
      id = user.id
    new = users[str(id)]['botCoin'] + int(change)
    print(users[str(id)]['botCoin'] + int(change))
    users[str(id)]['botCoin'] = new
    with open(f'{cwd}data\\users.json', 'w') as f:
        json.dump(users, f)


#####################################################################################


def get_bal(users, user):
    if isinstance(user, str):
      id = user
    else:
      id = user.id
    return users[str(id)]['botCoin']


#####################################################################################

def get_image(prompt):
    url = f"https://www.bing.com/images/search?q={prompt}&first=1"  # the URL of the search result page
    response = requests.get(url)  # make a GET request to the URL
    # print(response.text)
    soup = BeautifulSoup(response.text, "html.parser")  # parse the HTML content with BeautifulSoup
    img_tag = soup.find("img", {"class": "mimg"})
    if img_tag is not None:
        img_link = img_tag.get("src")
        return(img_link)  # print the first image link -> check bing classes when failed
    else:
        img_tag = soup.find("img", {"class": "cimg mimg"})
        if img_tag is not None:
            img_link = img_tag.get("src")
            return(img_link)  # print the first image link
        else:
            img_tag = soup.find("img", {"class": "mimg rms_img"})
            if img_tag is not None:
                img_link = img_tag.get("src")
                return(img_link)  # print the first image link
        return(None)

#####################################################################################

async def check_wotd(message, wotd):
    words = message.content.split()
    if len(words) <= 3:
        return False
    for word in words:
        if word == wotd:
            return await message.add_reaction("👀")
    return False

#####################################################################################

async def get_slothed_lmao(msg):
    rand = random.randrange(0, 200)
    if rand <= 1:
        with open(f'{cwd}media\\slomth.jpg', 'rb') as s:
            sloth = discord.File(s)
        await msg.channel.send("**YOUVE BEEN SLOTHED**", file = sloth)
        return True
    else:
        return False

#####################################################################################


async def check_bal(users, user, channel):
    if isinstance(user, str):
      id = user
    else:
      id = user.id
    await channel.send(f'<@{id}>\'s balance is: ' +
                       str(users[str(id)]['botCoin']) + ' BotCoins!')
    with open(f'{cwd}data\\users.json', 'w') as f:
            json.dump(users, f)


#####################################################################################

async def generateAchievement(name, user, guild):
    #get pfps
    pfp = await guild.fetch_member(int(user))
    response = requests.get(pfp.display_avatar.url)
    img = Image.open(BytesIO(response.content))
    img = Image.open(BytesIO(response.content))
    img = img.resize((220,220), Image.NEAREST)
    bbpfp = await guild.fetch_member(int(1038551765081137152))
    bbresponse = requests.get(bbpfp.display_avatar.url)
    bbimg = Image.open(BytesIO(bbresponse.content))
    bbimg = Image.open(BytesIO(bbresponse.content))
    bbimg = bbimg.resize((220,220), Image.NEAREST)
    #get description
    desc = ""
    if name in achievementlist:
        desc = achievementlist[name]
    else:
        return None
    #create base image
    canvas = Image.new(mode = "RGBA", size = (1200, 630))
    #attach user pfp
    canvas.paste(img, (808, 15))
    #attach botbot pfp
    canvas.paste(bbimg, (163, 15))
    #paste over base
    base = Image.open(f'{cwd}media\\achievement.png')
    base.convert("RGBA")
    canvas.convert("RGBA")
    canvas.paste(base, (0,0), base)
    draw = ImageDraw.Draw(canvas)
    #attach usernames
    fontsize = 30
    font = ImageFont.truetype(f'{cwd}fonts\\ss800Black.otf', fontsize)
    username = pfp.display_name
    bbusername = bbpfp.display_name
    userlen = font.getlength(username)
    bblen = font.getlength(bbusername)
    while(userlen > 250):
        font = ImageFont.truetype(f'{cwd}fonts\\ss800Black.otf', fontsize-1)
        fontsize -= 1
        userlen = font.getlength(username)
    font = ImageFont.truetype(f'{cwd}fonts\\ss800Black.otf', fontsize)
    draw.text((795 + (250 - userlen) / 2, 212 + (30 - fontsize)/2), username, font = font, fill = "white", align = "center", stroke_fill = "black", stroke_width = 4)
    fontsize = 30
    while(bblen > 230):
        font = ImageFont.truetype(f'{cwd}fonts\\ss800Black.otf', fontsize-1)
        fontsize -= 1
        bblen = font.getlength(bbusername)
    font = ImageFont.truetype(f'{cwd}fonts\\ss800Black.otf', fontsize)
    draw.text((153 + (250 - bblen) / 2, 212 + (30 - fontsize)/2), bbusername, font = font, fill = "white", align = "center", stroke_fill = "black", stroke_width = 4)
    #attach achievement name and description
    fontsize = 38
    font = ImageFont.truetype(f'{cwd}fonts\\ss800Black.otf', fontsize)
    namelen = font.getlength(name)
    desclen = font.getlength(desc)
    while(namelen > 1150):
        font = ImageFont.truetype(f'{cwd}fonts\\ss800Black.otf', fontsize-1)
        fontsize -= 1
        namelen = font.getlength(desc)
    draw.text((56 + (1088 - namelen) / 2, 326), name, font = font, fill = "white", align = "center", stroke_fill = "black", stroke_width = 4)
    fontsize = 38
    while(desclen > 1150):
        font = ImageFont.truetype(f'{cwd}fonts\\ss800Black.otf', fontsize-1)
        fontsize -= 1
        desclen = font.getlength(desc)
    draw.text((56 + (1088 - desclen) / 2, 505), desc, font = font, fill = "white", align = "center", stroke_fill = "black", stroke_width = 4)
    #save and return image
    with BytesIO() as image_binary:
        canvas.save(image_binary, 'PNG')
        image_binary.seek(0)
        file = discord.File(fp=image_binary, filename='image.png')
    
    return file#picture

#####################################################################################

async def update_activities(users, user, activity, time):
    # print(f'adding {time} to {user}, activity is {activity}')
    type = str(activity.type)[13:]
    if not type in users[str(user)]['activities']:
        users[str(user)]['activities'][type] = {}
    if not activity.name in users[str(user)]['activities'][type]:
        users[str(user)]['activities'][type][activity.name] = time
    else:
        users[str(user)]['activities'][type][activity.name] += time
    if type == "streaming":
        if not 'streamgames' in users[str(user)]['activities']:
            users[str(user)]['activities']['streamgames'] = {}
        if not activity.game in users[str(user)]['activities']["streamgames"]:
            users[str(user)]['activities']["streamgames"][activity.game] = 0
        else:
            users[str(user)]['activities']["streamgames"][activity.game] += time
    if type == 'listening':
        if not 'artists' in users[str(user)]['activities']:
            users[str(user)]['activities']['artists'] = {}
        if not 'tracks' in users[str(user)]['activities']:
            users[str(user)]['activities']['tracks'] = {}
        if not 'albums' in users[str(user)]['activities']:
            users[str(user)]['activities']['albums'] = {}
        if not activity.title in users[str(user)]['activities']['tracks']:
            users[str(user)]['activities']['tracks'][activity.title] = {"time" : time, "artist" : activity.artist, "albumcover" : activity.album_cover_url}
        else:
            users[str(user)]['activities']['tracks'][activity.title]["time"] += time
        if not activity.album in users[str(user)]['activities']['albums']:
            users[str(user)]['activities']['albums'][activity.album] = {"time" : time, "artist" : activity.artist, "albumcover" : activity.album_cover_url}
        else:
            users[str(user)]['activities']['albums'][activity.album]["time"] += time
        for artist in activity.artists:
          if not activity.artist in users[str(user)]['activities']['artists']:
              users[str(user)]['activities']['artists'][activity.artist] = time
          else:
              users[str(user)]['activities']['artists'][activity.artist] += time
        # print(f'artist is {activity.artist}')


#####################################################################################

with open(f'{cwd}data\\users.json', 'w') as f:
            json.dump(users, f)

# keep_alive()

client.run(TOKEN)
#Probably don't need both, leave for now
bot.run(TOKEN)
### IF DISCORD API BANNED, TYPE 'kill 1' IN SHELL -->

