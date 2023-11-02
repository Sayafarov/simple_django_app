from contextlib import contextmanager
from concurrent.futures import ThreadPoolExecutor
import django.db
from anyio._backends import _asyncio as anyio_asyncio


# В django на каждый поток создается свое соединение с БД.
# Но никто эти соединения не закрывает.
# Django закрывает соединение только в том потоке, в котором идет обработка запроса (про другие потоки она не знает).
# Поэтому мы заменяем ThreadPoolExecutor на свой DjangoThreadPoolExecutor, который об этом заботится.
class DjangoThreadPoolExecutor(ThreadPoolExecutor):
    def submit(self, func, *args, **kwargs):
        func = _fixup_django_db()(func)
        return super().submit(func, *args, **kwargs)


class DjangoAnyIOWorkerThread(anyio_asyncio.WorkerThread):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.original_queue_get = self.queue.get
        self.queue.get = self.patched_queue_get

    def patched_queue_get(self, *args, **kwargs):
        item = self.original_queue_get(*args, **kwargs)
        if item is None:
            # we are stopped
            _close_all_db_connections()
            return None
        context, func, args, future = item
        func = _fixup_django_db()(func)
        return context, func, args, future


def _close_all_db_connections():
    for conn in django.db.connections.all():
        conn.close()


@contextmanager
def _fixup_django_db():
    django.db.reset_queries()
    django.db.close_old_connections()
    try:
        yield
    finally:
        django.db.close_old_connections()
