import asyncio
import functools
import logging
from dataclasses import dataclass

import fastapi
from asgiref.sync import sync_to_async
from django.conf import settings
from django.core.asgi import get_asgi_application
from django.core.signals import request_finished, request_started
from starlette.middleware import Middleware
from starlette.routing import Mount
from starlette.types import ASGIApp, Receive, Scope, Send

from django_fast_api import DjangoThreadPoolExecutor

logger = logging.getLogger(__name__)


async def on_startup() -> None:
    loop = asyncio.get_event_loop()
    default_executor = DjangoThreadPoolExecutor(max_workers=settings.THREADS)
    logger.info(f'Setup ThreadPoolExecutor: max_workers={settings.THREADS}')
    loop.set_default_executor(default_executor)


# Не используем BaseHTTPMiddleware (декоратор `app.middleware`):
# ```python
# @app.middleware('http')
# async def http_middleware(request: Request, call_next):
#     return await call_next(request)
# ```
# Потому что `call_next` запускает новую(!) task-у, порождает новый context, который при выходе из task-и будет утерян.


middleware_list = []


def add_middleware(cls: type | None = None, **options):  # type: ignore
    if cls is None:
        return functools.partial(add_middleware, **options)
    middleware_list.append(Middleware(cls, **options))
    return cls


@add_middleware
@dataclass
class DjangoMiddleware:
    app: ASGIApp

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        await sync_to_async(request_started.send)(sender=self.__class__, scope=scope)
        try:
            await self.app(scope, receive, send)
        finally:
            await sync_to_async(request_finished.send)(sender=self.__class__)


app = fastapi.FastAPI(
    version=settings.VERSION,
    middleware=middleware_list,
    on_startup=[on_startup],
    routes=[
        Mount('/app', app=get_asgi_application()),
    ],
)


@app.get('/liveness', name='liveness')
def probe_liveness() -> dict:
    return {'status': 'alive'}
