import random

import numpy as np
import requests

from utils import cleanup_word, create_token


class State:
    def __init__(self, humans: list):
        self.url = None
        self.code = None
        self.verify = None

        self.humans = humans
        self.response_index = 0
        self.is_ready = False

        self.word_dict = {}

        self.used = set()
        self.die = False
        self.human_ids = set()
        self.player_ids = set()
        self.latest_word = ""

        self.rules = {}
        self.milestone = {}
        self.leaderPeerId = -1

        with open("../testing/correct.txt", "r") as f:
            words = set(f.read().split())
        with open("../lists/kaggle.txt", "r") as f:
            words = words.union(f.read().split())
        with open("../testing/wrong.txt", "r") as f:
            words = words.difference(set(f.read().split()))

        words = [word.lower() for word in words]
        words = list(set(words))
        random.shuffle(words)
        words.sort(key=lambda word: len(set(word)), reverse=True)
        self.words = np.array(words)
        print(f"Loaded {len(self.words)} words.")

    def create_room(self, token):
        payload = {
            "name": "Humans only!",
            "isPublic": True,
            "gameId": "bombparty",
            "creatorUserToken": token,
        }
        headers = {"content-type": "application/json"}

        response = requests.request(
            "POST", "https://jklm.fun/api/startRoom", json=payload, headers=headers
        )
        data = response.json()
        self.code = data.get("roomCode")
        if not self.code:
            raise Exception
        print(f"https://jklm.fun/{self.code}")
        self.url = data["url"]

    def create_verification_token(self):
        digits = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
        token = ""
        for x in range(16):
            token += random.choice(digits)
        self.verify = token
        print(f"Verification token: {self.verify}")

    def ready(self):
        self.create_verification_token()
        self.is_ready = True

    def setmod(self, peer_id):
        self.humans[0].sio.emit("setUserModerator", (peer_id, True), callback=lambda x: None)

    def get_word(self, syllable, missing):
        best_word = ""
        top = -1
        syllable_list = self.word_dict.get(syllable)
        if not syllable_list:
            syllable_list = set([word for word in self.words if syllable in word])
            self.word_dict[syllable] = syllable_list
        for word in syllable_list:
            if word in self.used:
                continue
            score = len(set(word.lower()).intersection(missing))
            if score > top:
                best_word = word
                top = score
        return best_word

    def get_words(self, syllable):
        syllable_list = self.word_dict.get(syllable)
        if not syllable_list:
            syllable_list = set()
            for word in self.words:
                if syllable in word:
                    syllable_list.add(word)
                if len(syllable_list) > 500:
                    break
        syllable_list = list(syllable_list)
        random.shuffle(syllable_list)
        length = -2
        p_words = []
        for word in syllable_list:
            length += len(word) + 2
            if length > 150:
                break
            p_words.append(word.upper())
        return p_words, len(syllable_list)

    def send(self, message):
        if not self.is_ready:
            return
        self.humans[self.response_index].sio.emit("chat", message[:300])
        self.response_index += 1
        if self.response_index >= len(self.humans) - 1:
            self.response_index = 0

    def parse_command(self, author, message, leader, ingame=False):
        if not self.is_ready:
            return
        if len(message) > 1 and message[0] in ["!", "/", "."]:
            split = message[1:].strip().split(" ")
            command = split[0]
            if command == "syllable" or command == "c":
                if len(split) > 1:
                    syllable = cleanup_word(split[1])
                else:
                    syllable = leader.milestone.get("syllable", "")
                if len(syllable) > 30:
                    self.send("Input syllable too long!")
                elif syllable:
                    p_words, amount = self.get_words(syllable)
                    self.send(
                        ("500+" if amount > 500 else str(amount))
                        + f" result{'' if amount == 1 else 's'}: "
                        + ", ".join(p_words),
                    )
                else:
                    self.send("No syllable!")
            elif not ingame:
                if command == "ping":
                    self.send("pong")
                elif command == "help" or command == "h":
                    self.send(
                        "Commands: /help|h - /ping - /syllable|c [syllable] - /github\n"
                        "You can run in chat or in-game.",
                    )
                elif command in ["now", "n"]:
                    if "moderator" in author["roles"]:
                        leader.gameSio.emit("startRoundNow")
                        self.send(f"Of course, {author['nickname']}!")
                    else:
                        self.send("Sorry, only moderators can use this command.")
                elif command == "github":
                    self.send("https://github.com/RealCyGuy/jklmbombpartystuff")
                elif command == "verify" or command == "v":
                    if split[1] == self.verify:
                        self.create_verification_token()
                        self.setmod(author["peerId"])
                        self.send(f"You are now a moderator, {author['nickname']}!")
                    else:
                        self.send("Invalid verification token!!!")
