import asyncio
import random
import glob
import re

import aiohttp
import socketio
import requests
from aioconsole import ainput

from utils import create_token, cleanup_word


class Human:
    def __init__(self, token, code, url, name):
        print(f"Created {name}!")

        log = False
        self.sio = socketio.AsyncClient(logger=log, engineio_logger=log)
        self.gameSio = socketio.AsyncClient(logger=log, engineio_logger=log)
        self.token = token
        self.url = url
        self.name = name
        self.code = code
        self.joinData = {}

        self.rules = {}
        self.milestone = {}
        self.peerId = -2
        self.leaderPeerId = -1

        self.latest_word = ""
        self.bonus_letters = []
        self.attempts = 0

    async def join_room_callback(self, joinData):
        self.joinData = joinData
        await self.gameSio.emit("joinGame", ("bombparty", self.code, self.token))

    async def connect(self):
        await self.events()
        await self.sio.connect(url=self.url, transports=["websocket"])
        await self.gameSio.connect(url=self.url, transports=["websocket"])
        await self.sio.emit(
            "joinRoom",
            {
                "roomCode": self.code,
                "userToken": self.token,
                "nickname": self.name,
                "language": "en-US",
            },
            callback=self.join_room_callback,
        )

    async def events(self):
        @self.sio.event
        async def connect():
            print(self.name, "connected to JKLM!")

        @self.gameSio.event
        async def connect():
            print(self.name, "connected to Bomb Party!")

        @self.gameSio.event
        async def setup(data):
            self.leaderPeerId = data.get("leaderPeerId", -1)
            self.peerId = data.get("selfPeerId", -2)
            self.milestone = data["milestone"]
            await self.check_milestone()

        @self.gameSio.event
        async def correctWord(data):
            if len(self.latest_word) == 0:
                return
            cleaned = cleanup_word(self.latest_word)
            if cleaned not in correct:
                correct.append(cleaned)
                print(f"{len(correct)} words:", cleaned)
                with open("correct.txt", "a") as f:
                    f.write(cleaned + "\n")

        @self.gameSio.event
        async def setPlayerWord(peer_id, word):
            self.latest_word = word

        @self.gameSio.event
        async def setMilestone(milestone, time):
            self.milestone = milestone
            await self.check_milestone()

        @self.gameSio.event
        def nextTurn(peer_id, syllable, prompt_age):
            syllable = syllable.lower()
            if syllable not in syllables:
                syllables.append(syllable)
                with open("syllables.txt", "a") as f:
                    f.write(syllable + "\n")

    async def check_milestone(self):
        if self.milestone.get("dictionaryManifest", {}).get("name") != "English":
            print(f"{self.code} not English, disconnecting.")
            await self.disconnect()

    async def disconnect(self):
        await self.sio.disconnect()
        await self.gameSio.disconnect()


async def main():
    global correct, syllables
    with open("correct.txt", "r") as f:
        correct = f.read().split()
    print(f"Loaded {len(correct)} correct words.")
    with open("syllables.txt", "r") as f:
        syllables = f.read().split()
    
    print('Input codes like "jklm.fun/CODE":')
    rooms = {}
    while True:
        codes = await ainput()
        codes = re.findall(r"jklm.fun/[A-Z]{4}", codes)
        codes = set([code[-4:] for code in codes])
        for code in codes:
            room = rooms.get(code)
            if room:
                await room.disconnect()
                del rooms[code]
            else:
                async with aiohttp.ClientSession() as session:
                    async with session.post("https://jklm.fun/api/joinRoom", json={"roomCode": code}) as response:
                        if not response.ok:
                            print("Code is bad?")
                            continue
                        url = (await response.json()).get("url")
                        if not url:
                            print("No url.")
                            continue
                rooms[code] = Human(create_token(), code, url, random.choice(correct))
                await rooms[code].connect()
        print(rooms)


if __name__ == "__main__":
    asyncio.run(main())
