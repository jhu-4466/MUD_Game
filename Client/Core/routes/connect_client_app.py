# -*- coding: utf-8 -*- #

# -----------------------------
# Topic: connect client end with tornado
# Author: k14
# Created: 2023.04.04
# Description: holding the control of tornado client to connect with tornado server
#              ususal port：64614
# History:
#    <autohr>    <version>    <time>        <desc>
#    k14         v0.1         2023/04/04    basic build unsuccess.
# -----------------------------


import tornado.ioloop
import tornado.websocket
import tornado.httpclient


class Tornado_Client_App(tornado.websocket.WebSocketClientConnection):
    """_summary_
    
    It connects to the Tornado server end via websocket.
    
    Args:
        url: the address of tornado server
        request: websocket connect need a httprequest
        connected: the state between client and server
    """
    def __init__(self, url):
        self.url = url
        self.request = tornado.httpclient.HTTPRequest(url)
        self.connected = False
        
        super().__init__(self.request)

    async def connect(self):
        """_summary_
    
        Connect to the Tornado server end via websocket
    
        """
        try:
            self.websocket = await tornado.websocket.websocket_connect(self.url)
        except tornado.websocket.WebSocketError as e:
            print(f"Failed to connect to server: {e}")
        else:
            self.connected = True

    async def on_message(self, message):
        """_summary_
    
        Calling back when the client receives message from Tornado server end via websocket
        
        """
        print(f"Received message from server: {message}")

    def send_message(self, message):
        """_summary_
    
        Send message to Tornado server end via websocket
        
        """
        assert self.connected, "Client is not connected to server yet."
        self.websocket.write_message(message)


if __name__ == "__main__":
    url = "ws://192.168.2.9:64614/websocket"
    test_client = Tornado_Client_App(url)
    tornado.ioloop.IOLoop.current().run_sync(test_client.connect)

    # send message to server
    test_client.send_message("Hello, Tornado server!")

    # wait for server's response
    def on_timeout():
        print("Timeout waiting for server's response.")
        tornado.ioloop.IOLoop.current().stop()

    tornado.ioloop.IOLoop.current().add_timeout(
        deadline=tornado.ioloop.time() + 1,  # wait for 1 second
        callback=on_timeout
    )
    tornado.ioloop.IOLoop.current().start()
