import asyncio
from multiprocessing import cpu_count
from concurrent.futures import ThreadPoolExecutor
from market_messenger import MarketMessenger
from bot_manager import BotManager
from indicator_manager import IndicatorManager

from google.protobuf.json_format import MessageToJson

import json
from quart import Quart, request

app = Quart(__name__)

loop = asyncio.get_event_loop()

# load utilities
market_messenger = MarketMessenger(loop)
indicator_manager = IndicatorManager(market_messenger)
bot_manager = BotManager(market_messenger, indicator_manager, loop)
asyncio.ensure_future(market_messenger.start())

# global variables for ass saving
IS_INITIALIZED = False
@app.route('/', methods=['GET'])
async def hello():
    return 'hello'

@app.route('/getbotlist', methods=['POST'])
async def getbotlist():
    try:
        return_data = bot_manager.get_bots()
        return json.dumps(return_data)
    except Exception as e:
        print(e)
        return e

@app.route('/pausetype', methods=['POST'])
async def pausetype():
    try:
        bots = bot_manager.get_bots()
        data = await request.form
        bot_type = data['bot_type']
        for bot in bots:
            if bot['type'] == bot_type:
                await bot_manager.pause_bot(bot['id'])
        return "bots paused"
    except Exception as e:
        print(e)
        return e

@app.route('/pausetags', methods=['POST'])
async def pausetag():
    try:
        bots = bot_manager.get_bots()
        data = await request.form
        required_tag = data['bot_tag']
        for bot in bots:
            bot_tag = bot['settings'].get('bot_tag')
            if bot_tag == required_tag:
                await bot_manager.pause_bot(bot['id'])
        return "bots paused"
    except Exception as e:
        print(e)
        return e

@app.route('/loadall', methods=['POST'])
async def loadAll():
    try:
        global IS_INITIALIZED
        if not IS_INITIALIZED:
            asyncio.ensure_future(bot_manager.load_all_bots())
            IS_INITIALIZED = True
            return "initialized"
        else:
            return "already initialized"
    except Exception as e:
        print(e)
        return e

@app.route('/createbot', methods=['POST'])
async def create_bot():
    """Route to create bots
        - bot_type
        - number
    """
    try:
        data = await request.form
        bot_settings = data['bot_settings']
        bot_type = data['bot_type']
        bot_name = data['bot_name']
        asyncio.ensure_future(bot_manager.create_bot(bot_type, bot_name, bot_settings))

        return "Bot " + bot_name + " of type " + bot_type + " was created"
    except Exception as e:
        print(e)
        return e

@app.route('/pausebot', methods=['POST'])
async def pause_bot():
    """Route to pause bots
        - bot_id
    """
    try:
        data = await request.form
        bot_id = int(data['bot_id'])
        await bot_manager.pause_bot(bot_id)
        return "Bot " + str(bot_id) + " was paused"
    except Exception as e:
        print(e)
        return e

@app.route('/unpausebot', methods=['POST'])
async def unpause_bot():
    """Route to unpause bots
        - bot_id
    """
    try:
        data = await request.form
        bot_id = int(data['bot_id'])
        await bot_manager.unpause_bot(bot_id)
        return "Bot " + str(bot_id) + " was unpaused"
    except Exception as e:
        print(e)
        return e

@app.route('/getdetails', methods=['POST'])
async def get_details():
    """Route to get bot details
        - bot_id
    """
    try:
        data = await request.form
        bot_id = int(data['bot_id'])
        return_data = await asyncio.ensure_future(market_messenger.get_portfolio(bot_id))

        return MessageToJson(return_data)
    except Exception as e:
        print(e)
        return e

@app.route("/getlogs", methods=['POST'])
async def get_logs():
    """Route returns bot logs
        - bot_id ( if bot_id == -1, send all )
    """
    try:
        data = await request.form
        bot_id   = data['bot_id']

        if bot_id == -1:
            return await bot_manager.get_log(-1)
        else:
            return await bot_manager.get_log(bot_id)
    except Exception as e:
        print(e)
        return e

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
