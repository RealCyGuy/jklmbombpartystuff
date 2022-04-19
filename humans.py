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
        missing = set(self.milestone["dictionaryManifest"]["bonusAlphabet"]) - set(
            self.bonus_letters
        )
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
            self.sio.emit(
                "chat", f"I don't know anything for {self.milestone['syllable']}."
            )

    def is_leader(self, peer_id: int = None):
        if peer_id is None:
            peer_id = self.peerId
        return peer_id == self.leaderPeerId

    def parse_command(self, author, message):
        if len(message) > 1 and message[0] in ["!", "/", "."]:
            command = message[1:].strip()
            if command == "ping":
                self.sio.emit("chat", "pong")
            elif (
                command == "start"
                or command == "s"
                and self.peerId == self.leaderPeerId
            ):
                self.sio.emit("chat", "Ok")
                self.gameSio.emit("setRulesLocked", True)
                self.gameSio.emit("startRoundNow")
            elif (
                command == "syllable"
                or command == "c"
                and self.peerId == self.leaderPeerId
            ):
                syllable = self.milestone.get("syllable", "")
                if syllable:
                    syllable_list = word_dict.get(syllable)
                    if not syllable_list:
                        syllable_list = set(
                            [word for word in words if syllable in word]
                        )
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
                        "maxPromptAge": 1,
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
