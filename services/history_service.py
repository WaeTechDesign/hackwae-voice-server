"""
HackWae Voice Server

History Service
"""

from services.history.manager import manager
from services.history.cleaner import cleaner


class HistoryService:

    # --------------------------------------------------

    def list(self):
        return manager.list()

    # --------------------------------------------------

    def add(self, item):
        return manager.add(item)

    # --------------------------------------------------

    def get(self, filename):
        return manager.get(filename)

    # --------------------------------------------------

    def exists(self, filename):
        return manager.exists(filename)

    # --------------------------------------------------

    def metadata(self, filename):
        return manager.metadata(filename)

    # --------------------------------------------------

    def delete(self, filename):
        return cleaner.delete(filename)

    # --------------------------------------------------

    def clear(self):
        return cleaner.clear()


history_service = HistoryService()
