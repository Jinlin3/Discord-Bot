import discord
import os
import requests
import random
from keep_alive import keep_alive

intent = discord.Intents.default()
intent.members = True
intent.message_content = True

client = discord.Client(intents = intent)

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
  "My rizz is impeccable.",
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

def get_line():
  url = "https://pick-me-up.p.rapidapi.com/dirty"
  headers = {
	"X-RapidAPI-Key": "36ef312bcemsh00e92d766bf9906p180189jsn5566eae4451b",
	"X-RapidAPI-Host": "pick-me-up.p.rapidapi.com"
}
  response = requests.request("GET", url, headers=headers)

  return (response.text)

@client.event
async def on_ready(): #Triggers when bot turns on
  print('We have logged in as {0.user}'.format(client))

@client.event #Triggers when a message is sent in a channel
async def on_message(message):
  if message.author == client.user:
    return

  msg = message.content.lower() #Converts message to lowercase for easier comparison

  if any(word in msg for word in pickUpLineCues):
    await message.channel.send(random.choice(starters))
    line = get_line()
    await message.channel.send(line)

  elif any(word in msg for word in shootingCues):
    await message.channel.send(random.choice(shootingResult))

  elif any(word in msg for word in cues):
    await message.channel.send(random.choice(cuesResult))
    await message.channel.send(random.choice(rizz))

keep_alive() #Reboots bot every 5 minutes
client.run(os.environ['TOKEN'])