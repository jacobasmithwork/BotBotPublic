#ACHIEVEMENTS FUNCTIONS FILE
#TODO: check video-editing-notes channel in loftzo server

import discord
from discord.ext import commands
from discord.utils import get
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from io import BytesIO
import requests
import asyncio

uuAchievements = {
    "Knowledgeable" : "knowledgeable",
    "Linguist" : "linguist",
    "Thesaurus" : "thesaurus",
    "Conversational" : "conversational",
    "Talkative" : "talkative",
    "Chatterbox" : "chatterbox",
    "Greeter" : "greeter",
    "Nosy" : "nosy",
    "CIA" : "cia",
    "Shitposter" : "shitposter",
    "Share the Wealth" : "share",
    "Face Snatcher" : "snatcher",
    "Idea Generator" : "idea",
    "Wrapper" : "wrapper",
    "Contributor" : "contributor",
    "Animal Lover" : "animallover",
    "Zoologist" : "zoologist",
    "Listener" : "listener",
    "Sound Enjoyer" : "soundenjoyer",
    "Music Freak" : "freak",
    "Take Off Your Headphones" : "headphones",
    "Gamer" : "gamer",
    "It's Just a Hobby" : "hobby",
    "Take a break" : "takeabreak",
    "You May Need Help" : "needhelp",
    "Touch Grass" : "touchgrass",
    "In a Simulation" : "simulation",
    "Pocket Change" : "pocket",
    "The 1%" : "one",
    "The 0.1%" : "pointone",
    #"How'd that get in there?" : "Get Slothed.",
    # "Insightful" : "insightful",
}

guAchievements = {
    "Gambling Man" : "gambling",
    "Losing Streak" : "losing",
    "I Don't Have a Problem" : "problem",
    "Rehab" : "rehab",
}

huAchievements = {
    "Escapee" : "escapee",
    "Serial Gallows Avoider" : "gallows",
    "Stay Down" : "staydown",
}

wuAchievements = {
    "So Close" : "soclose",
    "Lucky Guess" : "lucky",
    "Smart Cookie" : "cookie",
}
#Check Achievements and Send awarded acheivements to channel - Consider Throttling ##MAKE IT ASYNC 
def checkAchievements(users, hm, guessnum, wotd, user):
    user = str(user)
    if not "achievements" in users[user]:
        users[user]["achievements"] = []
    if not "commands" in users[user]:
        users[user]["commands"] = {}
    for uuach in uuAchievements:
        func = globals()[uuAchievements[uuach]]
        if(func(users, user) and uuach not in users[str(user)]["achievements"]):
            print(f'{user} unlocked achievement: {uuAchievements[uuach]}')
            users[str(user)]["achievements"].append(uuach)
            return uuach
    for guach in guAchievements:
        func = globals()[guAchievements[guach]]
        if(func(guessnum, user) and guach not in users[str(user)]["achievements"]):
            print(f'{user} unlocked achievement: {guAchievements[guach]}')
            users[str(user)]["achievements"].append(guach)
            return guach
    for huach in huAchievements:
        func = globals()[huAchievements[huach]]
        if(func(hm, user) and huach not in users[str(user)]["achievements"]):
            print(f'{user} unlocked achievement: {huAchievements[huach]}')
            users[str(user)]["achievements"].append(huach)
            return huach
    for wuach in wuAchievements:
        func = globals()[wuAchievements[wuach]]
        if(func(wotd, user) and wuach not in users[str(user)]["achievements"]):
            print(f'{user} unlocked achievement: {wuAchievements[wuach]}')
            users[str(user)]["achievements"].append(wuach)
            return wuach
    return ""

# have 100 unique words - knowledgeable
def knowledgeable(users, user):
    if(len(users[user]["words"]) >= 100):
        return True
    else:
        return False

# have 1000 unique words - linguist
def linguist(users, user):
    if(len(users[user]["words"]) >= 1000):
        return True
    else:
        return False

# have 5000 unique words - thesaurus
def thesaurus(users, user):
    if(len(users[user]["words"]) >= 5000):
        return True
    else:
        return False
    
# have 1000 total words - conversational
def conversational(users, user):
    if(users[user]["totalWords"] >= 1000):
        return True
    else:
        return False
    
# have 10000 total words - talkative
def talkative(users, user):
    if(users[user]["totalWords"] >= 10000):
        return True
    else:
        return False
    
# have 100000 total words - chatterbox
def chatterbox(users, user):
    if(users[user]["totalWords"] >= 100000):
        return True
    else:
        return False
    
# have used the BBhello command - greeter
def greeter(users, user):
    if( "BBhello" in users[user]["commands"]):
        return True
    else:
        return False
    
# have used the BBsnoop command - nosy
def nosy(users, user):
    if( "BBsnoop" in users[user]["commands"]):
        return True
    else:
        return False
    
# have used the BBsnoop command 50 times - CIA
def cia(users, user):
    if( "BBsnoop" in users[user]["commands"] and users[user]["commands"]["BBsnoop"] >= 50):
        return True
    else:
        return False
    
# have used the BBsuggest command - idea generator
def idea(users, user):
    if( "BBsuggest" in users[user]["commands"]):
        return True
    else:
        return False
    
# have used the BBshitpost command - shitposter
def shitposter(users, user):
    if( "BBshitpost" in users[user]["commands"]):
        return True
    else:
        return False
    
# have used the BBpay command - share the wealth
def share(users, user):
    if( "BBpay" in users[user]["commands"]):
        return True
    else:
        return False
    
# have used the BBfetchpfp command - face snatcher
def snatcher(users, user):
    if( "BBfetchpfp" in users[user]["commands"]):
        return True
    else:
        return False
    
# have used the BBwrapped command - wrapper
def wrapper(users, user):
    if( "BBwrapped" in users[user]["commands"]):
        return True
    else:
        return False
    
# have used the BBadda___ command - contributor
def contributor(users, user):
    sum = 0
    if("BBaddapet" in users[user]["commands"]):
        sum += users[user]["commands"]["BBaddapet"]
    if("BBaddaduck" in users[user]["commands"]):
        sum += users[user]["commands"]["BBaddaduck"]
    if("BBaddarat" in users[user]["commands"]):
        sum += users[user]["commands"]["BBaddarat"]
    if("BBaddafrog" in users[user]["commands"]):
        sum += users[user]["commands"]["BBaddafrog"]
    if("BBaddapanda" in users[user]["commands"]):
        sum += users[user]["commands"]["BBaddapanda"]
    if(sum) >= 1:
        return True
    else:
        return False
    
# have used the BBadda___ command 10 times - animal lover
def animallover(users, user):
    sum = 0
    if("BBaddapet" in users[user]["commands"]):
        sum += users[user]["commands"]["BBaddapet"]
    if("BBaddaduck" in users[user]["commands"]):
        sum += users[user]["commands"]["BBaddaduck"]
    if("BBaddarat" in users[user]["commands"]):
        sum += users[user]["commands"]["BBaddarat"]
    if("BBaddafrog" in users[user]["commands"]):
        sum += users[user]["commands"]["BBaddafrog"]
    if("BBaddapanda" in users[user]["commands"]):
        sum += users[user]["commands"]["BBaddapanda"]
    if(sum) >= 10:
        return True
    else:
        return False
    
# have used the BBadda___ command 50 times - zoologist
def zoologist(users, user):
    sum = 0
    if("BBaddapet" in users[user]["commands"]):
        sum += users[user]["commands"]["BBaddapet"]
    if("BBaddaduck" in users[user]["commands"]):
        sum += users[user]["commands"]["BBaddaduck"]
    if("BBaddarat" in users[user]["commands"]):
        sum += users[user]["commands"]["BBaddarat"]
    if("BBaddafrog" in users[user]["commands"]):
        sum += users[user]["commands"]["BBaddafrog"]
    if("BBaddapanda" in users[user]["commands"]):
        sum += users[user]["commands"]["BBaddapanda"]
    if(sum) >= 50:
        return True
    else:
        return False

#use magic 8 ball
def insightful(users, user):
    if("BB?" in users[user]["commands"]):
        return True
    else:
        return False
    
# have spotify linked - listener
def listener(users, user):
    if("listening" in users[user]["activities"]):
        return True
    else:
        return False
    
# listen to spotify for 10 hours - sound enjoyer
def soundenjoyer(users, user):
    if("listening" in users[user]["activities"] and users[user]["activities"]["listening"]["Spotify"] >= 36000):
        return True
    else:
        return False
    
# listen to spotify for 50 hours - music freak
def freak(users, user):
    if("listening" in users[user]["activities"] and users[user]["activities"]["listening"]["Spotify"] >= 180000):
        return True
    else:
        return False
    
# listen to spotify for 100 hours - take off your headphones
def headphones(users, user):
    if("listening" in users[user]["activities"] and users[user]["activities"]["listening"]["Spotify"] >= 360000):
        return True
    else:
        return False
    
# play a game - gamer
def gamer(users, user):
    if("playing" in users[user]["activities"]):
        sum = 0
        for game in users[user]["activities"]["playing"]:
            sum += users[user]["activities"]["playing"][game]
        if sum >= 1:
            return True
    return False
    
# play games for 5 hours - It's just a hobby
def hobby(users, user):
    if("playing" in users[user]["activities"]):
        sum = 0
        for game in users[user]["activities"]["playing"]:
            sum += users[user]["activities"]["playing"][game]
        if sum >= 18000:
            return True
    return False
    
# play games for 10 hours - take a break
def takeabreak(users, user):
    if("playing" in users[user]["activities"]):
        sum = 0
        for game in users[user]["activities"]["playing"]:
            sum += users[user]["activities"]["playing"][game]
        if sum >= 36000:
            return True
    return False
    
# play games for 50 hours - you may need help
def needhelp(users, user):
    if("playing" in users[user]["activities"]):
        sum = 0
        for game in users[user]["activities"]["playing"]:
            sum += users[user]["activities"]["playing"][game]
        if sum >= 36000:
            return True
    return False
    
# play games for 100 hours - touch grass
def touchgrass(users, user):
    if("playing" in users[user]["activities"]):
        sum = 0
        for game in users[user]["activities"]["playing"]:
            sum += users[user]["activities"]["playing"][game]
        if sum >= 360000:
            return True
    return False
    
# play games for 1000 hours - In a Simulation
def simulation(users, user):
    if("playing" in users[user]["activities"]):
        sum = 0
        for game in users[user]["activities"]["playing"]:
            sum += users[user]["activities"]["playing"][game]
        if sum >= 3600000:
            return True
    return False
    
#have 100 BotCoin at one time - pocket change
def pocket(users, user):
    if users[user]["botCoin"] >= 100:
        return True
    else:
        return False
    
#have 1000 BotCoin at one time - the 1%
def one(users, user):
    if users[user]["botCoin"] >= 1000:
        return True
    else:
        return False
    
#have 5000 BotCoin at one time - the 0.1%
def pointone(users, user):
    if users[user]["botCoin"] >= 5000:
        return True
    else:
        return False
    
def gamblestats(guessnum, user):
    gamesplayed = 0
    gameswon = 0
    gameslost = 0
    moneywagered = 0
    moneyearned = 0
    moneylost = 0
    for games in guessnum["active"]:
        if games["players"][0] == str(user):
            gamesplayed += 1
            moneywagered += games["wager"]
            if abs(int(games["p1guess"]) - games["answer"]) < abs(int(games["p2guess"]) - games["answer"]):
                moneyearned += games["wager"]
                gameswon += 1
            else:
                moneylost += games["wager"]
                gameslost += 1
        if games["players"][1] == str(user):
            gamesplayed += 1
            moneywagered += games["wager"]
            if abs(int(games["p1guess"]) - games["answer"]) > abs(int(games["p2guess"]) - games["answer"]):
                moneyearned += games["wager"]
                gameswon += 1
            else:
                moneylost += games["wager"]
                gameslost += 1
    return {"gamesplayed" : gamesplayed,
            "gameswon" : gameswon,
            "gameslost" : gameslost, 
            "moneywagered" : moneywagered, 
            "moneyearned" : moneyearned, 
            "moneylost" : moneylost
            }

#gamble and win once - gambling man
def gambling(guessnum, user):
    stats = gamblestats(guessnum, user)
    if stats["gameswon"] >= 1:
        return True
    return False

#gamble and lose five times - losing streak
def losing(guessnum, user):
    stats = gamblestats(guessnum, user)
    if stats["gameslost"] >= 5:
        return True
    return False

#gamble and wager 1000 BotCoin - I don't have a problem
def problem(guessnum, user):
    stats = gamblestats(guessnum, user)
    if stats["moneywagered"] >= 1000:
        return True
    return False

#gamble on 50 games - Rehab
def rehab(guessnum, user):
    stats = gamblestats(guessnum, user)
    if stats["gamesplayed"] >= 50:
        return True
    return False

#play and win a game of hangman - Escapee
def escapee(hm, user):
    if str(user) in hm:
        if hm[str(user)]["gameswon"] >= 1:
            return True
    return False

#play and win a game of hangman 20 times- Serial Gallows Avoider
def gallows(hm, user):
    if str(user) in hm:
        if hm[str(user)]["gameswon"] >= 20:
            return True
    return False

#play and lose a game of hangman 20 times- Stay Down
def staydown(hm, user):
    if str(user) in hm:
        if (hm[str(user)]["games"] - hm[str(user)]["gameswon"]) >= 20:
            return True
    return False

#guess the word of the day wrong - So close
def soclose(wotd, user):
    if str(user) in wotd["players"]:
        if(wotd["players"][str(user)]["incorrect"] >= 1):
            return True
    return False

#guess the word of the day right - Lucky Guess  
def lucky(wotd, user):
    if str(user) in wotd["players"]:
        if(wotd["players"][str(user)]["correct"] >= 1):
            return True
    return False

#guess the word of the day right 5 times - Smart Cookie
def cookie(wotd, user):
    if str(user) in wotd["players"]:
        if(wotd["players"][str(user)]["correct"] >= 5):
            return True
    return False

