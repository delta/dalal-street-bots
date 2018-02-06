import asyncio
from multiprocessing import cpu_count
from concurrent.futures import ThreadPoolExecutor
from market_messenger import MarketMessenger
from bot_manager import BotManager
from indicator_manager import IndicatorManager

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

@app.route('/')
async def hello():
    return 'hello'

@app.route('/loadall')
async def loadAll():
    global IS_INITIALIZED
    if not IS_INITIALIZED:
        asyncio.ensure_future(bot_manager.load_all_bots())
        IS_INITIALIZED = True
        return "initialized"
    else:
        return "already initialized"

@app.route('/createbot', methods=['POST'])
async def create_bot():
    """ This route creates bots.
        bot_type
        number
    """
    data = await request.form
    bot_type = data['bot_type']
    bot_name = data['bot_name']
    sleep_duration = data['sleep_duration']
    asyncio.ensure_future(bot_manager.create_bot(bot_type, bot_name,"{}"))

    return "Bot " + bot_name + " of type " + bot_type + " was created"

@app.route('/pausebot', methods=['POST'])
async def pause_bot():
    """ This is a route to pause bots
        Pass bot id to it
    """
    data = await request.form
    bot_id = int(data['bot_id'])
    asyncio.ensure_future(bot_manager.pause_bot(bot_id))
    return "Bot " + str(bot_id) + " was paused"

if __name__ == "__main__":
    app.run()