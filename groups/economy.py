'''
AllayBot Economy Module
'''

# Imports
import discord
from discord.ext import commands, pages
import random
import asyncio
import datetime
import time
import dotenv
import os
import json
from tools import dbhelper
from tools import template
from tools import errors

with open('data/config.json') as f:
	_config = json.load(f)

# Important Functions and Variables
_as = "<:amethys_balance:924606666291433482>"

def _create_account(user: discord.Member):
	"""
	Create an account for a user
	"""
	col_usermoney = dbhelper.col_money
	col_profile = dbhelper.col_profile
	col_user = dbhelper.col_users
	insert_money = template.Money(
		user.id,
		100,
		0,
		100,
		100,
		100,
		[{'nm': 'new_player_pack', 'amt': 1}],
		[]
	)

	insert_profile = template.Profile(
		user.id,
		"I love AllayBot",
		[{'tp': 'active', 'val': 'Wooden'}, {'tp': 'inv', 'val': []}],
		"world",
		"No Clan",
		user.name,
		0,
		user.name,
		0,
		1,
		1,
		1,
		1,
		[]
	)

	Udata = col_user.find_one({'uid': user.id})
	if Udata == None:
		insert_user = template.User(
			user.id,
			True,
			0,
			"None",
			0
		)
		col_user.insert_one(insert_user)
	else:
		col_user.update_one({'uid': user.id}, {'$set': {'eacc': True}})

	col_usermoney.insert_one(insert_money)
	col_profile.insert_one(insert_profile)

def _check_account(user: discord.Member):
	"""
	Check if an account exists for a user
	"""
	col_user = dbhelper.col_users
	Udata = col_user.find_one({'uid': user.id})
	if Udata == None:
		return False
	else:
		if Udata['eacc'] == False:
			return False
		else:
			return 
			
def _add_money(user: discord.Member, amount:int, type=None):
	"""
	Add money to a user's account
	"""
	if type == None or type == "wallet":
		col_usermoney = dbhelper.col_money
		Udata = col_usermoney.find_one({'uid': user.id})
		if Udata == None:
			return False
		col_usermoney.update_one({'uid': user.id}, {'$inc': {'w': amount}})
		return True
	elif type == "bank":
		col_usermoney = dbhelper.col_money
		Udata = col_usermoney.find_one({'uid': user.id})
		if Udata == None:
			return False
		col_usermoney.update_one({'uid': user.id}, {'$inc': {'b': amount}})
		return True
	else:
		raise ValueError("Invalid type")

def _remove_money(user: discord.Member, amount:int, type=None):
	"""
	Remove money from a user's account
	"""
	if type == None or type == "wallet":
		col_usermoney = dbhelper.col_money
		Udata = col_usermoney.find_one({'uid': user.id})
		if Udata == None:
			return False
		col_usermoney.update_one({'uid': user.id}, {'$inc': {'w': -amount}})
		return True
	elif type == "bank":
		col_usermoney = dbhelper.col_money
		Udata = col_usermoney.find_one({'uid': user.id})
		if Udata == None:
			return False
		col_usermoney.update_one({'uid': user.id}, {'$inc': {'b': -amount}})
		return True
	else:
		raise ValueError("Invalid type")

def _get_money(user: discord.Member, type=None):
	"""
	Get money from a user's account
	"""
	if type == None or type == "wallet":
		col_usermoney = dbhelper.col_money
		Udata = col_usermoney.find_one({'uid': user.id})
		if Udata == None:
			return False
		return Udata['w']
	elif type == "bank":
		col_usermoney = dbhelper.col_money
		Udata = col_usermoney.find_one({'uid': user.id})
		if Udata == None:
			return False
		return Udata['b']
	else:
		raise ValueError("Invalid type")

def _check_item(user:discord.Member, item_id, amount:int):
	"""
	Check if a user has a certain amount of an item
	"""
	col = dbhelper.col_money

	res = col.find_one({'uid': user.id})
	result = next((item for item in res['i'] if item['nm'] == item_id), None)
	if result == None:
		return False
	else:
		if result['amt'] < amount:
			return False
		else:
			return True

def _check_many_item(user:discord.Member, items:list, amount:list):
	"""
	Check if a user has a certain amount of an item
	"""
	missingItem = []
	for item in items:
		checkItem = _check_item(user, item, amount[items.index(item)])
		if checkItem == False:
			missingItem.append(item)
	return missingItem

def _give_item(user:discord.Member, item_id, amount:int):
	"""
	Give a user an item
	"""
	col = dbhelper.col_money
	res = col.find_one({'uid': user.id})
	result = next((item for item in res['i'] if item['nm'] == item_id), None)
	if result == None:
		col.update_one({'uid': user.id}, {'$push': {'i': {'nm': item_id, 'amt': amount}}})
	else:
		inventory = []
		for values in res['i']:
			inventory.append(values)
		itemIndex = inventory.index(result)
		col.update_one({'uid': user.id}, {'$set': {f'i.{itemIndex}.amt': inventory[itemIndex]['amt'] + amount}})

def _remove_item(user:discord.Member, item_id, amount:int):
	"""
	Remove an item from a user's inventory
	"""
	col = dbhelper.col_money
	res = col.find_one({'uid': user.id})
	result = next((item for item in res['i'] if item['nm'] == item_id), None)
	if result == None:
		return False
	else:
		inventory = []
		for values in res['i']:
			inventory.append(values)
		itemIndex = inventory.index(result)
		if result['amt'] - amount <= 1:
			col.update_one({'uid': user.id}, {'$pull': {'i': result}})
		else:
			col.update_one({'uid': user.id}, {'$set': {f'i.{itemIndex}.amt': inventory[itemIndex]['amt'] - amount}})

def _get_crypto(crypto_name):
	"""
	Get the current price of a cryptocurrency
	"""
	cryp = dbhelper.col_setting
	res = cryp.find_one({"placeholder": 0})

	if crypto_name == "bitcoin":
		return res['crypto']['bitcoin']
	elif crypto_name == "bitcoin.status":
		return res['crypto']['bitcoin_status']
	elif crypto_name == "ethereum":
		return res['crypto']['ethereum']
	elif crypto_name == "ethereum.status":
		return res['crypto']['ethereum_status']
	elif crypto_name == "chips":
		return res['crypto']['chips']
	elif crypto_name == "chips.status":
		return res['crypto']['chips_status']
	elif crypto_name == "amethereum":
		return res['crypto']['amethereum']
	elif crypto_name == "amethereum.status":
		return res['crypto']['amethereum_status']
	else:
		raise ValueError("Wrong type!")

def _give_crypto(user:discord.Member, name, amount:int):
	"""
	Give a user a cryptocurrency
	"""
	cryp = dbhelper.col_profile
	res = cryp.find_one({'uid': user.id})
	AvailableCrypto = ["bitcoin", "ethereum", "chips", "amethereum"]
	name = name.lower()
	if name not in AvailableCrypto:
		raise ValueError("Wrong value!")
	result = next((item for item in res['crypto'] if item['nm'] == name), None)
	if result == None:
		cryp.update_one({'uid': user.id}, {'$push': {'crypto': {'nm': name, 'amt': amount}}})
	else:
		inventory = []
		for values in res['crypto']:
			inventory.append(values)
		itemIndex = inventory.index(result)
		cryp.update_one({'uid': user.id}, {'$set': {f'crypto.{itemIndex}.amt': inventory[itemIndex]['amt'] + amount}})

def _remove_crypto(user:discord.Member, name, amount:int):
	"""
	Remove a cryptocurrency from a user's inventory
	"""
	cryp = dbhelper.col_profile
	res = cryp.find_one({'uid': user.id})
	AvailableCrypto = ["bitcoin", "ethereum", "chips", "amethereum"]
	name = name.lower()
	if name not in AvailableCrypto:
		raise ValueError("Wrong value!")
	result = next((item for item in res['crypto'] if item['nm'] == name), None)
	if result == None:
		return
	else:
		if (result['amt'] - amount) <= 0:
			cryp.update_one({'uid': user.id}, {'$pull': {'crypto': result}})
		else:
			inventory = []
			for values in res['crypto']:
				inventory.append(values)
			itemIndex = inventory.index(result)
			cryp.update_one({'uid': user.id}, {'$set': {f'crypto.{itemIndex}.amt': inventory[itemIndex]['amt'] - amount}})
	
def _check_crypto(user:discord.Member, name, amount:int):
	"""
	Check if a user has a certain amount of a cryptocurrency
	"""
	crypto = dbhelper.col_profile
	cryp = crypto.find_one({
		"uid": user.id
	})
	AvailableCrypto = ["bitcoin", "ethereum", "chips", "amethereum"]
	if name not in AvailableCrypto:
		raise ValueError("Crypto not found")
	result = next((item for item in cryp['crypto'] if item['nm'] == name), None)
	if result == None:
		return False
	if result['amt'] <= amount:
		return False
	else:
		return True

def _chance(percentage:int):
	"""
	Return a True or False based on a percentage
	"""
	upgraded = percentage / 100
	if random.random() < upgraded:
		return True
	else:
		return False

def _init(user: discord.Member = None):
	"""
	Initialize a user's profile
	"""
	get_data = _check_account(user)
	if get_data == False:
		raise errors.AccountNotFound("Account not found! The account mean the user that you mention or you. Use `allay start` to create an account")

	resdb = dbhelper.col_users
	res = resdb.find_one({'uid': user.id})
	if not res['bl'] == 0:
		if res['bl'] == "perma":
			raise errors.TheAccountIsBlacklisted("You are permanent blacklist from AllayBot with reason: {}".format(res['blr']))
		else:
			if res['bl'] > time.time():
				rem = res['bl'] - time.time()
				dt = datetime.timedelta(seconds=rem)
				det = f"{dt}"
				det = det.replace(".", ":")
				newdt = det.split(":")
				for_time =  f"{newdt[0]} hours, {newdt[1]} minutes, and {newdt[2]} seconds"
				raise errors.TheAccountIsBlacklisted(f"You are blacklisted from AllayBot for {for_time} with reason {res['blr']}")
			else:
				dbhelper.col_users.update_one({'uid': user.id}, {'$set': {'bl': 0}})

def _blacklist(user: discord.Member, for_time, reason):
	"""
	Blacklist an user
	"""
	if for_time == "permanent":
		dbhelper.col_users.update_one({'uid': user.id}, {'$set': {'bl': 'perma'}})
	else:
		for_time = int(for_time)
		dbhelper.col_users.update_one({'uid': user.id}, {'$set': {'bl': time.time() + for_time}})

	dbhelper.col_users.update_one({'uid': user.id}, {'$set': {'blr': reason}})

def _get_item_data(itemid):
	with open("data/items.json", "r") as f:
		data = json.load(f)
	return data[itemid]

def _rand_item(items:list, percentage:list):
	return random.choices(items, percentage)[0]

def _cnum(number):
	try:
		number = int(number)
	except:
		return number
	return "{:,}".format(number)

# Main Bot
class Economy(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def start(self, ctx):
		if _check_account(ctx.author) == True:
			return await ctx.send("You already have an account!")
		msg = await ctx.send(embed=discord.Embed(colour=discord.Colour.blue(), description="Creating your account...."))
		await asyncio.sleep(2)
		await msg.edit(embed=discord.Embed(colour=discord.Colour.blue(), description="Account successfully created!"))
		_create_account(ctx.author)

	@commands.command(aliases=['bal'])
	async def balance(self, ctx, user: discord.Member = None):
		if user == None:
			user = ctx.author
		_init(user)
		col_usermoney = dbhelper.col_money
		data = col_usermoney.find_one({"uid": user.id})
		embed = discord.Embed(colour = discord.Colour.blue())
		embed.set_author(name = f"{user.name}'s balance", icon_url = user.avatar.url)
		embed.add_field(name = "Wallet:", value = f"{_cnum(data['w'])} $amethys$")
		embed.add_field(name = "Piggy Bank:", value = f"{_cnum(data['b'])}) / {_cnum(data['mb'])}) $amethys$")
		embed.add_field(name = "Total:", value = f"{_cnum(data['w'] + data['b'])} $amethys$")
		embed.set_footer(text = f"Requested by {ctx.author.name}", icon_url = ctx.author.avatar.url)
		await ctx.send(embed=embed)

	@commands.command(aliases=['pf'])
	async def profile(self, ctx, user: discord.Member = None):
		if user == None:
			user = ctx.author
		_init(user)
		col_profile = dbhelper.col_profile
		col_money = dbhelper.col_money

		money = col_money.find_one({"uid": user.id})
		res = col_profile.find_one({"uid": user.id})
		if res['dim'] == "world":
			user_dimension = "World"
		elif res['dim'] == "nether":
			user_dimension = "Nether"
		elif res['dim'] == "end":
			user_dimension = "End"
		elif res['dim'] == "allayland":
			user_dimension = "AllayLand"
		else:
			user_dimension = "World"

		clane = dbhelper.col_clans.find_one({'cid': res['cl']})
		if clane == None:
			user_clan = "No Clan"
		else:
			user_clan = clane['nm']
		embed = discord.Embed(description = f"Bio: {res['bio']}",colour = discord.Colour.blue())
		embed.set_author(name = f"{user.name}'s profile", icon_url = user.avatar.url)
		embed.add_field(name = "Stats:", value = f'''
Wallet: {_cnum(money['w'])} $amethys$
Piggy Bank: {_cnum(money['b'])} / {_cnum(money['mb'])} $amethys$
Total: {_cnum(money['w'] + money['b'])}
Energy: {money['e']}
Life: {money['l']}
Dimension: {user_dimension}
Clan: {user_clan}
			''')
		acBadge = next((badge for badge in res['bdg'] if badge['tp'] == "active"), "Wooden")
		embed.add_field(name = "Active Badge:", value = acBadge['val'])
		embed.add_field(name = "AllayHub:", value = f'''
Name: {res["ah"]["nm"]}
Subscriber: {_cnum(res["ah"]["sbs"])}
			''')
		embed.add_field(name = "AllayGram:", value = f'''
Name: {res["ag"]["nm"]}
Follower: {_cnum(res["ag"]["fls"])}
			''')
		embed.add_field(name = "Enchantments:", value = f'''
Sword: {res['ench']['swd']}
Axe: {res['ench']['axe']}
Pickaxe: {res['ench']['pcxe']}
Fishing Rod: {res['ench']['fsh']}
			''')
		embed.set_footer(text = f"Requested by {ctx.author.name}", icon_url = ctx.author.avatar.url)
		await ctx.send(embed=embed)


def setup(bot):
	bot.add_cog(Economy(bot))