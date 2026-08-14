"""
HackWae Voice Server

Engine Lock
"""

import threading


class EngineLock:

    def __init__(self):

        self._locks = {}

    # --------------------------------------

    def get(self, engine: str):

        if engine not in self._locks:

            self._locks[engine] = threading.Lock()

        return self._locks[engine]


engine_lock = EngineLock()
