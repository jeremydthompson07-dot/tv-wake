import asyncio
import json

from androidtvremote2 import AndroidTVRemote
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
CONFIG_FILE = BASE_DIR / "config.json"
CERT_FILE = BASE_DIR / "cert.pem"
KEY_FILE = BASE_DIR / "key.pem"

with CONFIG_FILE.open("r", encoding="utf-8") as file:
    config = json.load(file)

TV_IP = config["tv_ip"]
CLIENT_NAME = config["client_name"]


async def main():
    remote = AndroidTVRemote(
        CLIENT_NAME,
        str(CERT_FILE.resolve()),
        str(KEY_FILE.resolve()),
        TV_IP,
    )

    await remote.async_connect()
    print("Connected to TV.")

    # Give the remote a moment to receive the TV's current state.
    await asyncio.sleep(1)

    print(f"TV power state: {remote.is_on}")

    if remote.is_on:
        print("TV is already on. Doing nothing.")
    else:
        print("TV is off/asleep. Waking it...")
        remote.send_key_command("POWER")
        print("Wake command sent.")

    await asyncio.sleep(1)
    remote.disconnect()


if __name__ == "__main__":
    asyncio.run(main())