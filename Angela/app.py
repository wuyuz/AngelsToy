from flask import Flask,render_template
from serv.content import content
from serv.uploader import uploaders
from serv.users import user
from serv.devices import devices
from serv.friends import friend


app = Flask(__name__)
app.debug = True

app.register_blueprint(content)
app.register_blueprint(user)
app.register_blueprint(devices)
app.register_blueprint(friend)
app.register_blueprint(uploaders)


@app.route("/", methods=['GET'])
def qr_list():
    return render_template('WebToy.html')

if __name__ == "__main__":
    app.__call__
    app.run("0.0.0.0",9527)
