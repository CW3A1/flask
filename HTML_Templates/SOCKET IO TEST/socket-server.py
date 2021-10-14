from flask import Flask, render_template
from flask_socketio import SocketIO, emit, send

app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = 'PNONISFUCKINGAWESOME'
socket = SocketIO(app)

number1 = 0
number2 = 0
@app.route('/<n1>/<n2>')
def home(n1,n2):
    number1 = n1
    number2 = n2
    return render_template('socket-site.html')

@socket.on('number')
def hanedmessage(msg):
    print('Message:' + msg)
    send(msg, broadcast=True)




if __name__ == '__main__':
    socket.run(app,debug=True)