import random

import socketio
import requests
import numpy as np

from utils import create_token, cleanup_word

token = create_token()


class Human:
    def __init__(self, token, url, name):
        print(f"Created {name}!")

        log = False
        self.sio = socketio.Client(logger=log, engineio_logger=log)
        self.gameSio = socketio.Client(logger=log, engineio_logger=log)
        self.token = token
        self.url = url
        self.name = name
        self.joinData = {}

        self.rules = {}
        self.milestone = {}
        self.peerId = -2
        self.leaderPeerId = -1

        self.bonus_letters = []

    def join_room_callback(self, joinData):
        self.joinData = joinData
        self.gameSio.emit("joinGame", ("bombparty", code, self.token))

    def join_game_callback(self, *args, **kwargs):
        print(args, kwargs)

    def connect_and_join(self):
        self.events()
        self.sio.connect(url=self.url, transports=["websocket"])
        self.gameSio.connect(url=self.url, transports=["websocket"])
        self.sio.emit(
            "joinRoom",
            {
                "roomCode": code,
                "userToken": self.token,
                "nickname": self.name,
                "language": "en-US",
                "picture": "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",
            },
            callback=self.join_room_callback,
        )

    def turn(self):
        # self.gameSio.emit("setWord", ("﷽" * 30, False))
        missing = set(self.milestone["dictionaryManifest"]["bonusAlphabet"]) - set(self.bonus_letters)
        best_word = ""
        top = -1
        syllable = self.milestone["syllable"]
        syllable_list = word_dict.get(syllable)
        if not syllable_list:
            syllable_list = set([word for word in words if syllable in word])
            word_dict[syllable] = syllable_list
        for word in syllable_list:
            if word in used:
                continue
            score = len(set(word.lower()).intersection(missing))
            if score > top:
                best_word = word
                top = score
        if best_word:
            self.gameSio.emit("setWord", (best_word, True))
            used.add(best_word)
        else:
            self.sio.emit("chat", f"I don't know anything for {self.milestone['syllable']}.")

    def is_leader(self, peer_id: int = None):
        if peer_id is None:
            peer_id = self.peerId
        return peer_id == self.leaderPeerId

    def parse_command(self, author, message):
        if len(message) > 1 and message[0] in ["!", "/", "."]:
            command = message[1:].strip()
            if command == "ping":
                self.sio.emit("chat", "pong")
            elif command == "start" or command == "s" and self.peerId == self.leaderPeerId:
                self.sio.emit("chat", "Ok")
                self.gameSio.emit("setRulesLocked", True)
                self.gameSio.emit("startRoundNow")
            elif command == "syllable" or command == "c" and self.peerId == self.leaderPeerId:
                syllable = self.milestone.get("syllable", "")
                if syllable:
                    syllable_list = word_dict.get(syllable)
                    if not syllable_list:
                        syllable_list = set([word for word in words if syllable in word])
                        word_dict[syllable] = syllable_list
                    syllable_list = sorted(list(syllable_list), key=lambda x: len(x))
                    p_words = []
                    for word in syllable_list:
                        if word in used:
                            continue
                        p_words.append(word.upper())
                        if len(p_words) >= 5:
                            break
                    for word in reversed(syllable_list):
                        if word in used or word in p_words:
                            continue
                        p_words.append(word.upper())
                        if len(p_words) >= 10:
                            break
                    if p_words:
                        self.sio.emit("chat", " ".join(p_words))
                    else:
                        self.sio.emit("chat", f"Couldn't find anything for {syllable}.")
                else:
                    self.sio.emit("chat", "No syllable!")

    def events(self):
        @self.sio.event
        def connect():
            print(self.name, "connected to JKLM!")

        @self.gameSio.event
        def connect():
            print(self.name, "connected to Bomb Party!")

        @self.gameSio.event
        def setup(data):
            self.leaderPeerId = data.get("leaderPeerId", -1)
            self.peerId = data.get("selfPeerId", -2)
            if self.peerId >= 0:
                human_ids.add(self.peerId)
            if self.is_leader():
                self.gameSio.emit("setRulesLocked", False)
                self.gameSio.emit(
                    "setRules",
                    {
                        "promptDifficulty": "custom",
                        "customPromptDifficulty": 1,
                        "startingLives": 1,
                        "maxLives": 10,
                        "maxPromptAge": 1
                    },
                )
            self.milestone = data["milestone"]
            self.gameSio.emit("joinRound")

        @self.gameSio.event
        def setLeaderPeer(peer_id):
            self.leaderPeerId = peer_id

        @self.gameSio.event
        def nextTurn(peer_id, syllable, prompt_age):
            self.milestone["currentPlayerPeerId"] = peer_id
            self.milestone["syllable"] = syllable
            self.milestone["promptAge"] = prompt_age
            if self.milestone.get("currentPlayerPeerId", -3) == self.peerId:
                self.turn()

        @self.gameSio.event
        def setMilestone(milestone, time):
            self.milestone = milestone
            if milestone["name"] == "round":
                if milestone["currentPlayerPeerId"] == self.peerId:
                    self.turn()
            elif milestone["name"] == "seating":
                self.gameSio.emit("joinRound")
                if self.is_leader():
                    global used
                    used = set()
                    self.gameSio.emit("setRulesLocked", False)

        @self.gameSio.event
        def failWord(peer_id, reason):
            if peer_id == self.peerId:
                self.turn()
            if reason == "notInDictionary" or reason == "mustContainSyllable":
                self.parse_command(peer_id, latest_word)

        @self.gameSio.event
        def correctWord(data):
            if self.is_leader():
                if data["playerPeerId"] not in human_ids:
                    used.add(cleanup_word(latest_word.lower()))
            if self.peerId == data["playerPeerId"]:
                self.bonus_letters = data["bonusLetters"]

        @self.gameSio.event
        def setPlayerWord(peer_id, word):
            if self.is_leader():
                global latest_word
                latest_word = word

        @self.sio.event
        def chat(author, message):
            self.parse_command(author, message)


with open("testing/correct.txt", "r") as f:
    words = set(f.read().split())
with open("lists/kaggle.txt", "r") as f:
    words = words.union(f.read().split())
with open("testing/wrong.txt", "r") as f:
    words = words.difference(set(f.read().split()))

words = [word.lower() for word in words]
words = list(set(words))
random.shuffle(words)
words.sort(key=lambda word: len(set(word)), reverse=True)
words = np.array(words)
print(f"Loaded {len(words)} words.")
used = set()

with open("testing/syllables.txt", "r") as f:
    syllables = set(f.read().split())
word_dict = {}

payload = {
    "name": "Humans only!",
    "isPublic": False,
    "gameId": "bombparty",
    "creatorUserToken": token,
}
headers = {"content-type": "application/json"}

response = requests.request(
    "POST", "https://jklm.fun/api/startRoom", json=payload, headers=headers
)
data = response.json()
code = data.get("roomCode")
if not code:
    raise Exception
print(f"https://jklm.fun/{code}")
humans = []
human_ids = set()
latest_word = ""
for x in range(4):
    humans.append(Human(token, data["url"], f"Human {x}"))
    humans[-1].connect_and_join()
    token = create_token()
humans[0].sio.wait()
