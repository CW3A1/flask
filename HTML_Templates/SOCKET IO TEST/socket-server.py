from flask import Flask, render_template
from flask_socketio import SocketIO, emit, send

app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = 'PNONISFUCKINGAWESOME'
socket = SocketIO(app)

@app.route('/')
def home():
    return render_template('socket-site.html')





if __name__ == '__main__':
    socket.run(app,debug=True)