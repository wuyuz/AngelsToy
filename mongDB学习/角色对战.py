
from pymongo import MongoClient
from setting import MongoDB
from flask import Flask,request, render_template,g,jsonify

app = Flask(__name__)
app.debug = True

class Person:
    def __init__(self,name,life,define, atc):
        self.name = name
        self.life = life
        self.define = define
        self.equip = []
        self.atc = atc
        self.package =[
            {"name":"大砍刀","atc":20,"define":-5,"life":0},
            {"name":"黄金甲","atc":-5,"define":20,"life":200},
            {"name":"小红药","atc":5,"define":0,"life":100},
         ]

    def attck(self,other):
        other.life -= self.atc

    def equip1(self,something):
        for i in self.equip:
            self.life += i.get('life')
            self.atc += i.get('atc')
            self.define += i.get('define')



a = Person('player1', 100, 100, 12)
b = Person('player2', 100, 100, 12)


@app.before_request
def func():
    g.a = a
    g.b = b

@app.route('/')
def index():
    if request.method == 'GET':
        a.equip = []
        b.equip = []
        a.life=100
        b.life=100
        a.define=100
        b.define=100
        a.atc = 12
        b.atc=12
        return  render_template('h.html',player = {"player1":g.a,"player2":g.b})


@app.route('/equip/')
def add():
    ret = request.args.to_dict()
    player = ret.get('player')
    name = ret.get('name')
    if player == 'player1':
        for i in a.package:
            if i.get('name')==name:
                a.equip1(i)
                a.equip.append(i)
    else:
        for i in b.package:
            if i.get('name')==name:
                b.equip1(i)
                b.equip.append(i)

    player1 = {'player1':a.equip,'player2':b.equip}
    player2 = {'life':a.life,'atc':a.atc,'def':a.define}
    player3 = {'life': b.life, 'atc': b.atc, 'def': b.define}

    return jsonify(
        player1,
        player2,
        player3,
    )

import random
@app.route('/battle/')
def battle():
    while a.life>0 and b.life>0:
        print(a.life,b.life,b.atc,a.atc)
        if random.randint(0,10)%2:
            a.attck(b)
        else:
            b.attck(a)
    print(a.life, b.life)

if __name__ == '__main__':
    app.run()