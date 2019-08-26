from flask import Blueprint, request, render_template,session,redirect
from setting import MongoDB
user = Blueprint("user",__name__)

@user.route("/login",methods=["POST","GET"])
def login():
    if request.method == "GET":
        return  render_template("login.html")
    else:
        userinfo = request.form.to_dict()
        user_dict = MongoDB.player.find_one(userinfo)
        user_dict["_id"] = str(user_dict.get("_id"))
        session["user"] = user_dict

        return redirect("/player")



@user.route("/reg",methods=["POST","GET"])
def reg():
    if request.method == "GET":
        return render_template("reg.html")
    else:
        userinfo = request.form.to_dict()
        if userinfo.get("repassword") != userinfo.get("password"):
            return render_template("reg.html")
        else:
            userinfo.pop("repassword")
            userinfo["ATC"] = 20
            userinfo["DEF"] = 20
            userinfo["LIFE"] = 300
            userinfo["Equip"] = []
            userinfo["Package"] = [
                {"name": "大砍刀", "atc": 20,"def" :-5, "life": 0},
                {"name": "黄金甲", "atc": -5,"def" :20, "life": 200},
                {"name": "小红药", "atc": 5,"def" :0, "life": 100},
            ]

            MongoDB.player.insert_one(userinfo)

            return render_template("reg.html")