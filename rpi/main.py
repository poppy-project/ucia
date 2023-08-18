import logging
from threading import Thread
from SimpleWebSocketServer import SimpleWebSocketServer

from handlers.input_output import WsIOHandler
from handlers.camera import WsCamServer, grab_frame_loop, publish_loop

def run_websocket_servers():
    io_server = SimpleWebSocketServer('', 1234, WsIOHandler)
    cam_server = SimpleWebSocketServer('', 5678, WsCamServer)
    
    video_loop = Thread(target=grab_frame_loop)
    video_loop.daemon = True
    video_loop.start()

    publish_t = Thread(target=publish_loop)
    publish_t.daemon = True
    publish_t.start()

    servers = [
        Thread(target=server.serveforever)
        for server in (io_server, cam_server)
    ]
    for server in servers:
        server.start()

    for server in servers:
        server.join()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, 
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        datefmt='%d-%m-%Y %H:%M:%S')

    logger = logging.getLogger(__name__)
    logger.info('Server up and running')

    run_websocket_servers()

