# const express = require('express');
# const http = require('http');
# const socketIo = require('socket.io');

# const app = express();
# const server = http.createServer(app);
# const io = socketIo(server);

# app.use(express.static('public'))

# io.on('connection', (socket) => {
#     console.log('A user connected');

#     socket.on('disconnect', () => {
#         console.log('User disconnected');
#     });

#     socket.on('playerPosition', (position) => {
#         console.log('Player Position:', position);
#         // You can also emit events back to the client if needed
#     });

#     socket.on('newAct', (action) => {
#         console.log('Player Action:', action)
#     });
# });

# const PORT = 3000;
# server.listen(PORT, () => console.log(`Server listening on port ${PORT}`));

from flask import Flask, send_from_directory
from flask_socketio import SocketIO

app = Flask(__name__, static_url_path='', static_folder='public')
socketio = SocketIO(app)

@app.route('/')
def index():
    return send_from_directory('public', 'index.html')

@socketio.on('connect')
def on_connect():
    print('A user connected')

@socketio.on('disconnect')
def on_disconnect():
    print('User disconnected')

#@socketio.on('playerPosition')
#def handle_player_position(position):
    #print('Player Position:', position)
    # Calculate the likelihood based on position
   # likelihoods = calculate_likelihood(position)
    # Emit the likelihood back to the client
    # emit('posterior', likelihoods)

#def calculate_likelihood(position):
    # Dummy function to calculate likelihood based on the position
    # You might want to replace this with actual logic based on 'position'
    #return {'goal1': 0.7, 'goal2': 0.2, 'goal3': 0.1}

@socketio.on('newAct')
def handle_new_act(action):
    print('Player Action:', action)
    # one message combine action and position

def calculate_likelihood(position)

if __name__ == '__main__':
    PORT = 3000
    socketio.run(app, port=PORT, debug=True)