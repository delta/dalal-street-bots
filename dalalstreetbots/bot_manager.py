"""bot_manager holds the BotManager class to manage all Bots"""

import os
import sqlite3
import json
import asyncio

DB_NAME = "dalalstreetbots.db"
# DB Structure:
# bots:
#   id
#   name
#   type
#   settings
#   state
#   run_count
#   is_paused -- if true means the bot has been rested, and isn't scheduled to execute
#   created_at
#
# logs:
#   bot_id
#   log
#   created_at

class BotManager:
    """BotManager class is used to manage all bots"""

    def __init__(self, market_messenger, indicator_manager, loop=None):
        self.conn, self.cursor = self.__init_db()
        self.market_messenger = market_messenger
        self.indicator_manager = indicator_manager
        self.loop = loop
        self.bot_instances = {}

    def __init_db(self):
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("SELECT name from sqlite_master WHERE type='table' AND name in ('bots', 'logs')")
        r = c.fetchall()
        if len(r) == 2:
            return conn, c

        c.execute("""CREATE TABLE bots (
            id int not null primary key,
            name varchar(100),
            type varchar(100),
            settings text,
            state text,
            run_count int,
            is_paused int,
            created_at datetime
        )""")
        c.execute("CREATE TABLE logs (bot_id int, log text, created_at datetime)")
        conn.commit()

        return conn, c

    def get_bot_types(self):
        """get_bot_types returns a list of names of bot classes found in the dalalstreetbots/bots
        directory"""
        bot_classes = [f[:-3] for f in os.listdir("./bots") if f[-3:] == ".py" and f != "__init__.py"]
        return bot_classes

    def get_bot_default_settings(self, bot_class_name):
        """Get a bot's default settings"""
        try:
            bot_module = __import__("bots." + bot_class_name)
            bot_module = getattr(bot_module, bot_class_name) # weird, but needs to be done. Life.
            bot_class = getattr(bot_module, bot_class_name)
            bot_settings = getattr(bot_class, "default_settings", {})
            return bot_settings
        except Exception as error:
            print(error)
            raise Exception("Error getting settings of " + bot_class_name + " class")

    def validate_bot_type(self, bot_type):
        """Validate given bot_type in the bots/ folder. Returns (False, error-message) if invalid.
        Returns (True, '') if valid."""

        settings = {}
        try:
            settings = self.get_bot_default_settings(bot_type)
        except Exception as error:
            return (False, str(error))

        if "sleep_duration" not in settings:
            return (False, "Required default setting 'sleep_duration' missing in class %s" % bot_type)

        return (True, "")

    def validate_bots(self):
        """Validate all bots in the bots/ folder. Returns a dict with key as bot_type name, and
        value as (is_valid, error_message_str) tuple"""
        return {
            bot_type:self.validate_bot_type(bot_type) for bot_type in self.get_bot_types()
        }

    async def create_bot(self, bot_type, bot_name, bot_settings, start_paused=False):
        """create_bot creates a bot of the given type, name and populates it with
        the given settings. It will check if bot_type is valid and bot_name is unique."""

        is_valid, error = self.validate_bot_type(bot_type)
        if not is_valid:
            raise Exception("Invalid bot class '%s': %s" % (bot_type, error))

        print("Gonna take the plunge")
        create_bot_res = await self.market_messenger.create_bot(bot_name)
        print("plunge taken. response gotten", create_bot_res)
        userid = create_bot_res.user.id

        self.cursor.execute("""Insert into bots (
                                id, name, type, settings, state, run_count, is_paused, created_at
                            ) VALUES (?, ?, ?, ?, ?, ?, ?, time('now'))""",
                            (userid, bot_name, bot_type, bot_settings, "{}", 0, start_paused))
        self.conn.commit()

        return userid

    async def load_all_bots(self):
        """loads all bots from the database and schedules them."""
        bots = self.get_bots()
        for bot in bots:
            await self.load_bot(bot)

    async def load_bot(self, bot_desc):
        """loads a bot given its description"""
        if bot_desc["is_paused"] is True:
            return

        bot_module = __import__("bots." + bot_desc["type"])
        bot_module = getattr(bot_module, bot_desc["type"])
        bot_class = getattr(bot_module, bot_desc["type"])

        # instantiate the bot class.
        bot = bot_class()
        await bot._hidden_init_(bot_desc["id"], bot_desc["name"], bot_desc["settings"],
                                self, self.indicator_manager, self.market_messenger)
        self.bot_instances[bot.id] = bot
        asyncio.ensure_future(bot.run())

    async def pause_bot(self, bot_id):
        """pause a bot given the bot_id"""
        if bot_id in self.bot_instances:
            self.bot_instances[bot_id].pause()
        else:
            raise Exception("Invalid bot_id!")

    def get_bots(self):
        """get_bots returns a list of all bot instances"""
        self.cursor.execute("SELECT id, name, type, settings, run_count, is_paused, created_at from bots")
        bot_rows = self.cursor.fetchall()

        bots = []
        for bot_row in bot_rows:
            bots.append({
                "id": bot_row[0],
                "name": bot_row[1],
                "type": bot_row[2],
                "settings": json.loads(bot_row[3]),
                "run_count": bot_row[4],
                "is_paused": bot_row[5],
                "created_at": bot_row[6],
            })

        return bots
