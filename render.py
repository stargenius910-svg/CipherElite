import asyncio
import logging
import os

from aiohttp import web
from telethon import TelegramClient
from telethon.sessions import StringSession
from config.config import Config
from utils.thanos import thanos_protect
from startup.startup import start_bot
from core.console import ColourFormatter

logging.basicConfig(
    level=logging.WARNING,
    handlers=[logging.StreamHandler()]
)
logging.getLogger().handlers[0].setFormatter(
    ColourFormatter("cipherelite")()
)

eliteses = thanos_protect(Config.STRING_SESSION)

client = TelegramClient(
    StringSession(eliteses),
    Config.API_ID,
    Config.API_HASH
)


async def health(request):
    return web.Response(text="OK")


async def start_http_server():
    app = web.Application()
    app.router.add_get("/", health)
    app.router.add_get("/health", health)

    runner = web.AppRunner(app)
    await runner.setup()

    port = int(os.environ.get("PORT", "10000"))
    site = web.TCPSite(runner, "0.0.0.0", port)

    await site.start()
    return runner


async def main():
    runner = await start_http_server()

    try:
        await start_bot(client)
    finally:
        await runner.cleanup()


if __name__ == "__main__":
    with client:
        client.loop.run_until_complete(main())
