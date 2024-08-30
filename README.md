# Synapse Username Checker

A versatile tool to verify the availability of usernames on Discord.

*(Note: This is the **official** repository. Please avoid downloading or using versions from unverified sources that claim to be this tool with modifications. Always check the repository's date and commit history before proceeding.)*

---

## Features

- **Targeted Username Verification**: Checks the availability of a specified list of usernames.
- **Username Generation & Validation**: Automatically generates usernames of a specified length (e.g., 4-character usernames) and checks their availability.
- **Multi-Token Support**: Seamlessly manage and utilize multiple tokens for checks.
- **Webhook Integration**: Supports webhooks for real-time notifications.
- **Highly Customizable**: Adapt the tool's settings and configurations to suit your needs.

> For critical information and FAQs, please refer to the <a href=#important-notes>important notes</a> section below before using this tool or raising any issues.

# How to use
- Have <a href="https://www.python.org/">Python</a> installed.
- First clone the repository or <a href="https://github.com/giiovi/synapse-name-checker/archive/refs/tags/discord.zip">download it as .zip</a>
- Install the required libraries, by running : ```pip install -r requirements.txt``` or `pip3 install -r requirements.txt` in your command line.
- Open `config.ini`
- Paste your account's token in front of the equal symbol `TOKEN`
- Configure Synapse as how you'd like (`config.ini`)
- Run `checker.py` 

> - For adding a specific list of usernames, create a file named `usernames.txt` in the same running directory as `checker.py` and list your usernames there, separating them by a new line.
> - For adding multiple tokens, open `config.ini` and enable `MULTI-TOKEN` by making it `true` and paste your tokens inside `tokens.txt` separating them by a new line.


# Notes
#### Disclaimer: I'm not responsible for/of any damage/results/returns/suspension made/resulted with/by this tool. It is your will to run, and once ran, it's your responsibility.

- This repository is licensed for **NON-COMMERCIAL USE ONLY.** For more details, please refer to the [LICENSE](https://github.com/giiovi/synapse-name-checker/blob/main/LICENSE).


- I **demand** my credits to the code wherever it's used.
- Spamming Discord's API is against TOS, You may get your account suspended/rate limited and I am not responsible.
- You need to get your Discord's account's authorization token and paste it inside the variable: `TOKEN` . On how to do that check these following steps: https://www.androidauthority.com/get-discord-token-3149920/
- Make sure to have a decent delay or you may get your account disabled. 


