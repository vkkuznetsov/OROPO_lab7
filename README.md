# Лаб работа №7 RabbitMQ
Окружение
1. Допустим у вас установлен кролик
2. Установлен питон 3.10.-3.12 желательно 3.11.9
# Запуск
1. Копируем файлы, ставим венв, и устанавливаем зависимости
2. pip install -r req.txt
3. Запуск продюсера (активированая venv)
4. python producer.py url
5. где юрл это ссылка
6. консюмер python consumer.py

Доп.  
Консюмер если что будет постоянно читать и записывать, смысл его не особо понятен, 
так что если нужно чтобы данные не хранились вечно то меняйте у консюмера 19 строчку на         message.ack()
он так все прочитает и упадет с ошибкой пустой очереди и все