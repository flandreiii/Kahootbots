#!/usr/bin/env python3
"""
Kahoot Bot Flooder for Termux
Install: pip install kahoot --break-system-packages
Usage:   python kahoot_bot.py
"""

import asyncio
import random
import string
import sys


def install_deps():
    import subprocess
    print("[*] Installing dependencies...")
    subprocess.run(
        [sys.executable, "-m", "pip", "install", "kahoot", "--break-system-packages"],
        check=True
    )
    print("[*] Done.\n")


try:
    from kahoot import KahootClient
    from kahoot.packets.server.question_start import QuestionStartPacket
except ImportError:
    install_deps()
    from kahoot import KahootClient
    from kahoot.packets.server.question_start import QuestionStartPacket


def random_name(prefix="Bot"):
    suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    return f"{prefix}_{suffix}"


async def run_bot(pin: int, name: str, delay: float = 0.0):
    await asyncio.sleep(delay)
    try:
        client = KahootClient()

        async def on_question(packet: QuestionStartPacket):
            try:
                num = getattr(packet, "number_of_choices", 4) or 4
                await asyncio.sleep(random.uniform(0.3, 2.5))
                choice = random.randint(0, int(num) - 1)
                # find and call the answer method
                if hasattr(client, "answer"):
                    await client.answer(choice)
                elif hasattr(client, "send_answer"):
                    await client.send_answer(choice)
            except Exception:
                pass

        client.on("question_start", on_question)
        await client.join_game(game_pin=pin, username=name)
        print(f"  ✓ {name} joined!")

    except Exception as e:
        msg = str(e).lower()
        if "not found" in msg or "no game" in msg or "invalid" in msg:
            print(f"[!] Game PIN {pin} not found or lobby isn't open.")
        elif "duplicate" not in msg and "taken" not in msg:
            print(f"  ✗ {name}: {e}")


async def flood(pin: int, count: int, prefix: str):
    print(f"\n[*] Launching {count} bots into game {pin}...\n")
    names = [random_name(prefix) for _ in range(count)]
    tasks = [run_bot(pin, name, delay=i * 0.4) for i, name in enumerate(names)]
    await asyncio.gather(*tasks, return_exceptions=True)
    print(f"\n[*] Bots active. Press Ctrl+C to stop.")
    try:
        await asyncio.sleep(9999)
    except (asyncio.CancelledError, KeyboardInterrupt):
        pass


def main():
    print("=" * 45)
    print("      KAHOOT BOT FLOODER  —  Termux")
    print("=" * 45)
    print("  [!] For educational purposes only\n")

    raw_pin = input("Enter Game PIN: ").strip()
    if not raw_pin.isdigit():
        print("[!] Invalid PIN.")
        return
    pin = int(raw_pin)

    try:
        count = int(input("Number of bots (1-50): ").strip())
        count = max(1, min(50, count))
    except ValueError:
        count = 5

    prefix = input("Bot name prefix (default: Bot): ").strip() or "Bot"

    print(f"\n[*] Starting {count} bots with prefix '{prefix}'...")
    print("    Press Ctrl+C to stop.\n")

    try:
        asyncio.run(flood(pin, count, prefix))
    except KeyboardInterrupt:
        print("\n[*] Stopped.")


if __name__ == "__main__":
    main()
