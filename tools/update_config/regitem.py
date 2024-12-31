import json

with open("cogs/helper/items.json", "r") as f:
    DATA = json.load(f)

while True:
    print("=== Item Registering ===")
    key = []
    for keys in DATA.keys():
        key.append(keys)
    _id = len(key) + 1
    _title = input("Enter the item's title")
    counter = 0
    while True:
        name = _title.replace(" ", "_")
        _name = name.lower()
        if counter > 1000:
            break
        counter+=1
    _desc = input("Enter the item's description")
    _rarity = input("Enter the item's rarity")
    if _rarity == "":
        _rarity = "Common"
    _chance = input("Enter the chance")
    _emoji = input("Enter the item's emoji")
    if _emoji == "":
        _emoji = "0"
    _buyprice = input("Enter the buy price")
    _sellprice = input("Enter the sell price")
    if _buyprice == "":
        _buyprice = "Cannot Buy"
    if _sellprice == "":
        _sellprice = "Cannot Sell"
    if _buyprice != "Cannot Buy":
        _buyprice = int(_buyprice)
    if _sellprice != "Cannot Sell":
        _sellprice = int(_sellprice)
    _group = input("Enter the item's group")
    _type = input("Enter the item's type")
    with open('cogs/helper/items.json', 'r') as file:
        theData = json.load(file)
        theData[_name] = {
            "name": _name,
            "title": _title,
            "description": _desc,
            "rarity": _rarity,
            "chance": _chance,
            "emoji": _emoji,
            "buy_price": _buyprice,
            "sell_price": _sellprice,
            "group": _group,
            "type": _type
        }
    with open('cogs/helper/config.json', 'r') as config:
        configData = json.load(config)
        configData['items'].append(_name)
    with open('cogs/helper/items.json', 'w') as write:
        json.dump(theData, write, indent=4)
    with open('cogs/helper/config.json', 'w') as configFile:
        json.dump(configData, configFile, indent=4)
    print("Done!")