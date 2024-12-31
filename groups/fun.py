import discord
import random
import requests
import asyncio
import akinator as ak
import string
import pyfiglet
from urllib.parse import urlencode, quote_plus
import os
from discord.ext import commands
from tools import dbhelper
from typing import List

def get_key():
    col = dbhelper.col_setting
    result = col.find_one({'placeholder': 0})
    return result['api_key']

class TicTacToeButton(discord.ui.Button["TicTacToe"]):
    def __init__(self, x: int, y: int, xPlayer: discord.Member, oPlayer: discord.Member):
        super().__init__(style=discord.ButtonStyle.secondary, label="\u200b", row=y)
        self.x = x
        self.y = y
        self.xPlayer = xPlayer
        self.oPlayer = oPlayer

    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        view: TicTacToe = self.view
        state = view.board[self.y][self.x]
        if state in (view.X, view.O):
            return

        if view.current_player == view.X:
            if interaction.user != self.xPlayer:
                return await interaction.response.send_message("Its not for you", ephemeral=True)
            self.style = discord.ButtonStyle.danger
            self.label = "X"
            view.board[self.y][self.x] = view.X
            view.current_player = view.O
            content = "It is now O's turn"
        else:
            if interaction.user != self.oPlayer:
                return await interaction.response.send_message("Its not for you", ephemeral=True)
            self.style = discord.ButtonStyle.success
            self.label = "O"
            view.board[self.y][self.x] = view.O
            view.current_player = view.X
            content = "It is now X's turn"

        self.disabled = True
        winner = view.check_board_winner()
        if winner is not None:
            if winner == view.X:
                content = "X won!"
            elif winner == view.O:
                content = "O won!"
            else:
                content = "It's a tie!"

            for child in view.children:
                child.disabled = True

            view.stop()
        textToEdit = f"Tic tac toe!\n{self.xPlayer.mention} as X\n{self.oPlayer.mention} as O\n{content}"
        await interaction.response.edit_message(content=textToEdit, view=view)

class TicTacToe(discord.ui.View):
    children: List[TicTacToeButton]
    X = -1
    O = 1
    Tie = 2

    def __init__(self, xPlayer: discord.Member, oPlayer: discord.Member):
        super().__init__()
        self.x_player = xPlayer
        self.o_player = oPlayer
        self.current_player = self.X
        self.board = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]

        for x in range(3):
            for y in range(3):
                self.add_item(TicTacToeButton(x, y, self.x_player, self.o_player))

    def check_board_winner(self):
        for across in self.board:
            value = sum(across)
            if value == 3:
                return self.O
            elif value == -3:
                return self.X

        for line in range(3):
            value = self.board[0][line] + self.board[1][line] + self.board[2][line]
            if value == -3:
                return self.X

            elif value == 3:
                return self.O
        diag = self.board[0][2] + self.board[1][1] + self.board[2][0]
        if diag == 3:
            return self.O
        elif diag == -3:
            return self.X

        diag = self.board[0][0] + self.board[1][1] + self.board[2][2]
        if diag == -3:
            return self.X

        elif diag == 3:
            return self.O
        if all(i != 0 for row in self.board for i in row):
            return self.Tie

        return None

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["hi"])
    async def hello(self, ctx):
        answer = ["Hello!!!",
                "Hiii!",
                "Hello, how are you?",
                "Good morning!",
                "Good afternoon!",
                "Good evening!",
                "Good night!"]

        await ctx.send(random.choice(answer))

    @commands.command(aliases=["IHATE"])
    async def ihate(self, ctx, *, whoyouhate):
        await ctx.send(f"Same!! I hate {whoyouhate} too! :middle_finger:")

    @commands.command(aliases=['repeat'])
    async def send(self, ctx, *, message):
        await ctx.message.delete()
        await ctx.send(f"{message}\n\n - {ctx.author}")

    @commands.command()
    @commands.cooldown(1, 100, commands.BucketType.user)
    @commands.has_role("ServerBrokener")
    async def spam(self, ctx, amount:int, *, text):
        if amount > 100:
            return await ctx.send("Cannot larger than 100")

        class ConfirmSpam(discord.ui.View):
            def __init__(self):
                super().__init__()
                self.value = None

            @discord.ui.button(label="Confirm", style=discord.ButtonStyle.green)
            async def confirm_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
                if interaction.user.id != ctx.author.id:
                    return await interaction.response.send_message("This button is not for you!", ephemeral=True)
                await interaction.response.send_message("Confirming", ephemeral=True)
                self.value = True
                self.stop()

            @discord.ui.button(label="Cancel", style=discord.ButtonStyle.grey)
            async def cancel_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
                if interaction.user.id != ctx.author.id:
                    return await interaction.response.send_message("This button is not for you!", ephemeral=True)
                await interaction.response.send_message("Cancelling", ephemeral=True)
                self.value = False
                self.stop()

        confirm = ConfirmSpam()
        await ctx.send("Are you sure? This will spam the channel for {} messages".format(amount), view=confirm)
        await confirm.wait()
        if confirm.value is None:
            return await ctx.send("Timeout..")
        elif confirm.value:
            for spam in range(amount):
                await ctx.send(text + f" \n - {ctx.author.name}")
        else:
            return await ctx.send("Cancelled..")

        await ctx.send("Done")

    @commands.command()
    async def meme(self, ctx):
        choice = random.choice(["herokuMemeApi", "someRandomApi"])
        if choice == "herokuMemeApi":
            memeApi = requests.get('https://meme-api.herokuapp.com/gimme')
            memeData = memeApi.json()

            memeUrl = memeData['url']
            memeName = memeData['title']
            memePoster = memeData['author']
            memeSub = memeData['subreddit']
            memeLink = memeData['postLink']

            embed = discord.Embed(title = memeName, description = f"Meme by: {memePoster} | in: {memeSub}", url = memeLink, colour=discord.Colour.blue())
            embed.set_image(url = memeUrl)
            embed.set_footer(text = "Powered by: reddit.com")
            await ctx.send(embed = embed)
        elif choice == "someRandomApi":
            get = requests.get("https://some-random-api.ml/meme")
            getJson = get.json()

            em = discord.Embed(title = f"Meme #{getJson['id']}", description = getJson['caption'], colour = discord.Colour.blue())
            em.set_image(url = getJson['image'])
            em.set_footer(text = "Powered by: some-random-api.ml")
            await ctx.send(embed=em)

    @commands.command()
    async def ratethisbot(self, ctx, rate:int=10):
        if rate > 10:
            return await ctx.send("Wow! Thats too much, i only accept integer less than 10!")
        elif rate < 1:
            return await ctx.send("I only accept integer bigger than 1!")
        elif rate > 8:
            return await ctx.send("Thank youuu!!!")
        elif rate < 5:
            return await ctx.send(":(, if you have any bug or suggestion use `allay bot [ suggest | report ]` command!")
        
        await ctx.send("Thank you for rate!")

    @commands.command(aliases=['rps'])
    async def rockpaperscissors(self, ctx):
        class RPSView(discord.ui.View):
            def __init__(self):
                super().__init__()
                self.value = None

            @discord.ui.button(label="Rock", style=discord.ButtonStyle.green)
            async def rock_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
                if interaction.user.id != ctx.author.id:
                    return await interaction.response.send_message("This button is not for you!", ephemeral=True)
                await interaction.response.send_message("Rock", ephemeral=True)
                self.value = "rock"
                self.stop()
            
            @discord.ui.button(label="Paper", style=discord.ButtonStyle.green)
            async def paper_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
                if interaction.user.id != ctx.author.id:
                    return await interaction.response.send_message("This button is not for you!", ephemeral=True)
                await interaction.response.send_message("Paper", ephemeral=True)
                self.value = "paper"
                self.stop()

            @discord.ui.button(label="Scissors", style=discord.ButtonStyle.green)
            async def scissors_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
                if interaction.user.id != ctx.author.id:
                    return await interaction.response.send_message("This button is not for you!", ephemeral=True)
                await interaction.response.send_message("Scissors", ephemeral=True)
                self.value = "scrissors"
                self.stop()

        rps = RPSView()
        choices = ["rock", "paper", "scrissors"]
        computers_answer = random.choice(choices)
        msg = await ctx.send("Choose your weapon!", view=rps)
        await rps.wait()
        answer = rps.value
        if rps.value is None:
            return await ctx.send("Timeout..")
        if computers_answer == answer:
            await msg.edit(f'Tie! Me and you choose {computers_answer}')
        if computers_answer == "rock":
            if answer == "paper":
                await msg.edit(f"You win! i choose {computers_answer} and you choose {answer}!")
        if computers_answer == "paper":
            if answer == "rock":
                await msg.edit(f"You lost! i choose {computers_answer} and you choose {answer}!")
        if computers_answer == "scrissors":
            if answer == "rock":
                await msg.edit(f"You win! i choose {computers_answer} and you choose {answer}!")
        if computers_answer == "rock":
            if answer == "scrissors":
                await msg.edit(f"You lost! i choose {computers_answer} and you choose {answer}!")
        if computers_answer == "paper":
            if answer == "scrissors":
                await msg.edit(f"You win! i choose {computers_answer} and you choose {answer}!")
        if computers_answer == "scrissors":
            if answer == "paper":
                await msg.edit(f"You lost! i choose {computers_answer} and you choose {answer}!")

    @commands.command(aliases=['emojify', 'tte'])
    async def texttoemoji(self, ctx, *, text):
        emojis = []
        for s in text.lower():
            if s.isdecimal():
                num2emo = {'0':'zero','1':'one','2':'two',
                        '3':'three','4':'four','5':'five',
                        '6':'six','7':'seven','8':'eight','9':'nine'}
                emojis.append(f':{num2emo.get(s)}:')
            elif s.isalpha():
                emojis.append(f':regional_indicator_{s}:')
            else:
                emojis.append(s)
        await ctx.send(''.join(emojis))
        await ctx.send(f"Copy: `{''.join(emojis)}`")

    @commands.command(aliases=['dm'])
    async def tell(self, ctx, member:discord.Member, invisible = "normal"):
        def check(m):
            return m.author.id == ctx.author.id

        if invisible.lower() == "invisible":
            await ctx.send("What did you want to tell {}?".format(member.name))
            message = await self.bot.wait_for("message", check=check)
            msg = await ctx.send(f'Telling {member.name} now!')
            await asyncio.sleep(2)
            await msg.delete()
            embed = discord.Embed(colour = discord.Colour.blue())
            embed.set_author(name = "Direct Message Send")
            embed.add_field(name = "Sender:", value = "Invisible")
            embed.add_field(name = "Sended From:", value = "Invisible")
            embed.add_field(name = "Message:", value = message.content)
            embed.set_footer(text = ctx.author.id)
            await member.send(embed = embed)
        else:
            await ctx.send("What did you want to tell {}?".format(member.name))
            message2 = await self.bot.wait_for("message", check=check)
            msge = await ctx.send(f'Telling {member.name} now')
            await asyncio.sleep(2)
            await msge.delete()
            embede = discord.Embed(colour = discord.Colour.blue())
            embede.set_author(name = "Direct Message Send")
            embede.add_field(name = "Sender:", value = ctx.author.name)
            embede.add_field(name = "Sended From:", value = ctx.message.guild.name)
            embede.add_field(name = "Message:", value = message2.content)
            embede.set_footer(text = ctx.author.id)
        
            await member.send(embed=embede)

    @commands.command(aliases=['randnum'])
    async def randomnumber(self, ctx, number1: int = 0, number2: int = 100):
        r = random.randint(int(number1), int(number2))
        await ctx.reply("Random number from {} to {} is **{}**".format(number1. number2, r))

    @commands.command(aliases=["ss"])
    async def screenshot(self, ctx, url="https://google.com", fullpage="false", width:int=1920, height:int=1080):
        msg = await ctx.send("Loading....")
        key = os.getenv('ssapikey')
        params = urlencode(dict(access_key=key,
                            url=url,
                            format = "png",
                            fullpage = fullpage,
                            no_cookie_banners="true",
                            accept_language="en",
                            response_type="json",
                            delay=3))
        req = requests.get("https://api.apiflash.com/v1/urltoimage?" + params)
        js = req.json()
        embed = discord.Embed(title = "Screenshot!", description=f'''
**Settings**
Fullpage: {fullpage} (true / false)
Width: {width}
Height: {height}
**Syntax**
`allay screenshot <url> <fullpage[true / false] OPTIONAL> <width OPTIONAL> <height OPTIONAL>`
            ''', colour=discord.Colour.blue())
        embed.set_image(url=js['url'])
        await ctx.send(embed=embed)
        await msg.delete()

    @commands.command(aliases=["8ball", "ask"])
    async def eightball(self, ctx, *, question):
        responses = ["no",
                    "i say no",
                    "of course no",
                    "maybe no",
                    "yesn't",
                    "idk",
                    "ask again later",
                    "i dont know ._.",
                    "yes",
                    "yezz",
                    "of couse yes",
                    "i say yes",
                    "YESSSS",
                    "its true",
                    "n o n o n o",
                    "my answer is yes",
                    "yes bro",
                    "Y \n E \n S"]

        await ctx.send(f"Question: {question}\nAnswer: {random.choice(responses)}")

    @commands.command()
    async def gaymeter(self, ctx, *, member = None):
        if member == None:
            member = ctx.author.name
        await ctx.send(f"{member} are {random.randint(0, 100)}% gay")

    @commands.command()
    async def smartmeter(self, ctx, *, member = None):
        if member == None:
            member = ctx.author.name
        await ctx.send(f"{member} are {random.randint(0, 100)}% smart")

    @commands.command()
    async def shortmeter(self, ctx, *, member = None):
        if member == None:
            member = ctx.author.name
        await ctx.send(f"{member} are {random.randint(0,100)}% short")

    @commands.command(aliases=['ng'])
    async def nitrogenerator(self, ctx, repeat:int = 1):
        await ctx.message.delete()

        if repeat > 5:
            return await ctx.send("Wow wow you cannot repeat it to bigger than 5 you a son of king!")

        for loop in range(repeat):
            characters = list(string.ascii_letters + string.digits)
            random.shuffle(characters)
            
            link = []
            for i in range(24):
                link.append(random.choice(characters))

            random.shuffle(link)

            newLink = "".join(link)

            msg = await ctx.send(f"discord.gift/{newLink}")
            await asyncio.sleep(5)
            await msg.delete()

    @commands.command(aliases=["aki"])
    async def akinator(self, ctx, language="en", child_mode = "false"):
        if child_mode == "true":
            child_mode = True
        else:
            child_mode = False
        if language.lower() == "list":
            return await ctx.send('''
    en: English (default)
    en_animals: English server for guessing animals. Here, Akinator will attempt to guess the animal you're thinking instead of a character
    en_objects: English server for guessing objects. Here, Akinator will attempt to guess the object you're thinking instead of a character
    ar: Arabic
    cn: Chinese
    de: German
    de_animals: German server for guessing animals
    es: Spanish
    es_animals: Spanish server for guessing animals
    fr: French
    fr_animals: French server for guessing animals
    fr_objects: French server for guessing objects
    il: Hebrew
    it: Italian
    it_animals: Italian server for guessing animals
    jp: Japanese
    jp_animals: Japanese server for guessing animals
    kr: Korean
    nl: Dutch
    pl: Polish
    pt: Portuguese
    ru: Russian
    tr: Turkish
    id: Indonesian
                ''')

        await ctx.send("Akinator is here!")
        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel and msg.content.lower() in ["y","n","p","b","e"]

        try:
            aki = ak.Akinator()
            q = aki.start_game(language=language, child_mode=child_mode)
            while aki.progression <= 80:
                embed = discord.Embed(title = "Akinator!", description = "Reply this question with ['y','n','p','b','e']", colour = discord.Colour.blue())
                embed.add_field(name = "Question:", value = q)
                embed.add_field(name = "Author:", value = ctx.author.mention)
                embed.add_field(name = "Try Akinator on web:", value = "[Click me!](https://akinator.com)")
                embed.set_footer(text = f"Requested by {ctx.author.name}")
                await ctx.send(embed=embed)
                try:
                    msg = await self.bot.wait_for("message", check=check, timeout=60.0)
                except asyncio.TimeoutError:
                    return await ctx.send("You too long to reply")
                if msg.content.lower() == "b":
                    try:
                        q=aki.back()
                    except ak.CantGoBackAnyFurther:
                        await ctx.send("You cannot back again!")
                        continue
                elif msg.content.lower() == "e":
                    return await ctx.send("Ok! Resetting the game!")
                else:
                    try:
                        q = aki.answer(msg.content.lower())
                    except ak.InvalidAnswerError as e:
                        await ctx.send("Invalid answer! use ['y','n','p','idk','pn','b','e']")
                        continue

            aki.win()
            embede = discord.Embed(title=f"It is **{aki.first_guess['name']}**", description = aki.first_guess['description'], colour=discord.Colour.blue())
            embede.set_image(url=aki.first_guess['absolute_picture_path'])
            embede.set_footer(text="AllayBot Akinator")
            await ctx.send(embed=embede)

        except ak.InvalidLanguageError:
            await ctx.send(f"Invalid language use `allay akinator list` for language list!")

    @commands.command()
    async def asciiart(self, ctx, *, text):
        result = pyfiglet.figlet_format(text)
        await ctx.send(f'''
    ```
    {result}
    ```
            ''')

    @commands.command()
    async def joke(self, ctx):
        get = requests.get("https://some-random-api.ml/joke")
        js = get.json()

        await ctx.send(js['joke'])

    @commands.command(aliases=["cb"])
    async def chatbot(self, ctx, *, message):
        apikey = get_key()
        try:
            req = requests.get("https://some-random-api.ml/chatbot?message={}&key={}".format(message, apikey))
            js = req.json()
            embed = discord.Embed(colour = discord.Colour.blue())
            embed.set_author(name = f"{ctx.author.name}'s Chat Bot", icon_url = ctx.author.avatar_url)
            embed.add_field(name = "Question:", value = message)
            embed.add_field(name = "Answer:", value = js['response'])
            embed.set_footer(text = "Powered by: some-random-api.ml")
            await ctx.send(embed=embed)
        except:
            channel = self.bot.get_channel(919438128765349898)
            send = discord.Embed(title = "A player found a bug!", description = f"{ctx.author} found a bug!", colour = discord.Colour.blue())
            send.add_field(name = "Player's ID:", value = ctx.author.id)
            send.add_field(name = "Bug:", value = f"Error: {js['error']}")
            msg = await channel.send(embed=send)
            await channel.send(f"Full JSON: {js}")
            await msg.add_reaction("⬆️")
            await msg.add_reaction("⬇️")
            await ctx.send("An error occured! The error has been sended to AllayBot developer to be fixed")

    @commands.command()
    async def custommeter(self, ctx, user = None, *, meter):
        if user == None:
            user = ctx.author.name
        await ctx.send(f"{user} are {random.randint(1, 100)}% {meter}")

    @commands.command()
    async def react(self, ctx, channel:discord.TextChannel, message:int, *, text):
        emojis = []
        for s in text.lower():
            strtoemo = {
                "a": "🇦",
                "b": "🇧",
                "c": "🇨",
                "d": "🇩",
                "e": "🇪",
                "f": "🇫",
                "g": "🇬", "h": "🇭", "i": "🇮", "j": "🇯",
                "k": "🇰", "l": "🇱", "m": "🇲", "n": "🇳",
                "o": "🇴", "p": "🇵", "q": "🇶", "r": "🇷",
                "s": "🇸", "t": "🇹", "u": "🇺", "v": "🇻",
                "w": "🇼", "x": "🇽", "y": "🇾", "z": "🇿"
            }
            if s.isdecimal():
                num2emo = {'0':'0️⃣','1':'1️⃣','2':'2️⃣',
                        '3':'3️⃣','4':'4️⃣','5':'5️⃣',
                        '6':'6️⃣','7':'7️⃣','8':'8️⃣','9':'9️⃣'}
                emojis.append(num2emo.get(s))
            elif s.isalpha():
                emojis.append(strtoemo.get(s))
            else:
                emojis.append(s)
        for emoji in emojis:
            msg = await channel.fetch_message(message)
            try:
                await msg.add_reaction(emoji)
            except discord.HTTPException as e:
                return await ctx.send(f"Uh an error occured! Error: `{e}`")

        msg = await ctx.send(f"Done add reaction on <#{channel.id}>")
        await asyncio.sleep(15)
        await msg.delete()

    @commands.command(aliases=['ttt'])
    async def tictactoe(self, ctx, user: discord.Member):
        if user == ctx.author:
            return await ctx.send("You cant play tictactoe alone!")
        if user.bot:
            return await ctx.send("You cant play tictactoe with bot!")
        choose = random.randint(0, 1)
        if choose == 0:
            firstPlayer = user
        else:
            firstPlayer = ctx.author
        await ctx.send(f"Tic tac toe!\n{ctx.author.mention} as X\n{user.mention} as O\nX goes first", view=TicTacToe(ctx.author, user))


def setup(bot):
    bot.add_cog(Fun(bot))