import json
from flask import Flask,request
from geventwebsocket.handler import WebSocketHandler
from geventwebsocket.server import WSGIServer
from geventwebsocket.websocket import WebSocket

ws_app = Flask(__name__)

user_socket_dict = {}

@ws_app.route('/toy/<toy_id>')
def find_toy(toy_id):
    web_toy = request.environ.get('wsgi.websocket')  #type:WebSocket

    if web_toy:
        user_socket_dict[toy_id] = web_toy
    # else:
    #     web_toy.close()

    while 1:
        print(user_socket_dict)

        user_msg = web_toy.receive()
        user_msg_dict = json.loads(user_msg)
        user_msg_dict['count'] = len(user_socket_dict)
        to_user = user_msg_dict.get('to_user')
        reveiver = user_socket_dict.get(to_user)
        reveiver.send(user_msg)


@ws_app.route('/app/<app_id>')
def find_app(app_id):
    web_app = request.environ.get('wsgi.websocket')  #type:WebSocket
    # print(web_app)
    if web_app:
        user_socket_dict[app_id] = web_app
    # else:
    #     web_toy.close()

    while 1:
        print(user_socket_dict)
        user_msg = web_app.receive()
        print(user_msg)
        user_msg_dict = json.loads(user_msg)
        to_user = user_msg_dict.get('to_user')
        reveiver = user_socket_dict.get(to_user)
        reveiver.send(user_msg)


if __name__ == '__main__':
    http_serv = WSGIServer(('0.0.0.0',9528),ws_app,handler_class=WebSocketHandler)
    http_serv.serve_forever()

#5faa4351b2c8770c725069cc7d1b716d