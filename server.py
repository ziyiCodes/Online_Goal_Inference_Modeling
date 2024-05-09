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

from inference import UpdatePosteriorClass

from flask import Flask, send_from_directory
from flask_socketio import SocketIO, emit
from enum import Enum, unique
import rx, random
from rx import operators as ops

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

# define a class, called "sendingMaps"
# in class, have attribute called "allMaps", a list of individual maps
# also a function called onDisplayReady
# and inside function, self.allMaps.pop

# pop the first item from the list, and remove the first item in the list
# so next time calling pop, just call the first item of the remaining list

class SendingMaps:
    def __init__(self):
        # Initialize the `allMaps` attribute with a list of game maps
        self.allMaps = [
            {
                'playerPosition': (0, 0),
                'goals': [(1, 1), (2, 3), (2, 4)],
                'blocks': [(4, 5), (5, 6)]
            },
            {
                'playerPosition': (1, 1),
                'goals': [(3, 3), (4, 2), (2, 2)],
                'blocks': [(6, 7), (7, 8)]
            }
            # Add more maps as required
        ]

    def onDisplayReady(self):
        # Check if there are maps available
        if self.allMaps:
            return self.allMaps.pop(0)
        else:
            return {'error': 'No more maps available'}

# Instantiate the SendingMaps class
map_manager = SendingMaps()

# Define the socket event handler outside the class
@socketio.on('playerReady')
def handlePlayerReady(button):
    print('player ready')
    game_map = map_manager.onDisplayReady()
    emit('initializeGame', game_map)

updatePosterior = UpdatePosteriorClass()

@socketio.on('updatePrior')
def handleNewAct(newActPos):
    action = tuple(newActPos['action'])
    print(action)
    posterior = updatePosterior(action)
    emit('updatePosterior', posterior)

if __name__ == '__main__':
    PORT = 3000
    socketio.run(app, port=PORT, debug=True)