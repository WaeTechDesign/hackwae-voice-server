"""
HackWae Voice Server

Model Scanner
"""

from services.model_manager import model_manager


class ModelScanner:

    def scan(self):

        return model_manager.scan()


scanner = ModelScanner()
