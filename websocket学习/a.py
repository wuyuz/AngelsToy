from flask import Flask,signals,render_template

app = Flask('app01')
app.debug = True

def func(*args, **kwargs):
    print('触发信号', args, kwargs)

signals.request_started.connect(func)  # 使用connect将函数注册到信号中，也就是说请求进来就执行

@app.before_first_request
def before_request():
    pass

@app.before_first_request  # 向全局before_first_request_funcs列表添加两个函数
def before_request2():
    pass

@app.before_request  # 向全局before_first_request_funcs列表添加两个函数
def before_request3():
    pass


@app.route('/',methods=['GET'])
def index():
    print('视图')
    return render_template('ws.html')



if __name__ == '__main__':
    app.__call__
    app.run()


