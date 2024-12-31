import discord
from discord.ext import commands

class GlobalChat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


def setup(bot):
    bot.add_cog(GlobalChat(bot))