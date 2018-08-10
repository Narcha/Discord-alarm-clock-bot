import asyncio
import discord
from discord.ext import commands
from time import strftime
from dateutil import parser
from datetime import datetime

prefix = '>'
alarmList = []

description = "A simple alarm clock bot.\ntype "+prefix+"help for help.\nMade by DaMightyZombie"
bot = commands.Bot(command_prefix=prefix, description=description)


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('-'*20)
    await bot.change_presence(activity=discord.Game(name='>help'))


# BEGIN COMMAND TEMPLATE------------
'''
@bot.command()
async def cmd_name(inp):
    """description"""
    await ctx.send(inp)
'''


# END COMMAND TEMPLATE--------------

# BEGIN COMMANDS--------------------

@bot.command()  # TIME COMMAND
async def time(ctx):
    """displays the current time."""
    time_str = strftime("%H:%M:%S")
    await ctx.send(time_str)


# END COMMANDS----------------------

# BEGIN ALIASES---------------------

@bot.command(pass_context=True)
async def la(ctx):
    """lists all currently active alarms. Short for ListAlarms."""
    await Ialarmlist(ctx)


@bot.command(pass_context=True)
async def alarm(ctx, time):
    """sets an alarm for the given time / date."""
    await Ialarm(ctx, time)


@bot.command(pass_context=True)
async def a(ctx, time):
    """sets an alarm for the given time / date. Short for alarm."""
    await Ialarm(ctx, time)


# END ALIASES-----------------------


# BEGIN FUNCTIONS-------------------

async def Ialarmlist(cont):  # ALARMLIST COMMAND
    """lists all currently active alarms."""
    embed = discord.Embed(title=":alarm_clock:Alarm List", color=0x22a7cc)
    embed.set_thumbnail(url="http://cdn.iphonehacks.com/wp-content/uploads/2017/01/alarm-icon-29.png")
    print('Current alarm list:')
    for i in range(len(alarmList)):
        embed.add_field(name='#' + str(i + 1) + ':' + str(alarmList[i].name).split('#', 1)[0],
                        value=str(alarmList[i].time), inline=True)
        print('#' + str(i + 1) + ':' + str(alarmList[i].name) + " -> " + str(alarmList[i].time))
    print('-'*50)
    await cont.send(embed=embed)


async def Ialarm(cont, inp):  # ALARM COMMAND
    """sets an alarm for the given time / date."""
    try:
        alarmTime = parser.parse(inp)
    except:
        await cont.send(":negative_squared_cross_mark:Please use the Format \"[M-D-Y] H:M:S\".\
__Examples:__\
12-24 10:00 --> 24th Dec of the current year, 10:00:00.\
12:30 --> 12:30, today.\
__if no date is supplied, the current day will be used.__");
        return

    temp = Alarm(cont.author, alarmTime)
    alarmList.append(temp)
    del temp
    await cont.send(
        ":white_check_mark:" + cont.author.mention + "'s alarm is now set to " + str(alarmTime.date()) + ", " + str(
            alarmTime.time()) + "!")


# END FUNCTIONS---------------------

# BEGIN CLASSES---------------------

class Alarm:
    name = None
    time = None

    def __init__(self, usr, t):
        self.name = usr
        self.time = t


# END CLASSES-----------------------

# BEGIN BACKGROUND TASKS------------

async def check_alarms():
    await bot.wait_until_ready()
    while not bot.is_closed():
        for itm in alarmList:
            if itm.time < datetime.now():
                print("alarm of "+str(itm.name)+" just rang!")
        await asyncio.sleep(5)  # task runs every 60 seconds


# END BACKGROUND TASKS--------------

bot.loop.create_task(check_alarms())
bot.run('NDc2ODIwNzc0ODcxNzYwODk3.DkzaCw.l8mhRpKl6zhmYGR3VGz4w7xBukg')
