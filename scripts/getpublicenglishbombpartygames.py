import requests

r = requests.get("https://jklm.fun/api/rooms")
data = r.json()
rooms = [
    room
    for room in data["publicRooms"]
    if room["gameId"] == "bombparty" and room.get("details") == "English"
]
rooms.sort(key=lambda x: x["playerCount"], reverse=True)
print(" ".join("jklm.fun/" + room["roomCode"] for room in rooms))
