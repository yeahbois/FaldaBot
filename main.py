from discord.ext import commands
import time
import discord
import json
import dotenv
import os

with open('data/config.json', 'r') as f:
    _config = json.load(f)

_prefix = ['beta ', 'Beta ']
_version = _config['version']
global _start_time
_start_time = time.time()

intents = discord.Intents.default()
intents.members = True
intents.messages = True
intents.guilds = True
intents.message_content = True

client = commands.AutoShardedBot(command_prefix=_prefix, shard_count=5, intents=intents)
client.remove_command('help')

dotenv.load_dotenv()

@client.event
async def on_ready():
    print("FaldaBot is ready!")
    print("FaldaBot Version: " + _version)

@client.event
async def on_message(message):
    if message.content == client.user.mention:
        if message.author.bot:
            return
        else:
            embed = discord.Embed(title = "Hello! 👋", description = "Im FaldaBot! A cool multipurpose discord bot. You can use `allay help` to see all my command", colour = discord.Colour.blue())
            embed.set_footer(text=f"FaldaBot {_version} | Requested by {message.author.name}", icon_url=message.author.avatar.url)
            await message.reply(embed=embed)
    await client.process_commands(message)

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title = "Command On Cooldown!", description = error, colour=discord.Colour.red())
        await ctx.send(embed=embed)
    elif isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title = "Something Missing!", description = error, colour=discord.Colour.red())
        await ctx.send(embed=embed)
    elif isinstance(error, commands.MemberNotFound):
        embed = discord.Embed(title = "Uh an error occured!", description = error, colour=discord.Colour.red())
        await ctx.send(embed=embed)
    elif isinstance(error, commands.BadArgument):
        embed = discord.Embed(title = "Uh an error occured!", description = error, colour=discord.Colour.red())
        await ctx.send(embed=embed)
    elif isinstance(error, commands.CommandInvokeError):
        embed = discord.Embed(title = "Uh an error occured!", description = error, colour=discord.Colour.red())
        await ctx.send(embed=embed)
    elif isinstance(error, commands.CommandNotFound):
        embed = discord.Embed(title = "Command Not Found!", description = error, colour=discord.Colour.red())
        await ctx.send(embed=embed)
    elif isinstance(error, commands.MissingRole):
        embed = discord.Embed(title = "Role Not Found!", description = error, colour=discord.Colour.red())
        await ctx.send(embed=embed)
    elif isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(title = "Missing Permissions!", description = error, colour = discord.Colour.red())
        await ctx.send(embed=embed)

async def runProv():
    groups = ["economy", "fun", "globalchat", "imagemanipulation", "moderation", "music", "owner", "utility"]
    for group in groups:
        await client.load_extension(f"groups.{group}")


TOKEN = os.getenv("token")
        
client.run(TOKEN)