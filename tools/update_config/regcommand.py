import json


while True:
    print("==== Command Registering ====")
    _name = input("Enter the command's name >> ")
    for loopForClearingName in range(1000):
        c = _name.replace(" ", "_")
        _clearName = c.lower()
    _usage = input("Enter the command usage >> ")
    _aliases = []
    while True:
        getAliases = input(f"Enter an aliases >> ")
        if getAliases == "":
            break
        _aliases.append(getAliases)
    _is_premium = input("Is the command must be premium? >> ")
    if _is_premium.lower() == "false":
        _is_premium = False
    elif _is_premium == "":
        _is_premium = False
    elif _is_premium.lower() == "true":
        _is_premium = True
    else:
        raise ValueError("Wrong value! true or false")
    while True:
        _permissions = []
        getPerm = input("Enter a permission, enter ecomem for economy member >> ")
        if getPerm == "":
            break
        if getPerm == "BREAK":
            break
        if getPerm == "ecomem":
            _permissions.append("ECONOMY_MEMBER")
        _permissions.append(getPerm)
    _description = input("Enter the command description >> ")
    _version_added = input("Version added, enter now to enter the newest version >> ")
    if _version_added == "now":
        with open("../../data/config.json", "r") as f:
            config = json.load(f)
            _version_added = config['version']
    _group = input("What is the command group? >> ")
    _cooldown = input("Enter the command cooldown >> ")
    with open("../../data/commands.json", "r") as file:
        data = json.load(file)
        data[_clearName] = {
            "name": _name,
            "clear_name": _clearName,
            "usage": _usage,
            "aliases": _aliases,
            "is_premium": _is_premium,
            "permissions": _permissions,
            "description": _description,
            "version_added": _version_added,
            "group": _group,
            "cooldowns": _cooldown
        }
        with open("../../data/commands.json", "w") as toWrite:
            json.dump(data, toWrite, indent=4)
        with open("../../data/config.json", "r") as readConfig:
            CONFIGDATA_ = json.load(readConfig)
        CONFIGDATA_['commands'][_group].append(_clearName)
        with open("../../data/config.json", "w") as writeConfig:
            json.dump(CONFIGDATA_, writeConfig, indent=4)
        print("Done!")