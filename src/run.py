import os

import click
import django
import uvicorn

os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'

django.setup()

from django.core import management  # noqa


@click.group()
def cli() -> None:
    pass


@cli.command()
@click.option(
    '--collectstatic/--no-collectstatic',
    is_flag=True,
    default=True,
    help='Collect Django static',
)
@click.option(
    '--uvicorn-debug/--no-uvicorn-debug',
    is_flag=True,
    default=True,
    help='Enable/Disable debug and auto-reload',
)
def web(collectstatic: bool, uvicorn_debug: bool) -> None:
    from app import app

    if uvicorn_debug:
        # Автоперезапуск при изменении кода: uvicorn.config.Config.should_reload
        # Удобно при локальной разработке
        app = 'app:app'  # noqa:F811

    if collectstatic:
        management.call_command('collectstatic', '--no-input', '--clear')

    uvicorn.run(
        app,
        host='0.0.0.0',
        port=8000,
        access_log=False,
        log_config=None,
        lifespan='on',
    )


if __name__ == '__main__':
    cli()
