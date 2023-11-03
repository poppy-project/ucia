import cv2
import asyncio
from aiortc import MediaStreamTrack, RTCPeerConnection, RTCSessionDescription
from aiortc.contrib.media import MediaBlackhole, MediaPlayer
from vision.camera import Camera

class VideoStreamTrack(MediaStreamTrack):
    kind = "video"

    def __init__(self):
        super().__init__()
        self.camera = Camera()
        self.logger = logging.getLogger(__name__)


    async def recv(self):
        while True:
            ret, frame = self.camera.grab_frame_loop()
            if not ret:
                break
            pts, time_base = await self.next_timestamp()
            frame_time = int(pts * time_base * 1000)
            self.on_frame(frame, frame_time)
            await asyncio.sleep(0.01)

    def on_frame(self, frame, timestamp):
        self.timestamp = timestamp
        self.frame = frame

class WebRTC():
    def __init__(self):
        self.rtc_peer_connections = set()
        self.logger = logging.getLogger(__name__)


    async def offer(self, request):
        params = await request.json()
        offer = RTCSessionDescription(sdp=params["sdp"], type=params["type"])

        pc = RTCPeerConnection()
        pcs.add(pc)

        @pc.on("datachannel")
        def on_datachannel(channel):
            @channel.on("message")
            def on_message(message):
                if isinstance(message, str) and message.startswith("ping"):
                    channel.send("pong" + message[4:])

        @pc.on("connectionstatechange")
        async def on_connectionstatechange():
            log_info("Connection state is %s", pc.connectionState)
            if pc.connectionState == "failed":
                await pc.close()
                pcs.discard(pc)

        @pc.on("track")
        def on_track(track):
            log_info("Track %s received", track.kind)
            
            video_track = VideoStreamTrack()
            rtc_peer_connection.addTrack(video_track)


            @track.on("ended")
            async def on_ended():
                log_info("Track %s ended", track.kind)
                await recorder.stop()

        # handle offer
        await pc.setRemoteDescription(offer)
        await recorder.start()

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



    def run(self):
        # Create HTTP Application
        self.app = web.Application()

        app.router.add_post("/offer", offer)

        self.loop = asyncio.get_event_loop()
        
        self.logger.info("Raspberry Pi WebRTC server listening on port 8080...")

        self.server = self.loop.run_until_complete(
            web.run_app(app, port="8080")
        )

    def close(self):
        coros = [pc.close() for pc in self.rtc_peer_connections]
        await asyncio.gather(*coros)
        pcs.clear()
