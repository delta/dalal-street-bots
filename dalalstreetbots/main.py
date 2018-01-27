"""Test script"""

import asyncio
from multiprocessing import cpu_count
from concurrent.futures import ThreadPoolExecutor
from market_messenger import MarketMessenger
from bot_manager import BotManager
from indicator_manager import IndicatorManager

def main():
    """Master controller"""
    loop = asyncio.get_event_loop()
    #executor = ThreadPoolExecutor(max_workers=cpu_count()*5) # max_workers defaults to this in Py3.5.

    #loop.set_default_executer(executor)

    market_messenger = MarketMessenger(loop)
    indicator_manager = IndicatorManager(market_messenger)
    bot_manager = BotManager(market_messenger, indicator_manager, loop)

    #loop.run_in_executor(None, market_messenger.run,)
    asyncio.ensure_future(market_messenger.start())

    ## EDITABLE STUFF STARTS
    asyncio.ensure_future(bot_manager.load_all_bots())
    #asyncio.ensure_future(bot_manager.create_bot("EmaBot", "Primus2 Bot", "{}"))
    #asyncio.ensure_future(bot_manager.create_bot("DumbBot", "testbot2", '{"sleep_duration": 5}'))
    ### EDITABLE STUFF ENDS

    #bots = bot_manager.get_bots()
    #print(bots, bot_manager.get_bot_types())

    loop.run_forever()
    loop.close()

if __name__ == "__main__":
    main()
