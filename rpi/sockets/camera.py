import asyncio
import websockets
import logging

from PIL import Image
from io import BytesIO
from vision.camera import Camera

class CameraServer:
    def __init__(self):
        self.connected = set()
        self.logger = logging.getLogger(__name__)
        self.camera = Camera()
    
    async def send_to_all_clients(self):
        while True:
            await asyncio.sleep(1/20.0) 
            
            if len(self.connected) == 0:
                continue

            img = self.camera.grab_frame_loop()
            if img is None:
                continue

            with BytesIO() as bytes:
                pil_img = Image.fromarray(img)
                pil_img.save(bytes, 'jpeg')
                message = bytes.getvalue()
            
            for websocket in list(self.connected): 
                try:
                    await websocket.send(message)
                except websockets.ConnectionClosed:
                    self.logger.warning("Client disconnected. Removing from list.")
                    self.connected.remove(websocket)

    async def handler(self, websocket, path):
        self.logger.debug("New connection added.")
        self.connected.add(websocket)

        try:
            async for message in websocket:
                self.logger.debug(f"Receive commands :", message)
        except (websockets.ConnectionClosed, Exception) as e:
            self.logger.warning(f"Connection closed due to error: {e}")
        finally:
            self.connected.remove(websocket)

    def run(self):
        server_coro = websockets.serve(self.handler, '0.0.0.0', 5678)
        
        self.loop = asyncio.get_event_loop()

        self.loop.run_until_complete(server_coro)
        self.loop.create_task(self.send_to_all_clients())