import logging
import asyncio
import websockets
import json
import settings

from controller.base import BaseController

class InputOuputServer():
    def __init__(self, controller: BaseController):
        self.robot = controller
        self.client = None
        self.logger = logging.getLogger(__name__)


    async def send_state(self):
        while True:
            await asyncio.sleep(1)  # Send a message every seconds
            if self.client:
                self.logger.debug("Sending state to client.")
                for websocket in self.connected:
                    try:
                        await self.client.send(json.dumps(self.robot.get_all_state()))
                    except:
                        self.logger.debug("Failed to send state to client.")
                        self.client = None


    async def handler(self, websocket, path):
        if self.client:
            self.logger.debug("Another client is already connected. Closing the connection.")
            return
        
        settings.set_status(settings.RobotState.API)
        self.client = websocket
        self.logger.debug("New connection added.")
        try:
            while True:  # Loop to handle multiple messages and timeouts
                try:
                    message = await asyncio.wait_for(websocket.recv(), timeout=10.0)  # Wait for a message for up to 10 seconds
                except asyncio.TimeoutError:
                    self.logger.debug("Timeout, no message received for 10 seconds.")
                    break  # Break the loop and remove the connection on timeout

                self.logger.debug(f"Receive commands: {message}")
                self.robot.process_incoming_commands(json.loads(message))
        except websockets.ConnectionClosedError:
            self.logger.debug("Connection closed without close frame.")
        except Exception as e:
            self.logger.error(f"An error occurred: {e}")
        finally:
            self.client = None
            self.logger.debug("Connection removed.")
            settings.set_status(settings.RobotState.MODE)
            self.robot.reset_robot_state()

    def run(self):
        server = websockets.serve(self.handler, '0.0.0.0', 1234)
        self.loop = asyncio.get_event_loop()
        self.loop.run_until_complete(server)
        self.loop.create_task(self.send_state())

    def close(self):
        self.loop.close()
