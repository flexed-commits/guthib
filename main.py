from keep_alive import keep_alive
keep_alive()

import discord
from discord.ext import commands
import asyncio
import time
from webbot import Browser
import argparse
import sys

intents = discord.Intents.default()
intents.typing = False
intents.presences = False

bot = commands.Bot(command_prefix='!', intents=intents)

def getOptions(args=sys.argv[1:]):
    parser = argparse.ArgumentParser(description="This bot helps users to mass report accounts with clickbaits or objectionable material.")
    parser.add_argument("-f", "--file", type=str, default="acc.txt", help="Accounts list (Defaults to acc.txt in program directory).")
    options = parser.parse_args(args)
    return options

async def report_user(username, user_pass_list, ctx):
    acc_file = getOptions().file

    for username, password in user_pass_list:
        web = Browser()
        web.go_to("https://www.instagram.com/accounts/login/")

        web.type(username, into='Phone number, username, or email')
        time.sleep(0.5)
        web.press(web.Key.TAB)
        time.sleep(0.5)
        web.type(password, into='Password')
        web.press(web.Key.ENTER)

        time.sleep(2.0)

        # Proceed with the rest of your script for reporting
        web.go_to("https://www.instagram.com/%s/" % username)
        time.sleep(1.5)
        web.click(xpath='//*[@id="react-root"]/section/main/div/header/section/div[1]/div/button')
        time.sleep(0.5)
        web.click(text='Report User')
        time.sleep(1.5)
        web.click(xpath="/html/body/div[4]/div/div/div/div[2]/div/div/div/div[3]/button[1]")
        time.sleep(0.5)
        web.click(text='Close')
        time.sleep(0.5)
        web.click(xpath='/html/body/div[1]/section/nav/div[2]/div/div/div[3]/div/div[3]/a')
        time.sleep(0.5)
        web.click(xpath='/html/body/div[1]/section/main/div/header/section/div[1]/div/button')
        time.sleep(0.5)
        web.click(text='Log Out')
        time.sleep(0.5)

    await ctx.send("Reporting completed for user: {}".format(username))



@bot.command()
async def rep(ctx, username, repetition='1x'):
    repetition_factor = int(repetition[:-1]) if repetition.endswith('x') else 1

    user_pass_list = [line.strip().split(":") for line in open(acc.txt)]

    await ctx.send("Reporting started for user: {} ({} times)".format(username, repetition_factor))

    tasks = []
    for _ in range(repetition_factor):
        tasks.append(report_user(username, user_pass_list, ctx))

    await asyncio.gather(*tasks)

    await ctx.send("All reporting completed for user: {}".format(username))

@bot.command()
async def ping(ctx):
    await ctx.send('pong!')

bot.run('Past_Your_Bot_Token_Here')