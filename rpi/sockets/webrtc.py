import cv2
import asyncio
import logging
import json
import aiohttp_cors
import av

from aiohttp import web
from aiortc import VideoStreamTrack, RTCPeerConnection, RTCSessionDescription
from aiortc.contrib.media import MediaBlackhole, MediaPlayer
from vision.camera import Camera

class VideoCameraPI(VideoStreamTrack):
    def __init__(self,frame_interval=100):
        super().__init__()
        self.direction = 'sendonly'
        self.camera = Camera()
        self.logger = logging.getLogger(__name__)
        self.frame_interval = frame_interval


    async def recv(self):
        while True:
            ret, frame = self.camera.grab_frame_loop()
            if not ret:
                break

            # Convert the OpenCV frame (a NumPy array) to an aiortc VideoFrame
            video_frame = av.VideoFrame.from_ndarray(frame, format="bgr24")

            # Update the timestamp of the video frame
            pts, time_base = await self.next_timestamp()
            video_frame.pts = pts
            video_frame.time_base = time_base

            # This line is crucial. Instead of calling self.on_frame(), 
            # you should return the video frame.
            await asyncio.sleep(self.frame_interval / 1000)  # Sleep for the frame interval
            return video_frame  # Return the video frame

class WebRTC():
    def __init__(self):
        self.rtc_peer_connections = set()
        self.logger = logging.getLogger(__name__)


    async def offer(self, request):
        params = await request.json()
        offer = RTCSessionDescription(sdp=params["sdp"], type=params["type"])

        pc = RTCPeerConnection()
        self.rtc_peer_connections.add(pc)
        # pc.addTransceiver('video', {'direction': 'recvonly'})
        # Create a new VideoStreamTrack instance and add it to the RTCPeerConnection
        video_pi = VideoCameraPI()
        pc.addTrack(video_pi)

      

        @pc.on("connectionstatechange")
        async def on_connectionstatechange():
            self.logger.info("Connection state is %s", pc.connectionState)
            if pc.connectionState == "failed":
                await pc.close()
                self.rtc_peer_connections.discard(pc)

        # handle offer
        await pc.setRemoteDescription(offer)

        # send answer
        answer = await pc.createAnswer()
        await pc.setLocalDescription(answer)

        return web.Response(
            content_type="application/json",
            text=json.dumps(
                {"sdp": pc.localDescription.sdp, "type": pc.localDescription.type}
            ),
        )

        return

        # while True:
            # try:
                # await asyncio.sleep(1)
                # frame = video_track.frame
                # if frame is not None:
                    # data = cv2.imencode(".jpg", frame)[1].tostring()
                    # await rtc_peer_connection.data_channels[rtc_peer_connection_id].send(data)
            # except Exception as e:
                # print("Error sending frame:", str(e))

    async def run_server(self):
        # Create HTTP Application
        self.app = web.Application()

        # Configure default CORS settings.
        cors = aiohttp_cors.setup(self.app, defaults={
            "*": aiohttp_cors.ResourceOptions(
                allow_credentials=True,
                expose_headers="*",
                allow_headers="*",
            )
        })

        # Define the /offer route, and enable CORS on it.
        resource = cors.add(self.app.router.add_resource("/offer"))
        cors.add(resource.add_route("POST", self.offer))

        self.logger.info("Raspberry Pi WebRTC server listening on port 8080...")

        self.runner = web.AppRunner(self.app)
        await self.runner.setup()

        self.site = web.TCPSite(self.runner, '0.0.0.0', 8080)
        await self.site.start()

    
    def run(self):
        self.loop = asyncio.get_event_loop()
        server_coroutine = self.run_server()  # create coroutine
        server_task = asyncio.ensure_future(server_coroutine)  # create task from coroutine
        self.loop.run_until_complete(server_task)  # run the task
        
    async def close(self):
        coros = [pc.close() for pc in self.rtc_peer_connections]
        await asyncio.gather(*coros)
        self.rtc_peer_connections.clear()
