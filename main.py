import signal
import sys
from lcu_driver import Connector
from loguru import logger as log
import signal
import sys
import asyncio
from lcu_driver import Connector
from loguru import logger as log

VALID_GAMESTATES = [
    'Lobby', 'Matchmaking', 'ReadyCheck', 'ChampSelect',
    'GameStart', 'InProgress', 'PreEndOfGame', None
]

class LClient:
    def __init__(self):
        self.state = None

    def set_state(self, event):
        if event.data in VALID_GAMESTATES or True:
            self.state = event.data
            log.debug(f"Switching state to {event.data}")
            return True
        else:
            log.error(f"Found not valid state: {event.data}")
            return False

connector = Connector()

@connector.ready
async def connect(connection):
    log.debug('LCU has made connection with League client.')

@connector.close
async def disconnect(_):
    log.debug('The client has been closed!')

@connector.ws.register('/lol-gameflow/v1/gameflow-phase', event_types=('UPDATE',))
async def client_state_change(connection, event):
    client.set_state(event)

# @connector.ws.register('/lol-champ-select/v1/session', event_types=('UPDATE',))
# async def client_pick_phase(connection, event):
#     log.debug(event.data["actions"][0][0]["type"])

@connector.ws.register('/lol-matchmaking/v1/ready-check', event_types=('UPDATE',))
async def state_match_found(connection, event):
    if event.data['state'] == 'InProgress' and event.data['playerResponse'] == 'None':
        log.debug("Match requested.")
        await connection.request('post', '/lol-matchmaking/v1/ready-check/accept', data={})
        
        log.debug("Match auto-accepted.")

def signal_handler(sig, frame):
    log.debug("Ctrl+C detected, attempting graceful shutdown...")
    loop = asyncio.get_event_loop()
    loop.create_task(connector.stop())
    sys.exit(0)

if __name__ == "__main__":
    client = LClient()
    signal.signal(signal.SIGINT, signal_handler)
    log.debug("LCU has finished initialising. Ctrl+C to exit.")
    connector.start()
