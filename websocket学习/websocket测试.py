#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Xu Junkai
"""

from flask import Flask,request,render_template
from geventwebsocket.handler import WebSocketHandler
from geventwebsocket.server import WSGIServer
from geventwebsocket.websocket import WebSocket

app = Flask(__name__)
socket_list = []

@app.route("/ws")
def my_ws():
    ws_socket = request.environ.get("wsgi.websocket")#type:WebSocket   #获取长链接对象
    print(ws_socket.closed)
    socket_list.append(ws_socket)#将每个连接过来的对象加入列表
    print(socket_list,len(socket_list))
    while True:
        print(ws_socket.closed)
        if not ws_socket.closed:
            msg = ws_socket.receive()#接收消息前端发送消息
            if ws_socket.closed:
                socket_list.remove(ws_socket)
                print(socket_list)
            print(socket_list)

            for usocket in socket_list:#遍历循环，实现群发功能
                if usocket == ws_socket:
                    continue
                try:
                    if not ws_socket.closed:
                        usocket.send(msg)
                except:
                    continue
        else:

            ws_socket.close()
            break
    return ' '



@app.route("/wechat")
def wechat():
    return render_template("ws.html")#当客户端访问/wechat进入ws.html地址


if __name__ == '__main__':
    app.__call__
    http_serv = WSGIServer(("0.0.0.0",9527),app,handler_class=WebSocketHandler)
    http_serv.serve_forever()

