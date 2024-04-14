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
    def __init__(self, frame_interval=16):
        super().__init__()
        self.direction = 'sendonly'
        self.camera = Camera()
        self.logger = logging.getLogger(__name__)
        self.frame_interval = frame_interval

    async def recv(self):
        while True:
            frame = self.camera.grab_frame()
            if frame is None:
                continue

            # Convert the OpenCV frame (a NumPy array) to an aiortc VideoFrame
            video_frame = av.VideoFrame.from_ndarray(frame, format="bgr24")

            pts, time_base = await self.next_timestamp()
            video_frame.pts = pts
            video_frame.time_base = time_base

            await asyncio.sleep(self.frame_interval / 1000)

            return video_frame

class DetectionVideoCameraPI(VideoStreamTrack):
    def __init__(self, frame_interval=16):
        super().__init__()
        self.direction = 'sendonly'
        self.camera = Camera()
        self.logger = logging.getLogger(__name__)
        self.frame_interval = frame_interval

    async def recv(self):
        while True:
            frame = self.camera.grab_detected_frame() 
            if frame is None:
                continue

            # Convert the OpenCV frame (a NumPy array) to an aiortc VideoFrame
            video_frame = av.VideoFrame.from_ndarray(frame, format="bgr24")

            # Update the timestamp of the video frame
            pts, time_base = await self.next_timestamp()
            video_frame.pts = pts
            video_frame.time_base = time_base

            # Sleep for the frame interval
            await asyncio.sleep(self.frame_interval / 1000)

            return video_frame 

class WebRTC:
    def __init__(self):
        self.rtc_peer_connections = set()
        self.logger = logging.getLogger(__name__)

    async def offer_camera(self, request):
        params = await request.json()
        offer = RTCSessionDescription(sdp=params["sdp"], type=params["type"])

        pc = RTCPeerConnection()
        self.rtc_peer_connections.add(pc)

        video_pi = VideoCameraPI()
        pc.addTrack(video_pi)

        @pc.on("connectionstatechange")
        async def on_connectionstatechange():
            self.logger.info("Connection state is %s", pc.connectionState)
            if pc.connectionState == "failed":
                await pc.close()
                self.rtc_peer_connections.discard(pc)

        # Handle offer
        await pc.setRemoteDescription(offer)

        # Send answer
        answer = await pc.createAnswer()
        await pc.setLocalDescription(answer)

        return web.Response(
            content_type="application/json",
            text=json.dumps(
                {"sdp": pc.localDescription.sdp, "type": pc.localDescription.type}
            ),
        )

    async def offer_detection(self, request):
        params = await request.json()
        offer = RTCSessionDescription(sdp=params["sdp"], type=params["type"])

        pc = RTCPeerConnection()
        self.rtc_peer_connections.add(pc)

        video_detection = DetectionVideoCameraPI()  # Use DetectionVideoCameraPI for detection
        pc.addTrack(video_detection)

        @pc.on("connectionstatechange")
        async def on_connectionstatechange():
            self.logger.info("Connection state is %s", pc.connectionState)
            if pc.connectionState == "failed":
                await pc.close()
                self.rtc_peer_connections.discard(pc)

        # Handle offer
        await pc.setRemoteDescription(offer)

        # Send answer
        answer = await pc.createAnswer()
        await pc.setLocalDescription(answer)

        return web.Response(
            content_type="application/json",
            text=json.dumps(
                {"sdp": pc.localDescription.sdp, "type": pc.localDescription.type}
            ),
        )

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

        # Define the /offer_camera route for camera streaming
        resource_camera = cors.add(self.app.router.add_resource("/offer_camera"))
        cors.add(resource_camera.add_route("POST", self.offer_camera))

        # Define the /offer_detection route for detection streaming
        resource_detection = cors.add(self.app.router.add_resource("/offer_detection"))
        cors.add(resource_detection.add_route("POST", self.offer_detection))

        self.logger.info("Raspberry Pi WebRTC server listening on port 8080...")

        self.runner = web.AppRunner(self.app)
        await self.runner.setup()

        self.site = web.TCPSite(self.runner, 'rosa.local', 8080)
        await self.site.start()

    def run(self):
        self.loop = asyncio.get_event_loop()
        server_coroutine = self.run_server()
        server_task = asyncio.ensure_future(server_coroutine)  
        self.loop.run_until_complete(server_task)

    async def close(self):
        coros = [pc.close() for pc in self.rtc_peer_connections]
        await asyncio.gather(*coros)
        self.rtc_peer_connections.clear()
