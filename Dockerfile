FROM python:3.6

WORKDIR /DalalBotServer
ADD . /DalalBotServer
RUN apt update && apt install -y vim netcat
RUN pip3 install -r requirements.txt
RUN pip3 install -U protobuf
RUN pip3 install -U aiogrpc
CMD ["./docker-bots-entry.sh"]
