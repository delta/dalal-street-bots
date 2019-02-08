"""indicator_manager holds the IndicatorManager class to manage all Bots"""

import os
import json
import asyncio
import traceback
import sqlite3

def hash_dict(mydict):
    return json.dumps(mydict, sort_keys=True)

DB_NAME = "dalalstreetbots.db"

class IndicatorManager:
    """IndicatorManager class is used to manage all indicator"""

    def __init__(self, market_messenger, loop=None):
        self.market_messenger = market_messenger
        self.loop = loop
        self.conn = sqlite3.connect(DB_NAME)
        self.cursor = self.conn.cursor()
        self.indicator_count = 0
        self.__indicators__ = dict()
        asyncio.ensure_future(self.start_stock_prices_stream())
        #asyncio.ensure_future(self.start_market_depth_streams())

    def write_to_logs(self, bot_id, text):
        try:
            self.cursor.execute("""INSERT INTO logs (bot_id, log, created_at) VALUES  (?, ?, time('now'))""", (bot_id, text))
            self.conn.commit()
        except Exception as e:
            error_traceback = ''.join(traceback.format_tb(e.__traceback__))
            error_message = "Got error: {} @@@ {}".format(str(e), error_traceback)
            print("Fatal error while writing to db. Error: {}".format(error_message))

    async def start_stock_prices_stream(self):
        while True:
            try:
                stream = await self.market_messenger.get_stock_prices_stream()

                async for update in stream:
                    for stock_id in update.prices:
                        for indic_type in self.__indicators__:
                            for settings_hash in self.__indicators__[indic_type][stock_id]:
                                indicator = self.__indicators__[indic_type][stock_id][settings_hash]
                                if indicator.update_type == "prices":
                                    indicator.update(update.prices[stock_id])
                        
            except Exception as e:
                error_traceback = ''.join(traceback.format_tb(e.__traceback__))
                error_message = "Got Error: {} @@@ {}".format(str(e), error_traceback)
                self.write_to_logs(0, error_message)
                return "Failed", 400
            
            await asyncio.sleep(2)

    async def start_market_depth_streams(self):
        try:
            await asyncio.sleep(3)
            all_stocks = self.market_messenger.stocks
            for stock_id in all_stocks:
                asyncio.ensure_future(self.start_market_depth_stream(stock_id))
        except Exception as e:
            error_traceback = ''.join(traceback.format_tb(e.__traceback__))
            error_message = "Got Error: {} @@@ {}".format(str(e), error_traceback)
            self.write_to_logs(0, error_message)
            return "Failed", 400

    async def start_market_depth_stream(self, stock_id):
        while True:
            try:
                stream = await self.market_messenger.get_market_depth_stream(stock_id)
                first_update = None

                async for update in stream:
                    if first_update is None:
                        first_update = update
                    
                    for indic_type in self.__indicators__:
                        if stock_id in self.__indicators__[indic_type]:
                            for settings_hash in self.__indicators__[indic_type][stock_id]:
                                indicator = self.__indicators__[indic_type][stock_id][settings_hash]
                                if indicator.update_type == "market_depth":
                                    indicator.update(first_update, update)

            except Exception as e:
                error_traceback = ''.join(traceback.format_tb(e.__traceback__))
                error_message = "Got Error: {} @@@ {}".format(str(e), error_traceback)
                self.write_to_logs(0, error_message)
                await asyncio.sleep(2)

    def get_indicator_types(self):
        """get_indicator_types returns a list of names of indicator classes found in the
        dalalstreetbots/indicators directory"""
        indicator_classes = [f[:-3] for f in os.listdir("./indicators") if f[-3:] == ".py" and f != "__init__.py"]
        return indicator_classes

    def get_indicator_default_settings(self, indicator_class_name):
        """Get a indicator's default settings"""
        try:
            indicator_module = __import__("indicators." + indicator_class_name)
            indicator_module = getattr(indicator_module, indicator_class_name)
            indicator_class = getattr(indicator_module, indicator_class_name)
            indicator_settings = getattr(indicator_class, "default_settings", {})
            indicator_update_type = getattr(indicator_class, "update_type") # should fail if update_type isn't defined
            return indicator_settings
        except Exception as error:
            print(error)
            raise Exception("Error getting settings of " + indicator_class_name + " class")

    def validate_indicator_type(self, indicator_type):
        """Validate given indicator_type in the indicators/ folder. Returns (False, error-message)
        if invalid. Returns (True, '') if valid."""

        try:
            settings = self.get_indicator_default_settings(indicator_type)
        except Exception as error:
            return (False, str(error))

        # no special checks
        return (True, "")

    def validate_indicators(self):
        """Validate all indicators in the indicators/ folder. Returns a dict with key as
        indicator_type name, and value as (is_valid, error_message_str) tuple"""
        return {
            indicator_type: self.validate_indicator_type(indicator_type)
            for indicator_type in self.get_indicator_types()
        }

    async def get_indicator(self, indicator_type, stock_id, indicator_settings):
        """get_indicator returns an indicator instance. It creates a new instance if required
        or returns an existing one"""
        indicator_settings_hash = hash_dict(indicator_settings)
        if indicator_type not in self.__indicators__:
            self.__indicators__[indicator_type] = dict()
        indicators = self.__indicators__[indicator_type]

        if stock_id not in indicators:
            indicators[stock_id] = dict()
        indicators = indicators[stock_id]

        if indicator_settings_hash not in indicators:
            indicator_module = __import__("indicators." + indicator_type)
            indicator_module = getattr(indicator_module, indicator_type)
            indicator_class = getattr(indicator_module, indicator_type)
            self.indicator_count = self.indicator_count + 1
            indicator = indicator_class()
            await indicator._hidden_init_(self.indicator_count, indicator_settings, self)
            indicators[indicator_settings_hash] = indicator

            if indicator.update_type == "market_depth":
                asyncio.ensure_future(self.start_market_depth_stream(stock_id))
            #elif indicator.update_type == "prices":
            #    indicator.update(self.market_messenger.stocks[stock_id].current_price)


        indicator = indicators[indicator_settings_hash]

        return indicator
