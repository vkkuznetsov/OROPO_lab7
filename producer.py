import os
import logging
import argparse
from pika import ConnectionParameters, BlockingConnection
from dotenv import load_dotenv
from get_links import get_link_inner_urls

logging.basicConfig(level=logging.INFO)
logging.getLogger('pika').setLevel(logging.WARNING)
load_dotenv()

connection_params = ConnectionParameters(
    host=os.getenv('RABBITMQ_HOST', 'localhost'),
    port=int(os.getenv('RABBITMQ_PORT', 5672)),
)


def produce(url_addr: str):
    with BlockingConnection(connection_params) as conn:
        with conn.channel() as channel:
            channel.queue_declare(queue='messages')
            channel.basic_publish(
                exchange='',
                routing_key='messages',
                body=url_addr,
            )
            logging.info(f'Отправлено: {url_addr}')


def main():
    parser = argparse.ArgumentParser(description="Запуск Producer для обработки ссылок")
    parser.add_argument('url', type=str, help="URL для поиска внутренних ссылок")
    args = parser.parse_args()

    url = args.url
    logging.info(f'Обработка страницы: {url}')
    links = get_link_inner_urls(url)

    for link in links:
        logging.info(f'Найдена ссылка: {link}')
        produce(link)


if __name__ == "__main__":
    main()
