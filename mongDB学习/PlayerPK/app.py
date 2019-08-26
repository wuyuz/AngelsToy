from flask import Flask

from serv.player import player
from serv.users import user

app = Flask(__name__)

app.debug = True
app.secret_key = "$%^*(%#@#$&*(%$#$%^"

app.register_blueprint(user)
app.register_blueprint(player)

if __name__ == '__main__':
    app.run()