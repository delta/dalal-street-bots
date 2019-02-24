FROM python:3.6

WORKDIR /DalalBotServer
ADD . /DalalBotServer
RUN pip install -r requirements.txt
CMD ["./build_proto.sh"]
CMD ["python", "dalalstreetbots/main.py"]
