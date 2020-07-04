import fire
import jinja2
import keyring
from aiohttp import web
from heidi.util import jsonify_response

from handlers import route as routing_table
from mail import Mail

HOST = 'smtp.yandex.ru:465'
LOGIN = 'master@boris.wtf'


async def create_jinja2(app):
    loader = jinja2.PackageLoader(__name__, 'templates')
    app['jinja'] = jinja2.Environment(loader=loader)


async def create_mail(app):
    credentials = (LOGIN, keyring.get_password(LOGIN, 'heidi'))
    app['mail'] = Mail('smtp.yandex.ru:465', credentials, app['jinja'])


def run(port):
    app = web.Application(middlewares=[
        jsonify_response,
    ])

    app.add_routes(routing_table)

    app.on_startup.extend([
        create_jinja2,
        create_mail,
    ])

    web.run_app(app, port=port)


fire.Fire(run)
