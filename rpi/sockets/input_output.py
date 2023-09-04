import logging
import asyncio
import websockets
import json

from controller.base import BaseController

class InputOuputServer():
    def __init__(self, controller: BaseController):
        self.robot = controller
        self.connected = set()
        self.logger = logging.getLogger(__name__)


    async def send_to_all_clients(self):
        while True:
            await asyncio.sleep(1)  # Send a message every 5 seconds
            self.logger.debug("Sending state to all client.")
            for websocket in self.connected:
                try:
                    await websocket.send(json.dumps(self.robot.get_all_state()))
                except:
                    pass  # The client may have disconnected, ignore the exception


    async def handler(self, websocket, path):
        self.logger.debug("New connection added.")
        self.connected.add(websocket)
        try:
            async for message in websocket:
                self.logger.debug(f"Receive commands :", message)
                self.robot.process_incoming_commands(json.loads(message))
        except websockets.ConnectionClosedError:
            self.logger.debug("Connection closed without close frame.")
        except Exception as e:
            self.logger.error(f"An error occurred: {e}")
        finally:
            self.connected.remove(websocket)
            self.logger.debug("Connection removed.")
            if len(self.connected) == 0:
                self.robot.reset_robot_state()

    def run(self):
        server = websockets.serve(self.handler, '0.0.0.0', 1234)
        self.loop = asyncio.get_event_loop()
        self.loop.run_until_complete(server)
        self.loop.create_task(self.send_to_all_clients())

    def close(self):
        self.loop.close()
