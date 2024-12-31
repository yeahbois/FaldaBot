import discord
from discord.ext import commands
import asyncio
import random
import qrcode
import string
from translate import Translator


class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['av'])
    async def avatar(self, ctx, user: discord.Member = None):
        if user == None:
            user = ctx.author
        view = discord.ui.View()
        view.add_item(discord.ui.Button(label="Download", url=user.avatar.url))
        embed = discord.Embed(colour=discord.Colour.blue())
        embed.set_author(name=f"{user.name}'s avatar", icon_url=user.avatar.url)
        embed.set_image(url=user.avatar.url)
        embed.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar.url)
        await ctx.send(embed=embed, view=view)

    @commands.command(aliases=["ce"])
    @commands.has_permissions(manage_messages=True)
    async def createembed(self, ctx, channel:discord.TextChannel = None):
        if channel == None:
            channel = ctx.channel
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        embed = discord.Embed()
        send = await ctx.send("Reply the message with your answer! Timeout = 120 second")

        try:
            delete1 = await ctx.send("Tell me the title! If you dont want a title, reply with `NONE`")
            title = await self.bot.wait_for('message', check=check, timeout=120)
        except asyncio.TimeoutError:
            return await ctx.send("You too long to reply!")

        if title.content == "NONE":
            pass
        else:
            embed.title = title.content

        try:
            delete2 = await ctx.send("Tell me the description! If you dont want a description, reply with `NONE`")
            description = await self.bot.wait_for('message', check=check, timeout = 120)
        except asyncio.TimeoutError:
            return await ctx.send("You too long to reply!")

        if description.content == "NONE":
            pass
        else:
            embed.description = description.content

        try:
            sendRequests = await ctx.send("Tell me the embed author! Enter `NONE` if you doesnt want that!")
            authorName = await self.bot.wait_for('message', check=check, timeout=120)
            await sendRequests.delete()
        except asyncio.TimeoutError:
            return await ctx.send("You too long to reply!")

        if authorName.content == "NONE":
            pass
        else:
            try:
                sendRequests2 = await ctx.send("Whats the url for the author icon? Enter `NONE` if you dont want a icon!")
                iconForAuthor = await self.bot.wait_for('message', check=check, timeout=120)
            except asyncio.TimeoutError:
                return await ctx.send("You too long to reply!")

            if iconForAuthor.content == "NONE":
                embed.set_author(name=authorName.content)
            else:
                embed.set_author(name=authorName.content, icon_url=iconForAuthor.content)
            await sendRequests2.delete()

        try:
            delete3 = await ctx.send('''
    Now tell me the colour!
    Available colour:
    `default`
    `random`
    `teal`
    `dark teal`
    `green`
    `dark green`
    `blue`
    `dark blue`
    `purple`
    `dark purple`
    `magenta`
    `dark magenta`
    `gold`
    `dark gold`
    `orange`
    `dark orange`
    `red`
    `dark red`
    `light gray`
    `dark gray`
    `darker gray`
    `lighter gray`
    `blurple`
    `greyple`
    `dark theme`
                ''')
            colour = await self.bot.wait_for('message', check=check, timeout = 120)
        except asyncio.TimeoutError:
            return await ctx.send("You too long to reply!")

        color = colour.content

        if color == "default":
            embed.colour = discord.Colour.default()
        elif color == "random":
            embed.colour = discord.Colour.random()
        elif color == "teal":
            embed.colour = discord.Colour.teal()
        elif color == "dark teal":
            embed.colour = discord.Colour.dark_teal()
        elif color == "green":
            embed.colour = discord.Colour.green()
        elif color == "dark green":
            embed.colour = discord.Colour.dark_green()
        elif color == "blue":
            embed.colour = discord.Colour.blue()
        elif color == "dark blue":
            embed.colour = discord.Colour.dark_blue()
        elif color == "purple":
            embed.colour = discord.Colour.purple()
        elif color == "dark purple":
            embed.colour = discord.Colour.dark_purple()
        elif color == "magenta":
            embed.colour = discord.Colour.magenta()
        elif color == "dark magenta":
            embed.colour = discord.Colour.dark_magenta()
        elif color == "gold":
            embed.colour = discord.Colour.gold()
        elif color == "dark gold":
            embed.colour = discord.Colour.dark_gold()
        elif color == "orange":
            embed.colour = discord.Colour.orange()
        elif color == "dark orange":
            embed.colour = discord.Colour.dark_orange()
        elif color == "red":
            embed.colour = discord.Colour.red()
        elif color == "dark red":
            embed.colour = discord.Colour.dark_red()
        elif color == "light gray":
            embed.colour = discord.Colour.light_gray()
        elif color == "dark gray":
            embed.colour = discord.Colour.dark_gray()
        elif color == "darker gray":
            embed.colour = discord.Colour.darker_gray()
        elif color == "lighter gray":
            embed.colour = discord.Colour.lighter_gray()
        elif color == "blurple":
            embed.colour = discord.Colour.blurple()
        elif color == "greyple":
            embed.colour = discord.Colour.greyple()
        elif color == "dark theme":
            embed.colour = discord.Colour.dark_theme()
        else:
            embed.colour = discord.Colour.default()
            await ctx.send("Sorry the colour is not found! I will change it to discord default colour.")

        try:
            delete4 = await ctx.send("Tell me how many field do you want for your embed! if you want a image in your embed reply with `IMAGE`")
            fieldMany = await self.bot.wait_for('message', check=check, timeout = 120)
        except asyncio.TimeoutError:
            return await ctx.send("You too long to reply!")

        if fieldMany.content == "IMAGE":
            try:
                send = await ctx.send("What the url for the image?")
                getLink = await self.bot.wait_for('message', check=check, timeout=120)
            except asyncio.TimeoutError:
                return await ctx.send("You too long to reply!")

            embed.set_image(url=getLink.content)
            await send.delete()
        else:
            for loop in range(int(fieldMany.content)):
                try:
                    deleteThis = await ctx.send("Tell me the field title!")
                    titleField = await self.bot.wait_for('message', check=check, timeout=120)
                except asyncio.TimeoutError:
                    return await ctx.send("You too long to reply!")

                try:
                    deleteThisAgain = await ctx.send("Tell me the field value!")
                    valueField = await self.bot.wait_for('message', check=check, timeout=120)
                except asyncio.TimeoutError:
                    return await ctx.send("You too long to reply!")

                await deleteThis.delete()
                await deleteThisAgain.delete()

                embed.add_field(name=titleField.content, value=valueField.content, inline=True)

        try:
            delete5 = await ctx.send("What the embed footer? If you dont want a footer, reply with `NONE`")
            footerText = await self.bot.wait_for('message', check=check, timeout=120)
        except asyncio.TimeoutError:
            return await ctx.send("You too long to reply!")

        if footerText.content == "NONE":
            pass
        else:
            try:
                delete6 = await ctx.send("Whats the embed footer's icon url? Enter `NONE` if you dont want a icon!")
                footerUrl = await self.bot.wait_for('message', check=check, timeout=120)
            except asyncio.TimeoutError:
                return await ctx.send("You too long to reply!")

            await delete6.delete()

            if footerUrl.content == "NONE":
                embed.set_footer(text=footerText.content)
            else:
                embed.set_footer(text=footerText.content, icon_url=footerUrl.content)

        try:
            thumbnail = await ctx.send("Enter a thumbnail link! Reply with `NONE` if you dont want it!")
            getThumb = await self.bot.wait_for('message', check=check, timeout=120)
        except asyncio.TimeoutError:
            return await ctx.send("You too long to reply!")

        await thumbnail.delete()

        if getThumb.content == "NONE":
            pass
        else:
            embed.set_thumbnail(url=getThumb.content)

        await ctx.send(f"Done! Look at <#{channel.id}>, an cool embed will be sended!")
        try:
            await channel.send(embed=embed)
        except discord.HTTPException as e:
            return await ctx.send(f"Uh! The embed cannot be sended! Maybe its because you're not entering the right field! Error: `{e}`")

        await delete1.delete()
        await delete2.delete()
        await delete3.delete()
        await delete4.delete()
        await delete5.delete()

    @commands.command()
    async def poll(self, ctx, *, question):
        embed = discord.Embed(title = "Polling", description = f"{ctx.author.name} started a poll", colour = discord.Colour.blue())
        embed.add_field(name = "Question:", value = question)
        msg = await ctx.send(embed=embed)
        await msg.add_reaction("👍")
        await msg.add_reaction("👎")
    # lanjut reg command sama edit beberapa di config dan commands.json

    @commands.command()
    async def passwordgenerator(self, ctx, length: int = 8):
        characters = list(string.ascii_letters + string.digits + "!@#$%^&*()")

        if length > 100:
            await ctx.reply("Error: Must be fewer than 100")
            return

        random.shuffle(characters)
        
        password = []
        for i in range(length):
            password.append(random.choice(characters))

        random.shuffle(password)

        await ctx.reply("".join(password))

    @commands.command(aliases=["cqr"])
    async def createqrcode(self, ctx, *, something):
        image = qrcode.make(something)
        image.save("caches/qrcode.png")
        await ctx.send(file = discord.File("caches/qrcode.png"))

    @commands.command()
    @commands.has_role("Giveaways")
    async def giveaway(self, ctx):
        def convert(time):
            pos = ["s","m","h","d"]
            timeDict = {"s": 1, "m": 60, "h": 3600, "d": 3600*24}
            unit = time[-1]

            if unit not in pos:
                raise(Exception("Unit Error, you must use [s|m|h|d]"))
                return
            try:
                val = int(time[:-1])
            except:
                raise(Exception("Time must be integer!"))
                return

            return val * timeDict[unit]

        await ctx.send("Answer this question within 15 second!")
        questions = ["Which channel that this giveaway will be hosted in?","Duration of the giveaway?, Example: 10s","What is the giveaway prize?", "Any requirements for the giveaway? If yes enter it!"]

        answers = []

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        for i in questions:
            await ctx.send(i)

            try:
                msg = await self.bot.wait_for('message', timeout=60.0,check=check)
            except asyncio.TimeoutError:
                await ctx.send("You late!")
                return
            else:
                answers.append(msg.content)

        try:
            c_id = int(answers[0][2:-1])
        except:
            await ctx.send(f"You didnt mention a channel correctly, do like this {ctx.channel.mention}")
            return

        channel = self.bot.get_channel(c_id)

        time = convert(answers[1])
        prize = answers[2]
        req = answers[3]

        await ctx.send(f"Giveaway will started soon in {channel.mention}, and will done in {answers[1]}")

        embed = discord.Embed(title = "Giveaway Time!", description = f"{ctx.author.name} is **giving away** **{prize}**", colour = discord.Colour.blue())
        embed.add_field(name = "Hosted By:", value = ctx.author.name)
        embed.add_field(name = "Prize:", value = prize)
        embed.add_field(name = "Requirements:", value = req)
        embed.set_author(name = ctx.author, icon_url = ctx.author.avatar.url)
        embed.set_footer(text = f"Ends {answers[1]} from now!")
        msg = await channel.send(embed = embed)
        await channel.send(f"Message ID: {msg.id}")
        await msg.add_reaction("🎉")
        await asyncio.sleep(time)

        newMsg = await channel.fetch_message(msg.id)

        users = await newMsg.reactions[0].users().flatten()
        users.pop(users.index(self.bot.user))

        try:
            winner = random.choice(users)
        except IndexError:
            return await channel.send("Giveaway ended with no winners, because no one react!")

        winnerEmbed = discord.Embed(title = "Giveaway Closed!", description = f"Giveaway that hosted by: {ctx.author.name} has closed!", colour = discord.Colour.blue())
        winnerEmbed.add_field(name = "Winner:", value = winner.mention)
        winnerEmbed.add_field(name = "Prize:", value = prize)
        await channel.send(embed=winnerEmbed)

    @commands.command()
    async def timer(self, ctx, time, *, reason):
        def convert(time):
            pos = ["s","m","h","d"]
            timeDict = {"s": 1, "m": 60, "h": 3600, "d": 3600*24}
            unit = time[-1]

            if unit not in pos:
                raise(Exception("Unit Error, you must use [s|m|h|d]"))
                return
            try:
                val = int(time[:-1])
            except:
                raise Exception("Time must be integer!")
                return

            return val * timeDict[unit]

        await ctx.send("Your timer has been set: {}".format(time))
        second = convert(time)
        await asyncio.sleep(second)

        embed = discord.Embed(title = "Time up!", colour = discord.Colour.blue())
        embed.add_field(name = "Author:", value = ctx.author.mention)
        embed.add_field(name = "Reason:", value = reason)
        embed.add_field(name = "Time:", value = "{} / {} second".format(time, second))
        embed.set_footer(text = "AllayBot Timer")
        await ctx.send(embed=embed)

        await ctx.author.send("{}!".format(reason))

    @commands.command()
    @commands.has_role("Giveaways")
    async def reroll(self, ctx, channel: discord.TextChannel, messageId:int):
        try:
            newMsg = await channel.fetch_message(messageId)
        except:
            await ctx.send("Incorrect ID!")

        users = await newMsg.reactions[0].users().flatten()
        users.pop(users.index(self.bot.user))

        try:
            newWinner = random.choice(users)
        except IndexError:
            return await channel.send("No winners found, no one react!")

        newWinnerEmbed = discord.Embed(title = "Giveaways Reroll!", description = f"{ctx.author} is rerolling his/her giveaways!", colour = discord.Colour.blue())
        newWinnerEmbed.add_field(name = "New Winner:", value = newWinner.mention)
        newWinnerEmbed.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
        await channel.send(embed=newWinnerEmbed)

    @commands.command()
    async def countdown(self, ctx, start, *, about = "Timer finished"):
        def convert(time):
            pos = ["s","m","h"]
            timeDict = {"s": 1, "m": 60, "h": 3600}
            unit = time[-1]

            if unit not in pos:
                raise(Exception("Unit Error, you must use [s|m|h]"))
                return
            try:
                val = int(time[:-1])
            except:
                raise(Exception("Time must be integer!"))
                return

            return val * timeDict[unit]

        time = convert(start)
        if time > (86400 * 2):
            return await ctx.send("Your time cannot longer than 2 days")

        message = await ctx.send(f"Countdown from {start} / {time} second will be started!")
        number = time
        while True:
            message = await message.edit(f"Timer: {number}")
            await asyncio.sleep(1)

            try:
                number-=1
            except:
                number = int(number)
                number-=1

            if number < 1:
                await ctx.send(f"{about}! {ctx.author.mention}")
                break

    @commands.command(aliases=['trans'])
    async def translate(ctx, from_lang, to_lang, *, text):
        translator = Translator(
            from_lang=from_lang, to_lang=to_lang
        )

        result = translator.translate(text)
        embed = discord.Embed(title="Translate", colour = discord.Colour.blue())
        embed.add_field(name = "Languages:", value = f"{from_lang} -> {to_lang}")
        embed.add_field(name = "Text:", value = text)
        embed.add_field(name = "Result:", value = result)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Utility(bot))