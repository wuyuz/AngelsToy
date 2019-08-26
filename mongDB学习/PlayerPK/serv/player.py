import random

from bson import ObjectId
from flask import Blueprint, request, render_template, session, redirect
from setting import MongoDB
player = Blueprint("player",__name__)

@player.route("/player",methods=["POST","GET"])
def players():
    user_info = session.get("user")
    user_info = MongoDB.player.find_one({"_id":ObjectId(user_info.get("_id"))})
    killer = MongoDB.player.find({"_id":{"$ne":ObjectId(user_info.get("_id"))}})
    return render_template("player.html",player=user_info,killer=killer)


@player.route("/set_equip/<equip_name>/<player_id>",methods=["POST","GET"])
def set_equip(equip_name,player_id):
    user_info = MongoDB.player.find_one({"_id":ObjectId(player_id)})
    for item in user_info.get("Package"):
        if item.get("name") == equip_name:
            user_info["Package"].remove(item)
            user_info["Equip"].append(item)

            user_info["ATC"] += item.get("atc")
            user_info["DEF"] += item.get("def")
            user_info["LIFE"] += item.get("life")

            break

    MongoDB.player.update_one({"_id":ObjectId(player_id)},{"$set":user_info})

    return redirect("/player")


@player.route("/unset_equip/<equip_name>/<player_id>",methods=["POST","GET"])
def unset_equip(equip_name,player_id):
    user_info = MongoDB.player.find_one({"_id":ObjectId(player_id)})
    for item in user_info.get("Equip"):
        if item.get("name") == equip_name:
            user_info["Equip"].remove(item)
            user_info["Package"].append(item)

            user_info["ATC"] -= item.get("atc")
            user_info["DEF"] -= item.get("def")
            user_info["LIFE"] -= item.get("life")

            break

    MongoDB.player.update_one({"_id": ObjectId(player_id)}, {"$set": user_info})

    return redirect("/player")


@player.route("/skill/<killer_id>",methods=["POST","GET"])
def skill(killer_id):
    killer_info = MongoDB.player.find_one({"_id":ObjectId(killer_id)})
    killer_name = killer_info.get("nickname")
    player_info = MongoDB.player.find_one({"_id":ObjectId(session["user"].get("_id"))})
    player_name = player_info.get("nickname")

    pk_log = {
        "player_list":[killer_id,session["user"].get("_id")],
        "player_log":[]
    }


    while 1:
        cut_life = int(player_info.get("ATC") *random.uniform(0,2) - killer_info.get("DEF") * random.uniform(0,1.5))
        p_k = {
            "player1":player_name,
            "player2":killer_name
        }
        if cut_life > 0:
            killer_info["LIFE"] -= cut_life
            p_k["log"] = f"{player_name} ATC {killer_name} , {killer_name} LIEF -{cut_life} , {killer_name} LIFE = {killer_info['LIFE']}"
            pk_log["player_log"].append(p_k)

            if killer_info.get("LIFE") <= 0:
                res = MongoDB.PKLog.insert_one(pk_log)
                return redirect(f"/lishi/{res.inserted_id}")
        else:
            p_k["log"] = f"{player_name} ATC {killer_name} , {killer_name} LIEF {cut_life}, {killer_name} LIFE = {killer_info['LIFE']}"
            pk_log["player_log"].append(p_k)

        cut_life_player = int(killer_info.get("ATC") * random.uniform(0, 2) - player_info.get("DEF") * random.uniform(0, 1.5))
        k_p = {
            "player1":killer_name,
            "player2":player_name
        }
        if cut_life_player > 0:
            player_info["LIFE"] -= cut_life_player
            k_p["log"] = f"{killer_name} ATC {player_name} , {player_name} LIEF -{cut_life_player} , {player_name} LIFE = {player_info['LIFE']}"
            pk_log["player_log"].append(k_p)

            if player_info.get("LIFE") <= 0:
                res = MongoDB.PKLog.insert_one(pk_log)
                return redirect(f"/lishi/{res.inserted_id}")

        else:
            k_p["log"] = f"{killer_name} ATC {player_name} , {player_name} LIEF {cut_life_player} , {player_name} LIFE = {player_info['LIFE']}"
            pk_log["player_log"].append(k_p)




@player.route("/lishi/<hid>")
def lishi(hid):
    h = MongoDB.PKLog.find_one({"_id":ObjectId(hid)})

    return render_template("h.html",h=h,winner = h.get("player_log")[-1].get("player1"))



# @user.route("/reg",methods=["POST","GET"])
# def reg():
#     if request.method == "GET":
#         return render_template("reg.html")
#     else:
#         userinfo = request.form.to_dict()
#         if userinfo.get("repassword") != userinfo.get("password"):
#             return render_template("reg.html")
#         else:
#             userinfo.pop("repassword")
#             userinfo["ATC"] = 20
#             userinfo["DEF"] = 20
#             userinfo["LIFE"] = 20
#             userinfo["Equip"] = []
#             userinfo["Package"] = [
#                 {"name": "大砍刀", "atc": 20,"def" :-5, "life": 0},
#                 {"name": "黄金甲", "atc": -5,"def" :20, "life": 200},
#                 {"name": "小红药", "atc": 5,"def" :0, "life": 100},
#             ]
#
#             MongoDB.player.insert_one(userinfo)
#
#             return render_template("reg.html")