# 🚀 Orbition Network Smart Auto Mining Bot

**Orbition Bot by DropsterMind**

A Python-based automation script for managing multiple Orbition Network accounts. The bot automatically checks your mining status, starts mining if idle, and intelligently sleeps until the next account is ready to mine. It now also supports proxy rotation to keep your accounts safe.

## ✨ Features

- **Multi-Account Support:** Easily manage multiple accounts by adding tokens to a text file.
- **Proxy Support (NEW):** Map different proxies to your accounts to prevent IP bans. Includes an interactive menu to run with or without proxies.
- **Smart Auto-Sleep:** Calculates the exact time when the next account finishes mining and puts the bot to sleep to save resources.
- **Colorful & Informative Logs:** Real-time, easy-to-read terminal output with status updates, point balances, and countdown timers.
- **24/7 Automation:** Just run it and leave it. The bot will handle the 24-hour mining cycles automatically.

## 🛠️ Prerequisites

- **Python 3.7+** installed on your system.
- **Requests Library**: For making API requests.

## 📦 Installation & Setup

1. **Clone the Repository**

```bash
git clone https://github.com/DropsterMind/OrbitionBot.git
cd OrbitionBot
```

2. **Install the required Python library** by running:
   ```bash
   pip install requests
          or
   pip3 install requests	  
   ```
3. **Set up your accounts:**
   - Create or edit `akun.txt` in the project directory.
   - Add your Orbition Network Bearer tokens to `akun.txt` (one token per line). 
   - *Note: Do not include the word "Bearer ", just the token string (e.g., `eyJhbGciOi...`).*

4. **Set up your proxies (Optional):**
   - Create a file named `proxies.txt` in the same directory.
   - Add your proxies (one per line). Format: `http://user:pass@ip:port` or `http://ip:port`.
   - The bot will cycle through the list if you have more accounts than proxies.

## 🚀 Usage

Run the script using Python:

```bash
python bot.py
or
python3 bot.py
```

Upon starting, the bot will prompt you to choose the mode:
```text
Select Mode:
1. With Proxy
2. Without Proxy
Enter your choice (1/2):
```
Choose your preferred mode, and the bot will start parsing the accounts, checking their current mining status, starting mining if necessary, and going to sleep until the next cycle.
