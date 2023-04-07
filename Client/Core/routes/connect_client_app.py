# -*- coding: utf-8 -*- #

# -----------------------------
# Topic: connect client end with tornado
# Author: k14
# Created: 2023.04.04
# Description: holding the control of tornado client to connect with tornado server
#              ususal port：64614
# History:
#    <autohr>    <version>    <time>        <desc>
#    k14         v0.1         2023/04/07    build the basic
# -----------------------------


import asyncio
import tornado.ioloop
import tornado.websocket


class Tornado_Client_App:
    def __init__(self, url):
        self.url = url
        self.websocket = None
        self.ioloop = tornado.ioloop.IOLoop.current()
        self.is_connecting = False
        self.keep_alive_callback = None

    def start(self):
        self.ioloop.run_sync(self.connect)
        self.ioloop.start()

    async def connect(self):
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
        if self.websocket is not None and self.is_connecting:
            self.keep_alive_callback.stop()
            self.websocket.close()
            self.ioloop.stop()

            self.is_connecting = False

    def keep_alive(self):
        self.send('ping')

    def send(self, message):
        if self.websocket is not None and self.is_connecting:
            self.websocket.write_message(message)

    async def listen(self):
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
        if type(message) == str:
            print(f"Received message: {message}")


if __name__ == "__main__":
    url = "ws://127.0.0.1:8080/websocket"
    test_client = Tornado_Client_App(url)

    try:
        test_client.start()
    except KeyboardInterrupt:
        test_client.close()