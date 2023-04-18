# -*- coding: utf-8 -*- #

# -----------------------------
# Topic: sky eye session
# Author: m14
# Created: 2023.04.11
# Description: maintains sky eye session list
# History:
#    <autohr>    <version>    <time>        <desc>
#    m14         v0.1         2023/04/11    basic build
# -----------------------------


class SESession():
    """
    
    it holds the session from one client.
    
    Args:
        connection: one client connection to server.
    """
    next_session_id: int = 0
    
    def __init__(self, connection):
        self.session_id = SESession.next_session_id
        self.connection = connection

        SESession.next_session_id += 1