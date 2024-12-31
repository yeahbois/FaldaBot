# Database Template #
def User(user_id:int, has_use_start: bool, blacklist:int, blacklist_reason, jail:int):
    return {
        "uid": user_id,
        "eacc": has_use_start,
        "bl": blacklist,
        "blr": blacklist_reason,
        "jld": jail,
        "stg": []
    }

def Music(user_id:int, favorite:list, playlist:list):
    return {
        "uid": user_id,
        "fav": favorite,
        "plst": playlist
    }

def Guild(guild_id:int, verify:bool, automod:list, auto_respond:list):
    return {
        "gid": guild_id,
        "vrfy": verify,
        "atm": automod,
        "atr": auto_respond
    }

def Clan(clan_id:int, name, icon, created_at, kills:int, deaths:int, owner:int, bank:int, points:int, defend:int, members:list, settings:list):
    return {
        "cid": clan_id,
        "nm": name,
        "ic": icon,
        "cat": created_at,
        "k": kills,
        "d": deaths,
        "own": owner,
        "bnk": bank,
        "pnt": points,
        "dfd": defend,
        "mbr": members,
        "stg": settings
    }

def Money(uid:int, wallet:int, bank:int, max_bank:int, energy:int, life:int, inventory:list, extra:list, cooldowns:list = []):
    return {
        "uid": uid,
        "w": wallet,
        "b": bank,
        "mb": max_bank,
        "e": energy,
        "l": life,
        "i": inventory,
        "ext": extra,
        "cd": cooldowns
    }

def Profile(uid:int, bio, badge:list, dimension, clan, allayhubName, allayhubSubs:int, allaygramName, allaygramSubs:int, swordEnch:int, axeEnch:int, pickaxeEnch:int, fishrodEnch:int, crypto:list):
    return {
        "uid": uid,
        "bio": bio,
        "bdg": badge,
        "dim": dimension,
        "cl": clan,
        "ah": {
            "nm": allayhubName,
            "sbs": allayhubSubs
        },
        "ag": {
            "nm": allaygramName,
            "fls": allaygramSubs
        },
        "ench": {
            "swd": swordEnch,
            "axe": axeEnch,
            "pcxe": pickaxeEnch,
            "fsh": fishrodEnch
        },
        "crypto": crypto
    }
# Short Text #
type = "tp"