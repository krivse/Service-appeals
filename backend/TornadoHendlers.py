import tornado.web
import tornado.ioloop
from tornado.options import define, options
import os
import uuid
import pika

from ConnectionPikaToTornado import PikaClient

define('port', default=8000, help='Запуск проекта на порту: 8000', type=int)


class Application(tornado.web.Application):
    """Модуль конфигурации Tornado."""
    def __init__(self):
        handlers = [
            (r'/', BaseHangler),
            (r'/send', SendHandler),
        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), 'templates'),
            static_path=os.path.join(os.path.dirname(__file__), 'static'),
            cookie_secret=uuid.uuid4().int,
            xsrf_cookie=True,
            debug=False
        )
        super(Application, self).__init__(handlers, **settings)


class BaseHangler(tornado.web.RequestHandler):
    """Базовый обработчик для метода GET."""
    def get(self):
        self.render('index.html', answer='Отправить обращение')


class SendHandler(tornado.web.RequestHandler):
    """
    Обработчик метода POST.
    Отправка данных в RabbitMQ.
    """
    def post(self):
        message = (f"{self.get_argument('first_name')},"
                   f"{self.get_argument('last_name')},"
                   f"{self.get_argument('middle_name')},"
                   f"{self.get_argument('phone_number')},"
                   f"{self.get_argument('appeal')}"
                   )
        try:
            app.pika.channel.basic_publish(
                exchange='',
                routing_key="DataBlock",
                body=message,
                properties=pika.BasicProperties(delivery_mode=2))
            self.render('index.html', answer='Обращение зафиксировано!')
        except Exception:
            self.render('index.html', answer='Ошибка запроса, попробуйте позже!')


if __name__ == "__main__":
    """
    Подключение к модулю Pika.
    Запуск сервера Tornado.
    """
    ioloop = tornado.ioloop.IOLoop.current().instance()
    app = Application()
    app.pika = PikaClient(ioloop)
    app.pika.connect()
    try:
        app.listen(options.port)
        ioloop.start()
    except KeyboardInterrupt:
        ioloop.stop()
    except Exception as err:
        print('Exception ioloop START:', err)
