from enum import Enum, auto
import random
from aiohttp import web
import socketio
import uuid 
import json

class Move(Enum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3
    LIZARD = 4
    SPOCK = 5

game_rules = {
    Move.SCISSORS: [Move.PAPER, Move.LIZARD],
    Move.PAPER: [Move.ROCK, Move.SPOCK],
    Move.ROCK: [Move.LIZARD, Move.SCISSORS],
    Move.LIZARD: [Move.SPOCK, Move.PAPER],
    Move.SPOCK: [Move.SCISSORS, Move.ROCK]
}

def get_winner(move1:Move, move2:Move) -> int :
    if move1 == move2:
        return 0
    elif move2 in game_rules[move1]:
        return 1
    elif move1 in game_rules[move2]:
        return 2
    else:
        return -1

# create a Socket.IO server
sio = socketio.AsyncServer()

# wrap with ASGI application
app = web.Application()

sio.attach(app)
matches = {}

class Match():
    def __init__(self,user1_sid,user2_sid,scores,cur_round=0) -> None:
        self.user1_sid = user1_sid
        self.user2_sid = user2_sid
        self.scores = scores
        self.room_id = str(uuid.uuid4())
        self.cur_round = cur_round

    def reset_scores(self):
        self.scores = {}
        self.cur_round = 0

    def get_current_round_result(self):
        result = get_winner(Move(self.scores[self.cur_round][self.user1_sid]),Move(self.scores[self.cur_round][self.user2_sid]))
        self.scores[self.cur_round].update({'result':result})
        old_round = self.cur_round
        self.cur_round +=1
        return self.scores[old_round]
    
    def add_move(self,sid,move):
        if not self.scores.get(self.cur_round,""):
            self.scores[self.cur_round]={}
            self.scores[self.cur_round].update({sid:move})
        else:
            self.scores[self.cur_round].update({sid:move})
    
    def join_match(self,sid):
        if not self.user1_sid:
            self.user1_sid = sid
        elif not self.user2_sid:
            self.user2_sid = sid
    
    def player_disconnect(self,sid):
        if sid == self.user1_sid:
            self.user1_sid = ''
        elif sid == self.user2_sid:
            self.user2_sid = ''
                   

    def all_players_made_choice(self):
        return (self.scores[self.cur_round].get(self.user1_sid,'') and self.scores[self.cur_round].get(self.user2_sid,''))

    def __repr__(self):
        return json.dumps({"room_id": self.room_id,"user1_sid": self.user1_sid,"user2_sid": self.user2_sid,'scores':self.scores},indent=2)


# Handler for connects
@sio.event
async def connect(sid, environ):
    print(f"Client connected: {sid}")

@sio.event
async def join_game(sid):
    print(f"Client Requested To Join A Game: {sid}")

    room_id = None
    for roomId,match in matches.items():
        if not match.user2_sid:
            room_id = roomId
            break

    if room_id:
        print("Joining an existing room")

        matches[room_id].join_match(sid)
        await sio.enter_room(sid, room_id)
        await sio.emit('game_joined', {'room_id': room_id} , room=sid)
        await sio.emit('message', f"""Player {sid} has joined the room""",room=room_id,skip_sid=sid)
    else:
        print("Creating a new room")
        new_match = Match(sid,None,{})
        matches[new_match.room_id] = new_match
        await sio.enter_room(sid, new_match.room_id)
        await sio.emit('game_joined',{'room_id': new_match.room_id}, room=new_match.room_id)
    
    await sio.emit('play_game', room=sid)

@sio.event
async def player_choice(sid,data):
    matches[data['room_id']].add_move(sid,data['choice'])
    if  matches[data['room_id']].all_players_made_choice():
        await sio.emit('message', f"Both players have made their choice",room=data['room_id'])
        round_score = matches[data['room_id']].get_current_round_result()
        result_messages = {
            0: "It's a TIE!",
            1: f"Player {matches[data['room_id']].user1_sid} WINS!",
            2: f"Player {matches[data['room_id']].user2_sid} WINS!"
        }

        await sio.emit('message', f"""
            Player 1 chose {Move(round_score[matches[data['room_id']].user1_sid]).name}
            Player 2 chose {Move(round_score[matches[data['room_id']].user2_sid]).name}
            {result_messages[round_score['result']]}
            """, room=data['room_id'])
            
        await sio.emit('play_game', room=data['room_id'])
    else:
        await sio.emit('message', f"Waiting for both players to make their choice",room=sid)

    print("Match Data: ",matches[data['room_id']])

# Handler for disconnects
@sio.event
async def end_game(sid,data):
    print(f"Client requested end game: {sid}")
    matches[data['room_id']].player_disconnect(sid)
    matches[data['room_id']].reset_scores()
    await sio.emit('message', f"""Player {sid} has left the game. Resetting game""",room=data['room_id'],skip_sid=sid)
    
    await sio.disconnect(sid)
    await sio.emit('play_game', room=data['room_id'])

# Handler for disconnects
@sio.event
def disconnect(sid):
    print(f"Client disconnected: {sid}")

# Start the web server
if __name__ == '__main__':
    web.run_app(app, host='127.0.0.1', port=5000)