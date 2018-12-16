FROM python:3.7-alpine

COPY . /app
WORKDIR /app/bot_engine
RUN pip install -r ../requirements.txt

CMD python bot.py
