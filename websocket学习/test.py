from flask import Flask
from werkzeug.wsgi import DispatcherMiddleware
from werkzeug.serving import run_simple

app = Flask('app01')

app2 = Flask('app02')  #生成两个app

@app.route('/index',methods=['GET'])
def home():
    return 'index'

@app2.route('/index2',methods=['GET'])
def index():
    return 'index2'

app3 = DispatcherMiddleware(app,{
    '/sec':app2,  # 做了 分发，必须要加'/sec/index2' 才能触发app2
})

if __name__ == '__main__':
    app.__call__
    run_simple('localhost',9000,app3)




