# advanced_online_guess_gui.py
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import threading, socket, json, time, os
from playsound import playsound  # optional

# ----------------- simple sound helper -----------------
def play_sound(path):
    def _p():
        try:
            playsound(path)
        except Exception:
            pass
    threading.Thread(target=_p, daemon=True).start()

def play_sound_if_exists(name):
    if os.path.exists(name):
        play_sound(name)

# ----------------- Network client -----------------
class NetworkClient:
    def __init__(self):
        self.sock = None
        self.recv_thread = None
        self.running = False
        self.buffer = b""
        self.on_message = None  # callback func(msg_dict)

    def connect(self, host, port=9999, timeout=8):
        self.sock = socket.socket()
        self.sock.settimeout(timeout)
        self.sock.connect((host, port))
        self.sock.settimeout(None)
        self.running = True
        self.recv_thread = threading.Thread(target=self._recv_loop, daemon=True)
        self.recv_thread.start()

    def send(self, obj):
        try:
            if not self.sock:
                return
            data = json.dumps(obj) + "\n"
            self.sock.sendall(data.encode())
        except Exception as e:
            print("send error", e)

    def _recv_loop(self):
        try:
            while self.running:
                data = self.sock.recv(4096)
                if not data:
                    break
                self.buffer += data
                while b"\n" in self.buffer:
                    line, self.buffer = self.buffer.split(b"\n",1)
                    try:
                        msg = json.loads(line.decode())
                        if self.on_message:
                            self.on_message(msg)
                    except Exception:
                        pass
        except Exception:
            pass
        self.running = False
        if self.on_message:
            self.on_message({"type":"DISCONNECTED"})

    def close(self):
        self.running = False
        try:
            if self.sock:
                self.sock.close()
        except:
            pass

# ----------------- Tkinter GUI -----------------
class OnlineGuessGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Advanced Networked Guess Game")
        self.geometry("620x560")
        self.resizable(False, False)

        # game/network state
        self.client = None
        self.player_index = None
        self.player_name = None
        self.players = []
        self.turn = None
        self.current_attempts = 0
        self.connected = False

        self.create_widgets()

    def create_widgets(self):
        title = tk.Label(self, text="🔮 Networked Number Guess", font=("Helvetica",20,"bold"))
        title.pack(pady=8)

        # connect frame
        conn_frame = tk.LabelFrame(self, text="Online Connect", padx=8, pady=8)
        conn_frame.pack(padx=10, pady=6, fill="x")

        tk.Label(conn_frame, text="Server IP:").grid(row=0,column=0, sticky="w")
        self.server_entry = tk.Entry(conn_frame)
        self.server_entry.grid(row=0,column=1, sticky="w")
        self.server_entry.insert(0, "127.0.0.1")

        tk.Label(conn_frame, text="Your name:").grid(row=1,column=0, sticky="w")
        self.name_entry = tk.Entry(conn_frame)
        self.name_entry.grid(row=1,column=1, sticky="w")
        self.name_entry.insert(0, "Player")

        tk.Label(conn_frame, text="Difficulty:").grid(row=2,column=0, sticky="w")
        self.diff_var = tk.StringVar(value="medium")
        ttk.Radiobutton(conn_frame, text="Easy", variable=self.diff_var, value="easy").grid(row=2,column=1)
        ttk.Radiobutton(conn_frame, text="Medium", variable=self.diff_var, value="medium").grid(row=2,column=2)
        ttk.Radiobutton(conn_frame, text="Hard", variable=self.diff_var, value="hard").grid(row=2,column=3)

        self.connect_btn = tk.Button(conn_frame, text="Connect & Join Match", command=self.connect_to_server, width=18)
        self.connect_btn.grid(row=0,column=3, rowspan=2, padx=8)

        # status
        self.status_label = tk.Label(self, text="Not connected", font=("Arial",12))
        self.status_label.pack(pady=6)

        # game controls
        game_frame = tk.Frame(self)
        game_frame.pack(pady=6)

        self.guess_entry = tk.Entry(game_frame, font=("Arial",18), width=8, justify="center")
        self.guess_entry.grid(row=0,column=0, padx=6)

        self.guess_btn = tk.Button(game_frame, text="Send Guess", command=self.send_guess, width=12, state="disabled")
        self.guess_btn.grid(row=0,column=1, padx=6)

        self.hint_label = tk.Label(self, text="", font=("Helvetica",14, "bold"))
        self.hint_label.pack(pady=8)

        # scoreboard & players
        side = tk.Frame(self)
        side.pack(fill="both", expand=True, padx=10, pady=6)
        left = tk.LabelFrame(side, text="Players / Turn", padx=8, pady=8)
        left.pack(side="left", fill="both", expand=True)
        self.players_list = tk.Listbox(left, height=6)
        self.players_list.pack(fill="both", expand=True)

        right = tk.LabelFrame(side, text="Server Leaderboard", padx=8, pady=8)
        right.pack(side="right", fill="both", expand=True)
        self.leader_list = tk.Listbox(right, height=8)
        self.leader_list.pack(fill="both", expand=True)

        # local sound hint info
        tk.Label(self, text="Place optional sound files in the same folder (correct.wav incorrect.wav start.wav timeup.wav)").pack(pady=6)

        # local disconnect button
        self.disconnect_btn = tk.Button(self, text="Disconnect", command=self.disconnect_from_server, state="disabled")
        self.disconnect_btn.pack(pady=6)

    def connect_to_server(self):
        host = self.server_entry.get().strip()
        name = self.name_entry.get().strip() or "Player"
        diff = self.diff_var.get()
        self.player_name = name

        self.client = NetworkClient()
        self.client.on_message = self.on_server_message
        try:
            self.client.connect(host, 9999)
        except Exception as e:
            messagebox.showerror("Connection Failed", f"Could not connect: {e}")
            return
        self.connected = True
        self.connect_btn.config(state="disabled")
        self.disconnect_btn.config(state="normal")
        self.status_label.config(text="Connected. Waiting for match...")
        # send JOIN
        self.client.send({"type":"JOIN", "name": name, "difficulty": diff})

        # also request leaderboard (optional)
        self.client.send({"type":"GET_LEADERBOARD"})

    def disconnect_from_server(self):
        if self.client:
            self.client.close()
        self.connected = False
        self.connect_btn.config(state="normal")
        self.disconnect_btn.config(state="disabled")
        self.guess_btn.config(state="disabled")
        self.status_label.config(text="Disconnected")
        self.players_list.delete(0, tk.END)
        self.hint_label.config(text="")

    def send_guess(self):
        if not self.connected or not self.client:
            return
        val = self.guess_entry.get().strip()
        try:
            v = int(val)
        except ValueError:
            messagebox.showerror("Invalid", "Please enter an integer.")
            return
        self.client.send({"type":"GUESS", "value": v})
        self.guess_entry.delete(0, tk.END)
        # play click sound
        play_sound_if_exists("click.wav")

    def on_server_message(self, msg):
        typ = msg.get("type")
        if typ == "DISCONNECTED":
            self.after(0, lambda: self.status_label.config(text="Server disconnected"))
            return
        if typ == "START":
            # msg keys: your_index, players, difficulty, turn
            self.player_index = msg.get("your_index")
            self.players = msg.get("players", [])
            self.turn = msg.get("turn")
            self.current_attempts = 0
            self.after(0, self.update_players_ui)
            self.after(0, lambda: self.status_label.config(text=f"Match started. You are {self.players[self.player_index]}"))
            self.after(0, lambda: self.guess_btn.config(state="normal"))
            play_sound_if_exists("start.wav")
            return
        if typ == "HINT":
            # show hint from server
            by = msg.get("by")
            hint = msg.get("hint")
            guess = msg.get("guess")
            display = f"{by} guessed {guess} → {hint}"
            self.after(0, lambda: self.hint_label.config(text=display))
            play_sound_if_exists("wrong.wav")
            return
        if typ == "TURN":
            self.turn = msg.get("turn")
            nxt = msg.get("next_player")
            self.after(0, lambda: self.status_label.config(text=f"Turn: {nxt}"))
            # enable guess only if it's our turn
            if self.player_index == self.turn:
                self.after(0, lambda: self.guess_btn.config(state="normal"))
            else:
                self.after(0, lambda: self.guess_btn.config(state="disabled"))
            self.after(0, self.update_players_ui)
            return
        if typ == "CORRECT":
            player = msg.get("player")
            attempts = msg.get("attempts")
            number = msg.get("number")
            self.after(0, lambda: self.hint_label.config(text=f"{player} guessed correctly! Number was {number}. Attempts: {attempts}"))
            play_sound_if_exists("correct.wav")
            # refresh leaderboard from server
            self.client.send({"type":"GET_LEADERBOARD"})
            return
        if typ == "TIMEUP":
            number = msg.get("number")
            self.after(0, lambda: self.hint_label.config(text=f"Time up! Number was {number}"))
            play_sound_if_exists("timeup.wav")
            return
        if typ == "LEADERBOARD":
            data = msg.get("data", [])
            # data contains list of entries {player, attempts, difficulty, timestamp}
            self.after(0, lambda: self.populate_leaderboard(data))
            return
        if typ == "OTHER_LEFT":
            self.after(0, lambda: messagebox.showinfo("Opponent left", "Your opponent disconnected. Waiting for new match..."))
            self.after(0, lambda: self.status_label.config(text="Waiting for new match..."))
            return
        if typ == "ERROR":
            err = msg.get("message","")
            self.after(0, lambda: messagebox.showerror("Server Error", err))
            return

    def populate_leaderboard(self, data):
        self.leader_list.delete(0, tk.END)
        if not data:
            self.leader_list.insert(tk.END, "No highscores yet.")
            return
        for e in data[:50]:
            ts = time.strftime("%Y-%m-%d %H:%M", time.localtime(e.get("timestamp", time.time())))
            label = f"{e.get('player')} [{e.get('difficulty')}] — {e.get('attempts')} tries ({ts})"
            self.leader_list.insert(tk.END, label)

    def update_players_ui(self):
        self.players_list.delete(0, tk.END)
        for i, p in enumerate(self.players):
            marker = "◀ Your Turn" if i == self.turn and i == self.player_index else ""
            label = f"{i+1}. {p}"
            if i == self.turn:
                label += "  (► TURN)"
            if i == self.player_index:
                label += "  (YOU)"
            self.players_list.insert(tk.END, label)

    def on_closing(self):
        try:
            if self.client:
                self.client.close()
        except:
            pass
        self.destroy()

if __name__ == "__main__":
    app = OnlineGuessGUI()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()
