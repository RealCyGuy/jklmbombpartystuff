import random

import requests
import numpy as np

from human import Human
from utils import create_token, cleanup_word

token = create_token()

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
words = np.array(words)
print(f"Loaded {len(words)} words.")
used = set()

word_dict = {}

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
code = data.get("roomCode")
if not code:
    raise Exception
print(f"https://jklm.fun/{code}")
humans = []
human_ids = set()
latest_word = ""
die = [False]
for x in range(8):
    humans.append(Human(token, data["url"], f"Human {x}", code, words, word_dict, used, human_ids, die))
    humans[-1].connect_and_join()
    token = create_token()
humans[0].sio.wait()
