import random
import string
import requests
import os
import time
import json
from colorama import Fore, Back, Style, init
import datetime
from configparser import ConfigParser
import sys

# Initialize colorama
init(autoreset=True)

# Constants and configurations
VERSION_INFO = "Author: giovi Synapse 1.0"
GITHUB_LINK = "https://github.com/giiovi"
DIR_PATH = os.path.dirname(os.path.abspath(__file__))
CONFIG = ConfigParser()
CONFIG.read(os.path.join(DIR_PATH, "config.ini"))
TOKEN_FILE = os.path.join(DIR_PATH, "tokens.txt")
API_USER_URL = "https://discord.com/api/v9/users/@me"
API_CHECK_URL = "https://discord.com/api/v9/users/@me/pomelo-attempt"
AVAILABLE_USERNAMES = []
AVAILABLE_USERNAMES_FILE = os.path.join(DIR_PATH, "available_usernames.txt")
USERNAME_SAMPLE_CHARS = "_."
DEFAULT_DELAY = CONFIG.getfloat("config", "default_delay")

# Enhanced ASCII Art for the UI header with colors
HEADER_ART = f"""
{Fore.MAGENTA} ░▒▓███████▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓███████▓▒░ ░▒▓██████▓▒░░▒▓███████▓▒░ ░▒▓███████▓▒░▒▓████████▓▒░ 
{Fore.MAGENTA}░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░        
{Fore.MAGENTA}░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░        
{Fore.MAGENTA} ░▒▓██████▓▒░ ░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓████████▓▒░▒▓███████▓▒░ ░▒▓██████▓▒░░▒▓██████▓▒░   
{Fore.MAGENTA}       ░▒▓█▓▒░  ░▒▓█▓▒░   ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░             ░▒▓█▓▒░▒▓█▓▒░        
{Fore.MAGENTA}       ░▒▓█▓▒░  ░▒▓█▓▒░   ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░             ░▒▓█▓▒░▒▓█▓▒░        
{Fore.MAGENTA}░▒▓███████▓▒░   ░▒▓█▓▒░   ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓███████▓▒░░▒▓████████▓▒░ 
"""

# Utility functions
def load_tokens(token_path):
    with open(token_path, 'r') as file:
        return file.read().splitlines()

def get_request_headers(token):
    return {
        "Content-Type": "Application/json",
        "Origin": "https://discord.com/",
        "Authorization": token
    }

def validate_configuration():
    token = CONFIG.get("sys", "TOKEN")
    multi_token = CONFIG.getboolean("sys", "MULTI_TOKEN")
    if not token and not multi_token:
        print(f"{Fore.RED}No token found. You must paste your token inside the 'config.ini' file.")
        sys.exit()
    elif multi_token and not load_tokens(TOKEN_FILE):
        print(f"{Fore.RED}No tokens found in 'tokens.txt'.")
        sys.exit()

def setup_config():
    global USERNAME_CHARSET, NUMERIC_CHARSET, PUNCTUATION_CHARSET, WEBHOOK_ENABLED
    string_enabled = CONFIG.getboolean("config", "string")
    digits_enabled = CONFIG.getboolean("config", "digits")
    punctuation_enabled = CONFIG.getboolean("config", "punctuation")
    WEBHOOK_URL = CONFIG.get("sys", "WEBHOOK_URL")
    
    USERNAME_CHARSET = string.ascii_lowercase if string_enabled else ""
    NUMERIC_CHARSET = string.digits if digits_enabled else ""
    PUNCTUATION_CHARSET = USERNAME_SAMPLE_CHARS if punctuation_enabled else ""

    WEBHOOK_ENABLED = bool(WEBHOOK_URL)

    # Ensure at least one character set is enabled
    if not (string_enabled or digits_enabled or punctuation_enabled):
        USERNAME_CHARSET = string.ascii_lowercase
        NUMERIC_CHARSET = string.digits
        PUNCTUATION_CHARSET = USERNAME_SAMPLE_CHARS

def generate_username(length):
    charset = USERNAME_CHARSET + NUMERIC_CHARSET + PUNCTUATION_CHARSET
    return ''.join(random.choices(charset, k=length))

def save_username(username):
    with open(AVAILABLE_USERNAMES_FILE, "a") as file:
        file.write(f"{username}\n")

def send_webhook_notification(username):
    if not WEBHOOK_ENABLED:
        return

    webhook = DiscordWebhook(url=CONFIG.get("sys", "WEBHOOK_URL"))
    webhook.post(
        username="Synapse",
        avatar_url="https://avatars.githubusercontent.com/u/70852615?v=4",
        embeds=[{
            "title": f"Username '{username}' is available!",
            "timestamp": datetime.datetime.utcnow().isoformat(),
            "color": 16768000
        }]
    )

def validate_username_availability(username, token_index=0):
    token = CONFIG.get("sys", "TOKEN") if not CONFIG.getboolean("sys", "MULTI_TOKEN") else load_tokens(TOKEN_FILE)[token_index]
    headers = get_request_headers(token)
    response = requests.post(API_CHECK_URL, headers=headers, json={"username": username})
    
    if response.status_code == 429:  # Rate limit hit
        retry_after = response.json().get("retry_after", 1)
        print(f"{Fore.RED}Rate limit hit. Retrying after {retry_after}s.")
        time.sleep(retry_after)
        return validate_username_availability(username, token_index=(token_index + 1) % len(load_tokens(TOKEN_FILE)))

    result = response.json()
    if not result.get("taken"):
        print(f"{Fore.GREEN}Username '{username}' is available.")
        save_username(username)
        send_webhook_notification(username)
        AVAILABLE_USERNAMES.append(username)
    else:
        print(f"{Fore.RED}Username '{username}' is taken.")

def process_usernames(usernames, option=1):
    for username in usernames:
        validate_username_availability(username)
        time.sleep(DEFAULT_DELAY)

def main():
    # Display header art
    print(HEADER_ART)
    print(f"{Fore.GREEN}Welcome to Synapse Username Checker")
    print(f"{Fore.LIGHTBLUE_EX}Connected as {requests.get(API_USER_URL, headers=get_request_headers(CONFIG.get('sys', 'TOKEN'))).json().get('username')}")
    print(f"{Fore.BLUE}1 - Generate and check usernames")
    print(f"{Fore.BLUE}2 - Check a specific list of usernames")
    
    validate_configuration()
    setup_config()

    choice = input(f"{Fore.YELLOW}Choose an option: ").strip()
    if choice == "1":
        length = int(input(f"{Fore.LIGHTCYAN_EX}Enter the number of letters in the username: ").strip())
        count = int(input(f"{Fore.LIGHTCYAN_EX}Enter the number of usernames to generate: ").strip())
        usernames = [generate_username(length) for _ in range(count)]
        process_usernames(usernames, option=1)
    elif choice == "2":
        list_path = os.path.join(DIR_PATH, "usernames.txt")
        with open(list_path, 'r') as file:
            usernames = [line.strip() for line in file]
            process_usernames(usernames, option=2)
    else:
        print(f"{Fore.RED}Invalid option selected.")
        main()

class DiscordWebhook:
    def __init__(self, url):
        self.url = url

    def post(self, **kwargs):
        response = requests.post(self.url, json=kwargs)
        if not response.ok:
            print(f"{Fore.RED}Failed to send webhook: {response.status_code}")

if __name__ == "__main__":
    main()
