import pika
from fastapi import FastAPI
import os
from dotenv import load_dotenv

from crud import message_decode

load_dotenv()
app = FastAPI()


def callback(ch, method, properties, body):
    """Получение обьекта сообщения / удаление из очереди."""
    message = body
    ch.basic_ack(delivery_tag=method.delivery_tag)
    return message_decode(message)


@app.on_event('startup')
def startup():
    """
    Запуск сервера FastApi.
    Подключение потребителя с очереди Pika.
    """
    conn_params = pika.ConnectionParameters(os.getenv('RABBITMQ_HOST'),
                                            os.getenv('RABBITMQ_PORT'))
    connection = pika.BlockingConnection(conn_params)
    channel = connection.channel()
    channel.queue_declare(queue='DataBlock', durable=True)
    channel.basic_consume(on_message_callback=callback, queue='DataBlock')

    try:
        channel.start_consuming()
    except Exception as err:
        print('Exception consumer START: ', err)
        channel.stop_consuming()
