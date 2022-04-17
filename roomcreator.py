import random

import requests
import time

from utils import create_token

with open("./testing/correct.txt", "r") as f:
    correct = f.read().split()
print(f"Loaded {len(correct)} correct words.")

while True:
    token = create_token()
    payload = {
        "name": random.choice(correct),
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
        break
    input(f"{code} {token}")
    time.sleep(1)
    