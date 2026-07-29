import requests
import time
import json
from datetime import datetime, timedelta
import sys
import os

# Mengaktifkan ANSI colors untuk Windows CMD
os.system('color')

# ================= CONFIGURATION =================
AKUN_FILE = 'akun.txt'
PROXIES_FILE = 'proxies.txt'
COOLDOWN_HOURS = 24
DELAY_BETWEEN_ACCOUNTS = 3  # Delay in seconds between accounts
DELAY_BETWEEN_QUESTS = 2    # Delay in seconds between completing quests
# Terminal Colors
C_GREEN = '\033[92m'
C_YELLOW = '\033[93m'
C_RED = '\033[91m'
C_CYAN = '\033[96m'
C_RESET = '\033[0m'
# =================================================

def get_headers(token):
    return {
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.9",
        "authorization": f"Bearer {token}",
        "content-type": "application/json",
        "origin": "https://airdrop.orbition.network",
        "referer": "https://airdrop.orbition.network/",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36"
    }

def get_user_info(token, proxy_dict=None):
    url = "https://api-airdrop.orbition.network/api/me"
    try:
        res = requests.get(url, headers=get_headers(token), proxies=proxy_dict, timeout=15)
        if res.status_code == 200:
            return res.json().get('user', {})
        else:
            print(f"{C_RED}    [!] Server Error {res.status_code}: {res.text}{C_RESET}")
    except Exception as e:
        print(f"{C_RED}    [!] Error Fetch User: {e}{C_RESET}")
    return None

def start_mining(token, proxy_dict=None):
    url = "https://api-airdrop.orbition.network/api/mining/start"
    try:
        res = requests.post(url, headers=get_headers(token), json={}, proxies=proxy_dict, timeout=15)
        if res.status_code == 200:
            return res.json()
        else:
            print(f"{C_RED}    [!] Start Mining Error {res.status_code}: {res.text}{C_RESET}")
    except Exception as e:
        print(f"{C_RED}    [!] Error Start Mining: {e}{C_RESET}")
    return None

def get_quests(token, proxy_dict=None):
    url = "https://api-airdrop.orbition.network/api/quests"
    try:
        res = requests.get(url, headers=get_headers(token), proxies=proxy_dict, timeout=15)
        if res.status_code == 200:
            return res.json().get('quests', [])
    except Exception as e:
        print(f"{C_RED}    [!] Error Fetching Quests: {e}{C_RESET}")
    return []

def verify_quest(token, quest_id, proxy_dict=None):
    url = "https://api-airdrop.orbition.network/api/quests/verify"
    payload = {"questId": quest_id}
    try:
        res = requests.post(url, headers=get_headers(token), json=payload, proxies=proxy_dict, timeout=15)
        if res.status_code == 200:
            return res.json()
    except Exception as e:
        print(f"{C_RED}    [!] Error Verifying Quest {quest_id}: {e}{C_RESET}")
    return None

def format_time(ms_timestamp):
    if ms_timestamp == 0:
        return "Never started"
    dt = datetime.fromtimestamp(ms_timestamp / 1000.0)
    return dt.strftime('%Y-%m-%d %H:%M:%S')

def main():
    print(f"{C_CYAN}===================================================={C_RESET}")
    print(f"{C_CYAN}           Orbition Bot by DropsterMind             {C_RESET}")
    print(f"{C_CYAN}    🚀 ORBITION NETWORK SMART AUTO MINING BOT 🚀    {C_RESET}")
    print(f"{C_CYAN}===================================================={C_RESET}\n")

    # Menu Pilihan Proxy
    print(f"{C_YELLOW}Select Mode:{C_RESET}")
    print("1. With Proxy")
    print("2. Without Proxy")
    
    use_proxy = False
    while True:
        choice = input(f"{C_YELLOW}Enter your choice (1/2): {C_RESET}")
        if choice == '1':
            use_proxy = True
            break
        elif choice == '2':
            use_proxy = False
            break
        else:
            print(f"{C_RED}[!] Invalid choice. Please enter 1 or 2.{C_RESET}")

    # Membaca file token
    try:
        with open(AKUN_FILE, 'r') as file:
            tokens = [line.strip().replace("Bearer ", "").replace("bearer ", "") for line in file if line.strip()]
    except FileNotFoundError:
        print(f"{C_RED}[!] File {AKUN_FILE} not found!{C_RESET}")
        sys.exit()
        
    if not tokens:
        print(f"{C_RED}[!] No tokens found in {AKUN_FILE}{C_RESET}")
        sys.exit()

    # Membaca file proxy
    proxies_list = []
    if use_proxy:
        try:
            with open(PROXIES_FILE, 'r') as file:
                proxies_list = [line.strip() for line in file if line.strip()]
            if not proxies_list:
                print(f"{C_RED}[!] {PROXIES_FILE} is empty. Running without proxy.{C_RESET}")
                use_proxy = False
            else:
                print(f"{C_GREEN}[*] Loaded {len(proxies_list)} proxies.{C_RESET}")
        except FileNotFoundError:
            print(f"{C_RED}[!] {PROXIES_FILE} not found. Running without proxy.{C_RESET}")
            use_proxy = False

    while True:
        print(f"\n{C_YELLOW}[*] Starting check for {len(tokens)} accounts at {datetime.now().strftime('%H:%M:%S')}...{C_RESET}\n")
        
        fastest_wait_time = None

        for index, token in enumerate(tokens):
            account_num = index + 1
            
            proxy_dict = None
            if use_proxy and proxies_list:
                proxy_url = proxies_list[index % len(proxies_list)]
                proxy_dict = {
                    "http": proxy_url,
                    "https": proxy_url
                }
                print(f"{C_CYAN}[Account {account_num}] | Using Proxy: {proxy_url}{C_RESET}")
            else:
                print(f"{C_CYAN}[Account {account_num}] | Direct Connection{C_RESET}")

            # 1. Fetch User Data
            user = get_user_info(token, proxy_dict)
            if not user:
                print(f"{C_RED}    -> Failed to fetch data, skipping...{C_RESET}")
                print("-" * 50)
                continue

            wallet = user.get('wallet_address', 'Unknown')
            wallet_short = f"{wallet[:6]}...{wallet[-4:]}" if len(wallet) > 10 else wallet
            points = user.get('total_points', 0)
            mining_start_time = user.get('mining_start', 0)
            mining_claimed = user.get('mining_claimed', 0)
            server_now = user.get('server_now', int(time.time() * 1000))
            
            # Parsing Completed Quests
            completed_quests_raw = user.get('completed_quests', "[]")
            completed_quests = []
            try:
                # Menangani format "[1,2,3]" menjadi list python
                if completed_quests_raw:
                    completed_quests = json.loads(completed_quests_raw)
            except:
                pass

            print(f"    -> Wallet: {wallet_short} | Points: {points}")

            # 2. Auto Complete Quests
            available_quests = get_quests(token, proxy_dict)
            if available_quests:
                quests_to_do = [q for q in available_quests if q.get('id') not in completed_quests and q.get('is_active') == 1]
                
                if quests_to_do:
                    print(f"{C_YELLOW}    -> Found {len(quests_to_do)} uncompleted tasks. Processing...{C_RESET}")
                    for q in quests_to_do:
                        q_id = q.get('id')
                        q_title = q.get('title')
                        
                        v_res = verify_quest(token, q_id, proxy_dict)
                        if v_res and v_res.get('success'):
                            reward = v_res.get('reward', 0)
                            print(f"{C_GREEN}       [+] Task '{q_title}' Done! Reward: {reward} Points{C_RESET}")
                        else:
                            print(f"{C_RED}       [-] Failed Task '{q_title}'{C_RESET}")
                        
                        time.sleep(DELAY_BETWEEN_QUESTS)
                else:
                    print(f"{C_GREEN}    -> All tasks are already completed!{C_RESET}")

            # 3. Mining Logic
            cooldown_ms = COOLDOWN_HOURS * 60 * 60 * 1000
            end_time_ms = mining_start_time + cooldown_ms
            remaining_time_ms = end_time_ms - server_now

            if mining_start_time == 0 or mining_claimed == 1 or remaining_time_ms <= 0:
                print(f"{C_YELLOW}    -> Status: Ready to Mine! Attempting to start...{C_RESET}")
                start_res = start_mining(token, proxy_dict)
                
                if start_res and start_res.get('status') == 'mining_started':
                    new_start = start_res.get('mining_start', server_now)
                    new_completion_time = format_time(new_start + cooldown_ms)
                    print(f"{C_GREEN}    -> Success: Mining started! Completes at: {new_completion_time}{C_RESET}")
                    remaining_time_ms = cooldown_ms
                else:
                    print(f"{C_RED}    -> Failed: Server rejected start mining request.{C_RESET}")
                    remaining_time_ms = 5 * 60 * 1000 
            else:
                remaining_time_sec = int(remaining_time_ms / 1000)
                hours, remainder = divmod(remaining_time_sec, 3600)
                minutes, seconds = divmod(remainder, 60)
                completion_time = format_time(end_time_ms)
                
                print(f"{C_YELLOW}    -> Status: Currently Mining ⏳{C_RESET}")
                print(f"{C_YELLOW}    -> Time Remaining: {hours}h {minutes}m {seconds}s (Ends at: {completion_time}){C_RESET}")

            if remaining_time_ms > 0:
                if fastest_wait_time is None or remaining_time_ms < fastest_wait_time:
                    fastest_wait_time = remaining_time_ms

            print("-" * 50)
            time.sleep(DELAY_BETWEEN_ACCOUNTS)

        if fastest_wait_time:
            sleep_seconds = int(fastest_wait_time / 1000) + 30
            sleep_hours, sleep_remainder = divmod(sleep_seconds, 3600)
            sleep_minutes, sleep_seconds_rem = divmod(sleep_remainder, 60)
            
            wake_up_time = (datetime.now() + timedelta(seconds=sleep_seconds)).strftime('%H:%M:%S')
            
            print(f"\n{C_CYAN}[*] All accounts processed.{C_RESET}")
            print(f"{C_CYAN}[*] Bot sleeping for {sleep_hours}h {sleep_minutes}m {sleep_seconds_rem}s. Next check at {wake_up_time}...{C_RESET}\n")
            
            time.sleep(sleep_seconds)
        else:
            print(f"\n{C_RED}[!] No valid wait time found, sleeping for 5 minutes...{C_RESET}")
            time.sleep(300)

if __name__ == "__main__":
    main()
