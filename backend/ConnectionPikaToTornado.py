import pika
from pika.adapters.tornado_connection import TornadoConnection
import os
from dotenv import load_dotenv

load_dotenv()


class PikaClient:
    """Конфигурация для соединения к Pika."""
    def __init__(self, io_loop):
        self.host = os.getenv('RABBITMQ_HOST')
        self.port = os.getenv('RABBITMQ_PORT')
        self.username = os.getenv('RABBITMQ_USERNAME')
        self.password = os.getenv('RABBITMQ_PASSWORD')
        self.io_loop = io_loop
        self.connected = False
        self.connecting = False
        self.connection = None
        self.channel = None

    def connect(self):
        """Создание соединения с Pika."""
        if self.connecting:
            return
        self.connecting = True
        credentials = pika.PlainCredentials(username=self.username, password=self.password)
        params = pika.ConnectionParameters(self.host, self.port, "/", credentials=credentials)
        self.connection = TornadoConnection(
            params,
            custom_ioloop=self.io_loop,
            on_open_callback=self.on_connected,
            on_close_callback=self.on_closed,
            on_open_error_callback=self.err
        )

    def on_connected(self, connection):
        """Открытие канала."""
        self.connected = True
        self.connection = connection
        self.connection.channel(on_open_callback=self.on_channel_open)

    def on_channel_open(self, channel):
        """Создание очереди."""
        channel.queue_declare(queue='DataBlock', durable=True)
        self.channel = channel

    def err(self, conn, c):
        """Ошибка подключения."""
        raise SystemExit('pika error!')

    def on_closed(self, conn, c):
        """Закрытие канала."""
        print('pika close!')
        return self.io_loop.stop()
