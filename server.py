import socket
import threading
import pickle
from ChessBoard import ChessBoard

server = "192.168.29.113"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.bind((server, port))
except socket.error as e:
    print(e)

s.listen()
print("Server started, waiting for connections...")

connected_clients = []
games = {}

def threaded_client(conn, player, game_id):
    global games
    conn.send(pickle.dumps(games[game_id]))
    while True:
        try:
            data = pickle.loads(conn.recv(2048))
            if game_id in games:
                games[game_id].move_piece(*data)
                games[game_id].update_turn()
                game_state = games[game_id]
                for client in connected_clients:
                    if client != conn:
                        client.send(pickle.dumps(game_state))
            else:
                break
        except:
            break

    print("Connection lost")
    try:
        del games[game_id]
        print("Closing game", game_id)
    except:
        pass
    conn.close()

while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    if len(connected_clients) % 2 == 0:
        games[len(connected_clients) // 2] = ChessBoard()
        print("Creating a new game...")

    connected_clients.append(conn)
    player = len(connected_clients) - 1
    game_id = len(connected_clients) // 2

    print(f"{addr} connected to game {game_id} as player {player % 2}")
    t = threading.Thread(target=threaded_client, args=(conn, player, game_id))
    t.start()