import socketio

sio = socketio.Client()

room_id = ''

@sio.event
def connect():
    print("Connected to the server")
    sio.emit('join_game')

@sio.event
def message(data):
    print(f"{data}")

@sio.event
def game_joined(data):
    print(f"Connected to room {data}")
    global room_id
    room_id = data['room_id']    

@sio.event
def play_game():
    choice = int(input("""Choose your move:
                        1. ROCK
                        2. PAPER
                        3. SCISSORS
                        4. LIZARD
                        5. SPOCK
                        0. QUIT GAME
                        CHOICE: """))
    if choice != 0:
        sio.emit('player_choice',{'choice': choice,'room_id':room_id})
    else:
        sio.emit('end_game',{'choice': choice,'room_id':room_id})



if __name__ == '__main__':
    sio.connect('http://localhost:5000')
    sio.wait()
    