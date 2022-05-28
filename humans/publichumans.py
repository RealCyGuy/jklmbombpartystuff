from core.human import Human
from core.state import State
from utils import create_token

token = create_token()

humans = []
state = State(humans)
state.create_room(token)

for x in range(8):
    humans.append(Human(token, f"Human {x}", state))
    humans[-1].connect_and_join()
    token = create_token()
state.ready()
humans[0].sio.wait()
