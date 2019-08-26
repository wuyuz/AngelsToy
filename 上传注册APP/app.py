from flask import Flask,request,jsonify,send_file
from pymongo import MongoClient

MC = MongoClient("127.0.0.1",27017)
MongoDB = MC['MyApp']

app = Flask(__name__)
app.debug = True

@app.route("/reg",methods=['post'])
def reg():
    user_info = request.form.to_dict()
    MongoDB.usertest.insert_one(user_info)
    print(user_info)

    return jsonify({"code":0,'msg':'注册成功'})

@app.route("/login",methods=['post'])
def login():
    user_info = request.form.to_dict()
    user_dict = MongoDB.usertest.find_one(user_info)
    print(user_info)
    if user_dict:
        return jsonify({"code":0,'msg':'登陆成功'})
    else:
        return jsonify({"code":1,'msg':'登陆失败'})

@app.route("/uploader",methods=['post'])
def uploader():
    file = request.files.get('my_tt')
    print(file)  #<FileStorage: '1565714967245.jpg' ('image/jpeg')> 里面有filename属性
    file.save(file.filename)

    ret = {
        "code":0,
        "filename":file.filename,
        "msg":"上传成功"
    }
    return jsonify(ret)

@app.route('/get_avatar/<tt_name>',methods=["GET"])
def get_tt(tt_name):
    return send_file(tt_name)

if __name__ == "__main__":
    app.__call__
    app.run("0.0.0.0",9527)