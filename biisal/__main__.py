# (c) @biisal
# (c) adars h-goel
import os
import sys
import glob
import asyncio
import logging
import importlib
from pathlib import Path
from pyrogram import idle
from .bot import StreamBot
from .vars import Var
from aiohttp import web
from .server import web_server
from .utils.keepalive import ping_server
from biisal.bot.clients import initialize_clients

import time

# Set timezone
if "TZ" not in os.environ:
    os.environ["TZ"] = "UTC"
    try:
        time.tzset()
    except Exception:
        pass  # Koyeb/Heroku me tzset fail ho sakta hai

LOGO = """
 ____ ___ ___ ____    _    _     
| __ )_ _|_ _/ ___|  / \  | |    
|  _ \| | | |\___ \ / _ \ | |    
| |_) | | | | ___) / ___ \| |___ 
|____/___|___|____/_/   \_\_____|"""

# Logging config
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logging.getLogger("aiohttp").setLevel(logging.ERROR)
logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.getLogger("aiohttp.web").setLevel(logging.ERROR)

ppath = "biisal/bot/plugins/*.py"
files = glob.glob(ppath)

loop = asyncio.get_event_loop()

async def start_services():
    print('\n------------------- Initializing Telegram Bot -------------------')

    # Start bot (no_updates argument removed to fix TypeError)
    await StreamBot.start()
    await asyncio.sleep(1)  # first API call se pehle chhota wait

    bot_info = await StreamBot.get_me()
    StreamBot.username = bot_info.username
    print("------------------------------ DONE ------------------------------\n")

    print("---------------------- Initializing Clients ----------------------")
    await initialize_clients()
    print("------------------------------ DONE ------------------------------\n")

    print('--------------------------- Importing Plugins ---------------------------')
    for name in files:
        with open(name) as a:
            patt = Path(a.name)
            plugin_name = patt.stem.replace(".py", "")
            plugins_dir = Path(f"biisal/bot/plugins/{plugin_name}.py")
            import_path = ".plugins.{}".format(plugin_name)
            spec = importlib.util.spec_from_file_location(import_path, plugins_dir)
            load = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(load)
            sys.modules["biisal.bot.plugins." + plugin_name] = load
            print("Imported => " + plugin_name)
    
    if Var.ON_HEROKU:
        print("------------------ Starting Keep Alive Service ------------------\n")
        asyncio.create_task(ping_server())

    print('-------------------- Initializing Web Server -------------------------')
    app = web.AppRunner(await web_server())
    await app.setup()
    bind_address = "0.0.0.0" if Var.ON_HEROKU else Var.BIND_ADRESS
    await web.TCPSite(app, bind_address, Var.PORT).start()
    print('----------------------------- DONE -----------------------------\n')

    print('----------------------- Service Started -----------------------')
    print(f"Bot =>> {bot_info.first_name}")
    print(f"Server IP =>> {bind_address}:{Var.PORT}")
    print(f"Owner =>> {Var.OWNER_USERNAME}")
    if Var.ON_HEROKU:
        print(f"App running on =>> {Var.FQDN}")
    print('---------------------------------------------------------------')
    print(LOGO)
    
    await idle()

if __name__ == '__main__':
    try:
        loop.run_until_complete(start_services())
    except KeyboardInterrupt:
        logging.info('----------------------- Service Stopped -----------------------')
