# -*- coding: utf-8 -*- #

# -----------------------------
# Topic: connect client end with tornado
# Author: k14
# Created: 2023.04.04
# Description: holding the control of tornado client to connect with tornado server
#              ususal port：8080
# History:
#    <autohr>    <version>    <time>        <desc>
#    k14         v0.1         2023/04/07    build the basic
# -----------------------------


import tornado.ioloop
import tornado.websocket

import asyncio
import threading


class TornadoServiceClient:
    """_summary_
    
    The client end connecting to the server.
    
    Attributes:
        url: the address of the server.
        websocket: due to the recommendation from the document that use websocket_connect() to build the client end.
        ioloop: one tornado client one I/O loop.
        is_connecting: the connecting state.
        keep_alive_callback: the keeping alive callback function.
    """
    def __init__(self, url):
        self.url = url
        self.websocket = None
        self.ioloop = tornado.ioloop.IOLoop.current()
        self.is_connecting = False
        self.keep_alive_callback = None

    def start(self):
        """_summary_
        
        Connect to server, all internet communications belongs the same ioloop.
        
        """
        self.ioloop.run_sync(self.connect)
        self.ioloop.start()

    async def connect(self):
        """_summary_
        
        The core logic of connecting.
        
        """
        try:
            self.websocket = await tornado.websocket.websocket_connect(self.url)
            self.ioloop.add_callback(self.listen)
            self.keep_alive_callback = tornado.ioloop.PeriodicCallback(self.keep_alive, 5000)
            self.keep_alive_callback.start()

            self.is_connecting = True
            print(f"Succeed to connect to {self.url}")
        except Exception as e:
            print(f"Failed to connect to {self.url}: {e}")

    def close(self):
        """_summary_
        
        Close connection.
        
        """
        if self.websocket is not None and self.is_connecting:
            self.keep_alive_callback.stop()
            self.websocket.close()
            self.ioloop.stop()

            self.is_connecting = False

    def keep_alive(self):
        """_summary_
        
        Keep the connection alive.
        
        """
        self.send('ping')

    def send(self, message):
        """_summary_
        
        Send message to the server.
        
        """
        if self.websocket is not None and self.is_connecting:
            self.websocket.write_message(message)

    async def listen(self):
        """_summary_
        
        Listen message from the server during the whole process.
        
        """
        while True:
            message = await self.websocket.read_message()
            if message is None:
                print("Disconnected from server")
                self.websocket = None
                self.keep_alive_callback.stop()
                break
            await self.handle_message(message)
            await asyncio.sleep(0)

    async def handle_message(self, message):
        """_summary_
        
        Handle message from the server.
        
        """
        if type(message) == str:
            print(f"Received message: {message}")


class TornadoThread(threading.Thread):
    """_summary_
    
    To avoid the stoppage between pyqt and tornado.
    
    Attributes:
        client: TornadoServiceClient
    """
    def __init__(self, _client: TornadoServiceClient):
        threading.Thread.__init__(self)
        
        self.client = _client

    def run(self):
        asyncio.set_event_loop(asyncio.new_event_loop())
        self.client.start()


if __name__ == "__main__":
    url = "ws://127.0.0.1:8080/websocket"
    test_client = TornadoServiceClient(url)

    try:
        test_client.start()
    except KeyboardInterrupt:
        test_client.close()