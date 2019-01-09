import asyncio
from multiprocessing import cpu_count
from concurrent.futures import ThreadPoolExecutor
from market_messenger import MarketMessenger
from bot_manager import BotManager
from indicator_manager import IndicatorManager

from google.protobuf.json_format import MessageToJson

import json
from quart import Quart, request
from quart_cors import cors

app = Quart(__name__)
app = cors(app)
QUART_CORS_ALLOW_ORIGIN	= ['*']

loop = asyncio.get_event_loop()

# load utilities
market_messenger = MarketMessenger(loop)
asyncio.ensure_future(market_messenger.start())
indicator_manager = IndicatorManager(market_messenger)
bot_manager = BotManager(market_messenger, indicator_manager, loop)

# global variables for ass saving
IS_INITIALIZED = False
@app.route('/', methods=['GET'])
async def hello():
    return 'hello'

@app.route('/getbotlist', methods=['GET'])
async def getbotlist():
    try:
        return_data = bot_manager.get_bots()
        return json.dumps(return_data), 200
    except Exception as e:
        print("[Failed]: {}".format(str(e)))
        return "[Failed]: {}".format(str(e)), 400

@app.route('/pausetype', methods=['POST'])
async def pausetype():
    try:
        if IS_INITIALIZED == False:
            return "Not initialized"
        bots = bot_manager.get_bots()
        data = await request.form
        bot_type = data['bot_type']
        for bot in bots:
            if bot['type'] == bot_type:
                await bot_manager.pause_bot(bot['id'])
        return "bots paused", 200
    except Exception as e:
        print("[Failed]: {}".format(str(e)))
        return "[Failed]: {}".format(str(e)), 400

@app.route('/unpausetype', methods=['POST'])
async def unpausetype():
    try:
        if IS_INITIALIZED == False:
            return "Not initialized"
        bots = bot_manager.get_bots()
        data = await request.form
        bot_type = data['bot_type']
        for bot in bots:
            if bot['type'] == bot_type:
                await bot_manager.unpause_bot(bot['id'])
        return "bots paused"
    except Exception as e:
        print("[Failed]: {}".format(str(e)))
        return "[Failed]: {}".format(str(e)), 400

@app.route('/pausetags', methods=['POST'])
async def pausetag():
    try:
        if IS_INITIALIZED == False:
            return "Not initialized"
        bots = bot_manager.get_bots()
        data = await request.form
        required_tag = data['bot_tag']
        for bot in bots:
            bot_tag = bot['settings'].get('bot_tag')
            if bot_tag == required_tag:
                await bot_manager.pause_bot(bot['id'])
        return "bots paused"
    except Exception as e:
        print("[Failed]: {}".format(str(e)))
        return "[Failed]: {}".format(str(e)), 400

@app.route('/unpausetags', methods=['POST'])
async def unpausetag():
    try:
        if IS_INITIALIZED == False:
            return "Not initialized"
        bots = bot_manager.get_bots()
        data = await request.form
        required_tag = data['bot_tag']
        for bot in bots:
            bot_tag = bot['settings'].get('bot_tag')
            if bot_tag == required_tag:
                await bot_manager.unpause_bot(bot['id'])
        return "bots paused"
    except Exception as e:
        print("[Failed]: {}".format(str(e)))
        return "[Failed]: {}".format(str(e)), 400

@app.route('/loadbot', methods=['POST'])
async def loadbot():
    try:
        data = await request.form
        bot_name = data['bot_name']
        asyncio.ensure_future(bot_manager.load_bot(bot_name))
        return "Loaded bot"
    except Exception as e:
        print("[Failed]: {}".format(str(e)))
        return "[Failed]: {}".format(str(e)), 400

@app.route('/pauseall', methods=['POST'])
async def pauseall():
    try:
        data = await request.form
        for bot_id in data:
            bot_id = int(bot_id)
            await bot_manager.pause_bot(bot_id)
        return "Paused bots"
    except Exception as e:
        print("[Failed]: {}".format(str(e)))
        return "[Failed]: {}".format(str(e)), 400

@app.route('/unpauseall', methods=['POST'])
async def unpauseall():
    try:
        data = await request.form
        for bot_id in data:
            bot_id = int(bot_id)
            await bot_manager.unpause_bot(bot_id)
        return "Unpaused bots"
    except Exception as e:
        print("[Failed]: {}".format(str(e)))
        return "[Failed]: {}".format(str(e)), 400

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
        print("[Failed]: {}".format(str(e)))
        return "[Failed]: {}".format(str(e)), 400

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
        print("[Failed]: {}".format(str(e)))
        return "[Failed]: {}".format(str(e)), 400

@app.route('/pausebot', methods=['POST'])
async def pause_bot():
    """Route to pause bots
        - bot_id
    """
    try:
        if IS_INITIALIZED == False:
            return "Not initialized"
        data = await request.form
        bot_id = int(data['bot_id'])
        await bot_manager.pause_bot(bot_id)
        return "Bot " + str(bot_id) + " was paused"
    except Exception as e:
        print("[Failed]: {}".format(str(e)))
        return "[Failed]: {}".format(str(e)), 400

@app.route('/unpausebot', methods=['POST'])
async def unpause_bot():
    """Route to unpause bots
        - bot_id
    """
    try:
        if IS_INITIALIZED == False:
            return "Not initialized"
        data = await request.form
        bot_id = int(data['bot_id'])
        await bot_manager.unpause_bot(bot_id)
        return "Bot " + str(bot_id) + " was unpaused"
    except Exception as e:
        print("[Failed]: {}".format(str(e)))
        return "[Failed]: {}".format(str(e)), 400

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
        print("[Failed]: {}".format(str(e)))
        return "[Failed]: {}".format(str(e)), 400

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
        print("[Failed]: {}".format(str(e)))
        return "[Failed]: {}".format(str(e)), 400

if __name__ == "__main__":
    IS_INITIALIZED = True
    asyncio.ensure_future(bot_manager.load_all_bots())
    app.run(host='0.0.0.0', port=5000)