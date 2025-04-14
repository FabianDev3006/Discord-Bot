import re
import discord
from discord.ext import commands
import os
import random
import datetime
from dotenv import load_dotenv
import time

load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")

if TOKEN is None:
    raise ValueError(":warning: DISCORD_BOT_TOKEN is missing! Check your .env file.")

intents = discord.Intents.default()
intents.message_content = True
intents.bans = True

bot = commands.Bot(command_prefix="!", intents=intents)

user_spam_tracker = {}

SPAM_THRESHOLD = 3
SPAM_TIME_WINDOW = 5 
TIMEOUT_DURATION = 3

banned_patterns = [
    r"n[i1!l|][gq9][gq9e3][e3@a4][r@]",     
    r"n[l1][gq9][gq9e3][e3@a4][r@]",        
    r"n[i1!l|][b8][b8e3][e3@a4][r@]?",      
    r"n[l1][b8][b8e3][e3@a4][r@]?",         
    r"n[il1!][gq9][gq9e3][e3@a4][r@]",      
    r"n[il1!][b8][b8e3][e3@a4][r@]?",       
    r"n[il1!][q9][q9e3][e3@a4][r@]",        
    r"n[il1!][gq9][gq9e3][e3@a4][h@]",      
    r"n[il1!][gq9][gq9e3][e3@a4][u@h]",     
    r"n[il1!][gq9]{2,}[e3@a4][r@]",         
    r"n[il1!][b8]{2,}[e3@a4][r@]?",         
    r"n[il1!][q9]{2,}[e3@a4][r@]?",         
    r"n[il1!][gq9]{2,}[e3@a4][h@]",         
    r"n[il1!][gq9]{2,}[e3@a4][u@h]",        
    r"[r@][e3@a4][gq9e3][gq9][i1!l|]n",     
    r"[r@][e3@a4][gq9e3][gq9][l1]n",        
    r"[r@]?[e3@a4][b8e3][b8][i1!l|]n",      
    r"[r@]?[e3@a4][b8e3][b8][l1]n",         
    r"[r@][e3@a4][gq9e3][gq9][il1!]n",      
    r"[r@]?[e3@a4][b8e3][b8][il1!]n",       
    r"[r@][e3@a4][q9e3][q9][il1!]n",        
    r"[h@][e3@a4][gq9e3][gq9][il1!]n",      
    r"[u@h][e3@a4][gq9e3][gq9][il1!]n",     
    r"[r@][e3@a4][gq9]{2,}[il1!]n",         
    r"[r@]?[e3@a4][b8]{2,}[il1!]n",         
    r"[r@]?[e3@a4][q9]{2,}[il1!]n",         
    r"[h@][e3@a4][gq9]{2,}[il1!]n",         
    r"[u@h][e3@a4][gq9]{2,}[il1!]n",        
    r"n[i1!l|][gq9][gq9e3]?",               
    r"n[l1][gq9][gq9e3]?",                   
    r"n[il1!][gq9]{2,}",                     
    r"n[il1!][gq9][gq9e3][e3@a4]?",          
    r"n[il1!][gq9][gq9e3][h@]?",             
    r"n[il1!][gq9][gq9e3][u@h]?",            
    r"[gq9e3]?[gq9][i1!l|]n",                
    r"[gq9e3]?[gq9][l1]n",                   
    r"[gq9]{2,}[il1!]n",                     
    r"[e3@a4]?[gq9e3][gq9][il1!]n",          
    r"[h@]?[gq9e3][gq9][il1!]n",             
    r"[u@h]?[gq9e3][gq9][il1!]n",            
    r"f[gq69][t+]",                          
    r"f[gq69] ?[t+]",                        
    r"f[gq69][t+]?",                         
    r"f[gq69][t+]?[sz5$]?",                  
    r"f[gq69][t+]?[!?]*",                    
    r"f[gq69]{2,}[t+]?",                     
    r"[t+]?[gq69]f",                         
    r"[t+]? ?[gq69]f",                       
    r"[t+]?[gq69]f",                         
    r"[sz5$]?[t+]?[gq69]f",                  
    r"[!?]*[t+]?[gq69]f",                    
    r"[t+]?[gq69]{2,}f",                     
    r"k[y¥][s$5z]",                         
    r"k[y¥] ?[s$5z]",                       
    r"k[i1!][l1!][l1!] ?(yourself|urself|yo self|u rself|urself|now)",  
    r"(delete|end|off|unalive) ?yourself",  
    r"f[a@][gq69][gq69o0][o0@]?[t+]?",      
    r"f[a@] ?[gq69] ?[gq69o0] ?[o0@] ?[t+]?",
    r"[t+]?[o0@]?[gq69o0][gq69][a@]f",      
    r"[t+]? ?[o0@] ?[gq69o0] ?[gq69] ?[a@]f",
    r"c[o0][o0]?n",                         
    r"c[o0] ?[o0]?n",                       
    r"r[e3][t+]a[r@]d",                     
    r"r[e3] ?[t+] ?a ?[r@] ?d",             
    r"n[o0]?[o0]c",                         
    r"n ?[o0]? ?[o0]c",                     
    r"d[r@]a[t+][e3]r",                     
    r"d ?[r@] ?a ?[t+] ?[e3] ?r",               
    r"n[i1!l|][gq9][gq9e3][e3@a4]?[r@]?[sz5$]?",  
    r"n[i1!l|][gq9][gq9e3][e3@a4]?[r@]?[!?]*", 
    r"n[i1!l|][gq9][gq9e3][e3@a4]?[r@]?[xX]*",   
    r"f[gq69][t+]?[xX]*",                         
    r"f[gq69][t+]?[o0]*",                         
    r"n[i1!l|][gq9][gq9e3][e3@a4]?[r@]?[o0]*",    
    r"n[íïîì][gq9][gq9e3][e3@a4][r@]",           
    r"f[gq69][t+]?[ṭțṯẗ]",                        
    r"n\s*[i1!l|]\s*[gq9]\s*[gq9e3]\s*[e3@a4]\s*[r@]",  
    r"f\s*[gq69]\s*[t+]",                               
    r"n[i1!l|][gq9][gq9e3][e3@a4][r@]?[\.\-_]*",  
    r"f[gq69][t+]?[\.\-_]*",                      
    r"[nN][iI1!l|][gGqQ9][gGqQ9eE3][eE3@aA4][rR@]",  
    r"[fF][gGqQ69][tT+]",                            
    r"n[i1!l|][gq9]{3,}[e3@a4][r@]?",               
    r"f[gq69]{2,}[t+]?",                            
    r"\b\w*n[i1!l|][gq9][gq9e3][e3@a4][r@]?\w*\b",
    r"\b\w*f[gq69][t+]?\w*\b",                    
]

banned_regex = re.compile(r"\b(" + "|".join(banned_patterns) + r")\b", re.IGNORECASE)

@bot.event
async def on_ready():
    print(f":white_check_mark: Logged in as {bot.user.name}")
    await bot.change_presence(activity=discord.Game(name="Fck Nzs v.161"))

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    message_content = message.content.lower()

    if banned_regex.search(message_content):
        user_id = message.author.id
        current_time = time.time()

        if user_id not in user_spam_tracker:
            user_spam_tracker[user_id] = {"count": 0, "timestamps": []}

        user_spam_tracker[user_id]["timestamps"].append(current_time)
        user_spam_tracker[user_id]["count"] += 1

        user_spam_tracker[user_id]["timestamps"] = [
            t for t in user_spam_tracker[user_id]["timestamps"]
            if current_time - t <= SPAM_TIME_WINDOW
        ]
        user_spam_tracker[user_id]["count"] = len(user_spam_tracker[user_id]["timestamps"])

        await message.delete()

        if user_spam_tracker[user_id]["count"] >= SPAM_THRESHOLD:
            await message.author.timeout(
                until=discord.utils.utcnow() + datetime.timedelta(seconds=TIMEOUT_DURATION),
                reason="Spamming bad words"
            )
            await message.channel.send(f"{message.author.mention} has been muted for {TIMEOUT_DURATION} seconds for spamming bad words.")
            user_spam_tracker[user_id] = {"count": 0, "timestamps": []}
        else:
            chance = random.random()
            if chance < 0.5:
                await message.channel.send(f"{message.author.mention}, Erste Verwarnung!")
            elif chance < 0.999:
                await message.channel.send(f"{message.author.mention}, Zweite Verwarnung!")
            else:
                await message.author.timeout(
                    until=discord.utils.utcnow() + datetime.timedelta(minutes=1),
                    reason="Dritte Verwarnung!"
                )
                await message.channel.send(f"{message.author.mention} unlucky!")

    await bot.process_commands(message)

@bot.event
async def on_message_edit(before, after):
    if after.author == bot.user:
        return

    message_content = after.content.lower()

    if banned_regex.search(message_content):
        user_id = after.author.id
        current_time = time.time()

        if user_id not in user_spam_tracker:
            user_spam_tracker[user_id] = {"count": 0, "timestamps": []}

        user_spam_tracker[user_id]["timestamps"].append(current_time)
        user_spam_tracker[user_id]["count"] += 1

        user_spam_tracker[user_id]["timestamps"] = [
            t for t in user_spam_tracker[user_id]["timestamps"]
            if current_time - t <= SPAM_TIME_WINDOW
        ]
        user_spam_tracker[user_id]["count"] = len(user_spam_tracker[user_id]["timestamps"])

        await after.delete()

        if user_spam_tracker[user_id]["count"] >= SPAM_THRESHOLD:
            await after.author.timeout(
                until=discord.utils.utcnow() + datetime.timedelta(seconds=TIMEOUT_DURATION),
                reason="merkste selbst"
            )
            await after.channel.send(f"{after.author.mention} wurde für {TIMEOUT_DURATION} Sekunden bestraft.")
            user_spam_tracker[user_id] = {"count": 0, "timestamps": []}
        else:
            chance = random.random()
            if chance < 0.5:
                await after.channel.send(f"{after.author.mention}, Erste Verwarnung!")
            elif chance < 0.999:
                await after.channel.send(f"{after.author.mention}, Zweite Verwarnung!")
            else:
                await after.author.timeout(
                    until=discord.utils.utcnow() + datetime.timedelta(minutes=1),
                    reason="Dritte Verwarnung!"
                )
                await after.channel.send(f"{after.author.mention} unlucky bye bye")

    await bot.process_commands(after)

bot.run(TOKEN)