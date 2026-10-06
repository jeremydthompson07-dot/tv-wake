import asyncio
import json
from pathlib import Path
from unicodedata import name

from androidtvremote2 import AndroidTVRemote, InvalidAuth


BASE_DIR = Path(__file__).resolve().parent
CONFIG_FILE = BASE_DIR / "config.json"
CERT_FILE = BASE_DIR / "cert.pem"
KEY_FILE = BASE_DIR / "key.pem"


def load_config():
    if not CONFIG_FILE.exists():
        raise FileNotFoundError(
            "config.json was not found.\n"
            "Copy config.example.json to config.json and enter your TV's IP address."
        )

    with CONFIG_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


async def main():
    config = load_config()

    tv_ip = config["tv_ip"]
    client_name = config["client_name"]

    remote = AndroidTVRemote(
        client_name,
        str(CERT_FILE.resolve()),
        str(KEY_FILE.resolve()),
        tv_ip,
    )

    await remote.async_generate_cert_if_missing()

    print(f"Looking for Android TV at {tv_ip}...")

    name, mac = await remote.async_get_name_and_mac()
    print(f"Found TV: {name} ({mac})")

    await remote.async_start_pairing()

    print()
    print("A pairing code should now appear on the TV.")
    code = input("Enter pairing code: ").strip()

    try:
        await remote.async_finish_pairing(code)
    except InvalidAuth:
        print("Pairing failed. Check the code and try again.")
        return

    print()
    print("Pairing successful.")
    print(f"Certificate saved to: {CERT_FILE.name}")
    print(f"Private key saved to: {KEY_FILE.name}")


if __name__ == "__main__":
    asyncio.run(main())