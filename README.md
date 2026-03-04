# 🎮 Kahoot Bot Flooder — Termux

> Flood any Kahoot lobby with bots from your Android phone using Termux. Bots join automatically, answer questions randomly, and stay connected for the entire game.

---

## 📋 Table of Contents

- [Features](#-features)
- [Requirements](#-requirements)
- [Installation](#-installation)
- [Usage](#-usage)
- [How It Works](#-how-it-works)
- [Troubleshooting](#-troubleshooting)
- [Disclaimer](#-disclaimer)

---

## ✨ Features

- 🤖 Spawns up to **50 bots** simultaneously
- 🎲 Bots **answer questions randomly** with human-like delays
- 🏷️ **Custom name prefix** for all bots (e.g. `Bot_A3K2`, `Bot_X9P1`)
- ⚡ **Async & parallel** — all bots run at the same time, not one by one
- 📱 Designed specifically for **Termux on Android**
- 🔄 Auto-installs missing dependencies on first run
- 🔇 Silently handles duplicate names and disconnects

---

## 📦 Requirements

| Requirement | Version |
|-------------|---------|
| Android | 8.0+ |
| Termux | Latest (F-Droid recommended) |
| Python | 3.8+ |
| kahoot (PyPI) | Latest |

---

## 🛠️ Installation

### 1. Install Termux
Download **Termux from F-Droid** (not the Play Store — that version is outdated):
👉 https://f-droid.org/packages/com.termux/

### 2. Set up Python in Termux
Open Termux and run:
```bash
pkg update && pkg upgrade
pkg install python
```

### 3. Install the Python dependency
```bash
pip install kahoot --break-system-packages
```

> ⚠️ The `--break-system-packages` flag is **required** on Termux's Python — without it, pip will refuse to install.

### 4. Download the bot script
Either download `kahoot_bot.py` directly or create it manually:
```bash
nano kahoot_bot.py
# paste the script contents, then Ctrl+X → Y → Enter to save
```

---

## 🚀 Usage

```bash
python kahoot_bot.py
```

You'll be prompted for 3 things:

```
Enter Game PIN:          → The PIN shown on the Kahoot screen
Number of bots (1-50):   → How many bots to flood with
Bot name prefix:         → e.g. "Bot", "Player", "Ghost" (default: Bot)
```

### Example session:
```
=========================================
      KAHOOT BOT FLOODER  —  Termux
=========================================
  [!] For educational purposes only

Enter Game PIN: 123456
Number of bots (1-50): 20
Bot name prefix (default: Bot): Ghost

[*] Starting 20 bots with prefix 'Ghost'...
    Press Ctrl+C to stop.

[*] Launching 20 bots into game 123456...

  ✓ Ghost_A3K2 joined!
  ✓ Ghost_X9P1 joined!
  ✓ Ghost_7YON joined!
  ...

[*] Bots active. Press Ctrl+C to stop.
```

Press **Ctrl+C** at any time to disconnect all bots and exit.

---

## ⚙️ How It Works

```
┌─────────────────────────────────────────────┐
│                  kahoot_bot.py               │
│                                              │
│  1. Takes game PIN + bot count from user     │
│                                              │
│  2. Spawns N async tasks in parallel         │
│     (staggered 0.4s apart to avoid bans)     │
│                                              │
│  3. Each bot:                                │
│     ├── Connects via KahootClient            │
│     ├── Joins lobby with random name         │
│     ├── Listens for QuestionStartPacket      │
│     └── Answers with random choice (0-3)     │
│         after a human-like delay (0.3–2.5s)  │
│                                              │
│  4. All bots stay alive until Ctrl+C         │
└─────────────────────────────────────────────┘
```

The bot uses the [`kahoot`](https://pypi.org/project/kahoot/) PyPI package (`KahootClient`) which correctly handles Kahoot's current WebSocket protocol, token challenge decoding, and CometD handshake — all automatically.

---

## 🔧 Troubleshooting

| Error | Fix |
|-------|-----|
| `module 'kahoot' has no attribute 'Client'` | Reinstall: `pip install --upgrade kahoot --break-system-packages` |
| `HTTP 400 WebSocket rejected` | Kahoot updated their API — make sure `kahoot` package is up to date |
| `Game PIN not found` | Make sure the Kahoot lobby is **open** before running the bot |
| `Duplicate name` | Normal — the bot silently retries with a different name suffix |
| Bots join but get kicked | Kahoot may have bot detection enabled on that game |
| `pip: command not found` | Run `pkg install python` first |

---

## ⚠️ Disclaimer

This tool is intended **for educational purposes only** — e.g. testing your own Kahoot games, studying async Python, or learning about WebSocket protocols.

- ✅ Use on **your own** Kahoot games
- ✅ Use for **learning and testing**
- ❌ Do **not** use to disrupt other people's games or classes
- ❌ Do **not** use in violation of [Kahoot's Terms of Service](https://kahoot.com/terms-conditions/)

The author takes no responsibility for misuse of this tool.

---

## 📄 License

MIT — free to use, modify, and distribute.

---

<p align="center">Made with 🐍 Python + 📱 Termux</p>
