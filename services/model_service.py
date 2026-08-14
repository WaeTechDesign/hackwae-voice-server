"""
HackWae Voice Server

Model Service
"""

from services.model.manager import manager


class ModelService:

    # --------------------------------------------------
    # Query
    # --------------------------------------------------

    list = manager.scan

    get = manager.get

    exists = manager.exists

    default = manager.default

    # --------------------------------------------------
    # Management
    # --------------------------------------------------

    create = manager.create

    update = manager.update

    remove = manager.remove


model_service = ModelService()
