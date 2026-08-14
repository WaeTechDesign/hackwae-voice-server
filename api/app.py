"""
HackWae Voice Server

FastAPI App
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from api.router import router

from core.engine_loader import engine_loader

from services.queue.worker import worker

from core.exceptions.handlers import register_handlers

@asynccontextmanager
async def lifespan(app: FastAPI):

    # ------------------------------------------
    # Startup
    # ------------------------------------------

    engine_loader.load()

    worker.start()

    yield

    # ------------------------------------------
    # Shutdown
    # ------------------------------------------

    worker.stop()


def create_app():

    app = FastAPI(

        title="HackWae Voice Server",

        description="Universal Local TTS Server",

        version="0.1.0",

        lifespan=lifespan,

        docs_url="/docs",

        redoc_url="/redoc",

    )

    register_handlers(app)

    app.include_router(router)

    return app
