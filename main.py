#Skyler

import discord
import os
import asyncio
import random
from dotenv import load_dotenv
intents = discord.Intents.all()
intents.members= True
intents.message_content = True
intents.presences = True
intents.guilds = True
intents.messages = True

#Declaring bot
bot = discord.Bot(intents = intents)

#Adding bot activity
@bot.event
async def on_ready():
    await bot.change_presence(status = discord.Status.do_not_disturb, activity = discord.Game(name = 'Fallout: New Vegas'))
    print("Bot {0.user} is running...".format(bot))

#-----> NEWS COMMANDS <-----#

#Patch Notes command
@bot.slash_command(name = 'patchnotes', description = "What's changed in the latest update")
async def self(ctx: discord.ApplicationContext):
    patchnotes_embed = discord.Embed(title = "Patch Notes v1.0", colour = discord.Colour.random())
    patchnotes_embed.add_field(name = "Thank you", value = "This is the very first version of RickBot! As a Rick, I will continue to improve on it and make it a better experience for you.", inline = False)
    patchnotes_embed.set_thumbnail(url = 'https://i.ibb.co/0C5RgM3/Rickbot-enjoying-death.png')
    await ctx.respond(embed = patchnotes_embed)

#Announcement Maker command
@bot.slash_command(name = 'announcement', description = "Create an announcement")
@discord.default_permissions(administrator = True)
async def announce(ctx: discord.ApplicationContext):
    await ctx.respond('Answer the following questions (10 minutes left):')

    questions = ["Main Title: ", "Short Description: ", "Field Title: ", "Field Description: ", "Thumbnail URL: ", "Mention The Channel: "]
    replies = []

    def check(user):
        return user.author == ctx.author and user.channel == ctx.channel
    
    for question in questions:
        await ctx.send(question)
        try:
            msg = await bot.wait_for('message', timeout = 600, check = check)
        except asyncio.TimeoutError:
            await ctx.send("Ran out of time! (Limited to 10 minutes, try again...)")
            return
        else:
            replies.append(msg.content)

    main_title = replies[0]
    short_desc = replies[1]
    field_title = replies[2]
    field_desc = replies[3]
    thumbnail_url = replies[4]
    target_channel = int(replies[5][2:-1])
    channel = bot.get_channel(target_channel)

    announcement_embed = discord.Embed(title = main_title, description = short_desc, colour = discord.Colour.random())
    announcement_embed.add_field(name = field_title, value = field_desc, inline = False)
    announcement_embed.set_thumbnail(url = thumbnail_url)

    await channel.send(embed = announcement_embed)
    await ctx.respond("Done, go check your announcement :D")

#-----> MEMBER MANAGEMENT COMMANDS <-----#

#Give Verified Role command
@bot.slash_command(name = 'verify', description = "Verify a member quickly")
@discord.default_permissions(manage_roles = True)
async def verify(ctx: discord.ApplicationContext, member: discord.Member):
    role = discord.utils.get(ctx.guild.roles, name = 'Verified')
    server = ctx.guild.roles
    if role in member.roles:
        msg = f"Member {member.mention} is already verified!"
    elif role not in member.roles and role in server:
        await member.add_roles(role)
        msg = f"Member {member.mention} just got verified!"
    elif role not in member.roles and role not in server:
        await ctx.guild.create_role(name = 'Verified', colour = discord.Colour(0x2ecc71))
        created_role = discord.utils.get(ctx.guild.roles, name = 'Verified')
        await member.add_roles(created_role)
        msg = f"Member {member.mention} just got verified!"
    await ctx.respond(msg)

#User Info command
@bot.slash_command(name = 'userinfo', description = "Display information about a member")
async def userinfo(ctx: discord.ApplicationContext, *, member: discord.Member):
    if member is None:
        member = ctx.author
    info_embed = discord.Embed(title = 'User Information', colour = discord.Colour.random())
    info_embed.set_thumbnail(url = member.avatar)
    info_embed.add_field(name = 'Name', value = member.name, inline = False)
    info_embed.add_field(name = 'Nickname', value = member.nick, inline = False)
    info_embed.add_field(name = 'Account Created Date', value = member.created_at, inline = False)
    info_embed.add_field(name = 'Joined Server Date', value = member.joined_at, inline = False)
    await ctx.respond(embed = info_embed)

#User Avatar command
@bot.slash_command(name = 'useravatar', description = "Get a user's avatar")
async def useravatar(ctx: discord.ApplicationContext, *, member: discord.Member):
    if member is None:
        member = ctx.author
        name = member.display_name
    name = member.display_name
    avatar_embed = discord.Embed(title = f"Avatar of {name}", colour = discord.Colour.random())
    avatar_embed.set_image(url = member.avatar)
    await ctx.respond(embed = avatar_embed)

#-----> SERVER MANAGEMENT COMMANDS <-----#

#Server Stats command
@bot.slash_command(name = 'serverstats', description = "Display the statistics of the server")
async def serverstats(ctx: discord.ApplicationContext):
    stats_embed = discord.Embed(title = 'Server Statistics', colour = discord.Colour.random())
    stats_embed.add_field(name = 'Name', value = ctx.guild.name, inline = False)
    stats_embed.add_field(name = 'Owner', value = ctx.guild.owner, inline = False)
    stats_embed.add_field(name = 'Server Created Date', value = ctx.guild.created_at, inline = False)
    stats_embed.add_field(name = 'Members Count', value = ctx.guild.member_count, inline = False)
    stats_embed.set_thumbnail(url = ctx.guild.icon)
    await ctx.respond(embed = stats_embed)

#-----> INTERACTION COMMANDS <-----#

#Rock Paper Scissors command
@bot.slash_command(name ='rockpaper', description = 'Play Rock Paper Scissors')
async def rockpaper(ctx: discord.ApplicationContext, member: discord.Member, choice: str):
    user_value = choice
    author = ctx.author
    member = member

    def check(message: discord.Message):
        return message.author == member and message.channel == ctx.channel

    try:
        await ctx.respond(f"Hey {member.mention}, {author.name} challenged you to Rock Paper Scissors and it's your turn:")
        message =  await bot.wait_for('message', check = check, timeout=120)
    except asyncio.TimeoutError:
        await ctx.respond(f"Ran out of time for this command. Try again!")
        return
    
    member_value = message.content

    if user_value.lower() == "Rock".lower() and member_value.lower() == "Rock".lower():
        await ctx.respond(f"{author.name}: 🗿 | {member.name}: 🗿. It's a tie!")
    elif user_value.lower() == "Rock".lower() and member_value.lower() == "Paper".lower():
        await ctx.respond(f"{author.name}: 🗿 | {member.name}: 📄. The win goes to {member.name}!")
    elif user_value.lower() == "Rock".lower() and member_value.lower() == "Scissors".lower():
        await ctx.respond(f"{author.name}: 🗿 | {member.name}: ✂. The win goes to {author.name}!")
    
    elif user_value == "Paper".lower() and member_value.lower() == "Rock".lower():
        await ctx.respond(f"{author.name}: 📄 | {member.name}: 🗿. The win goes to {author.name}!")
    elif user_value == "Paper".lower() and member_value.lower() == "Paper".lower():
        await ctx.respond(f"{author.name}: 📄 | {member.name}: 📄. It's a tie!")
    elif user_value == "Paper".lower() and member_value.lower() == "Scissors".lower():
        await ctx.respond(f"{author.name}: 📄 | {member.name}: ✂. The win goes to {member.name}!")
    
    elif user_value == "Scissors".lower() and member_value.lower() == "Rock".lower():
        await ctx.respond(f"{author.name}: ✂ | {member.name}: 🗿. The win goes to {member.name}!")
    elif user_value == "Scissors".lower() and member_value.lower() == "Paper".lower():
        await ctx.respond(f"{author.name}: ✂ | {member.name}: 📄. The win goes to {author.name}!")
    elif user_value == "Scissors".lower() and member_value.lower() == "Scissors".lower():
        await ctx.respond(f"{author.name}: ✂ | {member.name}: ✂. It's a tie!")

#Say command
@bot.slash_command(name = 'say', description = "Make RickBot say anything!")
async def say(ctx: discord.ApplicationContext, *, text):
    await ctx.respond(text)

#Hug command
@bot.slash_command(name = 'hug', description = "Hug a user")
async def hug(ctx: discord.ApplicationContext, member: discord.Member):
    gif = [
        "https://media.tenor.com/G_IvONY8EFgAAAAd/aharen-san-anime-hug.gif",
        "https://media.tenor.com/HYkaTQBybO4AAAAd/hug-anime.gif",
        "https://media.tenor.com/9e1aE_xBLCsAAAAd/anime-hug.gif",
        "https://media.tenor.com/Z9zjQy8uEvsAAAAd/clannad-hugs.gif",
        "https://media.tenor.com/RWD2XL_CxdcAAAAd/hug.gif",
        "https://media.tenor.com/cGFtCNuJE6sAAAAd/anime-aesthetic.gif",
        "https://media.tenor.com/PCIu5V-_c1QAAAAd/iloveyousomuch-iloveyou.gif"
    ]
    random_hug = random.choice(gif)
    author = ctx.author
    hug_embed = discord.Embed(colour = discord.Colour.random())
    hug_embed.add_field(name = '', value = f"{author.mention} is hugging {member.mention} ☺️", inline = True)
    hug_embed.set_thumbnail(url = random_hug)
    await ctx.respond(embed = hug_embed)

#Kiss command
@bot.slash_command(name = 'kiss', description = "Kiss a user")
async def kiss(ctx: discord.ApplicationContext, member: discord.Member):
    gif = [
        "https://media.tenor.com/jnndDmOm5wMAAAAd/kiss.gif",
        "https://media.tenor.com/YHxJ9NvLYKsAAAAd/anime-kiss.gif",
        "https://media.tenor.com/F02Ep3b2jJgAAAAd/cute-kawai.gif",
        "https://media.tenor.com/2tB89ikESPEAAAAd/kiss-kisses.gif",
        "https://media.tenor.com/mNPxG38pPV0AAAAd/kiss-love.gif",
        "https://media.tenor.com/woA_lrIFFAIAAAAd/girl-anime.gif",
        "https://media.tenor.com/rS045JX-WeoAAAAd/anime-love.gif",
        "https://media.tenor.com/jEqmKqupnOwAAAAd/anime-kiss.gif",
        "https://media.tenor.com/UlGZ_Q5VIGQAAAAd/beyonsatann.gif"
    ]
    random_kiss = random.choice(gif)
    author = ctx.author
    kiss_embed = discord.Embed(colour = discord.Colour.random())
    kiss_embed.add_field(name = '', value = f"{author.mention} is kissing {member.mention} 😘", inline = True)
    kiss_embed.set_thumbnail(url = random_kiss)
    await ctx.respond(embed = kiss_embed)

#Running the bot
load_dotenv
bot.run(os.getenv('TOKEN'))