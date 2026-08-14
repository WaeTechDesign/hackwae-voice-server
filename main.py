"""
HackWae Voice Server
"""

import uvicorn

from api.app import create_app

from core.config import settings

app = create_app()

if __name__ == "__main__":

    uvicorn.run(

        "main:app",

        host=settings.server.host,

        port=settings.server.port,

        reload=settings.server.reload,

        workers=settings.server.workers,

    )
