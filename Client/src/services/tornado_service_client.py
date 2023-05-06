# -*- coding: utf-8 -*- #

# -----------------------------
# Topic: connect client end with tornado
# Author: m14
# Created: 2023.04.04
# Description: holding the control of tornado client to connect with tornado server
#              ususal port：8080
# History:
#    <autohr>    <version>    <time>        <desc>
#    m14         v0.1         2023/04/07    build the basic
# -----------------------------


import tornado.ioloop
import tornado.websocket

import asyncio
import threading


class TornadoServiceClient:
    """
    
    The client end connecting to the server.
    
    Args:
        url: the address of the server.
        websocket: due to the recommendation from the document that use websocket_connect() to build the client end.
        ioloop: one tornado client one I/O loop.
        is_connecting: the connecting state.
        keep_alive_callback: the keeping alive callback function.
    """
    def __init__(self, url, reconnect_interval: int=5):
        self.url = url
        self.websocket = None
        self.ioloop = None
        self.keep_alive_callback = None
        self.reconnect_interval = reconnect_interval

    def on_start(self):
        """
        
        Connect to server, all internet communications belongs the same ioloop.
        
        """
        try:
            self.ioloop = tornado.ioloop.IOLoop.current()
            self.ioloop.run_sync(self.on_connect)
            self.ioloop.start()
        except asyncio.exceptions.TimeoutError:
            # may closes too fast so that producing a timeout error is un
            pass

    async def on_connect(self):
        """
        
        The core logic of connecting.
        
        """
        try:
            self.websocket = await tornado.websocket.websocket_connect(self.url)
            if self.websocket:
                self.ioloop.add_callback(self.listen)
                self.keep_alive_callback = tornado.ioloop.PeriodicCallback(self.keep_alive, 5000)
                self.keep_alive_callback.start()

                print(f"Succeed to connect to {self.url}")
        except Exception as e:
            print(f"Failed to connect to {self.url}: {e}")
            self.ioloop.add_timeout(self.ioloop.time() + self.reconnect_interval, self.on_reconnect)
    
    def on_reconnect(self):
        """
        
        The core logic of reconnecting.
        
        """
        print("Try to reconnect to the server...")
        self.ioloop.spawn_callback(self.on_connect)
        
    def on_close(self):
        """
        
        Close connection.
        
        """
        if self.websocket:
            self.keep_alive_callback.stop()
            self.websocket.close()
        
        # self.ioloop.add_callback(self.ioloop.stop)

    def keep_alive(self):
        """
        
        Keep the connection alive.
        
        """
        self.send('ping')

    def send(self, message):
        """
        
        Send message to the server.
        
        """
        if self.websocket:
            self.websocket.write_message(message)

    async def listen(self):
        """
        
        Listen message from the server during the whole process.
        
        """
        while True:
            message = await self.websocket.read_message()
            if message is None:
                print("Disconnected from server because the server closed, try to reconnect as soon...")
                self.websocket = None
                self.keep_alive_callback.stop()
                self.on_reconnect()
                break
            await self.handle_message(message)
            await asyncio.sleep(0)

    async def handle_message(self, message):
        """
        
        Handle message from the server.
        
        """
        if type(message) == str:
            print(f"Received message: {message}")


class TornadoClientThread(threading.Thread):
    """
    
    To avoid the stoppage between pyqt and tornado.
    
    Args:
        client: TornadoServiceClient
    """
    def __init__(self, _client: TornadoServiceClient):
        threading.Thread.__init__(self)
        
        self.client = _client

    def run(self):
        asyncio.set_event_loop(asyncio.new_event_loop())
        self.client.on_start()


# if __name__ == "__main__":
#     url = "ws://127.0.0.1:8080/websocket"
#     test_client = TornadoServiceClient(url)

#     try:
#         test_client.on_start()
#     except KeyboardInterrupt:
#         test_client.on_close()