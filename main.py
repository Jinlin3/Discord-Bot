import discord
import os
import requests
import random
from replit import db
from keep_alive import keep_alive

#Configuring intent settings and global variables

intent = discord.Intents.default()
intent.members = True
intent.message_content = True
client = discord.Client(intents = intent)

teamMode = 0
alreadySorted = 0

#All cue words and cue results

cues = [
  "christian", 
  "cruz", 
  "paul", 
  "salunga",
  "sorce", 
  "chris",
  "ohcool",
]

shootingCues = ["aim", "shoot", "fps", "csgo", "valorant", "val"]

cuesResult = [
  "This might be outta pocket but...",
  "Did someone call for me?",
  "Never fear! Christian is here!",
  "Yeooo!",
]

shootingResult = [
  "Did anyone mention shooting? I have top 1% aim btw!",
  "Not to be cocky, but I think my aim is the best on this server!",
  "Back when I played csgo, I was silver... but I def deserved Global Elite!",
  "If I played Valorant seriously, I would be Radiant fosho! No cap!"
]

#Below is for pick-up line API

pickUpLineCues = ["rizz", "love", "down bad"]

starters = [
  "Lemme rizz you up baby.",
  "Here's one from my personal arsenal.",
  "I'll seduce you with this one.",
  "Let me mystify you.",
  "I'll satisfy your desires."
]

rizz = [
  "I play the broken champs so I can win more!",
  "She's gotta be out there somewhere...",
  "I'm down bad rn :(",
  "Trung is a lazy bum!",
  "I wish I was a girl, cause then I'd be able to kiss the boys all the time.",
  "I need some dick rn :(",
  "I love coom <3!",
  "Osu!",
  "Top 1% in all stats btw!",
  "You know what would be nice rn? Some juicy cack ;)",
  "My penis --> 8=============D",
  "My name is Christian, but you can call me handsome ;)",
  "Riven, Irelia, Ekko, Yasuo, Kassadin... They're all balanced!",
  "The girls used to call me hot honey back in high school.",
  "I'm rich af btw, look at my stacks!"
]

#Retrieves a line from the API

def get_line():
  url = "https://pick-me-up.p.rapidapi.com/cheesy"
  headers = {
	"X-RapidAPI-Key": "36ef312bcemsh00e92d766bf9906p180189jsn5566eae4451b",
	"X-RapidAPI-Host": "pick-me-up.p.rapidapi.com"
}
  response = requests.request("GET", url, headers=headers)

  return (response.text)

#------------TEAM-BALANCING FUNCTIONS------------#

#Uploads a player and their ranking score to the lists

def upload_players(entry, score):
  if "players" in db.keys():
    players = db["players"]
    players.append(entry)
  else:
    db["players"] = [entry]

  if "scores" in db.keys():
    scores = db["scores"]
    scores.append(score)
  else:
    db["scores"] = [score]

#Clears players and scores list

def clear_all_players():
  db["players"].clear()
  db["scores"].clear()

#Turns team mode on

def team_on():
  global teamMode
  teamMode = 1

#Turns team mode off

def team_off():
  global teamMode
  teamMode = 0

#Converts rank to score

def convert_rank(list):
  score = 0
  tier = list[1].lower()
  division = list[2]
  
  if (tier.startswith("i")):
    score = 1
  elif (tier.startswith("b")):
    score = 2
  elif (tier.startswith("s")):
    score = 3
  elif (tier.startswith("gr")):
    return 8
  elif (tier.startswith("p")):
    score = 5
  elif (tier.startswith("d")):
    score = 6
  elif (tier.startswith("m")):
    return 7
  elif (tier.startswith("g")):
    score = 4
  elif (tier.startswith("c")):
    return 9
  else:
    return 0

  if (division == "4"):
    score += 0.2
  elif (division == "3"):
    score += 0.4
  elif (division == "2"):
    score += 0.6
  elif (division == "1"):
    score += 0.8
  else:
    score = 0

  return score

#Sorts players and scores list using Selection Sort 

def sort_lists(players, scores):
  print("---SORTING---")
  for i in range(len(scores)):
    max = i
    for j in range(i + 1, len(scores)):
      if scores[max] < scores[j]:
        max = j
    scores[i], scores[max] = scores[max], scores[i]
    players[i], players[max] = players[max], players[i]
  print(players)
  print(scores)

def sort_list(list):
  print("---SORTING---")
  for i in range(len(list)):
    max = i
    for j in range(i + 1, len(list)):
      if list[max] < list[j]:
        max = j
    list[i], list[max] = list[max], list[i]

#Creates team1/team2 team1score/team2score arrays

def balance_teams():
  print("---BALANCING---")
  if "team1" in db.keys():
    team1 = db["team1"]
    team1.clear()
  else:
    db["team1"] = []
    team1 = db["team1"]

  if "team1scores" in db.keys():
    team1scores = db["team1scores"]
    team1scores.clear()
  else:
    db["team1scores"] = []
    team1scores = db["team1scores"]

  if "team2" in db.keys():
    team2 = db["team2"]
    team2.clear()
  else:
    db["team2"] = []
    team2 = db["team2"]

  if "team2scores" in db.keys():
    team2scores = db["team2scores"]
    team2scores.clear()
  else:
    db["team2scores"] = []
    team2scores = db["team2scores"]

  players = db["players"]
  scores = db["scores"]

  print("length of players: " + str(len(players)))

  if len(players) % 2 == 0: #Method for even-numbered teams
    for i in range(len(players)):
      if i % 2 == 0:
        team1.append(players[i])
        team1scores.append(scores[i])
      else:
        team2.append(players[i])
        team2scores.append(scores[i])
  else: #Method for odd-numbered teams
    team2.append(players[len(players) - 1])
    team2scores.append(scores[len(scores) - 1])
    for i in range(len(players) - 1):
      if i % 2 == 0:
        team1.append(players[i])
        team1scores.append(scores[i])
      else:
        team2.append(players[i])
        team2scores.append(scores[i])
    
  print(team1)
  print(team1scores)
  print(team2)
  print(team2scores)

#Shuffles team1 and team2 indices

def shuffle():
  print("---SHUFFLING---")
  team1 = db["team1"]
  team2 = db["team2"]
  players = db["players"]
  team1scores = db["team1scores"]
  team2scores = db["team2scores"]
  shuffleNum = len(team1) // 2

  if "randomIndex" in db.keys():
    randomIndex = db["randomIndex"]
    randomIndex.clear()
  else:
    db["randomIndex"] = []
    randomIndex = db["randomIndex"]

  while len(randomIndex) != shuffleNum:
    if len(players) % 2 == 0:
      number = random.randint(0, len(team1) - 1)
      randomIndex.append(number)
    else:
      number = random.randint(1, len(team1) - 1)
      randomIndex.append(number)

    print("random number is: " + str(number))

    sort_list(randomIndex)

    if len(randomIndex) > 1:
      if randomIndex[len(randomIndex) - 1] == randomIndex[len(randomIndex) - 2]:
        randomIndex.pop()

  print(randomIndex)
      
  for x in randomIndex:
    team1[x], team2[x] = team2[x], team1[x]
    team1scores[x], team2scores[x] = team2scores[x], team1scores[x]

  sort_lists(team1, team1scores)
  sort_lists(team2, team2scores)
  
  print(team1)
  print(team1scores)
  print(team2)
  print(team2scores)

#Creates disparity bar

def make_disparity_string():
  value = sum(db["team1scores"]) - sum(db["team2scores"])
  totalPoints = sum(db["team1scores"]) + sum(db["team2scores"])
  blueCircles = (sum(db["team1scores"]) / totalPoints) * 10
  redCircles = 10 - blueCircles
  bluePercentage = str(round(blueCircles * 10, 1)) + "%"
  redPercentage = str(round(redCircles * 10, 1)) + "%"
  
  print("disparity is: " + str(value))
  print("total points is: " + str(totalPoints))
  print("blue's circle count: " + str(blueCircles))
  
  string = "__**TEAM DISPARITY**__ - "
  if round(value) > 0:
    string += "Blue Team has an advantage of " + str(round(value)) + " tier(s)\n" + bluePercentage + " **BLUE**  |  "
  elif round(value) == 0:
    string = "Disparity between teams is less than 1 tier\n" + bluePercentage + " **BLUE**  |  "
  else:
    string = "Red Team has an advantage of " + str(round(abs(value))) + " tier(s)\n" + bluePercentage + " **BLUE**  |  "
  
  blue = round(blueCircles)
  print("blue = " + str(blue))
  red = round(10 - blue)
  print("red = " + str(red))
  
  for x in range(0, blue):
    string += ":blue_circle:"
  for x in range(0, red):
    string += ":red_circle:"
  string = string + "  |  **RED** " + redPercentage
  return string

#Occurs on bot start-up

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

#Occurs on message

@client.event
async def on_message(message):
  global teamMode
  global alreadySorted
  if message.author == client.user:
    return
    
#Team Mode
    
  if teamMode == 1:
    if message.content.startswith("$team"):
      team_off()
      await message.channel.send("Team Mode Off!")

    # $clear
      
    elif message.content.startswith("$clear"):
      alreadySorted = 0
      clear_all_players()
      await message.channel.send("Cleared all players from the roster!")

    # $del

    elif message.content.startswith("$del"):
      msg = message.content.split(' ')
      players = []
      scores = []
      if "players" in db.keys():
        players = db["players"]
        scores = db["scores"]
        number = int(msg[1]) - 1
        if number > len(players) - 1 or (number) < 0:
          await message.channel.send("Index out of bounds, please try again!")
        else:
          alreadySorted = 0
          await message.channel.send("**" + players[number] + "**" + " has been removed from the roster!")
          players.pop(number)
          print(str(scores[number]) + " has been removed from the scores list")
          scores.pop(number)
      else:
        await message.channel.send("Roster is currently empty!")

    # $balance
      
    elif message.content.startswith("$balance"):
      if alreadySorted == 0: #only sorts and balances if it needs to
        if len(db["players"]) < 2:
          await message.channel.send("Not enough players to create teams!")
        else:
          await message.channel.send("*Generating teams. Might take a moment.*")
          players = db["players"]
          scores = db["scores"]
          await message.channel.send("*Sorting...*")
          sort_lists(players, scores)
          await message.channel.send("*Balancing...*")
          balance_teams()
          
      await message.channel.send("*Shuffling...*")
      shuffle()
        
      alreadySorted = 1

        #disparity values

      print("Team 1 = " + str(sum(db["team1scores"])))
      print("Team 2 = " + str(sum(db["team2scores"])))
      disparityString = make_disparity_string()
        
      team1string = "__**BLUE TEAM**__\n"
      team1 = db["team1"]
      for x in range(len(team1)):
        team1string += str(x + 1) + "." + " " + team1[x] + "\n"
      team2string = "__**RED TEAM**__\n"
      team2 = db["team2"]
      for x in range(len(team2)):
        team2string += str(x + 1) + "." + " " + team2[x] + "\n"
      await message.channel.send(team1string)
      await message.channel.send(team2string)
      await message.channel.send(disparityString + "\nTo **reshuffle** the teams, type in the command: **$balance**")
      
    # $print
      
    elif message.content.startswith("$print"):
      players = []
      if "players" in db.keys():
        players = db["players"]
        number = len(players)
        list = "__**CURRENT ROSTER**__  -  " + str(number) + " Player"
        if (number > 1 or number == 0):
          list += "s"
        i = 0
        while i < len(players):
          list += " \n" + db["players"][i] + " (" + str(i + 1) + ")"
          i = i + 1
        await message.channel.send(list)
      else:
        await message.channel.send("Roster is currently empty!")

    #Adding players to roster
      
    else:
      msg = message.content
      list = msg.split(' ')
      
      name = list[0] #name = players name (string)
      rank = convert_rank(list) #rank = rank score (integer)
      
      if rank < 1:
        await message.channel.send("*Invalid rank! Please try again!*")
      else:
        alreadySorted = 0
        upload_players(name, rank)
        await message.channel.send("**" + name + "**" + " has been registered!")
        print(name + " " + str(rank))
      
#Normal Bot Functions     
      
  else:
    msg = message.content.lower()
  
    if msg.startswith("$team"):
      team_on()
      await message.channel.send("Team Mode On! Everyone please type in your name and your rank like this: \n**Christian Iron 4** \n*(Type 1 after Master, Grandmaster, and Challenger)* \n*(Please type in one word for your name)*")
      await message.channel.send("To **balance** the teams, type in the command: **$balance** \n\nTo **view** the roster and player numbers, type in the command: **$print** \n\nTo **remove** a player, type in the command: **$del** followed by their player number \n\nTo **clear** the roster, type in the command: **$clear** \n\nTo **exit** Team Mode, type in the command: **$team**")
  
    if any(word in msg for word in pickUpLineCues):
      await message.channel.send(random.choice(starters))
      line = get_line()
      await message.channel.send(line)
  
    elif any(word in msg for word in shootingCues):
      await message.channel.send(random.choice(shootingResult))
  
    elif any(word in msg for word in cues):
      await message.channel.send(random.choice(cuesResult))
      await message.channel.send(random.choice(rizz))
      
#Reboots bot every 30 minutes
keep_alive()

#Runs kill 1 if there are errors with running the bot
try:
  client.run(os.environ['TOKEN'])
except:
  os.system("kill 1")