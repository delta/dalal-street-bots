FROM python:3.6

WORKDIR /DalalBotServer
ADD . /DalalBotServer
RUN pip install -r requirements.txt
CMD ["./docker-bots-entry.sh"]
