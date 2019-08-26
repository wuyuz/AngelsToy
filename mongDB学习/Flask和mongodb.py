from flask import Flask, request, render_template
from .setting import MongoDB
app = Flask(__name__)

@app.route("/reg",methods=["gEt","pOSt"])
def reg():
   if request.method == "GET":
       return render_template("reg.html")
   else:
       # username = request.form.get("username")
       # MongoDB.users.insert_one({"username":username})

       user_info = request.form.to_dict() #将用户信息转换成字典
       MongoDB.users.insert_one(user_info)  #插入一条数据

       return "注册成功"


@app.route("/login",methods=["gEt","pOSt"])
def login():
   if request.method == "GET":
       return render_template("login.html")
   else:
       res = MongoDB.users.find_one(request.form.to_dict()) #查找数据
       if res:
           return f"登陆成功 {res.get('username')}"
       else:
           return "用户名密码错误"

if __name__ == '__main__':
    app.run("0.0.0.0",9527)