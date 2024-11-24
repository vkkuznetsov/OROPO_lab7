import asyncio
import logging
from aio_pika import connect_robust, IncomingMessage
from producer import produce
from dotenv import load_dotenv
import os

logging.basicConfig(level=logging.INFO)

load_dotenv()

TIMEOUT = 10


async def process(message: IncomingMessage):
    async with message.process():
        url = message.body.decode()
        logging.info(f'Обрабатываем ссылку: {url}')
        produce(url)


async def main():
    connection = await connect_robust(
        host=os.getenv('RABBITMQ_HOST', 'localhost'),
        port=int(os.getenv('RABBITMQ_PORT', 5672))
    )

    async with connection:
        channel = await connection.channel()

        queue = await channel.declare_queue('messages')

        while True:
            try:
                message = await asyncio.wait_for(queue.get(), timeout=TIMEOUT)
                await process(message)
            except asyncio.TimeoutError:
                logging.info("Очередь пуста, завершение работы.")
                break


if __name__ == "__main__":
    asyncio.run(main())
