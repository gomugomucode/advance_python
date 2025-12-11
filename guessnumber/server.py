# server.py
import socket
import threading
import json
import random
import time
import os

HOST = "0.0.0.0"
PORT = 9999
LEADERBOARD_FILE = "leaderboard.json"

# utility: newline-delimited JSON messages
def send_json(conn, obj):
    try:
        data = json.dumps(obj) + "\n"
        conn.sendall(data.encode())
    except Exception:
        pass

def recv_json(sock, buffer):
    # buffer: bytes accumulator; returns (obj_or_None, remaining_buffer)
    try:
        if b"\n" not in buffer:
            return None, buffer
        line, rest = buffer.split(b"\n", 1)
        obj = json.loads(line.decode())
        return obj, rest
    except Exception:
        return None, buffer

# leaderboard persistence
def load_leaderboard():
    if not os.path.exists(LEADERBOARD_FILE):
        return []
    try:
        with open(LEADERBOARD_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return []

def save_leaderboard(data):
    with open(LEADERBOARD_FILE, "w") as f:
        json.dump(data, f, indent=2)

leaderboard_lock = threading.Lock()
leaderboard = load_leaderboard()

# matchmaking
waiting = []
rooms = {}
rooms_lock = threading.Lock()
client_rooms = {}  # conn -> room_id

def record_win(player_name, attempts, difficulty):
    entry = {
        "player": player_name,
        "attempts": attempts,
        "difficulty": difficulty,
        "timestamp": time.time()
    }
    with leaderboard_lock:
        leaderboard.append(entry)
        # keep sorted by attempts ascending (best first)
        leaderboard.sort(key=lambda e: e["attempts"])
        save_leaderboard(leaderboard)

def start_room(room_id):
    room = rooms.get(room_id)
    if not room:
        return
    # initialize round
    mode = room.get("difficulty", "medium")
    if mode == "easy":
        room["random_num"] = random.randint(0, 50)
    elif mode == "hard":
        room["random_num"] = random.randint(0, 500)
    else:
        room["random_num"] = random.randint(0, 100)
    room["attempts"] = {p: 0 for p in room["players"]}
    room["time_left"] = 60
    room["running"] = True
    room["turn"] = 0  # index of current player
    # notify both clients
    for i, p in enumerate(room["players"]):
        send_json(p["conn"], {"type":"START", "your_index": i, "players":[x["name"] for x in room["players"]],
                              "difficulty": room.get("difficulty","medium"), "turn": room["turn"]})
    # start timer thread for room
    threading.Thread(target=room_timer, args=(room_id,), daemon=True).start()

def room_timer(room_id):
    while True:
        with rooms_lock:
            room = rooms.get(room_id)
            if not room or not room.get("running"):
                return
            if room["time_left"] <= 0:
                # time up: notify both and switch player (start new round)
                for p in room["players"]:
                    send_json(p["conn"], {"type":"TIMEUP", "number": room["random_num"]})
                room["running"] = False
                # automatically start next round after small delay
                time.sleep(1)
                if room.get("players"):
                    room["turn"] = (room["turn"] + 1) % len(room["players"])
                    start_room(room_id)
                return
            room["time_left"] -= 1
        time.sleep(1)

def handle_client(conn, addr):
    print("Client connected:", addr)
    buffer = b""
    client_name = None
    try:
        while True:
            data = conn.recv(4096)
            if not data:
                break
            buffer += data
            while True:
                obj, buffer = recv_json(conn, buffer)
                if obj is None:
                    break
                typ = obj.get("type")
                if typ == "JOIN":
                    name = obj.get("name","Anon")
                    diff = obj.get("difficulty","medium")
                    client_name = name
                    # add to waiting queue and try to match
                    with rooms_lock:
                        waiting.append({"conn":conn, "name":name, "difficulty":diff})
                        # if two or more waiting, create room
                        if len(waiting) >= 2:
                            a = waiting.pop(0)
                            b = waiting.pop(0)
                            room_id = str(time.time()) + "_" + str(random.randint(0,9999))
                            room = {
                                "id": room_id,
                                "players": [{"conn": a["conn"], "name": a["name"]}, {"conn": b["conn"], "name": b["name"]}],
                                "difficulty": a["difficulty"], # use first player's difficulty
                            }
                            rooms[room_id] = room
                            client_rooms[a["conn"]] = room_id
                            client_rooms[b["conn"]] = room_id
                            start_room(room_id)
                elif typ == "GUESS":
                    room_id = client_rooms.get(conn)
                    if not room_id:
                        send_json(conn, {"type":"ERROR","message":"Not in a room."})
                        continue
                    with rooms_lock:
                        room = rooms.get(room_id)
                        if not room or not room.get("running"):
                            send_json(conn, {"type":"ERROR","message":"No active round."})
                            continue
                        # find player index
                        idx = None
                        for i,p in enumerate(room["players"]):
                            if p["conn"] is conn:
                                idx = i
                        if idx is None:
                            send_json(conn, {"type":"ERROR","message":"Player not found."})
                            continue
                        # check turn
                        if idx != room["turn"]:
                            send_json(conn, {"type":"ERROR","message":"Not your turn."})
                            continue
                        guess = int(obj.get("value", -1))
                        room["attempts"][room["players"][idx]["name"]] += 1
                        secret = room["random_num"]
                        diff = abs(secret - guess)
                        # compute hint
                        if diff == 0:
                            # winner
                            room["running"] = False
                            winner = room["players"][idx]["name"]
                            attempts = room["attempts"][winner]
                            # notify everyone
                            for p in room["players"]:
                                send_json(p["conn"], {"type":"CORRECT", "player": winner, "attempts": attempts, "number": secret})
                            # record to leaderboard
                            record_win(winner, attempts, room.get("difficulty","medium"))
                            # small delay then switch turn and start new round
                            room["turn"] = (room["turn"] + 1) % len(room["players"])
                            time.sleep(1)
                            start_room(room_id)
                        else:
                            # send HINT to both (indicate who made guess)
                            hint = "COLD"
                            if diff <= 3:
                                hint = "VERY_HOT"
                            elif diff <= 10:
                                hint = "WARM"
                            elif diff <= 30:
                                hint = "LUKEWARM"
                            # send HINT to both (client may display differently)
                            for i,p in enumerate(room["players"]):
                                send_json(p["conn"], {"type":"HINT", "by": room["players"][idx]["name"],
                                                      "guess": guess, "hint": hint, "turn": room["turn"]})
                            # advance turn
                            room["turn"] = (room["turn"] + 1) % len(room["players"])
                            # inform next player of new turn
                            for i,p in enumerate(room["players"]):
                                send_json(p["conn"], {"type":"TURN", "turn": room["turn"], "next_player": room["players"][room["turn"]]["name"]})
                elif typ == "GET_LEADERBOARD":
                    with leaderboard_lock:
                        send_json(conn, {"type":"LEADERBOARD", "data": leaderboard})
                else:
                    send_json(conn, {"type":"ERROR","message":"Unknown message type."})
    except ConnectionResetError:
        pass
    except Exception as e:
        print("Error:", e)
    finally:
        print("Client disconnected:", addr)
        with rooms_lock:
            # remove from waiting if present
            waiting[:] = [w for w in waiting if w["conn"] is not conn]
            # remove from rooms, notify remaining player
            rid = client_rooms.get(conn)
            if rid and rid in rooms:
                room = rooms.pop(rid, None)
                if room:
                    for p in room["players"]:
                        if p["conn"] is not conn:
                            try:
                                send_json(p["conn"], {"type":"OTHER_LEFT"})
                            except:
                                pass
            client_rooms.pop(conn, None)
        try:
            conn.close()
        except:
            pass

def main():
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen()
    print("Server listening on", HOST, PORT)
    try:
        while True:
            conn, addr = s.accept()
            threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()
    except KeyboardInterrupt:
        print("Shutting down.")
    finally:
        s.close()

if __name__ == "__main__":
    main()
