import asyncio
import discord
from discord.ext import commands
from time import strftime
from dateutil import parser
from datetime import datetime
import os

prefix = '>'
alarmList2 = {}  # Dictionary of lists of alarms

description = "A simple alarm clock bot.\ntype "+prefix+"help for help.\nMade by DaMightyZombie"
bot = commands.Bot(command_prefix=prefix, description=description)
client = discord.Client()

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
    await ctx.send("```"+time_str+"```")
    del time_str


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
async def a(ctx, in_time):
    """sets an alarm for the given time / date. Short for alarm."""
    await Ialarm(ctx, in_time)


@bot.command(pass_context=True)
async def d(ctx, ind):
    """removes the alarm at the given index from the alarmList. Alias of delete."""
    await Iremove_alarm(ctx, ind)


@bot.command(pass_context=True)
async def rm(ctx, ind):
    """removes the alarm at the given index from the alarmList. Alias of delete."""
    await Iremove_alarm(ctx, ind)


@bot.command(pass_context=True)
async def delete(ctx, ind):
    """removes the alarm at the given index from the alarmList."""
    await Iremove_alarm(ctx, ind)


@bot.command(pass_context=True)
async def remove(ctx, ind):
    """removes the alarm at the given index from the alarmList. Alias of delete."""
    await Iremove_alarm(ctx, ind)


# END ALIASES-----------------------

# BEGIN FUNCTIONS-------------------

async def Ialarmlist(cont):  # ALARMLIST COMMAND
    """lists all currently active alarms."""
    embed = discord.Embed(title=":alarm_clock:Alarm List", color=0x22a7cc)
    embed.set_thumbnail(url="http://cdn.iphonehacks.com/wp-content/uploads/2017/01/alarm-icon-29.png")
    print('Current alarm list:')
    if cont.channel not in alarmList2.keys() or alarmList2[cont.channel] == []:
        await cont.send('no alarms have yet been set in this channel. add one with ' + prefix + 'alarm [time].')
        return
    for i in range(len(alarmList2[cont.channel])):
        embed.add_field(name='#' + str(i + 1) + ':' + str(alarmList2[cont.channel][i].name).split('#', 1)[0],
                        value=str(alarmList2[cont.channel][i].time), inline=True)
        print('#' + str(i + 1) + ':' + str(alarmList2[cont.channel][i].name) + " -> " + str(alarmList2[cont.channel][i].time))
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
__if no date is supplied, the current day will be used.__")
        return
    if alarmTime < datetime.now():
        await cont.send('The date / time you supplied is in the past. No alarm has been set.')
        return

    temp = Alarm(cont.author, alarmTime)
    if cont.channel not in alarmList2.keys():
        alarmList2.update({cont.channel: []})

    alarmList2[cont.channel].append(temp)  # add the alarm to the list at the index (channel)
    del temp

    await cont.send(
        ":white_check_mark:" + cont.author.mention + "'s alarm is now set to **" + str(alarmTime.date()) + ", " + str(
            alarmTime.time()) + "**!")

async def Iremove_alarm(cont, index):
    index = int(index) - 1
    if cont.author == alarmList2[cont.channel][index].name:  # you shouldn't be able to delete other people's alarms
        alarm_time = alarmList2[cont.channel][index].time
        await cont.send(":white_check_mark:Your alarm for **" + str(alarm_time.date()) + ", "
                        + str(alarm_time.time()) + "** has been removed.")
        del alarmList2[cont.channel][index]
        del alarm_time
    else:
        await cont.send("the alarm at the Index you entered does not belong to you.")


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
        for alarmList in alarmList2.values():
            for i in range(len(alarmList)):
                if alarmList[i].time < datetime.now():
                    await alarmList[i].name.create_dm()
                    await alarmList[i].name.dm_channel.send(content=":alarm_clock:Your alarm for **"+alarmList[i].time+"** just rang!")
                    print("alarm of "+str(alarmList[i].name)+" just rang!")
                    alarmList.pop(i)
        await asyncio.sleep(5)  # task runs every 60 seconds


# END BACKGROUND TASKS--------------

bot.loop.create_task(check_alarms())
bot.run(os.getenv('token'))
